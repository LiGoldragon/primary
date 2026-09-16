#!/usr/bin/env bash
set -euo pipefail

package_dir="$(cd "$(dirname "$0")" && pwd)"
system_prompt="$package_dir/system-prompt.md"
user_prompt="$package_dir/user-prompt.md"
max_user_bytes=102400
max_record_bytes=262144

(cd "$package_dir" && sha256sum -c artifact-sha256sums.txt)
user_bytes="$(wc -c < "$user_prompt")"
test "$user_bytes" -lt "$max_user_bytes"

args=(
  claude
  --bg
  --name primary-claude-successor-efa157
  --remote-control primary-claude-successor-efa157
  --model fable
  --system-prompt-file "$system_prompt"
  -- "$(<"$user_prompt")"
)
record_bytes="$(printf '%s\0' "${args[@]}" | wc -c)"
test "$record_bytes" -lt "$max_record_bytes"

if [[ "${1:-}" != "--launch" ]]; then
  printf 'Dry run only: %s args, argv bytes=%s, model=fable, stdin=/dev/null.\n' "${#args[@]}" "$record_bytes"
  exit 0
fi
test "${2:-}" = "--cwd"
test -n "${3:-}"
test -d "$3"
case "$3" in "$package_dir"/*) ;; *) exit 64 ;; esac
cd "$3"

exec env -u NO_COLOR TERM=xterm-ghostty "${args[@]}" </dev/null
