## 7 — signal-persona migration: deeper holes after /244 + /245

**Lane:** second-operator-assistant
**Reads against:** report 6 (the migration writeup),
`reports/designer/244-hole-finding-after-243-implementations.md`,
`reports/designer/245-design-alternatives-for-244-holes.md`,
`reports/operator/140-signal-frame-executor-hole-analysis.md`
(operator's response to /244 + /245 with sharper designs for three
of the five holes — see §3 below for cross-walk),
and the macro source at
`/git/github.com/LiGoldragon/signal-frame/macros/src/{validate.rs,emit.rs}`.

## 0 · TL;DR

Re-analysing the migration with the macro source open and /244+/245
in context surfaces **one root-cause bug in `signal-frame`'s macro
validation** that produced cascading scar tissue across the migrated
contract, plus four sharper findings that report 6 either missed or
under-named. Five severity-ranked items:

| # | Finding | Severity | Status vs report 6 |
|---|---|---|---|
| 1 | **`validate_record_head_uniqueness` is incorrect for the case-1 variant-wrapped encoding the macro actually emits.** The check rejects two variants that share a payload TYPE name; the wire dispatches on the VARIANT name. The check is a relic of a different (case-2 tag-less) encoding strategy. | **High** | New — report 6 §1 named the symptom; this names the root cause. |
| 2 | **Six one-field wrapper structs add a parens layer with no information content** (`ComponentStartup`, `ComponentShutdown`, `ComponentReady`, `ComponentNotReady`, `ComponentHealthReport`, `GracefulStopAcknowledgement`, `SupervisionUnimplemented`). The first two are scar tissue from #1. The other four are independent ESSENCE-beauty violations. | **High** | New axis — report 6 §6 noted inconsistency, not the broader pattern. |
| 3 | **Two of three hand-rolled NotaSum codecs were unnecessary.** The engine `Query` and `supervision::Query` enums both have all-newtype variants; `NotaSum` derive supports that case (verified in `nota-derive/src/nota_sum.rs`). Only `SupervisionUnimplementedReason` (mixed unit + data) genuinely needs hand-rolling. | **High** | Sharpens report 6 §2 — it conflated three cases as one. |
| 4 | **Single-variant `*Scope` enums violate ESSENCE's "today's piece is held to ESSENCE's full priorities, not as a draft of the eventual."** `EngineCatalogScope::AllEngines` and `EngineStatusScope::WholeEngine` carry zero distinction today; scaffolding for a future second variant. | **Medium** | Report 6 §3 raised it as an open question; ESSENCE settles the question. |
| 5 | **/140's refined fix for /244+/245 should land BEFORE the persona-* daemon cascade — not after, and not /245 literally.** signal-persona is contract-only so it sidestepped /244 holes 1-4. The daemons that consume it (`signal-persona-mind`, `-router`, `-message`, `-harness`, `-terminal`) all face them on first contact. /140 sharpens /245 on holes 1, 2, 4 and flags hole 3 as needing another design pass — take /140's shape. | **High** | New — report 6 §"pending follow-up" listed the cascade but didn't sequence it. |

Plus three smaller cross-walk items in §5.

## 1 · The root cause hole

### Finding 1 · `validate_record_head_uniqueness` contradicts `emit_payload_enum_codec`

**What I see.** `signal-frame/macros/src/validate.rs` lines 143-201:

```rust
fn validate_record_head_uniqueness(spec: &ChannelSpec) -> syn::Result<()> {
    // The NOTA decoder dispatches by record head, not by Rust type
    // path. `domain_a::Status` and `domain_b::Status` both project to
    // `(Status ...)`, so they collide inside the same payload enum.
    flag_duplicate_record_heads(
        spec.request.variants.iter()
            .map(|v| (&v.variant_name, &v.payload_type)),
        "request",
    )?;
    // ...
}

fn projected_record_head(payload: &Type) -> String {
    // Takes the last `::`-segment of the payload TYPE name.
    let payload_text = quote::quote!(#payload).to_string().replace(' ', "");
    payload_text.rsplit("::").next().unwrap_or(&payload_text).to_string()
}
```

