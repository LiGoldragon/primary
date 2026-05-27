# Prototype target + per-component mapping

*Per-component mapping of `/35` schema-deep pilot state against `/392`'s 8-component fullness criterion (codified in Spirit record 972), with the specific extensions this iteration 2 targets. Designed to be read alongside `0-frame-and-method.md §"Subagent dispatch brief"`. The subagent uses this as the per-component checklist.*

## The 8-component fullness criterion

Per Spirit record 972 (Principle Maximum, 2026-05-27): "The prototype must be audited against whether it uses all designed components fully: NOTA structure, schema macro lowering, assembled schema, Rust emission, generated signal, Nexus mail keeper, SEMA state handling, and Spirit runtime behavior."

The 8 components correspond to the layers of the schema-derived stack (per `/392`'s pipeline) plus the runtime plane architecture (per `/392` + records 963-970).

## Per-component scoring of `/35` (the baseline)

This is the orchestrator's pre-iteration assessment. The subagent will re-score after iteration 2; the audit then drives iteration 3.

| # | Component | `/35` state | Score | Iteration-2 target | Component-development required |
|---|---|---|---|---|---|
| 1 | **NOTA structure** (nota-next: structural parsing, StructureHeader, source spans) | Used via schema-next's macro engine consuming nota-next-parsed Document blocks. StructureHeader not directly consumed; not yet load-bearing in lojix-next. | 0.7 | Continue consuming via schema-next; no direct extension needed unless tests demand it. | None for this iteration. |
| 2 | **Schema macro lowering** (schema-next: position-aware macro registry, Asschema endpoint) | Used in build.rs via `SchemaEngine::default().lower_source_with_context`. 4-position document (Imports / Input / Output / Namespace) authored in `schema/lojix.schema`. Macro registry assertion in build.rs (per spirit-next pattern). | 0.9 | Continue using. Add macro-pair assertion for any new schema constructs (e.g. brace-enum if subagent uses it). | None unless brace-enum sugar is needed — that lives on a designer branch per `/389`. |
| 3 | **Assembled schema** (Asschema: ordered, macro-free intermediate) | Consumed implicitly via the schema-next → schema-rust-next pipeline. Not directly inspected by lojix-next. | 0.8 | Continue consuming. | None. |
| 4 | **Rust emission** (schema-rust-next: emits `src/schema/lib.rs` + module files) | `build.rs` calls `RustEmitter::default().emit_file(...)`. Output in `src/schema/lib.rs` (per records 909/910). Freshness check via `assert_checked_in_schema_is_fresh` (per `/391`). | 0.9 | Continue. Add the DatabaseMarker namespace record to schema/lojix.schema; the emitter handles it. | None — schema-rust-next handles new namespace records mechanically. |
| 5 | **Generated signal** (schema-derived signal-frame: Communicate trait, signal protocol, mail mechanism, schema-derived frame primitives) | `/35` uses signal-frame's existing macro-based encode/decode (`StreamingFrame`). NOT yet the schema-derived rewrite. NOT yet a Communicate trait. NOT yet a mail mechanism. | **0.3** | **Add Communicate trait** (in signal-frame or schema-rust-next — subagent decides + documents). **Add DatabaseMarker** as schema-emitted reply payload. **Defer** the full schema-derived signal-frame rewrite to iteration 3 (substantial work per `/390`). | Extend signal-frame to host Communicate trait. Add DatabaseMarker schema declaration to lojix.schema. Possibly stub the schema-derived rewrite scaffold on signal-frame's `schema-deep-iteration-2` branch as iteration-3 setup. |
| 6 | **Nexus mail keeper** (per records 963-970: Nexus is the runtime mail keeper; "when Nexus has the mail, the mail is in BEING-PROCESSED state"; lifecycle hooks; push-not-poll) | `/35` has `OperationDispatcher` actor (executor-style routing). Does NOT track message lifecycle. Does NOT expose hooks. Does NOT name itself Nexus. | **0.2** | **Rename Executor → Nexus** workspace-wide in lojix-next. **Reshape OperationDispatcher into NexusMailKeeper** with typed `MailEntry`, lifecycle states (Sent / Queued / Processing / Replied), hookable events (MessageSent, MessageQueued, MessageProcessing, MessageReplied). Hooks fire push-style per `skills/push-not-pull.md`. | If `persona-mail` should be a shared crate, create it. If iteration-2 keeps it inside lojix-next, surface for iteration-3 promotion. |
| 7 | **SEMA state handling** (sema-engine: redb-backed durable single-writer state, schema-emitted SemaCommand/SemaResponse) | `/35` has `Store` actor with in-memory `Vec`. Schema-emitted SemaCommand + SemaResponse already exist in `schema/lojix.schema`. NOT using sema-engine. NOT durable across daemon restart. | **0.3** | **Replace in-memory Store with sema-engine-backed Store.** Store actor's State becomes the sema-engine handle. SemaCommand lowers to sema-engine operations; SemaResponse reads from sema-engine results. **Durable across restart.** | If sema-engine's surface lacks transaction-counter or state-hash for DatabaseMarker, extend sema-engine on its own `schema-deep-iteration-2` branch. |
| 8 | **Spirit runtime behavior** (the spirit-next pilot pattern: daemon binary takes single NOTA arg, CLI thin client, rkyv on Unix socket, build.rs assertion, src/schema emission, etc.) | `/35` follows the spirit-next pattern faithfully. Daemon binary takes single NOTA arg; CLI thin client; rkyv on Unix socket; build.rs asserts macro registry coverage; src/schema emission. | 0.9 | Maintain. The lifecycle hooks (#6) extend the spirit-next pattern with the mail mechanism; otherwise unchanged. | None — spirit-next's pattern is the model and `/35` already follows it. |

**Baseline aggregate**: 0.7 + 0.9 + 0.8 + 0.9 + 0.3 + 0.2 + 0.3 + 0.9 = **5.0 / 8.0** (62.5% component fullness)

**Iteration-2 target**: ≥ **6.7 / 8.0** (≈84%) — components 5/6/7 lift to ~0.7-0.8 each; others stay constant or improve.

## What this iteration explicitly defers

To keep the iteration scoped to "fully working prototype" rather than "shipped substrate rewrite," these deferrals are sanctioned by `1` (this report) and surface in the iteration-2 audit as **iteration-3 candidates**:

- **Full schema-derived signal-frame rewrite** per `/390` — substantial work; iteration 2 adds Communicate + DatabaseMarker but doesn't rewrite signal-frame's macro-based encode/decode into schema-derived emission.
- **Schema upgrade traits + diff machinery** per record 950 — iteration 2 doesn't add upgrade methods because the schema isn't versioned yet; iteration 3 adds versioning + upgrade traits as the first schema diff arrives.
- **Persona-mail as a shared substrate crate** — iteration 2 keeps the Nexus mail keeper inside lojix-next (in-process) unless the subagent's design demands earlier extraction; iteration 3 promotes if other components (cloud, spirit, mind) need the same mail mechanism.
- **Real nspawn boot in `nix flake check`** — `/35`'s test 10 uses sandbox-mode marker `nspawn-sandbox-activate` because `nix flake check`'s chroot lacks root+cgroups. Iteration 2 keeps this; real nspawn is operator-amalgamation-time work.
- **Owner-signal-lojix contract** — iteration 2 keeps only the ordinary signal surface (records 911-912's component-triad mandate is a full triad, but `/35` ships only one tier and iteration 2 maintains parity until owner-tier work earns its iteration).
- **Vectors in SemaResponse** — `/35` uses one-record-per-response per spirit-next precedent. Iteration 2 maintains. Vectors land when schema-next gains them (psyche-authorized per Spirit 883).

## Per-component sub-tasks the subagent owns

The subagent's `2-...md` report scores each component AFTER iteration 2 and lists what's still bypassed. The audit (this orchestrator's `N-overview.md`) then ranks each component's gap-to-1.0 as iteration-3 work.

### Component 5 (generated signal) sub-tasks

| Sub-task | Acceptance |
|---|---|
| 5a. Communicate trait declared in signal-frame OR schema-rust-next (subagent picks) | trait in source; documented decision in `2-...md` |
| 5b. `UnixSocketCommunicate` concrete impl using existing socket I/O | trait impl compiles + `lojix_next_communicate_trait_round_trip` test passes |
| 5c. `DatabaseMarker` namespace record in `schema/lojix.schema` | regenerates cleanly; `DatabaseMarker` field present in every Output reply variant |
| 5d. NexusMailKeeper populates DatabaseMarker on reply | `lojix_next_database_marker_in_every_reply` + `lojix_next_database_marker_state_hash_changes_on_write` tests pass |
| 5e. Schema-derived signal-frame rewrite scaffold (optional, iteration-3 setup) | if attempted, document the boundary cleanly in `2-...md` |

### Component 6 (Nexus mail keeper) sub-tasks

| Sub-task | Acceptance |
|---|---|
| 6a. Workspace-wide Executor → Nexus rename in lojix-next | ARCHITECTURE.md + module names + type names + tests align with record 964 |
| 6b. NexusMailKeeper actor with typed MailEntry + lifecycle states | `lojix_next_nexus_is_mail_keeper` test passes (assert lifecycle transitions Sent → Queued → Processing → Replied) |
| 6c. Hookable events (MessageSent, MessageQueued, MessageProcessing, MessageReplied) | `lojix_next_message_lifecycle_hooks_fire` test attaches a hook and verifies it fires |
| 6d. Mail correlation IDs threaded through reply path | DatabaseMarker reply (5d) carries the right correlation back |
| 6e. Documented decision on persona-mail extraction (now vs iteration-3) | one paragraph in `2-...md` §"Architectural decisions" |

### Component 7 (SEMA state handling) sub-tasks

| Sub-task | Acceptance |
|---|---|
| 7a. Store actor replaces in-memory Vec with sema-engine handle | source compiles + existing tests still pass against sema-engine backing |
| 7b. SemaCommand lowers to sema-engine operations | `lojix_next_input_lowers_to_sema_command_exhaustively` still passes; new test `lojix_next_sema_engine_durable_across_restart` passes |
| 7c. SemaResponse constructed from sema-engine results | `lojix_next_sema_response_maps_back_to_output_exhaustively` still passes |
| 7d. sema-engine extended if needed for transaction-counter / state-hash | extension on sema-engine's `schema-deep-iteration-2` branch; per-repo INTENT.md updated per record 944 |
| 7e. Daemon spawn + stop + restart preserves state | end-to-end witness; runs under `nix flake check` |

## Boundary with the parallel arcs

- **`/34` (existing-lean-stack MVP+sandbox)** — unaffected. Iteration 2 is on `schema-deep` branch; `/34`'s `horizon-leaner-shape` branch continues independently.
- **`/36` + `/162` + `/163` (production-to-lean reconciliation)** — also unaffected. Operator's ports land in `horizon-leaner-shape`, not `schema-deep`. The cross-arc amalgamation question (`/36 §"Cross-arc integration"` + `/163` finding 7) remains open.
- **`/35` baseline** — this iteration extends it on the same branch (`schema-deep`). The `/35/2` and `/35/3` reports stay as iteration-1 record; this directory carries iteration 2.
- **Designer-lane work `/389-395`** — informs the workspace direction (Signal/Nexus/SEMA, signal protocol, mail mechanism); doesn't conflict with this iteration. Per-repo INTENT.md edits already manifested via `/395`.

## Open psyche questions surfaced by this iteration's frame

(Subagent surfaces additional questions in `2-...md` as they arise; orchestrator collects in `N-overview.md`.)

1. **Communicate trait home** — `signal-frame` (where the wire substrate lives) vs `schema-rust-next` (where the emitter lives) vs new dedicated abstract crate? `/390 §"Open questions" #1` names the tradeoff. Iteration 2 will document the subagent's working choice; psyche may redirect for iteration 3.
2. **Nexus-mail-keeper extraction** — inside lojix-next (in-process plane) for iteration 2, vs immediately into `persona-mail` (shared substrate). Iteration 2 defaults to in-process unless the subagent's design demands extraction; psyche confirms or redirects.
3. **DatabaseMarker scope** — hash + counter on every reply (per `/390` design proposal), or only on write-replies? `/390 §"Open questions" #3`. Iteration 2 puts it on every reply for uniformity; psyche may scope down.
4. **Existing `nexus` repo naming collision** — the typed-semantic-text vocabulary repo predates the Nexus runtime plane. Long-term: rename existing `nexus` (to e.g. `nota-vocab` or `nexus-text`)? Prefix the new component as `persona-nexus`? Iteration 2 surfaces; doesn't decide.
5. **Per-repo INTENT.md/ARCHITECTURE.md propagation cost** — per record 944's continuous-manifestation discipline, every substrate repo the subagent touches gets updated. Iteration 2 will produce edits in sema-engine, signal-frame, schema-next (if extended), nota-next (if extended). Workspace-scale audit of how this discipline scales is iteration-3+ work.

## See also

- `0-frame-and-method.md` — frame + method + subagent brief (this directory).
- `/system-designer/35-schema-deep-new-logics/2-schema-deep-lojix-next-pilot.md` — baseline subagent report.
- `/system-designer/35-schema-deep-new-logics/3-overview.md` — baseline orchestrator synthesis.
- `/designer/392-vision-schema-driven-stack-canonical-2026-05-27.md` — workspace vision; 8-component fullness criterion source.
- `/designer/389-schema-macros-canonical-direction.md` — schema language layer.
- `/designer/390-wire-runtime-canonical-direction.md` — wire layer; Communicate trait + mail manager + DatabaseMarker design.
- `/designer/391-emission-discipline-direction.md` — emission target + Nix discipline.
- `/designer/395-runtime-nexus-signal-sema-triad-manifestation-2026-05-27.md` — Signal/Nexus/SEMA manifestation pass.
- Spirit records 894-980 — the source intent.
- `skills/component-triad.md` §"Runtime triad" — Signal/Nexus/SEMA per record 964.
- `skills/actor-systems.md` — actor-density discipline.
- `skills/repo-intent.md` + `skills/architecture-editor.md` — continuous-manifestation discipline (record 944).
