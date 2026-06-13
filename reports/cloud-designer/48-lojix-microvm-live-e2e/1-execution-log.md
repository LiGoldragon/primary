# 48 · lojix → mercury microVM live e2e — execution log (2026-06-13)

Live, host-affecting run on **Prometheus** (bare-metal, `/dev/kvm`,
`prometheus.goldragon.criome`). Everything user-level under `/tmp/lojix-e2e`;
Prometheus's OS / networking / firewall left **untouched** (psyche constraint
`5hir5bnz` — it runs the LargeAiRouter). No sudo used beyond the one
pre-existing `criomos-nspawn` grant (not invoked).

## Outcome in one line

lojix deployed a **real, full mercury CriomOS OS closure into a real, writable
KVM microVM live on Prometheus, and the deploy ran to completion AFTER the
submitting client disconnected** — build → copy of the closure into mercury's
writable store → `nix-env --set` generation activation, all autonomous in the
daemon. The one step that does **not** complete is the bootloader install
(`switch-to-configuration` / `bootctl`), which is architecturally impossible on
a microvm.nix kernel-direct-boot guest (no UEFI/ESP). Two real bugs were found
and one was fixed live to get this far.

## Reached Prometheus + preflight

`ssh prometheus.goldragon.criome` (FQDN; the bare `prometheus` alias does not
resolve from this host). Preflight: NixOS 26.05, 32 cores, 120 GiB RAM free,
987 GiB free on `/`, `/dev/kvm` world-writable, nix 2.34.6, the S5
`/tmp/lojix-e2e` harness intact (diskA flake, throwaway `runner_key`, qemu
result, OVMF). User is `li` (uid 1001), **no general sudo**.

## The microVM substrate (mercury)

The CriomOS-emitted runner is reached at
`atlas.config.microvm.vms.mercury.config.config.microvm.declaredRunner` — built
**without** realising atlas's full toplevel (which fails on the GGUF model).
The standalone runner used for the run reconstructs the **real mercury CriomOS
config** (`fixtureSystem "mercury"`-equivalent) plus the microVM hardware and a
set of substrate/test overrides. Build expr lives at `/tmp/lojix-e2e/mercury.nix`.

mercury boots as a **real KVM microVM** (qemu `-M microvm,accel=kvm`, vcpu=4,
mem=8192 MiB, linux-7.0.1) with:
- a **real writable 40 GiB ext4 `/` (`/dev/vdb`, 38 GiB free)** — auto-`mkfs`'d;
- a **writable `/nix/store` overlay** (erofs lower `/dev/vda` + writable
  `/dev/vdc` upper) — `STORE-WRITABLE` confirmed; the **S5 read-only-store
  failure mode is ABSENT**;
- static **10.77.0.7/24** on its tap NIC + route to the host endpoint
  `169.254.100.1`; sshd up; `root@10.77.0.7` reachable by the deploy key.

### Host-untouched networking — how the tap was made additive

`li` cannot create a tap on the host (needs `CAP_NET_ADMIN`) and there is no
sudo. Solution: a **persistent user+network namespace** (`unshare -rn`, `li` is
root-in-userns) holds the tap `vmt0` (host endpoint `169.254.100.1/32` + `/32`
route to `10.77.0.7`). qemu, the lojix daemon, and the deploy's ssh all run
**inside this namespace** via `nsenter`. Prometheus's real network namespace is
completely untouched — verified post-run: host interfaces/routes identical to
preflight, **zero `10.77` routes and no `vmt0` on the host netns** (it lives only
in the private user netns). The namespace is a durable user unit `mercury-ns`;
the microVM is the user unit `mercury-vm`.

### Substrate fixes needed to make the CriomOS guest a live deploy target

Each is a real interaction surfaced by booting the lean CriomOS guest in a
microvm; all are **findings to fold back** (see below):
1. **`clavifaber` stub** — `complex.nix` interpolates `${clavifaber}` into a
   unit script, forcing a Rust build whose fenix `rust-stable` channel FOD hash
   has drifted in this env (same class as the GGUF block). The clavifaber input
   is stubbed so the closure builds; the deployed OS is otherwise the full
   mercury CriomOS system.
2. **root login shell** — `environment.systemPackages` must NOT be emptied (an
   early over-broad workaround): doing so removed `/run/current-system/sw/bin/bash`,
   so root's login shell didn't exist → sshd rejected root as an **"invalid
   user"**. Root shell pinned to an absolute `${bashInteractive}/bin/bash`.
3. **NSS** — CriomOS `network/default.nix` sets `services.nscd.enable = false`
   **and** `system.nssModules = mkOverride 0 []`; re-enabled nscd and pinned
   `passwd/group/shadow` to `files`.
