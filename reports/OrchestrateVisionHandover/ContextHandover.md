# Orchestrate, Messenger, Mint, and maintenance handover

## Load-bearing point

Orchestrate is becoming the mechanical coordination owner: it owns worktree lifecycle and the live registry; it protects primary `main` from forks by directing contention into feature worktrees; and it will join work around explicit subjects with Messenger and Mint. Do not turn those mechanisms into archives, manual database surgery, whole-repository locks, or names that merely happen to match.

This handover is a fresh-manager pickup point. It carries settled psyche direction and verified state, not a chronology of workers.

## Psyche rulings and invariants

- **Primary must never fork.** Work happens in orchestrator-created worktrees. `main` stays clean, is pushed immediately, and integration is by rebase. A whole-repository lock is rejected because it creates the pressure to fork.
- **Worktree lifecycle is mechanical Orchestrate work.** A request names a PascalCase feature intent and optional purpose; Orchestrate indexes the repository, creates the worktree from current `main`, records its purpose and owner, and tears it down through its lifecycle. If `main` is taken, contention automatically redirects to the named feature worktree. When the main-holder releases, it is told about branches started from that repository. The MVP auto-lands first completed work by rebase; no review gate yet.
- **Names correlate; they are not one identity.** A lane is an ephemeral session owner. A worktree is a repository plus branch. A topic is classification. A Messenger thread is a sender-chosen name. The future PascalCase `WorkSubjectKey` must explicitly relate these things; Mint consumes the relation. Never infer it by equal spelling.
- **Registries are live views, not archives.** Unbounded accumulation is a defect. Rows represent current reality; age must be visible; stale and terminal reality must be reaped. Age-based hard deletion is acceptable.
- **Liveness is positive evidence, never silence.** A long command can be live. Use actual activity, child/process state, or a real event; do not report an agent dead or stalled because it has not spoken.
- **Mint is the orchestrator.** It allocates the agent ID before harness launch, reuses it on resume, puts it in the initial prompt, and launches through the harness component. The ID is the messaging endpoint.
- **Messenger carries IDs and threads.** Threads are plain sender-chosen names and may carry an explicit relation to repository, feature branch, lane, or future work subject. Incoming messages retain origin so an agent can consult or escalate instead of blindly obeying. A manager is meant to be subscribed to the thread covering its subagents. The `message` to `messenger` rename is incremental.
- **Human elapsed time is typed NOTA, not prose.** `HumanReadableTime` is a closed unit variant with a numeric magnitude. The ordinary CLI defaults to Human presentation; Explicit Canonical presentation preserves exact nanosecond-bearing contract output. Do not change the canonical duration codec merely to format a CLI view.
- **Meta maintenance is exact and non-destructive.** Every application-maintainable registry row needs a typed administrative escape hatch. Exact row removal never means delete a checkout, Jujutsu workspace, bookmark, or other filesystem resource.

## System map

```text
agent / manager
    | ordinary coordination, observation, worktree request
    v
Orchestrate daemon --------------------> durable live registry
    |                                      lanes, claims, repositories,
    |                                      worktrees, bounded ledgers,
    |                                      agents, topics
    |                     |
    |                     +--> readable projections and age views
    |                     +--> Git/Jujutsu worktree mechanics
    |
    +-- main contention --> PascalCase feature worktree --> rebase to main
    |
    +-- pre-launch Mint --> agent ID --> harness launch --> Messenger
                                                    |
                                                    v
                                      named threads + origin + relations

meta authority
    |
    +--> exact registry-row maintenance only
          never filesystem or Jujutsu deletion
```

## Current public and deployed facts

- **Orchestrate 0.16 is deployed.** Its hermetic service PATH includes Git. At deployment, startup reconciliation removed 28 vanished-worktree rows, reducing the observed registry from 67 to 40 and verifying the then-remaining paths. The live index is not an archive: a later direct observation sees 137 current rows, reflecting subsequent real worktree activity.
- Current public Orchestrate main contains daemon-owned `RequestWorktree` and `ConcludeWorktree`, automatic main-contention redirection, rebase-based AutoLand, release-time started-branch notice, abandoned-worktree marking, metadata-preserving refresh, and reaping of vanished terminal rows.
- Public Orchestrate main also contains typed human elapsed presentation. A direct live lane observation currently renders typed unit values by default; Explicit Canonical observation remains available for programmatic consumers.
- `relative-age-display` public main provides the closed typed elapsed-time projection. Its ladder uses one most-significant unit and two decimals: seconds through years, with the established promotion thresholds.
- `meta-signal-orchestrate` public main is v0.5.3 and contains `ForceRemoveRegistryRow`, exact identities for twelve application-maintainable row families, and Removed/NotFound replies. Its documentation now states the no-filesystem/no-Jujutsu boundary.
- The meta contract is **producer-complete only**. Orchestrate has not yet implemented or deployed its handler, so do not issue that operation to production expecting deletion.
- Current Orchestrate public main fails closed if a lane owns more than one non-recycled worktree. The rejection occurs before filesystem or Jujutsu effects. Its generated boundary unfortunately presents this as empty-success `PartialApplied` with a generic failure, not a dedicated ambiguous-conclusion refusal.
- Current Criome main has a narrowly repaired set of three witness binaries. The repair updated stale generated-field names only; it changed no daemon, library, schema, storage, manifest, lock, or wire behavior.

## Implemented but compatibility-bookmark-only

The legacy contract train is deliberately producer-first and immutable. These are published compatibility bookmarks, not a declaration that their dependency pins are on every repository main or deployed:

