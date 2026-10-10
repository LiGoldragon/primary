# Coordination-liveliness capability — revised design (B-ruling revision)

Status: authoritative pickup for implementer lanes. Read-only design, revised
against psyche rulings B1–B4 relayed by the coordinator. Supersedes the
message→router→harness MVP proposed in the prior checkpoint. Where this report
and the prior chat checkpoint disagree, this report wins.

Owning lane: `MessengerLivenessRename` (session `WorktreeLifecycle`).
Companion: `LaneAbandonmentMachinery` is implementing §4 NOW against the landed
`ConcludeWorktree`; treat that machinery as landing, not proposed.

## 0 · What changed in this revision

- **B1 (major redirect).** All local messaging goes through the **messenger**.
  The router shrinks to a **host-to-host leg only**, reached via a **deferred
  external-host capability inside messenger**. The messenger now owns local
  routing, delivery, the durable inbox/ledger, the thread model, and the
  harness-delivery leg. The prior "deploy message→router→harness" MVP is
  withdrawn. One load-bearing phrase remains ambiguous and is returned to the
  coordinator, not guessed (see §7).
- **B2.** Three-layer liveliness kept as designed, **signed off 2026-07-17**
  (§0c: "yes, messenger-first, liveness first"; §3 layer 3 amended by psyche
  ruling to an activity read); the delivery leg goes through **messenger**, not
  router.
- **B3.** Lane `Suspect` + grace **accepted**; durations are matter, set in §4.
  `ConcludeWorktree`/`RequestWorktree`/`WorktreeStatus::Abandoned` have landed
  (orchestrate `37fac745`, signal-orchestrate `9d030d0f`). The one open call —
  whether agent-initiated `ConcludeWorktree(Merged|Rejected)` cascades to lane
  release — is decided in §4c.
- **B4.** Both renames completed as one post-landing sweep; remotes in scope; no
  compatibility shim. Plan in §6.

## 0b · Psyche rulings folded in (2026-07-17)

Four rulings from the psyche working session of 2026-07-17, folded into §2g,
§3, and §7 below. Quotes are verbatim; sections carry a "psyche-ruled
2026-07-17" marker where amended.

- **§3 amended — the delivery-probe layer is replaced by an activity read.**
  Verbatim: "better to actually read the agent's latest activity; a single
  command could take hours (rebuilding nixos from source)". Layers 1–2 (pidfd
  exit-push, activity refresh) drew no objection and stand.
