# Investigation 6 — The orchestrate tools situation

Read-only forensic pass. Question from the psyche:

> Are there two orchestrate tools (one in primary)? Did we switch to using
> the dedicated-repo daemon-triad one? Or did an agent port the triad to
> the old tool in primary?

## Direct answer

There are **two artifacts but one architecture, and it is NOT a
duplication**. The workspace has switched to the dedicated
daemon-triad. Concretely:

- `/home/li/primary/orchestrate-cli/` is a **thin client** — a
  compatibility shim that translates the old `claim/release/status` argv
  shape into typed `signal-orchestrate` requests and sends them over a
  Unix socket. It has **no store, no redb dependency, no `tables.rs`, no
  domain logic.**
- `/git/github.com/LiGoldragon/orchestrate` is the **real triad
  component** — the `orchestrate-daemon` that owns the redb store, the
  claim/role/repository/activity tables, the lock-file projection, and
  the full SEMA/Nexus schema runtime. The full triad exists:
  `orchestrate` + `signal-orchestrate` + `meta-signal-orchestrate`, all
  present and depended upon.

So: the workspace **switched to the dedicated daemon-triad**. An agent
did **not** port triad logic into primary. `primary/orchestrate-cli` is a
**client of** `/git/orchestrate`, **not a fork of it**.

## The wave-1 stream C claim is wrong (and right)

Stream C claimed "tools/orchestrate is already the persona-orchestrate
component." That is imprecise and misleading:

- **Wrong**: `tools/orchestrate` is a 24-line bash shim, and
  `orchestrate-cli/` behind it is a client, not "the component." The
  component (daemon + store + schema runtime) lives in `/git`.
- **Right in spirit**: invoking `tools/orchestrate` *does* now drive the
  real persona-orchestrate component end-to-end — it spawns and talks to
  the `/git` daemon. The user-facing path is the real component; the
  primary-side code is just its launcher and argv adapter.

## Evidence

### (a) The shim — `/home/li/primary/tools/orchestrate`

24-line bash. Resolves `orchestrate-cli/target/release/orchestrate`,
builds it on first use, then `exec`s it. Its own comment:

> "The Rust port owns the claim / release / status flows; this script is
> the workspace-stable path agents reach for."

### (b) `orchestrate-cli` is a pure client, not a self-contained store

`Cargo.toml` description: *"Workspace coordination helper —
**compatibility surface over the orchestrate daemon**."* Dependencies are
`signal-orchestrate`, `meta-signal-orchestrate`, `signal-frame`,
`nota-next`, `rkyv`, `thiserror`. **No `redb`. No `sema`.**

- `find orchestrate-cli -name tables.rs` → none.
- `grep redb src/` → a single hit: a **path string**
  (`store_path: state.join("orchestrate.redb")`) passed to the daemon as
  config. It never opens a database.
- `src/daemon_client.rs` (281 lines) is the whole mechanism:
  - `OrchestrateDaemonClient::from_workspace` points at
    `<ws>/orchestrate/{orchestrate.redb, orchestrate.sock,
    orchestrate-owner.sock, orchestrate-upgrade.sock}` and
    `git_index_root = /git/github.com/LiGoldragon`.
  - `ensure_ready` → if it can't `UnixStream::connect` the socket, it
    builds (`cargo build --release ... --bin orchestrate --bin
    orchestrate-daemon`) and `spawn`s the daemon from
    `ORCHESTRATE_COMPONENT_ROOT`, defaulting to
    `/git/github.com/LiGoldragon/orchestrate`.
  - `submit_text` runs the `/git`-built `orchestrate` thin CLI with
    `PERSONA_ORCHESTRATE_SOCKET` set and the request as one NOTA argv,
    then decodes the NOTA reply.
  - Startup is a single **rkyv** `StartupConfiguration` written to
    `orchestrate/orchestrate-daemon.signal` and handed to the daemon as
    its one argument — matching the one-argument / binary-startup
    component rule.
