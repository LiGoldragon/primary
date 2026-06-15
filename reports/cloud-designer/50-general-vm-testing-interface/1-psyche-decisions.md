# 50 · psyche decisions (2026-06-15)

Resolving the proposal's open decisions:

- **Host role → `NodeService::VmHost`.** The host declares a VmHost service
  carrying its guest subnet, KVM availability, and max guests; the role IS the
  service declaration (the generator reads cluster-authored host data). NOT a new
  node species and NOT a `behavesAs` facet.
- **Smoke test (C6) → ship C1–C5, scope C6 to microvm.** Deliver the full
  hermetic OS/home-profile suite now (no production dependency); scope the one
  lojix smoke test to the proven microvm build→copy→generation-activation path;
  defer full BootOnce-on-q35 fidelity (the lean-profile q35 hardening) until
  later.
- **Minor defaults (taken):** tap subnet as one sliced CIDR; generator + suite
  live in CriomOS-test-cluster; the home-keeping guest reuses the existing
  `deployment.includeHome` flag; accept the non-stock `runNixOSTest` microvm
  override and track upstream.

## Implementation order

C1 `NodeService::VmHost` + invariant + golden test (horizon-rs) → C2 host module
reads the projected VmHost data (CriomOS) → C3 `test-substrate.nix` profile
(CriomOS) → C4 `mkVmTest` generator (CriomOS-test-cluster) → C5 fast-core suite →
C6 lojix microvm smoke test. Designer `~/wt` feature branches; operator
integrates main. C1–C5 deliver the full hermetic suite with no production
dependency.

Honors the recorded principle (`intent-capture.md`) and the workspace testing
discipline — Spirit [xxgp] (one concept per test, named invariant, PATTERN
comment), [dqg3] (unblock the blocker IN the test), [l50b] (intents → constraint
tests).

## Progress

- **C1 — DONE, review pass** (horizon-rs `horizon-test-vm`, commit `fe7182f1`,
  pushed; main untouched `9fae4a36`). `NodeService::VmHost { guest_subnet:
  TapSubnet, kvm: KvmAvailability, maximum_guests: Option<MaximumGuests> }`
  (fully typed — `TapSubnet` over `ipnet`, `kvm` a domain enum not a bool),
  projected via `Node::vm_host_capability()`; the Pod-super_node-must-exist
  invariant (`Error::MissingSuperNode`, checked independently of arch); a
  host-viewpoint golden + invariant + codec tests; INTENT.md manifested. ~135
  tests green, clippy `-D warnings` clean. Minor follow-on: a Pod with
  `super_node: None` yields `UnresolvableArch` not `MissingSuperNode` (still
  fails projection; untested None-branch) — tighten in a later horizon touch.
- **C2 + C3 — DONE, review pass-with-notes** (CriomOS `horizon-test-vm`
  `28ad489c`, pushed; CriomOS-test-cluster `horizon-test-vm` local; mains
  untouched). C2: `test-vm-host.nix` reads the host's projected `VmHost`
  capability (`guestSubnet`/`kvm`/`maximumGuests`) — the hardcoded
  `169.254.100+i.1` subnet and `inputs ? microvm` probe are GONE; the per-guest
  tap is sliced deterministically from `guest_subnet`, additive/host-untouched
  confirmed end-to-end (`5hir5bnz`). C3: `test-substrate.nix` =
  `{ substrate ? "microvm", deployKey ? null }: { guestModule; vmTypeModule; }`
  baking every live-run constraint (microvm machine type, writable store,
  require-sigs=false, the NSS/nscd/root-shell prebakes that fix the live-run
  "invalid user root", deploy key, horizon-derived address). atlas declares
  `VmHost` in fieldlab.nota; projections-match-fieldlab green. Notes: the `05-`
  networkd-priority fix (latent plain-center DHCP-claim; inert on atlas-router)
  → folded into C4; test-cluster branch local (expected — C4 builds on it).
- **C4 — DONE, review pass-with-notes** (CriomOS `horizon-test-vm` `084b00da`,
  pushed — the `05-` tap-prefix hardening; CriomOS-test-cluster `b454a1c9`,
  local — the generator). `lib/mkVmTest.nix`: `{ cluster, hostNode, vmNode,
  testScript, substrate ? "microvm" }` → a `runNixOSTest` check. The trivial
  `test-vm-guest-boots-sshd` **RAN GREEN** (independently re-verified: VM booted,
  driver connected, sshd up, asserted, 9.21s, exit 0) — the stack's first
  runnable cluster-data-generated test. Verified 100% data-driven by eval: guest
  = real CriomOS system from `mercury.json` projection, sized from machine facts
  (4/8192/40960), network from atlas `VmHost.guest_subnet` — no hand-stub; model
  invariants fail loudly on missing VmHost/non-TestVm.
  **Key substrate finding:** `runNixOSTest` uses qemu-vm.nix (PCI bus + *direct
  kernel boot, no bootloader*), so the report-49 q35 *bootloader* hang does not
  apply — the lean guest boots clean. `-M microvm` provably can't compose with
  the test driver's PCI backdoor, so it is correctly NOT forced in the hermetic
  path (it belongs to the C6 live path; the `vmTypeModule` split in C3 is right).
  Notes: `vmHost.kvm` (→ TCG when Absent) and `maximum_guests` are declared but
  not yet consumed by the generator → wire in C5.
- **C5 — in flight.** The readable suite for complex OS + home-profile testing.
  Model refinement: relax `mkVmTest`'s vmNode from "must be lean TestVm" to "any
  Pod-substrate node on a VmHost host" — the profile under test comes from the
  node's projected role (the lean TestVm becomes just the deploy-target case).