The check projects the *payload type's* record head and rejects
duplicates. Meanwhile `emit.rs` lines 546-571 emits the actual codec:

```rust
let encode_arms = kinds.iter().map(|k| {
    let variant = &k.variant;
    let variant_string = variant.to_string();
    quote! {
        Self::#variant(payload) => {
            encoder.start_record(#variant_string)?;  // ← variant name as record head
            payload.encode(encoder)?;
            encoder.end_record()
        }
    }
});
let decode_arms = kinds.iter().map(|k| {
    let variant = &k.variant;
    let variant_string = variant.to_string();
    let payload = &k.payload;
    quote! {
        #variant_string => {
            decoder.expect_record_head(#variant_string)?;  // ← matches variant name
            // ...
        }
    }
});
```

The actual emission is **case 1 of the three-case PascalCase rule**:
the variant name is the record head; the payload encodes itself
inside the outer record. The decoder dispatches on the variant name.

The validation's premise — "two variants with the same payload type
collide on the wire" — describes case 2 (tag-less struct encoding),
which the macro does NOT emit.

**Confirmation from `nota-derive`.** `nota_sum.rs` uses the same
variant-name dispatch strategy (`encoder.start_record(variant_string)`
on encode; `decoder.expect_record_head(variant_string)` on decode).
It has no equivalent "duplicate payload type" check because the
check would be wrong there too.

**What the validation should check** (if anything): the variant
NAMES (already covered by `validate_variant_uniqueness`). The
payload type name is irrelevant to wire ambiguity under case-1
dispatch.

**Why it's a hole.** The check forces every contract author whose
domain has two lifecycle operations on the same identifier type
(`Start` / `Stop` over a `ComponentName`, `Open` / `Close` over a
`FileDescriptor`, `Mount` / `Unmount` over a `Path`) to invent
distinct one-field wrapper types. The wrappers add a parens layer
to the wire form, add a Rust type per variant, and the discipline
the workspace's ARCH naming rules ask for ("don't carry redundant
ancestry, lift repeated prefixes into structure") falls apart
because the wrappers DO carry redundancy by construction.

**Severity.** High. The check actively damages contract design
across every contract that has a verb pair over a shared identifier.
Removing the check is a 1-function deletion in `validate.rs` plus
removal of the now-empty helper.

**What does this cost me in signal-persona, concretely?**
Two payloads — `ComponentStartup` and `ComponentShutdown` —
exist solely because of this check. The contract's wire form is
`(Start (persona-router))` / `(Stop (persona-router))` where the
inner `(persona-router)` is `ComponentStartup`'s tag-less struct
encoding of one field; under the fix it would be
`(Start persona-router)` / `(Stop persona-router)` — exactly the
wire form the supervision channel already uses for
`SupervisionOperation::Stop(ComponentName)`.

## 2 · Cascade holes from the migration

### Finding 2 · Six one-field wrapper structs add a parens layer with no info content

Stack-rank by inability-to-justify:

| Wrapper | Single field | Wire shape | Without wrapper |
|---|---|---|---|
| `ComponentStartup { component: ComponentName }` | `ComponentName` | `(Start (persona-router))` | `(Start persona-router)` |
| `ComponentShutdown { component: ComponentName }` | `ComponentName` | `(Stop (persona-router))` | `(Stop persona-router)` |
| `ComponentReady { component_started_at: Option<TimestampNanos> }` | `Option<TimestampNanos>` | `(Ready (None))` | `(Ready None)` |
| `ComponentNotReady { reason: ComponentNotReadyReason }` | `ComponentNotReadyReason` | `(NotReady (NotYetBound))` | `(NotReady NotYetBound)` |
| `ComponentHealthReport { health: ComponentHealth }` | `ComponentHealth` | `(HealthReport (Running))` | `(HealthReport Running)` |
| `GracefulStopAcknowledgement { drain_completed_at: Option<TimestampNanos> }` | `Option<TimestampNanos>` | `(StopAcknowledged (None))` | `(StopAcknowledged None)` |
| `SupervisionUnimplemented { reason: SupervisionUnimplementedReason }` | `SupervisionUnimplementedReason` | `(Unimplemented ((NotInPrototypeScope)))` | `(Unimplemented (NotInPrototypeScope))` |

