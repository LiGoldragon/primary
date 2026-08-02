# Codex Dispatch: Protos MVP Slices 1-3 — 2026-08-02

You are the ProtosEngine implementation agent. This package covers beads
`primary-vq6.1`, `primary-vq6.2`, `primary-vq6.3` — the critical path of
the MVP epic `primary-vq6`. Work them in order; each ends in a green e2e
witness wired into `nix flake check` before the next begins. Claim each
bead (`bd update <id> --claim`), close with proof
(`bd close <id> -r '...'`). The boot contract is
`/home/li/primary/AGENTS.md`; Rust doctrine per your role packet;
standards in `/git/github.com/LiGoldragon/standards` (traits are the
first pass; implementations under named traits with site-noted
exceptions; multi-field tuples forbidden).

## Read first (in this order)

1. `reports/EthosDotosSyntaxPrimer-2026-08-02.md` — the syntax rules
   you must not violate.
2. `reports/spiritEthosFixtures/` — the three psyche-reviewed fixtures
   (`interface.ethos`, `nexus.ethos`, `sema.ethos`) plus
   `Walkthrough.md`. These are the goldens; their text is
   psyche-reviewed and you do not change it. If a fixture proves
   unimplementable as written, STOP and report — the fix is a psyche
   conversation, never a silent fixture edit.
3. `reports/ProtosMvpDeepDesign-2026-08-02.md` — the MVP design, gap
   register, and engine inventory (sections 3-4 name your exact
   insertion points).
4. `design/ProtosEngine/*-2026-08-02.md` — the seated rulings: file
   structure (header-imports-body), non-repetition, no-tag, delimiter
   semantics, name-first-standalone rejection, parsing method.

## Slice 1 — `primary-vq6.1`: header-imports-body codec

In `core-ethos`: replace the single hardcoded `TypesOnlyRootRecord`
entry point with a composite root — header (`Kind.Version`), imports
object, kind-selected body — using a two-phase parse where the header's
kind selects the body root type through the existing
`AddressedStructuralTable` multi-rule dispatch. Add the WholeEthos item
vocabulary the fixtures need: struct declarations, trait declarations
with method signatures (positional params, last-position return,
explicit `Unit`), operator applications (`Stream.Name.{...}` — decode
as application nodes; no Stream semantics yet), interface body
positions (inputs/outputs/refusals/types), nexus positions
(types/traits), sema positions (record types/families as
`table.{Record Key}`). Imports parse and are retained textual-only.

Laws that are failure criteria: no per-file-kind parsing code (a new
kind must cost a root type plus at most a simple trait impl); no field
names; version mismatch and unknown kind are typed refusals.

Witness: all three spirit fixtures decode to typed WholeEthos and
re-emit byte-identical; goldens in the repo's `nix flake check`.

## Slice 2 — `primary-vq6.2`: trait/struct vocabulary to compiling Rust

Across `core-logos` and `rust-logos` (and `core-nomos` transformers):
add `Struct`, `TraitDef` (methods: name, positional parameter types,
return type; receiver implied — emitted as `&self`), and `TraitImpl`
(with associated-type bindings) to WholeLogos and the projection; Nomos
structural transformers for nexus-file trait and type declarations.
Emission differs by file kind: Interface types carry the wire
attributes (rkyv 0.8 little-endian/32-bit/unaligned, per the existing
WireAttributes macro); Nexus types are plain. Method names project
lowerCamel-to-snake_case as an assembly spelling decision.

Witness: `nexus.ethos` generates Rust that compiles in a
slice_one-style scratch crate (traits `SignalAdmission`,
`AgentGuardian`; decision enums), green in flake check.

## Slice 3 — `primary-vq6.3`: offline generator binary

Formalize the `language-engine-witness` `slice_one` wiring (decode ->
transform -> WholeLogos -> Rust emit) as a batch entry point: a thin
binary or library function linking the nomos-engine machinery,
invocable from `build.rs` and Nix derivations with no daemons and no
sockets. Typed refusals for header version/kind mismatches surface as
build errors. Keep the daemon path untouched.

Witness: the CLI takes each fixture and emits `.rs`; a scratch crate
builds the nexus output; a Nix derivation invokes it; all in flake
check.

## Hard stops

- Fixtures are psyche-reviewed goldens: never edit to make tests pass.
- No six-slot anything; the clean cut is ruled — do not read, bridge,
  or reference the legacy form.
- No output-identity allocation outside the translator; slices 1-3
  involve authored identities only.
- Stream semantics (chain-binding evaluation, family templates,
  StreamOpen/StreamEvent emission) are slice `primary-vq6.6` — in
  slices 1-3, `Stream.Name.{...}` only needs to decode/re-emit as an
  application node.
- The universal traits' home is ruled: the `protos` crate. Slices 1-3
  need at most forward declarations there; full seating is
  `primary-vq6.5`.
- No fixpoint machinery; dependencies form a DAG; cycles refuse typed.
- Version bumps per the versioning discipline; land producer-first,
  conclude worktrees Merged, release claims.

## Reporting

One morning-style report in `reports/` when the three slices land (or
when blocked): landed heads and versions, gates with counts,
`[assumption]` labels at sites for any provisional choice, failures
honestly, and ranked psyche questions only where a real gate was hit.
Note beads closed with proof.
