# Field Sol Codex 6.1 successor handoff — 2026-10-01

## Scope and authority

This is a durable handoff record for the successor who may eventually take the
unfinished Field Sol work. It records bounded receipts; it does not start a
Codex seat, repair a Messenger route, probe a host, change a service, apply an
AP fix, or retire the present seat.

The direct working request was to migrate Codex seats and diagnose and fix
Prometheus Wi-Fi Internet access. Field Sol `1bc255` accepted sole AP host
diagnosis and repair ownership. Its migration remains separate from that work.
See `flows/1bc255/log.md` lines 65–77 and `flows/e2a70a/log.md` lines 7,
78–80.

## Present Field Sol identity and route boundary

A bounded `hm-list` plus `hm-heartbeat-state` receipt in
`flows/e2a70a/log.md:60` records:

| Field | Receipt |
| --- | --- |
| Flow and typed route | `1bc255`, `field_sol_1bc255`, session `default`; **Bound** |
| Native | `01a0ee71-5824-7c40-b65c-7841bc2558eb` |
| Pane | `w1:pX` |
| Terminal | `term_65ca36abc213c1f` |
| Readiness | **Held/Blocked**, explicitly not `RepairRequired`; no identity mismatch and no retry |

That is the last cited route/identity witness. It is not a present connection,
terminal-state, or idle proof. The earlier launch receipt records gpt-6-sol,
medium and `working` registration at launch
(`flows/caf622/log.md:503`); it is historical.

The existing record says Field Sol supplied an “exact current Next binding” and
that the Next state was `/home/li/.codex-next`
(`flows/d5b96b/log.md:80`). That record does **not** give a 1bc255-specific
socket pathname. The common old-Next-looking endpoint
`unix:///home/li/.codex-next/app-server-control/app-server-control.sock`
is recorded for other Field material, but was not tied to this native UUID in
the bounded receipts used here. It must not be treated as a live or exact
1bc255 connection. No current old-seat remote connection was checked.

## Candidate facts and the successor gate

Field coordinator `e2a70a` supplied the candidate endpoint
`unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock`
and candidate home `/home/li/.codex-next-8mkkxq293hk2`. Its own candidate
receipt is gpt-6-astra, medium, `approval=never`,
`sandbox=danger-full-access`, with candidate server PID `1965146`
(`flows/e2a70a/log.md:48`, `flows/e2a70a/index.md:6-8`). This is
coordinator/candidate evidence; it is not a Field Sol successor identity.
No successor UUID, flow, pane, terminal, or typed route for the replacement is
currently recorded.

Before the present native seat can be ended, a new independent successor must:

1. receive the complete handoff and later supplements, and explicitly accept
   sole AP ownership and the unfinished work;
2. prove its actual model, effort, access, candidate connection, and a
   meaningful task command;
3. establish its `flow-id` lane, log, local and shared index;
4. establish exact Herdr pane/native binding and a typed Messenger
   registration;
5. return a substantive acceptance that retains the boundaries below.

Only after those facts can Mind Sol `5104af` witness this native seat's
natural completion/idle state and close or archive **this exact native
instance**. Do not close a pane or alter a server before that order. This gate
is recorded in `flows/1bc255/log.md` pending entries and
`flows/e2a70a/log.md:15-17, 60-62, 78-80`.

## Prometheus Wi-Fi AP: current bounded record

Field Sol remains the sole AP host diagnosis/fix executor. The latest report is
`flows/1bc255/reports/prometheus-ap-2026-09-30.md`, published at
`adcf542381e0`; observations are local UTC−06:00 on 2026-09-30.

| Time | Observed | Limit |
| --- | --- | --- |
| 23:42:20, :31 | Two stations associated and completed WPA handshakes; Kea allocated a `10.18.0.x` lease at 23:42:32. | Identities withheld. |
| 23:43:14 | AP and `br-lan` UP/LOWER_UP; hostapd/dnsmasq/Kea active; wired default route present; host HTTPS returned 200. | Host reachability is not phone-path proof. |
| 23:44:29 | IPv4 forwarding; explicit `br-lan → eno1` and return firewall rules; NAT masquerade; AP/bridge/USB members forwarding. | No counter-based client traversal proof. |
| 23:46–23:49:40 | Eight dnsmasq upstream resolvers; bridge bytes rose; conntrack showed 130 AP-LAN-to-public entries, 67 ESTABLISHED, 127 ASSURED, one UNREPLIED. | `br-lan` also carries USB, so these flows cannot identify Wi-Fi or the living’s phone. |
| 23:51:52–:53 | One station inactivity-disassociated/deauthenticated. | Other station's departure cause is unknown. |
| 23:53–23:54 | Zero current Wi-Fi stations; hostapd remained active; no AP restart, driver/firmware event, or pstore evidence in 23:40–23:55. | No natural phone Internet/DNS witness and no fault boundary. |

No AP configuration, DHCP/DNS/firewall/routing change, client probe, or repair
was made. The requested next discriminating input remains a natural phone test:
mobile data off, connected to Prometheus Wi-Fi, open a webpage, then report the
actual result. The useful identifiers are the randomized Wi-Fi MAC or displayed
lease, local time, and failure stage (visibility, WPA, DHCP, DNS, or Internet);
correlate the result with bounded hostapd, Kea, dnsmasq, and firewall/NAT reads
(`reports/prometheus-ap-2026-09-30.md:132-146`). Do not turn host upstream success or aggregate conntrack into a
claim that Wi-Fi Internet is fixed.

