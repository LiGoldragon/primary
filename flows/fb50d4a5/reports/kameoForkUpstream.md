# Kameo fork/upstream relationship

Status at 2026-08-22: the authoritative local fork is `/git/github.com/LiGoldragon/kameo`. Its `main` is `3486e4f63ea4e87123476cfbdefeb12403540306`; upstream is `tqwewe/kameo` `main` at `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`. The heads are diverged, not fast-forward-related.

## Observations

Local Jujutsu and forge evidence agree:

- Remotes: `origin = git@github.com:LiGoldragon/kameo.git`; `upstream = git@github.com:tqwewe/kameo.git`.
- Merge base: `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`, `chore: use libp2p::identity instead of libp2p_identity directly (#339)`, 2026-06-19.
- Fork unique commits: 6. Upstream unique commits after that base: 49. Forge comparison from fork to upstream says `status=diverged`, `ahead_by=49`, `behind_by=6`.
- Fork head's authored date is 2026-06-19; it was committed/pushed to the fork on 2026-08-12/13 by a later metadata-only `AGENTS.md` commit. Upstream `main` last committed 2026-07-21.
- The checkout was clean. No fetch, checkout, ref update, source edit, configuration edit, or live-state mutation was performed.

The six fork-only commits are:

1. `1325f6aef7e13996f929d17447ddd2abaa514444` — `actor: publish terminal lifecycle outcomes`.
2. `da0f64af20a4f3002a79a1a5aa2efae416eadfd6` — `actor: split lifecycle control mailbox`.
3. `1980e34b5e694b4eb268f24d75fcfa8e527d1472` — `actor: cover lifecycle control edge cases`.
4. `8ea1e3fab5350ddd86b1bfd18dd3cbd4a0002164` — `actor: gate weak shutdown result helpers`.
5. `f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01` — `fix lifecycle fork after upstream rebase`.
6. `3486e4f63ea4e87123476cfbdefeb12403540306` — `docs: mark Protos estate status`.

The full 49-commit upstream set and notable API commits are recorded in `witnesses/upstreamUniqueCommits.md` and the forge comparison in Sources.

## Substantive fork differences

The fork is a lifecycle-semantics fork, not a cosmetic fork.

- It introduces public `ActorTerminalOutcome`, `ActorTerminalReason`, and `ActorStateAbsence`, backed by an internal `ActorLifecycle` `SetOnce`. `ActorRef::wait_for_shutdown()` returns the terminal outcome and `is_terminated()` reports publication. Upstream's method returns `()` and waits for mailbox closure.
- It adds `outcome: ActorTerminalOutcome` to `Actor::on_link_died` while retaining `ActorStopReason` for legacy detail. It classifies `CleanupFailed` and `StartupFailed`, and passes the outcome into restart/link decisions.
- It changes `PreparedActor::run`, `spawn`, and `spawn_in_thread` from `Result<(A, ActorStopReason), PanicError>` to `Result<ActorStopReason, PanicError>`; actor state is consumed during teardown rather than returned.
- It orders terminal teardown around the new outcome: after `on_stop`, actor state is dropped before awaited link notification; compatibility shutdown result and terminal outcome are then published. Startup failure publishes `StartupFailed`/`NeverAllocated`.
- It replaces one signal channel with ordinary-message and unbounded control lanes. Ordinary messages carry an atomic generation; shutdown closes message admission and increments the generation. Biased receive/poll paths prioritize lifecycle/control signals and discard stale queued messages. Upstream's current `accepting` gate rejects new messages after `stop_gracefully`, but its mailbox still carries messages and lifecycle signals in one channel.
- It awaits link notification dispatch inline and carries the terminal outcome through local/remote link notifications. Upstream still schedules parent/sibling notifications with `tokio::spawn` and has no terminal-outcome parameter.

The fork diff from the common ancestor is 20 files, +2,117/−351. The upstream diff from that ancestor is 65 files, +8,014/−717. Upstream's additional 49 commits include root package `0.22.2`, lifecycle deadlock/panic fixes, pending-mailbox and drain changes, `on_undelivered`, `ctx.pipe`/`ctx.pipe_with`, single-Arc `ActorRef` cloning, FutureActor, console/TUI, tracing, and error improvements. The fork root `Cargo.toml` remains `0.20.0`.

## Tags and releases

- Upstream latest root release is `v0.22.2` (2026-07-18, commit `90138758779d2260798c41cfaa47598db84f05b8`). Releases after the fork base are `v0.21.0`, `v0.21.1`, `v0.22.0`, `v0.22.1`, and `v0.22.2`; latest component tags include `actors-v0.8.1` and `console-v0.1.4`.
- The local checkout contains these upstream tags, but they are not fork releases and are not ancestors of fork `main` after the common base.
- `LiGoldragon/kameo` has zero GitHub releases. Its latest origin root tag is `v0.20.0` (`2c075ec7...`); fork `main` is untagged. The fork's package version remains `0.20.0` and its Cargo repository metadata still names `tqwewe/kameo`.

