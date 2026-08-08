# Spirit-next deployment configuration audit — 2026-06-02

Role: system-designer sub-agent (orchestrator: report 53).
Frame: `reports/system-designer/53-spirit-next-production-parity-2026-06-02/0-frame-and-method.md:1`.

## Frame

This audit traces `~/.nix-profile/bin/spirit` and `~/.nix-profile/bin/spirit-next`
back through the home-manager Nix store, the home-manager module
that authored them, the flake inputs that pinned the builds, and the
running systemd user services that own the daemons. The output names
exactly what is missing for spirit-next to ship side-by-side and what
work is already done.

**Headline finding: the deployment skeleton for spirit-next is COMPLETE.**
The CLI wrapper exists, the daemon service runs, the state directory
is segregated, the env-var contract is correct, and the cutover from
`v0.3.0` to `next` is a one-line `currentDefault` change in
home-manager configuration. What is missing is upstream — the
`persona-spirit-next` flake input currently resolves to the same
commit as `v0.3.0`, so both slots are running identical daemon code
against separate redb files. Spirit-next's database has not been
written to since 2026-05-25 and stops at record ~708 while production
has continued to 1375+.

## Production deployment chain

The `~/.nix-profile/bin/spirit` symlink resolves through three hops
to a wrapper script in the Nix store, which in turn execs the real
binary the daemon serves.

### Symlink resolution

```text
/home/li/.nix-profile/bin/spirit
  -> /nix/store/gah0lf7442w7vfrdj0n9r713sbin993g-home-manager-path/bin/spirit
  -> /nix/store/n0pi3ahjv5s766lnxyvv0z7qyvy7aaw8-spirit-v0.3.0/bin/spirit-v0.3.0
```

The first hop is the home-manager profile aggregation; the second
hop is the per-version wrapper produced by
`modules/home/profiles/min/spirit.nix:104-118`.

### The wrapper script

`spirit-v0.3.0` is a tiny shell stub the home-manager module emits
through `pkgs.writeShellScriptBin`. The whole contents:

```sh
#!/.../bash-5.3p9/bin/bash
export PERSONA_SPIRIT_SOCKET=/home/li/.local/state/persona-spirit/v0.3.0/spirit.sock
export PERSONA_SPIRIT_OWNER_SOCKET=/home/li/.local/state/persona-spirit/v0.3.0/owner.sock

exec /nix/store/hn6gfrp8s537c48lxin25mr7z9zlbq62-spirit/bin/spirit "$@"
```

The wrapper's job is exactly two things: set the per-slot socket env
vars (which the `signal_cli!` macro reads to discover the daemon) and
exec the real binary. The real binary's first symlink hop lands on
`/nix/store/rrc4j5y5cxsav1w9rzw4w8scklagavrf-persona-spirit-0.3.0/bin/spirit`,
the full crane build of the persona-spirit crate at version 0.3.0.

### The unsuffixed `spirit` symlink

The `~/.nix-profile/bin/spirit` link does NOT name a separate Nix
store derivation; it is a `pkgs.runCommand` wrapper that symlinks the
unsuffixed name to the currently-selected versioned wrapper. From
`modules/home/profiles/min/spirit.nix:143-146`:

```nix
defaultCommandLine = pkgs.runCommand "spirit-current-${sanitizeVersion currentDefault}" { } ''
  mkdir -p "$out/bin"
  ln -s "${selectedDeployment.commandLineWrapper}/bin/${selectedDeployment.wrapperName}" "$out/bin/spirit"
'';
```

So the `currentDefault` option from `modules/home/profiles/min/spirit.nix:175-179`
controls which versioned wrapper the unsuffixed `spirit` points at.
Default is `"v0.3.0"`.

### The daemon under systemd

`systemctl --user list-units --type=service` shows the running
daemons:

```text
persona-spirit-daemon-next.service        loaded active running   Persona-spirit daemon next
persona-spirit-daemon-v0.1.0.service      loaded active running   Persona-spirit daemon v0.1.0
persona-spirit-daemon-v0.1.1.service      loaded activating ...   Persona-spirit daemon v0.1.1
persona-spirit-daemon-v0.2.0.service      loaded active running   Persona-spirit daemon v0.2.0
persona-spirit-daemon-v0.3.0.service      loaded active running   Persona-spirit daemon v0.3.0
```

Five segregated daemons; one per `deployedVersions` entry.

The v0.3.0 daemon's `ExecStart` resolves to a generated shell script
(`modules/home/profiles/min/spirit.nix:101-103`):

```sh
exec /nix/store/l0fpqd5qh64xv6h5vi4lg8r36wny31c1-persona-spirit-daemon/bin/persona-spirit-daemon \
  '([/home/li/.local/state/persona-spirit/v0.3.0/spirit.sock]
    [/home/li/.local/state/persona-spirit/v0.3.0/owner.sock]
    [/home/li/.local/state/persona-spirit/v0.3.0/upgrade.sock]
    [/home/li/.local/state/persona-spirit/v0.3.0/persona-spirit.redb]
    384 None None None None)'
```

The argument is the daemon's single positional NOTA record per
`skills/spirit-cli.md:255-263`: three sockets, redb path, magnitude
limit 384, four reserved `None` extension slots.

`ExecStartPre` runs an initialization shell stub
(`modules/home/profiles/min/spirit.nix:77-100`) that creates the
state directory, removes any stale sockets, and — only for v0.1.0 —
seeds the redb from the legacy unversioned path.

### The flake input that built the daemon

The home-manager flake at
`/git/github.com/LiGoldragon/CriomOS-home/flake.nix` declares the
input (`flake.nix` around the persona-spirit block):

```nix
persona-spirit-v0-3-0.url = "github:LiGoldragon/persona-spirit?rev=df09280a464f8a7be1c20ff433de4bfc4afc7f53";
persona-spirit-v0-3-0.inputs.nixpkgs.follows = "nixpkgs";
persona-spirit-next.url   = "github:LiGoldragon/persona-spirit?ref=main";
persona-spirit-next.inputs.nixpkgs.follows = "nixpkgs";
```

The lock file (`flake.lock`) pins both inputs. The `v0-3-0` input is
rev-pinned. The `next` input tracks `main` but, as of the current
lock, resolves to the SAME commit
`df09280a464f8a7be1c20ff433de4bfc4afc7f53` (`add verbal recency depth
queries`). This means both slots share an identical daemon binary
today.

The persona-spirit flake itself
(`/git/github.com/LiGoldragon/persona-spirit/flake.nix:43-49`)
exposes BOTH binaries from a single crane build:

```nix
spiritPackage     = pkgs.runCommand "spirit"     { } ''.../bin/spirit'';
spiritNextPackage = pkgs.runCommand "spirit-next"{ } ''.../bin/spirit-next'';
```

And its Cargo.toml declares both as separate `[[bin]]` entries
sharing the same crate
(`/git/github.com/LiGoldragon/persona-spirit/Cargo.toml:15-21`):

```toml
[[bin]]
name = "spirit"
path = "src/bin/spirit.rs"

[[bin]]
name = "spirit-next"
path = "src/bin/spirit-next.rs"
```

Both source files are one-liners over the same signal contract:

```rust
// src/bin/spirit.rs
signal_frame::signal_cli!(spirit, signal_persona_spirit);

// src/bin/spirit-next.rs
signal_frame::signal_cli!(spirit_next, signal_persona_spirit);
```

The macro derives the env-var stem from the binary name via
`signal-frame/src/command_line.rs:336-352`: `spirit` → `PERSONA_SPIRIT`
+ `_SOCKET` / `_OWNER_SOCKET`; `spirit-next` → `PERSONA_SPIRIT_NEXT`
+ `_SOCKET` / `_OWNER_SOCKET`. This is why the wrapper sets
distinct env-var names — they refer to different daemons listening
on different sockets.

