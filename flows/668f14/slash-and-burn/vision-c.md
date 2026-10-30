# vision-c sweep: candidates for destruction

## orchestrate
6 statements kept vs 1 candidate (statements counted: 7)

> A flow reserves its whole write set with a Lock before editing a shared path and releases it when editing ends; a flow's own directory is written freely, because only that flow writes there. A lock whose holder is live is messaged; a lock whose holder has no live flow and no live pane may be released by any flow, with the holder and its paths recorded.

procedure: lock/release/steal protocol belongs in the orchestrate skill (knowledge-orchestrate), not belief. The first sentence is common sense; the second (steal rules, "no live pane", recording) is mechanics. Harm 2.

## persona
5 kept vs 1 candidate (6 counted)

> It makes backups. It knows how to restart the whole cluster, every metaflow, with the right context. It runs the monitors, and when something has failed or a provider is offline it may act, moving to a backup model.

too specific: enumerates duties and a fallback mechanic (moving to a backup model) of a service not yet pinned; a feature list, not common sense. Harm 1.

## proposal
Kept 9 vs candidates 8 (statement count 17)

> A code block in a proposal stands on its own: it is shown without a path, directory or file name. It carries the code, why it is important, and what its function is.

not common sense: arbitrary rule (hide the path) that contradicts a sensible reader's wish to know where code lives; also conflicts with book-making's "repo > path" headings. Harm 3.

> The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.

too specific: file layout and archival mechanics. duplicate: vision-book says the same sentence. Harm 2.

> A line removed from a module is shown beside the line that makes it unnecessary; the compensation module is leaned out first, because vision replaces it.

duplicate: vision-book has the identical sentence. Also too specific (compensation-module ordering). Harm 2.

> A question between alternative lines shows each alternative as its own proposal, with the exact lines it lands; the living rules land, amend or reject.

duplicate: vision-book. procedure of presentation. Harm 1.

> A proposal in the chat shows the whole section as it would stand, with the part that changes in bold.

procedure: display convention; dead weight against book rendering (red/green). Harm 2.

> ```mermaid
> flowchart TB
>     a["his vision"] -- "is made into" --> b["a proposal (the proposal module's rules)"]
>     b -- "is rendered as" --> c["a book (the book module's rules)"]
>     c -- "is shown to" --> d["him"]
> ```

stale: refers to "the proposal module"/"the book module" as separate rule sets; restates a pipeline the prose already says. Harm 1.

> A proposal names the model that created it and, for each model that
> helped, what that help was, on a subtitle line under the title. Created
> by Fable, research by Opus, data retrieved by Sonnet.

too specific: subtitle-line format and model names; ceremony that spends attention. Harm 2.

> Every word of his redoes the proposal it bears on, unless it closes the topic; words that open a topic of their own get a proposal of their own.

duplicate: vision-book last paragraph (as "book"). Harm 1.

## protos
Kept 14 vs candidates 14 (28 counted)

> Protos is only about structure. It understands
> only form: the syntactic structure. What
> anything is, the conceptual layer says. A head in protos is just a head — anatomy, not interpretation. Pure anatomy is only structural recognition of structures, nothing more. Protos examples show the
> textual structure — the delimiters, the head, the capitalization, the
> recursive structure — universally, at a very high level,
> non-dialect-specific.

duplicate: says "structure only" four ways; the last sentence is a rule about how examples are written. Harm 1.

> Four layers, text above and the value below: the textual layer; the
> protosic layer, whose root type is the `Protos` enum; the conceptual
> layer, which is the datomic, ethosic, logosic, or nomosic layer
> according to the language; and the compositional layer, the
> composition, the value put together in memory, the densest form.
> Going down, the information gains density and strictness; going up,
> visibility. Each step converts into a wholly different type, and
> nothing of the previous step is used after it.

Wanted design (kept). Only candidate: none; listed for completeness as kept.

> ```rust
> // protosic: an enclosure of two bare runs, each structure at its extent in the text
> Protos::Enclosed(Braced, vec![Protos::Bare("Ada"), Protos::Bare("1990")])
> ... (the whole layers example block)
> ```