The first two are forced by Finding 1. The other five are
independent choices the migration made. Each adds:

- One Rust type that names nothing the variant doesn't already name.
- One parens layer to the wire form.
- One field-projection step at every consumer's match site
  (`if let Ready(c) = … { c.component_started_at }` vs
  `if let Ready(t) = … { t }`).

**The /241 rule from `skills/contract-repo.md` §"Anti-pattern:
repeated category words":** "if a word recurs across siblings, the
schema is missing a namespace that would supply it. ... names carry
only what the schema's structure doesn't carry; when names repeat a
word, that word should become structure." Applied to reply payloads:
when the *only field* of a struct named after a reply variant
duplicates information the variant already carries, the struct is
that missing namespace and the variant IS the structure. Drop the
struct.

**Why the migration landed it this way.** The pre-migration shape
had wrapper structs (`EngineLaunchProposal`, `ComponentReadiness`,
etc.) and the migration preserved them under new names. The "name
the relation" intuition is real but the threshold should be:
*the struct carries more than one field*. Single-field wrapper =
the variant already names the relation; drop the wrapper.

**The single justified single-field struct in the contract:**
none of the seven listed here. Mark them as scar tissue.

**Severity.** High. Each of these is a wire form that future
consumers will lock in; once external clients depend on the
shape, the cleanup gets harder.

### Finding 3 · Two of three hand-rolled NotaSum codecs were unnecessary

`nota-derive/src/nota_sum.rs` lines 40-89 supports two variant
shapes: **newtype** (`Foo(Inner)` → `(Foo <inner>)`) and **struct**
(`Foo { … }` → `(Foo field0 field1 …)`). It rejects unit variants
(line 90) and asks you to use `NotaEnum` for unit-only enums.

In signal-persona, three enums hand-roll codecs:

| Enum | Variant shapes | NotaSum derive applicable? |
|---|---|---|
| `Query` (engine relation) | 3 × newtype | **Yes** — all newtypes. |
| `supervision::Query` | 2 × newtype | **Yes** — all newtypes, both with the same payload type (`ComponentName`); the derive dispatches on the variant name, so this works. |
| `SupervisionUnimplementedReason` | 1 × unit + 2 × newtype | **No** — mixed variant kinds; the derive panics on `NotInPrototypeScope`. |

Report 6 §2 stated the problem as "neither derive applies when an
enum has *some* unit variants and *some* data-carrying ones." That
diagnosis is correct for `SupervisionUnimplementedReason` but the
migration applied the same workaround to two enums that didn't need
it. Result: ~50 lines of hand-rolled codec for the two `Query` enums
that could be replaced with `#[derive(NotaSum)]`.

**The genuine NotaSum-derive gap** is the mixed unit + data-carrying
case. `SupervisionUnimplementedReason` has both `NotInPrototypeScope`
(unit) and `DependencyMissing(DependencyKind)` (data). The fix is
the same as Hole 4 in /244: extend `nota-derive` to emit case-3
(bare PascalCase) for unit variants alongside case-1
(`(VariantName payload)`) for data-carrying ones. The three-case
PascalCase rule already covers this on the wire; the derive doesn't.

**Severity.** High for the principle (derives that exist should be
used; hand-rolling is the escape hatch, not the default); Medium
for the immediate fix (delete two codec blocks, add two derives).

