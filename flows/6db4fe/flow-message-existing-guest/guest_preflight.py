#!/usr/bin/env python3
"""Fail-closed, read-only preflight for Prometheus's existing vm-testing guest.

This program deliberately has no start, stop, build, login, or test command.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REMOTE = "root@prometheus.goldragon.criome"
HOST = "prometheus"
UNIT = "microvm@vm-testing.service"
GUEST_DIR = "/var/lib/microvms/vm-testing"
SSH = (
    "ssh",
    "-o", "BatchMode=yes",
    "-o", "StrictHostKeyChecking=yes",
    "-o", "HostKeyAlias=prometheus.goldragon.criome",
    "-o", "ForwardAgent=no",
    "-o", "ClearAllForwardings=yes",
    "-o", "ConnectTimeout=8",
    REMOTE,
)
REVISION = re.compile(r"^[0-9a-f]{40}$")
GRAPH_KEYS = (
    "flow_revision",
    "message_revision",
    "signal_flow_revision",
    "signal_message_revision",
    "meta_signal_flow_revision",
    "meta_signal_message_revision",
)


class GuardError(RuntimeError):
    pass


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise GuardError("unsupported fixture schema")
    if data.get("remote_host") != HOST or data.get("guest_unit") != UNIT:
        raise GuardError("fixture must target the one reserved Prometheus guest")
    if data.get("guest_directory") != GUEST_DIR:
        raise GuardError("fixture guest directory mismatch")
    graph = data.get("candidate_graph")
    if not isinstance(graph, dict) or set(graph) != set(GRAPH_KEYS):
        raise GuardError("candidate graph fields differ from the fixture contract")
    return data


def blocked_reasons(data: dict) -> list[str]:
    graph = data["candidate_graph"]
    missing = [key for key in GRAPH_KEYS if not isinstance(graph[key], str) or not REVISION.fullmatch(graph[key])]
    for key in ("generated_contract_receipt", "remote_check_receipt", "field_parity_receipt"):
        if not data.get(key):
            missing.append(key)
    return missing


def remote(argv: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    # argv is chosen only from this file's constants, never manifest text.
    return subprocess.run((*SSH, *argv), capture_output=True, text=True, timeout=15, check=False)


def guarded_snapshot(run=remote) -> dict:
    """Verify exact remote identity before any unit/image/process state read."""
    identity = run(("hostname", "--short"))
    if identity.returncode != 0 or identity.stdout.strip() != HOST:
        raise GuardError("remote host identity unverified; no guest state read")

    commands = {
        "unit": ("systemctl", "show", UNIT, "-p", "LoadState", "-p", "ActiveState", "-p", "SubState", "-p", "ConditionResult", "--no-pager"),
        "current": ("readlink", "-f", f"{GUEST_DIR}/current"),
        "toplevel": ("readlink", "-f", f"{GUEST_DIR}/toplevel"),
        "runner": ("test", "-x", f"{GUEST_DIR}/current/bin/microvm-run"),
        "root_image": ("test", "-e", f"{GUEST_DIR}/root.img"),
        "booted_link": ("test", "-e", f"{GUEST_DIR}/booted"),
    }
    result = {"host": HOST, "unit_name": UNIT, "guest_directory": GUEST_DIR}
    for name, argv in commands.items():
        answer = run(argv)
        if name in ("runner", "root_image", "booted_link"):
            result[name] = answer.returncode == 0
        elif answer.returncode == 0:
            result[name] = answer.stdout.strip() or None
        else:
            result[name] = None
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "inspect"))
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("manifest.example.json"))
    args = parser.parse_args()
    try:
        data = load_manifest(args.manifest)
        missing = blocked_reasons(data)
        readiness = {"declared_inputs_present": not missing, "trial_authorized": False, "missing": missing}
        if args.action == "plan":
            print(json.dumps({"guest": UNIT, **readiness}, indent=2))
        else:
            print(json.dumps({"snapshot": guarded_snapshot(), **readiness}, indent=2))
        return 0
    except (GuardError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"preflight refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
