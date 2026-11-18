#!/usr/bin/env python3
"""Proposal 2 finite admission boundary. No runtime action occurs without a complete manifest."""
import json
import pathlib
import sys

REQUIRED = {
    "candidate_commit", "flow_package", "curriculum_package", "place_compiler",
    "herdr", "raw_codex", "host_path", "bash", "python", "systemd_run",
    "systemctl", "provider_hashes", "admission_review_hash", "driver_hash",
    "unit_name", "root", "event_observer_api", "native_prompts_hash",
}
EXPECTED_COMMIT = "fe5a6930871707a7086c9a647867a519734220ef"

class AdmissionError(Exception):
    pass

def validate(doc):
    if not isinstance(doc, dict):
        raise AdmissionError("manifest must be a JSON object")
    missing = sorted(REQUIRED - doc.keys())
    if missing:
        raise AdmissionError("unobserved required inputs: " + ", ".join(missing))
    if doc["candidate_commit"] != EXPECTED_COMMIT:
        raise AdmissionError("candidate commit differs from reviewed source pin")
    for key in REQUIRED - {"provider_hashes"}:
        value = doc[key]
        if not isinstance(value, str) or not value.strip() or "PENDING" in value.upper():
            raise AdmissionError(f"unobserved or invalid {key}")
    hashes = doc["provider_hashes"]
    if not isinstance(hashes, dict) or not hashes:
        raise AdmissionError("provider_hashes must bind every executable/provider")
    for name, digest in hashes.items():
        if not isinstance(name, str) or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise AdmissionError("provider hash malformed")
    raise AdmissionError("admission manifest is structurally complete, but runtime controller stages are intentionally withheld pending independent review")

def main(argv):
    if len(argv) != 2:
        print("usage: controller.py PROVIDER-MANIFEST.json", file=sys.stderr)
        return 64
    path = pathlib.Path(argv[1])
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        validate(doc)
    except (OSError, json.JSONDecodeError, AdmissionError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 2
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
