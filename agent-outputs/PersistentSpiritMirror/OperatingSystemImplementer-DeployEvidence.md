# Operating-System Implementer — Persistent Two-VM Prometheus Deploy Evidence

## Task and scope

Deliver two persistent, network-reachable VM guests (node A, node B) on the live
`prometheus` server that can reach each other over the network — foundation for a
Spirit A→B mirror. Beads: epic `primary-1e6b`, covering `.1` (author the two VMs)
and `.2` (reproject + redeploy prometheus). Real production deploy; host-safety
first; do not break prometheus's existing services.

## Outcome in one line

The two guests are **authored, pushed, and correct**, and the `/128` networking
fix is **landed on CriomOS main**. But mutual A↔B reachability is **NOT
achievable with the available fix** — empirically confirmed on the live host —
and the live-router deploy required to ship the fix is a **large non-additive
main-jump**. Per the brief's explicit guardrails ("if the guests come up
unreachable, STOP and report"; "if the deploy would risk existing prometheus
services, stop rather than force it"), **I did NOT run the live prometheus
deploy.** Both guardrails are triggered. Details below.

## What I changed and pushed (durable)

1. **CriomOS main → `4f7953ebbbff`** (pushed). Landed the `/128` IPv6 guest-route
   fix into `modules/nixos/test-vm-host.nix`. This is byte-identical to the
   pre-written `enable-vm-hosting-prometheus` commit `ec198d4`.
   - The "rebase" collapsed to a one-file cherry-pick: `git diff main..branch`
     for `test-vm-host.nix` was exactly `ec198d4`. The branch's other two commits
     are already handled on main — the VmHost reconcile (`69458d7`) is already
     present on main (main's `test-vm-host.nix` blob == the branch's parent blob
     `5853f88`), and the clavifaber repin (`8b08a41`) is superseded (main's
     clavifaber rev `39f65fa1…` differs from and post-dates the branch's
     `1397a6bd…`). Merging the branch wholesale would have REVERTED ~2 weeks of
     main progress (criome/persona-router integration, INTENT elimination, lojix
     repins), so I applied only the one needed hunk.
   - The fix makes the host route prefix family-aware:
     `guestRoutePrefix = ip: if lib.hasInfix ":" ip then "128" else "32"`, and the
     route destination becomes `${guestIp}/${guestRoutePrefix guestIp}`.
   - Parse-checked (`nix-instantiate --parse` OK) and diffed byte-identical to the
     branch version.

2. **goldragon main → `824ffe6498c3`** (pushed). Authored two persistent TestVm
   guests in `datom.nota`, copying the `vm-testing` precedent exactly:
   - `mirror-alpha` — TestVm/Pod, 4 cores / 8 GiB / 40 GiB, superNode prometheus,
     location home-lab, `nodeIp 5::7/128`, `[(TailnetClient)]`, distinct ed25519
     host pubkey.
   - `mirror-beta` — same shape, `nodeIp 5::8/128`, distinct ed25519 host pubkey.
   - The two ed25519 host keypairs were generated throwaway (TestVm guests
     self-generate their real host key on first boot — `vm-testing` has no secret
     either); only the public bodies are in the datom. No private key material was
     stored durably.
   - Validated by projecting: `horizon-cli --cluster goldragon --node prometheus <
     datom.nota` projects cleanly and both guests appear as exNodes with their
     node IPs. prometheus already declares `(VmHost 169.254.100.0/22 Available
     (Some 4))`, so it now hosts 3 TestVm guests (vm-testing + 2), under the ceiling.

