# Nexus Tier 0 grammar — the plain explanation

Status: design clarification + operator help
Author: Claude (designer)

Operator created `~/primary/repos/nexus/spec/examples/tier-0-canonical.nexus`
(working from the design arc reports 22–35) but the file uses
forms the grammar locked out, and reserves forms the grammar
permanently dropped. The cause is on me: the Tier 0 grammar
was decided across several reports, none of which is a single
"here is the complete grammar" reference. This report fixes
that.

The intent: a single canonical explanation operator can use
to update `nexus/spec/grammar.md`, plus questions that surface
genuine ambiguity in what the design arc settled (or didn't).

---

## 0 · TL;DR — the complete Tier 0 grammar

```mermaid
flowchart TB
    subgraph delim["delimiters (2 pairs)"]
        rec["( ) records"]
        seq["[ ] sequences"]
    end

    subgraph mark["in-position markers"]
        at["@<name> bind"]
        wild["_ wildcard (just an ident)"]
    end

    subgraph lit["literals"]
        nums["Int / UInt / Float"]
        bool["Bool: true / false"]
        str["String: \"...\" or bare ident"]
        bytes["#hex bytes"]
        none["None (Option absent sentinel)"]
    end

    subgraph idents["identifier classes"]
        pascal["PascalCase: types/variants"]
        camel["camelCase: fields/instances"]
        kebab["kebab-case: titles/tags"]
    end
```

**That's everything.** No `(| |)` patterns. No `~` `!` `?`
`*` verb sigils. No `{ }` shapes. No `[| |]` atomic batches.
No `=` bind aliases.

| Construct | Form | Role |
|---|---|---|
| Record | `(KindName field0 field1 …)` | Named composite, positional fields |
| Sequence | `[elem0 elem1 …]` | Ordered collection |
| Bind | `@fieldname` | In pattern position only; matches the schema field name |
| Wildcard | `_` | In pattern position only; matches anything without binding |
| Comment | `;; …` | Parser-discarded line |
| Path | `Char:Upper:A` | Nested name with `:` separator |
| Byte literal | `#a1b2c3` | Hex bytes, even-length, lowercase |
| Inline string | `"text"` | Quoted |
| Multiline string | `"""…"""` | Auto-dedented |
| Bare-ident string | `nota-codec` | When schema expects String |

12 token variants in the lexer. First-token-decidable. Max
2-character lookahead. **No piped delimiters anywhere; no
curly braces; no verb sigils.**

---

## 1 · The two delimiter pairs

### `( )` — records

A typed composite. The first token after `(` is a PascalCase
identifier naming the record kind. Subsequent tokens are
positional fields, in source-declaration order from the Rust
schema.

```nexus
;; A Point record — schema: struct Point { horizontal: f64, vertical: f64 }
(Point 3.0 4.0)

;; A Node — schema: struct Node { name: String }
(Node "User")
(Node nexus-daemon)         ;; bare-ident-as-string

;; An Edge — schema: struct Edge { from: Slot<Node>, to: Slot<Node>, kind: RelationKind }
(Edge 100 101 Flow)         ;; Flow is a unit variant of RelationKind

;; Nested — record fields can be records
(Line (Point 0.0 0.0) (Point 10.0 10.0))
```

The receiving type at each field's position determines how
the field decodes. Fields aren't named in the text — position
carries identity.

### `[ ]` — sequences

An ordered collection. Elements are typed; the receiving Rust
type names the element type and the collection shape (`Vec<T>`,
`BTreeSet<T>`, `BTreeMap<K, V>` via pair-sequences, etc.).

```nexus
;; Vec<Node>
[(Node alice) (Node bob) (Node carol)]

;; Vec<Slot<Node>>
[100 101 102]

;; BTreeMap<String, u32> as sequence-of-pairs
[("name" 1) ("age" 2)]

;; Empty sequence
[]
```

The schema knows whether a `[a b c]` is a `Vec`, a
`BTreeSet`, or a sorted-`BTreeMap`-as-pairs. The wire form
doesn't distinguish.

---

## 2 · The two in-position markers

These appear **inside** a `( )` form, at field positions, and
only when the receiving Rust type at that position is a
`PatternField<T>`. Outside a pattern position, they're parse
errors.

### `@<fieldname>` — bind

Matches whatever value the schema field at this position
holds, and **binds** it to the name `<fieldname>`. The
`<fieldname>` **must equal the schema field name** at this
position; the parser rejects any other name. (This is what
makes the IR free of bind-name strings — position carries
identity.)

```nexus
;; NodeQuery: { name: PatternField<String> }
(Node @name)

;; EdgeQuery: { from, to, kind: PatternField<...> }
(Edge @from @to @kind)

;; Mixing concrete + bind
(Edge 100 @to Flow)
```

### `_` — wildcard

Matches any value without binding. Just a bare ident `_`;
no special token in the lexer.

```nexus
;; Match Edge with from=100, kind=Flow, any to
(Edge 100 _ Flow)

;; Match Node with any name
(Node _)
```

### When are these `PatternField` positions?

The receiving Rust type tells the decoder. If the Rust type
is `Node` (data record), the field types are `String`,
`u32`, etc. — `@` and `_` are parse errors.

If the Rust type is `NodeQuery` (the paired query type, with
fields of `PatternField<T>`), the decoder reads `@`,
`_`, or a concrete value at each position.

```rust
struct Node { name: String }
struct NodeQuery { name: PatternField<String> }
```

The text `(Node @name)` decodes into a `NodeQuery` if it
appears at a `NodeQuery`-expecting position; it's a parse
error if it appears at a `Node`-expecting position.

---

## 3 · Patterns vs data — the schema-driven distinction

This is the key Tier 0 insight that operator's file got tangled
in.

**Same delimiters; different decoded values, chosen by the
receiving type.**

| Text | Receiving type | Decoded value |
|---|---|---|
| `(Node "User")` | `Node` | `Node { name: "User" }` |
| `(Node @name)` | `NodeQuery` | `NodeQuery { name: PatternField::Bind(BindName("name")) }` |
| `(Node _)` | `NodeQuery` | `NodeQuery { name: PatternField::Wildcard }` |
| `(Node "User")` | `NodeQuery` | `NodeQuery { name: PatternField::Match("User") }` |
| `(Node @name)` | `Node` | **Parse error** — `@` invalid in `String` position |
| `(Node _)` | `Node` | **Parse error** — `_` not a `String` value |

The wire text `(Node @name)` looks like a record either way
— it's the schema-typed receiver that decides what it means.
**There is no separate pattern-delimiter pair to mark "this
is a pattern."** The original nexus's `(| Node @name |)` was
dropped in Tier 0 (per designer/23 §"Tier 0 vs Tier 1") for
exactly this reason: the schema was already disambiguating;
the piped delimiter was redundant visual cue.

---

## 4 · Top-level forms — the verb question (OPEN)

Nexus is a request-reply protocol. Every top-level form on
the wire is a request (or a reply on the response side).
Requests are typed records — variants of a closed `Request`
enum.

```rust
enum Request {
    Assert(AssertOperation),
    Mutate(MutateOperation),
    Retract(RetractOperation),
    Match(MatchQuery),
    Subscribe(SubscribeQuery),
    Validate(ValidateRequest),
    Aggregate(AggregateQuery),
    Project(ProjectQuery),
    Constrain(ConstrainQuery),
    Recurse(RecurseQuery),
    Infer(InferQuery),
    Atomic(AtomicBatch),
}
```

The 12 verbs from designer/26 §8 (the canonical scaffold).

**Every top-level form has a verb head identifier.** That
means the canonical wire form is:

```nexus
;; Assert a Node:
(Assert (Node "User"))

;; Match for Nodes by name pattern:
(Match (NodeQuery @name) Any)

;; Mutate a Node at a slot:
(Mutate (Slot 100) (Node "Renamed"))

;; Retract a Node at a slot:
(Retract Node 100)

;; Subscribe to a pattern:
(Subscribe (NodeQuery @name) ImmediateExtension Block)

;; Validate (dry-run) a mutation:
(Validate (Mutate (Slot 100) (Node "Tentative")))

;; Atomic batch:
(Atomic [(Assert (Node a)) (Mutate (Slot 100) (Node b))])
```

### The open question: implicit-assert shorthand?

The **original nexus grammar** (per `nexus/spec/grammar.md`
as it existed before Tier 0) said:

> *"A nexus expression at the top level is one verb. The
> verb is determined by the leading sigil + delimiter:
> `(R …)` | Assert | State a fact: this record exists"*

That is: a bare top-level `(Node "User")` was an implicit
**Assert**. The verb sigil was empty for the most common
operation.

**Operator/37 §1 example file uses this convention** —
top-level `(Node User)` as an Assert.

**Tier 0 didn't decide this explicitly.** Designer/26 §8
shows the closed Request enum but doesn't say whether
top-level forms must be wrapped (`(Assert (Node User))`) or
whether bare records are still implicit-assert.

Two options:

| Option | Wire form for "assert a Node" | Trade |
|---|---|---|
| **A. Fully explicit** | `(Assert (Node "User"))` | Verbose; uniform; the parser dispatches via the head ident only |
| **B. Implicit-assert shorthand** | `(Node "User")` (bare top-level) | Concise; matches old nexus; the parser must distinguish "is this head a Request variant or a domain kind?" |

**Question for the user:** Does Tier 0 keep the implicit-
assert shorthand (Option B), or require fully-explicit
verbs (Option A)?

My weak recommendation: **fully explicit (A)**. The Tier 0
spirit is "everything is a record dispatched by head
identifier" — implicit-assert breaks that uniformity. But
this is a real design choice; the user's call.

---

## 5 · The 12 verbs as records — concrete examples

Assuming Option A (fully-explicit), each verb at the wire:

### State-mutating

```nexus
;; Assert: introduce a new record. Slot is assigned by the store.
(Assert (Node "User"))
(Assert (Edge 100 101 Flow))

;; Mutate: replace at a slot. (Slot 100) is the slot reference.
(Mutate (Slot 100) (Node "Renamed"))

;; Retract: remove a record by slot. The kind is named.
(Retract Node 100)
(Retract Edge 200)

;; Atomic: bundle multiple operations.
(Atomic [(Assert (Node a))
         (Mutate (Slot 100) (Node b))
         (Retract Node 50)])
```

### Reads

```nexus
;; Match: find records by pattern.
(Match (NodeQuery @name) Any)

;; Match with cardinality limit:
(Match (NodeQuery @name) (Limit 10))

;; Subscribe: continuous match.
(Subscribe (NodeQuery @name) ImmediateExtension Block)

;; Validate: dry-run a state-mutating verb.
(Validate (Mutate (Slot 100) (Node "Tentative")))
```

### Reductions and composition

```nexus
;; Aggregate: reduce a matched set.
(Aggregate (NodeQuery @name) Count)
(Aggregate (EdgeQuery @from @to @kind) (GroupBy kind Count))

;; Project: select fields.
(Project (NodeQuery @name) (Fields [name]) Any)

;; Constrain: multi-pattern with bind unification.
(Constrain
  [(EdgeQuery 100 @to Flow)
   (NodeQuery @to)]
  (Unify [to])
  Any)

;; Recurse: fixpoint over a base + recursive pattern.
(Recurse (NodeQuery @name)
         (EdgeQuery @from @to DependsOn)
         Fixpoint)

;; Infer: apply rules to derive non-stored facts.
(Infer (NodeQuery @name) StandardOntology)
```

These are sketches — the exact field structures of each
*Query record need to be settled in `signal-core` before
canonical examples lock. But the **shape** is uniform:
verb-head record, payload records inside, schema-driven
PatternField positions for binds.

---

## 6 · Reply shapes

Replies are typed records too. The `Reply` enum (also
closed):

```rust
enum Reply {
    Ok,
    Diagnostic(Diagnostic),
    Records(Records),         // for Match / Subscribe results
    Outcome(OutcomeMessage),  // for state-mutating outcomes
    Outcomes(Vec<OutcomeMessage>),  // for AtomicBatch
    HandshakeAccepted(...),
    HandshakeRejected(...),
}
```

Wire forms:

```nexus
;; Success ack for a state-mutating verb:
(Ok)

;; Diagnostic / failure:
(Diagnostic Error "E0042" "no binding for unknown-target")

;; Match reply: a Records variant per kind.
;; Records::Node(Vec<Node>) renders as a sequence of Node records:
[(Node "User") (Node "nexus daemon") (Node "criome daemon")]

;; AtomicBatch reply: per-operation outcomes:
[(Ok) (Diagnostic Error "E0042" "conflict on slot 100") (Ok)]
```

### Question: how do replies carry slots?

Operator/37's example file used `(Tuple 1024 (Node User))` to
attach a slot to a record in a reply. **`Tuple` isn't a
typed kind** — it's an anonymous-tuple-as-record pattern,
which `~/primary/skills/rust-discipline.md` §"One object in,
one object out" rejects ("anonymous tuples are not used at
type boundaries").

Three plausible designs for "slotted record" replies:

**Option 1: Reply records carry slots in their structure.** The
data records themselves get a slot field when they appear in
replies. Wire form: `(Node 1024 "User")` if the schema for
"Node-with-slot" puts slot first.

But wait — this mixes assert-Node (no slot, store assigns)
with reply-Node (with slot, store-allocated). They can't be
the same record kind.

**Option 2: Replies use a pair record.** `(SlotBinding 1024
(Node "User"))` — a typed record `SlotBinding<T> { slot:
Slot<T>, value: T }`. The `Records::Node` reply variant
becomes `Vec<SlotBinding<Node>>`, rendering as a sequence of
`SlotBinding` records.

**Option 3: Replies omit slots.** Most reply paths don't need
the slot — the consumer queries for matches and gets the
record values; if they later want to mutate, they query
again (or a separate `MatchWithSlots` request returns
slot-record pairs).

This is **a real design gap.** signal/edit.rs currently has
`Records::Node(Vec<Node>)` — slot-free. If consumers need
slots for mutation, signal would need a paired type.

**Question for the user:** how should reply records carry
slot information? Recommend Option 2 (typed `SlotBinding<T>`
record) for simplicity and uniformity.

---

## 7 · What was dropped (and why)

For operator's reference, the table of "this used to be in
the spec but is now permanently dropped":

| Dropped construct | Old form | Tier 0 equivalent | Why dropped |
|---|---|---|---|
| `(\| \|)` pattern delimiter | `(\| Node @name \|)` | `(Node @name)` (in pattern position) | Schema disambiguates patterns from data — the delimiter was redundant. (designer/23 §"Tier 0 vs Tier 1") |
| `[\| \|]` atomic batch delimiter | `[\| (Node a) ~(Node b) \|]` | `(Atomic [(Assert (Node a)) (Mutate ...)])` | Atomic is a verb (record), not a delimiter. Per designer/26 §"closed Request enum". |
| `{ }` shape projection | `(\| Node @name \|) { @name }` | `(Project (NodeQuery @name) (Fields [name]) Any)` | Projection is a verb (record), not a delimiter. Per designer/22 §"shape" + designer/31 §"drop permanently". |
| `{\| \|}` constrain | `{\| (\| Node @id \|) (\| Edge @id \|) \|}` | `(Constrain [pat1 pat2] (Unify [id]) Any)` | Constrain is a verb. Per designer/22 §"constrain" + designer/26 §8. |
| `~` mutate sigil | `~(Node 100 "Updated")` | `(Mutate (Slot 100) (Node "Updated"))` | Verb-in-delimiter anti-pattern. Verbs are records. (designer/23 + 26 + 31) |
| `!` retract sigil | `!(Node 100)` | `(Retract Node 100)` | Same — verbs are records |
| `?` validate sigil | `?(Node "Tentative")` | `(Validate (Assert (Node "Tentative")))` | Same |
| `*` subscribe sigil | `*(\| Node @name \|)` | `(Subscribe (NodeQuery @name) ImmediateExtension Block)` | Same |
| `=` bind aliasing | `(\| Pair @left=@right \|)` | Not implemented; defer until needed | Per designer/22 §8 "no consumer" |
| `< > <= >= !=` comparison ops | `(\| Person @age (@age < 21) \|)` | Predicates as schema records: `(Adult @age)` where `Adult` is a typed predicate kind | Per designer/22 §"reserved comparisons" + designer/26 §11 |

The token vocabulary is locked at 12 variants per
designer/31 §5.

---

## 8 · What operator/37's file should change

Concrete adjustments to
`~/primary/repos/nexus/spec/examples/tier-0-canonical.nexus`:

| Line(s) | Current | Should be | Why |
|---|---|---|---|
| 27 | `(\| Node @name \|)` | `(Match (NodeQuery @name) Any)` | Tier 0 dropped piped patterns; queries are records inside `Match` |
| 28 | `(\| Edge @from @to @kind \|)` | `(Match (EdgeQuery @from @to @kind) Any)` | Same |
| 29 | `(\| Edge 100 @to Flow \|)` | `(Match (EdgeQuery 100 @to Flow) Any)` | Same |
| 38 | `(\| Node "nexus daemon" \|)` | `(Match (NodeQuery "nexus daemon") Any)` | Same |
| 39 | `(\| Edge _ @to DependsOn \|)` | `(Match (EdgeQuery _ @to DependsOn) Any)` | Same |
| 50 | `(Tuple 1024 (Node User))` | depends on user's call (§6 question) | Tuple isn't typed; needs slot-binding record kind decision |
| 61 | `~(Node "renamed")` | `(Mutate (Slot N) (Node "renamed"))` | Verb sigils permanently dropped |
| 62 | `!(Node User)` | `(Retract Node N)` | Same |
| 63 | `?(Node "dry run")` | `(Validate (Assert (Node "dry run")))` | Same |
| 64 | `*(\| Node @name \|)` | `(Subscribe (NodeQuery @name) ImmediateExtension Block)` | Same |
| 65 | `[\| (Node A) (Node B) \|]` | `(Atomic [(Assert (Node A)) (Assert (Node B))])` | Atomic batch is a record |

Plus the assert lines (16–18):

| Line(s) | Current | Choice |
|---|---|---|
| 16 | `(Node User)` | If Option A: `(Assert (Node User))`. If Option B (shorthand): keep as-is. |
| 17 | `(Node "nexus daemon")` | Same |
| 18 | `(Edge 100 101 Flow)` | Same |

And the comment "These forms belong to the language design but
are not active in the current M0 daemon" (line 58) needs
correcting — these forms are **permanently dropped**, not
"reserved for later." The grammar has 12 token variants, not
22. The verb-record forms `(Mutate …)` / `(Retract …)` etc.
are the active forms; the sigils are not "reserved" for any
future use.

---

## 9 · Open questions for the user

These are real design ambiguities the design arc didn't fully
settle. Each one affects the canonical example file.

### Q1 — Implicit-assert shorthand at top level?

**Question:** Does Tier 0 keep the original nexus convention
that bare `(Node User)` at top level means `(Assert (Node
User))`, or require the explicit wrapper?

**Options:**
- **A. Fully explicit:** every top-level form is a verb
  record. `(Assert (Node User))` always.
- **B. Implicit-assert shorthand:** bare records at top level
  are implicit-asserts. `(Node User)` ≡ `(Assert (Node User))`.

**Designer's lean:** A (uniformity). User's call.

### Q2 — How do replies carry slot information?

**Question:** When a `Match` reply returns records, do the
records carry their slots (so the consumer can mutate them
later)?

**Options:**
- **1. Slot-free replies:** `Records::Node(Vec<Node>)`.
  Consumer queries again with constraint to find the slot.
- **2. Slot-binding pairs:** `Records::Node(Vec<SlotBinding<Node>>)`,
  rendered as `[(SlotBinding 100 (Node "User")) …]`.
- **3. Slot-bearing variant:** records embed slots when
  returned, slot-free when asserted. Two record kinds
  (`Node` for assert; `SlottedNode` for replies).

**Designer's lean:** 2 (typed pair record; matches
verb-belongs-to-noun discipline). User's call.

