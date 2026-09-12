# Remote-only builds: system max-jobs=0 for goldragon

Subflow of main flow `f6db8d`, 2026-09-12. Brief: the living's stated
intent is that no Nix build ever runs on this machine (goldragon) again —
Prometheus builds everything. Find the CriomOS module that writes
`/etc/nix/nix.conf` and `/etc/nix/machines` for this host, and on a test
branch set the system `max-jobs = 0` for goldragon so local building is
impossible for every user, keep `builders-use-substitutes`, decide
`trusted-users`, evaluate before/after, push without landing.

Marks: **witnessed** — this thread ran the command and the text below is
what came back; **relayed** — a named file or prior report, not
independently re-verified; **this thread's inference** — reasoning, not a
ruling.

## Why this was needed

**Relayed**, `flows/f6db8d/log.md` (lines ~110–114): the living killed
every local nix client by PID and set `max-jobs = 0` in `li`'s
`~/.config/nix/nix.conf`, but whether the nix daemon actually honors a
non-trusted user's client-side override was left unknown — `li` is not in
`trusted-users`, and the log records that a system-level `max-jobs = 0`
(CriomOS module) was the proposed fix for exactly this gap. This thread
implements that proposal.

## The module

**Witnessed**: `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nix/client.nix`
is the module that assembles `nix.settings` (`trusted-users`, `cores`,
`max-jobs`, `substituters`, …) and `nix.extraOptions`, which NixOS renders
into `/etc/nix/nix.conf` for every host built from this flake — goldragon
included. The companion `modules/nixos/nix/builder.nix` sets
`builders-use-substitutes` (keyed off `isDispatcher`, untouched here) and
writes `/etc/nix/machines` via `nix.buildMachines` for hosts that dispatch
to remote builders. Per-host shape (whether a node is a dedicated builder,
an edge builder, or a plain client like goldragon) comes from the
`horizon.node` projection, supplied per-deploy — not hardcoded per hostname
in this repo — so there is no goldragon-named file to edit; the fix has to
live in the shared module's branching logic.

Before this change, `client.nix` had:
```nix
dedicatedNixBuilder = (node.isRemoteNixBuilder or false) && (node.behavesAs.center or false);
localMaxJobs = if dedicatedNixBuilder then (node.maxJobs or 4) else 1;
```
Every non-dedicated-builder host — goldragon among them — got exactly one
local build slot (`max-jobs = 1`), enough for the daemon (root) to still
run a build locally regardless of what `li`'s own `nix.conf` said.

## The change

