Presentation.{ «Raw psyche: the clearing» }

# Raw psyche: the clearing

## Crystallization

### Proposal 1: destroy the overruled records

```text
+----------+ +----------+
|   raw    | |duplicate |
|  record  | |          |
+----+-----+ +----+-----+
     |            |
     | overruled  | is a copy
     | by         | of
     v            v
+----------+ +----------+
| later    | | earliest |
| record   | | hearing  |
+----+-----+ +----+-----+
     |            |
     +-----+------+
           | lets us
           | destroy
           v
      +----------+
      |destroyed |
      +----------+

+----------+ +----------+
| advanced | |makeshift |
| unmarked | |          |
+----+-----+ +----+-----+
     |            |
     | is         | is
     | marked     | marked
     v            v
+----------+ +----------+
|long-term | |short-term|
+----------+ +----------+
```

**Destroy** Voice and seat vocabulary: 16 records.

```text
- The abstraction of a seat, under a better term (2026-10-02)
- Seats talk by seat name (2026-10-02)
- A voice's name is two variants, not a string (2026-10-02)
- A voice is aspect and rank, nine voices, three by three (2026-10-02)
- Voices, not seats (2026-10-03)
- Two registries: the true one with the ids, and the voices (2026-10-03)
- Role is an enum: voice, system audit, live psyche interaction, implementer, vision audit; each runs on the smallest, highest-signal context (2026-10-03)
- Voice is a struct of Aspect and Layer (2026-10-03)
- Voice is a struct of aspect and layer; structs over chained variants (2026-10-04~)
- The design is evolving fast with Jev in the middle of typed communication; the 3×4 table of voices may not be organic enough (2026-10-04)
- The format of a voice's name: a bare struct of aspect, layer and flow id (2026-10-05)
- A registry changes which flow is associated with a voice when there is a new one (2026-10-05)
- The voice is a type of metaflow; there are specialized metaflows (2026-10-05)
- The messenger identifies a message's originator by voice only, by voice and rank (2026-10-05)
- A flow ID and a role (2026-10-05)
- A voice is a permanent metaflow, one that may sleep and is woken by a message; the role is maybe a short camel-case string; the worker names are the old system (2026-10-07~)
```

Machine: the later record settled that the voice concept is gone, and the default topic is core (2026-10-11).

**Destroy** Curriculum and skill-generation machinery: 6 records.

```text
- the kinds of skill and psyche-level; the future Curriculum-nexus generates them with deterministic names (2026-09-16)
- This is where we want to go: towards Curriculum being a Nexus and taking it in; we take control of that state, and we can reset it through Nix, or repopulate it, reseed it from Nix; there is a reseed service part that recreates a basic seeded curriculum (2026-09-17~)
- Overhaul Curriculum. All this becomes a module system with modules for the different things that become skills from vision. Curriculum is a nexus, so it cannot hold data — it would keep rebuilding it. Curriculum is given a manifest of paths to Markdown files with names; the data lives elsewhere. A file in each directory names the type of each Markdown, or the type sits in the Markdown's header — the fields the Curriculum system knows about are read, others are ignored so people can put non-system data there (2026-09-17~)
- Unify. There is no separate Datom skill and Datom vision — same thing. A topic has faces: the core (named just by the topic, e.g. Datom), the extended (Datom extended), and specific subtopics named by subtopic that give a very extensive view of that aspect. Raw vision and raw Notion are the good source that becomes distilled into these (2026-09-17~)
- The curriculum generator is just a binary, a nexus with CLIs. Three types of skills from three repos, each with its own vocabulary. Skills have prefixes: operational, vision. Anybody regenerates when main moves. Primary is shared — all skills change when somebody regenerates. Primary next starts testing flows divided into three sectors (2026-09-20~)
- Vision, skills, and typed generation — 2026-09-24 (2026-09-24)
```

Machine: the later record settled that skills left the Curriculum for three skill repositories (2026-09-29), and the machinery was cut to something dirty and simple.

