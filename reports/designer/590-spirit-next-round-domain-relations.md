# Spirit next round — domain model (nested) + equivalence + guardian residue

The implementation spec for the next round, at the **settled** model: `Software` nests under
`Technology` (is-a is structural), cross-domain links are **symmetric equivalence only**
(subsumption dropped), and the vocabulary moves to a first-class **taxonomy schema**. This
report is the contract; operator's report responds. Recap of the reasoning in 591,
build-state in 589. This version supersedes the report's earlier top-level-`Software` /
subsumption drafts and folds in operator's live-guardian progress (363).

## 0. TL;DR

| # | Item | Kind |
|---|---|---|
| 1 | **Re-nest** `Software` from a top-level area to a cluster **under `Technology`** | schema restructure |
| 2 | **Domain scopes** — prefix matching at any depth | foundation |
| 3 | **Equivalence** — the one symmetric relation + query-expansion (no subsumption) | relation mechanism |
| 4 | **Taxonomy schema** — enum + relations in a new first-class schema kind (`schema/domain.schema`), reusable | new schema surface (`mn3k`) |
| 5 | **Overlap resolution** — structural by absorption; residual symmetric synonyms as equivalences | vocabulary |
| 6 | **Guardian residue** — few-shot (seed from 363's live scenarios) + equivalence-expanded retrieval | 585 leftovers |

Dropped/settled: directional **subsumption** (the tree + scopes carry hierarchy); **glosses**
(`2rb7` — names self-explanatory; the live prompt already judges domain-fit via `UnclearDomain`
without them).

## 1. What already landed (and what now changes)

- **Software branch** (`c30bed3`) — built as a **top-level area**. This round **re-nests it
  under `Technology`** (§2). The 12-cluster tree is unchanged; only its root moves.
- **Guardian** — gate over every live-arrow write + separate decision-log journal +
  justified-mutation gating (`5d47de6`, `18cb7f1`); prompt extracted into
  `src/guardian_prompt.rs`, temperature-zero, closed reason-set with definitions,
  nested-reject-form enforcement, **justification-is-evidence-not-a-second-arrow** (`a814a282`,
  good `tfpd` fidelity); and a **live DeepSeek scenario suite** that accepts/rejects correctly
  across Contradiction / Compound / NonIntent (`363`). Faithful; residue in §6.
- **Referent registry**; **agent `SecretSource` backends** (gopass) — progressing (363, the
  separate secrets thread).
- **Migration** (`production_migration.rs`) — its Craft→Software targets change with re-nesting
  (§2.3).

## 2. The domain model — `Software` under `Technology`

### 2.1 The nested tree

`Technology` is the broad tech area; `Software` is a **cluster inside it**, keeping its 12
sub-clusters. Sparse hardware leaves stay shallow beside it — mixed depth is exactly
density-proportional (`4wt3`): the sparse branches stay 2-tier, the dense software branch goes
4-tier.

```
Technology [
  Energy Power Robotics Materials Machinery Instrumentation Aerospace   ;; 2-tier hardware leaves
  Automation Networking                                                  ;; hardware senses (see §5)
  (Software [                                                            ;; the dense 4-tier cluster
    (Languages [...]) (Theory [...]) (Systems [...]) (Distributed [...])
    (Data [...]) (Intelligence [...]) (Security [...]) (Quality [...])
    (Operations [...]) (Observability [...]) (Surfaces [...]) (Engineering [...])
  ])
]
```

Resulting domain values, at their natural depths:

```
(Technology Energy)                                       ;; 2-tier, sparse hardware
(Technology (Software Quality))                           ;; a scope (cluster) — §3
(Technology (Software (Quality PropertyBasedTesting)))    ;; 4-tier leaf, dense software
```

The flat `Technology(Intelligence)` leaf is **removed** — AI is now
`Technology(Software(Intelligence(...)))` (§5).

### 2.2 Why nested (the reasoning, settled)

"Software is a kind of technology" becomes the **tree shape**, not a relation. This drops the
flawed directional subsumption (it fired in the noisy direction — a whole-`Technology` sweep
flooding with ~200 software domains — and was idle for the query you'd actually run); nesting
makes it not merely flawed but *unnecessary*, because scope prefix-matching (§3) already gives
"all of Technology, software included." Cost accepted: the software branch is 4-tier, the
deepest = densest, written mostly via scopes and tools.

### 2.3 Migration delta

`production_migration.rs` already maps the 7 evicted Craft software-leaves to top-level
`Software`. Re-target each under `Technology`:
`(Craft Architecture)` → `(Technology (Software (Engineering SoftwareArchitecture)))`, etc.
Live blast radius is still ~2 records (589). Any records already tagged top-level `(Software …)`
on `c30bed3` re-nest under `Technology`. Pre-deploy, free.

## 3. Domain scopes — prefix matching at any depth

A **`DomainScope`** is a *prefix* of a `Domain` at **any** depth, matching everything beneath:

```
Technology                                       ;; area — all of it, software included
(Technology Software)                            ;; cluster — all software
(Technology (Software Quality))                  ;; sub-cluster — all software-quality
(Technology (Software (Quality PropertyBasedTesting)))  ;; leaf — exactly that
```

Generalize `Partial`/`Full` to carry `DomainScope`s rather than full leaves. A record's
`Domain` *matches a scope* iff the scope is a prefix of it. This is independently useful and
is the substrate equivalence expands over. **Type modeling is operator's call**; recommended:
extract `AreaTag`/`ClusterTag`/`SubclusterTag` and define `DomainScope` as a prefix sum.

## 4. The relation — equivalence only — and where it lives

### 4.1 Taxonomy schema (a new schema kind, `mn3k`)

The vocabulary becomes a **first-class schema surface**, not a buried type or ad-hoc data
file. Extract `Domain` out of `signal.schema` into `schema/domain.schema`, which holds the
variant tree **and** its equivalences as one visible source of truth; the planes `Import`
`Domain` from it (that mechanism already exists in `signal.schema`). The new schema-language
construct declares relations **over an enum's values**:

```
;; schema/domain.schema
Domain     [ ... (Technology [... (Software [...])]) ... ]
Relations  [
  (Equivalence [(Technology Networking) (Technology (Software (Distributed Networking)))])
  (Equivalence [(Information Database)   (Technology (Software (Data DatabaseSystems)))])
]
```

It is a reusable schema *kind* — persona-mind declares its own taxonomy the same way.

**Rust shape (generated):**
```rust
pub enum Domain { /* ... */ Technology(Technology) /* Software is inside Technology */ }
pub enum DomainScope { /* prefix at any depth */ }
// the Relations section → a compiled equivalence table, exposed as one method
// (rust-discipline: emitted into an impl, not a free fn/const):
impl DomainScope { pub fn expand(&self) -> ScopeSet { /* equivalence closure */ } }
```

### 4.2 Equivalence semantics + expansion

`Equivalence` is a **symmetric** class of scopes that retrieve together. Expansion, in the
SEMA query path before matching: for each requested scope, add every scope sharing an
`Equivalence` class with it (declared classes are complete — **no transitive chaining across
classes**). Then prefix-match. Symmetric, both directions. There is no subsumption step.

### 4.3 Two consumers, one mechanism

- **Observe / Count / Subscribe** — `DomainMatch` expands before the query plan; user
  retrieval is robust to which equivalent domain a record was filed under.
- **Guardian retrieval** — `guardian_records_for` expands the candidate's domain by the same
  closure, closing report 585's **complete-retrieval** gap: the guardian sees records under
  *equivalent* domains, catching cross-boundary duplicates/contradictions.

### 4.4 Discipline

Equivalence is for **genuine near-synonyms only** — over-linking collapses the fine
vocabulary into synonym soup. No auto-transitivity. Relations make *retrieval* forgiving; they
do not relieve the guardian of filing each record *somewhere* — they lower the stakes of that
choice.

## 5. Overlap resolution

Nesting resolves most overlaps **structurally by absorption**; the genuine dual-framings stay
as **symmetric equivalences**:

| Overlap | Resolution |
|---|---|
| `Technology(Intelligence)` vs software AI | **Absorbed** — delete the flat leaf; AI is `Technology(Software(Intelligence(...)))` |
| networking (hardware vs software) | **Equivalence** `(Technology Networking) ≡ (Technology (Software (Distributed Networking)))` |
| `Automation` (industrial vs software) | **Keep both, no link** — different subjects (`(Technology Automation)` hardware; `Technology(Software(Operations))` software) |
| `Information(Database)` vs software DB | **Equivalence** `(Information Database) ≡ (Technology (Software (Data DatabaseSystems)))` |
| `Knowledge(Computing)` vs `Software(Theory)` | **Keep separate** (psyche) — Computing-as-science is broader than software-theory; no link |

**Open sub-decision — Technology's internal structure (§8.1).** Lean: keep the hardware leaves
flat (2-tier) beside the `Software` cluster — mixed depth is density-proportional, minimal
churn. Decide whether `Networking`/`Automation` keep a hardware leaf (as above) or fully
absorb.

## 6. Guardian residue (updated for 363)

The guardian's plumbing and most of its prompt are done and **live-validated** (363). What
remains:

- **Few-shot block** — `guardian_prompt.rs` is the home. **Seed it from 363's live scenario
  set** (the accept / reject-Contradiction / reject-Compound / reject-NonIntent cases are
  already curated, real, model-validated examples). Highest remaining judgment lever.
- **Retrieval completeness + equivalence-expansion** — the one guardian item the relations
  carry: have `guardian_records_for` produce a complete, ranked bundle and **equivalence-expand
  it** (§4.3). Tie this to the relation implementation.
- **Glosses — not needed.** The live prompt already judges domain-fit through the
  `UnclearDomain` reason without any gloss layer (`2rb7` vindicated). Do not add one.

## 7. Falsifiable spec (round-trip + behavior)

1. **Scope round-trips** — each §3 `(Partial […])` / `(Full […])` encodes↔decodes through
   NOTA + rkyv, including 4-tier leaves and shallow scopes.
2. **Relation data round-trips** — the §4.1 `Relations` block.
3. **Equivalence expansion** — a record under `(Technology Networking)` is returned by a query
   for `(Technology (Software (Distributed Networking)))`, and vice versa.
4. **Scope breadth** — a `(Technology Software)` query returns every software leaf; a
   `Technology` query returns hardware *and* software; a leaf query returns only the leaf.
5. **No-chaining** — equivalence does not leak across two classes sharing a member.
6. **Guardian completeness** — with a `(Technology Networking)` record and an equivalent
   software-networking duplicate, proposing the second is `Reject Duplicate`.

## 8. Decisions for the psyche

1. **Technology's internal structure (§5)** — hardware leaves flat beside the `Software`
   cluster (lean: yes), and the `Networking`/`Automation` calls.
2. **Confirm the re-nest (§2)** — `Software` becomes `Technology(Software(...))`, 4-tier. (Per
   `2msx`; restated here as the schema action.)

## 9. Out of scope this round (deferred)

- **Corpus-wide semantic re-tag** (~1400 records in catch-all leaves) — needs an LLM pass;
  *deferred per psyche*. Equivalence softens the need.
- **`kasm` / Craft-software re-file** — folds into the deferred re-tag.
- **588 `INTENT.md` prose** — designer-owned, lands on a designer `next` branch.

## 10. Net

Self-contained and additive: re-nest `Software` under `Technology` (§2) → scopes (§3) →
the one equivalence relation in a taxonomy schema (§4) → structural overlap resolution (§5) →
guardian residue that now has a home and a live test vehicle (§6). The is-a is carried by
structure, breadth by scopes, synonymy by equivalence — and nothing by convention. No new wire
verb; the relations are compiled vocabulary. The secrets/key-handling work on the `agent`
daemon is a separate component thread and is not folded in here.
