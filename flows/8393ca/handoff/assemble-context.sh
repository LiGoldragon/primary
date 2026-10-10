#!/usr/bin/env bash
set -euo pipefail
root=/home/li/.codex/worktrees/8673/primary
output="$root/flows/8393ca/handoff/primary-field-context.md"
paths=(
  flows/8393ca/vision/operational-herdrVoiceAccess.md
  flows/108ab0/vision/operational-programmaticPromptComposition.md
  flows/108ab0/vision/operational-promptMosaicComposition.md
  flows/01a03f49/reports/codexPhoneRemoteControl.md
  Vision/flowNexus.md
  Vision/distillation.md
  Intent/context.md
)
{
  printf '# Primary Field source context\n\n'
  printf 'Assembled mechanically from the selected paths in context-manifest.md. Each block retains its source path.\n\n'
  for path in "${paths[@]}"; do
    printf '## Source: %s\n\n' "$path"
    sed -n '1,260p' "$root/$path"
    printf '\n\n'
  done
} > "$output"
