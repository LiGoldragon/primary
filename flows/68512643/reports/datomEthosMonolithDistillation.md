# Datom / ethos-monolith distillation proposal

Composed in the main flow from gathered candidate records; awaiting
the living's review. Nothing lands in `Vision/` before explicit
approval, statement by statement.

Revised 2026-08-23 after the negatives record (68512643-2, -3):
prohibitions re-articulated as the duty or assignment they protect;
the inline-data-in-Ethos road left visible in datom statement 2.

## Proposed `Vision/datom.md`

1. **Name.** Datom is the psyche's own coinage for the new data
   notation, the successor to NOTA and to the rejected name Dotos.
   The name was chosen to stick and to echo what the notation is:
   data, strictly typed, super dense, no field names.
2. **Nature.** Datom carries data only — like JSON, but strictly
   typed. Generics belong to Ethos; Datom's whole work is
   serialization and deserialization — carrying data between text
   and typed form. Generating Rust is Ethos's duty, in today's
   division of labor. When Ethos becomes the full authoring
   language, with Rustlang as its assembly layer, Datom — the data
   dialect of the Protos family — may gain an inline place in
   authored Ethos, the way Rustlang composes data directly in code;
   the division assigns present duties and leaves that road visible
   (68512643-3).
3. **De/serialization.** Schema-driven and positional: the reader
   walks the expected type, writing is the exact reverse projection,
   and decoding lands directly in the typed Rust structs. All naming
   and self-description live in the type; the text carries only the
   data.
4. **Repository and migration.** Everything migrates to Datom; the
   old stack — Schema and NOTA — stays behind, frozen, and may be
   called legacy. The repository is plain datom, with no variant
   suffix.
5. **Relation to Ethos.** Datom and Ethos are different languages
   that share an approach, not a parser. What they may share is a
   substrate — traits with a shared implementation and types; the
   universal substrate machinery is homed in protos, all dialects
   ride it, and datom is the pure-data dialect on it. Ethos depends
   on Datom, at minimum to intake data for signals; the Meaning
   context therefore lives in the datom repository, seen by both
   languages.
6. **The interface shape.** A program's configuration surface is the
   datom's shape itself, as the ethos interface declares it: a data
   enum at the root whose variants are the main operations, each
   variant's data its options. The shape already is the interface:
   datom creates the configuration options by its very shape.
7. **Syntax.** Consistency comes first: datom's syntax is fixed
   before the rest. Parentheses carry a duty — they are a major
   symbol of cognition — and are the default string delimiter,
   balance-based: interior balanced pairs are plain content
   (parentheses inside text are markup, the seed of the structured
   string), the string closes at the final unbalanced closer, and an
   unbalanced interior parenthesis is escaped. A string is written
   bare whenever the bare form can carry it, and a bare string may
   carry symbols that are load-bearing elsewhere — the machinery is
   made fit for this by the right abstraction layers. String blocks
   are opaque: interior delimiters become content until the block
   closes. A bare brace block is a struct; a
   dot-parenthesis block is a string-carrying variant. The dotted
   prefix of a delimited block is part of the block's type; its
   official name is Head; a variant always re-emits its Head when
   textualized. A map's payload is a square-bracket vector of
   key.value entries, since a map is conceptually a list of
   key/values.
8. **Meaning.** The structured super-string type, Meaning, is
   postponed so a working syntax lands as soon as possible:
   parenthesis-delimited and curly-quote text both land as plain
   String for now, with the later Meaning type marked in code. The
   eventual shape is one string type with two variants — legacy
   (curly quotes) and structured (parentheses, arbitrary depth, a
   graph of sorts). Tracked on bead primary-xqb.8.5.

## Proposed `Vision/ethos.md`

1. **What Ethos is.** Ethos is the schema language. Of the two main
   syntaxes most agents will face, Ethos specifies the types and
   Datom fills them with data.
2. **Why Ethos.** Existing text data formats and existing
   programming languages both fail. Rust is the new assembly, read
   in full by no one; Ethos is the concise, dense, cognitively
   concentrated language for writing code with AI agents — easy to
   read and write, showing the interfaces: the main types and the
   main traits. Behavior falls under traits, which creates an
   ontology in code.
3. **Generation.** Ethos generates the Rust. Rust generated from
   ethos is committed, so ordinary tooling — language servers —
   works normally; a freshness mechanism is deliberately left open.
