# 21 - Sandbox full-engine testing gap review

*Designer-assistant report, 2026-05-11. Read-only review of what is
still missing before the `persona-engine-sandbox` path can run a real
full Persona engine test. Grounded in designer/125, designer/126,
designer/127, designer/129, operator-assistant/107, and the current
implementation in `/git/github.com/LiGoldragon/persona` plus the active
component repos.*

## 0 - Position

The sandbox-auth work is useful, but it is not yet a full-engine test
starter.

What exists now is a sandbox envelope:

- per-run sandbox directory layout;
- dedicated credential-root policy for Codex, Claude, Codex API, and Pi;
- systemd-run command generation;
- host Ghostty attach command generation;
- dry-run and artifact checks.

What does not exist yet is the actual full engine inside that envelope:

```text
persona-daemon
  -> engine instance
  -> persona-mind
  -> persona-router
  -> persona-message
  -> persona-harness
  -> persona-terminal
  -> terminal-cell
  -> real agent CLI
```

So the honest label for the current state is: **sandbox/auth envelope
implemented; full engine composition missing**.

## 1 - Canonical target

The current architecture target is designer/129's full sandboxed
federation: one fresh engine instance under `systemd-run --user`, with
a real message moving through `persona-message -> persona-router ->
persona-mind adjudication -> persona-harness -> persona-terminal ->
terminal-cell -> real agent`.

The target is also constrained by the recent terminal decisions:

- designer/127 says terminal injection safety is local to
  persona-terminal / terminal-cell: lock input gate, cache human bytes,
  check prompt state, inject, release, replay cache.
- designer/126 T9 says terminal-cell speaks `signal-persona-terminal`
  on the control plane while the attached viewer data plane stays raw.
- designer/125 says trust is filesystem ACL on sockets; origin is a
  message tag; router enforces authorized channel state; mind
  choreographs grants.

The sandbox test is therefore not allowed to become a fixture-only loop.
It has to start real daemons, pass real Signal frames, expose real
sockets, and leave artifacts that prove the path used production code.

## 2 - What operator's sandbox stack actually does

### 2.1 The runner stops at "inside-unit ready"

`/git/github.com/LiGoldragon/persona/scripts/persona-engine-sandbox`
prepares layout, writes manifests, writes harness env files, and then
prints readiness when invoked inside the systemd unit:

- layout: lines 99-102 create `state`, `run`, `home`, `work`,
  `artifacts`, `.claude`, `.codex`, `pi`, and `pi-session`;
- dedicated credential artifacts: lines 161-237;
- systemd-run command: lines 351-389;
- inside-unit behavior: lines 395-402.

The load-bearing gap is lines 395-402: `run_inside_unit` does not start
`persona-daemon`, `persona-dev-stack`, `persona-mind`,
`persona-router`, `persona-harness`, `persona-terminal`,
`terminal-cell`, or any real agent CLI. It just writes artifacts and
exits.

### 2.2 The auth witness is dry-run heavy

`/git/github.com/LiGoldragon/persona/scripts/persona-engine-sandbox-auth-isolation-witness`
creates fake host credential/session files at lines 15-18, then calls
`persona-engine-sandbox --dry-run` at lines 36-43.

That proves host files are not copied into dry-run artifacts. It does
not prove:

- an authenticated Codex or Claude CLI can run inside the systemd unit;
- the dedicated credential directory is readable after
  `ProtectHome=tmpfs`;
- host sessions remain untouched after a real prompt-bearing command;
- the sandbox can launch a real agent and receive a response.

This witness is still valuable. It is just not the credential-live-run
witness.

### 2.3 The attach helper points at a socket no current runner creates

`/git/github.com/LiGoldragon/persona/scripts/persona-engine-sandbox-attach`
defaults to `$sandbox/run/cell.sock` at lines 56-63 and launches
`ghostty -e terminal-cell-view --socket "$socket"` at lines 74-83.

But `persona-engine-sandbox` never starts a terminal-cell daemon at
that socket. The non-dry attach path correctly rejects missing sockets
at lines 114-117. So `primary-i10.4` is open for the right reason:
there is no sandbox `cell.sock` to attach to yet.

### 2.4 The dev stack is a useful smoke, not the engine

`/git/github.com/LiGoldragon/persona/scripts/persona-dev-stack` starts
only:

- `persona-router-daemon`;
- `persona-terminal-daemon`;
- an echo shell child inside persona-terminal.

Evidence:

- required packages are only message, router, and terminal at lines
  4-7;
