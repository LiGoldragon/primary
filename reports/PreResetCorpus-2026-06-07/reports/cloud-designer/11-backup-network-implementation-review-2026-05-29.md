# 11 · Backup-network implementation review — c250d9a vs intent 1141-1145 (2026-05-29)

Re-situation + design review for the cloud-designer lane (new session).
While I wrote the operator checklist (report 10, mtime 19:25 on 05-28)
the cloud-operator implemented the backup network in parallel —
CriomOS commit `c250d9a` ("add resilient backup router access",
committed 19:22). So report 10's "gaps to close" are mostly already
addressed in code. This report reconciles that and flags **one design
divergence from explicit High-magnitude intent** that needs a psyche
call before deploy.

## Status reconciliation — report 10's checklist is largely DONE

| Report 10 item | State now | Evidence |
|---|---|---|
| Gemma/auth secret (`localLlmApiToken`) minted + sops + wired | DONE | goldragon `c8b5840` `local-llm-api-token.sops`; lojix-cli `4c66b8a` `artifact.rs:26` (on **main** now, not a branch — report 9 §lojix is stale) |
| Backup secret (`routerBackupWifiPassword`) minted + sops + wired | DONE | goldragon `0298d21` `router-backup-wifi-password.sops`; lojix-cli `artifact.rs:25` |
| Don't rebuild — extend existing `backupWireless` leg | DONE | `c250d9a` added `hostapd-backup-wireless.service`, a separate hostapd on `wlp199s0f0u4` |
| Backup AP independent **radio** (separate hostapd) | DONE | `default.nix:256-334` — own service, own runtime dir, own sops `restartUnits` |
| Don't bounce live router services on switch | DONE (and smart) | `default.nix:236-254` `restartIfChanged/stopIfChanged = false` on networkd/hostapd/dnsmasq/kea |
| Backup AP off `br-lan` / `kea` / `dnsmasq` (own subnet+DHCP+DNS) | **NOT DONE** | `default.nix:281` `bridge=${lanBridgeInterface}`; USB-eth `default.nix:363-373` `Bridge=br-lan` |
| USB-eth master interface on router node | PARTIAL | un-gated as `30-usb-eth`, but **bridged into br-lan**, not an independent master |
| Live BootOnce deploy + verify gen 44 (Thread 1) | **NOT DONE** | operator pivoted to Pi-harness investigation (cloud-operator report 13); no deploy-verify report |
| Real console / out-of-band access (`primary-lome`) | OPEN | no evidence landed |

The two `restartIfChanged = false` / `stopIfChanged = false` additions
are a genuinely good move I did not propose: they make even a live
`Switch` stop bouncing `hostapd`/`networkd`/`kea`/`dnsmasq`, killing the
exact mechanism of the incident (records 1105/1117) at the source. Credit
to the operator. It complements — does not replace — the BootOnce rule
(a reboot still applies the new units fresh).

## The finding — the backup is NOT independent of kea/dnsmasq

Record 1145 (High): the backup "runs at the system level on plain
systemd-networkd with **simple DHCP and forwarded DNS, deliberately
independent of the main kea, dnsmasq, and hostapd stack**, so a
switchover or upgrade of the main router services cannot take it down."
Record 1141 (VeryHigh) and 1142 (VeryHigh) say the same in principle.

What `c250d9a` actually built, against that text:

| Record 1145 clause | Implementation | Met? |
|---|---|---|
| plain systemd-networkd | backup AP + USB-eth are networkd networks | partial — but they join `br-lan`, not a separate path |
| simple DHCP | clients get leases from **kea** (`kea.interfaces=[br-lan]`, `default.nix:201`) | **no** |
| forwarded DNS | clients resolve via **dnsmasq** (listens on the br-lan gateway, `dnsmasq.nix`) | **no** |
| independent of kea/dnsmasq/hostapd | independent of **hostapd** only (separate service) | **partial** |
| switchover/upgrade can't take it down | a `Switch` can't (no-bounce); an **upgrade/reboot into a broken gen** still drops br-lan→kea→dnsmasq, and the backup with them | **no, for the upgrade case** |

Mechanism: `hostapd-backup-wireless` puts `bridge=br-lan` in its hostapd
conf (`default.nix:281`), and `30-usb-eth` sets `Bridge=br-lan`
(`default.nix:369`). So a client on `CRIOM Backup` (or a USB-eth port) is
L2-bridged onto `br-lan` — its IP comes from kea, its DNS from dnsmasq,
its gateway is the br-lan address. The backup shares the main stack's L3
fate.

### Why it matters — this is exactly record 1144's scenario

