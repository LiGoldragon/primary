# Lojix → CriomOS migration

## LOJIX daemon migration for CriomOS — auditor status (2026-06-10)

The psyche asked how the "Logix migration for ClioMOS" is going. Short answer: **the daemon itself is the strongest part of the whole arc and is essentially built; the cutover is not. No node runs the new stack, and CriomOS is not yet wired to consume it.** The migration also quietly *pivoted shape* since `active-repositories.md` was last written — that doc is now stale in three concrete ways (see Doc-drift below).

### The migration story

There are now **three** generations of the lean rewrite, not two, and the active one is newer than the documented one:

1. **`horizon-leaner-shape` worktrees** (May 23, the branch `active-repositories.md` describes). The original lean shape: a hand-written `lojix` daemon (3694 LOC) over `signal-core` + `nota-codec`, with `daemon.rs`/`runtime.rs`/`client.rs`/`deploy.rs`/`socket.rs`. **Superseded.**
2. **`schema-deep` / `schema-deep-iteration-2`** (late May): a Kameo pilot with a bespoke runner, `NexusMailKeeper`, SEMA-backed store. **Superseded** (report 193 documents this).
3. **`triad-port`** — the current direction, and it *is* `lojix` `main` (HEAD `f9be5df`, June 8). The entire lojix repo `main` tree is now the `triad-port/` subdirectory; the old top-level lean stack is gone from `main`. This is the schema-derived port onto the shared triad runner.

So the daemon migrated **from hand-written → bespoke-actor pilot → schema-derived triad-port**, ending on the shape the psyche's captured intent calls for ("Logix … receives the full triad-engine and schema-based-component port", report 193).

**What's actually built in `triad-port` (lojix `main` f9be5df, 5092 LOC: 2154 handwritten + 2938 schema-generated):**

- A **real two-socket daemon**. `daemon.rs` binds an ordinary (`signal-lojix`) and an owner/meta (`meta-signal-lojix`) authority-tiered Unix socket via `triad_runtime::MultiListenerDaemon`. Each arriving frame is decoded, driven through the **generated `NexusEngine::execute`** (the schema engine is the single routing source of truth — no inline request store), and a typed reply is encoded back.
- **Actor-native async** as of June 8 (report 204, a psyche correction that killed an earlier `spawn_blocking` compatibility bridge): `engine.execute(work).await`, async SEMA/effect hooks, and **`tokio::process::Command`** for deploy effects.
- A **real deploy pipeline** in `schema_runtime.rs` (1503 LOC). `run_effect` does genuine `nix` IO: `nix eval`, `nix build`, `nix copy`, remote ssh dispatch + switch-to-configuration, `nix-store --gc`. The pipeline is a typed multi-step cursor (FlakeAuth → eval → build/copy → activate → record-generation-activated → Deployed), and the deploy is gated through the schema engine, not ad-hoc.
- A **thin CLI** (`lojix.rs`): one NOTA argument, classify ordinary vs owner, send on the matching socket, print one reply. Exemplary — delegates straight to `Client::run_from_environment()`.

**What is NOT built / not done:**

