# Handover — Whole-Engine Testing Readiness & the Synchronizer (2026-07-02)

Focus-scoped freshness aid for a session continuing the whole-engine
testing/operation work. Read `reports/field-readiness/02-kink-ledger.md` first,
then this.

## Focus

Bring the whole persona/criome engine to the point of continual assembly
testing and entering operation — get the field ready for a sustained session
that fits every component together and tests them together, especially by
running VM clusters on the high-capacity host. Find and clear the kinks that
would stall that session mid-flow.

## Settled psyche direction

- Continually test the complete assembly and enter operation of the whole
  engine; prepare the field so a sustained fitting-and-testing session is not
  blocked by broken tooling. VM-cluster testing on the high-capacity host is the
  main event.
- `prometheus` is the sole builder, permanently, and that is correct — no other
  host is suitable and no second/backup builder is wanted. Single-host
  concentration is an accepted condition, not a defect to fix.
- Builds run on the remote builder only; no local builds.
- Mechanical cross-repo version propagation belongs in a tool, not repeated by
  hand. Hence the `synchronizer` (design below).
- The `synchronizer` must be universal: no project-specific logic in the tool,
  so any project can use it in their own repos. Criome specifics live only in
  the runtime config, never the code.

## Confirmed facts (current state)

Field readiness — verdict READY-WITH-KINKS (ledger `02-kink-ledger.md`, evidence
`10`–`13`, 17 beads under label `field-readiness`):

- `prometheus` (16c/32t Ryzen AI Max+ 395, 124 GiB RAM, ~900 GB free, KVM +
  nixos-test) boots real KVM VMs; a two-VM test running real engine daemons
  (spirit, criome×2, persona-router, mirror) passed green with clean teardown —
  witnessed, not hearsay.
- Tooling field healthy: jj, nix, spirit, orchestrate, beads, and the test
  harness respond fast; remote builder and cache are hot.
- The whole engine builds from clean through the remote builder.
- The minimal runnable whole comes up and exchanges real origin-stamped mail
  after each repo is rebuilt against its own lock.
- 22 `NotBuiltYet`/stub operations (the unfinished federation surface) are
  enumerated and path-cited in `12-run-and-assembly.md`.
- No continuous-testing entry point exists yet — no CI, no timers.

Whole-engine gate:

- The gate (`persona-dev-stack` + the `persona-daemon-launches-nix-built-*`
  topology checks) was dead at instantiation on a stale fenix pin; now revived
  and building green. Commit `bbb7f070` on persona `main`; independently audited
  PASS. Bead `primary-j5j2` closed.
- The gate now fails one layer deeper, at runtime, on a router/message
  wire-skew (router config-decode) — bead `primary-w46v`. This is the current
  live blocker to the checks passing.

Synchronizer:

- Built and independently audited green, local only. Repo
  `/git/github.com/LiGoldragon/synchronizer`, commit `a8c95728`; all checks
  green, 41 tests plus a stateful on-builder Nix-resolution probe. No remote
  exists; by construction the tool can only ever write a `synchronizer` branch
  on a component remote.
- It has NOT been run against any live repo. Its effect on the real `w46v` skew
  is unproven until the first run.

## Synchronizer — locked design (for pickup)

- Purpose: cascade version bumps up the component dependency tree so wire
  contracts stay aligned when a low dependency's `main` advances.
- Rust; NOTA config in, NOTA report out; real typed serde throughout.
- Manages both Cargo pins (typed TOML, format-preserving edits that keep
  comments) and flake pins (typed `flake.lock` JSON; `nix` is shelled to only to
  prefetch the narHash).
- Topology discovered from the manifests; edges matched by repository identity
  from the git URL, never the Cargo package name.
- Cascade version source: latest pushed `main` tip for bottom deps and deps
  whose own deps did not move this run; the producer's `synchronizer`-branch tip
  for anything bumped this run. The flake input's `original` ref is preserved
  (pointing it at the `synchronizer` branch backfires — Nix re-locks to `main`
  and evaluates old content).
- Action: edit, commit, and force-push to a dedicated `synchronizer` branch per
  repo — never `main`.
- Verify at each step: run the wire-exercising flake checks (the ones that build
  and launch daemons) where a repo has them, else a default build; the builder
  host is resolved from a CriomOS role, with no hostname in the code.
- On a failed verify: keep going, collect all failures, report them together.
  The NOTA report records which verify gate ran (wire-checks vs default build).
- Universality (requested, NOT yet done): move builder-host resolution behind a
  generic strategy with the CriomOS cluster-datom resolver as one optional
  plugin; make the commit author configurable; keep the forge abstract (GitHub
  the sole current implementation). The tool must carry zero project data.

## Open questions and live uncertainties

- Synchronizer, pending psyche: create the GitHub remote (confirm intended
  visibility) and make the first live run against `w46v`. A run pushes only
  `synchronizer` branches; the NOTA report is meant to be reviewed before any
  merge to `main`.
- Sequencing undecided: generalize the tool to universal first, or run the
  `w46v` fix first and generalize afterward.
- `w46v` (router/message wire-skew) is the live blocker on the gate passing; the
  synchronizer is the intended durable fix, unproven until its first run.
- The 14 cheap-fix-now items in the ledger are not applied — the psyche wants to
  review the fix designs before any land.
- Five open decisions recorded in the ledger, unanswered: nixos-test remote
  scheduling from ouranos; a dirty 8-file spirit checkout on
  criome-authorization-push; cleanup of the Jun 30–Jul 1 demo daemons/sandboxes;
  GitHub as a hard VM-inner-loop dependency vs sanctioning `nix copy`; complete
  vs retire the declared persistent-VM guest.
- Suspected follow-ups: the `prometheus` ssh `HostName` was patched locally in
  `~/.ssh/config` and likely belongs in criomos-home declaratively; bead
  `primary-oeng` (single-builder concern) should be retired, since sole-builder
  is an accepted condition.
- Documented synchronizer limitation: a normal `[dependencies]` +
  `[dev-dependencies]` dual-pin of the same package is currently refused loud;
  relevant once such a producer joins a configured set.

## Pointers

- `reports/field-readiness/00-README.md`, `02-kink-ledger.md`, `10`–`13`-*.md
- `/git/github.com/LiGoldragon/synchronizer/ARCHITECTURE.md` and the repo
- Beads: label `field-readiness` (incl. `w46v`; `j5j2` closed; `oeng`, `mddx`,
  `95fm`, `vp6d`, others open)
- Commits: `4a5923dda079` (ledger), `bbb7f070` (persona fenix fix), `a8c95728`
  (synchronizer, local)
