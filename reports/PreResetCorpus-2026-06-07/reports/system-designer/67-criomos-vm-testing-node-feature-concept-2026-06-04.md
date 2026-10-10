# CriomOS VM-testing node feature — concept + VM-tech recommendation

System-designer lane. 2026-06-04. Concept report (no code landed in this
session; this is the design that a follow-up operator/designer wave
implements).

## Intent anchors

- **Spirit 2630** — [CriomOS gains a VM-based-testing node feature that uses
  the best Linux VM technology for properly testing CriomOS and its
  components, including the visual / GPU cases like chroma]. This report's
  job: name THE best VM tech (with the gamma verdict spelled out) and
  design it as a CriomOS node feature.
- **Spirit 2631** — [route the VM-testing feature via a Criome domain such as
  vm-testing.<cluster>.criome — the exact name illustrative — through
  domain-criome plus the cluster networking]. This report designs that
  routing.
- **Spirit 2623** — [sandbox UI end-to-end testing]. The decisive
  requirement traces back here: report 66 stood up a headless wlroots
  sandbox that verified chroma's logic + DBus wiring but could NOT apply or
  observe a gamma LUT, because the headless backend has no
  `wlr-gamma-control` and ghostty would not paint. Visual verification needs
  a real DRM/KMS-backed display the screenshot path can read.
- **Spirit 2620** — [report commit discipline: whole working copy, inline
  message, no $EDITOR, set + push main]. Applied at the end of this session.

Honesty discipline (carried from report 66): every claim about VM tech is
marked for certainty and cited; where the recommended path has a known
limitation it is stated plainly rather than asserted as a clean pass.

## The decisive requirement, restated

Report 66's failure was specific and instructive. chroma's warmth and
brightness are a **post-composite gamma LUT** pushed to the display's CRTC
via the `wlr-gamma-control-unstable-v1` protocol. Two independent things
must hold for a test to *observe* that warmth:

1. The compositor must have a real output whose DRM/KMS CRTC accepts a
   gamma LUT (so `wl-gammarelay-rs` does not get
   `gamma_control::Event::Failed` and drop its only output).
2. The screenshot tool must capture the framebuffer **after** the LUT is
   applied — i.e. the pixels that actually reach the scanout, not the
   pre-LUT client buffer.

The headless wlroots backend fails (1). And even on a real compositor,
`grim` fails (2): `grim` uses the Wayland `wlr-screencopy` protocol, which
copies the **composited surface before the CRTC gamma LUT**, so a `grim`
screenshot of a warmed desktop looks un-warmed. A gamma LUT is invisible to
every Wayland-screencopy-based screenshotter by construction.

A virtual machine dissolves both problems at once, and that is the core
insight of this design — explained in §"Why a VM solves the
screenshot-can't-see-gamma problem".

## Why a VM solves the screenshot-can't-see-gamma problem

In a QEMU VM the **host** owns the guest's virtual scanout. The NixOS test
driver's `screenshot` / `get_screen_text` capture the guest framebuffer
through the **QEMU monitor** (`screendump`, over QMP) — equivalently exposed
as QEMU's built-in VNC server framebuffer. That captured image is the
guest's **final scanout surface**: whatever the guest's DRM/KMS stack
produced after composition and after the CRTC's gamma LUT, IF the guest's
virtual display device applies the LUT.

So the capture-point problem (2) is solved structurally: the host sees the
post-LUT scanout, not the pre-LUT client buffer. This is the opposite of
`grim` on a live compositor. (Certainty: high for the capture-point being
the guest scanout via QMP `screendump`; the driver's screenshot path is the
QEMU monitor, confirmed by the nixpkgs test driver — `nixos/lib/testing/`.)

That leaves problem (1): does the guest's virtual GPU expose a CRTC gamma
LUT that `wl-gammarelay-rs` can program? That is the gamma verdict, and it
is where the VM-tech choice actually bites.

## The gamma verdict — which VM tech can apply a real gamma LUT

I compared the candidate Linux VM technologies on the ONE axis that report
66 proved decisive: can the guest program a DRM CRTC gamma LUT that the
host-captured scanout then reflects.

