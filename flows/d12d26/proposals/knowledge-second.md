Presentation.{ «Knowledge: ten seeds, second pass» }

# Knowledge: ten seeds, second pass

Created by Opus, rulings by Fable, seed tests by Astra

### Proposal 1: knowledge:beads · mind-belief › knowledge/beads.md

**Comment** Carried over from the first book as written: Astra's seed test found it sufficient for a flow to work with `bd`.

- Run `bd` from the repository the work belongs to.
-
- ## Fields
-
- `--title` — the outcome, not the activity.
- `-d/--description` — what an agent with no context needs: what is true now, what is wrong, where to look.
- `--design` — how this work is to be done, and why that way.
- `--acceptance` — what makes it done, checkable by someone who did not write it.
- `--notes` — current working state. `bd note <id> <text>` appends to it.
- `bd comment <id> <text>` — separate append-only stream. Comments are events; notes are state.
- `-t/--type` — bug, feature, task, epic, chore, decision, spike, story, milestone.
- `-p/--priority` — 0 highest, 2 default.
- `--parent`, `--labels`, `--due`, `--estimate`, `--external-ref`.
-
- ## Dependencies
-
- `bd dep add <id> <blocker>` — id waits on blocker. Default type `blocks`.
- Types: blocks, tracks, related, parent-child, discovered-from, until, caused-by, validates, supersedes.
- `bd dep add <new> <origin> -t discovered-from` when work uncovers work.
- Beads in another repository are named by id in text. No link crosses databases.
-
- ## Lifecycle
-
- `bd ready` — what can be worked now, blockers accounted for. Start here.
- `bd update <id> --claim` — assignee and in_progress in one atomic step.
- `bd close <id> -r '<proof>'` — the reason carries the evidence; there is no evidence field.
- `bd reopen`, `bd defer --until`, `bd blocked`, `bd query`.
- `--json` on any read command.
-
- ## Store
-
- Verify the selected store before using it.
- Run `bd init` only when `.beads` is absent.
- Run `bd bootstrap` when an existing scaffold has no usable database.
- Use embedded Dolt sequentially: never run `bd` commands in parallel, including reads.
- Wait and retry an embedded-Dolt lock instead of concurrent access.

+ Beads (`bd`) tracks work across sessions and is run from the repository the work belongs to. `bd ready` shows what can be worked now, `bd update <id> --claim` takes it, and `bd close <id> -r '<proof>'` closes it with its evidence in the reason. A bead's title is the outcome, its description what a flow without context needs, its acceptance what makes it done; `bd dep add <id> <blocker>` records order, and a bead in another repository is named by id in text. The store is embedded Dolt: `bd` commands never run in parallel, reads included, and a lock is waited out and retried.

### Proposal 2: knowledge:secrets · mind-belief › knowledge/secrets.md

**Comment** Carried over from the first book as written: Astra's seed test found it sufficient.

- Verify the consumer’s official stdin or file-descriptor interface first.
- Pipe GoPass producer output directly to that consumer.
- Use `set -o pipefail`.
- Use absolute or verified executables where appropriate.
- Suppress secret-bearing output. A secret travels by pipe from GoPass straight into the consumer’s verified stdin
- or file-descriptor interface, and by that path alone.
- Name the unavoidable crypto-backend, kernel, and consumer boundary as the exact extent of isolation held.
- Persistent import is allowed when the consumer’s supported contract requires it and the task authorizes credential setup.
-
- A secret or pairing code reaches the living only through its own device flow.

+ A secret travels by pipe from GoPass straight into the consumer's own stdin or file-descriptor interface, verified first, under `set -o pipefail` and with secret-bearing output suppressed, so it never enters the flow's output, arguments or environment. Persistent import is used only when the consumer's supported contract requires it and the task authorizes credential setup. A secret or pairing code reaches the living only through its own device flow.

### Proposal 3: knowledge:orchestrate · mind-belief › knowledge/orchestrate.md

