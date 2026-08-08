# Deploy-stack adoption + pilot readiness — engine-forward exploration

Area: `lojix`, `signal-lojix`, `spirit` (under
`/git/github.com/LiGoldragon/`). Read-only mapping toward the target
state: a live ORCHESTRATED system where persona supervises the
introspector, schema daemon, and triad components together. Every
citation below was verified against source on the named branch on
2026-06-05.

## 0 · Orientation — three repos, three very different maturity levels

| Repo | Most-advanced branch | Maturity | One line |
|---|---|---|---|
| `spirit` | `main` (HEAD detached @71618c6, commits today) | **Working schema-driven triad** | The pilot. Consumes `triad-runtime`'s generic runner + daemon shell; schema-derived planes; 9 test files; builds via Nix. |
| `signal-lojix` | `horizon-leaner-shape` | **Real contract crate** | 680-line `src/lib.rs`, round-trip tests; already migrated to `signal-frame` and contract-local verbs. |
| `lojix` | `horizon-leaner-shape` | **Real but pre-triad-adoption** | 3600+ lines of daemon/CLI; hand-writes Kameo supervision; consumes `sema-engine` + `signal-core`; does NOT consume `triad-runtime` or the schema pipeline. |

The single most important structural fact: **spirit has already done
what lojix has not** — it sits on the extracted generic runner. The
adoption work (intent `4sff`) is to make lojix look like spirit.

## 1 · CURRENT STATE — landed vs scaffold (brutally honest)

### 1.1 · `triad-runtime` — the generic runner IS extracted (foundation for everything here)

This crate is outside the three area repos but is the load-bearing
dependency, so it is stated first. It exists at
`/git/github.com/LiGoldragon/triad-runtime` with real source
(`src/runner.rs`, `src/daemon.rs`, `src/frame.rs`, `src/argument.rs`,
`src/role.rs`, `src/trace.rs`) and commits today (`0ec0048`,
2026-06-05). It realizes intent `7ca4` (extract the generic triad
runtime runner) and `rpr5` (authors write 3 plane engines + effect
handler + budget reply):

- `runner.rs:32` `pub trait RunnerEngines` with associated types and
  exactly the five author hooks intent `rpr5` names:
  `decide_next_step` (Nexus decision), `apply_sema_write`,
  `observe_sema_read`, `run_effect`, `budget_exhausted_reply`.
- `runner.rs:24` `pub enum NextStep<Reply, SemaWrite, SemaRead, Effect, Work>`
  — the generic action projection.
- `runner.rs:61` `Runner` + `ContinuationBudget` / `ContinuationLimit`
  / `ContinuationExhausted` (the budget machinery; `drive(...)` at
  `runner.rs:149`).
- `daemon.rs:11` `pub trait DaemonRuntime`, `daemon.rs:41`
  `SingleListenerDaemon<Runtime>` — the generic socket/listener shell
  with `start`/`stop`/`serve_streams`.

This is the runner shape the FOUNDATION CAVEAT says to lean on: it is
landed, consumed, and tested by spirit (not just proposed).

### 1.2 · `spirit` — the pilot is REAL and works on the new pipeline

LANDED (verified):

- **Schema-derived, asschema-free.** `build.rs` calls
  `schema_rust_next::build::{GenerationPlan, GenerationDriver,
  ModuleEmission}`, declares three modules
  (`signal_runtime_module("signal")`, `nexus_runtime()`,
  `sema_runtime()`), and `write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")`.
  Inputs are `schema/{signal,nexus,sema}.schema`; outputs are
  checked-in `src/schema/{signal,nexus,sema}.rs`. No `.asschema`
  anywhere in the tree. This confirms the FOCUS claim: the pilot
  builds `schema/*.schema -> src/schema/*.rs` directly.
- **Generic runner consumed, not hand-rolled.** `src/daemon.rs:4-7`
  imports `triad_runtime::{DaemonRuntime, SingleListenerDaemon,
  ComponentCommand, ...}`; `daemon.rs:99` constructs
  `SingleListenerDaemon::new(socket_path, runtime, RequestErrorLog)`.
  `Daemon` owns only engine construction + the one-stream
  signal-frame bridge (`daemon.rs:139` `handle_stream`). This is
  intent `4sff`'s end-state, already true for spirit.
