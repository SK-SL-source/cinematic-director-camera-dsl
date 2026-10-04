# -*- coding: utf-8 -*-
"""Minimal YAML-subset loader (stdlib only). Uses PyYAML instead when it is installed.

Supported subset (the registry and schema files are written in it):
  - block mappings (`key: value`, `key:` + indented block), 2-space indentation
  - block sequences (`- value`, `- key: value` with continuation lines)
  - flow sequences `[a, "b, c", 3]` and flow mappings `{k: v, k2: v2}` of scalars
  - scalars: "double quoted" (JSON escapes), 'single quoted', plain (null/true/false/int/float/str)
  - block scalars `|` (literal) and `>` (folded)
  - comments: a line starting with '#', or ' #' outside quotes
Anything outside this subset raises YamlLiteError with the line number.
"""
import json
import re

__all__ = ["load", "load_file", "YamlLiteError", "BACKEND"]


class YamlLiteError(ValueError):
    pass


def _strip_comment(line):
    out, q, esc = [], None, False
    for i, ch in enumerate(line):
        if q:
            out.append(ch)
            if esc:
                esc = False
            elif q == '"' and ch == "\\":
                esc = True
            elif ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


_INT = re.compile(r"^[-+]?\d+$")
_FLOAT = re.compile(r"^[-+]?(\d+\.\d*|\.\d+|\d+)([eE][-+]?\d+)?$")


def _scalar(tok, ln):
    t = tok.strip()
    if t == "":
        return None
    if t[0] == '"':
        if not t.endswith('"') or len(t) < 2:
            raise YamlLiteError(f"line {ln}: unterminated double-quoted string")
        return json.loads(t)
    if t[0] == "'":
        if not t.endswith("'") or len(t) < 2:
            raise YamlLiteError(f"line {ln}: unterminated single-quoted string")
        return t[1:-1].replace("''", "'")
    if t[0] == "[":
        return _flow_seq(t, ln)
    if t[0] == "{":
        return _flow_map(t, ln)
    low = t.lower()
    if low in ("null", "~"):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    if _INT.match(t):
        return int(t)
    if _FLOAT.match(t) and any(c in t for c in ".eE"):
        return float(t)
    return t


def _split_flow(body, ln):
    items, cur, q, depth = [], [], None, 0
    for ch in body:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
            cur.append(ch)
        elif ch in "[{":
            depth += 1
            cur.append(ch)
        elif ch in "]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            items.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if q:
        raise YamlLiteError(f"line {ln}: unterminated quote in flow collection")
    tail = "".join(cur)
    if tail.strip():
        items.append(tail)
    return items


def _flow_seq(t, ln):
    if not t.endswith("]"):
        raise YamlLiteError(f"line {ln}: unterminated flow sequence")
    return [_scalar(x, ln) for x in _split_flow(t[1:-1], ln)]


def _flow_map(t, ln):
    if not t.endswith("}"):
        raise YamlLiteError(f"line {ln}: unterminated flow mapping")
    out = {}
    for item in _split_flow(t[1:-1], ln):
        k, sep, v = _split_key(item.strip(), ln)
        if not sep:
            raise YamlLiteError(f"line {ln}: flow mapping item without ':'")
        out[k] = _scalar(v, ln)
    return out


def _split_key(s, ln):
    """Split 'key: value' respecting a quoted key. Returns (key, found, rest)."""
    if s[:1] in "\"'":
        q = s[0]
        end = s.find(q, 1)
        while q == '"' and end > 0 and s[end - 1] == "\\":
            end = s.find(q, end + 1)
        if end < 0:
            raise YamlLiteError(f"line {ln}: unterminated quoted key")
        key = _scalar(s[:end + 1], ln)
        rest = s[end + 1:]
        if rest.startswith(":") and (len(rest) == 1 or rest[1] == " "):
            return key, True, rest[1:].strip()
        return None, False, s
    m = re.match(r"^([^\s:\[\]{},][^:]*?):(\s+|$)(.*)$", s)
    if not m:
        return None, False, s
    return m.group(1).strip(), True, m.group(3)


class _Lines:
    def __init__(self, text):
        self.rows = []
        for n, raw in enumerate(text.splitlines(), 1):
            if "\t" in raw[: len(raw) - len(raw.lstrip())]:
                raise YamlLiteError(f"line {n}: tab indentation is not allowed")
            self.rows.append((n, raw))
        self.i = 0

    def peek(self):
        """Next significant (non-blank, non-comment) row: (lineno, indent, content)."""
        while self.i < len(self.rows):
            n, raw = self.rows[self.i]
            c = _strip_comment(raw)
            if c.strip() == "" or c.strip() == "---":
                self.i += 1
                continue
            return n, len(c) - len(c.lstrip(" ")), c.strip()
        return None

    def take(self):
        r = self.peek()
        self.i += 1
        return r


