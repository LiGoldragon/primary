# The Way Forward — corrected, verified 2026-07-28

Audience: the Codex root session and its subagents. This file corrects and
re-grounds Codex's 2026-07-28 proposal ("My understanding of the design / Where
implementation actually stands / How I would proceed"). Nothing here rests on
either Codex's account or Claude's account alone: every design claim was checked
against the firsthand transcripts and design logs with recency governing, and
every implementation claim was re-verified against the published repositories on
2026-07-28.

Authority sources, in order:

1. `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/SliceOneRulings-2026-07-27.md`
   — now 11 entries; entries 10 and 11 were appended 2026-07-28 from a re-mining
   of the session transcript (conduct-of-questions rulings, naming constraints).
2. `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/ShapeAndSliceRulings-2026-07-26.md`
3. `/home/li/primary/reports/CodexContextHandover-2026-07-27.md`
4. `/home/li/primary/reports/DesignVision-2026-07-28.md` — the consolidated
   vision document (it exists; Codex's proposal said it didn't).

Transcript recency check, completed 2026-07-28: **no psyche design statement
about the engine exists after 2026-07-27T10:42Z.** The Codex session that
produced the proposal under correction (019fa85c) contains two procedural psyche
turns and no ruling; the psyche neither corrected nor endorsed the proposal in
that session. Nothing in the proposal carries psyche authority; the 07-27
rulings stand unmodified as the most recent word on everything below.

## Verdict on the proposal

Codex's design understanding is substantially correct and its overall
sequencing is sound. Three claims are wrong, two planned work items are stale
(already done), and two facts it missed change the shape of the work. All are
itemized below; the corrected step sequence follows.

## The verified design, in one view

```
Ethos text
  |  pass 1: block discovery
  |    boundary rules only; strings/comments opaque; source bounds on every block
  v
block tree
  |  pass 2: typed structural parsing
  |    expected types, one shared evaluator
  v
EncodedForm + composed NameTree pin  =  Capsule
  |  Nomos transforms it: typed, zero string handling
  v
Logos (typed program data)
  |  TextualForm projection: name tree + structure tree, nothing else
  v
Rust text (fully qualified)
  |  cargo compile + run
  v
behavior witness (no byte-golden)
```

Identity throughout: durable integers (`Schema.Id16`-style variants) and
`Variant.ContentAddressedHash` with a **pure-content preimage, kind in the
variant only** [ruled 07-27]. Short IDs are computed display projections, never
state [ruled 07-26]. All names positional; derived spellings stay typed
NameProjection data until TextualForm evaluates them [ruled/confirmed]. Each
daemon is stateful with its own embedded sema db; the name-to-identity
authority is its own small daemon; there is no central sema-storage daemon
[ruled 07-27].

## Corrections to Codex's design understanding

