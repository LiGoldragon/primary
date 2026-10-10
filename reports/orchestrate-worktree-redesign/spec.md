# Orchestrate Worktree Redesign — Typed Message Board

**Status:** design specification, ready to build from
**Ruling (psyche):** Orchestrate is a typed message board. Agents post typed messages; Orchestrate stores them and serves them back. It does not scan the filesystem and it does not run commands. It keeps the worktree registry, populated by agent messages. Agents create and tear down worktrees themselves with `jj`. A doing-component, if ever built, is a separate component with its own contract.

## A · What Orchestrate is

Orchestrate stores speech acts and serves them back. Every row it holds is something an agent said. It performs no filesystem access of any kind — no directory walk, no `jj` invocation, no subprocess, no `stat`, not even read-only.

Ordinary contract verbs retained unchanged: `Claim`, `Release`, `Handoff`, `Observe`, `Submit`, `Query`, `Watch`, `Unwatch`, `RunWorkflow`, `RunResolvedWorkflow`, `ObserveWorkflowRun`, `WorkflowRunObservationRetraction`, `RegisterAgent`, `MintAgentIdentity`, `LaunchAgent`, `SendOrchestratorMessage`.

Meta contract verbs retained unchanged: `Create`, `Retire`, `Refresh`, `Register`, `Unregister`, `ClearSession`, `SetAuthority`.

Two new ordinary verbs replace the worktree surface: `DeclareWorktree`, `ReportWorktreeConclusion`.

Durable state: the claims table, lanes table, roles table, activity log, orchestrator agent/topic tables, repository index, and the **retained** `worktrees` table.

## B · What is removed

### B.1 Complete enumeration of daemon filesystem mutations

Every mutation in `repos/orchestrate/src/worktree.rs`. `S` = source checkout, `D` = worktree destination, `R` = remote. All move to the agent.

**Scaffolding**

| Line | Effect | Target | Fate |
|---|---|---|---|
| 116 | `create_dir_all(worktree_index_root)` | ~/wt/... | Delete. |
| 495 → 607-616 | `jj git init --colocate <checkout>` | S | Delete. |
| 498 | `create_dir_all(destination.parent())` | ~/wt/<repo>/ | Delete. |
| 505-517 | `jj workspace add --revision main --name <ws> <dest>` | S+D | Delete. |
| 518 | `jj bookmark create <branch> -r @` | D | Delete. |

**Teardown — conclude**

| Line | Effect | Target | Fate |
|---|---|---|---|
| 379-389 | `jj describe -r @ -m 'salvaged rejected working copy'` | D | Delete. |
| 393-404 | `jj bookmark set discard/<branch> -r <salvage> --allow-backwards` | D | Delete. |
| 406 | `jj git push --bookmark discard/<branch>` | R | Delete. |
| 410 | `jj bookmark delete discard/<branch>` (failed-push rollback) | D | Delete. |
| 414 | `jj workspace forget <workspace>` | S | Delete. The data-loss verb; see §G. |
| 416 | `remove_dir_all(destination)` | D | Delete. |
| 422 | `jj bookmark delete <branch>` | S | Delete. |
| 424-427 | `jj bookmark delete discard/<branch>` | S | Delete. |

**Teardown — AutoLand** (worktree.rs:902-1057, entered at :347)

| Line | Effect | Target | Fate |
|---|---|---|---|
| 920 | `jj describe -r @ -m 'auto-land working copy'` | D | Delete. |
| 925 | `jj git fetch` | R | Delete. |
| 929-935 | `jj rebase -b <salvage> -d main` | D | Delete. |
| 938, 959, 960 | `jj op restore <unwind>` | D | Delete. |
| 946-952 | `jj bookmark set main -r <salvage>` | D | Delete. |
| 956 | `jj git push --bookmark main` | R | Delete. |

**Lock / metadata handling**