- **§7 resolved — launch-minted agent ID as the endpoint.** Verbatim: "a lane
  should have a agent ID, which becomes our endpoint. Same short hashes we've
  been using for IDs in spirit, mind, wherever (4 chars + (adjusted for
  conflicts)). so each time a harness is launched, it gets an ID (or re-uses
  it if it's a resumed session) assigned, and knows it in his initial prompt.
  and messenger knows which process is which ID"
- **Cold-session delivery accepted (new §2g).** Asked whether the messenger
  may deliver to a non-live session by respawning the harness with its resume
  identity and the message as the next turn, the psyche ruled verbatim: "yes,
  that is exactly what should happen. unless the agent is marked as killed, in
  which case the message can bounce back with a notice of dead agent, for
  now". The "for now" is a hedge, tracked as bead `primary-pm92`.
- **Open psyche question, not ruled:** "how do we deal with claude subagents?"
  — see §7b. Do not resolve by taste. (A parent-only working model was later
  adopted via general blessing — see §0c and §7b; psyche review pending.)

## 0c · Second-batch rulings (2026-07-17, later same day)

- **Program spine ACCEPTED.** Verbatim: **"yes, messenger-first, liveness
  first"** — the messenger promotion program is a settled go, with liveness
  ordered first in the program.
- **General blessing.** Verbatim: **"go with your leans, good enough for me"**
  — applied by the manager to the then-open items. Lean-based applications are
  flagged for psyche review; they are not direct rulings:
  - Migration-safety hardening accepted (automatic pre-migration store backup
    + migration tests against captured real stores) → bead `primary-4khu`.
  - Orphaned rescue-preserve reap accepted, sequenced (recovery lane terminal,
    then fixture capture, then delete) → bead `primary-te4v`.
  - Claude subagents: parent-only working model adopted (see §7b), psyche
    review pending.
  - Two design tensions resolved by manager lean, psyche review pending:
    (i) the **messenger** owns the authoritative process↔ID map; orchestrate's
    registration-time discovery is a feed into it (the reconciling reading in
    §7); (ii) **terminal-cell** is the launcher-side component that mints the
    agent ID at harness launch — it owns session directories and spawning.
    **[SUPERSEDED same day: both leans are overtaken by the §0d Q2 ruling —
    the orchestrator is the mint, launch delegates through the harness
    component, and the messenger's registry becomes the consumer view of
    IDs + threads. See §0d and bead `primary-sdgy`.]**

## 0d · Third-batch vision (2026-07-17, dictated) — contention flow, feature lanes, session identity, threads

Dictated psyche vision batch, recorded verbatim with grading. Two clarifications
the manager posed were answered by the psyche shortly after dictation; both are
**rulings** below, not open questions. Superseded earlier records are marked in
place (§0c, §7) with history kept.

- **Subscription primitive: liked, deferred — not now-scope.** Verbatim: "Okay,
  so I like the idea of when X happens or when lane Y ends send a message.
  That's a cool idea, but for now I just wanted a message type to come in to
  the agent that tries to unregister, well, I guess will unregister his lane".
  The general when-X-happens/when-lane-ends subscription stays a tracked
  future item; only the specific release-time message below is now-scope.

- **Now-scope (a) — release-time contention message.** A new message type is
  delivered to the agent unregistering (releasing) a repo's main lane, telling
  him a feature branch/worktree was started off that repo while he held it.
  Verbatim continuation: "which is that now this branch while he was working
  on it had a work tree, or sorry, ostensibly he's working on main and because
  that's what we do by default".

- **Now-scope (b) — automatic contention answer.** An agent trying to edit a
  taken repo is answered automatically. Verbatim: "and then somebody tried to
  edit that repo and then saw that it just automatically responds saying,
  okay, well, that repo is taken".

- **Now-scope (c) — feature-named lanes become feature branches.** Verbatim:
  "when you register a lane, you have to give it a name of what you're working
  on, like a pascal case sort of feature. That you're going to implement and
  then you can even give a description, but that's what's going to be used to
  create the feature branch."

- **Now-scope (d) — default auto-worktree in a known place.** Verbatim: "just
  by default, it creates a work tree in a known place with the feature branch
  called after the feature that was used by the agent."

- **Now-scope (e) — orchestrator tracks branches and auto-rebases; mains stay
  clean.** Verbatim: "if nothing has worked on it since, like the orchestrator
  component can just try to rebase or merge whatever is more correct on main
  … whatever work comes in first is going to be based off the latest main. So
  it's just going to be a simple rebase operation. And well, it should know
  because it keeps track. And then we can keep those main trees clean."

- **RULING (Q1) — MVP merges clean branches into main, no review gate.** Asked
  whether a cleanly-rebasing finished branch lands on main automatically with
  no review (block/release-message reserved for conflicted or unfinished
  branches) or whether every branch awaits review, the psyche ruled verbatim:
  **"we'll build review into that later. first MVP doesnt, just merge in
  main"**. Review is deferred-explicit, tracked as bead `primary-njmu` so
  "later" cannot drift. The whole now-scope feature set is tracked as bead
  `primary-qz9l`.

- **Topic hedge (preserved, unresolved).** Verbatim: "And yeah, I guess that
  all goes under some kind of topic. That's session dependent" — the thought
  trailed off; not design authority.

- **Identity — main session ID allocated before process start.** Verbatim:
  "there's a main session ID, it's going to be this main session ID, which is
  just allocated to the process before it starts. And when that session
  begins, it gets given that idea, the agent knows. That's their main process
  ID. And that's how messages work. So yeah, the orchestrator can keep track
  because he's going to spawn these agents. And then the messenger can get a
  list of existing agent IDs."

- **RULING (Q2) — the orchestrator is the mint; launch delegates through the
  harness component.** Asked whether the messenger is a mint service called by
  the spawning orchestrator, or the orchestrator mints internally with the
  messenger as a passive list consumer, the psyche ruled verbatim: **"the mint
  is the orchestrator. he creates an agent id and will eventually launch it
  (through another daemon I think; maybe agent has all the harness launching
  logic - but where is that now? Or was it harness? thats fine too)"**. The
  manager confirmed from scout evidence that the ARCHITECTURE authority chain
  orchestrate→harness via `meta-signal-harness` already carries agent-run
  lifecycle; terminal-cell owns PTY/session directories beneath it.
  **Supersessions, recorded honestly:** this supersedes BOTH the §0c
  manager-lean "terminal-cell mints the agent ID at launch" AND the
  messenger-side mint semantics built into train packet 2.1 the same day (the
  messenger keeps its durable registry as the **consumer view** of IDs +
  threads, fed by the orchestrator; the mint operation relocates
  orchestrator-side). Follow-up tracked as bead `primary-sdgy` (relocate mint
  authority; reshape packets 2.1-amend/2.2/2.3).

- **Messenger model — IDs and threads only.** Verbatim: "the orchestrator is
  aware of also the agent IDs, but on the messenger side, there's only IDs and
  then threads." A thread MAY carry a relation to what is being worked on —
  hedged, verbatim: "the messenger can have threads, which is not directly
  related yet, or could have a field where it can relate to a certain feature
  branch or orchestrator lane and work tree, basically, like a repo, right,
  and the feature branch. This is sort of like what is being worked on." The
  hedge ("not directly related yet, or could") is preserved; the relation
  field is optional-future, not committed.

- **Manager auto-subscription to subagent threads.** Verbatim: "these threads,
  a subscription page, they can be subscribed to automatically by the manager
  for their sub agents so that they can talk to all their sub agents in one
  go, or so that anyone can talk to all their sub agents."

- **Messages carry origin; subagent-obedience doctrine seed.** Verbatim: "the
  incoming messages get the origin, like who sent this so that sub agents can
  be told to not necessarily obey every message or to consult or to escalate
  first and ask their manager if something comes in and they're not sure what
  they should do. It seems to contradict their initial instructions." Doctrine
  seed for the skills side, pending manifestation (skills deliberately not
  edited by this capture): subagents do not blindly obey incoming messages;
  they consult or escalate to their manager when a message contradicts their
  initial instructions.

## 0e · Fourth-batch blessing (2026-07-18) — open slate adopted by leans

The psyche answered the remaining open slate with, verbatim: **"go with your
leans, and report back with visuals"**. The manager's leans are ADOPTED —
each recorded accepted-via-general-blessing with a PSYCHE-REVIEW FLAG,
manager-lean wording preserved:

- **Deploy v0.8.0** — adopted; deployment dispatched in parallel with this
  record. (Production was v0.7.2; main carries reply-hardening,
  migration-safety, the teardown fix, and pidfd exit-watch.)
- **Sema-engine evolution primitive: BUILD.** Lean verbatim: "each table
  family registers how to read its older shapes; the engine applies the chain
  at store open, replacing hand-written raw-catalog migrations." → bead
  `primary-rlg7`.
- **Real repo identity: build NOW** as early train packet 0.4 (repo = real
  remote identity; local path incidental — the identity principle itself is a
  direct psyche ruling; only the timing is lean-adopted). → bead
  `primary-9wxr`.
- **Harness lifecycle push event stream** (turn-started/idle/exited):
  accepted, sequenced AFTER the messenger core — not on the critical path.
  Resolves §3's open producer question to build-later. → bead `primary-s4ep`.
- **Claude live-delivery posture:** Claude sessions launch through our
  launcher with the cooperative channel flag so they are live-reachable;
  plainly-launched sessions stay cold-respawn-only; the Anthropic-cloud
  remote-control path is off-limits by default (closed-by-default privacy).
  Pre-task: the flag is unverified on the installed build. → bead
  `primary-vpdx`.
- **Codex delivery: deferred** (deferred-by-lean). → bead `primary-ohrb`.

**§2e push-vs-pull reconciliation (manager-applied doctrine, flagged for
review):** §0d's "the messenger can get a list of existing agent IDs"
(pull-shaped) reconciles with §2e's push-not-pull as: the orchestrator PUSHES
minted identities into the messenger's delivery registry; the messenger "gets
the list" by reading its own pushed-to registry. No polling exists anywhere;
the psyche's sentence is satisfied by the registry being present, not by a
query to orchestrate.

## 1 · Ground truth (deltas since the prior checkpoint)

- `signal-orchestrate` now carries `ConcludeWorktree(WorktreeConclusionRequest)`
  and `RequestWorktree(WorktreeRequest)` on the ordinary tier;
  `WorktreeConclusion = Merged | Rejected`; `WorktreeStatus::Abandoned` exists;
  replies `WorktreeConcluded` / `WorktreeConclusionRejected(UnmergedWorkPresent…)`.
- `orchestrate/src/worktree.rs`: `Merged` teardown is **gated** — refused unless
  the work is already an ancestor of `main` (this is where "never auto-rm
  unpushed" is now hard-enforced, not advisory). `Rejected` has its own path. A
  `flag_abandoned` sweep sets `WorktreeStatus::Abandoned` on orphaned worktrees.
- Router source is legibly split into a **local-delivery reducer**
  (`harness_delivery.rs`, `harness_registry.rs`, `delivery.rs`, `route.rs`,
  `channel.rs`, local `message.rs`) and a **host-to-host trust plane**
  (`remote_router.rs`, `peer_delivery.rs`, `peer_session.rs`,
  `criome_attestation.rs`, `forward_attestation.rs`, `identity_proof.rs`,
  `criome_client.rs`, `adjudication.rs`, `authorized_object*.rs`). This split is
  exactly the B1 fault line.
- Nothing in the `signal-*` messaging plane is deployed/running; only
  `orchestrate-daemon` runs. `SendMessage` (harness) remains the only path
  agents actually use today, and it is unbridged from the durable plane.

## 2 · Messenger under the new architecture (B1)

### 2a · Component shape (component-architecture)

The messenger stops being a stateless ingress and becomes the **full local
messaging component**: a stateful triad daemon.

- Runtime crate `message`(→`messenger`), binary `messenger-daemon`, thin CLIs
  `messenger` / `meta-messenger`.
- **Signal plane** — ingress (`Submit`), inbox reads (`QueryInbox`), and a
  **delivery subscription** (a harness subscribes once; the messenger pushes
  current inbox + deltas — this is the "router pushes inbox into harness" leg,
  now owned by messenger).
- **Nexus plane** — local routing decisions: recipient resolution, thread
  resolution, local-vs-remote classification, and the **external-host escalation
  effect** (to router; deferred).
- **SEMA plane** — `messenger.sema`, newly non-empty. Durable tables: message
  ledger (slots + commit time), per-recipient inbox, **thread index**, and a
  **local delivery registry** (recipient identity → harness delivery endpoint).

This flips two current `message` ARCHITECTURE invariants that must be rewritten:
"no durable message ledger / stateless" and "SEMA honestly empty." The messenger
is now the single durable owner of local message state.

### 2b · What moves from router into messenger

| Concern | Today (router) | After B1 |
|---|---|---|
| Local delivery attempt to harness terminal | `harness_delivery.rs` | **messenger** |
| Local delivery-target registry | `harness_registry.rs` | **messenger** (fed by orchestrate reachability push) |
| Pending/backpressure queue | `delivery.rs` (`DeliveryQueue`) | **messenger** |
| Local routing decision | `route.rs`/`channel.rs`/`message.rs` | **messenger** |
| Message ledger / inbox / slots | `router.sema` (`tables.rs`) | **messenger** (`messenger.sema`) |
| Thread index | (was "deliberately open") | **messenger** (see §2d) |

### 2c · What stays in router / stays stubbed

- **Router = host-to-host leg only, deferred.** Remaining in router:
  `remote_router.rs`, `peer_delivery.rs`, `peer_session.rs`, and the whole
  attestation/identity/adjudication set. These carry cross-host delivery where
  `SO_PEERCRED` cannot vouch and BLS/attestation is required.
- **External-host capability in messenger is stubbed.** When recipient
  reachability names a remote host, the messenger's Nexus emits an
  `ExternalHost` escalation to router. Until built, it returns a typed
  `RequestUnimplemented(NotInPrototypeScope)`. No local traffic ever touches
  router.
- **Thread subscriptions** (subscribe to a thread's tail) — follow-on, stubbed.
- **Orchestrator topic judge** — already shelved per the approved messaging
  design; unchanged.

### 2d · Thread model

Per the approved messaging design (amendment 4), now resolved to messenger
ownership: **threads are plain sender-chosen names — no minting ceremony, no
topic-scoping.** A submission optionally names a thread; a reply names the
existing thread. The messenger persists the thread → messages association in its
`messenger.sema` thread index and can list a thread. Thread membership is
transport-level; the semantic payload (`signal-orchestrator-message`,
`Guidance|Interruption|Report`) still carries **no** thread field.

### 2e · Composition with the orchestrator (still tightly linked)

Plane split is unchanged in spirit, sharpened in fact: **orchestrator owns
who/where** (minted identity, agent registry, reachability discovery via
`SO_PEERCRED`+`/proc`+terminal-cell); **messenger owns carry/deliver/store**.
Because delivery now lives in messenger, the messenger needs the delivery target
per recipient. Per push-not-pull, **orchestrate is the producer and pushes**
agent registration + reachability (a local terminal-cell endpoint, or a
remote-host marker) into the messenger's local delivery registry via a
subscription; the messenger does not poll orchestrate. The minted identity
remains the join key (orchestrate registry = messenger recipient = router
`ActorIdentifier` on the deferred remote leg).

### 2f · Reconciliation with intent `alom` (existence vs delivery)

`alom` held message and router separate because the `SO_PEERCRED` trust boundary
cannot move into router. B1 does **not** violate this — it refines it. Local
delivery (same host, `SO_PEERCRED` valid) unifies with the existence fact inside
messenger; only **cross-host** delivery (where `SO_PEERCRED` cannot reach and
attestation is required) stays in router. The boundary `alom` protects is
exactly the local/remote line B1 draws. Flag for intent-maintenance: `alom`'s
manifestation text should be updated to say "cross-host delivery" where it says
"delivery." (I do not record intent; this is a pointer for the owner.)

### 2g · Cold-session delivery — respawn by resume identity (psyche-ruled 2026-07-17)

When a target session is not live, the messenger does not merely park the
message: it delivers by respawning the harness with its stored resume identity
and the message as the next turn. Psyche, verbatim: "yes, that is exactly what
should happen. unless the agent is marked as killed, in which case the message
can bounce back with a notice of dead agent, for now".

- **Live target** → ordinary delivery leg (§2b).
- **Not live, not marked killed** → record in the inbox/ledger as always, and
  respawn the harness by resume identity; the message arrives as the resumed
  session's next turn.
- **Marked killed** → no respawn; the message bounces back to the sender with
  a dead-agent notice. The "for now" is a psyche hedge preserved verbatim —
  bounce-with-notice is interim behavior, tracked as bead `primary-pm92`.

Consequences for §2a's storage: the local delivery registry carries the
harness **resume identity** alongside the live endpoint, and a killed/dead
mark fed by liveliness (§3). The killed mark is what distinguishes "cold,
respawnable" from "dead, bounce".

## 3 · Liveliness tests (B2 — psyche-ruled 2026-07-17)

Three-layer push model. Liveliness is a property of the agent owning a lane.
No clock-driven "are you alive?" loop exists at any layer. **Ruling status:**
the psyche replaced layer 3 (see below); layers 1–2 drew no objection and
stand.

1. **Hard liveness — kernel exit push (primary).** Orchestrate opens a `pidfd`
   on the reachability record's `harness_pid` (verified against
   `harness_start_time` to defeat pid reuse). A `HarnessLivenessWatch` IO actor
   epolls the pidfds; harness exit makes the pidfd readable → the watcher
   re-enters the daemon via the Signal socket (the `LaneReclaimer` pattern) →
   the owning lane's agent is marked dead. Kernel push, no agent cooperation, no
   poll.
2. **Soft liveness — activity refresh (existing push).** `touch_lane` on real
   orchestrator use keeps a working lane fresh; every mutation republishes the
   deadline.
3. **Activity read — inspect the agent's real latest activity (ambiguous
   cases). (Psyche-ruled 2026-07-17; replaces the messenger delivery probe.)**
   The psyche rejected the delivery-probe leg, verbatim: "better to actually
   read the agent's latest activity; a single command could take hours
   (rebuilding nixos from source)". When there is no pidfd (registration
   reachability was empty) or the case is ambiguous, the liveliness check
   READS the agent's genuine recent activity — harness transcript/output
   recency and the harness pid's live child-process tree — instead of probing
   deliverability. A live busy child process (e.g. a long build) is positive
   liveness: an agent inside one long-running command is NEVER judged Suspect
   or dead on output silence alone. This still fires on the `Active→Suspect`
   transition, not on a clock. Concrete activity sources (transcript paths,
   child-tree walk) are implementer matter for the owning lane.