- **Nexus schema IS the feature catalog (intent `z6qu`, VeryHigh).**
  `schema/nexus.schema` declares every internal feature as a verb/object:
  `CommandSemaWrite [(Record ...) (Remove ...) (ChangeCertainty ...)]`,
  `NexusEffectCommand [(Stash ...) (ClassifyState ...)]`,
  `NexusWork`/`NexusAction` enums. `State` classification and
  `ChangeCertainty` were ported *through the schema* (commits
  `86d518b`, `1ec334f`, `202f0e5`, all 2026-06-05) — proving the
  catalog discipline in live code, not just docs.
- **Plane separation (intent `lc2r`).** Three plane schema files exist
  (`schema/signal.schema`, `nexus.schema`, `sema.schema`); cross-plane
  references use the `spirit:signal:Entry` single-colon namespace
  (e.g. `nexus.schema` imports `SignalInput spirit:signal:Input`).
- **SEMA = sema-engine over `.sema` (intent `tirp`).** `src/store.rs`
  maps `Record -> Engine::assert_identified`, `ChangeCertainty ->
  mutate_identified`, `Remove -> retract_identified`, reads via
  `match_identified`. Durable: commit-sequence resume proven at the
  process boundary (`tests/process_boundary.rs`).
- **Bootstrap config as pre-encoded binary (intent `7x50`).**
  `daemon.rs:73` `signal_file_argument()` accepts ONLY
  `ComponentArgument::SignalFile` (binary rkyv `Configuration`);
  inline/NOTA-file args are rejected (`daemon.rs:77`). Daemon never
  links `nota-next` (`tests/dependency_surface.rs` guard).
- **Tests:** 9 files including `process_boundary.rs`,
  `runtime_triad.rs`, `socket_negative.rs`, `nix_integration.rs`,
  `instrumentation_logging.rs`. Nix `result` symlink exists (built).

NOT YET DONE (the open, gated surface):

- **Record identity is NUMERIC, not hash.** Schema:
  `RecordIdentifier Integer`; `store.rs` lets sema-engine allocate the
  numeric id via `assert_identified`. There is NO frozen-at-creation
  hash identity in the pilot. (The blake3 in `store.rs:314` is the
  `StateDigest` content-address of *committed state* — the database
  marker — NOT record identity.)
- **No `relations` field.** `Entry { Topics * Kind * Description *
  Magnitude * Privacy * }` — five fields, no relations vector. The
  record SHAPE (flat-vs-per-kind) is psyche-gated and untouched here.
- **Mail ledger in-memory** (ARCHITECTURE §"Known limits"); resets on
  restart. `UpgradeFrom`/`AcceptPrevious` traits exist but nothing
  implements schema diff/upgrade.
- **`Store` lives inside the `Nexus` mutex**, not a kameo single-writer
  actor (ARCHITECTURE §"Known limits"). Database boundary is correct
  (sema-engine); runner/actor ownership is the remaining question.
- **Repo-triad split not represented** — single crate, not `spirit` +
  `signal-spirit` + `meta-signal-spirit`.

### 1.3 · `signal-lojix` — real contract, but ARCHITECTURE.md badly stale

LANDED on `horizon-leaner-shape`:

- 680-line `src/lib.rs`: validated newtype macros, the records, and a
  `signal_frame::signal_channel!` invocation. `tests/round_trip.rs`.
- Migrated to **`signal-frame`** (Cargo.toml lists `signal-frame`, not
  `signal-core`) and to contract-local verbs (commits `1299346`,
  `355d205`).

STALE / SCAFFOLD:

- **ARCHITECTURE.md is wrong about its own state.** Line 5-10 still
  says *"Skeleton. Documentation only. No `Cargo.toml`, no `src/`...
  Status (2026-05-15)"* — false; the crate is implemented. The
  "MUST IMPLEMENT — three-layer migration" section (lines 31-79) is
  also largely done (verbs migrated). This file will misdirect any
  future sweep.
