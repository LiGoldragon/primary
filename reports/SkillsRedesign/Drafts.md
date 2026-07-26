# Eight skill redesigns — replacement text

Draft only. Nothing in `LiGoldragon/skills` was edited. Source files are
`/git/github.com/LiGoldragon/skills/skills/<name>.md`; the `description` field
lives in `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota`.

Recovered specifics come from `7f5753642f1d^` in the skills repo — the state
before "skills: reduce reusable guidance". Where a line survives from there, the
incident behind it is named in the notes.

## version-control

### Current

```
# Skill — version control

- Use `jj` for ordinary history and pushes.
- Use an explicit message for every authored commit.
- Preserve peer work and verify the pushed bookmark.
```

### Proposed

```
Pass `-R <path>` on every mutating `jj` command aimed at a repository other than the current working directory.
End any `cd` in a script with `|| exit`. The shell resets to the workspace root between tool calls, so a failed `cd` aims the next command at primary.
Outside primary, commit one logical change at a time.
Push each completed commit. Do not accumulate a finished local stack.
`jj` commits and pushes a conflicted tree without failing. Read `jj status` for conflicts before setting a bookmark.
Stop and ask before rewriting or force-moving a commit you did not author.
Capture a revision hash by pasting from `jj log`, `git ls-remote`, or an existing lock entry. Never type or complete one from memory.
Initialize a repository with no `jj` metadata using `jj git init --colocate`, then `jj bookmark track main@origin`.
Recover a destroyed working copy through `jj op log` and `jj op restore`.
Raw `git` is allowed for three things: reading or changing remote configuration, `git ls-remote`, and `git worktree prune`.
```

### Description

`Use when committing, pushing, or repairing history in any repository.`

### Cut

- `Use jj for ordinary history and pushes.` — AGENTS.md line 67 already binds this.
- `Use an explicit message for every authored commit.` — AGENTS.md lines 64-65 already bind inline messages and the no-editor rule.
- `Preserve peer work and verify the pushed bookmark.` — two rules welded into one line, and both are what any agent does untold. Replaced by the conflict line and the ask-before-rewrite line, which name the specific way peer work is actually lost here.
- The whole primary flow (`jj commit -m` / `jj bookmark set main -r @-` / `jj git push --bookmark main`, work on main, commit the whole working copy) — verbatim in AGENTS.md lines 62-66.
- `Do not use jj git push -c @.` (recovered) — I found no instance of it. Cut for want of an incident.
- `jj restore discards working-copy content. Use it only when the exact path and loss are understood.` (recovered) — "do not destroy what you do not understand" is the shape he rejects. The replacement is the `jj op restore` line, which gives the agent a move instead of a warning.
- `--no-pager` on every read command (recovered) — `jj log` and `jj status` return without a pager in this harness. Tested, not assumed.
- `Identify pushed work by its bookmark in reports.` (recovered) — an agent already reports "pushed to main".

### Added

- **`-R <path>` and `|| exit`.** Recovered. The mechanism is stated in this harness's own notes: cwd resets between bash calls. A `cd` that fails silently leaves a mutating `jj` command pointed at primary. The agent cannot derive this — it is a property of the tool, not of `jj`.
- **Conflicts commit and push without failing.** `jj` records a conflict in the commit rather than blocking. Witness: commit `d9b3382580cd` in primary, 2026-06-30, "skills: regenerate role destination doctrine", carries a conflict. It is not in `main`'s ancestry, so it was caught, but it was created. Every git-trained intuition says a conflict blocks the commit; here it does not.
- **Never compose a revision hash.** This workspace pins deploys and flake inputs by 40-hex rev (`github:LiGoldragon/CriomOS?rev=<40-hex>`) and release-train members by bare commit. Completing a short prefix to full length is a plausible action that produces a fabricated pin.
- **The escape-hatch list.** AGENTS.md line 67 says "No raw `git` except the documented escape hatches in the `jj` skill." **There is no `jj` skill.** The 26 deployed skills are listed in `.agents/skills/`; none is named `jj`, and no file anywhere enumerates the hatches. The boot contract points at nothing. `git worktree prune` is documented in `/home/li/primary/NON_IDEAL_AGENTS.md` and witnessed 2026-07-16 across CriomOS, signal-introspect, and signal-standard; remote-config repair and `git ls-remote` come from the recovered text. This skill is the only candidate home.
- **`jj op restore`.** No incident found. Included because an agent that clobbers a working copy reconstructs it by hand, and the operation log is a capability it will not reach for untold. Flagged as unevidenced.

### Open for the psyche