duplicate: the Delimiters section repeats the same Protos::Enclosed / Datom::Struct example. Keep one. Harm 1.

> The extent, where a structure sits in the text, is a fact of the protosic
> layer, and every `Protos` node carries one. The path, where a datom
> sits in its tree, is a fact of the datomic layer, and every datom
> carries one, read down from text or built up from a composition
> alike. The budget, how much reading one act allows, is a fact of the
> reader and lives on it. The composition carries no position: it is
> the layer where context has been consumed. An
> error's locus is the datom's path, and its extent
> is found by following that path into the protos the reader holds.

too specific: machine detail (extent, path, budget, error locus) of one implementation; design not yet common sense; a model implementing would infer it. Harm 2.

> | type | kind | becomes |
> |---|---|---|
> | text | `Protosizable` | protos |
> ... (whole Kinds table)

too specific: trait-name table; duplicates the impl block directly below. Harm 2.

> ```rust
> impl Protosizable  for String { fn protosize(&self) -> Result<Protos, Error>; }
> ... (whole impl block and the `let text = person.datomize(...)` line)
> ```

too specific: exact trait signatures, `Budget`, `ARITY`, `Positions` — implementation detail that belongs in the crate. Harm 2.

> Signal is not a layer of the chain: a parallel structure exchanging
> compositions in one step, an rkyv serialization carrying our own
> protocol.

duplicate: signal.md "What signal is" ("one step from the composition, beside the text chain"). Harm 1.

> Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every glyph
> content; `( )` reserved for meaning, its type unspecified, read by
> balance as opaque until it is. The curly quotes are not delimiters.
> Every structure of the protosic layer is a variant of the `Protos`
> enum, and none of them means anything on its own: whether an
> enclosure is a struct or a vector, whether a bare run is a name or a
> number, is said by the conceptual layer that reads it.

too specific: the delimiter set is syntax design (keep as owner design) but "curly quotes are not delimiters" and "read by balance as opaque until it is" are one-off mechanics. Harm 1.

> ```rust
> Protos::Enclosed(Braced, vec![Protos::Bare("Ada"), Protos::Bare("1990")])   // structure: an enclosure of two runs
> Datom::Struct(vec![Datom::Bare("Ada"), Datom::Bare("1990")])                // meaning: a struct of two positions
> ```

duplicate: repeats the Layers example. Also `Datom::Struct` conflicts with the earlier `Datom { path, form: Form::Struct }` shape (inconsistent). Harm 2.

> A headed structure is a head, a separator and a body. The separators
> are period, exclamation and colon. The body is written right after its separator.

too specific: separator list and spacing rule, one-off syntax detail; stale if the grammar is changing. Harm 1.

> The head is a symbol. The body is
> another structure. Heads may be daisy-chained: different separators
> too.

too specific: restates the previous definition in smaller words. Harm 1.

> A brace-enclosed structure's arity is anatomical;
> a bracket-enclosed structure's arity is not. Angle brackets are a
> real protos delimiter. The key-value map, which the guillemets once
> delimited, is dropped entirely from protos and its dialects.

stale: "once delimited ... dropped" describes history; "angle brackets are a real delimiter" is a patch against an old doubt. Harm 2.

> The text type is `String`. A closing guillemet inside a string is
> escaped with a backslash, so the ascent never refuses. The word is
> error, through the chain.

too specific: backslash escape and "the word is error" are per-case mechanics; "so the ascent never refuses" is unclear. Harm 2.

> ```
> «she said \»no\» and left»
> ```

too specific: one-off example of the escape rule. Harm 1.

> Multiple passes are wanted over a single pass, because a single pass
> creates corner-cutting bad design. The multiple steps create a mental
> model of the machinery, which enforces a correctness in the code that
> is millions of times more beneficial than the cost of doing these
> multiple passes.

not common sense: an unsupported quantified claim ("millions of times") that sounds like an argument to win; overlaps spirit-core's correctness-layer belief (duplicate). Harm 2.

