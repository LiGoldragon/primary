# Eight skill redesigns — replacement text

Draft only. Nothing in `LiGoldragon/skills` was edited. Source files are
`/git/github.com/LiGoldragon/skills/skills/<name>.md`; the `description` field
lives in `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota`.

Recovered lines come from `7f5753642f1d^` in the skills repo, the state before
"skills: reduce reusable guidance". Where one survives, the incident behind it
is named.

Two things moved under me while I worked, both in skills commit `6f23fd59a0eb`
at 13:36 today: `release-train-development` was **deleted**, and
`repository-management`/`publication`/`closeout` became `repository-lifecycle`.
The first changes the `main-feature-integration` answer.

## 1. version-control

### Current

```
# Skill — version control

- Use `jj` for ordinary history and pushes.
- Use an explicit message for every authored commit.
- Preserve peer work and verify the pushed bookmark.
```

### Proposed

```
Check that `@`'s parent is `main` before editing a repository. A clean working copy is not evidence of it.
Rebase with `jj rebase -s @ -d main` when `@` is a sibling of `main` rather than a descendant.
Outside primary, read `jj status` before committing. The working copy may hold another agent's uncommitted work.
Outside primary, commit one logical change at a time.
Push each completed commit. Do not accumulate a finished local stack.
Aim a mutating `jj` command with `-R <path>`, or with a `cd` that ends in `|| exit`. The shell resets to the workspace root between tool calls, and a bare `cd` that fails points the next command at primary.
`jj` commits and pushes a conflicted tree without failing. Read `jj status` for conflicts before setting a bookmark.
Read remote state with `git ls-remote`. Local bookmarks and `@origin` tracking refs go stale.
Capture a revision hash by pasting from `jj log`, `git ls-remote`, or an existing lock entry. Never type or complete one from memory.
Stop and ask before rewriting or force-moving a commit you did not author.
Recover a working copy you damaged with `jj op log` and `jj op restore`.
Initialize a repository with no `jj` metadata using `jj git init --colocate`, then `jj bookmark track main@origin`.
Raw `git` is allowed for three things: reading or changing remote configuration, `git ls-remote`, and `git worktree prune`.
```

### Description

`Use when committing, pushing, or repairing history in any repository.`

### Cut

- `Use jj for ordinary history and pushes.` — AGENTS.md line 67 binds it.
- `Use an explicit message for every authored commit.` — AGENTS.md lines 64-65 bind inline messages and the no-editor rule.
- `Preserve peer work and verify the pushed bookmark.` — two rules welded, and neither says what to do. Three replacement lines name the three ways peer work is actually lost here: a sibling commit that rolls `main` back, a `jj commit` that sweeps a peer's uncommitted files, and a stale local ref read as remote truth.
- The primary flow (`jj commit -m` / `jj bookmark set main -r @-` / `jj git push --bookmark main`, work on main, commit the whole working copy) — verbatim in AGENTS.md lines 62-66.
- `Do not use jj git push -c @.` (recovered) — no instance found. Cut for want of an incident.
- `jj restore discards working-copy content. Use it only when the exact path and loss are understood.` (recovered) — "do not destroy what you do not understand". The `jj op restore` line replaces a warning with a move.
- `--no-pager` on every read command (recovered) — `jj log` and `jj status` return without a pager in this harness. Tested, not assumed.
- `Identify pushed work by its bookmark in reports.` (recovered) — an agent already reports "pushed to main".
- The authorized-landing rebase paragraph (recovered) — "rebasing your own landing stack is in scope" follows from "ask before rewriting a commit you did not author". Stating both is the matched-pair shape.

### Added