4. **Non-repetition.** Any repetition in ethos syntax is an
   implementation failure. Ethos aims to be the most terse,
   non-repetitive syntax ever made.
5. **Self-description.** A datom object's basic CLI help emits the
   Ethos that describes its anatomy. The wanted mechanism extends
   this: point at any object — CLI now, Mentci later — and its Ethos
   prints, self-describing and self-evident. The schema syntax
   serves two audiences: it trains agents to use things properly,
   and it shows where the design is lacking.
6. **Horizon.** Ethos will eventually replace everything, Rustlang
   becoming its assembly layer. Designs are chosen for that horizon;
   what it enables — generator emission among it — comes in its
   time.

## Proposed `Vision/ethosMonolith.md`

1. **Origin.** The monolith is the shortcut stack: the incorrect
   stack's code is kept, left in place, frozen; new repositories
   carry a simplified path from Ethos straight to Rust. The earlier
   slowness came from imposing daemon-era architecture on a pipeline
   that did not need it.
2. **Name.** First named ethos-rust, the schema-rust analogue; then
   renamed ethos-monolith: it has no nomos and no logos component
   and goes straight to Rust — a monolith. The rename was authorized
   for remote and local, and dispatched.
3. **Shape.** The monolith will itself be a daemon.
4. **Purpose.** An incremental implementation and bootstrap process,
   so that ethos and datom get written and read as soon as possible,
   without cutting corners, and components start being written in
   ethos.
5. **Vocabulary carried.** The Signal, Nexus, SEMA vocabulary and
   principles are kept; nothing is bound to how they were used and
   implemented in the past. Nexus is authored in ethos so the
   daemon's main operations are visible. Sema is the database
   engine, authored in ethos so the stored types are visible; it
   matters more than nexus, because operational editing should yield
   database migration operations along with the editing operation.
6. **First fixture.** The psyche component is the first fixture: it
   holds Spirit, Intent, and Vision under a top-level layer enum,
   reuses much of spirit, and feeds the hijacked LLM calls.
7. **Readiness.** Ethos serves new work in place of legacy schema
   once the monolith is ready to use; readiness is witnessed.

## Records replaced (archived on approval)

Archive means: the record moves verbatim into an `archive-` prefixed
file beside its source file; nothing is deleted.

- flows/c6b71b4c/vision/threeStacks.md — all three records
  (2026-08-10: names confirmed and stickiness criterion; the echo
  criteria; the naming of Datom) → datom 1.
- psyche-raw/Vision/threeStacks.md — both records (2026-08-10
  shortcut-stack; 2026-08-11 migrate-everything) → datom 4,
  ethosMonolith 1.
- psyche-raw/Vision/datomSyntax.md — both records (2026-08-11
  no-generics; fix-first and parentheses fork) → datom 2, 7.
- psyche-raw/Vision/ethosDotosDivisionAndHelp.md — its one record →
  ethos 1, 5.
- psyche-raw/Vision/ethosNonRepetitionLaw.md — its one record →
  ethos 4.
- flows/a5587095/vision/threeStacks.md — its one record
  (ethos-depends-on-datom; Meaning in datom) → datom 5.
- flows/a5587095/vision/datomSyntax.md — all three records
  (parentheses must have a duty; structured-string delimiter and
  two variants; map payload) → datom 7, 8.
- flows/06196cc7/vision/datomSyntax.md — all nine records
  (Meaning postponed; block opacity; dotted prefix; unquoted bare
  strings; parenthesis default; balance-based strings; brace
  struct / dot-paren variant; Head official; head re-emission;
  load-bearing symbols) → datom 7, 8.
- flows/ba906ae2/vision/threeStacks.md — its one record (daemon;
  renamed ethos-monolith) → ethosMonolith 2, 3, 4.
- flows/bc05da32/vision/interfaceRootEnumerators.md — its one
  record (no derive; root data enum) → datom 6.
- flows/01a02a34/vision/ethos.md — both records (schema language;
  ethos-if-ready) → ethos 1, ethosMonolith 7.
- flows/01a02a34/vision/datum.md — both records (datom replaces
  dotos; use datom instead of dotos) → datom 1, 4.
- flows/01a02a34/vision/schemaSyntax.md — its one record (train
  agents; show design lacks) → ethos 5.

