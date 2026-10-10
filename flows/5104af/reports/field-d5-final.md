The remaining migration is proceeding through this seat’s replacement. Prometheus has upstream internet, but the phone’s failing path is not yet identified; no speculative network change has been made.

This is **Field Astra `d5b96b`’s complete final handoff**. Mind Sol `5104af` must use it in the successor’s first prompt.

The living’s controlling request is:

> Get everybody migrated on the new Codex harness and debug and fix the fact that Prometheus's Wi-Fi access point is not giving me internet access.

Both tasks remain active. Remote access to the candidate was explicitly confirmed by the living. Historical rotation holds are superseded. Do not interrupt working seats, infer an ambiguous “V2” rename, or treat a launch receipt as successful migration.

**Ownership and exact final boundary**

Mind Sol **`5104af` explicitly accepted sole migration execution** after preparation finished and this turn ends. `rotation_finish` has finished and relinquished execution. All this main flow’s subflows are now finished. No replacement for `d5b96b` has been launched.

**This response is the natural-final boundary.** After it ends, verify the predecessor’s actual ended/idle state, freeze and hash this complete handoff plus required startup context, then launch one fresh independent **Field Astra, `gpt-6-astra`, medium**.

Predecessor:

- Native UUID `01a0ee2e-a52e-7c92-98c7-9a5d5b96b3f3`.
- Pane `w1:pQ`, last client PID `643951`.
- Transcript `/home/li/.codex-next/sessions/2026/09/29/rollout-2026-09-29T11-20-29-01a0ee2e-a52e-7c92-98c7-9a5d5b96b3f3.jsonl`.

The successor’s real task is to reconcile this handoff, assume Field coordination, complete everybody’s migration, and carry the AP diagnosis through repair and verification. Require its actual answer and acceptance, native model/effort, candidate connection, initialized lane/log/index, and typed Messenger registration before closing or retiring this predecessor. Retain native transcripts and flow records.

**Prepared launch artifact**

Immutable commit:

`3f9faddff14a68a5146a53b735efd8a9a5445ad4`

Remote bookmark: `field-d5-successor-adapter-prepared`

Artifact:

`flows/d5b96b/reports/field-d5-successor-launch.py`

SHA256:

`be3bc75baa3bde7f0994a7357381b498912e3ab91aa3d28ccb36b6a28e492c2e`

Verify with:

`python3 flows/d5b96b/reports/field-d5-successor-launch.py --handoff COMPLETE_FILE --sha256 EXACT_SHA --verify`

Launch with the same arguments minus `--verify`, through the supported controller interface in an allocated successor pane.

The adapter supplies the complete prompt directly through `execv`; it does not ask the model to read a handoff file. It selects `gpt-6-astra`, medium, `-s danger-full-access -a never`, cwd `/home/li/primary`, and explicitly targets:

`unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock`

No separate `field-d5-successor-reparse.md` was created. Do not claim otherwise. Mind Sol owns the final extraction and complete first-prompt assembly.

**Current Codex state and remaining migration**

The last census found exactly two old-Next clients: this Field Astra and **Field Sol `1bc255`**. Field Sol is actively handling the AP outage and migrates after that work naturally ends. The living’s “everybody” instruction supersedes its earlier passive-only checkpoint restriction.

Already on the candidate:

- Field pilot `f69847`, actual GPT-6.1 Sol.
- Mind Luna `098f27`, GPT-6 Luna.
- Mind Astra `d32329`, GPT-6 Astra; last reported blocked on a tool approval.
- Mind Sol `5104af`, GPT-6.1 Sol, native `01a0f51b-c14f-7300-9778-3365104afba2`, pane `w1:p15`, registered `mind_sol`.

Mind Sol’s predecessor `b666e7` was closed and retired only after a fresh `done` witness. Its transcript remains. Acceptance commit `809e84762021`; retirement evidence `c8f5913501cd`; retirement receipt `a4a62ba9358a`.

Preserved servers:

- Legacy stable PID `1936`, state `.codex`, version 0.153.4.
- Former Next PID `1960`, state `.codex-next`, version 0.158alpha9.
- Candidate PID `1965146`, state `.codex-next-8mkkxq293hk2`, version 0.161alpha2.

