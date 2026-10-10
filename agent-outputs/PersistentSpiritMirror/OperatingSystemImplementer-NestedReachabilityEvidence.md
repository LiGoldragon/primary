# Nested Two-Guest Reachability — Fix + Sandbox-Green Evidence

## One-line outcome

GREEN. The guest-networking fix makes two same-host VM guests reach each other:
a nested `runNixOSTest` gate boots `alpha` (5::7) + `beta` (5::8) as real microvm
guests via `test-vm-host.nix` on a real CriomOS router host and proves
`alpha -> beta` by **ping AND TCP over the real tap path**. No live deploy was
run (per the coordinator's hard boundary).

## Scope

Coordinator round: design + implement + sandbox-validate ONLY; do NOT deploy to
the live prometheus router. Build/test drivers on prometheus (sandbox), feature
branches only, no `main` landing until green.

## The fix (CriomOS)

Branch `vm-guest-networking`, rev **`658b20849b6f`** (repo
`/git/github.com/LiGoldragon/CriomOS`). Builds on the already-landed `/128`
host-route fix. Makes the host-emitted (previously network-dark) guests reach
each other, host-as-router over the point-to-point taps:

- **`modules/nixos/test-vm-host.nix`**
  - Guest config: bind `<nodeIp>/128` to the guest tap NIC (matched by the
    deterministic tap MAC `02:00:00:00:00:0<index+1>`) + a default IPv6 route via
    the host tap gateway `fe80::1` (`GatewayOnLink`). Gated to IPv6 node IPs
    (`guestIsIpv6`) so IPv4-node-IP guests are left unchanged (their form differs).
  - Host tap: add `fe80::1/64` to each `05-test-vm-vmt*` network so the host
    answers guest NDP and is the guest's next hop/forwarder.
  - Enable `net.ipv6.conf.all.forwarding` (mkDefault; a router already sets true).
- **`modules/nixos/router/default.nix`** (the nftables ruleset)
  - input chain: `iifname "vmt*" meta l4proto ipv6-icmp accept` (guest NDP + ping
    to the host).
  - forward chain: `iifname "vmt*" oifname "vmt*" accept` (guest A -> host ->
    guest B). Both scoped to `vmt*` — inert on a host with no guests.

## The sandbox gate (CriomOS-test-cluster)

Branch `nested-vm-reachability`, rev **`82e49807557d`** (repo
`/git/github.com/LiGoldragon/CriomOS-test-cluster`). Check
`checks.x86_64-linux.nested-vm-guest-reachability` (`lib/nestedReachability.nix`).

Why nested: the existing harness (`mkVmTest`/`mkDeployTest`) NEVER wires the real
tap — it boots guests as sibling `qemu-vm` nodes on the driver's `192.168.1.0/24`
net (see `mkVmTest.nix` crux comment, lines 63-86/170-174). So a faithful test
requires nested microvm. It works: prometheus has nested KVM (AMD,
`kvm_amd nested=1`), proven first by a standalone `nested-microvm-spike` check.

The gate: one host node `atlas` (a real CriomOS `LargeAiRouter` VmHost, built from
its projection) boots two lean IPv6 `TestVm` guests as NESTED microvms via
`test-vm-host.nix`, then asserts:
1. host reaches both guests (`ping 5::7`, `ping 5::8`) — validates the guest
   binding + host tap `fe80::1` + `/128` route;
2. `alpha` reaches `beta` by **ping** and by **TCP** (a test-only probe injected
   into each nested guest; `beta` runs a TCP echo listener, `alpha` pings +
   TCP-connects and prints sentinels to its console, observed on the host via
   `journalctl -u microvm@alpha`).

### Passing run (exact evidence, `REACH_EXIT=0`)

```
HOST<->GUEST OK: host reaches both 5::7 and 5::8
microvm@alpha[1210]: reach-probe-start[940]: REACH-PING-OK-alpha-to-beta
microvm@alpha[1210]: reach-probe-start[940]: REACH-TCP-OK-alpha-to-beta
microvm@alpha[1210]: reach-probe-start[940]: PROBE-DONE-alpha
NESTED REACHABILITY GREEN: guest alpha reaches guest beta by ping AND TCP over the real tap path
```

Run recipe (prometheus, sandbox — NOT a deploy):
```
ssh root@prometheus.goldragon.criome 'nix build \
  "github:LiGoldragon/CriomOS-test-cluster/nested-vm-reachability#checks.x86_64-linux.nested-vm-guest-reachability" \
  --override-input criomos "github:LiGoldragon/CriomOS/vm-guest-networking" --no-link -L --refresh'
```

## What it took to get green (debugging ledger)

- host↔guest was correct from the first try (host routes `5::7 dev vmt0`,
  `5::8 dev vmt2`; `fe80::1/64` on both taps). The blockers were host-node/test
  substrate issues, not the fix's networking logic:
  1. `documentation.nixos.enable` conflict (normalize.nix vs nixos-test) → force off.
  2. atlas is a `LargeAiRouter` — dragged a multi-GB LLM model → zero the
     `largeAi` behavesAs facet (keeps router + VmHost).
  3. router wifi SAE secret: fixture is not a real sops file → `sops.validateSopsFiles=false`
     (hostapd, its only consumer, is forced off).
  4. guest failed to mount `/sysroot`: the 8 GiB guest images didn't fit the test
     node's disk/RAM-backed store → guest disk 2 GiB + `virtualisation.diskSize`.
  5. flaky TCP-sentinel grep: atlas journald RATE-LIMITED and dropped the guest's
     later console entry amid tailscale/headscale/nix-serve spam → silence those
     services + `journald RateLimit* = 0`, and capture the guest journal once
     after `PROBE-DONE`.

## Caveats / pre-land reconciliation (for the coordinator / next round)

- **projections-match-fieldlab is STALE on the test branch.** The pinned
  horizon-cli hits the fenix rust-stable FOD bomb and cannot regenerate fixtures,
  so `alpha`/`beta` were hand-added to `fixtures/horizon/atlas.json` (cloned from
  `mercury`, IPv6 IPs, ceiling 6) and `clusters/fieldlab.nota` was edited to
  match intent. Before landing the test-cluster branch to main, regenerate the
  fixtures with a buildable horizon and restore `projections-match`. The nested
  check does not depend on that check.
- **Tested rev vs gated rev.** The first green run used CriomOS `00131f3c` (fix
  without the `guestIsIpv6` gate). The branch head `658b20849b6f` adds that gate,
  which is IPv6-path-neutral (for `alpha`/`beta`, `guestIsIpv6` is true, so their
  emitted config is byte-identical) — the green covers the real IPv6 deploy path.
  CONFIRMED: a re-run against the gated head `658b20849b6f` was also GREEN
  (`CONFIRM_EXIT=0`, same `NESTED REACHABILITY GREEN`), so the exact landable rev
  is proven, not just the neutral-gate argument.
- The router `vmt*` firewall rules live in `router/default.nix` (the ruleset is a
  monolithic string, so they cannot be contributed from `test-vm-host.nix`); they
  are scoped to `vmt*` devices and inert without guests. Reasonable, but note the
  mild module coupling.

## Go/no-go recommendation

GO for the single careful live prometheus deploy next round: the fix is
sandbox-proven to make two same-host guests mutually reachable (ping + TCP) over
the real tap path, on a real CriomOS router host, with nested KVM. Before the
live deploy, land `vm-guest-networking` to CriomOS main (re-adding/keeping the
IPv6 gate), reconcile the test-cluster fixtures/projections-match, and deploy
prometheus from that main rev (BootOnce), then boot `mirror-alpha`/`mirror-beta`
and confirm A<->B on the metal.
