#!/usr/bin/env bash
# PreToolUse hook: intercept Agent tool calls that would land on a bad model.
#
# "Bad alias" = sonnet, opus, fable — all resolve to 5-generation models.
# The estate runs 4.6 only (claude-sonnet-4-6, claude-opus-4-6[1m]).
#
# updatedInput.model cannot carry a full model ID (the Agent tool re-validates
# against its enum ["sonnet","opus","haiku","fable"]).  Instead, the rewrite
# mechanism sets subagent_type to "write-ordinary", whose frontmatter pins
# claude-sonnet-4-6, and removes the model field so the role definition wins.
# prompt and description are preserved; all other tool_input fields are kept.
#
# Behaviour (fail-closed — unparseable input denies):
#   1. subagent_type == "fork"
#        → deny — forks inherit parent model
#   2. model ∈ {fable, sonnet, opus}  (bad 5-gen aliases)
#        → rewrite: subagent_type → "write-ordinary", model removed
#   3. model absent AND subagent_type is NOT a local role agent
#        → rewrite (same as rule 2)
#   4. model absent AND subagent_type IS a local role agent
#        → allow untouched (role frontmatter pins the model)
#   5. model == "haiku"  (haiku-4-5 is the current haiku, acceptable)
#        → allow untouched
#   6. anything else
#        → allow untouched
#
# NOTE: rewrites change the agent's role framing and toolset to write-ordinary's.
#
# Local role agents with pinned 4.6 models (verified 2026-08-07):
#   read-trivial    → claude-haiku-4-5
#   read-ordinary   → claude-sonnet-4-6
#   read-demanding  → claude-opus-4-6[1m]
#   read-critical   → claude-opus-4-6[1m]
#   write-trivial   → claude-haiku-4-5
#   write-ordinary  → claude-sonnet-4-6
#   write-demanding → claude-opus-4-6[1m]
#   write-critical  → claude-opus-4-6[1m]

FORK_DENY_REASON="forks inherit parent model; use a role agent instead"
GARBAGE_DENY_REASON="hook received unparseable input; denying Agent call"

deny() {
  jq -n --arg r "$1" \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$r}}'
  exit 0
}

allow() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
  exit 0
}

rewrite_to_write_ordinary() {
  # Set subagent_type → "write-ordinary", remove model field, keep everything else.
  printf '%s' "$INPUT" | jq -c \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","updatedInput":(.tool_input | del(.model) | .subagent_type = "write-ordinary")}}'
  exit 0
}

# Read stdin — fail closed on any read error
INPUT=$(cat 2>/dev/null) || deny "$GARBAGE_DENY_REASON"

# Fail closed on empty or non-JSON input
if [ -z "$INPUT" ] || ! printf '%s' "$INPUT" | jq -e . >/dev/null 2>&1; then
  deny "$GARBAGE_DENY_REASON"
fi

# Extract fields (empty string when absent)
MODEL=$(printf '%s' "$INPUT" | jq -r '.tool_input.model // ""' 2>/dev/null) || deny "$GARBAGE_DENY_REASON"
SUBAGENT_TYPE=$(printf '%s' "$INPUT" | jq -r '.tool_input.subagent_type // ""' 2>/dev/null) || deny "$GARBAGE_DENY_REASON"

# Rule 1: fork → deny (one line)
[ "$SUBAGENT_TYPE" = "fork" ] && deny "$FORK_DENY_REASON"

# Rule 2: bad 5-gen alias → rewrite to write-ordinary
case "$MODEL" in
  fable|sonnet|opus) rewrite_to_write_ordinary ;;
esac

# Rule 3 / 4: model absent → role agent check
if [ -z "$MODEL" ]; then
  case "$SUBAGENT_TYPE" in
    read-trivial|read-ordinary|read-demanding|read-critical|\
    write-trivial|write-ordinary|write-demanding|write-critical)
      allow
      ;;
    *)
      rewrite_to_write_ordinary
      ;;
  esac
fi

# Rules 5 / 6: explicit non-bad-alias model (haiku, or anything else) → allow
allow
