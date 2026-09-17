# Flow CLI POC design

Status: design for the user-authorized Flow CLI proof of concept.  It defines
the operational anatomy and migration boundary; it does not claim that the
production Flow Nexus, Curriculum handshake, Mind, Psyche, Creo, or a native
harness launch adapter exists today.

## Decision boundary

The cited psyche records settle the direction: Flow makes starting and
restarting small and direct; it shares one database across primary, secondary,
and tertiary; it runs from the shared main workspace; it identifies an
agentic flow separately from the meta-flow continuation; Mind owns memory;
and Psyche is a distinct cross-layer living corpus and dispatch surface.

This document decides the POC record anatomy, dispatch ordering, field
ownership, compatibility import, and testable supervisor behaviour.  It is a
design application of the records, not further psyche.  In particular, record
names, revision rules, SQLite layout, CLI spelling, migration mechanics,
origin-reader result variants, model-choice handling, and the production
Nexus boundary are design decisions.

The primary workspace stays one shared checkout on `main`.  A launch does not
make a worktree or branch.  Concurrent writers coordinate exact paths through
Orchestrate.  This removes copies of the workspace and of Flow data without
turning Flow into a memory archive.

The motivating words are concise:

> “It’s not going to be where the memory lives, so the mind is going to use it.”

> “if the flow ID matches the flow’s provenance, then we can restart it.”

The first is the Flow/Mind boundary; the second is the complete restart
authority rule.  Neither authorizes an extra harness, parent, owner, layer,
or meta/core permission gate.

## Terms and identity

`FlowId` is an opaque, durable identity for one agentic flow.  It has no
embedded layer, model, parent, harness, role, date, permission, or session
meaning.  It survives attempts, native sessions, fresh-context launches, and
restarts.  Display aliases are conveniences, never authority.

An **agentic flow** is the contained program that performs a job.  A **meta
flow** is a continuation identity, the whole to which Psyche commonly speaks.
They are separate fields and separate relationship records; neither is
derived from the other.  **Placement layer** records where work is placed
(`primary`, `secondary`, or `tertiary`).  It is also distinct from a
Curriculum **effort** selection such as `medium`.

`AttemptId` identifies one execution attempt of a `FlowId`.  `Generation` is
its monotonically increasing lifecycle fence: all externally visible effects
from an attempt carry its generation and consumers reject an older one after a
newer generation is ready.  A `SessionRef` identifies a harness-native
conversation/session; its shape belongs to that harness.  A `TranscriptRef`
locates a stable transcript entry and can include a native record id and a
content hash.  Flow stores references and hashes, never transcript bodies.

The current `flow-id` helper remains an imported compatibility mechanism, not
a FlowId generator to rewrite in this POC.  Its Codex mode takes
`CODEX_SESSION_ID`, its Claude mode takes `--parent-session`, and it currently
claims a six-hex display candidate, lengthening it when a collision demands
it.  It has no Codex `--parent-session`.  The POC records that alias mapping
and full harness identity as an external identity claim.  It does not mistake
an alias for the opaque FlowId.

Creo is a future verifier seam.  Given authenticated proof it must resolve to
the same `FlowId`; this POC neither defines a proof format nor builds crypto.

## One shared store

Flow has one logical Sema store globally for the three placement layers.  A
row has a layer index for locality and filtering, while the identity key stays
global.  The intended query is therefore ordinary:

```text
Find lifecycle and current attempt for FlowId 562869 across all layers;
join the attempt’s primary placement and its origin FlowId.
```

It must not require opening three layer-local Flow databases.  The store holds
operational anatomy only: identity, declared placement, type selection,
requests, receipts, attempt/generation state, aliases, origin locators,
relationships, immutable references, and append-only events.  It does not
hold narrative logs, vision text, reports, witness prose, annotations,
summaries, full prompts, tool bodies, model messages, or transcripts.

Mind owns per-flow memory and transcript entries, including retrieval and
archival policy.  Psyche owns authored living words and the cross-layer corpus
whose search is not constrained to one placement layer.  Flow may retain a
typed `MindEntryRef` or `PsycheRecordRef` with a digest for provenance, but
never becomes their duplicate store.  Archives and retrieval remain Mind or
Psyche operations.

## Typed records and ownership

The production contracts will be authored in Ethos and stored by Sema.  These
are the POC logical types; the field table is the authority over a convenience
JSON representation.

