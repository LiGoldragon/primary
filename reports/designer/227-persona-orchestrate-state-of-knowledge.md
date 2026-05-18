# 227 — Persona-orchestrate: state of knowledge

*The component does not exist as a repo. Scaffold work landed in
wrong repos in May. Design work has landed in the right places.
Inventory below.*

---

## 0 · TL;DR

**No `persona-orchestrate` or `signal-persona-orchestrate` repo
exists on GitHub or locally.** `gh repo list LiGoldragon` confirms.
The `persona` repo's `ARCHITECTURE.md` §0.8 acknowledges the gap:
"Persona-orchestrate slot — `persona-orchestrate` is the *planned*
orchestration-machinery component… The default prototype topology
does not launch orchestrate until the `signal-persona-orchestrate`
contract and `persona-orchestrate` runtime repo land."

What *does* exist:

1. **Misplaced scaffold in `persona-mind`** (3 commits, May 7-9, on `main`)
   that look like persona-orchestrate's initial files but landed in
   the wrong repo.
2. **Misplaced contract in `signal-persona-mind`** (1 commit, May 9,
   on `main`) that started as "initial signal-persona-orchestrate
   contract" but ended up inside signal-persona-mind's tree.
3. **A real persona-mind daemon** that has *absorbed* much of what
   persona-orchestrate would do: `RoleClaim` / `RoleRelease` /
   `RoleHandoff` / `RoleObservation` / `ActivitySubmission` /
   `ActivityQuery` all flow through mind today.
4. **Design reports + bead `primary-699g`** treating
   persona-orchestrate as a future component, with intended scope
   (spawn, supervise, schedule, escalate, executor lifecycle).
5. **`/home/li/primary/orchestrate-cli`** — the workspace's Rust
   port of `tools/orchestrate`. Projects `MindRequest` but talks
   directly to lock files; sends nothing to any daemon today.

The user has been doing real design work; it's been landing in
**reports, ARCH slots, the persona-mind contract, and the
orchestrate-cli helper** — not in a dedicated `persona-orchestrate`
repo.

---

## 1 · Misplaced scaffold in `persona-mind`

Three commits on `persona-mind` `main` (visible at
`/git/github.com/LiGoldragon/persona-mind`):

| Commit | Date | What |
|---|---|---|
| `afe6786` | 2026-05-07 16:09 | "scaffold persona-orchestrate" — 16 files: `.gitignore`, `AGENTS.md`, `ARCHITECTURE.md` (15 lines), `CLAUDE.md`, `Cargo.toml`, `README.md`, `flake.nix`, `flake.lock`, `rust-toolchain.toml`, `skills.md`, `src/{lib.rs, main.rs, claim.rs, role.rs}`, `tests/smoke.rs`. 257 insertions. |
| `de9b258` | (between) | "docs(persona-orchestrate): align architecture with persona-sema" |
| `73d6c41` | (later) | "ARCH: describe runtime shape consuming signal-persona-orchestrate; lib + bin (orchestrate); CLAIMS/ACTIVITIES/META tables; Nota-on-argv CLI discipline; auto-Activity on claim/release/handoff; per `~/primary/reports/designer/93-persona-orchestrate-rust-rewrite-and-activity-log.md`" |

These commits' descriptions name **persona-orchestrate**, but they
live in **persona-mind**. The current `persona-mind` repo on disk has
moved on from this scaffold — its ARCH describes persona-mind (state
component + command-line mind), not orchestrate. The early-May
scaffold was either (a) the wrong commit message, (b) the orchestrate
work that later got absorbed into mind, or (c) abandoned. Git history
preserves it; the current files don't reflect it as a standalone
orchestrate repo.

Designer report `/93-persona-orchestrate-rust-rewrite-and-activity-log`
referenced in commit `73d6c41`'s message **no longer exists** — it
was retired in a context-maintenance sweep at some point.

---

## 2 · Misplaced contract in `signal-persona-mind`

One commit on `signal-persona-mind` `main`:

| Commit | Date | What |
|---|---|---|
| `121f8d9` | 2026-05-09 16:20 | "initial signal-persona-orchestrate contract — orchestrate CLI ↔ persona-orchestrate channel; six request kinds (RoleClaim/Release/Handoff/Observation + ActivitySubmission/Query) + eight reply kinds; 21 round-trip witness tests; per `reports/designer/93-...`". 11 files, 993 lines: `ARCHITECTURE.md` (156), `src/lib.rs` (335), `tests/round_trip.rs` (309), `Cargo.toml`, `README.md`, `skills.md`, `flake.nix`. |

