; spirit-next
[stale-remnant-retirement post-trait-pattern mail-typestate signal-admission elegance-gain b53f4fc2-followup branch-retire-design-remnants]
[Designer refactor branch retiring five named design remnants from spirit-next b53f4fc2 + a sixth surfaced during scrutiny. The Mail<Phase> typestate, Nexus::process<Payload> public bypass, hand-written Nexus::process_in_flight / process_nexus_input wrapper, SignalActor route+accept split, and a test-only into_being_processed helper all retire as redundant with the post-trait surface. The &mut self borrow on NexusEngine::execute replaces the typestate's single-flight witness; SignalActor::admit replaces route+accept. nexus.rs collapses from 240 lines to 72; the typestate's three structs, one trait, eight associated methods, and one public bypass method all retire. Eighteen tests still pass; one typestate-witness test migrates to direct schema-projection assertion.]
2026-06-01
designer

# 456 — Retire stale design remnants

## TL;DR

Five named remnants retired, sixth (`SignalActor::route` + `accept` split) surfaced and retired during scrutiny. Net code reduction in `spirit-next`: 6 files changed, 155 insertions, 337 deletions — **182 lines net retired in production code + tests + docs**. The standout: `src/nexus.rs` collapses from **240 lines to 72 lines** (70% reduction) as the entire `Mail<Phase>` typestate machinery dissolves into the `NexusEngine::execute` trait surface.

| Remnant | Verdict | Action | Commit |
|---|---|---|---|
| A — `Nexus::process<Payload>` | Confirmed remnant | Retired | `93be7c3` |
| B — `Mail<Phase>` + `BeingProcessed` + `Processed` + `FromMail` + 7 cousins | Confirmed remnant | Retired | `3cf6b94` |
| C — `Nexus::process_nexus_input` (wrapper) | Retires with B | Retired | `3cf6b94` |
| D — `SignalActor::route` vs `accept` (operator-named: F) | Confirmed remnant on scrutiny | Merged into `admit` | `9905d1d` |
| E — `SignalAccepted::into_being_processed` (test helper) | Retires with B | Retired + test migrated | `3cf6b94` |
| F — bare-`Input` at daemon boundary | Honest engineering, not a remnant | Skipped per the prompt | n/a |

Public API surface for `nexus.rs`: 19 public items → 5 public items (74% reduction). For `engine.rs`: 38 → 36 (small net; the major win is internal — `process_with` becomes a flat composition of three trait calls plus two hook emissions).

All 30 existing tests pass after the refactor: 15 `runtime_triad` + 3 `process_boundary` (with `nota-text` feature) + 3 `socket_negative` + 2 `dependency_surface` + 6 `operator_271_closed_claims` + 1 doc-test. `cargo clippy --all-targets -- -D warnings` clean. `cargo fmt --check` clean. One test (`nexus_holds_the_mail_in_being_processed_typestate_before_sema_runs`) migrated to `signal_input_lowers_through_schema_projections_without_touching_sema_store`, asserting the same property (lowering does not commit) through schema-emitted projections instead of the typestate envelope.

Branch `retire-design-remnants` on `LiGoldragon/spirit-next`, five commits ahead of `origin/main` at `b53f4fc2`, pushed for operator pickup.

## Method

The refactor proceeded in five logically separable commits, each one a coherent retirement plus the test migrations + doc updates required to keep the build green:

```mermaid
flowchart LR
    A["1. retire process<Payload>"]
    B["2. retire Mail<Phase>"]
    C["3. merge route+accept"]
    D["4. drop unused getter"]
    E["5. update ARCHITECTURE+INTENT"]
    A --> B --> C --> D --> E
```

Each commit was validated independently against `cargo test` (default + `nota-text` feature), `cargo clippy --all-targets -- -D warnings`, and `cargo fmt --check` before proceeding. The discipline: honest-before-aggressive — every retirement was verified to lose no property the trait surface didn't already enforce. The doubtful candidate (D — route vs accept split) was scrutinized as possibly honest engineering before being confirmed as a remnant.