**Destroy** Flashbook illustration, swipe pages and buttons: 10 records.

```text
- We need illustration: the first page is always an illustration, then optionally a small text, then another illustration, never two boring charts in a row (2026-09-20~)
- A minimum page count for a book (2026-09-20)
- Each page carries an image (2026-09-20)
- Each section is a component at a level, with explicit imagery, a flowchart with comments, and brief text. The low-power model vivifies the SVG flowcharts into vivid imagery. Three densities and two layouts: portrait and landscape (2026-09-20~)
- You're not the Flashbook Renderer. You're the Psyche Low. The only roles we have right now are 12-fold. We have 3 aspects and 4 power levels (2026-09-20~)
- Illustrations are generated by an image model, not drawn as SVG (2026-09-23)
- A new flashbook brings forward only the six to nine most important topics (2026-09-23)
- Six to nine, illustrations that pull the living in, one rolling flashbook per main flow (2026-09-23)
- Three levels of flashbook (2026-09-24)
- Make our own web UI, Mentci Web, defined like a Nexus but a full web application, speaking a standardized Mentci UI signal; start simple with markdown fields in a three-part structure; make the flashbooks there (2026-09-21~)
```

Machine: the later record settled that books are red and green with graphs, and no illustration (2026-10-01).

**Destroy** High, Medium and Low effort tiers of psyche flows: 5 records.

```text
- High effort is a waste; right now we are in medium mode (2026-09-13)
- Three levels of psyche flows, low, medium and high effort, with a Codex and a Claude equivalent: Claude is a model stack and Codex is a model stack; roles have a preferred model, for psyche usually Fable, especially for complex ideas; the psyche always talks to the low effort, since talking first is a low-effort activity like listening, and the thinking goes up one level (2026-09-16~)
- The psyche stack on Claude: Fable on high power, the old Opus medium, the low level Sonnet, the new one or 4.6, Sonnet 5 for now, an interface to save the old Opus even more; the same stack on Codex, Astra for high power; Psyche is the interface and Codex comes in as Psyche too; all the flows the living accesses are psyche flows, which log the psyche and understand they are there to distill, preserve and interpret it; the Psyche's job is to interact with the living, who responds in the harness or in the messaging system (2026-09-16~)
- The psyche flows are the ones the living interacts with most; other flows are not trained the same way and pass what the psyche says to a psyche agent for logging; only psyche agents know how to log, but every agent is told what to do when the living speaks to it, done programmatically: the harness knows from the style of the message that it is from the psyche, and from which flow it was pushed to where to send it, an awareness command chain: to the psyche at low effort, which decides whether the medium effort should look into it, for logging the psyche or judging notion or vision; the low effort logs only when it is really clear; anything ambiguous or many-topic goes to the psyche at medium power (2026-09-16~)
- The remote thread names say the type and the model: primary Psyche, then the model; primary Psyche opus, primary Psyche sonnet, primary Psyche fable; unified up and down: the low goes to the medium and the medium to the high, each trained to know when to pass packages up; for now explicit instructions to pass things up and down, and a report is made on the topic (2026-09-17~)
```

Machine: the later record settled that effort is always medium, and layers replace the three tiers (2026-09-18).

**Destroy** Datom and Protos delimiters: parentheses, curly quotes, guillemet maps, key-value, version number: 12 records, 12 of them archived.

```text
- parentheses must not be unused in Datom (2026-08-11, archived)
- parentheses delimit the structured string; one string type, two variants (2026-08-11, archived)
- Meaning postponed in datom; () or curly quotes both land as String for now (2026-08-13, archived)
- parentheses are the default string delimiter; Meaning-as-parenthesis floated for dropping (2026-08-14, archived)
- paren strings are balance-based; parentheses are markup inside text (2026-08-14, archived)
- or a dedicated delimiter for maps (2026-08-26, archived)
- curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal (2026-08-26, archived)
- Guillemets for maps; key and value separated by a space (2026-09-03~, archived)
- an associated constant is CAPACITY, written with the key-value map delimiter (2026-09-04, archived)
- the constants in the key-value delimiter only works if their order doesn't matter (2026-09-04, archived)
- key-value delimiters for sections that cannot have the same key; capabilities would need another design for self (2026-09-04, archived)
- proper ethos is variant-headed, a struct with its version and fields: kinds, types, signal, sema variants with implied kind associations (2026-09-04, archived)
```

