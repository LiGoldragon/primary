# 126 — Lojix Engine Progress and Finish Plan

## Purpose

This report records where the new `lojix` daemon stands after the first
real build slice, what is already proven, what is still missing, and the
finish order I would use from here.

The branch is `horizon-re-engineering` in
`/home/li/wt/github.com/LiGoldragon/lojix/horizon-re-engineering`.
The tracked workspace bead is `primary-vhb6`.

## Current State

The new `lojix` repository now has the right outer shape:

- one Rust crate named `lojix`;
- `lojix-daemon` as the long-lived orchestrator binary;
- `lojix` as the thin CLI client;
- typed daemon and CLI configuration through `nota-config`;
- Unix-socket request/reply over `signal-core` frames carrying
  `signal-lojix` records;
- a Kameo `RuntimeRoot` that owns child actors instead of treating the
  daemon as a bag of helper functions.

The current deployed branch has these pushed commits in order:

- `76bf696c` — first daemon socket/runtime/client slice.
- `2f1506b5` — typed `nota-config` daemon/CLI configuration; no
  production socket-path environment control plane.
- `c826c733` — deploy-facing witnesses target the matching
  `horizon-re-engineering` branches.
- `978703b3` — build-only deployment actor pipeline.
- `78197649` — pin build outputs as GC roots.

`signal-lojix` on its matching branch has already moved to the current
`signal-core` streaming channel macro and owns the typed deployment,
generation, cache-retention, and observation vocabulary consumed here.

## What Works

The build-only deployment path is real enough to build a CriomOS system
closure for a real cluster node.

The path today is:

1. `lojix` sends one Nota `DeploymentSubmission` to `lojix-daemon`.
2. `RuntimeRoot` mints a deployment identifier and forwards to
   `DeploymentActor`.
3. `DeploymentActor` validates the request synchronously enough to
   reject unsupported modes before any tool runs.
4. A per-deployment `BuildJobActor` records `Submitted` and `Building`.
5. `BuildOnlyRequest` loads the Horizon proposal through
   `horizon-lib`, projects the requested cluster/node, and validates
   the plan against the projected view.
6. Generated flake inputs are materialized for:
   - `horizon`;
   - `system`;
   - `deployment` for full-OS / OS-only shape;
   - `secrets` when `secrets/*.sops` exists beside the proposal.
7. Generated inputs are hashed with `nix hash path`, staged to the
   selected remote builder over `ssh`/`rsync`, and used via
   `--override-input ... path:/...?...narHash=...`.
8. The selected builder runs remote `nix build --refresh --no-link
   --print-out-paths`.
9. `GarbageCollectionRoots` pins the realized store path under the
   configured root before success is reported.
10. `BuildJobActor` records `DeploymentBuilt`.

The current slice rejects these before external tools run:

- local builds;
- activation actions;
- eval actions;
- profile/switch/test/boot actions.

That is intentional. The build engine had to become real before the
copy/activation engine could be honest.

## Current GC-Root Shape

`RuntimeConfiguration` already carried a `gc_root_directory`; the latest
slice made that data live.

For realized build outputs, the current path is:

```text
<gc-root-directory>/<cluster>/<node>/<kind>/built/<deployment>
```

Example from the real smoke:

```text
/tmp/lojix-real-build-nxzl8X/gcroots/goldragon/zeus/full-os/built/deployment_1
  -> /nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66
```

This is a bootstrap retention slot, not the final cache-retention model.
The final architecture still wants sema-backed records plus slots such
as `current`, `boot-pending`, `rollback/<n>`, `pinned/<label>`, and
`recent/<timestamp>`.

## Verification

Rust inner-loop verification:

```sh
cargo test --jobs 1 -- --test-threads=1
cargo clippy --all-targets -- -D warnings
```

Nix witnesses, all run with low local parallelism:

```sh
nix build .#checks.x86_64-linux.test-build-pipeline --max-jobs 1 --cores 2
nix build .#checks.x86_64-linux.test --max-jobs 1 --cores 2
nix build .#checks.x86_64-linux.clippy --max-jobs 1 --cores 2
nix build .#checks.x86_64-linux.fmt --max-jobs 1 --cores 2
nix build .#checks.x86_64-linux.daemon-cli-integration --max-jobs 1 --cores 2
```

The Nix builds dispatched to Prometheus.

The real daemon/CLI smoke used:

- proposal:
  `/home/li/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering/datom.nota`
- flake:
  `github:LiGoldragon/CriomOS/horizon-re-engineering`
- target:
  `zeus`
- builder:
  `prometheus`
- plan:
  `(FullOsDeployment Build)`

It produced:

```text
(DeploymentBuilt deployment_1
  (RealizedStorePath "/nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66"))
```

and the GC-root symlink above.

## What Is Not Done

The current engine builds and roots real closures. It is not yet a full
replacement for `lojix-cli`.

Missing runtime planes:

- sema-backed deploy event log;
- live pushed observation streams;
- live generation set;
- sema-backed GC-root ledger;
- closure copy to the target;
- activation on the target;
- rollback behavior;
- cache-retention mutations;
- generation query backed by the live set;
- production service packaging and cutover from legacy `lojix-cli`.

Missing deeper tests:

- daemon restart reads sema state and preserves event history;
- subscriber receives live events without polling;
- generated build output becomes a `Generation` record;
- copy phase proves the target receives the intended closure;
- activation phase proves the target action ran and the generation
  became current;
- failure during activation leaves the previous current root intact;
- cache-retention pin/unpin/retire commits one typed transition and
  emits one observation.

## My Finish Order

### 1. Sema-backed event log

This should be next.

