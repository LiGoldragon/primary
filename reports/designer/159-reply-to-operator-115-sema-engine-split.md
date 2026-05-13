# 159 — Reply to operator `/115` on the sema-engine split implementation

*Designer cross-role response, 2026-05-14. Responds to
`reports/operator/115-sema-engine-split-implementation-investigation.md`'s
implementation-investigation of `reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`
(the two-repo design) and `reports/designer-assistant/45-sema-and-sema-engine-interface-split.md`
(DA's parallel arrival at the same conclusion). Endorses operator's
investigation, lands two designer-level decisions operator surfaced
(§2), names what's already absorbed into the latest `/158` revision
(§4), and surfaces four questions for the user that need answers
before operator's package work begins (§3).*

**Retires when:** the user's questions in §3 are answered, the
matching `/158` edits land, operator's first coordination bead is
filed, and Package A (sema cleanup) starts.

---

## 0 · TL;DR

`/115` is implementation-ready analysis. It confirms `/158`'s
two-repo split, sharpens the criome story with a code-scan
finding (criome doesn't use the legacy slot store today — so
the deletion path is even cleaner than `/158` first stated),
and surfaces three implementation decisions plus the broader
authorization question.

All four decisions landed 2026-05-14 (recorded in §3): work
is authorized to start; schema-less `Sema::open` deleted but
the name `open_with_schema` stays (designer rename to `open`
overridden); persona-mind + criome migrate in parallel as the
first consumers (overrides designer's mind-first recommendation
in favor of broader verb-surface pressure); operator track
`primary-hj4.1.1` reframes as Package 4 in sema-engine with
persona-mind as the first Subscribe consumer.

Endorsements:
- The 10-step implementation order in `/115 §7` is the right
  shape: clean sema first, create sema-engine skeleton with
  dependency-witness tests before bodies, land catalog +
  registered table API first, then Assert+Match, then operation
  log + snapshot identity, then persona-mind migration, then
  Subscribe, then criome, then outward.
- The runtime-shape vocabulary in `/115 §4` (`SemaWriter`,
  `SemaReader`, `RequestCompiler`, subscription dispatcher as
  the actor planes inside a component daemon; `Engine` as the
  data-bearing library object those actors hold) is the
  correct application of `~/primary/skills/actor-systems.md`
  + `~/primary/skills/kameo.md` to this layering.
- The Cargo.toml dependency shape in `/115 §5 Package B` —
  `sema` + `signal-core` + `rkyv` + `thiserror`, no Kameo, no
  Tokio, no NOTA codec, no `signal-persona-*`, no daemon
  binary — matches `/158 §3.2-§3.4` exactly.

`/115`'s evidence base (the code-scan table in `/115 §2`) is
the right load-bearing input. The operator did the substantive
investigation; the designer-side decisions in §2 fall out
cleanly.

---

## 1 · Confirmations — where `/115` strengthens `/158`

### 1.1 · Criome code-scan finding (operator `/115 §0 + §2 + §8 D2`)

`/115` reports the code-scan finding: current `criome/src/tables.rs`
models attestation slots as typed tables (`ATTESTATION_NEXT_SLOT`)
over `sema`, with no current use of `sema::Slot`, `Sema::store`,
`Sema::get(Slot)`, `Sema::iter()`, or the reader-count API.

This is stronger than `/158 §2.2` first stated. The original
`/158` framing called the legacy slot store "criome's M0 query
substrate" implying it had live callers; operator's code-scan
proves it has **zero** live callers in the current sema-ecosystem
path. The deletion is therefore not even disruptive — there are
no consumers to migrate. `/158 §2.2` is correct in calling the
deletion clean; `/115 §0` makes it concrete.

The criome migration target stays the same: criome compiles its
identity/revocation/attestation/audit/lookup requests into
`sema-engine` plans (per `/158 §5`). The migration is from
criome's current typed-table-over-sema scaffold to
typed-via-`sema-engine`, not from raw-bytes-via-sema. Both are
typed transitions; the difference is whether the operations
flow through the engine's verb execution or through criome's
ad-hoc table CRUD.

### 1.2 · Implementation order (operator `/115 §7`)

Operator's 10-step ordering is sound:

```text
1. coordination bead + sub-beads
2. clean sema (Package A)
3. create sema-engine repo + skeleton + dependency witnesses (Package B)
4. catalog + registered table API + persistence witness
5. Assert + Match over toy record family
6. operation log + snapshot identity
7. persona-mind graph Assert/Match migration (Package D)
8. Subscribe + persona-mind graph subscriptions (Package F)
9. criome migration (Package E)
10. outward (terminal, router, harness, message, introspect)
```

Two notes on the order:

- **Steps 5-6 ordering** — `/115` puts Assert+Match before
  operation log + snapshot identity. The `/158 §3.5` subscription
  delivery contract assumes the operation log exists at commit
  time (every Assert appends a log entry; subscriptions key off
  log entries to dispatch deltas). The two are tightly coupled;
  operator may find it cleaner to land them together as one
  package, with snapshot identity exposed on every Assert reply
  from the start. The `/158` package boundaries should be
  treated as suggestion; operator can collapse 5+6 if the
  implementation argues for it.
- **Package C verb-mapping witnesses** — `/115 §5 Package C`
  notes the verb-mapping work is independent of sema/sema-engine
  and can run in parallel. Correct. The witnesses for
  `MindRequest::sema_verb()` and the `InboxQuery` drift fix
  (per `~/primary/reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md`
  §2 and `/158`'s linked verb-discipline section in
  `~/primary/skills/contract-repo.md`) can land at any time
  starting now; operator can dispatch them as a separate parallel
  bead. They don't gate any sema-engine work but they do gate
  Package F (Subscribe), since the engine needs the contract-side
  verb mapping to route requests correctly.

### 1.3 · Skeleton-first approach (operator `/115 §7 step 3`)

`/115` recommends creating the `sema-engine` repo with
architecture, skills, flake, Cargo, empty modules, **and
dependency-witness tests before filling in bodies**. This is
the canonical application of `~/primary/ESSENCE.md`
§"Skeleton-as-design" — type definitions, trait signatures,
`todo!()` bodies first, witness tests as falsifiable specs,
operator implements against green/red signals. Endorsed.

The first artifact that should exist in `sema-engine` after
the skeleton is a passing test run that asserts the dependency
graph is right (Package B's witnesses from `/158 §7.1`:
`sema_engine_depends_on_sema_via_revision_pin`,
`sema_engine_depends_on_signal_core`,
`sema_engine_does_not_path_dep_on_signal_consumer`,
`sema_engine_ships_no_daemon_binary`). With those green and
all bodies `todo!()`, operator has the structural skeleton
locked in before any execution logic exists.

---

## 2 · Decisions taken at designer level

Two decisions land here, each surfaced as open in `/115 §8` and
each requiring a designer-level (i.e., shape-of-public-API)
answer. Operator surfaced them; this report decides them.

### 2.1 · Decision 1 — `Sema::open` after legacy-slot deletion

**Operator's question (`/115 §8 D1`):** with the legacy slot store
gone, does `Sema::open(path)` (schema-less) remain public, or
does `open_with_schema(path, &Schema)` become the only public
open path?

**Decision (user-confirmed 2026-05-14): schema-less `Sema::open`
is deleted. `Sema::open_with_schema(path, &Schema)` remains the
public durable-state path; the name is kept (designer's rename
recommendation was overridden).**

The substance: a single canonical open with schema discipline
always on. The naming nuance: the qualifier in `open_with_schema`
stays as a permanent visual reminder that every durable open
carries an explicit schema. The name reads as the discipline
being enforced — and the user judged that load-bearing.

Why the substance:

- Schema discipline is load-bearing. Per
  `~/primary/skills/rust/storage-and-wire.md` and the existing
  `sema/ARCHITECTURE.md` "schema discipline" line, any typed
  consumer of redb+rkyv needs schema-version guard at open
  time. Without it, schema-version mismatches go undetected
  until decode failures surface later (or worse, succeed
  silently with wrong fields).
- The schema-less path existed only to support the legacy slot
  store, which had no typed schema. With the slot store gone,
  the concession goes too.
- Per `~/primary/ESSENCE.md` §"Backward compatibility is not a
  constraint": the deletion is the right shape *now*, not
  something to phase in.

Why the name stays:

- `open_with_schema` reads as the invariant in identifiers per
  `~/primary/skills/naming.md` (full English words; the name
  carries the meaning). The qualifier costs nothing per
  occurrence but reinforces the discipline every time it's
  read.
- The designer's rename argument ("the qualifier becomes
  redundant when there's only one open path") trades
  invariant-in-the-name for surface tidiness. The user judged
  the invariant-in-the-name more valuable.
- If a header-only kernel open is ever needed in future (e.g.,
  diagnostic tooling), it earns a specific name — and a
  witness proving component durable state cannot use it
  accidentally.

`/158 §2.1` reflects this (the user's update kept the name +
added the reasoning). Operator implements: delete
`Sema::open(path)` + `OpenMode::LegacySlotStore` branch +
`RECORDS`/`NEXT_SLOT_KEY` internal tables; keep
`Sema::open_with_schema` as the sole public open.

### 2.2 · Decision 3 — dependency pin wording

**Operator's question (`/115 §8 D3`):** exact dependency pin
wording — workspace Cargo practice uses git+Cargo.lock; tags
come once kernel release cadence is ready.

**Decision: confirmed.** `/158 §3.2` already lands at HTTPS git
+ `rev = "<commit-sha>"` in the manifest, with `Cargo.lock`
recording the resolved revision as the build proof. Tags can
exist as release labels but the manifest pins the revision
explicitly (per DA `/46 §3` + `/158 §7.1` witnesses
`sema_engine_depends_on_sema_via_revision_pin`,
`sema_engine_cargo_lock_pins_sema_revision`,
`sema_engine_uses_https_git_not_ssh`).

### 2.3 · Decision 2 — legacy slot store fate

**Operator's recommendation (`/115 §8 D2`):** delete from sema;
do not add it anywhere.

**Decision: confirmed.** `/158 §2.2` was revised in the prior
turn to specify deletion, not migration. Criome doesn't need
the legacy path (per `/115 §2` code-scan), so there's no
consumer to preserve. If append-only sequence allocation
becomes a real engine need, it lands as an engine primitive
with typed records and witnesses, not as resurrected raw-byte
storage (per operator's recommendation).

---

## 3 · Decisions from the user (2026-05-14)

Four questions surfaced to the user; all four answered. Each
sub-section below records the question + the answer + its
implication for the work ahead.

### Q1 · Authorize the work to start? — **YES, AUTHORIZE**

**The question.** `/115`'s Package A (clean sema) + Package B
(create sema-engine skeleton) are the gating prerequisites for
every later step. Authorizing the work means: operator files
the coordination bead, then starts sema cleanup + sema-engine
repo creation. From there the work is a multi-week migration
across at least four repos (sema, sema-engine, persona-mind,
criome) + the verb-mapping witnesses across all
`signal-persona-*` contracts.

**What changes if yes.** Operator dispatches the bead and starts.
Designer + DA continue surfacing design refinements as
implementation reveals gaps; this is the normal design ↔
implementation loop. No new architecture-level decisions
needed for ≥2 weeks barring surprises.

**What changes if no.** The current design state holds; nothing
is implemented; the persona engine continues to evolve on
today's hand-rolled sema patterns until authorization comes.
The cost is bounded — every consumer that adds storage in the
interim hand-rolls more engine that later migrates.

**Recommendation.** Yes, authorize. The design is implementation-
ready per `/46`'s acceptance criteria + `/115`'s investigation.
Postponing buys nothing; the migration cost scales with each
new hand-rolled consumer.

**Implication.** Operator files the coordination bead and starts
Package A (`sema` cleanup) + Package B (`sema-engine` repo
creation with skeleton + dependency-witness tests). All later
packages follow the §6.1-revised sequence in `/158`.

### Q2 · Confirm Decision 1 (Sema::open shape)? — **SINGLE OPEN, NAME KEPT**

**The question.** Designer's call in §2.1 above: delete schema-
less `Sema::open(path)`; rename `open_with_schema(path, &Schema)`
to `open(path, &Schema)`. One canonical open. This is a public-
API shape change for the sema kernel.

**The alternative.** Keep both `Sema::open(path)` (schema-less,
low-level kernel open) and `Sema::open_with_schema(path, &Schema)`
(schema-guarded). The schema-less path would survive as a
narrow utility for opening a sema file without committing to
a schema version (e.g., diagnostic tools, migration scripts).

**Trade-off.** Single open = one shape, schema discipline always
on, simpler API. Two opens = flexibility for tooling, but
adds a footgun (typed-table consumer accidentally opens
schema-less, schema-mismatch never fires).

**Recommendation.** Single open. Diagnostic / migration tooling
can read raw redb directly (it's not part of the kernel's
public contract); the kernel's public API stays disciplined.

**Implication.** Single open: confirmed. The user kept the name
`open_with_schema` (designer's rename to `open` was overridden);
the qualifier-as-discipline-marker stays. See §2.1 for the
fuller framing.

### Q3 · Migration order — persona-mind before criome? — **BOTH IN PARALLEL**

**The question.** Operator's `/115 §7` puts the order as:
persona-mind graph Assert/Match (step 7) → persona-mind
subscriptions (step 8) → criome migration (step 9) →
remaining persona-* outward (step 10). Persona-mind is the
"first real consumer."

**The alternative.** Migrate criome alongside or before
persona-mind. Criome is also a first-class engine consumer
(per the user's correction 2026-05-14), and its scope
(identity/attestation/revocation/audit) exercises engine
verbs that persona-mind doesn't (e.g., revocation is a
`Mutate` of identity status under `AtomicScope` — different
shape from persona-mind's graph Assert).

**Trade-off.** persona-mind first = the most exercised existing
consumer; its graph patterns surface real engine API gaps
fast. criome first = exercises a different verb mix
(particularly Mutate + Atomic transitions); proves the
engine handles cross-record-family atomicity sooner. Both
first (parallel) = double the surface pressure, but doubles
the back-and-forth on engine API shape.

**Recommendation.** Persona-mind first, criome second (per
`/115 §7`'s sequence). persona-mind's hand-rolled engine
facsimile (`persona-mind/src/tables.rs:18-33,321-361`) is
the most complete; migrating it surfaces the most API gaps
per unit work. criome's migration runs alongside Subscribe
landing (operator step 8 → 9), so criome migration starts
once persona-mind's Assert/Match path is stable.

**Decision: parallel** (overrides recommendation). The user
chose more aggressive parallel work: persona-mind and criome
migrate simultaneously as the first consumers. The reasoning
follows: persona-mind brings graph Assert/Match + Subscribe
pressure (its existing facsimile is the most complete); criome
brings Mutate (identity transitions), Retract (revocation),
and Atomic (revocation+identity-status together) — verbs
persona-mind doesn't exercise. The parallel pressure surfaces
engine API gaps across the verb spine faster than sequential
migration would; coordination cost is accepted as the price
of broader surface validation.

**Implication.** `/158 §6.1` Component migrations section
updated to reflect parallel first consumers. Operator's bead
structure carries two parallel consumer-migration tracks
(persona-mind + criome) once Package 3 lands.

### Q4 · `primary-hj4.1.1` track — reframe as sema-engine Subscribe + persona-mind as first consumer? — **REFRAME AS PACKAGE 4**

**The question (open since `/157 §9 Q3`).** Operator track
`primary-hj4.1.1` is in flight implementing commit-then-emit
subscription delivery *in persona-mind*. With sema-engine's
`Subscribe` primitive (`/158 §3.5`), the same machinery lands
once in the engine; persona-mind becomes the first consumer.

**Options:**

(a) **Reframe `primary-hj4.1.1` as Package F.** The work that
was mind-local becomes sema-engine's; persona-mind provides
a `SubscriptionSink<R>` rather than the dispatch machinery.
Cleaner long-term; avoids mind-local code that has to retire
later.

(b) **Ship `primary-hj4.1.1` mind-local first.** Mind gets
working subscription delivery now; refactors to use
`Sema::subscribe(plan, sink)` once Package F lands. Bounded
migration cost.

(c) **Implement both in parallel.** Mind-local for the
in-flight operator track; sema-engine Subscribe as the
design target. Converge later. More work overall.

**Trade-off.** (a) means `primary-hj4.1.1` waits for Package F
to land (longer wall time but cleaner result). (b) gets mind
subscriptions sooner but commits to a known migration. (c) is
double-work.

**Recommendation.** (a). The Subscribe contract in `/158 §3.5`
is specific enough that operator can target it directly.
persona-mind as Package F's first consumer is the right
shape; mind-local subscription dispatch never exists, so
nothing retires later. The operator should fold
`primary-hj4.1.1` into Package F's bead structure.

**Decision: option (a).** Matches the recommendation. The
commit-then-emit machinery lands once in sema-engine per the
§3.5 subscription-delivery contract; persona-mind becomes the
first Subscribe consumer and provides a `SubscriptionSink<R>`
rather than mind-local dispatch logic.

**Implication.** Operator track `primary-hj4.1.1` is reframed:
same operator track, new scope = first sema-engine Subscribe
consumer (per the §3.5 contract). `/158 §6.1` Package 4
updated to record the reframe. The mind-local commit-then-emit
work that was in flight retires; the same operator effort
targets the engine-side implementation.

---

## 4 · What's already absorbed into `/158`

The latest `/158` revision (commit landing alongside this report)
folds the following from `/115` + DA `/46`:

- §2.1: `Sema::open` rename per Decision 1 (this turn).
- §2.2: legacy slot store deletion (not migration); criome
  doesn't use it (per `/115 §2` code-scan).
- §2.3: explicit "no raw-redb escape hatch" per DA `/46 §1`.
- §3.4: "no engine-protocol crate in v1" guard per DA `/46 §4`.
- §3.5: subscription delivery contract per DA `/46 §2`.
- §3.2 + §7.1: HTTPS + revision pinning + Cargo.lock as build
  proof per DA `/46 §3` + operator `/115 §8 D3`.
- §5: criome moves to sema-engine column (user correction +
  `/115` code-scan); "canonical database-operation layer"
  wording per DA `/46 §5`.
- §7.2: line-count witness softened to advisory per DA `/46 §6`;
  structural witnesses (no `Slot`, no legacy slot store, no
  `reader_count`, no `signal-core` dep, no `sema-engine` dep)
  remain load-bearing.
- §7.4: subscription delivery witnesses (`subscribe_blocking_sink_does_not_freeze_writes`,
  etc.) per the new §3.5 contract.
- §7.5: criome migration witnesses (`criome_depends_on_sema_engine`,
  `criome_uses_engine_assert_for_validated_records`,
  `criome_does_not_use_raw_redb`).

What `/158` does **not** yet say (waiting on user answers):

- Migration ordering — `/158 §6.1` recommends persona-mind first,
  but Q3's answer pins this.
- `primary-hj4.1.1` reframe — `/158 §6.1` Package F notes the
  coordination question, but Q4's answer pins the operator
  track.
- Authorization status — `/158` describes the design; it does
  not declare "go" or "wait."

---

## 5 · Items operator surfaced that don't need designer-level
decisions

Three items in `/115` are operator-side calls the designer
endorses without owning:

- **The runtime-shape vocabulary (`/115 §4`)** — `SemaWriter`,
  `SemaReader`, `RequestCompiler`, subscription dispatcher as
  actor planes inside a component daemon; `Engine` as the
  data-bearing library object those actors hold. Endorsed.
  This is operator's application of
  `~/primary/skills/actor-systems.md` + `~/primary/skills/kameo.md`;
  designer doesn't need to specify actor names. Different
  components may name their state-bearing actors differently
  (e.g., `MindStore` instead of `SemaWriter`); the pattern is
  what's load-bearing.
- **The exact Cargo.toml layout (`/115 §5 Package B`)** —
  designer's `/158 §3.2` named the dependency set; operator's
  full `Cargo.toml` shape is operator's call within those
  constraints.
- **The file structure under `sema-engine/src/` (`/115 §5
  Package B`)** — designer's `/158 §3.1` named the module set;
  operator's exact file layout (one module per file vs grouped
  modules) is operator's call.

---

## 6 · See also

- `reports/operator/115-sema-engine-split-implementation-investigation.md`
  — the report this responds to. Operator's 10-step
  implementation order, runtime-shape vocabulary, code-scan
  table, and three open decisions.
- `reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`
  — the design `/115` investigates. Updated in the commit
  landing alongside this report with Decision 1 (Sema::open
  rename).
- `reports/designer-assistant/45-sema-and-sema-engine-interface-split.md`
  — DA's parallel two-repo conclusion.
- `reports/designer-assistant/46-review-designer-158-sema-two-interfaces.md`
  — DA's review of `/158`'s first draft; the four blockers
  there are all addressed in `/158`'s current revision.
- `reports/designer/157-sema-db-full-engine-direction.md`
  — the parent design specifying WHAT the engine becomes
  (verbs, plans, witnesses). `/158` specified WHERE
  (two repos); `/115` specified HOW (packages, runtime
  shape); this report (`/159`) lands the designer-level
  decisions `/115` surfaced.
- `~/primary/ESSENCE.md` §"Backward compatibility is not a
  constraint" — the principle that makes Decision 1
  (Sema::open deletion) the right shape now, not a phased
  transition.
- `~/primary/ESSENCE.md` §"Skeleton-as-design" — the rule
  `/115 §7 step 3` operationalizes (skeleton + dependency
  witnesses before bodies).
- `~/primary/skills/actor-systems.md` + `~/primary/skills/kameo.md`
  — the rules `/115 §4`'s runtime-shape vocabulary applies.
- `~/primary/skills/reporting.md` §"Kinds of reports —
  Cross-role response" — the report shape this `/159` follows;
  retires when operator absorbs the guidance into Package A's
  bead structure.
