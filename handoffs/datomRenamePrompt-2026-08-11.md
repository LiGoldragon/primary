# Realizer dispatch: the datom rename (2026-08-11)

Printed by Designer session 012fbf07; the psyche pastes this into the
Realizer flow. Pasting it is the approval to execute, including the
deletion it names.

WITHDRAWN 2026-08-11T17:35+02:00 — never pasted, never executed.
The psyche ruled: "we don't need to worry about the old repo. We're
just going to move forward and migrate everything to datum [Datom]."
The fresh datom repository stands; dotos/nota stays behind. See
psyche/Vision/threeStacks.md and psyche/Vision/datomSyntax.md
2026-08-11 entries. Do not paste.

```
Realizer — the datom rename, one cut.

You are Athena, the realizing aspect, in a fresh flow. Load as
primordial, valid for the whole session: tenets, psyche, management,
beads, repository-lifecycle, version-control, nix-workflow.

Bead: primary-xqb.8.1 in primary — bd show it first; track all work
and evidence there.

Ruled ground (psyche/Vision/threeStacks.md 2026-08-11 entries and
psyche/Vision/parserIsTheParser.md — do not reopen):
- "datom is just a renamed dotos" — the Datom repository is the
  existing dotos repository renamed, history carried. Rename, never
  delete-and-recreate.
- The fresh LiGoldragon/datom repository created 2026-08-11 is
  unnecessary and is deleted; salvage nothing from it unless it adds
  proof (its code is itself a dotos port; its round-trip witnesses
  may be carried over if they add test coverage).
- De/serializer rulings, carried as context — no codec rework in
  this cut: schema-driven positional reading; decode directly into
  typed Rust structs, no intermediate document tree; no
  self-describing tags in the text.
- The parser is the parser: nothing else implements Datom parsing.
- Datom does not generate Rust (Ethos does). Zero Cargo or Nix edges
  from datom into frozen repos.

First verify which checkout is the authoritative dotos — the estate
report (reports/ThreeStacksCurrentState-2026-08-10.md) flags
name/package mismatches: a checkout named nota exports package dotos
v0.10.0, and a stale archived nota also exists. The authoritative one
carries the 2026-08-04 syntax revision (bead primary-xqb.1). Verify,
then rename: repository, package, and identifiers
Dotos/DOTOS/dotos -> Datom/DATOM/datom.

Finish line: LiGoldragon/datom is the renamed dotos repository with
its history, flake-green, tests passing, package and identifiers
renamed; the 2026-08-11 fresh repo is gone; consumers of the old
dotos package are not migrated in this cut — record each consumer
found as a comment on primary-xqb.8.1.
```