- `src/bin/orchestrate.rs` header is explicit: *"The daemon owns durable
  state and projects lock files back into
  `<workspace>/orchestrate/<lane>.lock`."* `daemon_status` issues an
  observation request and reads a `RoleSnapshot` reply — it does not read
  any local store.
- `src/claim.rs` (178 lines) is argv→signal projection + render DTOs,
  not store logic. Largest file is `verify_jj.rs` (618), which is
  jj-bookmark verification, unrelated to any store.

### (c) The dedicated `/git` triad is the real component

`/git/github.com/LiGoldragon/orchestrate` `Cargo.toml` (v0.4.1,
*"Typed orchestration state for Persona agents"*) declares three bins:
`orchestrate-daemon` (`src/main.rs`), `orchestrate` (thin ordinary CLI),
`meta-orchestrate` (thin meta CLI). Deps include `sema-engine`,
`signal-sema`, `triad-runtime`, `signal-version-handover`,
`version-projection`, `tokio`, and **`redb 4.1.0`** (in its Cargo.lock).
Source has `tables.rs`, `service.rs`, `daemon.rs`, `lock_projection.rs`,
`legacy_lock_import.rs`, `repository.rs`, plus a generated
`src/schema/{nexus,sema,daemon}.rs`.

- `service.rs`: `OrchestrateService::open` → `OrchestrateTables::open(store)`
  — the daemon opens the redb.
- Full triad present:
  `signal-orchestrate` and `meta-signal-orchestrate` both exist with
  schema-emitted `src/`.

### (d) Source of truth = the daemon's redb; lock files are a projection

- A live `orchestrate-daemon` is **running**: PID 653243,
  `/git/.../orchestrate/target/release/orchestrate-daemon
  /home/li/primary/orchestrate/orchestrate-daemon.signal`, holding the
  `LISTEN` end of `orchestrate.sock` (confirmed via `lsof`).
- **No systemd unit** (user or system). The daemon is **CLI-spawned** by
  `orchestrate-cli` on first connect — lazy, not a managed service.
- `/home/li/primary/orchestrate/orchestrate.redb` (~1.3 MB) is the
  daemon's store (the path the client passes in). A
  `orchestrate.redb.pre-nota-next-20260618103416` backup sits beside it
  from a wire migration.
- The `*.lock` files are **projected by the daemon**, not authored by
  agents. `lock_projection.rs` `LockProjection::project` reads
  `claim_records()` from the tables and `std::fs::write`s each
  `<role>.lock`. Live proof: `system-designer.lock` and
  `cloud-operator.lock` carry multi-line claims with `# reason` glosses
  that match the redb claim shape. `legacy_lock_import.rs`
  (`import_if_store_has_no_claims`) imports the old bash-era flat locks
  **once** into the store on first open — confirming the direction of
  truth flipped from files→store (bash era) to store→files (now).
- INTENT.md states it outright: *"Do not let compatibility lock files
  become a second state model after daemon cutover. **The daemon store is
  the source of truth.**"*

### Git history — evolution, not duplication

`git log` on `orchestrate-cli/` and `tools/orchestrate` shows the arc:

- `1730087a` — *"orchestrate-cli — rust port of tools/orchestrate"*: the
  shim flipped from bash to a Rust binary (initially self-contained,
  bash-era model).
- `f1d8d317` — *"point orchestrate cli at orchestrate contract"*: pivot
  to consuming `signal-orchestrate` types.
- `a903edf7` — *"orchestrate: document daemon-backed helper"*.
- `6a10678c` / `acaa893c` / `6d14de26` / `0ae84222` — daemon startup
  config drain, encode errors, schema CLI transport, schema release.

The code does not mirror the daemon's store internals at any point; it
mirrors the daemon's **wire contract** (signal-orchestrate). This is a
client that grew up alongside the component, not a copy of it.

## One operational note (not architectural)

The daemon log is spammed with `daemon frame error: frame IO error:
early eof` (every recent line). The architecture is sound, but the
daemon's connection/frame handling is logging an error on what looks
like normal client disconnects (the client invokes the short-lived
`orchestrate` thin CLI per request rather than holding the socket). Worth
a maintainer/operator follow-up, but it does not change this answer.

