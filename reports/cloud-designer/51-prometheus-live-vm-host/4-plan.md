# 51 — Plan: Prometheus as the LIVE on-demand VM-testing host

Concrete, ordered, confirmation-gated. Read `0-frame.md` first for the
gap, the two access modalities, and `5hir5bnz`.

## Summary of the recommendation

- **Declare `VmHost` on Prometheus in its own real cluster** (`goldragon`)
  using its real `guest_subnet` / `kvm` / `maximum_guests`, plus ≥1
  on-demand `TestVm` guest with `super_node = prometheus`. This is the
  one model edit that makes Prometheus's projection emit the generated
  runner + additive tap from its own cluster data.
- **Run host-untouched (user network namespace), NOT a system-config
  deploy.** Per the grounded access reality and `5hir5bnz`: the live
  router must not be switched. Materialize the same C2/C3-generated
  emission through the proven reports-48/49 namespace harness.
- **The only step that touches Prometheus** is a *user-level* one (start
  a `--user` systemd unit that brings up a private netns + runs the
  generated runner + lojix deploy + teardown). **No root, no
  `switch-to-configuration`, no new system generation, host netns
  byte-identical.** Everything before it is a model edit or a `nix build`
  with zero host effect.
- **The single key decision needing psyche confirmation:** do we put the
  `VmHost` declaration in the **production `goldragon` proposal**
  (Prometheus permanently advertises a test-VM-host capability in its
  canonical cluster data — the cleanest "Prometheus IS the host" form,
  but couples a test capability into the production router model), versus
  a **separate non-production proposal** that names the real Prometheus
  node as the host (keeps `goldragon/datom.nota` untouched). Both drive
  the host-untouched run identically. See §6.

## 1. Declare Prometheus with `NodeService::VmHost` (the model edit)

**1a — the host service.** Append a `VmHost` service to Prometheus's
services vector, mirroring ATLAS's shape (C1 typed schema:
`VmHost { guest_subnet: TapSubnet, kvm: KvmAvailability, maximum_guests:
Option<MaximumGuests> }`):

```
;; goldragon/datom.nota — prometheus services (currently :97)
[(TailnetClient) (NixBuilder (Some 6)) (NixCache)
 (VmHost [169.254.100.0/22] Available (Some 4))]
```

- **`guest_subnet`**: a link-local test CIDR carved for the taps — use
  `169.254.100.0/22` (ATLAS's value; link-local, never routed, the same
  CIDR `test-vm-host.nix` slices the host endpoint from). It does NOT
  overlap Prometheus's routed space, so it is `5hir5bnz`-inert: the C2
  endpoint is a `/32` link-local, the host's routed IP is never touched.
  (Final value is the psyche's to confirm; link-local is the safe class.)
- **`kvm`**: `Available` — Prometheus has `/dev/kvm` (report-48 preflight
  confirmed). This must say `Available` so C2's
  `mkIf (hasGuests && kvmAvailable)` fires and the generator picks KVM
  over TCG.
- **`maximum_guests`**: `(Some 4)` (or as desired) — asserted-not-exceeded
  at eval (C4/C5); a ceiling, not a reservation.

`VmHost` is a `NodeService`, sibling to `NixBuilder`/`NixCache` — adding
it does **not** change Prometheus's species (`LargeAiRouter` stays) and
does not by itself alter its system config until a deploy. (We are NOT
deploying — see §2.)

**1b — the on-demand guest(s).** Declare ≥1 `TestVm` Pod guest in the
same cluster with `super_node = prometheus`, mirroring fieldlab's
`mercury` (`fieldlab.nota:105-129`):

```
mercury (TestVm
  Min  Max
  (Pod (Some X86_64) 4 None None (Some prometheus) (Some <code-node>) None
       (Some 8) (Some 40) (Some [home-lab]))
  (Qwerty Uefi { [/] ([/dev/vda] Ext4 []) } [])
  (<guest ssh keys>)
  []
  (Some [10.77.0.7/24])
  …
  [(TailnetClient)])
```

The `Pod` substrate field carries `super_node = (Some prometheus)` — this
is what C2 reads (`(n.machine.superNode == thisNode) && n.behavesAs.testVm`)
to host the guest. `TestVm` species ⇒ `behavesAs.testVm` (lean: sshd +
writable disk, home/doc weight suppressed). Reuse C5's "any Pod-on-VmHost
node" relaxation if a non-`TestVm` role guest is wanted (mkVmTest now
accepts any Pod-substrate node hosted on a VmHost host, not only lean
TestVm).