## Slot-model implementation today

Per `skills/spirit-cli.md:28-44` the deployment model is:

```text
spirit            -> spirit-vX.Y.Z       (production)
spirit-vX.Y.Z     -> installed
spirit-vX.Y.Z-1   -> installed
spirit-vX.Y.Z+1   -> installed
spirit-next       -> (slot)
```

The home-manager module manifests this model in full:

### Available versions

`modules/home/profiles/min/spirit.nix:23-29` lists every slot the
module knows about:

```nix
availableVersions = [
  "v0.1.0"
  "v0.1.1"
  "v0.2.0"
  "v0.3.0"
  "next"
];
```

### Per-version input mapping

`modules/home/profiles/min/spirit.nix:31-37` maps each slot name to a
flake input:

```nix
packageInputsByVersion = {
  "v0.1.0" = inputs."persona-spirit-v0-1-0";
  "v0.1.1" = inputs."persona-spirit-v0-1-1";
  "v0.2.0" = inputs."persona-spirit-v0-2-0";
  "v0.3.0" = inputs."persona-spirit-v0-3-0";
  "next"   = inputs.persona-spirit-next;
};
```

### Per-version package selection

`modules/home/profiles/min/spirit.nix:52-62` picks the CLI binary
based on whether the slot is `next`:

```nix
commandLine =
  if version == "next" then
    packageInput.packages.${system}.spirit-next
  else
    packageInput.packages.${system}.spirit;
commandLineBinary = if version == "next" then "spirit-next" else "spirit";
```

The daemon binary is the same for every slot:

```nix
daemon = packageInput.packages.${system}.persona-spirit-daemon;
```

### Per-version state segregation

`modules/home/profiles/min/spirit.nix:64-69`:

```nix
stateDirectory      = "${rootStateDirectory}/${version}";
ordinarySocketPath  = "${stateDirectory}/spirit.sock";
ownerSocketPath     = "${stateDirectory}/owner.sock";
upgradeSocketPath   = "${stateDirectory}/upgrade.sock";
databasePath        = "${stateDirectory}/persona-spirit.redb";
```

Each slot lives entirely under
`~/.local/state/persona-spirit/<version>/`. Sockets and redb are
NEVER shared. Confirmed on disk:

```text
~/.local/state/persona-spirit/
├── next/        # spirit-next slot
├── v0.1.0/
├── v0.1.1/
├── v0.2.0/
└── v0.3.0/      # production slot
```

### Per-version env-var wrapper

`modules/home/profiles/min/spirit.nix:104-118` emits a shell wrapper
that exports per-slot env vars before exec'ing the CLI. For `next`
the env-var names are `PERSONA_SPIRIT_NEXT_SOCKET` and
`PERSONA_SPIRIT_NEXT_OWNER_SOCKET`; for every other version they are
`PERSONA_SPIRIT_SOCKET` and `PERSONA_SPIRIT_OWNER_SOCKET`. The
asymmetry is correct — `spirit` (the CLI binary name) and
`spirit-next` (the CLI binary name) derive different env-var stems
via the `signal_cli!` macro.

### Per-version daemon configuration

`modules/home/profiles/min/spirit.nix:70-76` per-version shape of the
daemon's NOTA argument:

```nix
configuration =
  if version == "v0.1.0" then
    ''([...sockets] [...] [...upgrade.sock] [...redb] 384 None)''
  else if version == "v0.1.1" then
    ''([...] [...] [...redb] 384 None)''
  else
    ''([...] [...] [...upgrade.sock] [...redb] 384 None None None None)'';
```

The branches reflect the contract's evolving shape across versions;
both `v0.3.0` and `next` use the same five-positional shape.

### Per-version systemd service

