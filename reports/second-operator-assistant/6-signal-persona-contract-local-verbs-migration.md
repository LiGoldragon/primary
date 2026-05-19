# 6 — signal-persona migration to signal-frame + contract-local verbs

**Lane:** second-operator-assistant
**Bead:** primary-hj63 Phase 3 cascade (the wire-form codec change closed at commit `bdd3a61e` previously; this is the contract-shape cascade that follows /241)
**Reads against:** `reports/designer/241-signal-architecture-migration-guide.md` MUST IMPLEMENT note.

## TL;DR

Migrated `/git/github.com/LiGoldragon/signal-persona` from the
verb-tagged `signal-core` shape to the contract-local-verb shape on
`signal-frame`. Engine relation now speaks `Launch` / `Query` /
`Retire` / `Start` / `Stop`. Supervision relation now speaks
`Announce` / `Query` / `Stop`. The five `*Query` siblings collapsed
into a single `Query` operation root whose payload is a closed enum
(`Catalog` / `EngineStatus` / `ComponentStatus` for engine;
`ReadinessStatus` / `HealthStatus` for supervision). 26 tests pass;
`nix flake check --max-jobs 0` green. Landed on `main` at
`/git/github.com/LiGoldragon/signal-persona` commit `0b8adc28`.

## What landed

Single repository, single commit. Files touched:

- `Cargo.toml` — `signal-core` dep replaced with `signal-frame`.
- `src/lib.rs` — both `signal_channel!` invocations rewritten in the
  new shape; type renames per the verb-form rule; hand-rolled
  NotaSum codecs on the two `Query` enums and
  `SupervisionUnimplementedReason` (see Design problems §2 below).
- `examples/canonical.nota` — all wire fixtures updated to the new
  `(Verb (payload))` shape.
- `tests/canonical_examples.rs` — rewritten to use the new types and
  verb names; covers every operation + reply variant.
- `tests/engine_manager.rs` — rewritten; dropped `signal_verb()` /
  `operation_kind()` assertions (the macro auto-generates `kind()`
  now); kept frame-round-trip + NOTA-text + kind-witness coverage.
- `ARCHITECTURE.md` — `MUST IMPLEMENT` section replaced with a
  `Migration history` section carrying the rename table; relation
  surface tables rewritten for the new operation/payload/reply
  shape; mermaid diagram type label updated.

Type renames (the load-bearing list):

| Was | Now |
|---|---|
| `EngineRequest` (manual) | `EngineOperation` (macro-generated) |
| `SupervisionRequest` (manual) | `SupervisionOperation` (macro-generated) |
| `EngineOperationKind` (manual) | `EngineOperationKind` (macro-generated) |
| `SupervisionOperationKind` (manual) | `SupervisionOperationKind` (macro-generated) |
| `EngineLaunchProposal` | `EngineLaunch` |
| `EngineLaunchAcceptance` | `LaunchAcceptance` |
| `EngineLaunchRejection` | `LaunchRejection` |
| `EngineLaunchRejectionReason` | `LaunchRejectionReason` |
| `EngineRetirement` | (removed; `Retire(EngineId)` direct) |
| `EngineRetirementAcceptance` | (removed; `Retired(EngineId)` direct) |
| `EngineRetirementRejection` | `RetirementRejection` |
| `EngineRetirementRejectionReason` | `RetirementRejectionReason` |
| `EngineCatalogQuery` / `EngineStatusQuery` / `ComponentStatusQuery` | (removed; `Query` enum variants) |
| `ComponentStatusMissing` | (removed; `ComponentMissing(ComponentName)` direct) |
| `SupervisorActionAcceptance` | `ActionAcceptance` |
| `SupervisorActionRejection` | `ActionRejection` |
| `SupervisorActionRejectionReason` | `ActionRejectionReason` |
| `ComponentHello` | `Presence` |
| `ComponentReadinessQuery` / `ComponentHealthQuery` | (removed; `supervision::Query` variants) |
| `GracefulStopRequest` | (removed; `Stop(ComponentName)` direct) |

Reply variant naming choices (the MUST IMPLEMENT note was silent on
the reply surface): outcome variants use past-participle verb form
(`Launched`, `Retired`, `Identified`, `Ready`, `HealthReport`,
`StopAcknowledged`); value variants use direct data-shape nouns
(`Catalog`, `EngineStatus`, `ComponentStatus`, `ComponentMissing`).
Matches the `/241` §2 example shape (`Accepted(Receipt)` +
`Inbox(Inbox)`). If a different reply discipline is wanted, the swap
is local to `src/lib.rs` and `tests/canonical_examples.rs`.