**Comment** Carried over from the first book as written: Astra's seed test found it sufficient for a flow to lock, release and observe.

- Use `orchestrate` for ordinary requests. The installed wrapper supplies `ORCHESTRATE_SOCKET`; a direct client binary requires it.
-
- Acquire a Lock. Its four positional fields are `LockName`, `FlowId`, `LockPaths`, and `LockReason`:
-
-     orchestrate 'Lock.{ <LockName> <FlowId> [ <absolute-path> ... ] <LockReason> }'
-
- `LockName` names the work; `FlowId` is the owning flow's `FLOW_ID`; `LockPaths` lists the reserved absolute paths; `LockReason` states why. Put the actual owning `FLOW_ID` only in `FlowId`, never concatenated into `LockName` merely for uniqueness or title display.
-
- Datom strings are in guillemets, «like this»; curly quotes and ASCII double quotes are not delimiters.
-
- A single-word reason is bare.
-
- `Locked` returns the complete Lock: its integer ID, name, Flow, paths, and reason. `LockRejected` is a typed refusal. Paths are absolute.
-
- Release by the returned integer ID using the Orchestrate release request skill variable, substituting the integer for <lock-id>. Read the typed reply.
-
- `Released` returns the complete Lock. `ReleaseRejected` is a typed refusal.
-
- Observe current Locks:
-
-     orchestrate 'Observe.Locks'
-
- `Observed` carries one complete point-in-time Lock snapshot. It is not a subscription.
-
- Treat a client failure as a failed operation.

+ Orchestrate holds path locks between flows. `orchestrate 'Lock.{ <LockName> <FLOW_ID> [ <absolute-path> ... ] «reason» }'` answers `Locked` with the lock's integer id, or `LockRejected`; `orchestrate 'Release.<id>'` releases a lock; `orchestrate 'Observe.Locks'` shows the current locks. A lock whose holder has no live flow, checked against `herdr pane list` and `flow 'Metaflows'`, is stale and is released by whoever meets it.

### Proposal 4: knowledge:flow-nexus · mind-belief › knowledge/flow-nexus.md, a new file

**Comment** Carried over from the first book as written: Astra's seed test found it sufficient for a flow to send and launch. The module was deleted in rounds 1 and 2, so it lands as a new file.

+ ---
+ description: A message must be sent, a flow launched, or flow state read through the flow command.
+ dependencies: []
+ ---
+
+ The `flow` command speaks to the Flow Nexus. `flow 'Send.{ Address.{ Aspect topic Layer } Wake Soft.Order.«text» }'` sends a message: the recipient is an `Address` or `Up`, delivery is `Wake` or `Queue`, and the priority (`Soft`, `MiddleAbrupt`, `HardAbrupt`) carries a request (`Order`, `Question`, `Result`, `Notice`, `Psyche`, `Psyches`); the sender is taken from the calling process. `SendAccepted` witnesses durable acceptance only, not arrival or reading.
+
+ `flow 'Current.{ Aspect topic Layer }'` and `flow 'Metaflows'` read state; `flow 'BindSeat.{ Aspect topic Layer }'` binds the calling native seat to an address; `flow 'Launch.{ { Aspect topic Layer } Predecessors.0 «instruction» }'` starts the address's declared modules on its configured model.

### Proposal 5: knowledge:book-making · mind-belief › knowledge/book-making.md

**Comment** Carried over from the first book as written: Astra's seed test found it sufficient for a flow to author and build a book.

