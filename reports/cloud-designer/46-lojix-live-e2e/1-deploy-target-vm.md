# lojix S5 live e2e — the deploy-target VM on Prometheus

Read-only reconnaissance. Every claim grounded in a file read, a Spirit
record, or a read-only command against Prometheus. Mutated nothing.

## 1 · The psyche's model (Spirit `7let`, refines `se72`)

Verbatim decision, retrieved via `spirit "(Observe (Any Any (ContainsText vm) Any None Any Any Any))"` → `LookupStash 6`:

`7let` (Clarification, High/Medium): *"the lojix cutover e2e is harmless
because lojix deploys a full OS INTO a throwaway KVM-hosted VM, so a
broken deploy kills only the VM and never the host; it does NOT require
reconfiguring the host to declaratively run a microVM. Prometheus is a
fine host — bare-metal with AMD-V, a live /dev/kvm, 32 cores and 124 GiB
free — running a transient qemu KVM VM via nix with no change to
Prometheus production config or networking. The earlier
vm-testing-host-module framing … was designer over-engineering and not
psyche intent. Use the host KVM infra, deploy into the VM, leave the host
untouched."*

So: **no `microvm.nix` host module, no tap, no `networking.hosts`
projection on Prometheus.** Run a plain qemu/KVM VM as user `li`, deploy
into it, host generation untouched. `se72` (the parent Decision) still
sets the bar: full OS deploy that survives SSH disconnect; `5hir5bnz`
(don't break Prometheus networking) is honoured for free by hostfwd.

## 2 · Prometheus host facts (confirmed live, read-only)

`ssh prometheus.goldragon.criome '<inspect>'` (resolves via getent to
IPv6 `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f`, an overlay /7 global addr):

| Fact | Value | How confirmed |
|---|---|---|
| NixOS | `26.05.20260422.0726a0e (Yarara)` | `nixos-version` |
| /dev/kvm | `crw-rw-rw-` mode 666, **world-writable** | `ls -l /dev/kvm`; `test -w` → `KVM-WRITABLE-by-li` |
| AMD-V | `svm` flag present | `grep svm /proc/cpuinfo` |
| Cores | 32 | `nproc` |
| Memory | 124.5 GiB total, 121.4 GiB available | `/proc/meminfo` |
| qemu in system profile | **absent** — `NO-QEMU`, `/run/current-system/sw/bin/qemu*` no matches | `command -v qemu-system-x86_64` |
| nix | 2.34.6, flakes usable, builds from `github:NixOS/nixpkgs` (cache reachable: built `hello-2.12.3`) | `nix --version`, `nix eval` |
| login user | `li` (uid 1001), groups: users,audio,video,dialout,systemd-journal,plugdev,nixdev (NOT `kvm` — but 666 mode makes that moot) | `id` |

Key consequence: qemu must be pulled **via nix** (`nix run nixpkgs#qemu`
or as a VM-runner script dependency); `li` can open `/dev/kvm` directly.

## 3 · How lojix actually reaches and activates a target

From `lojix/src/schema_runtime.rs` — these fix the VM's requirements:

- **Address**: `SshTarget::root_at_node` →
  `root@<node>.<cluster>.criome` (`:2155-2176`), used as
  `ssh-ng://root@<domain>` for copy (`ssh_uri`, `:2186`) and `ssh -o
  BatchMode=yes root@<domain>` for activate (`remote_invocation`,
  `:2194-2205`). **The VM must be reachable at a name that resolves to
  it, and it must accept `root` over ssh with lojix's key.** Address is
  computed from cursor cluster+node, not configurable per-deploy.
- **Copy**: `nix copy --substitute-on-destination --to
  ssh-ng://root@<domain> <closure>` (`ClosureCopy::invocation`,
  `:2298-2312`). Requires `nix` + ssh-ng on the VM (any NixOS has it).
- **Activate** (`SystemActivation`, `:2390-2515`):
  - `Switch`/`Boot`: `nix-env -p /nix/var/nix/profiles/system --set
    <closure> && <closure>/bin/switch-to-configuration <switch|boot>`
    (`:2407-2411`).
  - `Test`: `switch-to-configuration test` only, no profile set
    (`:2404-2405`).
  - `BootOnce`: `systemd-run --unit=… --collect --wait
    --service-type=oneshot /bin/sh -c '<boot-once script>'`
    (`:2459-2471`) — owned by PID 1, survives the ssh drop. The script
    reads `bootctl status` Current Entry, `nix-env --set`,
    `switch-to-configuration boot`, then `bootctl set-default OLD` +
    `bootctl set-oneshot NEW` (`:2435-2453`).
  - `Boot`/`Switch` then **EFI-reconcile** via `bootctl set-default` /
    `bootctl set-oneshot ''` (`:2478-2508`).

**Therefore the target must be a real systemd-boot **UEFI** NixOS with a
mutable `/boot` and `bootctl`** for `Boot`/`BootOnce` to mean anything.

## 4 · Recommended VM flavor: `vmWithBootLoader` (UEFI disk image)

Two nixpkgs build attributes on a `nixosConfiguration` (from
`nixpkgs/nixos/modules/virtualisation/qemu-vm.nix`):

- `config.system.build.vm` — fast stateless runner; boots the closure
  directly via qemu kernel/initrd, **no real bootloader, /boot not a
  managed ESP**. `nixos-rebuild build-vm` produces this.
- `config.system.build.vmWithBootLoader` — builds a qcow2 with the
  **actual systemd-boot bootloader installed on a real ESP**; the VM
  boots through the loader. `nixos-rebuild build-vm-with-bootloader`
  produces this.

**Choose `vmWithBootLoader` with `boot.loader.systemd-boot.enable =
true` + `boot.loader.efi.canTouchEfiVariables = true` + an OVMF UEFI
firmware.** Only this makes the full activation matrix meaningful (see
§6). A stateless `system.build.vm` is fine for a Switch/Test-only smoke
but cannot exercise `Boot`/`BootOnce`/EFI-reconcile — the heart of
`se72`'s "full OS deploy that survives disconnect across a reboot."

### Build + run commands (run ON Prometheus, as `li`)

Author a tiny standalone flake (NOT CriomOS `nixosConfigurations.target`,
which needs horizon/deployment specialArgs — too heavy for a throwaway).
Minimal target module:

```nix
# vm-target/flake.nix — nixosConfigurations.target
{ inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }: {
    nixosConfigurations.target = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ({ modulesPath, ... }: {
        imports = [ "${modulesPath}/virtualisation/qemu-vm.nix" ];
        boot.loader.systemd-boot.enable = true;          # systemd-boot → bootctl works
        boot.loader.efi.canTouchEfiVariables = true;
        virtualisation = {
          graphics = false;
          diskImage = "/home/li/lojix-e2e/target.qcow2";  # persistent disk → reboot survives
          useEFIBoot = true;                              # OVMF UEFI firmware
          forwardPorts = [ { from = "host"; host.port = 2222; guest.port = 22; } ];
          memorySize = 4096; cores = 4;
        };
        services.openssh = { enable = true;
          settings = { PermitRootLogin = "yes"; PasswordAuthentication = false; }; };
        users.users.root.openssh.authorizedKeys.keys = [ "<OPERATOR_PUBKEY>" ];
        system.stateVersion = "25.11";
      }) ];
    };
  };
}
```

Build (eval/build only — no run, dry-run-checkable):
```sh
nix build .#nixosConfigurations.target.config.system.build.vmWithBootLoader -o /home/li/lojix-e2e/vm-runner
```
Run, detached so it survives the ssh that launched it (qemu pulled via
the runner's closure; KVM via mode-666 /dev/kvm):
```sh
systemd-run --user --unit=lojix-e2e-vm --collect -- /home/li/lojix-e2e/vm-runner/bin/run-*-vm
# (or: setsid nohup … & — but a --user transient unit is cleaner and survives the launching ssh)
```
The runner script enables KVM accel automatically when `/dev/kvm` is
present. First boot installs the initial NixOS (sshd + operator key)
into the persistent qcow2; lojix then deploys the NEXT generation into
the running VM.

## 5 · Reachable-ssh approach: **qemu user-mode + hostfwd** (recommended)

`virtualisation.forwardPorts` (or `-netdev user,hostfwd=tcp::2222-:22`)
gives `prometheus:2222 → VM:22` with **zero host network change** —
directly honours `7let`/`5hir5bnz` ("leave the host untouched"). Where
lojix runs reaches the VM via Prometheus's existing address.

The friction: lojix computes the target as
`root@<node>.<cluster>.criome` on **port 22** with no per-deploy
host/port override (`schema_runtime.rs:2155-2205`). Two clean ways to
bridge hostfwd to that fixed address (pick one for the runbook,
deciding-doc fodder for sibling reports):
- **Operator ssh config alias**: map the deploy's
  `<node>.<cluster>.criome` to `HostName prometheus…`, `Port 2222` in the
  lojix-runner's `~/.ssh/config`. No code change; the daemon's `ssh`/`nix
  copy --to ssh-ng://` pick it up. Cleanest for a throwaway.
- **hostfwd on 22 over an isolated address**: forward a dedicated
  Prometheus loopback/overlay address's port 22 to the VM — but binding
  :22 on the host risks colliding with Prometheus sshd; avoid.

A tap/bridge giving the VM its own routed Criome IP is the `se72`
"routed microVM" shape but is exactly the host-networking reconfig
`7let` rejected for this throwaway. **Use hostfwd + an ssh alias; do not
add a tap.** (If a future cutover wants the real routed-domain proof,
that is a separate host-touching task the psyche must authorize.)

## 6 · Operator-key wiring

- The VM's `users.users.root.openssh.authorizedKeys.keys` must carry the
  **public key of whatever identity the lojix daemon's `ssh`/`nix copy`
  use** (the daemon shells out to plain `ssh -o BatchMode=yes` and `nix
  copy --to ssh-ng://`, inheriting the runner's ssh agent/identity —
  `schema_runtime.rs:2194-2205`, `:2298-2312`).
- `PasswordAuthentication = false`, key-only; `PermitRootLogin = yes`
  because activation runs `nix-env`/`switch-to-configuration`/`bootctl`
  as root.
- Note: Prometheus's own `~li/.ssh/authorized_keys` is empty and we reach
  it by host trust (getent + known host trust), so the operator key for
  the VM is a separate concern — bake the lojix-runner's pubkey into the
  VM image at build time. Confirm the exact runner identity from where
  the daemon is launched (open item for sibling report on the daemon
  host).

## 7 · Which activation actions are meaningful, by flavor

| Action | `system.build.vm` (stateless, no loader) | `vmWithBootLoader` (UEFI + systemd-boot + persistent qcow2) |
|---|---|---|
| `Eval` / `Build` | meaningful (no target side) | meaningful |
| `Switch` | **meaningful** — sets system profile + `switch-to-configuration switch`, takes effect live | **meaningful** |
| `Test` | **meaningful** — non-persistent live activation | **meaningful** |
| `Boot` | **NOT meaningful** — no real bootloader; EFI-reconcile `bootctl set-default` has no ESP to write | **meaningful** — writes loader entry, reconciles EFI, takes effect next boot |
| `BootOnce` | **NOT meaningful** — script reads `bootctl status` / writes `set-oneshot`; no systemd-boot ⇒ fails | **meaningful** — the disconnect-survival headline case; needs `bootctl` + reboot |

For the `se72`/`up9q` "survives SSH disconnect across the activation,"
`BootOnce` is the load-bearing action (transient unit owned by PID 1 on
the VM), and it **requires `vmWithBootLoader`**. That is the decisive
reason to pick the bootloader VM over the stateless runner.

## 8 · Hard-safety log

Mutated nothing. On Prometheus ran only: `nixos-version`, `ls -l
/dev/kvm`, `test -w /dev/kvm`, `grep /proc/cpuinfo`, `nproc`,
`/proc/meminfo` read, `command -v`, `id`, `nix --version`, `nix eval`,
`nix build` of `hello` into the shared cache (a pure read-through build,
no host config change, no service touched). No VM run, no deploy, no
nixos-rebuild, no nix copy to a host, no service start/stop.
