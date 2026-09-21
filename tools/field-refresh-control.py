#!/usr/bin/env python3
"""Validate the temporary Field refresh route-control Datom contract."""

from __future__ import annotations

import sys

from messaging import Group, Text, Variant, actualize


def validate(value: str, expected_head: str, expected_marker: str) -> None:
    if expected_head not in {"Probe", "Ack"}:
        raise ValueError("unknown Field refresh control variant")
    root = actualize(value)
    if not isinstance(root, Variant) or root.head != expected_head:
        raise ValueError("Field refresh control variant differs")
    body = root.body
    if not isinstance(body, Group) or body.kind != "{" or len(body.values) != 1:
        raise ValueError("Field refresh control must carry one positional marker")
    marker = body.values[0]
    if not isinstance(marker, Text) or marker.value != expected_marker:
        raise ValueError("Field refresh control marker differs")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: field-refresh-control.py Probe|Ack MARKER DATOM")
    try:
        validate(sys.argv[3], sys.argv[1], sys.argv[2])
    except (ValueError, SyntaxError) as error:
        print(f"invalid Field refresh control: {error}", file=sys.stderr)
        raise SystemExit(2)
    print("Field refresh control valid")
