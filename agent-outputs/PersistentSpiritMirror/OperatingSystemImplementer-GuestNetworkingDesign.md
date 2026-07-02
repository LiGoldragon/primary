# Guest-Networking Fix — Design + Decision Record (round 2)

## Scope (coordinator-approved)

Design + implement + sandbox-validate ONLY the guest-networking fix so two
same-host TestVm guests (mirror-alpha / mirror-beta shape) can reach each other.
NO live prometheus deploy this round — go/no-go back to the coordinator first;
the single careful live deploy is the next round.

## Approach chosen: host-as-router (routed point-to-point taps), and why

The guests carry individual `5::N/128` overlay-style node IPs on separate
point-to-point taps, so the topology-consistent path is L3 forwarding through the
host (guest A → host → guest B), building on the already-landed `/128` host-route
fix. This is the coordinator's suggested surgical approach and keeps the module's
existing per-guest point-to-point tap structure (no bridge restructure). A shared
bridge was considered and rejected as no-cleaner: with `br_netfilter` active on
the router, bridged guest↔guest traffic ALSO traverses the `inet filter forward`
chain, so it needs the same firewall allowance while additionally restructuring
tap creation.

## What changed (CriomOS branch `vm-guest-networking`, rev 00131f3ce60a, pushed)

`modules/nixos/test-vm-host.nix`:
- Guest config (`microvm.vms.<guest>.config`) now binds the guest's `<nodeIp>/128`
  to its tap NIC (matched by the deterministic tap MAC, robust to in-guest
  naming) and adds a default IPv6 route via the host tap gateway `fe80::1`
  (`GatewayOnLink`). Without this the guest booted network-dark.
- Host tap `.network` gains `fe80::1/64` (per-link; same on every tap is correct)
  so the host answers guest NDP and acts as gateway/forwarder. Keeps the `/128`
  route.
- Host enables `net.ipv6.conf.all.forwarding` (`mkDefault true`; a router host's
  explicit `true` overrides) when it hosts guests.

`modules/nixos/router/default.nix` (the router's monolithic nftables ruleset —
the ONLY place that can override its `policy drop` forward chain, since an
earlier separate base chain cannot save a packet a later drop-policy chain sees):
- input: `iifname "vmt*" meta l4proto ipv6-icmp accept` (guest NDP + ping to host).
- forward: `iifname "vmt*" oifname "vmt*" accept` (guest↔guest routing).
- Both scoped to `vmt*` devices, which exist only when the host runs TestVm
  guests — inert otherwise.

Both modules parse-check clean. On a feature branch, UNTESTED until the sandbox
reachability check is green.

## Key structural finding that enlarged the scope beyond "3 lines"

1. The host emits MINIMAL guests (no networking, no sshd) — making them reachable
   is a real feature, not a tweak. (The "guest is a full CriomOS node" language in
   test-vm-guest.nix describes the intent, not the minimal host-emitted config.)
2. The existing `runNixOSTest` harness CANNOT wire the real tap (mkVmTest.nix
   crux comment, lines 63-86/170-174: it boots guests as `qemu-vm` nodes on the
   driver's own network). So faithful runtime validation needs a NET-NEW
   nested-microvm harness (one VmHost node booting two microvm guests). Nested KVM
   IS available on prometheus (AMD, `kvm_amd nested=1`) — feasibility positive.
3. The fix touches the router's nftables forward+input chains — small, `vmt*`-
   scoped, auditable rules, but security-adjacent; the sandbox check is exactly
   the mechanism that de-risks them before the live router sees them.

## Validation status

The nested-microvm reachability check (build + prometheus iteration) is delegated
to a background worker; its result lands in
`OperatingSystemImplementer-NestedReachabilityEvidence.md`. Observability plan for
the minimal guests: host↔guest via host `ping` of each guest `5::N`; guest↔guest
via a TEST-ONLY probe injected into each nested guest's `microvm.vms.<name>.config`
(ping/TCP the peer, print a sentinel to the guest console) read back from the
`microvm@<guest>` service journal on the host — no production pollution, no sshd
needed.

## Go/no-go (pending)

Go = the nested check proves A↔B; then land `vm-guest-networking` to CriomOS main
and (next round) the single careful live prometheus deploy. No-go = a specific
sandbox blocker, reported with the fix branch state for the coordinator to weigh.