### virtio-gpu (virtio-vga / virtio-gpu-gl / virgl / venus / drm-native-context)

virtio-gpu is QEMU's paravirtualized GPU. Its guest DRM driver
(`drivers/gpu/drm/virtio/`) presents a KMS device, and the GL variants
(`virtio-vga-gl`, virgl/venus, and the newer `drm_native_context=on` needing
host kernel ≥ 6.13 / guest ≥ 6.14) give real GPU acceleration for client
rendering. **But virtio-gpu's KMS is a restricted paravirtual modesetting
device.** The kernel documentation groups virtio (with qxl, vmwgfx,
virtualbox) among the paravirtualized drivers carrying *additional plane/CRTC
restrictions*, and virtio-gpu's CRTC historically does NOT advertise a
per-CRTC `GAMMA_LUT` atomic property. Without that property, a compositor's
`wlr-gamma-control` LUT has nowhere to land — the same class of failure as
report 66's headless backend, just for a different reason.

**Verdict for virtio-gpu: gamma LUT NOT reliably applicable.** (Certainty:
medium-high. virtio-gpu does the rendering job well; the missing piece is
specifically the CRTC GAMMA_LUT KMS property, which I could not find evidence
of being present. This must be empirically confirmed on the target kernel
before relying on it — see Open questions.) virtio-gpu remains the right
choice for the NON-gamma component tests (theme flips, DBus wiring, daemon
lifecycle, OCR of painted UI), which is most of the test surface.

### VFIO GPU passthrough

