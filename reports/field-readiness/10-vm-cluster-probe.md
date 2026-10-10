# VM-Cluster Field Probe — prometheus (2026-07-02)

RECON+WITNESS pass for field readiness. Prior agents claimed the machine's VM
infrastructure "works"; that claim was treated as unproven. Every load-bearing
claim below was witnessed by a command run during this session (2026-07-02,
from ouranos). FACT = observed output. INFERENCE = reasoned. Full two-VM run
log archived in the session scratchpad (`criome-auth-witness-run.log`).

## VERDICT

**USABLE — witnessed.** prometheus boots real KVM VMs, runs real engine
daemons inside them, and passes a two-VM cross-network engine test in ~100
seconds end-to-end; teardown is clean. The one dead surface is the *declared
persistent guest* (`vm-testing`): it boots but is network-dark and
un-enterable (kink 1). The runNixOSTest path — the one a sustained session
would actually iterate on — works today.

## MACHINE SPECS (all FACT, via `ssh root@prometheus.goldragon.criome`)

| Surface | Witnessed value |
|---|---|
| Identity | `hostname` → `prometheus`; goldragon cluster, species LargeAiRouter |
| Reached via | `ssh root@prometheus.goldragon.criome` (BatchMode, key auth, no prompt); resolves to yggdrasil `200:ca41:…:165f`, ping RTT ~24 ms from ouranos |
| CPU | AMD RYZEN AI MAX+ 395 w/ Radeon 8060S — 16 cores / 32 threads (`nproc` → 32) |
| RAM | 124 GiB total, ~121 GiB available at idle (`free -h`) |
| Disk | 1.9 TB NVMe, **913 GB free** (51% used), `/` and `/nix` same fs |
| OS generation | `/run/current-system` → `nixos-system-prometheus-26.05.20260422.0726a0e` (`2j08dj66…`), profile `system-49-link`; **identical to the closure lojix records as Current** (`lojix "(Query (ByNode (goldragon prometheus None)))"` → `FullOs BootOnce Current /nix/store/2j08dj66…`) — the lojix live set is truthful for this node |
| KVM | `/dev/kvm` present, mode `crw-rw-rw-` |
| Nix | 2.34.6; `system-features = benchmark big-parallel kvm nixos-test` |
| Uptime at probe | 1 day 14 h; booted 2026-06-30 22:22 |

## VM INFRA IDENTITY (what it actually is)

FACT — **microvm.nix (QEMU/KVM flavor) + runNixOSTest, no libvirt.**
- `microvm`, `systemd-nspawn`, `machinectl` on PATH; `qemu-system-x86_64`,
  `cloud-hypervisor`, `virsh`, `libvirtd` all absent from PATH (QEMU lives
  inside microvm runner closures: `qemu-host-cpu-only-for-vm-tests-10.2.2`).
- One cluster-authored guest declared: `microvm@vm-testing.service`
  (non-autostart), emitted by CriomOS `modules/nixos/test-vm-host.nix` from
  the horizon `VmHost` payload — prometheus declares
  `(VmHost 169.254.100.0/22 Available 4)` and hosts the one projected ex_node
  with `behavesAs.testVm` (`vm-testing`: Pod, 4 cores, 8 GB RAM, 40 GB disk,
  nodeIp `5::6/128`, superNode prometheus). Witnessed shape: qemu microvm,
  `-smp 4 -m 8192M`, tap `vmt0`, MAC `02:00:00:00:00:01`, auto-created
  40 GB ext4 `root.img`.
- The older `modules/nixos/vm-testing/default.nix` (`VmTesting` service:
  libvirtd, Spice, 2 vcpu/2 GB) is NOT what is deployed — prometheus's
  horizon carries `VmHost`, not `VmTesting`, and no libvirt exists on the
  host. INFERENCE: `test-vm-host.nix` superseded it.
- Ephemeral path: `CriomOS-test-cluster` runNixOSTest checks (`vm-mercury`,
  `vm-dune`, `vm-edge-desktop`, `vm-base-home`, two-VM `criome-auth-witness`,
  two-node `lojix-deploy-smoke`) — runnable natively on prometheus because
  its local nix advertises `kvm nixos-test`.

