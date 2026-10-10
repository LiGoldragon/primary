# virtio-gpu CRTC gamma-LUT spike — empirical verdict

System-designer lane. 2026-06-04. A SAFE empirical spike answering the one
open question report 67 §"Open questions" flagged as medium-uncertain:
**does a plain QEMU/KVM virtio-gpu guest expose a usable DRM CRTC gamma LUT
that `wl-gammarelay-rs` can program?** If yes, the CriomOS gamma-observation
test needs no VFIO passthrough. If no, VFIO on a GPU node is required.

This touched nothing outside a throwaway local VM under `/tmp/gamma-spike`:
no router, no host networking change, no VFIO/passthrough, no deploy.

## Verdict

**virtio-gpu does NOT expose a usable CRTC gamma LUT — on any device variant
tested, on a current kernel (6.18.24).** The answer is a clean **no**, and it
is confirmed two independent ways:

1. **DRM-property probe** — every virtio-gpu CRTC reports legacy
   `Gamma size: 0` and carries **no `GAMMA_LUT` atomic property** (and no
   `GAMMA_LUT_SIZE`, `DEGAMMA_LUT`, or `CTM`). There is nowhere for a LUT to
   land.
2. **Live functional test** — a real wlroots compositor (sway, DRM backend)
   on the virtio output, with `wl-gammarelay-rs` against it, reproduces the
   EXACT failure report 66 hit headless: `gamma_control::Event::Failed`,
   output dropped, no temperature applied.

**VFIO GPU passthrough is therefore required** for the chroma
warmth/brightness *observation* test, exactly as report 67's gamma verdict
predicted (which it had marked medium-high certainty pending this spike).
The spike upgrades that to **confirmed**.

## Method

Environment check first (honesty discipline — the spike only runs if KVM is
real here): `/dev/kvm` present and world-rw, `kvm_intel nested = Y`, `vmx` in
`/proc/cpuinfo`. Nested KVM works in this environment, so the VMs are real
KVM-accelerated guests, not pure TCG emulation.

Substrate: a minimal NixOS guest built with `nix-build '<nixpkgs/nixos>' -A
vm` from a tiny `configuration.nix` (qemu-vm.nix module, serial console,
auto-poweroff probe service). Guest kernel **6.18.24**. The guest's
`gamma-probe` oneshot dumps `lspci`, `/sys/class/drm`, loaded DRM modules,
and full `drm_info`, then powers off; output captured over the serial
console. QEMU 10.2.2 (the full nixpkgs build, with virglrenderer/gfxstream)
for the GL variants, which need an EGL-capable display backend the default
`qemu-host-cpu-only` runner lacks.

The probe ran across virtio-gpu device variants by overriding the device via
`QEMU_OPTS` on the VM runner.

## Device variants tried + per-variant result

| QEMU device | display backend | guest DRM driver | `Gamma size` | `GAMMA_LUT` property |
|---|---|---|---|---|
| `virtio-gpu-pci` (alias `virtio-gpu`) | none/serial | `virtio_gpu` | 0 | absent |
| `virtio-vga` | none/serial | `virtio_gpu` (+ bochs-drm secondary) | 0 | absent |
| `virtio-gpu-gl-pci` (alias `virtio-gpu-gl`) | `egl-headless,gl=on` | `virtio_gpu` (GL/virgl active) | 0 | absent |

Every variant resolves to the same guest KMS driver (`virtio_gpu`, version
0.1.0); the `-vga` forms additionally expose a `bochs-drm` CRTC, which also
reports `Gamma size: 0` and no `GAMMA_LUT`. The GL variant adds GPU-accel
client rendering (virgl) but leaves the **KMS** path — where gamma lives —
unchanged. `virtio-vga-gl` is the bochs+virtio pair already covered by
`virtio-vga` + `virtio-gpu-gl`; both its CRTCs are among those probed.

The complete set of atomic CRTC properties virtio-gpu advertises is exactly:
`ACTIVE`, `MODE_ID`, `OUT_FENCE_PTR`, `VRR_ENABLED`, `CRTC_ID`. No
colour-management property of any kind.

## Evidence — key lines

DRM-property probe (representative, `virtio-gpu-pci`; identical shape on all
variants):

