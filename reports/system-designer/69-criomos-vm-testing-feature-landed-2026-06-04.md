# CriomOS VM-testing node feature — implemented + tested on `next`

System-designer lane. 2026-06-04. Implementation report — the feature designed
in report 67 is now landed on the CriomOS / CriomOS-home `next` branches and
tested (eval + a booted-VM runNixOSTest), with the per-node `gpuPassthrough`
option DISABLED on Prometheus. No deploy to any node.

## Intent anchors

- **Spirit 2630 / 7d326jk** — VM-based testing node using the best Linux VM
  technology to test CriomOS and its components, including visual/GPU cases
  such as chroma's gamma warmth a headless sandbox cannot exercise.
- **Spirit 2631 / 7hckmg8** — reachable via a Criome domain such as
  `vm-testing.<cluster>.criome` through `domain-criome` plus cluster networking.
- **Spirit 2632 / 76qdqown** — the per-node gpuPassthrough option (VFIO GPU
  passthrough, for the gamma visual test) is DISABLED on Prometheus: Prometheus
  is an AI node whose GPU must not be monopolized by `vfio-pci`. Prometheus runs
  the non-gamma harness + routed VM; the gamma passthrough test runs on a node
  where passthrough is acceptable.
- **Spirit 5hir5bnz** — the feature may land + deploy to Prometheus ONLY if it
  will not break networking (Prometheus is the cluster router). Non-breakage
  must be proven before any deploy; gated to cluster-operator.
- **Spirit 2623** — sandbox UI end-to-end testing (chroma is the first target).
- **Spirit 19e6mzu** — main-and-next branching model: designer works on `next`.

## What was implemented

### CriomOS (`next` branch, commit `c193127`)

- **`modules/nixos/vm-testing/default.nix`** — new module gated on the horizon
  node-service variant `VmTesting` (resolved by the existing
  `node-services.nix` `has`/`payload`, exactly like `TailnetClient`). Payload
  fields, with chosen-adjustable defaults: `gpuPassthrough : bool` (default
  **false**), `display` (default **Spice**), `gpu` (PCI id, default null =
  virtio-gpu mode). The module:
  - installs the QEMU/KVM runtime (`qemu_kvm`, `OVMF.fd`, `libvirtd`) + Spice
    tooling;
  - declares the persistent routed test microVM via `microvm.vms.vm-testing`
    (qemu hypervisor, tap interface, graphics) — the always-on
    human-viewable endpoint;
  - emits the provider-neutral Criome-domain projection
    `vm-testing.<cluster>.criome`: a `networking.hosts` entry resolving the
    name to the host node IP (matching `network/default.nix`'s
    `mkCriomeHostEntries` grain) plus a structured `config.criomos.vmTesting`
    surface for the `domain-criome` registration path;
  - **arms VFIO only when `gpuPassthrough = true`** — IOMMU `kernelParams`
    (`intel_iommu=on`, `amd_iommu=on`, `iommu=pt`), `vfio-pci.ids=<gpu>`, and
    the `vfio_pci`/`vfio`/`vfio_iommu_type1` modules in a separate `mkIf
    gpuPassthrough` branch. Driven entirely by Horizon payload data, never a
    hardcoded node name (CriomOS network-neutral rule). When false the whole
    branch is inert.
- **`modules/nixos/criomos.nix`** — imports the new module and (guarded on the
  input being present) the `microvm.nix` host module so the `microvm.vms.*`
  options exist. Inert unless a `VmTesting` node declares a VM.
- **`flake.nix`** — added the `microvm.url = github:astro/microvm.nix` input
  (`nixpkgs` follows) and the lock entry; wired `vm-testing-prometheus-policy`
  into `projectChecks`.
- **`checks/vm-testing-prometheus-policy/default.nix`** — eval-time check
  (isolated `evalModules`, same grain as `desktop-audio-policy`) asserting:
  a Prometheus node with `VmTesting{gpuPassthrough=false}` resolves
  `gpuPassthrough=false`, `vfioArmed=false`, **no** IOMMU kernel param, **no**
  `vfio_pci` module, the projected domain `vm-testing.criome.criome`, and the
  hosts entry; AND a contrasting `gpu-lab` node with `gpuPassthrough=true`
  correctly arms VFIO + binds the declared GPU PCI id. The opt-in is real and
  per-node.

### CriomOS-home (`next` branch, commit `ad4c2fb`)

- **`checks/chroma-visual/default.nix`** — the first booted-VM check
  (`pkgs.testers.runNixOSTest`). Boots a graphical guest (sway +
  `wl-gammarelay-rs` + chroma), drives `(SetTheme Light)`,
  `(SetWarmthKelvin 3000)`, `(SetBrightnessPercent 50)`, and asserts the
  **non-gamma** surface: the theme state-file rewrite (`current-mode`
  dark→light) plus the backend-independent `wl-gammarelay` DBus wire-trace gate
  (Temperature/Brightness `Set` calls, per report 66). The gamma colour-shift +
  screenshot assertions are gated behind a `gpuPassthrough` arg (default
  **false** → skipped), per the gamma verdict: they only hold on a
  VFIO-passthrough node whose guest exposes a CRTC `GAMMA_LUT`.