FACT — prior-agent hearsay quantified: before this probe the declared guest
had **never run** — `journalctl -u microvm@vm-testing` empty across all
listed boots, and the first-run-created `root.img` did not exist.

## BOOT WITNESS

### Witness A — the declared persistent guest (`microvm@vm-testing`)

- `systemctl start microvm@vm-testing.service` → `active`; guest console (via
  journal) reached **`Multi-User System`** in <25 s, gettys up, hostname
  `vm-testing`. BOOT: PROVEN.
- Host tap appeared: `vmt0 UP 169.254.100.1/32` plus route toward the guest.
- NETWORKING: **FAILED.** `ping -6 fe80::ff:fe00:1%vmt0` (guest EUI-64),
  `ping -6 5::6` (declared IP), and all-nodes `ping -6 ff02::1%vmt0` — 100%
  loss; `ip -6 neigh` FAILED; 8 s tcpdump on `vmt0` post-boot: 0 packets.
  Tap counters showed ~30 guest packets at boot then silence. No sshd, no
  vsock in the qemu cmdline, `machinectl list` → "No machines"; the serial
  console is journal-attached (not interactive). EXEC-INSIDE: impossible for
  this guest as declared (see kink 1).
- TEARDOWN: `systemctl stop` → `inactive`, 0 failed units, no qemu processes;
  removed the run-created `root.img`/`booted`/`vm-testing.sock`; state dir
  restored to exactly its pre-boot contents (`current` + `toplevel` symlinks
  only); `vmt0` gone. CONFIRMED.

### Witness B — two-VM engine slice, forced boot (runNixOSTest)

Ran on prometheus:
`nix run "github:LiGoldragon/CriomOS-test-cluster#test-criome-auth-witness"`
(the forced-boot driver — boots both VMs every invocation; cannot be
satisfied by a cached green).

