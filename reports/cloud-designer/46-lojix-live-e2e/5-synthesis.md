# 46 · Lojix live e2e (S5) — synthesis: the executable cutover runbook

cloud-designer, 2026-06-13. Synthesis of the read-only reconnaissance in
`0-frame-and-method.md` through `4-disconnect-test-and-safety.md`. This is the
exact ordered, verified runbook for the first live daemon-touches-a-target
cutover (Spirit `se72`/`7let`; psyche authorized proceeding 2026-06-13). Every
step carries its concrete command(s) and the verification that gates moving on.
Ordering is deliberate: a non-mutating eval/Build proves the whole pipeline
before the first activating Deploy, and every artifact (VM, daemon, state) lives
in a throwaway location so a broken deploy kills only the VM, never the host.

## What this run proves

The full lojix deploy pipeline — eval → build → `nix copy` → activate — driven
by the `lojix-daemon` over its owner socket, landing a full NixOS generation
into a throwaway qemu/KVM VM on Prometheus, and surviving an SSH disconnect on
**both** surfaces:

- **S4b — client → daemon.** Killing the `meta-lojix` client mid-deploy cannot
  cancel the daemon-owned pipeline (`daemon.rs:321-367,524-537`).
- **S4a — daemon → target.** A BootOnce activation runs inside a target-side
  `systemd-run --collect` transient unit owned by the VM's PID 1; the daemon's
  ssh to the VM dropping mid-activation leaves the unit running to completion
  (`schema_runtime.rs:2380-2382,2456-2471`).

## Reconciled facts (where the sibling reports disagreed)

Three conflicts in the source reports are resolved here against the fixture's
own baked horizon, which is the ground truth the daemon's derived address and
the ssh alias must both match:

1. **Cluster is `fieldlab`, not `goldragon`.** Reports 3 and 4 used
   `root@dune.goldragon.criome`; report 2 used `fieldlab`. The fixture's baked
   identity (`fixtures/horizon/dune.json`, read live) is
   `cluster.name = fieldlab`, `node.name = dune`, `nodeIp 10.77.0.4/24`. The
   daemon derives the target address purely from the cluster+node passed on the
   Deploy cursor — `CriomeDomainName::for_node` = `{node}.{cluster}.criome`
   (`horizon-rs/lib/src/name.rs:106-108`, `schema_runtime.rs:2154-2176`). So the
   Deploy MUST pass `fieldlab dune` to make the address
   `root@dune.fieldlab.criome` match the fixture, and the ssh alias must be keyed
   on that exact name. **Use `fieldlab` / `dune` everywhere.**

2. **Build attribute is `dune-toplevel`, not `dune-nspawn-toplevel`.** S5 wants a
   *full bootable OS* that survives disconnect across a reboot, which needs a
   real systemd-boot ESP and `bootctl` for `Boot`/`BootOnce` to mean anything
   (report 1 §7). `dune-toplevel = fixtureSystem "dune" []` is a full bootable OS
   (no `boot.isContainer`/`isNspawnContainer`); `dune-nspawn-toplevel` sets
   `boot.isNspawnContainer = true` and is a container that CANNOT do BootOnce
   (`flake.nix:201-215`, read live). **Use `dune-toplevel`.**

3. **Event-log observation verb.** Report 3 used
   `lojix "(Query ((ByEventLog (from until))))"`; report 4 used
   `lojix "(ReadEventLog (EventLogRange from until))"`. Both target the durable
   event log. The runbook uses the `Query (ByEventLog ...)` form as primary
   (it is the documented Selection variant, `signal-lojix/schema/lib.schema:72-75`)
   and notes `ReadEventLog` as the alternative; the operator confirms which the
   built binary accepts at Step 6 with a harmless read before relying on it.

## Throwaway-location discipline (all under one scratch root)

Everything the run creates lives under `/tmp/lojix-e2e/` on Prometheus (a large
scratch filesystem; the real bound is disk for the closure + qcow2, not CPU/RAM
— report 4). Teardown is `rm -rf` of that tree plus killing two transient units.
Nothing touches Prometheus's own system config, networking, or `/etc`.

