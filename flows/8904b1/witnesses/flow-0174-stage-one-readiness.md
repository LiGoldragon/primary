# Flow 0.17.4 three-live-start witness: stage-one readiness

Subflow of 8904b1, read-only, 2026-09-26/27. Method: shell commands run
directly in this seat's own pane (w1:p8, HERDR_PANE_ID matches), reading
this seat's own environment, Herdr's read-only CLI (`session list`,
`workspace list`, `agent list`), `systemctl --user cat`/`show` (read-only),
`ls`/`stat` on directories and socket files (names/sizes/times only, no
file opened for content on a live store), and `git show`/`git grep` against
the already-fetched local clone `/git/github.com/LiGoldragon/flow` at tag
`flow-0.17.4` (bc464e5e1b94fcc179af73111f43b69db1f69fc5). No Flow instance,
Herdr pane, or seat was started, stopped, or configured. Labels: **O**
observed here, **I** inference, **U** unknown/cannot-prove-read-only.

**Deviation to disclose:** while probing `flow-nexus --help` for usage
text, the binary does not recognize `--help` (main.rs: only a lone
`--version` short-circuits; every other argv starts the daemon). The
process ran `RunningNexus::open` against this host's live default store
(`/home/li/.local/state/flow/flow.sema`), which was already locked by the
running `flow-nexus.service`; it printed `Database already open. Cannot
acquire lock.` and exited nonzero immediately. No content was read from or
written to the store; this is itself evidence for item 5 (concurrent open
is refused), but it was an unintended live-store touch and is reported as
required. No further un-flagged commands were run against live sockets or
stores after this was noticed.

## 1. Herdr context — proved

Kind-only environment (O): `HERDR_PANE_ID`, `HERDR_TAB_ID`,
`HERDR_WORKSPACE_ID` (small identifiers, e.g. `w1:p8`); `HERDR_SOCKET_PATH`
(a path, `/home/li/.config/herdr/herdr.sock`); `HERDR_BIN_PATH` (a Nix
store path); `HERDR_ENV=1` (a flag). `herdr session list`, `herdr workspace
list`, `herdr agent list` answered live; the returned agent list contains
this exact pane (`pane_id":"w1:p8"`, `agent_session` value equal to
`CLAUDE_CODE_SESSION_ID`), confirming the environment is this session's
own, not stale.

## 2. Identity — proved

Brief: `FLOW_ID=8904b1`, `FLOW_DIRECTORY=/home/li/wt/primary/56ae53/flows/8904b1`.
Environment (O): `CLAUDE_JOB_DIR=/home/li/.claude/jobs/native-8904b10d-...`,
`CLAUDE_CODE_SESSION_ID=8904b10d-7f06-4e44-9342-3a8a2d7e17bd`. The native
session id's first six hex characters equal `FLOW_ID`; the working
directory of this seat, `/home/li/wt/primary/56ae53`, is the parent of
`FLOW_DIRECTORY`. They agree.

## 3. Terminal — proved (no controlling tty here; caller-side tty not required)