- ## The author makes the book
-
- The author makes the book properly and sends the source as made. The builder renders what it is given and enforces nothing; the book is as correct as the author made it. The publisher builds the source and publishes the page.
-
- ```sh
- bb tools/book-build.clj \
-   /abs/book.md out.html \
-   --figures /abs/figures
- ```
-
- ## What a source holds
-
- Outside a proposal a source holds only: one `Presentation.{ «title» }` line, one `# title`, unlabelled diagram fences, and modules shown as they stand, each under a level-two heading `## repo › path`. A module shown as it stands is its text at origin main, byte for byte, front matter left out.
-
- A proposal opens with `### Proposal N: title · repo › path`, numbered from 1; a new module ends the heading with `, a new file`, a deleted one with `, a deleted file`. A line moved between modules is one proposal headed `### Proposal N: title · repoA › pathA, and repoB › pathB`, with a level-four heading for each path, the line in red under the first and green under the second. No other level-three heading exists.
-
- ## Red and green
-
- Colour comes only from signed lines. In a change every line opens with `- ` (red, removed), `+ ` (green, added) or two spaces (unchanged, shown for place). A removed line is a whole line of the module at origin main; an added line is not. Colour comes from the diff marks alone.
-
- A module line is shown whole. A change to a hard-wrapped paragraph shows every physical line of that paragraph, so each sentence shows whole. A replaced paragraph is diffed as one paragraph: its removal and its addition together, with only the changed words marked.
-
- A code line in a book is at most 52 characters.
-
- ```text
- ### Proposal 1: A sender · psyche › messaging.md
-
- **Comment** Flow names the sender.
-
-   ## A message is a datom
-
- - The body is a datom.
- + The body is a datom; Flow names it.
- ```
-
- ## Marks inside a proposal
-
- Inside a proposal a source holds only its change lines, one Comment, its Alternatives, its Destroy or Archive mark, path headings at level four, `#### repo › path`, as the moved-line form has them, and code that the proposed lines themselves land.
-
- Every fence inside a proposal is signed line by line: red, green, or two spaces for a line kept in place, code-file proposals included, because code shown in a proposal is either what stands at origin main or what is proposed.
-
- One `**Comment**` paragraph at most, before every change: the machine's word, in its own colour. `**Alternative 1**`, `**Alternative 2**` and on, two or more, in order, each alone on its line and followed by the exact lines it lands. `**Destroy**` or `**Archive**` opening a paragraph marks a deleted module or record. Prose stands as its own paragraph, a blank line apart from any change.
-
- ## Figures and fences
-
- Every figure in a book is headed by the module it lives in and one of three states: as it stands, proposed added in green, or proposed removed in red.
-
- A figure already in a belief module shows without colour.
-
- An unlabelled fence holds a box-and-arrow sketch and nothing else; each one has its figure, `fig-N.svg` in the figures directory, drawn by the illustrator from the sketch with every box, label and arrow kept. A figure shows how a thing moves, one question per figure, is at most 52 columns wide, and is drawn in the figure grammar of vision-book. Every other fence carries its language: `ethos`, `datom`, `rust`, `sh`, `yaml`, `text`. An `ethos` fence is code that passes ethos-zero's Check, run by the author before the book is sent. A module written in Markdown is shown as rendered text. A book shows belief modules as rendered text and change marks.
-
- ## Code in a proposal
-
- Code the proposed lines land is shown in labelled fences, the Datom it reads or writes and the Ethos that types it, run against the source by the author before the book is sent.
-
- ## Commented books
-
- A book the living has commented on stays as he saw it; what his comments change goes into the next book. Its redo is a new book at a new link, and the commented one stays as he left it.

+ A book source holds a `Presentation.{ «title» }` line, one `# title`, modules shown as they stand at origin main under `## repo › path`, and proposals headed `### Proposal N: title · repo › path`. Inside a proposal every line is signed, `- ` red removed, `+ ` green added, two spaces kept, with at most one `**Comment**`, numbered `**Alternative N**` blocks, and `**Destroy**` or `**Archive**` for a deleted module.
+
+ An unlabelled fence holds a box-and-arrow sketch drawn as `fig-N.svg`; every other fence names its language, and lines are at most 52 characters. `bb tools/book-build.clj /abs/book.md out.html --figures /abs/figures` renders the source as given; a commented book stays as the living saw it, and its redo is a new book.

### Proposal 6: knowledge:ethos · mind-belief › knowledge/ethos.md, a new file