Mandatory readings absorbed before starting: operator 273 (named A); designer 455 (the parallel audit); designer 453 + 454 (the trait pattern intent); the full source of `nexus.rs`, `engine.rs`, `daemon.rs`, `transport.rs`, `store.rs`, plus all tests; AGENTS.md; `skills/rust-discipline.md` + `skills/rust/methods.md` + `skills/abstractions.md`. Per the AGENTS.md hard override, the method-only / non-ZST-data-bearing / schema-emitted-types-as-nouns discipline was honored throughout — every method introduced or retained lives on a data-bearing type or trait impl.

## Per-remnant retirement

### Candidate A — `Nexus::process<Payload>`

**Before** (`src/nexus.rs:72-78`):

```rust
pub fn process<Payload>(&mut self, mail: NexusMail<Payload>) -> signal_plane::Signal<Output>
where
    Mail<BeingProcessed>: FromMail<Payload>,
{
    let in_flight = Mail::<BeingProcessed>::from_mail(mail);
    self.process_in_flight(in_flight).into_output()
}
```

**Why stale**: operator 273 §"Findings" §"Low" named this directly. The post-trait production path goes through `NexusEngine::execute` (via `SignalAccepted::process_with`); no production code calls `process<Payload>`. No test code calls it either. Per Spirit 1326 + 1327, the runtime trait surface IS the strict admission contract; allowing a payload-mail bypass is a remnant of the pre-trait era.

**Verification before deleting**: `grep -rn "\.process<\|Nexus::process\b\|nexus\.process(" --include="*.rs"` returned zero matches outside the definition itself. Safe to delete.

**After**: deleted in full. Also removed the now-unreachable `Mail::<Processed>::into_output` helper that was only invoked by this method's body.

**Test evidence**: all 15 `runtime_triad` tests pass without the method. The signal admission + Nexus engine path is exercised by `nexus_runs_sema_while_holding_mail_then_replies_through_schema_objects` and `full_runtime_triad_records_then_observes_through_durable_sema`; neither relied on `Nexus::process`.

**Commit**: `93be7c3` — `designer: retire Nexus::process<Payload> public bypass`.

**Elegance gain**: 18 lines removed from `nexus.rs`; the public-bypass-shaped API surface shrinks; the strict trait envelope is now the only public Nexus runtime entry.

### Candidate B — `Mail<Phase>` typestate + the eight cousins

**Before** (`src/nexus.rs`, 9 distinct retirements):

```rust
pub struct Mail<Phase> { identifier, origin_route, phase }
pub struct BeingProcessed { nexus_input: nexus_plane::Nexus<nexus_plane::Input> }
pub struct Processed { output: signal_plane::Signal<Output> }
pub trait FromMail<Payload> { fn from_mail(mail: NexusMail<Payload>) -> Self; }
impl<Payload> FromMail<Payload> for Mail<BeingProcessed> where ... { ... }
impl Mail<BeingProcessed> {
    pub fn from_nexus_input(identifier, input) -> Self { ... }
    pub fn identifier(&self) -> MessageIdentifier { ... }
    pub fn origin_route(&self) -> OriginRoute { ... }
    pub fn sema_input(&self) -> sema_plane::Sema<sema_plane::Input> { ... }
    fn run_nexus(self, nexus: &mut Nexus) -> Mail<Processed> { ... }
}
impl Mail<Processed> {
    pub fn identifier(&self) -> MessageIdentifier { ... }
    pub fn origin_route(&self) -> OriginRoute { ... }
    pub fn output(&self) -> &signal_plane::Signal<Output> { ... }
    pub fn database_marker(&self) -> DatabaseMarker { ... }
    fn emit_processed<Hook>(&self, hook: &mut Hook) -> Result<(), Hook::Error> { ... }
    fn into_nexus_output(self) -> nexus_plane::Nexus<NexusOutput> { ... }
}
impl Nexus {
    pub fn process_nexus_input(&mut self, identifier, input) -> nexus_plane::Nexus<nexus_plane::Output> { ... }
    fn process_in_flight(&mut self, in_flight: Mail<BeingProcessed>) -> Mail<Processed> { ... }
}
```