| Line | Effect | Fate |
|---|---|---|
| 49-69 | `GitCheckoutLock` — opens `<S>/.git`, `flock(LockExclusive)` | Delete. Existed only to serialize the daemon's own scaffolding. §H.2 names the regression. |

**Read-only filesystem and subprocess access — also deleted.** Read-only is still access.

| Site | Effect | Fate |
|---|---|---|
| worktree.rs:739-881 | `WorktreePathProbe` — runs `jj` to derive `PushedState` and `last_activity` | Delete. |
| worktree.rs:1036 | `AutoLand::read` | Delete with AutoLand. |
| claim.rs:157 | `std::fs::canonicalize` on claim scope paths | Delete. Normalize scope paths lexically. |
| table_reclamation.rs:231 | `Path::exists()` in `reap_missing_worktrees` | Delete with the reaper (§B.2). |

**Registry bookkeeping (redb) — retained.** `insert_worktree` at worktree.rs:103, 289-290, 431 is kept, but its callers change: rows are written by `DeclareWorktree` and `ReportWorktreeConclusion` instead of by scaffold and teardown. `replace_worktrees` (worktree.rs:167) is deleted with `RefreshWorktreeIndex`.

**Projection** — `worktree_projection.rs:58-80` writes `orchestrate/worktrees.nota`. Retained as a dump of the registry, rewritten when the registry changes. `WorktreeProjection::gc_candidates` (worktree_projection.rs:32-56) is deleted; it read the projection back as if it were state.

### B.2 Verb-by-verb disposition

**`RequestWorktree` → `DeclareWorktree`.** No longer scaffolds. The agent creates the workspace itself and tells Orchestrate what it created; the reply reports any prior outstanding record at the same identity so the caller can detect a conflict. Orchestrate does not reject on "already registered" — it records the declaration and reports the collision.

**`ConcludeWorktree` → `ReportWorktreeConclusion`.** No longer tears down. The agent performs the teardown and then reports how it ended. **Keyed by exact `WorktreeIdentity` (repository + branch), never by lane.** This kills the unsafe lane selection at worktree.rs:310-340, where one lane owning several worktrees produced either a wrong-repository teardown or `Error::WorktreeLaneAmbiguous`.

**`RegisterWorktree` (meta) — DELETE.** `DeclareWorktree` on the ordinary surface is the same act, where it belongs.

**`RefreshWorktreeIndex` (meta) — DELETE.** It re-scanned the filesystem and replaced the table. Orchestrate does not scan.

**`ArchiveWorktree` (meta) — DELETE.** It set `WorktreeStatus::Archived`; that variant is deleted (§C.2).

**`ForceRemoveRegistryRow`, Worktree variant — RETAINED.** The registry can be wrong when an agent fails to report, and there is no mechanism inside Orchestrate to correct it. A manual override is therefore the only correction path and must stay.

**`flag_abandoned` (worktree.rs:627) — DELETE.** Already dead code; no caller outside its own test.

**Reapers `reap_missing_worktrees` and `reap_terminal_worktrees`** (table_reclamation.rs:230-257) — DELETE. The first probes the filesystem. The second is replaced by the retention rule in §F step 4.

### B.3 What the migration does to existing callers

- `execution.rs:526-537` (ordinary dispatch), `:590-607` (meta dispatch), `:3333-3340`, `:3396-3402`, `:4577-4660`, `:4799-4845`, `:5121-5160` — projection impls and dispatch arms for removed verbs are deleted.
- `claim.rs:499-527` `RepositoryContention::answer` calls `feature_worktree_for`, which scaffolds. It becomes a pure string computation over the repository index: name the path the claimant should create, or report the outstanding record already at that identity. `FeatureWorktree [(Scaffolded Worktree) (Existing Worktree)]` becomes `FeatureWorktree [(Available WorktreePlacement) (Occupied WorktreeRecord)]`.
- `orchestrate/AGENTS.md:96-103`, `:230-240`, `:402-414` document the removed verbs. Rewritten in migration step 2.
- Skill sources in `LiGoldragon/skills` that teach RequestWorktree/ConcludeWorktree must be edited in that repository. The generated copies under `.claude/`, `.agents/`, `.codex/`, `.pi/` are outputs.