- **Durable storage is not wired.** Despite the INTENT.md and the old HLS Cargo.toml naming `sema-engine`, the **`triad-port` Cargo.toml has no `sema-engine`/`redb` dependency at all**. State is an in-memory `Mutex`-backed `Store` mirroring the `cloud` shape; `lib.rs` itself says "sema-engine / redb persistence is a noted next step." On daemon restart there is no self-resume — this contradicts the daemon-resume constraint in AGENTS.md and is a hard cutover blocker (an operator-owned deploy ledger that evaporates on restart can't be production).
- **CriomOS is not wired to the daemon.** CriomOS's HLS flake still takes `lojix-cli` (input pinned `ad6ce8ad`) as its horizon/system/deployment input producer; there is no `lojix-daemon` or `criomos-horizon-config` flake reference anywhere in CriomOS, on `main` OR on `horizon-leaner-shape`. The flake `description` *talks about* "consuming inputs from lojix," but the wired input is still `lojix-cli`.
- **No node cutover.** Confirmed: nothing on any node runs the daemon. The `active-repositories.md` claim "smoke-built zeus end-to-end through prometheus, not cut over" is directionally right but the underlying state has moved (the smoke artifact predates the triad-port + async-runner rewrite).
- **Horizon shape still predates the latest cluster-data correction** (report 193): `NodeServices` is still optional-field record rather than a vector of typed feature variants; `TailnetControllerRole::Server { port }` still carries a port in cluster data; `ClusterProposal`/`NodeProposal` still carry how-not-what fields. The psyche explicitly wants a "variants first / typed end-to-end / what-not-how" pass on Horizon **before** cutover.

### Per-repo status

| Repo | Branch / where the work is | Status | Notes |
|---|---|---|---|
| `lojix` | `main` = `f9be5df` (triad-port IS main) | **Daemon built, async, real nix IO** | 5092 LOC. No sema-engine/redb yet (in-memory Store). 2 sockets, generated Nexus engine. |
| `signal-lojix` | `main` = `0b8a9e3` (triad-port IS main) | **Contract port landed** | One `schema/lib.schema`, generated `src/schema/lib.rs`. Build-time schema-rust-next gen. Clean. |
| `meta-signal-lojix` | `main` = `5cf4824` (triad-port IS main) | **Contract port landed** | Owner/meta Deploy/Pin/Unpin/Retire surface. Generated. Clean. |
| `criomos-horizon-config` | `main` = `90e7906` | **Data repo only** | Just `INTENT.md` + `horizon.nota`. NOT yet consumed by horizon-rs (no Cargo dep, no CriomOS flake ref). Constants split exists on paper; consumption not wired. |
| `horizon-rs` | `main` = `48df4bd` (ahead of HLS!) | **nota-next migration on MAIN** | `main` migrated the proposal codec to nota-next (Jun 8); HLS branch (`7a3072c`) is behind main. Production-clean to_nota delegation. |
| `lojix-cli` | `main` = `fc2ff02` | **Stack A, still live, advanced** | nota-next migration landed on production main. This is what CriomOS actually deploys. |
| `CriomOS` | `main` `0ca45d5`; HLS `d47cb5a` | Stack A live; HLS still on `lojix-cli` | HLS flake takes `lojix-cli`, not the daemon. |
| `CriomOS-home` / `CriomOS-lib` / `goldragon` | main + HLS exist | Stack A live; HLS tracking | goldragon HLS adds cluster-intent; CriomOS-lib HLS clarifies transitional LAN constants. |

### Foundation dep pins (lojix-stack consumers, against today's HEADs)

Read from the real lock pins, not Cargo.toml `branch="main"`. All three triad-port crates are **internally consistent but collectively behind**:

| Crate (consumer) | Foundation crate | Pinned | HEAD | Behind |
|---|---|---|---|---|
| lojix `main` (f9be5df) | schema-rust-next | `5cadd25` | `eca4028` | ~43 |
| lojix `main` | nota-next | `f0e435a` | `d8862b6` | 8 |
| lojix `main` | schema-next | `5311f9a` | `c8ebb39` | 8 |
| lojix `main` | triad-runtime | `28d03c3` | `6ea8316` | 25 |
| lojix `main` | signal-frame | `d61ebf2` | `166bda8` | 7 |
| lojix `main` | nota-config | `bd9173a` | `ba689f0` | 1 |
| signal-lojix / meta-signal-lojix | schema-rust-next | `ec0678c` | `eca4028` | ~44 |
| signal-lojix / meta-signal-lojix | nota-next | `fb600e3` | `d8862b6` | 10 |

**The `nota-next d8862b6` flag does NOT fire for any lojix-stack consumer.** Every consumer pins nota-next *behind* `d8862b6` (lojix at `f0e435a`, the signal crates at `fb600e3`), and — critically — each consumer's own `schema-rust-next` pin agrees with its `nota-next` pin (lojix's schema-rust-next `5cadd25` itself pins nota-next `f0e435a`). So there is **no encoding-format straddle today**: each crate emits from a schema-rust-next that matches its nota-next. The real exposure is the inverse and is *latent*: when lojix rebases onto current foundation, it jumps the entire encoding arc in one step — `f0e435a` → `ae5c25c` (numeric codecs, the rev schema-rust-next HEAD deliberately isolates) → `16493c8`/`027e18a`/`d8862b6` (lossless-pipe bracket strings + bare-safe atom projection). That is an 8-commit encoding-format jump that must be taken as a coordinated lojix + signal-lojix + meta-signal-lojix re-pin-and-regenerate, never piecemeal. Flag it for the operator who does the rebase, but it is not a live mismatch right now.

