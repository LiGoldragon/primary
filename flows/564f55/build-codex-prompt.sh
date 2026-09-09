#!/usr/bin/env bash
# build-codex-prompt — assemble the Codex realization prompt: the directive,
# then the full text of every Vision and Intent file it rests on, inlined so
# the flow starts with the vision in context rather than fetching it.
#
#   build-codex-prompt <directive-file> <output-file>

set -euo pipefail

directive=${1:?usage: build-codex-prompt <directive-file> <output-file>}
out=${2:?usage: build-codex-prompt <directive-file> <output-file>}

visionFiles=(
  /home/li/primary/Vision/protos.md
  /home/li/primary/Vision/datom.md
  /home/li/primary/Vision/ethos.md
  /home/li/primary/Vision/signal.md
  /home/li/primary/Vision/sema.md
  /home/li/primary/Vision/nexus.md
  /home/li/primary/Intent/anatomy.md
  /home/li/primary/Intent/conversion.md
  /home/li/primary/Intent/context.md
  /home/li/primary/Intent/mandatoryTraits.md
)

for f in "$directive" "${visionFiles[@]}"; do
  [ -r "$f" ] || { echo "not readable: $f" >&2; exit 2; }
done

{
  cat "$directive"
  printf '\n----\n\nThe Vision and Intent named above follow in full, each under its\nabsolute path. This is the text as landed; read no stale copy of it.\n'
  for f in "${visionFiles[@]}"; do
    printf '\n===== %s =====\n\n' "$f"
    cat "$f"
  done
} > "$out"
