# Intent handover: Orchestrate, Messenger, Mint, and the live coordination frontier

This is a fresh-context handover written for a manager. It supersedes no prior report by editing it; it is a new account grounded in the psyche's direction, the current workspace, and live daemon observations made on 2026-07-21.

## Psyche intent handover

The founding invariant is that **Primary must never fork**. The rejected answer is a whole-repository lock: it is the pressure that leads someone who cannot write Primary to create a fork. Agents normally work from a repository's `main`; when it is taken, Orchestrate must automatically say that main is taken, create an Orchestrate-owned worktree on a PascalCase feature name, and place the agent there. Worktrees are mechanical operations that the agent should not have to perform.

Main stays clean, is pushed immediately, and integrates by rebase. There is no pile of unpushed main work. The branch or bookmark where work was pushed matters; the psyche is not interested in commit hashes. Worktrees live in a known location, begin from the latest main, and use their feature/lane name plus an optional description to state what the work is for. When main's holder releases while a feature branch was started from that repository, the holder is informed. The first MVP auto-lands the first completed work by rebase; review is deliberately later, not an incidental gate.

The name carried through this system is a subject, not a claim that all objects have the same identity. The psyche wants these PascalCase lane/topic names reused throughout the engine so information aggregates around the subject. An agent with a question or statement about that subject should be able to use the thread of that name. But lane, worktree, topic, and thread have different lifecycles and must not be joined merely because their spelling happens to match. The future `WorkSubjectKey` must explicitly relate them.

Mine is where the psyche expects the system eventually to be tied together and organized. Mint is the orchestrator: it allocates an agent ID before the harness process starts, reuses that ID on resume, provides it in the initial prompt, and launches through the harness/launcher. That main session ID is the messaging endpoint. Messenger holds agent IDs and sender-chosen named threads. A thread may explicitly relate to a repository, feature branch, lane, or work subject. Incoming messages retain origin, so a receiving agent can consult or escalate instead of blindly obeying a message. A manager is meant to be subscribed to the thread covering its subagents so one send can address them together.

Registries are a live view of reality, not an archive. Unchecked data expansion is a defect class. A record must represent a present thing, and stale or terminal reality may be hard-deleted by age. Bounded current windows are appropriate for ledgers. Growing stores are acceptable only while their ages are documented. Liveness likewise comes from real positive activity, never silence: a single command may run for hours. Do not call an agent stalled or dead because it has not emitted a message.

Human elapsed time must be typed data, not prose glued onto a terminal. A closed human-readable time value carries a unit and magnitude; the ordinary interface uses it by default, while an explicit canonical mode preserves precise nanosecond contract output. The shorthand path should lower into the same explicit interpretation path rather than creating two independent implementations. Canonical duration encoding must not be changed solely to make a human display convenient.

Meta maintenance needs to exist for every application-maintainable registry, but its boundary is narrow: an exact typed row identity can be removed or reported absent. It is not a wildcard, a lane-wide purge, a database edit, or permission to delete a checkout, a Jujutsu workspace, or a bookmark. Filesystem and version-control destruction remain separate explicit lifecycle operations.

Several directions are intentionally deferred rather than silently accepted: the worktree auto-land review gate; a privileged-repository daemon and enforced file-granular ownership before there is a meaningful filesystem sandbox; cold delivery by resume and the dead-agent bounce; and the subscription primitive that sends when a condition ends. The psyche liked the subscription idea but deferred it. Narrow path claiming remains doctrine now.

## Delegated situation summary

### What is live now

The installed user service `orchestrate-daemon.service` was directly observed active and running Orchestrate 0.16. The CLI answered a live worktree observation. That snapshot contained 137 worktree records; it is a timestamped live view, not a durable count to repeat later. It includes many active entries, several abandoned entries, and an archived entry. The daemon is therefore functioning as a registry surface, while the population continues to change.

Current public Orchestrate main contains the worktree lifecycle direction already landed: daemon-owned worktree request/conclusion mechanics, contention redirection, rebase-based auto-landing, release-time notices, refresh that preserves stored owner/purpose/status, and startup reaping of vanished terminal worktree rows. A prior 0.16 deployment added Git to the daemon's hermetic PATH and reaped vanished rows through supported reconciliation rather than editing the database.

Typed human elapsed time is landed in the relative-age component and Orchestrate's CLI surface. The intended default Human presentation and explicit Canonical presentation exist in source; their typed value is not a reason to alter canonical nanosecond duration encoding.

The public meta-Orchestrate producer contains the exact-row maintenance vocabulary: exact identities across claims, roles, lanes, repositories, worktrees, bounded diagnostics, workflow resolutions, agents, topics, memberships, and triage rows; typed Removed and NotFound outcomes; and a documented no-filesystem/no-Jujutsu boundary. This producer is not evidence that production can already perform the removal: the Orchestrate runtime handler and deployment are unfinished.

Current coordination also shows an active `VersionProjectionPins` lane and a corresponding modified, uncommitted version-projection worktree. Its completion must be checked directly before anyone says the Nota 0.9 presentation-family release train is complete.

