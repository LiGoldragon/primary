# Architecture / Implementation Drift Audit - 2026-05-11

Role: designer-assistant

## Request

Read the active architecture documents and the skills that govern how we write
code, then use subagents to scour implementations for drift from architecture
and for architecture documents that disagree with each other.

## Method

I read the required workspace entry points first:

- `ESSENCE.md`
- `repos/lore/AGENTS.md`
- `protocols/orchestration.md`
- `protocols/active-repositories.md`
- required skills: `skills/autonomous-agent.md`,
  `skills/skill-editor.md`, `skills/reporting.md`, `skills/jj.md`,
  `skills/repository-management.md`

I then read the code-shape and design skills that constrain implementation:

- `skills/abstractions.md`
- `skills/actor-systems.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`
- `skills/beauty.md`
- `skills/contract-repo.md`
- `skills/kameo.md`
- `skills/language-design.md`
- `skills/micro-components.md`
- `skills/naming.md`
- `skills/nix-discipline.md`
- `skills/library.md`
- `skills/push-not-pull.md`
- `skills/rust-discipline.md`
- `skills/testing.md`
- role skills for designer, designer-assistant, operator, and
  operator-assistant

I read the active architecture set named in
`protocols/active-repositories.md`: `persona`, `persona-mind`,
`persona-router`, `persona-message`, `persona-system`, `persona-harness`,
`persona-terminal`, `terminal-cell`, `sema`, `signal-core`, `signal`,
`signal-persona`, `signal-persona-message`, `signal-persona-system`,
`signal-persona-harness`, `signal-persona-mind`, `signal-persona-terminal`,
`nexus`, `nexus-cli`, `nota`, `nota-codec`, `nota-derive`, plus adjacent
architecture docs for `criome`, `chroma`, `chronos`, `CriomOS`,
`CriomOS-home`, `horizon-rs`, and `lojix-cli`.

I also read the current vision/engine-manager reports:

- `reports/designer/114-persona-vision-as-of-2026-05-11.md`
- `reports/designer/115-persona-engine-manager-architecture.md`

Subagents split the implementation sweep across:

- Persona runtime repos: `persona`, `persona-mind`, `persona-router`,
  `persona-message`, `persona-system`, `persona-harness`
- terminal stack: `persona-terminal`, `terminal-cell`,
  `signal-persona-terminal`
- contract/text stack: `signal-core`, `signal`, `signal-persona-*`, `nota-*`,
  `nexus`, `nexus-cli`
- sema/criome/adjacent repos: `sema`, `criome`, `chroma`, `chronos`,
  `lojix-cli`, `horizon-rs`, `mentci-lib`, `CriomOS`, `CriomOS-home`

I locally rechecked their highest-signal claims with `rg` and direct source
reads. If an agent finding had already been fixed in the working tree, I
dropped it from the current finding list.

## Current Agreement Map

The active architecture documents mostly agree on these current truths:

- Actor runtime is direct Kameo today. `ractor`, `persona-actor`, and
  `workspace-actor` are stale unless a current report explicitly reopens that
  decision. See `protocols/active-repositories.md:74`.
- `persona-terminal` owns terminal byte transport around `terminal-cell`;
  terminal-brand mux helper repositories are retired. See
  `protocols/active-repositories.md:29` and
  `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md:5`.
- `terminal-cell` is the low-level PTY/transcript primitive, not the global
  Persona registry. See
  `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md:11`.
- Today's `sema` is a typed database library, rename pending to `sema-db`;
  each state-bearing component owns its own database and table layer. See
  `protocols/active-repositories.md:79`.
- Signal is the typed binary communication fabric. Component contracts live in
  dedicated `signal-*` repos.
- NOTA is the only text syntax. Nexus is typed semantic content written in NOTA
  syntax, not a second parser. See `protocols/active-repositories.md:96`.
- `persona-mind` is the central state component for orchestration and the work
  graph; lock files and BEADS are transitional. See
  `protocols/active-repositories.md:99`.

## Findings

### P1 - `persona-message` still owns retired terminal delivery

Current architecture says `persona-message` is the NOTA boundary and proxy, not
the durable ledger or terminal transport owner:

- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md:54` says the
  Signal path must not append to `messages.nota.log`.
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md:86` to
  `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md:92` says this
  repo does not own terminal byte transport.
- `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md:5` says
  `persona-terminal` is the current terminal byte transport owner.

The implementation still has active WezTerm and local-ledger paths:

- `/git/github.com/LiGoldragon/persona-message/Cargo.toml:26` depends on
  `persona-wezterm`.