Passing a real PCI GPU into the guest gives the guest the *real* DRM driver
(amdgpu/i915/nouveau), which exposes the full CRTC `GAMMA_LUT` property — so
`wl-gammarelay-rs` programs a real LUT and it lands. This is the only path I
can assert *will* carry a gamma LUT, because it is literally the same driver
that works on bare metal. The costs are heavy: the host must release the GPU
(driver rebind, generally a dedicated/second GPU or single-GPU teardown of
the host session), it is poorly automatable in CI, and the host-captured
screenshot path changes (the display goes to the passed GPU's outputs or a
SPICE/looking-glass bridge, not QEMU's emulated scanout). VFIO is the
**fallback for the gamma-observation test specifically**, not the default
node feature.

**Verdict for VFIO: gamma LUT YES — the only certain-yes path — but not
CI-friendly and not the default.**

### crosvm / cloud-hypervisor / Firecracker / microvm.nix

- **Firecracker**: no GPU, no display device at all (serial-only microVM).
  Disqualified for any visual test.
- **cloud-hypervisor**: virtio-gpu support is limited/nascent; same KMS
  restriction as QEMU virtio-gpu even where present, plus weaker NixOS-test
  integration. Not chosen.
- **crosvm** (ChromeOS VMM): the strongest virtio-gpu/gfxstream
  implementation and the upstream home of much virtio-gpu DRM work, but it is
  not the NixOS test driver's backend and wiring it as a CriomOS node feature
  would mean re-implementing the harness QEMU already gives us for free. Not
  chosen as the substrate; worth watching as the place virtio-gpu KMS gamma
  would land first.
- **microvm.nix**: a NixOS-native way to run persistent lightweight guests
  (QEMU/cloud-hypervisor/crosvm/firecracker backends) declaratively. This is
  the right tool for the *persistent, viewable, routed* VM (the always-on
  `vm-testing.<cluster>.criome` node), as opposed to the *ephemeral CI*
  VM. See §"CriomOS feature shape" — the design uses BOTH.

### Recommendation

**QEMU/KVM is THE recommended VM technology**, used in two modes:

1. **Default mode — QEMU + virtio-gpu-gl, driven by the NixOS test
   framework** (`pkgs.testers.runNixOSTest`). Covers the whole non-gamma
   test surface for CriomOS and its components, automatable in CI, and
   human-viewable via `driverInteractive`. This is the node feature's
   backbone.
2. **Gamma mode — QEMU + VFIO GPU passthrough** for the chroma
   warmth/brightness *observation* test only, run on a node that has a
   spare/dedicated GPU. This is the one path that certainly carries a real
   CRTC gamma LUT.

QEMU is chosen over crosvm/cloud-hypervisor/Firecracker because it is the
backend the NixOS test driver already speaks, it has the broadest display
backend support (QMP screendump, VNC, SPICE, GTK, SDL), it supports both
virtio-gpu AND VFIO passthrough in one tool, and it is what microvm.nix and
`nixos-rebuild build-vm` already target — so every layer of the CriomOS
feature reuses one substrate.

## Nix-native integration — how the VM becomes automatable AND viewable

CriomOS already uses NixOS `checks` heavily (see
`/git/github.com/LiGoldragon/CriomOS/checks/`), but every existing check is
an **eval-time assertion** (`runCommand` + `lib.assertMsg`), not a booted
VM. The VM-testing feature adds the first **booted-VM checks**. Three Nix
mechanisms, each for a distinct purpose:

- **`pkgs.testers.runNixOSTest`** (a.k.a. `nixosTest`) — the CI-automatable
  booted VM. Declarative `nodes.<name>` NixOS configs + a Python
  `testScript` driving the guest. Gives `machine.wait_for_unit`,
  `machine.screenshot`, `machine.get_screen_text` / `wait_for_text` (OCR via
  `enableOCR = true`, tesseract on the host), `send_key`, `send_chars`. The
  screenshot path is the QEMU-monitor scanump described above — the reason
  this can see gamma where `grim` cannot.
- **`<test>.driverInteractive`** — the SAME test, built as an interactive
  driver (`nix build .#checks.<system>.<name>.driverInteractive` then run
  it). Drops into a Python shell where `start_all()` boots the VM and it
  stays alive; with `QEMU_OPTS` / display enabled a human watches the actual
  guest. This is the "viewable" half intent 2630 asks for, from the exact
  same source as the CI half.
- **microvm.nix** (new flake input) — the **persistent** VM behind the
  routed Criome domain. `runNixOSTest` VMs are ephemeral (boot, assert,
  discard); the always-on `vm-testing.<cluster>.criome` endpoint is a
  long-lived microVM declared as a CriomOS node service, exposing a remote
  display (SPICE/VNC) and a small harness control surface.

`nixos-rebuild build-vm` stays as the dev-loop convenience (build a runnable
`./result/bin/run-*-vm` of any CriomOS config) but is not the feature.

## CriomOS feature shape — the node-service variant + the booted checks

CriomOS expresses node capabilities as **`horizon.node.services` variants**,
resolved by `modules/nixos/node-services.nix` (`has` / `payload`). A module
gates itself with `lib.mkIf (nodeServices.has (node.services or []) "X")` —
exactly how `network/tailscale.nix` gates on `"TailnetClient"`. The
VM-testing feature follows that established grain:

1. **New node-service variant `VmTesting`** (illustrative name). A node whose
   horizon declares `services = [ ... { VmTesting = { display = Spice;
   gammaPassthrough = false; gpu = <pci-id-or-null>; }; } ]` becomes a
   VM-testing host. Payload fields: which remote-display protocol, whether to
   arm VFIO gamma passthrough, and which GPU (null = virtio-gpu default
   mode).
2. **New module `modules/nixos/vm-testing/default.nix`** gated on that
   variant. It (a) installs the QEMU/microvm.nix runtime + the test harness,
   (b) for `gammaPassthrough = true` arms VFIO (`boot.kernelParams` IOMMU,
   `vfio-pci` device binding for the declared GPU) — driven by Horizon data,
   never a hardcoded node name, per CriomOS's network-neutral rule, (c)
   defines the persistent microVM and its remote-display endpoint, (d)
   registers the Criome domain projection (§ next).
3. **New booted-VM checks under `checks/`**, wired into `projectChecks` in
   `flake.nix` next to the existing entries:
   - `checks/chroma-visual` — `runNixOSTest` booting a CriomOS-home graphical
     guest, launching chroma + `wl-gammarelay-rs` + ghostty, driving the
     axes, and asserting on `machine.screenshot` luminance/colour. In default
     virtio-gpu mode this asserts the screenshot-observable axes (theme flip,
     ghostty paints — the things report 66 could NOT see headless); the
     gamma-warmth assertion is gated behind the passthrough variant.
   - This is also the home for the **backend-independent wire-level gate**
     report 66 recommended (assert chroma's `Set Temperature/Brightness` DBus
     trace) so warmth/brightness have a CI gate even on nodes without a
     passthrough GPU.

Concrete `runNixOSTest` skeleton (illustrative — exact module wiring lands in
implementation):

```nix
# checks/chroma-visual/default.nix
{ pkgs, inputs, ... }:
pkgs.testers.runNixOSTest {
  name = "chroma-visual";
  enableOCR = true;
  nodes.machine = { ... }: {
    imports = [ inputs.self.nixosModules.criomos ];
    virtualisation.qemu.options = [ "-device" "virtio-vga-gl" "-display" "egl-headless" ];
    # graphical CriomOS-home session: sway/niri + ghostty + wl-gammarelay-rs + chroma
  };
  testScript = ''
    machine.wait_for_unit("graphical-session.target")
    machine.wait_for_text("ghostty")           # OCR: UI actually painted
    machine.screenshot("before")
    machine.succeed("chroma '(SetTheme Light)'")
    machine.wait_for_text("...")
    machine.screenshot("after-light")          # theme flip is scanout-visible
    # gamma-warmth assertion only on the passthrough variant:
    machine.succeed("chroma '(SetWarmthKelvin 3000)'")
    machine.screenshot("after-warm")           # post-LUT scanout iff CRTC gamma present
  '';
}
```

The `virtio-vga-gl` default sees theme/paint but (per the gamma verdict) the
`after-warm` colour-shift assertion only holds under VFIO; that assertion is
therefore conditional on the node's `gammaPassthrough` payload.

## Criome-domain routing — vm-testing.<cluster>.criome

The persistent microVM's remote-display + harness endpoint is published as a
Criome domain through `domain-criome`, consistent with its content-addressed
model (per its ARCHITECTURE.md and Spirit 312):

- The CriomOS `vm-testing` module emits a **provider-neutral projection** for
  the per-cluster name (e.g. `vm-testing.<cluster>.criome`) declaring the
  record that resolves to the VM-testing host's reachable address. Because
  CriomOS nodes already run inside the tailnet (`network/tailscale.nix`,
  `TailnetClient` service), the reachable address is the host's tailnet
  address; the cluster's `.criome` authority delegates the name to this
  node. `domain-criome` owns the meaning (registration + resolution +
  projection); `cloud` owns any external provider execution — the
  VM-testing endpoint is internal/tailnet, so it stays within
  `domain-criome`'s resolution + the cluster resolver and needs no external
  provider.
- A `Resolve(vm-testing.<cluster>.criome)` follows the delegation chain to
  the owning node's authority, which returns the current display/harness
  endpoint — exactly `domain-criome`'s `NotAuthoritative(Delegation { name,
  authority_endpoint })` then authoritative-record flow.
- Naming: keep the name as Horizon-derived data (cluster name flows from
  Horizon, never a Nix control-flow predicate), so the literal
  `vm-testing.<cluster>.criome` is rendered from cluster facts, matching
  CriomOS's network-neutrality rule and the `criomos-horizon-config` domain
  derivation already used for cluster domains / resolver addresses.

What reaches the user at that domain: a SPICE (preferred — best interactive
latency + clipboard) or VNC endpoint showing the **actual gamma'd
framebuffer** of the test guest, plus the harness control surface to launch a
named visual test. SPICE/VNC over the VM's scanout shows post-LUT pixels —
the same property that lets the CI screenshot see gamma — so a human opening
`vm-testing.<cluster>.criome` watching a chroma warmth test sees the warmth,
unlike a `grim` capture on a live desktop.

## The concrete chroma visual-test path on this VM

Putting the pieces together, the end-to-end path that finally lets chroma's
warmth/brightness be both APPLIED and OBSERVED:

1. **Backend**: QEMU guest with a CriomOS-home graphical session. For the
   gamma assertion, the node carries `gammaPassthrough = true` and a
   VFIO-passed GPU, so the guest's real DRM driver exposes a CRTC
   `GAMMA_LUT`. For non-gamma axes, `virtio-vga-gl` suffices.
2. **Compositor**: the real CriomOS desktop compositor (sway/niri) with a
   real output — NOT the headless wlroots backend that defeated report 66.
   `wl-gammarelay-rs` binds the output's `wlr-gamma-control`; with a real
   CRTC gamma LUT it gets a working output instead of
   `gamma_control::Event::Failed`.
3. **Drive**: the test (CI or interactive) runs `chroma '(SetWarmthKelvin
   3000)'`, `'(SetBrightnessPercent 50)'`, `'(SetTheme Light)'`.
