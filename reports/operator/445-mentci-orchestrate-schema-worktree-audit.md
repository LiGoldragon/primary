# 445 — Operator follow-up to designer report 707

## Scope

The psyche asked whether designer report 707 affects the operator lane and asked
three factual follow-ups:

- what happened historically with `mentci-lib`;
- whether `tools/orchestrate` is primary-local or the dedicated orchestrate
  daemon triad;
- what the two unowned `schema-rust-next` worktrees contain, whether main already
  has the work, and how exposed they are.

## Operator impact

Report 707 changes the operator order. The next Mentci implementation slice
should not start with more `mentci-egui` widgets. It should first reconcile the
shared model:

1. re-found `mentci-lib` on the live `signal-mentci` /
   `meta-signal-mentci` / criome contracts;
2. use that shared model from the daemon CLI and GUI;
3. then build the approval card and VM proof.

The worktree registry belongs in the real `orchestrate` triad, with primary's
`tools/orchestrate` remaining the compatibility argv client.

The two unowned `schema-rust-next` trees are protected work. They are not GC
candidates.

## mentci-lib history

`mentci-lib` started on April 29, 2026 as a heavy MVU-style workbench library
for a different stage of the system: direct criome/sema introspection plus a
second nexus rendering connection over the old `signal` graph vocabulary. The
initial commit created `WorkbenchState`, `WorkbenchView`, `UserEvent`,
`EngineEvent`, `Cmd`, graph canvas state, constructor flows, and a dual
`Criome`/`Nexus` connection driver.

April 29 follow-up commits made the old model runnable: Unix socket handshake,
query/subscribe-style graph/node/edge loading, graph canvas rendering, and
constructor flow examples. Those commits targeted a live criome graph/sema
surface, not today's Mentci daemon.

June 18 commits added approval state, approval subscriptions, edited-answer
proposal modeling, and component-triad intent text. They did not repoint the
crate onto `signal-mentci` or make the daemon/egui consume it. The June 19 commit
is only a build-tool repin.

Current reality:

- `mentci-lib` depends on `signal`, not `signal-mentci`.
- It still has `DaemonRole::Criome | Nexus`.
- It duplicates approval nouns now owned by `signal-mentci`.
- `mentci` and `mentci-egui` do not depend on it.

So the history is not "the daemon forgot to use the right library." The library
predates the current daemon triad, then intent moved under it. The correct
operator move is to re-found it on the live contracts, not to force the daemon or
GUI back to the stale graph-signal model.

## orchestrate tool shape

There are two code surfaces but one live state owner.

Primary's `/home/li/primary/tools/orchestrate` is a 21-line shell shim. It builds
and execs `/home/li/primary/orchestrate-cli/target/release/orchestrate`.

`/home/li/primary/orchestrate-cli` is a compatibility client crate. It accepts
the old argv shape (`claim`, `release`, `status`, `verify-jj`), translates it
into `signal-orchestrate` requests, starts the daemon if needed, and renders the
daemon-projected lock files. Its `daemon_client.rs` defaults
`ORCHESTRATE_COMPONENT_ROOT` to `/git/github.com/LiGoldragon/orchestrate`, builds
that repo's release `orchestrate` and `orchestrate-daemon` binaries if missing,
writes the daemon startup rkyv file, and spawns the daemon.

`/git/github.com/LiGoldragon/orchestrate` is the actual daemon triad runtime
repo: ordinary and meta clients, daemon, schemas, sema/redb tables, lock-file
projection, repository registry, and generated Nexus/SEMA runtime.

So the answer is: an agent ported the old primary helper into a primary-local
compatibility client that drives the dedicated orchestrate daemon triad. We have
not simply switched `tools/orchestrate` to exec the repo's thin one-argument CLI,
because it still preserves the old multi-argument agent ergonomics. The state
owner is still the dedicated `/git/.../orchestrate` daemon.

## schema-rust-next worktrees

### `reaction-expand`

Path:
`/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand`

Unique local work:

- `a1582dfd` — `base: 660/661 composition prototype`
- `8b147fac` — `schema-capability-resolution: thread shape resolver + standard
  struct impls`

No remote bookmark descends from either commit. The local `reaction-expand`
bookmark is an empty working-copy commit above `8b147fac`, not a pushed branch.

This tree is incomplete as a runnable stack. Its `Cargo.toml` patches
`schema-next` to `../../schema-next/reaction-expand`, but that sibling worktree
does not exist. Targeted tests fail at dependency load before compiling:
`failed to read .../schema-next/reaction-expand/Cargo.toml`.

The work is not obviously on main. Current main has newer impl-catalog and
malformed-name work, but it does not contain the `composition_demo` /
`pipe_delimiter_demo` tests, fixtures, generator examples, or the explicit
`CapabilityResolver` references that this tree carries. Preserve before GC.

### `structural-forms-integration`

Path:
`/home/li/wt/github.com/LiGoldragon/schema-rust-next/structural-forms-integration`

Unique local work:

- `a0138ce1` — `schema-rust-next: migrate fixtures to positional struct-body
  syntax (advance schema-next pin to positional integration tip)`

The local bookmark is diverged from `structural-forms-integration@origin` and no
remote bookmark descends from `a0138ce1`.

This tree is internally coherent: `cargo test --all-targets --features
nota-text` passed. It is nevertheless older than current main and mostly a
fixture/dependency-pinning migration. Current main has later schema lowering
work, so this is likely superseded, but it is not an ancestor of main and should
be report-captured or pushed before any GC.

## Recommended operator actions

1. For Mentci, start a focused `mentci-lib` refoundation branch only after
   claiming `mentci-lib`, `mentci`, and `mentci-egui`. First deliverable:
   remove the stale graph-signal/dual-daemon model and expose a shared
   `signal-mentci` observation/control model that daemon and GUI can both use.
2. For orchestrate, build the worktree registry in
   `/git/github.com/LiGoldragon/orchestrate`,
   `/git/github.com/LiGoldragon/signal-orchestrate`, and
   `/git/github.com/LiGoldragon/meta-signal-orchestrate`; update primary's
   `orchestrate-cli` only as the compatibility argv adapter.
3. For schema worktrees, preserve first. Best low-risk next move is to create
   pushed preservation bookmarks for the two `schema-rust-next` trees and record
   the missing `schema-next/reaction-expand` dependency. Do not delete or recycle
   either tree until that preservation exists.
