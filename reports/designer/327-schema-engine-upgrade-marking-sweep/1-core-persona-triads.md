*Kind: Triage · Topic: schema-engine-upgrade-marking-sweep slice A · Date: 2026-05-24*

# 327/1 · Slice A — core persona triads

Subagent A's edits for §6.1 of the marking sweep frame. Five
component triads, ten repos. Every repo had a current
`ARCHITECTURE.md` on disk; two repos (`persona-spirit`,
`orchestrate`) also had `INTENT.md`. All edits applied; all
commits landed cleanly via `jj describe`; no pushes.

## §1 · Edit summary table

| Repo | ARCH | INTENT | Triad slot | jj change | commit |
|---|---|---|---|---|---|
| `persona-spirit` | edited | edited | spirit daemon | `wtwvzzxn` | `68ab513a` |
| `signal-persona-spirit` | edited | absent | spirit ordinary contract | `xkskousw` | `608e1654` |
| `mind` | edited | absent | mind daemon | `kttlmpon` | `190ed166` |
| `signal-mind` | edited | absent | mind ordinary contract | `rpvqwsyt` | `1e4f6e40` |
| `router` | edited | absent | router daemon | `snmlruus` | `5352ec3d` |
| `signal-router` | edited | absent | router ordinary contract | `kuszxqow` | `3b2f0f34` |
| `message` | edited | absent | message daemon | `wlvqmylp` | `01d9e086` |
| `signal-message` | edited | absent | message ordinary contract | `kopustlm` | `7861eb40` |
| `orchestrate` | edited | edited | orchestrate daemon | `lnxopzny` | `75be54f9` |
| `signal-orchestrate` | edited | absent | orchestrate ordinary contract | `kpnlvsyr` | `85b5dee4` |

Eight repos got an ARCH edit only; two (`persona-spirit`,
`orchestrate`) got ARCH + INTENT edits. Zero creations
(every ARCH already existed). Zero blockers.

## §2 · Per-repo notes

### §2.1 · `persona-spirit` (daemon)