`modules/home/profiles/min/spirit.nix:148-165` defines the user
service. Each daemon gets a `Conflicts` entry against the legacy
unsuffixed `persona-spirit-daemon.service` and an `After` ordering
that lets it cleanly take over from any older single-version
deployment.

### Cutover machinery

The single-default selector at
`modules/home/profiles/min/spirit.nix:137-141`:

```nix
selectedDeployment =
  if builtins.elem currentDefault deployedVersions then
    deployments.${currentDefault}
  else
    throw "criomosHome.personaSpirit.currentDefault must be listed in deployedVersions";
```

Plus the symlink-emitting derivation at lines 143-146 (see above).
Cutover is one configuration change: set
`criomosHome.personaSpirit.currentDefault = "next"` and rebuild.

### Check coverage

The deployment shape is exercised end-to-end by
`checks/persona-spirit-versioned-deployment/default.nix`. The check
spins up fake inputs for every slot, instantiates the module, and
asserts:

- Each per-version systemd service exists
  (`checks/persona-spirit-versioned-deployment/default.nix:71-95`)
- Each per-version CLI wrapper is present in the profile
  (`checks/persona-spirit-versioned-deployment/default.nix:105-110`)
- The daemon's `ExecStart` argument references the correct per-slot
  redb / upgrade.sock paths and contains no `"` characters
  (`checks/persona-spirit-versioned-deployment/default.nix:112-136`)
- Each wrapper exports the correct per-slot env vars
  (`checks/persona-spirit-versioned-deployment/default.nix:144-177`)
- The `spirit-next` wrapper specifically prints `version=next` and
  the `next/`-prefixed paths
  (`checks/persona-spirit-versioned-deployment/default.nix:172-177`)
- The unsuffixed `spirit` resolves to whichever slot
  `currentDefault` names
  (`checks/persona-spirit-versioned-deployment/default.nix:179-181`)

## Spirit-next slot status

The slot is **already deployed and running**. Live state:

- `~/.nix-profile/bin/spirit-next` exists, resolves to
  `/nix/store/y43j833yc5jpr5r5kwkjavkj5mb5raap-spirit-next/bin/spirit-next`,
  which is the per-slot wrapper exporting `PERSONA_SPIRIT_NEXT_SOCKET=
  ~/.local/state/persona-spirit/next/spirit.sock`.
- The wrapper execs
  `/nix/store/77b3y13mj5awfxnqxnjb19215gkqdy2z-spirit-next/bin/spirit-next`,
  which is a symlink to the real binary in the persona-spirit-0.3.0
  build (because the `next` flake input currently resolves to the
  v0.3.0 commit).
- `persona-spirit-daemon-next.service` is active and running.
- `~/.local/state/persona-spirit/next/` contains the three sockets,
  an active 569 KB `persona-spirit.redb`, and an
  `empty-before-migration` backup from 2026-05-25.
- The CLI works: `spirit-next "(Observe Topics)"` returns
  `(TopicsObserved [...])` with the expected catalog.

**The "missing" pieces are NOT deployment pieces.** Everything Nix-
side is wired. The two open issues are:

### Issue 1: `next` flake input points at the same commit as v0.3.0

`flake.lock` resolves both `persona-spirit-v0-3-0` and
`persona-spirit-next` to rev `df09280` (the v0.3.0 tip). This means:

- The deployed `spirit-next` CLI is literally the same binary as
  `spirit-v0.3.0`, just renamed.
- Until persona-spirit's `main` branch advances past v0.3.0 with
  spirit-next-distinguishing behaviour, the two daemons are
  functionally identical engines running against separate state.

This is normal at this point in the cycle. The `?ref=main` form
deliberately lets the input float; the next `nix flake update
persona-spirit-next` will pull whatever main has advanced to.
Sub-agents 1 (wire-shape parity) and 2 (build/test) will report on
whether spirit-next today is intended to deviate from v0.3.0 in code.

### Issue 2: spirit-next's redb has drifted from production

Compared against production records:

