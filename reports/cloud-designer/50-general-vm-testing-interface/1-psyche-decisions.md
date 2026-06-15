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
- **C2 + C3 — in flight.**
