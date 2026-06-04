# Cloud port — first `next` prototype: results and design findings

*cloud-designer, 2026-06-04. Companion to report 18 (the concept). This
records what the `next`-branch prototype fan-out actually produced, and —
the point of the exercise — the design flaws it surfaced. **Status:** on
`next` branches, pushed to origin, NOT on `main`. Branch locators in §6.*

## What the prototype proved

The derivation chain is real and runnable for cloud's domain. Two
schema-derived contract crates were authored from scratch (modeled on the
`spirit` pilot), generated through `schema-next` → `schema-rust-next`, and
**both compile**. The cloud daemon's three engine impls were scaffolded for
both contracts, and the single most important shape — **provider IO as a
Nexus `CommandEffect`, never inline** (Spirit 1486: [NexusAction 5-variant
set ReplyToSignal / CommandSemaWrite / CommandSemaRead / CommandEffect /
Continue; effects per-component declared in schema]) — is demonstrated end
to end in the owner decide loop.

| Crate | Schema authored | Generated Rust | Build |
|---|---|---|---|
| `signal-cloud` (working) | `schema/lib.schema` (read-only Observe/Validate) | `src/schema/lib.rs`, 1974 lines | **PASS** (`nota-text` + default) |
| `meta-signal-cloud` (policy, in `owner-signal-cloud/next`) | `schema/meta-signal-cloud.schema` (8 ops) | `src/schema/meta_signal_cloud.rs`, 2271 lines, all 3 engine traits | **PASS** (after fixing a self-alias bug) |
| `cloud` daemon | — | engine impls for both contracts + `schema_daemon.rs` | both **new** contract crates compile; **whole-crate build blocked** (see Finding 2) |

The freshness round-trip works: `build.rs` lowers the schema, compares the
checked-in `.asschema`, re-emits Rust from both NOTA and rkyv artifacts and
asserts they match — so a stale schema fails the build loudly.

## The shape, proven — the owner decide loop

The daemon's owner `decide` loop is the proof that provider IO is an
effect, not inline handler code. Hand-written, modeled on `spirit`:

```rust
fn decide(&mut self, input: Nexus<Work>) -> Nexus<Action> {
    let origin_route = input.origin_route();
    let mut work = input.into_root();
    let mut budget = ContinuationBudget::default_for_pilot();
    loop {
        match self.step_decide(work) {
            NexusAction::ReplyToSignal(reply) => return reply.with_origin_route(origin_route),
            NexusAction::CommandSemaWrite(c) => { let o = SemaEngine::apply(&mut self.store, …); work = NexusWork::sema_write_completed(o); }
            NexusAction::CommandSemaRead(c)  => { let o = SemaEngine::observe(&self.store, …);   work = NexusWork::sema_read_completed(o); }
            NexusAction::CommandEffect(c)    => { let r = self.run_provider_effect(c);            work = NexusWork::effect_completed(r); }  // <- provider IO HERE only
            NexusAction::Continue(next)      => { work = next; }
        }
        budget = budget.spend_one()?;  // bounded continuation
    }
}
```

`ApplyPlan` recurses: a SEMA write that does **not** reply but emits
`CommandEffect(CloudflareApplyPlan(plan))`; `run_provider_effect` is the
sole site the Cloudflare client is touched (per Nexus). The two-listener
daemon shape (working socket + owner socket over one in-memory `Store`) is
preserved.

## Design findings — the flaws the prototype surfaced

### Finding 1 — `schema-rust-next` emits no `SemaEngine` for a read-only contract (DECISION NEEDED)

The emitter gates `SemaEngine` emission on the presence of a
`SemaWriteInput` root. `signal-cloud` is read-only (Observe/Validate, no
writes), so it gets `SignalEngine` + `NexusEngine` + the `sema` namespace
module + the `Sema<Root>` envelope + the `CommandSemaRead →
SemaReadCompleted` routing — **but no trait method to implement the
observe**. The typed read path exists with no engine hook.

This is an upstream `schema-rust-next` design gap, not a cloud bug, and it
affects every read-only/observation-only contract. Two resolutions:

- **(a) Grow a `SemaReadEngine`** (`observe_inner` / `observe` +
  `trace_sema_read_observed`) emitted whenever a `SemaReadInput` root is
  present, independent of `SemaWriteInput`. The target schema explicitly
  lists `SemaReadInput`/`SemaReadOutput`, which argues for this. **(Recommended.)**
- **(b) Read-via-effects only** — treat `SemaReadInput` as a Nexus-impl
  pass-through and drive reads through effects, dropping the read-SEMA
  trait. Simpler emitter, but the read path loses the single-writer/
  parallel-reader SEMA discipline.

This changes `schema-rust-next` (operator-owned `main`), so it needs the
psyche's direction + operator coordination before the working-contract
engine impl can be authored.

