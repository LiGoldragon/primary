# Conflict-Free and Principled Merge for a Typed Event-Log Database: eg-walker, Patch Theory, CRDTs, and Per-Family Merge Policy

## Frame: the question report 92 did not answer

Report 92 surveyed general version-control prior art. This report attacks the *merge* dimension specifically, against one concrete fact about our design: **our event log already carries each change's payload/diff in a typed, hash-linked DAG.** That single fact changes which prior art is relevant. Most CRDT libraries are *forced* to store per-element conflict-resolution metadata forever because they have no separate authoritative log. We already have the log. So the family of techniques that *separate the operation log from the materialized state and rebuild merge state on demand* — exactly the 2024-2026 frontier — is not an optimization for us; it is the shape we are already in.

The research question is therefore narrow and answerable: **given a typed, DAG-structured event log per component, which merge discipline gives us branch/fork/rebase/merge with per-family policy hooks, where does merge become provably conflict-free, and where must a conflict or a guardian decision surface?**

### The central distinction this report turns on

Two incompatible philosophies of automated merge exist, and our design should consciously pick per-family rather than globally:

- **Convergence-by-construction (CRDT / patch theory).** Define the data type so that concurrent operations *always* commute to one deterministic state. There is never a "merge failed." The cost: the *semantic* conflict still exists, it is just resolved by a fixed rule (interleave, last-writer-wins, both-survive) chosen at type-design time, not at merge time. You cannot reject.
- **Convergence-by-decision (3-way merge / guardian).** Detect divergence, surface a conflict set, and run a policy to admit / reject / transform. This is the only model that can *reject* an entry — which our Spirit guardian requirement demands.

The clever move for us is that **a typed event log lets us choose per `RecordFamily` which of these two applies**, because both are just different *replay functions* over the same DAG. That is the thesis of this report.

## Patch theory: Pijul and darcs — sound, commuting, conflict-as-a-state

### What it is

darcs and Pijul model history as a **set of patches**, not a sequence of snapshots. A repository state is the (unordered) set of patches applied. Pijul is grounded in Mimram & Di Giusto's *Categorical Theory of Patches*: files are objects, patches are arrows, and **merge is a pushout** in a category constructed to *have all pushouts* — the smallest generalization of flat files for which every concurrent pair has a well-defined least-upper-bound state ([pijul.org/model](https://pijul.org/model/), [Mimram & Di Giusto PDF](https://www.lix.polytechnique.fr/Labo/Samuel.Mimram/docs/mimram_ctp.pdf)).

### How it does the thing