| Record | Immutable fields | Mutable/append fields | Owner |
| --- | --- | --- | --- |
| `Flow` | `flow_id`, creation request, created time | current lifecycle pointer | Flow |
| `FlowPlacement` | `flow_id`, `layer`, `revision` | superseded by later revision | Flow |
| `FlowTypeSelection` | flow, descriptor id/revision/digest, role, effort, requested model | superseded selection only through new generation | Flow receipt + Curriculum source |
| `FlowRelation` | subject, relation kind, object, revision | tombstone/supersession event | Flow |
| `AliasClaim` | harness, harness identity, alias, claim digest | collision extension/revocation event | imported helper/Flow |
| `DispatchRequest` | request id, target/caller FlowId, variant, goal, origin locator, requested type | acceptance and terminal result events | CLI/Flow |
| `Attempt` | attempt id, flow id, generation, launch plan digest | state transitions | supervisor |
| `LaunchReceipt` | request id, attempt id, curriculum receipt ref/digest, harness/session refs | ready/failed timestamps | launcher/Curriculum |
| `OriginLocator` | trusted host observations and hashes | resolution result ref | trusted host/Flow |
| `LifecycleEvent` | event id, flow, generation, type, occurred time, payload version | never changed | Flow |
| `LegacyRecordLink` | source path, source digest, imported record id, lineage | archive state event | migration |

Every typed payload has `schema_version`; every replaceable declaration has a
monotonic `revision`; every append-only event has an event id and payload
version.  Time is recorded by the component writing the record and is not
treated as caller-supplied fact.  `FlowId`, `AttemptId`, `RequestId`, and
`Generation` are component-owned.  The caller owns only the requested
operation, small goal, optional requested type/model, and its available
origin inputs.  Curriculum owns descriptor contents and revisions.  The
trusted host owns observed process/tool-call facts.  Mind and Psyche own the
referenced bodies.

## Dispatch inputs and lifecycle

The native contract has typed variants, approximately:

```text
DispatchInput = Start { type_request, goal, origin }
              | Restart { target_flow, origin }
              | ResolveOrigin { target_flow, locator }
              | Observe { selector }

Lifecycle = Requested | Accepted | Provisioning | Launching | Ready
          | Retiring | Retired | Failed
```

`flow start <type> <small goal>` and `flow restart <flow-id>` are deliberately
supported user-authorized CLI sugar.  The CLI parses them into the same typed
`Start` and `Restart` inputs; it does not erase the user’s command behind a
generic one-Datom rule.  The zero-argument production Nexus is `flow-nexus`.
Its ordinary client is `flow`; its privileged client is `flow-meta`; each
speaks only its compiled binary Signal contract.  Ethos authors the contracts,
and Sema persists their types.  Observation is a subscription: current state
on opening, then events as state changes, with no polling.

The POC uses a Python process supervisor and SQLite so its state transitions
can be inspected and tested. Its current ergonomic surface is
`flow.py [--db PATH] [--fixture] start GOAL [--type TYPE] [--model MODEL]
[--job NAME]` and `restart [FLOW_ID]`, with `show`/`status` and `origin` for
inspection. That is an explicit stand-in, not a production Nexus and not
evidence that native Claude or Codex launch/resume works.

### Start

1. The CLI obtains a trusted origin envelope where available and constructs a
   request id.  Missing data remains `unknown`; it is never guessed from the
   latest transcript or a model assertion.
2. Flow durably writes `Requested`, deduplicates on request id, then writes
   `Accepted` before replying.  Retrying the same request returns the same
   accepted outcome.
3. Flow resolves the flow type descriptor and asks Curriculum for the selected
   immutable files, base instructions, bootstrap procedure, and revision.
4. It creates the next attempt/generation, records the receipt reference, and
   launches out of process in the shared primary directory.
5. The new attempt becomes `Ready` only after its readiness signal.  Effects
   are fenced to its generation.  A failed provision/launch records `Failed`;
   it does not leave a half-current attempt.

### Restart

The resolved caller `FlowId == target FlowId` is the sole authority predicate.
It deliberately has no veto based on meta/core identity, placement layer,
owner, parent, harness, live PID, or model.  Invalid/missing caller identity,
unknown target, malformed typed input, unavailable curriculum, readiness
timeout, or supervisor failure are operational failures, not extra authority
rules.

Flow accepts and persists the idempotent restart request before it returns to
the self caller.  It then provisions and launches a successor attempt out of
process.  The predecessor stays active until the successor reports ready;
only then does it retire gracefully.  If the successor fails, the predecessor
remains active.  A supervisor restart replays accepted-but-nonterminal
requests from the durable queue and uses request ids plus generations to avoid
duplicate effects.  There is no live-PID veto.