### Q3 — `(Slot N)` as the wire form for slot references?

**Question:** When `Mutate` and `Retract` need to reference a
slot, what's the wire form?

`Slot<T>` is per `signal/src/slot.rs` a `NotaTransparent`
newtype around `u64`. Per nota's transparent rule, it emits
bare: just `100`, not `(Slot 100)`.

But context-free, a bare `100` is ambiguous (`u64`?
`Slot<Node>`?). The schema at the receiving position
determines. So:
- `(Mutate 100 (Node "Renamed"))` if `MutateOperation::Node
  { slot: Slot<Node>, new: Node, … }` is the schema.
- `(Retract Node 100)` if `RetractOperation::Node { slot:
  Slot<Node> }` is the schema.

The bare-integer form is consistent with `signal`'s current
design (per `signal/src/edit.rs`).

**Question:** confirm that `Mutate` / `Retract` use bare
integer slots, not wrapped `(Slot 100)` records?

**Designer's lean:** bare integer (matching signal's current
shape).

### Q4 — The `*Query` naming

**Question:** Is the convention that every record kind `Foo`
has a paired query type `FooQuery` whose fields are
`PatternField<T>`? Or should queries be embedded directly in
the record name (`Node` for both data and query, with the
schema choosing interpretation)?

`signal/src/flow.rs` already uses `NodeQuery` /
`EdgeQuery` / `GraphQuery`. That's the established
pattern.

