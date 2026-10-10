# TestVm Guest Login Substrate (bead primary-dw95) — Implementation Evidence

## Task and scope

Complete bead `primary-dw95` per the psyche's open-decision-(e) ruling: COMPLETE
the persistent VM guest surface, do NOT retire it. It is the shared VM-host
reachability substrate the spirit/mirror front (`primary-1e6b`, guests
`mirror-alpha`/`mirror-beta`) composes on; retiring it (removing the VmHost)
would destroy the mirror endpoints. Two code deliverables:

1. Verify the already-landed same-host guest-network fix is correct/complete.
2. Make TestVm guests LOGINABLE (add sshd + user keys to the host-emitted guest
   boot config), generic to all `TestVm` guests — not mirror-specific.

Then record the (e) resolution on `dw95` (keep OPEN), and defer the live
prometheus redeploy + reachability verify (prometheus is the sole builder,
imminently busy with migration verify builds).

## Files consulted

- `CriomOS modules/nixos/test-vm-host.nix` — the guest emitter (edited).
- `CriomOS modules/nixos/{test-vm-guest.nix, users.nix, normalize.nix}` — the
  full-node login identity I lifted down to the boot layer.
- `CriomOS-test-cluster lib/nestedReachability.nix` + `flake.nix` — the
  registered reachability gate proving the network fix.
- `CriomOS-test-cluster fixtures/horizon/atlas.json` — confirmed ex_node
  projections carry NO `adminSshPubKeys`; only `horizon.node.adminSshPubKeys`.
- `agent-outputs/PersistentSpiritMirror/OperatingSystemImplementer-LandAndBuildEvidence.md`
  — peer coordinator round (staged gen 50).
- beads `primary-dw95`, `primary-1e6b`, `primary-1e6b.1`, `primary-1e6b.2`.
- `reports/field-readiness/02-kink-ledger.md` decision (e).

## Observed facts

- Landed network fix `ee49b20` (main tip was `1bf35f80` at start) wires the full
  same-host path: guest binds `nodeIp/128` to its tap by MAC + default `::/0`
  route via host `fe80::1` (GatewayOnLink), gated `guestIsIpv6`; host tap gains
  `fe80::1/64` (answers guest NDP) + the `/128` route; host enables
  `net.ipv6.conf.all.forwarding` (mkDefault); router firewall admits ICMPv6 from
  `vmt*` and forwards `vmt*<->vmt*`.
- The fix is proven GREEN by the registered flake check
  `CriomOS-test-cluster#checks.x86_64-linux.nested-vm-guest-reachability`: atlas
  boots alpha (5::7) + beta (5::8) as nested microvms via `test-vm-host.nix` and
  asserts host<->guest AND guest-A->guest-B over ping AND TCP. The test injects
  test-only probes and explicitly notes "the guests are minimal (no sshd)" —
  confirming the loginability gap was still open.
- The host-emitted guest boot config carried only `hostName` + tap networking +
  `stateVersion`. No sshd, no authorized key → reachable but un-enterable and
  un-deployable-into.
- ex_node projections carry no `adminSshPubKeys`; the host's
  `horizon.node.adminSshPubKeys` is the correct generic source (fixture-verified).
- A peer coordinator round already BootOnce-STAGED prometheus gen 50 from
  `1bf35f80` (closure `61bajpa7...`), one commit below my sshd change; gen 50 is
  network-reachable but sshd-less. prometheus still runs gen 49; gen 50 is the
  bootctl OneShot entry awaiting a reboot.

## Interpretation

- The network fix is correct and complete for the same-host mirror A->B path the
  spirit/mirror front needs; no gap found on read. Two non-blocking caveats
  below.
- Loginability is the missing bootstrap: `test-vm-guest.nix` documents that a
  TestVm guest "REMAINS a real, deployable CriomOS node — sshd keys-only
  (normalize.nix), root authorizedKeys = adminSshPubKeys (users.nix) ... lojix
  deploys into it exactly like any node." But that lojix-into-guest deploy needs
  ssh reachability first, so the host-emitted BOOT image must itself carry sshd +
  a key. That is exactly what I added.

## Changed files

`CriomOS modules/nixos/test-vm-host.nix` (guest `config` block, item (f)):

```nix
services.openssh = {
  enable = true;
  settings.PasswordAuthentication = false;   # keys only, mirroring normalize.nix
};
users.users.root.openssh.authorizedKeys.keys = horizon.node.adminSshPubKeys or [ ];
```