A restart resumes the same `FlowId` with a new attempt and session.  It may use
a native harness resume when available, or a fresh context with the same
identity and its origin/Mind references; they are explicitly different launch
strategies.  The POC may choose fresh launch.  It must never mint a new FlowId
just because a session cannot natively resume.

## Origin and transcript boundary

The CLI request envelope carries these optional typed observations:

```text
flow_id, session_ref, turn_ref, native_transcript_record_id,
tool_call_ref, cli_pid, cli_process_start, cli_executable_digest,
caller_pid, caller_process_start, caller_executable_digest, parent_chain
```

Only the trusted host stamps an actual tool-call origin and observed process
chain. Model-supplied flags, heuristic “latest transcript” selection, and
unverified caller text cannot become trusted fields. The POC fixture harness
is the named cooperative boundary that supplies exact session/turn data; it is
not an assertion that every production harness already exposes them. A real
bridge must resolve its stamped session to a stored Flow attempt/binding before
it can identify the caller FlowId. A missing turn is `unknown`/`Missing`, not
a license to select adjacent or latest content.

`launcher-origin` is a light leaf flow type.  Its target is the launcher’s
origin, never its own spawn origin, preventing recursive retrieval.  Given a
bounded user turn and surrounding assistant/tool messages, it preserves exact
context with transcript locators and content hashes, stores the selected entry
in Mind, and returns one typed result:

```text
Found { mind_entry_ref, locators, hashes }
Missing { searched_locator }
Ambiguous { candidates, reason }
Truncated { available_locator, omitted_bounds }
```

The response is small evidence, not a copied transcript.  A target flow can
then retrieve the Mind entry under Mind’s access and retention rules.

## Naming and relationships

Subflow job names are addressable identities inside a parent flow scope.  The
first requested bare name is used; repetitions become `name-second`,
`name-third`, then `name-4` and onward.  Canonical addressing remains
`FlowId + job-name`, so a display rename cannot change identity.  Requested
base-name collisions are checked globally within the parent scope before a
launch is accepted.  A failed reservation/launch leaves its name unavailable;
it is not silently reused for a different attempt.

Relationship kinds include `ParentOf`, `JobOf`, `ContinuationOf`, and
`OriginatesFrom`.  Parenthood is descriptive and provides no restart authority.
The meta-flow continuation relation is not a parent/child replacement.

## Type selection and recursive training discovery

Flow types are external Curriculum-owned descriptors.  A descriptor includes
role, placement layer, default model policy, base instructions, bootstrap
procedure, and descriptor revision.  A request/receipt records the descriptor
id, revision, content digest, selected immutable skill file references, and
the generated launch selection.  Files are immutable for an attempt and live
outside common generated discovery roots.  A launch must not mutate shared
`AGENTS.md`, a shared skill projection, or a common harness directory to
change one flow’s role. The launch receipt may claim a Skill interface only
when the selected harness actually exposes a callable skill mechanism in that
launch. A readable `SKILL.md` on the filesystem is not injected skill
authority. Provisioning records the tested interface and fails or marks
unsupported a selection that requires injected skills but has no such
interface.

The bootstrap procedure is recursive training discovery: read declared
dependencies, detect cycles, track visited skills, observe a bounded budget
and explicit end condition, read origin first, then retrieve relevant Mind and
Psyche evidence.  It requests a missing skill through the skills mechanism.
If a required skill or required context cannot be retrieved, it pauses with a
typed missing-context outcome; it does not invent facts or substitute a
similarly named file.

`medium` is a placement/effort choice and defaults to Claude under the cited
vision.  A type may name a preferred model; a caller may make an explicit
model request.  If the model is unspecified, Flow may select Claude or Codex
using configured quota awareness, but freshness/availability unknowns must be
recorded.  An explicit request is never silently switched.  Actual model names
and availability are setup configuration, not hard-coded durable assumptions.

## Legacy migration, one-way

Migration imports evidence before any source is archived.  For each source it
writes its source path, digest, source record type, importer revision, import
time, and `LegacyRecordLink` lineage to the created Flow/Mind/Psyche record or
to an explicit unclassified result.  It validates the digest and resulting
reference before marking the original read-only archive.  There are no dual
writes after cutover and no deletion in this POC.

