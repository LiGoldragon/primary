#!/usr/bin/env bash
# Capsule, first embodiment: a semi-sandbox for a light-model Claude Code flow
# against its own Orchestrate Nexus. Usage: capsule.sh create|start|test|enter|status|stop|teardown|all
set -euo pipefail

SCRATCH=/tmp/claude-1001/-home-li-primary/3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3/scratchpad
SB="$SCRATCH/capsule"                 # the whole sandbox lives here
SHORT=/tmp/cap3ec                     # symlink -> $SB; only to fit sun_path (108 bytes)
LIVE_CRED=/home/li/.claude/.credentials.json
NEXUS_BIN=/nix/store/6ynfv0hywpwg8gpapyfh7zn0yqzdg52z-orchestrate-0.35.0/bin/orchestrate-nexus
CLIENT_DIR=/home/li/.nix-profile/bin  # installed `orchestrate` wrapper
CLAUDE_BIN=/nix/store/qsq3lh2i05dz77dakipwy9f1fkssq1zw-claude-code-2.1.284/bin/.claude-wrapped  # unwrapped: the `claude` wrapper prepends --dangerously-skip-permissions
NEXUS_UNIT=capsule-3ec648-nexus
RUN_UNIT=capsule-3ec648-claude
MODEL="${CAPSULE_MODEL:-haiku}"

# The sandbox environment. Every per-user root is redirected; nothing is inherited.
sandbox_env=(
  HOME="$SHORT/home"
  XDG_RUNTIME_DIR="$SHORT/runtime"
  XDG_STATE_HOME="$SHORT/state"
  XDG_CONFIG_HOME="$SHORT/config"
  XDG_CACHE_HOME="$SHORT/cache"
  XDG_DATA_HOME="$SHORT/data"
  TMPDIR="$SHORT/tmp"
  PATH="$CLIENT_DIR:/run/current-system/sw/bin"
  LANG=C.UTF-8
  TERM=dumb
  USER=li
  LOGNAME=li
  SHELL=/run/current-system/sw/bin/bash
  ENABLE_CLAUDEAI_MCP_SERVERS=false   # the credential otherwise brings the account's claude.ai connectors
)

create() {
  [[ -e "$SHORT" ]] && { echo "refusing: $SHORT exists" >&2; exit 1; }
  mkdir -p "$SB"/{home/.claude,runtime,state,config,cache,data,tmp,transcripts}
  mkdir -p "$SB/work/.claude/skills/orchestrate"
  chmod 700 "$SB" "$SB/runtime" "$SB/home" "$SB/home/.claude"
  ln -s "$SB" "$SHORT"
  # The one copied file. Copied with cp, never read into the terminal.
  install -m 600 "$LIVE_CRED" "$SB/home/.claude/.credentials.json"
  # The one skill the test flow loads (generated projection, copied read-only).
  install -m 644 /home/li/primary/.claude/skills/orchestrate/SKILL.md \
    "$SB/work/.claude/skills/orchestrate/SKILL.md"
  touch "$SB/created.marker"
  echo "created $SB (alias $SHORT)"
}

start() {
  systemd-run --user --unit="$NEXUS_UNIT" --collect \
    -p MemoryMax=256M -p RuntimeMaxSec=1800 -p WorkingDirectory="$SB" \
    -p StandardOutput=append:"$SB/nexus.log" -p StandardError=append:"$SB/nexus.log" \
    /run/current-system/sw/bin/env -i "${sandbox_env[@]}" "$NEXUS_BIN"
  # wait on the socket appearing, bounded
  timeout 20 bash -c "until [[ -S '$SB/runtime/orchestrate-nexus/orchestrate.sock' ]]; do sleep 0.2; done"
  echo "nexus up: $SHORT/runtime/orchestrate-nexus/orchestrate.sock"
}

# Run a command inside the sandbox environment (e.g. `capsule.sh enter orchestrate 'Observe.Locks'`).
enter() { cd "$SB/work" && exec /run/current-system/sw/bin/env -i "${sandbox_env[@]}" "$@"; }

# test allow rule (print mode has no prompt): Skill tool and 'orchestrate ...' Bash commands only
test_run() {
  local prompt
  prompt='Load the orchestrate skill through your Skill tool. Then, using the Bash tool, run exactly:
orchestrate '"'"'Lock.{ CapsuleProbe 3ec648 [ /tmp/cap3ec/work/probe ] CapsuleRoundTrip }'"'"'
Read the integer lock ID from the Locked reply, then release it by running orchestrate '"'"'Release.<id>'"'"' with that integer. Finish by printing the two replies verbatim and nothing else.'
  systemd-run --user --unit="$RUN_UNIT" --collect --wait \
    -p MemoryMax=2G -p RuntimeMaxSec=600 -p WorkingDirectory="$SB/work" \
    -p StandardOutput=file:"$SB/transcripts/run.stream.jsonl" \
    -p StandardError=file:"$SB/transcripts/run.stderr" \
    /run/current-system/sw/bin/env -i "${sandbox_env[@]}" \
    DISABLE_AUTOUPDATER=1 DISABLE_NON_ESSENTIAL_MODEL_CALLS=1 DISABLE_INSTALLATION_CHECKS=1 \
    "$CLAUDE_BIN" -p "$prompt" --model "$MODEL" \
      --output-format stream-json --verbose \
      --permission-mode default --strict-mcp-config \
      --allowedTools Skill 'Bash(orchestrate:*)' \
      --max-turns 12
}

status() {
  systemctl --user --no-pager status "$NEXUS_UNIT" 2>&1 | head -5 || true
  ls -la "$SB/runtime/orchestrate-nexus" "$SB/state/orchestrate-nexus" 2>&1 || true
}

stop() {
  systemctl --user stop "$RUN_UNIT" 2>/dev/null || true
  systemctl --user stop "$NEXUS_UNIT" 2>/dev/null || true
}

teardown() {
  stop
  rm -f "$SHORT"
  rm -rf "$SB"
  echo "torn down"
}

case "${1:-}" in
  create) create ;; start) start ;; test) test_run ;; status) status ;;
  enter) shift; enter "$@" ;; stop) stop ;; teardown) teardown ;;
  all) create; start; test_run; status ;;
  *) echo "usage: $0 create|start|test|enter CMD...|status|stop|teardown|all" >&2; exit 2 ;;
esac
