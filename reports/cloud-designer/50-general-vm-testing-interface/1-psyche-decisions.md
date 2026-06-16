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
- **C5 — DONE, review PASS** (CriomOS-test-cluster `horizon-test-vm` `ce4463fd`;
  CriomOS `horizon-test-vm` `724fae1a`; both pushed, mains untouched). **The
  headline deliverable.** `mkVmTest` relaxed to any Pod-on-VmHost node (profile
  from projection; lean TestVm a special case); `kvm` (Absent→TCG) + capacity
  wired. Two cluster-data-generated anchors declared in fieldlab.nota and **RUN
  GREEN** (independently re-verified on fresh builds):
  - `edge-desktop-boots-greeter` — an Edge Pod → the real desktop stack
    (regreet/greetd, niri, gnome-keyring, polkit), boots under KVM, 12.95s.
  - `base-home-activates` — a lean node + `includeHome` → the real home-manager
    generation, asserting the projected user email lands in the generated git
    config, 11.67s.
  Each is ONE concept with a PATTERN comment; the author writes only
  `(cluster, hostNode, vmNode, testScript)`. Two lean-guest substrate gaps (docs
  conflict, home re-wipe) fixed in `test-substrate.nix`/`test-vm-guest.nix`, not
  papered over. Spirit [xxgp]/[aipc] satisfied. → **Your ask is delivered: a
  cluster-data-generated, readable suite for complex OS + home-profile testing,
  proven green.**
- **C6 — DONE, review PASS** (CriomOS-test-cluster `horizon-test-vm` `f9910de7`,
  pushed; mains untouched; lojix consumed as a pinned input). `lib/mkDeployTest.nix`
  — a hermetic 2-node `runNixOSTest` (`lojix-deploy-smoke`): a deployer running
  the **real fixed lojix daemon** (lojix main, the `<drv>^*` fix) via
  `lojix-write-configuration → rkyv → lojix-daemon` (both sockets 660/600) +
  `meta-lojix`, deploying mercury's **projection-generated** CriomOS system into
  the target. The daemon's unmodified pipeline (`eval → nix build <drv>^* → nix
  copy ssh-ng → nix-env --set → switch-to-configuration boot`) runs offline; the
  target's `/nix/var/nix/profiles/system` flips to the deployed
  `nixos-system-mercury` closure (146s — not instant, so not faked; the target
  boots a *different* system and never pre-stages the closure), corroborated by
  the durable deploy-job record via the ordinary CLI. Real nixos-system, not a
  `.drv` — the fix held. **RUNS GREEN, deterministic.** Scoped to
  generation-activation (the bootloader write is a no-op on the direct-boot test
  guest — the deferred-BootOnce boundary), per decision (b).

## Complete — what shipped + operator handoff

The directive is delivered end to end. A general, cluster-data-generated
VM-testing interface + a readable suite, all proven by real `runNixOSTest` runs:

- **horizon-rs** `horizon-test-vm` (`fe7182f1`): `NodeService::VmHost` — the host
  role carrying cluster-authored data (typed `TapSubnet`/`KvmAvailability`/
  `MaximumGuests`) + the Pod-host invariant.
- **CriomOS** `horizon-test-vm` (`724fae1a`): `test-vm-host.nix` reads the
  projection (no hardcoding); `test-substrate.nix` bakes every live-run
  constraint; the lean-guest gaps fixed in the substrate; the `05-` networkd
  hardening.
- **CriomOS-test-cluster** `horizon-test-vm` (`f9910de7`): `mkVmTest` (the
  generator — author writes only `(cluster, hostNode, vmNode, testScript)`),
  `mkDeployTest` (the lojix smoke), and the suite — `edge-desktop-boots-greeter`,
  `base-home-activates`, `lojix-deploy-smoke`, all green; atlas declares
  `VmHost`; the projection check green.
- **lojix** main: the `<drv>^*` fix (pinned input).

**Operator handoff:** integrate the three `horizon-test-vm` branches to their
mains (they also carry Units A/B). Cross-repo flake pins resolve once all land
(horizon → CriomOS → test-cluster → lojix).

**Follow-ons (none blocking):** the Spirit store migration (`spirit-migrate-store`)
so the recorded principle + the report-47 decision land in Spirit; the router
node + second-tier suite (pure cluster-data additions via `mkVmTest`); the
TCG/`kvm=Absent` path (verified by logic, no booted test); full BootOnce-reboot
fidelity (the deferred lean-profile-on-q35 hardening); the minor C1
`None`-super_node→`UnresolvableArch` tightening.

## Operator review 387 — cleanup DONE, re-review PASS (2026-06-16)

The operator (CO) reviewed C1–C6 (`reports/operator/387`), verdict strong /
merge-after-a-short-cleanup. All four findings addressed on the
`horizon-test-vm` branches and independently re-reviewed PASS (the reviewer drove
each assert to prove it fires):
- **F1** (horizon-rs `8fb25be9`): `TapSubnet`→`Ipv4Net` (IPv6 rejected into
  `InvalidTapSubnet`) + `usable_host_count`/`can_host` + a Nix `assertModel`
  subnet-capacity check (a `/30` with >2 guests aborts eval).
- **F2** (CriomOS-test-cluster `89f93ba3`): `mkDeployTest` reads + asserts
  `hostNode` (declares VmHost, `vmNode` a Pod with `superNode==hostNode`).
- **F3** (same commit): the durable lojix `Query` is asserted (node + slot +
  closure). The slot is **`Current`** — correct: `activation_commit()` hardcodes
  `GenerationSlot::Current` in the durable record; the `BootPending` value only
  feeds a discarded transient payload (so C6's "Current" was right; an earlier
  relay of "BootPending" was the implement agent mis-describing its own change).
  `lojix-deploy-smoke` re-ran GREEN.
- **F4** (CriomOS `42bc62b3`): `test-substrate.nix` prose corrected
  (`vmTypeModule` not composed on the hermetic path).
Branches re-locked (horizon `8fb25be9`, criomos `42bc62b3`) and merge-ready in
operator order. Out-of-scope flag to CO: the `source-constraints` check is
pre-existing RED (`llm.nix:158` has a `goldragon` host-fact token in a comment —
untouched by this cleanup).
