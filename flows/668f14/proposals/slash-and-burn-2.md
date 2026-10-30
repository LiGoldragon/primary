# Slash and burn, round 2: the rest of the belief

Created and judged by Fable; candidates gathered by Sonnet, each ruled on here.

Source for the book metaflow. Markers: [-removed-] red, [+added+] green, [~moved from <module>: ...~] blue. Everything unmarked stands as it is. A module deleted whole is shown whole in red; otherwise each touched passage is shown whole; modules are in order of harm, the most harmful first.

What this is: every belief module outside the Primary's own set, swept by his criterion, anything that does not sound like common sense and is too specific. Every mark is a removal. Thirty-eight whole modules go: the compensation kind and the mind-belief evidence files already ordered gone, and the knowledge modules that are version pins, commit hashes, dated witnesses, tool help or copied code. The role procedures of the book pipeline are left standing until the Curriculum successor replaces them; their worst passages are cut here. The gatherers also flagged his own design decisions, routing between aspects, the anger rule, the fallback-chain symptom, replacing a system whole: those are kept, because he said them.

## mind-belief › knowledge/nexus.md — Destroy

Why: it promises what the nexuses are today and holds a Curriculum commit hash, a dated witness with flow ids, and four lines telling a flow to read Cargo.toml.

[-Orchestrate: read the current source version in the declared Orchestrate repository's `Cargo.toml`.
Flow: read the current source version in the declared Flow repository's `Cargo.toml`.
Message: read the current source version in the declared Message repository's `Cargo.toml`.
Lojix: read the current source version in the declared Lojix repository's `Cargo.toml`.

Curriculum receives one typed request through the socket at
`$XDG_RUNTIME_DIR/curriculum/curriculum.sock`. Its three authored-context
checkouts come from `CURRICULUM_PSYCHES_REPOSITORY_DIR`,
`CURRICULUM_MIND_CONTEXT_DIR` and `CURRICULUM_FIELD_CONTEXT_DIR`; its refresh
executable comes from `CURRICULUM_CONTEXT_REFRESH_PROGRAM`. These configured
values, including the service account and checkout locations, belong to the
installation and are read there rather than assumed from another setup.

At Curriculum `2d74e7725bfff88ee3aec1ebe9ce31d52873ebbc`, every query follows
`CurriculumOperation::perform` → `SourceConfiguration::from_environment` →
`SourceConfiguration::read`. `read` runs the configured refresh executable
synchronously and requires its success before reading the three checkout
revisions and their module sources; only then does `perform` dispatch
`ResolveSkills`, `ResolveSources`, `ComposeStartup` or `ComposeRole`. Nexus
startup also calls `read` while opening its memory. Thus `ExecStartPre` is not
the request-time refresh: it is an additional startup action.

The 2026-10-29 operational witness from Psyche Primary
`psyche228c47e` (with Mind `2eff0f9` and Field `77feb34`) observed the user
`curriculum-nexus.service`, with no root process, configured to run
`curriculum-refresh-contexts`. That program fetches each context repository's
`origin/main` and detaches its configured checkout there. The same witnessed
checkout update was performed manually with `git fetch origin` followed by
`git checkout --detach origin/main`. A
`ResolveSources.[ ModuleIdentity ]` request through the configured socket then
reported the revision from which Curriculum served that module. The returned
revision witnesses the request's source checkout; it does not identify the
Curriculum executable revision by itself.-]

## mind-belief › knowledge/flow-seats.md — Destroy

Why: two commit hashes, then the Flow CLI's own help copied out; the CLI prints its help itself.

## mind-belief › knowledge/ethos.md — Destroy

Why: generator mechanics pinned to datom-codec 0.32.2 and a 15.0.0 cutoff; vision/ethos.md and ethos-zero's own output hold what stands.

## mind-belief › knowledge/codex-harness.md — Destroy

Why: a dated version observation, per-release config keys, and vendor internals with no way given to check them.

## mind-belief › knowledge/datom.md — Destroy

Why: the crate's Rust copied into belief; vision/datom.md holds the syntax and the crate holds the code.

## mind-belief › knowledge/protos.md — Destroy

Why: the crate's type definitions copied into belief, and two sentences beside empty headings.

## mind-belief › knowledge/claude-harness.md — section changed

Why: a dated version observation and the launcher's internals.

[-On 2026-10-09, `claude --version` returned `2.1.294 (Claude Code)`.
This is an observation of the installed command, not a metaflow binding.-]