## C · The worktree registry

### C.1 What it is

A table of messages agents posted about worktrees. Two message types:

- **Declaration** — a lane created a worktree at an identity and path, for a stated purpose.
- **Conclusion** — the lane that declared it finished with it, Merged or Rejected, and has already torn it down.

The registry holds those messages and serves them back: by identity, by lane, by repository, and as the outstanding set for a repository (declared, not concluded). That is the whole component.

### C.2 Contract types

`WorktreeStatus [Active Merged Archived Recycled Abandoned]` is deleted; `Archived`, `Recycled`, and `Abandoned` were daemon-computed. `PushedState` is deleted — Orchestrate cannot derive it without running `jj`.

```
WorktreeIdentity     { RepositoryName BranchName }
WorktreeDeclaration  { WorktreeIdentity LaneName WirePath PurposeText declared_at.TimestampNanos }
WorktreeConclusion   [Merged Rejected]
ConcludedReport      { WorktreeConclusion concluded_at.TimestampNanos }
WorktreeRecord       [ (Outstanding WorktreeDeclaration)
                       (Concluded WorktreeDeclaration ConcludedReport) ]
WorktreeRecords      (Vector WorktreeRecord)
WorktreePlacement    { source.WirePath destination.WirePath }
```

### C.3 Verbs

```
DeclareWorktree { WorktreeIdentity LaneName WirePath PurposeText }
  -> WorktreeDeclared { WorktreeRecord prior.WorktreeRecords }

ReportWorktreeConclusion { WorktreeIdentity WorktreeConclusion }
  -> WorktreeConclusionRecorded { WorktreeRecord }
```

`prior` carries any records already at that identity, empty in the normal case. `ReportWorktreeConclusion` on an identity with no outstanding declaration returns `Error::WorktreeNotFound`; it does not invent a record.

### C.4 What is given up

The registry is accurate only insofar as agents report. Specifically:

- An agent that creates a worktree without declaring it leaves it invisible to Orchestrate. Orchestrate will not find it.
- An agent that tears a worktree down without reporting leaves an Outstanding record forever. Orchestrate will not notice the directory is gone.
- Orchestrate reports no merge state, no push state, no commit counts, and no last-activity time. Nothing in the registry describes the current contents of a worktree. An agent that needs those facts runs `jj` itself.

There is no reconciler, no scanner, no self-healing, and none is to be specified. A wrong record is an agent-doctrine failure, corrected by fixing doctrine or by `ForceRemoveRegistryRow`.

## D · Agent-side protocol

### Obtaining an isolated workspace

```sh
orchestrate "(Claim (<lane> [(Path /git/github.com/LiGoldragon/<repo>)] [scaffold worktree <branch>]))"

# If the source has no colocated jj metadata yet:
jj git init --colocate /git/github.com/LiGoldragon/<repo>

jj --no-pager -R /git/github.com/LiGoldragon/<repo> \
   workspace add --revision main --name <branch> \
   /home/li/wt/github.com/LiGoldragon/<repo>/<branch>

jj --no-pager -R /home/li/wt/github.com/LiGoldragon/<repo>/<branch> \
   bookmark create <branch> -r @

orchestrate "(DeclareWorktree ((<repo> <branch>) <lane> \
  /home/li/wt/github.com/LiGoldragon/<repo>/<branch> [<why this worktree exists>]))"
# The reply's second field lists prior records at this identity. Non-empty means
# another lane already declared it; read it before proceeding.

orchestrate "(Release <lane>)"
```

The workspace name must equal the final path component, so a later teardown can name the workspace deterministically.