- **`@`'s parent is `main`.** The line the current skill most conspicuously lacks. Three separate sessions hit it and wrote it up. `agent-outputs/IntentEliminationPhase1ProvingBatch/RepoScaffolder-FoldAndEliminateHandoff.md`: "Committing as-is would have created a SIBLING of main, not a child — a non-fast-forward push that drops the newer main work. Fix applied: `jj rebase -s @ -d main`… LESSON FOR FAN-OUT: 'clean working copy' is not sufficient." Same failure in `agent-outputs/IntentToArchitecturePhase1/RepoScaffolder-Handoff.md` ("would have rolled `main` back 3 commits") and `agent-outputs/PerRepoIntentFold/RepoScaffolder-Handoff.md`.
- **`jj status` before committing outside primary.** `agent-outputs/FieldReadiness/OperatingSystemImplementer-FieldHardeningEvidence.md`: "my first `jj commit` there accidentally swept their uncommitted changes into my commit and moved their bookmark. Caught before any push; recovered with `jj op restore` to their last op (`5644f88`)." This is also the incident behind the `jj op restore` line.
- **`git ls-remote` for remote truth.** `agent-outputs/RenamePropagator/Residue-Sweep-Evidence.md`: "Those local remote-tracking refs are STALE/DIVERGED for many repos. `git ls-remote` proved the true pushed state differs… A '0 residue' claim read from a local jj bookmark is worthless here." The same file records the false claim this produced, and its retraction.
- **`-R <path>` or a guarded `cd`.** Recovered. The mechanism is a property of this harness, not of `jj`: cwd resets between bash calls, so a `cd` that fails leaves a mutating command aimed at primary.
- **Conflicts commit and push without failing.** Witness: `d9b3382580cd` in primary, 2026-06-30, "skills: regenerate role destination doctrine", carries a conflict. Not in `main`'s ancestry, so it was caught — but `jj` did not stop it being made. Git-trained intuition says a conflict blocks the commit.
- **Never compose a revision hash.** This workspace pins deploys and flake inputs by 40-hex rev (`github:LiGoldragon/CriomOS?rev=<40-hex>`) and release-train members by bare commit. Completing a short prefix to full length produces a fabricated pin.

### Open for you