- **Both VMs booted under KVM** (`node-a`, `node-b`; guest dmesg: "Detected
  virtualization kvm"). Whole invocation ~100 s wall clock including nix
  eval/substitution; the in-VM **test script finished in 10.92 s**.
- **Real engine daemons ran inside the VMs**: spirit guardian daemon
  (fail-closed, meta Import + ObserveHead), criome daemons on both nodes,
  persona-router (TCP :7440) on node-b, mirror-witness 0.1.2 + sema-engine
  re-hash on node-b, router-forward-witness 0.4.1 on node-a.
- **Inter-VM networking proven**: node-a (`192.168.1.1/24` on eth1) opened
  `</dev/tcp/node-b/7440` across the virtual LAN and sent real forwards with
  `ROUTER_PEER_ADDRESS=node-b:7440`.
- **Engine semantics exercised, not just boot**: two fail-closed refusals
  (`ForwardRefused AttestationInvalid` for unregistered signer and for
  registered-identity-with-foreign-key), then `ForwardAccepted 0`; the real
  spirit head `326640ac…` durably landed in node-b's mirror and the landed
  body **re-hashed in the VM** to the same head (`MATCH`). Final line:
  `WITNESS GREEN (full chain)`. `EXIT=0`.
- TEARDOWN: driver exits → VMs die; verified 0 qemu processes, 0 failed
  units, memory back to baseline (~120 GiB available); removed the scratch
  dir `/root/field-probe-20260702` after archiving the log. CONFIRMED.

### Iteration cost (FACT)

`nix build --dry-run` on prometheus for `vm-mercury` and `lojix-deploy-smoke`:
only the 2–3 test-run derivations need building; downloads ≤ 27 MiB. A
sustained session pays roughly eval + VM boot per iteration (~1–2 min for a
two-VM test), not a cold build.

## ENGINE DEPLOY/TEST ASSESSMENT

- **Usable today for engine integration testing in VMs.** Witness B is
  exactly the pattern: test-cluster fixtures package real daemons (spirit,
  criome, router, mirror) into VM guests and drive them cross-VM. A sustained
  session can author more such fixtures without touching prometheus's host
  config, and run them via `ssh root@prometheus … nix run/nix build`
  (push-first: refs must be on GitHub; local-path flakes don't travel).
- **Capacity**: ~120 GiB free RAM / 32 threads / 913 GB disk supports on the
  order of a dozen 8 GB guests or many 2 GB ones; the declared-guest path is
  capped at `maximumGuests 4` (cluster-authored), but runNixOSTest clusters
  are bounded only by resources.
- **Whole-engine-in-VMs is still blocked by packaging, not by this machine**
  (audit 24 corroborated): persona, mind, message, harness, system, terminal,
  introspect, orchestrate, spirit, sema have no NixOS modules; only
  router/mirror/repository-ledger/criome/lojix are OS-packaged. Until Stage-3
  packaging lands, "the engine on VMs" means test-fixture slices (proven)
  rather than a declaratively deployed federation node (not yet possible
  anywhere, including here).
- **Deploy machinery in VMs exists**: `lojix-deploy-smoke` (deployer node
  deploys the target's projected config, 2-node runNixOSTest) is one boot
  away on prometheus (dry-run: 3 drvs). Recommended as the sustained
  session's first self-check.

## KINK LEDGER

1. **Declared persistent guest is network-dark and un-enterable.**
   Where: CriomOS `modules/nixos/test-vm-host.nix` — `vmDeclarations` emits a
   guest config of hostname+stateVersion ONLY (no guest-side address, no
   sshd/users, no vsock); and `tapNetworks` hardcodes an IPv4-style `/32`
   onto the guest IP, so IPv6 `5::6` becomes route `5::/32 dev vmt0`
   (witnessed) instead of `5::6/128`; host tap endpoint is IPv4
   (`169.254.100.1`, sliced from `guestSubnet`) while the guest's declared
   nodeIp is IPv6 — address-family mismatch end to end. The
   `vm-testing.goldragon.criome` reachability intent (Spirit 2631 lineage) is
   unrealized.
   Blast radius: the whole "persistent, reachable test VM" surface is
   unusable for a sustained session (boot-only). runNixOSTest path unaffected.
   Likelihood: certain (witnessed).
   Proposed fix: give emitted guests a real guest-side network (assign the
   declared nodeIp inside, or an IPv4 sliced from guestSubnet mirroring the
   host endpoint), sshd + operator key, and a family-correct host route
   (/128 for IPv6). **Needs-a-bead** (CriomOS module change + cluster-facts
   decision + prometheus redeploy).
   Evidence: boot log to Multi-User; 100% loss on EUI-64/declared/ff02::1
   pings; `ip -6 neigh` FAILED; 0-packet tcpdump; `ip -6 route show dev vmt0`
   → `5::/32`.

2. **VM tests cannot be remote-scheduled from ouranos.**
   Where: ouranos `/etc/nix/machines` — prometheus line advertises
   `big-parallel,kvm` but not `nixos-test` (witnessed), so runNixOSTest drvs
   (`requiredSystemFeatures = kvm,nixos-test`) never schedule to it; ouranos
   itself is forbidden to fire QEMU (test-cluster script doctrine).
   Blast radius: medium — a sustained session must wrap every VM test in
   `ssh root@prometheus …` instead of plain `nix build`; forgetting this
   yields a confusing local `nixos-test` scheduling failure.
   Likelihood: certain; hit on the first naive `nix build` of a vm check.
   Proposed fix: either add `nixos-test` to the prometheus builder line
   (one-word host-config change on ouranos — may be a deliberate omission per
   the run-criome-auth-on-prometheus doctrine, so confirm intent first) or
   codify the ssh-run pattern in the session's skill surface.
   **Needs-a-bead** (host-config/doctrine decision), though the edit itself
   is cheap.
   Evidence: `cat /etc/nix/machines`; script comment in
   `CriomOS-test-cluster/scripts/run-criome-auth-on-prometheus`.

3. **Malformed CriomOS flake registry on prometheus.**
   Where: `flake-registry = /nix/store/x9ykb0…-criomos-flake-registry.json`;
   its entries are `{"from":{"id":…},"to":{"rev":…,"type":"github"}}` with
   **no `owner`/`repo`** → every flake op prints
   `warning: cannot read flake registry … input attribute 'owner' is missing`
   and all indirect registry aliases (`criomos-home`, `home-manager`, …) are
   dead. Direct `github:owner/repo` refs work (witnessed — Witness B ran).
   Blast radius: low-medium — noise on every command; any tooling that leans
   on registry aliases breaks.
   Likelihood: certain, every nix invocation.
   Proposed fix: emit `owner`/`repo` (+`type:"github"`) in the CriomOS
   registry generator. **Cheap-safe-fix** in CriomOS source; reaches the host
   at next deploy.
   Evidence: warning during `nix shell nixpkgs#tcpdump`; `head` of the
   registry file.

4. **`microvm -l` inventory is blind.**
   Where: prometheus, `microvm -l` → empty output despite a declared guest in
   `/var/lib/microvms/vm-testing` (witnessed). The stock CLI assumes a
   `git+file:///etc/nixos` flake (per its usage text), which CriomOS hosts
   don't have. Blast radius: low — the systemd units and `/var/lib/microvms`
   are the real interface; but naive inventory during a session silently
   reports "no VMs". Likelihood: certain when used. Proposed fix: none needed
   if doctrine says "use systemctl + /var/lib/microvms"; note it in the
   operating doctrine. **Cheap-safe-fix** (doc line).
   Evidence: `microvm -l` empty vs `ls /var/lib/microvms`.

5. **Push-first iteration loop.**
   INFERENCE from witnessed mechanics: prometheus runs tests from
   `github:` refs (and the reproduce script hard-requires a clean, pushed
   revision). A sustained session editing fixtures locally must push every
   iteration before prometheus can see it; there is no sanctioned local-path
   channel to the VM host. Blast radius: latency + forced commit granularity;
   also GitHub becomes a hard availability dependency of the inner test loop.
   Proposed fix: accept (it matches the workspace's pushed-refs doctrine), or
   add a `nix copy`-based derivation-shipping path if loop latency bites.
   Classification: doctrine-accept for now; **needs-a-bead** only if latency
   becomes real friction.

6. **Declared-guest capacity model is heavyweight.**
   INFERENCE (from `test-vm-host.nix` + horizon): adding a *declared* VM to
   the cluster means authoring an ex_node in goldragon cluster facts,
   re-projecting, and redeploying prometheus's system — versus zero host
   changes for runNixOSTest guests. With kink 1 open, the declared path has
   no working payoff yet. Not a session blocker (ephemeral path suffices);
   fold into the kink-1 bead.

## BLOCKERS NEEDING THE PSYCHE

**None.** Access (root SSH), KVM, disk, RAM, cache, and network all
witnessed working; no account, spend, or physical action is required for a
sustained session to run VM clusters on prometheus. The only psyche-shaped
question is intent confirmation on kink 2 (is the missing `nixos-test`
builder feature deliberate?) — answerable in one sentence, not blocking
(the ssh-run path works today).

## COMMANDS CONSULTED (non-exhaustive core)

`lojix "(Query (ByNode (goldragon prometheus None)))"`; horizon projection at
`/var/lib/lojix/generated-inputs/goldragon/prometheus/full-os/horizon/horizon.json`;
`ssh root@prometheus.goldragon.criome` for: specs (`nproc`, `lscpu`,
`free -h`, `df -h`, `readlink /run/current-system`), infra discovery
(`systemctl list-units`, `command -v`, `ip -br addr`), Witness A
(`systemctl start/stop microvm@vm-testing`, `journalctl -u …`, pings,
tcpdump, state-dir restore), Witness B
(`nix run github:LiGoldragon/CriomOS-test-cluster#test-criome-auth-witness`,
log at scratchpad `criome-auth-witness-run.log`), teardown checks (`pgrep
qemu`, `systemctl --failed`), and dry-runs of `vm-mercury` /
`lojix-deploy-smoke`. Source read: CriomOS
`modules/nixos/{test-vm-host.nix,vm-testing/default.nix}`,
CriomOS-test-cluster `flake.nix` + `scripts/run-criome-auth-on-prometheus`.
No host config was mutated; no commits made (recon brief).
