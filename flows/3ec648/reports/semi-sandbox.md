# Semi-sandbox: the Capsule's first embodiment

A light-model Claude Code flow (claude-haiku-4-5-20251001) ran inside a sandbox root under the scratchpad. It loaded the `orchestrate` skill and completed one Lock/Release round trip against a sandbox Orchestrate Nexus that has its own sockets and store. Tear-down left nothing behind. Three gaps were found: two are hardwired paths, and one is the account state that comes in with the credential.

## Layout

Everything lives under `SB=<scratchpad>/capsule`. A symlink `/tmp/cap3ec -> SB` exists only for the sandbox's lifetime (see gap 1).

| Path (via `/tmp/cap3ec`) | Role |
|---|---|
| `home/` | `HOME`; `home/.claude/.credentials.json` (0600) is the only file copied from the live home |
| `runtime/` | `XDG_RUNTIME_DIR` (0700); the Nexus binds `runtime/orchestrate-nexus/orchestrate.sock` and `orchestrate-meta.sock` here |
| `state/` | `XDG_STATE_HOME`; the store is `state/orchestrate-nexus/orchestrate-nexus.sema` (fresh) |
| `config/ cache/ data/ tmp/` | `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`, `TMPDIR` |
| `work/` | cwd of the flow; `work/.claude/skills/orchestrate/SKILL.md` is the one skill it loads |
| `transcripts/` | the `claude -p` stream-json output; the native session jsonl is in `home/.claude/projects/<cwd>/` |
| `nexus.log` | Nexus stdout/stderr |

Every process runs under `env -i` with only the variables shown in the script. No `CLAUDE_*`, `SSH_AUTH_SOCK`, `GNUPGHOME`, `LOJIX_*` or D-Bus variable is passed through.

## What was copied, and what deliberately was not

- Copied: `/home/li/.claude/.credentials.json` (with `install -m 600`; its contents were never printed). Its only key is `claudeAiOauth`. The access token was valid for about 7 more hours, so no refresh happened. After the runs the sandbox copy was byte-identical to the live file (`cmp`), so no refresh-token rotation occurred.
- Copied (not from the live home): the generated `orchestrate` skill from `/home/li/primary/.claude/skills/orchestrate/SKILL.md`.
- Not copied:
  - `~/.claude.json`: account cache, project history and `machineID`. Claude Code recreated its own copy.
  - `~/.claude/settings.json`: hooks, statusLine, permissions, env, model and plugins.
  - `~/.claude/skills`, `plugins`, `projects`, `history.jsonl`, `sessions` and `daemon*`.
  - The live Orchestrate store. A populated store resumes its persisted socket paths, so a copy would try to bind the live sockets.
  - Anything under `/run/user/1001`.

## How each part locates its sockets and store

- `orchestrate-nexus` (0.35.0, `crates/orchestrate-nexus/src/defaults.rs`) takes no arguments. It reads `XDG_RUNTIME_DIR` (required) and `XDG_STATE_HOME` (falling back to `HOME/.local/state`). From these it derives `<runtime>/orchestrate-nexus/{orchestrate.sock,orchestrate-meta.sock}` and `<state>/orchestrate-nexus/orchestrate-nexus.sema`. The file names are compiled in, but the roots can be overridden through the environment.
- The direct client `orchestrate` requires `ORCHESTRATE_SOCKET` and has no compiled default (`crates/orchestrate/src/main.rs`).
- The installed wrapper `~/.nix-profile/bin/orchestrate` runs `export ORCHESTRATE_SOCKET="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/orchestrate-nexus/orchestrate.sock"`. This overwrites any caller-set `ORCHESTRATE_SOCKET`. The sandbox therefore redirects the stock wrapper by setting `XDG_RUNTIME_DIR`, and the flow uses the same `orchestrate` command a live flow uses.

## The script

The script is at `/tmp/claude-1001/-home-li-primary/3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3/scratchpad/capsule.sh`, with a copy at `/home/li/primary/flows/3ec648/witnesses/semi-sandbox-capsule.sh`. It has these subcommands:

- `capsule.sh create`: makes the layout and copies the credential and the skill.
- `capsule.sh start`: starts the Nexus as the transient user unit `capsule-3ec648-nexus` (MemoryMax=256M, RuntimeMaxSec=1800) and waits up to 20 s for the socket.
- `capsule.sh enter CMD...`: runs a command in the sandbox environment, for example `capsule.sh enter orchestrate 'Observe.Locks'`.
- `capsule.sh test`: runs the light-model `claude -p` as the transient unit `capsule-3ec648-claude` (MemoryMax=2G, RuntimeMaxSec=600, `--max-turns 12`, `--wait`).
- `capsule.sh status`, `capsule.sh stop`, `capsule.sh teardown`, and `capsule.sh all` (create, start, test, status).

Set `CAPSULE_MODEL=sonnet` to swap the model.

```bash
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
```

## Witnessed results

Method: I ran each subcommand from the parent harness and read the outputs listed below. I parsed transcripts with `jq` over the stream-json output, and checked the live system only with read-only commands (`ls`, `grep -c`, `cmp`, `orchestrate 'Observe.Locks'`).

1. **Own root, credential only.** After `create`, `home/.claude/` held only `.credentials.json`. The flow's init event reported `apiKeySource: none` and model `claude-haiku-4-5-20251001`, so it authenticated from the copied OAuth file. Claude Code then wrote its own files into the sandbox: `home/.claude.json`, backups, the `projects/` session jsonl, `plugins/synced`, `skills/synced`, and `cache/claude-cli-nodejs/...`.
2. **Own Nexus.**
   - `start` bound `runtime/orchestrate-nexus/orchestrate.sock` and `orchestrate-meta.sock`, created a fresh 188 KB `state/.../orchestrate-nexus.sema`, and logged `orchestrate-nexus ready`.
   - `enter orchestrate 'Observe.Locks'` returned `Observed.Locks.[]`. The live Nexus holds many locks, so this reply came from the sandbox one.
   - The direct client without `ORCHESTRATE_SOCKET` returned `ORCHESTRATE_SOCKET is required` (rc 1).
3. **Light-model round trip.**
   - **Run 1 (failed):** haiku loaded the skill but rewrote the Datom curly-quoted reason `“Capsule round trip”` as ASCII `"..."`. All 12 Lock attempts returned `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 6 } }`, and the run ended with `error_max_turns` ($0.093).
   - **Run 2:** with a bare single-word reason, the flow did `Skill: orchestrate`, got `Locked.{ 1 CapsuleProbe 3ec648 [ /tmp/cap3ec/work/probe ] CapsuleRoundTrip }`, then `Released.{ 1 ... }`. It finished with `success` in 5 turns ($0.028, 19.5 s, peak 168 MB).
   - **Run 3 (hardened env):** the same steps returned `Locked.{ 2 ... }` and `Released.{ 2 ... }` (5 turns, $0.028, 8.3 s, peak 136 MB). Lock ID 2 after ID 1 shows the sandbox store persisted across runs. Live `Observe.Locks` contained no `CapsuleProbe` at any point.
   - The run 3 transcript is preserved at `/home/li/primary/flows/3ec648/witnesses/semi-sandbox-run3.stream.jsonl`. I grepped the transcripts for `sk-ant|accessToken|refreshToken` and found no match.
4. **Tear-down.** After `teardown`:
   - `/tmp/cap3ec` and `SB` were gone, and no `capsule-3ec648*` unit remained.
   - The only `orchestrate-nexus` process was the live one (pid 1944, running since Sep 26).
   - `/run/user/1001/orchestrate-nexus/` held its original four entries.
   - `~/.claude/projects` had no capsule entry, and `~/.claude.json` contained no capsule or cap3ec string.
   - A `find /tmp -maxdepth 3 -newer created.marker` and a `find` over `~/.claude ~/.cache ~/.config ~/.local/state` for capsule names showed nothing from the sandbox. The only hits were `/tmp` itself (the symlink) and the parent harness's own `bash-edit-diff`.
   - Limit: the live store's mtime advanced during the session. Other flows use the live Nexus, and I also made read-only `Observe.Locks` calls, so this check cannot tell whether an Observe writes the store.

## Implementation gaps