3. **Housekeeping** (task Do #5): dropped the stale "private / authorization-gated"
   goldragon framing.
   - Bead `primary-1e6b.1`: retitled ("public goldragon datom"), rewrote the
     description (authored+pushed, records the reachability blocker), removed the
     `authorization-gated` label.
   - Added dated correction banners to `TrackerWeaver-WeavePlan.md` and
     `Scout-SituationalMap.md` and fixed the load-bearing lines.

## The load-bearing finding: `/128` is necessary but NOT sufficient

The brief framed the `/32`→`/128` route as "the ONE remaining fix". A fresh
read-only source pass (parallel Explore agent) plus **live read-only checks on
prometheus** prove the guests still boot network-dark after that fix. The Scout's
original "kink 1" already flagged this ("declared guests are network-dark and
un-enterable; a real prerequisite, not cosmetic"); the brief simplified it away.

### Live prometheus evidence (read-only, 2026-07-03)

- Host is healthy: `systemctl is-system-running` → `running`; reachable over ssh.
- Current gen: `goldragon prometheus FullOs BootOnce Current` (gen/deploy `1 1`),
  store path `…-nixos-system-prometheus-26.05.20260422.0726a0e`. Only ONE lojix
  generation ever, written ~2026-06-20.
- `microvm@vm-testing.service` is `loaded inactive dead` (present, not running;
  autostart=false).
- **The `/32` bug is live**: `/etc/systemd/network/05-test-vm-vmt0.network` has
  `Destination=5::6/32` (my fix → `5::6/128`).
- **Host tap is IPv4-only**: `Address=169.254.100.1/32` — no IPv6 on the tap, so
  NDP for the guest's `5::N` cannot resolve.
- **IPv6 forwarding is ON** (`net.ipv6.conf.all.forwarding = 1`) BUT the router's
  nftables forward chain is `policy drop`, permitting only `br-lan ↔ eno1`
  (LAN↔WAN). The guest taps (`vmt*`) are neither, so **tap↔tap (guest↔guest)
  forwarding is dropped.**

### Static source evidence (Explore, CriomOS repo, cited)

- The host emits a **minimal** guest config (`test-vm-host.nix` `vmDeclarations`):
  only `microvm` (hypervisor/vcpu/mem/volumes/interfaces), `networking.hostName`,
  `system.stateVersion`. **No address is put on the guest's tap NIC.**
- The only place `node.nodeIp` binds to an interface is
  `modules/nixos/network/wireguard.nix` (`wgNode.ips = [ node.nodeIp ]`), gated on
  `hasWireguardPubKey` — and it lands on the WireGuard interface, not the tap. The
  new guests have no wireguard pubkey, so `5::N` is bound nowhere at runtime.
- `network/networkd.nix` (DHCP/RA on `10-main-eth`) is gated `center && !router`;
  a TestVm guest is not `center`, so it never applies.
- `TailnetClient` renders to tailscale with **manual enrollment only** ("Phase 1
  scaffolding", no auth key) → no overlay address at boot. Yggdrasil runs but has
  **no peers** configured across the point-to-point taps. So no overlay bridges
  the two guests either.

### Net verdict

After a plain boot, guest A cannot reach guest B — by the tap path (guest never
claims `5::N`; host tap has no IPv6; router drops tap↔tap), by WireGuard (no
pubkey; and it wouldn't use the tap anyway), by tailscale (manual enrollment), or
by yggdrasil (no peers). The `/128` fix corrects the host's *route* but the guest
side, the host tap IPv6, and the forward-chain allowance are all still missing.

## Why I did NOT run the live deploy (STOP decision)

Two of the brief's explicit guardrails are triggered:

1. **Guests would come up unreachable.** The reachability outcome is unachievable
   with the available fix (proven above). The brief: "If … the guests come up
   unreachable, STOP and report the specific failure — do not force it."

2. **The deploy is a large non-additive blast radius on a live router.** Shipping
   even the `/128` fix means deploying CriomOS main (`4f7953ebbbff`) to a
   production router that has only ever run ONE gen (~Jun 20). Main has since
   integrated the criome (T2) + persona-router (T3) modules, eliminated INTENT.md,
   and repinned lojix/clavifaber — none of it the "additive two-guests + tiny
   route fix" the brief imagined. prometheus is also the cluster's build host,
   nix cache, tailnet node, and Wi-Fi router. The brief: "if the deploy would risk
   existing prometheus services, stop and report rather than force it."

Deploying is genuinely SAFE-to-attempt in the narrow sense (BootOnce builds first
and auto-rolls-back; the new microvm units are autostart=false; the tap networks
are additive) — but it would (a) not achieve the goal and (b) carry the main-jump
service risk, so forcing it serves neither the outcome nor host-safety.

## What it would take to actually deliver A↔B reachability (recommendation)

This is net-new CriomOS guest-networking work, NOT a pre-written fix. Concretely,
one of:

- **Host-as-router path**: give each guest's tap an IPv6 address on the host
  (host tap gets an IPv6 endpoint so NDP resolves), bind `5::N` to the guest's tap
  inside the emitted guest config (a `behavesAs.testVm` guest-networking module),
  give the guest a route toward the host, and add an nftables forward-chain
  allowance for `vmt* ↔ vmt*` on the router. Then A→host→B routes.
- **Shared-bridge path**: put both guests on one bridge / shared `/64` so they are
  on-link and ping directly (host bridges rather than routes) — a cleaner redesign
  of `test-vm-host.nix` guest emission.
- **Overlay path**: automatic tailnet enrollment (tailscale auth key) or explicit
  yggdrasil peers so the guests get overlay addresses independent of the tap.

Whichever is chosen should be **validated first in `CriomOS-test-cluster` via a
two-guest `runNixOSTest` reachability check** (the `lojix-deploy-smoke`
two-node pattern is the template) BEFORE it is deployed to the live router. Doing
first-try guest-networking design on the production router is the host-safety risk
the brief warns against.

Then the deploy (once the fix is validated) is:

```
meta-lojix "(Deploy (System (goldragon prometheus FullOs \
  /git/github.com/LiGoldragon/goldragon/datom.nota \
  github:LiGoldragon/CriomOS/<rev> BootOnce None [] None)))"
```

(9-field System shape confirmed from the prior working ouranos deploy in
`agent-outputs/BootOnceColemakDeploy/…`; proposal-source is the LOCAL datom path,
which the running lojix-daemon reads directly; `BootOnce` is prometheus's
established safe action.) Then `lojix "(Query (ByNode (goldragon prometheus
None)))"` until the expected store path is `Current`, boot each guest
(`systemctl start microvm@mirror-alpha microvm@mirror-beta`), and prove
reachability with `ping`/`ssh` A↔B.

## Checks run (exact)

- `git diff` main↔branch for `test-vm-host.nix` == `ec198d4` (byte-identical).
- CriomOS: `nix-instantiate --parse modules/nixos/test-vm-host.nix` → OK.
- CriomOS: `jj commit` + `jj bookmark set main` + `jj git push` → main `4f7953ebbbff`.
- goldragon: projected `datom.nota` for prometheus → both guests present as
  exNodes with `5::7/128` / `5::8/128`; clean parse (NOTA count-strict decode OK).
- goldragon: `jj commit` + push → main `824ffe6498c3`.
- prometheus (read-only ssh): health `running`; live `/32` route bug confirmed;
  host tap IPv4-only; IPv6 forwarding on; nft forward `policy drop` (only
  br-lan↔eno1); `microvm@vm-testing` inactive.
- lojix `(Query (ByNode (goldragon prometheus None)))` → gen `1 1` Current.
- NO `meta-lojix` mutation, deploy, activate, or build was run. No host state
  was changed. Only read-only ssh diagnostics + read-only lojix Query.

## Blockers / follow-up

- **BLOCKER (reachability):** guest-side networking is unbuilt; A↔B is not
  reachable with the `/128` fix alone. Net-new CriomOS work + test-cluster
  validation required (recommendation above). Recorded on `primary-1e6b.1` and
  refines `primary-dw95` (kink-1).
- **DECISION for the psyche:** whether to authorize the guest-networking design +
  test-cluster validation, and separately whether a live prometheus main-jump
  redeploy (to carry the `/128` fix) is acceptable now or should wait until the
  full guest-networking fix is ready (so prometheus is redeployed once, not twice).
- Coordination note: the `orchestrate` daemon was unreachable (connection
  refused) for the whole session, so path claims could not be registered; the
  CriomOS and goldragon checkouts were clean/uncontended and edited directly.
- Primary working copy carried substantial peer changes from other sessions
  (MindLiveJudgeEval, NotaStrictPositional, field-readiness, an AGENTS.md edit,
  generated-skill drift); named at closeout per whole-working-copy doctrine.
