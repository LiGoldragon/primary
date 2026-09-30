#!/usr/bin/env python3
"""One-shot local launcher for the authorized Mind Astra successor."""
import hashlib
import os
import sys
from pathlib import Path

HANDOFF = Path("/tmp/mind-astra-first-prompt")
HANDOFF_SHA256 = "eedcf0fc697236faa64b2bfb5dd5ac7d543a5cd1f865f0d65f66c7e39e0eae2f"
WRAPPER = "/nix/store/nmr4py6p0kwwza41l0gkhsa13k9971jb-codex-next-flow-client/bin/codex-next-flow-client"
REMOTE = "unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock"
CONTEXT = """Machine handoff paragraph formatting is flattened only where the launcher transport requires it; the preserved raw handoff below remains whole. You are a fresh independent Mind Astra successor, not a transfer. Fable succession rules supersede any older identity implication: create a new native UUID and Flow identity. Use gpt-6-astra at medium reasoning through the explicit candidate remote endpoint. Preserve old pG/native files until your meaningful first answer and correct registration; do not touch current Field Astra pQ, Mind Sol, Field Sol, Zeus, servers, or unrelated seats. First task: boundedly reconcile the transferred Mind work and state concrete next actions; do not undertake broad host or source implementation during registration. COMPLETE RAW HANDOFF FOLLOWS:\n"""


def prompt() -> str:
    raw = HANDOFF.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != HANDOFF_SHA256:
        raise SystemExit(f"handoff checksum mismatch: {actual}")
    return CONTEXT + raw.decode("utf-8")


def argv() -> list[str]:
    return [
        WRAPPER,
        "-m", "gpt-6-astra",
        "-c", 'model_reasoning_effort="medium"',
        "--remote", REMOTE,
        "-C", "/home/li/primary",
        prompt(),
    ]


if __name__ == "__main__":
    args = argv()
    if sys.argv[1:] == ["--verify"]:
        print(f"verified handoff bytes={HANDOFF.stat().st_size} sha256={HANDOFF_SHA256} argv={len(args)} prompt_bytes={len(args[-1].encode())}")
    elif len(sys.argv) == 1:
        os.execv(args[0], args)
    else:
        raise SystemExit("usage: mind-astra-successor-launch.py [--verify]")
