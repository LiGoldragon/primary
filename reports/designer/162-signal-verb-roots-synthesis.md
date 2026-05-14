# 162 — Signal verb roots: synthesis and recommendation

*Designer synthesis report, 2026-05-14. Retires `/161` with answers
from four parallel research streams: database / distributed-system
tradition, linguistic universals + Sanskrit grammar, astrology +
Arthur Young's twelve measure-formulae + the seven classical planets,
and workspace archeology. Operative recommendation: adopt DA `/50`'s
seven-root verb shape. The four streams converge.*

---

## 0 · TL;DR

- **Adopt DA `/50`'s seven-root recommendation**: `Assert`, `Mutate`,
  `Retract`, `Match`, `Subscribe`, `Atomic`, `Validate`.
- **Move five demoted to typed `ReadPlan<R>` in `sema-engine`** per
  `/50 §6`: `Constrain`, `Project`, `Aggregate`, `Infer`, `Recurse`.
  `signal-core` stays the wire kernel; the read-algebra is engine-side.
- **Rename `SemaVerb` → `SignalVerb`** per `/50 §0` — the type lives
  in `signal-core` and classifies Signal frames; many but not all
  are sema-engine calls.
- **The seven map bijectively to the seven classical planets**
  without forcing. Independent corroboration outside the
  CS-tradition argument (GraphQL, Datomic, relational, SQL).