### Finding 4 · Single-variant `*Scope` enums are scaffolding rejected by ESSENCE

```rust
pub enum EngineCatalogScope {  // 1 variant
    AllEngines,
}
pub enum EngineStatusScope {  // 1 variant
    WholeEngine,
}
```

`ESSENCE.md` §"Today and eventually — different things, different
names": *"Today's narrower piece is held to ESSENCE's full
priorities — built rightly for its scope, not as a draft of the
eventual."* And §"Beauty is the criterion": special cases should
dissolve into the normal case, not stand as their own scaffolding.

These enums add:
- A type that says "the only thing we do here today."
- A wire token (`AllEngines`, `WholeEngine`) that carries no
  information at decode time — the receiver already knows.
- A discriminator the call site must spell every time:
  `Query::Catalog(EngineCatalogScope::AllEngines)` instead of
  `Query::Catalog`.

The eventual second variant — date range, generation filter,
selective component scope — IS expected to land. Per ESSENCE's
non-optimisation rule: *"Not backward compatibility for systems
being born."* When the second variant is real, introduce the
enum; until then, the variant is unit. The cost of adding the
enum later (one new variant on `Query`, all call sites updated)
is paid once and the call sites are the contract author's own —
internal coordinated upgrade, no external semver constraint.

**Severity.** Medium. Aesthetic but persistent; every consumer
pays the verbosity at every read site.

**Cleaner shape today:**

```rust
pub enum Query {
    Catalog,                       // unit variant (case 3)
    EngineStatus,                  // unit variant (case 3)
    ComponentStatus(ComponentName), // newtype (case 1)
}
```

But: this is precisely the **mixed unit + data-carrying** case
that Finding 3 just named as the genuine `NotaSum`-derive gap.
The fix lives in `nota-derive`; the cleaner shape here depends
on it. Until then, two paths:

- **A:** Add the `nota-derive` mixed-variant support, then
  collapse the scope enums.
- **B:** Collapse the scope enums and accept hand-rolled codec
  for `Query` until A lands.

A is the right shape (the derive should cover the language's own
three-case rule); B is a transitional shape — explicitly the kind
of compromise ESSENCE §"Backward compatibility is not a
constraint" warns against. The right move is to file A as the
gating item and not land B.

## 3 · Cross-walk: report 6 against /244 + /245 + the skill edits since

### What /244 + /245 supersede in report 6

**Report 6 §4 — "Reply-variant naming discipline is unwritten."**
Closed by /243's skill edit to `skills/contract-repo.md`
§"Reply discipline" (commit `a7f3a0ee`): past-tense for outcomes,
`*Rejected` for rejection variants, `Action*` pair for
lifecycle-shaped verbs, verb→noun-collision fallthrough rule. Also
ratifies the supervision channel's `Identified` naming as the
correct fallthrough for `Announce` → `Announcement` (noun collision).
**This part of report 6 is now historical.**

**Report 6 §7 — "Cross-relation Query operation name reuse."**
Still open. `skills/contract-repo.md` §"Public contracts use
contract-local operation verbs" notes that "same verb spelling
across contracts is allowed" — but signal-persona has same verb
spelling across two *relations within the same contract*. The
skill doesn't address the within-crate case. Module qualification
(`signal_persona::Query` vs `signal_persona::supervision::Query`)
disambiguates at use sites, which is fine; worth a sentence in the
skill that within-crate reuse is also allowed and that module
splits are the disambiguation.

### What /244 + /245 add that report 6 didn't anticipate

The five /244 holes split: signal-persona is contract-only, so it
sidesteps holes 1-4 directly, but the persona daemon cascade
(`-mind`, `-router`, `-message`, `-harness`, `-terminal`) faces
all four on first contact. /245 proposed bundled fixes; operator's
report 140 sharpened three of them substantially. Where /140
improves over /245, take /140's shape.

