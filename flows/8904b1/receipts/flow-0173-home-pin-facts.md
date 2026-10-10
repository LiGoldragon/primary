# Flow 0.17.3 Home pin — read-only fact-finding

Subflow of 8904b1, 2026-09-26. Read-only throughout: no branch, commit, rebase,
merge, push, build, check, or install performed by this subflow. All builds/tests
below were run earlier by someone else; this subflow only read the pre-existing
`nix log` output and git/jj history.

Each item marked **witnessed** (this subflow verified it directly) or **claimed**
(56ae53's account, not independently verified here).

## Where Flow 0.17.3 lives — witnessed

- Repo: `LiGoldragon/flow`, real remote `ssh://git@github.com/LiGoldragon/flow.git`.
- Local clone used for this check: `/tmp/flow17-review.iXvykH` (its `.git/logs`
  reflog shows the exact rev was fetched from `origin`, not created locally).
- Revision: `0b512ee0b6681b1925fee7b6435aa7c2eac26bfb`, on remote branch
  `flow/0173-merge-56ae53`. Commit: "Merge Flow 0.17.3 Claude startup repair onto
  main", author `li`, 2026-09-26 18:42:36 -0600. Its two parents are
  `9fcd625ac7a0d44be58b9d365a94064e91f09219` (current tip of the flow repo's own
  `main`) and `0b2929ef24dea8dd83ebc8924bf3e2b6c8950493` (a startup-repair branch) —
  confirmed as an actual merge onto flow's main, not a side branch pretending to be.
- `Cargo.toml` at that revision reads `version = "0.17.3"`.
- **Untagged**: no git tag reaches this revision in the local clone.
- Flow's own `UPGRADES.md` at this revision, for 0.17.3 and for 0.17.2/0.17.1
  before it: "Deploy beside Message 0.17.0, or do not deploy at all." This is a
  coupling requirement authored by Flow's own maintainers, not part of 6fe957's
  Messenger-pin scope.

## What Home pins for Flow now — witnessed

- CriomOS-home real remote `origin/main` tip: `fed500843629c828a91fa0e06b9946b69c167898`,
  "Home: repin next Flow to 0.17.1". (Local `main` branch pointer in
  `/git/github.com/LiGoldragon/CriomOS-home` is stale at `657f4ba8...`, three
  commits behind `origin/main` — a local-clone staleness, not a remote-main fact.)
- At `origin/main`, Home's `flake.nix`/`flake.lock` carry two separate Flow-repo
  inputs: a stable `flow` input pinned at `9fcd625...` (flow's own main tip) and a
  `flow-next` input pinned at `ac216c899b8e43fa3401609e3ca2605d9856e7e4` (Flow
  0.17.1). A sibling pair `message` / `message-next` exists the same way; `message-next`
  is pinned at `481b579fcf72797ffa9ccf8ce4e2283a58cdff97` = Message 0.17.0
  (verified against the `LiGoldragon/message` repo's own `Cargo.toml`). Home's
  `flake.nix` comment states `flow-next` "moves with message-next below: both
  share signal-flow 1c9e4b30 and meta-signal-flow 2ac045c2" — Home already treats
  Flow-next and Message-next as one coupled unit, consistent with Flow's own
  "deploy beside Message 0.17.0" rule.

## The Home stage branch — witnessed

- Location: `/home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-0173-stage-56ae53`,
  a `jj` (Jujutsu, colocated) checkout, no separate `.git` dir of its own visible
  from outside jj.
- Bookmark: `home/flow-0173-stage-56ae53`, at commit `b7030941b6a0`, "Stage Flow
  0.17.3 for next Home service", author `li`, 2026-09-26 18:44:19 -0600. No
  Claude/Codex co-authorship line on this commit (contrast: an earlier commit in
  the same history, `657f4ba8`, does carry a `Co-Authored-By: Claude Opus 5.5`
  line, so the absence here is a real difference, not a missing convention).
- **Cut from**: its immediate parent is `fed500843629` — i.e. it is cut directly
  from current Home main (`origin/main`), not from an older main. It needs no
  rebuild on that account today.
- **What it changes** (3 files, verified by full diff):
  1. `flake.nix`: `flow-next.url` rev bump only, `ac216c8...e7e4` (0.17.1) →
     `0b512ee...26bfb` (0.17.3). The nearby `message-next.url` line is untouched.
  2. `flake.lock`: the `flow-next` node's `lastModified`/`narHash`/`rev` fields
     updated to match (`narHash: sha256-p/F8vLbS1UEPJ4BuL8VwczP5LrmS7qGl5ieMdu/ldtU=`,
     `lastModified: 1790469756`) — flake and lock move together in this one commit.
  3. `checks/flow-message-next/default.nix`: only the `nextFlow` expected-hash
     literal updated to the new revision, plus an unrelated small refactor of the
     `stableMessageService.ExecStart` assertion (line-wrap only, same check).
     `stableFlow`, `stableMessage`, and `nextMessage` expected values are
     untouched — the stage commit does not touch Message versions at all.
- **Does it touch the same flake/lock lines as the Messenger pin?** Not the same
  lines: the Messenger pin (`home-messenger-pin-6fe957`, commit `3991923ac2c1`,
  "Home: pin messenger-clj 0.2.6 determinism successor") changes the
  `messenger-clj.url` line (~108) and its own lock node; the Flow stage changes
  the `flow-next.url` line (~102) and the `flow-next` lock node. Different lines,
  same two files (`flake.nix`, `flake.lock`) and the same lock file's node graph —
  this is the ground the standing ruling already gives for one owner/sequencer.
- **Would it need rebuilding on a Home main that carries the Messenger pin?**
  Yes, and more concretely than the ruling assumed: the Messenger-pin commit
  (`3991923ac2c1`) is itself based on `657f4ba8167132a70357a4326532bcda2416b789`,
  which is **two commits behind current Home main** (missing `b8b45e2f...` "Move
  next Flow and next Message to 0.17.0 together" and `fed500843629` "repin next
  Flow to 0.17.1"). So the Messenger branch itself needs to move onto current
  main before or as it lands; once it lands, main will carry one more commit than
  the Flow stage's parent, so the Flow stage (cut from `fed50084`) will then be
  one commit behind and must be rebuilt on the new main, exactly as the ruling
  anticipated.

## Who made it — witnessed

Both the stage commit and the Messenger-pin commit are authored `li`
(the human operator), not attributed to any Mind/Field/Psyche flow identity in
the commit metadata.

## The claimed tests — witnessed for Flow specifically

- `nix log /nix/store/d3ixary6dfx80928m3y35ihin2nin1l7-flow-0.17.3.drv` (an
  existing, already-recorded Nix build log — reading it triggers no new build)
  shows a completed build: 164 `flow` crate unit tests passed, plus `flow-nexus`
  unit and integration tests passed, 0 failed; `checkPhase completed`; installed
  to `/nix/store/xcyfmwlp35pkpsz6jfajbv2vbql3yk9i-flow-0.17.3`.
- This substantiates 56ae53's claim of a passed capped local build/test for
  **Flow** 0.17.3. Messenger 0.2.6's build/test log was not checked by this
  subflow (out of scope: Messenger is 6fe957's existing, separately-owned step).
- Content-hash verification: `flake.lock`'s recorded `narHash` for the `flow-next`
  source at this rev is internally consistent with the fetched git history; this
  subflow did not independently recompute the nix content hash from a fresh
  fetch (that would require a network fetch/build, excluded by the read-only
  constraint), so treat the hash as recorded-and-consistent, not re-derived here.

## Temporary GC roots — witnessed

- `/home/li/.local/state/flow/recovery-gcroots/flow-0.17.3-56ae53` →
  `/nix/store/xcyfmwlp35pkpsz6jfajbv2vbql3yk9i-flow-0.17.3`
- `/home/li/.local/state/flow/recovery-gcroots/messenger-clj-0.2.6-93c12756-56ae53` →
  `/nix/store/b1jm0wg94v7pc6p95kr01hh2byl1jifw-messenger-clj-0.2.6`
- Both confirm 56ae53's claim of temporary GC roots for both packages. A
  temporary GC root is not a release and does not imply activation.

## Installed / running on this host — witnessed, and one addition to 56ae53's account

- `/nix/store/xcyfmwlp35pkpsz6jfajbv2vbql3yk9i-flow-0.17.3` is **not** linked from
  `/run/current-system` or any user profile found, and no running process's
  `/proc/<pid>/exe` resolves to it. Nothing of 0.17.3 is installed or running —
  consistent with 56ae53's "nothing is activated."
- Not part of 56ae53's claim, but observed while checking: two *other*
  `flow-nexus` processes are live on this host right now — PID 1937 running
  `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus` and PID
  90750 running `/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-nexus`.
  Neither is 0.17.3; this is offered as host context, not a contradiction of the
  "nothing activated" claim about 0.17.3.

## Nothing contradicts 56ae53's account

Every specific claim checked (tested source and package, a separate Home stage
branch, no activation) held up under direct witness. The one correction is a
sharpening, not a contradiction: the Messenger-pin branch is itself two commits
behind current Home main, which matters for how "on top of the Messenger main
move" is carried out.