Open push-not-pull escalation, unchanged: the ideal producer is the harness
pushing a lifecycle event stream (idle/stalled/resumed/exited) the orchestrator
subscribes to once. `pidfd` gives only the exit transition; "alive but stuck"
has no event without harness cooperation. Whether the harness daemon can expose
a push lifecycle subscription is the open producer-capability question. Until it
can, exit-push + on-transition activity read are the honest maximum and the
idle deadline is the backstop. **Sign-off status (2026-07-17): layer 3 ruled
as above; layers 1–2 drew no objection and stand. Later same day the psyche
accepted the program spine — verbatim "yes, messenger-first, liveness first"
(§0c) — so this design is signed off, with liveness ordered first.**

## 4 · Unified abandonment (B3 — landing via LaneAbandonmentMachinery)

The special case is dissolved: **the lane is the single abandonment subject;
worktree abandonment is lane abandonment.** The chain is
session → lane → {claims, worktree}; a worktree carries `owning_lane`. The
lifecycle bracket is now real on both ends: a worktree is born owned-by-a-lane
(`RequestWorktree`) and dies with its lane (`ConcludeWorktree`).

### 4a · Detection → grace → terminal

- **Detection.** Any liveliness signal failing (pidfd exit; an activity read
  (§3.3, psyche-ruled 2026-07-17) finding neither recent output nor a live
  child process; idle-deadline backstop) transitions `Active → Suspect`.