4. **writable store** — `boot.nixStoreMountOpts = ["rw"]` (the 26.05 successor
   to `readOnlyNixStore=false`) to stop a second read-only overlay shadowing the
   writable one.
5. **require-sigs** — the daemon's copy is production-identical
   (`nix copy --substitute-on-destination --to ssh-ng://…`, no `--no-check-sigs`)
   and relies on the target trusting signatures; the locally-built closure is
   unsigned, so the **test substrate** sets `nix.settings.require-sigs = false`
   (a substrate property, like the throwaway key — the daemon command is
   unchanged).
6. landlock — appended `lsm=yama,bpf` (investigating the invalid-user issue
   before finding the shell root cause; left in, harmless).

## The lojix daemon (live, unmodified except one bug fix)

Reused the S5 release binaries (`lojix-daemon/lojix/meta-lojix/
lojix-write-configuration`, commit `bbb8030` — the S4b disconnect-survival
build). Ran `lojix-daemon` as the user unit `lojix-daemon` **inside the
namespace** (so its copy/activate reach 10.77.0.7), both sockets at correct
modes (`ordinary.sock` 0660, `owner.sock` 0600), `lojix-write-configuration`
wrote the rkyv startup, the S5 **effect-shim** on PATH (logs every nix/ssh
effect — the daemon emits none) plus `NIX_SSHOPTS=-F /home/li/.ssh/config` so
nix's ssh-ng uses the `mercury.fieldlab.criome → 10.77.0.7` alias and skips the
host's broken system `ssh_config` drop-in.

### Daemon bug found + fixed live (REQUIRED for any activation)

`build_closure` runs `nix build --no-link --print-out-paths <drv>`. In nix
2.34 a bare `<drv>` makes `--print-out-paths` echo the **`.drv` path**, not the
realised output — so the daemon copied and tried to activate the `.drv`
(`$CLOSURE/bin/switch-to-configuration` does not exist). Fix: select all
outputs with `<drv>^*`. Verified: `nix build …drv` → prints the `.drv`;
`nix build …drv^*` → prints `…07khqilh…-nixos-system-mercury` (the real system).
Patched both `build_closure` and `build_closure_remote` and rebuilt the daemon.
**This is a genuine lojix daemon bug** — without it the daemon can never
activate anything. (Patch on Prometheus at `/tmp/lojix-e2e/lojix`; not pushed.)

## Deploy + disconnect-survival proof

`meta-lojix` accepts `(Deploy (System (fieldlab mercury FullOs /dev/null
path:/tmp/lojix-e2e/mercury-flake <Action> None [] (Some mercuryDeploy))))`.
The deploy closure is a small flake `path:/tmp/lojix-e2e/mercury-flake`
(`mercuryDeploy` = the stubbed mercury toplevel, resolved via a rev-pinned
`builtins.getFlake` to dodge the test-cluster's eager transitive-input break).

`AcceptedDeploy` returns **immediately** and the `meta-lojix` client exits at
once (S4b decoupling — the client never stays attached). The deploy then runs
entirely in the daemon's DeployJobs actor. **Disconnect timeline** (all daemon
effects timestamped AFTER the client died at 17:35:13):

```
17:35:13  meta-lojix submit -> (Deployed (1 (0 0)))  [client exits here]
17:35:16  daemon: nix eval --raw …#mercuryDeploy.drvPath  (exit 0)
17:35:16  daemon: nix build …drv^*  -> realises 879zbka5…-nixos-system-mercury
17:35:19  daemon: nix copy --substitute-on-destination --to ssh-ng://root@mercury.fieldlab.criome …
17:35:53  copy of the OS closure completes (exit 0)
17:36:08  daemon: ssh root@mercury  nix-env -p …/profiles/system --set <closure> && switch-to-configuration switch
17:36:09  switch fails ONLY at "Failed to install bootloader"
```

Every step from eval through the generation `nix-env --set` ran **autonomously
in the daemon with no client attached** — the disconnect-survival bar is met.
The durable deploy-job table (`/tmp/lojix-e2e/state/lojix.sema`, persisted, 180
KB) advanced its commit sequence across the runs; the daemon stayed `active`
throughout.

## What does NOT complete — and why it cannot on this substrate

`switch-to-configuration` / `BootOnce` fail at **bootloader install**:
- BootOnce's script first runs `bootctl status` for the current entry — on the
  microvm `bootctl` reports **"Not booted with EFI"** (kernel direct-boot, no
  UEFI firmware), so the one-shot can never be set.