Machine: the later record settled that the key-value delimiter and its concept are dropped from protos and its dialects (2026-09-04).

**Destroy** Kinds as qualifiers, verbs and layer capabilities: 6 records, 6 of them archived.

```text
- common traits are the right abstraction; all protos dialects are transcodable; qualification by module (2026-08-13, archived)
- Kinds as verbs not allowed; rust-imposed verbs tolerated as legacy until ethos takes over; Delineated is true (delineation intrinsic; implementation fetches it); all kinds move to qualifiers; Textualized; Realized reconsidered, candidates listed (2026-09-04~, archived)
- Textual as a kind; Actual too strong; the form the runtime can use; Embodied, unless Forged (2026-09-04~, archived)
- corrections to the first proposal: might imply; an example with no Rust standard; no conversion tables (2026-09-03, archived)
- The layer capabilities sit on the layer above: structure on Text, conceive on Structure, incorporate on Concept; each layer kind is an alias of a Potential (2026-09-04~, archived)
- what identifies a trait in Rust is what identifies a kind in the ethos (2026-09-04, archived)
```

Machine: the later record settled that kind became trait (2026-10-09).

**Destroy** Message envelope: 800-character pieces and part numbers: 1 record.

```text
- Psyche messages split into 800-character pieces for Claude (2026-09-25~)
```

Machine: the later record settled that psyche messages have no 800-character limit and no part numbers (2026-09-25).

**Destroy** Mentci GUI: 1 record.

```text
- the daemon is the central logic; front-ends are not Rust; Qt for Linux first (2026-08-13)
```

Machine: the later record settled that the Mentci GUI is obsolete (2026-09-28); the Mentci Web record sits in the flashbook group.

**Destroy** Opus 4.6 preferred over Opus 5: 7 records.

```text
- the fence meme, instruction hierarchy, and search compulsion (2026-08-10)
- Opus 4.6, not Opus 5 (2026-09-05)
- Opus 4.6 for the interlocutor, Opus 5 for subagents (2026-09-08~)
- The model for the lower layers: Opus 4.7, or 4.6 with the million context; whichever most resists the temptation to act and instead questions, doubts or seeks clarification, and is good at understanding the unspoken part of a design, rewording and representing it and asking the psyche whether that is what was meant: attaining alignment of vision (2026-09-16~)
- Two Opus models, named by role: the older Opus, the wiser one, and the newer Opus, faster and blinder but good at getting stuff done; the older Opus for consideration, qualitative audits such as comparing vision, and the thinking for a Fable or old-Opus session flow; all thinking, design and psyche interaction on the old Opus or the newest Fable (2026-09-16~)
- Make that the default for psyche medium Claude, being Opus 4.6 — which is 1 million if you have a Max subscription, but is not 1 million for other people. For the basic subscription they don't have much access anyway, so that might even be better in a way (2026-09-18~)
- I would like 4.6 even better than 4.7 — the 4.6 1 million token. Let's roll back to that (2026-09-18~)
```

Machine: the later record settled that Opus 4.6 is being phased out (2026-09-24).

**Destroy** Nota and Dotos syntax: 4 records, 4 of them archived.

```text
- The two main syntaxes most agents will face (2026-08-02, archived)
- Signal is our messaging layer (2026-08-08, archived)
- names confirmed; the successor name must stick (2026-08-10, archived)
- datom is just a renamed dotos; no new repo was needed (2026-08-11, archived)
```

Machine: the later record settled that the nota/dotos format is obsolete, and Datom replaces it (2026-08-26).

**Destroy** Training daemon: 1 record.