- **Grace.** A bounded window after `Suspect`, driven by the existing
  `LaneReclaimer` deadline worker (timerfd carve-out). Any real lane activity
  or a positive activity read returns the lane to `Active` and cancels
  reclamation — this is how a live-but-quiet agent proves itself; per §3.3 an
  agent inside one long-running command reads as alive via its child process.
- **Terminal (grace expires) — conclude the lane, reusing the landed op:**
  1. Release the lane's claims.
  2. Call `ConcludeWorktree` on the owning worktree. It branches on
     `PushedState`: ancestor-of-main → recycle (removed); pushed-not-in-main →
     `Archived` (kept for human merge/discard); unpushed → **`Abandoned`**
     (kept on disk, flagged; `Merged` teardown is gated-refused on unpushed
     work, so unpushed is never auto-removed).
  3. Retire the lane record.

### 4b · Durations (matter — set here, tunable constants)

- Idle-backstop window (Active→Suspect when no pidfd/probe fired): **6h**
  (demoted to backstop now that liveliness is primary; was a 24h primary).
- Grace window (Suspect→terminal): **15 min**.
- Terminal retention: **1h** (unchanged).

### 4c · Decision — agent-initiated `ConcludeWorktree(Merged|Rejected)` cascade

**No direct hard cascade to lane release.** Instead adopt the unifying rule:

> When a lane's **last owned resource is released or concluded** — its last
> claim released *or* its last worktree concluded — the lane enters `Suspect`
> immediately (accelerated grace entry), rather than waiting for the idle
> backstop.

Rationale (design-quality): a lane may own several worktrees/claims, so a
blanket "conclude → release lane" conflates one worktree's completion with lane
death. The agent is present and alive at a voluntary conclusion, so an immediate
hard release would reclaim under a live agent's feet. Routing voluntary
conclusion into the **same** `Suspect`+grace path gives the still-present agent
a window to start follow-on work (touch / `RequestWorktree` → back to `Active`)
or drift off (grace expires → normal conclusion). This subsumes the
`Merged|Rejected` case with **no new terminal path** — voluntary conclusion is
just an accelerated liveliness signal, and worktree-conclusion and
last-claim-release become the same event class. One policy, no special case.

## 5 · Sequencing (build-now vs stage), revised

- **Now, independent:** `HarnessLivenessWatch` (pidfd) and the `Suspect`+grace
  machinery — the latter is already in flight as `LaneAbandonmentMachinery`
  against landed `ConcludeWorktree`. §4c's last-resource-release rule folds into
  that lane.
- **Now, own lane — the big B1 build:** turn messenger stateful — add
  `messenger.sema` (ledger/inbox/thread index/local delivery registry), migrate
  the local-delivery reducer actors out of router, wire orchestrate→messenger
  reachability push, and prove the harness-delivery leg (`signal-harness` + a
  reachable harness daemon — still the least-proven part). Router keeps only the
  host-to-host actors; external-host escalation is a typed stub.