**Witnessed**, this thread edited
`modules/nixos/nix/client.nix`:
```nix
localMaxJobs =
  if dedicatedNixBuilder then
    (node.maxJobs or 4)
  else if (node.isRemoteNixBuilder or false) then
    1
  else
    0;
```
A node with no builder role at all (goldragon's shape: `isRemoteNixBuilder
= false`) now gets `max-jobs = 0` — no local build slot for any user,
root included, since this is a *system* setting the daemon reads from its
own environment rather than a per-user override the daemon may or may not
trust. A node that still serves `sshServe` builds for a dispatcher
(`isRemoteNixBuilder = true` but not the cluster center — an "edge
builder") keeps its prior single slot, since zeroing it would silently
break its ability to build what dispatchers route to it. `dedicatedNixBuilder`
hosts (e.g. Prometheus) are unaffected, still using `node.maxJobs`.

`builders-use-substitutes` (in `builder.nix`) was left untouched, as
instructed — it is keyed off `isDispatcher`, a separate axis from the
`max-jobs` branch touched here, and nothing in this task changes whether
goldragon is a dispatcher.

**`checks/nix-role-policy/default.nix`** was updated to match: its
`baseNode` fixture (`behavesAs.center = false`, `isRemoteNixBuilder =
false` — the same shape as goldragon) now asserts `max-jobs = 0` instead
of `1`. Its `edgeBuilderNode` fixture (`isRemoteNixBuilder = true`,
`behavesAs.center = false`) and `serviceNode`/dedicated-builder fixture
were left asserting their prior values (`1` and `4`) and needed no edit —
both still pass, confirmed by the build below.

## Trusted-users decision: leave `li` out

**This thread's decision, with reasoning**: `trusted-users` stays
`["root" "@nixdev"]`; `li` was **not** added.

Two reasons:

1. **Not needed for Prometheus.** Per
   `flows/f6db8d/reports/prometheus-builder.md` (relayed), the nix daemon's
   SSH connection to Prometheus runs as `root`, authenticating as
   `nix-ssh` using **the host's own SSH host key**
   (`/etc/ssh/ssh_host_ed25519_key`), with Prometheus's public host key
   inlined in the `/etc/nix/machines` line. The identity the remote
   builder trusts is the machine, not any particular local user — `li`
   being in `trusted-users` contributes nothing to that path working.
2. **Actively counterproductive for this task's goal.** `trusted-users`
   membership is what lets a user's own `nix.conf` or command-line
   `--option` override settings the daemon would otherwise not honor
   from an untrusted account. The entire point of moving `max-jobs = 0`
   into this system module is to make it not depend on whether `li`'s
   personal override is honored. Adding `li` to `trusted-users` would
   hand `li` exactly the power to raise `max-jobs` back above 0 from
   `~/.config/nix/nix.conf`, defeating "impossible for every user."

## Evaluation: before / after

**Witnessed**, `nix eval --max-jobs 0 --impure --json`, evaluating
`modules/nixos/nix/client.nix` + `modules/nixos/nix/default.nix` under a
`horizon.node` fixture shaped like goldragon (`isRemoteNixBuilder =
false`, `behavesAs.center = false`) via `lib.nixosSystem`, reading back
`config.nix.settings` and `config.nix.extraOptions`, rendered as
`nix.conf`-shaped key=value text (`lib.generators.toKeyValue`).

**Before** (git blob `acc3feab4d99492276a353a80bbccffac9d6fb58`'s
`client.nix`, temporarily swapped in for this eval only, then restored):
```
max-jobs=1
builders-use-substitutes=false
trusted-users=root
trusted-users=root
trusted-users=@nixdev
cores=2
```

**After** (this branch's `client.nix`):
```
max-jobs=0
builders-use-substitutes=false
trusted-users=root
trusted-users=root
trusted-users=@nixdev
cores=2
```

Only `max-jobs` changed, `0` vs `1`; `builders-use-substitutes` and
`trusted-users` are identical in both (the duplicate `root` line is
NixOS's own module default plus this module's explicit `"root"` entry,
present before this change and unrelated to it). Full settings text
(after):
```
allowed-users=@users
allowed-users=nix-serve
auto-optimise-store=true
builders=null
builders-use-substitutes=false
connect-timeout=5
cores=2
fallback=true
max-jobs=0
require-sigs=true
sandbox=true
sandbox-fallback=false
substituters=https://cache.nixos.org/
system-features=nixos-test
system-features=benchmark
system-features=big-parallel
system-features=kvm
trusted-public-keys=cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
trusted-public-keys=cache.example:CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
trusted-users=root
trusted-users=root
trusted-users=@nixdev
```
(`builders=null` and the `cache.example` key are eval-fixture artifacts —
this test node has no real `horizon.cluster`/builder data supplied, unlike
a live deploy where `/etc/nix/machines` and `trusted-public-keys` carry
Prometheus's real entries per `reports/prometheus-builder.md`.)

`nix.extraOptions` (unaffected by this change, shown for completeness):
```
keep-derivations = false
keep-outputs = false

flake-registry = /nix/store/abbwy0wsrn98licr149lk5vga0m01grp-criomos-flake-registry.json
experimental-features = nix-command flakes recursive-nix

# !include <path>: include without an error for missing file.
!include nixTokens
```

**Witnessed**, `nix build --max-jobs 0 -L` of `checks/nix-role-policy`
against this branch (built on Prometheus — the log lines show
`building '...' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` for
both derivations): exit 0. This is the module's own fixture-based
regression check (`baseNode`/`edgeBuilderNode`/`serviceNode` shapes),
confirming the updated `max-jobs = 0` assertion for the goldragon-shaped
`baseNode` fixture, and that the edge-builder and dedicated-builder
fixtures are unaffected.

Direct evaluation of `.#checks.x86_64-linux.nix-role-policy` through the
top-level flake failed (`CriomOS: no system input was provided` — the
flake's `system`/`horizon`/`deployment` inputs are stubs by default,
normally supplied by the `lojix` deploy-materialization tool per the
flake's own error text); the check was instead built directly by
importing `checks/nix-role-policy/default.nix` with `pkgs`/`inputs`
supplied from the flake's locked `nixpkgs`, bypassing the stub inputs.
This is the same fixture the check itself would run under a real deploy
materialization — nothing about the check's own logic was changed to make
it pass.

## What deploying this changes, and what "Prometheus unreachable" then means

**This thread's inference, stated as the landing note the brief asked
for**: deploying this branch to goldragon changes `/etc/nix/nix.conf`'s
`max-jobs` from `1` to `0`. Concretely:

- Every `nix build`/`nix-store --realise` invocation on goldragon that
  would otherwise run a derivation locally — by any user, `li` or
  `root`, trusted or not, with or without an explicit `--max-jobs` flag —
  is refused with Nix's own `local builds are disabled (max-jobs = 0)`
  error (witnessed, verbatim, in `reports/prometheus-builder.md`'s
  reproduction) **unless** the derivation can be dispatched to a
  configured remote builder (Prometheus, via the unrelated,
  already-correct `/etc/nix/machines` entry that `builder.nix` writes on
  dispatcher hosts) or fetched pre-built from a substituter.
- **If Prometheus is unreachable when this is deployed, no build runs at
  all on goldragon** — not a slower local fallback, not a degraded mode.
  `fallback = true` in this same settings block governs *substituter*
  fallback (falling back to building from source when a binary substitute
  can't be fetched), not builder fallback; it does not let a
  remote-builder failure fall back to a local build once local build
  slots are zero. This is the exact scenario the brief names as the
  living's stated intent: a machine with `max-jobs = 0` cannot build
  anything of its own accord, ever, so if Prometheus is down, goldragon
  simply cannot build until it's back — no build is safer than a stray
  local one.
- This does not change eval (`nix eval`, `nix flake check`'s evaluation
  phase, `nix flake metadata`) — those already run locally regardless of
  `max-jobs`, matching the running convention in this flow (`--max-jobs 0`
  prefixed to every nix invocation, which only affects the *build* phase).
- `trusted-users` and `builders-use-substitutes` are unchanged by this
  deploy — see above for why.

## Not landed

This is a test branch (`f6db8d-remote-only-builds`) pushed to
`git@github.com:LiGoldragon/CriomOS`, not merged to `main`. **Witnessed**,
`git ls-remote https://github.com/LiGoldragon/CriomOS.git
f6db8d-remote-only-builds` → `dbf2daaf4f5a2505f9740f5ee146d123c27a9eef
refs/heads/f6db8d-remote-only-builds`, confirmed against the real remote
URL (not merely the checkout's `origin`, which points at the same
`ssh://git@github.com/LiGoldragon/CriomOS` here but was checked
independently per the file-editing skill). No deploy was run and no
CriomOS/CriomOS-home `main` was touched.

## Lock

Took Orchestrate lock 1334 (`RemoteOnlyBuildsNixModule`, `f6db8d`) on
`modules/nixos/nix/client.nix`, `modules/nixos/nix/builder.nix`, and
`checks/nix-role-policy/default.nix` before editing (a sibling f6db8d
subflow held lock 1227 on `CriomOS/flake.nix`, `flake.lock`,
`modules/nixos/lojix.nix`, `checks/lojix-ownership/default.nix` for the
lojix landing — disjoint paths, no wait needed). Released on completion
(`Release.1334` → `Released`).

## Sources

- **Witnessed**, this thread, 2026-09-12: `cat modules/nixos/nix/client.nix`
  and `builder.nix`; `cat checks/nix-role-policy/default.nix`; the edit
  itself; `nix eval --max-jobs 0 --impure --json --file …` against both
  the pre-edit (`git show
  acc3feab4d99492276a353a80bbccffac9d6fb58:modules/nixos/nix/client.nix`)
  and post-edit module; `nix build --max-jobs 0 -L --impure --file …`
  importing `checks/nix-role-policy/default.nix` directly (exit 0, built
  on `ssh-ng://nix-ssh@prometheus.goldragon.criome`); `jj commit`, `jj
  bookmark set f6db8d-remote-only-builds`, `jj git push --bookmark
  f6db8d-remote-only-builds`; `git ls-remote
  https://github.com/LiGoldragon/CriomOS.git f6db8d-remote-only-builds`;
  `orchestrate 'Lock.{…}'` / `'Release.1334'`; `orchestrate
  'Observe.Locks'` (checked for conflicting locks before acquiring).
- **Relayed**: `flows/f6db8d/log.md` lines ~108–114 (the living's
  corrections and the kill pass); `flows/f6db8d/reports/prometheus-builder.md`
  (root's SSH identity to Prometheus, the `local builds are disabled
  (max-jobs = 0)` error text, `/etc/nix/machines`'s existing correctness).