- router starts at lines 71-75;
- terminal starts at lines 77-88 with an inline shell that echoes
  `terminal-echo:<line>`;
- smoke sends a message and terminal input at lines 100-140.

It does not start `persona-daemon`, `persona-mind`, `persona-harness`,
`terminal-cell-daemon` as a visible socket, or a real Codex/Claude/Pi
agent. It is a good lower-stack smoke, but not the full engine.

### 2.5 The flake checks mostly inspect generated artifacts

`/git/github.com/LiGoldragon/persona/flake.nix` exposes the sandbox
apps at lines 70-89 and checks dry-run artifacts at lines 192-335.
The current checks verify script existence, manifest content, bootstrap
artifacts, no host-auth copy in dry-run, attach command shape, and a
documented bwrap profile.

Those checks are good for the envelope. They do not run the systemd unit
with live daemons.

## 3 - Component readiness facts

### 3.1 `persona` daemon is still a manager-state daemon, not an engine spawner

Current `persona-daemon` accepts requests over a Unix socket and routes
them to `EngineManager`. The daemon binds the socket and starts the
manager at `/git/github.com/LiGoldragon/persona/src/transport.rs`
lines 180-196.

`EngineManager` can answer status and mutate desired component state:

- status/start/stop handling is in
  `/git/github.com/LiGoldragon/persona/src/manager.rs` lines 82-100;
- persisted manager records live in
  `/git/github.com/LiGoldragon/persona/src/manager_store.rs`.

But "start component" today means "change desired state in the manager
record." It does not fork/exec the component. There is no component
launcher in `src/`, no process tree, no socket permission application,
and no real engine instance lifecycle.

The engine layout types are ahead of the process runtime:

- `EngineComponent::first_stack()` names the six components at
  `/git/github.com/LiGoldragon/persona/src/engine.rs` lines 148-158;
- socket names and modes are defined at lines 171-200;
- `ComponentSpawnEnvelope` exists at lines 274-331.

Those are the right nouns. The missing piece is the actor that turns
those nouns into running child processes.

### 3.2 `persona-router` is closer than older reports imply, but the live mind bridge is not there

Router now has channel state, adjudication outbox, and mind grant/deny
application records. Evidence in `/git/github.com/LiGoldragon/persona-router`:

- `RouterInput` includes `GrantChannel`, `RetractChannel`,
  `InstallStructuralChannels`, `ApplyMindChannelGrant`, and
  `ApplyMindAdjudicationDeny` in `src/router.rs` lines 1627-1635;
- unknown channels record adjudication requests and keep the message
  pending at lines 680-704;
- mind grant projection exists at lines 1558-1619;
- router daemon CLI accepts `daemon --socket --store` at lines
  899-938.

The missing piece is a live bridge where router sends its
`signal-persona-mind` adjudication request to a running `persona-mind`
daemon and receives the grant/deny back. Current router logic can apply
a mind grant when something supplies one; the full engine needs the
wire subscription / request path between the router daemon and the mind
daemon.

### 3.3 `persona-mind` has a daemon, but not the channel-choreography surface wired into router

`persona-mind` has the correct daemon-first shape:

- `mind daemon --socket --store` is in
  `/git/github.com/LiGoldragon/persona-mind/src/command.rs` lines
  32-84;
- the daemon accepts Signal frames and submits them to `MindRoot` in
  `/git/github.com/LiGoldragon/persona-mind/src/transport.rs` lines
  198-224.

But the searched surface is still the role/work graph. I did not find a
live `AdjudicationRequest -> ChannelGrant / AdjudicationDeny` daemon
flow in `persona-mind`. Without that, the full message path can either:

- preinstall a structural channel and bypass adjudication for the first
  smoke; or
- stop at "router parked the message and emitted an adjudication
  request."

The first full-engine witness needs the second half: mind consumes the
request and router receives the grant.

### 3.4 `persona-harness` is a library, not a daemon

`/git/github.com/LiGoldragon/persona-harness/Cargo.toml` has only a
library target at lines 11-13. No `[[bin]]`, no socket daemon, no
durable harness store.

`HarnessKind` is now closed (`Codex`, `Claude`, `Pi`) in
`src/harness.rs` lines 18-23, which matches designer/127. But there is
no harness daemon to:

- register harness identity and lifecycle;
- publish prompt patterns;
- produce typed transcript observations and sequence pointers;
- own per-harness durable state;
- bridge router delivery into terminal injection.

For a first sandbox smoke, the stack can bypass the harness daemon and
launch the agent directly as the terminal child. That is not the full
architecture. The full engine needs T7's harness daemon.