**Comment** Rewritten from the first book's seed: it now shows a Library file whole, the root word and its four sections, taken from vision:ethos and passed by ethos-zero's Check; a newtype replaces the first seed's alias, and traits and associations replace kinds. The module was deleted in rounds 1 and 2, so it lands as a new file.

+ ---
+ description: An ethos file is written, read, checked, or generated into Rust.
+ dependencies: []
+ ---
+
+ Ethos declares the types and traits from which ethos-zero generates Rust. `ethos-zero 'Check./abs/file.ethos'` answers `Checked`, or `Rejected` with the line, the column and the reason; `ethos-zero 'Generate.{ /abs/file.ethos /abs/out }'` writes the Rust and answers `Generated`, and a refusal writes nothing.
+
+ A file is its root word, then its sections. A Library's four sections are imports, types, traits and associations:
+
+ ```ethos
+ Library
+ []                            ; imports
+ [ Record.{ String Integer } ] ; types
+ [ Summarizable.[              ; traits
+     summarize.[ String ] ] ]
+ [ Record.[ Summarizable ] ]   ; associations
+ ```
+
+ In types, `Name.Type` is a newtype, `Name.{ }` a struct and `Name.[ ]` an enum. A trait holds its capabilities, and an association names a type and the traits it bears. A Signal root generates `Query` and `Response`, an Operation root `Operation` and `Outcome`, and Memory heads the store root. Generated Rust is committed and held fresh by a test.

### Proposal 7: knowledge:lojix · mind-belief › knowledge/lojix.md

**Comment** Reviewed against the signal-lojix and meta-signal-lojix contracts and cut less than the first seed: every query shape, Deploy with its positions in one sentence, admission, the terminal records, Pin and the deployment contract stay; the numbered field lists, Test, watch replies, startup configuration, store reset and bootstrap go. The query shapes, the terminal records and the multi-line Deploy were witnessed against the live clients; a failed terminal now carries evidence, and both contracts now take `Configure`, which the removed startup section denied.

