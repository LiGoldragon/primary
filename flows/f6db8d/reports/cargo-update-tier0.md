# Tier 0 item 1 — lockfile-only `cargo update`, eleven month-stale repositories

Subflow of main flow f6db8d, executing Tier 0 item 1 of
`reports/dependency-survey.md` §6: "`cargo update` (lockfile-only, no
manifest edit) in the 11 month-stale repositories" — message, aggregator,
agent, listener, harness, mirror, spirit, router, repository-ledger,
clavifaber, terminal-cell. **spirit and mirror were skipped** per this
flow's brief: deprecated, and the survey's "What must not be done
unattended" section names spirit explicitly. Everything below is
witnessed by this flow on this host at 2026-09-11 unless marked relayed.

Method per repository, in the order executed: acquire an Orchestrate
lock on the repository path; if the working tree held uncommitted
changes, commit them first as their own commit (per `file-editing` and
`NON_MANAGEMENT_AGENTS.md`) and land that on main before starting; work
on a test bookmark `f6db8d-cargo-update` from main; run `cargo update`
(no manifest edit); if it produced a lockfile diff, run the gate
(`cargo test`, `cargo fmt --check`, `cargo clippy --all-targets -- -D
warnings`, `nix flake check -L --builders ''`, all local, no remote
builders); land on green, leave the pushed test branch and record the
failure on red or on an update that aborts before writing a lockfile
change; release the lock.

**Versioning reading**: the `versioning` skill updates "the version
surface changed by public behavior, wire, storage, package, or
deployment changes." A lockfile-only refresh of transitive dependency
patch/minor versions within already-declared manifest ranges changes
none of those — no manifest edit, no public API, no wire format, no
on-disk format. No repository's own package version was bumped for a
lockfile-only landing in this report.

## Outcome by repository

### message — landed

- Dirty tree found: a tracked, deleted `result` build symlink. Committed
  separately: `chore: commit build symlink removal found in tree`.
- Revisions: main before this flow touched it `bf7295641bb2` → after the
  found-in-tree commit `eddd02ed8477` → after the landed cargo update
  `dee8f271b67f`.