> It is canonical, and it is considered good style, to leave a space
> between the delimiters and the content, except inside the guillemets,
> where every glyph is content and a space would be load-bearing. Space
> the delimiters and the inner content.

too specific: formatting rule the printer enforces; last sentence repeats the first. Harm 1.

> Datom is a protos dialect, carrying only
> pure typed data; it does not take part in the multi-pass
> rust-generation engine that ethos, nomos and logos are slated to
> become, but it shares the protos style. The final fully-decomposed
> engine with three daemons is the protos engine.

stale/too specific: "three daemons", "slated to become" describe a plan about names not yet built; "fully-decomposed engine" is unmotivated. Harm 2.

## psyche-aspect
Kept 4 vs candidates 2 (6 counted)

> Psyche core keeps track of all the psyche and passes each matter to the topic flow it belongs to.

duplicate: restated in the next two sections ("keeps track of all the psyche within Psyche", "decides what reaches a topic flow"). Harm 1.

> Psyche core keeps track of all the psyche within Psyche; a topic Secondary packages what it observes for its own Primary, which answers its Secondary, which reports to core.

procedure: routing chain Secondary/Primary/core as a mechanic; confusing loop ("Primary answers its Secondary, which reports to core"). Harm 2.

## psyche
Kept 8 vs candidates 6 (14 counted)

> Psyche reaches through its hierarchy to Orchestrate coordinates. Unprefixed
> vision is Psyche's most reliable, accepted gold. These statements are approved
> by the living in the native desktop record at
> `flows/8393ca/vision/operational-herdrVoiceAccess.md` (archive ordinal 1833).

too specific: names a flow id, a file path and an archive ordinal; first sentence is garbled ("reaches ... to Orchestrate coordinates"); provenance of one acceptance event. Harm 2.

> Psyche data belongs in a dedicated repository symlinked into Primary. Primary
> Next begins from Primary's root commit and carries selected repository mounting
> points plus a README and AGENTS.md explaining those relationships. Orchestrate
> coordinates concurrent work across those repositories.

too specific: symlinks, "Primary Next", root commit, README/AGENTS.md — repo-layout detail and a one-off project. Harm 2.

> The belief modules belong in a context repository; Psyche's is psyche-belief.

too specific: names one repository. Harm 1.

> This accepted Vision describes a target shape. It does not authorize a data
> migration, repository creation, history rewrite, or broad archival operation.

procedure: a disclaimer addressed to a one-off migration; a model reads it as a ban on ordinary work. Harm 3.