**Question:** confirm `*Query` naming as the workspace
convention?

**Designer's lean:** confirm. The existing signal pattern is
right.

### Q5 — `_` wildcard inside non-pattern positions

**Question:** Is `_` ever valid outside a pattern position?

In nexus's old grammar, `_` was *only* valid in pattern
positions. Outside a pattern, it was a parse error.

**Question:** confirm `_` stays pattern-position-only?

**Designer's lean:** confirm. `_` outside patterns has no
clear meaning.

### Q6 — Record-as-data vs record-as-query at top level

**Question:** if Option B (implicit-assert) is chosen for Q1,
how does the parser distinguish `(NodeQuery @name)` (a
top-level query? what verb does it imply?) from `(Node
User)` (a top-level assert)?

This is a real complication for Option B. With Option A, no
ambiguity: every top-level form has a verb head.

If Option B is chosen, probably:
- `(Match (NodeQuery @name) Any)` — explicit Match wrapping
  is required for queries.
- `(Node User)` — implicit Assert for data records.
- The parser dispatches based on the head identifier:
  if it's a Request variant (`Match`, `Mutate`, etc.), the
  verb is named; otherwise the bare record is implicit
  Assert.

This requires the parser to know the closed Request enum at
parse time, which it does anyway.

---

## 10 · For nexus/spec/grammar.md