```
Node: /dev/dri/card0
├───Driver: virtio_gpu (virtio GPU) version 0.1.0
├───CRTCs
│   └───CRTC 0
│       ├───Legacy info
│       │   ├───Mode: 1280×800@74.99 ...
│       │   └───Gamma size: 0
│       └───Properties
│           ├───"ACTIVE" (atomic): range [0, 1] = 1
│           ├───"MODE_ID" (atomic): blob = 42
│           ├───"OUT_FENCE_PTR" (atomic): range [0, UINT64_MAX] = 0
│           └───"VRR_ENABLED": range [0, 1] = 0
```

(No `GAMMA_LUT`, `GAMMA_LUT_SIZE`, `DEGAMMA_LUT`, or `CTM` line exists — a
grep for `GAMMA_LUT` across every variant log returns zero matches.)

Live functional test — sway (DRM backend) + `wl-gammarelay-rs`, temperature
set to 3000 K over DBus:

```
# wl-gammarelay-rs stdout:
New output: 53
Output 53: name = "Virtual-1"
Output 53: gamma_control::Event::Failed
Output 53 removed
Output 54: name = "Virtual-2"
Output 54: gamma_control::Event::Failed
Output 54 removed

# the SetTemperature DBus call, after both outputs were dropped:
"No calls to rs.wl.gammarelay.SetTemperature are accepted for object
 /rs/wl_gammarelay"
```

sway itself came up fine on the real virtio DRM output (`wlr-randr` lists
`Virtual-1 "Red Hat, Inc. QEMU Monitor"` with its full mode list, commit
succeeded, `drm_dumb` allocator) — so this is NOT a sway/compositor failure.
It is specifically `wlr-gamma-control` finding no programmable gamma on the
CRTC and refusing the output. That is byte-for-byte report 66's headless
failure, now reproduced on a real KMS-backed virtio output — proving the
failure is the missing CRTC gamma LUT, not the headless backend per se.

## What this means for report 67's design

- The **default mode** (QEMU + virtio-gpu-gl, NixOS test framework) stands
  for the whole NON-gamma surface — theme flips, ghostty paint, DBus wiring,
  daemon lifecycle, OCR. virtio-gpu does all of that; the spike showed sway,
  outputs, and modesetting all working.
- The **gamma-warmth colour-shift assertion** cannot run in default
  virtio-gpu mode. It must be gated behind the VFIO `gammaPassthrough`
  variant report 67 already designed. The spike removes the "maybe the cheap
  path works" branch from open question 1: it does not.
- The **backend-independent DBus wire-level gate** (assert chroma's
  `SetTemperature`/`SetBrightness` trace) becomes more important, since it is
  the only warmth/brightness gate available on non-passthrough nodes — and
  even it must drive chroma's DBus directly, because behind chroma,
  `wl-gammarelay-rs` itself drops its outputs on virtio-gpu (the
  `gamma_control::Event::Failed` above), so an end-to-end-through-gammarelay
  assertion would fail on virtio-gpu for environmental, not logic, reasons.

## Honesty notes / limits of this spike

- Screenshot before/after R/B comparison was not run: it is moot. With no
  LUT to program, no warmth can reach the scanout, so a scanout diff would
  trivially show "no change" and add nothing beyond the two confirmations
  above. The DRM-property + live-functional answer is complete and primary.
- Not tested: `virtio-gpu-rutabaga` (gfxstream/Vulkan path) and the newer
  `drm_native_context=on` mode (host ≥6.13/guest ≥6.14). These change the
  rendering/context path, not the paravirtual KMS CRTC, so there is no
  mechanism by which they would add a CRTC `GAMMA_LUT` the base virtio_gpu
  KMS driver lacks; flagged as a residual low-probability unknown rather
  than claimed-tested.
- This is one kernel (6.18.24). The result is consistent with the
  virtio_gpu KMS driver design (no gamma support upstream), so it is very
  unlikely to differ on nearby kernels, but the claim is scoped to what was
  measured.
- Throwaway artifacts live in `/tmp/gamma-spike` (~34 MB, the qcow2 disks +
  logs); they vanish on reboot and reference only nix-store paths.
