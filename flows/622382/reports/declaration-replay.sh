#!/bin/sh
# Replays declaration-replay.datom through flow-meta Configure against the
# meta socket given as $1. No default: production is never implied.
set -eu
[ $# -eq 1 ] || { echo "usage: $0 <meta-socket-path>" >&2; exit 2; }
socket=$1
case $socket in
  /run/user/1001/flow/*|/run/user/1001/flow) echo "refusing production socket" >&2; exit 2;;
esac
[ -S "$socket" ] || { echo "not a socket: $socket" >&2; exit 2; }
here=$(cd "$(dirname "$0")" && pwd)
export FLOW_META_SOCKET=$socket
# A datom ends at a newline outside «», since a Purpose may hold newlines.
python3 -I - "$here/declaration-replay.datom" <<'PY'
import os, subprocess, sys
text = open(sys.argv[1], encoding="utf-8").read()
datoms, current, depth = [], "", 0
for c in text:
    if c == "«": depth += 1
    if c == "»": depth -= 1
    if c == "\n" and depth == 0:
        if current.strip(): datoms.append(current)
        current = ""
    else:
        current += c
for datom in datoms:
    head = datom.split(".", 2)[1]
    out = subprocess.run(["flow-meta", datom], capture_output=True, text=True)
    answer = out.stdout.strip()
    print(head, "->", answer[:120])
    if out.returncode != 0 or not answer.startswith("Configured."):
        print("refused or failed at", head, ":", answer[:400], out.stderr[:400], file=sys.stderr)
        sys.exit(1)
PY
