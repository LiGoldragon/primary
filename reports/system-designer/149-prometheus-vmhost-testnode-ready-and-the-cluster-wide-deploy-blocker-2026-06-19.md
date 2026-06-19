# 149 — Prometheus VM-host test node: change ready + proven router-safe, blocked by a cluster-wide deploy breakage

*The psyche has asked for days to enable VM hosting on prometheus and stand up a
durable test VM node, and it was never deployed. This prepared the real change (no
QEMU, no deploy — pure builds only), proved it is purely additive and cannot disturb
the live router, and in doing so found why nothing has been deploying: the CriomOS
build is broken cluster-wide by a deleted dependency. Tracked as bead `primary-dw95`
(P1, the prometheus test-node stand-up). Branches: `goldragon:enable-vm-hosting-prometheus@a477c96d`,
`CriomOS:enable-vm-hosting-prometheus@fd780e10` — both ~/wt feature branches, not
integrated.*

## Status

The VM-hosting change is **written and additive-safe** — prometheus's router and
networking config is provably untouched. It is **not yet deployable**, blocked by two
pre-existing problems (not introduced by this change): a cluster-wide build breakage,
and the CriomOS branch needing a rebase. Once those clear, the node is a single
BootOnce deploy away.

## The change

The goldragon datom (`datom.nota`) carries two prometheus edits:

```
- [(TailnetClient) (NixBuilder (Some 6)) (NixCache)]
+ [(TailnetClient) (NixBuilder (Some 6)) (NixCache) (VmHost 169.254.100.0/22 Available (Some 4))]
```

The tap subnet `169.254.100.0/22` is RFC3927 IPv4 link-local (the `TapSubnet` type is
IPv4-only) and collides with nothing — not the cluster `5::/x` node-IP space, not the
tailnet, not prometheus's router LAN `10.18.0.0/24`. `Available` reflects prometheus's
real `/dev/kvm`; `(Some 4)` is the guest ceiling.

Second, a durable `TestVm` node `vm-testing`: a `Pod` with `super_node = prometheus`,
`X86_64`, 4 cores / 8 GiB / 40 GiB, `node_ip 5::6/128` (next free slot after prometheus
`5::5`), a generated Yggdrasil keypair and SSH host keypair (publics authored, privates
not stored — see Gaps), criome domain `vm-testing.goldragon.criome` projected
automatically, plus a `vm-testing Max` node-trust entry.

The CriomOS branch is pure deletion: keep the already-typed `test-vm-host.nix`
(byte-identical to main), delete the dead string-keyed `vm-testing/default.nix` (the
old `autostart=true`/libvirtd/persistent-tap hack that gated on a non-existent
service), its `criomos.nix` import, and its flake check. This is the substance of bead
`primary-wvey` (the typed-source-first cleanup).

A separate **pre-existing schema drift** was found and fixed in the goldragon branch:
the committed datom no longer parsed against horizon-rs main (missing the 5th
`ClusterProposal` root `(criome [...])` and three trailing `Machine` fields). That
migration (36 insertions, 7 deletions) unblocks *every* deploy and should be reviewed
on its own merits.

## Safety — purely additive, router untouched (verified three ways)

- **Git delta:** prometheus's only behavioral change is the one appended `VmHost`
  service; the new node and the cluster `criome` domain are new data; the `Machine`
  widening is defaulted `None`/`[]`.
- **Projection (horizon-cli):** prometheus with vs without `VmHost` differs by exactly
  one appended `services` entry. Router interfaces (`eno1`, `wlp195s0`, backup
  wireless), `nodeIp 5::5/128`, criome domain, machine, and all public keys identical.
- **Full toplevel config eval (control vs new):** exactly THREE additions, ZERO
  removals or modifications — (a) `systemd.network` gains `05-test-vm-vmt0` (matches
  `vmt0` by name only, address from the guest subnet not the host IP,
  `RequiredForOnline=no`, no default route); (b) `microvm.vms` gains `vm-testing` while
  `microvm.autostart` stays `[]`; (c) `networking.hosts` gains one inert `/etc/hosts`
  alias. **Byte-identical** between control and new: WAN, the LAN bridge
  (`10.18.0.1/24`), tailscale, hostapd, kea DHCP, nftables, NAT, IP forwarding.

