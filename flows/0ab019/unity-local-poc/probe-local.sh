#!/usr/bin/env bash
set -euo pipefail

# Read-only, bounded HTTP asset witness after the capped unit starts.
base=http://127.0.0.1:38081
systemctl --user show unity-local-poc-0ab019.service \
  -p ActiveState -p MemoryMax -p CPUQuotaPerSecUSec
for route in / /app.js /unity.css \
  /unity-local-poc/browser-signal-codec/pkg/browser_signal_codec.js \
  /unity-local-poc/browser-signal-codec/pkg/browser_signal_codec_bg.wasm; do
  curl --fail --silent --show-error --max-time 3 --output /dev/null \
    --write-out "$route %{http_code} %{content_type}\n" "$base$route"
done
