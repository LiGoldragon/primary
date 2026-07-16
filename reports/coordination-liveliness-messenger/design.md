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
- **B2.** Three-layer liveliness kept as designed but **awaiting sign-off**; the
  delivery-probe leg now goes through **messenger**, not router.
- **B3.** Lane `Suspect` + grace **accepted**; durations are matter, set in §4.
  `ConcludeWorktree`/`RequestWorktree`/`WorktreeStatus::Abandoned` have landed
  (orchestrate `37fac745`, signal-orchestrate `9d030d0f`). The one open call —
  whether agent-initiated `ConcludeWorktree(Merged|Rejected)` cascades to lane
  release — is decided in §4c.
- **B4.** Both renames completed as one post-landing sweep; remotes in scope; no
  compatibility shim. Plan in §6.

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

## 3 · Liveliness tests (B2 — awaiting sign-off)

Kept as the prior three-layer push model; the only change is the probe
transport. Liveliness is a property of the agent owning a lane. No clock-driven
"are you alive?" loop exists at any layer.

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
3. **Liveliness probe — messenger-backed reachability check (ambiguous cases).**
   When there is no pidfd (registration reachability was empty) or the case is
   ambiguous, orchestrate asks the **messenger** to attempt a delivery to the
   agent's registered target; the messenger's delivery leg reports
   success/failure, so an undeliverable target is a dead endpoint. This fires on
   the `Active→Suspect` transition, not on a clock — the reachability-probe
   carve-out. **(Changed from router to messenger per B2.)**

Open push-not-pull escalation, unchanged: the ideal producer is the harness
pushing a lifecycle event stream (idle/stalled/resumed/exited) the orchestrator
subscribes to once. `pidfd` gives only the exit transition; "alive but stuck"
has no event without harness cooperation. Whether the harness daemon can expose
a push lifecycle subscription is the open producer-capability question. Until it
can, exit-push + on-transition probe are the honest maximum and the idle
deadline is the backstop. **This whole section awaits psyche sign-off.**

## 4 · Unified abandonment (B3 — landing via LaneAbandonmentMachinery)

The special case is dissolved: **the lane is the single abandonment subject;
worktree abandonment is lane abandonment.** The chain is
session → lane → {claims, worktree}; a worktree carries `owning_lane`. The
lifecycle bracket is now real on both ends: a worktree is born owned-by-a-lane
(`RequestWorktree`) and dies with its lane (`ConcludeWorktree`).

### 4a · Detection → grace → terminal

- **Detection.** Any liveliness signal failing (pidfd exit; probe
  undeliverable/timeout; idle-deadline backstop) transitions `Active → Suspect`.
- **Grace.** A bounded window after `Suspect`, driven by the existing
  `LaneReclaimer` deadline worker (timerfd carve-out). Any real lane activity or
  a positive probe returns the lane to `Active` and cancels reclamation — this
  is how a live-but-quiet agent proves itself.
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
- **After messenger local delivery works:** wire the on-transition
  liveliness probe through messenger (needs §3 sign-off first).
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

## 7 · Returned to the coordinator — load-bearing ambiguity (do not guess)

The psyche phrase **"it routes its own lane; messages"** is materially ambiguous
on a point my whole liveliness/abandonment design leans on (the word "lane" is
overloaded in this workspace, where a *work-lane* is the abandonment subject).
Readings with divergent contracts:

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

The router→messenger migration in §2b–2c is reading-independent and can proceed.
The only piece blocked on this is **whether "lane" is an address/route type in
`signal-messenger`.** Please confirm the reading before Slice work touches the
messenger's addressing contract.

Also awaiting sign-off: §3 liveliness mechanism as a whole (B2).