This commit's title says **signal-persona-orchestrate** but the
files landed in **signal-persona-mind**. The current
`signal-persona-mind` ARCH describes it as "the public vocabulary
for Persona's central mind" — *not* orchestrate. The verbs that
shipped in this commit (`RoleClaim`, `RoleRelease`, `RoleHandoff`,
`RoleObservation`, `ActivitySubmission`, `ActivityQuery`) **are now
the canonical Mind contract**.

So `signal-persona-mind`'s current contract surface IS what
`signal-persona-orchestrate` was originally meant to carry. The
contract got renamed/repurposed; the implementation lives in
`persona-mind`.

---

## 3 · What `persona-mind` already does that maps to orchestrate's intent

From the persona-mind audit (per `/226` §1):

- `MindRoot` Kameo actor system supervises `IngressPhase`,
  `DispatchPhase`, `DomainPhase`, `ViewPhase`, `ReplyShaper`,
  `SubscriptionSupervisor`, `StoreSupervisor`.
- Real `MindClient` + `MindDaemon` + `MindFrameCodec` Unix-socket
  transport.
- Sema-engine durability with tables: `claims`, `activities`,
  `activity_next_slot`, `memory_graph`, `thoughts`, `relations`,
  `thought_subscriptions`, `relation_subscriptions`.
- Wired verbs (per `persona-mind/src/actors/dispatch.rs:55-119`):
  `SubmitThought`, `SubmitRelation`, `QueryThoughts`,
  `QueryRelations`, `SubscribeThoughts`, `SubscribeRelations`,
  `Opening`, `NoteSubmission`, `Link`, `StatusChange`,
  `AliasAssignment`, `Query`, `RoleClaim`, `RoleRelease`,
  `RoleObservation`, `RoleHandoff`, `ActivitySubmission`,
  `ActivityQuery`.
- Channel-adjudication verbs (`AdjudicationRequest`, `ChannelGrant`,
  `ChannelExtend`, `ChannelRetract`, `AdjudicationDeny`,
  `ChannelList`) are declared in the contract but return
  `MindRequestUnimplemented { NotInPrototypeScope }` at runtime —
  this is the **channel-grant authority** that would be
  orchestrate's bread and butter once orchestrate exists.
- Smoke scripts at `persona-mind/scripts/mind-*`:
  - `mind-cli-accepts-one-nota-record-and-prints-one-nota-reply` —
    end-to-end NOTA round-trip.
  - `mind-store-survives-process-restart` — sema-engine durability.
  - `mind-sends-signal-frames` — protocol-level witness.
  - `mind-opens-and-queries-work-item` — work-graph round-trip.

In short: **today's `persona-mind` IS the runtime for the role/
activity verbs that were originally drafted as
`signal-persona-orchestrate`**.

---

## 4 · Design landings — where the architecture work has actually gone

| Where | What |
|---|---|
| `persona/ARCHITECTURE.md` §0.8 | "Persona-orchestrate slot" — reserves the component principal, kind, socket names, state path, spawn-envelope mapping. Lists persona-orchestrate + signal-persona-orchestrate in §1 Component Map as **"Planned"**. |
| `persona-mind/ARCHITECTURE.md` §6.6 | Documents that mind's `Mutate` chain "extends downward through orchestrate" when it lands. Names `SpawnAgent` / `SuperviseAgent` / `EscalateBlockedWork` as the orders mind issues to orchestrate. Cites `reports/second-designer-assistant/4-persona-orchestrate-control-plane-2026-05-17.md` and bead `primary-699g`. |
| `reports/designer/219-persona-orchestrate-state-2026-05-18.md` | My own audit. Names the design state, the OwnerSignal chain, the LaneRegistry-as-config direction. Did not catch that the scaffold landed in wrong repos. |
| `reports/designer/224-workspace-redesign-first-concept-2026-05-18.md` | The redesign-first-concept treating persona-orchestrate as a future repo. |
| `reports/designer/226-persona-orchestrate-implementation-shape.md` | My recommendation that orchestrate-cli wire through persona-mind instead of standing up persona-orchestrate today. |
| `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md` | The four-layer integration design (helper / mind / orchestrate / persona-daemon). |
| `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md` | OwnerSignal discipline for `owner-signal-persona-orchestrate`. |
| `reports/second-designer-assistant/6-roles-as-config-owner-socket-mutable-2026-05-17.md` | Lane-registry-as-config direction; replaces RoleName closed enum with `LaneIdentifier` newtype owned by orchestrate's sema-engine state. |
| Bead `primary-699g` | The open designer pickup: "design persona-orchestrate component + signal-persona-orchestrate ordinary + OwnerSignal chain (orchestrate/router/harness)". |
| `/home/li/primary/orchestrate-cli/` | Rust port of `tools/orchestrate`. Projects `MindRequest` but writes lock files; doesn't send to any daemon. Closed bead `primary-68cb`. |