## Design problems observed during the migration

These are concrete friction points the macro and contract shape
produced during this migration. Listed so the designer / macro
maintainer can decide whether each is intentional and worth
documenting, or a sharpness to file.

### 1 · `signal_frame::signal_channel!` rejects duplicate payload types within a channel

`operation Start(ComponentName)` + `operation Stop(ComponentName)`
compiles only after the payload types are made structurally distinct.
The macro emits `error: duplicate NOTA record head 'ComponentName' in
request block`. Workaround: introduce
`pub struct ComponentStartup { pub component: ComponentName }` and
`pub struct ComponentShutdown { pub component: ComponentName }` —
two one-field wrappers that exist only to satisfy the macro.

Question for designer: the wire form is `(Start (...))` vs
`(Stop (...))`, distinguishable by the variant tag per the three-case
PascalCase rule. Why is the macro forbidding the shared payload type?
If it's because the *NOTA record head* check is treating the payload
type name as the head (rather than the variant tag), the check is
mis-positioned — the new dispatch is on the variant name, not the
payload name. If it's intentional (e.g. to keep payload types
single-source-of-truth per variant), the rationale would be worth
naming in the macro doc or skill.

### 2 · `NotaSum` derive doesn't support mixed unit + data-carrying variants

Both `Query` enums (engine and supervision relation) and
`SupervisionUnimplementedReason` use hand-rolled `NotaEncode` /
`NotaDecode`. `NotaSum` derive panics on unit variants
(`use NotaEnum for unit-variant enums`). When an enum has *some*
unit variants and *some* data-carrying ones, neither derive applies.

Repeating the same case-1 dispatch boilerplate by hand for each enum
is mechanical and error-prone. A derive that supports mixed variants
— emitting bare PascalCase for unit variants (case 3) and
`(VariantName payload)` for data-carrying variants (case 1) — would
remove ~30 lines of hand-rolled codec per mixed enum in this crate
alone. The three-case PascalCase rule already covers this; the
derive could too.

(Out of scope for this contract migration; would file as a
nota-derive feature bead.)

### 3 · Single-variant `NotaEnum`s as forward-looking scaffolding

`EngineCatalogScope { AllEngines }` and `EngineStatusScope
{ WholeEngine }` are single-variant `NotaEnum`s. Their job is to
carry a discriminator that is currently constant. The wire form is
`AllEngines` / `WholeEngine` (bare PascalCase) — semantically the
same as no token at all from the receiver's perspective today, but
the type lets future filters (date-range, generation, etc.) land
without changing the operation shape.

The cost is real: every call site reads
`Query::Catalog(EngineCatalogScope::AllEngines)` instead of
`Query::Catalog`. The benefit pays off only when the second variant
lands. Worth a design call: do we accept this scaffolding, or
collapse to unit-tagged variants and re-introduce the enum when the
second case is real?

### 4 · Reply-variant naming discipline is unwritten

The MUST IMPLEMENT note in `signal-persona`'s old ARCH pinned the
operation root verbs but left the reply side silent. Three options
exist in the workspace:

- Past-participle verb-form per outcome (`Launched`, `Retired`).
- Bare `Accepted` / `Rejected` per outcome (the `/241` §2 example
  uses this for single-outcome cases).
- Variant matching the operation that produced it
  (`Launch` reply variant under `EngineReply::Launch`).

I picked the first. Pinning a discipline in `skills/contract-repo.md`
or `/241` would close this for future migrators.

### 5 · `RequestPayload` trait method discoverability