- `/git/github.com/LiGoldragon/persona-message/src/delivery.rs:2` imports
  `persona_wezterm::pty`.
- `/git/github.com/LiGoldragon/persona-message/src/delivery.rs:3` imports
  `TerminalPrompt` and `WezTermMux`.
- `/git/github.com/LiGoldragon/persona-message/src/delivery.rs:77` still
  dispatches `EndpointKind::WezTermPane`.
- `/git/github.com/LiGoldragon/persona-message/src/schema.rs:191` still
  exposes `EndpointKind::WezTermPane`.
- `/git/github.com/LiGoldragon/persona-message/src/store.rs:41` still names
  `messages.nota.log`.
- `/git/github.com/LiGoldragon/persona-message/src/store.rs:235` tails that
  log with `thread::sleep(Duration::from_millis(200))`.
- `/git/github.com/LiGoldragon/persona-message/scripts/setup-harnesses:112`
  and nearby scripts still construct `EndpointTransport WezTermPane`.

This is the highest-risk drift because it keeps the old terminal path alive in
the message layer while the current architecture wants the byte path in
`persona-terminal`/`terminal-cell` and delivery policy in
`persona-router`/`persona-harness`.

Related existing bead: `primary-2w6` - "persona-message becomes
Nexus-to-router and router-to-terminal proxy".

Recommended fix: make `persona-message` a pure NOTA-to-router projection layer.
Remove `persona-wezterm`, retire `WezTermPane`, stop direct terminal delivery
from this repo, and move any still-useful harness scripts to the
`persona-terminal`/`persona-harness` path.

### P1 - `persona-router` still inherits retired terminal code through dependencies

`persona-router` source has already moved in the right direction: it rejects
`EndpointKind::WezTermPane` at
`/git/github.com/LiGoldragon/persona-router/src/harness_delivery.rs:43` and
delegates real PTY delivery through `persona-harness`.

The lock file still pulls `persona-wezterm` through the current
`persona-message` dependency:

- `/git/github.com/LiGoldragon/persona-router/Cargo.lock:458`
- `/git/github.com/LiGoldragon/persona-router/Cargo.lock:510`
- `/git/github.com/LiGoldragon/persona-router/Cargo.lock:512`

This is downstream of the `persona-message` fix. The router cannot fully shed
the retired terminal dependency until the published or pinned `persona-message`
revision sheds it.

Related existing bead: `primary-2w6`.

### P2 - Ractor and zero-sized actor markers remain in active implementation repos

The active repo map says direct Kameo is the current runtime and direct Ractor
is stale unless reopened by a current report
(`protocols/active-repositories.md:74`). The codebase still has three
implementation islands using Ractor and public zero-sized actor markers:

`criome`:

- `/git/github.com/LiGoldragon/criome/Cargo.toml:25` depends on `ractor`.
- `/git/github.com/LiGoldragon/criome/AGENTS.md:9` still describes a Ractor
  supervision tree.
- `/git/github.com/LiGoldragon/criome/src/daemon.rs:24` has `pub struct
  Daemon;`.
- `/git/github.com/LiGoldragon/criome/src/engine.rs:29` has `pub struct
  Engine;`.
- `/git/github.com/LiGoldragon/criome/src/reader.rs:22` has `pub struct
  Reader;`.

`nexus`:

- `/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md:138` already calls
  remaining Ractor implementation legacy migration debt.
- `/git/github.com/LiGoldragon/nexus/Cargo.toml:29` depends on `ractor`.
- `/git/github.com/LiGoldragon/nexus/src/daemon.rs:17` has `pub struct
  Daemon;`.
- `/git/github.com/LiGoldragon/nexus/src/listener.rs:22` has `pub struct
  Listener;`.
- `/git/github.com/LiGoldragon/nexus/src/connection.rs:33` has `pub struct
  Connection;`.

`lojix-cli`:

- `/git/github.com/LiGoldragon/lojix-cli/Cargo.toml:16` depends on `ractor`.
- `/git/github.com/LiGoldragon/lojix-cli/AGENTS.md:21` names the starting
  point as "CLI + ractor".
- `/git/github.com/LiGoldragon/lojix-cli/src/project.rs:36`,
  `/git/github.com/LiGoldragon/lojix-cli/src/build.rs:389`, and
  `/git/github.com/LiGoldragon/lojix-cli/src/copy.rs:84` use `type State =
  ();`.

Related existing beads:

- `primary-915` - `criome: migrate public ZST Ractor actors to Kameo`
- `primary-92n` - `nexus: migrate daemon actors from Ractor to Kameo`
- `primary-q3y` - `lojix-cli: migrate Ractor/ZST actors to current Kameo
  discipline`

Recommended fix: migrate these one repo at a time, keeping actor nouns
data-bearing. The public actor type should carry the durable identity, config,
ports, or counters that make the actor a real noun. Empty control messages
should also be replaced with data-bearing request records.

### P2 - Message body contracts are still opaque strings

The current semantic direction is typed Nexus content written in NOTA syntax,
not an untyped body string. The harness architecture already admits this:

- `/git/github.com/LiGoldragon/signal-persona-harness/ARCHITECTURE.md:36`
  says `MessageBody` is provisional and the destination is a typed Nexus record
  written in NOTA syntax.

The contracts still expose opaque body strings:

- `/git/github.com/LiGoldragon/signal-persona-message/src/lib.rs:45` has
  `pub struct MessageBody(String);`.
- `/git/github.com/LiGoldragon/signal-persona-message/src/lib.rs:79` documents
  the body as opaque text.
- `/git/github.com/LiGoldragon/signal-persona-harness/src/lib.rs:60` has
  `pub struct MessageBody(String);`.
- `/git/github.com/LiGoldragon/signal-persona-harness/src/lib.rs:95` carries
  that body in `MessageDelivery`.

This is known provisional design debt, but it is a contract-level debt, so it
will become expensive if implementation builds more policy around opaque text.

Related existing bead: `primary-b7i` - "Migrate body: String -> typed Nexus
record across signal-persona-message".

### P2 - `signal` still carries duplicate kernel files after `signal-core`
extraction

The `signal` architecture says the frame envelope, handshake, auth, slots, and
pattern markers moved to `signal-core`:

- `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md:40`
- `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md:135`

The source still declares and re-exports duplicate kernel modules:

- `/git/github.com/LiGoldragon/signal/src/lib.rs:43` declares `pub mod auth`.
- `/git/github.com/LiGoldragon/signal/src/lib.rs:44` declares `pub mod frame`.
- `/git/github.com/LiGoldragon/signal/src/lib.rs:45` declares `pub mod
  handshake`.
- `/git/github.com/LiGoldragon/signal/src/lib.rs:53` declares `pub mod
  pattern`.
- `/git/github.com/LiGoldragon/signal/src/lib.rs:56` declares `pub mod slot`.
- `/git/github.com/LiGoldragon/signal/src/lib.rs:69` re-exports `auth`.
- `/git/github.com/LiGoldragon/signal/src/lib.rs:70` re-exports `frame`.

The architecture already labels this as a rebalance, so this is not conceptual
confusion. It is unfinished migration work.

Related existing beads: `primary-kmr` and `primary-aww`.

### P2 - `sema` still exposes the raw-byte slot store

The active architecture wants component-owned typed table layers and no generic
untyped blob fallback for new state. `sema` currently documents the legacy
surface as compatibility:

- `/git/github.com/LiGoldragon/sema/src/lib.rs:16` describes the "Legacy slot
  store".

The public API is still present:

- `/git/github.com/LiGoldragon/sema/src/lib.rs:539` has `Sema::open`.
- `/git/github.com/LiGoldragon/sema/src/lib.rs:666` has `Sema::store(&[u8])`.
- `/git/github.com/LiGoldragon/sema/src/lib.rs:685` has `Sema::get`.
- `/git/github.com/LiGoldragon/sema/src/lib.rs:700` has `Sema::iter`.

This is acceptable only as explicitly temporary compatibility for older
`criome` code. It should not remain the easy path for new component state.

Related existing bead: `primary-6nr` - `sema: decide legacy raw-byte slot-store
retirement path`.

### P2 - `criome` subscribe architecture contradicts push discipline

`skills/push-not-pull.md:54` says every push subscription emits the producer's
current state when the consumer connects, then emits deltas. It also says the
consumer must not perform a separate query to seed itself.

`/git/github.com/LiGoldragon/criome/ARCHITECTURE.md:735` says:

```text
No initial snapshot - issue a Query first if you want current state.
```

That is a direct architecture-vs-skill conflict. The push discipline is the
better general contract because it avoids the missed-state race where a client
subscribes after state already exists and then waits forever.

Recommended fix: update `criome/ARCHITECTURE.md` so `Subscribe` sends an
initial matching `Records` snapshot followed by deltas, or explicitly document
why criome is the exception. I do not see a good reason for an exception.

No existing bead in the open list looked specific to this.