AGENTS.md line 67 names a `jj` skill that does not exist. Two fixes: rename this
skill to `jj`, or amend line 67 to say `version-control`. Renaming is the better
one — the repo's version control is `jj`, and the name would then match what the
boot contract already calls it. Both touch the boot contract, so neither is mine.

## testing

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

- All three current lines. "Smallest meaningful witness", "durable test gate", and "keep requirements explicit" name end states without naming a command, a test, or a case.
- Test naming, fixture minimalism, assertion-message craft, and where unit versus integration tests live (recovered) — this is how to write a test. Documentation. It belongs in `standards`, and I am not moving it there this session.
- `Test architecture, not just regression` (recovered) — the `architectural-truth-tests` module already carries it.
- `Do not weaken tests to pass. Do not delete coverage without replacing the proof.` (recovered) — I looked for an agent deleting or skipping a failing test to reach green and found none. Every "removed test" hit was dead code after a migration. Cut for want of an incident; the three gaming shapes that *are* evidenced are covered by the `--rebuild`, assertions, and skip-reporting lines.

### Added

- **`--rebuild` when the run is the evidence.** `reports/capacityAdmissionSlice/4-Audit-adversarial-reaudit-deploy-smoke-green.md`: a `nix build` of a VM check hit an already-realized store path and "boots zero VMs and exits 0". A prior agent reported that as green. The re-audit had to force a rebuild to get a real boot.
- **Read the assertions.** Same report: `assert not expected_closure.endswith(".drv")` is true regardless of whether the deploy ran, and `assert 'Deployed' in deploy_reply` proves admission, not completion. `reports/synchronizer/train-flow-audit-v1.md`: the live-run test "builds `members` from its own selectors so the check passes trivially… membership passes tautologically."
- **VM host designation.** `CriomOS-test-cluster/INTENT.md` requires VM checks on an authorized VM host and says an unknown host is "a documented blocker, not an attempted QEMU run". An agent ran QEMU on the laptop instead, justified by KVM presence alone.
- **Skips and unevaluable components are not-run.** `harness/tests/message_router_harness_e2e.rs` skips silently when peers are absent and is not wired into `harness/flake.nix` at all. Separately, `forge` and `mentci` are invisible to the Nix sweep, which made "all repos build" vacuous.
- **Background and file for long runs.** `reports/field-readiness/11-build-readiness.md`: router ~44, mind ~60, persona ~120 checks; a worker session "died mid-sentence" because `nix flake check` on a cache-missing repo "silently becomes an hours-long build with logs flooding the worker's context."
- **`tail`/`head` and the socket path limit** are recovered lines. Both name a mechanism that silently inverts a result.

## versioning

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

- The semver table (patch / minor / major definitions, recovered) — that is what semver means. Documentation. There is no versioning document in `standards` today; that is where it goes, and I am not moving it this session.
- `If patch/minor/major or landed/deployed status is unclear, ask instead of guessing.` (recovered) — `general-instructions` already routes unresolved questions to the caller.
- The four-item bullet list of version surfaces — the current first line already enumerates them, and enumerating them again teaches rather than directs.

### Added

- **Storage schema changes carry a migration path.** The lojix daemon self-upgraded `0.3.10 → 0.4.1` during a live System Switch. The switch stopped the old daemon before it committed deploy 41's activation record, and the successor came up on fresh generation state with a changed query vocabulary. Result: `GenerationUnknown (0 0)`. Two independent audits converged on the same root cause — `agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md` and `agent-outputs/Handover-Orchestrate-RustAudit-SEMAEpic.md`, which states it generally: "components generally lack an explicit next step: migration, deliberate reset/quarantine for disposable state, or durable rebuild path for durable state."
- **Bump the consuming daemon; update downstream locks.** Cross-repo rkyv decode failures surfaced as "router socket unreachable" and failed-then-passed on identical sources. Root cause was contract lock drift; the fix was `signal-frame 0.3.0` with consumers repinned, verified green on prometheus (`reports/field-readiness/02-kink-ledger.md` closeout delta).
- **Landed versus deployed.** Landing on `main` and being the current generation on a node are separate facts here, and a report that says "shipped" without distinguishing them is unverifiable.
- **Minor bump signals a breaking wire change before 1.0.** *This one is not yours yet.* The only statement of it I found is one auditor's judgment in `agent-outputs/MentciOrchestrateSessionFlow/RustAuditor-LiveViewReview.md`: "a `0.2 → 0.3` minor bump is the correct breaking-signal under 0.x semver." Nothing in `standards` or any skill says it. I put it in the block so you can rule on it rather than leaving it out silently. Delete the line if it is not your rule.
