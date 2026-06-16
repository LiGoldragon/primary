# BUILD H2 — Arc&lt;Engine&gt;-accepting ComponentShipper forward-ported onto mirror MAIN

Slice 2 of the 670 first-e2e-offline-unblock arc. Resolves blocker 2 from
designer 669 (`669-first-e2e-offline-build/1-p1-shipper-reland.md`): the only
`Arc<Engine>` `ComponentShipper` lived on the stale `origin/arc-shipper`
branch (pinned to nota-next 0.4.0, no longer compiling against current
signal-mirror 0.5.0). This slice forward-ports the `Arc<Engine>` capability
onto mirror MAIN — the green, deployed, nota-next-0.5.0 lineage — instead of
refreshing `arc-shipper`'s nota-next, exactly as recommended.

## Branch

- Repo: `/git/github.com/LiGoldragon/mirror`
- Worktree: `/home/li/wt/github.com/LiGoldragon/mirror/arc-shipper-mainline`
- Bookmark: `arc-shipper-mainline` at commit `6bcefa4f` (change `srrsuuor`),
  fresh off `main@origin` (`b9c171a7`, "mirror: port daemon to mainline
  schema tooling").
- NOT pushed (operator integrates).
- Scope: a single file, `src/shipper.rs` (48 insertions, 1 deletion). No
  schema change was needed — the shipper holds no schema-emitted noun in the
  changed surface; the `Arc` lives entirely in the engine-handle plumbing.

## The seam, restated

Spirit's `Store` keeps `database: Arc<sema_engine::Engine>` and writes through
it; the shipper must hold a CLONE of that SAME `Arc` so it reads the outbox
the working writes append to and records `acknowledge_mirror` back into one
engine. `sema_engine::Engine` is intentionally NOT `Clone` (it holds a
`Mutex`; it is `Send + Sync` for `Arc` sharing). Mirror main's
`ComponentShipper` took `engine: ComponentEngine` BY VALUE, so a store that
keeps its engine behind an `Arc` could not hand it over.

## API delta (additive — by-value callers stay green)

The field generalises to an `Arc`-held handle, and two SHARED constructors
join the existing two OWNING constructors. The by-value entry points keep
their exact signatures, so `tests/end_to_end_arc.rs` (which passes an owned
`source: ComponentEngine` into `ComponentShipper::new`) compiles unchanged.

| Surface | Before (main) | After (this branch) |
|---|---|---|
| field | `engine: ComponentEngine` | `engine: Arc<ComponentEngine>` |
| `new(engine: ComponentEngine, addr, store)` | owns engine | owns engine (wraps in fresh `Arc` internally) — UNCHANGED signature |
| `with_client(engine: ComponentEngine, client, store)` | owns engine | owns engine (delegates to `with_shared_client(Arc::new(engine), ...)`) — UNCHANGED signature |
| `from_shared_engine(engine: Arc<ComponentEngine>, addr, store)` | absent | NEW — shares a component's already-`Arc`-held engine |
| `with_shared_client(engine: Arc<ComponentEngine>, client, store)` | absent | NEW — shared engine over an explicit client |
| `engine(&self) -> &ComponentEngine` | `&self.engine` | `&self.engine` (unchanged; `Arc` deref) |
| `shared_engine(&self) -> Arc<ComponentEngine>` | absent | NEW — hands the same `Arc` to another holder |

Name choice vs `arc-shipper`: this branch KEEPS main's `MirrorTailnetClient`
name (not `arc-shipper`'s reverted-to `TailnetClient`), because
`tests/end_to_end_arc.rs` imports `MirrorTailnetClient` and constructs it at
two call sites. Forward-porting onto main means inheriting main's vocabulary,
not re-importing the older branch's rename. So the only behavioural delta from
main is the `Arc` field + two shared constructors + `shared_engine()`.

Spirit will now construct the shipper as
`ComponentShipper::from_shared_engine(store.engine_handle(), mirror_address, store_name)`
where `engine_handle()` returns `Arc<sema_engine::Engine>` (the seam
`Store::engine_handle()` re-landed on the spirit `mirror-shipper-reland`
branch in 669/1). Both shipper and store then hold clones of one `Arc`.

## Discipline notes

- All five touched methods live on the data-bearing `ComponentShipper` type
  (no free functions, no ZST namespace, no new parser). The internal
  `self.engine.<method>()` calls and the public `engine()` accessor are
  unchanged because `Arc<ComponentEngine>` derefs to `&ComponentEngine`.
- No generated Rust was hand-written; no `.schema` change was required for
  this slice (the change is engine-handle plumbing, not a signal noun).
- Identifiers are full English words (`from_shared_engine`,
  `with_shared_client`, `shared_engine`).

## Build / test result — GREEN

Built and tested from the worktree
(`/home/li/wt/github.com/LiGoldragon/mirror/arc-shipper-mainline`) and the
shared default workspace; reconciled to current mirror-main pins (no stale
pins touched): nota-next branch `main` (0.5.x), signal-mirror branch `main`
(`df2d1ff`), sema-engine branch `main` (`1afcd01`, v0.6.2), triad-runtime
branch `main` (`7a84034`, v0.6.1).

- `cargo build` — clean, no warnings (the previously-unused-import warning is
  gone once `Arc` is in use).
- `cargo test` — all targets pass:
  - `tests/end_to_end_arc.rs` — **2 passed** (
    `component_history_ships_over_tcp_and_a_fresh_store_restores_identically`,
    `component_shipper_actor_ships_suffix_and_publishes_checkpoint`). The
    REQUIRED green target stays green.
  - `tests/daemon_logic.rs` — 14 passed.
  - all `src/bin/*` + lib + doc unit targets — 0 tests, ok.
- `cargo clippy --all-targets` — clean, no warnings.

## What this unblocks (handoff)

Blocker 2 from 669/1 is cleared: mirror main now exposes an `Arc<Engine>`
constructor on a tree that compiles against current signal-mirror/nota-next
0.5.0. Next:

1. **spirit (designer, `mirror-shipper-reland`):** repin `mirror = branch
   arc-shipper-mainline` (or `main` once operator integrates this branch),
   and construct via `ComponentShipper::from_shared_engine(...)`.
2. **meta-signal-spirit (nota-designer):** blocker 1 is still open — re-add
   the `MirrorTarget` schema noun + `mirror_target` field on
   `ConfigureRequest`/`ConfigureReceipt`, regenerate into spirit.
3. **operator:** integrate `arc-shipper-mainline` into mirror main and rebase.

## Worktree-mechanics note (process, not code)

The jj `Arc<Engine>` change lives once, as bookmark `arc-shipper-mainline`
(`6bcefa4f`). It is reachable from both the default repo workspace
(`/git/...`) and the required feature worktree
(`/home/li/wt/github.com/LiGoldragon/mirror/arc-shipper-mainline`), whose `@`
is an empty wip child of the bookmark so the bookmark commit stays the clean,
single-file additive delta operator integrates.