The above can become the structure for `nexus/spec/grammar.md`'s
Tier 0 update. Suggested layout:

1. **Introduction** — what nexus is (typed text format
   mirroring rkyv); the principle "delimiters define
   structure, head identifiers define meaning."
2. **The grammar** — §1 and §2 of this report.
3. **Patterns** — §3 of this report.
4. **Top-level forms (Requests)** — §4 + §5 of this report,
   with the user's answer to Q1.
5. **Replies** — §6 of this report, with the user's answer to
   Q2.
6. **Examples** — concrete canonical examples for each verb,
   parallel to the test suite.
7. **What was dropped** — §7 of this report, as a "what
   changed from earlier nexus" reference.

Operator can use this structure to update grammar.md once
the user answers the open questions in §9.

---

## 11 · See also

### Internal arc
- `~/primary/reports/designer/22-nexus-state-of-the-language.md`
  — original audit; identified what was in the old spec but
  unused.
- `~/primary/reports/designer/23-nexus-structural-minimum.md`
  §"Tier 0 vs Tier 1" — picked Tier 0 (drop piped pattern
  delimiters in favor of schema-driven disambiguation).
- `~/primary/reports/designer/26-twelve-verbs-as-zodiac.md`
  §8 — the closed Request enum scaffold.
- `~/primary/reports/designer/31-curly-brackets-drop-permanently.md`
  §5 — the locked grammar at 12 token variants.
- `~/primary/reports/designer/35-operator-33-34-critique.md`
  §3 — the Tier 0 grammar lock referenced from operator/34's
  restructure plan.

### Operator
- `~/primary/repos/nexus/spec/examples/tier-0-canonical.nexus`
  — the file this report is meant to help operator fix.
- `~/primary/reports/operator/37-sema-signal-nexus-execution-plan.md`
  §6 — the Nexus daemon stance (keep Criome-specific in M0;
  spec becomes domain-neutral).

### Skills
- `~/primary/skills/language-design.md` §18 "Delimiters earn
  their place" — the principle that justifies dropping
  unused delimiters.
- `~/primary/skills/contract-repo.md` §"PatternField<T>
  ownership" *(suggested follow-up — currently not in the
  skill; belongs in nota-codec/skills.md as a component-
  specific rule)*.
- `~/primary/repos/signal/src/slot.rs` — `Slot<T>` and the
  `NotaTransparent` newtype pattern.
- `~/primary/repos/signal/src/edit.rs` — `AssertOperation`,
  `MutateOperation`, `RetractOperation`, `AtomicBatch` —
  the typed payloads operator/37 wants to lock first.

---

*End report.*
