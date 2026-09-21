#!/usr/bin/env python3
"""Validate the temporary Field refresh route-control Datom contract."""

from __future__ import annotations

import datetime as dt
import sys
import uuid

from messaging import Group, Text, Variant, actualize, q, relay


def validate(value: str, expected_head: str, expected_marker: str) -> None:
    if expected_head not in {"Probe", "Ack", "Offer", "Accept", "Notice"}:
        raise ValueError("unknown Field refresh control variant")
    root = actualize(value)
    if not isinstance(root, Variant) or root.head != expected_head:
        raise ValueError("Field refresh control variant differs")
    body = root.body
    expected_arity = 2 if expected_head == "Offer" else 1
    if not isinstance(body, Group) or body.kind != "{" or len(body.values) != expected_arity:
        raise ValueError("Field refresh control has wrong positional arity")
    marker = body.values[0]
    if not isinstance(marker, Text) or marker.value != expected_marker:
        raise ValueError("Field refresh control marker differs")
    if expected_head == "Offer" and (not isinstance(body.values[1], Text) or not body.values[1].value):
        raise ValueError("Field refresh offer requires a nonempty brief path")


def probe_envelope(sender: str, seat: str, recipient: str, marker: str) -> str:
    """Build the bounded machine-origin HM probe; HM transport is not origin auth."""
    quote = f"Probe.{{ {q(marker)} }}"
    validate(quote, "Probe", marker)
    heard = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    context = (
        "Declared Field refresh control type: "
        "flows/6db4fe/field-astra-native/refresh-control.ethos. "
        "This is a machine-origin route check. Reply as a single exact Datom value "
        f"Ack.{{ {q(marker)} }} with no prose or Markdown."
    )
    result = (
        f"Machine.Relay.{{ e{uuid.uuid4().hex} {sender} {seat} {q(heard)} typed "
        f"[ {recipient} ] {q(quote)} {q(context)} }}"
    )
    parsed = relay(result)
    if parsed["quote"] != quote or parsed["recipients"] != [recipient] or parsed["context"] != context:
        raise ValueError("Field refresh probe envelope mismatch")
    return result


if __name__ == "__main__":
    try:
        if len(sys.argv) == 6 and sys.argv[1] == "build":
            print(probe_envelope(*sys.argv[2:]))
        elif len(sys.argv) == 4:
            validate(sys.argv[3], sys.argv[1], sys.argv[2])
            print("Field refresh control valid")
        else:
            raise ValueError("usage: field-refresh-control.py build SENDER SEAT RECIPIENT MARKER | Probe|Ack MARKER DATOM")
    except (ValueError, SyntaxError) as error:
        print(f"invalid Field refresh control: {error}", file=sys.stderr)
        raise SystemExit(2)
