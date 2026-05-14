# 161 — How to research the signal-core verb roots

*Designer research brief, 2026-05-14. Scopes the question of where
`signal-core::SemaVerb`'s twelve verbs come from — not just as names
but as a closed set that names every operation crossing a Signal
boundary. The workspace recently committed (per DA `/43` recovery +
this session's verb-spine work) that **Signal is the workspace's
typed binary database-operation language** and every cross-component
request declares which of these twelve verbs it instantiates. That
makes the choice of these verbs (and not others) load-bearing
architectural truth. This report does not answer the question; it
scopes the research that should.*

**Retires when:** a follow-up research report lands answering the
questions in §3 with concrete genealogy + completeness analysis +
forward-to-eventual-Sema connection.

---

## 0 · TL;DR

The twelve verbs in `signal-core/src/request.rs:6-19` —

```
Assert  Subscribe  Constrain  Mutate  Match  Infer
Retract  Aggregate  Project  Atomic  Validate  Recurse
```

— are the closed dispatch set every cross-component Signal request
maps to (per `~/primary/skills/contract-repo.md` §"Signal is the
database language — every request declares a verb"). The workspace
has committed to them being load-bearing: if no existing verb fits a
new payload, that's a design event (the payload is mis-modeled, or
the verb set is incomplete — per ESSENCE-level commitment).

We know **where the verbs live now** (`signal-core`, recovered from
`nexus-spec-archive` per DA `/43`), but we do not have a documented
account of:

- **Per-verb genealogy** — which database / programming-language
  tradition each verb's name and semantics come from;
- **Set completeness** — why exactly twelve, not ten or fifteen;
  what argument makes this set closed under workspace communication;
- **Composition closure** — which verbs are orthogonal vs which
  compose (e.g., `Atomic` is a meta-verb wrapping others; `Subscribe`
  is `Match` + push delivery);
- **Forward to eventual Sema** — when the workspace self-hosts on
  eventual `Sema` (per ESSENCE §"Today and eventually"), do these
  twelve persist? Are they Sema's primitive operations? Or do they
  collapse / expand?

These are research questions that a designer-assistant pass or an
Explore agent should answer. This brief specifies what to research,
where to read, and what the output should look like.

---

## 1 · The artifact

The twelve verbs as Rust:

```rust
// signal-core/src/request.rs:6-19
pub enum SemaVerb {
    Assert,      Subscribe,   Constrain,
    Mutate,      Match,       Infer,
    Retract,     Aggregate,   Project,
    Atomic,      Validate,    Recurse,
}
```

Carried by every Signal frame's envelope:

```rust
// signal-core/src/request.rs:21-25
pub enum Request<Payload> {
    Handshake(HandshakeRequest),
    Operation { verb: SemaVerb, payload: Payload },
}
```

And projected to text at the edge per `nexus/spec/grammar.md`:

```
Every top-level Nexus request is a verb record.
(Assert (Node User))
(Match (NodeQuery (Bind)) Any)
(Mutate 100 (Node "renamed"))
(Retract Node 100)
(Atomic [(Assert (Node A)) (Assert (Node B))])
(Subscribe (NodeQuery (Bind)) ImmediateExtension Block)
```

The twelve are the only operations that can cross a Signal boundary.
Per the verb-discipline rule (in `~/primary/skills/contract-repo.md`),
every `signal-<consumer>::Request` variant declares which verb it
instantiates; if no verb fits, the payload is mis-modeled or the
verb set is incomplete — and incompleteness is a workspace-level
coordinated change, not a per-contract escape hatch.

---

## 2 · What we already know

Two pieces of context the research can build on without re-doing:

### 2.1 · The verbs are recovered, not invented

Per DA `reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md`
§1.1-1.3: the verb spine was developed in older Nexus design work,
preserved in `/git/github.com/LiGoldragon/nexus-spec-archive/`. That
archive had:

- assert a typed record as a fact;
- mutate a record at a stable identity;
- retract an asserted fact;
- batch operations atomically;
- query by patterns with binds and wildcards;
- constrain multiple patterns through shared binds;
- support negation/left-join/datalog-like evaluation later.

The syntax retired (old `(| Node @name |)`, `~record`, `!record`,
`[| op1 op2 |]`); the semantic spine survived as `SemaVerb`. The
workspace's current commitment is "Signal is the typed binary
projection of the same language; Nexus/NOTA is the text projection."

### 2.2 · Per-component request mappings (partial, in progress)

Operator's verb-mapping witnesses (`/158 §6.1` Package 1, in flight)
will produce concrete mappings:

| Already mapped | Verb |
|---|---|
| `signal-persona` engine status | `Match` |
| `signal-persona` startup/shutdown | `Mutate` |
| `signal-persona` supervision hello/readiness/health | `Match` |
| `signal-persona` graceful stop | `Mutate` |
| `signal-persona-message::MessageSubmission` | `Assert` |
| `signal-persona-message::StampedMessageSubmission` | `Assert` |
| `signal-persona-introspect` observations (current four variants) | `Match` |
| `signal-persona-introspect::SubscribeComponent` (future, Slice 3) | `Subscribe` |
| `signal-persona-message::InboxQuery` (drift fix) | `Match` |

`Aggregate`, `Project`, `Constrain`, `Infer`, `Recurse`, `Atomic`,
`Validate` have no current concrete consumer mapping in the
prototype stack. They exist in the closed set but aren't yet used.

That gap is itself research material: are they reserved for
foreseeable use cases, or vestigial from the older Nexus work?

---

## 3 · Research questions

### Q1 · Per-verb genealogy

For each of the twelve verbs, the research should answer:

- **Naming origin.** Which database / programming-language tradition
  does the verb's name come from? (Hypothesis: Assert/Retract from
  Datomic + logic programming; Match/Project/Aggregate from
  relational algebra; Subscribe from reactive programming + event
  sourcing; Constrain/Infer/Recurse from Datalog; Atomic from SQL
  transactions; Validate from query EXPLAIN-shape; Mutate from
  GraphQL or CRUD discourse.)