> A raw record is written at flows/<flow>/vision/<topic>.md or
> flows/<flow>/notion/<topic>.md and is open there. When it is landed,
> superseded or refuted it moves to the same path under the flow's
> archive directory, flows/<flow>/archive/vision/<topic>.md, under one
> line that says which: Landed, with the module and the commit, written
> by the lander in the commit that lands it; Superseded, by the record
> that overruled it; Refuted, with his reason. The archived records of
> the whole system are flows/*/archive/**; the open ones are every
> record outside an archive directory. A file is never renamed to say
> what became of its records. In the long term the records live in the
> psyche nexus and the state is a field.

procedure/too specific: full paths, glob, status-line grammar, never-rename rule; belongs in the lander role (role-lander-landing). The long-term closing sentence is the only belief. Harm 2.

> Crystallized vision preserves references to its supporting raw records. Archived
> records retain their original words and provenance.

duplicate: vision-psyche/vision-crystallization say provenance is kept (per description "how crystallized vision keeps its provenance"). Harm 1.

## remembering
Kept 5 vs candidates 5 (10 counted)

> A flow's remembering includes the open beads of its address.

too specific: names the beads tool; mechanic of one tracker. Harm 1.

> The log's record of a remembering carries a short description of what
> from the remembered flow was found most relevant to the current one.

procedure: log-entry format. Harm 1.

> A fresh flow receives the living's content weighed by importance, and only the important part.

not common sense: "weighed by importance" is unfalsifiable and drops information silently; a fresh flow would not know what it is missing. Harm 3.

> ```mermaid
> flowchart TB
>     a["living content"] -- "weighed by importance" --> b["important part"]
> ... (whole figure)
> ```

duplicate: restates the preceding sentence. Harm 1.

> A launch names how far back the new flow remembers: the raw vision and notion logs of its predecessors to a depth, or of flows named one by one. The remembering is a field of the launch; the belief modules come from the declaration, from main; the brief comes last and carries the task alone. The logs are the record.

too specific: launch-field anatomy; belongs in vision-flow / knowledge-flow. Harm 2.

> ```
> RememberingDepth.Integer
> Remembering.[ Predecessors.RememberingDepth Custom.Vector<FlowId> ]
> Launch.{ Address Remembering InstructionPrompt }
> ```

Datom-style type declaration, the owner's design: keep only if Remembering is a settled type. Marked: borderline, harm 1.

> ```
> flow 'Launch.{ { Psyche core Primary } Predecessors.2 «brief» }'
> flow 'Launch.{ { Psyche core Primary } Custom.[ 36b71b e3c8c1 ] «brief» }'
> ```

too specific: tool invocation with flow ids 36b71b e3c8c1; per-tool mechanic. Harm 2.

> A refreshed flow receives its beliefs and the raw vision and notion logs named at its launch, and those alone. The predecessor's biases end with it.

not common sense: "and those alone" forbids a flow from reading anything else, contradicting the module's first section (reach the transcript directly). Harm 3.

## sema
Kept 4 vs candidates 2 (6 counted)

> In the long term, speech-to-Sema renders a dictation as Sema; how much it adds to the bare text depends on the event and on how many channels are read.

too specific: a feature of a tool not yet designed; vague. Harm 1.

> In the far long term, Sema reads the living through as many channels and nuances as possible: the speech style of each person, learned; facial and body expression; heart rate and blood pressure; eye movement and the iris dilating and contracting.

not common sense: speculative surveillance list (heart rate, iris) that a model could act on or cite to the owner as a plan; wish-list detail. Harm 2.

## signal
Kept 6 vs candidates 4 (10 counted)

> Signal is the messaging layer: fully binary, portable rkyv fixed
> across endianness, fully typed with both sides knowing the full schema.
> It is one step from the
> composition, beside the text chain.

too specific: rkyv endianness detail; "one step from the composition" duplicates protos "Signal is parallel". Harm 1.

> A Signal declares queries and responses; input and output are too
> low-level for it.

not common sense: unmotivated naming rule ("too low-level"). Harm 1.

> ```
> Signal
> []                                     ; imports
> [ Lock.LockRequest  Release.LockId ]   ; queries
> ...
> ```

Illustrates a syntax the owner designs, but uses the Lock example (one component, orchestrate) as the only shape; keep trimmed. Borderline, harm 1.

> The meta signal is always present: the daemon is configured only over
> its meta surface.

too specific: "only over its meta surface" is an absolute rule about a particular daemon design; duplicates vision-nexus / vision-persona on configuration. Harm 2.

> Signal is portable rkyv plus whatever protocol is standardized on top
> of it. The protocol is to be decided.

duplicate: restates "portable rkyv"; the second sentence is an inquiry, not a belief. Harm 1.

## subflows
Kept 1 vs candidates 0 (1 counted)

No candidates.

## system-one
Kept 1 vs candidates 1 (1 counted, partly)

> A System 1 model puts intelligence into the system's logic: the decisions a program would otherwise hard-code are made by a System 1 model. Jev is the first.

too specific: "Jev is the first" names a one-off instance (belief ages when a second arrives). Only the final sentence; harm 1.

## testing
Kept 2 vs candidates 1 (2 counted)

> A test repository holds scenarios of components working together, each scenario in its own sandbox.

too specific: sandbox-per-scenario mechanic; belongs in vision-deployment/vision-horizon. Harm 1.

## x11
Kept 0 vs candidates 1 (1 counted)

> CriomOS should move toward operating without X11.

too specific: a single hardware/display preference, already routed by vision-criomos; arguably a decision not belief. Harm 1.
