#!/usr/bin/env bash
# Supervisor-owned Claude PreToolUse gate for c56100 source-only workers.
set -euo pipefail
input=$(cat)
tool_name=$(printf '%s' "$input" | jq -r '.tool_name // ""')
[ "$tool_name" = Bash ] || exit 0
command=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
deny() {
  printf '%s\n' '{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"SOURCE_ONLY_GATE: Bash denied before execution"}'
  exit 2
}
# No shell composition, redirection, expansion, substitution, escapes, or env wrappers.
[[ -n "$command" ]] || deny
[[ "$command" =~ [\;\|\&\<\>\`\\\$] ]] && deny
[[ "$command" == *$'\n'* || "$command" == *$'\r'* ]] && deny
# The worker may inspect/commit/push only with jj and acquire/observe/release its
# exact coordination lock. All other Bash, including nix, tests and formatters,
# is denied before execution.
case "$command" in
  'jj status'|'jj log'*|'jj diff'*|'jj show'*|'jj commit '*|'jj bookmark '*|'jj git push '*|'orchestrate Observe.Locks'|'orchestrate Lock.'*|'orchestrate Release.'*)
    exit 0
    ;;
  *) deny ;;
esac