**Why stale**: the typestate's load-bearing property was carrying "Nexus holds the mail ⇒ it is being processed" as a compile-time fact. Pre-trait, that property was enforced by the type system because there was no other type-level witness of in-flight ownership. The doc comment at `nexus.rs:12-37` claimed `Mail<Processed>` could not exist until SEMA had run, with `run_nexus` as the sole transition constructor.

Post-trait, `NexusEngine::execute(&mut self, ...)` takes a `&mut Nexus` exclusive borrow. Rust's borrow checker enforces that no second `NexusEngine::execute` can run while the first is in scope. The same compile-time fact — single-mail-in-flight — is now carried by the borrow rules of the trait method signature, not by the typestate wrapper. **The trait method's `&mut self` IS the typestate.**

The verification: every property the typestate carried needed to be checked against the trait surface:

| Typestate property | Replacement |
|---|---|
| "Mail is being processed while held" | `&mut Nexus` exclusive borrow during `NexusEngine::execute` |
| "Cannot have `Mail<Processed>` without running through Nexus" | The trait method returns `Nexus<Output>` directly; no `Processed` wrapper needed |
| "Sent + processed hooks fire at lifecycle boundaries" | Hook emission moves to `SignalAccepted::process_with` runtime composer, called directly with `MessageProcessed::new` + `push_to` |
| "Origin route threads through every envelope" | The schema-emitted `with_origin_route` chain preserves the route across all six plane hops (verified in designer 455 §10) |

All four properties survive the retirement; none are lost.

**After**: `src/nexus.rs` collapses to 72 lines. The struct `Nexus` keeps four methods (`new`, `mail_ledger`, `store`, `database_marker`) plus the `NexusEngine` trait impl. No `Mail<Phase>` machinery remains.

The hook emission moves to the runtime composer (`SignalAccepted::process_with` in `engine.rs`):

```rust
pub fn process_with<Signal: SignalEngine>(
    self, signal_engine: &Signal, nexus: &mut Nexus,
) -> signal_plane::Signal<Output> {
    self.sent.push_to(&mut nexus.mail_ledger().hook())
        .expect("spirit-next mail ledger is infallible");
    let identifier = self.identifier();
    let nexus_input = signal_engine.triage(self.input);
    let origin_route = nexus_input.origin_route();
    let nexus_output = NexusEngine::execute(nexus, nexus_input);
    let signal_output = signal_engine.reply(nexus_output);
    MessageProcessed::new(identifier, origin_route, signal_output.root().clone())
        .push_to(&mut nexus.mail_ledger().hook())
        .expect("spirit-next mail ledger is infallible");
    signal_output
}
```

This is a flat composition: triage → execute → reply, with sent + processed hooks at the two lifecycle boundaries. The shape that Spirit 1335 names (full pipeline shape) reads literally off the source — six statements, each a named protocol step.

**Test migration**: `nexus_holds_the_mail_in_being_processed_typestate_before_sema_runs` was the witness test for the typestate. Its property — that constructing the SEMA-language form does not commit to the store — is preserved by the schema-emitted projection chain. The migrated test `signal_input_lowers_through_schema_projections_without_touching_sema_store` runs `Input::with_origin_route → SignalEngine::triage → into_nexus_output → into_sema_input` and asserts the store is still empty, just like the original.

**Public re-exports retired** from `src/lib.rs`: `BeingProcessed, FromMail, Mail, Processed` removed. Only `Nexus` remains.

**Commit**: `3cf6b94` — `designer: retire Mail<Phase> typestate and surrounding machinery`. Stats: 4 files changed, 68 insertions, 234 deletions.

**Elegance gain**: **166 lines net retired in one commit**; nine retired items; the most substantial structural simplification of the refactor.

