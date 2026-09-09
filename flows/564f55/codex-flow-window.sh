#!/usr/bin/env bash
# codex-flow-window — open a ghostty window running an interactive Codex TUI
# attached to the Nix-owned remote-control app-server, seeded with a prompt.
#
#   codex-flow-window <prompt-file> <working-directory> [title-suffix]
#
# Not installed. Draft for flow 564f55.

set -euo pipefail

promptFile=${1:?usage: codex-flow-window <prompt-file> <working-directory> [title]}
workDir=${2:?usage: codex-flow-window <prompt-file> <working-directory> [title]}
title=${3:-Codex realization}

[ -r "$promptFile" ] || { echo "prompt file not readable: $promptFile" >&2; exit 2; }
[ -d "$workDir" ]    || { echo "working directory not a directory: $workDir" >&2; exit 2; }

# The daemon is Nix-owned. Never `codex remote-control start` on this host.
if ! systemctl --user is-active --quiet codex-remote-control.service; then
  echo "codex-remote-control.service is not active; start it with" >&2
  echo "  systemctl --user start codex-remote-control.service" >&2
  exit 3
fi

socket="${CODEX_HOME:-$HOME/.codex}/app-server-control/app-server-control.sock"
[ -S "$socket" ] || { echo "app-server control socket missing: $socket" >&2; exit 3; }

unit="codex-flow-window-$(date +%s%N)-$$"

exec systemd-run --user --scope --collect --quiet \
  --unit="$unit" \
  --property=CPUWeight=1000 \
  --property=IOWeight=1000 \
  --property=MemoryAccounting=yes \
  --property=MemoryLow=512M \
  --property=OOMPolicy=continue \
  ghostty \
    --gtk-single-instance=false \
    --class=criomos-codex-flow \
    --title="$title" \
    --working-directory="$workDir" \
    --wait-after-command \
    -e sh -c 'exec codex-remote --cd "$1" "$(cat "$2")"' sh "$workDir" "$promptFile"