- `lojix-nexus` owns durable state and two authority-tiered sockets. The ordinary contract is `signal-lojix`; the owner contract is `meta-signal-lojix`.
-
- Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.
-
- Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.
-
- Use `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET`; neither socket has a default path.
-
- ## Request syntax
-
- Each public client rejects files, zero arguments, and extra arguments. A request root is one value.
-
- A struct is brace-enclosed and positional, a vector is bracket-enclosed, a variant is a head with the period glued to both sides, and a variant carrying nothing is bare. `None` is bare and `Some` carries one glued payload. A string with a space or a delimiter is written in guillemets.
-
- ```text
- Variant.{ field0 field1 field2 }
- [ field0 field1 ]
- Some.Value
- «alpha beta»
- ```
-
- Never name a field in a request; the position carries the data.
-
- ## Ordinary requests
-
- The current `lojix` executable exchanges one request for one reply and exits. It cannot consume ongoing subscription events. Do not use it as a streaming terminal monitor; re-query with `Query.ByDeployment` or `Query.ByEventLog`.
-
- ## Replies and terminal state
-
- `DeployAccepted` is admission only. It does not prove evaluation, build, copy, activation, or completion.
-
- After `DeployAccepted`, re-query by deployment identifier or event-log position until a terminal deployment record exists.
-
- ## Deployment contract
-
- Every deployment transport is explicit. Lojix uses the supplied Nix store URI and SSH destination verbatim; it never derives a route from cluster, node, or user names.
-
- The logical node selects what is built; the activation destination selects which machine is changed. Before a state-changing deployment, verify that they identify the same node. If they do not, stop.
-
- A `CompleteHost` deployment uses an explicit root-privileged Nix store URI and SSH destination.
-
- A `UserEnvironment` deployment uses an explicit user-scoped Nix store URI and SSH destination.
-
- When a deployment directly names a target pair, use it without asking for a second transport confirmation. Otherwise derive the canonical internal hostname as `<node>.<cluster>.<internal suffix>` from Horizon cluster data and use it as the host in the required `CompleteHost` or `UserEnvironment` Nix store URI and SSH destination. If the supplied or derived pair is invalid, report it rather than substituting another route.
-
- A deployment proposal must be an existing absolute regular non-symlink `horizon-definition.datom` file.
-
- Use `RequireImmutable` when production deployment must identify one exact source revision. Push producer revisions before pushing the consumer revision that pins them.
-
- A `Current` generation is Lojix's committed state. It does not establish the target's live Nix profile or runtime links.
-
- A terminal activation failure can follow a partial target change. Inspect the target profile, runtime links, and activation journal, then report Lojix state and live state separately.
-
- ## Startup configuration
-
- The Nexus does not accept operator requests. `lojix-write-configuration` is the datom-to-startup boundary and writes the archive consumed by `lojix-nexus`.
-
- ## Store inspection and reset
-
- Inspect a store read-only with exactly:
-
- ```sh
- lojix-inspect-store 'InspectStore.{ /tmp/lojix.sema }'
- ```
-
- Inspection does not create or register missing tables.
-
- Reset accepts only:
-
- ```sh
- lojix-reset-store 'ResetStore'
- ```
-
- It takes no path. Store selection comes from the service-owned `LOJIX_CONFIGURATION` archive.
-
- Stop the Nexus before reset.
-
- ## Bootstrap
-
- `lojix-bootstrap` is a separate Nexus-free ingress. It accepts exactly one inline `BootstrapRun` value and does not read Nexus sockets, configuration, or store state.
-
- Ambient SSH configuration is not accepted.
-
- Bootstrap immutable flakes use:
-
- ```text
- github:owner/repository/40-lowercase-hex-revision
- ```
-
- This differs from Nexus deployment flake syntax.
-
- ## Placement
-
- The supported deployment and observation interface is `lojix` and `lojix-meta`; setup-specific wrapper scripts are not an alternative interface.