The claim on the source checkout is advisory only — see §H.2.

### Concluding, Merged

Order is not optional. Push before forget.

```sh
cd /home/li/wt/github.com/LiGoldragon/<repo>/<branch>

UNWIND=$(jj --no-pager op log --no-graph -n 1 -T 'id.short()')   # capture the unwind point first

jj --no-pager describe -r @ -m '<what this change does>'   # only if @ holds real undescribed changes
jj --no-pager git fetch
jj --no-pager rebase -b 'latest(heads(::@ & ~(empty() & description(exact:""))))' -d main

# If the rebase conflicted:  jj op restore "$UNWIND"  — then resolve by hand and retry.
jj --no-pager log -r '::@ & conflicts()' --no-graph -T 'commit_id.short()'   # must be empty

jj --no-pager bookmark set main -r 'latest(heads(::@ & ~(empty() & description(exact:""))))'
jj --no-pager git push --bookmark main

# VERIFY before destroying anything:
jj --no-pager bookmark list -r main --all-remotes -T 'remote ++ "\n"'   # must show a non-`git` remote

cd /git/github.com/LiGoldragon/<repo>
jj --no-pager workspace forget <branch>
rm -rf /home/li/wt/github.com/LiGoldragon/<repo>/<branch>
jj --no-pager bookmark delete <branch>

orchestrate "(ReportWorktreeConclusion ((<repo> <branch>) Merged))"
```

### Concluding, Rejected

```sh
cd /home/li/wt/github.com/LiGoldragon/<repo>/<branch>

jj --no-pager describe -r @ -m 'salvaged rejected working copy'   # only if @ holds real undescribed changes
jj --no-pager bookmark set discard/<branch> \
   -r 'latest(heads(::@ & ~(empty() & description(exact:""))))' --allow-backwards
jj --no-pager git push --bookmark discard/<branch>

# VERIFY:
jj --no-pager bookmark list -r 'discard/<branch>' --all-remotes -T 'remote ++ "\n"'   # non-`git` remote

cd /git/github.com/LiGoldragon/<repo>
jj --no-pager workspace forget <branch>
rm -rf /home/li/wt/github.com/LiGoldragon/<repo>/<branch>
jj --no-pager bookmark delete <branch>
jj --no-pager bookmark delete discard/<branch>

orchestrate "(ReportWorktreeConclusion ((<repo> <branch>) Rejected))"
```

The salvage revset `latest(heads(::@ & ~(empty() & description(exact:""))))` is preserved verbatim from worktree.rs:77-78. It skips the empty description-less placeholder jj parks the working copy on, which `jj git push` refuses. `--allow-backwards` handles a retried teardown finding the previous attempt's bookmark.

### Reporting is mandatory

Both messages are required, every time. Orchestrate has no way to detect a missed one. Declare immediately after creating; report immediately after teardown.

## E · The notification gap

`ClaimAcceptance { RoleName ScopeReferences }` gives an agent claiming a repository a bare acceptance, even when that repository has outstanding worktrees. `ReleaseAcknowledgment { RoleName ScopeReferences Worktrees }` already carries that information at the wrong end of the session.

Contract change — in `signal-orchestrate` schema/lib.schema:

```
ClaimAcceptance       { RoleName ScopeReferences WorktreeRecords }
ReleaseAcknowledgment { RoleName ScopeReferences WorktreeRecords }
```

Field name `outstanding_worktrees` on both, same shape at both ends of the session. Served from the registry.

Implementation — `claim.rs:173-205` `started_branches` is the reusable core. Three changes:

1. Rename `started_branches` → `outstanding_worktrees`.
2. Parameterize the lane filter. Today it hardcodes `record.owning_lane.as_str() != releasing_lane.as_wire_token()` (claim.rs:201), which is right for release — other lanes' branches started while you held main. It is wrong for claim: a lane starting work wants to see its own leftovers from a previous session too. Add `LaneFilter [All (Excluding LaneIdentifier)]`; release passes `Excluding(lane)`, claim passes `All`.
3. Filter the `worktree_records()` read (claim.rs:193) to Outstanding records. The repository-selection half (`held_repositories`, claim.rs:180-191, via `RepositoryDirectory::scope_covers_repository`) is unchanged and correct.

Call site: `apply_claim` at claim.rs:105-108 constructs the acceptance; it gains the third field computed from `claim.scopes`.

The notice carries identity, path, owning lane, purpose, and declaration time. It does not carry merge or push state; the claiming agent runs `jj` if it needs those.

## F · Migration order

Each step independently landable and reversible. Release-train coupling: `repos/orchestrate/Cargo.toml:54,57` pins the contracts by `branch = "main"`, so a contract change and its daemon consumption land as a pair within one step.

**Step 1 — contract pair, additive.** signal-orchestrate minor bump: add `WorktreeIdentity`, `WorktreeDeclaration`, `WorktreeConclusion`, `ConcludedReport`, `WorktreeRecord`, `WorktreePlacement`; add `DeclareWorktree` and `ReportWorktreeConclusion`; add `outstanding_worktrees` to `ClaimAcceptance` and change `ReleaseAcknowledgment`'s third field type. Daemon: both new verbs writing the existing `worktrees` table, plus §E. Old verbs still present and working. §E lands here — it is small and independently valuable.

**Step 2 — protocol and skills.** Rewrite `orchestrate/AGENTS.md` §"Verbs an ordinary agent needs", §Status, and the worktree lines at :96-103, carrying §D verbatim. Edit the corresponding skill sources in `LiGoldragon/skills`, not the generated copies. No code. Must precede step 3 or agents lose worktree capability.

**Step 3 — remove the doing.** Delete every entry in §B.1: `scaffold_workspace`, `bootstrap_colocated_jj_metadata`, `GitCheckoutLock`, `AutoLand` in full, conclude's teardown legs, request's scaffold branch, `WorktreePathProbe`, the `canonicalize` in claim.rs. Reshape `feature_worktree_for` to a pure computation and `FeatureWorktree` to `[(Available WorktreePlacement) (Occupied WorktreeRecord)]`. Remove `RequestWorktree` and `ConcludeWorktree` from the contract — a breaking change, permitted (ARCHITECTURE.md: "Backward compatibility is not a constraint for systems being born"). Roughly 400 lines of worktree.rs deleted.

**Step 4 — remove the dead ledger machinery.** Delete `WorktreeStatus` and `PushedState` from the contract. From meta-signal-orchestrate: delete `RegisterWorktree`, `RefreshWorktreeIndex`, `ArchiveWorktree`. From the daemon: delete `replace_worktrees`, `flag_abandoned`, `reap_missing_worktrees`, `reap_terminal_worktrees`, `WorktreeProjection::gc_candidates`, and `derive_owning_lane`. Add retention: Concluded records drop 30 days after `concluded_at`; Outstanding records are never dropped, since they are the evidence of an unreported teardown.

## G · Draining the existing backlog

Agent work, not Orchestrate work. A separate work item, filed and scheduled on its own. Orchestrate is not involved except to receive `ReportWorktreeConclusion` for identities it has records for.

| Category | Count |
|---|---|
| Stale workspace entries (root unresolvable) | 186 |
| Workspaces with no recorded path | 3 |
| /tmp-rooted workspaces | 21 |
| ~/agent-worktrees workspaces (267M) | 40 |
| ~/wt depth-2 dirs in no store — true corpses | ~17 |
| Flat independent clones at ~/wt depth 1 | 9 |
| ~/wt live workspaces (13G) | 242 distinct |
| jj-unreadable / corrupt | 4 |

