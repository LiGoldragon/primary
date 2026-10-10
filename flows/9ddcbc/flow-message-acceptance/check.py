#!/usr/bin/env python3
"""Check evidence from the sole existing-guest Flow/Message trial; never actuate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REV = re.compile(r"[0-9a-f]{40}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
GRAPH = (
    "flow", "message", "signal_flow", "signal_message",
    "meta_signal_flow", "meta_signal_message",
)
RECEIPTS = (
    "generated_contract", "remote_pair_build", "field_parity",
    "controller_acceptance", "native_authority",
)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def object_at(root: dict, key: str, errors: list[str]) -> dict:
    value = root.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key}: object required")
        return {}
    return value


def check(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema: expected 1")
    target = object_at(data, "target", errors)
    if target.get("host") != "prometheus" or target.get("unit") != "microvm@vm-testing.service":
        errors.append("target: only the reserved Prometheus guest is allowed")
    if target.get("controller") != "6db4fe" or target.get("guest_lock") != 4373:
        errors.append("target: controller/guest lock mismatch")
    if target.get("consumer_lock") != 3776:
        errors.append("target: consumer lock mismatch")
    if target.get("host_key_verified") is not True or target.get("node_identity_verified") is not True:
        errors.append("target: pinned endpoint and Prometheus identity must precede state reads")

    graph = object_at(data, "graph", errors)
    for key in GRAPH:
        if not isinstance(graph.get(key), str) or not REV.fullmatch(graph[key]):
            errors.append(f"graph.{key}: immutable 40-hex revision required")
    receipts = object_at(data, "receipts", errors)
    for key in RECEIPTS:
        if not nonempty(receipts.get(key)):
            errors.append(f"receipts.{key}: exact receipt required")

    artifacts = object_at(data, "artifacts", errors)
    for key in ("flow", "message"):
        item = artifacts.get(key)
        if not isinstance(item, dict):
            errors.append(f"artifacts.{key}: object required")
            continue
        for field in ("built_sha256", "running_sha256"):
            if not isinstance(item.get(field), str) or not HASH.fullmatch(item[field]):
                errors.append(f"artifacts.{key}.{field}: SHA-256 required")
        if item.get("built_sha256") != item.get("running_sha256"):
            errors.append(f"artifacts.{key}: guest executable differs from immutable build")
        if not nonempty(item.get("nix_output")) or not nonempty(item.get("guest_executable")):
            errors.append(f"artifacts.{key}: exact output and guest executable required")
    consumer = object_at(data, "consumer_parity", errors)
    for key in ("flow_package", "message_package"):
        if not nonempty(consumer.get(key)):
            errors.append(f"consumer_parity.{key}: exact Field mapping required")
    for key in ("effective_unit_digest", "effective_config_digest"):
        if not isinstance(consumer.get(key), str) or not HASH.fullmatch(consumer[key]):
            errors.append(f"consumer_parity.{key}: SHA-256 of effective materialization required")

    case = object_at(data, "case", errors)
    if case.get("recipient_count") != 1 or not nonempty(case.get("recipient")):
        errors.append("case: exactly one named disposable recipient required")
    if not nonempty(case.get("source_event_id")):
        errors.append("case.source_event_id: stable identifier required")
    if not isinstance(case.get("cli_argv"), list) or not case["cli_argv"] or not all(nonempty(x) for x in case["cli_argv"]):
        errors.append("case.cli_argv: actual compiled CLI invocation required")
    if not isinstance(case.get("contract_revision"), str) or not REV.fullmatch(case["contract_revision"]):
        errors.append("case.contract_revision: immutable compiled contract revision required")
    for key in ("typed_request_digest", "typed_response_digest"):
        if not isinstance(case.get(key), str) or not HASH.fullmatch(case[key]):
            errors.append(f"case.{key}: SHA-256 of actual typed evidence required")
    if not nonempty(case.get("transport_receipt")):
        errors.append("case.transport_receipt: typed transport receipt required")
    if case.get("transport_state") not in ("Confirmed", "Unconfirmed", "DefinitiveNonDelivery", "Ambiguous"):
        errors.append("case.transport_state: typed transport state required")
    if case.get("read_state") not in ("Unknown", "Read"):
        errors.append("case.read_state: separate read grade required")
    if case.get("read_state") == "Read" and not nonempty(case.get("read_receipt")):
        errors.append("case.read_receipt: independent target evidence required")
    if case.get("application_state") not in ("Unknown", "Accepted", "Refused", "Completed"):
        errors.append("case.application_state: separate application grade required")
    if case.get("application_state") != "Unknown" and not nonempty(case.get("application_receipt")):
        errors.append("case.application_receipt: independent target evidence required")

    mode = case.get("mode")
    authority = object_at(case, "authority", errors)
    if mode == "Raw":
        if authority.get("kind") != "RawUid" or not nonempty(authority.get("receipt")):
            errors.append("case.authority: Raw requires explicit UID authorization receipt")
        if authority.get("bound_flow") is not None or case.get("permit") is not None:
            errors.append("case: Raw cannot claim BoundFlow or carry a permit")
        if case.get("read_state") != "Unknown" or case.get("application_state") != "Unknown":
            errors.append("case: Raw transport demonstration makes no read/application probe")
    elif mode == "FlowLocked":
        if authority.get("kind") != "BoundFlow" or not nonempty(authority.get("receipt")):
            errors.append("case.authority: FlowLocked requires independently bound sender")
        binding = case.get("binding")
        if not isinstance(binding, dict) or not nonempty(binding.get("id")) or not isinstance(binding.get("generation"), int) or binding["generation"] <= 0:
            errors.append("case.binding: exact binding and positive generation required")
        if not nonempty(case.get("permit")):
            errors.append("case.permit: durable permit required")
        if case.get("raw_fallback") is not False:
            errors.append("case: FlowLocked cannot fall back to Raw")
        if case.get("transport_state") == "Confirmed" and case.get("confirmed_release") is not True:
            errors.append("case: matching confirmed transport must precede permit release")
        if case.get("transport_state") == "Confirmed" and not nonempty(case.get("target_delivery_receipt")):
            errors.append("case.target_delivery_receipt: independent one-target delivery evidence required")
        if case.get("transport_state") == "Ambiguous" and (case.get("confirmed_release") is not False or case.get("held_after_restart") is not True):
            errors.append("case: ambiguous attempt must remain held across restart")
    else:
        errors.append("case.mode: actual Raw or FlowLocked contract required")

    rollback = object_at(data, "rollback", errors)
    if not nonempty(rollback.get("preimage_id")) or not nonempty(rollback.get("schema_version")):
        errors.append("rollback: preimage and typed schema version required")
    for key in ("preimage_state_digest", "post_attempt_state_digest", "recovered_state_digest"):
        if not isinstance(rollback.get(key), str) or not HASH.fullmatch(rollback[key]):
            errors.append(f"rollback.{key}: SHA-256 of exact state required")
    if rollback.get("unit_stopped") is not True or rollback.get("qemu_gone") is not True or rollback.get("tap_gone") is not True:
        errors.append("rollback: same-unit stop and QEMU/tap exit proof required")
    for after, kept in (("post_checkpoint_events", "retained_events"), ("ambiguous_attempts", "retained_ambiguous_attempts")):
        a, b = rollback.get(after), rollback.get(kept)
        if not isinstance(a, list) or not isinstance(b, list) or not all(nonempty(x) for x in a + b):
            errors.append(f"rollback: {after}/{kept} identifier lists required")
        elif not set(a).issubset(set(b)):
            errors.append(f"rollback: {kept} loses post-checkpoint state")
    if not nonempty(rollback.get("recovery_receipt")):
        errors.append("rollback.recovery_receipt: lossless restore or forward-repair proof required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "check"))
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.evidence.read_text())
        if not isinstance(data, dict):
            raise ValueError("evidence root must be an object")
        errors = check(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"evidence refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"accepted": not errors, "missing_or_refused": errors}, indent=2))
    return 0 if args.action == "plan" or not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