The in-memory `EventLogActor` is useful for the first slice, but every
later phase depends on durable event history. The event log should
become the first sema-backed actor because it is the audit spine: build,
copy, activation, rollback, cache-retention, and generation queries all
need to explain what happened.

The test should be chained:

1. start daemon;
2. submit a build-only deployment;
3. shut daemon down;
4. start daemon again over the same state directory;
5. query/subscribe and observe the old events.

The witness should consume the daemon through `lojix`, not by reading
private memory.

### 2. Live pushed observation streams

Current observation subscriptions return a snapshot. That is not the
final architecture. The next observation slice should connect event-log
append to `signal-core` stream delivery so subscribers see new
deployment events as they happen.

The test should open a subscription before submitting a deployment and
prove `Submitted`, `Building`, and `Built` arrive without polling the
daemon with repeated subscription requests.

### 3. Live generation set

After build events are durable and pushed, the build output should mint
a `Generation` record:

```text
Generation {
  generation,
  cluster,
  node,
  kind,
  store_path,
  state: Built,
}
```

`GenerationQuery` should read from the live generation set, not return
an empty list. This is the first point where `DeploymentBuilt` can be
connected to queryable deploy state.

### 4. GC-root ledger and retention slots

The current `built/<deployment>` symlink is the right bootstrap witness,
but it should be folded into the final retention vocabulary.

The durable model should say which generation owns which roots and why:

- built output retained for recent deploy history;
- current generation retained because it is active;
- boot-pending retained until reboot resolves it;
- rollback generations retained by policy;
- pinned labels retained by explicit operator request.

The actor should be `GarbageCollectionRoots`, backed by sema state and
filesystem symlinks. The filesystem remains the Nix retention mechanism;
sema is the daemon's truth for why each root exists.

### 5. Closure copy

Once a built generation exists, add a copy phase. The old `lojix-cli`
path and the system-specialist cluster-signing notes matter here:
cross-host deploys must prefer signed substitution from cache nodes,
not raw unsigned daemon-to-daemon transfers.

The copy phase should be a separate actor/concern, not code inside the
build actor. It should emit a typed event before it starts and after it
finishes. If `signal-lojix` lacks a success event for copy, the contract
should be extended rather than overloading `ActivationRunning`.

### 6. Activation

Activation should land after copy is observable.

The activation actor should support the typed actions already present
in `signal-lojix`:

- full OS: `Boot`, `Switch`, `Test`, `BootOnce`;
- OS-only analogues if still part of the contract;
- home: `Profile`, `Activate`;
- build/eval remain non-activating modes.

The first activation witness should target a disposable test node, not a
live workstation. The Prometheus sandbox/test-cluster infrastructure is
the right place to prove this.

### 7. Rollback

Rollback is not an afterthought. It is the behavior that makes
activation safe.

The test should force activation failure after copy and prove:

- failed generation does not become `current`;
- previous current root remains in place;
- failure event records the reason;
- query surface still reports the previous activated generation.

### 8. Cache retention

After roots and generations are durable, implement
`CacheRetentionRequest`.

This should use one sema commit per mutation and one pushed observation
per mutation. `PinGeneration`, `UnpinGeneration`, and
`RetireGeneration` should not read the filesystem as truth; they should
apply typed state transitions and then reconcile filesystem symlinks.

### 9. Production cutover

Only after build/copy/activation/rollback are proven in the test
cluster should CriomOS-home move the user-facing deploy command from
legacy `lojix-cli` to the new `lojix` daemon stack.

Cutover work includes:

- package/service wiring;
- socket path, group, and mode in the host profile;
- profile activation path for the CLI;
- retirement plan for legacy `lojix-cli`;
- operator docs and skills update.

## Shape Recommendation

Do not turn the current `deploy.rs` into a permanent large module.

The right next structural move is to split by actors once the event-log
and generation-set actors are being added:

```text
src/deploy/
  mod.rs
  event_log.rs
  garbage_collection_roots.rs
  deployment.rs
  build_job.rs
  build_request.rs
  generated_inputs.rs
  remote_inputs.rs
  nix_build.rs
```

The split should happen when it removes pressure from the next sema
slice, not as cosmetic churn. The current single-file shape was
acceptable to prove the first real build path; it should not become the
final structure.

## Design Risks

### Wire vocabulary may need one or two additions

`signal-lojix` currently has `ClosureCopying` but not obviously a
separate copy-success observation. If the activation pipeline needs
that state to be inspectable, add the typed record. Do not bury copy
success as a log line.

### Build-only roots are not final retention

`built/<deployment>` is a useful witness. It is not enough to implement
retention policy. The final cache-retention work should not preserve
this bootstrap path as a compatibility promise unless it becomes part of
the intended model.

### Generated secret input shape is only first-pass

The build path currently includes `secrets/*.sops` beside the proposal
when present. That is enough to keep the first real build path moving,
but the Horizon/ClaviFaber/SOPS design still needs the final typed
secret-binding shape to decide which secrets are projected for which
node and purpose.

### The real-build witness is build-only

The successful real smoke proves projection, generated inputs, remote
builder staging, remote Nix build, and GC-root pinning. It does not
prove copy or activation. Those must be tested in a disposable
environment before any live switch path is trusted.

## Bottom Line

The project has crossed the important threshold: `lojix-daemon` is no
longer just a socket skeleton. It builds a real CriomOS system closure
through the new Horizon branch, through the typed CLI/daemon boundary,
on a real remote builder, and pins the result.

The next threshold is durability. I would finish the daemon from the
inside out: event log, live streams, live generation set, GC-root
ledger, then copy and activation. That keeps every new effect
observable and recoverable before adding the next one.