### P2 - NOTA optional-field policy conflicts between skill and repo

`skills/language-design.md:250` says tail-omitted optionals are a compatibility
read-shape and a decoder may accept missing trailing optional fields.

`/git/github.com/LiGoldragon/nota-codec/ARCHITECTURE.md:41` to
`/git/github.com/LiGoldragon/nota-codec/ARCHITECTURE.md:44` says every declared
field must appear and there is no field omission, including at the end.
`/git/github.com/LiGoldragon/nota-codec/ARCHITECTURE.md:58` to
`/git/github.com/LiGoldragon/nota-codec/ARCHITECTURE.md:78` makes this an
implementation commitment and names the regression guard.

The `nota-codec` architecture is more precise and looks like the newer
decision. The workspace skill should be updated to match it unless the user
reopens the compatibility rule.

No existing bead in the open list looked specific to this.

### P3 - Some adjacent architecture docs still use GitHub links where local
cross-references would be cleaner

`repos/lore/AGENTS.md:127` discourages deep GitHub `blob/main` links for repo
cross-references because local paths should be the working truth for agents.

Examples:

- `/git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md:40` links to
  `https://github.com/LiGoldragon/criome/blob/main/ARCHITECTURE.md`.
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md:4` links to
  GitHub `CriomOS`.
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md:11` links to
  GitHub `CriomOS-emacs`.
- `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md:57` links to GitHub
  `lojix-cli`.

This is low-risk documentation drift, but it affects agent navigation quality.

### P3 - `terminal-cell` is coherent, but its status wording is still partly
experimental

The terminal architecture and implementation are now much more aligned than
they were during the failed relay design. The current architecture correctly
documents the raw attach path, the input gate, transcript side-channel, and
the split where `persona-terminal` owns registry/Sema policy.

Minor wording still frames the repo as experimental:

- `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md:3` says "Durable
  terminal session experiments".
- `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md:8` says the repo
  "explores one narrow capability".

This is not a blocker. If the component is now accepted as the primitive under
`persona-terminal`, update status language to "low-level primitive" while
keeping the architecture history of the rejected relay path.

## Healthy Or Recently Fixed Areas

I saw several areas where the current implementation is now aligned enough to
avoid reopening old worries:

- `persona-terminal` depends on `terminal-cell`, uses component Sema tables,
  and has actor-runtime truth tests that reject non-Kameo runtime fragments.
  Evidence:
  `/git/github.com/LiGoldragon/persona-terminal/Cargo.toml:44`,
  `/git/github.com/LiGoldragon/persona-terminal/src/tables.rs:102`,
  `/git/github.com/LiGoldragon/persona-terminal/tests/actor_runtime_truth.rs:140`.
- `persona-harness` no longer depends on `persona-wezterm`; it depends on
  `persona-terminal` and `signal-persona-terminal`.
  Evidence: `/git/github.com/LiGoldragon/persona-harness/Cargo.toml:16`.
- `persona-harness` terminal delivery goes through
  `TerminalTransportBinding` and `TerminalInputBytes` rather than old WezTerm
  APIs.
  Evidence: `/git/github.com/LiGoldragon/persona-harness/src/terminal.rs:3`
  and `/git/github.com/LiGoldragon/persona-harness/src/terminal.rs:111`.
- `persona-router` delivery code rejects `WezTermPane` rather than trying to
  support it.
  Evidence: `/git/github.com/LiGoldragon/persona-router/src/harness_delivery.rs:43`.
- I did not find active `persona-actor`, `workspace-actor`, or `ActorKind`
  implementation surfaces in the current active Persona path. Mentions that
  remain are mostly negative guard tests or historical reports.

## Recommended Order

1. Finish `primary-2w6`: remove `persona-wezterm`, `WezTermPane`, direct
   terminal delivery, and local durable message assumptions from
   `persona-message`; then update `persona-router` locks/dependencies.
2. Update `criome/ARCHITECTURE.md` so `Subscribe` emits the initial snapshot
   before deltas, matching `skills/push-not-pull.md`.
3. Update `skills/language-design.md` to match `nota-codec`'s explicit `None`
   rule, unless compatibility tail omission is intentionally reopened.
4. Continue the Ractor/ZST migrations already tracked for `criome`, `nexus`,
   and `lojix-cli`.
5. Keep contract debt visible: migrate opaque message body strings to typed
   Nexus-in-NOTA records before more policy builds around body text.
6. Complete the `signal` -> `signal-core` kernel cleanup and decide the
   retirement path for `sema`'s raw slot-store API.