The decisive design choice: **conflicts are first-class states inside the data structure, not merge failures.** Pijul represents a file as a graph of byte-chunks with ordering edges; when two patches conflict, the pushout exists because the category was completed to contain "a file with two unordered alternatives at this spot." Merge is therefore **associative and commutative** — order of integration cannot change the result — and **cherry-pick is free** (a patch is the same object wherever it lands), which Git cannot offer because Git rebases rewrite identity ([pijul.org/manual/why_pijul](https://pijul.org/manual/why_pijul.html)). Crucially Pijul *differs from darcs*: in darcs conflicting changes never commute and resolution is exponential patch-commutation search; in Pijul conflicting changes *do* commute and conflict is just a graph state, giving O(log) operations.

### What is genuinely state-of-the-art here

The conflict-as-a-state idea is the durable, clever insight — and it is *older* than the CRDT formulation but isomorphic to it. The 2024-2026 CRDT frontier (below) independently rediscovered that "the merged state must be able to *represent* an unresolved conflict" rather than pick a winner eagerly.

## The 2024-2026 frontier: eg-walker (and why it is our shape)

### What it is

**Eg-walker (Event Graph Walker)**, Gentle & Kleppmann, **published at EuroSys 2025** ([arXiv:2409.14252](https://arxiv.org/abs/2409.14252)), is the most important recent result. It is the algorithm behind **diamond-types** (Gentle) and the philosophical basis of **Loro** ([loro.dev eg-walker](https://loro.dev/docs/advanced/event_graph_walker)).

### How it does the thing — and why it matches us exactly

Eg-walker **stores only the raw operations on a DAG** (e.g. `insert(pos, char)`, `delete(pos)`) — the *original description*, not CRDT metadata. It does **not** keep per-element conflict tags at rest. When a merge is needed, it **walks the event graph, builds a *temporary* CRDT in memory purely for the concurrent region, resolves positions, then discards it** ([HN/author, id=41669840](https://news.ycombinator.com/item?id=41669840)). Steady-state memory is an order of magnitude below traditional CRDTs; document load from disk is "orders of magnitude faster" because you load a snapshot, not a metadata-laden CRDT; and you "only ever need to look at historical edits when merging concurrent changes."

The replay is **bounded by the fork point**: "the algorithm only needs to look at operations as far back as the most recent 'fork point' between the two branches." Eg-walker formalizes this with **critical versions** — points in the DAG where everything before is causally before everything after — so replay never needs to start earlier than the last critical version before the divergence. This is precisely a **checkpoint that bounds replay**, which is already a named primitive in our design.

This is the single most important mapping in this report: **our "version the log, not the store; checkpoints bound replay" direction *is* eg-walker's architecture, arrived at independently.** The redb store is eg-walker's discardable materialized snapshot; the typed event log is eg-walker's DAG of operations; our Checkpoint is eg-walker's critical version.

### Verified current state of the implementations

- **Loro** — Rust core, eg-walker-based "Replayable Event Graph," supports list / map / text / **movable tree**, and ships **git-like version control primitives**: `fork`/`fork_at` to branch, `import`/`export` to merge, `checkout` to time-travel to any frontier, and **shallow snapshots** that discard old history while keeping current state ([github.com/loro-dev/loro](https://github.com/loro-dev/loro), [shallow snapshots](https://loro.dev/docs/concepts/shallow_snapshots)). Past 1.0 with a stable binary format; npm `loro-crdt` ~1.10.x, actively maintained into 2026. **Loro is the closest existing artifact to what the psyche is asking us to build** — a typed, version-controlled, fork/merge-capable CRDT database over an event graph.
- **diamond-types** (Gentle) — "world's fastest CRDT," the reference eg-walker text implementation; run-length-encoded ops + B-tree range index ([crates.io/diamond-types](https://crates.io/crates/diamond-types), [josephg.com/crdts-go-brrr](https://josephg.com/blog/crdts-go-brrr/)).
- **Automerge 3.0** — shipped 2025; re-architected to use its on-disk **columnar compression in memory**, ~10x (sometimes 100x) less RAM, load times from "17 hours to 9 seconds" on pathological docs ([automerge.org/blog/automerge-3](https://automerge.org/blog/automerge-3/)). Notably it kept file-format compatibility — it is the conservative production CRDT, not the frontier.
- **Cola** — Rust text CRDT, competitive with / faster than diamond-types upstream in its benchmark ([nomad.foo/blog/cola](https://nomad.foo/blog/cola)).
- **Yjs / Yrs** — mature, but YATA; the eg-walker author notes bugs found in published competing algorithms (YATA, Automerge) — a point *for* keeping the log as the source of truth so the resolution algorithm can be replaced without rewriting history.

## Where merge is conflict-free, and where it cannot be

This is the crux for per-family policy. The honest, verified position:

- **Sequence/text families** can be made conflict-free *if* you accept a fixed interleaving rule. But the rule matters: **Fugue (Weidner & Kleppmann 2023)** proved that *every* prior text CRDT and OT algorithm suffers **interleaving anomalies** — concurrent insertions at the same spot get shuffled into garbage — and introduced **maximal non-interleaving** as the correct property, with Tree-Fugue / List-Fugue satisfying it ([arXiv:2305.00583](https://arxiv.org/abs/2305.00583)). Loro's rich-text builds on this. Takeaway: "conflict-free" for sequences is only *good* with a 2023-era interleaving discipline; naive RGA is not enough.
- **Register/map families** are conflict-free only by *choosing a loser*. LWW silently drops the concurrent write; multi-value keeps both as a conflict set. There is no free lunch — the semantic conflict is real, you only pick who absorbs it ([lars.hupel.info CRDT registers](https://lars.hupel.info/topics/crdt/07-deletion/)).
- **Tree/move families** are conflict-free via **Kleppmann's highly-available move operation** ([martin.kleppmann.com/2021/10/07](https://martin.kleppmann.com/2021/10/07/crdt-tree-move-operation.html)): operations are kept in a log ordered by Lamport timestamp; an out-of-order remote op forces **undo of newer ops, re-apply of the old one, then redo** — pure event-log replay — and **each move is checked by a validity predicate (no cycle) at apply time and silently skipped if it would create a cycle.** This is exactly an event-log replay with a per-operation policy predicate. It is the template for a guardian.
- **Invariant-bearing families cannot be made conflict-free by construction at all.** CRDTs guarantee replicas converge to the *same* state, but **not that the state satisfies an application invariant** (`balance >= 0`, no duplicate identifier, valid reference) ([programming-group 2024 invariants paper](https://programming-group.com/assets/pdf/papers/2024_Consistent-Local-First-Software-Enforcing-Safety-and-Invariants-for-Local-First-Applications.pdf)). Two solutions exist: **(a) coordination/reservation** — escrow/bounded-counter "rights" pre-allocated per replica so each can act locally within its share (ElectricSQL Rich-CRDTs, [electric-sql.com rich-crdts](https://electric-sql.com/blog/2022/05/03/introducing-rich-crdts)); or **(b) a guardian** that runs at merge/intake time, inspects the candidate entry against current state, and **admits / rejects / transforms** it. For Spirit, (b) is the requirement.

## Mapping it all onto our typed event-log design

The unifying realization: **branch, fork, merge, and rebase are all the same operation — "replay a set of DAG events into a target state through a per-family policy function" — differing only in which events and which target.**

- **Branch / fork** = name a frontier (a set of DAG heads). Free; Loro's `fork_at` proves it. No data copied; a branch is a label on the hash-linked log.
- **Merge** = take the union of two frontiers' events, find the fork point (last common critical version / Checkpoint), and replay the concurrent suffix into the materialized redb view. The *replay function is per-`RecordFamily`*: sequence-shaped families run Fugue-style interleaving; map families run LWW or multi-value; tree families run Kleppmann move-replay-with-cycle-check; invariant families run the **guardian**.
- **Rebase** = replay one branch's events onto another's frontier through the same policy. For Spirit this is precisely "route each entry through the guardian," which admits/rejects/transforms — and because the guardian is the policy function, rebase and intake share one code path.
- **Policy as a trait, default + override** = a `MergePolicy` trait per `RecordFamily`, with a default (`ConvergentReplay`: deterministic, never rejects — for clean CRDT-shaped families) and a per-component override (`GuardedReplay`: validity predicate + reject/transform — for Spirit). The closed-sum decode we already require *selects the policy by schema-hash*, so the policy dispatch is the same closed enum the store decode already is.
- **Crypto** stays consistent: blake3 already content-addresses every event, so the DAG edges, the frontier identity, and the critical-version/Checkpoint identity are all blake3. BLS signs/attests *frontiers and checkpoints* — a merge result is a new attested frontier, and the remote ouranos mirror verifies the BLS attestation over the appended suffix before materializing. This is the version-control analog of a signed transparency log ([LegoLog 2025](https://eprint.iacr.org/2025/1234.pdf), [BLS+Merkle selective disclosure](https://arxiv.org/html/2402.15447v3)).

## What is genuinely clever for our case

The combination — not any single import — is the contribution:

1. **Eg-walker's "discard the merge CRDT" applied to a *typed, closed-sum* record store.** Every public eg-walker implementation is monomorphic (one text type, or one JSON shape). We get the same temporary-CRDT-on-replay benefit while keeping a *closed enum of typed families*, with the schema-hash selector choosing both the decode *and* the merge policy. Nobody ships this; it is the clever delta over Loro.
2. **Merge policy = replay function, so branch/fork/rebase/merge collapse to one mechanism per family**, and the Spirit guardian is not a special case bolted on — it is just the `GuardedReplay` policy instance, sharing the rebase path.
3. **Kleppmann move-replay is the proof-of-concept that "replay with a per-op validity predicate" converges** — we generalize its cycle-check predicate to an arbitrary per-family guardian predicate.
4. **Conflict-as-a-state (Pijul) gives the default policy a principled target**: when a convergent family genuinely cannot pick, the materialized view holds a *typed conflict record* (a family variant), not a crash — and a later guardian/human entry resolves it as another logged event.

## What does NOT fit our event-log shape (reject the cargo cult)

- **Operational Transformation.** OT needs a central server to impose canonical operation order and has no usable TP2 (multi-peer transform) for non-trivial types ([taskade OT vs CRDT 2026](https://www.taskade.com/blog/ot-vs-crdt)). Our design is a decentralized hash-linked DAG with a remote mirror — there is no canonical-order server, and we explicitly want offline branches. OT is the wrong family. Borrow nothing structurally; only note its failure mode as motivation.
- **Full Pijul pushout machinery as our merge engine.** The *conflict-as-a-state* insight is gold, but Pijul's specific byte-chunk-graph file model is a sequence-CRDT in disguise specialized to source code. Adopting its category construction wholesale would force *all* our typed families into a line-graph representation, defeating the typed closed-sum. Take the principle, not the representation.
- **Escrow/reservation invariant enforcement as the *default*.** Reservation (bounded counters) is the right tool *only* for numeric-threshold invariants under high-availability write load where you cannot tolerate a rejection. Spirit's guardian *wants* to reject; it is not availability-bound. Using escrow there would add a distributed rights-allocation protocol to solve a problem the guardian solves with a synchronous predicate at intake. Keep escrow in the toolbox for a future bounded-resource family, not as the policy substrate.
- **Automerge/Yjs as a dependency.** They keep conflict metadata at rest (Automerge 3 compresses it, doesn't eliminate it) and are monomorphic JSON. We want the *eg-walker idea* (separate log, transient merge state, replay bounded by critical version), implemented natively over our typed closed-sum and rkyv, not a JSON-CRDT library wedged under a typed schema. diamond-types/Loro are the *reference to read*, not the *crate to depend on*, given our rkyv-0.8 + redb + closed-sum constraints.
- **Eg-walker's worst case.** The paper is honest: when branches are deeply interleaved with no critical versions for a long stretch, replay degrades to "comparable with existing CRDT algorithms." For us this means **Checkpoints must be emitted aggressively** (at every critical version we can prove) so divergent Spirit branches never force a from-genesis replay — and shallow-snapshot-style history truncation must respect that you can no longer merge a branch that forked before the truncation boundary.

