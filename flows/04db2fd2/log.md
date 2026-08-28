# Flow 04db2fd2 — design

## About
Review of the Datom textualize/realize anatomy, then a first-principles design of protos and datom
with the psyche (2026-08-27/28), in ethos syntax. Code set aside by the psyche's word.

## Remembered
Remembered: 01a04339, b675f3d9, ac1e9ec8 — depth 1 (reports/rememberedFlows.md): 01a04339 ruled
`Observed.Locks.[]` "good enough for now", realization open; b675f3d9 kinds/anatomy/structural parsing,
distillation proposals unapproved; ac1e9ec8 datom syntax acquired, skill never started.
Remembered: b675f3d9, f426777b, aa4c7747, 5abf3be8, ba906ae2 — depth 2 on ethos kind syntax: kind =
qualifier; capability = a kind's function, written head.Concept; identity Name<…>; the handwritten
Capability enum; sections confer; types block vs kinds block (placement unruled).

## Landed
- Vision/datom.md: curly quotes default string delimiter; guillemets delimit a map, key and value
  separated by a space, positional; no Map head in expected position; a Head is always a variant;
  balance-based parenthesis rules moved under Meaning (escape rule dropped — unanswered).
- Vision/protos.md (new): Direction — text arrives prospective and leaves as a value; Realize may
  fault, Textualize cannot; spans found on the way in, computed on the way out; several passes.
- Skills (Curriculum 9e114dc6, 25bb7864): design.md rolling-distillation cadence;
  psyche-distillation.md proactive dispatch; psyche-interraction.md sole home of the psyche-record
  protocol (excerpt rule with ` ... `, no timestamps/session id, `-- psyche, STT.`/`typed.`, no
  overtalk, holding comment while subflows are out); flows.md points there, artifacts only in the
  flow's listed subdirectories, prefer the final response; subflows.md: a subflow's production is
  its final response.

## Settled design (the psyche's rulings)
- Delineate (kind Delineated; product Delineation) is the untyped structural pass; delineation is
  protos; a type's anatomy is a dialect's; pure anatomy is structural recognition only; Head is
  just a Head in protos; arity recorded for every enclosure incl. [].
- Kinds are qualifiers (Delineated, Textual, Embodied — replacing Realized; Datomic for datom);
  Rust-imposed verbs tolerated as legacy. Capabilities are a kind's functions; yields always in [];
  a fallible yield is Result<A F>; one separator per head, options mutually exclusive, ! for mutable
  self; the struct form is for complex kinds. Kind syntax as accepted:
  `Delineated.[ delineate.[ Result<Delineation Fault> ] ]`.
- Portion.{ Extent Form }; Extent once, over Span; Form.[ Headed Enclosed Bare ]; Bare.Symbol;
  Headed keeps Body.Box<Portion> (explicit box is fine); Enclosed vs Bare is enclosure, opacity a
  separate concern; opaque has no containing portion; non-opaque Enclosed holds Vector<Portion>;
  Form and Anatomy are one tree. Guillemets « », curly quotes “ ”; parentheses opaque till the first
  unbalanced closer, not yet protos.
- Text over String: normalized, hashable; a type so it can bear kinds. Datom stays a library;
  library to be renamed to free "datom" for a later nexus. Multi-pass over single pass.
- Process: separate ethos blocks for types and kinds; rolling distillation; excerpt logging; no file
  reports — talk in the flow; software-anatomy skill to come out of this work.

## Open (for the next session)
- Kind-to-type association: a bearings block (`Text.[ Delineated ]`) proposed, unruled; its name.
- Kinds block placement in an ethos interface file (sixth section?).
- Prospective as a kind on Text; Prospect.{ Text Delineation } (flow's draft, not approved).
- Datom reading rules and Fault names (flow's draft, not approved). Library name (datom-forms offered).
- Meaning escape rule. `<>` in datom.
- Rolling distillation of this flow's vision/ (datom, protos, kinds, portion, text, delimiters,
  artifacts, overtalking, psycheLogging, rollingDistillation, softwareAnatomySkill) — due.
- Realization of `Observed.Locks.[]` (01a04339) and the code gap (witnesses/datomTextualizeRealizeAnatomy.md).