### AP source and held source-pointer delivery

The source pointers to preserve are:

- Goldragon `/git/github.com/LiGoldragon/goldragon/proposal.datom` for Prometheus router/WAN/WLAN declarations;
- CriomOS `modules/nixos/router/default.nix` for hostapd/`br-lan`, Kea,
  forwarding, nftables and masquerade;
- CriomOS `modules/nixos/network/dnsmasq.nix`;
- CriomOS-home `modules/home/profiles/min/default.nix` SSH Match;
- psyche records `flows/753e69/vision/prometheusWifiReliability.md`,
  `flows/7328f4/vision/network.md`, and
  `flows/d5b96b/vision/prometheus-wifi.md`.

They are preserved source/context pointers, not a live deployment proof.
Historical addresses are not current host evidence. The required diagnostic
distinctions are association/address/gateway/DNS; bridge/WAN/routing; DHCP
options; forwarding/NAT; direct-IP upstream; and DNS resolution.

The predecessor attempted to deliver the complete pointer body to recipient
`1bc255` and received
`Held.{ 1bc255 Blocked attempt-c1929e0e-967 }`
(`flows/d5b96b/log.md:203`, `flows/e2a70a/log.md:15`). The candidate
coordinator attempted the full body once through
`FLOW_ID=e2a70a hm-send 1bc255 --stdin`, with
`Held.{ 1bc255 Blocked attempt-2655b5d1-6b3 }`
(`flows/e2a70a/log.md:54`). Neither body was typed. This is an undelivered
source-message obligation, not permission for a blind retry, forced readiness,
duplicate host diagnosis, or route repair. The reported predecessor extraction
was 8,856 UTF-8 bytes with SHA-256
`2958deca2f92909f7f7312f1a8692efa25c47df300050ad2ccc111d1e302a288`;
the coordinator explicitly did not independently rehash it
(`flows/e2a70a/log.md:21`).

## Ouranos and Zeus boundaries

The corrected transient USB observer started once at 2026-09-30 10:02:27 as
PID `1982485`, after a 10:02:22 preflight; its initial event/passive pair was
at 10:02:39 (`flows/1bc255/log.md:39-40`). The last direct observer watch was
10:07:26–10:08:26, with sequence 63 at 10:08:35: carrier remained up and no
natural plug or carrier transition occurred (`flows/1bc255/log.md:41`). Its
output was not complete peer identity evidence. The observer was runtime-only,
bounded to the next natural Zeus plug or reboot; do not induce a plug or make
it durable. Its actual state after that bounded witness is unknown.

Ouranos full-system deployment remains held. A September 30 19:11:39 local
receipt had distinct runtime `R=dbhsh7…`, selected profile/boot
`P=hm7z…`, and Home `xp12f872…`; no target-proven rollback preserves all
three identities. The historical dry activation at 2026-09-29 17:53:52 created
residue: `/run/secrets` is a symlink to generation 2; metadata later found an
empty generation 3. No secret content was read, and emptiness does not prove
that transient material never existed. No cleanup, retry, or deployment follows
from this record. See manual-state audit lines 50–57.

Zeus contact was later established by bounded authenticated wired and overlay
checks on 2026-09-30 10:09–10:10, while cross-host journals show a separate
approximately four-hour wired outage on 2026-09-29 17:01–21:07
(`flows/1bc255/log.md:44-45`). This proves neither a cause nor continuous
availability outside the bounded windows. No Zeus network change is pending
from this handoff.

## Preservation, reports, and recovery surface

- Preserve `/home/li/wt/primary/e167d8-cleanup`; no cleanup authority is
  granted here.
- The manual/state audit is
  `flows/1bc255/reports/manual-state-audit-2026-09-30.md`, published as
  `b4d2a947`. It keeps five nodes and Bird user buses explicitly Unknown and
  does not infer clean state from absent overrides.
- The worktree audit is
  `flows/1bc255/reports/worktree-commit-audit-2026-09-30.md`, published as
  `deb64f486917`. It records Git-unreachable candidates without calling any
  lost or disposable, and prohibits cleanup, ref movement, GC, expiry, or
  workspace forgetting.
- That audit also records observation side effects: Jujutsu commands in shared
  Primary created operations `09532cebfb00`, `385351956eb3`, and
  `0d7fdf293405`, and surfaced
  `record-delivery-mind-sol-reparse-corrected@origin` at `897f2470`.
  Working-copy effect for the initial operations is unknown. Do not run
  Jujutsu in shared `/home/li/primary` merely to inspect it.

## No in-flight action and unknowns

This handoff records no host command, AP probe, repair, seat command,
Messenger send, archive, or service action in flight by Field Sol. The
unresolved items are the phone result, the Held source-pointer delivery,
the AP fault boundary and a justified reversible remedy, current old-seat
readiness/remote connection, successor identity/acceptance, observer state
after its last bounded witness, and a whole-system deployment/rollback plan.