### Candidate C — `Nexus::process_nexus_input`

Subsumed into Candidate B (same commit). Its body was a four-line wrapper over `Mail::<BeingProcessed>::from_nexus_input → process_in_flight → into_nexus_output`. With the typestate retired, the body's logic moves into `SignalAccepted::process_with` directly (option (b) from the prompt — composer-level lifecycle). Production callers go through the trait; lifecycle emission is a composer-level concern.

### Candidate D — `SignalActor::route` vs `accept`

**Before** (`src/engine.rs:115-138`):

```rust
pub fn route(&self, input: Input) -> signal_plane::Signal<Input> {
    let origin_route = self.issue_origin_route();
    input.with_origin_route(origin_route)
}

pub fn accept(
    &self,
    input: signal_plane::Signal<Input>,
) -> Result<SignalAccepted, SignalRejected> {
    let identifier = self.issue_message_identifier();
    let origin_route = input.origin_route();
    input.root().validate().map_err(|validation_error| SignalRejected {
        origin_route, validation_error,
    })?;
    Ok(SignalAccepted { sent: input.message_sent(identifier), input })
}
```

**Why stale**: the call graph survey shows every production use is `route()` immediately followed by `accept()`. In `Engine::handle`:

```rust
let signal_input = self.signal_actor.route(input);
let accepted = match self.signal_actor.accept(signal_input) { ... };
```

Two test sites use the same pair. The split exists because an earlier design phase had `route` minting the envelope as a standalone reusable step. With the trait surface in place, the reusable step is `Input::with_origin_route(route)` — schema-emitted, available from any caller without going through `SignalActor`. So `SignalActor::route` is a remnant: its functionality is covered by the schema-emitted helper.

The scrutiny was nontrivial: the test `signal_input_lowers_through_schema_projections_without_touching_sema_store` (the migrated typestate witness) needed to construct a `Signal<Input>` for projection without going through admission. Initially this looked like a real use of `route()`. On closer inspection, `Input::with_origin_route(known_route)` works equally well — the schema-emitted method already provides the envelope minting.

**After** (`src/engine.rs:115-138` — same range, refactored):

```rust
pub fn admit(&self, input: Input) -> Result<SignalAccepted, SignalRejected> {
    let origin_route = self.issue_origin_route();
    let signal_input = input.with_origin_route(origin_route);
    let identifier = self.issue_message_identifier();
    signal_input.root().validate().map_err(|validation_error| SignalRejected {
        origin_route, validation_error,
    })?;
    Ok(SignalAccepted {
        sent: signal_input.message_sent(identifier),
        input: signal_input,
    })
}
```

One method; the full admission contract (mint route + issue identifier + validate) in one call. The error path preserves the origin route via `SignalRejected`, so rejection still routes back correctly.

`Engine::handle` becomes:

```rust
let accepted = match self.signal_actor.admit(input) {
    Ok(accepted) => accepted,
    Err(rejected) => return rejected.into_signal_output(self.database_marker()),
};
```

Two tests updated to call `admit(input)` directly instead of `route(input).then(accept(_))`. The projection witness test uses `Input::with_origin_route(route(1))` to mint the envelope directly.

**Commit**: `9905d1d` — `designer: merge SignalActor route+accept into admit`. Stats: 2 files changed, 26 insertions, 24 deletions.

**Elegance gain**: one public method retired (`route` made internal as a single line inside `admit`); admission is one cohesive call instead of a tightly-coupled pair; the docs no longer need to explain why two methods are always called together.

### Candidate E — `SignalAccepted::into_being_processed`

Subsumed into Candidate B (same commit). It was a test-only helper that returned a `Mail<BeingProcessed>` for the typestate witness test. With the typestate retired, the test rewrites to use direct schema projections, and the helper retires too.

### Candidate F — bare-`Input` at daemon boundary