**Cross-cluster note (the real wiring work).** Prometheus is in
`goldragon`; the C4-C6 generators, `mkVmTest`/`mkDeployTest`, the
committed projection fixtures (`fixtures/horizon/*.json`), and the
existing guests all live in `fieldlab`/CriomOS-test-cluster and project
`--cluster fieldlab`. Driving from Prometheus's *declared* role requires
**either**:
- **(A) goldragon-native:** declare the `VmHost` + the `TestVm` guest in
  `goldragon/datom.nota`, and teach the test-cluster generators to
  project the goldragon cluster for the Prometheus host node (a second
  `--cluster goldragon` projection path + committed
  `fixtures/horizon/prometheus.json` + guest fixtures); **or**
- **(B) test-surface:** add a Prometheus-as-host node + its `TestVm`
  guest to a fieldlab-style non-production proposal the generator already
  projects, leaving `goldragon/datom.nota` untouched.

(A) is the truest "Prometheus IS declared as the VmHost in its real
cluster"; (B) avoids touching the production proposal. This A-vs-B choice
is the psyche decision in §6.

## 2. Generate the on-demand hosting from the VmHost projection

Once §1 lands, **no further declaration is needed** — the generated
artifacts fall out of Prometheus's projection, because
`CriomOS/modules/nixos/criomos.nix:46` imports `test-vm-host.nix`
unconditionally (inert until a projection declares `VmHost` + hosts a
guest) and `:54` imports the microvm host module.

**What is GENERATED (a `nix build` — zero host effect):**

- **C2 `microvm.vms.<guest>`** — qemu/KVM microVM, `vcpu`/`mem`/`disk`
  sliced from the guest's projected `machine.{cores,ramGb,diskGb}`, one
  tap NIC `vmt<index>`, **`autostart = false`** (the on-demand property).
- **C2 additive tap spec** `systemd.network.networks."05-test-vm-vmt<i>"`
  — matches only the tap by name, host endpoint
  `<sliced-from-guest_subnet>/32` + a `/32` route to the guest IP,
  `RequiredForOnline = no`. (`05-` prefix sorts before a plain-center's
  `10-main-eth`; inert on a router, which has none.)
- **C2 `networking.hosts`** — guest criome domain → guest IP.
- **C3 `guestModule`** — writable `/nix/store`, `require-sigs=false`,
  nscd+NSS `files` pin, absolute root shell, deploy key, `console=ttyS0`,
  ESP/root labels — composed onto the guest's own CriomOS `nixosSystem`.
- **The actual runner:** `prometheus.config.microvm.vms.<guest>.config.config.microvm.declaredRunner`
  — the generated qemu-launch script, built via `fixtureSystem
  "prometheus"` / `nix build …#prometheus…declaredRunner`. **A build of
  this touches nothing on Prometheus.**

**The RUN approach — host-untouched user namespace (RECOMMENDED), not a
system-config deploy.**

Grounded reasoning (`safety` sub-report; `5hir5bnz`):

| | (a) System-config deploy of the emission | (b) Host-untouched namespace (RECOMMENDED) |
|---|---|---|
| Touches live router config | **Yes** — rewrites networkd materialized config, new system generation | **No** — host netns/config byte-identical (proven 48/49) |
| `5hir5bnz` | **Violates the spirit** — re-arms the switch-restarts-networkd mechanism that caused the gemma outage; needs BootOnce of a full new router gen with no console fallback | **Honors it** — no switch, no networkd bounce, no new generation |
| Privilege | root on a production router | **none** — `li`, no sudo (`unshare -rn`) |
| Blast radius | router lockout possible (bad `br-lan`/`kea`/firewall gen), no out-of-band recovery | confined to the private netns |
| Reversibility | another deploy/reboot | `systemctl --user stop` removes tap+route; nothing on host to undo |
| Cluster-data-generated | yes | yes — consumes the same C2/C3 generated runner + tap params |