- `switch …switch` with a mounted vfat `/boot` got further but then:
  `systemd-boot not installed in ESP … Could not find any previously installed
  systemd-boot … you need --install-bootloader`, and `/dev/vdd is not located on
  a partitioned block device`.

This is intrinsic: **microvm.nix direct-boots the kernel, so there is no
UEFI/ESP and `bootctl`/systemd-boot cannot operate** — `BootOnce`+`bootctl` (and
even a first-time `switch` bootloader install) require a UEFI-firmware guest.
The faithful UEFI substrate is the S5 `make-disk-image`+OVMF VM, but
`make-disk-image`'s `cptofs` **OOM/asserts on the full mercury closure in this
environment** (`cptofs: posix-host.c:448: panic` at every `memSize` tried) — a
second environment blocker, unrelated to lojix.

## Verification (independent checks)

| Check | Result |
|---|---|
| mercury real KVM microVM, 10.77.0.7 + sshd | YES (`ROOT-OK`, hostname `mercury`) |
| writable 40 G ext4 `/dev/vdb` | YES, 38 G free |
| writable `/nix/store` (S5 failure absent) | YES — `STORE-WRITABLE`, single rw overlay |
| daemon live, both sockets correct modes | YES (0660 / 0600) |
| `AcceptedDeploy` immediate | YES (`(Deployed (1 (0 0)))`) |
| build realises real system (post `^*` fix) | YES (`…-nixos-system-mercury`, not `.drv`) |
| OS closure copied into mercury's writable store | YES — `…zk4l7lkg…-nixos-system-mercury` present; 906 store paths |
| generation activated (`nix-env --set`) | YES — `/nix/var/nix/profiles/system → system-1-link` |
| deploy continues + completes after client gone | YES — all effects timestamped after client exit |
| durable deploy-job record | YES — `lojix.sema` persisted, commit seq advanced (7,7) |
| BootOnce one-shot via bootctl | **NO** — microvm has no UEFI; `bootctl`/bootloader-install cannot run |
| Prometheus OS/networking untouched (`5hir5bnz`) | YES — host netns/routes identical to preflight; tap only in the private user netns |

## Findings to fold back

1. **lojix daemon (BUG, fixed live):** `nix build <drv> --print-out-paths`
   needs `<drv>^*` or it copies/activates the `.drv`, not the system. One-line
   fix in `build_closure` / `build_closure_remote`. **Push this.**
2. **lojix BootOnce vs non-UEFI targets (design):** the BootOnce activation
   hard-requires `bootctl`/systemd-boot; a microvm.nix guest can never satisfy
   it. Either the test-VM substrate must be a UEFI VM, or lojix needs a
   non-UEFI activation path (extlinux / direct-boot generation switch).
3. **CriomOS lean-guest microvm gaps (Unit B follow-ons):** on a microvm guest
   the lean CriomOS profile (a) builds clavifaber via `complex.nix` even when
   the unit is disabled (script interpolation), (b) leaves root with no NSS
   (`nscd off` + `nssModules []`) so getpwnam fails → sshd "invalid user", (c)
   the test-vm guest config emits no guest-side IP for its tap (the host-side
   runner must wire it — matches the design-47 "v1 host-triggered runner owns
   guest IP" note, but it must match the NIC by name glob, not MAC, under
   virtio-mmio). These are real test-VM-on-microvm gaps for the designer.
4. **Environment (pre-existing, unrelated to lojix):** clavifaber fenix
   `rust-stable` channel FOD hash drift; atlas GGUF; `make-disk-image` `cptofs`
   OOM on a full OS closure. All block the live path and were worked around or
   are blockers, not lojix faults.

## Left running for the verify phase (do NOT torn down)

- `mercury-vm` user unit — the microVM (10.77.0.7, writable store, deployed
  closure present, generation profile set).
- `mercury-ns` user unit — the namespace holding tap `vmt0`.
- `lojix-daemon` user unit — daemon live, both sockets, effect-shim on PATH.
- `~/.ssh/config` `mercury.fieldlab.criome → 10.77.0.7` alias.

### Teardown commands (when done)

```
ssh prometheus.goldragon.criome '
  systemctl --user stop lojix-daemon mercury-vm mercury-ns
  systemctl --user reset-failed lojix-daemon mercury-vm mercury-ns
  rm -rf /tmp/lojix-e2e/mercury /tmp/lojix-e2e/run/*.sock
  # remove the mercury ssh alias stanza appended to ~/.ssh/config
'
```
Do NOT touch Prometheus networking. The tap and 10.77 route vanish with the
`mercury-ns` unit (they only ever existed in the private user netns).