**/244 hole 1 (typed rejection on the wire).** /245 said `lower()`
returns `Result<Vec<SemaOperation>, Self::Reply>` and the executor
passes the contract reply through as the wire `Reply`. **/140
corrects this:** `signal-frame::Reply::Rejected` has no payload
slot, and that is the right kernel shape — kernel rejection stays
kernel-shaped. The contract reply lives inside `SubReply::Failed.detail`
on a `Reply::Accepted { outcome: AcceptedOutcome::Aborted,
per_operation: [Invalidated, Failed { detail: Some(contract_reply) },
Skipped] }`. For multi-operation requests this also gives a
principled answer for what the *other* operations report
(Invalidated for earlier, Skipped for later). **Without this fix,
signal-persona's typed rejection reply variants
(`LaunchRejected`, `RetireRejected`, `ActionRejected`) are
dead-letter on the wire.** Land /140's encoding shape, not /245's
flat passthrough.

**/244 hole 2 (`Observe` collision).** Doesn't bite signal-persona
yet (no `observable` block). Will bite the daemons. /245 proposed
`operation_open Watch(Filter) opens ObserverStream, operation_close
Unwatch(ObserverToken)`. **/140's grammar is tighter:**

```rust
observable {
    open Watch(Filter);
    close Unwatch;
    filter Filter;
    event OperationReceived;
    event SemaEffectEmitted;
}
```

The contract author writes `open <Verb>(<FilterType>);` and
`close <Verb>;` — the macro infers the close payload type. Same
expressivity, less boilerplate.

**/244 hole 3 (publish-bridge).** /245 said "move `ObserverChannel`
to signal-frame; macro emits the impl." **/140 pushes back:** the
crate-ownership boundary is non-trivial. The macro publishes
concrete event records (`OperationReceived`, `SemaEffectEmitted`);
the executor publishes source facts (`Operation`, `SemaEffect`).
Something must project execution facts into channel event records,
and `signal-frame` cannot depend on `signal-executor` (one-directional
dependency). /140 names four candidate resolutions and says **"do
not implement 245 hole 3 literally yet — first decide the observer
event projection boundary."** Treat this as the gating design
question for the persona daemon cascade.

**/244 hole 4 (filter-match trait impl is contract-author-trusted).**
Doesn't apply to signal-persona today. /140 proposes the keyword
`filter default;` as the opt-in for the macro-emitted closed-enum
filter set; contract authors only write custom filters when the
defaults can't express the selection.

**/244 hole 5 (no end-to-end worked example).** signal-persona
won't be the worked example — it's contract-only. /140 sequences
the worked example concretely: finish library fixes →
`signal-repository-ledger` ARCH update → `repository-ledger`
pinned to the latest contract → `Lowering` impl → one live test
exercising open-stream → submit → OperationReceived → commit →
SemaEffectEmitted → typed operation reply.

**Bigger rethinks /245 floated.** /140 rejects all four (universal
observability, executor in macro, drop kernel Reply, contract-
extensible Sema) with justification. The persona daemon cascade
should plan on /140's conservative direction: observability stays
opt-in, executor stays a library, kernel `Reply` stays (narrowed),
Sema's six-root vocabulary stays closed.

### Sequencing implication

The /244+/245+/140 fixes are LOAD-BEARING for the persona daemon
cascade. Report 6 §"Pending follow-up" listed the cascade as if it
were just mechanical rename work. It isn't. The cascade should be:

1. Land /140's refined fix for /244 holes 1, 2, 4 (typed rejection
   via `AcceptedOutcome::Aborted` + per-op `Failed.detail`; tighter
   `observable { open / close }` grammar; `filter default;`
   keyword).
2. Resolve the /140 §"Hole 3" projection-boundary design question
   (the four-candidate resolution). This is the gating design pass
   before any daemon adopts observability.
