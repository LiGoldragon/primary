# Manual and stateful drift audit — 2026-09-30

Prepared for Mind Sol `b666e7` and the living. This is a bounded evidence
report, not an activation, cleanup, recovery, or host-inventory command.

## Scope and authority

The living's new raw Vision says that nodes should use declarative features,
that nothing should be hand-tuned on a host, and that the living is captain of
any stateful hack. The exact words and their STT provenance are in
`flows/7328f4/vision/stateful.md`. This report does not turn that Vision into a
standing instruction to remove, restart, activate, or migrate anything.

The report combines current, bounded read-only audits relayed within this flow
with cited historical receipts and source inspection. A source `main` revision
is not evidence of a host deployment. No host mutation, cleanup, deployment,
probe, or secret read was performed for this report.

| Source checkout | Read source `main` | What it establishes |
| --- | --- | --- |
| Goldragon | `dc57e801` | cluster declaration and intended node capabilities |
| CriomOS | `6485b64e` | NixOS feature implementations |
| CriomOS-home | `0025894f` | Home Manager feature implementations |
| criome | `2f4dded8` | source only; no deployed parity claimed |
| Field | `34fe6c88` | Field source conventions only |

## Coverage

| Node | Audit coverage | Limit |
| --- | --- | --- |
| Ouranos | current bounded live audit plus source/history crosswalk | root-only state is not implied by ordinary-user evidence |
| Prometheus | current bounded live audit plus source/history crosswalk | Bird user bus unavailable/unknown |
| Zeus | current bounded live audit plus source/history crosswalk | Bird user bus unavailable/unknown |
| balboa | Unknown | no trusted current host route/inventory witness |
| mirror-alpha | Unknown | no trusted current host route/inventory witness |
| mirror-beta | Unknown | no trusted current host route/inventory witness |
| tiger | Unknown | no trusted current host route/inventory witness |
| vm-testing | Unknown | no trusted current host route/inventory witness |

An Unknown row says neither that a node is clean nor that it has drift. It has
no current source-to-runtime comparison. The three Bird user buses are
separately Unknown, rather than evidence of absent user units.

## Current host crosswalk

### Ouranos

