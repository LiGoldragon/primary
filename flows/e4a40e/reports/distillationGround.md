# Distillation ground for proposal 1

Gathered by flow e4a40e. Each claim is marked witnessed (read by
this flow) or relayed (carried from another flow's account).

---

## 1. Vision files for the five topics

All five topics have a Vision/<topic>.md file. Witnessed.

### Vision/kinds.md

```
     1	# Kinds
     2	
     3	## Kind
     4	
     5	Kind is the word for the bearer of capabilities: something that can
     6	run is a runner, Runnable is its kind, and run is its capability, a
     7	function the kind has. Trait is set aside as acoustically ambiguous.
     8	In ethos there are no generics, only kinds. Declaring a new kind
     9	declares a new trait in the Rust world and might imply more in the
    10	ethos world.
    11	
    12	## Naming
    13	
    14	Kinds are qualifier-named: Runnable, Textualizable, Structural,
    15	Embodied. Run is not a kind. The verbs Rust imposes, Write and Read
    16	among them, are tolerated as legacy, for cognitive ease while Rust
    17	and ethos code are switched between so often; once ethos is the
    18	authored language that debt is removed.
```

Vision/sources/kinds.md exists:

```
     1	# Sources — kinds
     2	
     3	f426777b spokenVocabulary
     4	b675f3d9 kinds
     5	6863ef19 traitsAsCapabilities
     6	06196cc7 traitsAsCapabilities
     7	2b34fafa traitsAsCapabilities
     8	04db2fd2 kinds
     9	5abf3be8 encodedFormFingerprintTraitDesign
    10	4decf7 kinds
```

### Vision/protos.md

```
     1	# Protos
     2	
     3	## Direction
     4	
     5	Text arrives as a prospective value and leaves as a value. Realize reads the textual form into the real form and may fault: the text is prospective until it matches its anatomy. Textualize writes the real form into the textual form and cannot fault: a real value is already whole. Spans are found on the way in and computed on the way out. Each direction is several passes.
```

Vision/sources/protos.md does not exist. Witnessed.

### Vision/datom.md

```
     1	# Datom
     2	
     3	## Name
     4	
     5	Datom is the psyche's own coinage for the new data notation, the
     6	successor to NOTA and to the rejected name Dotos. The name was
     7	chosen for its energetic power and to echo what the notation is:
     8	data, strictly typed, super dense, no field names.
     9	
    10	## Nature
    11	
    12	Datom carries data only — like JSON, but strictly typed. Generics
    13	belong to Ethos; Datom's whole work is serialization and
    14	deserialization — carrying data between text and typed form.
    15	Generating Rust is Ethos's duty, in today's division of labor. When
    16	Ethos becomes the full authoring language, with Rustlang as its
    17	assembly layer, Datom — the data dialect of the Protos family — may
    18	gain an inline place in authored Ethos, the way Rustlang composes
    19	data directly in code. That road is reached, or even floated, only
    20	with explicit context: how, when, and where data yields Rust, stated
    21	without ambiguity; until then the division stands as spoken.
    22	
    23	## De/serialization
    24	
    25	Schema-driven and positional: the reader walks the expected type,
    26	writing is the exact reverse projection, and decoding lands directly
    27	in the typed Rust structs. All naming and self-description live in
    28	the type; the text carries only the data.
    29	
    30	## Repository and migration
    31	
    32	Everything migrates to Datom. Datom's own line of descent is NOTA —
    33	which also passed through the temporary name Dotos; that old
    34	notation stays behind, frozen, and may be called legacy. Schema is
    35	the abandoned ancestor of Ethos, not of Datom. The repository is
    36	plain datom, with no variant suffix.
    37	
    38	## Relation to Ethos
    39	
    40	Datom and Ethos are different languages that share an approach, not
    41	a parser. What they may share is a substrate — traits with a shared
    42	implementation and types; the universal substrate machinery is homed
    43	in protos, all dialects ride it, and datom is the pure-data dialect
    44	on it. Ethos depends on Datom, at minimum to intake data for
    45	signals; the Meaning context therefore lives in the datom
    46	repository, seen by both languages.
    47	
    48	## The interface shape
    49	
    50	A program's configuration surface is the datom's shape itself, as
    51	the ethos interface declares it: a data enum at the root whose
    52	variants are the main operations. A variant's data carries what
    53	follows: another enum where sub-operations are wanted, a struct or
    54	vector for final options — and a struct may embed further
    55	sub-operations, or any combination imaginable. Output is an enum,
    56	always — even the most basic response interface is an enum: Success
    57	or Failure. The shape already is the interface: datom creates the
    58	configuration options by its very shape.
    59	
    60	## Syntax
    61	
    62	Curly quotes are the default string delimiter. A string is written
    63	bare whenever the bare form can carry it, and a bare string may
    64	carry symbols that are load-bearing elsewhere — the machinery is
    65	made fit for this by the right abstraction layers. String blocks are
    66	opaque: interior delimiters become content until the block closes. A
    67	bare brace block is a struct; a dot-parenthesis block is a
    68	string-carrying variant. The dotted prefix of a delimited block is
    69	part of the block's type; its official name is Head; a variant
    70	always re-emits its Head when textualized. Guillemets delimit a map;
    71	inside, key and value are separated by a space, resolving by
    72	position. A map in a position that expects a map carries no Head; a
    73	Head is always a variant.
    74	
    75	## Meaning
    76	
    77	Meaning is the structured string: parenthesis-delimited, arbitrary
    78	depth, a graph of sorts, seeded by the fact that parentheses inside
    79	text are markup. Curly quotes delimit the plain string. Meaning is
    80	postponed so a working syntax lands as soon as possible: parenthesis
    81	text lands as plain String today, the later type marked in code. The
    82	name Meaning is provisional — it smells of a verb — and is reopened
    83	together with the type.
```

Vision/sources/datom.md exists:

```
     1	# Sources — datom
     2	
     3	ac1e9ec8 datomSyntax
```

### Vision/ethos.md

```
     1	# Ethos
     2	
     3	## What Ethos is
     4	
     5	Ethos is the schema language. Of the two main syntaxes most agents
     6	will face, Ethos specifies the types and Datom fills them with data.
     7	
     8	## Why Ethos
     9	
    10	Existing text data formats and existing programming languages both
    11	fail. Rust is the new assembly, read in full by no one; Ethos is the
    12	concise, dense, cognitively concentrated language for writing code
    13	with AI agents — easy to read and write, showing the interfaces: the
    14	main types and the main traits. Behavior falls under traits, which
    15	creates an ontology in code.
    16	
    17	## Generation
    18	
    19	Ethos generates the Rust. Rust generated from ethos is committed, so
    20	ordinary tooling — language servers — works normally; a freshness
    21	mechanism is deliberately left open.
    22	
    23	## Non-repetition
    24	
    25	Any repetition in ethos syntax is an implementation failure. Ethos
    26	aims to be the most terse, non-repetitive syntax ever made.
    27	
    28	## Self-description
    29	
    30	A datom object's basic CLI help emits the Ethos that describes its
    31	anatomy. The wanted mechanism extends this: point at any object —
    32	CLI now, Mentci later — and its Ethos prints, self-describing and
    33	self-evident. The schema syntax serves two audiences: it trains
    34	agents to use things properly, and it shows where the design is
    35	lacking.
    36	
    37	## Horizon
    38	
    39	Ethos will eventually replace everything, Rustlang becoming its
    40	assembly layer. Designs are chosen for that horizon; what it
    41	enables — generator emission among it — comes in its time.
```

Vision/sources/ethos.md does not exist. The ethos report notes this
as an anomaly: the earlier 68512643 distillation left no sources file.
Witnessed.

### Vision/distillation.md

```
     1	# Distillation
     2	
     3	## Vision impurities
     4	
     5	A working instruction logged as vision is a vision impurity. It may
     6	sit in a log beside valid vision; when distillation finds it, the
     7	impurity is dissected out of the log and destroyed, and the valid
     8	vision around it stays.
     9	
    10	## Impurities fall out through distillation
    11	
    12	Impurities come out in the course of distillation: a distillation
    13	proposal points out the impurities it dissects out, and the living
    14	rules on them with the statements.
    15	
    16	## A proposal names each statement's destination
    17	
    18	A distillation proposal says, for every statement, the topic it goes
    19	to; a statement under the wrong topic is corrected by a distillation
    20	edit of its own.
    21	
    22	## A statement carries what the psyche said
    23	
    24	A distilled statement carries what the psyche said and nothing
    25	beyond it. A small ruling makes a small statement.
    26	
    27	## Designing model behavior is vision
    28	
    29	Designing model behavior is vision, and a correction of an agent's
    30	conduct can be vision. The line of what counts as designing is drawn
    31	wide, and what does not qualify as vision is stated with the same
    32	clarity.
    33	
    34	## No useless negatives
    35	
    36	A distilled statement carries no useless negative. Such negatives
    37	stay in the archive, which remains linkable.
    38	
    39	## A statement never attributes itself to the psyche
    40	
    41	Vision is the psyche's; a distilled statement never says so of itself.
```

Vision/sources/distillation.md exists:

```
     1	# Sources — distillation
     2	
     3	b675f3d9 visionImpurities
     4	acbb6006 distillation
     5	b675f3d9 distillation
     6	ac1e9ec8 distillationNegatives
```

---

## 2. Other Vision files overlapping proposal 1

### Vision/ethosMonolith.md

Overlaps with proposal1/ethos.md (Horizon, Generation, and the
ethos-to-Rust relationship) and with proposal1/datom.md (the
monolith as the path that brings ethos and datom into production).
Witnessed.

Passages:

```
     1	# Ethos-monolith
     2	
     3	## Origin
     4	
     5	All our systems will be Nexuses, and the correct three-nexus ethos
     6	stack is the desired stack — but it is too complex to go for
     7	directly, and the previous effort devolved into agent hallucinations
     8	for lack of proper instructions. The monolith is the short-term path
     9	that brings ethos into production: the earlier stack's code is kept,
    10	left in place, frozen, and new repositories carry a simplified path
    11	from Ethos straight to Rust.
```

Lines 19-29 overlap with ethos Generation (monolith goes from Ethos
straight to Rust) and with datom Nature (ethos and datom get written
and read as soon as possible):

```
    19	## Shape
    20	
    21	The monolith will itself be a Nexus. Nexus by itself names our
    22	specifically designed daemon — distinct from Nexus Core, the
    23	runtime engine — and executables are named component-nexus.
    24	
    25	## Purpose
    26	
    27	An incremental implementation and bootstrap process, so that ethos
    28	and datom get written and read as soon as possible, without cutting
    29	corners, and components start being written in ethos.
```

Lines 31-38 overlap with ethos's "Behavior falls under traits" and
datom's Relation to Ethos:

```
    31	## Vocabulary carried
    32	
    33	The Signal, Nexus, SEMA vocabulary and principles are kept; nothing
    34	is bound to how they were used and implemented in the past. Nexus is
    35	authored in ethos so its main operations are visible. Sema is the
    36	database engine, authored in ethos so the stored types are visible;
    37	it matters more than nexus, because operational editing should yield
    38	database migration operations along with the editing operation.
```

Lines 40-43 overlap with ethos Generation and Horizon:

```
    40	## Readiness
    41	
    42	Ethos serves new work in place of legacy schema once the monolith is
    43	ready to use; readiness is witnessed.
```

Vision/sources/ethosMonolith.md:

```
     1	# Sources — ethosMonolith
     2	
     3	vision-raw threeStacks
     4	vision-raw rustComponentArchitecture
     5	aa4c7747 ethosMonolith
```

### Vision/nexus.md

Overlaps with proposal1/datom.md (datom as signal's edge form; the
datom nexus; datom-converting CLIs) and with proposal1/protos.md
(signal form as one of a value's forms). Witnessed.

Lines 12-18, sockets, overlap with datom's interface shape (a CLI
per socket):

```
    12	## Sockets
    13	
    14	A Nexus opens at least two sockets. The ordinary socket serves
    15	ordinary peers. The meta socket is privileged — the root user of the
    16	Nexus — and configuration and privileged operations pass through it;
    17	every Nexus has one, since without it nothing could configure the
    18	Nexus. A Nexus that needs more levels of access opens more sockets.
```

Lines 20-28, default clients, overlap with datom De/serialization and
Nature (datom as the edge form, datom-converting CLIs):

```
    20	## Default clients
    21	
    22	A client is a separate program from the Nexus. For now the default
    23	clients are packaged with the Nexus as separate crates of its
    24	repository, which is a multi-crate repository: one datom-converting
    25	CLI per socket, however many sockets the Nexus has, at least two. A
    26	default client serves bootstrap first, then debugging and testing,
    27	long after production has stopped using it. The meta CLI is named
    28	component-meta.
```

Lines 30-36, signal only, overlap with datom Nature (signal's form at
the edge) and protos Forms of a value (signal form):

```
    30	## Signal only
    31	
    32	Every client speaks to a Nexus in pure signal, fully binary. A Nexus
    33	speaks only the signal contracts it is compiled with; two of these
    34	are its own, one per socket. A Nexus thinks in typed values — enums,
    35	structs, scalars — and the string fields it still carries are
    36	records on the way to a fully typed form.
```

Line 82, Everything is a Nexus, overlaps with datom Repository
(the datom nexus):

```
    80	## Everything is a Nexus
    81	
    82	Everything built from now on is a Nexus, and what was built in
    83	another shape is rewritten as one. The consistency creates
    84	reliability and raises quality and clarity.
```

Vision/sources/nexus.md:

```
     1	# Sources — nexus
     2	
     3	e06e4c07 nexus
     4	01a03d6e nexus
     5	acbb6006 nexus
     6	98fbfa47 metaCliIsComponentDashMeta
     7	012fbf07 threeStacks
     8	15b67974 actorLibrary
```

### Other Vision files checked, no overlap found

Vision/flowNexus.md, Vision/highLevelView.md, Vision/orchestrate.md,
Vision/remembering.md, Vision/x11.md: none contain statements that
overlap with the five proposal 1 texts. Witnessed.

---

## 3. Apparatus in the composite proposal

File: flows/4decf7/design/distillationProposal1.md.

### Source-tracing apparatus

The composite proposal carries the following apparatus tying
statements to their raw sources. Witnessed.

**Header (lines 1-13):** names the origin of the proposal.

```
     1	# Distillation proposal 1 — flow 4decf7
     2	
     3	Composed in the main flow from the six gatherings in reports/, from
     4	flows/b675f3d9/reports/distillProposalProtosDatom.md and its
     5	acbb6006 addendum, and from the living's fresh words in this flow.
     6	Each statement lands only on the living's explicit approval, and
     7	each names its topic. On approval: the referenced raw records move to
     8	`archive-` files beside their sources; the fresh verbatim heard in
     9	this flow (the opening message on the practice; "kinds are
    10	qualifier-named") is logged directly as archived in
    11	flows/4decf7/vision/archive-<topic>.md; transcript-only words that
    12	no log carries are logged the same way; the sources files are
    13	appended; impurities named below are destroyed.
```

**Ordering assumption (lines 15-23):**

```
    15	## Ordering assumption
    16	
    17	Several records are undated in their files. The record's own words
    18	date them: 2ef42163 answers the Embodied/Forged debate of 04db2fd2
    19	(2026-08-26/27) and precedes e8c4cc61 (2026-08-29), which precedes
    20	62022e8f (2026-08-30/31) and 995a164e (2026-08-30 to 09-01). Under
    21	that order the naming of the text-to-value direction is a succession,
    22	realize → embody → actualize, and Prospective → Potential likewise,
    23	not a same-time conflict.
```

**Topic headers:** each section names the Vision file and what
happens to it. Examples: "Topic: kinds -- Vision/kinds.md (new)",
"Topic: protos -- Vision/protos.md (Direction replaced, the rest
new)", "Topic: datom -- Vision/datom.md (revision)",
"Topic: ethos -- Vision/ethos.md (two additions, from the b675f3d9
draft)", "Topic: distillation -- Vision/distillation.md (additions)".
Each subsection heading carries an annotation: "(replaces the current
statement)", "(new)", "(replaces the first paragraph; the second
paragraph stands)", "(addition, last sentence)", "(replaces)", etc.
Witnessed.