- `schema/signal-lojix.concept.schema` (on `push-schema-concept-signal-lojix`
  only) is a `{}` placeholder marked `(Status Concept)` and
  "pending schema-engine upgrade" (commit `e1e6db8`). Not a real
  schema yet.

### 1.4 · `lojix` — real daemon, but pre-triad and possibly NOT compiling against its own contract

LANDED on `horizon-leaner-shape` (this is the FOCUS "leaner-shape"
branch that hand-writes Kameo supervision):

- `src/deploy.rs` (2105 lines) hand-writes the actor tree: `DeploymentLedgerActor`
  (`deploy.rs:360`), `GarbageCollectionRoots` (`deploy.rs:622`),
  `DeploymentActor` (`deploy.rs:715`), `BuildJobActor` (`deploy.rs:895`),
  plus `CriomeAuthorization` (`authorization.rs:10`).
- `src/runtime.rs` (364 lines) hand-writes `RuntimeRoot` — a Kameo
  actor that manually `spawn`s the four actors in
  `try_with_configuration` (`runtime.rs:147-170`) and hand-writes a
  giant `Message<RuntimeRequest>` match dispatching each
  `wire::Request` variant. **This is exactly the boilerplate intent
  `7ca4`/`rpr5` says to delete.**
- `src/socket.rs` (520 lines) hand-writes its own Unix-socket accept
  loop, length-prefix framing, group-chown — duplicating what
  `triad-runtime::SingleListenerDaemon` + `LengthPrefixedCodec`
  already provide.
- Build-only deploy pipeline is real (`tests/build_pipeline.rs`,
  `real-build-smoke.sh`); GC-root pinning, event log in sema-engine,
  streaming observations are implemented.

NOT DONE / RISK:

- **Criome authorization is fail-closed scaffold.**
  `authorization.rs:43` `unavailable_until_criome_socket_lands()` —
  production policy rejects every deploy until the signal-criome
  daemon client lands. So lojix cannot do a real (non-test) deploy
  today regardless of triad adoption.
- **Does NOT consume the new stack.** Cargo.toml on
  `horizon-leaner-shape` has NO `triad-runtime`, NO `schema-rust-next`,
  NO `schema-next`, NO `nota-next`. It is on `sema-engine` +
  hand-rolled Kameo — the pre-adoption shape.
- **Likely contract/kernel mismatch (load-bearing).** lojix
  `horizon-leaner-shape` Cargo.toml pins **`signal-core`** and uses
  `use signal_core::{...}` (`socket.rs:8`), but its dependency
  `signal-lojix` on the *same* branch name uses
  **`signal_frame::signal_channel!`**. signal-lojix moved to
  signal-frame; lojix did not. Unless signal-core transitively
  re-exports the macro, lojix `horizon-leaner-shape` does not compile
  against current signal-lojix `horizon-leaner-shape`. This must be
  reconciled before any adoption work — the consumer is behind its
  own contract's kernel migration.
- **ARCHITECTURE.md status stale** (line 7: "Status (2026-05-15)
  in-development", references `horizon-re-engineering` as where first
  impl lands — but impl is on `horizon-leaner-shape`).
- `lojix` HEAD is detached on a docs-only commit (`c830eeb`, the
  INTENT.md add); the live code is on `horizon-leaner-shape`.

## 2 · MOVE-FORWARD WORK ITEMS (ordered) with FOUNDATION-STABILITY VERDICT

The verdict column is load-bearing: the psyche wants to port now
WITHOUT creating rework.

### Item 1 — Reconcile lojix's signal kernel to `signal-frame`
**[SAFE-NOW]** · repo `lojix` (`horizon-leaner-shape`), `Cargo.toml`
+ `src/socket.rs` imports · size S-M.
Point lojix at `signal-frame` to match what signal-lojix already
emits. **Why no rework:** the wire-contract migration (signal-core ->
signal-frame, contract-local verbs) is ALREADY DONE and frozen on the
signal-lojix side; lojix is the lagging consumer, so aligning it is
catching up to a settled decision, not betting on a moving one. This
is a prerequisite to everything else — adoption work on a
non-compiling consumer is wasted.
Depends on: nothing (signal-frame is published and signal-lojix tracks it).