An agent enumerates these itself with `jj --ignore-working-copy -R <source> workspace list -T 'self.name() ++ "\t" ++ self.root() ++ "\n"'` across the source checkouts, plus a directory walk of `~/wt` at depth 1 and 2 and `~/agent-worktrees` at depth 2. Deduplicate by store identity, not by checkout path: linked Git worktrees share one common `.git`, so many checkout paths reach one colocated store.

### The data-loss rule

Read this before running anything.

`rm -rf <worktree>` alone does not lose commits. These are shared-store jj workspaces: the operand store lives in `<source>/.jj` and the commits remain reachable through the source's operation log.

`jj workspace forget <name>` drops the working-copy commit's reference. The commits are still reachable via the source's op log.

The point of no return is `jj util gc` on a source checkout after a forget.

Two hard rules:

1. Never run `jj util gc` on any source checkout for the duration of the drain.
2. `jj workspace forget` + `rm -rf` is forbidden until a push has been verified, for any worktree carrying unmerged unpushed work. Verification means `jj bookmark list -r <bookmark> --all-remotes` shows a non-`git` remote. A zero exit status from `jj git push` is not sufficient evidence.

### Procedure

Record `du -sh ~/wt ~/agent-worktrees` and the full enumeration before touching anything. Work one repository at a time: claim the source checkout, drain its worktrees, release. Expect several sessions.

**G.1 — Stale workspace entries (186, zero risk).** Root already gone; only bookkeeping remains. `jj --no-pager -R <source> workspace forget <name>`. Reclaims no disk but makes everything after it legible.

**G.2 — /tmp-rooted workspaces (21, zero risk).** Same treatment. Then fix the generator: whatever creates jj workspaces in scratchpad directories must stop or must forget them on exit. File as its own bug.

**G.3 — Fully merged (zero risk).** `jj log -r '@-::main'` non-empty ⇒ the work is on main. `workspace forget` then `rm -rf`. Largest disk reclaim.

**G.4 — Pushed but unmerged (zero risk to the work).** The branch survives on the remote. Record the bookmark name in the drain report, then `workspace forget` + `rm -rf`.

**G.5 — Unmerged AND unpushed (the only real loss risk).** Largest: lojix/home-attribution-integration 59 commits, CriomOS/prometheus-vm-host 55, CriomOS-home/pi-subagent-home-activation 49. One at a time, human-visible, in this exact order:

```sh
cd <worktree>
jj --no-pager log -r 'main..@' --no-graph -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\n"'
jj --no-pager describe -r @ -m 'salvaged <branch>'                    # only if @ holds real undescribed changes
jj --no-pager bookmark set salvage/<branch> \
   -r 'latest(heads(::@ & ~(empty() & description(exact:""))))' --allow-backwards
jj --no-pager git push --bookmark 'salvage/<branch>'
jj --no-pager bookmark list -r 'salvage/<branch>' --all-remotes -T 'remote ++ "\n"'   # GATE
# Only if the line above shows a non-`git` remote:
jj --no-pager -R <source> workspace forget <branch>
rm -rf <worktree>
```

If the push fails or the gate does not pass, stop, leave the worktree alone, record it, move on.

**G.6 — ~/agent-worktrees (40) and the ~17 ~/wt corpses.** Classify each into G.3/G.4/G.5. The corpses are in no workspace list, so `workspace forget` does not apply — assess for unpushed work, then `rm -rf`.

**G.7 — Flat independent clones (9).** Not workspaces; each has its own store. `jj workspace forget` is wrong here. Handle individually: check for unpushed commits, push what matters, then remove.

**G.8 — jj-unreadable / corrupt (4). Do not delete. Do not forget.** Move to `~/wt-quarantine/<repo>/<branch>` and record. Attempt recovery from the source store's op log (`jj -R <source> op log`) only under human supervision.

Measure after and report the delta.

## H · Risks and what this gives up