## Consumer pins and authority

Read-only manifest inspection found 20 repositories with direct `LiGoldragon/kameo` URLs:

- 15 use `branch = "main"`.
- 4 use immutable revision `f491b45d...`: `ethos-engine`, `logos-engine`, `sema-storage`, `triad-runtime`.
- `persona-spirit` uses `branch = "persona-lifecycle-terminal-outcome"`.

Most local lockfiles resolve branch-main consumers to `f491b45d...`, not the later docs-only `3486e4f6`; the source code is therefore the same as the fork head, but lockfiles are stale snapshots and branch manifests are not immutable authorities. The forge currently returns 404 for `persona-lifecycle-terminal-outcome`; its lockfile retains commit `22514f7c...`, which remains addressable by commit SHA. Whether Cargo can resolve that deleted branch from the lockfile without a fresh branch ref was not tested.

`lojix/Cargo.toml` declares crates.io `kameo = "0.20"`, while its local lockfile contains LiGoldragon fork revision entries at `f491b45d...`. This manifest/lock discrepancy was observed, not resolved; effective build provenance remains unknown without a Cargo-resolution probe.

## Claims

- The present Git relationship is a 6-commit fork versus 49 upstream commits from one common ancestor; this is witnessed by both local Jujutsu ancestry and fresh forge comparison.
- The fork's custom lifecycle/mailbox design remains materially absent from upstream `main` at the witnessed head; upstream's `accepting` gate partially overlaps message admission only.
- Upstream has advanced to release line 0.22.2 while the fork remains package-version 0.20.0 and has no fork release.
- The current consumer estate is not governed by one uniform immutable pin: branch-main, f491 revision, a deleted feature branch, and a manifest/lock discrepancy all coexist.

## Hypotheses

- The six fork commits were intentionally kept as a lifecycle contract experiment; this is inferred from commit subjects and code shape, not from a current design ruling.
- Upstream's lifecycle deadlock fixes may address some problems that motivated the fork, but code evidence alone does not establish equivalence to the fork's terminal-outcome cell or two-lane mailbox.

## Unknowns and evidence limits

- No build, test, Cargo metadata, or dependency-resolution command was run. Compile compatibility and actual selected revisions therefore remain unknown.
- The deleted `persona-lifecycle-terminal-outcome` branch may still resolve from the lockfile's retained object, or may fail when Cargo requires the branch ref; this needs an explicitly authorized resolution probe.
- The `lojix` manifest/lock mismatch may be caused by a stale lock, workspace inheritance, or another dependency path; the cause is not established.
- No decision was made here about keep/rebase/return, upstream contribution, or consumer migration. The actor-use standards are also outside this factual Git audit.

## Psyche context (not Git evidence)

The written psyche says: “I want to dedicate a flow to the actor question. Everything was done by previous flows that received little to no guidance on design in this respect. Distrust it all, including our fork.” It also says: “we are definitely using kameo actors in nexus. I just havent designed the standards of use.” These are design context, not evidence that settles the relationship or a migration decision.

## Sources

- Witness: `flows/fb50d4a5/witnesses/repositoryRelationship.md`
- Witness: `flows/fb50d4a5/witnesses/upstreamIdentity.md`
- Witness: `flows/fb50d4a5/witnesses/upstreamUniqueCommits.md`
- Witness: `flows/fb50d4a5/witnesses/forkApiArchitecture.md`
- Witness: `flows/fb50d4a5/witnesses/releaseTags.md`
- Witness: `flows/fb50d4a5/witnesses/consumerPins.md`
- `/git/github.com/LiGoldragon/kameo`
- `/git/github.com/LiGoldragon/kameo/Cargo.toml`
- `/git/github.com/LiGoldragon/kameo/src/actor/lifecycle.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/actor_ref.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/spawn.rs`
- `/git/github.com/LiGoldragon/kameo/src/links.rs`
- `/git/github.com/LiGoldragon/kameo/src/mailbox.rs`
- `/git/github.com/LiGoldragon/persona-spirit/Cargo.toml`
- `/git/github.com/LiGoldragon/persona-spirit/Cargo.lock`
- `/git/github.com/LiGoldragon/lojix/Cargo.toml`
- `/git/github.com/LiGoldragon/lojix/Cargo.lock`
- `psyche-raw/Vision/actorLibrary.md`
- https://github.com/LiGoldragon/kameo/compare/3486e4f63ea4e87123476cfbdefeb12403540306...b4aaee797cc3fd12e8194db406d9d73a6bc021ce
- https://github.com/tqwewe/kameo/releases
- https://github.com/LiGoldragon/kameo/releases