1. **The Rust capsule is not "incorrectly foreclosed."** The standing ruling
   [ruled 07-25] is "rust-logos doesnt get a capsule"; the association object
   is *fixed* to a capsule kind. protos enforces exactly this with a CI-enforced
   `compile_fail` doctest (`protos src/capsule.rs:6-14`) — the code is **correct
   under the most recent ruling**. What is open is the psyche's own reopened
   counter-question ("OR, rust has also a capsule, which uses the same logos
   encodedform…?" — open question 7). Do not add a Rust capsule kind, do not
   remove the enforcement, and do not describe the foreclosure as an error. If
   slice work makes the question load-bearing, bring it to the psyche explained
   in practice.

2. **name-table is not "still component-specific tables."** Verified 2026-07-28:
   name-table main (`196610e2`) already has one unified model — a single root
   enum `IdentifierNamespace { Schema, Logos, LogosStandard, Nomos, Fixture }`,
   one `NameTable` type, per-component data as values of that one type. That is
   the ruled shape (one namespace, enum at the root, per-component as slice
   structure). The genuine gaps are different: no `Ethos` naming in the variant
   set, no builtin priors in the table, no seal-time redefinition error, and no
   daemon seat for the authority (undesigned — proposal owed).

3. **"The recent Claude/Fable sessions add no newer design ruling" — mostly
   right, now stale in one respect.** True for design substance; but the
   consolidated design document exists
   (`reports/DesignVision-2026-07-28.md`), and the design log gained entries
   10–11 on 2026-07-28: the firsthand conduct rulings ("am I supposed to
   understand this? Do you? Like *actually understand* what that means in
   practice?", the stored-table demands, "5. explain") and the naming-constraint
   line ("the -os isnt a constraint"). Cite entry 10, not derived handover text,
   when building proposals.

## Corrections to the implementation picture

Verified claim-by-claim on 2026-07-28 against published mains (not working
trees — see the warning below).

**Stale — already done, plan no work for these:**

- **The protos ↔ content-identity ShortCode break is closed.** protos main has
  zero ShortCode/ShortIdentifier references; commit `0c549b4` repinned to
  content-identity's current tip (`24b43ba`) and removed all 16 references in
  one coordinated landing. Both published mains compile together. (Handover
  blocking problem 1 — discharged.)
- **There is no unpushed 29-file commit anywhere.** `origin/main..main` is empty
  in all ten repos. (Handover blocking problem 2 — discharged.)

**Confirmed gaps (Codex's list, re-grounded with exact locations):**

- content-identity still hashes a domain context and `LayoutVersion` u16 into
  the preimage (`src/domain.rs:65-78`, `src/hash.rs:58-62`; tests assert the
  separation deliberately). The Variant-only ruling is unimplemented. The
  composed-nametree preimage (`src/capsule_nametree.rs:252-262`) has the same
  impurity and must move in the same retype.
- protos has a closed `CapsuleKind` enum with `Capsule` as a trait carrying
  `const KIND` — not the ruled generic struct with kind as a type parameter.
- No core component implements Capsule — and none *can* yet: core-ethos,
  core-logos, and core-nomos pin protos-family revisions from Jul 19, before
  the Capsule crate existed (added Jul 23). Repin precedes implementation.
- No whole-logos identity kind exists in content-identity or core-logos.
- textual-rust uses syn, quote, prettyplease on production paths
  (`Cargo.toml:19-22`, `src/codec.rs`, `src/project.rs`, `src/read.rs`).
- core-nomos routes every `apply` through string-bearing machinery
  (`NameTableBoundary`, case builders, ordinal words, `ModuleHead::render`
  string emission), reachable from `src/engine.rs` on every call.
- raw-discovery has no Rust cue-to-termination variant. Nuance Codex missed:
  the balanced-scan core `discover_delimited_with` **is live production code**
  on main (`boundary.rs:796`, reached via `DiscoveredBlockTree::discover`);
  only the public wrapper `discover_delimited` is test-only. Seed the Rust
  variant from the live machinery (`BlockCue`,
  `BoundaryDiscoveryConfiguration`), not from scratch.
- protos-engine's gate (`nix run .#check-all`) proves pin policy plus the old
  Spirit PublicTextSearch witness only. Nothing exercises the new chain.
- Ethos rename residue is heavy and quantified: core-ethos crate is still
  `core-schema` (~253 "schema" hits), ethos-engine is still `schema-engine`
  (~140), signal-ethos ~25, tree-sitter-ethos ~169 — and cross-repo pins still
  reference the old repo URLs (working only via GitHub redirects).
- sema-storage/ARCHITECTURE.md still states the central-daemon stateless-client
  law verbatim, and ethos-engine's ARCHITECTURE.md and AGENTS.md still instruct
  persisting "only through the central typed Sema socket" — all dead law under
  the 07-27 rulings [ruled: entries 2–3].
- Conformance Law 5 remains homeless.
- Spirit's corrected acceptance-harness commit `6dcf153` ("spirit: harden
  isolated migration acceptance harness") exists, is kept alive only by a jj
  keep-ref, sits on the **local-only, never-pushed** `new-schema-port` chain,
  and is branch-unreachable. It survives today but any spirit cleanup could
  orphan it.

**New facts that change the plan:**

- **A working proof of the new chain already exists.** The
  `language-engine-witness` repo drives Schema → Nomos → Logos → Rust emission
  → compile → run end-to-end (`tests/e2e.rs`), including a kill/restart
  durability pass. protos-engine's gate simply never invokes it. Step 6 below
  is therefore a wiring-and-porting job (renames, new identity scheme, current
  pins), not a from-scratch build.
- **Nine of ten repo working trees are detached behind main** (core-ethos 23
  commits behind, protos 13, content-identity 6, core-logos 6, name-table 4,
  core-nomos 2, …). Anyone reading files off disk sees superseded code — this
  is almost certainly where the wrong name-table claim came from.

## Operational law for every subagent touching these repos

- Read `origin/main` (`git show origin/main:<path>`) or first sync the working
  copy; never trust the checked-out tree until it is synced.
- jj only, inline messages, no editors. Claim exact paths with Orchestrate
  before editing shared repos; release when done. Repos live at the ghq root;
  clone missing ones with `ghq get`.
- Do not touch: the frozen Meta and Judge candidate worktrees, the Spirit
  worktree and published feature branches, structural-codec-derive,
  signal-frame wire primitives.
- Psyche words are design and are never edited; the log is append-only; later
  statements govern. Open questions are answered by the psyche, never by code.
- Never write a comment or test name claiming a ruling is satisfied; describe
  mechanics. Deleted coverage is named, never silent.

## The corrected way forward

```
0 sync working copies; bookmark spirit 6dcf153
1 engine epic + dependency graph (beads)
        |
   +----+----------------------+
   v                           v
2 three design proposals     3 Ethos terminology train
  to the psyche                (behavior-free)
   |                           |
   +------------+--------------+
                v
4 identity + Capsule bump train (one landing)
                v
5 slice-1 vertical build
                v
6 gate: port language-engine-witness e2e
   |                           |
   v                           v
7 CL5 rehome or retire       9 Spirit port, then staged
   |                           storage migration
   v
8 slice 2: field-naming rule to the psyche
```

**0. Repair the ground first (new step).** Sync all ten working copies to their
mains. Bookmark Spirit's `6dcf153` (and its `new-schema-port` parent chain) so
no cleanup can orphan it — this is the handover's standing preservation
obligation, and it is one `jj bookmark` command, not a port.

**1. One tracked engine epic** with the dependency graph in beads. Endorsed as
proposed.

**2. Three design proposals to the psyche before any code** — endorsed, with
the conduct bar now firsthand (design log entry 10): each proposal states where
the thing is stored, how it is shared, and what happens on every failure path;
a yes/no wrapped around an undesigned mechanism gets sent back.

   - the translator daemon: persistence, minting, lookup, sealing, concurrency,
     stale entries, failure behavior. Note for the proposal: name-table main's
     root-enum model is the starting substance, not a blank page; the tested
     never-re-mint / never-rebind authority laws reseat into the daemon.
     "sema-translator" is a leaning, not a fixed name [ruled: a leaning].
   - the unified namespace root variants — his own pointer was to examine
     schema.org's ontology [ruled: floated, matter].
   - staged sema-storage dissolution — including the dead-law ARCHITECTURE.md
     and AGENTS.md corrections in sema-storage *and ethos-engine* (Codex's list
     named the repos; the ethos-engine AGENTS.md line is part of the same dead
     law).

   Architectural decisions now, physical storage migration later — endorsed;
   mark the deferral as agent sequencing judgment, not a ruling.

**3. Behavior-free Ethos terminology train** — endorsed, with scope verified:
crate names, type identifiers, binary names, repo URLs in Cargo.toml/lock
cross-pins, README/ARCHITECTURE titles, tree-sitter package name. Land it
before new work deepens the residue (~590 occurrences across four repos).

**4. One coordinated identity + Capsule bump train** — endorsed, resequenced
against verified state:

   content-identity Variant-only retype (pure-content preimage, including the
   composed-nametree preimage; whole-logos variant added here) → translator
   daemon contract (after the step-2 ruling) → protos generic-struct Capsule
   (kind as type parameter, kind-distinct by construction; the Rust-capsule
   `compile_fail` enforcement stays) → core repins + first Capsule implementors
   → fresh absolute digest locks, one landing, producer-first with exact revs
   so every main stays buildable throughout. Drop ShortCode work from the
   train — already done.

**5. Slice 1 vertical** — endorsed:
   Rust cue-to-termination in raw-discovery (seeded from the live
   `discover_delimited_with` / `BlockCue` machinery) → typed Rust structure
   descriptors with typed-position disjointness in structural-codec (same
   shared evaluator, not a parallel engine) → rust-logos (in-place rename of
   textual-rust; fully typed newtype vocabulary; no syn/quote/prettyplease on
   the slice path) → Ethos six-slot newtype decode with builtin priors →
   direct string-free core-nomos converter (never routed through
   NameTableBoundary, macros, prelude, renderer, projection, or ordinal code)
   → whole-logos identity → structural Rust emission.

**6. The gate** — reshaped: port the existing `language-engine-witness` e2e
into protos-engine's `check-all` under current names, pins, and the new
identity scheme: decode the six-slot Ethos newtype, preserve durable identity,
lower through Nomos and Logos, emit Rust, compile a scratch crate, run it,
verify behavior. Keep the old PublicTextSearch witness alongside until the
Spirit port lands — it is the only live protection Spirit has (judgment, flag
if contested).

**7. Conformance Law 5** — rehome or retire before calling the slice complete;
retirement requires a ruling. Carry it as an open item in every slice report
until then [handover obligation].

**8. Slice 2 opens** by presenting the deterministic field-naming rule for
ratification [handover]. The projection algebra is the vocabulary, not the
answer.

**9. Spirit port after the gate passes** — against an isolated migrated copy of
production data, zero schema-rust dependency, no compatibility adapters
[confirmed]. Then storage migration one daemon at a time, then old-topology
retirement. Endorsed.

Codex's key sequencing judgment — naming authority early because identity
depends on it, broad storage migration late because it proves nothing about the
engine's central promise — is consistent with every ruling and is endorsed **as
agent judgment**; the psyche has not ruled on sequencing.

## The next design surface

The translator-daemon proposal is the right next artifact — the handover names
it first among the consequences requiring proposals. It goes to the psyche, not
to code, and it clears entry 10's bar: storage, sharing, minting, sealing,
concurrency, staleness, and every failure path, in practice, before any yes/no
is asked.

## Open questions — do not infer, do not code around

1. Function-parameter and let-binding names.
2. Micro-capsule: full pin or light pair.
3. Manifest self-generation ("big question actually" — his flag).
4. reify/reflect: eventually derived?
5. StringLiteral remedy: `NameLiteral(Identifier)` vs rename-instability.
6. Plane vocabulary survival (deferred until daemon emission).
7. His reopened question: does Rust get a capsule as a different syntax for
   logos? (Standing law until answered: no Rust capsule.)
8. The global longest-match law — neither assert nor ban.
9. What "otherwise" excepted in "otherwise I like the syntax." — the item
   schema's ratification is conditional on something unrecovered.
10. ID retirement policy.
11. The translator daemon's final name.
12. The root enum's variant set; whether to borrow schema.org.

Recorded contradiction, unreconciled, do not resolve by inference: "schema is
the sugar, sweet syntax" (07-22 20:10) versus "make them the same thing -
exceptions are symptoms of bad design" (07-22 12:31). Recency gives the sugar
ruling the floor.