The `kx32` router-restart protection is confirmed present at the evaluated level
(`modules/nixos/router/default.nix:241-246`: `systemd-networkd.restartIfChanged=false`
+ `stopIfChanged=false`, hostapd/dnsmasq the same) — so even with the new
`.network` file present, an activation would not restart networkd to pick it up. The
`vmt0` tap appears only when `microvm@vm-testing` starts, and `autostart=false` means
it never starts at boot. The guest is inert until `systemctl start
microvm@vm-testing.service`.

**Honest caveat:** this is a pure-evaluation proof. No nixosTest, no QEMU, no VM was
booted, no SSH to prometheus. The deep store realization of the closure was *not*
exercised — blocked by the `nota-derive` fetch below.

## The blockers (why nothing has been deploying)

- **CLUSTER-WIDE BUILD BLOCKER (the headline):** `inputs.clavifaber`'s `Cargo.lock`
  still references the renamed/deleted `LiGoldragon/nota-derive` repo, fetched via
  import-from-derivation in `modules/nixos/complex.nix`. This fails the toplevel build
  for **every** node — proven by an identical failure on unmodified `tiger`, not just
  VM hosting. **Until clavifaber is bumped onto `nota-next` and CriomOS's clavifaber
  input repinned, no node's closure realizes.** This is the deploy pipeline being
  broken at the root.
- **CriomOS branch rebase:** `fd780e10` predates `fdd07e2` (browser-agent home pin) and
  `fcd9f79` (lojix daemon git for flake eval); deploying as-is would revert both. Must
  rebase onto current CriomOS main before any build.

## Smaller gaps before a working node

- **Key provisioning (decision):** the node has an authored Yggdrasil public key, so
  `yggdrasil.nix` sets `seedYggdrasil=false` and expects the matching private key on
  the guest (same for SSH host key). The privates aren't in `goldragon/secrets`. Two
  valid choices: provision the private keys, or **switch the datom ygg entry to `None`
  so the guest self-seeds at first boot** — the simpler path for a test node. Default
  recommendation: self-seed.
- **Route bug (non-blocking):** `test-vm-host.nix:273` hardcodes `/32`, so the guest
  route emits `5::6/32` — an IPv4 prefix on an IPv6 address; should be `/128`. Inert at
  activation (tap is down until the guest starts) but the reachability route is
  malformed. Fix before relying on routed reachability.
- **Criome admission:** the `vm-testing.goldragon.criome` domain projects as cluster
  data, but live criome admission for the new domain couples to the cluster-root
  admission ceremony and must be confirmed at bring-up.

## Deploy (cluster-operator / system-operator; psyche-gated)

The live-router activation is **not designer territory** — it is cluster-operator /
system-operator on the production router. prometheus is a live `LargeAiRouter`:
**`Switch` is forbidden** (it runs `switch-to-configuration switch` and restarts
hostapd/kea/nftables/networkd live, dropping the SSH you reach the host through). Use
**BootOnce only**, which is self-healing: a bad generation reverts on the second reboot
with zero console action. The first live-router activation is psyche-gated (cloud-operator
report 388).

```
rev=<CriomOS fd780e10 rebased onto current main>
# build-only (no activation):
lojix-cli "(OsOnly goldragon prometheus <goldragon datom source> github:LiGoldragon/CriomOS/$rev Build None None)"
# BootOnce (stages NEW as a one-shot; does NOT switch live):
lojix-cli "(OsOnly goldragon prometheus <goldragon datom source> github:LiGoldragon/CriomOS/$rev BootOnce None None)"
# reboot prometheus to land NEW; vm-testing stays NOT booted (autostart=false).
# rollback: reboot again — the one-shot is consumed, returning to OLD.
```

After landing: `systemctl start microvm@vm-testing.service`, confirm the `vmt0` tap and
`05-test-vm-vmt0.network` activate, the node appears on Yggdrasil at its address, and is
reachable by `vm-testing.goldragon.criome`.

## Next

Drive the blockers to clear: repin clavifaber off `nota-derive` onto `nota-next`
(unblocks the whole cluster's deploys), rebase the CriomOS branch onto main, set the
node ygg to self-seed, fix the `/128` route, then a deep toplevel build to prove the
closure realizes for real — then the BootOnce deploy on psyche authorization. Bead
`primary-dw95` tracks it.
