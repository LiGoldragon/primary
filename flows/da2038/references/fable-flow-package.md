# Flow hand-over package for the Flow design book

From Psyche Flow Secondary da2038 to the Fable Core Primary 39bd0c. The package is self-contained. The living's words are in the companion file fable-flow-psyches.edn, sent as psyche. Everything below is da2038's account: each fact states where it was witnessed (by Field 42265e, by a da2038 subflow, by da2038 reading), and da2038's own inference is marked as such. Hashes are shortened to six characters. The text of books 5 and 6 is copied as published, with one change: a commit hash is cut to six characters.

## 1. Flow as it stands

Production. Flow 0.34.4 (commit d0f6f0) runs on Ouranos together with Message 0.19.1 (Field witness, receipt in Field's flow-evidence for 0.34.4). Production Flow does these things:
- A seat that is not running keeps no harness. When a Claude seat's turn ends and Herdr shows the harness idle, with nothing in its queue, the harness is closed; the transcript and the address stay, and the metaflow becomes Asleep. Only resumable Claude seats sleep; a Codex seat does not sleep yet.
- A request that reaches an Asleep metaflow wakes it. Defaults in code (WakePolicy): an order, a question or the living's words wake it; a result or a notice waits in the queue; a Primary never wakes automatically. The queue is durable and first-in-first-out; the whole queue is handed over in the first prompt. The wake is durable across a restart of Flow.
- A wake resumes the old Claude session when its recorded context size, read at each Stop, is below the layer's refresh threshold; otherwise it starts fresh. A flow that was Retired is never resumed. A duplicate guard refuses a second pane for one session.
- The native proof, witnessed by Field: the same flow, native session and pane were recovered at startup after a stuck wake; the queued order was delivered once; the seat answered, went Asleep, the queue was empty and the pane gone. The proof was staged across a restart; it is not one fresh full cycle on 0.34.4.
- Identify finds the caller's pane when only HERDR_PANE_ID is set, by resolving the Herdr session from the Herdr server ancestor of the process. After a Herdr upgrade, panes cannot be resolved until the Herdr server restarts.
- A launch registers the Address, and the launch itself records the metaflow Awake as the launched flow, when the native binding is witnessed and before the first prompt; the first-prompt brief carries the task; there is no marker-only first turn. A refused launch closes its pane and gives the Address back. A Start naming the model by an alias such as haiku is ambiguous; the Start must name the exact native id such as claude-haiku-5-5 (da2038 decision).
- The Terra model is removed from Flow. The model of each layer is configured over the meta wire; a whole-Nexus Reconfigure exists. Production configuration: Sol and Luna on the OpenAI side, Quaternary haiku at medium effort.
- Flow's SIGTERM handling: a clean stop; a store flagged as needing recovery is recognized through a repaired temporary copy; a socket is cleaned when stale and refused when live.

Main. Flow main is 80df5f (0.35.0, the direct starter), with signal-flow b619ea and meta-signal-flow e9ec03; the Curriculum schema in Flow is byte for byte Curriculum main 691852. Main also holds, from before 0.35.0: pane titles of the form { Psyche core Tertiary 7c89aa } (aspect and layer capitalized, topic uncapitalized) and a fresh wake that reuses the Address's stored Start system bundle (0.34.5, 0.34.6; the activation of these was requested from Field).

Activation of 0.35.0. Field rolled the activation back: Flow 80df5f fails to decode the table flow_nexus_launch_attempts of the production store, because the table is not migrated. Production stays on 0.34.4. The fix, 0.35.1, is in progress as a migration that opens a copy of the production store and reads every row of every table; a change to stored types is accepted only after it passes that proof. The Field adapters for the new Start and the context-v2 declarations are ready; native trials wait for the paired Home cutover of Flow 0.35 and Curriculum 691852. The adapter oracle (Flow's parser run on Prometheus: requests, replies, refusals, harness-scoped leave-outs) passed.

Order in force. A fresh Mind Astra metaflow takes Flow to production; da2038 hands it the starter work and branch state on arrival. Field is preparing the Astra; its birth waits on the 0.35.1 fix. The living's words about it (Flow merged, deployed, in production; heartbeat; reports on major Astra efforts; respecification from flow definitions in a datom dialect specified in Ethos) are in the psyches file, last entry.

Rule for builds. Every build and test of Flow runs on the remote builder Prometheus, never on Ouranos; no LSP tool is used on Rust code.

## 2. Open proposals

Book 5 «Flow: sleeping and waking seats» (published, https://claude.ai/artifact/RHpbudqE2dajBhqc488jTA, 5 proposals to vision-flow, with the defaults da2038 built). Ruling state: unruled by the living. Choice 4 is settled in practice by the living's words: a session is resumed when it is not too big (resume below a size threshold), recorded in the psyches file. Production Flow already builds choices 1a, 2a, 3a and 5a as defaults and 4 as resume below the layer's refresh threshold. The question the living asked, what a young context is in ratio, with degradation near 100,000 tokens, is also in the psyches file and remains without a proposal.

Book 6 «Metaflow roles» (published, https://claude.ai/artifact/1bjt3LCT3JDszJZQZ3SGr8, version 2, seven proposals). Ruling state: unruled. Core holds the role-library redo (Field relayed: layout settled as type/subject.md, ids type-subject, terminology metaflow for the identity and flow for one run), so proposals 2, 3, 4 and 6 wait for that redo. The text of the two books follows, proposals verbatim.


### Book 5 text

#### 1. Crystallization: what puts a seat to sleep

Machine: the harness's turn-end report can arrive early or twice, so 1a also waits for an idle harness. A Codex seat lives in a shared server, so closing its pane may free less memory than a Claude seat's; this is not measured.

File: `psyche-context/skills/vision-flow.md`

```text
  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.
+
+ A metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.
  
  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id.
```

1. A metaflow sleeps 1a «as soon as its turn ends and the harness is idle, with nothing waiting in its queue» · 1b «once its harness has stayed idle for a set time, with nothing waiting in its queue; the timer is a poller, registered and reported» · 1c «when it is ordered to sleep». Default: 1a.

#### 2. Crystallization: which requests wake a sleeping seat

Machine: the closed set of request types already exists; 2c is the judgment by a small model that the line above it already describes for the living's own touch on a topic. Proposals 2, 4 and 5 edit one paragraph and merge.

File: `psyche-context/skills/vision-flow.md`

```text
  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; …
- A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A metaflow asleep is woken by an order, a question or the living's words and receives its whole queue, oldest first, in the first prompt, a result or a notice waiting there until a waking; a metaflow under refresh queues what arrives until its successor has started.
  A metaflow a request needs is started whether or not it is running; …
```

2. A metaflow asleep is woken by 2a «an order, a question or the living's words» with the added words «, a result or a notice waiting there until a waking» · 2b «any request», no added words · 2c «a request that a small model judges worth a waking», no added words. Default: 2a.

#### 3. Crystallization: whether a Primary wakes automatically

Machine: two readings of his orders. 3a follows the low-usage order, where every Fable call goes through him: a Primary runs on Fable, so a waking by message spends Fable without his word. 3b follows his record that a Primary is not started without a Secondary: it wakes on a request whenever its Secondary is awake, spending Fable each time that holds. 3c treats a Primary as any layer.

File: `psyche-context/skills/vision-flow.md`

```text
  A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+
+ A sleeping Primary stays asleep until it is started on the living's permission; requests for it wait in its queue.
  
  Flow exposes everything from the harness, the bare input: …
```

3. A sleeping Primary 3a «stays asleep until it is started on the living's permission; requests for it wait in its queue» · 3b «is woken only while its Secondary is awake; requests for it wait in its queue until then» · 3c «is woken like any other layer». Default: 3a.

#### 4. Crystallization: resume the old transcript or start fresh

Machine: whether a resumed Claude session keeps its session id, and so its flow id, is unverified; the build checks it before this lands. 4b uses each layer's existing refresh threshold as the measure of a young transcript, pending his proposal on what a young context is.

File: `psyche-context/skills/vision-flow.md`

```text
  A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; …
- A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A metaflow a request needs is started whether or not it is running; with no transcript kept from its sleep to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
```

4. A started metaflow is fed its context modules and prompt 4a «with no transcript kept from its sleep to reawaken» · 4b «with no transcript below its layer's refresh threshold to reawaken» · 4c «on every waking». Default: 4a, moving to 4b once the proposal on a young context is ruled.

#### 5. Crystallization: what waking holds meanwhile

Machine: the waking runs on a worker, the metaflow locked by a held lease, as a refresh locks it; 5b serves one launch at a time and holds Flow's other deliveries for its length.

File: `psyche-context/skills/vision-flow.md`

```text
  A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; …
- A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh or waking queues what arrives until its successor or woken seat has started, while Flow keeps serving every other request.
```

5. A metaflow under refresh or waking queues what arrives until its seat has started 5a «, while Flow keeps serving every other request» · 5b «, while Flow serves one waking at a time and holds its other deliveries until then». Default: 5a.


### Book 6 text

Machine: a metaflow is one standing topic of work (an aspect and a topic, such as Field publishing). A seat is one running model session in a metaflow, at one layer. A role says which seat runs there: its layer, its model, its skills. Flow Nexus is the program that starts seats. Its meta wire is the control channel it is configured over. Datom is the plain-text data format; ethos is the language that says what shape a datom file has.

Machine: the Publisher is a Haiku seat, so by the present rule it may call only models at its own rung, Haiku, and below. The living asked for one exception: it may call the Sonnet Illustrator, one rung up. A subagent is a model that a seat calls for one piece of work and that has no seat of its own.

#### Proposal 1: A repository for metaflow definitions

Machine: roles and subagents are configuration data, not cluster data, so they leave the cluster repository (goldragon) and get a public repository of their own, typed by its own ethos library. The layout:

- `ethos/role.ethos` the library of types (proposal 2).
- `metaflows/<aspect>-<topic>.datom` one metaflow per file (proposal 3).
- `subagents/<name>.datom` one subagent per file (proposal 4).

Ruling: Name the repository.

a. `metaflow`
b. `metaflows`
c. `metaflow-roles`
d. No new repository.

#### Crystallization

#### Proposal 2: the role library

Machine: a new file; nothing is removed. It imports Flow's shared leaf types (Aspect, Layer, Topic, Key) from `crates/flow-ethos/ethos/library.ethos` and is written in the sweet form of `psyche-context/vision/ethos.md`: the head, then imports, types, traits, associations.

File: `metaflow/ethos/role.ethos` (new)

```ethos
+ Library
+ [ flow:[ Aspect Layer Topic Key ] ] ; imports
+ [ RoleName.String                  ; types
+   SubagentName.String
+   Native.String
+   Effort.[ Low Medium High Xhigh ]
+   Duty.String
+   Role.{ RoleName Layer Native Effort Duty
+          Modules.Vector<Key>
+          Reach.Vector<Native> }
+   Subagent.{ SubagentName Native Effort Duty
+              Modules.Vector<Key> }
+   Metaflow.{ Aspect Topic Contact.Layer
+              Roles.Vector<Role> } ]
+ []                                 ; traits
+ []                                 ; associations
```

Machine: what each type is, and why it is there.

- `Native` is the exact model id the Claude harness takes, such as `claude-haiku-5-5`. A seat's model is written once, in the role, as the harness needs it.
- `Effort` is how hard the model thinks, the same four levels Curriculum already uses.
- `Duty` is one sentence on what the role is for; the seat and the generated file both show it.
- `Role` is one seat of a metaflow: its name, its layer, its model, its effort, its duty, its `Modules` and its `Reach`. A module is a skill, named by a `Key`: a subaspect (Vision, Intent, Knowledge, Operation, Trial or Compensation) and a topic, so the skill `vision-book` is the key `Vision book`.
- `Reach` lists the subagent models the role may call beyond the default. By default a role calls the models at its own rung and below; the list is empty for most roles.
- `Subagent` is a model a seat calls for one piece of work: name, model, effort, duty, modules.
- `Metaflow` is one file's whole content: the aspect and topic, the `Contact` (the layer whose seat every sender reaches), and its roles.

Ruling: Land the library as shown, or not.

a. Land it as shown.
b. Neither; it is redesigned.

#### Proposal 3: the publishing metaflow

Machine: a new file; nothing is removed. The ids `claude-sonnet-5-5` and `claude-haiku-5-5` are read from the usage ledger in `flows/d68c82/reports/flow-context-2026-10-14.edn` and from the layer-model table in `mind-context/skills/knowledge-layer-models.md`. Curriculum's `roles.datom` itself names only the aliases `sonnet` and `claude-haiku-4-5`; I did not find the deployed Flow configuration file, so the ids are not read there. The Publisher's modules are the standing skills the present `book` subagent file is composed with, as listed in `roles.datom`; of that list, `compensation-book-distillation` has no skill file I could find, and `spirit` has no subaspect to key it by (its text already reaches every subagent as the base `spirit-role`), so both are left out. `compensation-messenger-clj` becomes `Compensation messengerClj`, the topic in camelCase.

File: `metaflow/metaflows/field-publishing.datom` (new)

```datom
+ Metaflow.{
+   Field publishing Quaternary
+   [ { Illustrator Tertiary
+       claude-sonnet-5-5 Medium
+       «Draws figures and illustrations for books.»
+       [ { Vision book }
+         { Compensation bookCrystallization } ]
+       [] }
+     { Publisher Quaternary
+       claude-haiku-5-5 Medium
+       «Publishes books; the contact.»
+       [ { Compensation truth }
+         { Compensation orders }
+         { Compensation prose }
+         { Compensation understanding }
+         { Compensation launch }
+         { Compensation design }
+         { Compensation defaultEffort }
+         { Compensation messengerClj } ]
+       [ claude-sonnet-5-5 ] } ] }
```

Machine: the last line is the Publisher's `Reach`: the one exception to the default. The topic word `publishing` is a choice.

Ruling: Land the file, with the topic word.

a. `publishing`
b. `books`
c. `illustration`
d. Neither.

#### Proposal 4: the Illustrator subagent

Machine: a new file; nothing is removed. It is the subagent file the Publisher calls. Its modules are the two figure-grammar skills of the book procedure. The rules for drawing a figure that the book subagent now copies into each figure brief live in `compensation-flashbook-illustration`; 4b adds that key.

File: `metaflow/subagents/illustrator.datom` (new)

```datom
+ Subagent.{
+   Illustrator claude-sonnet-5-5 Medium
+   «Returns an illustration for each book figure.»
+   [ { Vision book }
+     { Compensation bookCrystallization } ] }
```

Ruling: Land the file.

a. Land it with the two keys shown.
b. Land it with a third key, `Compensation flashbookIllustration`.
c. Neither.

#### Proposal 5: Flow reads metaflow definitions

Machine: the Flow Nexus reads a `Metaflow` over its meta wire as `Configure.Metaflow`, and a seat's model comes from its role, so the layer-only `ConfigureModel` is removed. The `Contact` makes a send addressed to the metaflow (aspect and topic, no layer) land on the Contact seat. In `crates/flow-nexus/src/waking.rs`, `start_fresh` now looks up the model by the address's layer in the configured models (lines 947 to 953); it would instead find the metaflow by aspect and topic, then the role at the address's layer, and take that role's `Native`, refusing as it does today when there is none. The lines below are as Flow pins them: `meta-signal-flow` at commit b6f865, read with `git show b6f865:ethos/signal.ethos`, where `ConfigureModel` is at line 103, `ConfigurationChange` at lines 107 to 110 and `ConfigurationSnapshot` at line 111. Two consequences are not settled by this proposal. Every metaflow then needs a definition file, and only Field publishing is written here. Flow already has its own `Metaflow` record in its library (address, state, past, queue); 5b renames the definition type so the two never meet.

File: `meta-signal-flow/ethos/signal.ethos`

```ethos
  …
+ metaflow:Metaflow
  …
- ConfigureModel.{ Layer Native.String }
  …
-                         Model.ConfigureModel
+                         Metaflow
  …
- ConfigurationSnapshot.{ Nexus.ConfigureNexus Models.Vector<ConfigureModel> Thresholds.Vector<ConfigureThreshold> Modules.Vector<ConfigureModule> }
+ ConfigurationSnapshot.{
+   Nexus.ConfigureNexus
+   Metaflows.Vector<Metaflow>
+   Thresholds.Vector<ConfigureThreshold>
+   Modules.Vector<ConfigureModule> }
```

Ruling: Read definitions on the meta wire.

a. As shown, the type named `Metaflow`.
b. As shown, the definition type renamed `MetaflowDefinition` in proposal 2 and here.
c. Neither.

#### Proposal 6: subagent definitions leave Curriculum

Machine: the five role aliases (default, explorer, worker, tester, book) and the six read and write depth descriptions become eleven subagent files in the new repository. Curriculum keeps only generation: it reads each `subagents/*.datom` and composes the file with the skills of its modules. The marked removals are archived apart, not destroyed. Not settled here: the `Subagent` type of proposal 2 has no permission (read or write) and no surface (which harness), which an alias carries today; 6b adds both to the type. Whether the depth ladder and permissions then also leave Curriculum is not proposed.

File: `Curriculum/roles.datom`

```datom
  …
- [ { read trivial «The answer is in one known place. You are fetching it, not finding it.» } { read ordinary «You know what you are looking for but not where it is.» } { read demanding «The answer is written nowhere. Assemble it from how the parts behave.» } { write trivial «The change is fully specified. No decisions remain.» } { write ordinary «The approach is known. Applying it is the work.» } { write demanding «The approach has to be chosen.» } ]
  …
- [ { default write ordinary «General-purpose sub-agent for the Codex orchestrator» [ CodexAgent ] } { explorer read ordinary «Read-only exploration sub-agent for the Codex orchestrator» [ CodexAgent ] } { worker write demanding «Implementation sub-agent for the Codex orchestrator» [ CodexAgent ] } { tester write trivial «Independent testing worker. Given only a bounded target, immutable revision, authority limits, and acceptance contract, choose the procedure, fixtures, negative cases, and independent oracle; return evidence grades and gaps.» [ CodexAgent ClaudeAgent ] } { book write ordinary «Publish a fresh living-messenger presentation from the calling flow's transcript.» [ ClaudeAgent ] } ]
  …
```

File: `Curriculum/curriculum.ethos`

```ethos
  …
- RoleDescription.{ String String String }
- RoleAlias.{ String String String String Vector<Surface> }
  …
- Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> Vector<String> }
+ Roles.{
+   Vector<RoleModule> Vector<Model>
+   Vector<RolePermission> Vector<RoleDepth>
+   Vector<String> Vector<TargetInsertion>
+   Vector<String> }
```

**Archive, on approval:** the five aliases and six descriptions removed above, and the `RoleAlias` and `RoleDescription` types, each into its archive file.

Ruling: Move the subagent definitions.

a. As shown.
b. As shown, and the `Subagent` type gains `Permission` and `Surfaces`.
c. Neither.

#### Proposal 7: how far a role may reach

Machine: the line lands in the vision-flow skill after the paragraph on layers and models, where the layer decides the model. That paragraph says the model is declared once in Flow as configuration; if proposal 5 lands, it is stale and needs its own edit, which is not proposed here.

File: `psyche-context/skills/vision-flow.md`

```text
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+
+ A role declares the subagent models it may call: by default those at its own rung and below; a role may name models above it in its reach.
  
  Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect.
```

Ruling: Land the line.

a. As written.
b. Neither.


## 3. Designs built or in progress

The direct-text starter (on main as 0.35.0, not yet in production). Flow's Start carries the whole task in text. Shape: Start.{ LaunchRequestId SystemModules UserModules Address ModelName Effort Option<FlowId> [RememberedFlow] HerdrSessionName Option<LeaveOuts> InstructionPrompt }. Harness (Claude or Codex), power level and origin are derived: the harness from the model, the power level from the layer, the origin from the caller process by the Nexus. The reply is Launched.{ FlowId SessionId HerdrRouteSelection Origin }.
- Composition. The Nexus asks Curriculum, over its wire, ComposeStartup.{ CallerMetaflow SystemModules UserModules } with a Target (Claude, Codex, Pi or OpenCode); Curriculum answers StartupComposed with the system text, user text, payload hashes (including a rendered hash) and provenance. Modules are named by id, type-subject, and resolve only in the three aspect context repositories (psyche, mind, field); Curriculum owns the closure and the guard. Spirit and intent go only into the system text, never the user text. No composed file in Primary is consumed.
- Guard. In crates/flow-nexus/src/context.rs a VerifiedContext is the only value the launcher accepts: composed text whose hashes were checked. Gap: ethos-zero generates every struct field public and has no visibility syntax, so the type cannot be unforgeable by private fields; ethos-zero refuses concrete types as trait-method inputs (inputs become trait-bounded generics) while outputs are unrestricted (witnessed by a second read of the generator).
- Parts and receipt. The text is delivered as one message over the Herdr socket (1 MiB limit) when it fits; otherwise in parts at module boundaries, each part delivered after the previous Stop and idle. The first topic reply comes after all context. The receipt is the part hashes seen in the transcript plus the first answer at the requested model and effort; there is no READY stage. A receipt error is a refusal, not an ambiguity. The skill-load path, the skill-name vector, native skill selection and ResolveSkills are removed.
- Fresh wake recomposition. A fresh wake reuses the Address's stored Start system bundle and recomposes through the same guard; with no stored bundle it is refused (StartBundleMissing, in main).
- Leave-outs. LeaveOut has 26 variants naming removable parts of the harness's own startup. Defaults per metaflow row, overridden by a call. Nexus refuses leave-outs of ToolSearch and Bash and of UserSettings (indispensable: dropping UserSettings drops the Herdr SessionStart hook). Agreed main-flow default additions: ClaudeMd, GitInstructions, CodexAgentsMd, CodexSkillListing; leave-outs are harness-scoped.
- Store. The store migrates on open; the proof of migration on a production copy is the 0.35.1 work.

Lean flows. Measured with Claude Code: the first request is 26.9k tokens by default and 596 tokens fully lean. A workable lean set (Bash, Read, Edit, Write, Skill) costs 11.2k tokens. Largest parts: tools 21.6k, skill listing 10k, connectors 3.4k, agents 2.8k. Traps: turning ToolSearch off adds 16k tokens; turning Bash off breaks hm-send. Codex is partly measured (the skills listing is about 5.6k tokens). The lean feature is part of the starter branch.

The refresh study. Pilot (Sonnet, three books by four modes, 1.32 USD): resume B 0.193 USD per job; fresh restart per job A 0.220; compact every second job C 0.251; compact every job D 0.338. Output tokens were noise. The Claude CLI cache lives one hour. A fresh start costs 16.5k tokens of fixed context; a warm restart costs about 0.026 USD per job. No quality difference attributable to the mode (judged on the old keep-the-boxes figure rule). The living judged the test flawed (no cache expiry, non-lean fresh starts). The rerun is in progress: lean starts, at least five jobs per mode, with gaps over an hour and with jobs back to back, about 5 USD. Core's desk study (restart per job wins; idle compaction beats cold compaction but loses overall) is a claim da2038 has not witnessed.

Proposed Illustrator refresh path (da2038's proposal, awaiting the rerun): the Illustrator seat is a fresh flow per job. The layer's refresh threshold is set to zero for that role, so the seat sleeps after each job and the next job wakes it fresh with a lean start, instead of resuming a growing transcript. Flow already reads thresholds per layer; setting it per role needs the role definition of book 6 proposals 2 and 5.

Sleep and wake as deployed: see section 1.

## 4. Unknowns and open questions

- Whether the living rules book 5 choices 1 to 5 as defaulted, and what a young context is in ratio (his 100,000-token point).
- Whether the living rules book 6; the role library waits on Core's redo; the repository name; whether the definition type is Metaflow or MetaflowDefinition; whether Subagent gains Permission and Surfaces.
- Whether 0.35.1 migrates every table of the production store; not yet proven.
- Codex seats do not sleep; sleeping needs hooks with a flow id, a transcript reader and resume. A shared Codex server may free less memory on close; unmeasured.
- A message's sender is identified by Herdr pane marks, which a same-user process can forge. The proof was accepted as behavioural, not as sender authentication.
- The cause of the loss of Message route metadata after a Field repair is unknown (fixed in messenger-clj 7985ac, not yet pinned in Home).
- A Start with a model alias is ambiguous; refusing non-exact Claude ids needs a Claude model set in configuration (signal change), deferred.
- Outside consumers of the removed launch marker: persona-test packages message-flow.nix, the sandbox scenario scenarios_late.py, and the signal-flow receipt fields.
- Clippy debt in crates/flow/src/main.rs near line 528 (outside Field's five checks).
- The unforgeable-guard gap in ethos-zero (section 3). Flow declares no traits in Ethos today; hand-written traits stay for now by Core's ruling; the long-term goal is all traits in Ethos.
- Title casing: the living's words lowercase the topic only; Core withdrew a lowercase-everything directive and is asking him about aspect and layer.
- Whether the lean refresh rerun overturns the pilot ordering, and the restart cost with a Herdr launch over gaps longer than five minutes.
- Heartbeat every six hours bringing the important topics back, reports on major Astra efforts, and respecification of Flow from flow definitions in an Ethos-specified datom dialect: designs not yet begun (living's words in the psyches file).