### Finding 2 — old and new contract surfaces cannot coexist in one crate (cutover tension)

`[patch]`-ing `signal-cloud` to the schema-derived crate poisons every
pre-schema crate that still depends on the old `signal-cloud` (the old
published `owner-signal-cloud` fails its `NotaRecord` derive: *no method
`encode` for `Provider`/`Capability`/…*). So the new engine surface
compiles, but the cloud crate cannot build **whole** until the pre-schema
45 KB surface (`lib.rs`/`daemon.rs`/`frame_io.rs`/`client.rs`) is removed.
This is the expected staged-cutover shape, not a defect — per
`active-repositories.md` §"Cutover discipline": build the replacement to
parity, run both in parallel, switch consumers one at a time, retire the
old. The prototype is the parallel-build stage.

### Finding 3 — `ObservationResult::Zones`/`Records` are query-shaped, not listing-shaped (schema flaw)

In `signal-cloud`, the `Observed` reply's `Zones`/`Records` arms carry
`ZoneQuery`/`RecordQuery` (the request types), not `ZoneListing`/
`RecordListing` (the result types). So a Cloudflare observe-effect result
has nowhere to ride home — the daemon currently replies
`request_unsupported` rather than fabricate a query-shaped result. Fix:
give `ObservationResult` listing-shaped arms (mirroring
`SemaReadOutput::Observed`). This is a cloud-schema fix I can make on
`next` directly.

### Finding 4 — cross-contract Plan/record drift → contracts must share record schema

The working `Plan` (`plan_identifier`, `domain_name`) and the owner `Plan`
(`identifier`, `zone`) differ in field names, and the two
`DomainNameSystemRecord`/`RecordKind` shapes differ between the contracts.
With two schemas, shared record types should be authored **once** and
imported via the schema language's `Import`/`Export` reuse blocks (the
Spirit 1557-1562 cross-crate `pub use … as` pattern), not re-declared
per contract. The prototype declared them self-contained per contract
(deferred-imports posture). This is the natural next refinement of the
two-schemas decision (Spirit 2568) — two contracts, one shared record
vocabulary.

### Finding 5 — single-field records lower to tuple newtypes (shape change)

`Approval { plan: PlanIdentifier }` lowers to `Approval(pub
PlanIdentifier)` (correct `schema-next` newtype rule), so callers using
`.plan` field access now use `.0` / `.payload()`. A real ergonomics shift
for the operator's `main`-track comparison to weigh.

### Finding 6 — `Output` variants must be bare, not self-aliased (authoring gotcha)

The policy schema first failed with `DuplicateSourceDeclaration` because
each `Output` variant was self-aliased (`AccountRegistered
AccountRegistered`), colliding with the same-named struct. `Output`
variants must be **bare** — they auto-resolve to same-named structs via the
`SourceTypeResolver`. Worth a one-line note in the schema-authoring skill.

### Finding 7 — `cloudflare.rs` is typed against the old contracts

The existing `ProviderClient` expects the old `signal-cloud` types
(`Zone{account,identifier,name}`, 15-variant `RecordKind`). The new
contracts use different shapes (6-variant `RecordKind`, restructured
`Zone`). `run_provider_effect` stubs the real call today; `cloudflare.rs`
must be re-typed against the generated contracts before the effect handler
does real IO.

## Next slices (the path forward)

1. **Resolve Finding 1** (psyche/operator) — pick the `SemaReadEngine`
   shape or read-via-effects, then regenerate.
2. **Author the hand-written runtime impls** end-to-end against the
   generated traits (working contract once Finding 1 lands).
3. **Share the record schema** across the two contracts via Import/Export
   (Finding 4); fix `ObservationResult` listing shape (Finding 3).
4. **Re-type `cloudflare.rs`** (Finding 7) and wire `run_provider_effect`
   to real IO (token via gopass handle only).
5. **Cutover** (operator, Finding 2) — remove the pre-schema surface so the
   crate builds whole; create the `meta-signal-cloud` GitHub repo and drop
   the local path/patch deps.
6. **Durable `Store`** — swap in-memory for `sema-engine`/redb once
   `signal-core` is removed (the decide loops don't change — SEMA is
   already behind the trait).

## Branch locators

- `primary` → `cloud-designer/next` — reports 18 + 19, the `next`-workflow skill edits.
- `cloud` → `next` (`073dcf60`) — daemon engine scaffold (both contracts), provider-IO-as-effect.
- `signal-cloud` → `next` (`ab456c41`) — working contract, compiles.
- `owner-signal-cloud` → `next` (`65b21e81`) — policy contract as package `meta-signal-cloud`, compiles. (Repo rename is a separate slice.)

All on `next`, pushed to origin, awaiting operator integration to `main`
and the operator's parallel `main`-track mirror (double-implementation
comparison).