The router module's guards (`router/default.nix:236-260`:
`restartIfChanged = false` / `stopIfChanged = false`) protect only
against a live bounce of *existing* units — they explicitly do NOT apply
changed network policy until a reboot or explicit restart. So a
system-deploy of the emission would either not bring the tap up until a
reboot (defeating "on-demand") or require a forbidden live networkd
reload. **Modality (a) is off the table until Prometheus has real
out-of-band/console access** (`5hir5bnz`'s own named prerequisite).

The host-untouched run is **not** "bespoke instead of generated": it
*consumes* the C2-emitted `declaredRunner` and the C2-computed tap params
(link-local `/32` endpoint sliced from `guest_subnet`, `/32` route) and
materializes them inside `unshare -rn` instead of in host networkd. The
emission's tap design maps one-to-one onto what the namespace already
does by hand.

## 3. The on-demand lifecycle (report-47 v1 + C6 deploy path)

A single host-side runner script — modeled on the existing
`scripts/run-on-prometheus` / `nspawn-dune-on-prometheus`
(`ssh prometheus.goldragon.criome` + `systemd-run --user`) — owns the
*invoked* half. Steps:

1. **Build (no host effect):** `nix build` the generated
   `declaredRunner` + guest closure (§2). On a builder; Prometheus
   untouched.
2. **Bring up (host-untouched):** start a durable `--user` unit
   (`mercury-ns`) that does `unshare -rn`, creates the additive tap
   `vmt<i>` *inside the private netns* with the C2-computed host
   endpoint + `/32` route to the guest IP (the C2 `.network` content,
   applied in the netns instead of host networkd), then runs the
   generated `declaredRunner` under `nsenter`. `autostart=false` means
   the VM only ever starts here — the on-demand property. Host netns
   byte-identical (`5hir5bnz`).
3. **lojix deploys in (the production path):** start the fixed lojix
   daemon (lojix main, the `<drv>^*` fix; C6
   `lojix-write-configuration → rkyv → lojix-daemon`, sockets 660/600)
   as a `--user` unit *inside the netns*; submit
   `(Deploy (System (<cluster> <guest> FullOs … Boot …)))` over the owner
   socket. The daemon targets `root@<guest>.<cluster>.criome` (resolved
   to the tap IP via the runner's `~/.ssh/config` alias) and runs
   build→copy→generation-activate autonomously — **zero VM
   special-casing**; this is the same daemon that does production
   deploys. Report 49 proved BootOnce + disconnect survival on the UEFI
   substrate.
4. **Assert:** the C6 pattern queries the daemon's durable terminal
   deploy-job record via the ordinary `lojix Query` path and checks the
   guest booted the lojix-deployed closure (`nixos-system-<node>-…`).
5. **Tear down:** `systemctl --user stop mercury-vm mercury-ns
   lojix-daemon`. The tap + route vanish with the namespace; Prometheus
   untouched. This is report-47's v1 lifecycle (create+start → lojix
   Deploy → stop, non-autostart, "integrated, not always running")
   realized on the role-generated runner.

The hermetic C4/C5 `runNixOSTest` checks remain the default path and
**never touch Prometheus**; the namespace run is the single fidelity
proof, not the per-test path.

## 4. Retarget the hermetic suite's `hostNode` to Prometheus

Today every generator call pins `hostNode = "atlas"`
(`flake.nix:131,161,207,215`) and projects `--cluster fieldlab`
(`flake.nix:56-66`, `projections-match-fieldlab`). To drive the tests
from Prometheus's *real* cluster data:

- **`hostNode = "prometheus"`** in each `mkVmTest` / `mkDeployTest` call
  whose host should be Prometheus. `hostNode` is read by
  `mkVmTest.nix:165,190` (`hostHorizon = readHorizon hostNode`) to find
  the VmHost service, the hosted guests, and the `guest_subnet` slice;
  retargeting it changes which projection drives the tap + capacity +
  accel decisions.
- **`vmNode`** stays the guest name (`mercury` etc.), now declared with
  `super_node = prometheus` (§1b).
- **`cluster`** = the cluster the projection comes from. Under §6-A this
  becomes `goldragon` for the Prometheus-hosted tests, which requires:
  (i) a `--cluster goldragon` projection path added alongside the
  `fieldlab` one in `projections-match-*`; (ii) committed
  `fixtures/horizon/prometheus.json` + the guest fixtures, generated by
  `horizon-cli --cluster goldragon --node <n>`; (iii) the
  `fixtureSystem`/`readHorizon` helpers parameterized by cluster (today
  they assume the single fieldlab fixture set). Under §6-B the cluster
  stays the test proposal's name and only `hostNode`/`vmNode` change.
- The hermetic checks themselves are unchanged in shape — they still run
  `runNixOSTest` with no host; only the projection source changes. They
  continue to never touch Prometheus.

This is the smallest retarget: `hostNode` is the single seam. The
heavier work is the cross-cluster projection plumbing (§6-A) if the
psyche wants the production cluster to be the source of truth.

## 5. Implementation order + the confirmation gate

Ordered so every Prometheus-touching step is last and is user-level only.
**Steps 0-4 touch NOTHING on Prometheus** (model edits + builds +
eval/hermetic checks). **Only step 6 touches Prometheus, and only at
user level.**

| # | Step | Touches Prometheus? | How |
|---|---|---|---|
| 0 | Confirm §6 decision (production vs test-surface; A vs B) | No | — |
| 1 | Declare `VmHost` on Prometheus + the `TestVm` guest (§1) | No | cluster-data edit only |
| 2 | Wire the cross-cluster projection / generate fixtures (§4) | No | nix/horizon-cli eval |
| 3 | Retarget `hostNode = "prometheus"`; run hermetic C4/C5/C6 green | No | `runNixOSTest`, no host |
| 4 | `nix build` the generated `declaredRunner` + guest closure (§2) | No | build on a builder |
| 5 | Confirmation gate — psyche OKs the live run | No | — |
| 6 | Host-untouched live run on Prometheus (§3 lifecycle) | **Yes — user level only** | `ssh prometheus…` + `systemd-run --user`; `unshare -rn` netns; **no sudo, no switch, no new generation; host netns byte-identical** |

**What step 6 does and does NOT do to Prometheus:**
- DOES: log in as `li`, start `--user` systemd units, create a tap inside
  a private user network namespace, open the world-writable `/dev/kvm`,
  append one line to `li`'s own `~/.ssh/config`.
- DOES NOT: use sudo or root; run `switch-to-configuration`; create a new
  system generation; touch host networkd / `hostapd` / `kea` /
  `dnsmasq` / `br-lan`; add any route or interface to the host netns;
  change anything that survives `systemctl --user stop` + namespace
  teardown.

**The system-config deploy modality (a) is explicitly NOT in this plan.**
It is gated behind a separate, explicit psyche decision AND the
`5hir5bnz` prerequisite of real out-of-band/console access on Prometheus,
which does not exist today.

## 6. The single decision needing psyche confirmation

**Where does Prometheus's `VmHost` declaration live?**

- **Option A — production `goldragon/datom.nota`.** Prometheus's real,
  canonical cluster data declares `VmHost` + the on-demand `TestVm`
  guest. This is the truest realization of "Prometheus IS the live VM
  host," and the tests are driven by production cluster data. Cost: a
  test capability is now permanently advertised in the production router
  proposal, and the test-cluster generators must learn to project the
  `goldragon` cluster (§4 plumbing). The declaration is inert on the
  router until a deploy — and we are **not** deploying — so it changes no
  running system, only the model.
- **Option B — a separate non-production proposal** naming the real
  Prometheus node as the host. `goldragon/datom.nota` stays untouched;
  the production router model carries no test capability; the generator
  projects the test proposal as it does fieldlab today. Cost: the
  "Prometheus IS declared as the VmHost in its real cluster" property is
  slightly weaker — it's declared in a test surface that *names*
  Prometheus, not in goldragon proper.

**Both options drive the identical host-untouched live run** (§3) and
neither requires a system-config deploy. The choice is purely *where the
truth of "Prometheus hosts test VMs" is recorded* — in the production
cluster model (A) or in a test surface that names it (B).

**Independent of A/B, confirm:** (1) the run modality is host-untouched
user-namespace, never a system-config switch, while Prometheus has no
out-of-band access (recommended, `5hir5bnz`); (2) the chosen
`guest_subnet` (link-local `169.254.100.0/22` proposed — non-routed,
`5hir5bnz`-inert); (3) authorization to perform the user-level live run
(step 6) on Prometheus.

Nothing in steps 0-5 touches Prometheus; the plan halts at the gate
(step 5) for this confirmation before step 6.