- File: `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md`
- Existing tail: free-prose status paragraphs ending at line 354
  ("The next implementation step is subscription event delivery or
  spirit-to-mind owner-Mutate forwarding."). No `## See also` section
  exists in this file. Schema-engine upgrade section appended at the
  end of the file.
- Per-component concerns: first MVP cutover target; v0.1.0 → v0.1.1
  handover via `primary-x3ci` named as the realistic test surface;
  called out the handover-marker / readiness / completion path
  through `signal-version-handover` interacting with the schema's
  VersionProjection emission; called out
  `tests/daemon.rs:236-241` upgrade-socket witnesses as the staged-
  replacement guarantees that must keep passing; called out owner-vs-
  ordinary frame isolation (`tests/daemon.rs:234` /
  `:235`) as a discipline the schema-derived dispatcher must
  preserve.
- INTENT.md edit: new `## Pending schema-engine upgrade` section
  inserted before the existing `## See also` section
  (`INTENT.md:127`). Same status/target/sequence shape as the
  ARCH section; the per-component concerns paragraph is
  pilot-focused — Spirit lands first because it already has the
  upgrade socket plus split-package nix infrastructure needed to
  prove cross-version schema projection.
- jj: `wtwvzzxn` / commit `68ab513a` — `spirit: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.2 · `signal-persona-spirit` (ordinary contract)

- File: `/git/github.com/LiGoldragon/signal-persona-spirit/ARCHITECTURE.md`
- Existing tail: `## Code Map` block at lines 117-123. No `## See
  also` section exists in this file. Schema-engine upgrade section
  appended after the Code Map.
- Per-component concerns: noted the persona- prefix still on the
  repo per /318 pilot block (rename lands after schema-engine cutover
  proves the macro library shape); noted that the existing three-
  layer model section (`signal-persona-spirit/ARCHITECTURE.md:17-65`)
  documents contract-local verbs (`State`, `Record`, `Observe`,
  `Watch`/`Unwatch`, mandatory `Tap`/`Untap`) the schema source must
  encode rather than collapse; observed that the `schemas/`
  directory and `spirit.schema` file already exist on disk as the
  early shape — operator work via `primary-ezqx.1` lands the macro
  that consumes them.
- INTENT.md: absent in this repo.
- jj: `xkskousw` / commit `608e1654` — `spirit: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.3 · `mind` (daemon)

- File: `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- Existing tail: `## See Also` section at line 696 with one link
  to `../signal-mind/ARCHITECTURE.md`. Schema-engine upgrade
  section inserted **before** that See Also.
- Per-component concerns: largest hand-written contract today (per
  /166); explicitly called out that mind is intentionally not the
  pilot ("its surface is larger and its choreography/subscription
  state more entangled than Spirit's"); called out the schema-
  derived dispatcher must preserve the existing `MindRoot` actor-
  tree routing through `IngressPhase` → `DispatchPhase` →
  `DomainPhase` → `StoreSupervisor` (per `mind/ARCHITECTURE.md:135-150`);
  named the subscription destination split (`SubscriptionManager`
  + `StreamingReplyHandler` + `SubscriptionDeltaPublisher`) at
  `mind/ARCHITECTURE.md:183-210` that the macro must continue to
  emit support for; called out the `ChoreographyAdjudicator`
  outbound caller path to orchestrate's owner socket
  (`mind/ARCHITECTURE.md:454-478`); named the `MindTables` schema v7
  shape (typed `memory_graph`, `thoughts`, `relations`,
  subscription registration tables) as the storage descriptors the
  schema must emit equivalents of.
- INTENT.md: absent.
- jj: `kttlmpon` / commit `190ed166` — `mind: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.4 · `signal-mind` (ordinary contract)

- File: `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`
- Existing tail: `## See Also` at line 462 with seven links.
  Schema-engine upgrade section inserted **before** that See Also.
- Per-component concerns: called out that the schema must encode
  all three relations on this contract (typed mind graph;
  work-and-memory graph; channel choreography) and the mandatory
  `Tap`/`Untap` plus the streaming-grammar close-by-retract
  pairings; named the existing `signal_channel!` block at
  `signal-mind/ARCHITECTURE.md:134-182` as the destination the
  schema must replace; called out closed-enum integrity of
  `ChannelMessageKind`, `ChannelDuration`, `MindUnimplementedReason`,
  `ThoughtKind`, and `RelationKind` (these are not stringly-typed
  today and must survive schema-to-Rust emission).
- INTENT.md: absent.
- jj: `rpvqwsyt` / commit `1e4f6e40` — `mind: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.5 · `router` (daemon)

- File: `/git/github.com/LiGoldragon/router/ARCHITECTURE.md`
- Existing tail: `## See Also` at line 537 with five links.
  Schema-engine upgrade section inserted **before** that See Also.
- Per-component concerns: 4-hop delivery durability (per
  `primary-07ot`) interacts with schema-derived dispatch — the
  macro's dispatcher emit must cover ack-on-delivery semantics;
  noted the existing `## 4 · Invariants` (`router/ARCHITECTURE.md:402-483`)
  enumerates ordering guarantees the schema-derived dispatcher
  must preserve (message acceptance before delivery attempt,
  delivery result before post-delivery events, durable effects
  before externally visible delivery/subscription events); named
  the router-owned sema tables (`messages`, `channels`,
  `channels_by_triple`, `adjudication_pending`, `delivery_attempts`,
  `delivery_results`, `meta`) as needing schema storage
  descriptors that emit equivalent registrations; called out
  `RouterTables::open()` schema-version guard must keep failing
  closed on mismatch (`router/ARCHITECTURE.md:118-121`); flagged that
  the `signal-router` bootstrap document is typed data records,
  not request/reply — the schema must distinguish it from the
  live `Observe` channel.
- INTENT.md: absent.
- jj: `snmlruus` / commit `5352ec3d` — `router: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.6 · `signal-router` (ordinary contract)

- File: `/git/github.com/LiGoldragon/signal-router/ARCHITECTURE.md`
- Existing tail: `## See also` at line 247 with five links.
  Schema-engine upgrade section inserted **before** that See also.
- Per-component concerns: 4-hop delivery durability per
  `primary-07ot`; the macro must emit closed `RouterDeliveryStatus`
  and `RouterChannelStatus` enums with the positive `Missing`
  variant (no `Unknown` sentinel) and keep `MessageTraceMissing`
  as a distinct reply variant rather than a status field (named
  the existing closed-enum integrity discipline at
  `signal-router/ARCHITECTURE.md:126-156`); noted that the
  bootstrap-document vocabulary (`RouterBootstrapDocument`,
  `RouterBootstrapOperation`, `RegisterActor`,
  `GrantDirectMessage`, `InstallStructuralChannels`) is typed
  data records consumed at daemon startup — not a live
  request/reply channel — and the schema must distinguish those
  from the `Observe` channel without folding both into a single
  dispatcher; explicitly excluded owner-only channel policy
  orders (they live in `owner-signal-router`, slice C territory).
- INTENT.md: absent.
- jj: `kuszxqow` / commit `3b2f0f34` — `router: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.7 · `message` (daemon)

- File: `/git/github.com/LiGoldragon/message/ARCHITECTURE.md`
- Existing tail: `## See Also` at line 219 with three links.
  Schema-engine upgrade section inserted **before** that See Also.
- Per-component concerns: cross-component messaging; schema
  cutover should preserve `(Send <destination> [<text>])` CLI form
  (bracket-string body per `primary-36iq`) and the matched
  `(Inbox <recipient>)` form; called out that the schema-derived
  dispatcher must keep the two relations (CLI/owner ingress on
  `message.sock` mode 0660; internal forward on `router.sock` mode
  0600) distinct — plain `MessageSubmission` is legal only on
  Relation A, `StampedMessageSubmission` only on Relation B (per
  the existing payload-by-payload legality discipline at
  `message/ARCHITECTURE.md:124-148`); called out the daemon's typed
  `MessageDaemonConfiguration` argv path via `nota-config` must
  keep working under the schema cutover; flagged the stateless
  boundary discipline (no durable message ledger inside `message`,
  per `message/ARCHITECTURE.md:148`) — storage-descriptor emission
  must not accidentally introduce a local store.
- INTENT.md: absent.
- jj: `wlvqmylp` / commit `01d9e086` — `message: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.8 · `signal-message` (ordinary contract)

- File: `/git/github.com/LiGoldragon/signal-message/ARCHITECTURE.md`
- Existing tail: `## See also` at line 270 with two links.
  Schema-engine upgrade section inserted **before** that See also.
- Per-component concerns: cross-component messaging; CLI form
  `(Send <destination> [<text>])` per `primary-36iq`; the schema
  must keep the **two named relations sharing one root family**
  invariant — `MessageRequest` carries `MessageSubmission` (legal
  on Relation A only) and `StampedMessageSubmission` (legal on
  Relation B only); these payload-by-payload legality rules at
  `signal-message/ARCHITECTURE.md:98-100` need schema enforcement,
  not runtime string checks; closed `MessageKind` enum (`Send`,
  `Inbox`) and `MessageUnimplementedReason` must survive
  emission; `MessageOrigin` import from `signal-persona-origin`
  must continue to work under the schema's import grammar.
- INTENT.md: absent.
- jj: `kopustlm` / commit `7861eb40` — `message: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.9 · `orchestrate` (daemon)

- File: `/git/github.com/LiGoldragon/orchestrate/ARCHITECTURE.md`
- Existing tail: `## See Also` at line 308 with eight links.
  Schema-engine upgrade section inserted **before** that See Also.
- Per-component concerns: cluster/lifecycle orchestration; schema
  cutover after Spirit + mind; sequencing matters because
  orchestrate consumes `owner-signal-persona-router` and
  `owner-signal-persona-harness` for the authority chain (per
  `orchestrate/ARCHITECTURE.md:118-132`), so those downstream owner
  contracts should land on the schema engine before orchestrate's
  outbound calls cut over; called out that orchestrate already
  implements `OperationLowering` as the contract-to-Component-Command
  translation point (per `src/lowering.rs`) — the schema must keep
  that boundary intact and have the macro emit the same lowering
  shape; called out the dual-socket discipline (owner contract
  `owner-signal-orchestrate` with `Create` / `Retire` / `Refresh`
  distinct from ordinary `signal-orchestrate` with `Claim` /
  `Release` / `Handoff` / `Observe` / `Submit` / `Query` /
  `Watch` / `Unwatch`); named the sema-backed tables (`claims`,
  `roles`, `repositories`, `activities`, `activity_next_slot`,
  `divergences`) as needing equivalent schema storage-descriptor
  emission; lock-file projection from accepted daemon state must
  keep working.
- INTENT.md edit: new `## Pending schema-engine upgrade` section
  inserted **before** the existing trailing source-link line
  (`INTENT.md:51-52`). Per-component concerns paragraph notes
  that lane definitions stay data (not closed role enums) under
  the schema — the schema must enable dynamic-role registry
  persistence without baking the live role set into the wire.
- jj: `lnxopzny` / commit `75be54f9` — `orchestrate: mark
  pending schema-engine upgrade per /326-v13 + /324`.

### §2.10 · `signal-orchestrate` (ordinary contract)

- File: `/git/github.com/LiGoldragon/signal-orchestrate/ARCHITECTURE.md`
- Existing tail: `## See Also` at line 174 with six links.
  Schema-engine upgrade section inserted **before** that See Also.
- Per-component concerns: cluster/lifecycle orchestration
  contract; schema cutover after Spirit + mind; called out that
  the schema must preserve the closed reply variants
  (`ClaimAcceptance`, `ClaimRejection`, `ReleaseAcknowledgment`,
  `HandoffAcceptance`, `HandoffRejection`, `RoleSnapshot`,
  `ActivityAcknowledgment`, `ActivityList`, `PartialApplied`,
  `ObservationOpened`, `ObservationClosed`) without an `Unknown`
  sentinel; named the typed values (`RoleIdentifier`,
  `HarnessKind`, `ScopeReference`, `WirePath`, `TaskToken`,
  `ScopeReason`, `TimestampNanos`, plus the divergence
  vocabulary `PartialApplied` / `ApplicationSuccess` /
  `ApplicationFailure` / `DownstreamComponent` /
  `ApplicationFailureReason`) as needing validation hooks the
  schema emits without losing the `from_wire_token` /
  `from_absolute_path` / `from_text` discipline; referenced the
  existing Migration history section (`signal-orchestrate/ARCHITECTURE.md:18-39`)
  as the destination verb set the schema must encode.
- INTENT.md: absent.
- jj: `kpnlvsyr` / commit `85b5dee4` — `orchestrate: mark
  pending schema-engine upgrade per /326-v13 + /324`.

## §3 · Cross-cutting observations

### §3.1 · ARCH file structure varies, schema-engine section placement was always natural

Eight of the ten repos already had `## See also` (lowercase) or
`## See Also` (titlecase) sections; the schema-engine upgrade
section landed immediately before. Two repos
(`persona-spirit/ARCHITECTURE.md`, `signal-persona-spirit/ARCHITECTURE.md`)
had no See-also section at all — Spirit's daemon ARCH ends with a
free-prose status block; Spirit's contract ARCH ends with a Code
Map block. In those two repos the new section went at the very
end. Frame §4 said "before See also if present" which mapped
cleanly to both cases.

### §3.2 · INTENT.md presence is sparse

Only two of the ten repos carry INTENT.md (`persona-spirit`,
`orchestrate`). The other eight repos do not. Per frame §3.1 the
target was "edit INTENT.md when present" — so no creations were
needed. The absence in `mind`, `router`, `message`, and their
contracts is a cross-cutting gap from a different sweep
(`skills/repo-intent.md`'s INTENT-everywhere discipline). Not in
scope for this marking sweep, but worth flagging to the
orchestrator for the overview file. If the orchestrator wants
INTENT.md created where absent, that's a follow-on sweep with a
different shape — psyche-derived intent rather than designer-
authored migration marking.

### §3.3 · Per-component concerns landed concretely, not generically

Frame §4 said "populate only when concrete specifics exist; leave
empty otherwise." Every repo got a concrete concerns paragraph
because every component had real specifics worth flagging — the
upgrade-socket / handover-marker pair in Spirit, the
choreography destination split in mind, the 4-hop delivery
ordering in router, the two-relations-one-root invariant in
message, the `OperationLowering` boundary in orchestrate, and so
on. The frame's optional field became non-optional in practice
because every component carries non-trivial state.

### §3.4 · `signal-persona-spirit` carries a live schemas/ directory already

The contract repo at `/git/github.com/LiGoldragon/signal-persona-spirit/`
already has `schemas/` and `spirit.schema` on disk
(per the directory listing). The schema-engine upgrade work has
already begun there. The marking section for this repo notes that
fact; the existing schema file is the early shape that
`primary-ezqx.1` will consume. No other repo in slice A had a
schema file or directory.

### §3.5 · Sequencing language stayed consistent

Every per-repo Sequence field opens with the same sentence:
"Spirit is the MVP pilot landing first via `primary-ezqx.1`."
This is the canonical phrasing from frame §3.1's template and
keeps the cross-component story uniform. The mind / router /
message / orchestrate sections then add component-specific
ordering notes (mind not as pilot because of surface size; router
+ message cutover together because of the shared ingress path;
orchestrate after mind because of the authority chain).

## §4 · Hard-constraint compliance

- **One new section per file** — yes; every edit was a single
  `## Pending schema-engine upgrade` section. No other content was
  changed in any of the ten ARCH files or two INTENT files.
- **Placed near the end, before See also when present** — yes;
  eight files had See-also; two did not (Spirit's pair), and
  those got end-of-file placement.
- **NOTA examples in bracket-string form per `primary-36iq`** —
  only the message + signal-message sections include the form
  `(Send <destination> [<text>])`; the brackets are correct per
  the rule.
- **Mermaid label discipline** — no mermaid added; not needed for
  any of these edits.
- **No emojis** — yes.
- **No `---` horizontal-rule lines** — yes; none added in any of
  the new sections or in this triage report. The existing files
  carried some `---` separators in places; those were left
  untouched per the "no other content changes" hard rule.
- **jj headless inline messages only** — yes; every commit used
  `jj describe -m '<msg>'` with the message inline. No editor
  fallback. All ten commits produced their change IDs and commit
  hashes on the first try.
- **Per-repo commit with `<component>: mark pending schema-engine
  upgrade per /326-v13 + /324`** — yes; ten commits, ten matching
  messages. Note that the `<component>` short name is the
  component (`spirit`, `mind`, `router`, `message`,
  `orchestrate`) so both the daemon repo and the contract repo
  in each triad share the same component-name in their commit
  message (e.g., both `persona-spirit` and `signal-persona-spirit`
  commits read `spirit: mark pending...`).
- **No push to remotes** — yes; commits are local only.
- **No `/nix/store` filesystem search** — yes; not used.

## §5 · What carries forward to orchestrator overview

- Slice A produced 10 edits and 2 INTENT-file edits, with 0
  creations and 0 blockers.
- INTENT.md absent in 8/10 repos is a workspace-wide gap visible
  across slices, worth surfacing in the orchestrator's `5-overview.md`.
- The schema-engine upgrade section is now uniformly discoverable
  at the tail of every Slice A ARCH; future operators landing on
  any of these repos will see the migration marker and the four
  cross-reference reports.
- The per-component concerns paragraphs land concrete component
  truth that operators implementing `primary-ezqx.1` per-component
  cutover beads will need: handover-socket interactions in Spirit,
  destination-split actors in mind, ordering invariants in router,
  two-relations discipline in message, `OperationLowering` boundary
  in orchestrate.

## Slice A summary: 12 edits + 0 creations + 0 blockers.

Counts ten ARCH edits + two INTENT.md edits = 12 file edits; zero
creations (every ARCH and the two present INTENT.md files
existed); zero blockers.

## See also

- `reports/designer/327-schema-engine-upgrade-marking-sweep/0-frame-and-method.md`
  — orchestrator frame for this sweep.