- **`flake.nix`** — wired `chroma-visual` into `projectChecks`.

## Chosen defaults (noted as adjustable)

- microvm.nix input: **yes** (`github:astro/microvm.nix`).
- Criome domain literal: **`vm-testing.<cluster>.criome`**.
- Remote display: **SPICE**.

These match the design report's stated defaults; all are data fields, not
hardcoded control flow, so they are changed by editing the Horizon payload or
the option default, not the module logic.

## Test results — verbatim

### nix flake check / eval

CriomOS and CriomOS-home both require lojix-projected `system` + `horizon`
inputs to evaluate at all (the stub inputs `throw`); this is pre-existing — a
bare `nix flake check` fails on `main` too. Validation therefore used the
established per-check build path with satisfying overrides
(`--override-input system path:/tmp/sys`, a fixture horizon).

- **CriomOS-home `nix flake check --no-build`** (system override): `all checks
  passed!` (exit 0) — every check evaluates, including `chroma-visual`.
- **CriomOS per-check builds** (system + horizon override): `vm-testing-
  prometheus-policy` → **PASS**; `desktop-audio-policy`, `devshell-repository-
  layout`, `legacy-chroma-runtime`, `nspawn-role-policy`, `nix-role-policy` →
  all PASS. (The `resolver-role-policy` / `router-*` checks fail under an
  arbitrary non-router horizon fixture — verified to fail **identically on
  `main`**, so pre-existing fixture sensitivity, not introduced by this work.)
- **Full target integration** — evaluating
  `nixosConfigurations.target.config.criomos.vmTesting` with a horizon carrying
  `VmTesting{gpuPassthrough=false}`:

  ```json
  {"address":"10.77.0.4","criomeDomain":"vm-testing.fieldlab.criome",
   "display":"Spice","enable":true,"gpu":null,"gpuPassthrough":false,
   "vfioArmed":false}
  ```

  Kernel params filtered for `iommu|vfio` on that config: `[]` (VFIO not armed).
  `microvm.vms` attr names: `["vm-testing"]` (persistent VM registered). The
  `microvm.nix` host import evaluates cleanly inside the full system.

### Booted-VM check (runNixOSTest) — chroma-visual, non-gamma path

Built and run **locally** (KVM present at `/dev/kvm`):
`nix build .#checks.x86_64-linux.chroma-visual` → **exit 0**, result
`/nix/store/ys39l2vw1gjql3mmb3n0kd4lcj2zv67z-vm-test-run-chroma-visual`.

Verbatim from the test driver:

```
machine: must succeed: cat /tmp/r-theme.log || true
=== r-theme.log ===
rc-theme=0
=== r-warm.log ===
rc-warm=0
=== chroma-daemon.log ===
=== state dir ===
-rw-r--r-- 1 tester users       6 Jun  4 14:17 current-mode
machine: must succeed: cat /home/tester/.local/state/chroma/current-mode
gpuPassthrough disabled: skipping gamma colour-shift screenshot assertion
```

The guest booted, sway created `wayland-1`, the chroma daemon parsed its config
and served the UDS, all three CLI calls returned `rc=0`, `current-mode` flipped
to `light` (6 bytes), the DBus trace carried `Temperature`/`Brightness`/`3000`,
and the gamma path was correctly skipped (gpuPassthrough false).

Two iterations were needed to get the guest config right and are worth noting
for the next agent: (1) the deployed chroma config parser does **not** accept
NOTA bracket-string hex (`[#1d1f21]`) at palette positions — it wants the
legacy quoted form (`"#1d1f21"`), the same form `CriomOS-home/.../chroma.nix`
itself emits; (2) the Theme `Schedule` must contain a `Manual` or `Waypoint`
record, not a bare `Default`. Both are properties of the current chroma
release, not the harness.

## What is gated (NOT done here, by design)

- **VFIO passthrough + the gamma colour-shift / screenshot assertion** → a
  future node with a spare/dedicated GPU. Never armed in this work; the option
  defaults false and Prometheus carries false.
- **Prometheus deploy** → gated on networking non-breakage verification (VM
  bridges / TAP / NAT / firewall / Criome-domain routing must be proven
  non-conflicting with Prometheus's router role) per Spirit 5hir5bnz, and is
  the **cluster-operator's** cutover. Nothing was deployed to any node.

## Branches

- `CriomOS` → `next` @ `c193127`, pushed to `origin/next`.
- `CriomOS-home` → `next` @ `ad4c2fb`, pushed to `origin/next`.

Worktrees: `~/wt/github.com/LiGoldragon/CriomOS/next/` and
`~/wt/github.com/LiGoldragon/CriomOS-home/next/` (git worktrees off `main`; jj
colocation is unavailable inside a secondary git worktree, so git was used as
the prior agent noted).