| Finding | Witness / time | Current status | Declarative coverage and parity | Risk and rollback boundary |
| --- | --- | --- | --- | --- |
| System and Home generations differ | Current bounded audit, 2026-09-30: runtime `R=dbhsh7`; selected profile/boot `P=hm7z`; Home `xp12` | Three identities are distinct. No claim selects one as the rollback target. | Goldragon/CriomOS/CriomOS-home source can describe a desired composition, but source revisions above do not prove any of these running identities. Historical Lojix Current was already stale relative to host changes. | A rollback must prove preservation and restoration of **all** selected R, P, and Home identities, including effective units and state. No target-proven rollback exists here. |
| USB observer | Current relay: corrected observer PID `1982485`, runtime-only; its event grammar/parser limits remain under audit. Earlier defective transient was stopped after reporting carrier as unknown from the wrong `brif` carrier path. | Do not treat observer output as complete peer identity evidence. | CriomOS `modules/nixos/network/usb-downlink-observer.nix` declares a non-Router UsbDownlink observer with AF_UNIX/AF_NETLINK only, IP deny, strict filesystem, and `/run/usb-downlink-observer` as sole writable path. Deployment parity is not proved. | Starting/replacing/stopping it changes a runtime witness. Keep any runtime-only exception explicit and bounded; no durable cutover follows from source alone. |
| USB downlink base service | Source inspection of CriomOS `modules/nixos/network/usb-downlink.nix`; historical 29–30 Sep Field observations | Bridge/DHCP/DNS/NAT/firewall ownership is source-defined for a declared non-Router UsbDownlink, while live feature-to-source parity remains unproved in this audit. | Source derives `br-downlink`, Kea, resolved, NAT and bridge firewall from the capability. It removes the pre-declaration hotfix during activation. | The removal may reload NetworkManager and removes a former second owner. It requires a controlled activation and target rollback, never opportunistic cleanup. |
| Former USB hotfix | Current bounded audit reports old hotfix firewall files absent. The temporary `prometheus-share-temporary` NetworkManager profile was not verified. | Firewall hotfix absence is observed; NM-profile status is Unknown. | `usb-downlink-hotfix.nix` covers removal only when the UsbDownlink declaration activates. | Do not infer a clean network from an absent firewall drop-in. Retain the unverified profile as a separate audit item. |
| Dry activation residue | Exact prior dry activation at 2026-09-29 17:53:52; current metadata statement carried forward. | `/run/secrets` is a **symlink**, unchanged to generation 2. Empty generation 3 remains; it is mode 0751 owner `0:96`. Dry-activation lists are gone. No secret name or content was read. | No source feature makes dry activation side-effect free. The candidate also had Home-impact changes, so switching was held. | Earlier `stat -L` described the symlink's target directory, not a change to the symlink. Empty generation 3 does not prove transient decrypted material never existed. No cleanup is authorized. |
| Lojix deployment records | Current relay: deploy-46 retained `active (exited)`; deploy-50 failed metadata. | They are stateful records requiring owner interpretation; no deletion or retry occurred. | Lojix source/deploy metadata is not the same thing as current R/P/Home parity. | Preserve records until a host-specific recovery plan identifies ownership, intended state, and rollback. |
| User unit overrides | Current audit: local regular `flow-nexus` override and `codex` limits drop-in, each mode 0600; provenance/content unknown. `field-luna-heartbeat` remains masked through `/dev/null`. | These are manual-state findings, not proof the corresponding source feature is absent or wrong. | CriomOS-home has Flow, Codex and heartbeat declarations, but actual unit/link ownership and selected Home generation need readback. | Never replace a regular file or symlink simply because a declaration exists. Preserve bytes and effective unit readback before a one-composition cutover. |
| Stateful stores not read | Current audit left Lojix, repository-ledger, Kea, and Headscale data unread. | Unknown by design. | Some services are declaratively configured; their durable databases/leases/enrollment state are separate runtime facts. | No purge, migration, or inferred repair. |

### Prometheus

| Finding | Witness / time | Current status | Declarative coverage and parity | Risk and rollback boundary |
| --- | --- | --- | --- | --- |
| System and Home identities | Current bounded audit, 2026-09-30: `R=P=7f8…`; Home `n5q5…` | Runtime and selected system identity matched in this audit. This does not establish whole-host declarative parity. | Goldragon declares Prometheus as router and sole configured Nix builder; source does not prove its generated links or running units came from the listed source mains. | Preserve the witnessed R/P/Home and effective generated links before any declarative replacement. |
| Generated unit/store links | Current bounded audit reported generated links/store links. | No selected manual override was asserted by that audit. | Source has router/builder and Home feature definitions; deployment parity remains only partially observed. | “No selected override observed” is not a clean-state claim; coverage is bounded. |
| WAN lease recovery timer | Current source/live crosswalk reports source coverage. | It can reconfigure when its declared conditions occur; no such action was observed in this audit. | Goldragon router capability and CriomOS network source cover the intended feature. | Do not turn a conditional source behavior into a claimed runtime event, and do not manually tune it without a declared path. |
| Lojix/generation history | Historical 25 Sep receipt: system-55 had no Lojix generation record. | Historical drift only; not re-proven as the present source of R/P. | A source declaration cannot repair missing deployment provenance by itself. | Recovery requires current Lojix plus profile/system evidence before any activation or rollback. |

### Zeus

