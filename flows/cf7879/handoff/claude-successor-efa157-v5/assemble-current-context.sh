#!/usr/bin/env bash
set -euo pipefail

package_dir="$(cd "$(dirname "$0")" && pwd)"
efa_root="/home/li/wt/github.com/LiGoldragon/primary/claude-successor-840e42-bootstrap-local/.claude/worktrees/claude-successor-840e42"
cf_report="/home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery/flows/cf7879/reports/to-efa157.md"
curriculum="/home/li/wt/github.com/LiGoldragon/Curriculum/efa157-branches"
primary_root="/home/li/primary"
current="$package_dir/current"

rm -rf "$current"
install -d "$current/efa157/vision" "$current/cf7879" "$current/spirit" "$current/intent" "$current/skills"
cp "$efa_root/flows/efa157/log.md" "$current/efa157/log.md"
cp "$efa_root/flows/efa157/reports/ordersToCodex-2026-09-16.md" "$current/efa157/ordersToCodex-2026-09-16.md"
cp "$efa_root/flows/efa157/vision/"*.md "$current/efa157/vision/"
cp "$cf_report" "$current/cf7879/to-efa157.md"
cp "$primary_root/vision-raw/spirit.md" "$current/spirit/spirit.md"
cp "$primary_root/Intent/"*.md "$current/intent/"
for skill in main-flow spirit behavior psyche correction vocabulary testing psyche-interraction subflow edit-coordination claude-harness prompt-crafting; do
  cp "$curriculum/skills/$skill.md" "$current/skills/$skill.md"
done

{
  printf '%s\n\n' '# Primary Claude successor system prompt — efa157 v5'
  printf '%s\n\n' 'Identity and boundary: you succeed efa157 at depth 1. Flow 840e42 is historical only. The current authority is the current source set below; do not execute an instruction, launch shape, session identity, thread name, or order from the v4 archival block. A copied skill body is package content, not a native skill-loader receipt.'
  printf '%s\n\n' 'The living ordered the Cloud Nexus DNS proof of concept for xmpp.goldragon.criome.net first. Use gopass only through a program invocation; do not read credentials. Secondary owns deployment. The existing launch own-scope defect is unresolved and must not be repaired without a supported receipt.'
  printf '%s\n\n' '## Current verified source set'
  for source in "$current/spirit/spirit.md" "$current/intent/"*.md "$current/skills/"*.md "$current/efa157/log.md" "$current/efa157/ordersToCodex-2026-09-16.md" "$current/efa157/vision/"*.md "$current/cf7879/to-efa157.md"; do
    printf '\n## Source: %s\n\n' "${source#$current/}"
    cat "$source"
    printf '\n'
  done
  printf '%s\n\n' '## Historical v4 archive — not active instructions'
  cat "$package_dir/v4-archive-system-prompt.md"
} > "$package_dir/system-prompt.md"

(cd "$current" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$package_dir/current-source-sha256sums.txt"
(cd "$current" && sha256sum -c "$package_dir/current-source-sha256sums.txt" --quiet)
(cd "$package_dir" && sha256sum README.md system-prompt.md user-prompt.md v4-source-manifest.tsv v4-archive-system-prompt.md launch-successor.sh assemble-current-context.sh current-source-sha256sums.txt > artifact-sha256sums.txt)
(cd "$package_dir" && sha256sum -c artifact-sha256sums.txt --quiet)