- Production (`spirit "(Observe (RecordIdentifiers ((Exact 1375)
  WithProvenance)))"`): record 1375 exists, dated 2026-06-01.
- Spirit-next (`spirit-next ...` same query): empty reply.
- Spirit-next records range only up to ~708 (May 25 era — confirmed
  via `(Range (690 800)) SummaryOnly` which returns only entries 695
  through 708 then runs out).

The next slot was seeded from the production snapshot
`~/.local/state/persona-spirit/persona-spirit.redb.v0.2.0.production-cutover-20260525235707`
during the v0.2.0 → next migration on 2026-05-25, and has received
some local writes since then (size grew from 1.06 MB
empty-before-migration to 569 KB compacted — net it has roughly 708
records vs production's 1375). It is NOT kept in sync with production
writes; agents write through `spirit` which lands in the v0.3.0 slot
only.

Sub-agent 4 (data and storage compatibility) is responsible for
deciding the cutover/sync strategy. From the deployment side, the
relevant fact is: the home-manager module's `initializeState` hook
(`modules/home/profiles/min/spirit.nix:77-100`) currently only seeds
v0.1.0 from the legacy unversioned redb. There is no equivalent hook
that would re-seed `next` from `v0.3.0`. If we want spirit-next to
reflect current production data, that hook needs an extension, OR
the cutover is the moment we abandon next's accumulated writes and
re-seed from production. Both options are deployment-config matters.

## Concrete change list

Per the task description ("concrete diff or pseudo-diff describing
the home-manager additions needed"), the answer is **no
deployment-config changes are needed to ship spirit-next as a
side-by-side slot — that's already done.** The remaining work splits
across upstream + home-manager:

### Required upstream (persona-spirit repo) — sub-agents 1+2 territory

- Decide whether `spirit-next`'s source binary needs to diverge from
  `spirit` (multi-topic records per record 707, hard database
  migration, etc.). When it does, persona-spirit's `main` advances
  past `df09280`.
- When it advances, run `nix flake update persona-spirit-next` in
  CriomOS-home. No `flake.nix` edit needed; the
  `?ref=main` input form picks up the new commit.

### Optional home-manager additions (if we want re-sync from production)

If the cutover plan is to keep spirit-next in sync with production
records (rather than abandon next's history at cutover), one of these
home-manager additions is needed:

**Option A (re-seed on next deploy).** Extend
`modules/home/profiles/min/spirit.nix:77-100` to copy v0.3.0's redb
into next's slot when next's redb is absent or older. The copy must
happen with the v0.3.0 daemon stopped to avoid redb corruption (per
record 1287 the redb cannot be safely copied during writes). The
existing `ExecStartPre` pattern is close to right; would need a
gating predicate.

**Option B (live mirror via upgrade.sock).** Spirit's
`upgrade.sock` is contractually the channel that mirrors stamped
entries between daemon versions. Sub-agent 4 should evaluate whether
the upgrade mirror is functional enough to keep next current with
v0.3.0 in real time. This is the contract-designed path; option A is
the brute-force fallback. No home-manager changes are needed for
option B because the upgrade-sock path is already wired in the daemon
configuration (see the v0.3.0 daemon's NOTA argument above).

### One-line cutover when spirit-next is ready

When sub-agents 1+2+4 conclude spirit-next is ready to replace
v0.3.0, the cutover is one line. Add to whichever home-manager
configuration sets up the persona-spirit module (or to the module's
defaults at line 178):

```nix
criomosHome.personaSpirit.currentDefault = "next";
```

Rebuild home-manager. After the switch, `~/.nix-profile/bin/spirit`
resolves to the spirit-next wrapper; agents using the unsuffixed
command land on the next daemon. Both `spirit-v0.3.0` and
`spirit-next` remain as explicit testing surfaces.

### Estimated cost

| Piece | Status | Effort |
|---|---|---|
| Per-slot CLI wrapper | Done | n/a |
| Per-slot daemon service | Done | n/a |
| Per-slot state directory | Done | n/a |
| Per-slot env-var contract | Done | n/a |
| Flake input for `next` tracking persona-spirit main | Done | n/a |
| Cutover machinery (`currentDefault`) | Done | n/a |
| Check coverage | Done | n/a |
| Re-seed next from v0.3.0 (if needed) | Not done; option A | Small (~30 lines of shell in `initializeState`) |
| Live mirror via upgrade.sock | Wired contractually; sub-agent 4 verifies | Zero deployment-config cost if already functional |
| Spirit-next source distinct from v0.3.0 | Sub-agent 2 territory | Unknown |

## Side-by-side safety verdict

**Yes — current deploy code is fully side-by-side safe.**

Evidence:

- Daemon state directories are absolutely segregated per slot
  (`modules/home/profiles/min/spirit.nix:65-69`). No code path in the
  module crosses slot boundaries except the v0.1.0 legacy seeding
  step, which only fires when v0.1.0's own redb is absent
  (`modules/home/profiles/min/spirit.nix:93-99`).
- Sockets are per-slot (no socket reuse across daemons).
- The daemon NOTA argument contains only paths under the slot's own
  state directory — verified by the check that asserts
  `grep -q '/persona-spirit/v0.3.0/persona-spirit.redb'` for v0.3.0's
  service and `grep -q '/persona-spirit/next/persona-spirit.redb'` for
  next's service
  (`checks/persona-spirit-versioned-deployment/default.nix:127-136`).
- The unsuffixed `spirit` symlink is generated by a separate `runCommand`
  derivation (`modules/home/profiles/min/spirit.nix:143-146`) and points
  ONLY at `currentDefault`'s wrapper. No code path force-aliases new
  versions onto the production slot — changing `currentDefault` is the
  only way to move the unsuffixed `spirit`.
- Service unit `Conflicts` is against the legacy unsuffixed
  `persona-spirit-daemon.service` only, never between versioned
  slots. All versioned daemons coexist.
- The check file asserts the unversioned `persona-spirit-daemon`
  service is absent
  (`checks/persona-spirit-versioned-deployment/default.nix:91-94`),
  preventing a regression to the single-daemon model.

The one nuance: today's `next` slot daemon and v0.3.0 daemon are
**the same binary** (because both flake inputs resolve to the same
commit). They run as separate processes with separate state — so
side-by-side correctness holds — but a bug in the shared daemon code
would affect both. As soon as persona-spirit's main advances past
v0.3.0, this convergence breaks naturally.

## Recommendations

In order of work:

1. **Confirm with sub-agents 1+2 whether spirit-next today is
   intended to diverge from v0.3.0 in the source tree.** If yes, the
   work is on the persona-spirit repo side and lands in main; the
   home-manager `?ref=main` input picks it up via
   `nix flake update persona-spirit-next`.
2. **Confirm with sub-agent 4 whether `upgrade.sock` mirroring is
   the intended path to keep `next` current with `v0.3.0` writes.**
   If yes, no further home-manager changes are needed. If no, evaluate
   option A (extend `initializeState`) when next's redb is determined
   to be re-seedable.
3. **Defer the `currentDefault = "next"` flip** until sub-agents
   1+2+4 confirm spirit-next has wire-shape parity AND a viable data
   story. The cutover itself is one line; the prerequisites determine
   when it's safe.
4. **Do not modify `~/.local/state/persona-spirit/next/` directly.**
   The redb is a live database under the running daemon (per
   record 1287 redb can't safely be copied or modified during writes).
   Re-seeding requires stopping the next daemon first; defer to
   sub-agent 4's plan.
5. **Spirit-next's database has drifted from production by ~667
   records** (1375 - 708). This is the most actionable deployment-
   adjacent fact. Either it's harmless (we plan to drop next's state
   at cutover and re-seed) or it's a feature (next is an independent
   redb the user wants to keep); the answer is upstream of deployment
   config.
