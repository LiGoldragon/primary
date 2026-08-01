# Atomic Operation Editing, True-Name Identity — 2026-08-01

Rulings from the psyche vision session, correcting the manager's
generated-output identity framing.

## Ruling 1: same true name, same thing

Agent text answered: the manager proposed that two byte-identical generated
helpers "share a true name... while keeping two distinct encoded names,"
a git-blob-style dedup reading.

Psyche ruling [psyche-verbatim]: "if two things have the same true name,
they are the same thing"

Seated: identity IS the content address. Byte-identical content is one
thing, referenced from however many places. Divergence happens only when a
later operation produces different content — a different thing with its own
true name; the slot/encoded layer records which lineage went where. There
is no two-encoded-names-one-true-name dedup model.

## Ruling 2: the atomic operation editing model

Psyche ruling [psyche-verbatim, condensed]: "the real model is a
single-edit operation, through an operation-interface (signal message),
which will naturally create a vcs. 'single-edit' doesnt necessarily mean
only a single object is affected. I should say atomic edit (one operation;
it either works and goes through or doesnt and doesnt change anything)...
all the 3 engines hold the encoded form in slots, with the associated
change log (which gives us vcs)"

Seated meaning:

- The three engines hold the encoded form in **slots**. The encoded name's
  continuity is the slot's continuity.
- Every change enters as **one operation through the operation interface**
  (a signal message). An operation is **atomic**: it applies in full —
  including every cascaded effect, e.g. regenerating transformer outputs
  whose sources changed; many objects, one operation — or not at all.
- The **change log** of operations per engine is the version control
  system. VCS is not layered on top; it falls out of the model.
- Consequence [agent-inference, accepted by the psyche's framing]: there is
  no re-run continuity-matching problem for generated outputs. A generated
  object's slot is created by the operation that first produces it and
  edited by operations that change its sources. Continuity is structural,
  not inferred. The earlier "continuity judgment" question is void.
- This concretizes the transactional-editing horizon
  (threeLayerNamingAndNomosBootstrap-2026-08-01.md section 4): text files
  are bootstrap; the engine's slots plus change log are the source.

## Open: terminology

The psyche requested terminology proposals and research for this
"atomic / structural / operation-based" editing paradigm. Research
commissioned (prior art: event sourcing, operational transformation,
Unison's content-addressed codebase, Smalltalk image + changes log,
Datomic transaction log, patch theory). Manager candidates offered,
undecided: Greek family names for the operation (Praxis — deed; Metabole —
change; Ergon — work) with the log as the natural plural chain; English
alternatives (operation, transaction, patch; "operation-sourced structural
editing" for the paradigm). Nothing ruled.

## Appended, later same day: terminology ruled — plain English

Agent text answered: the research report's recommended Greek set
(Praxis for the operation, Mneme for the log;
`reports/OperationalEditingPriorArt-2026-08-01.md`).

Psyche ruling [psyche-verbatim]: "im not looking for exotic names. plain
english engineering terms."

Seated: the Greek candidates are withdrawn. The vocabulary is the psyche's
own dictation, unchanged: **operation** (the atomic unit), **operation
interface** (the signal-message entry), **change log** (the per-engine
record that is the VCS), **slot** (the encoded-form holder), and
**operational editing** (the paradigm, his 07-29 phrase). Exotic naming
remains reserved for the language family (Ethos, Nomos, Logos, Protos,
Dotos); engineering machinery is named in plain English. The prior-art
survey's substance (Unison, event sourcing, log-structured storage,
projectional editors; git vocabulary to avoid) stands unaffected.