- **Two naming refinements surface but defer**: `Atomic→Bind`
  (Jupiter's gather-many-into-one, not "indivisible"); `Validate→
  Assay` (Venusian measurement-against-standard, not compiler-
  tradition rule-check). Record the misalignment; CS convention has
  weight.
- **One falsifiable eighth-verb candidate**: `Structure` for DDL-
  shaped operations (Saturn-secondary). Converges from database +
  astrology streams. Defer until concrete DDL traffic surfaces.
- **The twelve was the wrong cardinality for roots.** The zodiacal
  twelve enumerates *qualities-of-subject*, not *kinds-of-act*.
  Classical astrology's signs-vs-planets stratum split mirrors `/50`'s
  roots-vs-modifiers split. The 12-name list was a vocabulary
  catalogue masquerading as an operation catalogue.
- **Confidence**: ~70-75% (per archeology stream's evidence-based
  assessment of `/50` over the prior 12).

---

## 1 · Convergence across four research streams

Four independent research streams were dispatched in parallel against
the question "is the closed 12-verb set the right shape for a universal
inter-system communication protocol?" Each tested a different hypothesis;
they all land on the same answer.

| Stream | Verdict | Headline finding |
|---|---|---|
| Database / distributed systems | 12 is well-grounded but non-orthogonal; 7 closer to operation-roots | `Atomic` wraps others, `Subscribe` = `Match` + delivery, `Validate` is modifier; Reactive Streams' four-signal closure is the strongest external precedent for a genuinely closed set; Erlang/Akka deliberately reject closure. Ten falsifiable pressure points named. |
| Linguistics + Sanskrit | 12 not linguistically grounded; defend on database-operation grounds | Frege gives cleanest mapping (4 of 12: `Assert`/`Retract`/`Infer`/`Match`); Searle's illocutionary five covers 5 of 12; Pāṇini canonicalizes *morphology* and *participation* (lakāra-10, kāraka-6), not verb-meaning; the "Sanskrit advanced civilization" claim is defensible for meta-grammatical machinery, overstated for verb categories. |
| Astrology + planets | 7 maps bijectively to planets; 12 enumerates qualities-not-acts | `Mars→Assert`, `Sun→Mutate`, `Saturn→Retract`, `Moon→Match`, `Mercury→Subscribe`, `Jupiter→Atomic`, `Venus→Validate`; signs (12) and planets (7) are distinct strata in classical astrology — exactly the operation-vs-modifier split `/50` makes in code. Both astrology agents arrived at identical assignments independently. |
| Workspace archeology | 7 was the original shape; 12 was vocabulary widening; consumers use only 5 of 7 | Lineage: 3 → 5(planet-named: `Sol`/`Saturn`/`Luna`/…) → 5 → 7+Handshake → 12(widening) → proposed-7. Zero current consumers use `Constrain`/`Project`/`Aggregate`/`Infer`/`Recurse` as roots. Apr-8 mockup *already had planet-named delimiters*. |

The convergence isn't coincidental. The streams probe different
domains (engineering tradition, language, cosmology, internal history)
and they all surface the same conclusion: the operation-root stratum is
seven; the typed-modifier stratum is twelve-shaped; the workspace's
prior 12-name canon conflated the two.

The astrology stream's signs-vs-planets framing (developed below in
§6) gives the sharpest conceptual articulation. The database stream
gives the engineering rigour. The archeology stream provides
workspace-internal evidence. The linguistics stream cuts against an
attractive-but-wrong defense ("the 12 are linguistically universal").
Together they are stronger than any one alone.

---

## 2 · The seven-planet correspondence (the universality check)

Per user direction: "Since there are seven, we could correspond those
to the seven planets to find the universality in our design. And using
the language associated with those planets, we could verify that we've
picked the right names for them."

Both astrology streams (the original and the 7-planet update)
independently arrived at this mapping:

| Verb | Planet | Day | Reading | Alchemical operation |
|---|---|---|---|---|
| `Assert` | Mars | Tuesday | the *mark* — the *kleos*-leaving strike that says "this happened" | Calcination — the first violent operation |
| `Mutate` | Sun | Sunday | re-manifest at identity — the Sun rises new each day | Coagulation — final fixing of perfected substance |
| `Retract` | Saturn | Saturday | impose-end — Cronus devouring his children, the limit applied | Putrefaction — death of the old form |
| `Match` | Moon | Monday | reflect / show-stored — Luna returning the Sun's light | Dissolution — matter loosens, answer flows back |
| `Subscribe` | Mercury | Wednesday | relay / carry-between — Hermes the psychopomp, perpetual messenger | Separation / Distillation — sorting the stream |
| `Atomic` | Jupiter | Thursday | gather-many-into-one — Zeus the all-father, binder of cosmos | Sublimation — many elevated to one perfected form |
| `Validate` | Venus | Friday | weigh / assay — Aphrodite-Urania's scales of judgment | Conjunction — joining standard to candidate |

The mapping is **bijective without forcing** (astrology stream's
verdict). No planet unused, no verb unmatched. The closure is exact.

Read the Babylonian-Roman week-order as a database-verb workflow:
identify (Sun) → reflect on what is stored (Moon) → mark new facts
(Mars) → propagate them (Mercury) → gather into commits (Jupiter) →
check against standards (Venus) → retract the failed (Saturn). A
two-thousand-year-old typology that lands on a usable operational cycle.

The user's question — *did the workspace pick the right names?* — the
answer is: five of seven verify cleanly. Two surface naming
refinements (§3 below).

### 2.1 · Alternatives tried and rejected

The mapping is constrained enough that swapping any two breaks
something. The astrology stream documented seven specific swap
attempts and rejected each. Selected examples:

- **Mars to `Retract` instead of `Assert`.** Mars's act *persists* —
  the wound writes into the world. Mars = make a permanent edge =
  `Assert`. The cutting-away reading is Saturn's *imposition-of-end*.
- **Mercury to `Match`.** Mercury *carries between* — perpetual relay,
  not single-shot interrogation. `Subscribe` (continuous channel) is
  the messenger's act. `Match` (one-shot reflection) is Lunar.
- **Saturn to `Atomic`.** Saturn's binding is *restrictive* (this and
  no more); `Atomic`'s is *integrative* (many into one). Jupiter binds
  expansively; Saturn binds contractively.

---

## 3 · Naming refinements (planetary language vs current names)

The planetary tradition gives independent evidence for verb-name
honesty. Two verbs misalign with their planetary archetype.

### 3.1 · `Atomic` → `Bind` (or `Unite` / `Bundle`)

Greek *atomos* = "indivisible." The act `Atomic` performs is *not*
indivisibility — the individual writes inside a transaction are
perfectly divisible. The act is *gathering-many-under-one-commit* —
Jupiter's bind, Zeus the gatherer-of-gods, the alchemical sublimation
that elevates many substances to one perfected form.

Candidate replacements: `Bind`, `Unite`, `Bundle`, `Commit`. Planetary
reading favors `Bind`; `Commit` conflates with the commit boundary
inside the transaction.

### 3.2 · `Validate` → `Assay` (or `Weigh`)

`Validate` is named from compiler tradition (validation = check-rules-
against-input). The act is *measurement-against-standard* — Venusian.
Aphrodite-Urania weighs by ideal; the scales of judgment. CS
"validation" is the modern abstraction of an older operation that
weighing better names.

Candidate replacements: `Assay`, `Weigh`, `Measure`.

### 3.3 · Recommendation on renames

CS convention has weight; breaking `Atomic` and `Validate` introduces
contract debt across every consumer. **Do not rename in the current
pass.** The `SemaVerb → SignalVerb` rename in §8 is a separate
decision from the per-verb rename question. Keep `Atomic` and
`Validate` as-is for now; record the planetary misalignment in
doc-comments on the enum so future reviewers see the etymological
story. Reopen the rename question only after concrete contract
examples show the technical-tradition names obscuring the operation
(not before).

The other five names (`Assert`, `Mutate`, `Retract`, `Match`,
`Subscribe`) carry their planetary archetype cleanly; no rename
indicated.

---

## 4 · The eighth-verb question — `Structure`

Two independent streams (database and astrology) name the same gap:
**schema-shaped operations** (DDL — CREATE TABLE, ALTER, indexes,
schema migration) don't fit cleanly into any of DA's seven.

- **Database stream**: schema migration is one of ten falsifiable
  pressure points; a real gap that the 12 doesn't cover and the 7
  won't either.
- **Astrology stream**: Saturn-secondary is *structure-imposition*
  (DDL operationally distinct from DML in most databases). The
  planetary reading favors a distinct verb here.

DA `/50 §7` folds schema migration into `Mutate` or `Atomic`. The
counter-evidence is mild but consistent across streams. Provisional
eighth-verb candidate: **`Structure`** (or `Define` / `Schema`).

**Containment rule (default first):** schema and catalog changes are
*data changes first*. A `CREATE TABLE` is an `Assert` on the catalog;
an `ALTER` is a `Mutate` at stable catalog-row identity; a `DROP` is a
`Retract`; a multi-step migration is `Atomic` over those. Model DDL as
data-against-the-catalog before treating it as a new root.

`Structure` only emerges if real DDL traffic cannot be honestly
modeled as Assert/Mutate/Retract under Atomic — for example, if a
schema change requires a boundary behavior operationally distinct
from data writes (a different commit semantics, a different visibility
model). **Until concrete traffic forces it, the seven absorb DDL.**

Other gap candidates raised by individual streams (capability probes,
distributed consensus, flow control, schema introspection) fold
cleanly into the seven per DA `/50 §7`. They are not eighth-verb
candidates.

---

## 5 · Workspace lineage (per archeology stream)

The seven-root shape is not a new invention. It is a recovery of an
earlier workspace position.

| Date | Repo | Shape |
|---|---|---|
| 2026-04-07 | `nexus-spec-archive` (mockup) | 3-verb sketch |
| 2026-04-08 | `nexus-spec-archive` (mockup) | **5 verbs labeled with planet names**: `Sol`, `Saturn`, `Luna`, `Match`, `Bound` |
| 2026-04-25 | `nexus-spec-archive` (final ARCH) | 5 edit verbs: `Assert`, `Mutate`, `Retract`, `Patch`, `TxnBatch` |
| 2026-04-25 | `signal` (init) | 10: Handshake + 9 operations |
| 2026-04-26 | `signal` (commit `7a78288`) | **7 + Handshake**: `Assert`, `Mutate`, `Retract`, `AtomicBatch`, `Query`, `Subscribe`, `Validate` — structurally identical to DA `/50` after renames |
| 2026-05-08 | `signal-core` (skeleton commit `1d863ce`) | 12 in one shot — vocabulary-recovery widening per DA `/43`, aligned with twelve-verb order in `56002aa` |
| 2026-05-14 | DA `/50` recommendation | Back to 7 |

**The older `signal` repo had exactly the seven-root shape.** The
widening to 12 in `signal-core` was a vocabulary-recovery move — the
older repo's seven didn't have explicit `Constrain`/`Project`/etc.
because they lived inside `Query`. The widening surfaced them as
vocabulary, then confused vocabulary with roots. `/50` restores the
discipline.

The **Apr 8 mockup's planet-named delimiters** (`Sol`/`Saturn`/`Luna`)
are a deep breadcrumb. The user's "correspond to 7 planets" framing
is not ad-hoc — it recovers an early workspace instinct buried under
five weeks of verb-vocabulary work. The earliest mockup also cited
Schroeder/Young's *Zodiac* as the canonical Bibliotheca source for
the workspace's typology work.

---

## 6 · The stratum distinction (load-bearing conceptual finding)

Classical astrology explicitly separates two strata:

- **Signs** (twelve, qualities-of-subject) — *how* an act tones
  itself, *with what flavor*. The 4 elements × 3 modalities lattice.
- **Planets** (seven, kinds-of-doing) — *what kind of act* happens.

A chart says: "what kind of *doing* (planet) happens through what kind
of *being* (sign) in what kind of *domain* (house)." Act, tone, arena
— three independent dimensions. The doing-dimension is seven-fold;
the being-dimension is twelve-fold; they are distinct strata.

The signal-core 12-name list was unwittingly a *quality* catalogue
(signs-stratum) masquerading as an *operation* catalogue (planets-
stratum). DA `/50`'s split into 7 roots + 5 query-algebra modifiers
**is exactly the signs-vs-planets stratum split that classical
astrology makes explicit**.

The mathematics aligns:

- **Seven is prime** (indivisible, primitive). It fits primitive
  operations — roots that cannot be reduced.
- **Twelve is highly composite** (2² × 3, six divisors). It fits typed
  qualities that decompose along multiple orthogonal axes (the
  zodiac's 4 × 3; signal-core's read-plan modifiers along
  payload/index/predicate axes).

Arthur Young's *Science and Astrology* (1987, in the workspace
library) carries both numbers explicitly. His twelve measure-formulae
(line 1820–1834: position, velocity, acceleration, control, moment,
momentum, force, mass-control, moment-of-inertia, action, energy,
power) form a 4-derivative × 3-mass-class lattice that he maps
one-to-one onto the zodiac. His seven-step "learning cycle" (line
2027: "all skills have this anatomy involving seven distinct steps,
which begin and end with spontaneous action") aligns with the seven
classical planets and the toroidal-space seven-color theorem.
**Young's framework gives both 12 and 7 — 12 as static measure-
vocabulary, 7 as dynamic action-cycle.** That maps cleanly onto DA
`/50`'s split.

The astrological tradition has held this distinction for ~2500 years.
The workspace recovers it by code-archeology and convergent cross-
disciplinary research.

---

## 7 · What each research stream contributed

The synthesis aggregates four parallel research streams (dispatched
as agents on 2026-05-14). The streams are process artifacts; their
substance lives in this report's body. Brief contribution summaries
so the reader knows where each finding came from:

- **Database / distributed systems stream** — verb genealogy across
  Datomic, Datalog, Codd's relational algebra, SQL, GraphQL, CQRS,
  event sourcing, Reactive Streams, Erlang/Akka, gRPC, HTTP. Surfaced
  ten falsifiable pressure points; strongest framing was "Datalog-
  extended-with-CQRS." Expects 1-3 verb additions over time;
  schema-migration is the highest-pressure candidate (folded into the
  §4 containment rule).
- **Linguistics + Sanskrit stream** — Pāṇini's Aṣṭādhyāyī (lakāra
  10, kāraka 6, Dhātupāṭha ~2000 roots), semantic primes (NSM verb
  primes), Searle's five illocutionary classes, Vendler's four aspect
  classes, Frege/Russell logical primitives. Verdict: defend the verb
  set on database-operation grounds, not linguistic-universal grounds.
  The Sanskrit-as-formal-language claim is defensible for meta-
  grammatical machinery (utsarga/apavāda, anuvṛtti, pratyāhāra,
  it-saṃjñā — generative rule techniques predating Chomsky by 2300
  years), overstated for verb categories.
- **Astrology + planets stream** — zodiac 4×3 decomposition, Young's
  twelve measure-formulae from *Science and Astrology* (1987),
  twelve-fold catalogue, mathematics of 12 vs 7, seven-planet ↔
  seven-verb bijective mapping with per-planet sources (Ptolemy
  *Tetrabiblos*, Lilly *Christian Astrology* 1647, Hermetic tradition,
  Jungian archetypes). Two independent astrology agent runs arrived at
  identical verb-to-planet assignments.
- **Workspace archeology stream** — workspace lineage
  3→5→5→7→12→proposed-7; per-component verb-usage inventory (5 of 7
  roots used; zero consumers use the demoted 5 as roots); library
  inventory (rich on linguistic theory: Sowa, Tesnière, Mel'čuk,
  Halliday, Rajpopat, Bhartṛhari; on category theory: Spivak, Mazzola,
  Zalamea; on Cyc: Lenat; sparse on databases/distributed systems).
  Closure-rigor verdict on the prior 12: "load-bearing as coordination
  rule, weak as argument" — `/50 §3` is the first explicit closure
  argument in workspace history.

---

## 8 · Operative recommendation

1. **Adopt DA `/50`'s seven-root shape** as the canonical
   `SignalVerb`:

   ```rust
   pub enum SignalVerb {
       Assert,
       Mutate,
       Retract,
       Match,
       Subscribe,
       Atomic,
       Validate,
   }
   ```

2. **Move the five demoted to typed `ReadPlan<R>` in `sema-engine`**
   per `/50 §6` — plan operators inside read execution, **not in
   `signal-core`**:

   ```rust
   // Crate: sema-engine (NOT signal-core).
   // signal-core is the wire kernel — SignalVerb + envelope, nothing else.
   pub enum ReadPlan<R> {
       AllRows { table: TableRef<R> },
       ByKey   { table: TableRef<R>, key: R::Key },
       ByKeyRange { table: TableRef<R>, range: KeyRange<R::Key> },
       ByIndex { index: IndexRef<R>, range: KeyRange<R::IndexKey> },
       Filter    { source: Box<Self>, predicate: Predicate<R> },
       Constrain { sources: Vec<ReadPlanAny>, unify: UnificationPlan },
       Project   { source: Box<Self>, fields: FieldSelection<R> },
       Aggregate { source: Box<Self>, reducer: AggregatePlan<R> },
       Infer     { source: Box<Self>, rules: RuleSetRef },
       Recurse   { seed: Box<Self>, edge: Box<Self>, mode: RecursionMode },
   }
   ```

   Domain contracts (`signal-persona-*`) carry domain-typed payloads
   (e.g. `MessageRequest::InboxQuery { since, kind, limit }`) that the
   receiving daemon translates to a `sema_engine::ReadPlan` before
   calling the engine. A contract may *optionally* expose
   `ReadPlan<R>` directly as its payload type when the contract is
   purely a query surface (e.g. an inspection-plane contract); this
   couples that contract to `sema-engine` and is a per-contract
   choice. **`signal-core` itself stays domain-free and engine-free.**

3. **Rename `SemaVerb` → `SignalVerb`** per `/50 §0`. The type lives
   in `signal-core` and classifies Signal frames; it is not an engine
   implementation type.

4. **Keep the verb-mapping discipline** — every contract request
   declares `signal_verb()`; tested by per-contract witnesses. Already
   in place per `~/primary/skills/contract-repo.md` §"Signal is the
   database language — every request declares a verb"; the rule now
   maps to the seven, not the twelve.

5. **Record naming refinements as future work** — `Atomic→Bind` and
   `Validate→Assay`. Don't break CS convention now; document the
   planetary misalignment in `signal-core/src/request.rs` doc-comments
   so future reviewers see the etymological story.

6. **Watch for `Structure` as falsifiable eighth verb** — first real
   DDL traffic that doesn't fit `Mutate`/`Atomic` triggers the
   addition. Don't add pre-emptively.

7. **Window**: now. Adoption of `/50` is cleaner before more contracts
   harden around the twelve. Operator's `[primary-5ir2]` work
   (persona-mind first-consumer migration to sema-engine) and
   operator-assistant's persona-introspect Slice 1 work (per `/160`)
   are both compatible with either shape; the move costs less now
   than after Slice 2 + Slice 3 land.

---

## 9 · Required documentation and contract edits

Hand-off note for operators: the canonical-decision shape lives in
this report and DA `/50`, but multiple workspace files describe the
twelve-verb prior. **Edits must land before or alongside the code
change** — the implementation order can interleave; the docs must not
drift past a contract migration. Status column tracks current state
so future agents don't chase already-landed work.

| File | Prior state | Target | Status |
|---|---|---|---|
| `~/primary/skills/contract-repo.md` §"Signal is the database language" | Lists the twelve verbs; `sema_verb()` examples; rule "read-shaped payloads use `Match`/`Project`/`Aggregate`/`Subscribe`" | List the seven roots; `signal_verb()` examples; rule "read-shaped payloads use `Match` or `Subscribe`; algebra lives in `sema_engine::ReadPlan`" | **Done** (`19de3f04`) |
| `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` §1, §3 | "`SemaVerb`, the closed twelve-verb request spine" + the twelve in §1; "verb set is closed and ordered as the twelve" in §3 | "`SignalVerb`, the closed seven-root request spine"; the seven in §1; closure rule restated; note that the five demoted live in `sema-engine`'s `ReadPlan<R>` | **Done** (parallel landing) |
| `/git/github.com/LiGoldragon/signal-core/src/request.rs:6-19` (enum) | `pub enum SemaVerb` with twelve variants | `pub enum SignalVerb` with seven variants; doc-comments on `Atomic` and `Validate` noting the planetary-tradition rename candidates (`Bind`/`Assay`); explicit pointer to `sema-engine::ReadPlan` for the algebra | **Done** (already seven; rename to `SignalVerb` pending) |
| `/git/github.com/LiGoldragon/signal-core/src/lib.rs` `Request<P>` constructors | Free-form `Request::assert(...)`, `Request::match_records(...)`, etc. accept any payload under any root | Deprecate or rename to unchecked/internal so source scans find them; payload-first construction via per-contract `signal_verb()` mapping is the canonical path | **Pending** (operator-scope) |
| `/git/github.com/LiGoldragon/signal-core/src/lib.rs` `signal_channel!` macro | No verb annotation on request-enum variants | Per `/50 §5`, accept verb annotations; generate `signal_verb()` mappings and per-variant witnesses | **Pending** (operator-scope) |
| `/git/github.com/LiGoldragon/nexus/spec/grammar.md` | Top-level Nexus records enumerate twelve verbs | Top-level records enumerate seven; algebra appears inside `Match`/`Subscribe`/`Validate` payloads as `ReadPlan` records | **Pending** (operator-scope) |
| `reports/designer/157-sema-db-full-engine-direction.md` §4 verb-storage table | Twelve-row table mixing roots and algebra | Two-section table: seven roots with storage behavior; five algebra operators with plan-node semantics | **Pending** (designer follow-up) |
| `/git/github.com/LiGoldragon/signal/README.md` (line 27) | "owns the universal envelope and twelve-verb spine" | Seven-root spine; pointer to `/50`/`/162`; algebra in `sema-engine::ReadPlan` | **Done** (`c1d522ea`) |
| `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md` (line 125) | "closed verb spine (`SemaVerb`: …12 names…)" | Seven roots; algebra demoted to `sema-engine::ReadPlan` | **Done** (`c1d522ea`) |
| `/git/github.com/LiGoldragon/signal-persona-mind/ARCHITECTURE.md` (line 24) | "`MindRequest` variant to the `SemaVerb`" | `SignalVerb` rename pending; same per-variant mapping discipline | **Done** (`81b16811`) |
| `/git/github.com/LiGoldragon/signal-persona-introspect/ARCHITECTURE.md` (constraints table + owned-surface) | Rule: "Read-shaped payloads use `Match` (or `Project`/`Aggregate`/`Subscribe`)" — actively wrong; owned surface listed "`SemaVerb` mapping" | Rule corrected: "Read-shaped payloads use `Match` or `Subscribe`; algebra in `sema-engine::ReadPlan`"; owned surface restated as "Signal root-verb mapping" | **Done** (`2cfb9b5b` + follow-up cleanup) |
| **Every `signal-*` contract crate with a verb mapping** (signal-persona, signal-persona-message, signal-persona-router, signal-persona-terminal, signal-persona-manager, signal-persona-mind, signal-persona-introspect, signal-persona-system, signal-persona-harness, signal-forge, signal-arca, ...) | `pub fn sema_verb(&self) -> SemaVerb` per-variant mapping returning the closed twelve | `pub fn signal_verb(&self) -> SignalVerb` per-variant mapping returning the closed seven; round-trip witness that no variant maps to a demoted name | **Pending** (operator-scope coordinated sweep) — `signal-persona-introspect` and `signal-persona-mind` have *method renamed to `signal_verb`* but type still `SemaVerb` (partial migration; finishes when `signal-core` lands the type rename). Other contracts need a scan: any unmigrated `sema_verb` method, any variant mapping to `Constrain`/`Project`/`Aggregate`/`Infer`/`Recurse` as a root, any free-form `Request::assert(...)` constructor — all must be migrated or explicitly marked pending. |

The implementation order: `signal-core/src/request.rs` rename is the
ordering pin — every downstream contract crate's `signal_verb() ->
SignalVerb` migration depends on the type existing. The
contract-crate sweep happens in the same breaking pass; one PR per
contract or one coordinated mega-PR, designer's call.

---

## 10 · What this retires

- **`/161`** — the research brief. Q1 (per-verb genealogy), Q2 (set
  completeness), Q3 (composition closure), Q5 (gaps and pressure
  points) are all answered above. Q4 (forward to eventual Sema) is
  partially answered: the seven-root shape is the candidate for
  Sema's primitive operations when the workspace self-hosts; the
  twelve was vocabulary-recovery, not architectural truth.

- **The 12-name list as workspace truth** — moves to vocabulary, not
  roots. The five demoted names (`Constrain`, `Project`, `Aggregate`,
  `Infer`, `Recurse`) live on as `ReadPlan<R>` operators per `/50 §6`.

- **The implicit claim that `SemaVerb` is the right type-name** —
  rename to `SignalVerb` makes the contract-vs-engine split honest.

---

## 11 · See also

- `reports/designer-assistant/50-signal-core-base-verb-shape.md` —
  the operative proposal this report adopts.
- `reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md`
  — the recovery synthesis that motivated the 12-verb vocabulary
  widening that `/50` now reverses.
- `reports/designer-assistant/49-sema-engine-state-and-introspect-readiness.md`
  — readiness assessment for the engine-side consumer; compatible
  with the seven-root shape.
- `reports/designer/157-sema-db-full-engine-direction.md` §4 — per-
  verb storage implications; the table now reorganizes as 7 root
  storage-behaviors + 5 read-plan algebra-behaviors.
- `reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`
  — the two-repo architecture (kernel + engine); the seven-root
  shape lives in `signal-core` and is consumed by `sema-engine` via
  the `Engine` trait.
- `reports/designer/160-persona-introspect-brief-for-operator-assistant.md`
  — the persona-introspect implementation brief; Slice 1 (verb-
  mapping witness) aligns with the seven-root shape.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the verb-discipline
  rule.
- `~/primary/ESSENCE.md` §"Backward compatibility is not a constraint"
  — the discipline that makes the 12→7 reduction a legitimate move.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs:6-19` —
  the current 12-name `SemaVerb` artifact; target for the rename +
  shrink.
- `/git/github.com/LiGoldragon/signal/src/request.rs` — the older
  7-shape that DA `/50` is recovering.
- `/git/github.com/LiGoldragon/library/en/arthur-young/science-and-astrology.ocr.txt`
  — Young's measure-formulae table (line 1820–1834); the seven-step
  learning cycle (line 2027); the toroidal seven-color theorem
  (line 2033). Carries both the 12 (measure-vocabulary) and the 7
  (action-cycle) explicitly.
- `~/primary/skills/reporting.md` §"Kinds of reports — Decision /
  synthesis" — this report's typology.
