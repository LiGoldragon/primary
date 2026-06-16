# 52 · Synthesis — lojix daemon + the general VM-testing interface (everything)

A single read-through of the whole arc: what was asked, what was built, what is
*proven* vs *pending*, the findings that mattered, the decisions you made, and
where every piece lives. The per-area reports (41–51, operator 387) hold the
depth; this is the map.

## The arc, in one paragraph

You asked for the **lojix** deploy daemon to be refreshed onto the latest crates
with two CLIs and production parity (deploy a full OS, survive an SSH
disconnect, every operation in schema types), tested end-to-end against a VM on
another host. That landed. Testing it surfaced that the bespoke `/tmp` VM rig
was cluster-specific, so you redirected: make VM testing a **real stack
capability** — cluster-data-generated, a proper host role in horizon, a
predictable nix-generated interface — and build a **readable test suite** for
complex OS and home-profiles on top of it. That landed too, proven by real VM
boots. The operator reviewed it and it's merge-ready after a cleanup pass that's
done. The last open thread is making **Prometheus** the live on-demand test-VM
host — designed, awaiting one decision before any change touches it.

## 1 · lojix — refreshed, two-CLI, production-parity, live-proven

**Reports 41–46, 48, 49. On lojix `main`.**

- **The daemon + two CLIs.** `lojix` (ordinary socket: Query/Watch), `meta-lojix`
  (owner socket: Deploy/Pin/Unpin/Retire), `lojix-write-configuration` (NOTA→rkyv
  bootstrap), `lojix-daemon` (takes exactly one rkyv startup arg, never parses
  NOTA). Modern schema syntax, refreshed deps.
- **Durable + disconnect-surviving.** A `sema-engine` store (self-resumes on
  restart) and a kameo `DeployJobs` actor owned by the daemon, so a deploy
  outlives the client that submitted it (S4b). All of S1–S4b adversarially
  reviewed before push.
- **Proven live on Prometheus, host-untouched.** The daemon's real pipeline —
  build → `nix copy` ssh-ng → `nix-env --set` generation → `switch-to-configuration`
  → BootOnce — ran end to end against a real writable-disk VM. The deploy
  completed *after* the submitting client died (disconnect survival), the durable
  job record was queryable via the CLI, and on a UEFI VM the deployed OS's kernel
  was *directly witnessed* booting via the BootOnce one-shot. Prometheus's
  networking stayed byte-identical throughout (`5hir5bnz`).
- **A real bug the live run paid for.** The daemon was building and copying the
  `.drv` *recipe* instead of the built OS, because `nix build --print-out-paths`
  returns the recipe path for a bare derivation on modern nix. **Without the fix
  the daemon could never activate any deploy.** Fixed (`<drv>^*`),
  regression-tested, and on lojix `main`. Unit tests and the earlier runs never
  caught it because they stopped at *build*, before *activation*.

**One residual, not a lojix defect:** the *lean* CriomOS guest profile doesn't
reach a stable userspace on a generic q35/OVMF VM (it hangs/watchdog-reboots
after the kernel boots). That's a CriomOS profile-on-q35 matter; the deploy
machinery is sound.

## 2 · The horizon test-VM model

**Report 47. Units A/B on the `horizon-test-vm` branches.**