### 3.5 `terminal-cell` is ready enough; `persona-terminal` has not caught up

`terminal-cell` is the strongest low-level piece right now. Its
architecture says it has:

- raw attach byte path;
- input gate;
- `signal-persona-terminal` control frames;
- prompt patterns;
- write injection;
- worker lifecycle subscription.

See `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md` lines
8-32, 79-83, and 153-164.

The contract also has the needed records in
`/git/github.com/LiGoldragon/signal-persona-terminal/src/lib.rs`:

- `PromptPattern` and registration records at lines 130-204;
- `AcquireInputGate`, `ReleaseInputGate`, `WriteInjection`, and
  `PromptState` at lines 237-262;
- the request/reply channel includes those variants at lines 463-497.

`persona-terminal` is behind that contract. Its `persona-terminal-signal`
CLI still exposes only `connect`, `input`, `prompt`, `capture`, and
`resize` in `/git/github.com/LiGoldragon/persona-terminal/src/signal_cli.rs`
lines 56-63. It imports old `TerminalInput` / `TerminalCapture` /
`TerminalResize` request shapes at lines 5-10, but not the gate,
prompt-pattern, injection, or worker-lifecycle records.

`persona-terminal` does embed terminal-cell and can launch a PTY child
from a command at `/git/github.com/LiGoldragon/persona-terminal/src/pty.rs`
lines 74-103. That is enough for a direct terminal smoke. It is not yet
enough for the designed gate-and-cache supervisor path.

## 4 - Missing before "full engine testing" can start

### 4.1 A real stack launcher inside `persona-engine-sandbox`

`run_inside_unit` must stop being a manifest writer and become an engine
starter. Minimum production-shaped behavior:

1. create the sandbox layout;
2. source `harness-env.sh`;
3. set engine-scoped env vars;
4. start the chosen stack runner;
5. keep the unit alive while the engine runs;
6. write a process manifest and socket manifest into artifacts;
7. cleanly stop children on unit shutdown.

This can start incremental:

- first run `persona-dev-stack smoke` inside the systemd unit, proving
  the envelope executes real component daemons;
- then run a terminal-cell live-agent stack inside the unit, proving
  `$sandbox/run/cell.sock` exists and host Ghostty can attach;
- then replace the dev stack with the full engine composition as
  component daemons land.

### 4.2 Component launcher in `persona-daemon`

The `persona` crate already has the right data vocabulary:
engine-scoped paths, component socket modes, and spawn envelopes. It
needs the actual runtime actor that:

- creates engine state/run directories;
- creates sockets with the correct modes or starts daemons with
  precomputed socket paths and then verifies modes;
- fork/execs each component with the spawn envelope;
- records child PIDs and health;
- shuts down components in reverse dependency order;
- exposes current component health through the existing daemon socket.

Until this exists, the sandbox must use a shell stack runner. That is
acceptable as an interim witness, but it should be named "stack runner,"
not "full engine manager."

### 4.3 A harness daemon or an explicit temporary bypass

Full architecture requires `persona-harness` as a daemon. It is not
there. The implementation needs either:

- T7: a harness daemon with identity, prompt pattern publication,
  transcript pointer publication, and delivery-to-terminal injection; or
- a named temporary bypass for the first sandbox witness:
  `persona-terminal` runs Codex/Claude/Pi directly as the PTY child,
  and the test labels itself "terminal live-agent sandbox smoke," not
  "full engine."

The second path is useful, but it does not close full-engine testing.

### 4.4 Router-to-mind live adjudication

Router can now park and apply grants. Mind can run as a daemon. The
missing path is the live channel between them:

```text
router unknown channel
  -> signal-persona-mind AdjudicationRequest
  -> mind decision
  -> signal-persona-mind ChannelGrant or AdjudicationDeny
  -> router applies grant/deny
  -> parked message releases or closes
```

For the very first end-to-end smoke, preinstalled structural channels
can let one message flow without adjudication. But the first
architecture-complete witness must exercise this bridge.

### 4.5 Persona-terminal supervisor integration with terminal-cell Signal control

`terminal-cell` can speak the control records now. `persona-terminal`
needs to consume them and become the per-engine supervisor:

- session registry and state table;
- per-cell `cell.sock` path export;
- prompt-pattern registration;
- acquire-gate / write-injection / release-gate flow;
- worker lifecycle subscription;
- typed terminal observations and sequence pointers;
- attach metadata for host Ghostty.

This is the missing link between "terminal-cell primitive works" and
"Persona terminal component owns terminal sessions."

### 4.6 A real live-auth witness

