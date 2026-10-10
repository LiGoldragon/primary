# flow-claude-hook — a gated semi-sandbox: the Flow harness hook
# (lib/components/flow-hook.nix) configured in a light-model Claude Code
# print run, against its own Flow Nexus. It needs the living's Claude login
# and the network, so it is a runner, never a check, and it refuses to run
# unless FLOW_TEST_LIVE=1 is set. `nix flake check` only builds this script.
#
# Drive:
#   1. A fresh short `mktemp -d` root, removed in an exit trap with the
#      Nexus killed. HOME, every XDG root and TMPDIR point into it.
#   2. Copy only `~/.claude/.credentials.json` into the root's home; refuse
#      when its access token expires within 15 minutes.
#   3. Start a Flow Nexus on the root (fresh store, its own sockets) and
#      assert `List.{}` -> `Listed.[]`.
#   4. Write the hook settings into the root and run Claude Code once:
#      `-p`, the cheapest model, one allowed tool (`Bash(echo:*)`), a prompt
#      that runs one echo, bounded by a 2G scope, 300 s and 4 turns. Every
#      hook input is tapped into the root before the hook reads it.
#   5. Witness, every check printed before the verdict:
#      a. the hook fired on SessionStart, PostToolUse and Stop;
#      b. SessionStart's ResolveCaller answered (exit 0);
#      c. Stop's QueueTurnEnd answered TurnEndQueued (exit 0);
#      d. `List.{}` now holds a flow carrying the run's session id: the
#         Nexus's state shows the flow's events.
#   Exit 0 only when every check holds; 1 otherwise.
{
  pkgs,
  flake,
  system,
  ...
}:
let
  flow = flake.lib.components.flow.forSystem system;
  claude = flake.lib.components.claude.forSystem system;
  hook = flake.lib.components.flow-hook.forSystem system;
  settings = hook.settings {
    prefix = ''tee -a "$FLOW_HOOK_WITNESS/inputs.jsonl" | '';
    suffix = " 2>> \"$FLOW_HOOK_WITNESS/calls.tsv\"";
  };