3. Adopt `observable` in `signal-repository-ledger` per /140's
   sequencing (library fixes → contract ARCH → daemon update →
   `Lowering` impl → one live worked test).
4. Then cascade signal-persona-{mind,router,message,terminal,harness}
   onto the settled macro + executor.
5. The daemon cascade picks up `observable` blocks, typed rejection
   replies, and `ObserverChannel` impls AS PART OF the refactor —
   not as a separate retrofit later.

Doing the cascade BEFORE steps 1-3 means each daemon either invents
hand-rolled adapters (technical debt) or skips observability
entirely (functional debt). Either way, retrofitting costs more
than landing in order.

## 4 · The deeper hole

The five findings above share a generator: **`signal-frame`'s
macro grew faster than the discipline that should constrain it.**

- Finding 1: a validation rule from an older encoding strategy
  survived a refactor of the emission strategy.
- Finding 2: the one-field-wrapper habit propagated through the
  contract because the macro's first-error-on-collision pushed
  the author toward "make payload types distinct" rather than
  "fix the validation."
- Finding 3: `NotaSum` derive exists and works for newtype
  variants; the hand-rolled codecs were defensive copies because
  the derive's failure mode (panic on mixed variants) wasn't named
  in the macro docs.
- Finding 4: `EngineCatalogScope::AllEngines` exists because the
  macro accepts it and ESSENCE's "today's piece is built rightly
  for its scope" rule wasn't surfaced during the migration's
  schema review.
- Finding 5: the macro shipped without the executor pattern that
  consumes its output; daemons will pay the integration tax until
  /245's bundled fix lands.

The root remediation is editorial discipline at the macro layer:
the validation rules, the derive coverage, and the executor
integration should be re-audited as one set before the daemon
cascade. `skills/contract-repo.md` § "Public contracts use
contract-local operation verbs" is the part of the discipline
that holds; the macro should be brought into alignment with it.

## 5 · Smaller cross-walk items

### A — Migration ARCHITECTURE.md surface relation analysis

`skills/contract-repo.md` §"Contracts name a component's wire
surface" asks every contract to name (1) endpoints, (2) cardinality,
(3) direction, (4) authority, (5) lifecycle vectors per relation.
The migrated `signal-persona/ARCHITECTURE.md` has a relation
surface table per the report 6 change-list, but I haven't verified
which of the five points it covers. **Action item: re-read ARCH
and check the five-point coverage for each of Engine and
Supervision relations; gap-fill what's missing.**

### B — `EngineReply` payload-type stutter

`EngineReply::EngineStatus(EngineStatus)` and
`EngineReply::ComponentStatus(ComponentStatus)` — variant name and
payload type repeat. Report 6 §8 accepted this as "status quo."
Per `skills/naming.md` §"Anti-pattern: prefixing names with their
namespace": the prefix is fine when descriptive (this is the
component's STATUS, not its name or version), and the
reply-variant-naming discipline names the *outcome* — the daemon
reports the engine's status. So the stutter reads as redundant
ceremony rather than restating the noun. Two cleaner shapes:

- Rename variants: `EngineReply::Status(EngineStatus)` and
  `ComponentReport(ComponentStatus)`. Loses the verb-past-tense
  consistency.
- Rename payloads: `EngineSnapshot` / `ComponentSnapshot` — names
  what the data IS, not what variant it lives in. Then variants
  stay `EngineStatus(EngineSnapshot)`. Reads less stuttery.

Designer call. Status quo is acceptable; pointing it out so the
designer can sign off.

### C — The `kind()` projection is solid

`emit.rs` lines 302-380 emits `EngineOperationKind`,
`EngineReplyKind`, and `kind()` methods consistently. The
migration tests
(`engine_manager.rs::engine_operation_kind_is_auto_generated_by_macro`)
witness this. **No hole here**, but worth noting as the macro
feature that genuinely earned its place.

## 6 · Recommendations

