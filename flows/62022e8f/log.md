# Flow 62022e8f — design: Protos datom ethos anatomy and syntax

Aspect: design.
Skills loaded: design, spirit, psyche, flows, subflows, psyche-interraction, behavior.

## About

Remember e8c4cc61 in detail and all vision on Protos, datom, ethos, Nexus, sema, Signal; focus with the psyche on the Protos datom ethos implementation (anatomy) and syntax design.

## Remembered
- Remembered: e8c4cc61 — depth 1 in-flow (log.md, all vision/*.md, last model response and last psyche message from the transcript); depth 2 via subflow (full transcript, Datomizable page, skill drafts, open-question list). Most relevant: the settled kind chain (Text.[ Prospective<Protos> ]; Protos.[ Prospective<Datom> Prospective<Ethos> Textualizable ]; Datom/Ethos Embodied); Embodied = alias of Sized, Situation for "context", Structure replaces Portion, Structural returns the protos structure recursively; `;` comment; space inside brackets; outer `{}` omitted in ethos files; sweet file = sugar for a value of a type (name wanted); Signal file = head [imports] [requests] [responses]; Library file = head [] [types] [kinds] [associations]; inline type declaration and variant-named-as-type (inventory pass); Datomizable raised to vision; three skills (protos/datom/ethos) drafted, held for approval; last flow answer (associated kinds: Nexus yes, Prospective no; spacing: brackets only, `[]` when empty) unanswered by the psyche.
- Distilled Vision read in-flow: highLevelView, protos, datom, ethos, ethosMonolith, nexus, flowNexus; raw: signalIsOurMessagingLayer, Intent/protosParsing.
- Observation: the harness places this session's task outputs under session 67cd2f5c-…; the scratchpad path names 62022e8f-…. Short id taken from the scratchpad path (same anomaly e8c4cc61 recorded).

## Witnessed (subflow C, code read + probes, 2026-08-30)
- Local checkouts: protos 0.14.0 (1 behind remote), datomic 0.7.1 (`datom` dir is the same clone; 3 behind), ethos-zero 0.1.0 local (14 behind; remote head "Derive value semantics for data-only unit enums"), orchestrate 0.25.0 local (1 behind, dirty), signal-orchestrate 0.17.1 (2 behind, dirty). No remote commit after 2026-08-29 11:30 UTC on any of 14 repos — codexCorrection still unlanded.
- Protos parser today (protos/src/lib.rs): comment is `;;` (lib.rs:1169-1184), not `;`; separators `.` `!` `:`; structural `{}` `[]` `<>` `«»`; opaque curly quotes and `( )`; integers/decimals via ScalarAnatomy; `Portion` enum {Headed, Enclosed, Bare}; traits Delineatable, Embodiable (assoc type Embodied), Embodied: Sized {from_portion}, Textualizable, ShapeDefined; `Prospective<T>` is a type alias of Text<T> (lib.rs:106). Absent: Structure, Structural trait, Situation, Meaning, Datomizable, a Protos/Ethos/Datom type.
- datomic: trait `Datomic` (embody/portion/textualize), not Datomizable. ethos-zero: library only (no binary, no nexus); reads `Schema.{v}` / `Interface.{v} Channel.{…}` headed files, outer `{}` not required, headerless rejected; `Channel` still required; emits Rust via syn/quote incl. trait decls and `carries::<T>()` association checks.
- pgrep found no orchestrate-nexus, yet `orchestrate 'Observe.Locks'` answered with lock 19 (01a0433a) — how the CLI answered without a daemon is unknown (possible: different process name; a socket served otherwise).

## Remembered (subflow A, e8c4cc61 transcript at full depth)
- Proposal status ledger (psyche-ruled yes): prospect capability; Prospective<Sized> then Embodied=alias of Sized; `:` no-self receiver; sweet file = sugar for a value of a type (EthosFile name rejected); file = one sweet Ethos or full datom; Structure (name), Structural (name); Situation; a second `{` syntax for complex kinds (psyche-originated, line 807). Never answered: the Ethos type map (Library/Signal/TypeDeclaration/VariantDeclaration/KindDeclaration…); the KindDeclaration spec and the four-section order [superkinds] [associated kinds] [associated values] [capabilities]; Structure's inner anatomy (Enclosure, Arity, Head, Shape, Context); emitter output; "no associated kind on Prospective, yes on Nexus"; braces spacing; `[]` when empty; Fault vs Error (psyche asked "why are we using Fault instead of Error?" — Fault is a 04db2fd2 agent coinage; flow recommended Error; unruled).
- Skill drafts: protos/datom/ethos last shown together at transcript line 772; psyche's only responses: no Embodiable (Embodied = alias of Sized), protos skill too deep into dialects; datom and ethos drafts uncommented. Redrafted protos at line 793 uncommented.
- Open-question lists: flows/b675f3d9/reports/capabilityAnatomy.md §6 (11 questions on capability anatomy) + Datomizable page §10 (6 points).
- Flow coinages a reader may mistake for the psyche's: Shape, Datomic (as a kind), Fault, Textualizable, Context (as a type — psyche said the word is wrong), KindDeclaration/AssociatedKind/AssociatedValue/KindReference/TypeExpression/PortionDeclaration, the capability names shape/situation inside Datomizable.
- Recovered and logged into e8c4cc61 (annotated): complex-kind `{` syntax (vision/kinds.md); code blocks with comments (vision/designPractice.md).

## Remembered (subflow B, raw vision across flows)
- Remembered: 04db2fd2, 2ef42163, db97561c, b675f3d9, ac1e9ec8, 01a03eda, 01a04339, a5587095, 06196cc7, ba906ae2, 6863ef19, 2b34fafa, aa4c7747, f426777b, fd301d9a, e06e4c07, 55d18f4f, 5abf3be8, 01a03d6e, acbb6006, 4d5fc7da — depth 1 (via subflow, raw vision on Protos/datom/ethos/Nexus/sema/Signal). Most relevant to the drafts: "Re datom kind: Datomic" (04db2fd2) predates Datom-as-type; "all our components speak signal, not datom; datom is only used at the edge" (ac1e9ec8); "no tuple in the code we design" (aa4c7747, cff271af); "Observed.Locks.[] good enough for now" (01a04339); "datom doesnt support omittable fields yet" (4d5fc7da); integer canonical form approved (01a03eda); "Processable<[Clonable Sendable] Serializable>" (b675f3d9); stream as a fourth section (5abf3be8, streamSection) absent from the 2026-08-29 Signal anatomy; imports `/` blessed 2026-08-07, `:` on the 2026-08-29 page.
- The "six unruled datom atoms" are never enumerated anywhere; the phrase comes from db97561c's audit of the Codex port (01a04a30 authored Boolean, integer, finite decimal, String, Vector, guillemet Map, Option, positional anatomy). Inference only.
- Distillation candidates with no Vision/ counterpart (2+ flows): Signal (6 flows, strongest), nexusTraits (4), ethosInterfaces (4), kind syntax (3 + e8c4cc61), ethosSourceFiles+importResolution (2), Portion/Structure (2), Sema (4, thin).

## Dispatched
- Subflow A (read-critical): e8c4cc61 transcript at full depth — every syntax/anatomy proposal and status, skill drafts, open questions, unlogged psyche words.
- Subflow B (read-demanding): all raw vision across flows/*/vision, notion, psyche-raw on Protos/datom/ethos/Nexus/sema/Signal not in Vision/; distillation candidates.
- Subflow C (read-demanding): witness of protos/datomic/ethos-zero/signal/sema/orchestrate repos — versions, parser acceptance, which kind names exist, ethos-zero file form, commits after 2026-08-29 11:30 UTC, running nexuses.

## Instructions
- Psyche (typed, 2026-08-30): re-infer the protos, datom, ethos skill proposals adjusted for the newer psyche. Three drafts presented in-flow for approval (not written anywhere); five assumptions put to the psyche: Error over Fault; braces spaced like brackets; Datomizable capability names form/situation (flow-named); Embodied alias mechanism left out of the map; Structure inner anatomy shown minimally.
- After subflow B: two draft amendments — `Generated.{ Files.Vector<RustFile> }` (no tuple struct); datom description drops "in a payload" (datom is edge-only).

## Settled

(none yet)

## Open

(none yet)
