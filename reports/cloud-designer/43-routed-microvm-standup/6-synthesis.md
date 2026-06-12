# 43 · Routed microVM standup — synthesis (safe standup plan)

cloud-designer, 2026-06-12. Consolidates the five read-only recon dimensions
(`1`–`5`) into one concrete, safe plan to stand up the routed `vm-testing`
microVM — its own Criome domain + a reachable IP, viewable from ouranos — as
the lojix end-to-end test target, honouring constraint `5hir5bnz` (do not break
Prometheus networking) and Decision `se72` ("setup the full routed microVM, go
all the way").

## Bottom line

Stand the routed microVM up on **zeus**, not Prometheus.

`se72` says "go all the way" on the *routed microVM* (its own domain + reachable
IP) — it does not say "on the router." The binding gate `5hir5bnz` is satisfied
most strongly by the host that *structurally cannot* break Prometheus
networking: a non-router node. zeus is a plain `Edge` node, already reachable
from ouranos over the same Yggdrasil mesh that reaches Prometheus, already
carries KVM + qemu + virsh, and runs the identical 26.05 generation. It gives a
*real* routed microVM with a real `vm-testing.goldragon.criome` domain and a
host-side tap — the full feature — while keeping the router's `hostapd` / `kea`
/ `dnsmasq` / `br-lan` stack completely untouched. Prometheus stays the *future*
target once out-of-band/console access exists; doing it on zeus first also de-
risks the eventual Prometheus standup by proving the host-tap routing the module
does not provide.

Deploy with production **`lojix-cli`** (flagless NOTA), action **`BootOnce`**,
run **on zeus itself**. Roll back by **rebooting** (BootOnce self-heals to the
prior generation on reboot 2). The lojix *daemon* cannot do this yet — it
rejects every activating action by contract — so the standup uses the CLI; the
daemon proving the same deploy is the downstream cutover validation, not a
prerequisite.

## Host choice: zeus over Prometheus

| Dimension | zeus (`Edge`) | prometheus (`LargeAiRouter`) |
|---|---|---|
| Router / networking blast radius | **None** — not a router, no `br-lan`/hostapd/kea/dnsmasq | **Maximal** — the live cluster router; a networking break is the `5hir5bnz` failure mode |
| `5hir5bnz` exposure | Cannot break Prometheus networking by construction | Every change is directly under the gate |
| Out-of-band / console recovery | Lockout is bad but blast radius is one Edge node | **None today** (`kx32`) — a router lockout needs physical access and is not remotely recoverable |
| KVM / virt tooling | `/dev/kvm` + `kvm_intel`; `qemu-system-x86_64` + `virsh` already on PATH | `/dev/kvm` present; qemu/virsh/microvm **not** on PATH yet |
| Reachable from ouranos | Yes — `200:17f7:…` over `200::/7 dev yggTun`, resolves in `/etc/hosts` | Yes — `200:ca41:…`, ssh:22 open, ~16ms |
| RAM headroom | **Tight** — ~9.6Gi free of 15Gi; VM at 2048MB fits but size small | Huge — 121Gi free of 124Gi |
| Bridge / tap today | None — must add host tap (the module does not provide it) | None on PATH; same gap, on a router |

The host-state recon (file 2) already named zeus the safest target on capacity +
role grounds; the risk recon (file 5 §"Prefer the lower-risk fallback first")
independently flags that the routed-microVM-on-Prometheus is the strictly
higher-risk path and recommends sequencing lower-risk first. The networking/IP
recon (file 4) confirms the domain/IP projection is **data-driven from the
horizon node**, so it works identically for zeus — the projected domain just
becomes `vm-testing.goldragon.criome` resolving to zeus's address, which ouranos
already reaches. Choosing zeus therefore loses nothing the psyche asked for and
removes the entire `5hir5bnz` risk class.

The one real cost is RAM: zeus has ~9.6Gi free. The guest is declared at
`mem = 2048` / `vcpu = 2` (file 1), which fits, but the host must not be loaded
with other work during the standup. If 2Gi proves tight, the guest mem is a
fixture-time field and can be reduced.

## How the vm-testing module works (recap from file 1)

- A **Horizon node-service feature**, not a hand-set host toggle. Enablement is
  data-driven: the node must carry a `VmTesting` service variant in its
  `node.services` vector. `options.criomos.vmTesting.enable` exists but is *set
  by the module* as a projection, gated by that service entry.
- To enable on zeus: add `{ VmTesting = { gpuPassthrough = false; display =
  "Spice"; gpu = null; }; }` to zeus's `services` vector in the goldragon
  horizon fixture (`goldragon/datom.nota`). zeus's `services` is currently `[]`.
- The host import wiring is already unconditional in `modules/nixos/criomos.nix`
  (`./vm-testing/default.nix` imported; `inputs.microvm.nixosModules.host`
  imported when `inputs ? microvm`, which the CriomOS flake satisfies via
  `microvm.url = github:astro/microvm.nix`).
- Guest closure attribute: `microvm.vms.vm-testing` (hypervisor qemu, vcpu 2,
  mem 2048, `graphics.enable = true`, one tap interface id `vm-testing` mac
  `02:00:00:00:00:01`, hostName `vm-testing`).
- CI check `checks.<system>.vm-testing-prometheus-policy` is a **pure isolated
  eval** (`lib.evalModules` against a synthetic horizon, microvm input
  deliberately omitted): it asserts the Prometheus policy path (`enable`,
  `gpuPassthrough == false`, `vfioArmed == false`, no iommu param, no vfio_pci,
  domain string, hosts entry) and a contrasting opt-in `gpu-lab` path. It
  validates **policy logic, not a booted/routed VM**. (system-designer report 69
  notes a separate booted-VM `runNixOSTest` PASS on `next`.)
- The feature lives **only on CriomOS `next`** (`qnqvptll c1931279`), deployed to
  no node. CriomOS-test-cluster has no `next` and no `VmTesting` fixture.

## The two gaps the module does not fill

1. **Host-side tap/routing.** The module declares only the *guest* tap NIC. It
   provisions **no host bridge, tap IP/route, forwarding, or DHCP** — this is
   the "routed" half the standup must add. For the display path (host fronts the
   guest) a routed guest L3 is not strictly required, but a real routed microVM
   wants the host tap created and either bridged or routed/NAT'd so the guest is
   reachable. On zeus this is a clean addition with no router config to disturb.
2. **A reachable display/registration surface.** The domain resolves to the
   **host**, and the host's remote display (SPICE/VNC/QMP) fronts the guest. The
   module does not open a display port. The standup must serve the display on
   zeus's reachable (Yggdrasil) address and allow it through zeus's firewall.

## Deploy path + rollback (from file 3)

Production tool: **`lojix-cli`** — flagless, NOTA-only, one positional record,
tag-dispatched (`FullOs` / `OsOnly` / `HomeOnly` / `CheckHostKeyMaterial`). For a
microVM-host system deploy:

```
(OsOnly goldragon zeus <source.nota> github:LiGoldragon/CriomOS/<next-rev> <action> None None)
```

`<action>` is a `SystemAction = Eval | Build | Boot | Switch | Test | BootOnce`.
Only `Boot | Switch | Test | BootOnce` copy + activate; `Eval`/`Build` never
touch the host.

- **Run on zeus itself.** Addressing derives from
  `horizon.node.criome_domain_name`; there is **no `--target` flag**
  (network-neutrality). Invoke `lojix-cli` while logged into zeus.
- **Validate first with `Build`** — `(OsOnly … Build None None)` builds the
  toplevel, no activation, no host mutation.
- **Activate with `BootOnce`.** It installs the new generation's bootloader
  entry but keeps the persistent default pointing at the *currently running*
  generation and stages the new one as a systemd-boot **one-shot**: reboot 1
  lands NEW, reboot 2+ auto-returns to OLD. A networking break self-heals on the
  next reboot with zero operator action. The activation runs as a **transient
  `systemd-run` oneshot unit owned by PID 1**, so an ssh drop does not kill it;
  re-attach with `journalctl -u <unit>`.
- **Rollback = reboot.** If the new generation is broken (networking included),
  just reboot; the one-shot is consumed and the prior generation returns as the
  default. No menu interaction needed. If you reboot into a *good* gen you want
  to keep, promote it later with a deliberate `Boot`/`Switch` from a safe
  context. Always pin `github:LiGoldragon/CriomOS/<rev>` so nix fetches fresh
  code, not a stale eval.

`BootOnce` is the right action even on zeus: it is the headless-safe default and
keeps the standup uniform with the eventual Prometheus path. `Switch` is
avoided as a matter of discipline (and is outright forbidden on a router).

## Networking / domain / IP mechanics (from file 4)

- The domain is **projected, not allocated**: `criomeDomain =
  vm-testing.<cluster>.criome`, `nodeAddress = head(split "/" node.nodeIp)`,
  emitted as `networking.hosts = { "<nodeAddress>" = [ criomeDomain ]; }` — the
  same `mkCriomeHostEntries` grain CriomOS already uses. The live cluster is
  **goldragon** (not the CI stub's `criome`), so on zeus the real domain is
  **`vm-testing.goldragon.criome`** resolving to zeus's node address. Do not
  hardcode `criome.criome`; the projection self-corrects from `cluster.name`.
- The domain points at the **host**; the host's display surface fronts the
  guest. The guest does not join Yggdrasil or get its own routed cluster IP from
  the module today — it is reached through the host.
- **Resolution is `/etc/hosts`, not live DNS** (nscd disabled). For ouranos to
  resolve `vm-testing.goldragon.criome`, the new hosts entry must land in
  **ouranos's own generation** too (it is projected per-node from the same
  horizon) — or the human targets zeus's address / `zeus.goldragon.criome`
  directly. Confirmed live: ouranos resolves `zeus.goldragon.criome →
  200:17f7:…` and routes `200::/7 dev yggTun`, identical to the Prometheus path.
- The human views the VM with a **SPICE/VNC/QMP client on zeus** over the
  existing Yggdrasil route (the module enables SPICE by default,
  `graphics.enable = true`). The standup must serve that port on zeus's
  reachable address and open the firewall.

## Risk surface

| # | Risk | Source | Likelihood on zeus | Mitigation |
|---|---|---|---|---|
| R1 | Activation bounces live networking (the gemma incident) | `kx32`, file 5 | Low — zeus runs no router services | `BootOnce` never activates live; nothing restarts until a deliberate reboot |
| R2 | Bad new generation booted, host locks out | `1144`, file 5 | Medium — zeus has no out-of-band access either | `BootOnce` self-heals on reboot 2; verify before promoting to default |
| R3 | Host tap/bridge collides with existing host networking | file 5 R1 | Low on zeus (no `br-lan`; only one wifi client iface + yggTun) | New tap/bridge on a fresh subnet; verify `ip -br addr` post-reboot before promotion |
| R4 | RAM exhaustion — 2Gi guest on ~9.6Gi-free host | file 2 | Medium | Keep zeus unloaded during standup; reduce guest `mem` in the fixture if tight |
| R5 | Display port unreachable / firewalled — "not viewable from ouranos" | file 4 §gap | Medium | Serve SPICE/VNC/QMP on zeus's ygg address; open the firewall port explicitly |
| R6 | ouranos cannot resolve the new domain (hosts entry not in its gen) | file 4 §3 | Medium | Land the hosts entry in ouranos's generation too, or target `zeus.goldragon.criome` directly |
| R7 | Cluster-name / domain-string mismatch (`criome` vs `goldragon`) | file 4 §2 | Low | Projection is data-driven; do not hardcode — verify the rendered string post-deploy |
| R8 | **Prometheus networking broken** | `5hir5bnz`, `kx32`, file 5 | **Eliminated** by host choice | Standup does not touch Prometheus at all |

The whole `5hir5bnz` risk class (R8 and the gemma-class R1 on the router) is
**removed by choosing zeus**. The residual risks (R2–R7) are ordinary
single-Edge-node deploy risks, all bounded and recoverable by reboot.

## Ordered standup steps

1. **Pin the rev.** Record the CriomOS `next` rev carrying `vm-testing`
   (`qnqvptll c1931279` at recon time; re-confirm `jj bookmark list` before
   deploy). Use `github:LiGoldragon/CriomOS/<rev>` everywhere.
2. **Wire the fixture (designer, on a `next`/feature branch in `~/wt`).** Add
   `{ VmTesting = { gpuPassthrough = false; display = "Spice"; gpu = null; }; }`
   to zeus's `services` vector in `goldragon/datom.nota`. Add the host-side tap
   provisioning the module lacks (host tap `vm-testing`, an address/route or a
   small bridge on a fresh subnet, forwarding/NAT as needed) and open the
   chosen display port in zeus's firewall on its reachable address. Operator
   integrates to main per the worktree flow.
3. **Eval / Build gate (no host mutation).** On zeus, run `lojix-cli "(OsOnly
   goldragon zeus <source.nota> github:LiGoldragon/CriomOS/<rev> Build None
   None)"`. A pure build cannot touch networking. Confirm it builds clean.
4. **Confirm CI is green** for `vm-testing-prometheus-policy` on the rev (and
   the booted-VM `runNixOSTest` if run), so the policy logic and a VM boot are
   already proven before touching a live host.
5. **Deploy with `BootOnce`, run on zeus.** `lojix-cli "(OsOnly goldragon zeus
   <source.nota> github:LiGoldragon/CriomOS/<rev> BootOnce None None)"`. The
   activation runs as a durable transient `systemd-run` oneshot owned by PID 1;
   an ssh drop does not kill it. Do **not** use `Switch`.
6. **Reboot zeus** to land the BootOnce generation.
7. **Verify before promoting (verify-then-commit, never stage-and-walk-away).**
   On zeus: `systemctl --failed` clean; `ip -br addr` shows wlp/yggTun healthy
   and the new tap/bridge present with no collision; `/dev/kvm` present; the
   `microvm@vm-testing` unit up; the guest reachable via its display surface;
   `getent hosts vm-testing.goldragon.criome` renders the expected
   (data-driven) string. From **ouranos**: resolve + reach
   `vm-testing.goldragon.criome` (or `zeus.goldragon.criome`) and open the
   SPICE/VNC/QMP client to see the guest.
8. **Promote to default** only after step 7 passes — a deliberate `Boot` (or
   reboot-pin) making the verified generation the persistent default. An
   unverified generation must never be left as the next-reboot default.
9. **If any verification fails, reboot zeus.** BootOnce returns the prior good
   generation automatically; do not retry blind. Capture the failure and re-cut
   the fixture/tap design.
10. **(Later, separately) Prometheus standup.** Once out-of-band/console access
    exists and the zeus standup has proven the host-tap routing, repeat steps
    1–9 against Prometheus under the full `5hir5bnz` protocol (build-only first,
    `BootOnce`, transient unit, verify-then-promote, reboot-to-rollback). Obtain
    psyche sign-off before any Prometheus activation that could need physical
    recovery.

## Prerequisites

- CriomOS `next` rev carrying `vm-testing` pinned (`qnqvptll c1931279`; re-
  confirm).
- A `next`/feature branch (in `~/wt`) adding: zeus's `VmTesting` service entry,
  the host-side tap/route the module omits, and the display-port firewall
  opening — integrated to main by an operator lane.
- `source.nota` = the goldragon cluster proposal
  (`/git/github.com/LiGoldragon/goldragon/datom.nota`).
- Shell access on zeus as the user (lojix-cli escalates internally); zeus
  reachable from ouranos over Yggdrasil (verified).
- A SPICE/VNC/QMP client on ouranos for viewing.
- zeus kept lightly loaded during the standup (RAM headroom ~9.6Gi).
- `vm-testing-prometheus-policy` CI green on the rev.

## What needs psyche input

1. **Host choice confirmation.** `se72` said "full routed microVM, go all the
   way" and the prior recon framed it around Prometheus, but "go all the way"
   names the *microVM*, not the router. This synthesis recommends zeus to honour
   `5hir5bnz` by construction. Confirm zeus is an acceptable first target (with
   Prometheus as a deliberate later step), or state that Prometheus
   specifically is required now.
2. **Routed depth.** The module fronts the guest through the host's display; a
   *fully* routed guest with its own L3 cluster IP/domain (not just the host-
   projected entry) is more work and a domain-criome registration question.
   Confirm whether host-fronted display reachability satisfies "reachable IP +
   own domain," or whether the guest must get its own routed address.
3. **Prometheus precondition.** The risk recon is explicit that Prometheus has
   **no out-of-band/console access today** and the backup AP is not independent.
   Standing up on Prometheus at all should wait for that — confirm we defer
   Prometheus until console access exists.
4. **ouranos-resolution method.** Either land the new hosts entry in ouranos's
   generation (a second deploy) or target zeus's name directly for first
   viewing. Confirm which the psyche wants for the e2e target.
