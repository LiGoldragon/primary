# Flow 0.17.4 three-live-start witness: fixture, empty store, baseline

Subflow of 8904b1, zero seats started, 2026-09-26. Method: shell commands
run directly in this seat's own pane, `nix-store --verify-path`/`--check-validity`/`-q
--deriver` (read-only), the 0.17.4 client/service binaries run only with the
bare `--version` argument, `systemctl --user show`/`stop` and `journalctl`
(read-only except the one scratch unit this seat started and stopped),
`ps -ef`, `ss -xlp`, `stat`/`sha256sum` on store/socket files (content of
`flow.sema` never opened, only size/mtime/hash and, for the scratch store,
one `List` reply), one read-only `flow 'List.{ }'` against the live stable
socket taken before and after, `herdr session list`/`workspace
list`/`agent list` (read-only), a `systemd-run --user` transient service
holding the scratch `flow-nexus` under a memory cap and an internal
`timeout`, and `Read`/`grep` of the already-fetched immutable checkout
`/home/li/wt/flow-0174-independent-test-407811` at tag `flow-0.17.4`
(`bc464e5e1b94fcc179af73111f43b69db1f69fc5`) plus the vendored
`signal-flow` 7.0.0 source pinned by its Cargo.lock
(`1c9e4b306e2686a2aa7088e461ff6b2f22b45064`). No Start, Stop-of-a-real-row,
Restart, or message was sent; the only Stop issued was `systemctl --user
stop` on the one unit this seat held.

Scratch directory: `/tmp/flow0174-fx.hoygQ9` (moved here from the assigned
scratchpad after the scratchpad's absolute path proved too long for a Unix
socket's 108-byte `SUN_LEN`; reported and left as-is, not silently
substituted).

## 1. Field Sol's own record — held

`flows/9ac67c/summary-flow-upgrade.md` in Field Sol's own checkout
(`/home/li/wt/primary/field-packet-56ae53`), section "2026-09-26 disposable
Flow 0.17.4 live-test profile and build decision", in its own words: "The
chosen scratch-only profile for each of three strictly sequential native
Claude Starts is `flow_aspect=Field`, `power_level=UltraLow`,
`harness_kind=Claude`, `model_name=claude-haiku-4-5-20251001`,
`effort=medium`, with ordered skills `[spirit, testing,
operational-final-response]`." Matches the relayed profile exactly,
including that Field Sol names the last two skills as its own choice, not
Fable's named words. The same file's later sections ("Fable scratch
fixture decisions") also match this seat's fixture instructions
(live Herdr, test-named session, existing Claude login, scratch working
directory, absolute scratch HOME/XDG_RUNTIME_DIR/FLOW_SOURCE_ROOT) word for
word.

## 2. Provenance — held

`/nix/store/7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4`: `nix-store
--verify-path` and `--check-validity` both exit 0; deriver
`/nix/store/vfv1g24y22h9iqj285d328kziwqy6b7c-flow-0.17.4.drv`. The
derivation's source input is content-addressed (`fixed:r:sha256:...`) with
no retained deriver and no `.git`, so the store path alone does not carry
the git revision (matches Field Sol's and Sonnet's prior notes). Tie to
the tag: the already-fetched checkout `/home/li/wt/flow-0174-independent-test-407811`
is at `bc464e5e1b94fcc179af73111f43b69db1f69fc5`, clean, tag
`flow-0.17.4` points at HEAD. `flow --version` -> `flow 0.17.4`; `flow-nexus
--version` -> `flow-nexus 0.17.4`; both exit 0, both run with the bare
version argument only, no other invocation of the service binary.

## 3. Fresh live baseline — held

Stable `flow-nexus.service`: active/running, PID 1937 (0.12.2), 0
restarts. Next `flow-nexus-next.service`: active/running, PID 90750
(0.17.1), 0 restarts. Stable store `flow.sema`: 1,056,768 B, mtime
2026-09-26 18:22:10, SHA-256 `f03f610a...c78c0f03`. Next store: 581,632 B,
mtime 20:30, SHA-256 `ece72cc1...8d35e06e`. All four sockets present,
mtimes unchanged across this witness. Stable `List.{ }` through the
ordinary client: 25 top-level rows (counted by bracket-depth parse, not
text search). Herdr: sessions `default` (running), `messaging-build`
(stopped), `recovery-56ae53` (running) — no session named for this test
exists yet. `agent list`: 10 agents, all pre-existing named seats; none
belongs to this test.

## 4. The fixture — held

`/tmp/flow0174-fx.hoygQ9/{home,run,source,work}`, all new and empty before
use. `run` is `chmod 700`. All four paths absolute and under the scratch
root (checked programmatically before use, not asserted).

## 5. The scratch service — held

Environment printed and checked absolute-and-under-scratch before start:
`HOME=/tmp/flow0174-fx.hoygQ9/home`,
`XDG_RUNTIME_DIR=/tmp/flow0174-fx.hoygQ9/run`,
`FLOW_SOURCE_ROOT=/tmp/flow0174-fx.hoygQ9/source`. Started via
`systemd-run --user --unit=flow0174-scratch-1790483655 -p MemoryMax=512M
--setenv=... -- timeout 300 <store-path>/bin/flow-nexus`: unit active,
`ExecMainCode=0`. Its child (PID 496111, `flow-nexus`) held by that PID.
Open files read from `/proc/496111/fd` and `ss -xlp`, not from intent
alone: fd 3 -> `/tmp/flow0174-fx.hoygQ9/home/.local/state/flow/flow.sema`;
listening sockets `.../run/flow/flow-meta.sock` (fd 4) and
`.../run/flow/flow.sock` (fd 6) — all three under the scratch directory.
`/proc/496111/environ` confirms the three variables as given.

**Deviation**: the first attempt, with the scratch root under this
session's scratchpad path, failed at start (`meta socket ... path must be
shorter than SUN_LEN`) — an AF_UNIX 108-byte path limit, not a Flow
defect. Reported; the unit was reset-failed and a second, shorter scratch
root (`/tmp/flow0174-fx.hoygQ9`, 22 characters) was used instead. No Flow
process ran under the first attempt.

## 6. Empty store shown — held

Scratch store directory listing: one file, `flow.sema`, 1,056,768 B (an
initial redb allocation size, coincidentally equal to the live stable
store's *size*) but SHA-256 `8536b9b2...9e27f04ce12` — distinct from the
live store's hash. `FLOW_SOCKET=<scratch>/run/flow/flow.sock flow
'List.{ }'` against the scratch client/socket answered `Listed.[]` — zero
rows, not the live 25. The size coincidence is explained (redb's default
file size on creation) and not mistaken for a live-store collision.

## 7. The three Start requests — derived, not sent

From the vendored `signal-flow` 7.0.0 at
`1c9e4b306e2686a2aa7088e461ff6b2f22b45064` (`src/generated/signal.rs`):
`Query::Start(StartRequest{ launch_profile: LaunchProfile, origin_clue:
OriginClue })` travels on the **ordinary** socket, via the `flow` client
(not `flow-meta`). `LaunchProfile` fields, in order: `launch_request_id,
launch_source_vector, skill_name_vector, flow_aspect, power_level,
harness_kind, model_name, effort, flow_id_option, remembered_flow_vector,
herdr_session_name, system_prompt_bundle_file, instruction_prompt`.
`OriginClue{ flow_id, session_id, turn_id }`. `FlowAspect` is confirmed a
closed 3-variant enum (`Psyche, Mind, Field`) in this exact revision — no
`Test` variant exists, so Field Sol's choice of `Field` is the real aspect
value, not a fourth "no real role" variant; the disposable-ness is carried
by the seat being scratch/throwaway, not by the aspect tag itself. This
is the point stage one flagged as unresolved; it is now resolved by
reading Field Sol's own accepted decision (item 1) and the type (item 7):
plan text stands corrected, no blocker.

Every field below is exactly what a caller passes; the server-side
composed prompt text (with the receipt footer, skill stacking, and the
800-UTF-16-unit paste threshold in `composition.rs`) is computed by
`flow-nexus` at Start time from `instruction_prompt`, not sent by the
client. `launch_source_vector: []` and `remembered_flow_vector: []` for
all three (no extra sources named in the plan; no predecessor). Each
`launch_request_id` and `herdr_session_name` must be unique per the plan
("every attempt uses a unique request and Flow ID... never the default
session"); the exact session name and per-run bundle file path are the
executing worker's to mint at run time, shown here as placeholders.

**A — two short lines (reaches the harness plain):**
```
Start.{
  { launch-0174-A [] [ spirit testing operational-final-response ]
    Field UltraLow Claude claude-haiku-4-5-20251001 medium None []
    flow0174-test-8904b1 «<scratch-source>/flow-system-prompt.md»
    «Report your two-line status.
Nothing else.» }
  { 8904b1 <this-seat-session-id> <this-turn-id> }
}
```
**B — longer than eight hundred units (reaches it wrapped):**
```
Start.{
  { launch-0174-B [] [ spirit testing operational-final-response ]
    Field UltraLow Claude claude-haiku-4-5-20251001 medium None []
    flow0174-test-8904b1 «<scratch-source>/flow-system-prompt.md»
    «<a single-line instruction_prompt of >800 UTF-16 units, e.g. a
    long repeated sentence long enough that render_claude_line's
    candidate body plus the fixed receipt footer exceeds
    ClaudePasteThreshold::LIMIT=800, forcing render_claude_direct and,
    at the harness, Claude Code's own pasted-content wrap>» }
  { 8904b1 <this-seat-session-id> <this-turn-id> }
}
```
**C — one short line (plain):**
```
Start.{
  { launch-0174-C [] [ spirit testing operational-final-response ]
    Field UltraLow Claude claude-haiku-4-5-20251001 medium None []
    flow0174-test-8904b1 «<scratch-source>/flow-system-prompt.md»
    «Report ready.» }
  { 8904b1 <this-seat-session-id> <this-turn-id> }
}
```

**Herdr session/pane choice** (`herdr/launch.rs`, read only):
`create_launch_pane` issues `herdr --session <launch_profile.herdr_session_name>
workspace create --cwd <configured_workspace_root> --label <agent_name>
--env FLOW_LAUNCH_REQUEST_ID=... --no-focus`; the session name is taken
verbatim from the profile field the caller sets — Flow does not default it
to `default`, so naming it `flow0174-test-8904b1` (never the default
session) is entirely the caller's choice, satisfied by construction.
`configured_workspace_root()` resolves to `FLOW_SOURCE_ROOT` (the
`DefaultConfiguration`'s `source_root`), so a seat's cwd is the scratch
source directory when the scratch service's `FLOW_SOURCE_ROOT` is scratch.

**Pane environment**: before `agent start`, Flow only runs `herdr pane run
<pane> "unset CLAUDE_CODE_CHILD_SESSION CLAUDE_JOB_DIR
CLAUDE_CODE_SESSION_ID CLAUDE_CODE_SESSION_KIND && printf ..."` in the
pane's own shell — it does not set `HOME`, `CLAUDE_CONFIG_DIR`, or any
other identity variable. The pane's process therefore inherits the *live*
Herdr server's own ambient environment for a newly created pane (this
seat's fixture instructions specify a live, not scratch, Herdr server), so
a started seat's `HOME` and Claude login are the living's real ones,
unedited — matching this seat's fixture decision exactly, and confirmed
from source rather than assumed.

**Outside the scratch directory, a real Start would write**: (1) Herdr's
own state — a new workspace/pane/tab record inside the live Herdr config
tree, under the test-named session directory (`~/.config/herdr/sessions/flow0174-test-8904b1/...`
or equivalent), scoped to panes the test itself creates and can close; (2)
the started Claude process's own new session transcript and job directory
under the real `~/.claude` (transcript root and job dir are not
overridden by anything in `herdr/launch.rs`); (3) Herdr's pane-label
write/readback for the new pane, likewise scoped to it. **Not** written
outside scratch: the per-launch system-prompt bundle copy (written under
the scratch service's own `state_directory/launch-bundles`, since that
state directory is scratch `HOME`-derived); the Messenger registry (no
message is sent until a start reaches Started, per the plan's standing
consequence, and this plan's seats are never given a route). No
dry-run/validating mode exists in this revision — `Query::Start` always
drives `create_launch_pane` and `start_native_harness`, which always issue
live Herdr calls; nothing in `composition.rs` or `herdr/launch.rs`
short-circuits before those calls.

## 8. Live baseline again — held

Stable service PID 1937 unchanged, 0 restarts; next service PID 90750
unchanged, 0 restarts. Stable store size/mtime/hash unchanged
(`f03f610a...c78c0f03`); next store unchanged (`ece72cc1...8d35e06e`).
All four socket mtimes unchanged. `flow 'List.{ }'` against the live
stable socket: byte-identical to the before-reading. Herdr `session list`:
unchanged, no new session. The only differences observed anywhere are the
scratch directory's own new store/socket files and the one transient
systemd unit this seat created and then stopped — both accounted for as
this seat's own.

## 9. Scratch service stopped — held

`systemctl --user stop flow0174-scratch-1790483655.service`: unit now
`inactive`/`dead`, `MainPID=0`. `kill -0 496111` (the held child PID):
"no such process". `ss -xlp` no longer lists either scratch socket as
listening; the socket files remain on disk as stale inodes (not removed,
per "leave the scratch directory in place ... for my review"). `ps -ef`
after stop shows only the two live processes (1937, 90750) — no other
Flow process was started or stopped by this seat.

## Scratch directory left for review

`/tmp/flow0174-fx.hoygQ9` — contains `home/.local/state/flow/flow.sema`
(empty store, 0 rows), stale `run/flow/{flow.sock,flow-meta.sock}`, empty
`source/` and `work/`. Not removed, per instruction.

## Sources

- flows/8904b1/witnesses/flow-0174-stage-one-readiness.md
- flows/8904b1/witnesses/flow-service-post-stray-start-check.md
- flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md
- flows/8904b1/log.md, "Sonnet 38f337's stage-one evidence" entry
- /home/li/wt/primary/field-packet-56ae53/flows/9ac67c/summary-flow-upgrade.md
  (Field Sol's own record, read-only, in its own checkout)
- /home/li/wt/flow-0174-independent-test-407811 at bc464e5e1b94fcc179af73111f43b69db1f69fc5
  (`crates/flow-nexus/src/{main.rs,store.rs,composition.rs,herdr.rs,herdr/launch.rs}`)
- vendored signal-flow 7.0.0 source at 1c9e4b306e2686a2aa7088e461ff6b2f22b45064
  (`src/generated/signal.rs`), located under
  `/nix/store/fki72s640140f2525jhhwf5x24ihd0wd-.../signal-flow-7.0.0`
- Direct commands: `nix-store`, `systemctl --user`, `journalctl --user`,
  `ps -ef`, `ss -xlp`, `stat`, `sha256sum`, `herdr session/workspace/agent
  list`, `flow 'List.{ }'`, `systemd-run --user`, `/proc/<pid>/{fd,environ}`.
