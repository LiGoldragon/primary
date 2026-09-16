#!/usr/bin/env sh
set -eu

execute=false
if [ "${1:-}" = "--execute" ]; then
  execute=true
fi

prompt='Spawn exactly one child using the default built-in type. Have it return JSON stating whether it received PROBE_DEVELOPER_SENTINEL and PROBE_SKILL_BODY_SENTINEL as developer text, a native skill body, a path, or an actual system role. Do not read files or make changes. Wait once.'
developer='PROBE_DEVELOPER_SENTINEL=dev-7e52. Synthetic skill body supplied as developer text, not a native skill load or a path: <skill name=ProbeSkill>PROBE_SKILL_BODY_SENTINEL=body-c18b.</skill>'

set -- codex exec --json -m gpt-5.6-luna -s read-only -C /tmp --skip-git-repo-check \
  -c "developer_instructions=\"$developer\"" "$prompt"

if [ "$execute" = false ]; then
  printf '%s\n' "This would run:" "$*"
  exit 0
fi
exec "$@"