| Artifact | Throwaway path | Reset |
|---|---|---|
| VM flake + qcow2 disk | `/tmp/lojix-e2e/vm-target/`, `/tmp/lojix-e2e/target.qcow2` | delete files |
| VM runner closure | `/tmp/lojix-e2e/vm-runner` (gc-root symlink) | delete symlink |
| Daemon sockets | `/tmp/lojix-e2e/run/{ordinary,owner}.sock` | unlink with unit |
| Daemon state (SEMA) | `/tmp/lojix-e2e/state/` | delete dir |
| Daemon startup rkyv | `/tmp/lojix-e2e/run/startup.rkyv` | delete file |
| ssh alias for `dune.fieldlab.criome` | `~/.ssh/config.d/lojix-e2e` (user-level only) | delete file |
| VM transient unit | `--user` unit `lojix-e2e-vm` | `systemctl --user stop` |
| Daemon transient unit | `--user` unit `lojix-daemon-e2e` | `systemctl --user stop` |

## The runbook

Run as user `li` on Prometheus unless noted. Steps 0–4 mutate nothing on the
host beyond writing throwaway files under `/tmp/lojix-e2e/` and one user ssh
alias; the first time anything *activates* a generation is Step 8, and even then
only inside the VM.

### 0 · Preflight — confirm the host is ready, read-only

```sh
ssh prometheus.goldragon.criome '
  ls -l /dev/kvm; test -w /dev/kvm && echo KVM-WRITABLE;
  nproc; free -h | head -2; nixos-version; systemctl is-system-running'
```

Gate: `/dev/kvm` is `crw-rw-rw-` and writable by `li`; ≥ ~30 GiB scratch free
under `/tmp`; system `running`. (Already confirmed in reports 1/4; re-run
because the live run is a fresh session.) No write occurs.

### 1 · Lay down the scratch tree and the VM target flake

```sh
ssh prometheus.goldragon.criome 'mkdir -p /tmp/lojix-e2e/{vm-target,run,state}'
```

Write `/tmp/lojix-e2e/vm-target/flake.nix` (the standalone first-boot image —
NOT the heavy CriomOS `nixosConfigurations.target`; report 1 §4). It must: be
UEFI + systemd-boot (so `bootctl` exists for BootOnce), use a persistent qcow2
(so a reboot survives), forward host `:2222 → guest:22`, run sshd accepting
`root` key-only, and bake in the daemon-runner's public key.

```nix
{ inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }: {
    nixosConfigurations.target = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ({ modulesPath, ... }: {
        imports = [ "${modulesPath}/virtualisation/qemu-vm.nix" ];
        boot.loader.systemd-boot.enable = true;
        boot.loader.efi.canTouchEfiVariables = true;
        virtualisation = {
          graphics = false;
          diskImage = "/tmp/lojix-e2e/target.qcow2";
          useEFIBoot = true;
          forwardPorts = [ { from = "host"; host.port = 2222; guest.port = 22; } ];
          memorySize = 4096; cores = 4;
        };
        services.openssh = { enable = true;
          settings = { PermitRootLogin = "yes"; PasswordAuthentication = false; }; };
        users.users.root.openssh.authorizedKeys.keys = [ "<RUNNER_PUBKEY>" ];
        system.stateVersion = "25.11";
      }) ];
    };
  };
}
```