**Impurities section (lines 390-399):**

```
   390	## Impurities discarded (destroyed on approval)
   391	
   392	- 01a038b5 curriculumStackToDatomInsteadOfDotos: "I want to migrate
   393	  curriculum stack to datom instead of dotos": a working instruction.
   394	- ac1e9ec8 datomSkill: the session opener "Acquire all psyche on
   395	  datom syntax. We will distill it all, then create a skill…": a
   396	  working instruction (the acbb6006 addendum asked; unanswered).
   397	- 04db2fd2 kinds, third entry: "extend our example to specify all of
   398	  protos, and draft out the accompanying kinds…": a working
   399	  instruction with a question.
```

**Not carried section (lines 401-412):**

```
   401	## Not carried, left for their own topics
   402	
   403	- The protos, datom and ethos skills (e8c4cc61 designPractice,
   404	  62022e8f designPractice, f426777b skillDesigning): topic skills.
   405	- Import resolution (2b34fafa importResolution, sourceNotCrate,
   406	  vision-raw importResolution): the ethos round, once the separator
   407	  is ruled.
   408	- "datom doesnt support omittable fields yet" (4d5fc7da datom):
   409	  implementation status; archived with its record, listed under
   410	  datom Open.
   411	- The crystallization of this practice into a skill: the flow's
   412	  plan, in log.md.
```