- Legacy contract and generator family: `legacy-0v2`, `legacy-0v3`, `wire-safe-0v7`, `SignalMessageCompatibility`, `HarnessContractCompatibility`, and `SchemaLegacyCompatibility`.
- Criome-compatible family: `SignalCriomeCompatibleFamily`, `MetaSignalCriomeElevenFamily`, `CriomeElevenFamilyComplete`, `CriomeRuntimeCompatibility`, `SemaEngineFrameCompatibility`, and `TriadRuntimeFrameCompatibility`.
- Ordinary and maintenance contract family: `SignalOrchestrateReplyReliableFamily`, `VersionHandoverPins`, and `VersionProjectionLegacyPins`.
- Human presentation family: `RelativeAgeDisplayPins` is published and preserves typed time behavior. `VersionProjectionPins` is the remaining active Nota 0.9 producer at the time of this handover.

The release train has two intentional codec families:

```text
legacy coordination and wire contracts  -> Nota 0.5 family
human / projection presentation          -> Nota 0.9 family
```

They may coexist only behind a deliberate boundary. No runtime type or codec trait may cross that boundary. Moving branch selectors, local path patches, and lock-only repairs are not acceptable substitutes for immutable producer pins.

## Required next-action order

```text
finish VersionProjectionPins (Nota 0.9)
             |
             v
pin the complete immutable producer family into Orchestrate
             |
             +--> prove legacy and presentation families do not cross traits
             +--> full locked checks, freshness, round trips, and test graph
             |
             v
implement ForceRemoveRegistryRow runtime lowering
             |
             +--> exact table-key retraction only
             +--> Removed / NotFound idempotence
             +--> prove no filesystem or Jujutsu effect
             |
             v
deploy Orchestrate and live-test one harmless exact row plus repeat-not-found
             |
             v
continue the separate Protos-era exact WorktreeIdentity / WorkSubjectKey migration
```

The runtime handler should cover the closed contract identities: claim, role, lane, repository, worktree, activity, divergence, workflow resolution, agent, topic, topic membership, and triage audit. It must exclude counters and engine metadata.

## Open work and deferred decisions

- **Exact worktree conclusion identity is open.** `ConcludeWorktree` must evolve from lane selection to `WorktreeIdentity` of repository plus branch. This is blocked on a stable new Protos/schema generator and a consumer bridge. Do not solve it by choosing the first matching worktree.
- **WorkSubjectKey is open.** It must be PascalCase and explicitly relate lane, worktree, Messenger named thread, and topic where applicable. Mint aggregates those relations; it does not guess them from strings.
- **Messenger integration remains incomplete.** The working messenger, its agent-ID registry, thread relations, and delivery/liveness chain must be checked against live component state before new implementation. Cold delivery by resume and dead-agent bounce remain a later phase; the dead-agent bounce was explicitly hedged "for now." The subscription primitive was liked and deferred.
- **Review gate is deferred.** The worktree AutoLand MVP has no review gate; introducing one requires the later review-gate work, not an incidental change.
- **Privileged repository daemon and enforced file-granular claiming are deferred.** Without per-agent filesystem sandboxing, permission enforcement is not useful enough to justify the work. Narrow-path claims remain doctrine.
- **New Protos is not yet the consumer bridge.** Its structural decimal/float work is useful groundwork, but it has not published the stable generator, exact typed-duration conformance fixture, and legacy bridge needed to migrate these contracts. Current typed time uses the established legacy codec; do not author imagined new-syntax renderings.
- **Store open atomicity is an upstream sema-engine design question.** The existing repair loop handles recognized migrations, but the store-format stamp is still not atomic with family registration.

## Operational hazards a fresh manager must not repeat

- Treat `PartialApplied` with no successes from lane-selected conclusion as a refusal. Leave all worktrees intact. Several clean, ambiguous worktrees remain because deleting or concluding one by lane could hit the wrong repository.
- Do not hand-edit `orchestrate.sema`, delete worktree directories, or use lane-wide purge as cleanup. Use reconciliation for vanished terminal rows and the future exact meta operation for a confirmed row.
- `RequestWorktree` still assumes a colocated Jujutsu source checkout. A Git-only indexed checkout needs safe `jj git init --colocate` preparation or a future typed bootstrap/refusal; do not hide this as an arbitrary subprocess failure.
- Contract-family failure is usually a real trait-universe problem, not an invitation to patch one local checkout. Pin producers first, preserve generated artifacts, and run the entire consumer graph. The historical schema generator revision matters: using a different one can change a real reply surface, not merely formatting.
- Verify public remote state rather than trusting stale local tracking names. A prior obsolete `main@git` reference caused false conflict; GitHub `origin/main` was authoritative.
- The installed daemon/CLI can lag current source. Derive command shapes from the installed contract before invoking a destructive or coordination operation; legacy positional parsing is unforgiving.
- Do not infer liveness from silence or interrupt workers only because a command has been quiet for a minute.
- Keep reports in their own lane directory. Do not turn this handover into a growing archive; replace it with a fresh, verified handover when the next major state changes.

## Durable pointers

- `reports/coordination-liveliness-messenger/design.md` — psyche rulings on messenger-first/liveness-first, Mint, delivery, and liveness.
- `reports/orchestratorMessengerProgramPlan/release-train-plan.md` — phased Messenger/Mint/contention program; verify current code before treating its old status lines as live.
- `reports/orchestrator-messaging-design/orchestrator-messaging-design.md` — named-thread and topic decisions; later amendments supersede earlier prose.
- `orchestrate/ARCHITECTURE.md` and `orchestrate/NON_IDEAL_AGENTS.md` — current lifecycle, presentation, and known-debt mechanics.
- `meta-signal-orchestrate/ARCHITECTURE.md` — exact row-maintenance contract and its consumer boundary.