- Crate diff (patch/minor, all within declared ranges): rkyv
  0.8.16→0.8.18, tokio 1.52.3→1.53.1, serde/serde_core/serde_derive
  1.0.228→1.0.229, thiserror 2.0.18→2.0.20, uuid 1.23.2→1.26.1, blake3,
  bytecheck, rancor, libc 0.2.186→0.2.189, indexmap 2.14.0→2.14.2,
  futures 0.3.32→0.3.34 (family), wasm-bindgen family, mio, memchr,
  socket2, tinyvec, quote/proc-macro2/rustversion; syn 2.0.117 replaced
  by syn 2.0.119 alongside the pre-existing syn 3.0.5 (transitive,
  matches the survey's noted mid-transition); several no-longer-needed
  transitive crates removed (itoa, log, semver, serde_json, wasip2/3,
  wit-* family, zmij as a direct pin).
- Gate: `cargo fmt --check` clean; `cargo clippy --all-targets -- -D
  warnings` clean; `cargo test --all` — all suites passed (unit +
  `contract_convergence`, `delivery`, `dependency_surface`,
  `message_store`, `process_boundary`, `pty_end_to_end`,
  `store_migration`); `nix flake check -L --builders ''` — `message-test`
  built and ran `cargo test --release --locked --all-targets
  --no-default-features` inside the sandbox, "all checks passed!".
- Landed on main at `dee8f271b67f`, pushed, test bookmark deleted
  (never pushed remotely — unneeded once green).

### aggregator — FAILED, not landed

- No dirty tree.
- `cargo update` aborts immediately, before writing any lockfile change:
  ```
  error: no matching package named `nota` found
  location searched: Git repository https://github.com/LiGoldragon/nota-next.git?branch=main
  required by package `aggregator v0.3.1 (/git/github.com/LiGoldragon/aggregator)`
  ```
- Cause: aggregator pins `nota` via a mutable `branch = "main"`
  dependency (`Cargo.toml:35`, `nota = { package = "nota", git =
  ".../nota-next.git", branch = "main" }`) whose producer's `main` HEAD
  no longer defines a package named `nota`. This matches the survey's
  §3.4 finding on the estate's 205 mutable pins resolving to producers
  that have moved out from under them.
- Cargo.lock confirmed byte-identical before and after the failed
  attempt (`diff` empty).
- Main untouched, still at `f777eb2a6e92`. Test branch
  `f6db8d-cargo-update` (an empty commit describing the failure) pushed
  at `7ef8d506e139`, left in place per brief.

### agent — landed

- No dirty tree.
- Revisions: main before `9f32646e62e8` → after the landed cargo update
  `df5f5bfdd3ee`.
- Crate diff: rkyv 0.8.16→0.8.18, tokio 1.52.3→1.53.1, serde family
  1.0.228→1.0.229, thiserror 2.0.18→2.0.20, rustls 0.23.41→0.23.44 (+
  rustls-pki-types, rustls-webpki), uuid 1.23.3→1.26.1, quinn-udp,
  smallvec, web-sys/wasm-bindgen family, zerovec/zerotrie/tinystr (icu),
  syn 2.0.118 replaced by 2.0.119 alongside pre-existing syn 3.0.5.
  Notably `rand` moved 0.9.4→0.10.2 — checked: **not a direct dependency**
  of agent's `Cargo.toml` (`grep` empty), purely transitive, so this is
  not a manifest-crossing edit; confirmed harmless by the gate. Several
  now-unused transitive crates removed (windows-* family, wit-bindgen,
  zerocopy, r-efi, rand_chacha 0.9).
- Gate: fmt clean; clippy clean; `cargo test --all` — all suites passed
  (`configuration_writer`, `fixture_round_trip` including the live
  DeepSeek/OpenAI-compatible provider fixtures, run offline); `nix flake
  check -L --builders ''` — `agent-test` ran `cargo test --release
  --locked --all-targets --no-default-features`, 13 tests total, "all
  checks passed!".
- Landed on main at `df5f5bfdd3ee`, pushed, test bookmark deleted.

### listener — FAILED, not landed (found-in-tree commit landed separately)

- Dirty tree found: `.beads/issues.jsonl` addition, one line, sitting on
  a `bd init: initialize beads issue tracking` commit that was itself a
  direct child of main. Committed the dirty addition
  (`bd: record beads issue tracking state found in tree`) and fast-
  forwarded main through both: `6905a4f11509` → `471b0d598f4e`, pushed.
- `cargo update` aborts before writing any lockfile change:
  ```
  error: no matching package named `nota` found
  location searched: Git repository https://github.com/LiGoldragon/nota.git?branch=main
  required by package `listener v0.14.0 (/git/github.com/LiGoldragon/listener)`
  ```
- Cause: listener pins `nota` via a mutable `branch = "main"` dependency
  (`Cargo.toml:45`, feature `nota-text`) whose producer HEAD no longer
  defines package `nota`. Cargo.lock confirmed unchanged.
- Test branch `f6db8d-cargo-update` pushed at `04137484445b`, describing
  the failure, left in place.

### harness — FAILED, not landed (stale formatting fix landed as a no-op)

- Dirty tree found: reformatting-only diffs (line-wrap changes, "No
  syntactic changes" per `jj diff`'s Rust-aware view) in `src/launch.rs`,
  `tests/launch.rs`, `tests/message_router_harness_pi_steer_e2e.rs`,
  based on a `main` commit (`d6f2b6f4aec1`) three commits behind the
  actual current main (`722b68b3579b`). Committed the reflow separately,
  then rebased it onto the current main tip: the rebase landed as an
  **empty diff** — main's own later commits had already touched and
  reformatted the same lines — so `29c79561fadf` (main's new tip) is a
  content-identical, empty commit on top of `722b68b3579b`. Pushed.
- `cargo update`, run against the correct current main base, fails:
  ```
  error: no matching package named `nota` found
  location searched: Git repository https://github.com/LiGoldragon/nota.git?branch=main
  required by package `harness v0.3.4 (/git/github.com/LiGoldragon/harness)`
  ```
  Cargo pre-writes a large partial re-resolution before hitting this
  error (adding `datom-codec`, `ethos-zero`, bumping `protos`,
  `signal-terminal`, replacing bare `syn` with `syn 2.0.118`) — this
  flow caught that partial write via a Cargo.lock byte comparison,
  discarded it, and restored the file to main's exact committed content
  before describing the failure, so the pushed test branch carries **no**
  lockfile diff.
- Cause: harness pins `nota` via a mutable `branch = "main"` dependency
  (`Cargo.toml:56`) whose producer HEAD no longer defines package
  `nota`.
- **Method note for future runs**: capture the `Cargo.lock` "before"
  snapshot only *after* `jj new main` has actually checked out main's
  content — taking it beforehand can capture a stale pre-rebase working
  copy, as happened here on the first pass, and produces a false
  "cargo update partially succeeded" reading.
- Test branch `f6db8d-cargo-update` pushed at `d28634c26cd5`
  (superseding an earlier, incorrectly-described push at `866dafc62c84`
  that still carried the discarded partial lockfile; the corrected push
  moved the bookmark sideways to the clean revision), left in place.

### router — FAILED, not landed

- No dirty tree.
- `cargo update` aborts before writing any lockfile change:
  ```
  error: no matching package named `nota` found
  location searched: Git repository https://github.com/LiGoldragon/nota.git?branch=main
  required by package `router v0.11.0 (/git/github.com/LiGoldragon/router)`
  ```
- Cause: router pins `nota` via a mutable `branch = "main"` dependency
  (`Cargo.toml:58`) whose producer HEAD no longer defines package
  `nota`. Cargo.lock confirmed unchanged.
- Main untouched, still at `f60d4e33d0d0`. Test branch
  `f6db8d-cargo-update` pushed at `f15220b0d4bc`, left in place.

### repository-ledger — FAILED, not landed

- No dirty *working-copy* changes, but local `main` (`0580eff46139`,
  "docs: restore Protos estate status") and `main@origin`
  (`4153fd848c69`, "docs: integrate Protos estate status") have
  **diverged** — sibling one-line doc-marker commits, 6 commits
  local-ahead / 1 commit origin-ahead of their common ancestor. This
  flow did not attempt to resolve that divergence (out of Tier 0
  lockfile scope) and based its work on `main@origin`, the pushed
  authority, leaving the local-only divergent commit untouched.
- `cargo update` aborts before writing any lockfile change:
  ```
  error: no matching package named `nota` found
  location searched: Git repository https://github.com/LiGoldragon/nota.git?branch=main
  required by package `repository-ledger v0.4.1 (/git/github.com/LiGoldragon/repository-ledger)`
  ```
- Cause: repository-ledger pins `nota` via a mutable `branch = "main"`
  dependency (`Cargo.toml:35`, aliased `nota-next`) whose producer HEAD
  no longer defines package `nota`. Cargo.lock confirmed unchanged.
- Test branch `f6db8d-cargo-update` (based on `main@origin`) pushed at
  `0c9bd81bde7b`, left in place. The local/origin `main` divergence is
  flagged here for the main flow's attention; it is unrelated to this
  item's cargo-update work.

### clavifaber — landed

- Dirty tree found: a tracked, deleted `result` build symlink, on a
  working-copy parent three commits behind main. Committed separately,
  rebased cleanly onto main (`d0488014bf93` → `e805120075ae`
  attempted), then **origin's `main` moved during this flow's work** to
  `2203f677d344` (a sibling commit pushed by another agent while this
  flow held the Orchestrate lock on the same path — likely a push
  admitted just before the lock was acquired, since `Locked` was
  returned cleanly) — the initial push was rejected
  (`refs/heads/main ... reason: stale info`). Fetched, confirmed the
  found-in-tree fix and the new origin tip shared a common ancestor and
  neither was an ancestor of the other, rebased the found-in-tree fix
  onto the new `main@origin` tip (`e805120075ae`), and pushed
  successfully.
- Revisions: main before this flow touched it `d0488014bf93` → after
  origin's concurrent push `2203f677d344` → after the rebased
  found-in-tree fix `e805120075ae` → after the landed cargo update
  `2aaf293f4533`.
- Crate diff: futures family 0.3.32→0.3.34, tokio 1.52.3→1.53.1, serde
  family 1.0.228→1.0.229, thiserror 2.0.18→2.0.20, libc, memchr,
  zerocopy 0.8.48→0.8.57, zeroize 1.8.2→1.9.0, rand **0.8.6→0.8.8**
  (stayed within the declared `0.8` range — clavifaber is one of the two
  repositories the survey named still on rand 0.8.x; this update did
  not cross to 0.9/0.10), serde_json 1.0.149→1.0.151, syn 2.0.117
  replaced by 2.0.119 alongside pre-existing syn 3.0.5. The mutable
  kameo fork pin (`branch = "main"`) advanced from commit `f491b45d` to
  the branch's current head `3486e4f6`; the resolved package version
  stayed `0.20.0`. No manifest edit — `Cargo.toml` still reads `branch =
  "main"` before and after.
- Gate: fmt clean; clippy clean (full dependency tree rebuilt cleanly
  including the moved kameo fork revision); `cargo test --all` — all
  suites passed (`actor_topology`, `actor_trace`,
  `certificate_validity_window`, `forbidden_edges`,
  `issuance_idempotency`, `publication_writing`, `request_surface`);
  `nix flake check -L --builders ''` — `clavifaber-test` ran the release
  test suite in the sandbox, "all checks passed!".
- Re-fetched immediately before landing to confirm no further remote
  movement; none found. Landed on main at `2aaf293f4533`, pushed, test
  bookmark deleted.

### terminal-cell — BLOCKED, not attempted

- Orchestrate `Lock` request rejected:
  ```
  LockRejected.PathOverlap.{ /git/github.com/LiGoldragon/terminal-cell
    { 1124 F6db8dRemovalsTerminalCell f6db8d
      [ terminal-cell/Cargo.toml, terminal/Cargo.toml, mentci/Cargo.toml ]
      "Remove dead-code dotos-text feature flag" } }
  ```
  A sibling subflow of this same main flow (f6db8d) holds an active
  lock on `terminal-cell/Cargo.toml` (and two other repositories'
  manifests) for an unrelated manifest edit. Per the `edit-coordination`
  skill: "On `LockRejected` or a client failure, report the failure and
  do not edit" — no narrower lock request, worktree request, or other
  workaround was attempted; the working tree was never touched, and
  terminal-cell's dirty `result-1`…`result-7` build symlinks (present at
  the start of this flow's survey pass) were left exactly as found.
- terminal-cell's cargo update remains outstanding for a future attempt
  once lock 1124 is released.

## Summary of the mutable-pin finding

Five of the nine attempted repositories — aggregator, listener, harness,
router, repository-ledger — fail `cargo update` outright and identically
on the same root cause: each pins a package literally named `nota` from
a mutable `branch = "main"` git dependency (`nota.git` or
`nota-next.git`), and that branch's current HEAD no longer defines a
package by that name. This is not a Tier 0-scope fix — the survey's
Tier 3 item 12 ("The 205 mutable `branch = "main"` pins... Converting
them to immutable revs is the precondition for ever surveying this
estate cheaply again") is the exact fix this exposes, and it now blocks
five of eleven Tier 0 lockfile refreshes outright, not just the "unknown
resolution" the survey described. Only message, agent, and clavifaber —
the three repositories without a `nota` pin among the eleven surveyed —
completed successfully.

## Sources

- Witnessed on this host, 2026-09-11: `jj status`, `jj diff`, `jj log`,
  `jj commit`, `jj new`, `jj rebase`, `jj bookmark`, `jj git fetch`,
  `jj git push`, `cargo update`, `cargo fmt --check`, `cargo clippy
  --all-targets -- -D warnings`, `cargo test --all`, `nix flake check -L
  --builders ''`, in each of
  `/git/github.com/LiGoldragon/{message,aggregator,agent,listener,harness,router,repository-ledger,clavifaber}`.
  `Cargo.lock` diffs taken directly against `cp`-saved snapshots (with
  the harness correction noted above).
- Witnessed: `orchestrate 'Lock...'`, `orchestrate 'Release...'`, and
  `orchestrate 'Observe.Locks'` for every repository, including the
  `LockRejected.PathOverlap` on terminal-cell.
- Read: `/home/li/primary/flows/f6db8d/reports/dependency-survey.md`
  §1.3, §3.4, and §6 Tier 0 item 1 and Tier 3 item 12, for the surveyed
  scope, the mutable-pin count, and the ordering rule.
- Skills loaded and applied: `subflow`, `spirit`, `behavior`,
  `orchestrate`, `file-editing`, `testing`, `nix-workflow`, `versioning`,
  `flow-evidence`, `psyche`, `edit-coordination`.
