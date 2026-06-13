# 46 · 3 — Running the lojix daemon live + issuing the deploy

Read-only reconnaissance. Repo `/git/github.com/LiGoldragon/lojix` at git
`bbb8030` (jj change `szrnnoskqspl`, "a deploy survives a dropped client — S4b").
Every claim is grounded in a file read or a command run. Mutated NOTHING.

## TL;DR

- Four binaries: `lojix-daemon`, `lojix` (ordinary CLI), `meta-lojix` (owner
  CLI), `lojix-write-configuration` (NOTA→rkyv startup encoder)
  (`Cargo.toml:14-28`).
- Build with cargo (no `flake.nix` in the repo); the CLIs need
  `--features nota-text` to accept inline/`.nota` NOTA, the daemon never does.
- **Run the daemon ON PROMETHEUS**, not ouranos — the deploy activates
  `root@dune.goldragon.criome`, a name ouranos cannot resolve (verified below)
  but Prometheus owns (its own VM).
- The daemon runs in the foreground forever (`block_on`); SSH-disconnect
  survival of the *daemon process* requires detaching it (`systemd-run` /
  `setsid`), independent of the in-flight-deploy survival the daemon already
  implements (up9q).
- Drive the deploy with `meta-lojix "(Deploy (...))"`; start with `Build`
  (non-activating, realises the closure, no target mutation), then `BootOnce`
  (transient unit, the disconnect-safe activation) or `Switch`.
- Observe over the ordinary `lojix` CLI: `Query` against the durable event-log
  (`ByEventLog`) is the reconnect-by-Query path; `WatchDeployments` opens a
  subscription (handshake-only today).

## 1. Building the binaries

No `flake.nix`/`default.nix` in `lojix` — `ls` returned none, so this is a
plain cargo build. Toolchain on ouranos is rustc/cargo 1.95.0, satisfying
`rust-version = "1.89"` (`Cargo.toml:5`). The repo is a git dependency graph
(horizon-lib, nota-next, signal/meta-signal-lojix, sema-engine, triad-runtime,
kameo all `git` deps — `Cargo.toml:34-49`), so the build needs network on first
fetch.

```
# build on the host where the daemon will run (see §3 → Prometheus)
cargo build --release --features nota-text
```

`--features nota-text` is load-bearing for the CLI clients. Without it, inline
NOTA and `.nota` files are rejected with `Error::NotaTextUnsupported`
(`client.rs:110-113,169-172`; tests `client_nota.rs:46-72` assert exactly this).
The feature flows into both contracts (`Cargo.toml:32`). The
`lojix-write-configuration` tool parses NOTA *unconditionally* (it derives
`NotaDecode` directly, `lojix-write-configuration.rs:27-39,57-59`) — it does not
need the feature. The daemon also never needs it: it takes only the rkyv file
(`lojix-daemon.rs:16-23`).

Resulting binaries land in `target/release/{lojix-daemon,lojix,meta-lojix,
lojix-write-configuration}` (none built yet — `ls target/release/...` empty).

## 2. Authoring the rkyv startup config

`lojix-write-configuration` takes ONE NOTA argument and writes the rkyv startup
file the daemon consumes — the NOTA→binary boundary
(`lojix-write-configuration.rs:1-7,55-62`). The request type is positional
(NOTA records are positional, not labelled), fields in declared order
(`lojix-write-configuration.rs:27-35`):

```
ConfigurationWriteRequest = (
  ordinary_socket_path   ordinary_socket_mode
  owner_socket_path      owner_socket_mode
  state_directory_path   output_path )
```

Modes are decimal `u32` octal-values in the NOTA (`WriterMode(u32)`,
`lojix-write-configuration.rs:45-46`); the canonical test passes `432` = `0o660`
and `384` = `0o600` (`write_configuration.rs:14-17,31-33`). The daemon REFUSES
an owner mode granting any "other" access at startup (`mode & 0o007 != 0`,
`daemon.rs:126-131`; `build_smoke.rs:192-217`), so the owner socket must be
`0o600` (384) or `0o660` (432) — never `0o666`.