The design is **substantial**. The repo is **absent**.

---

## 5 · Why this happened (best reconstruction)

This is reconstruction, not a confession from the agents involved.
The pattern fits:

1. **May 7-9**: an agent (or sequence of agents) scaffolded
   persona-orchestrate. They put the scaffold code into
   `persona-mind`'s working copy by mistake — probably because the
   agent was already in `persona-mind`'s checkout and didn't `gh repo
   create persona-orchestrate` first.
2. **Same period**: the contract crate for orchestrate got
   scaffolded inside `signal-persona-mind`'s working copy with the
   same misdirection.
3. **Within a day or two**: the agents realized this and pivoted —
   the work that was tagged "persona-orchestrate" got refit into
   `persona-mind` and `signal-persona-mind`. The role-claim /
   activity verbs are real and shipping; they live in
   signal-persona-mind today.
4. **Subsequent design reports** kept treating persona-orchestrate
   as a *future component*, because: (a) the original commit messages
   in persona-mind and signal-persona-mind suggested it had its own
   home, (b) the persona ARCH §0.8 reserved a slot, and (c) no one
   verified the repo existed.
5. **Bead `primary-699g`** was filed to track the designer pickup,
   reinforcing the illusion that the repo just hadn't been created
   yet.

The user reasonably thought they were building this component "for
several days." The design *is* moving; the repo just was never made.

---

## 6 · Options going forward

### Option A — Create the repo properly now

1. `gh repo create LiGoldragon/persona-orchestrate --public` and
   `gh repo create LiGoldragon/signal-persona-orchestrate --public`.
2. **Either** extract the May 7-9 scaffold from `persona-mind`'s git
   history and replay it into the new repo (cleanest history),
   **or** start fresh from `skills/repository-creation.md` (cleaner
   today; lose the original lineage).