**Sources to append on approval (lines 414-460):** lists the
flow-id + topic for every source per Vision topic file, in the form
used by Vision/sources/. Witnessed.

```
   414	## Sources to append on approval
   415	
   416	Vision/sources/kinds.md (new):
   417	6863ef19 traitsAsCapabilities · 06196cc7 traitsAsCapabilities ·
   418	2b34fafa traitsAsCapabilities · f426777b spokenVocabulary ·
   419	04db2fd2 kinds · 2ef42163 kinds · e8c4cc61 kinds · 62022e8f kinds ·
   420	995a164e kinds · b675f3d9 kinds ·
   421	5abf3be8 encodedFormFingerprintTraitDesign · 4decf7 kinds
   422	
   423	Vision/sources/protos.md (new; includes the landed Direction's
   424	source):
   425	04db2fd2 directionAsymmetry · a5587095 protosIsTheSharedStyle ·
   426	ba906ae2 protosIsTheSharedStyle · ba906ae2 encodedFormIsTheCode ·
   427	06196cc7 encodedFormIsTheCode · 06196cc7 traitsAsCapabilities ·
   428	06196cc7 threeStacks · 6863ef19 encodedFormIsTheCode ·
   429	6863ef19 traitsAsCapabilities · 2b34fafa traitsAsCapabilities ·
   430	2b34fafa protosIsTheSharedStyle · 04db2fd2 textualTypes ·
   431	04db2fd2 multiPass · 04db2fd2 delineate · 04db2fd2 anatomy ·
   432	04db2fd2 portion · 04db2fd2 delimiters · 04db2fd2 kinds ·
   433	db97561c prospective · e8c4cc61 protos · e8c4cc61 prospective ·
   434	2ef42163 kinds · 62022e8f kinds · 62022e8f concept ·
   435	62022e8f headedAndContained · 62022e8f symbols · 62022e8f passes ·
   436	995a164e designPractice · b675f3d9 structuralParsing ·
   437	5abf3be8 dotOpensDelimiterEverythingIsData ·
   438	vision-raw encodedFormIsTheCode · vision-raw traitsAsCapabilities ·
   439	vision-raw protosIsTheSharedStyle · 4decf7 protos (transcript-only
   440	words of 2026-08-04 on angle brackets, logged archived)
   441	
   442	Vision/sources/datom.md (append):
   443	ac1e9ec8 datomIsData · 01a03eda datomInteger · 04db2fd2 datomMaps ·
   444	04db2fd2 datomNexus · 04db2fd2 text · 04db2fd2 textualTypes ·
   445	04db2fd2 anatomy · 04db2fd2 directionAsymmetry ·
   446	e8c4cc61 datomSyntax · e8c4cc61 datomizable · 62022e8f datomSyntax ·
   447	62022e8f kinds · 995a164e datomSyntax · 01a04339 datom ·
   448	01a035d3 rustCodeFromTheData · 01a03d6e dotosFiles ·
   449	01a03d6e ethosInterfaces · a5587095 structuredStringType ·
   450	5abf3be8 colonLegalInStringPosition · 4decf7 datomSyntax
   451	(transcript-only words: 2026-08-07 floats question; 2026-08-04
   452	"String is correct", logged archived)
   453	
   454	Vision/sources/ethos.md (new; the earlier 68512643 distillation left
   455	none, its sources reconstructed from archive headers):
   456	01a02a34 ethos · 01a02a34 schemaSyntax ·
   457	vision-raw ethosDotosDivisionAndHelp · vision-raw ethosNonRepetitionLaw ·
   458	b675f3d9 structuralParsing · a5587095 colonFormTransformerSyntax ·
   459	4decf7 ethos (transcript-only words of 2026-08-03 on X.{ and Y.[,
   460	logged archived)
```