4. **Capture**: `machine.screenshot()` reads the guest scanout via QEMU
   monitor — post-composition, post-CRTC-gamma. The captured PNG's mean
   colour temperature shifts warm under `SetWarmthKelvin 3000` and back at
   6500; brightness shows as luminance change; theme shows as the ghostty
   background flip. Assertions compare per-channel means before/after.
5. **Also capture (backend-independent)**: the DBus `Set Temperature/
   Brightness` wire trace, as report 66 recommends, so warmth/brightness
   have a green gate on every node, with the screenshot colour assertion as
   the stronger gate where a passthrough GPU exists.
6. **Human view**: the same guest reachable live at
   `vm-testing.<cluster>.criome` over SPICE/VNC for eyeball confirmation.

This is the exact thing report 66 could not do, now decomposed into a default
CI path (theme/paint + wire trace, everywhere) and a gamma-observation path
(VFIO node, colour-shift screenshot assertion).

## Open questions for the psyche

1. **Gamma scope vs. cost.** The certain-gamma path is VFIO passthrough,
   which needs a node with a spare/dedicated GPU and is not casual CI. Is a
   single dedicated VM-testing node with a passthrough GPU acceptable, or
   should we first empirically check whether the target kernel's virtio-gpu
   exposes a CRTC GAMMA_LUT (which would make the cheap path work and avoid
   passthrough entirely)? I recommend an empirical spike on virtio-gpu before
   committing to VFIO — flagged medium-uncertain.