- **After messenger local delivery works:** wire the on-transition activity
  read (§3.3 as psyche-ruled 2026-07-17; the messenger delivery-probe variant
  is withdrawn) and the §2g cold-session respawn leg.
- **Last, staged, after all above merged + quiescent:** the rename sweep (§6).

## 6 · Rename sweep plan (B4)

Complete **both** renames as a single post-landing mechanical sweep; retire the
incremental "rename-on-touch" policy (it manufactures a persistent half-renamed
state — design-quality "replaceable over additive").

**Scope (per component family, done together because a socket/wire name is a
coordinated rename):**

- `orchestrate → orchestrator`: crate + `Orchestrate*` plumbing identifiers,
  binaries `orchestrate`/`meta_orchestrate` → `orchestrator`/`meta_orchestrator`,
  socket/env names, plus contracts `signal-orchestrate → signal-orchestrator`
  and `meta-signal-orchestrate → meta-signal-orchestrator`, repo directories,
  and remotes.
- `message → messenger`: crate + all `Message*` identifiers, binaries
  `message`/`meta-message`/`message-daemon` →
  `messenger`/`meta-messenger`/`messenger-daemon`, `message.sock`/`MESSAGE_*`
  env, plus contracts `signal-message → signal-messenger` and
  `meta-signal-message → meta-signal-messenger`, repo directories, and remotes.

