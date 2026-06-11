# Spirit redesign — session recap (insights and decisions)

A simple synthesis of what this session established. Report **590 is now the aligned
implementation spec** for this model (`Software` nested under `Technology`, equivalence-only,
taxonomy schema); report **589** is the build-state snapshot. This recap is the reasoning
behind both.

## Decisions, in one table

| Decision / insight | Spirit record |
|---|---|
| The intent layer holds **intent** (directives, wants, decisions), not **information** (a belief/fact with no directive behind it) | `qjrf` |
| Recompile is cheap; **zero-downtime is the goal** — a daemon's vocabulary grows by recompile-and-redeploy, not runtime config | `uuh7` |
| **Software nests under Technology** — "software is a kind of technology" is made structural by the tree, not a relation | `2msx` |
| Cross-domain relations are **symmetric equivalence only**; directional **subsumption is dropped** | `2msx` |
| **Domain names are self-explanatory** — meaning lives in the variant name; no gloss/annotation layer (rename if unclear) | `2rb7` |
| Relations + the enum live in a **first-class taxonomy schema** (a new, reusable schema kind), not ad-hoc data | `mn3k` |

## The domain model — three pieces, one relation

The big evolution this session was settling how domains relate. The answer is three plain
mechanisms, only one of which is a "relation":

1. **The tree carries *is-a*.** Software nests under Technology
   (`Technology(Software(Cluster(Leaf)))`). The hierarchy is the structure. This deepens the
   densest branch to four tiers — density-proportional depth (`4wt3`), the deepest branch
   being the most-used one.
2. **Scope prefix-matching carries *breadth*.** A `DomainScope` is a prefix at any depth;
   matching it returns everything beneath. Ask for `Technology` → get all of it including
   software; ask for `(Technology Software)` → just software; ask for a leaf → just that.
   Breadth comes from *where you point in the tree*, not from a relation.
3. **Equivalence (the one relation) carries *synonymy*.** Two domains in different branches
   that name the same subject retrieve together, both ways — e.g. hardware-networking ↔
   software-networking, or `Information(Database)` ↔ the database leaf under software.

**Why subsumption died.** A one-way "broader pulls narrower" link fired in the noisy
direction (a `Technology` sweep would flood with ~200 software domains) and did nothing for
the query you'd actually run. Nesting then made it not just flawed but *unnecessary* — the
tree + scope-matching already do its job, correctly. Equivalence is the only relation that
earns its place.

**Why no glosses, no rename.** A gloss ("Technology means hardware") is a convention, and a
convention enforces nothing — the live store proved it (below). Names must be
self-explanatory instead (`2rb7`). And `Technology` keeps its broad name precisely because
it now *contains* software, so renaming it to "Hardware" would be wrong.

## Where the relations live

A new **taxonomy schema** (`schema/domain.schema`) holds the variant tree **and** its
equivalences as one visible source of truth — promoted out of `signal.schema`, which then
imports `Domain`. The new schema-language construct declares relations *over an enum's
values*. Generated Rust = the enum + a compiled equivalence table + one `DomainScope::expand`
method that the query path and the guardian both call. It's a reusable schema *kind* —
persona-mind will declare its own taxonomy the same way (`mn3k`).

## State of the build (report 589)

- **The blessed design is essentially fully implemented on `origin/main`, not deployed.**
  Operator landed the Software branch, the guardian gate + separate decision-log journal +
  justified-mutation gating, the referent registry, and the Craft→Software migration. The
  live daemon (v0.8.1, 1398 records) is three commits behind. The gap to "live" is one
  system-operator deploy.
- **The migration is the easy part.** The Craft→Software remap already exists and touches
  only **2 records**.
- **The live store barely uses the vocabulary.** ~79% of records sit under
  `(Information Documentation)` and most of the rest under `(Governance Policy)` — software
  intent dumped in catch-all leaves because the old vocab had no home. Making the corpus
  reflect the real vocabulary is a per-record semantic re-tag (an LLM/guardian pass) —
  **deferred**. (Equivalence softens the need: a generically-filed record stays reachable if
  its generic home is linked.)

## The guardian

Mostly landed and faithful: temperature pinned to 0, the closed rejection-reason set inlined
in the prompt with definitions, a typed retry, the gate covering every live-arrow write, and
a *separate* append-only decision-log database. **Residue:** a few-shot example block, and
retrieval completeness — which the equivalence-expansion delivers for free (the guardian
sees records across synonym boundaries, so it catches cross-boundary duplicates).

## Method insights (meta)

- **A convention enforces nothing.** Only two things enforce a domain boundary: *structure*
  (which variants exist, and now the tree shape) and *the guardian* (semantic, and only if
  told the rule). This is why we chose structural nesting over glosses/conventions.
- **Intent vs information** (`qjrf`) — the same filter applies everywhere: a durable-sounding
  statement with no directive behind it is information, and doesn't get captured.

## Open / next

1. **Deploy** `origin/main` + run the migration (system-operator). The single gate to live.
2. **Align report 590** to this nested model (Software under Technology, equivalence-only) so
   operator implements from a clean spec. Pending.
3. **Technology's internal structure** — with Software a deep cluster under it, keep the
   hardware leaves flat (`(Technology Energy)`, sparse → shallow) beside the Software cluster?
   Lean: yes, mixed depth is density-proportional. Decide `Networking`/`Automation` (hardware
   leaf + equivalence vs absorb into software).
4. **One residual link** — `Knowledge(Computing)` ↔ `Software(Theory)`: equivalence or keep
   separate. Lean: keep separate.
