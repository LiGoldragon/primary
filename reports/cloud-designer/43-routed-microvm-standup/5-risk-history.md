# 43 · Routed microVM standup — risk history + safety protocol

Cloud-designer recon sub-agent, session 43, dimension 5. READ-ONLY. Every
claim cites a Spirit record (by short code), a report path, or a command run.

## Bottom line

Standing up the routed microVM means deploying a CriomOS config to **Prometheus
— the cluster router** — and adding a tap/bridge + projected Criome domain. The
single binding gate is `5hir5bnz` (Prometheus-networking-non-breakage). It is
not a live retrievable record from this socket (`spirit "(Lookup 5hir5bnz)"` →
`record not found`), but it is the canonical *name* of the constraint family,
cited verbatim by the governing decision `se72` ("Honour constraint 5hir5bnz
and do not break Prometheus networking while standing it up") and by
system-designer report 69 (`§Intent anchors`, line 20-22). Its operative
content is carried by three live, High-certainty Deployment constraints —
`kx32`, `xv9v`, `1lex` — all in domain
`(Technology (Software (Operations Deployment)))`. Treat those three as the
enforceable text of `5hir5bnz`.

## What `5hir5bnz` forbids (the binding text, from the three live records)

- **`kx32` (Constraint, High)** — the root rule. "Deploying to prometheus must
  not knock out its network connectivity. prometheus is the cluster router
  running hostapd and dnsmasq; a **live switch activation restarts those
  services and drops the connection** we reach it through, **which is what broke
  during the gemma deploy**. Future deploys to the router node must avoid
  restarting networking live: use **boot-mode activation rather than a live
  switch**, or an approach that preserves connectivity, and prefer out-of-band
  or console access before any risky activation **since there is none today**."
- **`xv9v` (Constraint, High)** — the activation-path rule. "Prometheus deploys
  should use the safe **BootOnce path rather than Switch** until console/
  out-of-band access and sign-off are in place; avoid leaving an **unverified
  generation staged for the next reboot** unless deliberately accepted."
- **`1lex` (Constraint, High)** — the durability rule. "Prometheus live switch
  and promotion operations that may disrupt SSH or Wi-Fi must be launched as
  **durable systemd transient units** so the operation continues even if the
  agent's SSH session drops and reconnect is needed."

So `5hir5bnz` forbids, concretely: (1) a live `switch-to-configuration switch`
on Prometheus that bounces `hostapd`/`networkd`/`kea`/`dnsmasq` (the gemma
incident — see `kx32`); (2) any activation whose connectivity is unproven, run
without out-of-band fallback; (3) leaving an unverified generation as the
default boot target (`xv9v`); (4) running the risky step inside the foreground
SSH session rather than a detached transient unit (`1lex`).

## The concrete risk surface

### What could break Prometheus networking

Prometheus is role `LargeAiRouter` (`goldragon/datom.nota:59,95`, per
cloud-designer report 41/10 §3). The router config
(`CriomOS@main:modules/nixos/router/default.nix`, read via
`jj file show -r main`) runs the live access path: `hostapd` (line 166), `kea`
DHCP on `br-lan` (line 193), `dnsmasq`, and the `br-lan` bridge (`20-br-lan`,
line 346). The reachable SSH/Wi-Fi path to Prometheus rides this stack. A
microVM deploy adds a **tap interface + microvm bridge + nftables forward/NAT
rules + a projected `networking.hosts` Criome-domain entry**
(report 69 §"What was implemented"). The risk vectors:

1. **Bridge/tap collision with `br-lan`.** A new VM bridge or tap that overlaps
   br-lan addressing, MAC/bridge membership, or steals the WAN forward path can
   sever client routing.
2. **nftables forward/NAT rule edits.** The router's `nat`/`forward` chains
   currently allow `br-lan ↔ wan` (report 11 §Path A); a microVM subnet needs
   its own forward rule, and a careless edit to the chain can drop br-lan↔wan.
3. **Service restart on activation.** The historical kill mechanism: a live
   `switch` restarting `hostapd`/`networkd`/`kea`/`dnsmasq` drops the very
   connection we hold (`kx32`). This is the gemma-deploy incident.
4. **A bad new generation booted.** Even with no live bounce, rebooting into a
   generation whose `br-lan`/`kea`/`dnsmasq`/firewall config is broken locks the
   node out (report 11 §"Why it matters", record `1144`).

### Mitigations already in the tree (reduce, do not remove, the gate)

- **No-bounce guards are LIVE on `main`** (verified
  `jj file show -r main modules/nixos/router/default.nix`, lines 241-258):
  `systemd-networkd`, `hostapd`, `dnsmasq`, `kea-dhcp4-server` all carry
  `restartIfChanged = false` and `stopIfChanged = false`. So even a live
  `switch` no longer bounces the router services — this kills the `kx32`
  mechanism at the source (cloud-designer report 11 §Status reconciliation).
  It protects the *deploy*, not a *bad new generation*.
- **Backup admin network** (`wn7q`, `l01b`): a separate hostapd
  (`hostapd-backup-wireless`, router default.nix line 262) + USB devices,
  intended as an independent dumb path. **Caveat (report 11, the open
  finding):** as built (`c250d9a`) the backup AP and USB-eth are *bridged into
  br-lan* (`bridge=br-lan`, line 286), so they share br-lan's L3 fate and do
  **not** yet satisfy `1145`'s "independent of kea/dnsmasq" — they give L2
  association but no IP/DNS if the main stack is down. So the backup is NOT a
  reliable rollback path for a bad-generation lockout today. This is an open
  psyche call (report 11 Path A vs B). Do not rely on it as the safety net.
- **gpuPassthrough is forced false on Prometheus** (`cncj`, report 69) — the VM
  feature does not touch VFIO/IOMMU on the router node, removing one whole class
  of boot-time risk.
- **There is no out-of-band/console access today** (`kx32`: "there is none
  today"; report 11 line 24: `primary-lome` OPEN). This is the most important
  fact: a lockout is **not remotely recoverable** — it needs physical access.

## Safe-test protocol to honour `5hir5bnz`

Combine the three constraint texts into one ordered procedure. Build and CI are
already proven on `next` (`qnqvptllvnrk`, report 69: eval + booted-VM
`runNixOSTest` PASS); the risk is entirely at the *activation on Prometheus*
step.

1. **Build, never switch live.** Build the new Prometheus toplevel (closure)
   first — `nix build` on Prometheus over its wired LAN (`8qnc`), no activation.
   A pure build cannot touch networking.
2. **Activate via `BootOnce`, not `Switch`** (`xv9v`). Use
   `switch-to-configuration boot` + a one-shot boot entry (or the lojix
   `BootOnce` action once it is unblocked — currently lojix rejects all
   activating actions, report 41/10 §6) so the *current* running generation and
   its live router services are untouched. Nothing about the live `hostapd`/
   `kea`/`dnsmasq`/`br-lan` changes until a deliberate reboot.
3. **Launch the risky step as a durable transient unit** (`1lex`):
   `systemd-run --unit microvm-standup ...` so the operation survives an SSH
   drop and is re-attachable by reconnect. Never run activation in the
   foreground SSH session.
4. **Verify-then-commit, never stage-and-walk-away** (`xv9v`). After reboot into
   the BootOnce generation: confirm SSH/Wi-Fi still reachable, `hostapd`/`kea`/
   `dnsmasq`/`br-lan` healthy (`systemctl --failed`, `ip -br addr`), AND that
   the microVM's tap/bridge and `vm-testing.<cluster>.criome` resolve without
   conflicting with br-lan. Only after that verification do you make the
   generation the **default** boot target. An unverified generation must NOT be
   left as the next-reboot default (`xv9v`).
5. **Rollback trigger + path.** If post-reboot connectivity or any router
   service is degraded: BootOnce means a **plain reboot reverts to the last
   good generation** — that is the rollback. Because there is no out-of-band
   access (`kx32`) and the backup AP is bridged/not-independent (report 11), do
   NOT promote the new generation to default until step 4 passes, and obtain
   psyche sign-off before any operation that could need physical recovery. The
   trigger condition is binary: SSH unreachable after reboot, or any of
   networkd/hostapd/kea/dnsmasq in `--failed`, or br-lan↔wan forwarding lost →
   reboot to prior generation, do not retry blind.
6. **Prefer the lower-risk fallback first.** The nspawn path on Prometheus
   (`dune-nspawn-toplevel`, report 41/10 §7) gives a host-local container IP
   with no router-config change at all and is the proven E2E target; the routed
   microVM is the strictly higher-risk step `se72` deliberately chose to "go all
   the way" on. Sequence: prove the daemon/deploy mechanics on nspawn, then do
   the routed-microVM standup under steps 1-5.

## Sources

- Spirit: `5hir5bnz` (name of the gate; not live-retrievable, cited by `se72`
  and report 69), `kx32` / `xv9v` / `1lex` (the live binding text, all
  High-certainty Deployment Constraints), `se72` (governing Decision: full
  routed microVM target, honour 5hir5bnz), `cncj` (gpuPassthrough false on
  Prometheus), `wn7q` / `l01b` (backup network), `1144` / `1145` (backup
  independence intent, referenced in report 11), `8qnc` (prefetch over wired
  LAN). Retrieved via `spirit "(Lookup ...)"` and
  `spirit "(Observe (... (ContainsText router|prometheus) ...))"` → LookupStash.
- Reports: `reports/cloud-designer/41-lojix-production-refresh/10-test-cluster-and-vm.md`
  (host/role, nspawn vs microVM, the `5hir5bnz` gate at §3/§7),
  `reports/system-designer/69-criomos-vm-testing-feature-landed-2026-06-04.md`
  (the vm-testing module + the `5hir5bnz` deploy gate, §Intent anchors / §gated),
  `reports/cloud-designer/11-backup-network-implementation-review-2026-05-29.md`
  (no-bounce guards landed; backup-NOT-independent open finding; gemma incident).
- Code (read-only via jj): `CriomOS@main:modules/nixos/router/default.nix`
  — no-bounce guards at lines 241-258, hostapd/kea/dnsmasq/br-lan at 166/193/346;
  `CriomOS` branches: `main` @ `wwpyzmtwtooz`, `next` @ `qnqvptllvnrk` (carries
  vm-testing, undeployed).