- **Semantic root.** What does the verb mean *as a primitive
  operation* in its tradition? Cite the canonical reference (a
  Datomic page, a Datalog paper, Codd's relational algebra, a
  GraphQL spec section, etc.).
- **Workspace specialization.** How does the workspace's reading of
  the verb differ from its tradition? (E.g., the workspace's
  `Mutate` operates "at a stable identity" per `/43 §1.1` — that's
  closer to GraphQL Mutation than to Datomic's tx fns.)
- **Per-verb storage implication.** What does the verb require of
  `sema-engine`? (`Assert` needs append + log; `Subscribe` needs
  commit-then-emit; `Constrain` needs join over indexed patterns;
  `Recurse` needs fixed-point evaluation.) Some of this is already
  in `/157 §4` + `/158 §3`; the research can extend.

For each verb, expected output: 1-3 paragraphs naming the tradition,
the canonical reference, and how the workspace specializes.

### Q2 · Set completeness — why these twelve?

The question: **what argument makes this set closed under
workspace communication?**

Candidate frames:

- **Datalog completeness.** Datalog over typed records gives:
  reads (Match), joins (Constrain), aggregations (Aggregate),
  projections (Project), derivations (Infer), and transitive
  closure (Recurse). Plus operational verbs (Assert, Retract,
  Mutate) for state changes. Plus transactional (Atomic), reactive
  (Subscribe), and observational (Validate). Total: 12.
- **CRUD + Query + Event** framing. C/U/R/D = Assert/Mutate/
  Match/Retract. + Query → Match/Project/Aggregate/Constrain. +
  Event → Subscribe. + Transaction → Atomic. + Inference →
  Infer/Recurse. + Validation → Validate. The set covers
  CRUD+Query+Event+Transaction+Inference+Validation.
- **Operational vs algebraic split.** Write-shaped (`Assert`,
  `Mutate`, `Retract`, `Atomic`) vs read-shaped (`Match`,
  `Project`, `Aggregate`, `Constrain`, `Subscribe`,
  `Validate`, `Infer`, `Recurse`). 4 + 8 = 12.

The research should test these framings. Is the set genuinely
closed? Or is the closure argument missing verbs (e.g., `Index`
for explicit index management; `Schema` for type introspection;
`Quiesce`/`Drain` for shutdown coordination; `Replicate` for
distributed state)?

The workspace-level commitment ("if no verb fits, add a new verb")
makes set-completeness a falsifiable claim, not a definitional
one. Research should propose tests.

### Q3 · Composition closure

Are these verbs orthogonal (no overlap) or composing?

Specific cases:

- `Atomic` is meta-verb wrapping a sequence of `Assert`/`Mutate`/
  `Retract` operations. Is it a verb or a request-wrapper?
- `Subscribe` semantically composes `Match` (filter) + commit-then-emit
  push. Is `Subscribe` reducible to `Match` + a delivery primitive,
  or is it primitive?
- `Validate` is "execute as dry-run." Composes with `Assert` / `Mutate`
  / `Retract` / `Atomic`. Is it a verb or a modifier?
- `Infer` derives facts from rules — could be implemented via
  `Match` + materialized view. Primitive or derived?
- `Recurse` is fixed-point over `Match` + `Infer`. Primitive or
  derived?

The research should classify each verb on the orthogonal-vs-composing
axis. A composition reduction (some verbs being expressible in terms
of others) is not a defect; it's evidence for whether the set is
canonical or could be shrunk.

### Q4 · Forward to eventual Sema

Per `~/primary/ESSENCE.md` §"Today and eventually": eventual `Sema`
is the universal medium for meaning — self-hosting computational
substrate. The workspace plans to run "Sema on Sema": components are
Sema programs on a Sema runtime on a Sema-written OS.

The research should ask: **when the workspace self-hosts, do these
twelve verbs persist?**

- Are they Sema's primitive operations at the language level?
- Are they preserved as a wire protocol on top of Sema (signal-core
  becomes a Sema-implemented layer)?
- Or do they collapse — eventual Sema has a smaller closed set, or
  a richer one?

This is speculative but load-bearing for the workspace's long arc.
The verbs are today's contract; whether they survive eventual Sema
informs how seriously we treat them as canonical (vs heuristic).

### Q5 · Gaps and pressure points

Where might the twelve be incomplete? Specific research targets:

- **Schema introspection.** `ListRecordKinds` (per `/41 D7`) is
  arguably a `Match` over registered tables (per `/158 §3.1`
  `list_tables()`). Is "schema introspection" really `Match`, or
  is it conceptually distinct enough to be its own verb?
- **Permission / capability checks.** Today the daemon validates
  auth before passing to sema-engine (per `/158 §4` boundary).
  Should a verb explicitly name "permission probe" (akin to "may
  I do this?" before doing it)?
- **Coordination / consensus.** Distributed agreement is not a
  verb. In a self-hosting eventual-Sema world, is consensus a
  verb or a composition of `Constrain` + `Atomic`?
- **Schema migration.** Adding a column / changing a record kind
  is currently a coordinated upgrade outside the wire (per the
  schema-version guard in `sema`). Is migration a verb?
- **History / time travel.** Datomic's `db.asOf(t)` and
  `db.history()` aren't separate verbs; they're modifiers on the
  database value the query operates over. The workspace currently
  has `OperationLogEntry` + `SnapshotId` (per `/158 §4.6`); is
  "history" a verb-level concern or a database-handle concern?

The research should produce: a list of pressure points where the
twelve might be incomplete + designer-style argument for each
(add a verb? compose existing? out-of-scope?).

---

## 4 · What to read

The research grounds in primary sources for each verb's tradition.

### Datomic / Datalog tradition

- **Datomic documentation.** Specifically: `tx-data` (Assert /
  Retract as datom operations), `tx-report-queue` (Subscribe-shape
  change feed), `(d/q ...)` (Match query), `db.asOf(t)` +
  `db.history()` (snapshot/time semantics), `(d/transact ...)`
  (Atomic). Look for the conceptual frame: "what is a database?"
  → an immutable value, with operations producing new database
  values.
- **Datalog literature.** The canonical Datalog reference is
  Ceri, Gottlob, Tanca (1989) "What you always wanted to know
  about Datalog (and never dared to ask)." Plus modern Datalog
  systems: Soufflé, DDlog. For `Constrain` (joins via shared
  binds), `Infer` (rules), `Recurse` (fixed-point).
- **Prolog.** The deeper logic-programming tradition behind
  Datalog. `Infer` and `Recurse` come from Prolog's evaluation
  model.

### Relational algebra / SQL tradition

- **Codd 1970** "A Relational Model of Data for Large Shared Data
  Banks." The original relational algebra: select (Match),
  project (Project), join (Constrain), union, intersect,
  difference. Plus aggregation (Aggregate) which Codd added
  later as Codd 1972.
- **SQL standards.** Transactions (Atomic), EXPLAIN (Validate-shape).
- **Tarski's logical algebra.** The mathematical root of relational
  algebra; relevant if the research wants to go to first
  principles.

### Reactive / event-sourcing tradition

- **Event sourcing patterns** (Martin Fowler, etc.) for the
  Assert-as-event-emission framing.
- **CQRS** (Command Query Responsibility Segregation) for the
  read/write verb split.
- **GraphQL Spec** — Operations: Query, Mutation, Subscription.
  Three roots that map to the workspace's Match-shaped reads,
  Mutate-shaped writes, and Subscribe-shaped change feeds.
- **Reactive Streams** for the Subscribe delivery contract.

### Pattern-matching tradition

- **Erlang's pattern matching** for the `Bind` + `Wildcard` + literal
  match shape that `signal-core::PatternField<T>` implements.
- **Rust's `match`** is the local-language pattern-matching the
  workspace's prose intuition is built on.

### Workspace archeology

- `/git/github.com/LiGoldragon/nexus-spec-archive/README.md` +
  `ARCHITECTURE.md` — the original Nexus database-language work.
  This is the most direct source for *why these twelve* in the
  workspace specifically.
- `/git/github.com/LiGoldragon/nexus/spec/grammar.md` — the
  current Nexus grammar.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs:6-19` —
  the `SemaVerb` enum as it lives today.
- `/git/github.com/LiGoldragon/signal-core/src/pattern.rs:48-52` —
  the `PatternField<T>` pattern markers.
- `reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md`
  — the recovery synthesis. Its §4 verb-to-storage interpretation
  table is the starting point for Q1's per-verb genealogy.
- `reports/designer/157-sema-db-full-engine-direction.md` §4 — what
  each verb requires of `sema-engine`. Confirms (or contradicts) Q1's
  per-verb storage implication answers.

---

## 5 · Workspace archeology — what to surface

The older Nexus work in `nexus-spec-archive` likely has the most
direct answer to "why these twelve, not other twelve." The research
should look for:

- **Per-verb origin notes.** Did each verb get added in response to
  a specific use case? A specific external system the workspace
  was mimicking?
- **Verb-set evolution.** Did the set start smaller and grow? Or
  was it specified up-front?
- **Verbs that almost made it or got dropped.** Are there verbs in
  the archive that didn't survive to `signal-core`? Why?
- **The completeness argument.** Did the original Nexus work
  articulate *why* this set is closed?

The output here is: a chronological retelling of how the verb set
took its current shape, with the load-bearing decisions named.

---

## 6 · Output shape

The research returns a designer-side or designer-assistant-side
report (numbered after `/161`) containing:

1. **Per-verb genealogy** (Q1). A table or per-verb section: name,
   tradition, canonical reference, workspace specialization,
   storage implication. Twelve entries.
2. **Set-completeness argument** (Q2). Which framing makes the
   twelve closed? Tested against alternate framings. Falsifiable
   pressure points named.
3. **Composition map** (Q3). Which verbs are primitive, which are
   compositions or modifiers. A graph or table.
4. **Forward to eventual Sema** (Q4). Whether the twelve persist
   into self-hosting. Speculative but load-bearing.
5. **Gaps / pressure points** (Q5). A list of cases where the
   twelve might be incomplete, with designer-style argument for
   each (add / compose / out-of-scope).
6. **Workspace archeology** (§5). The history of how the verb set
   took shape in the older Nexus work.
7. **Recommendations.** Whether the set should be:
   - Frozen as-is (canonical workspace commitment);
   - Shrunk (remove vestigial verbs that aren't load-bearing);
   - Expanded (add the gap-pressure verbs Q5 surfaced);
   - Left to evolve (keep current set; revisit when concrete
     pressure appears).

The recommendation isn't pre-decided. The research informs it.

---

## 7 · Who runs the research

This is research-shaped, not implementation-shaped. Candidates:

- **Designer-assistant pass.** DA has done the verb-spine recovery
  work already (`/43`) and is the natural continuation.
- **Explore subagent.** For the per-verb genealogy + canonical
  references work — wide read across Datomic docs, Datalog
  literature, GraphQL spec, etc.
- **Combined.** Explore agent does the lit-review pass; DA
  synthesizes into the final report shape.

The research is not blocking — operator's `sema-engine` work
(`[primary-5ir2]` persona-mind first-consumer migration) continues
without it. But the **falsifiable pressure points (Q5)** matter for
ongoing work: every per-component verb-mapping witness Operator is
landing exercises the set's coverage. If a payload doesn't fit any
of the twelve, that's the workspace-level coordinated change the
verb-discipline rule names.

---

## 8 · See also

- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the canonical home
  for the verb-spine discipline. The "if no verb fits, we need
  another verb" rule is what makes Q5 (gaps) load-bearing.
- `reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md`
  — DA's recovery synthesis; the starting point for Q1 per-verb
  genealogy and §5 workspace archeology.
- `reports/designer/157-sema-db-full-engine-direction.md` §4 — what
  each verb requires of `sema-engine`. Q1 per-verb storage
  implication can extend from here.
- `reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`
  §3.5 (Subscribe delivery contract) + §4.6 (operation log +
  commit sequence) — concrete engine-side implementations of
  specific verbs that the research can compare against the verbs'
  tradition-side semantics.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs:6-19` —
  the artifact under research.
- `/git/github.com/LiGoldragon/nexus-spec-archive/` — the workspace
  archeology target.
- `/git/github.com/LiGoldragon/nexus/spec/grammar.md` — the current
  Nexus text projection.
- `~/primary/ESSENCE.md` §"Today and eventually" — the discipline
  that makes Q4 (forward-to-eventual-Sema) meaningful.
- `~/primary/ESSENCE.md` §"Perfect specificity at boundaries" — the
  principle that justifies a closed verb spine over an open
  "anything goes" wire vocabulary.
- `~/primary/skills/reporting.md` §"Kinds of reports — Research /
  exploratory draft" — this report's typology; retires when the
  follow-up research report lands.