**Remotes.** Rename the GitHub repos; GitHub auto-redirects the old repo URLs
(clone/fetch/push against the old name resolve to the new), so no dangling
references break. Update `ghq` local paths and workspace `repos/` links.

**Crate names — what "old name redirecting" means.** A GitHub repo redirect does
**not** redirect a Cargo crate name. Because every consumer of these crates is
in-workspace and git-dep'd (not an external crates.io dependant), the
**rename-propagator rewrites every `Cargo.toml` dependency entry and every `use`
path atomically in the same sweep** — no compatibility re-export shim. A shim
would manufacture legacy; it is warranted only if a consumer outside the
workspace cannot be updated atomically. **Check before the sweep:** confirm none
of these crates is published to crates.io with an external dependant; if one is,
that single crate gets a thin re-export shim under the old name and nothing else
does. Default expectation: no shim anywhere.

**Sequencing:** unchanged — only after the worktree protocol, liveliness, and
messenger work are merged and the tree is quiescent.

## 7 · Lane addressing — RESOLVED (psyche-ruled 2026-07-17)

**Ruling, verbatim:** "a lane should have a agent ID, which becomes our
endpoint. Same short hashes we've been using for IDs in spirit, mind, wherever
(4 chars + (adjusted for conflicts)). so each time a harness is launched, it
gets an ID (or re-uses it if it's a resumed session) assigned, and knows it in
his initial prompt. and messenger knows which process is which ID"

Design consequences (agent reading of the ruling, marked as such):

- **The endpoint/address type is the agent ID**, not a lane-typed address in
  `signal-messenger`. A lane *carries* an agent ID; sending "to a lane"
  resolves through the lane's agent ID on the orchestrator side.
- **Mint discipline:** the same short-hash mint already used in spirit/mind —
  random, 4 chars to start, length adjusted on conflicts.
- **Mint moment moves to harness launch.** The ID is assigned when the harness
  is launched — or re-used when the session is a resumed one — and the agent
  **knows its own ID from its initial prompt**, ahead of any
  self-registration. Registration binds the already-minted ID; it no longer
  mints. (This supersedes the minted-at-registration language in the
  orchestrator-messaging design's Settled Decisions; a superseding pointer has
  been added there.) **Mint authority resolved by the §0d Q2 ruling: the
  ORCHESTRATOR is the mint** — "the mint is the orchestrator. he creates an
  agent id and will eventually launch it" — with launch delegated through the
  harness component (`meta-signal-harness` authority chain); §0d refines this
  further: the ID is "allocated to the process before it starts". The earlier
  terminal-cell-as-minter lean is superseded (see §0c marker, bead
  `primary-sdgy`).
- **The messenger owns the process↔ID mapping** ("messenger knows which
  process is which ID"). Orchestrate's reachability discovery remains a feed
  into that mapping per §2e; the authoritative map lives with the messenger.
  **Refined by §0d Q2:** the orchestrator mints and spawns and "can keep
  track"; the messenger "can get a list of existing agent IDs" and holds
  "only IDs and then threads" — i.e. the messenger's durable registry is the
  consumer view of identity, fed by the orchestrator, while remaining the
  delivery-side map for messaging.
- The ID is stable across resume, which is exactly what the §2g cold-session
  respawn leg needs as its join key.

Historical record — the ambiguity this resolves. The earlier psyche phrase
"it routes its own lane; messages" was ambiguous across readings, kept here
for the record:

1. **Routing-plane reading:** "routes its own [delivery plane]; [carries]
   messages" — the semicolon separates two capabilities; "lane" ≈ the
   messenger's own routing path. Consequence: messenger is a self-contained
   local router+store; **no** lane addressing. (This report's working
   assumption; nothing in §2 commits to lane-addressing.)
2. **Lane-addressed reading:** "routes its own-lane messages" — "lane" = the
   orchestrator work-lane; a message can be **addressed to a lane** and
   delivered to whichever agent currently holds it. Consequence: lane becomes a
   first-class messenger address type, tightly binding the messenger contract to
   the orchestrate lane registry, and directly connecting messaging to
   liveliness (message-a-lane).
3. **Per-lane routing reading:** each work-lane has its own message stream/routing
   context inside the messenger.

The router→messenger migration in §2b–2c was reading-independent and remains
unaffected. The formerly blocked piece — whether "lane" is an address/route
type in `signal-messenger` — is now unblocked: it is not; the agent ID is the
address (see the ruling above).

## 7b · Claude subagents — parent-only working model adopted (psyche review pending)

The psyche asked, verbatim: **"how do we deal with claude subagents?"** —
i.e. how subagents spawned inside a harness session fit the launch-minted
ID/endpoint model, given they have no separately launched harness process for
the messenger to map.

Manager proposal on file: subagents share the parent session's ID/endpoint
and the parent relays to them, since they have no separate OS process the
messenger can reach; optionally they could be named by a hierarchical suffix
under the parent ID.

**Working model (2026-07-17, accepted-via-general-blessing — "go with your
leans, good enough for me" — NOT a direct psyche ruling; flagged for psyche
review):** the parent-only shape is adopted. Subagents share the parent
session's ID and endpoint; the parent relays inward; **no suffix vocabulary
is minted now**.

Implementers may build the parent-only shape, but must not mint
subagent-suffix address vocabulary into contracts until the psyche reviews.

Cross-reference (§0d, third batch): the psyche's thread model gives the
parent-only shape its group-addressing surface without new address vocabulary —
a manager is auto-subscribed to a thread for its subagents "so that they can
talk to all their sub agents in one go, or so that anyone can talk to all
their sub agents", and incoming messages carry origin so subagents
consult/escalate rather than blindly obey. Threads group; the parent
ID/endpoint remains the only address type.
