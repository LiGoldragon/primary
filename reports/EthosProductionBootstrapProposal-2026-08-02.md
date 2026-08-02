# Ethos Production Bootstrap Proposal — 2026-08-02

Psyche goal [psyche-verbatim, condensed]: "attain a working ethos syntax;
used in a component in production to produce the public interfaces and
traits of components in production, even if parts of the design are left
for later (data evolution engine, etc), so I can see and use the language
in production, and so we can have a real test surface to keep developping
against."

This proposal charts the shortest honest path to that goal: Ethos authored
in real files, generating the public interface surface (types and
contracts) of a production component through the new engine train, wired
into the component's real build. Written by the manager; decisions below
marked as questions are the psyche's.

## 1. Why this is close

Verified today (audit of the overnight work, all claims confirmed):

- The types-only Ethos root reads through the shared structural codec
  (`core-ethos` 0.23.0) — one brace-delimited types block, no tags, no
  empty slots. The file-kind law makes adding a kind cheap: a new root
  type plus at most a simple trait implementation.
- The Nomos train runs end to end for authored declarations:
  TextualNomos decoding, structural transformers, WholeLogos, Rust
  projection (`core-nomos` 0.31.0, `core-logos` 0.20.0, `rust-logos`
  0.20.0, `signal-nomos` 0.6.0, `nomos-engine` 0.6.0), all green.
- `signal-domain` already generates production Rust from an authored
  source file at build time (the legacy six-slot path), so the production
  wiring pattern exists.
- The seven ScopeOf contract traits exist handwritten in
  `signal-domain/src/scope.rs` — a perfect reference to generate against.
- The trait standard is ruled: traits are always the first pass; they are
  the spec in code. Ethos authoring the spec layer is exactly aligned.

## 2. The one genuinely new surface

Ethos has no contract (trait) declaration form and no method-signature
form. Types (newtypes, structs, enums) are covered; the public interface
of a component is types **plus contracts with method signatures**. That
syntax is the new design work, and it is small — everything else is
plumbing an existing train.

Candidate surface for psyche reaction (manager construction, following the
positional, non-repetition, and known-type-at-position laws; NOT ruled):

```ethos
{
  Scope.ScopeOf.Domain
  ScopeContainment.Contract.{
    contains.{Scope Bool}
  }
  ScopeOverlap.Contract.{
    overlaps.{Scope Bool}
  }
}
```

Reading: at a declaration position, `Name.Contract.{...}` declares a
contract; each member is a method signature `name.{...}` whose positions
are the parameter types with the **last position the return type**; the
receiver (Rust `&self`) is implied by contract membership and never
written; reference-ness, borrowing, and dispatch (`&`, `dyn`, `impl`,
monomorphization) are assembly decisions made by the Nomos object —
Rust-is-assembly. A parameterized contract names its parameter contracts
per the generics-are-traits ruling.

## 3. Proposed slice, in order

**Phase 0 — rulings.** The four questions in section 5. Nothing starts
until the syntax question (B) has at least a reviewed fixture.

**Phase 1 — fixture first, so the psyche sees the language.** Author the
complete interface file for the first target as a fixture — **spirit**
first (its domain fixture and schema lineage already exist and its
revival is in flight), then mind, orchestrator, messenger. Each fixture
carries the daemon's public message types and contracts in the interface
file kind. Psyche reviews the authored text itself — the fastest see-it
moment, before any engine work. Iterate until the fixture reads right;
the reviewed fixtures become the golden sources.

**Phase 2 — engine work (codex dispatch).** Add the interface file kind
as a root type over the shared machinery (no per-kind parsing); extend
the item vocabulary and Logos payloads with contract and
method-signature carriers (Logos stays fully explicit); add the Nomos
structural transformer(s) emitting Rust trait declarations; extend the
rust-logos projection. All identities in this slice are authored, so the
translator-only identity gate (morning-report question 2) is never
touched. No ScopeOf transformation, no recursion, no generated symbols.

**Phase 3 — production seating in the four target daemons.**
Psyche-ruled first targets
(`design/ProtosEngine/ethosProductionFirstTargets-2026-08-02.md`):
**spirit, mind, orchestrator (former orchestrate — rename rides this
train), messenger (former message — same)**. Each daemon's interface
`.ethos` file generates its public types and traits in the real build
(same pattern as today's schema generation). Witness per component: the
generated surface is API-equivalent to the current handwritten public
surface (exact witness proposed by codex). Then flip authority: the
generated interface becomes the source, handwritten code keeps the
implementations falling under the generated traits — spec in code,
generated from Ethos. The two component renames land with this train,
slated-rename pattern as with NOTA to Dotos.

**Phase 4 — integration.** Advance the language witness and the
ProtosEngine root pins for the new train coherently (this touches the
integration boundary of morning-report question 8 and needs the psyche's
go at that point). From here every future syntax change has a live
production test surface: the fixture suite, the witness, and a real
component consuming the output.

## 4. Deliberately deferred

- Data evolution engine (seated as design; no implementation here).
- Operational editing daemon as source — files remain the ruled bootstrap.
- ScopeOf realization, generated-output identity, recursion under the DAG
  law (questions 2 and 3 stay open; their gates stay in force).
- The complete Logos output family for ScopeOf (question 4).
- Migration of the six-slot `domain.schema` types — see question A: the
  recommendation sidesteps rather than bridges, so the legacy path keeps
  producing what it produces today until migration is separately ruled.
- Impl declarations in Ethos (question D recommends out of scope).

## 5. Questions for the psyche

**A — Pipeline and canonicity.** Recommendation: the new interface file
kind runs on the new train only, and the six-slot `domain.schema` path is
left untouched for now — no bridge, no adaptation, no dual authority over
the same content, because the new file kind carries new content (the
contracts) that the legacy path never produced. `primary-pjm`'s
types-migration question stays open and becomes its own later phase.
Confirm, or rule instead that types migrate off six-slot in this same
slice.

**B — The contract and signature syntax.** React to the section 2
candidate: `Name.Contract.{...}` members as `method.{Params... Return}`,
last-position return, receiver implied, assembly details owned by the
Nomos object. Corrections at any level welcome, including the shape being
wrong root-and-branch; the fixture in Phase 1 is where the syntax gets
seen whole before implementation.

**C — First seating scope: ANSWERED.** Psyche-ruled: first targets are
spirit, mind, orchestrator (former orchestrate; rename on this train),
and messenger (former message; same). Seated in
`design/ProtosEngine/ethosProductionFirstTargets-2026-08-02.md`. The
manager's proposed order within the train — spirit first, then mind,
orchestrator, messenger — stands unless corrected.

**D — Impls and visibility.** Recommendation: impl declarations are out
of scope — Ethos generates types and contracts; implementations remain
handwritten Rust falling under the generated traits. And in the interface
file kind everything is public by default with no `Public` literal (the
non-repetition law upgrade of the audit's noise finding). Confirm both,
or pull impl declarations into scope.

## 6. After the rulings

Codex receives a dispatch extending `handoffs/codex-catchup-2026-08-02.md`
(or a dedicated package): Phase 1 fixture support work if any, then
Phase 2 engine work gated on the reviewed fixture, with the standing hard
stops unchanged. Beads track the phases; the morning-report cadence
reports gates and any new psyche questions the work surfaces.
