#!/usr/bin/env python3
"""Launch a fresh Field Astra successor from a verified complete handoff.

The handoff is read locally into Codex's first positional user prompt.  It is
not a request for the model to read a path, and this program never copies a
native session or credential state.
"""
import argparse
import hashlib
import os
from pathlib import Path

CANDIDATE_WRAPPER = "/nix/store/nmr4py6p0kwwza41l0gkhsa13k9971jb-codex-next-flow-client/bin/codex-next-flow-client"
CANDIDATE_REMOTE = "unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock"

CONTEXT = """You are a fresh independent Field Astra successor, never a native-session transfer. You must use gpt-6-astra at medium effort through the explicit candidate remote supplied by this launcher. The old Field Astra d5 seat remains open until you have completed a meaningful reconciliation, created your own main flow lane/log/index, received correct Herdr/Messenger registration, and Field verifies all of those facts. Do not close, retire, or otherwise alter the predecessor; do not restart any Codex service; do not copy credentials or native state; do not rename V2; do not start another migration before establishing your own identity.\n\nThe living's current direction is to migrate everybody to the new Codex harness and repair Prometheus Wi-Fi AP internet access. Field Sol 1bc255 is the sole AP host executor; do not duplicate its host probes or repairs. Current candidate-migrated Codex seats are Field Sol f69847, Mind Luna 098f27, Mind Astra d32329, and Mind Sol 5104af. The old Next endpoint presently retains the Field Astra d5 and Field Sol 1bc255 seats while their active work ends. The candidate uses /home/li/.codex-next-8mkkxq293hk2 and its app-server-control socket. Candidate Bubblewrap is technically unqualified; do not call that an approval hold or a repair. The required documented launch permissions are sandbox danger-full-access and approval never, and an actual task command must be observed before declaring the new environment usable.\n\nThe complete final handoff follows verbatim after this delimiter. Reconcile it into a concrete next-action plan, preserve its unresolved source obligations, and establish your own flow lane before registration.\n\n===== COMPLETE FINAL HANDOFF =====\n"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handoff", required=True, type=Path)
    ap.add_argument("--sha256", required=True)
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    handoff = args.handoff.read_text(encoding="utf-8")
    actual = hashlib.sha256(handoff.encode()).hexdigest()
    if actual != args.sha256:
        raise SystemExit(f"handoff sha256 mismatch: expected {args.sha256}, got {actual}")
    prompt = CONTEXT + handoff
    argv = [CANDIDATE_WRAPPER, "-m", "gpt-6-astra", "-c", 'model_reasoning_effort="medium"', "-s", "danger-full-access", "-a", "never", "--remote", CANDIDATE_REMOTE, "-C", "/home/li/primary", prompt]
    if args.verify:
        print(f"handoff_bytes={len(handoff.encode())} sha256={actual} argv={len(argv)} prompt_bytes={len(prompt.encode())}")
        return
    os.execv(CANDIDATE_WRAPPER, argv)

if __name__ == "__main__":
    main()