Concrete (Prometheus paths under `/run/lojix` + `/var/lib/lojix`, mirroring the
test's defaults `write_configuration.rs:15`):

```
lojix-write-configuration \
  "(ConfigurationWriteRequest (/run/lojix/ordinary.sock 432 /run/lojix/owner.sock 384 /var/lib/lojix /run/lojix/startup.rkyv))"
# -> prints (ConfigurationWritten [/run/lojix/startup.rkyv])
```

The daemon opens `<state_directory>/lojix.sema` as the durable store and
self-resumes from it (`daemon.rs:97-103`, `lib.rs:226-270`) — so `/var/lib/lojix`
must persist across restarts for the disconnect test.

## 3. Launching the daemon — and WHERE it runs

Launch is binary-only, exactly one rkyv argument, no flags
(`lojix-daemon.rs:16-23`; it rejects inline NOTA / `.nota` via the signal-file
boundary):

```
lojix-daemon /run/lojix/startup.rkyv
```

`Daemon::run` builds a multi-thread tokio runtime and `block_on`s
`run_async` forever, binding the ordinary + owner sockets at the configured
modes and serving (`daemon.rs:73-110`). **It does not self-daemonize / fork** —
it holds the foreground. So to survive the operator's SSH disconnect the daemon
*process* must be detached at launch (the deploy-job survival in §S4b is a
separate, already-built guarantee — a dropped *client* connection no longer
kills an in-flight deploy, `lib.rs:447-475`, `daemon.rs:164-189`). On Prometheus:

```
# detach so the daemon outlives the launching ssh session
systemd-run --user --unit=lojix-daemon-e2e --service-type=exec \
  --setenv=PATH=/run/current-system/sw/bin \
  <abs-path>/lojix-daemon /run/lojix/startup.rkyv
# (or: setsid <path>/lojix-daemon /run/lojix/startup.rkyv </dev/null &>/var/lib/lojix/daemon.log & )
```

### Where: ON PROMETHEUS, not ouranos — decisive

The deploy's copy and activate steps address the target as
`root@<node>.<cluster>.criome` (NEVER a bare node name) — built by
`SshTarget::root_at_node` → `CriomeDomainName::for_node` = `{node}.{cluster}.criome`
(`schema_runtime.rs:2154-2192`, `horizon-rs/lib/src/name.rs:107-108`). For the
`dune`/`goldragon` fixture that is `root@dune.goldragon.criome`:
- `nix copy --substitute-on-destination --to ssh-ng://root@dune.goldragon.criome <closure>`
  (`schema_runtime.rs:2298-2312`)
- `ssh -o BatchMode=yes root@dune.goldragon.criome '<store>/bin/switch-to-configuration <action>'`
  (`schema_runtime.rs:2194-2205,2377-2409`)

Verified resolution (read-only): from ouranos
`getent hosts dune.goldragon.criome` → **NO-RESOLVE**, while
`prometheus.goldragon.criome` resolves (`200:ca41:...:165f`). The VM (`dune`,
an nspawn/qemu fixture) lives ON Prometheus, so its
`dune.goldragon.criome` address is reachable from Prometheus, not from ouranos.
Running the daemon on Prometheus gives it localhost-ish SSH reach to its own VM;
running on ouranos would fail at the copy/activate hop on an unresolvable host.
Prometheus is amply provisioned for the build too (read-only inspect:
`prometheus`, NixOS `26.05.20260422.0726a0e (Yarara)`, 32 cores, 124Gi RAM, nix
present; `libvirtd` inactive → use qemu user-mode, not libvirt).

Daemon builds locally by default (`BuildTarget::Local` when no `builder`,
`schema_runtime.rs:365-370`), so building on Prometheus also keeps the heavy
`nix build` on the well-provisioned host. (Optional `builder` would ssh-dispatch
the build; not needed here.)

## 4. The deploy command: meta-lojix Build-then-Deploy

`meta-lojix` is the owner-only CLI on the owner socket; one NOTA argument
decoded as a `meta-signal-lojix` `Input` (`meta-lojix.rs:1-23`,
`client.rs:124-155`). Socket path via `LOJIX_OWNER_SOCKET`
(default `/run/lojix/owner.sock`; `client.rs:23,25,151`).

`DeployRequest = [(System SystemDeployment) (Home HomeDeployment)]`
(`meta-signal-lojix/schema/lib.schema:108`). `SystemDeployment` positional field
order (`…lib.schema:87-97`):

```
SystemDeployment = (
  ClusterName  NodeName  DeploymentKind
  source(ProposalSource)  flake(FlakeReference)
  SystemAction
  builder(Optional Builder)  substituters(Vec ExtraSubstituter)
  build_attribute(Optional FlakeAttribute) )
```

`SystemAction = [Eval Build Boot Switch Test BootOnce]`,
`DeploymentKind = [FullOs OsOnly HomeOnly]` (`signal-lojix/schema/lib.schema:54,55`).
The reply is `(Deployed (AcceptedDeploy (DeploymentIdentifier DatabaseMarker)))`
or `(DeployRejected (RejectedDeploy (DeployRejectionReason DatabaseMarker)))`
(`…lib.schema:65,114,129`). All System actions Eval/Build/Boot/Switch/Test/
BootOnce now enter the pipeline (no UnsupportedDeployAction rejection,
`schema_runtime.rs:846-865`).

When `build_attribute` is PRESENT the daemon builds that self-contained flake
output with NO horizon override (`schema_runtime.rs:379-426`,
`needs_horizon_materialization == build_attribute.is_none()`). The
self-contained fixture is
`github:LiGoldragon/CriomOS-test-cluster#dune-nspawn-toplevel` — a
`fixtureSystem "dune"` toplevel with its horizon baked in
(`build_smoke.rs:21-22,44-61`, `CriomOS-test-cluster/flake.nix:202`). Dry-eval
of that attribute's `.drvPath` succeeds read-only:
`/nix/store/vnqscazqif8...-nixos-system-dune-26.05....drv`. A full-OS production
deploy (no `build_attribute`) instead triggers horizon materialization — the
deferred M3 path; the fixture build_attribute is the proven S5 route.

Concrete commands (matching the test fixture: cluster `goldragon`, node `dune`):

Step A — non-mutating BUILD to confirm eval→build→copy lands the closure
WITHOUT touching the VM (`Build` does not activate —
`DeployAction::activates()` is false for Eval/Build, `schema_runtime.rs:244-256`;
copy still runs, activation does not):

```
meta-lojix "(Deploy ((System (goldragon dune OsOnly /dev/null github:LiGoldragon/CriomOS-test-cluster Build None [] (dune-nspawn-toplevel)))))"
```

(`builder` = `None`, `substituters` = `[]` empty vec, `build_attribute` =
`(dune-nspawn-toplevel)` an `Optional FlakeAttribute` present-value;
`source = /dev/null` is the unused-on-this-path placeholder, `build_smoke.rs:47-54`.
First confirm the even-cheaper `Eval` — same command with `Build`→`Eval` — which
stops at the realised `.drv` path, the lightest pipeline proof, `build_smoke.rs:79-92`.)

Step B — activating deploy INTO the VM, disconnect-safe via BootOnce
(`BootOnce` writes a PID-1-owned transient unit `lojix-boot-once-deploy-<id>`
that survives the daemon and is the resume-poll target,
`schema_runtime.rs:506-520,548-554`):

```
meta-lojix "(Deploy ((System (goldragon dune FullOs /dev/null github:LiGoldragon/CriomOS-test-cluster BootOnce None [] (dune-nspawn-toplevel)))))"
```

(For a permanent switch use `Switch` in place of `BootOnce`; `DeploymentKind`
`FullOs` for the full-OS S5 goal. Both copy `--to ssh-ng://root@dune.goldragon.criome`
then `ssh root@dune.goldragon.criome switch-to-configuration {boot|switch}`.)

## 5. Observing progress: Query / WatchDeployments

After the `AcceptedDeploy` handle, observe over the ORDINARY `lojix` CLI
(`lojix.rs`, `client.rs:56-114`; socket `LOJIX_ORDINARY_SOCKET`, default
`/run/lojix/ordinary.sock`, `client.rs:22,24,92`). The phase lifecycle
(`Submitted Building Built Copying Activating Activated Failed`,
`signal-lojix/schema/lib.schema:90`) is recorded into the durable event log, so
observation is a Query against that log — reconnect-by-Query is just re-issuing
the Query after a disconnect; nothing is held in connection state.

`Selection = [(ByNode NodeSelector) (ByGeneration GenerationLookup)
(ByEventLog EventLogRange)]`; `EventLogRange = (from until)`;
`NodeSelector = (ClusterName NodeName kind(Optional DeploymentKind))`
(`…lib.schema:72-75`). The canonical inline Query is
`(Query ((ByNode (goldragon dune None))))` (`client_nota.rs:49,67`).

```
# live-set / phase by node (re-run to reconnect; no subscription needed)
lojix "(Query ((ByNode (goldragon dune None))))"

# durable event-log slice — the reconnect-by-Query path; widen `until` to tail
lojix "(Query ((ByEventLog (0 1000))))"

# by the minted generation identifier (from the AcceptedDeploy reply)
lojix "(Query ((ByGeneration (<generation_identifier>))))"
```

Reply: `(Queried (GenerationListing (generations DatabaseMarker)))`
(`…lib.schema:31,70`; `client_nota.rs:150-159` confirms it renders
`(Queried ...)`).

`WatchDeployments` opens a subscription:

```
lojix "(WatchDeployments (None None None))"   # all deployments (deployment cluster node all absent)
```

CAVEAT (day-one decision 2tfa, `signal-lojix/schema/lib.schema:11-20`):
schema-next cannot yet emit daemon-pushed event frames, so `WatchDeployments`
today is the SUBSCRIPTION HANDSHAKE only — it replies
`(Watching (SubscriptionOpened (SubscriptionToken CommitSequence)))`
(`…lib.schema:32,80`) and returns; the streamed `DeploymentPhaseEvent`s are not
yet pushed. So for live S5 progress, **poll `Query (ByEventLog ...)`** as the
real observation loop; `WatchDeployments`/`Unwatch` exercise the handshake but
do not stream yet. Close with `lojix "(Unwatch (<token>))"` (`…lib.schema:79`).
```