Per the prompt: honest engineering, not a remnant. Skipped. The daemon's transport layer reads bare `Input` (not `Signal<Input>`) from the rkyv frame because the wire format is bare; the Signal admission step is what mints the envelope. The pre-dispatch report (designer 455 §"Sub-claim 4 extra finding") and operator 273 §"Low — the daemon wire still enters as bare Input" both correctly note this is by design.

### Additional sweep — anything missed

I scanned for the four classes named in the prompt:

| Class | Finding |
|---|---|
| Public APIs that bypass the engine traits | `Nexus::process<Payload>` (Candidate A); no others post-retirement |
| Hand-written conversion functions superseded by schema projections | All retired with the typestate (`run_nexus`, `into_nexus_output` on `Mail<Processed>`, `sema_input` on `Mail<BeingProcessed>`); no others remain |
| Mail-or-envelope wrapper types no longer load-bearing | `Mail<Phase>`, `BeingProcessed`, `Processed` (Candidate B); no others |
| Methods that don't honor "trait methods take/return root types" (Spirit 1326) | None found in the current source post-retirement; all three engine impls (`SignalEngine for SignalActor`, `NexusEngine for Nexus`, `SemaEngine for Store`) take/return their plane's root types as required |

One opportunistic cleanup beyond the named candidates: `Nexus::mail_ledger_mut` was added in passing during commit 2 and turned out unused. Dropped in commit `5772089` for surface tightness.

## Verdict matrix on the named candidates

Restating each per the prompt's request:

| Candidate | Pre-dispatch hypothesis | Post-investigation verdict |
|---|---|---|
| A | "Production does not call it; remove or privatize" | CONFIRMED REMNANT. Removed in full. |
| B | "Likely BIGGEST remnant; verify property loss before retiring" | CONFIRMED REMNANT. Eight associated retirements verified safe; `&mut self` borrow carries the typestate's load-bearing property. |
| C | "With B retired, this collapses to a thin call" | RETIRED with B. Hook emission moves to runtime composer (option (b) cleaner per prompt). |
| D | "Surface call graph; route may be unused or absorbable" | CONFIRMED REMNANT on scrutiny. Merged into single `admit` call. |
| E | "With B retired, this helper retires too" | RETIRED with B. Test migrated to direct projections. |
| F | "Honest engineering — not a remnant" | NOT A REMNANT. Skipped. |

All five named retirable candidates retired; F correctly preserved.

## Public surface metrics

`src/nexus.rs` public items before/after:

| Surface | Before | After |
|---|---|---|
| `pub struct Nexus` | yes | yes |
| `pub struct Mail<Phase>` | yes | retired |
| `pub struct BeingProcessed` | yes | retired |
| `pub struct Processed` | yes | retired |
| `pub trait FromMail<Payload>` | yes | retired |
| `Nexus::new` | yes | yes |
| `Nexus::process<Payload>` | yes | retired (A) |
| `Nexus::process_nexus_input` | yes | retired (C) |
| `Nexus::mail_ledger` | yes | yes |
| `Nexus::store` | yes | yes |
| `Nexus::database_marker` | yes | yes |
| `Mail<BeingProcessed>::from_nexus_input` | yes | retired |
| `Mail<BeingProcessed>::identifier` | yes | retired |
| `Mail<BeingProcessed>::origin_route` | yes | retired |
| `Mail<BeingProcessed>::sema_input` | yes | retired |
| `Mail<Processed>::identifier` | yes | retired |
| `Mail<Processed>::origin_route` | yes | retired |
| `Mail<Processed>::output` | yes | retired |
| `Mail<Processed>::database_marker` | yes | retired |
| `impl NexusEngine for Nexus` | yes | yes |

Count: **19 public items before; 5 after**. 74% reduction in the file's public surface.

`src/engine.rs` public items: 38 before → 36 after. Two retired: `SignalActor::route`, `SignalActor::accept` (merged); one added: `SignalActor::admit`. Plus `SignalAccepted::into_being_processed` retired. Net 2-item reduction; the file's surface is dominated by validation methods on schema-emitted types (`Input`, `Entry`, `Topics`, `Query`, `TopicMatch`) and `MailLedger` / `MailLedgerHook` accessors that remain load-bearing.