### Compatibility release train

The legacy coordination/wire family and the human/projection family are now deliberately separate:

```text
legacy coordination and wire contracts  -> established Nota 0.5 family
human and projection presentation        -> Nota 0.9 family
```

This is a boundary, not permission for arbitrary duplicate traits. No runtime type or codec trait may cross it. Moving branch selectors, local path patches, and lock-only repairs are not substitutes for a published immutable producer chain.

Published compatibility bookmarks exist for the legacy contracts, message and harness dependencies, the Criome-compatible family, the ordinary Orchestrate contract, exact-row meta producer, and the legacy version-handover chain. They are producer releases; they do not mean every dependent repository main or deployed service has adopted them. The recent relative-age-display presentation pin is published. The version-projection presentation pin is still verified only as an active worktree at this handover point.

A narrow Criome repair was landed on its main to update three stale witness binaries to generated field names. It changed neither daemon/library behavior nor schemas, storage, manifests, locks, or wire representation. It was necessary because no compatible dependency pin alone could make the existing witness binaries compile.

### Required next work

```text
verify and finish the Nota 0.9 version-projection producer
                         |
                         v
pin the full immutable producer closure in Orchestrate
                         |
                         +--> prove the Nota 0.5 / Nota 0.9 boundary
                         +--> run full locked checks, freshness, round trips,
                         |    and the complete consumer graph
                         v
implement ForceRemoveRegistryRow in the Orchestrate meta runtime
                         |
                         +--> exact table-key removal only
                         +--> Removed / NotFound idempotence
                         +--> tests proving no filesystem or Jujutsu effect
                         v
deploy Orchestrate and live-test one harmless exact row, then NotFound replay
                         v
continue separate contract evolution for exact worktree identity and subjects
```

The runtime handler must cover only the closed application-row identities in the meta contract. It must exclude engine metadata and sequence/counter rows. Do not send the meta operation to production until the consumer handler is compiled, deployed, and live-tested.

### Open design and correctness work

`ConcludeWorktree` still selects by lane. A lane can legitimately own several worktrees, so selecting the first is unsafe. Current source fails closed before filesystem or Jujutsu effects when that ambiguity occurs. The generated boundary incorrectly renders this refusal as an empty-success `PartialApplied` style result with generic failure, rather than a dedicated typed ambiguity refusal. Several clean worktrees remain because lane-wide conclusion could affect the wrong repository. Keep them intact.

The proper fix is an exact `WorktreeIdentity` keyed by repository plus branch. The `WorkSubjectKey` and explicit Messenger/Mint relations should evolve alongside it, but must not be fabricated with string equality. This exact-identity and subject-relation evolution still waits on a stable Protos/schema consumer generator and bridge; current Protos groundwork is not yet that bridge.

Messenger integration itself must be re-grounded against live component state before implementation: agent-ID registry, named threads, relation storage, message delivery, manager subscription, and liveness all need current source and deployed evidence. The older `message` to `messenger` transition is incremental, not a reason to duplicate delivery planes.

`RequestWorktree` still needs a safe answer for an indexed Git-only checkout that lacks a colocated Jujutsu workspace. It needs a typed bootstrap/refusal path, not an opaque subprocess failure.

### Fresh-manager cautions

- Never hand-edit `orchestrate.sema`, delete a worktree directory, or use a lane-wide purge to clean registry rows.
- Treat an ambiguous lane conclusion as a refusal even if its current outer rendering looks like a partial success. Do not retry it destructively.
- Derive coordination and destructive command shapes from the installed daemon contract, not current source alone; installed CLIs can lag and legacy positional parsing is strict.
- Public remote tracking must be verified against the authoritative GitHub `origin`, not stale local tracking labels.
- A contract-family build failure normally reflects real incompatible trait universes. Release/pin producers first; preserve generated artifacts; test the full consumer graph. A historically wrong generator revision can change a real wire reply surface, not just formatting.
- The daemon service name is `orchestrate-daemon.service`; querying an absent or differently named service can yield a false health conclusion.
- Do not infer worker failure from silence. A prior WebSocket failure was recovered successfully; later inactivity alerts were not by themselves evidence of a problem.

## Durable starting points

- `reports/coordination-liveliness-messenger/design.md` for Messenger, Mint, delivery, and liveness direction.
- `reports/orchestratorMessengerProgramPlan/release-train-plan.md` for phased program context; verify its status against current source.
- `reports/orchestrator-messaging-design/orchestrator-messaging-design.md` for named threads and topic decisions.
- `orchestrate/ARCHITECTURE.md` and `orchestrate/NON_IDEAL_AGENTS.md` for lifecycle and implementation debt.
- `meta-signal-orchestrate/ARCHITECTURE.md` for the maintenance contract boundary.
- This report is the new intent/situation handover for this lane. Replace it with another verified handover when the runtime implementation or the compatibility frontier changes; do not turn it into an accumulating archive.