1. **Socket path length (hardwired by the kernel; not compiled in).** `sun_path` holds 108 bytes. The scratchpad root plus `/capsule/runtime/orchestrate-nexus/orchestrate-meta.sock` is 137 bytes, so the sandbox needs the short alias `/tmp/cap3ec`, which lives outside the scratchpad until tear-down. A Capsule needs a short runtime root of its own, for example a private runtime directory such as `/run/user/<uid>/capsule/<id>` with ownership rules for it, or a mount namespace.
2. **Nexus file names are compiled in.** `orchestrate-nexus`, `orchestrate.sock`, `orchestrate-meta.sock` and `orchestrate-nexus.sema` are constants. Only the XDG roots can be moved. This is enough for a Capsule, but it means one Nexus per XDG root.
3. **The installed client wrapper ignores `ORCHESTRATE_SOCKET`.** It unconditionally exports a value derived from `XDG_RUNTIME_DIR`. Redirection works only through `XDG_RUNTIME_DIR`, which also moves every other per-user runtime socket for the flow (D-Bus, Wayland, other nexuses). A `${ORCHESTRATE_SOCKET:-...}` form would let a Capsule point one client independently.
4. **A copied store carries live socket paths.** The store persists the socket configuration ("a populated store resumes them"), so a copied store would try to bind the live paths. A Capsule must start from a fresh store, or relocate the store first (`orchestrate-relocate` exists and was not examined).
5. **The live meta wrapper does not match the live store.** The live runtime dir holds `meta-orchestrate.sock`, but `~/.nix-profile/bin/orchestrate-meta` targets `orchestrate-meta.sock`. This is a live-system finding outside the sandbox and was not acted on.
6. **The credential brings in account state.**
   - Claude Code synced the account's claude.ai skills (`anthropic-skills:*`) into the sandbox home.
   - Before hardening, it opened claude.ai MCP proxy connectors for Gmail, Google Drive, Google Calendar and Claude Docs. Their logs are under `cache/.../mcp-logs-claude-ai-*`.
   - `ENABLE_CLAUDEAI_MCP_SERVERS=false` plus `--strict-mcp-config` stopped new connector logs in run 3. The synced skills still arrived (28 skills listed at init).
   - A sandbox flow therefore runs as the living's account, not as an anonymous seat.
7. **The permission mode: explained and fixed.** The installed `claude` wrapper ends with `exec ... .claude-wrapped --dangerously-skip-permissions "$@"`, so the earlier runs really were in bypass (see `witnesses/sandbox-permission-mode.md`). `test` now runs the unwrapped binary (`/nix/store/qsq3lh2i05dz77dakipwy9f1fkssq1zw-claude-code-2.1.284/bin/.claude-wrapped`) under `env -i` with the sandbox variables plus the three `DISABLE_*` variables the wrapper used to set. Outcome: the init event reports `permissionMode: default`, `permission_denials` is empty, and the haiku flow completed Lock then Release (`Locked.{ 1 ... }`, `Released.{ 1 ... }`; 5 turns, $0.014, 6.1 s). Bash was allowed by the print-mode allow rule `--allowedTools Skill 'Bash(orchestrate:*)'`, on the command line; no settings file was needed, and the rule stays bound to the run, not to the sandbox HOME. The live Nexus saw no `CapsuleProbe`; teardown left no unit or alias. Still true: there is no filesystem isolation, so the flow can read and write the live home by absolute path.
8. **Light-model fidelity at the Datom boundary.** Haiku normalizes curly quotes to ASCII, so a multi-word `LockReason` is unwritable for it as the skill teaches it. Light-model test flows need bare single-word values, or the Datom reader needs to report the ASCII-quote case with a typed hint.
9. **Token refresh risk.** If the copied access token is expired, the sandbox flow would refresh it. If the provider rotates refresh tokens, that could invalidate the live home's copy. This did not occur here (`cmp` identical), but a Capsule must either refuse to start near expiry or write the refreshed credential back.

## Sources

- `/git/github.com/LiGoldragon/orchestrate` at 9070cbb (version 0.35.0 = installed): `crates/orchestrate-nexus/src/defaults.rs`, `crates/orchestrate/src/main.rs`, `crates/orchestrate-meta/src/main.rs`.
- `/home/li/.nix-profile/bin/orchestrate`, `/home/li/.nix-profile/bin/orchestrate-meta`, and `systemctl --user cat orchestrate-nexus.service`.
- `/home/li/primary/flows/3ec648/witnesses/semi-sandbox-run3.stream.jsonl` and `/home/li/primary/flows/3ec648/witnesses/semi-sandbox-capsule.sh`.
- The living's words (STT, 2026-10-02), as quoted in the main flow's brief.