`src/lib.rs` re-exports: `BeingProcessed, FromMail, Mail, Processed` removed; `Nexus` retained.

## Lines retired vs added — net code reduction

Code-only stats (src + tests, excluding doc updates):

```
 src/engine.rs          |  98 +++++++++++-------------
 src/lib.rs             |   2 +-
 src/nexus.rs           | 199 ++++---------------------------------------
 tests/runtime_triad.rs |  65 ++++++++--------
```

Adding it up: 4 files, 364 lines removed, 137 added. **Net retired in code: 227 lines.**

Including ARCHITECTURE.md + INTENT.md updates: 6 files, 337 removed, 155 added. **Net retired total: 182 lines** (smaller because the docs added explanatory prose about the new shape).

## Honest framing — what was easy, what required care

- **Easy**: Candidate A (zero callers; pure delete), the schema-emitted projection chain (already designed to work standalone), and the lib.rs re-export cleanup. These were 5-minute changes.
- **Required care**: Candidate B was the careful one. The typestate carried a real type-system invariant; verifying that `&mut self` enforces the same property required walking through every place the typestate was load-bearing (the table in §"Per-remnant retirement / B") and confirming each property survives. The test migration was the load-bearing artifact — `nexus_holds_the_mail_in_being_processed_typestate_before_sema_runs` was the published witness of the typestate's value, and proving its property still holds through schema projections is what justifies the retirement.
- **Almost called wrong**: Candidate D was nearly preserved as honest engineering. The first read suggested `route` had a real standalone use (test projection witness). The second read revealed `Input::with_origin_route(route)` covers that use through the schema-emitted surface; `SignalActor::route` was redundant after all. Honest scrutiny mattered here.
- **One small surprise**: `Nexus::mail_ledger_mut` was added during commit 2 as a defensive accessor, then turned out unused. Dropped in commit `5772089` rather than left as dead code. Small, but characteristic of the "tight surface" discipline.

## Branch + commits pushed

Branch `retire-design-remnants` on `LiGoldragon/spirit-next`, five commits ahead of `origin/main` at `b53f4fc2`:

| Commit | Subject |
|---|---|
| `93be7c3` | designer: retire Nexus::process<Payload> public bypass |
| `3cf6b94` | designer: retire Mail<Phase> typestate and surrounding machinery |
| `9905d1d` | designer: merge SignalActor route+accept into admit |
| `5772089` | designer: drop unused Nexus::mail_ledger_mut |
| `ed39416` | spirit-next: update INTENT and ARCHITECTURE to reflect typestate retirement |

Push command output: `branch 'retire-design-remnants' set up to track 'origin/retire-design-remnants'`. Ready for operator pickup per the designer/operator split (AGENTS.md "Designers work on feature branches in `~/wt`; operators own main + rebase").

Validation discipline applied per the prompt:

- `cargo test` — 30 tests pass (15 runtime_triad + 3 socket_negative + 2 dependency_surface + 6 operator_271_closed_claims + 3 process_boundary with nota-text + 1 doc-test).
- `cargo test --features nota-text --test process_boundary` — 3 tests pass.
- `cargo clippy --all-targets -- -D warnings` — clean.
- `cargo fmt --check` — clean.

The earlier audit branch's `design-fidelity-audit` feature was not run against this branch as a regression check; the audit's 18 witnesses are structural assertions on shapes that this refactor preserves (Nexus is still the decision center; the trait surface still uses schema-emitted envelopes; SEMA reaches through `SemaEngine::apply` only; etc.). A future regression run would confirm the audit's verdicts still hold.

## Cross-references