```text
- Athena is deployment specific; the successor is a Rust daemon holding variables, regenerating through a terse datom interface (2026-08-17)
```

Machine: the later record settled that the daemon is Flow, not training (2026-08-18).

**Destroy** Flow titles with V2 and per-model names: 3 records.

```text
- Test flows through the new Flow, titled in the V2 form as a Datom struct: PsycheV2.{ Fable <id> } (2026-09-25)
- A test network: a second flow container, fully Flow-controlled, whose seats show a V2 title with the model name and id (2026-09-25)
- Model name, power levels, and Mind Astra panes (2026-09-27)
```

Machine: the later record settled that the V2 form and per-model names in flow titles are obsolete (2026-10-08).

**Destroy** Psyche log ids as hashes: 1 record.

```text
- distillation corrections: re-articulation, many-to-many, 4-hex ids, psyche-archive/ (2026-08-14)
```

Machine: the later record settled that log ids are increasing numerics, not hashes (2026-08-14).

**Destroy** Ethos Monolith as its own stack: 2 records, 1 of them archived.

```text
- the shortcut stack becomes a daemon; renamed ethos monolith (2026-08-14, archived)
- the top is the assembled source, which includes the manifest; two things make a new type; monolith first, not logos (2026-08-21)
```

Machine: the later record settled that Ethos Monolith and Ethos Zero are the same thing, and the name need not be spoken (2026-09-10).

Ruling:

1. Destroy every group as shown, except those held under Proposal 5.
2. Destroy only the groups he names.
3. Destroy none.

### Proposal 2: destroy the duplicates, keeping the earliest hearing of each

**Destroy** Duplicates: 360 exact copies and 259 contained copies, 619 records. An exact copy repeats the same words in another flow; a contained copy is an excerpt whose whole text sits inside a longer record of another flow, and the longer record is kept. The earliest hearing of each stays, so no word is lost.

| Topic | Exact + contained = total |
|---|---|
| flow | 30 + 22 = 52 |
| books | 27 + 15 = 42 |
| ethos | 12 + 10 = 22 |
| messaging | 8 + 12 = 20 |
| meaning | 10 + 7 = 17 |
| skills | 8 + 9 = 17 |
| flashbooks | 6 + 8 = 14 |
| voices | 12 + 2 = 14 |
| nexus | 6 + 6 = 12 |
| communication | 8 + 3 = 11 |
| subflows | 4 + 6 = 10 |
| identifiers | 5 + 3 = 8 |
| 232 more | 224 + 156 = 380 |

```text
- the definition; context-switching parse; the protos engine (2026-08-11, archived)
- direct deploy authority (2026-08-19)
- universal cluster/home fix (2026-08-09)
- keeping the two operating-system repositories in sync (2026-08-08)
- no setup-specific scripts in general repos (2026-08-14)
```

Machine: the 619 can overlap in places, so the destroyed total may fall a little below it; each destroyed copy has its keeper named in the references.

Ruling:

1. Destroy all the copies.
2. Destroy exact copies only.
3. Keep all.

### Proposal 3: the open scope

Ruling, one number from each group:

The 23 archived earlier records in the groups above (all of the Datom delimiters, kinds and Nota groups, and one of the Ethos Monolith group), already crystallized into vision skills:
1. Destroy them with their groups.
2. Keep them.

The 52-record archive-kinds family, whose originals sit in files the crystallization kept:
3. Destroy all 52.
4. Keep all 52.

The 13 unclear cases, all kept until he rules each:
5. Keep all 13 as they are.
6. Rule them one at a time, as listed below.

The unclear cases, with the records in question:

```text
- Subagent facility removed against main flows delegating to subagents (2026-09-20, 2026-09-24)
  Machine: two readings, the harness facility is replaced, or main flows still use it for now.
- Messages forced to be Datom against not enforcing Datom on a messenger that does not need it (2026-09-19, 2026-09-27)
  Machine: the later record may be a short-term posture for the Clojure messenger.
- Skill manifest dropped against a manifest of paths (2026-08-21, 2026-09-17)
  Machine: the two records reverse each other, so neither is the older of a rollback.
- Mentci as an app on a minimal CriomOS, after the Mentci GUI was declared obsolete (2026-10-01, 2026-09-28)
  Machine: the later record may mean Mentci as a nexus, not the GUI.
- Flow lock given to the receiving seat against the flow not giving the lock to the message (2026-09-24, 2026-10-11)
  Machine: the later record names a change of mind but not what it changed from.
- Voice remnant in the base prompt against the voice concept being gone (2026-10-11)
  Machine: the base prompt still defines a flow as one run of a voice.
- Flow-id length: four, six, or words from 33 bits (2026-08-26, 2026-10-03)
  Machine: likely different identifiers, not a rollback.
- Refresh payload and addendum against handover at cache expiry (2026-09-21, 2026-10-14)
  Machine: the later records do not say whether handover replaces the refresh payload.
- Reports and logs as files against everything in the transcript (2026-09-17, 2026-08-21)
  Machine: the file protocol is what runs today; the later record reads as a long-term target.
- Value layer in Datom, reclassified as a notion (2026-09-09)
  Machine: the vision record is itself the reclassification; the notion records stay notions.
- Psyche Medium online (2026-09-17~)
  Machine: the effort record (2026-09-18) does not name this record as overruled.
- Big messages and the psyche message type (2026-09-25~)
  Machine: the overruling record carries the same date, so the order is not shown.
- Flow artifacts: the directory gives the flow; only subflows mark their id (2026-08-21)
  Machine: the overruling record carries the same date; the no-handoff record is the live ruling and is kept, not destroyed.
```

### Proposal 4: long term made explicit, and the makeshift stack named

File: `psyche-context/skills/vision-psyche.md`, a new section «Long term and short term».

Machine: the themes below are matched by keyword, 9 themes, none of whose records carries a short-term or long-term mark today; each is a candidate he can strike.

```text
+ ## Long term and short term
+
+ The vision is long-term, the goalpost, or short-term, the makeshift. Unmarked vision is long-term. When the long term is implemented and documented, the short term goes.
+
+ The advanced machinery below is marked long-term:
+
+ - Models trained on binary signal, with Datom as the language models speak.
+ - The meaning language: Panini, Sanskrit, ontology, content-addressed links, linked-data garbage collection.
+ - Typed storage, typed strings and structured enum logs.
+ - Topics that go idle and are woken by a judgment call, system-1 models, queuing.
+ - Event hooks instead of polling, and a registry of polling systems.
+ - Unity, the tailnet mesh and phone clients.
+ - Open-source models, the private layer and local model hosting.
+ - Criome identity, authenticated updates, an own sandbox and security.
+ - The Nexus component architecture: Signal, Sema, CLI and daemon sockets.
+
+ The makeshift prototype stack is marked short-term: Clojure under Babashka, Malli specs, EDN data. Its 59 records are short-term; the long term is Ethos and Rust.
```

Ruling, strike any number he does not want marked long-term:

1. Models trained on binary signal; Datom as their language (3 records).
2. The meaning language (48 records).
3. Typed storage, typed strings, structured enum logs (3 records).
4. Idle topics woken by judgment; system-1 models; queuing (6 records).
5. Event hooks instead of polling (8 records).
6. Unity, tailnet mesh, phone clients (32 records).
7. Open-source models, the private layer, local hosting (22 records).
8. Criome identity, authentication, own sandbox (19 records).
9. The Nexus component architecture (258 records).
10. The makeshift stack marked short-term (59 records).

### Proposal 5: two cautions that need his ruling

Ruling, one number from each group:

The voice group (16 records, the first in Proposal 1). The base prompt still defines a flow as one run of a voice, while the 2026-10-11 record removes the voice:
1. Hold the voice group until that base-prompt line changes.
2. Destroy the voice group now.

The records that put reports and logs in the transcript rather than in files:
3. Keep them as long-term, and do not destroy them; the file protocol is what runs today.
4. Treat them as overruled and destroy them.
