#!/bin/sh
set -eu
out=$(cargo run --quiet --manifest-path tools/disk-situation-report/Cargo.toml -- 'Request.{ prometheus alice }')
printf '%s\n' "$out" | grep -F 'store: 3072 bytes'
printf '%s\n' "$out" | grep -F '/repos/example 8192 bytes state=dirty'
printf '%s\n' "$out" | grep -F 'user retention reference bytes: 5120'
if cargo run --quiet --manifest-path tools/disk-situation-report/Cargo.toml -- 'Request.{ zeus alice }' >/dev/null 2>&1; then exit 1; fi
