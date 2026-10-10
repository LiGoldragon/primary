#!/usr/bin/env python3
"""A generic datom reader.

Datom text carries no field names: a brace structure is a struct, a bracket
structure is a vector, a head in front of a structure is a variant carrying it,
guillemets delimit a string, and a bare run is a string or an integer according
to the position that reads it. This module parses the generic form tree; the
schema walk that gives each position its meaning lives with the type that
knows it (see index_read.py).

A line comment begins with a `;` token and runs to the end of the line. It is
not part of the datom dialect proper; it is admitted here because this index is
authored by hand and read by the living.
"""

from dataclasses import dataclass, field
from typing import List, Optional


class DatomError(Exception):
    """Raised with a typed one-line message; the caller prints it as a Refusal."""


@dataclass
class Form:
    kind: str                      # 'struct' | 'vector' | 'variant' | 'string'
    text: str = ''                 # for 'string': the content; for 'variant': the head
    items: List['Form'] = field(default_factory=list)
    payload: Optional['Form'] = None
    line: int = 0


_OPEN = {'{': 'struct', '[': 'vector'}
_CLOSE = {'}': 'struct', ']': 'vector'}


def _tokenize(text: str):
    i, line, n = 0, 1, len(text)
    while i < n:
        c = text[i]
        if c == '\n':
            line += 1
            i += 1
            continue
        if c in ' \t\r':
            i += 1
            continue
        if c == ';':
            while i < n and text[i] != '\n':
                i += 1
            continue
        if c in _OPEN or c in _CLOSE:
            yield (c, c, line)
            i += 1
            continue
        if c == '«':          # opening guillemet
            i += 1
            out = []
            while True:
                if i >= n:
                    raise DatomError(f'Error.{{ Read [ {line} ] UnterminatedString }}')
                if text[i] == '\\' and i + 1 < n:
                    out.append(text[i + 1])
                    i += 2
                    continue
                if text[i] == '»':
                    i += 1
                    break
                if text[i] == '\n':
                    line += 1
                out.append(text[i])
                i += 1
            yield ('string', ''.join(out), line)
            continue
        start = i
        while i < n and text[i] not in ' \t\r\n{}[]«»':
            i += 1
        yield ('bare', text[start:i], line)


def parse(text: str) -> Form:
    """Parse one datom value. Trailing content is an error."""
    tokens = list(_tokenize(text))
    pos = 0

    def take():
        nonlocal pos
        if pos >= len(tokens):
            raise DatomError('Error.{ Read [] UnexpectedEnd }')
        tok = tokens[pos]
        pos += 1
        return tok

    def value() -> Form:
        kind, body, line = take()
        if kind in _OPEN:
            items = []
            while True:
                if pos >= len(tokens):
                    raise DatomError(f'Error.{{ Read [ {line} ] UnclosedStructure }}')
                if tokens[pos][0] in _CLOSE:
                    close = take()
                    if _CLOSE[close[0]] != _OPEN[kind]:
                        raise DatomError(
                            f'Error.{{ Read [ {close[2]} ] MismatchedClose.{close[1]} }}')
                    break
                items.append(value())
            return Form(_OPEN[kind], items=items, line=line)
        if kind in _CLOSE:
            raise DatomError(f'Error.{{ Read [ {line} ] UnexpectedClose.{body} }}')
        if kind == 'string':
            return Form('string', text=body, line=line)
        # A bare run. A head is a bare run ending in '.', followed by its payload.
        if body.endswith('.'):
            head = body[:-1]
            if not head or not head[0].isupper():
                raise DatomError(f'Error.{{ Read [ {line} ] NotAVariantHead.{body} }}')
            return Form('variant', text=head, payload=value(), line=line)
        if '.' in body and body[0].isupper():
            head, _, rest = body.partition('.')
            inner = parse_fragment(rest, line)
            return Form('variant', text=head, payload=inner, line=line)
        if body and body[0].isupper() and _looks_like_symbol(body):
            return Form('variant', text=body, line=line)
        return Form('string', text=body, line=line)

    out = value()
    if pos != len(tokens):
        raise DatomError(f'Error.{{ Read [ {tokens[pos][2]} ] TrailingContent }}')
    return out


def parse_fragment(text: str, line: int) -> Form:
    """Parse the part of a dotted bare run that follows a variant head."""
    if not text:
        raise DatomError(f'Error.{{ Read [ {line} ] EmptyVariantPayload }}')
    if '.' in text and text[0].isupper():
        head, _, rest = text.partition('.')
        return Form('variant', text=head, payload=parse_fragment(rest, line), line=line)
    if text[0].isupper() and _looks_like_symbol(text):
        return Form('variant', text=text, line=line)
    return Form('string', text=text, line=line)


def _looks_like_symbol(body: str) -> bool:
    return all(ch.isalnum() or ch == '_' for ch in body)


def struct(form: Form, arity: int, at: str) -> List[Form]:
    if form.kind != 'struct':
        raise DatomError(f'Error.{{ Read [ {form.line} ] NotAStruct.{at} }}')
    if len(form.items) != arity:
        raise DatomError(
            f'Error.{{ Read [ {form.line} ] Arity.{{ {at} {arity} {len(form.items)} }} }}')
    return form.items


def vector(form: Form, at: str) -> List[Form]:
    if form.kind != 'vector':
        raise DatomError(f'Error.{{ Read [ {form.line} ] NotAVector.{at} }}')
    return form.items


def string(form: Form, at: str) -> str:
    if form.kind != 'string':
        raise DatomError(f'Error.{{ Read [ {form.line} ] NotAString.{at} }}')
    return form.text


def variant(form: Form, allowed, at: str) -> Form:
    if form.kind != 'variant':
        raise DatomError(f'Error.{{ Read [ {form.line} ] NotAVariant.{at} }}')
    if form.text not in allowed:
        raise DatomError(
            f'Error.{{ Read [ {form.line} ] UnknownVariant.{{ {at} {form.text} }} }}')
    return form