You redesigned the throwaway rig into *integrated, on-demand, horizon-declared*
test VMs — "a proper role in horizon, a cluster node defined as the test VM with
its host/location." Decisions you made: a **real KVM microVM** substrate (not
nspawn) and a **v1 host-triggered** lifecycle (lojix unchanged; it just deploys
to the node's address). Unit A added `NodeSpecies::TestVm` + the guest model;
Unit B made CriomOS emit the microvm.nix guest + an additive tap. These became
the foundation for §3.

## 3 · The general cluster-data-generated VM-testing interface + suite ← the headline

**Report 50. The `horizon-test-vm` branches across horizon-rs / CriomOS /
CriomOS-test-cluster. Merge-ready.**

Your directive: *"general vm testing … using cluster-data-generated code, not
cluster specific … the node hosting it needs a role … the interface must be
predictable and/or use a generated config (generated in nix with cluster data
from the vm host and the vm-node config) … a suite of easy-to-read tests for
complex os and home-profile testing."* Delivered as six layers (C1–C6), each
implemented then adversarially reviewed:

- **C1 — the host role** (horizon-rs `8fb25be9`): `NodeService::VmHost` carrying
  the host's *cluster-authored* data as typed domain values — `TapSubnet`
  (IPv4), `KvmAvailability` (an enum, not a bool), `MaximumGuests` — plus a
  "a Pod must name an existing host" invariant.
- **C2/C3 — CriomOS consumes the projection** (`42bc62b3`): `test-vm-host.nix`
  reads the projected `VmHost` (the hardcoded subnet + `inputs ? microvm` probe
  are gone; the tap is sliced from `guest_subnet`, additive/host-untouched), and
  `test-substrate.nix` bakes every hand-rediscovered live-run constraint
  (microvm machine type, writable store, the NSS/root-shell fixes that caused the
  live "invalid user root", deploy key, address) into one composable profile.
- **C4 — the generator** (CriomOS-test-cluster): `mkVmTest { cluster; hostNode;
  vmNode; testScript }` → a runnable `runNixOSTest`. The guest is the *real*
  CriomOS system built **from the node's projection**, sized from its machine
  facts, networked from the host's `VmHost` data — nothing hand-stubbed. **A test
  is a function of the cluster model; the author writes four arguments.**
- **C5 — the readable suite** (`89f93ba3`): the model relaxed so *any* role's
  profile can be tested (the profile comes from the node's projected role). Two
  anchors **run green** on real VM boots: `edge-desktop-boots-greeter` (a real
  desktop stack — greetd/niri/keyring/polkit) and `base-home-activates` (a
  home-manager profile, asserting the *projected* user identity lands in the
  generated config). One concept each, PATTERN-commented.
- **C6 — the production-path smoke** (`f9910de7`→`89f93ba3`): a hermetic 2-node
  `runNixOSTest` where a deployer runs the *real fixed lojix daemon* and deploys
  a projection-generated target into a sibling node; it asserts (adversarially
  proven *not* faked — 146s pipeline, the target boots a different system and
  never pre-stages the closure) the target's generation becomes the deployed
  `nixos-system`, and the durable job record corroborates via the CLI.

**Key substrate finding:** the report-49 q35 hang was *bootloader-specific*.
`runNixOSTest` uses qemu-vm.nix (PCI bus + direct kernel boot, no bootloader), so
the lean guest boots cleanly there; the `-M microvm` machine-type override can't
compose with the test driver's PCI backdoor and is correctly *not* used in the
hermetic path (it belongs to the live path).

**Operator review (387):** verdict strong / merge-after-cleanup. The four
findings (TapSubnet IPv4-only + capacity; `mkDeployTest` actually using
`hostNode`; asserting the durable `Query` rather than printing it; a stale
comment) are all fixed and the re-review is **PASS** — the reviewer drove each
assert to prove it fires. Branches merge-ready in order horizon-rs → CriomOS →
CriomOS-test-cluster.

## 4 · Prometheus as the live on-demand test-VM host ← pending one decision

**Report 51. Designed; nothing has touched Prometheus.**

You want Prometheus to *literally* host on-demand test VMs (declared with the
role, generated emission, lojix deploys in). The design found the safe path and
one real hazard:

- **Don't system-deploy the router.** Even with root, running
  `switch-to-configuration` on Prometheus re-arms the *switch-restarts-networkd*
  mechanism that broke it during the gemma incident, with no console fallback —
  and a deployed tap wouldn't even come up until a reboot. So: declare the role
  (data), but run the *same generated emission* **host-untouched** (user
  namespace, no sudo — the proven reports-48/49 way), keeping Prometheus's netns
  byte-identical.
- **The one open decision:** does Prometheus's `VmHost` declaration go in its real
  cluster file (`goldragon/datom.nota` — truest, just data, but the production
  router model would carry a test capability) or a separate test file (production
  stays minimal)? My recommendation: goldragon. Both drive the identical
  host-untouched run.
- **The plan halts before the one Prometheus-touching step** (the user-level live
  run) for your explicit go.

## 5 · Findings worth keeping (cross-cutting)

- The lojix `.drv`-vs-output activation bug (§1) — found live, fixed, on main.
- The substrate split: q35/OVMF *bootloader* hang ≠ runNixOSTest direct-boot;
  the lean profile boots fine in the hermetic path (§3).
- The router deploy hazard (gemma incident, no console fallback) → host-untouched
  for Prometheus (§4).
- The CriomOS-test-cluster fixtures were *already stale* vs horizon-rs main
  (missing `backup_wireless`/`compressedSwap`) — reconciled during Unit A.
- The daemon **emits no logs** — a failed deploy is silent; surfaced via an
  effect-shim during the live runs. A production observability gap.

## 6 · Decisions you made

Real KVM microVM substrate + v1 host-triggered lifecycle (47) · the host role is
a declared `NodeService::VmHost`, not a species or facet (50) · ship C1–C5, scope
C6 to microvm generation-activation (50) · Prometheus as the live on-demand host
(51). Pending: the goldragon-vs-separate-file declaration (51).

## 7 · Where everything lives

- **lojix `main`:** the daemon, two CLIs, durable store, disconnect-survival, the
  `<drv>^*` fix.
- **`horizon-test-vm` feature branches** (horizon-rs `8fb25be9`, CriomOS
  `42bc62b3`, CriomOS-test-cluster `89f93ba3`): Units A/B + C1–C6 + the operator
  cleanup — **merge-ready for the operator**, all three mains untouched.
- **primary `main`:** reports 41–52, operator 387, the recorded VM-testing
  principle (`50/intent-capture.md`).

## 8 · Open items

1. **Your Prometheus decision** (goldragon vs separate file), then I run the safe
   steps and halt before the live run for your go.
2. **Operator merge** of the three branches (their lane).
3. **Spirit store migration** (`spirit-migrate-store`) — blocked workspace-wide;
   the VM-testing principle + the report-47 decision are durably in-report
   (`50/intent-capture.md`) until it's done. I offered to run it; awaiting the
   maintainer/your call.
4. **Cheap follow-ons** (all pure cluster-data or small): the router + second-tier
   suite tests (one node + one ~10-line spec each); the TCG/`kvm=Absent` booted
   path; the C1 `None`-super_node tightening; full BootOnce-reboot fidelity (the
   lean-profile-on-q35 hardening); the pre-existing `source-constraints` red
   (`llm.nix:158` has a `goldragon` token in a comment — not ours); the daemon
   observability gap.