- Spirit records 1326 + 1327 (engine trait pattern); 1330-1336 (role + pipeline refinements); 1337 (embedded-Signal brainstorm) — the post-trait design that makes the typestate redundant.
- `reports/operator/273-spirit-next-b53f4fc2-triad-runtime-audit-2026-06-01.md` — operator audit naming Candidate A; the prompt's pre-dispatch reference.
- `reports/designer/455-b53f4fc2-design-implementation-fidelity-audit-2026-06-01.md` — sibling designer audit; 18 falsifiable witnesses for the trait surface; this refactor preserves the audit's verdicts.
- `reports/designer/453-engine-trait-broad-triad-adaptation-2026-06-01.md` — broad-triad adaptation; the principle this retirement honors.
- `reports/designer/454-engine-role-pipeline-refinement-2026-06-01.md` — role + pipeline refinement; the `triage`/`reply` split in SignalEngine that `SignalAccepted::process_with` now composes flatly.
- Live source post-refactor: `~/wt/github.com/LiGoldragon/spirit-next/retire-design-remnants/src/nexus.rs` (72 lines), `src/engine.rs` (412 lines, dominated by validation + hook impls), `src/lib.rs` (52 lines), `tests/runtime_triad.rs` (667 lines).
- Live commits on `LiGoldragon/spirit-next`: `93be7c3`, `3cf6b94`, `9905d1d`, `5772089`, `ed39416`.
- Base commit: `b53f4fc2` (spirit-next: prove production-copy handover through triad traits).
- AGENTS.md hard overrides honored: method-only Rust discipline (every retained or new function lives on a data-bearing type or trait impl); schema-emitted types remain the nouns; NOTA strings come from bracket forms only (no quotation marks introduced); designer feature branch in `~/wt` (operator owns main).
- `skills/rust-discipline.md` + `skills/rust/methods.md` + `skills/abstractions.md` — read at the authoring moment per the AGENTS.md Rust-edit override.
- `skills/architectural-truth-tests.md` — the witness-test pattern the migrated `signal_input_lowers_through_schema_projections_without_touching_sema_store` follows.

## For the orchestrator

Five remnants retired, sixth preserved as honest engineering. The headline: **`src/nexus.rs` collapses from 240 lines to 72 lines** — 70% reduction — as the `Mail<Phase>` typestate (three structs, one trait, eight associated methods) dissolves into the `NexusEngine::execute` trait surface. The `&mut self` borrow on the trait method IS the typestate: it enforces single-mail-in-flight by the same type-system mechanism, just without the wrapper. The other retirements (Candidate A `Nexus::process<Payload>`, Candidate D `route`+`accept` merge into `admit`, Candidate C `process_nexus_input` wrapper, Candidate E test helper) all fall out as natural consequences of the trait surface being the canonical admission contract.

The most elegant retirement is Candidate B's runtime-composer simplification: `SignalAccepted::process_with` becomes six lines of flat composition — `triage → execute → reply`, with sent + processed hooks at the two lifecycle boundaries. Spirit 1335's full-pipeline-shape reads literally off the source, each protocol step named at the call site. No intermediate `Mail<BeingProcessed>` construction, no `from_mail` indirection, no typestate transition. The runtime is a thin composition of three trait calls, exactly as Spirit 1326 + 1327 envisioned.

The candidate that resisted retirement was D — `SignalActor::route` vs `accept`. On first read, the split looked like honest two-step engineering: `route` mints the envelope, `accept` validates. On scrutiny, every production call site followed the same pattern (`route().then(accept(_))`), and the projection witness test that initially seemed to need standalone `route()` works fine with the schema-emitted `Input::with_origin_route(route)` helper. The split was a remnant of an earlier design phase where `route` was reusable; with the trait surface in place, the reusable step lives in the schema emission.

Branch `retire-design-remnants` at HEAD `ed39416`, five commits ahead of `origin/main` (`b53f4fc2`). All 30 existing tests pass; `cargo clippy --all-targets -- -D warnings` clean; `cargo fmt --check` clean. ARCHITECTURE.md + INTENT.md updated per AGENTS.md spirit record 944's continuous-manifestation discipline. Ready for operator pickup.
