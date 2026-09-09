# Flow 564f55 — landing the approved distillation

Session: https://claude.ai/code/session_0199mTWBDkRm53xFVmZuMFqp

The living approved the proposal on 2026-09-09 ("Okay, then the
proposal is good, and land it all"), as presented in the final
"## Vision / ## Intent / ## Housekeeping" message and amended by the
later exchanges: string not text everywhere, the migration statement
dropped, the error example without parentheses, the named-type
variants split into two statements each with a complete Library root,
every declared struct and enum bearing both derives with aliases
inheriting, the datom derives conditional on a `datom` feature, and
the careful wording about `Protos` being a type that lacks meaning.

## Vision written

- `Vision/protos.md` — rewritten. New statements: Layers; Every layer
  carries its own context; Kinds are borne by the type converted and
  named for the layer it becomes; Signal is parallel; Delimiters;
  String, escape, error. Superseded and removed: Direction (the
  incorporate/corporate chain), Delineation, the old Layers table.
  Rewritten: Structure (its type is the `Protos` enum; the guillemets
  are no longer the map's), Multi-pass (the extent sentence dropped,
  extents now being a fact every `Protos` node carries), Canonical
  print (guillemets, not curly quotes), What Protos knows.
- `Vision/datom.md` — rewritten. New statements: A datom is a form at
  a path; Strings; The datom composes, the type states its positions;
  Any Rust type; From text and back; Containers; Errors; Omittable
  fields. Name absorbs the library name datom-codec and the ruling
  that Datomic names the layer abstractly, not the code. Nature loses
  "Datom is a kind, not a type; the kind is Datomic". Syntax, De/
  serialization and Meaning rewritten for guillemets, `String` and
  composition. "Repository and migration" became "Repository", the
  library naming folded into Name.
- `Vision/ethos.md` — rewritten. New statements: Why Ethos; Roots;
  What a declaration turns into; Inline types; A variant named as a
  defined type carries that type; A variant may declare its payload
  inline; Every declared type bears both kinds; The datom kinds are
  compiled in only where text is spoken; Shapes and placement; Kinds
  are explicit, bodies are hand-written; Generation. Superseded: the
  old Generation statement, the old Types statement (tuple structs,
  unnamed positions), the file-root enum of kinds/types/signal/sema
  variants. Every ethos example is now a complete root with its
  sections labeled by comment; every `Text` became `String`.
- `Vision/signal.md` — new. Name; What signal is; Query and response;
  Text and signal; Meta signal; Universal signal.
- `Vision/sema.md` — new. What sema is.
- `Vision/nexus.md` — added A kind of thing; The nexus core; Library
  and daemon; Universal traits first; Processing is for the effect;
  Documents. "A Nexus is the whole" lost its Nexus Core sentence,
  superseded by The nexus core. "Everything is a Nexus" became "Why
  everything is a Nexus" with the approved wording.
- `Vision/flowNexus.md` — added Starting flows.

## Intent written

- `Intent/anatomy.md`
- `Intent/conversion.md`
- `Intent/context.md`

## Sources appended

`Vision/sources/protos.md`, `datom.md`, `ethos.md`, `nexus.md`,
`flowNexus.md`; new `Vision/sources/signal.md`,
`Vision/sources/sema.md`; new `Intent/sources/anatomy.md`,
`conversion.md`, `context.md`.

## Archived

Whole-file moves to `archive-` beside the source:
`flows/4d5fc7da/vision/datom.md`, `flows/1a6ca4/vision/datom.md`,
`flows/1a6ca4/vision/nexus.md`, `flows/01a05487/vision/nexus.md`,
`flows/db97561c/vision/nexus.md`, `flows/aa4c7747/vision/ethos.md`,
`flows/e8c4cc61/vision/ethosTypes.md`,
`flows/b675f3d9/vision/ethosMonolith.md`,
`flows/f426777b/vision/ethosSourceFiles.md`,
`flows/f426777b/vision/nexusTraits.md`,
`flows/55d18f4f/vision/signalIsOurMessagingLayer.md`,
`flows/564f55/vision/protos.md`, `nexus.md`, `sema.md`, `signal.md`.

Entry-level moves, the rest left raw:
`flows/fd301d9a/vision/nexusTraits.md` (3 of 5 moved; the mandatory-
traits duplicate and the execution-engine excerpt left),
`flows/6863ef19/vision/signalIsOurMessagingLayer.md` (2 of 3; routable
signal left raw), `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`
(6 of 8; input-versus-output and the shape-table question left raw),
`flows/62022e8f/vision/designPractice.md` (2 of 6),
`flows/564f55/vision/datom.md` (19 moved; Rust-not-rest and the two
value-layer entries left raw as the housekeeping said),
`flows/564f55/vision/ethos.md` (9 of 11; the nomos/logos pair left
raw).

## Destroyed

- `flows/da223f/vision/datom.md` — relayed rewrite sentence.
- `flows/84eb1e/vision/ethos.md` — the same relay.
- `flows/acbb6006/vision/nexus.md` — two approval directives.
- `flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md`.
- `vision-raw/workingSpiritNewEthosSyntax.md` — the overnight
  authorization and its extension.
- Four skill-draft feedback entries in
  `flows/f426777b/vision/skillDesigning.md`; the protos-philosophy
  heading kept.
- Two Rust-fact exchange entries in `flows/564f55/vision/datom.md`
  ("you cannot call a method on T" and its neighbour, the CLI's
  Potential of Request).
- Seven heading-only files: `flows/ac1e9ec8/vision/datomSkill.md`,
  `flows/01a02fd5/vision/nexuses.md`, `flows/01a03d6e/vision/nexus.md`,
  `flows/98fbfa47/vision/metaSignalNotOptional.md`,
  `vision-raw/nexus.md`, `vision-raw/ethosNamespaces.md`,
  `vision-raw/ethosSourceFiles.md`.

## Notes on fidelity

- Every statement was landed as approved. Where an approved example
  was a single ethos line, it was expanded into a complete root with
  its sections labeled by comment, as the living required; where the
  approved line referred to type names it did not define (LockId,
  LockName, FlowId), those aliases were added to the types section so
  the root stands complete. The Sema example keeps only its imports
  and record-type sections, since the rest of Sema's shape is
  undecided.
- `flows/564f55/vision/designPractice.md` was left raw: its two
  entries were distilled into the psyche-distillation and
  psyche-interraction skills by a separate landing, not into Vision.
