# 5 — two-runtime situation, cutover plan, and history

Workflow dimension `explore:cutover-history`. History via git pickaxe across all
branches.

## Headline

cloud carries **two synchronous, actorless runtimes** that grew sequentially. The
legacy production runtime (`src/daemon.rs`) was born 2026-05-23 and is still what
`cloud-daemon` runs with live Cloudflare IO. The schema-engine triad path was
started fresh 2026-06-04, is build/socket-verified, but does **no live IO**
(`run_effect` returns empty listings); cutover is pending. The §"Actor Shape"
mandate was written in the **first commit** and has **never been touched since** —
pure unimplemented aspiration. **No kameo/actor implementation of cloud ever existed
in any branch** (`git log --all -S kameo` = zero). Maintaining two sync runtimes
**compounds** the divergence.

## Timeline (commit short-ids, one line each)

| Date | Commit | Effect on the runtime |
|---|---|---|
| 2026-05-23 | `ba35849` birth runtime architecture | Wrote `ARCHITECTURE.md` including §"Actor Shape" (the one-actor-per-concern mandate). No code runtime yet. |
| 2026-05-23 | `84e6109` first runtime slice | **Born: legacy `src/daemon.rs`** — `thread::spawn` per listener over `Arc<Mutex<Store>>`. The production runtime. |
| 2026-05-24 | `7bb0d80` mark pending schema-engine upgrade | First marker that a schema-engine path is coming (doc/intent only). |
| 2026-06-04 | `073dcf6` (branch `next`) schema-derived engine scaffold prototype | First schema-engine prototype: `impl SignalEngine/NexusEngine`+`SemaEngine`; **provider IO as a Nexus `CommandEffect` (`run_provider_effect`), explicitly "not inline" — the key shape, proven.** Whole-crate build blocked by old-vs-new contract incompatibility. |
| 2026-06-04 | `413e4ba` integrate meta-signal schema artifacts | Legacy `daemon.rs` last touched here (only two commits total: `84e6109` + `413e4ba`). |
| 2026-06-04 | `d85873b` start fresh generated schema runtime | **Born: `src/schema_runtime.rs`** (prototype discarded for the emitted path). |
| 2026-06-05 | `bbb96c8` uses generated runner schema path | schema_runtime moves onto the generated runner. |
| 2026-06-06 | `4db0e26` wire schema engine to live MultiListenerDaemon over durable SchemaStore | **Born: `src/schema_daemon.rs` + `src/schema_store.rs` + `src/schema_role.rs`.** Two-listener `MultiListenerDaemon`; `tests/schema_daemon.rs` round-trips both tiers on real sockets. Message: "the legacy `daemon::Daemon`+`Store` remains the production Cloudflare-IO runtime (cutover lands once the effect plane carries live IO)." |
| 2026-06-06 | `4a378d3` retire hand-written schema_daemon.rs onto emitted triad_main | Hand-written `SchemaDaemon`/`CloudRuntime`/`serve_*`/`ListenerRole` replaced by emitted `src/schema/daemon.rs`; cloud now hand-writes only `impl ComponentDaemon for CloudDaemon`. Deletes `schema_role.rs`. Cites designer 542 / Spirit `ocu7` / `ug6i`. |
| 2026-06-07 | `a0f061c` require binary daemon startup archives | schema_daemon refinement. |
| 2026-06-07 | `87686a1` reconcile ARCHITECTURE.md to the emitted triad_main daemon | Doc reconcile to the emitted spine. **Did NOT touch §"Actor Shape".** |

## Was an actor cloud ever built? No — never.

- `git log --all -S kameo`: **zero results** across all branches and history.
- Working tree + `Cargo.toml`: no `kameo`, no `tokio`.
- The only "Provider"/"Actor" pickaxe hits (`073dcf6`, `ba35849`) are the
  `CloudflareProvider` **enum** and provider IO modeled as a Nexus **`CommandEffect`**
  (`run_provider_effect`) — a data-driven effect command, NOT a kameo actor.
  Prototype `073dcf6` explicitly chose "provider IO as a Nexus CommandEffect, not
  inline" — the schema-engine's **substitute** for the actor shape.
- No file ever named `*actor*` was added.

## §"Actor Shape" — always-unimplemented aspiration

Born in the first commit, the five-actor block has been **byte-identical since
birth** (`git log -S 'CloudflareProvider' -- ARCHITECTURE.md` returns only the
birth commit(s); thesis-2 corrects this to TWO birth commits `ba35849`+`db5dc5c`,
both 2026-05-23, never since). The section **below** it (the implementation slice)
evolved — and notably the OLD slice even said "Add a Cloudflare read-only **actor**
for zones and records" / "Store provider policy and plan records in sema-engine".
**That actor language was REMOVED from the slice while the §Actor Shape mandate
above it was LEFT standing.** The doc actively walked away from actors in the plan
while keeping the actor mandate as a frozen header.

## Cutover plan and explicitly-deferred items

- **Cutover gate** (`4db0e26` + `ARCHITECTURE.md:166`): legacy `Daemon`+`Store`
  stays production "until the effect plane carries live IO." Cutover = teach
  `SchemaRuntime::run_effect` to do the real Cloudflare calls (port the `Store`
  cloudflare path onto the Nexus `CommandEffect` effect plane).
- **Deferred items, with stated reasons** (`schema_store.rs:9-14`):
  1. SEMA tables are **in-memory** for "this slice, matching the lojix `Store`
     template" — not durable.
  2. **Durable `sema-engine` / redb backing is the noted follow-on, "deferred while
     the engine still pulls the deprecated `signal-core` dependency."** The concrete
     blocker: redb persistence waits on sema-engine shedding deprecated
     `signal-core` (an AGENTS/ARCHITECTURE hard constraint: "No deprecated
     signal-core dependency in new code").
  3. `PlanTable` is an interim composite-key collection ("report 77") so no
     `sema-engine` identified-multi-key (`ox7e`) primitive is required yet.
- "Report 77" cited here is NOT a cloud-designer report (this lane reaches 36) — it
  is another lane's report; treat as an external locator.

## Does maintaining two sync runtimes compound the divergence? Yes.

Two listener loops, two store types (`Store` vs `SchemaStore`), two plan/policy
state representations, both synchronous, both actorless. The divergence is
**doubled**: NEITHER runtime is an actor system, and the live one (`daemon.rs`)
makes blocking Cloudflare calls while serializing the global `Arc<Mutex<Store>>` —
the exact thing §"Actor Shape" forbids. The schema path was the chance to land the
actor shape and **did not**: it chose Nexus `CommandEffect` (synchronous effect
dispatch in the runner) over kameo provider actors. So the schema-engine direction
has **institutionalized the actorless shape as the going-forward substrate**, while
the frozen §Actor Shape header still mandates the opposite.

## Open questions raised here

- Is the `signal-core` removal (the named redb/sema-engine durability gate) tracked
  anywhere, and is it the true critical-path gate for cutover, or is the
  `run_effect` IO port the real gate?
- When cutover lands, does the Nexus-CommandEffect effect plane permanently
  foreclose §"Actor Shape" (so ARCHITECTURE.md should retire/rewrite it), or is the
  intent to host kameo provider actors behind the triad listener at the effect-plane
  boundary?
