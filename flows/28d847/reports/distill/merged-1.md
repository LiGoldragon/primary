# Merged distillation set 1

This merges three candidate files with the current distilled vision (`Vision/*.md`, `Intent/*.md`), so that each topic holds one consistent set of statements. Nothing here has landed, and nothing lands before the living approves it statement by statement. No raw record has been moved.

Candidate references (section numbers are the candidate file's own):

- `CM-n`: `flows/28d847/reports/distill/1-context-modules.md`, section n
- `FL-n`: `flows/28d847/reports/distill/2-flow.md`, section n
- `BP-n`: `flows/28d847/reports/distill/5-8-books-and-practice.md`, section n

Quote ids (1.1.6, 2.3.12, E13, N3, 5.1.27 and so on) and tension tags (T1 to T23) are the package's, as the candidate files cite them. Dates of existing Vision statements are their landing dates in git. Where a source record's date is known, it is given too.

Merge rules applied across the whole set:

- **The living, not he.** Existing Vision says "the living". Every candidate's "he", "him" and "his" is rewritten that way.
- **Layers, not models.** On 2026-10-03 the living ruled that skills and vision speak of layers, never of models (2.3.5, 2.3.6). Model names in candidates outside subject 2 (BP-1, BP-2, BP-3, BP-5, BP-14) are therefore taken out too. Wherever a model had to be mapped onto a layer, the entry says so. That mapping is the agent's work, to be checked against the knowledge-layer-models skill.
- **Voice, not seat.** Under the 2026-10-02 and 2026-10-03 rulings, "seat" becomes "voice" wherever a statement means a voice (BP-15).
- **Each clause appears once in the set.** When two candidates, or a candidate and an existing statement, say the same thing, the clause is kept in one entry, and the other entry names where it went.

Decisions: **new** (no existing statement; the landing file is named); **extends** (one merged statement replaces the existing one and the candidate); **replaces** (later words supersede the existing statement; both are given with dates); **duplicates** (the candidate is dropped and the existing statement cited); **conflicts** (both sides stated with dates, not resolved).

"Quotes replaced" counts the package quotes (or quote paragraphs) the entry would archive on landing, with their word count. A quote is counted in one entry only. When a candidate is split across entries, its quotes are counted where the entry says.

---

# Vision/voices.md (new topic)

This topic must land first, or together with the entries that use its terms: voice, aspect, layer, primary, secondary, tertiary, quaternary.

## 1. Voices and layers

- **Decision:** new
- **From:** FL-4, FL-14 (merged)
- **Existing touched:** `Vision/modelRoles.md`, which names seats by model throughout (see entry 18). `Intent/models.md` "Two scales share the words high and medium" (see entry 54). `Vision/flowNexus.md` "Subflows are created from the questions and requests a flow ends with" says "ultra-low power" (T7, listed under conflicts).
- **Quotes replaced:** 14 (531 words): 2.3.2, 2.3.3, 2.3.4, 2.3.5, 2.3.6, 2.3.7, 2.3.12, 2.3.15, 2.3.17, 2.3.22, 2.3.8, 2.3.11, 2.4.8, 2.4.16

**Text.** A voice is one aspect at one layer. The aspects are psyche, mind and field. The layers, by rank, are primary, secondary, tertiary and quaternary. So the voices are psyche primary, mind secondary, field quaternary, and so on. A voice is the continuous aspect and layer that flows carry on, and it outlives any one flow. What agents called a seat is a voice, and seat is not used.

```
Voice.{ Aspect.[ Psyche Mind Field ]
        Layer.[ Primary Secondary Tertiary Quaternary ] }
```

A layer is a rank of authority, never a model's effort. Every skill and every vision speaks of voices and layers, never of models, because the models are not exposed to the voices. Which model serves which layer is set separately for each stack, the Claude stack and the Codex stack. That correspondence lives in one knowledge skill, which is loaded wherever it is needed.

**Notes.** FL-4's clause "the layer words do not overlap the effort words" moved to entry 54, where the scale distinction already stands. The code is the living's own ethos (2.3.7), with the unclosed `Layer.[` bracket closed. The separation between a flow (one running session) and a voice (the continuous name) is the agent's reading of 2.4.9 and 2.4.16 together, and the living should confirm it. Conflicts: T8 (nine voices against four layers), T6.

## 2. What each layer is

- **Decision:** new
- **From:** FL-3
- **Existing touched:** none
- **Quotes replaced:** 2 (481 words): 2.3.25, 2.3.29

**Text.** The four layers differ in authority. The primary is where ideas go. It is the top authority, it watches everything below it, and it can give orders anywhere down. The secondary is the stable trunk. It is a large knowledge memory that stays aware of many things, it is trusted for a fairly reliable current view, and it can talk with the living. When it is unsure, it asks the layer above. The tertiary is the fast, mercurial layer of real-time communication. It keeps things live, alert and attentive, handles speech-to-text back and forth, and does the quick thinking, drawing on the secondary as quick, good knowledge. The quaternary is the instinctive layer at the bottom. As a filter or firewall, it corrects speech-to-text and drops noise before the noise can sway anything. As the earthy layer, it runs cheap, long, continuing jobs that monitor, clean up data that is not useful, maintain the system, and report anything that looks wrong. A layer may ask questions upward, but a matter goes higher only through the layer above it.

**Conflicts.** T8: the 2026-09-14 and 2026-09-17 meanings of tertiary and quaternary, against the 2026-10-02 tertiary as a short-lived job and the 2026-10-03 quaternary as the low-effort model of each stack. Joining "filter" and "janitor" into one layer is the agent's reading.

## 3. Sparing the primary layer; the secretary

- **Decision:** new
- **From:** FL-1
- **Existing touched:** none
- **Quotes replaced:** 9 (774 words): 2.1.1, 2.1.5, 2.1.6, 2.1.7, 2.1.8, 2.1.9, 2.1.12, 2.2.6, 2.2.7

**Text.** The primary layer is spoken to rarely. It is the most expensive layer, and its time is kept for what matters: design, rulings and judgment. Nothing goes to it until there is something to tell it. Before anyone speaks to it, the secondary layer gathers the thoughts and investigates, then assembles one package that carries all the relevant psyche. The primary then receives a fully formed question and returns a well-formed answer. Before it judges, it may verify one or two things with its own flows. The secondary also keeps the knowledge of everything being talked about. In the end, that knowledge is for giving new flows good context: the right prompt, the right system prompt, and a vision that keeps growing. In the psyche aspect, the psyche secondary is the messenger and the secretary. Every message into or out of the psyche primary passes through it, and only it speaks to the psyche primary. The psyche primary may speak to the mind primary under the same rules.

**Notes.** One condition is open: 2.1.5 says "for now, it's on my word only". The main flow should ask whether it still holds. Conflict: T9 ("only you talk to" it, 2026-10-04, against "not a hard rule; it's guidance", 2026-10-03). Entry 4 carries the guidance reading.

## 4. Speech moves one layer at a time

- **Decision:** extends
- **From:** FL-2
- **Existing touched:** `Vision/modelRoles.md` "Native names use aspect and model", paragraph 3 ("Horizontal communication joins aspects at equivalent behavioral power ... it does not make the message disappear") and paragraph 5 ("Horizontal routing selects the unique eligible cell ..."). Landed 2026-09-23 from 9ddcbc (2026-09-23).
- **Quotes replaced:** 8 (637 words): 2.1.2, 2.1.3, 2.1.4, 2.1.10, 2.1.11, 2.3.16, 2.3.19 (routing paragraph), 2.3.23

**Text.** Speech moves one layer at a time. A voice speaks to the layer just above or just below it in its own aspect, and to its own layer in another aspect. It does not speak diagonally. A mind secondary reaches the psyche primary only through the psyche secondary, or through the mind primary, which may pass on some of what was said. Field speaks to mind, and mind speaks to psyche. Field speaks to psyche very rarely, almost never. Every contact needs a good reason. Field reaches mind when code or documentation must change and be tested before field can deploy, because mind builds the better, more integrated solution. Mind reaches psyche for feedback on a design, a choice or a judgment, never just to talk.

A request going up passes the layer above first. That layer audits it and rules on it if it can. If the request came from a misunderstanding, it says so and sends the request back, so the lower layer can return with a different proposal or proof of concept. It passes the request higher only when it does not want to rule on it itself. Asking the layer above is how a lower layer gains certainty. If the next layer up is not running, the request goes to the nearest running layer above. The missing layer is reported as a gap, and the message does not disappear.

Routing within one aspect selects the nearest eligible layer in the requested direction. Routing across aspects selects the unique eligible voice in the target aspect at the sender's layer. Busy is still eligible. Missing or unavailable needs fresh lifecycle and route evidence. Several bindings for one voice are an unresolved conflict, never fanout. When no voice is eligible, the result is explicitly undeliverable. The binding is resolved immediately before each attempt. A fallback has succeeded only when the exact recipient accepts it. An ambiguous attempt stays attached to that recipient and is reconciled, never resent to another layer.

These rules are guidance drawn from the living's examples, not law, and a rare exception may happen. What has to be kept is the posture behind the examples: the primary's time is kept for important things.

**Notes.** The third paragraph is the existing modelRoles routing paragraph. Following the 2026-10-03 layer vocabulary, "behavioral power" and "rung" become "layer" and "cell" becomes "voice", and nothing else in it changes. Conflict: T9, as in entry 3. "Medium levels speak to each other" (2.3.19) is read as "own layer in another aspect", and that reading is the agent's.

## 5. Naming and addressing a voice

- **Decision:** replaces
- **From:** FL-6
- **Existing touched:** `Vision/modelRoles.md` "Native names use aspect and model", paragraph 1 (every native main session is titled `<Aspect> <Model> <FLOW_ID>`), paragraph 2 (power High, Medium, Low, Ultra Low as a typed property) and paragraph 4 (aspect, model identifier, model display, behavioral power, Flow ID and native binding are separate typed facts). Landed 2026-09-23 from 9ddcbc, a 2026-09-23 record.
- **Superseded by:** 2.3.9 and 2.3.10 (2026-10-03, 5578cc flow), aspect and layer only, aspect first; and 2.3.5 and 2.3.6 (2026-10-03), layers, never models.
- **Quotes replaced:** 7 (405 words): 2.3.9, 2.3.10, 2.4.9, 2.4.10, 2.3.13, 2.3.19 (naming paragraphs), 2.3.28

**Text.** A voice is named and addressed by its aspect first and then its layer, as in psyche secondary, followed by a word id. Voices message each other by that continuous name, never by flow id. Flow ids remain for accounting: the ledger, the archive, and knowing where to search when a transcript is needed.

**Notes.** "Word id" is defined in no record. Either the living defines it before landing, or that clause stays raw. Paragraph 4 of the existing section is not superseded in substance. It would stay, reading "layer" where it reads "behavioral power"; the living should confirm that. Impurity discarded: "Not soul" (2.3.19), a speech-to-text correction. Possible conflict with `Vision/flowNexus.md` "A session is named after its direct ancestor", listed under conflicts.

## 6. The primary designs, the secondary implements

- **Decision:** new
- **From:** FL-13
- **Existing touched:** none
- **Quotes replaced:** 5 (145 words): 2.2.1, 2.2.2, 2.2.3 (first sentence), 2.2.4, 2.2.5

**Text.** The primary deals with design, ideas and concepts. It thinks and makes the big decisions, and it does not sweep the floor. It passes what it has designed down to the secondary. The secondary manages the work, implementing and testing it by coordinating its own sub-agents. This holds in each aspect: the mind primary designs and orchestrates, and the mind secondary implements and tests. Design is not done by the secondary.

**Conflict (untagged).** On 2026-09-28 (2.2.3), finished design passes across aspects to the mind primary. On 2026-10-03 (2.2.1), it passes down to the psyche secondary within the psyche aspect.

---

# Vision/flowNexus.md

## 7. A flow's role

- **Decision:** extends
- **From:** FL-5 (first paragraph)
- **Existing touched:** `Vision/flowNexus.md` "Starting flows" (landed 2026-09-20): "A Nexus component decides the system prompt and everything about a launch ...". Its clause about replacing the harness's subagents goes to entry 8.
- **Quotes replaced:** 2 (142 words): 2.4.2, 2.4.15

**Text.** Flow, a Nexus component, decides each flow's system prompt and everything about its launch, and every specialty has its own system prompt. A flow's definition is a struct, and one of its fields is the flow's role. Role is an enum. One variant is voice. The others are the specialized roles, named as activities: living interaction, implementation, vision audit, system audit, and others as they are made. A monitor is one. Vision distillation is another: it delivers a full document, a spec and example code for the living to review, and mind can then implement an accepted distillation. A specialized flow starts with its prompt perfectly aligned and gets to work at once. It produces the best output it can from the smallest, most concentrated context, with the highest signal-to-noise ratio that can be assembled.

```
Flow.{ Role … }
Role.[ Voice LivingInteraction Implementation VisionAudit SystemAudit … ]
```

**Notes.** No record names the other fields of the struct, so they are marked `…`. Conflicts: T23 (role as a field here; role as a module type in entry 12; the word kind). Untagged: "specialty type" or "a different kind of call" (2026-09-25) against a role field (2026-10-03). Untagged, across candidates: the vision-distillation role delivers "a full document" (2026-09-25), while entry 33 asks for concise proposals small enough to answer yes quickly (2026-10-01, 2026-10-03).

## 8. Sub-agents now, independent flows eventually

- **Decision:** replaces
- **From:** FL-5 (second paragraph)
- **Existing touched:** `Vision/flowNexus.md` "Subflows replace the harness subagent facility" (landed 2026-09-20 from records of 2026-09-05, 1a6ca4, and 2026-09-19, f38926), and the clause in "Starting flows" about "replacing the harness's subagents with specialized harnesses launched with specialized system prompts". The existing text says the facility *is* replaced.
- **Superseded by:** 2.4.3 and 2.4.5 (2026-10-03): pass work to sub-agents now; "eventually all the sub-agents will themselves be flows".
- **Quotes replaced:** 3 (291 words): 2.4.3, 2.4.18, 2.4.20

**Text.** For now, main flows pass work to sub-agents. Eventually every sub-agent is itself an independent flow. Each has its own system prompt, because the flows need different prompts, and each can reply to whichever flow succeeds the one that asked. The harness sub-agent facility puts two flows into one synchronous user interface and locks them into a single main flow. With independent flows the whole system is asynchronous, and no flow is locked into another flow's synchronous interface.

**Notes.** FL-5's last sentence ("sending work then becomes routing: is there already a flow that should simply get this message?") duplicates the opening of `Vision/flowNexus.md` "Subflows are created from the questions and requests a flow ends with", which stays as it is. T21 is the tension behind this entry. The later words keep the eventual aim and add "for now".

## 9. Launching from premade roles

- **Decision:** new
- **From:** FL-7
- **Existing touched:** `Vision/modelRoles.md` "One declaration sets the model everywhere" (consistent, unchanged); `Intent/models.md` (medium default, see entry 53)
- **Quotes replaced:** 3 (338 words): 2.3.14, 2.4.11, 2.4.14 (first part)

**Text.** Flows are launched only from premade roles. Each role is programmed in a list with its datom configuration, model and effort already set, so a launcher never makes them up. A launch feeds that configuration into the new flow, along with additions to its prompt drawn from files or other sources. A setting left unset takes its default. Datom is explicit, though, so a configuration either names the setting or uses a shorthand. A role that has not been designed is not launched. Nothing runs at high effort because no designed role uses high effort, not because high effort is refused. The Flow tool has one complex central start call that carries every argument. It also has shorthands: partly preconfigured, minimal calls that need few arguments. The same pattern, one central call plus shorthands, serves any main function or main feature.

**Notes.** "Which for effort is medium" is dropped here, because `Intent/models.md` already holds it. Conflicts: T17, T13 (is a role's configuration a place where the program needs datom?).

## 10. The brief sub-agent

- **Decision:** new
- **From:** FL-8
- **Existing touched:** none
- **Quotes replaced:** 4 (283 words): 2.4.1, 2.4.4, 2.4.5, 2.4.19

**Text.** A sub-agent is launched with as few tokens as possible. Its definition already carries almost everything it needs to know for its specialty. The launcher sends one or two lines, the job and which vision files to inject, and the sub-agent gets to work and answers back when done. A main flow never repeats standing instructions in a brief, because standing instructions are what sub-agent definitions are for. Every kind of job has a sub-agent tailor-made for it, and there should be very many. Missing ones are designed with the psyche primary, deployed, and used. The aim is an extremely cheap sub-agent.

**Conflicts.** T21 (see entry 8). T13: 2.4.19 has subflows written in datom. The format of the one or two lines is left unsaid.

## 11. Behavior modules are chosen at launch

- **Decision:** new
- **From:** CM-15
- **Existing touched:** `Intent/startupPrompt.md` "One block, with the startup skills in it" (consistent: startup skills go to particular flows and never to their subflows; unchanged)
- **Quotes replaced:** 2 (167 words): 1.3.26 p3, 1.1.10 p2

**Text.** Skills that alter how a flow behaves are behavior modules: features a flow is launched with. Examples are the main flow; an expert on a subject; a doubter or critic; a visualizer that makes visualizations; one that knows certain software and how to operate it; and a browser that operates web apps for the user. A Flow command launches a flow with these particular skills loaded in its prompt, and they need not be reachable by any other agent. Knowledge is never restricted this way: any agent that wants to know anything can load it. The main flow's system prompt can carry a part its subagents do not receive, so the main flow is programmed one way and its subagents another. Whether the harness allows that is to be found out.

**Conflicts.** T5, T21. 1.1.16 (a notion) stays verbatim.

## 12. Flow's registry of modules and the launch list

- **Decision:** new
- **From:** CM-10
- **Existing touched:** `Vision/nexus.md` "Sockets" (the meta socket carries configuration; consistent)
- **Quotes replaced:** 4 (388 words): 1.1.6, 1.1.7, 1.1.8, 1.1.9

**Text.** Context modules stay Markdown files, because they reach the model as a string anyway. Flow keeps a registry in its database of where every module is: its name and its location, for now a local file path, later perhaps a Git repository. That configuration is kept apart from launches, served through the meta socket, and updated whenever a skill is added. A launch names the modules wanted for each place it loads into: the system prompt at each layer, and the origin startup prompt, the first prompt a flow is started with. It names them as a vector of module types, in which each variant carries the names of its modules, so nothing repeats, and Flow inserts each module in its place. Role is a module type. The field naming a module's type is not called kind, because ethos already uses kind for something more basic. This is the prototype, the minimum viable product.

```
; illustrative shape only; type and field names are placeholders
SystemPrompt.[ Spirit.[ spirit ] Vision.[ flow psyche behavior ] Role.[ main-flow ] ]
StartupPrompt.[ Vision.[ datom ] ]
; kept separately in Flow's registry: name to location
[ { flow «skills/flow.md» } { psyche «skills/psyche.md» } ]
```

**Conflicts.** T23. Untagged: no manifest, generate whatever is present (2026-08-21, entry 26), against a registry (2026-10-03). 1.1.7 corrects 1.1.6 within the same exchange, and the main flow should confirm that reading.

## 13. No compaction: a refresh restarts on a fat first prompt

- **Decision:** new
- **From:** CM-9, plus FL-9's refresh sentence (merged)
- **Existing touched:** `Vision/flowNexus.md` "A replaced session is reaped by the refresh itself" (consistent, unchanged)
- **Quotes replaced:** 4 (393 words): 1.1.20, 1.1.22, 1.1.23, 1.1.26. FL-9's quotes are counted in entry 14.

**Text.** A flow does not compact. When its context has grown big, it is refreshed. It restarts itself on a fresh flow with a really good first prompt, always a fat prompt, and it never holds back from restarting. It carries its useful state forward in that prompt, or in a custom system prompt holding the high-level intent, spirit, operational flow and operational rules. A flow changes over at 60 percent of its context at most. It changes over sooner when the conversation shifts hard, repopulating a fresh flow with context fitted to the new emphasis. A main designer flow's first prompt is big, with the vision for most of its topics. The old flow winds down and is marked, by its thread name or by a status such as ancestor or concluded. A concluded flow can be woken to ask it something, but once its cache has lapsed that is expensive and better avoided.

**Notes.** 2.4.17 (a refreshed flow's first goal is a presentation) stays verbatim, as the candidate decided. T3 touches the system-prompt half.

## 14. An ordered launch; reaping

- **Decision:** new
- **From:** FL-9 (without the refresh sentence), plus the dead-flow example of BP-5 (merged)
- **Existing touched:** `Vision/flowNexus.md` "A replaced session is reaped by the refresh itself" (consistent, unchanged)
- **Quotes replaced:** 3 (242 words): 2.4.7, 2.4.12, 2.4.13. BP-5's quotes are counted in entry 46.

**Text.** A flow the living orders is launched. It is launched properly, but it is launched, and an order is never quietly given up. An abandoned flow is reaped. When several flows hold the same role, or a flow runs at too high an effort, those flows are stopped. Their whole context goes to whoever carries the torch for them, or to a new flow started for that purpose. Any voice may call such a flow out. A careful model judges whether a flow is dead and has a successor by reading its transcript. The voice charged with stopping and starting flows then acts on that word: it has the authority to act, not to decide. Once such a mistake has happened, code makes sure it cannot happen again.

## 15. How far down a flow may launch

- **Decision:** replaces
- **From:** FL-12
- **Existing touched:** `Vision/modelRoles.md` "Delegation ceiling" with its "Codex side" and "Claude side" subsections, which are model-named. Landed 2026-09-18 from 4a2502, a 2026-09-18 record.
- **Superseded by:** 2.3.5 and 2.3.6 (2026-10-03), layers, never models. The substance comes from the same record.
- **Quotes replaced:** 1 (179 words): 2.3.20

**Text.** A flow launches subflows only at its own layer or below. It is conservative about this and mostly launches below. The highest layers launch at their own layer rarely. No flow ever launches a primary-layer subflow, because only a main flow is ever at the primary layer. A primary-layer flow often launches the layers just below it, and launches the bottom layer for small jobs.

**Notes.** This moves from `modelRoles.md` to `flowNexus.md`. The mapping of models to layers is the agent's: Fable and Astra to primary, Opus and Sol to secondary, Haiku to the bottom. Terra was removed on 2026-09-26. The model-by-model ceilings go to the knowledge-layer-models skill. T8: the record does not place tertiary and quaternary separately.

---

# Vision/modelRoles.md

## 16. A model is placed by its character

- **Decision:** replaces
- **From:** FL-11
- **Existing touched:** `Vision/modelRoles.md` "Opus is two seats, not one model"; "Thinking, design and psyche interaction run on the older Opus or the newest Fable"; "The older seat's work is consideration and qualitative audit"; "The older seat is chosen for disposition, not capability". All landed 2026-09-18 from f55ec8 (2026-09-17) and 1ac573.
- **Superseded by:** 2.3.5 and 2.3.6 (2026-10-03), layers, never models. The substance comes from the same 2026-09-17 records.
- **Quotes replaced:** 2 (179 words): 2.3.24, 2.3.26

**Text.** A model is placed by its character. Thinking, design, interaction with the psyche, and qualitative audits such as comparing work against the vision go to the wiser model. Getting things done goes to the faster, blinder model. Where a layer must think, the model chosen is the one most likely to resist the temptation to act, and to question, doubt or ask for clarification instead. It must also be good at understanding the unspoken part of a design or an idea: rewording it, representing it, and asking the psyche whether that is what was meant, until the two are aligned on the vision.

**Notes.** "Where a layer must think" generalizes 2.3.24's "the lower layers", and the living should confirm it (T8). The audit method in entry 46 sits beside this statement and does not repeat it.

## 17. High effort is a declared mode

- **Decision:** new
- **From:** FL-10 (the part that `Intent/models.md` does not hold)
- **Existing touched:** `Intent/models.md` "Better models, not higher effort" (see entry 53)
- **Quotes replaced:** 0. FL-10's quotes are counted in entry 53.

**Text.** High effort is waste, and a sign that someone is rushing. It is a declared mode that switches everything to high, used only when quotas are about to run out unused.

**Notes.** Conflict: T17. Untagged: entry 47 says that when quota goes unused, light work runs. Both read "unused quota" differently, and neither is resolved.

## 18. Model correspondences leave Vision

- **Decision:** replaces
- **From:** FL-4 (the rule in entry 1)
- **Existing touched:** `Vision/modelRoles.md` "The older seat is Opus 4.6, and its million-token version is Max-only", with its callable ids, and "The lower layer's main flow is the older Opus". Both landed 2026-09-18 and 2026-09-19 from 1ac573 and f55ec8.
- **Superseded by:** 2.3.5 and 2.3.6 (2026-10-03): the layer-to-model correspondence lives in one knowledge skill, not in Vision.
- **Quotes replaced:** 0 (counted in entry 1)

**Text.** None in Vision. These two sections leave `Vision/modelRoles.md` when entry 1 lands, and their content is carried by the knowledge-layer-models skill.

**Notes.** "One declaration sets the model everywhere" stays. It uses "seat" (T6). Once entries 4, 5, 15, 16 and 18 land, `modelRoles.md` holds entry 16, entry 17 and that section.

---

# Vision/contextModules.md (new topic)

## 19. Context modules: the work is editing them

- **Decision:** new
- **From:** CM-7
- **Existing touched:** none
- **Quotes replaced:** 7 (506 words): 1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.1.5, 1.1.10 p1, 1.2.16

**Text.** A context module is one of the things a thinking machine starts its thinking with: vision, intent, spirit, knowledge, operation and role. Together they are the aspects of its awareness. The family still needs a better name than aspect, which is taken. The work now is editing context modules: creating, editing, removing, splitting and merging them. Every redirection, every book and every exchange with the living comes down mostly to that, and agents are told so at the level of the system prompt. Skills are a prompt system: the same module can go into the system prompt, into the prompt, or stay available for an agent to load. One standard for context modules populates both the skills and the system prompt. Flow uses it, and Curriculum implements it. The component keeps the name Curriculum, because context is too common a word. The concentration is on high-quality modules for the system prompt, and on launching flows educated from them.

**Conflicts.** T2 (the name: training, context, Curriculum). T23 (this module list against entry 26's list).

## 20. Where a module enters: the top and middle layers

- **Decision:** new
- **From:** CM-2
- **Existing touched:** `Intent/startupPrompt.md` (startup skills enter through the startup prompt; it touches the middle-layer side and is unchanged)
- **Quotes replaced:** 10 (792 words): 1.1.13, 1.1.17 p1 and p3, 1.1.18, 1.1.19, 1.1.21, 1.1.24, 1.1.25, 1.1.27, 1.1.29, 1.1.30

**Text.** A model's context has layers of authority, and this is among the most important things in programming with models. The system prompt, the top layer, carries the highest authority. Skills carry the same authority as the user prompt, the middle layer. The living's raw words go in the middle layer until they are distilled. The distillation goes in the top layer, together with specialized expert guidance and a corrected version of the guidance the harness ships with. Steady, well-distilled spirit, intent and vision in the system prompt free room in the prompt, which is maxing out. They also replace whatever conflicts with them there, even words of ours, for better behavior. Intent distilled further goes the same way, and what is already being put directly in the system prompt keeps going there. The primary's system prompt holds the vision for most of its topics, if that can be done. Only the system prompt can hold what must hold against the harness's own guidance, as main-flow mode must. Reloading a skill by hook every so many messages was raised as a fallback. Where intent and vision are skills, they are highly positioned skills.

Against the top-layer placement stand the middle-layer records. The middle layer is the best, and a flow started with a perfect middle layer gives perfect results. A context subflow gathers the vision and skills a piece of implementation needs, and that brief enters the implementing subflow's prompt. Distilled vision is loaded into the middle stratum, and perhaps it is the skill that moves to the top. The living's whole psyche is injected into a new flow at the user level, so the flow has it from there and not from the bottom layer. The living has said that it is not yet known which kinds of module qualify for the system prompt, or what modifying it changes over modifying the user prompt.

**Conflict.** T3. Top-layer side: 2026-09-13, 2026-09-15, 2026-09-17, 2026-09-24, 2026-09-25. Middle-layer side: 2026-09-14 (twice), 2026-09-24. Open: 2026-10-03. The statement carries both sides, and it cannot stand as a rule until T3 is ruled.

---

# Vision/systemPrompt.md (new topic)

## 21. The anatomy of the system prompt

- **Decision:** new
- **From:** CM-6
- **Existing touched:** `Vision/flowNexus.md` "Repository and skills" (the basic skills replace the prompt the harnesses build in; consistent, unchanged)
- **Quotes replaced:** 7 (534 words): 1.1.10 p3, 1.1.14, 1.1.15, 1.1.28, 1.4.3, 1.4.5, 1.4.6

**Text.** The system prompt is not one thing. It has many parts with many subparts. Its anatomy is drawn up in ethos by studying system prompts of every kind, among them the latest Claude and Codex prompts, together with the parts that change per model. Every line is classified: what it is; whether it is behavior, personality or operational safety; which kind of training or guidance it belongs to; and whether it is good, bad, neither, some of each, confusing or unnecessary. The result is data files in Markdown with datom and ethos syntax: the data specified, then shown. The stock prompts are suspected to be full of instructions that go partly or wholly against the living's philosophy of using models, and that encourage the behavior the living keeps steering against. They are replaced by a corrected version. A draft of the open-source stack, wholly self-authored, says what changes from the default harnesses' prompts. That draft is honest about how the living works. It asks the living how they see work, law and behavior, which today live in seed form in the skills and the vision. A rule specific to one model or harness, such as stopping on a classifier refusal, is not spirit, because spirit is universal. It goes in that model's or harness's own core part of the system prompt. The research into harnesses that did replace the system prompt is completed.

**Conflicts.** T4 (replace the harness system prompt, against keeping harnesses as stock as possible). T13 (datom and ethos syntax in these files, 2026-09-25, against datom only where a program needs it, 2026-09-27).

---

# Vision/skills.md (new topic)

## 22. Vision is skill

- **Decision:** new
- **From:** CM-1
- **Existing touched:** none
- **Quotes replaced:** 11 (847 words): 1.3.1, 1.3.5, 1.3.8, 1.3.11, 1.3.18, 1.3.20 p1, 1.3.22 p1, 1.3.25 p1, 1.3.26 p1, 1.3.32, 1.2.1 p2

**Text.** Vision is skill, and there is no separation between them. A distilled vision file is a skill, so writing vision is writing a skill, and vision distillation is skill editing. The vision data is written once, in the place Curriculum generates the skills from. The vision holds every detail an implementation needs. The skill is its concentration: the part one must know to understand the concept. The effort that went into writing skills belongs in reinforcing the distilled vision with actual code: the ethos, the Rust expected from it, and the invariant Rust that compiling an ethos or a Nexus executable yields. That way the flows touching a topic read it up front and in one place. Where a skill conflicts with the current distilled vision on the same topic, a path runs from the vision to a proposed update of the skill. This vision is what should carry the most important context a model is given.

**Conflict (untagged).** 2026-08-30 and 2026-09-14: a skill differs from the vision. 2026-09-16 onward: they are one and the same.

## 23. Skills live in the three aspect repositories

- **Decision:** extends
- **From:** CM-3
- **Existing touched:** `Vision/psyche.md`: "The skills belong in a repository. This is a target shape, not authorization to create or migrate a repository" (landed 2026-09-18, from 8393ca). Also "Psyche data belongs in a dedicated repository symlinked into Primary ..." (consistent, unchanged).
- **Quotes replaced:** 11 (717 words): 1.3.3, 1.3.4, 1.3.12, 1.3.13, 1.3.14, 1.3.15 p2, 1.3.20 p3 (first two sentences), 1.3.23, 1.2.8 p1 and p2, 1.2.9 p2, 1.2.12

**Text.** Curriculum does not hold the skills. It is only the executable source that regenerates them. Its code is kept apart from the skill data, so that a change to a skill does not rebuild it. The skill data lives in three repositories, one per aspect: psyche, mind and field, each named for its aspect. A repository has one type, assigned to it and controlled centrally, so which type comes from which repository is fixed. The psyche repository holds vision, intent, spirit and notion, and nothing else. Mind's and field's repositories hold theirs, and each may separate its own levels by directory, among them operation and documentation. Beside each skill repository stands a logs repository: psyche logs, mind logs and field logs. It holds the raw records under their flow ids, so the distilled part stays apart from the raw. The logs repositories are symlinked into the workspace, and a small Clojure executable searches the raw vision across all three. The skills are loaded into Curriculum's database typed by their aspect, with each aspect's sub-variants (psyche's are vision, intent and spirit). The generator prefixes each skill from its payload. The three repositories exist so that the agents of an aspect can easily edit the skills that pertain to them. The primary workspace is a bare template that expects these repositories mounted in it. This is a target shape, not authorization to create or migrate a repository.

**Notes.** The last sentence keeps the existing statement's condition. The statement moves from `psyche.md` to `skills.md`. Conflicts: T1 (2026-09-17, "Curriculum skills are good for now", against 2026-09-29 and 2026-10-03, which take skills out of Curriculum into three repositories). Untagged: one Psyche Skills repository with directories (2026-09-28), against three repositories.

## 24. One topic, one family of skill files

- **Decision:** new
- **From:** CM-4
- **Existing touched:** none
- **Quotes replaced:** 6 (551 words): 1.3.6, 1.3.7, 1.3.20 p2, 1.3.22 p2, 1.3.26 p2, 1.3.27

**Text.** A topic does not have a skill and a vision side by side. It has one family of skill files:

- Its core, named by the topic alone, is the vision an agent loads first.
- An extended file carries the rationale and the general aspect of the topic.
- A subtopic file, named by its subtopic, gives an extensive view of one aspect.

A vision too big for one file breaks into subsections that become their own skill files, so an agent loads only the layer it needs. The generator gives each kind a deterministic name: rationale, subject rationale, subject extended, subject experimental, subject undecided proposal, notion, vision. Every skill that touches a piece of work sits under its proper prefix. A distillation is split across the skills it concerns, not put into one.

```
datom              ; the core: the vision of datom, loaded first
datom-extended     ; rationale and the general aspect
datom-<subtopic>   ; one aspect, in full
```

**Notes.** No record says how rationale and extended differ. Untagged: whether skill generation moves into Harness (entry 27).

## 25. Each aspect edits its own skills

- **Decision:** extends
- **From:** CM-13
- **Existing touched:** `Vision/psyche.md`: "Operational vision skills use the `operational-` prefix and support faster iteration with an overview to the living. Testing skills use `testing-`. Pure vision skills use neither prefix." Also "Unprefixed vision is Psyche's most reliable, accepted gold." Both landed 2026-09-18.
- **Quotes replaced:** 3 (239 words): 1.3.15 p4, 1.3.16, 1.3.21

**Text.** Each aspect is in charge of its own skills, and the instructions on changing skills say where an agent's reach stops. When an agent sees a need to change a skill of another aspect, it messages that aspect, which weighs the suggestion on its merits. Psyche brings a suggestion bound for psyche to the living. The golden skills, unprefixed and the most trusted, live in their own repository, and changing them takes more approval. Operational skills are the ones agents write for themselves, to help with their tasks without disturbing the psyche much. They live in their own repository under the `operational-` prefix, and they support faster iteration with an overview to the living. A human reviews them less and they are trusted less. They are good guidelines and good to know, and they are more likely to be taken out than vision, because that knowledge need not be carried forever. Testing skills use `testing-`.

**Notes.** These lines move from `psyche.md` to `skills.md`. T23: whether operational skills are mind's (2026-09-24, entry 26) or a separate set written by agents (2026-09-17). Untagged: `testing-` as a prefix (landed 2026-09-18) against testing as a notion (entry 26, 2009-09-24). The installed tree uses `trial-`, which is state, not the living's word.

## 26. Skill types: vision, operation, compensation, usage

- **Decision:** new
- **From:** CM-14
- **Existing touched:** `Vision/psyche.md` "Testing skills use `testing-`" (see entry 25)
- **Quotes replaced:** 2 (234 words): 1.3.17, 1.3.25 p2

**Text.** Skills are typed by the layer they come from:

- Vision describes what is wanted.
- Operation, mind's, is what is being worked with.
- Compensation, field's, is what is welded in place for now to make the system run, like a hotfix. It is owed a proper implementation designed in the psyche.
- Testing, putting something in live to see if it works, is a notion. It becomes compensation once it holds.
- Usage skills say how to use something, a tool, with the language to speak to it.

These are the main layers, probably with some above and below. They do not always form a total hierarchy, and field holds domains of its own. Some knowledge, mind, is hooked into skills beside the vision. Each type comes from its own place.

**Conflict.** T23: this list (2026-09-24) against vision, intent, spirit, knowledge, operation and role (2026-10-03, entry 19).

---

# Vision/curriculum.md (new topic)

## 27. Curriculum, the typed generator

- **Decision:** new
- **From:** CM-8
- **Existing touched:** `Vision/flowNexus.md` "Repository and skills" (skills live outside the flow repository so that a skill change causes no Nix rebuild; same principle as entry 23, unchanged)
- **Quotes replaced:** 6 (447 words): 1.2.2, 1.2.6, 1.2.7, 1.2.9 p1, 1.2.15, 1.3.15 p1

**Text.** Curriculum is a binary: a nexus with CLIs that regenerates the skills. It takes the repositories it is given and recognizes their special files. Among them are the Nix entry point and a datom configuration such as `config.datom`, for which Curriculum defines its own ethos object. The skills are typed, never copied by directory name. The nexus has a fully typed specification of every input it takes: a schema, perhaps in a datom file fed in through the CLI and turned into a signal to the generator. Every source signal can be its own repository, taken as a dependency. A nexus library handles the rebuild: it regenerates the ethos and rebuilds the CLI when a dependency or a source signal's ethos changes. Any type of skill can be generated from more than one source. People can therefore write their own knowledge skills and take others' knowledge or vision skills like plugins, with vision they share and vision they keep for themselves, and the same for every other type. Curriculum generates whatever skills are present.

**Notes.** No record gives the fields of `config.datom`, so the statement owes example code once the type exists. Conflicts, both untagged: on scope (2026-09-20, "just a binary"; 2026-09-24, "revamp everything"; 2026-09-16, "becomes a nexus"; 2026-09-18, perhaps rewritten into Harness). On the manifest: no manifest, generate whatever is present (2026-08-21), against a registry with dependencies (2026-09-29, entry 31) and Flow's registry (2026-10-03, entry 12).

## 28. One source, emitted per harness by `{%` templates

- **Decision:** new
- **From:** CM-17
- **Existing touched:** none
- **Quotes replaced:** 3 (116 words): 1.2.1 p3, 1.2.13, 1.2.14

**Text.** A skill is written once. Curriculum emits it into the workspace for each supported harness, regenerating modified skills and adding missing ones. The blocks that differ by harness are written in the Markdown templating language. A template is triggered only by `{%`, so it never collides with skill text. The skill on designing skills says the template syntax exists, and nothing more is needed: there is no checker.

```
{% if claude %}
Text only Claude's tree receives.
{% endif %}
{% if codex %}
Text only Codex's tree receives.
{% endif %}
```

## 29. Setup variables

- **Decision:** new
- **From:** CM-18
- **Existing touched:** none
- **Quotes replaced:** 1 (43 words): 1.2.18

**Text.** A value that differs between setups has a name and is not part of Curriculum. Curriculum's documentation tells agents that such values must be set, and how.

**Conflict.** T22, where the values live: their own setup-specific file (2026-08-17), against knowledge-type skills (2026-10-03).

---

# Vision/harness.md (new topic)

## 30. A standard, Nix-defined harness home

- **Decision:** new
- **From:** CM-16
- **Existing touched:** none
- **Quotes replaced:** 2 (165 words): 1.4.1, 1.4.2

**Text.** Every new Claude or Codex home gets a standard set of settings, all of them, set automatically with Nix. They may come from a repository of their own that also documents the options each harness offers. With it a home can be stood up whole, even as a semi-sandbox that uses a copy of the living's tokens to test things. How subagents work is understood harness by harness, and the open-source harness is set up.

**Conflict.** T4 touches this entry (see entry 21). 1.4.4 stays verbatim.

---

# Vision/psyche.md

## 31. The psyche's hierarchy: distilling upward, depending upward

- **Decision:** extends
- **From:** CM-11
- **Existing touched:** `Vision/psyche.md`, line 3: "Psyche contains Spirit, Intent, Vision, and Notion, in descending authority." (landed 2026-09-18)
- **Quotes replaced:** 3 (300 words): 1.3.24, 1.3.28, 1.2.5

**Text.** Psyche contains spirit, intent, vision and notion, in descending authority. Distillation is the psyche's output: the psyche is always distilling vision or intent. Things move up by repeated distillation. Vision is distilled often, intent is distilled out of vision, and spirit out of intent. Vision is what is seen clearly enough to try now. Intent is where the project is going. Spirit is how everything is approached: how the work is done and how one behaves. Notion sits below vision. Distilled notion, less committal, keeps clear what might be wanted but is not yet decided, and it is owed too.

The same hierarchy governs dependency, which is kept in a registry of everything. A module depends only on what is above it or on its own kind: a vision on another vision, an intent or the spirit; an operation on a vision or higher; and so on, down through documentation and operation to trial at the bottom. Each variant is an ethos struct that holds the skill's text as one field beside its metadata: title, description, whether it is visible to the user or the agent, and its dependencies.

```rust
// illustrative: the fields named, not a ruling on their types
pub struct Skill { pub title: Title, pub description: Description, pub visibility: Visibility, pub dependencies: Vec<SkillName>, pub text: Text }
```

**Notes.** 1.2.5 says one level of field's hierarchy was forgotten, and the statement does not fill it in. The registry here sits against "no manifest" (entry 27).

---

# Vision/distillation.md

## 32. A distillation proposal is tangible

- **Decision:** extends
- **From:** CM-12
- **Existing touched:** `Vision/distillation.md` "A proposal names each statement's destination" (landed with b675f3d9 and acbb6006, from records of August 2026)
- **Quotes replaced:** 3 (244 words): 1.1.12 p1 and p4, 1.3.31, 1.3.36

**Text.** A distillation proposal is tangible. It says which module, which edit, what is removed and what replaces what. For every statement it names the topic it goes to, and a statement under the wrong topic is corrected by a distillation edit of its own. A proposal distills with the distillate: it reads the distilled vision it would land in, not the raw records alone. One subject gets one unified statement. Nothing in a proposal is vague, padded or supposed. What is not known is found out, not guessed and passed off as known. A report that only lines up what was said, one record after another, and never makes a point is not a proposal. Every flow distills the same way, by the skill.

**Conflict (untagged).** 1.3.36 (2026-08-19, one unified statement for one subject) against 1.3.37 (2026-08-19, the same record: calling a distillation one statement that replaces a set of records is a falsehood). 1.3.37 stays verbatim.

## 33. Distillation rolls as the work goes

- **Decision:** new
- **From:** CM-5
- **Existing touched:** none
- **Quotes replaced:** 5 (540 words): 1.2.1 p1, 1.3.9, 1.3.10, 1.3.29, 1.3.30

**Text.** Distillation rolls as the work goes. Whenever a topic involves gathering vision, the raw vision it touches is distilled then, with subagents sent to gather everything that even remotely touches the subject. At every second or third turn, an agent proposes distilling what has accumulated. Raw vision is not left to pile up, go stale and contradict itself as the living's mind changes. The living's first expression is rough, and several passes make it clean. The output reaches the living as a constant flow of concise proposals, small enough to answer yes quickly:

- a new skill
- an edit or addition to a skill
- a skill added to or removed from the dependencies of another skill or of a subagent definition

Each aspect that a matter concerns makes its own proposal. A subagent is a type of skill, one implemented by a fresh flow. Most proposals edit a skill that already exists.

**Conflicts.** T20: 2026-09-03 (just keep logging) against 2026-09-12, 2026-10-01 and 2026-10-03 (distill as we go). Untagged: a full document from the vision-distillation role (entry 7, 2026-09-25) against small, concise proposals.

---

# Vision/livingMessenger.md (new topic)

## 34. The living messenger: the book

- **Decision:** new
- **From:** BP-16, BP-19 and the first sentence of BP-14 (merged). BP-19's proposed `Vision/vocabulary.md` is not created, because the term is defined here, where it is used.
- **Existing touched:** none
- **Quotes replaced:** 6 (354 words): 5.1.10, 5.1.12, 5.1.13, 5.1.15, 5.1.29, 5.1.31

**Text.** The living messenger is the user interface through which machines speak to the living: the book. What the living reads is not called a page. When the living says page, a book is meant, and a booklet is a short book. Book is not quite the right word either, and for now the book is a poor user interface. The living reads the books, not the chat, so what does not become a book most likely never reaches the living. A flow that answers the living answers in a book. A machine that talks to the living only through its chat has failed.

**Conflicts.** T12: "just call it a page" (2026-09-28); book or booklet, never page (2026-09-29); book is not right either (2026-10-02). Untagged: "I only read the presentations" (2026-10-02) against "a little bit of the chats" and "maybe you just tell me now here" (2026-10-02).

## 35. A main flow's presentation becomes a new book

- **Decision:** new
- **From:** BP-3
- **Existing touched:** none
- **Quotes replaced:** 5 (603 words): 5.1.11, 5.1.24, 6.1.6, 5.1.27, 5.1.32

**Text.** A primary-layer flow's most important work is its view of a thing, and its presentation of that view is its main output. Whenever a main flow speaks to the living, it marks that block as meant for the living at its beginning and at its end, in an agreed pattern that a tool can detect. The marks need not render. Everything else the machine writes stays mechanical and log-like, so prose addressed to the living stands out. Keeping the presentation simple is the main flow's own job. It passes the marked block a layer down, to a subagent, which makes a book of it. It is always a new book, because a book the living has commented on keeps its comments when edited, and they no longer apply. That subagent knows the psyche. It checks the presentation against the psyche and puts small, specially colored notes where it strongly agrees or disagrees, naming the psyche record and its age.

**Notes.** "Sonnet subagent" becomes "a subagent a layer down" under the layer rule. Untagged: 5.1.24 (blocks may update an existing book) against 5.1.11 and 5.1.27 (always a new book).

## 36. Flowcharts

- **Decision:** new
- **From:** BP-2
- **Existing touched:** none
- **Quotes replaced:** 8 (634 words): 5.1.7, 5.1.9, 5.1.14, 5.1.16, 5.1.22, 5.1.38, 5.1.39, 5.1.41

**Text.** The living wants many visuals and fewer long paragraphs, and above all well-made flowcharts. A flowchart is drawn in SVG and rendered, readable on a phone held upright without zooming. It is enriched beyond black-and-white boxes and arrows. A model good at SVG gives it expressive power, judges its size and its kinds of arrow, and brings out its meaning the way syntax highlighting brings out code. Mermaid is not used, because the living cannot read it. The book skill carries distilled guidance that reliably yields such flowcharts, tuned in trials the living rates.

**Notes.** The model name is taken out. Impurity discarded: 5.1.38's third-person relay additions (CSS Grid, container queries, a headless screenshot check). Conflict: T11 (ASCII or Mermaid, 2026-09-16 and 2026-09-18, against SVG and no Mermaid, 2026-10-02 and 2026-10-03). Untagged: the relayed screenshot check against "no screenshots of the book" (5.1.23, which stays verbatim).

## 37. Illustrations convey information; three levels of book

- **Decision:** new
- **From:** BP-4
- **Existing touched:** none
- **Quotes replaced:** 6 (468 words): 5.1.20, 5.1.30, 5.1.35, 5.1.36, 5.1.37, 5.1.40

**Text.** An illustration conveys information or is left out, and prettiness is no reason for one. The base of every visual presentation is a Markdown report with flowcharts. A book is made at one of three levels:

- the plain report with its flowcharts and no generated image
- the report with AI-generated illustrations
- the report whose drawings are themselves redrawn handsomely, so that it comes alive

To illustrate, a model adds an illustration module and chooses where each illustration goes. The result is the illustrated book: flash book, picture book and photo book name the same thing. A flowchart that a model stylizes and sets beside prose is an illustrated flowchart. The low-power level comes first and keeps improving. The Markdown payload is read structurally: headers and subheaders map to sections and subsections in an ethos and datom spec.

**Conflict.** T11 (see entry 36). Which level is the default today is not said.

## 38. Rendering is mechanical; our own display app

- **Decision:** new
- **From:** BP-14 (its first sentence is in entry 34)
- **Existing touched:** none
- **Quotes replaced:** 2 (218 words): 5.1.4, 5.1.21

**Text.** A presentation that a main flow outputs enters the book pipeline by itself. Rendering is mechanical, so calling a model only to display something is wasteful, and a tool is written for it. Until then Claude artifacts stand in, made mechanically by a cheap subagent at light effort. They are the best there is, and they are poor. The aim is our own display app, a minimal nexus, because driving the harness by remote control is clumsy and a security exposure: whoever breaks the cloud side can order the agents on every machine exposed that way. Alternatives are researched.

**Notes.** "Sonnet" becomes "a cheap subagent". "Light" is the living's word (T17). Impurity discarded: "Unity", kept as heard and unconfirmed.

## 39. The living's questions are gathered into a book

- **Decision:** new
- **From:** BP-13
- **Existing touched:** none
- **Quotes replaced:** 2 (236 words): 5.1.25, 5.1.28

**Text.** The living's questions are gathered in one place, the implied ones too: wherever what the living says carries a need to know, even where speech-to-text loses that it was a question. They are logged as psyche is logged, perhaps as mind logging. They are brought into a book that answers each one, proposes an answer, or asks a counter-question to clarify what the living wants to know. A first presentation on a subject is mostly questions: the presenter's preconception of the thing, the questions it raises, and several scenarios.

## 40. Code, ethos and datom are shown

- **Decision:** new
- **From:** BP-18
- **Existing touched:** none
- **Quotes replaced:** 2 (173 words): 5.1.1, 5.1.19

**Text.** Where code logic is involved, a presentation shows code, at a high level when the detail would be noise. Almost every presentation shows some ethos and datom, even for what is not yet in production. Ethos is to become how everything is defined and implemented, and this keeps alive the picture of what is being built in it. Ethos and the architecture are also drawn as flowcharts.

## 41. A series of books on the vision

- **Decision:** new
- **From:** BP-17
- **Existing touched:** none
- **Quotes replaced:** 2 (187 words): 5.1.2, 5.1.5

**Text.** A series of books is kept on the vision: everything the living wants, fleshed out to the bones, under subjects, topics and subtopics, and reviewed and corrected in rounds of correction and implementation. The subjects and topics become variants in nexus components such as Mind. A new variant is submitted, approved into the ethos spec, and the whole is recompiled, so Mind is recompiled and its database updated often.

**Conflict.** T10 (see entry 42).

---

# Vision/writing.md (new topic)

## 42. Every statement dense; every book few and simple

- **Decision:** new
- **From:** BP-8
- **Existing touched:** `Vision/highLevelView.md` "A view takes room" (landed 2026-08-27; adjacent, unchanged); `Vision/distillation.md` "A statement carries what the psyche said" ("A small ruling makes a small statement"; consistent)
- **Quotes replaced:** 4 (395 words): 5.1.6, 5.1.26, 5.1.33, 5.1.34

**Text.** Writing for a model is programming it, so every statement, at every layer, is dense, compact and minimal. A statement is a statement, not a novel elaborated in every direction. Intent is broad and never a detailed proposal. Skills are written the same way, and conciseness is trained into agents, who reach for length at every chance. A presentation to the living shows a few central, simple concepts, directly and visually, without showering the living with data. A round of books is small, about one per aspect, around three. Titles are plain, never convoluted.

**Conflicts.** T10: few, simple concepts (2026-09-30) and every statement minimal (2026-09-25), against everything fleshed out "to the bones" (2026-10-03, entry 41). Untagged: "a high-level view takes room and breaks everything down in-line" (`highLevelView.md`) beside "not showered with data".

## 43. A thing found wrong is no longer said

- **Decision:** new
- **From:** BP-11
- **Existing touched:** `Vision/distillation.md` "No useless negatives" (consistent, unchanged)
- **Quotes replaced:** 3 (322 words): 5.1.8, 8.1.4, 8.1.5

**Text.** Once a thing is found wrong, it is no longer said, not even as context. Repeating a wrong association keeps it alive, and that is the main flaw of these models. A design describes the thing designed, never what went wrong on the way: not the hallucinations, and not the unclear words that needed correcting. A correction never becomes part of the spec. A book that opens on a discarded error makes the living think the error is its point, and the living stops reading. History lives in a chronology, which most flows do not read, because creating needs only the freshest, truest version. This is killed in the system prompt.

---

# Vision/speakingToTheLiving.md (new topic)

## 44. Find out, then tell; never ask the living where things are

- **Decision:** new
- **From:** BP-12
- **Existing touched:** none. Entry 32's "what is not known is found out" is the distillation case of the same rule and is kept there, scoped to proposals.
- **Quotes replaced:** 4 (297 words): 8.1.1, 8.1.11, 8.1.12, 8.1.13

**Text.** What can be found out is found out, then told. Coming back to the living with "we don't know" is the wrong behavior. The living is never asked where things are: files and locations are not the living's field, and the living works from a phone through remote sessions. How a thing works is not the living's ruling. It works the way it works, and only the code answers it. What the living is asked is what the living means, in clear, simple questions. The harness system prompts give every incentive to admit not understanding and to seek clarity, rather than to talk around it in complexity, though the pre-training will keep pulling the other way.


## 45. The living is not written to as machines write to each other

- **Decision:** new
- **From:** BP-15
- **Existing touched:** none
- **Quotes replaced:** 4 (197 words): 8.1.7, 8.1.2, 8.1.3, 5.1.18

**Text.** The living is not a machine and is not written to the way machines write to one another. What is told to the living is explained, never left as a shorthand status, and a vague paragraph is rewritten until it is clear. Vagueness repeated from machine to machine wears away the reasoning behind it until hallucination replaces it, and it leads other machines to act on too little. What voices send each other carries no hashes, timestamps or other useless matter.

**Notes.** "Seats" (8.1.2, 8.1.3) becomes "voices" under entry 1.

---

# Vision/judgment.md (new topic)

## 46. Judgment is sized to its call; judging and doing are split

- **Decision:** new
- **From:** BP-5. Its opening clause went to entry 52, and its dead-flow example went to entry 14.
- **Existing touched:** none
- **Quotes replaced:** 5 (475 words): 6.1.5, 6.1.7, 6.1.9, 6.1.10, 6.1.11

**Text.** Judgment is sized to the call. Some work wants almost none. Creating a session takes at most a tiny, fast, nearly free judgment call, like the judge that decides whether data fits the database. Where a result is plainly typed, as when a flow's last response is clearly a datom final response, reaping it needs little judgment: that flow checks for a replacement and, if there is none, tells field to consider a continuation. Where much judgment is needed, a strong model does the work in a subflow. Auditing work against the vision is one such case: it scans the latest raw psyche and gives recency more power. Judging and doing are split: a careful model judges, and its yes authorizes a cheap model to do the now trivial act. Where code cannot tell what is what, as in repairing a record, a thinking machine decides.

**Notes.** Model names are taken out (Terra, Opus, old Opus, Luna, Astra, Sol).

---

# Vision/quotas.md (new topic)

## 47. Quota is spent to a rhythm

- **Decision:** new
- **From:** BP-1
- **Existing touched:** none
- **Quotes replaced:** 5 (696 words): 5.1.3, 7.3.3, 7.3.4, 7.3.9, 7.3.10

**Text.** Quota is spent to a rhythm. Each stack, Claude and Codex, is used at about a seventh of its week's allowance a day, so the two meet at the end of the week. The five-hour window is the gauge of fair use for each, and an overused primary layer falls back to the secondary. When the hourly or daily share goes unused, light work runs to keep concepts materialized and testable, because unused quota is lost, and a reset close at hand may be used up harder. When one stack runs high, work on it waits at design while the other carries more. Secondary-layer main-flow jobs drive proofs of concept when Codex is idle, and the lower layers take the small and trivial jobs. Priority goes to the core and the primary layer, which agree ideas and proofs of concept before the secondary implements them at scale. A proof of concept now is preferred to escalation, and a later version changes what is disliked. What flows spend talking to one another is watched, and books are redone by the lower layers. The slack is counted for the system to decide when to start flows, not for the living to read.

**Notes.** The model names are mapped to layers by the agent: Fable to the primary, Opus to the secondary, Sonnet and Haiku to the lower layers. Impurity discarded: 7.3.4's garbled closing ("4, so it's uploading onto codex"). Conflict: T18. Untagged: entry 17.

## 48. One call for every quota, checked on events

- **Decision:** new
- **From:** BP-6
- **Existing touched:** `Vision/nexus.md` "Polling is forbidden" (cited; BP-6's "never by polling" is dropped as a duplicate)
- **Quotes replaced:** 5 (463 words): 7.3.1, 7.3.2, 6.1.3, 7.3.7, 7.3.8

**Text.** One CLI call returns the full breakdown of all the living's subscriptions and quotas. It comes from a simple nexus component that queries Claude and Codex, designed after prior attempts by others. Any flow can ask it, learn its own quota, and tell the living. Quota is checked on an agent's events, pushed through a hook with no model, because nothing needs checking while no agent runs. The hook attaches the quotas, with a timestamp, to the next message a model receives, so the model never stops. It also adds a few precomputed metrics, such as time left and the recent burn rate. The accounting supports several subscriptions and says whether each provider is in high-power or low-power mode.

---

# Vision/committing.md

## 49. Commits go through one queueing nexus

- **Decision:** new
- **From:** BP-7
- **Existing touched:** `Vision/committing.md` "A commit names its files" (see entry 50)
- **Quotes replaced:** 3 (371 words): 7.2.1, 7.2.4, 7.2.7

**Text.** Agents commit through one simple nexus, used in place of raw JJ and Git commands. It speaks our own version-control language, offered as an API to the other nexuses, and it makes every commit atomic, so agents working on one thing at once never clobber each other's work. A call waits for the commit ahead of it to land, be pushed and move main. Then, if nothing conflicts, it is rebased and goes through. Changes queue for merging. A reserved place lets a flow keep working. A flow without one is told what to rebase on to earn one. A place held past its time is investigated. Publishing is queued by this tool.

**Conflict.** T19 (see entry 50).

## 50. One shared tree; a commit takes what is in it

- **Decision:** conflicts
- **From:** BP-10
- **Existing touched:** `Vision/committing.md` "A commit names its files" (landed 2026-09-20 from f38926 and b81560, records of 2026-09-19 to 2026-09-20)
- **Quotes replaced:** 3 (330 words): 7.2.2, 7.2.3, 7.2.6 (only once the living rules)

**Side A, existing (landed 2026-09-20; records of 2026-09-19 to 2026-09-20).** The commit call is explicit with file paths. A flow commits the files it edited, and usually works only in its own flow directory. A commit made without paths takes the whole working copy, and is made only while the whole repository is locked, when nobody else may be editing.

**Side B, candidate (records of 2026-09-22 and 2026-09-29).** Primary is one shared checkout. Every flow works in the same tree, with no work trees and no second checkouts, because every subflow must see the same psyche database, and a flow needs only its own flow-id subdirectory. A commit takes the changes in the tree, including what others left uncommitted. Committing only selected files is where changes are left behind and lost.

**Notes.** Not resolved. Side B is later, but 7.2.2 says the living may still be missing a flow by which changes are lost, so the understanding that day was provisional. The "no work trees, one shared checkout" half does not contradict side A and could land alone if the living splits it. T19: the handover's account of a field flow that publishes named paths from its own clone is state, not the living's word.

---

# Vision/permissions.md (new topic)

## 51. No manual approvals

- **Decision:** new
- **From:** BP-20
- **Existing touched:** none. `CLAUDE.md`'s rule that no agent message authorizes permission changes is unaffected: this is the living's own word, and a flow acts on it only by the living's direct word.
- **Quotes replaced:** 1 (72 words): 7.1.2

**Text.** The living does not approve commands by hand. The living is training the machines to behave, so what a flow means to do, it is allowed to do, while the system is still being changed in deep ways.

---

# Intent (enters only on the living's explicit word)

## 52. Deterministic work is done by code (`Intent/deterministicWork.md`, new)

- **Decision:** new
- **From:** BP-9, plus BP-5's opening clause (merged)
- **Existing touched:** none. 6.1.13 (mechanical tests do not create ontology) stays verbatim as the counter-case.
- **Quotes replaced:** 5 (348 words): 6.1.1, 6.1.2, 7.1.1, 6.1.8, 6.1.12

**Text.** Whatever is deterministic is done by code, never by a model. A thinking machine is for judging. Mechanical work that a cheap program can do costs context, money and noise when a model does it, and models do it badly. A flow is handed what a program already knows, such as its flow id, in its prompt, rather than made to look it up. Where flows scramble at mechanical work, tools are built for them, by Codex if need be, in place of shell scripts passed between flows. The flows are crippled by the lack of such infrastructure. Models carry the work for now while logic grows to take it over, and the datom language that the nexus CLIs speak is the way there.

**Notes.** On 2026-10-03 the living asked for this to be developed into intent (`flows/5578cc/vision/flow.md`). The wording still needs the living's approval.

## 53. Better models, not higher effort

- **Decision:** duplicates
- **From:** FL-10 (core)
- **Existing touched (cited):** `Intent/models.md` "Better models, not higher effort" (landed 2026-09-18): calls go out at medium effort by default, and effort is never raised to buy quality, because raising it costs a great deal and changes little.
- **Quotes replaced:** 2 (195 words): 2.3.21, 2.3.31. They are archived against the existing Intent statement and entry 17.

**Text.** Dropped: every harness call goes out at medium effort; effort is not raised to buy quality; better AI comes from better models. The rest of FL-10 is in entry 17.

**Conflict.** T17: medium for everything (2026-09-13, 2026-09-18), against the quaternary at low effort (2026-10-03). `Intent/models.md` says "light", and the living's records use both light and low.

## 54. Two scales: effort and layer

- **Decision:** replaces
- **From:** FL-4 (layer words against effort words) and FL-10 ("the power words the living uses are layer ranks, not effort")
- **Existing touched:** `Intent/models.md` "Two scales share the words high and medium" (landed 2026-09-18): "The harness's model-effort setting is one scale. The naming of a flow's tier is another. A flow named high is named by tier, not by effort setting ..."
- **Superseded by:** 2.3.5, 2.3.6 and 2.3.15 (2026-09-26 to 2026-10-03). The layer words replace tier and power words, and they do not overlap the effort words.
- **Quotes replaced:** 0 (counted in entries 1 and 53)

**Text.** The harness's effort setting is one scale. A voice's layer is another: a rank of authority, from primary through secondary and tertiary to quaternary. The layer words do not overlap the effort words. A flow that reads its layer as an effort setting has misread it.

**Notes.** This changes Intent, so it needs the living's explicit word.

---