In priority order:

1. **Fix Finding 1** in `signal-frame/macros/src/validate.rs`:
   delete `validate_record_head_uniqueness` and the
   `flag_duplicate_record_heads` / `projected_record_head` helpers.
   Add a `tests/channel_macro.rs` case asserting that
   `operation Start(ComponentName), operation Stop(ComponentName)`
   compiles and round-trips correctly.
2. **Land /140's refined bundle for /244 holes 1+2+4** (typed
   rejection via `AcceptedOutcome::Aborted` + per-op `Failed.detail`;
   tighter `observable { open/close }` grammar; `filter default;`
   keyword) BEFORE cascading. Treat /244 hole 3 as gated on the
   /140 §"Hole 3" projection-boundary design pass; do not implement
   /245's literal "move `ObserverChannel` to signal-frame" until
   that pass settles.
3. **Cascade Finding 2** in signal-persona: remove six one-field
   wrapper structs, collapse their payloads to bare types in the
   reply enum. Wire form shortens; consumers simplify.
4. **Cascade Finding 3** in signal-persona: replace the two
   `Query`-enum hand-rolled codecs with `#[derive(NotaSum)]`.
   Leave `SupervisionUnimplementedReason` hand-rolled until
   `nota-derive` gains mixed-variant support.
5. **File Finding 3's `nota-derive` gap** (mixed unit +
   data-carrying support) as its own designer item. Cleans up
   the remaining hand-rolled codec and unlocks Finding 4's
   cleaner shape.
6. **Cascade Finding 4 (after #5)**: collapse `EngineCatalogScope`
   and `EngineStatusScope` to unit variants on the `Query` enum.
   Wire form: `(Query Catalog)` / `(Query EngineStatus)` instead
   of `(Query (Catalog AllEngines))` / `(Query (EngineStatus
   WholeEngine))`.
7. **Verify §5A** in `signal-persona/ARCHITECTURE.md`. Gap-fill
   the five-point relation analysis if missing.
8. **§5B** — designer call on the variant-name/payload-type
   stutter; status quo is acceptable.

The bundle of #1, #3, #4, #6 is a single PR against
signal-persona's contract crate; #2 is the upstream gating work;
#5 is parallel work in nota-derive; #7 is a one-paragraph ARCH
edit.

## 7 · See also

- `reports/second-operator-assistant/6-signal-persona-contract-local-verbs-migration.md`
  — the migration this report re-analyses.
- `reports/designer/244-hole-finding-after-243-implementations.md`
  — the five holes /244 found in the `signal-frame` `observable`
  block and `signal-executor` design.
- `reports/designer/245-design-alternatives-for-244-holes.md`
  — different-approach moves for /244's holes.
- `reports/operator/140-signal-frame-executor-hole-analysis.md`
  — operator's response to /244 + /245; sharpens /245's hole 1
  (Reply::Accepted + Aborted + per-op Failed.detail), hole 2
  (tighter open/close grammar), hole 4 (filter default keyword);
  flags /245 hole 3 as needing another design pass on the
  projection boundary. **This report's §3 sequencing follows
  /140's shape.**
- `reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
  — the contract-local-verb redirection signal-persona migrates onto.
- `reports/designer/241-signal-architecture-migration-guide.md`
  — the MUST IMPLEMENT spec /6 implemented.
- `/git/github.com/LiGoldragon/signal-frame/macros/src/validate.rs`
  lines 143-201 — the offending validation in Finding 1.
- `/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs`
  lines 546-571 — the actual codec emission contradicting that
  validation.
- `/git/github.com/LiGoldragon/nota-derive/src/nota_sum.rs`
  — the derive whose coverage was undersold in report 6 §2.
- `/git/github.com/LiGoldragon/signal-persona/src/lib.rs`
  (commit `0b8adc28` on `main`) — the migrated contract with the
  scar tissue Findings 2-4 describe.