[-The native Claude launcher reads generated
`.claude/skills/<name>/SKILL.md` files, sends bounded leading slash
requests, and verifies the returned skill bodies against those files.
Configuration is Flow's datom, read with `flow-meta 'Configuration'`.-]

[-Claude Code stops its background tasks when the host's free memory
looks low, judging by free rather than available memory, so another
process's build can end a long task that is nowhere near its own
limit. A long-running process launched from the harness runs
detached, as a transient systemd user service or scope with its own
memory cap, and the harness watches for its end.-]

## mind-belief › knowledge/lojix.md — sections changed

Why: the field lists of every request and reply are signal-lojix's; the schema history (v2 to v5) and the fixture transcripts with literal ids and paths age with the next release. What stays: which client speaks to which socket, that admission is not completion, and the deployment contract.

[-The Nexus accepts schema v5 and refuses earlier schemas. Reset removes and recreates recognized v2/v3/v4 stores as v5. An existing v5 store is left intact.-]

[-Successful reset replies are:

```text
LojixStoreReset.{ path 5 count }
LojixStoreAlreadyCurrent.{ path 5 }
```-]

[-Reset is destructive for a recognized v2/v3/v4 store.-]

[-Exact witnessed reply:

```text
DeployAccepted.{ 13 { 263 263 } }
```-]

[-Exact tested form:

```text
ConfigurationWriteRequest.{ /run/fixture-lojix/ordinary.sock 432 /run/fixture-lojix/owner.sock 384 /var/lib/fixture-lojix /var/lib/fixture-lojix/configured-lojix-store.db fixture-nexus NoTestDefaults /tmp/startup.rkyv }
```-]

[-Every "has, in order:" field list, every "carries" variant list and every "Exact witnessed form" example of a request or reply, from `Query` through `BootstrapRejected`: sixty-odd passages, each the contract crate's own vocabulary.-]

## mind-belief › knowledge/orchestrate.md — passages changed

Why: a flow-id token in an example, and a stale-lock check written as herdr and flow commands.

[-    orchestrate 'Lock.{ OrchestrateDocs 444e5e [ /absolute/path/to/file ] «Clarify Lock fields» }'-]

[-A lock whose holder has no live flow is stale: check the holder's six-character id against `herdr pane list` labels and `flow 'Metaflows'`; `orchestrate 'Release.<id>'` releases any lock by its number, whoever holds it, and a stale lock is released by whoever meets it.-]

## field-belief › compensation, 9 modules — Destroy

Why: the compensation kind is gone on his word. behavior.md, book-crystallization.md, correction.md, deployment.md, file-editing.md, nix-workflow.md, operating-system.md, secrets.md (shown in round 1), testing.md. With them psyche-belief › compensation/book-making.md and compensation/messaging.md.

## mind-belief › evidence, 4 files — Destroy

Why: research transcripts kept beside belief, never composed into a flow. android-paralinguistic-transcription-sources.md, belief-module-inventory.md, cache-compaction-research.md, instruction-length-research.md.

## mind-belief › knowledge, the 29 modules of the first draft — Destroy

Why: version-pinned descriptions of a harness or of our own code at one commit, carrying hashes, ids and paths. belief-module-size, belief-modules, claude-agent-frontmatter, claude-tool-allowance, codex-rollout, codex, compaction, context-source-contracts, context-strata, file-editing, flow-caller, flow-configuration, flow-queue, flow-receipt, generated-projection, handover, harness-effort, last-response, monitoring-systems, obsidian-app, obsidian-comments, obsidian-hosts, obsidian-self-hosted-sync, obsidian-sync, paralinguistic-transcription, periodic-hook-context, psyche-grasp, refresh, subagent-context, subflow-token-cost, yt-dlp.

## psyche-belief › intent/mandatory-traits.md — passage changed

Why: a date, a session hash and an approval quote inside a belief module.

[-— living-approved wording, 2026-08-13 (Steward session d2bb5f5f).
Proposed by Steward, approved with "otherwise its good, implement
commit and deploy."-]

## field-belief › role/book-publishing-procedure.md — passages changed

Why: a SHA-256 path template, a reservation protocol, and a gallery sweep at 950 artifacts are the tool's job, written as instruction to a model.

[-Preserve the local source. Build to `FLOW_DIRECTORY/publications/<source-path-digest>/<source-basename>.html`, where `source-path-digest` is the SHA-256 digest of the source's canonical path. A fixed or caller-independent output such as the scratchpad's `book.html` is forbidden. A prior URL supplies comment context, never replacement source. Every revised presentation has its own source and page and a fresh artifact; preserve the older publication and its comments.-]

[-Before any Artifact call, atomically reserve that source's digest directory with a `publishing` entry, re-read the publication state while holding it, and remove only your reservation when the operation ends. On a first publication, call Artifact without a URL, then atomically create `publication` in that directory with one `source <canonical-path>` line and one `url <returned-url>` line. An existing record makes the operation a republish attempt, not another first publication. A book is published once, at one URL, and a republish keeps its URL.-]

[-When the gallery passes 950 artifacts, the book Secondary runs artifact-sweep (tracker repo tools/artifact-sweep/) with a cutoff seven days back.-]

## field-belief › role/book-page-procedure.md — passages changed

Why: model names, an absolute path, a retired schema listed as a type, and a batch limit of 50 with version pins.

[-You are the judge: you run at medium effort (Opus), start
readers at medium effort (Sonnet), merge what they return into what the page
already holds, and write the page.-]

[-Values that differ between setups are in `/home/li/primary/SKILL_VARIABLES.md`:
`The living's page` (the page's address), `Claude transcript root`,
`Curriculum skills`. Read them there.-]

[-Historical read schema only; these are not writable current proposal destinations:

    Subject.{ Name State Vector<Waiting> Changed }
    Waiting.{ Question Proposal Vector<Option> Lost Answer }
    Answer.[ None Chosen.{ Option Note } ]
    Crystallization.{ Statement Destination Vector<Source> State }
    LegacyDestination.[ Vision.Topic Intent.Topic Skill.{ LegacyKind Name } ]
    LegacyKind.[ Operation Documentation Compensation Trial ]
    Source.{ FlowId Topic }
    State.[ Proposed Approved Changed.Markdown Refused ]-]

[-- Historical `crystallizations/<id>` rows: `statement` (Markdown), legacy `destination` (one
  of `{"vision": "<topic>"}`, `{"intent": "<topic>"}`,
  `{"skill": {"kind": "Operation"|"Documentation"|"Compensation"|"Trial",
  "name": "<skill name>"}}`), `sources` (list of `{flowId, topic}`: the
  flow that heard each record and the record file's topic), `records`
  (list of record ids drawn on; never shown), `state` (`"Proposed"`,
  `"Approved"`, `{"changed": "<the living's note>"}` or `"Refused"`),
  historical `approvedAs` (read as its original value; never generate a new retired kind), `answeredAt` (written by the
  page), `order`.-]

[-    node /home/li/primary/tools/book-fetch.mjs --from <line> --out <scratch>/book-]

## field-belief › role/subflow-role.md — passage changed

Why: environment variable names, a PROVENANCE handoff, jj and git invocations and a compensation module name, in one paragraph every subflow carries.

[-Your flow is `FLOW_ID` and `FLOW_DIRECTORY` in your environment. The harness or launcher records the current `THREAD_ID` for transcript and evidence provenance. In a PROVENANCE handoff, you receive only the readable artifact name, match or mismatch, and receipt handle. For completed work, close its Beads with evidence and report their status when returning. A subflow never stashes, resets or checks out over the shared working copy; it reads a baseline from a revision with `git show <rev>:<path>` or `jj file show -r <rev> <path>`. A search over files is rg. Do not create a lane, index entry, or log. Create a report or witness only when the main flow delegates it or a named tool or flow will consume it, and use compensation-flow-evidence for its contract. A witness or test launch takes a throwaway topic of its own; an address a live flow holds stays with that flow.-]

## field-belief › role/comment-relay.md — passage changed

Why: a flow command written out literally, for a relay the tool should make.

[-Compose the `Psyches` request yourself from the new comments and send it to Psyche core Secondary: `flow 'Send.{ Address.{ Psyche core Secondary } Wake MiddleAbrupt.Psyches.[ { «context» «verbatim» } … ] }'`.-]

## psyche-belief › vision/archive-ethos-monolith.md — Destroy

Why: it describes itself as retired; every paragraph is history of a renamed stage.

[-Retired on landing by flow fe34eb, 2026-09-10. The living ruled Ethos
Monolith and Ethos Zero one stage under two names.
What still stands is carried by Vision/ethos.md,
heading Zero; the words are kept here.

# Ethos-monolith

## Origin

All our systems will be Nexuses, and the correct three-nexus ethos
stack is the desired stack — but it is too complex to go for
directly, and the previous effort devolved into agent hallucinations
for lack of proper instructions. The monolith is the short-term path
that brings ethos into production: the earlier stack's code is kept,
left in place, frozen, and new repositories carry a simplified path
from Ethos straight to Rust.

## Name

First named ethos-rust, the schema-rust analogue; then renamed
ethos-monolith: it has no nomos and no logos component and goes
straight to Rust — a monolith.

## Shape

The monolith will itself be a Nexus. Nexus by itself names our
specifically designed daemon — distinct from Nexus Core, the
runtime engine — and executables are named component-nexus.

## Purpose

An incremental implementation and bootstrap process, so that ethos
and datom get written and read as soon as possible, at full correctness,
and components start being written in ethos.

## Vocabulary carried

The Signal, Nexus, SEMA vocabulary and principles are kept, and
how they are used and implemented is designed afresh. Nexus is
authored in ethos so its main operations are visible. Sema is the
database engine, authored in ethos so the stored types are visible;
it matters more than nexus, because operational editing should yield
database migration operations along with the editing operation.

## Readiness

Ethos serves new work in place of legacy schema once the monolith is
ready to use; readiness is witnessed.-]

## psyche-belief › vision/datom.md — passages changed

Why: a postponement and the patch note that contradicts it, a speculative future guarded by a gag, and the name's history.

[-Meaning is postponed so that a working syntax lands as soon as
possible: today a parenthesized text lands as a plain String, with
the later type marked in code. The name Meaning smells of a verb; it
stands provisionally and is reopened together with the type.-]

[-The meaning language is now developed, and is defined in
Vision/meaning.md; that supersedes the postponement stated above.-]

[-Generating Rust is Ethos's duty, in today's division of labor. When
Ethos becomes the full authoring language, with Rustlang as its
assembly layer, Datom, the data dialect of the Protos family, may gain
an inline place in authored Ethos, the way Rustlang composes data
directly in code. That road is reached, or even floated, only with
explicit context: how, when, and where data yields Rust, stated
without ambiguity; until then the division stands as spoken.-]

Everything moves to Datom: all of the stack, Horizon, Lojix, everything.
[-Datom's own line of descent is NOTA, which also
passed through the temporary name Dotos; that old notation stays
behind, frozen, and may be called legacy. Schema is the abandoned
ancestor of Ethos, not of Datom.-] The library is named datom-codec so
that datom is free for the datom nexus, which comes when there is more
to do: translating datom objects between formats, and a parsing cache
keyed by the content-addressed hash of normalized text.

## psyche-belief › vision/flow.md — further passages changed

Why: a code note on payloads, a fallback that round 1 removed from messaging, and a reaping section the refresh paragraph already says.

[-Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.-]

[-A request that Flow holds or refuses reaches its recipient by the Herdr fallback the same minute, as vision:messaging gives it.-]

[-## A replaced session is reaped by the refresh itself

Reaping belongs to the refresh event. A refreshed flow
takes the replaced end out of receiving messages, so only live ends stay
registered and addressable.-]

## psyche-belief › vision/ethos.md — further passages changed

Why: a map of which module lives where, a datom carrying a literal path, and the generator's invocation.

[-```
┌──────────────────────────────────────────┐
│ vision-ethos                             │
│                                          │
│  what ethos is · its layout              │
│  its two anatomies: types and traits     │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ the ethos of ethos                 │  │
│  │ the types an ethos file is made of │  │
│  │ the first golden ethos             │  │
│  └────────────────────────────────────┘  │
└───────────────────┬──────────────────────┘
                    │ example
                    ▼
        ┌───────────────────────┐
        │ vision-flow-ethos     │
        │ the Flow Nexus, in    │
        │ ethos; its own skill  │
        └───────────────────────┘
```

The anatomy of ethos lives in vision-ethos itself, as
the first golden ethos; Flow's ethos is one example,
in its own skill.-]

[-```
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]     ; the datom
```-]

[-## Generation

By request to ethos-zero, which is not a daemon, hence its name; committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```-]

## psyche-belief › vision/protos.md — passages changed

Why: a repeated example whose `Datom::Struct` contradicts the `Datom { path, form }` shape above it; history of a dropped delimiter; a plan about three daemons.

[-```rust
Protos::Enclosed(Braced, vec![Protos::Bare("Ada"), Protos::Bare("1990")])   // structure: an enclosure of two runs
Datom::Struct(vec![Datom::Bare("Ada"), Datom::Bare("1990")])                // meaning: a struct of two positions
```-]

A brace-enclosed structure's arity is anatomical;
a bracket-enclosed structure's arity is not. Angle brackets are a
real protos delimiter. [-The key-value map, which the guillemets once
delimited, is dropped entirely from protos and its dialects.-]

Datom is a protos dialect, carrying only
pure typed data; it does not take part in the multi-pass
rust-generation engine that ethos, nomos and logos are slated to
become, but it shares the protos style. [-The final fully-decomposed
engine with three daemons is the protos engine.-]

## psyche-belief › vision/crystallization.md — further passages changed

Why: said twice beside it, and a record-id format.

[-## Impurities fall out through crystallization

Impurities come out in the course of crystallization: a crystallization
proposal points out the impurities it dissects out, and the living
rules on them with the statements.-]

[-A record's id is its originating session's short id and that
session's own count.-]

## psyche-belief › vision/nexus.md — further passage changed

Why: an open naming question left in belief.

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. [-The name is open,
Apply liked.-]

## psyche-belief › vision/chronos.md — passages changed

Why: an ephemeris version and a build order.

[-Chronos reckons from JPL's DE440 ephemeris, for the years 1550 to 2650.-]

Chronos is the golden example: a simple, idiomatic Nexus with a full ethos specification, built on Ethos and the Nexus.
[-Flow is implemented from it, then the other nexuses.-]

## psyche-belief › vision/committing.md — passage changed

Why: a version-control mechanic.

[-A commit
made without paths takes the whole working copy, and is made only
while the whole repository is locked, when nobody else may be
editing.-]

## psyche-belief › vision/remembering.md — section changed

Why: a log-entry format.

[-## The remembering line says what was found most relevant

The log's record of a remembering carries a short description of what
from the remembered flow was found most relevant to the current one.-]

## psyche-belief › vision/psyche-aspect.md — passage changed

Why: said again in the two sections under it.

[-Psyche core keeps track of all the psyche and passes each matter to the topic flow it belongs to.-]

## psyche-belief › vision/signal.md — section changed

Why: portable rkyv is said above; the rest is an open question.

[-## Protocol

Signal is portable rkyv plus whatever protocol is standardized on top
of it. The protocol is to be decided.-]

## psyche-belief › vision/high-level-view.md — passage changed

Why: a roadmap of named products that ages.

In the long term, the great advancements are the improvements that most increase the definition of the psyche[-:

- a more complete and reliable Ethos and Datom;
- reliable flow spawning and communication: transcripts scanned by hooks with programmatic reactions, and flows that are truly lean;
- real-time communication with the living, and better, a functioning interface, Unity, over Mentci;
- Sema, the rich-expression dialect of protos;
- paralinguistic speech-to-text, on Android and iOS-].

## psyche-belief › vision/horizon.md — passage changed

Why: a host name in passing and a status note.

A virtual machine runs on a node, and sandboxing is a feature a node
has. Which node has it is known by querying Horizon. [-Prometheus is
mostly the workhorse. Allocating resources is not easy and is not yet
designed.-]

## psyche-belief › vision/meaning.md — passage changed

Why: a flow id cited in belief.

The roots of the ontology are the seven Vaiśeṣika categories, and
its verbs follow the Aṣṭādhyāyī of Pāṇini, which an earlier ruling
makes the base for how the system thinks, communicates, and
classifies things in the world[- (flow 5851f4)-]. How the two divide
beyond that is not yet ruled.

## psyche-belief › vision/git-server.md — passages changed

Why: the implementing program, and a bare record id.

The cluster runs its own Git server on the node whose cluster data gives it the GitServer role. It serves thinking machines: it accepts the SSH keys the cluster data holds, carries no web interface, and mirrors every repository to GitHub as a backup. [-Gitolite serves it, with every key and every access rule declared from the cluster data.-]

[-## Sources

d68c82 git-]

## psyche-belief › vision/nix-builds.md — passages changed

Why: a status note and a bare record id.

[-Tracking Nix builds is long term.-]

[-## Sources

d68c82 builds-]

## mind-belief › role/default-description.md, explorer-description.md, worker-description.md — changed

Why: each names the Codex orchestrator.

[-General-purpose sub-agent for the Codex orchestrator-][+General-purpose subflow+]

[-Read-only exploration sub-agent for the Codex orchestrator-][+Read-only exploration subflow+]

[-Implementation sub-agent for the Codex orchestrator-][+Implementation subflow+]