def _block_scalar(lines, parent_indent, style):
    buf, ind = [], None
    while lines.i < len(lines.rows):
        n, raw = lines.rows[lines.i]
        if raw.strip() == "":
            buf.append("")
            lines.i += 1
            continue
        cur = len(raw) - len(raw.lstrip(" "))
        if cur <= parent_indent:
            break
        if ind is None:
            ind = cur
        buf.append(raw[ind:] if cur >= ind else raw.lstrip(" "))
        lines.i += 1
    while buf and buf[-1] == "":
        buf.pop()
    if style == "|":
        return "\n".join(buf) + "\n"
    return " ".join(x for x in buf if x) + "\n"


def _value_after_key(lines, rest, indent, ln):
    rest = rest.strip()
    if rest in ("|", ">", "|-", ">-"):
        v = _block_scalar(lines, indent, rest[0])
        return v.rstrip("\n") if rest.endswith("-") else v
    if rest == "":
        nxt = lines.peek()
        if nxt is None or nxt[1] <= indent:
            if nxt is not None and nxt[1] == indent and nxt[2].startswith("- "):
                return _parse_block(lines, indent)
            return None
        return _parse_block(lines, nxt[1])
    return _scalar(rest, ln)


def _parse_block(lines, indent):
    first = lines.peek()
    if first is None:
        return None
    if first[2].startswith("- ") or first[2] == "-":
        return _parse_seq(lines, indent)
    return _parse_map(lines, indent)


def _parse_map(lines, indent):
    out = {}
    while True:
        r = lines.peek()
        if r is None or r[1] < indent:
            return out
        n, ind, content = r
        if ind > indent:
            raise YamlLiteError(f"line {n}: unexpected indentation")
        if content.startswith("- "):
            return out
        lines.take()
        key, found, rest = _split_key(content, n)
        if not found:
            raise YamlLiteError(f"line {n}: expected 'key: value', got {content[:40]!r}")
        if key in out:
            raise YamlLiteError(f"line {n}: duplicate key {key!r}")
        out[key] = _value_after_key(lines, rest, indent, n)


def _parse_seq(lines, indent):
    out = []
    while True:
        r = lines.peek()
        if r is None or r[1] < indent:
            return out
        n, ind, content = r
        if ind != indent or not (content.startswith("- ") or content == "-"):
            if ind > indent:
                raise YamlLiteError(f"line {n}: unexpected indentation in sequence")
            return out
        lines.take()
        item = content[1:].strip()
        if item == "":
            nxt = lines.peek()
            out.append(_parse_block(lines, nxt[1]) if nxt and nxt[1] > indent else None)
            continue
        key, found, rest = _split_key(item, n)
        if found:
            child_indent = indent + 2
            m = {key: _value_after_key(lines, rest, child_indent, n)}
            nxt = lines.peek()
            if nxt is not None and nxt[1] == child_indent and not nxt[2].startswith("- "):
                more = _parse_map(lines, child_indent)
                for k, v in more.items():
                    if k in m:
                        raise YamlLiteError(f"line {n}: duplicate key {k!r}")
                    m[k] = v
            out.append(m)
        else:
            out.append(_scalar(item, n))


def _lite_load(text):
    lines = _Lines(text)
    first = lines.peek()
    if first is None:
        return None
    if first[1] != 0:
        raise YamlLiteError(f"line {first[0]}: document must start at column 0")
    data = _parse_block(lines, 0)
    rest = lines.peek()
    if rest is not None:
        raise YamlLiteError(f"line {rest[0]}: could not parse (check indentation)")
    return data


try:  # prefer the real parser when it exists
    import yaml as _pyyaml  # type: ignore

    def load(text):
        return _pyyaml.safe_load(text)

    BACKEND = "pyyaml"
except Exception:  # pragma: no cover - depends on environment
    load = _lite_load
    BACKEND = "yaml_lite"

lite_load = _lite_load


def load_file(path):
    with open(path, encoding="utf-8") as fh:
        return load(fh.read())


if __name__ == "__main__":
    import sys
    sample = """
# comment
a: 1
b: "x: y # not a comment"
c: [L, R, "a, b"]
d:
  e: true
  f: {x: 1, y: two}
g:
  - one
  - k: v
    k2: [1, 2]
  - "quoted"
h: |
  line1
  line2
i: plain text with: colon inside
"""
    got = _lite_load(sample)
    want = {"a": 1, "b": "x: y # not a comment", "c": ["L", "R", "a, b"],
            "d": {"e": True, "f": {"x": 1, "y": "two"}},
            "g": ["one", {"k": "v", "k2": [1, 2]}, "quoted"], "h": "line1\nline2\n",
            "i": "plain text with: colon inside"}
    ok = got == want
    print("yaml_lite self-test:", "PASS" if ok else f"FAIL\n{got}")
    sys.exit(0 if ok else 1)
