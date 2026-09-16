#!/usr/bin/env bash
set -euo pipefail

package_dir="$(cd "$(dirname "$0")" && pwd)"
system_prompt="$package_dir/system-prompt.md"
user_prompt="$package_dir/user-prompt.md"

sha256sum -c "$package_dir/artifact-sha256sums.txt"

args=(
  claude
  --bg
  --name primary-claude-successor-efa157
  --remote-control primary-claude-successor-efa157
  --system-prompt-file "$system_prompt"
  -- "$(<"$user_prompt")"
)

if [[ "${1:-}" != "--launch" ]]; then
  printf 'Dry run only. Would execute with %s structured arguments; stdin is /dev/null.\n' "${#args[@]}"
  exit 0
fi

exec "${args[@]}" </dev/null