in
pkgs.writeShellApplication {
  name = "flow-claude-hook";

  runtimeInputs = [
    pkgs.coreutils
    pkgs.jq
    pkgs.systemd
  ];

  meta.description = "The Flow harness hook in a light-model Claude Code run against its own Flow Nexus (gated: needs FLOW_TEST_LIVE=1).";

  text = ''
    if [ "''${FLOW_TEST_LIVE:-}" != 1 ]; then
      echo "flow-claude-hook: needs the living's Claude login and the network; set FLOW_TEST_LIVE=1 to run it" >&2
      exit 2
    fi

    model="''${FLOW_TEST_MODEL:-${flake.lib.cheapestModel.claude}}"
    livingCredentials="$HOME/${claude.credentials}"
    # systemd-run reaches the living's user manager through these two; the
    # bounded scope then gets the sandbox's runtime directory back.
    livingRuntime="''${XDG_RUNTIME_DIR:?needed to reach the user manager}"
    expiresAt="$(jq -r '.claudeAiOauth.expiresAt // 0' "$livingCredentials")"
    if [ "$expiresAt" -lt $(( ($(date +%s) + 900) * 1000 )) ]; then
      echo "flow-claude-hook: the Claude access token expires within 15 minutes; refresh the login first" >&2
      exit 2
    fi

    # A short root: sun_path holds 108 bytes.
    root="$(mktemp -d /tmp/fh-XXXXXXXX)"
    flowNexusPid=
    trap 'if [ -n "$flowNexusPid" ]; then kill "$flowNexusPid" 2>/dev/null || true; wait "$flowNexusPid" 2>/dev/null || true; fi; rm -rf "$root"' EXIT

    export HOME="$root/home" XDG_RUNTIME_DIR="$root/run" XDG_STATE_HOME="$root/state" \
      XDG_CONFIG_HOME="$root/config" XDG_CACHE_HOME="$root/cache" XDG_DATA_HOME="$root/data" \
      TMPDIR="$root/tmp" FLOW_HOOK_WITNESS="$root/witness"
    mkdir -p "$HOME/.claude" "$XDG_STATE_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" \
      "$XDG_DATA_HOME" "$TMPDIR" "$FLOW_HOOK_WITNESS" "$root/work"
    chmod 700 "$HOME" "$HOME/.claude"
    install -m 600 "$livingCredentials" "$HOME/${claude.credentials}"
    unset FLOW_SOCKET FLOW_META_SOCKET
    ${flow.start}
    reply="$(timeout 10 ${flow.client} 'List.{}')"
    test "$reply" = 'Listed.[]' || { echo "flow-claude-hook: List answered $reply before the run" >&2; exit 1; }

    cat > "$root/settings.json" <<'SETTINGS'
    ${settings}
    SETTINGS
    touch "$FLOW_HOOK_WITNESS/inputs.jsonl" "$FLOW_HOOK_WITNESS/calls.tsv"

    echo "flow-claude-hook: running ${claude.package.name} ($model) with the hook on $root"
    set +e
    (cd "$root/work" && XDG_RUNTIME_DIR="$livingRuntime" DBUS_SESSION_BUS_ADDRESS="unix:path=$livingRuntime/bus" \
      systemd-run --user --scope --quiet -p MemoryMax=2G \
      env XDG_RUNTIME_DIR="$root/run" DBUS_SESSION_BUS_ADDRESS= DISABLE_AUTOUPDATER=1 DISABLE_NON_ESSENTIAL_MODEL_CALLS=1 \
        ENABLE_CLAUDEAI_MCP_SERVERS=false \
      timeout 300 ${claude.binary} -p 'Run exactly this with the Bash tool: echo flow-hook-probe. Then reply with the single word done.' \
        --model "$model" --settings "$root/settings.json" \
        --permission-mode default --strict-mcp-config \
        --allowedTools 'Bash(echo:*)' --max-turns 4 \
        --output-format stream-json --verbose > "$root/run.jsonl" 2> "$root/run.stderr")
    runCode=$?
    set -e
    sessionId="$(jq -r 'select(.type == "system" and .subtype == "init") | .session_id' "$root/run.jsonl" | head -n 1)"
    echo "run: exit $runCode, session $sessionId"
    if [ "$runCode" != 0 ]; then
      echo "--- run stderr"
      tail -n 20 "$root/run.stderr"
      echo "--- run stream tail"
      tail -n 3 "$root/run.jsonl"
    fi
    echo "--- hook messages in the run's stream"
    jq -c 'select(.type == "system" and (.subtype | startswith("hook"))) | {subtype, hook_event, exit_code, stderr}' "$root/run.jsonl"
    echo "--- hook inputs"
    jq -c . "$FLOW_HOOK_WITNESS/inputs.jsonl"
    echo "--- hook calls (event, datom, flow exit, flow output)"
    cat "$FLOW_HOOK_WITNESS/calls.tsv"

    red=0
    check() {
      if [ "$2" = yes ]; then echo "green: $1"; else echo "red: $1"; red=1; fi
    }
    fired() { jq -e --arg e "$1" 'select(.hook_event_name == $e)' "$FLOW_HOOK_WITNESS/inputs.jsonl" > /dev/null && echo yes || echo no; }
    answered() {
      awk -F '\t' -v e="$1" -v w="$2" '$1 == e && $3 == "0" && index($4, w) == 1 { found = 1 } END { print (found ? "yes" : "no") }' "$FLOW_HOOK_WITNESS/calls.tsv"
    }
    check "the run exited 0" "$([ "$runCode" = 0 ] && echo yes || echo no)"
    check "the hook fired on SessionStart" "$(fired SessionStart)"
    check "the hook fired on PostToolUse" "$(fired PostToolUse)"
    check "the hook fired on Stop" "$(fired Stop)"
    check "SessionStart: ResolveCaller answered" "$(answered SessionStart CallerResol)"
    check "Stop: QueueTurnEnd answered TurnEndQueued" "$(answered Stop TurnEndQueued)"
    listed="$(timeout 10 ${flow.client} 'List.{}')"
    echo "List.{} after the run: $listed"
    check "the Nexus lists the run's session" "$(case "$listed" in *"$sessionId"*) [ -n "$sessionId" ] && echo yes || echo no ;; *) echo no ;; esac)"

    ${flow.stop}
    flowNexusPid=
    if [ "$red" = 0 ]; then echo "flow-claude-hook: green"; else echo "flow-claude-hook: red" >&2; fi
    exit "$red"
  '';
}