## What this means for Decision eh5a (worktree registry)

The daemon **already owns a repository registry**. `repository.rs`
`RepositoryRegistry::refresh` scans `git_index_root`
(`/git/github.com/LiGoldragon`), creates `repos/<name>` symlinks into the
workspace, and persists `StoredRepository` rows in redb, replying with a
meta-signal `RepositoryIndexRefreshed`. There is **no worktree concept
yet** (`grep -ri worktree` over `/git/orchestrate/src` → empty).

So the worktree registry is a **natural extension of an existing
daemon-owned surface**, not a greenfield decision about *where*.

## Recommendation

**Build the eh5a worktree registry in the dedicated `/git` orchestrate
triad as a client-facing feature. Do NOT extend `primary/orchestrate-cli`,
and there is no duplication to reconcile first.**

Rationale:

1. There is no duplication — `orchestrate-cli` is a thin client with zero
   store logic. Nothing to reconcile.
2. The daemon already owns repository/git-index state, redb persistence,
   lock-file projection, and the meta-signal surface
   (`RepositoryIndexRefreshed`). Worktrees are the same kind of
   filesystem-discovered, store-persisted entity — model
   `StoredWorktree` next to `StoredRepository`, extend
   `RepositoryRegistry` (or a sibling `WorktreeRegistry`), and add wire
   roots/replies to the appropriate contract.
3. Worktree registration is a **policy/meta operation** (registering and
   refreshing the worktree set under `~/wt/...`), so the wire roots
   belong in **`meta-signal-orchestrate`** alongside the existing
   repository-refresh meta signal, with the daemon projecting any
   human-facing view.
4. `orchestrate-cli` then gets, at most, a thin argv adapter if agents
   need a `claim`-style ergonomic entry point — but the registry itself,
   its types, and its persistence live in the component. This honors
   INTENT.md's anti-pattern ("Do not deepen the transitional shell
   helper") and its boundary ("`orchestrate` owns machinery").

## Relevant files (absolute)

- `/home/li/primary/tools/orchestrate` — bash shim → execs Rust client.
- `/home/li/primary/orchestrate-cli/Cargo.toml` — *"compatibility surface
  over the orchestrate daemon"*; no redb/sema deps.
- `/home/li/primary/orchestrate-cli/src/daemon_client.rs` — spawns +
  talks to `/git` daemon over the socket; the whole client mechanism.
- `/home/li/primary/orchestrate-cli/src/bin/orchestrate.rs` — argv →
  signal; reads `RoleSnapshot` from daemon.
- `/home/li/primary/orchestrate-cli/src/claim.rs` — argv→signal DTOs, no
  store logic.
- `/home/li/primary/orchestrate/orchestrate.redb` — the daemon's store
  (daemon-owned, lives under primary for locality).
- `/home/li/primary/orchestrate/*.lock` — daemon-projected, not
  agent-authored.
- `/home/li/primary/orchestrate/orchestrate-daemon.log` — running
  daemon's log (note the `early eof` spam).
- `/git/github.com/LiGoldragon/orchestrate/Cargo.toml` — the real
  component; three bins, redb, sema-engine, triad-runtime.
- `/git/github.com/LiGoldragon/orchestrate/src/service.rs` — `open` →
  `OrchestrateTables::open` (daemon owns redb).
- `/git/github.com/LiGoldragon/orchestrate/src/lock_projection.rs` —
  writes the `<role>.lock` files from the store.
- `/git/github.com/LiGoldragon/orchestrate/src/legacy_lock_import.rs` —
  one-time bash-era flat-lock import (truth direction flipped).
- `/git/github.com/LiGoldragon/orchestrate/src/repository.rs` —
  existing repository registry; the surface eh5a should extend.
- `/git/github.com/LiGoldragon/orchestrate/INTENT.md` — "The daemon store
  is the source of truth"; component vs shim boundary.
