#!/usr/bin/env bash
set -euo pipefail

# Run only inside the documented user-systemd unit with combined CPU/memory
# ceilings. This script never compiles, polls transcripts, or starts providers.
: "${UNITY_POC_PACKAGE:?set the remote-built host package path}"
: "${UNITY_POC_ASSETS:?set the remote-built assets path}"
[[ -x "$UNITY_POC_PACKAGE/bin/unity-poc-mentci-nexus" ]]
[[ -x "$UNITY_POC_PACKAGE/bin/unity-poc-persona-seat" ]]
[[ -s "$UNITY_POC_ASSETS/unity-local-poc/browser-signal-codec/pkg/browser_signal_codec_bg.wasm" ]]

state_root="${XDG_STATE_HOME:-/home/li/.local/state}"
attempt_dir="$state_root/unity-local-poc-attempts"
[[ ! -L "$attempt_dir" ]]
install -d -m 0700 "$attempt_dir"
runtime_dir=$(mktemp -d "${XDG_RUNTIME_DIR:-/tmp}/unity-local-poc.XXXXXXXX")

export UNITY_POC_BIND=127.0.0.1:38081
export UNITY_POC_PERSONA_SOCKET="$runtime_dir/persona.sock"
export UNITY_POC_FLOW_ROOT="$UNITY_POC_ASSETS"
export UNITY_POC_ATTEMPT_DIR="$attempt_dir"
# This reviewed seat lives in the named Herdr session. A user-systemd unit
# does not inherit the interactive pane's HERDR_SESSION environment.
export HERDR_SESSION=messaging-build

"$UNITY_POC_PACKAGE/bin/unity-poc-mentci-nexus" &
mentci_pid=$!
export UNITY_POC_MENTCI_PID="$mentci_pid"
"$UNITY_POC_PACKAGE/bin/unity-poc-persona-seat" &
persona_pid=$!

printf 'Unity localhost POC: Mentci PID %s, Persona PID %s, socket %s\n' \
  "$mentci_pid" "$persona_pid" "$UNITY_POC_PERSONA_SOCKET"
trap 'kill "$mentci_pid" "$persona_pid" 2>/dev/null || true' EXIT
wait -n "$mentci_pid" "$persona_pid"