Record 1144 (High) asks for a backup that "survives an OS upgrade and a
switchover of the main router services… defence in depth beyond the
boot-mode deploy rule." The bridged design survives a *transient* main
restart (kea leases persist; the br-lan static address is networkd-held)
— but it does **not** survive the case 1144 is actually about: rebooting
into a new generation whose `kea`/`dnsmasq`/`br-lan` config is broken.
Then the backup AP gives you L2 association and nothing else — no IP, no
DNS, no route. That is the lockout 1144 wants to make impossible.

The acid test from report 10 still applies and the current build would
**fail** it: bring the backup AP up, stop `kea` + `dnsmasq`, and a new
backup client can no longer get an address or resolve names.

## Two paths — needs a psyche call

**Path A — honour 1145: make the backup a real independent dumb stack.**
The design (cloud-designer to detail, cloud-operator to implement):

- Backup AP `wlp199s0f0u4`: drop `bridge=br-lan` from the hostapd conf;
  give the interface its own networkd network — static `Address`
  (e.g. `10.99.0.1/24`), `DHCPServer = true`, `IPMasquerade = "ipv4"`,
  `dhcpServerConfig` handing out an upstream resolver directly
  (`DNS = 1.1.1.1`, `EmitDNS = true`) so there is **no dnsmasq/kea in the
  path**.
- USB-eth master: the same shape on its own subnet (revive the gated
  `20-usb-eth` `10.47.0.1/24` master rather than bridging via `30-usb-eth`),
  wired (no radio) — the sturdiest leg of all.
- nftables: add a `forward` rule allowing the backup subnet(s) ↔ WAN
  (`oifname wan masquerade` in the `nat` chain already covers egress; the
  `forward` chain currently only allows `br-lan ↔ wan`). The backup
  interface is already in `localInputInterfaces` (`default.nix:76`), so
  input to the router over the backup is already permitted.
- Result: a `kea`/`dnsmasq`/`br-lan` failure in any new generation leaves
  `CRIOM Backup` + the USB-eth master fully serving and routable. Passes
  the acid test. This is what 1144/1145 ask for.

**Path B — accept `c250d9a` as the end state (no-bounce + bridged).**
Simpler; directly kills the incident mechanism via `restartIfChanged =
false`. But it does not satisfy 1145's "independent of kea/dnsmasq" or
1144's survive-a-bad-upgrade, so it would need the psyche to **relax
1145** to "independent radio + no-bounce is sufficient."

**Recommendation:** Path A. 1145 is explicit, High-magnitude, and the
independence is the whole point of the defence-in-depth in 1144 — the
no-bounce safety helps the *deploy* but not a *bad new generation*. The
extra cost over B is one networkd network per backup leg plus one
nftables forward rule; small for the guarantee. But because the operator
clearly chose the bridged reading deliberately (the `ARCHITECTURE.md`
note frames "independent hostapd service" + "avoid automatic
restart-on-switch" as the design), the psyche should adjudicate rather
than me silently re-opening landed work.

## What I'd do next (pending the psyche's path call)

- If Path A: detail the independent-stack module shape as a small diff
  spec for cloud-operator (own subnets, networkd DHCP, masquerade
  forward rule, drop the two `bridge=br-lan`s), then hand off.
- Either path: Thread 1 (the gen-44 BootOnce deploy + verify) is still
  unfinished and is the actual prerequisite the psyche set first
  (report 10). The full stack is now wired and committed, so this is a
  deploy-and-verify step for cloud-operator, not a build step.

## Anchors

- Implementation: CriomOS `c250d9a`; `modules/nixos/router/default.nix`
  (`hostapd-backup-wireless` 256-334, `restartIfChanged` 236-254,
  `30-usb-eth` 363-373, bridge at 281); `ARCHITECTURE.md` backup note.
- Datom leg: `goldragon/datom.nota:94`
  (`wlp199s0f0u4 [CRIOM Backup] TwoG 11 Wifi4 (routerBackupWifiPassword)`).
- DHCP/DNS owners: `default.nix:193-228` (kea on br-lan),
  `modules/nixos/network/dnsmasq.nix` (dnsmasq on the br-lan gateway).
- Secrets: goldragon `c8b5840`, `0298d21`; lojix-cli `4c66b8a`
  `src/artifact.rs:25-26`.
- Prior context: reports 8 (incident), 9 (handoff), 10 (checklist).
- Intent: records 1105/1117 (deploy safety), 1141/1142 (sturdy +
  basic-access principles), 1143 (human-readable secret), 1144
  (independence as a hard requirement), 1145 (the dumb-stack design).
