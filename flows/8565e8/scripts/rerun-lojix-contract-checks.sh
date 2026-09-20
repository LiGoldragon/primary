#!/usr/bin/env bash
set -euo pipefail
umask 077

if [[ $# -ne 1 || -z ${1:-} ]]; then
  printf 'usage: %s RUN_DIR\n' "$0" >&2
  exit 64
fi

run_dir=$1
if [[ ! -r /etc/nix/machines ]]; then
  printf 'required builder file is not readable: /etc/nix/machines\n' >&2
  exit 78
fi
mkdir -p -- "$run_dir"
if [[ -e "$run_dir/sequence.result" ]]; then
  printf 'run directory is not unique: %s\n' "$run_dir" >&2
  exit 73
fi
: > "$run_dir/sequence.result"

run_check() {
  local name=$1
  local ref=$2
  local check=$3
  local log="$run_dir/$name.log"
  local pid_file="$run_dir/$name.pid"
  local exit_file="$run_dir/$name.exit"
  local child status

  timeout --signal=TERM --kill-after=60s 7200 \
    nix build --no-link -L --builders @/etc/nix/machines \
      --option max-jobs 0 --option fallback false \
      "$ref#checks.x86_64-linux.$check" > "$log" 2>&1 &
  child=$!
  printf '%s\n' "$child" > "$pid_file"
  if wait "$child"; then
    status=0
  else
    status=$?
  fi
  printf '%s\n' "$status" > "$exit_file"
  printf '%s\t%s\n' "$name" "$status" >> "$run_dir/sequence.result"
  if (( status != 0 )); then
    return "$status"
  fi
}

signal_ref='git+file:///git/github.com/LiGoldragon/signal-lojix?rev=3f550fc278b8e14c37158036d420e7e3ed1d7c7b'
meta_ref='git+file:///git/github.com/LiGoldragon/meta-signal-lojix?rev=a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85'

run_check signal-datom "$signal_ref" test-datom-contract
run_check signal-generated "$signal_ref" test-generated-contract
run_check meta-datom "$meta_ref" test-datom-contract
run_check meta-generated "$meta_ref" test-generated-contract
