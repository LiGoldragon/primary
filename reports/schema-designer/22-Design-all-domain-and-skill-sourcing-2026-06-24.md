# 22 — The `All` domain, and Spirit-skill sourcing (design handoff)

Two decisions came out of an intent-alignment session on the central
essence/intent material. Both are captured in Spirit; this report is the
implementation handoff for the schema-operator (the `All` change in
`signal-spirit`) and the plan for the primary-side skill work.

## What the psyche decided

Per Spirit `nob8` (Decision High): [All is a complete leaf domain value
available at every level of the domain tree — the value meaning all
alternatives at that level — symmetric across querying and assignment… A
domain-based query returns, alongside the specific matches, the All-tagged
records of every parent level along the queried path… This ancestor-All
inclusion is configurable: shorthand query options expose both the
domain-based mode that folds the parent-All records in and a regular mode
that does not.]

Per Spirit `xblw` (Decision High): [The Spirit skill manual half — what
Spirit and intent are, the CLI and wire shape, how to read and query — is
generated from the spirit repository production-versioned documentation…
The capture discipline… stays primary-authored agent-conduct teaching.]

This session also retired the earlier framing that `All` is the tree
*root* (`r5yi`, superseded): `All` is a **leaf**, not an abstract trunk —
the most grounded, complete value, present at every level.

## The `All` design

`All` is one uniform construct, used identically from the root down to any
sub-level. Four properties:

1. **Leaf at every level.** `All` is a selectable, complete `Domain` leaf
   at every enum level, including the root `Domain` itself. `(Software All)`
   is a complete value meaning "all of Software."
2. **Reifies the early-stop.** Today the domain tree expresses "all of a
   sub-area" by *stopping early* — the implicit `(Software (Optional
   SoftwareLeaf))` with no leaf. `All` is the explicit, self-describing
   name for that stop: the implicit Optional stop becomes the value `All`.
   At the root, where no stop exists today, `All` is added. This unifies
   the representation rather than adding a redundant second spelling.
3. **Symmetric.** `All` works in both directions — a record may be *tagged*
   `All` at any level (assignment), and a query may *request* `All` at any
   level.
4. **Ancestor-All matching, configurable.** A domain-based query returns,
   alongside the specific matches, the `All`-tagged records of every parent
   level along the queried path. So the top-level `All` maxim surfaces for
   any specific domain query, and an intermediate `All` surfaces for any
   query beneath it. Whether the ancestor-`All` records are folded in is
   configurable per query, with shorthand options for the domain-based mode
   (includes them) and a regular mode (does not).

The payoff: a maxim tagged top-level `All` always comes out of a
domain-based query, because top-level `All` is a parent of every path. No
special top-level rule — it is the per-level construct applied at the root.

## The change in `signal-spirit`

Today, from the deployed schema:

- `schema/domain.schema`: the `Domain` tree is `(Programming (Optional
  ProgrammingLeaf))`-style; there is **no `All` value anywhere** (the only
  `All` in the schemas is `ObserverFilter [All …]`, unrelated). Records
  carry complete leaves (`izib`); the early-stop lives only on the
  query/scope side.
- `schema/signal.schema`: `DomainMatch [Any (Partial) (Full)]`,
  `Partial DomainScopes`, `Full DomainScopes`, inside the eight-field
  `Query`.

So this is net-new, in three parts:

| Part | Where | Change |
|---|---|---|
| `All` leaf at every level | `domain.schema` | Name the level early-stop `All`; add `All` at the root `Domain`. The generated tree carries `All` as a terminal at each node. |
| Record-side assignment | record `Domains` field + guardian | A record's domain may terminate at `All` at any level. |
| Ancestor-`All` matching + shorthands | matcher/engine + `signal.schema` | Domain-based query folds in `All`-tagged records of every parent level; expose shorthand query options for domain-based vs regular mode. |

The deployed `spirit` daemon (0.16.0) must be rebuilt and redeployed before
any record can be tagged `All` — the live guardian rejects an unknown
domain. Schema-operator owns the `signal-spirit` change and the daemon
cutover; this is a clean break (no production wire contract to preserve).

## Consistency with existing domain intent

The `All` design was shaped to fit, not break, the recorded domain
principles:

- `izib` (VeryHigh) [subdomains mandatory to a leaf; no Some/None exposed] —
  upheld: `All` is a valid terminal leaf, and it is precisely the
  self-describing form of the "no None exposed" stop.
- `2rb7` [domain names self-explanatory] and `ywua` [grounded subjects] —
  `All` carries its meaning in its name.
- `081i` (VeryHigh) [matching is structural nesting + scope-prefix] — the
  ancestor-`All` fold-in is the one behavior beyond pure prefix nesting;
  flagged here as an intentional matcher rule for the operator, not an
  accident.
- `qr5o` [the taxonomy is broad-routing; leaves earn routing load] — `All`
  earns its place as the universal/maxim routing target.

## Sequencing: the first `All` record is the maxim

The reason this work exists: an essence-level maxim that must surface
everywhere. Once the daemon ships `All`, record this under top-level `All`
at **Maximum** importance (it is the explicitly psyche-elevated founding
axiom):

> [The work aims at the best possible shape — the one than which none better
> could be made — and beauty is the criterion that knows it is done: if it
> is not beautiful it is not finished, and ugliness is evidence the problem
> is still unsolved.]

The intent-discipline half ("intent is primordial; inferring is forbidden")
is deliberately *not* a maxim record — per `xblw` it is Spirit-manual
teaching, which lives in the repo docs / skill, not duplicated as an intent
record.

## Related track: Spirit-skill sourcing (`xblw`)

The current `skills/spirit-cli.md` + `skills/intent-log.md` bundle two
kinds of content. The decision splits them:

- **Manual** (what Spirit/intent is, CLI + wire shape, how to read/query) →
  generated from the spirit repo's production-versioned docs into a
  read-side skill, so it tracks the deployed binary and is never a
  hand-maintained duplicate. This also realizes the read-only-vs-capture
  modular split: a read-only agent loads only this.
- **Capture discipline** (the Spirit gate, certainty/importance ladder,
  affirmative framing, when-not-to-record, maintenance) → stays
  primary-authored agent-conduct teaching beside the other behavior skills.

Consistent with `k4i3` [skills are tight self-contained teaching, cite
nothing external]: generation is a build-time relationship; the produced
skill stays standalone.

## Open implementation choices (operator)

- Exact generated representation of the `All` terminal in the emitted Rust
  enum tree (a per-level unit variant vs. a generator-level construct) —
  `izib` says the generator owns the internal representation.
- The concrete shorthand query verbs for domain-based vs regular mode,
  alongside the existing `PublicTextSearch` shorthand (`sn1g`).
- Whether `Full`/`Partial` `DomainMatch` semantics need adjustment, or the
  ancestor-`All` fold-in is a separate query flag.
