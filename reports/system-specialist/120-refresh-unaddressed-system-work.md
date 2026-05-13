# System Work Refresh: Important Unaddressed Items

Role: system-specialist
Date: 2026-05-14

## Purpose

This is a refreshed handoff after re-reading the system-specialist
discipline, the repo skills for CriomOS and CriomOS-home, the current
role beads, and the recent system reports. It brings forward the work
that still matters rather than relying on older chat memory.

## Current Coordination State

`system-specialist` and `system-assistant` are idle. The only active
lock I saw is `designer` on
`reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`.

The primary workspace has dirty files that are not system-specialist
work:

- `primary.code-workspace`
- `reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`
- `reports/operator-assistant/111-persona-introspect-contract-dependency-gap.md`

Do not make broad commits from `/home/li/primary` until those are
understood or split. System repos checked clean: `CriomOS`,
`CriomOS-home`, `horizon-rs`, `CriomOS-test-cluster`, `clavifaber`,
`chroma`, `whisrs`, `lojix-cli`, `goldragon`, and `CriomOS-lib`.

## Corrections To Older Reports

Some older report items are now stale:

- Node-name service gates are gone from active CriomOS modules. The
  bad `node.name == "ouranos"` / `node.name == "prometheus"` shape is
  not currently present in `CriomOS/modules` or `CriomOS-home/modules`.
- Tailnet controller port and base domain have moved into Horizon data:
  `CriomOS/modules/nixos/network/headscale.nix` now reads
  `tailnetControllerRole.Server.port` and `.baseDomain`.
- `dnsmasq.nix` now reads Headscale's configured base domain rather
  than reconstructing `tailnet.${cluster}.criome` locally.

These are good examples of the intended pattern: Horizon owns semantic
cluster facts; CriomOS renders them.

## Top Unaddressed Work

### 1. Wi-Fi Policy, Secrets, And EAP-TLS Migration

This is still the biggest architectural violation.

Live leaks and scaffolds:

- `CriomOS/modules/nixos/router/default.nix` still contains the
  production SSID, regulatory country, WPA3-SAE mode, and literal SAE
  password for the transitional network.
- `CriomOS/modules/nixos/network/wifi-eap.nix` still hardcodes SSID
  `criome`, keys identity to `node.name`, lacks the EAP-TLS safety
  fields, and points at stale complex key material.
- `CriomOS/modules/nixos/router/wifi-pki.nix` prepares a directory and
  prints manual hints; it does not configure hostapd for EAP-TLS.

Current decision: keep the password Wi-Fi temporarily. The migration is
dual radio: old WPA3-SAE network on the existing radio, new EAP-TLS
network on the USB Wi-Fi dongle, migrate clients, then delete the old
network. The old password should not be "cleaned up" by moving the
secret value into Horizon. If represented during transition, it should
be a `SecretReference`.

Tracked beads:

- `primary-a61` — move router Wi-Fi policy and SAE secret out of Nix
  modules.
- `primary-nvs8` — feed ClaviFaber Wi-Fi EAP certificates into
  CriomOS-test-cluster fixtures.

### 2. Horizon Schema Re-Engineering Is The Main Unlock

Reports `reports/system-specialist/119-horizon-data-needed-to-purge-criomos-literals.md`
and `reports/system-assistant/12-horizon-re-engineering-combined-audit.md`
converge on the same core work: Horizon needs typed data for the
cluster policy CriomOS is still forced to invent locally.

Important additions still needed:

- cluster identity/domains;
- Wi-Fi networks and authentication policy;
- LAN and DHCP policy;
- resolver policy;
- AI provider records;
- VPN profiles;
- secret references for user tools and system services;
- typed `NodeCapabilities` payloads for binary cache and build host
  instead of booleans whose true branch hides endpoint/key/retention
  data.

The current schema still has some too-small fields, such as
`NodeProposal.wifi_cert: bool`, `Node.is_nix_cache`, and
`Node.is_remote_nix_builder`. The useful rule is not "delete every
derived predicate"; it is "a boolean is wrong when the true case carries
data."

### 3. CriomOS-Test-Cluster Needs Booted Service Witnesses

`CriomOS-test-cluster` is the right testing direction, but it is still
mostly evaluation/build evidence. It proves projection and module
rendering, not service runtime behavior.

Missing witnesses:

- booted router DNS test for dnsmasq, cluster records, upstream
  forwarding, and recovery;
- VM or nspawn smoke for Tailnet/Headscale service wiring;
- Wi-Fi EAP-TLS parsing/connectivity evidence, likely with
  `mac80211_hwsim` or a more realistic VM/lab setup;