**H.1 — The registry is only as good as agent reporting. Highest risk.** Orchestrate cannot detect a missing declaration or a missing conclusion, and by ruling it will not try. The registry can be incomplete and can be stale, silently and indefinitely. Mitigation is doctrine (§D) and `ForceRemoveRegistryRow`, both unenforced. Accepted deliberately.

**H.2 — Cross-process serialization is lost. A genuine regression.** `GitCheckoutLock` (worktree.rs:44-70) held an exclusive flock on `<source>/.git` across the read-check-create sequence, so two daemon processes could not race `jj git init --colocate` or `jj workspace add` on the same source. Agents doing this themselves have no such interlock. jj's own store locking covers most of it; concurrent `jj git init --colocate` on the same source is a real race. The mitigation is the documented Claim on the source checkout path, and a claim enforces nothing mechanically: `apply_claim` (claim.rs:55-109) checks lane registration, compares path prefixes, and writes redb rows. No flock, no permission interlock. A real lock is traded for an advisory convention.

**H.3 — Atomicity is lost.** Creation and declaration are now two steps by two actors. A crash between them leaves either a worktree with no record or a record with no worktree, and Orchestrate distinguishes neither.

**H.4 — Auto-land is gone.** AutoLand (worktree.rs:902-1057) did fetch / rebase / bookmark-set / push with a captured operation head and a full `jj op restore` unwind, tested against jj 0.40 semantics. Agents now do it by hand. Upside: a rebase conflict gets agent judgment instead of a typed `AutoRebaseConflicted` refusal that parked the worktree — 143 parked worktrees is the evidence that parking was not working. Downside: tested unwind code is replaced by a documented convention. §D carries the unwind capture so the convention preserves the safety property, but a convention is not a test.

**H.5 — No mechanical prevention of double-occupancy.** Two lanes can declare the same `WorktreeIdentity`. Orchestrate reports the prior record but cannot prevent it. Consistent with how claims already work.

**H.6 — Breaking wire change with coordinated callers.** Removing `RequestWorktree`, `ConcludeWorktree`, `WorktreeStatus`, `PushedState`, and three meta verbs breaks both CLIs, `orchestrate/AGENTS.md`, and the skill sources in `LiGoldragon/skills` at once. Step 2 exists to front-load it.

**H.7 — Doing has no home.** Until a doing-component exists, worktree creation and teardown quality rests on agents following §D, with no enforcement and no tests. Expect drift. The natural seam, out of scope: a `worktree` component with `worktree` / `worktree-daemon` binaries and `signal-worktree` / `meta-signal-worktree` contracts, which agents call and Orchestrate never calls.

**H.8 — Orchestrate no longer answers "is this worktree merged or pushed."** The old `PushedState` field, however unreliable, gave a caller a first-order answer without shelling out. Callers that need it now run `jj` themselves. This is the direct cost of the ruling.

**H.9 — Outstanding records grow without bound.** They are never dropped by design, being the evidence of an unreported teardown. At 143 rows over the system's life this is not a live concern, but it is worth watching.

## Flagged — not verified

- The backlog counts in §G were gathered by jj store enumeration; a prior audit reporting 143 rows, 147 registry rows, 112 orphans, 33 unmerged, and 4 corrupt used registry comparison. The two may be counting different things.
- Whether the deployed daemon binary matches repos/orchestrate HEAD. The Cargo.lock pins were confirmed (signal-orchestrate 0.10.1 / d5ecda9, meta-signal-orchestrate 0.5.0 / c3ba5567) and the local contract checkouts are on different lines (repos/signal-orchestrate at 0.5.0, repos/meta-signal-orchestrate at 0.5.3) — contract edits must go to /git/github.com/LiGoldragon/{signal,meta-signal}-orchestrate or a fresh worktree, not to the stale repos/ checkouts.
- `ClaimAcceptance`'s generated Rust field-for-field. The pinned schema/lib.schema was read (2 fields) but not the generated Rust in the pinned checkout.