`.into_request()` on a macro-generated request enum is only
available if `signal_frame::RequestPayload` is in scope. Consumers
get a "method not found" error with a helpful `help:` hint, but the
trait import is an extra friction point per consumer crate. The
macro could emit an inherent `into_request` method alongside the
trait impl, or document the required import in
`signal-frame/AGENTS.md` (it isn't currently).

### 6 · Single-field struct payloads degenerate to bare values cleanly — except where the macro forbids it

`Retire(EngineId)` is cleaner than `Retire(EngineRetirement)`
where `EngineRetirement { engine: EngineId }`. Wire form
`(Retire prototype)` reads more directly than `(Retire (prototype))`.
Same for `Retired(EngineId)`, `ComponentMissing(ComponentName)`.

But `Start(ComponentStartup)` and `Stop(ComponentShutdown)` *can't*
degenerate because of Design problem §1 (macro rejects shared
`ComponentName` payload). So adjacent variants on the same enum end
up with inconsistent payload shapes: some bare value, some
one-field wrapper struct. Aesthetic only — both forms work —
but the disciplineless landing surface is a discomfort.

### 7 · Cross-relation `Query` operation name reuse

Both `EngineOperation` and `SupervisionOperation` have a `Query`
variant. Different channels, different payload enums
(`signal_persona::Query` vs `signal_persona::supervision::Query`),
but the same surface verb. Per /241 §3, cross-contract verb reuse
is "fine and expected." Within the same crate / different relations
is a more subtle case — readers need module-qualification to tell
which Query is meant. Worth a sentence in the contract-repo skill
about how to handle cross-relation reuse within one crate.

### 8 · Variant-name / payload-type stutter on value replies

`EngineReply::EngineStatus(EngineStatus)` —  variant name and
payload type are the same identifier. Works because variant names
are enum-scoped, but reads as repetition. Could rename either side
(e.g. `EngineReply::Status(EngineStatus)`) but `Status` is less
specific in context. Status quo accepted.

### 9 · `Presence` rename of `ComponentHello` — future-shape ambiguity

MUST IMPLEMENT said the Announce payload "names what's being
announced (presence, readiness snapshot, health snapshot)." The
current `ComponentHello` struct carries identity-confirmation
fields; renamed to `Presence`. If `Announce` is later expected to
carry readiness/health snapshots, the payload becomes a sum type:

```
operation Announce(Announcement)

pub enum Announcement {
    Presence(Presence),
    Readiness(ReadinessSnapshot),
    Health(HealthSnapshot),
}
```

Worth a designer note: do we expect Announce to fan out, or stay
single-payload?

### 10 · "Lift the repeated prefixes into the payload structure" — interpretation ambiguity

The MUST IMPLEMENT note said to lift the repeated `Engine*` /
`Component*` prefixes from sibling variant names "into the payload
structure rather than top-level variant names." Two readings:

- (A) Variant names of the inner `Query` enum carry the
  distinction: `Query::Catalog`, `Query::EngineStatus`,
  `Query::ComponentStatus`. (What I did.)
- (B) Field names of payload structs carry the distinction.

I picked (A). Reading (B) would mean a less hierarchical `Query`
payload — probably less idiomatic, but worth a sentence in the skill
on which reading is canonical.

## Pending follow-up

- **Daemon-side cascade** — the persona daemon and any CLI binary
  importing `signal_persona::EngineRequest`, `SupervisionRequest`,
  `signal_verb()`, etc., now have unresolved imports. Update path:
  rename to `EngineOperation` / `SupervisionOperation`, drop the
  `signal_verb()` usage, switch dispatch to `kind()` / variant
  matching. Mechanical, no design judgment.
- **The broader Phase-3 cascade** per /241 §7 — `signal-persona-mind`,
  `signal-persona-orchestrate`, `signal-persona-router`,
  `signal-persona-harness`, `signal-persona-message`,
  `signal-persona-terminal`, `signal-persona-auth`, and their owner-*
  counterparts. signal-persona is now a worked example for the
  others (alongside the pilot `signal-repository-ledger`).
- **The earlier primary-hj63 cascade** still has pending consumer
  wire-form fixtures listed in
  `reports/second-operator-assistant/5-nota-three-case-codec-implementation.md`:
  persona-router smoke tests (5 fixtures), persona-mind,
  persona-message, persona-introspect, owner-signal-persona-terminal,
  horizon-rs, persona-harness, signal-persona-mind,
  signal-persona-orchestrate, signal-persona-terminal,
  signal-persona-harness.

## See also

- `reports/designer/241-signal-architecture-migration-guide.md` — the spec this migration implements.
- `reports/designer/238-signal-architecture-redirection-contract-local-verbs.md` — the why.
- `reports/second-operator-assistant/5-nota-three-case-codec-implementation.md` — the earlier primary-hj63 codec change and its pending cascade.
- `/git/github.com/LiGoldragon/signal-frame/tests/channel_macro.rs` — the canonical worked example of the new macro shape.
- `/git/github.com/LiGoldragon/signal-persona/src/lib.rs` (commit `0b8adc28`) — the migrated contract.
- `/home/li/primary/intent/workspace.nota` 2026-05-19 23:00 — the `--max-jobs 0` Nix invocation discipline applied during this migration.