3. Decide what moves from `persona-mind` → `persona-orchestrate`:
   - `RoleClaim` / `RoleRelease` / `RoleHandoff` / `RoleObservation`
     / `ActivitySubmission` / `ActivityQuery` *currently* live in
     `signal-persona-mind`. If they belong in
     `signal-persona-orchestrate` per the original design, they
     migrate (cascade: every consumer's `git = ...` line updates).
   - `claims`, `activities`, `activity_next_slot` tables similarly
     might migrate from `persona-mind`'s sema schema to
     `persona-orchestrate`'s.
4. Update `persona`'s ARCH §0.8 to reflect the new state.
5. Re-scope bead `primary-699g` to track the implementation rather
   than the "design pickup."

### Option B — Confirm the consolidation (the path /226 leaned toward)

1. **Accept that `persona-mind` is the orchestrate runtime** for the
   role/activity verbs. The early-May commits were wishful-naming;
   the actual architecture is mind-as-orchestrator-of-state.
2. Rewrite `persona/ARCHITECTURE.md` §0.8: "Persona-orchestrate is
   absorbed into persona-mind for the prototype. A future split may
   carve out the machinery half when memory routing pressure
   justifies it."
3. Update the §1 Component Map to remove `persona-orchestrate` /
   `signal-persona-orchestrate` as planned components.
4. Close bead `primary-699g` with a note that the component was
   absorbed.
5. Update mind's ARCH §6.6 to remove "when orchestrate lands"
   forward-references; replace with "mind owns this."

### Option C — Hybrid: stand up `persona-orchestrate` as the *machinery* component only

1. Create the repo with a narrow scope: spawn / supervise / schedule
   / escalate. State stays in mind.
2. The contract carries `SpawnAgent`, `SuperviseAgent`, `RetireAgent`
   (the **`Mutate` chain extensions** named in mind's ARCH §6.6) —
   *not* the role-claim verbs that live in mind.
3. mind orders orchestrate; orchestrate orders harness/router.
4. The role-claim work stays in `signal-persona-mind` /
   `persona-mind`.

This is what `persona/ARCH §0.8` actually describes if you read it
carefully ("`persona-mind` remains the authority root and state owner
for role/work records; orchestrate is the machinery that carries out
mind's down-tree `Mutate` orders").

---

## 7 · Recommendation

**Option C with Stage 1 deferred.** Reasons:

1. The machinery — spawn / supervise — has nothing real to do today.
   `persona-harness` and `persona-router` are the existing
   targets-of-orders, but there's no live spawn pipeline yet (the
   sandbox tests use a manager, not orchestrate). Standing up
   persona-orchestrate before the spawn pipeline is real is
   premature.
2. The state — role claims, activities — IS real and IS in mind. Per
   `/226`, the immediate slice is wiring `orchestrate-cli` to send
   through mind. That doesn't need orchestrate to exist.
3. When the spawn pipeline becomes real (Persona daemon manages
   actual long-running agents via owner-socket spawn envelopes), the
   machinery half of orchestrate earns its repo.

**Concrete near-term action**:

- **Update `persona/ARCHITECTURE.md` §0.8** to reflect today's
  truth: role/activity state is in mind; the machinery component
  doesn't exist yet; when it does, its scope is narrow (spawn /
  supervise / schedule / escalate); the role-claim verbs stay in
  signal-persona-mind.
- **Update `persona-mind/ARCHITECTURE.md` §6.6** to match.
- **Reframe bead `primary-699g`** to track the *narrow-scope*
  `persona-orchestrate` as machinery component; mark blocked-on-real-
  spawn-pipeline.
- **Garbage-collect references** in design reports that imply
  persona-orchestrate is imminent (it isn't).
- **Do NOT extract the May 7-9 scaffold from persona-mind** — the
  scaffold's intent was the role-claim work which has already
  successfully landed in mind. Leave the historical commits in mind's
  history; they're context, not active code.

---

## 8 · What the user has actually been building

To answer "where has all this work been landing":

- **Design work**: in `~/primary/reports/designer/`,
  `reports/designer-assistant/`, `reports/second-designer-assistant/`.
- **Architecture slots**: in `persona/ARCHITECTURE.md` §0.8 +
  Component Map + Mermaid topology diagrams.
- **Bead trail**: `primary-699g` + the closed `primary-68cb`
  (orchestrate-cli Rust port).
- **Contract**: `signal-persona-mind` carries every verb the user
  thought was going into `signal-persona-orchestrate`. Real, shipped,
  tested.
- **Runtime**: `persona-mind` carries the actor topology and
  sema-engine state. Real, shipped, smoke-tested.
- **CLI**: `orchestrate-cli` is the workspace-side Rust port that
  projects to mind's request types.

The user **has been doing the work**. It just hasn't been
"persona-orchestrate the repo" — it's been "the orchestrate role
inside persona-mind."

---

## 9 · Open questions

- **Does the user want Option A, B, or C?** /226 leaned toward
  Option B (the de-facto state). The architecture reports lean
  toward Option A (the original plan). Option C is the principled
  middle.
- **If A or C: who carves out the persona-mind scaffold history?**
  An operator pickup — non-trivial git surgery if we preserve
  lineage.
- **If B: what does the user want to do with bead `primary-699g`?**
  Close as superseded? Re-scope?
- **Are there design reports that should retire** because they
  describe a persona-orchestrate that isn't going to be built?
  Candidates: `reports/designer-assistant/115`, `116`,
  `reports/second-designer-assistant/6`. Each carries some substance
  about OwnerSignal / registry-as-config that doesn't depend on
  orchestrate being a separate component — that substance should
  forward into mind's ARCH or skill files before retiring the
  reports.

---

## See also

- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` §0.8 "Persona-orchestrate slot" — the architecture's own status note.
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` §6.6 — mind's Mutate-chain description that references the future orchestrate.
- `/git/github.com/LiGoldragon/signal-persona-mind/ARCHITECTURE.md` — current contract, which is what was originally meant for signal-persona-orchestrate.
- `/git/github.com/LiGoldragon/persona-mind/` commits `afe6786`, `de9b258`, `73d6c41` — the misplaced scaffold.
- `/git/github.com/LiGoldragon/signal-persona-mind/` commit `121f8d9` — the misplaced contract.
- `reports/designer/226-persona-orchestrate-implementation-shape.md` — the implementation slice that doesn't need orchestrate to exist.
- Bead `primary-699g` — the open designer pickup.