### Item 2 — Adopt `triad-runtime` daemon shell in lojix (delete `socket.rs` accept loop)
**[SAFE-NOW]** · repo `lojix`, replace `src/socket.rs` /
`bin/lojix-daemon.rs` plumbing with `SingleListenerDaemon` +
`DaemonRuntime` impl · size M.
**Why no rework:** spirit already runs on exactly this surface
(`daemon.rs:99`), proving the shell fits a real component end to end;
`triad-runtime::SingleListenerDaemon` is landed + tested, not
proposed. lojix's hand-written socket/group-chown/framing is pure
duplication of the shared shell. This is the "delete choreography"
half of intent `4sff`.
Depends on: Item 1 (kernel alignment).

### Item 3 — Re-express lojix's Kameo tree as `RunnerEngines` (the real adoption)
**[PREP -> SAFE-NOW after spirit proves a non-spirit author]** · repo
`lojix`, replace `runtime.rs` `RuntimeRoot` + the four-actor manual
spawn/dispatch with one `impl RunnerEngines` (decide_next_step +
apply_sema_write + observe_sema_read + run_effect + budget reply) ·
size L.
**Why PREP not SAFE-NOW:** the `RunnerEngines` trait is landed and
spirit consumes it — but spirit is currently the ONLY consumer, and
its Nexus is a single-decision-step shape over a record store. lojix's
domain (build jobs, GC roots, streaming observations, per-deployment
sub-actors) is a *different* shape than spirit's. The runner trait is
stable enough to scaffold the impl against NOW (write the engine
struct, the work/action enums), but DO NOT delete the working Kameo
tree until the lojix `RunnerEngines` impl passes lojix's existing
`tests/build_pipeline.rs` + `event_log.rs`. The risk is not the
foundation (the trait is fixed) — it is that lojix is the first
multi-job, sub-actor-spawning author and may surface a trait gap.
Scaffold now; cut over once green.
Depends on: Items 1-2; spirit as the reference impl.

### Item 4 — Author lojix's three plane schemas + adopt schema-rust-next
**[WAIT — partially]** · repo `lojix` + `signal-lojix`, add
`schema/{nexus,sema}.schema` in lojix daemon crate + finalize
`signal-lojix` wire schema · size L.
**Why WAIT:** intent `lc2r` wants Signal wire schema in the contract
repo + Nexus/SEMA plane schemas inside the daemon crate. spirit
proves the *mechanism* works, BUT the schema authoring surface is
under active flux: the `primary-vllc` dual-lowering bare-header bug
(operator-owned, report 73 §2c) sits under payload-less unit-enum
headers — and lojix's deploy-phase enums (`Submitted`, `Building`,
`Built`, ...) are exactly that shape. Blind schema authoring +
regeneration risks landing on the bug. The `signal-lojix.concept.schema`
placeholder confirms this surface is not yet exercised for lojix.
Blocker: `primary-vllc` (operator) + the schema-authoring path needs
one more proven payload-less-variant consumer before lojix bets its
whole feature catalog on it.
Depends on: `primary-vllc` fix; Item 3 (runner adoption first, schema
second — match spirit's order: it ran on the runner before every
feature was schema-authored).

### Item 5 — Wire the criome authorization client (unblock real deploys)
**[WAIT]** · repo `lojix`, `authorization.rs` · size M.
**Why WAIT:** `authorization.rs:43` is explicit — blocked on the
signal-criome daemon client landing. Until then lojix is build-only;
it cannot be the live deploy leg of the orchestrated system. This is
the gate on lojix participating in the "live orchestrated" target at
all, independent of triad adoption. Blocker: signal-criome client
(not in this area).
Depends on: signal-criome daemon client.