`<RUNNER_PUBKEY>` is the public half of the identity the daemon's `ssh` /
`nix copy --to ssh-ng://` will present — i.e. the ssh identity of user `li` on
Prometheus, the host where the daemon runs (the daemon shells out and inherits
the runner's agent/identity, `schema_runtime.rs:2194-2205,2298-2312`). Resolve
the exact pubkey first (Step 2). x86_64 is required — the fixture toplevel is
architecturally x86_64 (report 2), matching the qemu VM arch.

Gate: `flake.nix` written; `nix flake show /tmp/lojix-e2e/vm-target#` lists
`nixosConfigurations.target`. No host mutation.

### 2 · Resolve the runner identity and wire the ssh alias

```sh
# the identity the daemon will present from Prometheus as user li
ssh prometheus.goldragon.criome 'ls ~/.ssh/*.pub 2>/dev/null; ssh-add -L 2>/dev/null || echo NO-AGENT'
```

Pick the pubkey (generate a throwaway keypair under `/tmp/lojix-e2e/` if `li`
has none) and paste it into the flake's `authorizedKeys` from Step 1. Then write
the user-level alias mapping the fixture's derived name to the hostfwd port —
this is the whole networking bridge, and it touches only `~/.ssh`, never host
config or DNS (report 2 §networking, report 1 §5):

```sshconfig
# ~/.ssh/config.d/lojix-e2e   (Include it from ~/.ssh/config, or append inline)
Host dune.fieldlab.criome
  HostName 127.0.0.1
  Port 2222
  User root
  IdentityFile /tmp/lojix-e2e/<runner-key>     # or the resolved existing key
  StrictHostKeyChecking accept-new
  UserKnownHostsFile /tmp/lojix-e2e/known_hosts
```

Gate: `ssh -G dune.fieldlab.criome` (from `li` on Prometheus) shows
`hostname 127.0.0.1`, `port 2222`, `user root`. `dune.fieldlab.criome` does NOT
resolve via DNS and must not — the alias is the only resolution path
(`getent hosts dune.fieldlab.criome` → NO_RESOLVE is expected and correct).

### 3 · Build the VM image — NON-MUTATING eval/build, no run yet

```sh
ssh prometheus.goldragon.criome '
  nix build /tmp/lojix-e2e/vm-target#nixosConfigurations.target.config.system.build.vmWithBootLoader \
    -o /tmp/lojix-e2e/vm-runner'
```

`vmWithBootLoader` (not `system.build.vm`) installs a real systemd-boot loader on
an ESP in the qcow2 — the only flavor where `Boot`/`BootOnce` mean anything
(report 1 §4, §7). This is a pure build: it produces the runner script + closure,
starts no VM, mutates no host config.

Gate: `/tmp/lojix-e2e/vm-runner/bin/run-*-vm` exists; the build pulls qemu via
nix (`nix eval --raw nixpkgs#qemu.outPath` already resolved, report 4). Nothing
running yet.

### 4 · Boot the throwaway VM (detached) and confirm reachability

```sh
ssh prometheus.goldragon.criome '
  systemd-run --user --unit=lojix-e2e-vm --collect -- /tmp/lojix-e2e/vm-runner/bin/run-*-vm'
```

A `--user` transient unit so the VM outlives the launching ssh (report 1). The
runner auto-enables KVM from the mode-666 `/dev/kvm`. First boot installs the
initial NixOS (sshd + runner key) into the persistent qcow2.

Gate (poll until green, then this is the reachability proof the daemon depends
on):

```sh
ssh prometheus.goldragon.criome '
  systemctl --user is-active lojix-e2e-vm;
  ssh -o BatchMode=yes -o ConnectTimeout=5 dune.fieldlab.criome true && echo VM-SSH-OK'
```

`VM-SSH-OK` means `root@dune.fieldlab.criome` (via the alias → hostfwd) accepts
the runner key. If this fails, do NOT proceed — the daemon's copy/activate would
fail at the ssh hop. No deploy has run; the VM is a bare first-boot image.

### 5 · Build the lojix binaries (on Prometheus)

```sh
# in the lojix checkout on Prometheus
ssh prometheus.goldragon.criome 'cd <lojix-checkout> && cargo build --release --features nota-text'
```

`--features nota-text` is load-bearing for the CLI clients (`lojix`,
`meta-lojix`) so they accept inline NOTA; without it they reject with
`Error::NotaTextUnsupported` (`client.rs:110-113,169-172`). The daemon and
`lojix-write-configuration` do not need it. Binaries land in
`target/release/{lojix-daemon,lojix,meta-lojix,lojix-write-configuration}`.

Gate: all four binaries exist and `--version`/`--help`-equivalent (run one
harmless `lojix`/`meta-lojix` invocation that errors cleanly) shows they load.

### 6 · Write the daemon startup rkyv and launch the daemon (detached)

Encode the NOTA config to the binary startup file (the NOTA→rkyv boundary; the
owner socket mode must NOT grant "other" access — use `384` = `0o600`,
`daemon.rs:126-131`):

```sh
ssh prometheus.goldragon.criome '<lojix>/target/release/lojix-write-configuration \
  "(ConfigurationWriteRequest (/tmp/lojix-e2e/run/ordinary.sock 432 /tmp/lojix-e2e/run/owner.sock 384 /tmp/lojix-e2e/state /tmp/lojix-e2e/run/startup.rkyv))"'
# -> (ConfigurationWritten [/tmp/lojix-e2e/run/startup.rkyv])
```

Launch the daemon detached so it survives the launching ssh (this is the daemon
*process* survival; distinct from the in-flight-deploy survival the daemon
already implements, report 3 §3):

```sh
ssh prometheus.goldragon.criome '
  systemd-run --user --unit=lojix-daemon-e2e --service-type=exec \
    --setenv=PATH=/run/current-system/sw/bin \
    <lojix>/target/release/lojix-daemon /tmp/lojix-e2e/run/startup.rkyv'
```

Gate: the two sockets exist at the configured modes
(`ls -l /tmp/lojix-e2e/run/*.sock` → ordinary `srw-rw----`/`0660`, owner
`srw-------`/`0600`); a harmless ordinary-socket read returns cleanly. Confirm
the event-log query verb the built binary accepts (resolves conflict #3) with an
empty-range read:

```sh
ssh prometheus.goldragon.criome 'LOJIX_ORDINARY_SOCKET=/tmp/lojix-e2e/run/ordinary.sock \
  <lojix>/target/release/lojix "(Query ((ByEventLog (0 0))))"'
```

If that errors, fall back to `(ReadEventLog (EventLogRange 0 0))`. Record which
form works; use it for all observation below.

### 7 · NON-MUTATING pipeline proof — Eval, then Build (no VM activation)

This is the gate that proves eval → build → (copy) lands BEFORE anything
activates. `Eval`/`Build` do not activate (`DeployAction::activates()` is false,
`schema_runtime.rs:244-256`); `build_attribute` present skips horizon
materialization (`needs_horizon_materialization == build_attribute.is_none()`,
`schema_runtime.rs:379-426`).

Step 7a — Eval (lightest: stops at the realised `.drv`):

```sh
ssh prometheus.goldragon.criome 'LOJIX_OWNER_SOCKET=/tmp/lojix-e2e/run/owner.sock \
  <lojix>/target/release/meta-lojix \
  "(Deploy ((System (fieldlab dune OsOnly /dev/null github:LiGoldragon/CriomOS-test-cluster Eval None [] (dune-toplevel)))))"'
```

Step 7b — Build (realises the full closure; on this build_attribute path the
copy step still runs, activation does not):

```sh
ssh prometheus.goldragon.criome 'LOJIX_OWNER_SOCKET=/tmp/lojix-e2e/run/owner.sock \
  <lojix>/target/release/meta-lojix \
  "(Deploy ((System (fieldlab dune OsOnly /dev/null github:LiGoldragon/CriomOS-test-cluster Build None [] (dune-toplevel)))))"'
```

Field order is positional (`SystemDeployment`,
`meta-signal-lojix/schema/lib.schema:87-97`): `cluster=fieldlab node=dune
kind=OsOnly source=/dev/null flake=github:LiGoldragon/CriomOS-test-cluster
action=Eval|Build builder=None substituters=[] build_attribute=(dune-toplevel)`.
`/dev/null` is the unused-on-this-path source placeholder.

Gate: each returns `(Deployed (AcceptedDeploy (DeploymentIdentifier
DatabaseMarker)))` (capture the identifier); the event log
(`lojix "(Query ((ByEventLog (0 1000))))"`) advances `Submitted → Building →
Built` for Build (and `Copying` if copy runs), with **no** `Activating`/
`Activated` and **no change inside the VM** (re-`ssh dune.fieldlab.criome
'readlink /run/current-system'` — unchanged from first boot). If Build does not
reach `Built`, STOP and debug the pipeline before any activating deploy.

### 8 · The activating deploy — BootOnce full-OS into the VM

Now, and only now, activate. `FullOs` for the full-OS S5 goal; `BootOnce` is the
disconnect-safe activation (PID-1-owned transient unit on the VM,
`schema_runtime.rs:506-520,2459-2471`):

```sh
ssh prometheus.goldragon.criome 'LOJIX_OWNER_SOCKET=/tmp/lojix-e2e/run/owner.sock \
  <lojix>/target/release/meta-lojix \
  "(Deploy ((System (fieldlab dune FullOs /dev/null github:LiGoldragon/CriomOS-test-cluster BootOnce None [] (dune-toplevel)))))"'
```

Gate: `(Deployed (AcceptedDeploy ...))` returned; event log reaches
**`Activated`** for this identifier (note: there is no `Activating` event-log
phase — the log goes `Copying` then `Activated`, `schema_runtime.rs:984-987`);
`lojix "(Query ((ByNode (fieldlab dune None))))"` shows a generation in the
`BootPending` slot (BootOnce → `BootPending`, `schema_runtime.rs:1802`). The
boot-once journal on the VM
(`ssh dune.fieldlab.criome "journalctl -u 'lojix-boot-once-*'"`) shows the final
`boot-once: oneshot=<NEW> persistent-default=<OLD>` line
(`schema_runtime.rs:2452`).

### 9 · Confirm the deploy actually landed (reboot the VM once)

```sh
ssh prometheus.goldragon.criome 'ssh dune.fieldlab.criome "readlink /run/current-system; nixos-version"'   # before
ssh prometheus.goldragon.criome 'ssh dune.fieldlab.criome "systemctl reboot" || true'
# wait for the VM ssh to come back (poll Step 4 gate), then:
ssh prometheus.goldragon.criome 'ssh dune.fieldlab.criome "readlink /run/current-system; nixos-version"'   # after
```

Gate: after the reboot, `/run/current-system` points at the deployed
`dune-toplevel` closure (the BootOnce one-shot booted the NEW generation). This
is the "full OS deploy that took effect across a reboot" half of `se72`.

### 10 · S4b proof — client → daemon disconnect survival

The reply lands synchronously on admit, BEFORE any pipeline effect
(`daemon.rs:344-350`), so the deploy is already decoupled the moment
`meta-lojix` returns. To exercise an in-flight connection drop:

```sh
# issue a fresh BootOnce deploy from a shell whose connection you then sever
ssh prometheus.goldragon.criome 'LOJIX_OWNER_SOCKET=/tmp/lojix-e2e/run/owner.sock \
  <lojix>/target/release/meta-lojix "(Deploy ((System (fieldlab dune FullOs /dev/null github:LiGoldragon/CriomOS-test-cluster BootOnce None [] (dune-toplevel)))))"' &
CLIENT_SSH=$!
# immediately kill the carrying ssh (client gone mid-pipeline)
kill -9 $CLIENT_SSH
```

Gate: with the client gone, re-issue the observation Query against the daemon's
own event log and confirm the deploy still advances to `Activated` for that
identifier (`lojix "(Query ((ByEventLog ...)))"`). Completion **with the client
gone** is the S4b proof.

### 11 · S4a proof — daemon → target disconnect survival (BootOnce unit)

During a BootOnce activation, drop the daemon→VM ssh and confirm the target-side
transient unit completes independently:

```sh
# while activation is running, kill the daemon's ssh/nix child to the VM:
ssh prometheus.goldragon.criome "pkill -f 'ssh.*dune.fieldlab.criome' || true"
# the transient unit is owned by the VM's PID 1, not that ssh — confirm on the VM:
ssh prometheus.goldragon.criome 'ssh dune.fieldlab.criome "journalctl -u '\''lojix-boot-once-*'\''"'
```

Gate: the boot-once journal (matched by the **glob** `lojix-boot-once-*`, NOT the
deterministic cursor name — see the unit-name gap below) shows the script
reaching its final `boot-once: oneshot=… persistent-default=…` line and the unit
`dead`/auto-reaped (`--collect`), proving it ran to completion after the daemon's
ssh died (`schema_runtime.rs:2380-2382,2456-2471`).

### 12 · Teardown — return to zero, host untouched

```sh
ssh prometheus.goldragon.criome '
  systemctl --user stop lojix-daemon-e2e lojix-e2e-vm 2>/dev/null || true;
  rm -rf /tmp/lojix-e2e ~/.ssh/config.d/lojix-e2e'
```

(Also remove the `Include ~/.ssh/config.d/lojix-e2e` line if one was added.)

Gate: no `lojix-e2e`/`lojix-daemon-e2e` user units active; `/tmp/lojix-e2e`
gone; Prometheus `systemctl is-system-running` still `running`, its generation
unchanged. Nothing persisted; the host config was never touched.

## Success criteria (the run passed iff all hold)

1. Step 7 Build reached `Built`/`Copying` with **no** VM-side change — pipeline
   proven before any activation.
2. Step 8 reached event-log `Activated`; the VM shows a `BootPending` generation
   and the boot-once completion journal line.
3. Step 9: after one reboot, the VM's `/run/current-system` is the deployed
   `dune-toplevel` — the full OS took effect.
4. Step 10: a deploy completed to `Activated` with the `meta-lojix` client
   killed mid-flight (S4b).
5. Step 11: the `lojix-boot-once-*` unit completed on the VM after the daemon's
   ssh to the VM was killed (S4a).
6. Step 12: `/tmp/lojix-e2e` removed, both user units gone, Prometheus's own
   generation and `systemctl is-system-running` unchanged throughout.

## Resource and safety bounds

- **Resources.** VM at 4 GiB / 4 cores + the toplevel-closure build fit
  trivially in Prometheus's 121 GiB free / 32 cores (report 4). The only bound
  to watch is **disk** for the qcow2 + closure + `nix copy`'d store paths — keep
  ≥ ~30 GiB free under `/tmp` and `/nix/store`; CPU/RAM are not constraints.
- **Throwaway reset.** A broken deploy kills only the VM. Reset is `rm -rf
  /tmp/lojix-e2e` + stopping the two `--user` units (Step 12). Inside the VM,
  BootOnce additionally self-heals (reboot 2 returns to the OLD generation,
  `schema_runtime.rs:2435-2453`), but the real reset is deleting the image.
- **Prometheus host config is never mutated.** qemu and the lojix binaries come
  via `nix`/cargo (no host package install); the daemon runs as an unprivileged
  `li` process in a `--user` unit; the `nix copy`/`switch-to-configuration`/
  `bootctl` targets are ONLY `ssh-ng://root@dune.fieldlab.criome` (the VM),
  never the host. No `nixos-rebuild`, no host `nix copy`, no host service
  start/stop, no `/etc` write, no DNS/networking change (the bridge is a
  user-level `~/.ssh/config` alias + qemu hostfwd). Prometheus is the
  LargeAiRouter — its networking and system config stay exactly as found.

## Risk table

| # | Risk | Likelihood | Impact | Mitigation / gate |
|---|---|---|---|---|
| R1 | Runner pubkey baked into the VM ≠ the identity the daemon actually presents → copy/activate ssh-auth fails | Medium | Blocks deploy | Step 2 resolves the exact `li`-on-Prometheus identity; Step 4 gate (`VM-SSH-OK`) proves `root@dune.fieldlab.criome` accepts it before any deploy |
| R2 | ssh alias collides or `dune.fieldlab.criome` unexpectedly resolves via DNS, routing the daemon elsewhere | Low | Wrong target | Step 2 gate asserts `ssh -G` resolves to `127.0.0.1:2222` and confirms NO DNS resolution; alias is user-level only |
| R3 | Wrong cluster name (`goldragon` from reports 3/4) → address `root@dune.goldragon.criome` has no alias, copy fails | Medium (carried in sibling reports) | Blocks deploy | Reconciled: use `fieldlab` everywhere; alias keyed on `dune.fieldlab.criome` matching the fixture's baked horizon |
| R4 | Using `dune-nspawn-toplevel` (container) → BootOnce/bootctl meaningless, S4a unprovable | Medium (in reports 3/4) | Invalidates disconnect proof | Reconciled: use `dune-toplevel` (full OS) + `vmWithBootLoader` (real ESP/bootctl) |
| R5 | Stateless `system.build.vm` instead of `vmWithBootLoader` → no real loader, Boot/BootOnce no-op | Low | Invalidates reboot/disconnect proof | Step 3 explicitly builds `vmWithBootLoader`; Step 9 reboot gate would catch a no-op loader |
| R6 | BootOnce live unit name is `lojix-boot-once-{secs:x}-{pid:x}`, not the deterministic cursor `lojix-boot-once-deploy-<id>` (`schema_runtime.rs:2544-2550` vs `512-517`) | Confirmed | S4a observation by exact name fails; daemon-restart resume polls a never-used name | Observe with the glob `lojix-boot-once-*` (Step 11); flag the resume-path mismatch to operator (see open questions) |
| R7 | `WatchDeployments` does not stream events yet (day-one `2tfa`) | Confirmed | No live push | Observe by polling `Query (ByEventLog ...)`; `WatchDeployments` only exercises the handshake |
| R8 | First-boot qcow2 install slow / VM ssh not up when daemon deploys | Medium | Step 8 ssh hop fails | Step 4 gate polls `VM-SSH-OK` before proceeding; do not advance until green |
| R9 | Owner socket mode grants "other" access → daemon refuses at startup | Low | Daemon won't start | Step 6 uses owner mode `384` (`0o600`); ordinary `432` (`0o660`) |
| R10 | Event-log query verb (`Query (ByEventLog)` vs `ReadEventLog`) mismatch with the built binary | Low | Observation command errors | Step 6 confirms the accepted form with an empty-range read before relying on it |
| R11 | Disk exhaustion on `/tmp` or `/nix/store` during build/copy | Low | Build/copy fails | Step 0 confirms ≥ ~30 GiB free; teardown reclaims it |

## Open questions / unresolved gaps before the live run

- **Runner identity (R1).** The exact ssh identity `li` presents from Prometheus
  is not yet pinned in any report — Step 2 must resolve it (existing key vs. a
  throwaway keypair) and bake the matching pubkey into the VM flake. This is the
  single most likely blocker.
- **Build-then-copy on the `build_attribute` path.** Reports state that with
  `build_attribute` present the daemon builds the self-contained output and that
  `Build` does not activate; whether `Build` also performs the `nix copy` to the
  VM (vs. copy happening only on activating actions) should be confirmed at Step
  7b's gate by watching for a `Copying` event — it changes whether Step 7
  already exercises the ssh-ng copy hop or whether Step 8 is the first copy.
- **BootOnce unit-name reconcile (R6).** Live activation uses the time/pid unit
  name; the daemon-restart resume path intends to poll the deterministic
  cursor name. For S5 this only affects daemon-restart resume (not the disconnect
  proofs, which use the glob), but it is a real S4b/S5 reconcile gap for the
  operator: either thread the deterministic name into `systemd_run_invocation`
  or have resume glob `lojix-boot-once-*`.
- **`fieldlab.nota` proposal source on the `build_attribute` path.** `source`
  (`/dev/null` placeholder) is unused for eval when `build_attribute` is set, but
  is still a required field; if a later production-path run drops
  `build_attribute` to exercise horizon materialization, the source must be the
  real `clusters/fieldlab.nota`. Out of scope for this S5 fixture run; noted so
  it is not conflated.

## Hard-safety log

This synthesis mutated nothing live. Beyond the read-only inspections recorded in
reports 1–4, the only new commands run for this synthesis were read-only file
reads of the `CriomOS-test-cluster` fixture (`flake.nix`,
`fixtures/horizon/dune.json`, `clusters/`) and the `lojix`/`horizon-rs` source
(`schema_runtime.rs`, `name.rs`) to reconcile the cluster name and build
attribute. No VM run, no deploy, no `nix build`, no host contact.