### Free-function sweep (Rust repos)

Discipline is **clean** across all four Rust repos.

- **lojix** (`triad-port/src`, against current `main` f9be5df): only `fn main()` ×2 and **`fn run()` in `lojix-daemon.rs:16`** — a thin `Result`-returning split of `main` that delegates to `Daemon::new(cfg).run()`. Borderline (it's a free fn outside `main`), trivially fixable into a `Daemon::run_from_environment()` associated fn; the CLI binary already does exactly that with `Client::run_from_environment()`. Honest count of real violations: **0–1** (the `run()` wrapper is the only debatable one).
- **signal-lojix / meta-signal-lojix**: **0** module-level fns (pure generated contracts).
- **horizon-rs** production code (`lib/src` + `cli/src`): **1**, and it's `fn main()` in the CLI. The other 150 column-0 fns the grep surfaced are all in `tests/` (test fns and test fixtures like `fn machine() -> Machine`) — all legitimate.

### Fake-NOTA sweep (Rust repos)

**Clean.** No hand-assembled paren-records anywhere in handwritten source.

- The many `fn to_nota(&self) -> String` hits in `lojix`, `signal-lojix`, `meta-signal-lojix` are all inside `@generated by schema-rust-next` files (`src/schema/*.rs`) — emitter output, explicitly whitelisted. The handwritten lojix source (`daemon.rs`, `client.rs`, `lib.rs`, `schema_runtime.rs`) has **zero** `format!("(")` / `push_str("(")` / `write!(…"(")` hand-assembly.
- **horizon-rs** is the real hand-written test, and it passes: `to_nota` delegates to the inner type's NotaEncode (`self.0.to_string().to_nota()`) or uses nota-next's structured builder `Delimiter::Parenthesis.wrap([… child.to_nota() …])`; decode uses the real parser (`NotaBlock::new(block).expect_delimited(...)` / `parse_string()` / `Option::<T>::from_nota_block`). Most types `#[derive(NotaDecode, NotaEncode)]`. No char-indexing, no manual paren splitting. A grep for `format!("("`/`push_str("("` across all of `horizon-rs/lib/src` returns **nothing**.

### Doc-drift to fix in `protocols/active-repositories.md`

1. **Production lojix-cli pin is stale.** The doc says CriomOS/CriomOS-home pin `lojix-cli` at `4c66b8a6fa55`; both flake.locks are now at **`fc2ff0287f53`** (the nota-next migration landed on Stack A `main`, plus a horizon swap-policy update). Production moved forward.
2. **The lean-stack shape moved.** The doc describes the daemon as `horizon-leaner-shape` top-level over `signal-core`/`nota-codec`/`sema-engine`. The active shape is **`triad-port`** (= lojix `main`), schema-derived over `triad-runtime`/`signal-frame`, and **without** sema-engine wired (in-memory Store). The "Replaces Stack" table entries for `lojix`/`signal-lojix` need refreshing.
3. **Smoke claim is dated.** "smoke-built zeus end-to-end through prometheus" predates the triad-port + actor-native-async rewrite (reports 200–204). Re-verify against current `main` before re-asserting.

### Critical path to cutover

1. Wire **durable storage** (sema-engine/redb) into `lojix` triad-port + daemon self-resume — the single biggest gap (an operator deploy ledger can't be in-memory).
2. The **Horizon "variants-first / what-not-how" pass** the psyche asked for (report 193), and actually **consume `criomos-horizon-config`** from horizon-rs.
3. **Wire CriomOS to the daemon** (or to daemon-produced inputs) on the HLS branch — today it still takes `lojix-cli`.
4. **Coordinated foundation re-pin** of lojix + signal-lojix + meta-signal-lojix onto current schema-rust-next/nota-next (the 8-commit encoding jump), regenerate, smoke.
5. Cut over **one node**, run both stacks parallel, then retire `lojix-cli`.