- cluster trust end-to-end path: host A publishes key material, the
  registry ingests it, host B receives the update.

Tracked beads:

- `primary-58l` — VM or nspawn service smoke for DNS and tailnet roles.
- `primary-1ha` — negative Horizon fixtures for role invariants.
- `primary-7ay8` — keep Prometheus sandbox artifacts and metadata.

### 4. ClaviFaber Cluster Trust Runtime Is Still Missing

ClaviFaber has useful per-host primitives and actor separation, but the
cluster side is still not implemented as a live push path.

The missing component shape is:

- `ClusterRegistryActor` commits public material to the cluster
  registry;
- `TrustDistributionActor` pushes current state on subscription and
  deltas after commits;
- no polling;
- slow subscribers cannot block unrelated subscribers;
- tests prove the actor path and pushed delivery.

Tracked beads:

- `primary-e3c` — cluster registry and trust distribution actors with
  push primitive.
- `primary-mm0` — ClaviFaber end-to-end test sandbox and Prometheus
  integration runner.
- `primary-8b3` — ClaviFaber owns the per-host Yggdrasil keypair;
  CriomOS consumes that keypair instead of seeding its own.

### 5. Resolver/Tailnet Direction Needs A Final Decision

The DNS split is now healthier: edge nodes use `systemd-resolved`,
router nodes use dnsmasq, and Unbound is no longer the default edge
resolver. The open question is broader network strategy:

- whether Headscale is worth keeping;
- whether Yggdrasil should become bootstrap-only and power down once a
  better overlay is connected;
- whether the policy eventually belongs in a state daemon.

Tracked bead:

- `primary-tpd` — review Headscale and Yggdrasil roles in CriomOS.

### 6. Firmware Policy Blocks Better Synthetic Bare-Metal Tests

`CriomOS/modules/nixos/metal/default.nix` still has
`hardware.enableAllFirmware = true` under bare-metal imports. That made
synthetic bare-metal test builds drag in unrelated unfree firmware, so
the test-cluster built a Pod node instead.

This should become a Horizon hardware capability or deployment policy.

Tracked bead:

- `primary-un7p` — gate all-firmware policy by deployment or hardware
  capability.

### 7. WireGuard Is Probably Stale And Has A Known Bug

`CriomOS/modules/nixos/network/wireguard.nix` still appears unused, and
it has a concrete bug:

```nix
mkUntrustedProxy = untrustedProxy: {
  inherit (wireguardUntrustedProxies) publicKey endpoint;
  allowedIPs = [ "0.0.0.0/0" ];
};
```

It inherits `publicKey` and `endpoint` from the whole list instead of
from `untrustedProxy`. Before testing or expanding this module, decide
whether WireGuard is still part of the system.

Tracked bead:

- `primary-cua` — audit whether WireGuard module is still used.

### 8. Deployment/JJ Hygiene Still Needs A Tool Guard

The bookmark divergence incident is not only a documentation problem.
The workspace needs a helper that makes the wrong state visible.

Tracked bead:

- `primary-eedk` — add `tools/orchestrate verify-jj`.

Minimum useful behavior: count `push-*` bookmarks per repo, flag merged
ones for deletion, flag stale diverging ones, and refuse role release
when local-only push bookmarks would strand work.

### 9. Chroma Looks Structurally Better, But Runtime Observation Remains

Chroma's current architecture and hard constraints now name the
resume/suspend and warmth-ramp behavior explicitly:

- post-resume schedule reconciliation runs before geolocation refresh;
- location refresh is separate and delayed;
- missing location does not cause civil-trigger defaults to apply;
- ramps project current wall-clock progress instead of replaying from
  the beginning.

The `chroma` repo is clean and has no open role bead right now. The
remaining risk is operational: if the screen wakes warm during daytime
again, the next action should be runtime observation of Chroma state,
GeoClue state, and wl-gammarelay state, not another architectural guess.

## Recommended Next Queue

1. Take `primary-a61` only if ready to do Horizon + CriomOS changes
   together; otherwise leave the old Wi-Fi network alone and start with
   schema/test prep for the second EAP-TLS network.
2. Take `primary-un7p` as a contained high-signal fix: it unblocks
   better bare-metal fixture tests and has a clear acceptance shape.
3. Take `primary-58l` to move from evaluation-only confidence to booted
   service confidence for DNS/tailnet.
4. Take `primary-eedk` to prevent another bookmark cleanup incident.
5. Take `primary-tpd` if the goal is design clarity before touching
   Tailnet/Yggdrasil runtime behavior.

Before any edit: claim exact paths with `tools/orchestrate`, re-run
`jj st` in the repo, and avoid committing the dirty primary workspace
files listed above.