AGENTS.md line 67 says "No raw `git` except the documented escape hatches in the
`jj` skill." **There is no `jj` skill.** There was. It lived at
`modules/jj/full.md`; commit `c2306bd84ddf` ("skills: rename active
appellations") deleted it and introduced today's three-line `version-control`
stub in the same commit, carrying none of the escape-hatch content.
`agent-outputs/SkillDoctrineV2/SkillEditor-CorpusTriage.md` had said to
"preserve content" when merging `jj`, so the loss was not the ruled outcome.
Two reports — `reports/field-readiness/13-tooling-field.md` and
`reports/orchestrate-worktree-redesign/spec.md` — still cite "the
`version-control` escape hatch" as a live procedure. It does not exist.

Both fixes touch the boot contract, so both are yours: rename this skill to
`jj`, or amend AGENTS.md line 67 to say `version-control`. Rename is better —
the boot contract already calls it `jj`.

## 2. testing

### Current

```
# Skill — testing

- Test the changed contract with the smallest meaningful witness.
- Use the repository's durable test gate.
- Keep stateful test requirements explicit.
```

### Proposed

```
Build the one named check that covers the edit: `nix build .#checks.x86_64-linux.<check>`. Run `nix flake check` before commit, not during iteration.
Run a check that takes minutes in the background with output to a file, and read the exit status from that run.
Do not judge a run through `tail` or `head`. The pipe reports the pager's exit status and truncates a failure into a green.
Pass `--rebuild` when the run itself is the evidence. A realized store path makes `nix build` exit 0 having executed nothing.
Read a check's assertions before citing it as proof. An assertion that holds at evaluation time, or over inputs the test handed itself, proves nothing about the path it names.
Run VM checks only on the host the repository designates for them. Local KVM is not that designation.
Report a test that skips by default, and a component a sweep could not evaluate, as not run.
Do not offer a passing unrelated check in place of the one that covers the edit.
Put a test daemon's unix socket under `/tmp/<lane>/`. The scratchpad path is longer than the 108-byte socket path limit.
```

### Description

`Use when a change needs a check run, or when a check result is being reported as evidence.`

### Cut

- All three current lines. "Smallest meaningful witness", "durable test gate", "keep requirements explicit" name end states without a command, a test, or a case.
- Test naming, fixture minimalism, assertion-message craft, and where unit versus integration tests live (recovered) — that is how to write a test. Documentation. It belongs in `standards`, and relocation is out of scope this session.
- `Test architecture, not just regression` (recovered) — the `architectural-truth-tests` module carries it.
- `Do not weaken tests to pass. Do not delete coverage without replacing the proof.` (recovered) — I searched for an agent deleting or skipping a failing test to reach green and found none; every "removed test" hit was dead code after a migration. Cut for want of an incident. The three gaming shapes that *are* evidenced are covered by the `--rebuild`, assertions, and skip-reporting lines.

### Added

- **`--rebuild` when the run is the evidence.** `reports/capacityAdmissionSlice/4-Audit-adversarial-reaudit-deploy-smoke-green.md`: a `nix build` of a VM check hit an already-realized store path and "boots zero VMs and exits 0. 'Run the command and report GREEN' is satisfiable with no VM ever running." A prior agent had reported exactly that as green.
- **Read the assertions.** Same report: `assert not expected_closure.endswith(".drv")` holds whether or not the deploy ran; `assert 'Deployed' in deploy_reply` proves admission, not completion. And `reports/synchronizer/train-flow-audit-v1.md`: the live-run test "builds `members` from its own selectors so the check passes trivially… membership passes tautologically."
- **VM host designation.** `CriomOS-test-cluster/INTENT.md` requires VM checks on an authorized VM host and says an unknown host is "a documented blocker, not an attempted QEMU run". An agent ran QEMU on the laptop instead, "justified by KVM presence alone — exactly what INTENT.md rejects".
- **Skips and unevaluable components are not-run.** `harness/tests/message_router_harness_e2e.rs` skips silently when peers are absent and is not wired into `harness/flake.nix` at all. Separately, `forge` and `mentci` are invisible to the Nix sweep, which made "all repos build" vacuous.
- **Background and file for long runs.** `reports/field-readiness/11-build-readiness.md`: router ~44, mind ~60, persona ~120 checks; a worker session "died mid-sentence" because `nix flake check` on a cache-missing repo "silently becomes an hours-long build with logs flooding the worker's context".
- **`tail`/`head` and the socket path limit** are recovered. Both name a mechanism that silently inverts a result.

## 3. operating-system-operations

### Current

```
# Skill — operating system operations

- Change system behavior through pushed, reproducible source and supported deployment.
- Name the target, action, rollback owner, and activation evidence before a host change.
- Do not patch managed output.
- Require explicit psyche approval before a reboot or emergency runtime mutation.
```

### Proposed

```
State the node, the action, and the exact source revision before submitting a deploy.
Choose a non-activating or boot-once action first. A live switch can drop the connection that manages the host you are changing.
Reboot only with contemporaneous psyche approval for that reboot. An instruction to fix something does not authorize one.
A returning `meta-lojix` means the request was admitted. Poll `lojix "(Query (ByNode ...))"` until the expected generation is current.
Poll in the foreground. A background waiter dies with the turn, and the deploy parks unnoticed.
Do not kill a deploy during a build or an evaluation.
Check the live host after a rejected deploy. A rejection can arrive after the switch has already changed `/run/current-system` and the running units.
Read `journalctl` for the failing unit before treating a deploy failure as an authorization problem. Lojix reports any activation-stage failure as `BuilderUnreachable`.
Stop when the live daemon's interface does not match the documented one. Do not substitute the closest-looking request.
Rehearse a storage migration against a copy of the live data. Synthetic fixtures have passed a layout mismatch that the production copy caught.
A generation rollback does not reverse a migrated store. Restore the data separately.
Do not start a long-lived daemon by hand. Add its Home Manager service module and deploy it.
Report a daemon that is down. Do not restart it.
Repoint an input by writing the revision. `nix flake update` resolves the branch head instead.
Report the failing command and the shortest next step. Do not widen a routine deploy into an investigation.
```

This is the longest of the eight. Every irreversible action in the workspace is
here, and each line has a witness.

### Cut

- The entire `lojix`/`meta-lojix` interface reference (recovered, roughly 40 lines): field orders, `UserEnvironmentDeployment`'s nine positional fields, `HostDeployment`'s ten, the `RequireImmutable` query-string form, `<builder>` and `<substituters>` shapes, `runuser --login`, the Niri reload. This is documentation of another repository's interface, and by `documentation-placement` it belongs inside `lojix`. It also rots: `agent-outputs/NotaStrictPositional/OperatingSystemImplementer-V11DeployBlocked.md` records the skill claiming Lojix 0.4.0 while the daemon was 0.3.10 and rejecting `Host` as an unknown variant. That rot is the reason for the "stop when the interface does not match" line.
- `Do not patch managed output.` — no evidence of an agent doing it; every observed touch of `/etc/keyd/laptop.conf` and similar was read-only. And `nix-workflow` now carries "Treat managed output as evidence, not a patch target."
- `rollback owner` from the pre-change checklist — no report ever names one. Cut the field, keep the checklist.
- `Change system behavior through pushed, reproducible source and supported deployment.` — a goal welded to a mechanism, and `nix-workflow` has "Build and deploy reproducible source."
- `A unit built into the store is not active until it is linked into ~/.config/systemd/user/.` — considered and cut, not for want of evidence. `agent-outputs/Handover-OrchestrateDaemon-Fix-and-RootCause.md` records the orchestrate daemon's unit "built in the Nix store... but NOT symlinked into `~/.config/systemd/user/`", so nothing supervised it back up after a restart. Cut because the hand-started-daemon line gives the remedy and the journalctl line gives the diagnosis, and os-operations is already the longest of the eight. Call it back if you want the diagnostic stated directly.
- `Read the lojix repo's NON_IDEAL_AGENTS.md before deploying` (recovered) — the general rule ("a workaround recorded in the target repository's `NON_IDEAL_AGENTS.md` is sanctioned; follow it without asking") is worth having, but it is not an os-operations rule. Left out rather than misplaced. Flagged below.

### Added

- **A permission-shaped failure is usually a failing unit.** `agent-outputs/LojixDeployAuthMap/Scout-H945-NoPermissionDiagnosis.md` calls it a triple mislabel: `switch-to-configuration` exits 4 when a post-switch unit fails, systemd renders that as `status=4/NOPERMISSION`, and Lojix maps any activation-stage failure to `BuilderUnreachable`. "No privilege, credential, or store permission is denied anywhere." Actual cause: `mirror.service` crash-looping on a storage schema mismatch. The same misdiagnosis recurred in `SpiritGuardianSecretAccess/OperatingSystemImplementer-RedeployEvidence.md`, root-caused separately to a home-manager collision on a hand-edited `~/.ssh/config`.
- **A rejected deploy may already have applied.** `agent-outputs/EmergencyColemakRecovery/OperatingSystemImplementer-MergeSwitchEvidence.md`: deploy 38 was rejected `BuilderUnreachable`, but "`/run/current-system` matched the new build and keyd/Niri already showed the new layout… Lojix did not record deploy 38 as a current generation."
- **Boot-once before live switch.** `CriomOS/ARCHITECTURE.md` and `reports/field-readiness/13-tooling-field.md`: a live `Switch` on prometheus restarts `hostapd`/`dnsmasq` and drops the management connection, so `BootOnce` is mandated there. The line is written as the general behavior rather than the host fact, which stays in CriomOS.
- **Stop on an interface mismatch.** `agent-outputs/LaptopColemakKeyd/OSImplementer-Evidence.md`: doctrine named `Host`/`ScheduleBootOnce`, the live daemon exposed only `System`/`Switch`, and "deployment stopped rather than improvising a live `Switch` or a retired request shape." That was the right call and is now a rule.
- **Rehearse migrations on live data.** `agent-outputs/NotaStrictPositional/OperatingSystemImplementer-V11DeployBlocked.md`: the migrator failed against a copy of production with "engine storage layout 5 does not match this build's layout 3" — a failure the synthetic fixtures never caught.
- **Rollback does not reverse a migration.** `reports/logos/next-gen-spirit-foundation-audit-v1.md`: "a profile rollback does not reverse a migrated `.sema` database." Procedure in `agent-outputs/TrueSchema/V11ProductionRedeploy-Closeout.md`: stop the service, restore the migration backups over the live and archive paths, then start the old generation.
- **No hand-started daemons.** `agent-outputs/FieldReadiness/OperatingSystemImplementer-FieldHardeningEvidence.md`: `orchestrate-daemon` was installed imperatively and started with `setsid nohup … &`, and "its earlier crash silently took the whole claim fabric down until a manual restart."
- **Report a down daemon, do not restart it.** `spirit-daemon.service` is inactive and `spirit-judge.service` failed right now. The audit that found it wrote "No activation, recovery, store inspection, or mutation was attempted by this audit", and a separate agent's `systemctl restart lojix-daemon.service` was refused by policy and escalated instead.

### Open for you

- The name. Every line is about deploying, activating, or rolling back. `deployment` says that; `operating-system-operations` says "operations operations". Not changed here.
- Placement for one orphan rule: "a workaround recorded in the target repository's `NON_IDEAL_AGENTS.md` is sanctioned; follow it without asking." It prevents an agent stalling on the sanctioned SSH-and-root deploy fallback, but it is general, not os-operations. `documentation-placement` is the nearest home.

## 4. disk-hygiene

### Current

```
# Skill — disk hygiene

- Measure before and after cleanup.
- Delete only authorized, understood data.
- Preserve boot and rollback state when reclaiming generations.
```

### Proposed

```
Baseline with `df -h`. Store reclaim never shows in `du`, because the store is on its own filesystem; measure it by the `df` delta.
Delete stray `result` symlinks before collecting garbage. Each one is a GC root pinning a whole closure.
Delete old generations from the user profiles first, then collect once.

    nix-env --profile ~/.local/state/nix/profiles/home-manager --delete-generations old
    nix-env --profile ~/.local/state/nix/profiles/profile --delete-generations old
    nix-collect-garbage -d

A user-invoked `nix-collect-garbage -d` collects the whole store through the root daemon and needs no sudo.
Run `nix-collect-garbage` on the system profile without `-d`. Bare `-d` drops the booted generation's symlink.
Read `readlink /run/booted-system` and `readlink /run/current-system` and keep both generations. They differ.
Hand the system profile to whoever holds sudo. A non-interactive agent cannot authenticate for it.
`rm -rf` on a jj workspace directory loses no commits. The commits live in the source repository's store.
`jj workspace forget` drops the working copy's only reference, and a later `jj util gc` in the source checkout destroys it. Verify the push with `git ls-remote` first; a zero exit from `jj git push` is not evidence.
Confirm a `target/` directory by `CACHEDIR.TAG` or a `debug/` or `release/` subdirectory, then `rm -rf` it.
Report a worktree sitting in the ghq owner directory as litter. Do not delete it.
Self-authorize two categories: old nix generations, and rust `target/` directories. Ask before deleting media, Downloads, browser profile data, the `.cargo` registry cache, or anything else.
```

### Description

`Use when reclaiming disk space, or when deciding whether a deletion is reversible.`

### Cut

- All three current lines. "Delete only authorized, understood data" is the shape you reject; the two-category line says the same thing checkably.
- `Never du, find, or walk /nix/store` (recovered) — AGENTS.md line 68 already binds it. Only the non-derivable half survives, that store reclaim is invisible to `du` and must be read from `df`.
- `Lojix records that reference store paths are historical, not GC roots, so store GC does not corrupt lojix.` (recovered) — reassurance against a fear nobody has recorded having.
- `After deleting a system-profile generation, refresh stale boot-menu entries with a lojix deploy, never a manual nixos-rebuild.` (recovered) — a deploy rule. It belongs in os-operations, and I did not move it there; relocation is out of scope. Flagged.
- `Re-measure with df -h and report space reclaimed.` — an agent reports what it reclaimed.

### Added

- **The whole jj-workspace block.** This is the change of subject the redesign needed. `reports/orchestrate-worktree-redesign/spec.md` audits the actual litter: 186 stale workspace entries whose root is gone, 21 rooted in `/tmp`, 40 under `~/agent-worktrees` (267M), ~17 corpses at `~/wt` in no store at all, 4 jj-unreadable stores, 242 live workspaces at `~/wt` totalling 13G. The same file states the safety rule verbatim: "`rm -rf <worktree>` alone does not lose commits… `jj workspace forget <name>` drops the working-copy commit's reference. The commits are still reachable via the source's op log. The point of no return is `jj util gc` on a source checkout after a forget." And: "`jj workspace forget` + `rm -rf` is forbidden until a push has been verified… A zero exit status from `jj git push` is not sufficient evidence."
- **Stray `result` symlinks.** True right now: `/home/li/primary/result`, `result-1`, and `result-2` point at store paths from 22-24 July and each holds a closure against collection.
- **The ghq-root worktrees, reported not deleted.** 212 directories under `/git/github.com/LiGoldragon` against 167 `ghq list` entries. The 45 extra are branch worktrees created in the ghq owner root instead of `~/wt/<host>/<owner>/<repo>/<branch>`. "Report, do not delete" because a live workspace looks identical to a corpse from outside.
- **Everything in the nix-generation block is recovered, and its only witness is the recovered skill text itself.** Grepping `reports/` and `agent-outputs/` for `nix-collect-garbage`, `nix store gc`, `nix profile wipe-history`, and `cargo clean` returns nothing. The skill records its own sweep — a 196 GB store GC out of a 215 GB total, and one host booted on `system-136` while `system-142` was current, both needing to survive — and I am keeping it on the strength of that first-hand record. If you do not recognize that sweep, the block has no witness and should go.

### Context, not a rule

Root is at 745G used of 916G, 86%, against `reports/field-readiness/13-tooling-field.md`'s 2026-07-03 reading of "disk 51% used, 433G free". The ghq owner root is 132G and `~/wt` is 50G.

## 5. work-tracking

### Current

```
# Skill — work tracking

- Track work only when it must survive the session or coordinate independent work.
- Give each item an outcome, proof, and dependencies.
- Close an item only with durable evidence.
```

### Proposed

```
Run `bd` commands one at a time. The tracker is a single-writer store and a parallel call fails on the `.beads/embeddeddolt` lock.
Retry the same `bd` command after a lock error instead of starting a second one.
Open an item only when the work must survive the session, or another agent must pick it up.
Give an item acceptance criteria that name the command or artifact which will prove it.
Say how the item's scope was enumerated. A count of repositories or files is worth no more than the list it came from.
Claim the item you are working, not the area around it.
Refuse an item whose description is factually wrong, and say what is wrong with it.
Close an item with the commit and the command output that prove it, or leave it open and name the blocker.
Sort a backlog by age and start at the oldest. An item open two weeks needs a reason; an item open a month is a candidate to close as invalidated.
```

### Description

`Use when opening, closing, or triaging tracked work items.`

### Cut

- `Give each item an outcome, proof, and dependencies.` — replaced by the acceptance-criteria line, which says what the proof has to be.
- The six-part bead-content list and the anti-pattern list (recovered) — how to write a ticket. Documentation.
- `Dependencies are directional: producer before consumer, schema before generated code, contract before implementation, migration before removal.` (recovered) — producer-before-consumer now lives in the landing skill, and the other three follow from it.
- `Split a bead when part of the work can land and be verified independently.` (recovered) — derivable from the acceptance-criteria line.
- `Do not rewrite history into certainty.` (recovered) — `tenets` covers it.
- The word "bead" in the body. The command is `bd`, the skill name is work-tracking, and an agent connects them.

### Added

- **Sequential `bd`.** The strongest line here, because it contradicts a default this harness actively encourages: independent tool calls are supposed to go in one block. `bd` uses a single-writer embedded Dolt store and a concurrent call fails on the `.beads/embeddeddolt` lock. Recovered, and beads is live — `/home/li/primary/.beads/last-touched` is dated yesterday and `bd list` returns a populated `primary-*` graph.
- **Say how scope was enumerated.** `agent-outputs/RenamePropagator/Tier2-SchemaDrift-Evidence.md`: `signal-lojix` had drift identical to eleven tracked repos but "was NOT in bead 5kxh's 11-repo list — it was masked as 'no-flake (false-fail)' in the A checkpoint." The item could have closed 11/11 with the defect still live.
- **Refuse a wrong description.** `reports/nota-release-train/recovery-status.md`: an inherited item was not executed because "the enumeration that framed it was factually wrong (named live code for deletion)". Agents comply with the ticket; this says not to.
- **The age gradient** is recovered. The numbers are what make it usable.

## 6. main-feature-integration

### Recommendation: rename to `cross-repo-landing`, and absorb the deleted `release-train-development`

I was going to recommend merging into `release-train-development` — it and
`main-feature-integration` are one discipline at two maturity levels, stating
the same producer-before-consumer invariant with different rigour. Skills commit
`6f23fd59a0eb`, landed at 13:36 today, deleted `release-train-development`
outright. Its three lines are now nowhere.

So: rename, and take the orphaned lines. Not a merge into `feature-development`,
which is a genuinely separate single-checkout concern (which branch or worktree
you work in, do not share it, conclude it) with no overlap.

The current name is three nouns that do not say when to reach for it. Every
incident under this heading is about a consumer pinning a producer across
repository boundaries, which is what the new name says. It also closes a
manifest gap: `main-feature-integration` declares zero module dependencies
today, while the skill it duplicated declared
`[feature-development version-control nix-discipline testing]`.

### Current

```
# Skill — feature integration

- Integrate from current main on the assigned integration branch.
- Test affected branches together.
- Land portable producers before consumers.
```

### Proposed, as `cross-repo-landing`

```
Pin a consumer to a pushed revision of the producer. A branch-named dependency under `--locked` keeps resolving to the revision already in the lock.
Push the producer before building anything against it. A build from an unpushed working copy does not reproduce from a fresh clone.
Land producers before consumers, then update each consumer's lock.
Check `Cargo.lock` and `flake.lock` separately. They pin the same dependency independently and drift apart.
Name every repository that must move to the integration branch, not only the one you changed.
Remove local path overrides before the branch is merge-ready.
Rebase onto `main` and rerun the checks that cover the change when `main` moves while the candidate is going green.
Report which repositories landed and which are blocked on an upstream landing.
```

### Description

`Use when a change must land in more than one repository, or when a consumer pins a producer you are changing.`

### Cut

- `Integrate from current main on the assigned integration branch.` — two rules welded; the branch assignment is `feature-development`'s.
- `Test affected branches together.` — replaced by the rebase-and-rerun line, which says when.
- The seven-step numbered flow (recovered) — steps 1, 3, and 7 are `feature-development` and `version-control`; the rest survive as the lines above.
- `Resolve every train member to a pushed immutable revision.` (deleted skill) — survives as the first two lines, in the form the incidents took.
- `Verify the resolved closure before landing producers and consumers.` (deleted skill) — the Synchronizer closure does not exist yet, so this instructs against a tool that is NO-GO in all four audit passes. Reduced to the ordering rule that remains true by hand.

### Added

- **Branch-named deps resolve stale under `--locked`.** `agent-outputs/RenamePropagator/Tier2-SchemaDrift-Evidence.md`: five consumers were "own-fixed; CASCADE-BLOCKED on `signal-domain-criome@3aca3282` (stale dep pin)" — `branch=drop-next` under `--locked` still resolved to the pre-fix revision. The fix was done and the consumers still could not build.
- **Push before building against it.** `reports/field-readiness/11-build-readiness.md`: spirit was built from unpushed local dirty state on `criome-authorization-push`, and "a fresh clone or remote builder-only flow produces different bits".
- **Name every repository that must move.** `agent-outputs/CapacityAdmissionSlice/CriomosImplementer-IntegrationBaseEvidence.md`: a `signal-criome` 0.6.0 bump forced a `links="signal-criome"` conflict in `meta-signal-criome`, fixed by repointing that repo's integration branch too, with the warning "Any future consumer of this stack must pin meta-signal-criome to the integration branch too."
- **Two lock files.** `Cargo.lock` and `flake.lock` pin independently. The cross-repo rkyv decode failures that surfaced as "router socket unreachable" were lock drift, not a network fault.

### Open for you

`release-train-development` was deleted rather than cut down to its own lines,
which is not what handover item 1 proposed. The three lines above are my
rehoming of what it carried. If the deletion was meant to discard that content
rather than move it, say so and I will drop them.

## 7. versioning

### Current

```
# Skill — versioning

- Update the version surface changed by public behavior, wire, storage, package, or deployment changes.
- Do not bump docs-only changes unless the docs are runtime-visible.
```

### Proposed

```
Bump the version surface in the same change that changes the behavior.
Give a durable storage schema change a stated migration, reset, or rebuild path in the same change.
Bump a daemon when a contract it consumes changes.
Update the locks of every repository that pins the changed component.
Say whether a new version is landed only, or also deployed.
Signal a breaking wire change before 1.0 with a minor bump.
A major bump needs psyche authorization.
Change the version for a documentation edit only when that prose ships inside the component.
```

### Description

`Use when a change alters public behavior, a wire contract, a storage schema, or a deployed package.`

### Cut

- The semver table (recovered) — that is what semver means. Documentation. There is no versioning document in `standards`; that is where it goes, and relocation is out of scope this session.
- `If patch/minor/major or landed/deployed status is unclear, ask instead of guessing.` (recovered) — `general-instructions` already routes unresolved questions to the caller.
- The four-item enumeration of version surfaces — the current first line already lists them; a second listing teaches rather than directs.

### Added

- **Storage schema changes carry a migration path.** The lojix daemon self-upgraded `0.3.10 → 0.4.1` during a live System Switch. The switch stopped the old daemon before it committed deploy 41's activation record, and the successor came up on fresh generation state with a changed query vocabulary. Result: `GenerationUnknown (0 0)`. Two independent audits converged on the same root cause — `agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md`, and `agent-outputs/Handover-Orchestrate-RustAudit-SEMAEpic.md`, which generalizes it: "components generally lack an explicit next step: migration, deliberate reset/quarantine for disposable state, or durable rebuild path for durable state." The same schema-mismatch class also took down `mirror.service` and `orchestrate-daemon`.
- **Bump the consuming daemon; update downstream locks.** Cross-repo rkyv decode failures surfaced as "router socket unreachable" and failed-then-passed on identical sources. Root cause was contract lock drift; the fix was `signal-frame 0.3.0` with consumers repinned, verified green on prometheus.
- **Landed versus deployed.** Landing on `main` and being the current generation on a node are separate facts here, and a report that says "shipped" without distinguishing them cannot be checked.
- **Minor bump signals a breaking wire change before 1.0.** *This one is not yours yet.* The only statement of it I found is one auditor's judgment in `agent-outputs/MentciOrchestrateSessionFlow/RustAuditor-LiveViewReview.md`: "a `0.2 → 0.3` minor bump is the correct breaking-signal under 0.x semver. Deliberate and correct." Nothing in `standards` or any skill says it. It is in the block so you can rule on it rather than being left out silently. Delete the line if it is not your rule.

## 8. engine-analysis

### Current

```
# Skill — engine analysis

- Trace real components, channels, state owners, and end-to-end flows.
- Mark each claim as wired, stubbed, contract-only, conceptual, or stale.
- Name missing witnesses instead of filling gaps with design intent.
```

### Proposed

```
Mark every claim wired, stubbed, contract-only, conceptual, or stale.
Cite the file and symbol behind each claim.
Follow each flow to the point where it stops, and name that point.
Find the construction site of every declared variant. A type nothing constructs is contract-only.
Code outranks a doc comment. Mark a comment that contradicts the code as stale.
Re-derive a prior lane's claim from source before repeating it.
Run the component's tests and checks. Do not only read the source.
List the files and subsystems you did not read this pass.
Name a missing witness. Do not fill the gap with design intent.
```

### Description

`Use when explaining how a running system works, or judging which of its paths are real.`

### Cut

- `Trace real components, channels, state owners, and end-to-end flows.` — this is "analyze the engine". It restates the skill name, which is the first entry on `skill-designing`'s own cut list.
- The channel ledger, the trust-boundary map, and the seven-part output shape (recovered) — report formatting. Documentation.
- `Prefer source files, tests, generated schemas, runtime commands, and small diagrams.` (recovered) — a preference, not an action; the cite-the-file line does the work.
- Separating observations from interpretations into named sections — the best exemplars do this, but `tenets` already says "Keep observations, hypotheses, and unknowns separate." Not restated.

### Added

- **Find the construction site.** `agent-outputs/PersistentSpiritMirror/CriomeQuorumReadiness-Scout.md`: "The `ComplexQuorum` policy class exists in the type system but the runtime never emits it." The vocabulary already has a word for that state; nothing told the agent the search that finds it.
- **Doc comments go stale against code.** Same report: "the `admission.rs` module doc-comment still says the gate is unwired — that comment is stale relative to `registry.rs`."
- **Re-derive a prior lane's claim.** `agent-outputs/PersistentSpiritMirror/RouterTransportReadiness-Scout.md`: "The earlier lane note conflated this local fanout with the peer-forward path." And the author of `reports/SkillsCorpusRedesign/context-handover.md` lists as their own first failure: "Relayed a subagent's claim of a contradiction in the standards repo without checking it. There was none."
- **List what you did not read.** `RouterTransportReadiness-Scout.md` carries a "Not checked this pass" section naming untouched files. "Name missing witnesses" covers claims that lack support; it does not cover scope that was never surveyed, which is how an analysis reads as complete when it is partial.
- **Run it.** `agent-outputs/MindLiveJudgeEval/RustAuditor-CorrectionAudit.md` ran `jj status`, `cargo test`, and `cargo check` as part of the trace. Reading-only is the default failure of this kind of work.

### Open for you

The status vocabulary has drifted. The recovered text and the reports say
**hooked**; the deployed skill says **wired**. I kept `wired`, which is the
current word and the clearer one, but the two must not both circulate. Also,
"engine" is undefined anywhere in `AGENTS.md`, `protocols/`, or `standards` —
in practice it means a standing daemon with a thin CLI, hosting Kameo actors
over a `signal-*` wire contract, per `logos-engine/ARCHITECTURE.md` and
`schema-engine/ARCHITECTURE.md`. If that definition is right it is a standards
entry, not a skill line.