From flows/012fbf07/vision/threeStacks.md, these records are
replaced: the transcription correction (ethos-rust confirmed) →
ethosMonolith 2; datom-does-not-generate-Rust → datom 2, ethos 3;
generated-Rust-committed → ethos 3; the de/serializer anatomy →
datom 3; different-languages-shared-substrate → datom 5; and the
superseded renamed-dotos record (its supersession is already on
record) → datom 4.

## Records drawn from, not replaced

These stay in place because they carry subjects this pass does not
exhaust:

- psyche-raw/Vision/rustComponentArchitecture.md 2026-08-14 — the
  monolith and ethos content is carried (ethos 2, 5; ethosMonolith
  2–5), but the record also rules actors, the skills-history
  recognition, and research direction; it stays whole.
- flows/012fbf07/vision/threeStacks.md — remaining records:
  schema-old naming, no-core-split / three repos per component, the
  psyche-component anatomy, router and universal-signal repo. These
  belong to component-architecture and signal topics, not yet
  distilled. (Psyche-component-as-first-fixture is carried into
  ethosMonolith 6; the record stays for its component-anatomy
  content.)
- flows/06196cc7/vision/threeStacks.md — signal repo naming and the
  protos-repo occupancy note stay; the substrate-homed-in-protos
  ruling is carried into datom 5.
- flows/bc05da32/vision/mainFunction.md — the
  ethos-replaces-everything record is drawn into ethos 6; the file
  belongs to the software-design cluster, second pass.
- flows/a5587095/vision/rustComponentArchitecture.md — Rust-as-new-
  assembly is drawn into ethos 2; the mandatory-traits corpus stays
  for the trait topic.

## Held out of this pass

- The 2026-08-06 session 5abf3be8 syntax rulings (dot opens a
  delimiter, colon legal in string position, chained names
  scrapped, sections confer traits, stream rulings) — they predate
  the Datom naming and the 08-13/14 syntax rounds; each needs
  supersession triage before distilling.
- The tuple thread (cff271af) — live, awaiting the ruling.
- The mainFunction / assembly / worldModelBeforeCode /
  machineAnatomy cluster — its own pass, entangled with the tuple
  ruling and cff271af's pending mainFunction distillation.
- Signal/router, component anatomy, the trait corpus, protos
  substrate detail — later topics.

## Open questions for the living

1. The root-enumerator record (bc05da32 2026-08-22) says it extends
   a 2026-08-07 root-enumerator ruling; that earlier record was not
   found — psyche-raw/Vision/interfaceRootEnumerators.md is a
   title-only stub. Where it lives is unknown.
2. Datom 7 and 8 present the parentheses story's end state (balance-
   based default delimiter; Meaning postponed) across four rounds of
   evolution (08-11 open fork → structured-string delimiter →
   postponed-to-String → balance-based default). Confirm the
   reading.
3. EthosMonolith 3 states the daemon word as spoken. The built
   ethos-monolith v0.2.0 is a generator library; whether the library
   phase is legitimate bootstrap or already owes the daemon shape
   remains the open design fork — the distillation does not touch
   it.
4. Component anatomy (three repos per component, signal naming,
   router/universal-signal) is left in place — is that the next
   pass?

## Sources

- Witness: code read flows/012fbf07/vision/threeStacks.md,
  flows/c6b71b4c/vision/threeStacks.md,
  flows/06196cc7/vision/datomSyntax.md,
  flows/06196cc7/vision/threeStacks.md,
  flows/ba906ae2/vision/threeStacks.md,
  flows/a5587095/vision/threeStacks.md,
  flows/a5587095/vision/datomSyntax.md,
  flows/a5587095/vision/rustComponentArchitecture.md,
  flows/bc05da32/vision/interfaceRootEnumerators.md,
  psyche-raw/Vision/threeStacks.md,
  psyche-raw/Vision/interfaceRootEnumerators.md (this flow, this
  session).
- Witness record: flows/68512643/witnesses/datomVisionGround.md.
- Subflow gatherings (claims, relayed as claims): first gatherer
  over psyche-raw/Vision (full contents of datomSyntax,
  ethosDotosDivisionAndHelp, ethosNonRepetitionLaw,
  rustComponentArchitecture, mainFunction, structuredStringType);
  second gatherer over flows/*/vision (01a02a34 ethos/datum/
  schemaSyntax contents, bc05da32 mainFunction excerpt, quote
  attributions).
- Flows: cff271af (distillation protocol and tuple thread),
  01a02a06 (migration of records to origin flows).