| Finding | Witness / time | Current status | Declarative coverage and parity | Risk and rollback boundary |
| --- | --- | --- | --- | --- |
| System and Home identities | Current bounded audit, 2026-09-30: `R=P=4yk8…`; Home `lmib8…` | Runtime and selected system matched in this audit. | Goldragon/CriomOS source describes node capabilities; wired and Wi-Fi runtime source parity is Unknown. | Preserve exact R/P/Home and effective network unit state before any convergence. |
| Generated links / manual overrides | Current audit reported generated links and no selected manual override. | Bounded observation only. | No selected override is not proof of clean state or declarative deployment parity. | Keep unknown user/root state separate; Bird user bus was unavailable. |
| Message daemon preservation refusal | Bounded journal witness through 19:12 on 2026-09-30: repeated `message-preserve-live-store: Refusing Message pre-open preservation: existing snapshot differs from live store`; MainPID 0 / activation-auto-restart in the earlier 11:25–11:26 witness. | No active-enter witness; no store deletion, rewrite, restart or recovery was performed. | CriomOS-home `message.nix` intentionally refuses pre-open preservation when a regular preserved snapshot differs from the live state database. It restarts on failure, but source does not identify why these two files differ. | A Zeus Message recovery plan must first capture ownership/provenance and compatibility of both regular files, select a rollback/restore policy, and produce target-side startup proof. Do not delete either database/snapshot to force a start. |
| Downlink reachability history | Bounded 29–30 Sep Field evidence established current wired and overlay contact after earlier physical carrier outages; the exact monitor had parser limits. | This does not prove continuous availability or a network configuration cause. | UsbDownlink is declared on Ouranos, not a proof of Zeus wired/Wi-Fi parity. | No network replug, config change, or service action follows from this audit. |

## Historical drift, separated from current witnesses

The 2026-09-25 source-versus-host inventory is historical evidence, not a
statement that every row persists. It found on Ouranos a profile-installed Flow
binary and `flow-nexus` drop-in, hand-made messenger-clj / `hm-*` links, masks,
mutable-path Field timers, recovery transients for Codex-next and Herdr, and a
system generation outside Lojix. See
`flows/da88cf/reports/inventory-system.md`, especially sections A–D and F.

The later Field-monitoring declaration in CriomOS-home deliberately makes
monitors default-off, pins script sources, and warns about hand-made unit name
collisions. It is a proposed declarative replacement surface, not proof that a
particular host enabled it. The 2026-09-21 census restoration separately
preserved source/roster before-images and gives a narrowly scoped timer rollback
procedure; it is not a whole-Home rollback.

The `switch-to-configuration dry-activate` experiment is likewise historical
and exceptional: it was explicitly authorized once, detected Home-impact and
SOPS-generation metadata residue, and did not switch the host. It must not be
repeated merely to refresh this report.

## Captain decisions needed

1. Choose which named exceptions are retained temporarily and which are replaced
   by a declared feature: Field monitors, Flow/Message migration surfaces,
   Codex/Herdr recovery units, heartbeat mask, and the USB observer.
2. Require a target-proven recovery/rollback plan per host that preserves R, P,
   Home, effective units, and owned state before any one-composition cutover.
3. Choose a Zeus Message recovery plan that preserves and attributes the live
   store and pre-open snapshot before any restart or deletion.
4. Obtain an explicit inventory for balboa, mirror-alpha, mirror-beta, tiger,
   and vm-testing; Unknown coverage cannot authorize a declaration or cleanup.

## Sources

- `flows/7328f4/vision/stateful.md` — raw living Vision and provenance.
- `flows/1bc255/log.md` — observer, supplied-closure/dry-activation, SOPS
  residue, and bounded Zeus evidence history.
- `flows/da88cf/reports/inventory-system.md` and
  `flows/da88cf/reports/prometheus-pending.md` — historical manual-state and
  generation/Lojix observations.
- `flows/6db4fe/reports/field-census-restoration.md` — historical census
  restoration and its narrow rollback boundary.
- `CriomOS/modules/nixos/network/usb-downlink.nix`,
  `CriomOS/modules/nixos/network/usb-downlink-hotfix.nix`, and
  `CriomOS/modules/nixos/network/usb-downlink-observer.nix` at source main
  `6485b64e`.
- `CriomOS-home/modules/home/profiles/min/{field-monitoring,message,flow}.nix`
  at source main `0025894f`.
- `goldragon/{README.md,UPGRADES.md}` at source main `dc57e801`.