**Revision history (lines 462-645):** revisions 2 through 5 carry
provenance for every change. Revision 2 (line 462) cites the
living's corrections and directs that the merged texts stand in
design/proposal1/. Revision 3 (line 498) explains example origins
with flow ids. Revision 4 (line 572) pairs every Rust example with
ethos. Revision 5 (line 585) adds contextualization and un-bluffs
Identity.

### Does the composite show existing distilled text beside proposed text?

It does not. The composite annotates each statement with what it
replaces, adds to, or stands beside in the existing distilled text
(e.g. "replaces the current statement", "replaces the first
paragraph; the second paragraph stands", "addition, last sentence"),
but does not quote the existing distilled text inline for comparison.
The merged proposal1/*.md files are the full proposed topic files
(existing text incorporated and revised), not a side-by-side.
Witnessed.

---

## 4. Raw records gathered by the three reports

References only, as requested.

### flows/4decf7/reports/protos.md

Self-statement: "Gathered by flow 4decf7 for the parent's
distill-as-we-go practice. Each record quoted verbatim, considered
individually." Witnessed.

Records gathered (by reference):

Intent:
- Intent/protosParsing.md

Vision distilled:
- Vision/protos.md "Direction"

Vision-raw (legacy):
- vision-raw/parserIsTheParser.md
- vision-raw/encodedFormIsTheCode.md (two entries: 2026-08-06 and 2026-08-13)
- vision-raw/colonConfusion.md
- vision-raw/colonFormTransformerSyntax.md
- vision-raw/importResolution.md
- vision-raw/itsATranslator.md
- vision-raw/protosIsTheSharedStyle.md
- vision-raw/structuredStringType.md
- vision-raw/traitsAsCapabilities.md
- vision-raw/mainFunction.md

Flow vision records:
- 55d18f4f itsATranslator (two entries)
- 06196cc7 encodedFormIsTheCode (two entries)
- 06196cc7 traitsAsCapabilities (five entries)
- 06196cc7 codeIsLanguage
- ba906ae2 protosIsTheSharedStyle
- ba906ae2 encodedFormIsTheCode
- a5587095 protosIsTheSharedStyle (eight entries)
- a5587095 colonFormTransformerSyntax
- a5587095 structuredStringType (six entries)
- a5587095 rustComponentArchitecture
- 2b34fafa protosIsTheSharedStyle
- 2b34fafa traitsAsCapabilities
- 2b34fafa sourceNotCrate
- 2b34fafa importResolution (four entries)
- f426777b spokenVocabulary
- 04db2fd2 textualTypes
- 04db2fd2 multiPass
- 04db2fd2 directionAsymmetry
- 04db2fd2 delimiters
- 04db2fd2 decomposable
- 04db2fd2 text
- 04db2fd2 delineate
- 04db2fd2 portion
- 04db2fd2 anatomy
- 04db2fd2 kinds
- e8c4cc61 protos
- e8c4cc61 prospective
- e8c4cc61 designPractice
- e8c4cc61 datomizable
- e8c4cc61 kinds
- e8c4cc61 datomSyntax
- e8c4cc61 ethosFileAnatomy
- 62022e8f passes
- 62022e8f multiFormConcepts
- 62022e8f headedAndContained
- 62022e8f concept
- 62022e8f designPractice
- 62022e8f kinds
- 62022e8f symbols
- 995a164e contexts
- 995a164e explodedForm
- 995a164e designPractice
- 995a164e kinds
- 995a164e rust
- b675f3d9 structuralParsing
- 2ef42163 kinds
- 358f143a realizer
- 5abf3be8 colonLegalInStringPosition
- 5abf3be8 dotOpensDelimiterEverythingIsData
- 5abf3be8 encodedFormFingerprintTraitDesign
- 5abf3be8 sectionsExistToConferTraits
- e4be1c4a rustComponentArchitecture
- 55d18f4f signalIsOurMessagingLayer
- 55d18f4f highLevelView
- 06196cc7 threeStacks
- 6863ef19 codeIsLanguage
- 6863ef19 encodedFormIsTheCode
- 6863ef19 signalIsOurMessagingLayer
- 6863ef19 traitsAsCapabilities
- 6863ef19 theBestShape
- ba906ae2 signalIsOurMessagingLayer
- d63804f2 newtypeWrappingAndSingleFieldStructs
- db97561c prospective
- db97561c promptCrafting
- db97561c psycheLogging
- 2b34fafa rustComponentArchitecture
- f426777b skillDesigning
- 13cfc23f threeStacks
- c6b71b4c archive-threeStacks
- 68512643 negatives
- ac1e9ec8 datomIsData
- acbb6006 distillation
- acbb6006 nexus
- b675f3d9 archive-distillation

Also read: b675f3d9/reports/distillProposalProtosDatom.md,
acbb6006/reports/distillProposalProtosDatomAddendum.md, two notions
(62022e8f layerMatching, 62022e8f terminology), Vision/datom.md,
Vision/sources/, design/ProtosEngine/ listing, 04db2fd2/log.md,
b675f3d9/log.md.

### flows/4decf7/reports/datom.md

Self-statement: "Every psyche record that could qualify as a
candidate for distilling together on the subject of Datom -- the data
notation -- and its neighbouring names (NOTA, Dotos, datum, schema
syntax ancestor line, Meaning, Head, guillemets, curly quotes, string
blocks, interface shape, de/serialization, positional, the datom
repository)." Witnessed.

Records gathered (by reference):

Intent:
- Intent/data.md
- Intent/protosParsing.md

Vision distilled:
- Vision/datom.md (all sections)

Vision-raw and flow records:
- ac1e9ec8 datomIsData
- ac1e9ec8 datomSyntax (multiple entries)
- ac1e9ec8 archive-distillationNegatives
- 01a03eda datomSyntax
- 01a03eda datomInteger
- 04db2fd2 datomMaps
- 04db2fd2 datomNexus
- 04db2fd2 text
- 04db2fd2 textualTypes
- 04db2fd2 delimiters
- 04db2fd2 decomposable
- 04db2fd2 directionAsymmetry
- 04db2fd2 delineate
- 04db2fd2 kinds
- 04db2fd2 portion
- e8c4cc61 datomSyntax
- e8c4cc61 datomizable
- e8c4cc61 protos
- 62022e8f datomSyntax
- 62022e8f headedAndContained
- 62022e8f concept
- 62022e8f symbols
- 995a164e datomSyntax
- 995a164e data
- 995a164e concept
- 01a04339 datom
- 4d5fc7da datom
- 01a038b5 curriculumStackToDatomInsteadOfDotos
- 01a035d3 rustCodeFromTheData
- 01a03d6e dotosFiles
- 01a03d6e ethosInterfaces
- 5abf3be8 dotOpensDelimiterEverythingIsData
- 5abf3be8 colonLegalInStringPosition
- a5587095 structuredStringType
- a5587095 protosIsTheSharedStyle
- vision-raw/archive-datomSyntax.md
- vision-raw/archive-threeStacks.md
- vision-raw/archive-ethosDotosDivisionAndHelp.md
- vision-raw/structuredStringType.md

Also read: 68512643 witnesses/datomVisionGround.md,
b675f3d9/reports/distillCandidatesProtosDatom.md,
b675f3d9/reports/distillProposalProtosDatom.md,
acbb6006/reports/distillProposalProtosDatomAddendum.md,
multiple prior reports.

### flows/4decf7/reports/ethos.md

Self-statement: "Gathered by flow 4decf7. Every record below is a
psyche record that could qualify as a candidate for distilling
together on the subject of Ethos -- the schema language. Each record
is quoted verbatim with its provenance." Witnessed.

Records gathered (by reference):

Intent:
- Intent/mandatoryTraits

Vision distilled:
- Vision/ethos.md (all sections)
- Vision/ethosMonolith.md (all sections)

Vision-raw and flow records:
- 5abf3be8 dotOpensDelimiterEverythingIsData
- 5abf3be8 chainedNamesScrapped
- 5abf3be8 streamDisqualifiesBundling
- 5abf3be8 sectionsExistToConferTraits
- 5abf3be8 colonLegalInStringPosition
- 5abf3be8 replacementKillsOldSystem
- 5abf3be8 disavowAuthorNeverWrites
- 5abf3be8 encodedFormFingerprintTraitDesign
- vision-raw encodedFormIsTheCode
- 55d18f4f everythingIsInTheDaemon
- 55d18f4f majorRecoveryEffort
- 55d18f4f itsATranslator
- 012fbf07 threeStacks
- a5587095 colonFormTransformerSyntax
- a5587095 structuredStringType
- 6863ef19 traitsAsCapabilities
- 06196cc7 traitsAsCapabilities
- vision-raw traitsAsCapabilities
- vision-raw genericParametersAreTraits
- ba906ae2 rustComponentArchitecture (via archive)
- 2b34fafa traitsAsCapabilities
- 2b34fafa protosIsTheSharedStyle
- 2b34fafa rustComponentArchitecture
- 2b34fafa importResolution
- 2b34fafa ethosSourceFiles
- 2b34fafa ethosNamespaces
- 2b34fafa sourceNotCrate
- vision-raw assembly
- vision-raw mainFunction
- vision-raw worldModelBeforeCode
- bc05da32 mainFunction
- aa4c7747 ethos
- aa4c7747 ethosTraitSyntax
- aa4c7747 ethosMonolith
- aa4c7747 interactions
- aa4c7747 tuples
- aa4c7747 orchestrate
- aa4c7747 spokenVocabulary
- 01a02fd5 interfaces
- f426777b ethosSourceFiles
- f426777b spokenVocabulary
- b675f3d9 kinds
- b675f3d9 structuralParsing
- b675f3d9 ethosMonolith
- 01a03d6e ethosInterfaces
- e8c4cc61 ethosFileAnatomy
- e8c4cc61 ethosTypes
- e8c4cc61 designPractice
- e8c4cc61 designExamples
- e8c4cc61 kinds
- e8c4cc61 prospective
- e8c4cc61 datomizable
- e8c4cc61 protos
- e8c4cc61 psycheLayers
- 04db2fd2 kinds
- 04db2fd2 portion
- 2ef42163 ethos
- 2ef42163 kinds
- 62022e8f ethosTypes
- 62022e8f kinds
- 62022e8f headedAndContained
- 62022e8f layers
- 62022e8f multiFormConcepts
- 62022e8f concept
- 62022e8f vocabulary
- 62022e8f distilledVision
- 62022e8f designPractice
- 62022e8f passes
- 62022e8f symbols
- 62022e8f datomSyntax
- 995a164e ethosTypes
- 995a164e concept
- 995a164e kinds
- 995a164e explodedForm
- 995a164e rust
- 995a164e designPractice
- 995a164e layerMatching
- 995a164e contexts
- 995a164e data
- 995a164e vocabulary
- 995a164e intent
- 995a164e tokenCosts
- 995a164e entryFiles
- 68512643 negatives
- db97561c nexus
- vision-raw workingSpiritNewEthosSyntax
- vision-raw ethosNamespaces (empty)
- vision-raw ethosSourceFiles (empty)
- vision-raw archive-ethosDotosDivisionAndHelp (archived)
- vision-raw archive-ethosNonRepetitionLaw (archived)
- vision-raw archive-threeStacks (archived)
- vision-raw archive-rustComponentArchitecture (archived)
- 01a02a34 archive-ethos (archived)
- 01a02a34 archive-schemaSyntax (archived)

Also read: Vision/sources/ethosMonolith.md, 62022e8f/notion/layerMatching.md,
b675f3d9/vision/spokenVocabulary.md (empty).

---

## 5. Unreferenced raw records on these five topics

Records under flows/*/vision/, flows/*/notion/, and vision-raw/ that
exist on the five topics but are not referenced by the three
gathering reports (protos.md, datom.md, ethos.md). By reference, with
one line saying what each is about. Witnessed.

- **flows/e4a40e/vision/kinds.md** — The living's rulings of
  2026-09-03 on kind identity (two heads differing in a required kind
  are two kinds; what identifies a trait in Rust identifies a kind in
  ethos). Current flow record.

- **flows/e4a40e/vision/distillation.md** — The living's ruling of
  2026-09-03 on distillation practice (a proposal says where it goes
  and what it replaces; distill with the distillate in hand).
  Current flow record.

- **flows/04db2fd2/vision/rollingDistillation.md** — The living's
  directive (STT) to distill vision as an ongoing process, every
  second or third turn, to prevent stale contradictions.

- **flows/a60a9e85/vision/distillation.md** — The living's ruling of
  2026-08-23 that distillation is comprehension, one concept at a
  time, after stopping a synthesis that had not understood the
  concepts.

- **flows/cff271af/vision/distillation.md** — The living's ruling of
  2026-08-22 that distilled psyche has more value than raw psyche; a
  correction should be proposed as a distillation, not a raw edit.

- **flows/ac1e9ec8/vision/distillationNegatives.md** — On negatives
  in distillation. Already distilled into Vision/distillation.md per
  Vision/sources/distillation.md ("ac1e9ec8 distillationNegatives"),
  but the non-archived record is unreferenced by the three reports.

No unreferenced records were found in vision-raw/ on these five
topics beyond what the three reports already list. The notions
(62022e8f/notion/layerMatching.md and 62022e8f/notion/terminology.md)
were read by the protos report and the ethos report respectively.
Witnessed.

---

## 6. Vision/sources/kinds.md — sources line form

The file has eight entries total (fewer than ten), shown in full.
Witnessed.

```
     1	# Sources — kinds
     2	
     3	f426777b spokenVocabulary
     4	b675f3d9 kinds
     5	6863ef19 traitsAsCapabilities
     6	06196cc7 traitsAsCapabilities
     7	2b34fafa traitsAsCapabilities
     8	04db2fd2 kinds
     9	5abf3be8 encodedFormFingerprintTraitDesign
    10	4decf7 kinds
```

The form is: flow short id, one space, topic file name (no path, no
extension, no date). One entry per line. The header is
"# Sources -- <topic>".

---

## Sources

What this report read, in order:

1. Vision/kinds.md
2. Vision/protos.md
3. Vision/datom.md
4. Vision/ethos.md
5. Vision/distillation.md
6. Vision/sources/kinds.md
7. Vision/sources/datom.md
8. Vision/sources/distillation.md
9. Vision/ethosMonolith.md
10. Vision/nexus.md
11. Vision/flowNexus.md
12. Vision/highLevelView.md
13. Vision/orchestrate.md
14. Vision/remembering.md
15. Vision/x11.md
16. Vision/sources/ethosMonolith.md
17. Vision/sources/nexus.md
18. flows/4decf7/design/proposal1/kinds.md
19. flows/4decf7/design/proposal1/protos.md
20. flows/4decf7/design/proposal1/datom.md
21. flows/4decf7/design/proposal1/ethos.md
22. flows/4decf7/design/proposal1/distillation.md
23. flows/4decf7/design/distillationProposal1.md
24. flows/4decf7/reports/protos.md (headers, record references, sources section)
25. flows/4decf7/reports/datom.md (headers, record references, sources section)
26. flows/4decf7/reports/ethos.md (headers, record references, sources section)
27. flows/4decf7/vision/archive-kinds.md
28. flows/e4a40e/vision/kinds.md (first 20 lines)
29. flows/e4a40e/vision/distillation.md (first 20 lines)
30. flows/04db2fd2/vision/rollingDistillation.md (first 10 lines)
31. flows/a60a9e85/vision/distillation.md (first 10 lines)
32. flows/cff271af/vision/distillation.md (first 15 lines)
33. flows/ac1e9ec8/vision/distillationNegatives.md (first 10 lines)
34. Vision/sources/protos.md — confirmed absent
35. Vision/sources/ethos.md — confirmed absent