This seat itself (O): `tty` reports not a tty; stdin/stdout are not a tty
(it runs headless under Herdr, invoked as a background Claude process, not
attached to the pane's PTY). From source (O), `crates/flow-nexus/src/main.rs`
starts the Nexus with no terminal interaction of its own; the herdr launch
code (`herdr/launch.rs`) drives the target through Herdr's socket API
(`herdr agent start`, `agent prompt`, `agent get`, `agent read`) — a
caller-side PTY is never referenced. The PTY that matters is the one Herdr
itself creates for the new pane, not one held by whatever process invokes
Flow. So: no controlling terminal is needed from Flow's caller; the pane
Herdr creates supplies it.

## 4. A runnable Flow 0.17.4 — not proved; build required, not attempted

Installed live: stable `flow-nexus.service` runs Nix store build
`flow-0.12.2` (`/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`);
`flow-nexus-next.service` runs `flow-0.17.1`
(`/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1`). Neither is
0.17.4 (O). `~/.nix-profile/bin/flow{,-nexus}` also resolve to 0.12.2 (O).
No Nix store path containing `flow-0.17.4` was found (search of
`/nix/store` derivation/output names) (O, negative result). The tagged
source is present in `/git/github.com/LiGoldragon/flow` as commit
`bc464e5e...` (fetched, objects+FETCH_HEAD only, working tree not checked
out to it) (O). Building it (`nix build` of the flake at that rev, or
`cargo build --release`) was not attempted — out of stage-one's authority.
What it would take: a `nix build` of `crates/flow-nexus`/`crates/flow` at
bc464e5e (pulling `signal-flow`@1c9e4b3 and `meta-signal-flow`@cbea31e from
their own git remotes, since those two crates are not vendored in this
tree), or an equivalent `cargo build --release --locked`. Time/limits are
unwitnessed here (I: comparable Rust workspace builds on this host have
taken low-single-digit minutes when cached, longer cold); stage one does
not authorize running it.

## 5. Scratch isolation — proved from source; the point that matters most

From `crates/flow-nexus/src/store.rs` (`DefaultConfiguration`) and
`src/main.rs` (O): every path is derived from exactly two anchors, `HOME`
and `XDG_RUNTIME_DIR` (falling back to `/etc/passwd` and `/run/user/<uid>`).
`state_directory = $HOME/.local/state/flow`, `store_path =
state_directory/flow.sema`, `launch_bundle_directory =
state_directory/launch-bundles`; `socket_directory =
$XDG_RUNTIME_DIR/flow`, sockets `flow.sock` and `flow-meta.sock` under it.
There is no separate `FLOW_STATE_DIR`/`FLOW_SOCKET_DIR` override — only
`HOME`/`XDG_RUNTIME_DIR` move these paths (`DeploymentOverrides` only
covers `FLOW_SOURCE_ROOT` and the Codex-endpoint `FLOW_CODEX_*` fields, not
the store/socket location). **The exact way to get an isolated instance**:
run `flow-nexus` (built at bc464e5e) with `HOME` and `XDG_RUNTIME_DIR` set
to a fresh scratch directory (e.g. under this flow's own tmp/scratch tree)
that does not yet contain `.local/state/flow`; `main.rs` creates the
directories with `create_dir_all` and opens/creates a brand-new
`flow.sema` there — an empty store — and binds fresh `flow.sock`/
`flow-meta.sock` under the scratch runtime dir. Because `redb` (the sema
engine's backing store) takes an exclusive file lock on open (witnessed
directly in the deviation above: a second opener on the same file is
refused, not merged), and because the scratch store is a distinct
inode/path from either live store, the scratch instance cannot open,
write, or lock either live store; and because Unix domain sockets are
bound at distinct paths, it cannot bind or be reached at either live
socket path.

Live sockets and stores to check untouched before/after (O, current
sizes/times):
- Live stable store: `/home/li/.local/state/flow/flow.sema` — 1,056,768 bytes, mtime 2026-09-26 18:22 (plus `launch-bundles/`, `recovery-gcroots/` beside it).
- Live stable sockets: `/run/user/1001/flow/flow.sock`, `/run/user/1001/flow/flow-meta.sock` (present, both sockets, mtime 2026-09-26 16:19).
- Live next store: `/home/li/.local/state/flow-next/.local/state/flow/flow.sema` — 581,632 bytes, mtime 2026-09-26 20:30.
- Live next sockets: `/run/user/1001/flow-next/flow/flow.sock`, `flow-meta.sock` (mtime 2026-09-26 17:38).

Other things a start touches, and containment, all read from source (I
unless noted):
- **Herdr's own state** (panes/workspaces/agent registry): the scratch run
  would create its own new Herdr workspace/pane through Herdr's ordinary
  API — this is Herdr state for a pane the test itself owns and can close;
  it does not touch any existing pane's record.
- **Claude's own session directory / transcript**: a new pane starts a new
  `claude` process, which gets its own new `CLAUDE_CODE_SESSION_ID` and
  writes to its own new transcript file; no existing transcript is
  appended to.
- **Job-directory-shared title state**: `herdr/launch.rs` names
  `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_JOB_DIR`, `CLAUDE_CODE_SESSION_ID`,
  `CLAUDE_CODE_SESSION_KIND` as `CLAUDE_INHERITED_ENVIRONMENT` (O, with the
  comment: a shared `CLAUDE_JOB_DIR` shares one job/title state between
  processes) and the launch path is documented there as one that must not
  let the new process inherit them — i.e. Flow's own launcher already
  strips these before starting the child, so the new seat gets its own job
  directory and does not share title state with the launching pane. This
  seat's own `CLAUDE_JOB_DIR` (`/home/li/.claude/jobs/native-8904b10d-...`)
  would not be inherited by a start Flow performs.
- **Messenger's registry / Message service**: not exercised — the plan's
  "standing consequence" is that no message is sent to a seat until
  Started, and stage one sends no message and the started seats in stage
  two, per plan, are never real roles that a message route would target.
  Not fully provable read-only beyond this source-level guard.
- **Herdr's own pane-label / title readback**: `label_herdr_pane` sets a
  Herdr pane label via `herdr pane ...` and reads it back — again scoped
  to the new pane the test creates.

## 6. The disposable seats — partly proved, one point flagged

`LaunchProfile`/`FlowAspect` (O, `composition.rs`): the aspect enum in
this revision's wire type (`signal_flow::FlowAspect`) is a **closed** set
with exactly three variants used here — `Psyche`, `Mind`, `Field` — with
no fourth "test" variant found in this repo's use of it (the enum itself
lives in the separate `signal-flow` crate, not vendored in this tree, so
its full variant list was not read directly; only its three-way match in
`composition.rs::aspect_name` was). **This does not confirm the plan's
"test aspect that is no real role" exists as such** — if `FlowAspect` truly
has no fourth variant, the disposable seat would have to be labelled with
one of the three real aspects, which the plan should reconcile before
stage two. Model/effort/remote-control name/system-prompt path are passed
as explicit Claude argv flags (`--model`, `--effort`, `--remote-control
<name>`, `--system-prompt-file <bundle>`) built per-launch (O,
`herdr/launch.rs` argv-construction tests), so a specific low-cost model
at medium effort is mechanically selectable. Stopping: the plan's own text
that "each closed by the pane and process the test itself holds, never by
name or pattern" matches this skill set's `testing` requirement ("stop a
process by the PID that test holds, never by a process-name or path
pattern"); Herdr's `agent get`/`pane` commands return the pane/agent ids
needed to do this, held by the test from its own start call. Not proved:
whether anything in Flow/Herdr would *bind a message route* to a
test-aspect seat — not read here (I: plan's "no message sent until
Started" plus no real role/name argues against it, but the routing code
itself was not inspected under this budget).

## 7. Budget — not provable read-only; estimate only

No live run occurred, so no measured number exists. Estimate (I, from
ordinary Claude Code session-start behavior and this seat's own visible
skill-load cost): three sequential starts, spirit + 2 more skills each,
short first prompts. Per start: session boot + skill loads roughly
30-90 seconds; total tokens per seat on the order of 10-30k (system
prompt + 3 skills + short first turn, no further conversation) at the
least-costly model. Three starts sequential: well under 10 minutes
wall-clock, well under 100k tokens total. Bounds to apply per run: a
wall-clock timeout (e.g. 3-5 minutes per start) and a memory cap via a
transient systemd scope/cgroup, per the `claude-harness` skill's note that
long-running launched processes should run detached with their own memory
cap.

## 8. What could refuse the test — proved (from record), not re-tested

`claude-harness` skill's operators' notes record the Claude Code auto-mode
classifier refusing `claude --bg` launches and a `--bg --resume`, both at
15:06-15:17 UTC 2026-09-17, and separately a worktree-isolation guard
refusing `jj git clone --colocate` outside its own worktree. These are
prior, recorded refusals, not re-produced here (O, as a citation; not
re-witnessed live). Applicability to *this* environment (launched from a
Herdr pane, not `--bg`) is unknown (U) — the plan's route (`herdr agent
start` inside an existing pane, not a backgrounded `claude` process) may
not trigger the same classifier path, but this is inference, not proof.

## Stage-two procedure, as this seat would run it

1. Build Flow at bc464e5e (`nix build .#flow-nexus` or `cargo build
   --release --locked` in a scratch checkout of the tag) — the one step
   stage one leaves undone. Record the binary's path and confirm its
   `--version` string and/or embedded revision.
2. Before: record live stable/next store sizes+mtimes and confirm both
   live sockets present and accepting connections (a benign no-op query
   against each, e.g. `herdr`-independent `flow` CLI query against the
   *scratch* endpoint only — never touch the live ones beyond `stat`/`ls`).
3. Create a fresh scratch directory tree; export `HOME=<scratch>` and
   `XDG_RUNTIME_DIR=<scratch>/run` for the child process only (not this
   seat's own environment); launch the built `flow-nexus` under a
   transient systemd user scope with a memory cap and record its PID.
4. Confirm the scratch store/sockets exist under the scratch tree only,
   and that both live sockets/stores are unchanged in size/mtime.
5. Through the scratch instance's own `flow`/CLI client (pointed at the
   scratch sockets), run the three live starts A, B, C from the plan
   (and, once passing, the fail-first cases D-K from the amendment), each
   under the timeout/memory bounds, waiting on the observed Started/
   Ambiguous/Failed state, never the clock.
6. For each start: read the seat's own native transcript (oracle outside
   Flow) for the byte-exact first entry, skill-expansion order, and
   model/effort; compare to Flow's own recorded verdict.
7. Stop each seat by the pane/process id the test itself holds (never by
   name/pattern); close its pane.
8. Stop the scratch `flow-nexus` process by its recorded PID; remove the
   scratch directory tree.
9. After: re-check live stable/next store sizes+mtimes and live socket
   presence/reachability match step 2 exactly, and that no new Herdr
   workspace/pane/agent belonging to the scratch run remains registered.

## Verdict

Stage two **may proceed after** one named step: building Flow 0.17.4 (item
4) is required before any start can run, and the plan's "test aspect that
is no real role" (item 6) should be reconciled against `FlowAspect`'s
apparent three-variant closed enum before the seats are labelled, so the
launch does not silently claim a real Psyche/Mind/Field role. Nothing
found here would make the isolation itself unsafe (item 5 is proved from
source and the accidental live-store contention above independently
confirms concurrent-open is refused, not merged); item 3 needs no
caller-side terminal. Budget (item 7) is small on any plausible estimate.
Item 8's known refusals are precedent, not a proof of safety or of
failure, for this specific launch route.

## Sources

- flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md
- flows/8904b1/reports/flow-0174-semantic-review.md
- This seat's own environment and `herdr session/workspace/agent list` output.
- `systemctl --user cat flow-nexus.service`, `flow-nexus-next.service` (read-only).
- `ls -la` on `/home/li/.local/state/flow{,-next/.local/state/flow}` and `/run/user/1001/flow{,-next/flow}` (names/sizes/times only).
- `/git/github.com/LiGoldragon/flow` at `bc464e5e...` (tag `flow-0.17.4`): `crates/flow-nexus/src/main.rs`, `store.rs`, `herdr/launch.rs`, `composition.rs`, `Cargo.toml`.
- `.claude/skills/claude-harness` operators' notes (background-launch and worktree-guard refusals, 2026-09-16/17).
- Nix store search for `flow-0.17.4` build outputs (negative).