+ `lojix-nexus` owns Lojix's state and two sockets. `lojix` speaks the ordinary contract, `signal-lojix`, on `LOJIX_ORDINARY_SOCKET`, to query and watch; `lojix-meta` speaks the owner contract, `meta-signal-lojix`, on `LOJIX_OWNER_SOCKET`, to deploy, pin, unpin, retire and test. Neither socket has a default path.
+
+ Each client takes exactly one argument, one datom, and returns one reply. Positions carry the data and a field is never named: a struct is `{ }`, a vector `[ ]`, a variant a head glued to its payload by a period, `None` bare and `Some.value` glued, and a string holding a space in guillemets. A request may span lines.
+
+ ## Observing
+
+ ```sh
+ lojix 'Query.ByNode.{ cluster node None }'
+ lojix 'Query.ByDeployment.{ 13 }'
+ lojix 'Query.ByEventLog.{ 0 0 }'
+ lojix 'Query.ByGeneration.{ 42 }'
+ lojix 'Query.ByTestRun.{ cluster node None }'
+ ```
+
+ `ByNode` may name the artifact in its third position: `Some.CompleteHost`, `Some.BaseHost` or `Some.UserEnvironment`. `ByEventLog` takes the first and the last event-log position. `Queried` carries the generations and the deployment records, `DeploymentEventsQueried` the phase and cache-retention events, and `TestRunsQueried` the test runs, each ending in the database marker; `QueryRejected` names its reason.
+
+ `lojix` exits after one reply, so it cannot follow a watch: a deployment is observed by re-querying.
+
+ ## Deploying
+
+ ```sh
+ lojix-meta 'Deploy.Host.{ fixture-cluster target
+   BaseHost
+   /var/lib/lojix/horizon-definition.datom
+   NoSecrets
+   github:fixture-owner/fixture-flake?ref=main
+   { ssh-ng://root@target root@target }
+   Direct
+   { packages.x86_64-linux.fixture }
+   NixosSystemdBootV1
+   TestActivation
+   ResolveAndRecord
+   Some.@/etc/nix/machines
+   [] }'
+ ```
+
+ A `Deploy.Host` request's positions are, in order: cluster, node, `CompleteHost` or `BaseHost`, the proposal file, `NoSecrets` or a secrets directory, the flake reference, the transport `{ nix-store-uri ssh-destination }`, `Horizon` or `Direct`, the output selector `{ flake-attribute }`, the activation backend `NixosSystemdBootV1` or `HomeManagerNixProfileV1`, the action, `RequireImmutable` or `ResolveAndRecord`, an optional builder, and a vector of extra substituters. A host's action is `Evaluate`, `Realize`, `SetBootProfile`, `ActivateNow`, `TestActivation` or `ScheduleBootOnce`. `Deploy.UserEnvironment` carries the user name in the third position, and its action is `Realize`, `SetProfile` or `ActivateNow`.
+
+ `DeployAccepted.{ 13 { 263 263 } }` gives the deployment identifier and the database marker. It is admission only: it proves no evaluation, build, copy or activation. `DeployRefused` and `DeployRejected` refuse the request.
+
+ A deployment is done when its record, read with `Query.ByDeployment.{ 13 }`, ends in its terminal: `Some.Succeeded`, `Some.Rejected.reason`, or `Some.Failed.{ stage reason evidence }`, where the optional evidence carries the failed command, its exit code and its output.
+
+ `lojix-meta 'Pin.{ alpha node-1 42 keep }'` pins generation 42 under the label `keep`; `Unpin.{ cluster node label }` and `Retire.{ cluster node generation }` take the same form.
+
+ ## Deployment contract
+
+ Every deployment transport is explicit. Lojix uses the supplied Nix store URI and SSH destination verbatim; it never derives a route from cluster, node, or user names.
+
+ The logical node selects what is built; the activation destination selects which machine is changed. Before a state-changing deployment, verify that they identify the same node. If they do not, stop.
+
+ A `CompleteHost` deployment uses an explicit root-privileged Nix store URI and SSH destination; a `UserEnvironment` deployment uses an explicit user-scoped one.
+
+ When a deployment directly names a target pair, use it without asking for a second transport confirmation. Otherwise derive the canonical internal hostname as `<node>.<cluster>.<internal suffix>` from Horizon cluster data and use it as the host in the Nix store URI and SSH destination. If the supplied or derived pair is invalid, report it rather than substituting another route.
+
+ A deployment proposal must be an existing absolute regular non-symlink `horizon-definition.datom` file.
+
+ Use `RequireImmutable` when production deployment must identify one exact source revision. Push producer revisions before pushing the consumer revision that pins them.
+
+ A `Current` generation is Lojix's committed state. It does not establish the target's live Nix profile or runtime links.
+
+ A terminal activation failure can follow a partial target change. Inspect the target profile, runtime links, and activation journal, then report Lojix state and live state separately.

### Proposal 8: knowledge:datom · mind-belief › knowledge/datom.md, a new file

**Comment** The seed stays as in the first book. The module was deleted in rounds 1 and 2, so it lands as a new file.

+ ---
+ description: A datom is written, read, or typed in Rust.
+ dependencies: []
+ ---
+
+ A datom is a form at a path: a struct `{ }` of positional values, a vector `[ ]`, a variant `Head.payload` with the period glued on both sides and bare when it carries nothing, a bare token, or a string in guillemets «like this» when it holds a space or a delimiter. Positions carry the meaning and fields are never named; a datom is written only against a type that already exists, declared in Ethos first when none does.
+
+ In Rust, `#[derive(datom_codec::Datomizable, datom_codec::Composing)]` gives a type its datom kinds; text becomes a value through `Potential::<T>::from(text).actualize(&mut budget)` and returns through `value.datomize(Path::new()).protosize().textualize()`. A composition error names the path where the value failed.

### Proposal 9: knowledge:protos · mind-belief › knowledge/protos.md, a new file