Generic to every TestVm guest (not mirror-specific). openssh `openFirewall`
(default true) opens 22 on the guest tap-facing firewall; `PermitRootLogin`
stays the NixOS default (`prohibit-password`) so the admin key logs in but no
password ever does. Keys are the HOST's cluster-admin keys (ex_node projections
carry none of their own; the operator who governs the VM host governs its
guests). Mirrors `users.nix` `rootUserAkses` + `normalize.nix` sshd policy.

Landed: CriomOS main **`17caaf888b6d`** (parent `1bf35f80`). Pushed
(`git ls-remote origin refs/heads/main` = `17caaf888b6d`).

## Checks run

- `nix-instantiate --parse modules/nixos/test-vm-host.nix` → PARSE OK.
- Pure `nix eval` on a constructed atlas horizon hosting one IPv6 TestVm guest,
  reading the emitted `microvm.vms.alpha.config`:
  `{"hostName":"alpha","netIsMkIf":"if","passwordAuth":false,`
  `"rootKeys":["ssh-ed25519 AAAAADMINKEY li@operator"],"sshdEnable":true}`.
  Proves: sshd enabled, password auth off, host `adminSshPubKeys` flow into guest
  root `authorizedKeys`, hostName intact, and the IPv6 tap binding (network fix)
  untouched.
- Live `lojix "(Query (ByNode (goldragon prometheus None)))"` (read-only):
  prometheus deployment records `1` (store `2j08dj66...`, gen 49) and `38`
  (store `61bajpa7...`, gen 50) — confirms the staged-not-live state.

Did NOT run the live nested-reachability check (needs prometheus KVM — deferred)
nor any prometheus activation.

## Non-blocking caveats (folded into the reachability-verify step)

- Guest-side networking is gated `guestIsIpv6`; an IPv4 TestVm guest would get a
  host route but no guest-side binding. All current TestVm nodes are IPv6
  (5::6/7/8), so inert.
- Direct reachability from an arbitrary tailnet/Yggdrasil peer to a guest needs
  (a) the host to FORWARD inbound tailnet->`vmt*` (the router chain currently
  accepts only `vmt*<->vmt*` + ICMPv6-from-`vmt*`) and (b) Yggdrasil to route
  `5::N` to the host. The operator two-hop path (ssh host, then host->guest; and
  lojix-into-guest which runs over the host) is served by host-originated output
  + the `/128` route + guest sshd, so loginability is met without broadening the
  firewall. Broadening is a live-validated decision for the redeploy, not taken
  here.

## Deferred: live prometheus redeploy + verify (coordinated watched window)

prometheus is the sole builder and imminently busy with migration verify builds.
The redeploy is exactly `primary-1e6b.2`'s vehicle, now unblocked on the CriomOS
side. Run jointly with the mirror lane, after/around the migration builds:

```
# BootOnce (NEVER Switch) System redeploy of prometheus at the landed rev:
meta-lojix "(Deploy (System (goldragon prometheus FullOs \
  /git/github.com/LiGoldragon/goldragon/datom.nota \
  github:LiGoldragon/CriomOS/17caaf888b6d1cb54973cee34e7546e73c88c4a6 BootOnce None [] None)))"
# Poll until the new toplevel is Current:
lojix "(Query (ByNode (goldragon prometheus None)))"
# Start + smoke each guest:
#   ssh root@prometheus 'systemctl start microvm@vm-testing microvm@mirror-alpha microvm@mirror-beta'
# Reachability + LOGIN smoke from prometheus: ping 5::6/7/8, then ssh root@<guestIp> with the admin key.
# Optional gate: nix build CriomOS-test-cluster#checks.x86_64-linux.nested-vm-guest-reachability --print-build-logs
```

CRITICAL interplay: the already-staged gen 50 is from `1bf35f80` (sshd-less). Do
NOT reboot prometheus into gen 50 if the guests must be loginable — RE-STAGE a
BootOnce from `17caaf888b6d` first, then reboot.

## Coordination status

No collision with the mirror lane. Files are disjoint — I edited only CriomOS
`modules/nixos/test-vm-host.nix` (claimed + released via `orchestrate` under lane
`operating-system-implementer`); the mirror lane (`1e6b.1`) edits goldragon
`datom.nota`, and the peer coordinator round's evidence file is a separate file
in this weave dir (untouched). Edited directly (no defer needed on the code).
Deferred only the prometheus activation, per the contention brief.

## Blockers / follow-up

- None on the code (landed + eval-proven).
- Live activation blocked on prometheus-builder contention (deferred, handed to
  `1e6b.2` with exact commands above).
- `dw95` stays OPEN as the shared substrate bead; two notes appended recording
  the (e) resolution + the gen-50 interplay.