| Existing material | Import destination | POC treatment |
| --- | --- | --- |
| `flows/*/log.md` | Mind transcript/log entry reference; Flow lifecycle facts only when parseable | digest, link, read-only archive |
| `flows/*/index*` | Flow identity/alias/relation records | import lineage, archive |
| `flows/*/vision/*` | Psyche authored-record reference | preserve source/digest, archive |
| `flows/*/reports/*` | Mind artifact/document reference | preserve source/digest, archive |
| `flows/*/witness*` | Mind evidence reference | preserve source/digest, archive |
| `flows/*/annotations*` | Mind annotation reference | preserve source/digest, archive |
| `flows/*/summary*` | Mind summary reference | preserve source/digest, archive |

Narrative material is never parsed into asserted Flow facts merely because it
mentions an identifier.  Ambiguous material stays linked to its source.  Mind
and Psyche own subsequent archive storage and retrieval.  “Archive” means
read-only preservation with a locator; it does not mean removal.

## POC acceptance and non-goals

The prototype should demonstrate typed start and self-restart request
acceptance, request idempotency, generation fencing, predecessor preservation
on successor failure, queue recovery after supervisor interruption, alias
claim import, job-name reservation, typed origin outcomes, and subscription
events without polling. The fixture can demonstrate exact-turn correctness; a
real bridge/readiness adapter needs separate integration evidence. It should
expose the SQLite rows and deterministic fixture observations so these
properties can be inspected.

It does not prove production sockets, binary Signal codecs, Ethos emission,
Sema implementation, native harness session resume, authenticated Creo,
Curriculum delivery, quota accounting, full Mind/Psyche retrieval, or the
actual migration.  Those are follow-on contracts and integration work, not
implicit claims of this POC.

### Implementation and validation matrix

| Area | POC status | Production decision / pending evidence |
| --- | --- | --- |
| State store | local SQLite, one supervisor process | one Flow Core writer behind compiled Signal and Sema |
| Start/restart CLI | implemented surface specified above | native `flow` binary contract remains to be authored |
| Restart provenance | bridge session must resolve to stored binding | real harness bridge smoke pending `launch_check` |
| Exact-turn origin | fixture boundary can supply it | real adapter must stamp and resolve it; no transcript guessing |
| Readiness and retirement | planned POC state model | actual harness readiness/retirement smoke pending; no termination guarantee claimed |
| Idempotency/recovery/fencing | POC acceptance target, test evidence required | production uses durable idempotent outbox and generation fences; proposed until built |
| Skill delivery | receipt check specified | each harness must prove callable Skill interface or return unsupported |
| Mind/Psyche migration | source links and read-only archive design | importer, stores, and retrieval are pending |

The local POC supervisor is deliberately not a distributed authority.  The
production Flow Core is the single writer for lifecycle state and the durable
outbox.  Consumers apply an effect only when its request id and generation are
current, making a replay after a crash safe to retry.  These are production
requirements proposed by this design; the document does not report them as
implemented or tested until the corresponding evidence exists.

## Source inventory

The governing vision is [Flow Nexus](/home/li/primary/Vision/flowNexus.md),
[Nexus](/home/li/primary/Vision/nexus.md), [Sema](/home/li/primary/Vision/sema.md),
and [Remembering](/home/li/primary/Vision/remembering.md), alongside the raw
psyche records [flow anatomy](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/flowAnatomy.md),
[dispatch](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/easyFlowDispatch.md),
[origin](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/flowOriginClue.md),
[restart](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/flowRestart.md),
[identity layers](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/flowIdLayers.md),
[subflow identity](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/subflowIdentity.md),
[workspace provisioning](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/workspaceProvisioning.md),
[caller identity](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/callerIdentity.md),
[transcript over files](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/transcriptOverFiles.md),
[structured log](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/structuredLog.md),
[sprawl](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/sprawlFix.md),
[shared primary](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/oneSharedPrimary.md),
[Mind memory](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/mindMemory.md),
[Psyche versus Mind](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/psycheVsMind.md),
[no more branches](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/noMoreBranches.md),
[launch on main](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/launchOnMain.md),
and [commit binding](/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/orchestrateCommitBinding.md).

The current helper evidence is [flow_id.rs](/home/li/primary/repos/harness/src/flow_id.rs)
and [flow_id CLI](/home/li/primary/repos/harness/src/bin/flow_id.rs).  The
existing [primary skeleton proposal](/home/li/primary/PRIMARY-SKELETON.md) is
concurrent design evidence, not accepted vision.  Historical samples
[4647d2](/home/li/primary/flows/4647d2/log.md),
[01a03603](/home/li/primary/flows/01a03603/log.md), and
[7b4d4c](/home/li/primary/flows/7b4d4c/log.md) show the material that
migration must preserve without making Flow a narrative store.