### Item 6 — Refresh stale architecture docs
**[SAFE-NOW]** · `signal-lojix/ARCHITECTURE.md` (delete the false
"Skeleton/doc-only" status + done "MUST IMPLEMENT" section),
`lojix/ARCHITECTURE.md` (fix the 2026-05-15 status + the
`horizon-re-engineering`-vs-`horizon-leaner-shape` mismatch),
`spirit/INTENT.md` line ~9 (still says `.asschema` is no longer
checked — that part is correct now, but cross-check against report 73
item 9 which flags `spirit/INTENT.md` "still claims .asschema
materialization" — VERIFY the exact line) · size S.
**Why SAFE-NOW:** documentation truth about LANDED state never becomes
rework; these files actively misdirect sweeps today.
Depends on: nothing.

### Item 7 — spirit record-redesign (hash identity + relations)
**[WAIT — psyche-gated]** · repo `spirit`, `schema/signal.schema`
`Entry` + `RecordIdentifier` · size M-L.
**Why WAIT:** This is the FOCUS's "do NOT assume the shape" item.
Flat-vs-per-kind is psyche-gated (report 73 clarification A,
unresolved). relations is a vector of stable hashes coupled to
frozen-at-creation hash identity (report 73 §2d); the pilot's
`RecordIdentifier` is still reusable numeric, so relations-of-numeric
would be silent corruption. Hash identity must land BEFORE relations.
And `primary-vllc` sits under the `Kind` payload-less headers, so even
the regeneration is blocked. Blocker: psyche shape decision +
`primary-vllc` + hash-identity-first.
Depends on: psyche clarification A; `primary-vllc`; hash-identity
migration.

## 3 · What is portable/ready NOW vs gated (FOCUS's split)

PORTABLE NOW (foundation under it is stable):
- The generic runner + daemon shell (`triad-runtime`) — landed,
  consumed by spirit, tested.
- Wire contracts (`signal-lojix` -> `signal-frame`, contract-local
  verbs) — migrated and frozen.
- Schema-derived build pipeline (`schema/*.schema -> src/schema/*.rs`,
  asschema-removal done) — proven live in spirit.
- Plane separation discipline — three plane files, single-colon
  namespace refs — proven in spirit.
- lojix's adoption of runner + daemon shell (Items 1-3, with Item 3
  scaffolded-not-cut-over).

GATED (do NOT port onto these yet):
- Record SHAPE (flat-vs-per-kind) — psyche clarification A.
- Hash record identity + relations plumbing — coupled, hash-first,
  + `primary-vllc`.
- lojix feature-catalog schema authoring — `primary-vllc`
  payload-less-header bug.
- Real (non-test) deploys — signal-criome client.

## 4 · THE ONE highest-leverage first step

**Reconcile lojix to `signal-frame` and stand it on
`triad-runtime`'s `SingleListenerDaemon` (Items 1+2), keeping the
existing Kameo tree behind it for now.** This is the highest leverage
because: (a) it is the prerequisite that unblocks all later lojix work
— a consumer that doesn't compile against its own contract can't be
ported onto anything; (b) it is provably zero-rework — spirit already
runs on this exact shell, and the wire migration it aligns to is
already settled on the contract side; (c) it converts lojix from a
divergent hand-rolled stack into a triad-runtime consumer WITHOUT
touching the gated surfaces (no schema authoring, no record redesign,
no criome). It is the safe, foundation-stable first move that makes
lojix start to look like the pilot, which is the whole shape of intent
`4sff`.

## 5 · Cross-references

- Prior session: `reports/system-designer/73-improved-nota-schema-situate-2026-06-05/`
  (the record-redesign gating, `primary-vllc`, hash-identity coupling).
- Intent (description-first; short codes re-minted 2026-06-05, may
  drift): `7ca4` extract generic runner; `rpr5` author writes 3 plane
  engines + effect + budget reply; `tirp` SEMA=DB/Nexus=decisions/
  Signal=comms; `z6qu` (VeryHigh) Nexus schema is the feature catalog;
  `lc2r` plane-schema-file separation; `7x50` bootstrap NOTA -> binary;
  `4sff` lojix adopts triad+schema; `mazv` (Decision) live orchestrated
  system target.