2. **Persistent VM substrate.** microvm.nix as a new flake input for the
   always-on routed VM, or stretch `runNixOSTest`'s `driverInteractive` into
   a long-lived service? microvm.nix is the cleaner declarative fit; it adds
   an input. Approve the input?
3. **Node-service variant name.** `VmTesting` is illustrative; intent 2630/
   2631 leave naming open. Confirm the variant name and the domain literal
   (`vm-testing.<cluster>.criome` vs e.g. `lab.<cluster>.criome`).
4. **Remote-display protocol.** SPICE (best interactive, clipboard/USB) vs
   VNC (simplest, broadest client) vs RDP/waypipe. I lean SPICE for the
   human-viewable endpoint; confirm.
5. **Which components beyond chroma** get booted-VM visual checks first?
   chroma is the proven motivating case; the feature generalises to any
   CriomOS desktop component, but the first check should be chroma per 2623.

## Web sources

- VirtIO GPU / DRM native context, device variants, host/guest kernel
  requirements: https://github.com/qemu/qemu/blob/master/docs/system/devices/virtio-gpu.rst
  and https://patchew.org/QEMU/20250601135709.847395-1-dmitry.osipenko@collabora.com/
- DRM GAMMA_LUT CRTC property + paravirtual driver plane/CRTC restrictions:
  https://www.kernel.org/doc/html/latest/gpu/drm-kms.html and
  https://drmdb.emersion.fr/properties/3435973836/GAMMA_LUT
- virtio_gpu guest DRM driver:
  https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/virtio/virtgpu_drv.c
- NixOS integration-test driver (screenshot/OCR/interactive/driverInteractive):
  https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html
  and https://nixcademy.com/posts/nixos-integration-tests-part-2/ and
  https://github.com/NixOS/nixpkgs/blob/master/nixos/lib/testing/driver.nix
- grim uses wlr-screencopy (pre-CRTC-LUT capture):
  https://github.com/emersion/grim
- VFIO GPU passthrough (driver rebind, single/dedicated GPU constraints):
  https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF
- SPICE display: https://www.linux-kvm.org/page/SPICE