The settled auth decision is dedicated auth, not host auth copying.
The missing witness sequence is:

1. run `persona-engine-sandbox --bootstrap-auth --harness codex`
   once and authenticate into dedicated `CODEX_HOME`;
2. run an actual systemd unit using that dedicated credential root;
3. execute a small non-destructive Codex prompt from inside the unit;
4. prove the host `~/.codex` session files did not change;
5. repeat the shape for Claude token-file or dedicated
   `CLAUDE_CONFIG_DIR`.

This must be a named Nix app or script, not a remembered manual
command. It can be stateful and non-pure; the test contract is that it
is versioned and Nix-entered.

### 4.7 A full-engine driver with inspectable artifacts

The final sandbox test needs a driver that leaves evidence at each
boundary:

- systemd unit id;
- process tree;
- socket manifest and modes;
- component readiness lines;
- message frame bytes or decoded NOTA artifacts;
- router channel/adjudication artifacts;
- mind decision artifacts;
- terminal-cell transcript;
- host attach artifact;
- credential isolation digest before/after.

One huge "send prompt and grep answer" is too weak. The test should be
chained: each phase emits an artifact, and the next phase consumes the
real artifact rather than sharing in-memory state.

## 5 - Small documentation drift to clean up

Designer/129 still has older language in its TL;DR about Codex
`SnapshotCredential` and `model_reasoning_effort = "minimal"`. The
implementation and the settled decision are now different:

- Codex prompt-bearing sandbox uses dedicated `CODEX_HOME` and
  `codex login --device-auth`;
- the checked-in Codex config uses `model_reasoning_effort = "low"`.

This is not an implementation blocker, but it is a reading-order hazard
because designer/129 is the sandbox architecture entrypoint. Either
designer/129 should be edited, or this report should be treated as the
post-operator gap note.

## 6 - Recommended next work order

1. **Turn `persona-engine-sandbox` into a real runner for the existing
   dev stack.** Inside the systemd unit, run `persona-dev-stack smoke`
   with `PERSONA_STACK_ROOT=$sandbox_dir/state/dev-stack`. This proves
   the systemd envelope runs real daemons and writes real artifacts.
2. **Add a terminal-cell live-agent sandbox smoke.** Start
   `terminal-cell-daemon --socket "$sandbox_dir/run/cell.sock"` inside
   the unit with the selected harness command as child. Use
   `persona-engine-sandbox-attach` from the host. This closes the open
   attach gap and proves dedicated auth can drive a real agent inside
   the sandbox.
3. **Wire persona-terminal to terminal-cell's Signal control plane.**
   This turns the terminal smoke into the designed T6/T9 path.
4. **Add harness daemon or make the bypass explicit.** If bypassing,
   name it and do not call the witness full-engine.
5. **Wire router-to-mind adjudication live.** Use preinstalled
   structural channels only for the earliest smoke; full architecture
   needs adjudication.
6. **Move component launching into `persona-daemon`.** Retire the shell
   stack runner once the engine manager can spawn the component set
   itself.

## 7 - Suggested BEADS

These are operator-shaped, not designer-assistant-owned:

- `role:operator` - make `persona-engine-sandbox --inside-unit` run
  `persona-dev-stack smoke` and emit a process/socket artifact bundle.
- `role:operator` - add sandbox terminal-cell live-agent smoke with
  real `$sandbox/run/cell.sock`, host Ghostty attach, and transcript
  artifact.
- `role:operator` - add live dedicated-auth witness for Codex
  `CODEX_HOME` and Claude token/config isolation.
- `role:operator` - implement `persona-daemon` component launcher from
  `ComponentSpawnEnvelope`.
- `role:operator` - wire router unknown-channel adjudication to
  `persona-mind` daemon over `signal-persona-mind`.
- `role:operator` - add `persona-harness` daemon or write the temporary
  direct-terminal bypass into the sandbox test name and artifacts.

## 8 - Bottom line

The next missing thing is not more auth research. It is the first
production-code run inside the sandbox envelope.

The smallest honest next witness is:

```text
persona-engine-sandbox
  -> systemd unit
  -> start real terminal-cell daemon at $sandbox/run/cell.sock
  -> run one real harness CLI as child
  -> host Ghostty attaches
  -> test driver injects a prompt
  -> transcript artifact proves response
  -> before/after digests prove host auth/session isolation
```

That still is not the full Persona engine, but it is the right bridge
from today's envelope to the eventual full-engine witness. After that,
the work is component composition: persona-daemon launcher,
persona-terminal supervisor, persona-harness daemon, and router/mind
adjudication.