The old standalone client PID `1824790` has exited. Both Flow services still depend on legacy stable, however. **Do not retire servers until every actual client and dependency has been reconciled.** Logical `codex` still selects former Next; `codex-next` selects the candidate. Finish role promotion without changing occupied endpoint identities or restarting working sessions.

Claude seats are not Codex migration targets. “Mine” with “V2” remains unresolved; the inspected Mind Sol and Psyche Opus terminal titles contained no V2. No historical or Psyche rename was made.

Candidate tools have executed successfully under the documented full-access session configuration. This does **not** establish that the separate Bubblewrap packaging/exposure defect was repaired.

**Prometheus AP: sole executor and latest evidence**

**Field Sol `1bc255` explicitly accepted sole Prometheus AP host diagnosis/fix execution.** No other delegate made target probes. Mind Sol reported no conflicting AP work in its lane; that was not a global ownership audit.

Field Sol’s latest report, at **23:43–23:44**, found:

- AP associations and recent DHCP allocations.
- A wired default route and host HTTPS response 200.
- IPv4 forwarding.
- nftables LAN-to-WAN forwarding and masquerading.
- Healthy AP, DHCP and DNS services.

It reported **no identified fault boundary or justified fix**, and no host mutation. These findings do not prove the phone has internet.

The living was asked to turn mobile data off, connect to Prometheus’s Wi-Fi, and open a webpage. **The phone-test response is pending.** Relay that result to Field Sol and let the sole executor distinguish the failing client path, make the warranted reversible repair, and verify it. Do not independently duplicate its probes or claim the outage fixed.

**Complete local AP source-pointer handoff**

The following source handoff to Field Sol was held by Messenger:

`Held.{ 1bc255 Blocked attempt-c1929e0e-967 }`

Do not claim delivery. Preserve and deliver these exact substantive pointers through the supported route when available:

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix`: hostapd bridges the AP into `br-lan`; Kea serves `.100–.240` and advertises the LAN gateway as router and DNS; nftables enables IPv4 forwarding, permits `br-lan` to `routerInterfaces.wan`, and masquerades egress.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/network/dnsmasq.nix`: DNS binds to the LAN gateway and uses configured external upstream resolvers.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`: SSH match configuration for `prometheus.goldragon.criome`. Historical `root@prometheus.goldragon.criome` access requires current owner verification.
- Relevant written psyche: `flows/753e69/vision/prometheusWifiReliability.md`, `flows/7328f4/vision/network.md`, and `flows/d5b96b/vision/prometheus-wifi.md`. They describe recurring phone association without internet and the expectation that Prometheus shares its upstream.
- Historical addresses `10.18.0.1`, upstream `192.168.1.11` via `192.168.1.1`, are **not current evidence**.
- Diagnostic distinctions: phone association/address/gateway/DNS; bridge and WAN state/routes; DHCP options; forwarding/NAT counters; upstream direct-IP connectivity; DNS resolution. These are distinctions to investigate, not diagnosed causes.

Prefer the managed source for a durable repair, preserve recovery and current connectivity, and document any justified immediate reversible correction. No generic approval gate is required for the requested diagnosis/fix.

**Preserve other Field obligations**

Field Sol owns the worktree/lost-commit audit. Reports `b4d2a947` and `deb64f486917` were delivered; no cleanup occurred. Preserve `/home/li/wt/primary/e167d8-cleanup` and unresolved Git-unreachable candidates.

Zeus previously had authenticated wired and overlay contact; the physical cause of its carrier outages remains unknown. The corrected USB observer was last witnessed active, runtime-only, bounded to one natural plug record or reboot. Do not induce a plug or silently turn it into a durable deployment. Ouranos whole-system deployment remains held pending intentional changes and proven recovery.

The final main log is published at **`bca77af16`**, bookmark **`record-delivery-final-field-prep`**. No source build or host action is running from this main flow. Field Sol’s AP work continues independently.

**Next executor action:** after this final ends, Mind Sol `5104af` establishes the fresh Field Astra successor with this complete prompt, verifies acceptance, then retires old `d5b96b`. The new Field carries both living requests through completion.