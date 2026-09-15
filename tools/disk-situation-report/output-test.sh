#!/bin/sh
set -eu
out=$(cargo run --quiet --manifest-path tools/disk-situation-report/Cargo.toml -- 'Request.{ prometheus alice }')
expected='Disk report for prometheus user alice
store: 7168 bytes
  /nix/store/bob 4096 bytes retained_by=bob
  /nix/store/example 1024 bytes retained_by=alice
  /nix/store/shared 2048 bytes retained_by=alice,bob
build: 2048 bytes
  /build/example 2048 bytes
cache: 4096 bytes
  /cache/example 4096 bytes
repositories: 8192 bytes
  /repos/example 8192 bytes state=dirty
oversized: 1050624 bytes
  /data/example.bin 1048576 bytes
  /nix/store/shared 2048 bytes
oversized paths overlap store paths: /nix/store/shared
requested user retention bytes: 3072
Suggestions for alice'"'"'s agent: review authorized retention, preserve boot/rollback/unknown data, and measure before/after; no deletion performed.'
if [ "$out" != "$expected" ]; then
  printf '%s\n' 'unexpected report output:' >&2
  printf '%s\n' "$out" >&2
  exit 1
fi
for request in 'Request.{ zeus alice }' 'Request.{ prometheus bob }'; do
  if cargo run --quiet --manifest-path tools/disk-situation-report/Cargo.toml -- "$request" >/dev/null 2>&1; then
    printf '%s\n' "expected request rejection: $request" >&2
    exit 1
  fi
done