**Comment** The first seed shrinks to the layering sentence. The module was deleted in rounds 1 and 2, so the other way is rejecting this proposal, which leaves it deleted; vision:protos already holds the four layers.

+ ---
+ description: The layers between text, tree, datom, and typed value are needed.
+ dependencies: []
+ ---
+
+ Protos reads text into a tree; a datom is the conceptual layer above that tree, and a typed Rust value the compositional layer above the datom.

### Proposal 10: knowledge:psyche · mind-belief › knowledge/psyche.md

**Comment** vision:psyche holds the four levels and that records live in the flow that heard them; intent:psyche holds that reviewed words outweigh inference and that a knowledge module holds only facts verified in code. The rest of this module, written psyche as residue, reading between the lines, keeping his raw words and weighing a later correction, is conduct and vision in kind, so by that intent it cannot stay in knowledge; whether it is proposed into vision:psyche is its own book. What remains is where the records are on disk, which a vision module may not name.

- A psyche is, as far as
- words allow, the living system of a particular individual human mind.
-
- Agents never access the living. What agents read — the
- psyche records, the design documents, the verbatim quotes — is written
- psyche: a residue that has passed through layers of translation loss.
- It is tentative and fallible.
-
- Sometimes the living is confused, or lacks perspective. A log entry can faithfully record a confused moment.
-
- Agents must read between the lines — using written psyche to infer
- the living, the way a human tries to read another human's
- mind. Never treat a psyche log as ground truth. It is an
- approximation of a living thing you cannot touch.
-
- Every rephrasing compounds the drift. Preserve the living's raw
- words. Do not paraphrase without the living reviewing the result.
-
- "Psyche" alone means the written psyche, the records named under
- Where psyche lives;
- the living person is always called the living.
-
- ## Four levels
-
- - **Spirit** — philosophy. Almost never changes. Load the `spirit:core` belief module.
- - **Intent** — declared goals and guiding rules. Broader and fewer than Vision.
- - **Vision** — concrete, topic-scoped, abundant, moves constantly.
-   The default level. Everything starts here unless obviously broader.
-
- - **Notion** — a brainstorm: an idea the living is turning over, binding nothing. The bottom level. Logged verbatim; never built on as if ruled.
-
- A notion may be drawn upon for suggestions.
-
- ## Where psyche lives
-
- - The `spirit:core` belief module — spirit's current home; entry files will
-   carry it.
- - The `vision:<topic>` belief module — crystallized vision: self-standing statements.
- - The `intent:<topic>` belief module — crystallized intent.
- - `flows/<short-id>/vision/<topic>.md` — raw records, in the flow
-   that heard them. Finding raw psyche means searching
-   `flows/*/vision/`.
- - `flows/<short-id>/notion/<topic>.md` — raw notions, in the flow that heard them.
-
- Raw means no confirmation was asked. Vision and Notion can be
- raw; Intent and Spirit can only be crystallized.
-
- A topic is a noun subject an agent would guess before knowing any ruling; a statement is an entry heading inside it.
-
- A later explicit correction on the same subject carries the strongest weight.
- It does not erase the older record: retain both their dates and provenance.
- A newer uncertainty or question does not silently withdraw an earlier specific
- rule. When records point to incompatible actions, the flow takes his latest word, acts on it, and says in its report which reading it took and why. He is asked only when the two readings would cost him differently.
-
- Any agent can search psyche logs for answers. If a topic is raised
- that the living may have spoken on, check before assuming.

+ Crystallized psyche is in the psyche-belief repository, in `spirit/`, `intent/` and `vision/`, one module per subject: `vision/ethos.md` is `vision-ethos`. A raw record is in the flow that heard it, `flows/<id>/vision/<topic>.md`, a raw notion in `flows/<id>/notion/<topic>.md`, and a settled one in `flows/<id>/archive/` under the same kind. The living's words on a topic are found by searching `flows/*/vision/` and `flows/*/archive/vision/`.
