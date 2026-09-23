# Flow recovery status, 2026-09-23

## Current blocker

The configured Prometheus route is still blocked, so remote Nix compilation and deployment are unproved. The latest user relay points to the durable Field checkpoint at `field/0ad137/reports/prometheus-route-20260923.md`, revision `199c9ec`: strict root SSH and hostname verification succeed over USB `10.44.0.148`; configured Yggdrasil TCP ports 22 and 80 time out; Prometheus serves `/nix-cache-info` locally; and Ouranos has IPv6 disabled on the USB profile, preventing local Ygg peer discovery. The earlier relay additionally reported USB port 80 timing out, Prometheus seeing only a different `200:17f7:…` peer through `br-lan` with no sessions, and Ouranos `201:6de1:…` disconnecting during the Wi-Fi transition. Field classifies this as an overlay peer/path fault distinct from local cache operation.

These are user-relayed Field observations, not observations independently repeated by this flow. The main flow's earlier bounded read-only probe independently observed only that the configured Prometheus IPv6 TCP ports 22 and 80 and cache-info request timed out. It did not compile remotely and did not use a local fallback.

At the durable `199c9ec` checkpoint, Terra `df09b6` owned the active machine, route, and session repair; Sol owned storage and repositories. Delivery acceptance is not repair completion, and the builder path is not fixed. Preserve the wired default route and DNS, controller lock `4639`, and all existing locks. Do not weaken authentication, change the builder URL or key, restart services, mutate routes, introduce a local build fallback, or launch competing seats.

Field High `9e735b` was the requested coordinator. The first passive route lookup found no exact HM registration or live Herdr binding for that identity, so no message was sent then and no substitute recipient was chosen. A later attempt reached the exact Field High through the existing `tools/prompt-relay` native Codex adapter: native thread `01a0cfbd-1e70-7913-886d-a919e735b32f`, Herdr `messaging-build/w12:p1`, terminal `term_65c2b874c5b4460`, accepted turn `01a0d078-52c9-78c0-882c-9581c60ae31f`. The target received the report and said it would carry the evidence limits into its aggregate. The witnessed grade is `Submitted` + `Presented` + `Read`, not `Completed`; the target also says Terra `df09b6` retains repair ownership and that neither HM registration for `9e735b` nor repair completion follows from this receipt.

The latest user source gives fresh direction, quoted here without upgrading it to an accepted transfer: “fresh Field High 9e735b is being asked to own the coordinated CriomOS/Ygg network repair with Medium 9ddcbc and Terra df09b6, based on living’s fresh direction. Preserve wired default/DNS, auth, controller/locks, and remote-only builds. Existing diagnosis: USB strict SSH works but Ygg TCP22/80 fails; inspect USB IPv6 and Ygg firewall/multicast on both nodes. Do not split controllers or claim deployment complete.” This records a requested handoff only. No acceptance receipt, controller transfer, independent repair completion, remote build, or deployment follows from it.

## Flow implementation status

- Composer revision `be898a4` is source-published. Independent review passed 4 focused and 27 package tests and byte/hash negative checks. This establishes the composer boundary only.
- Adapter revision `073c052` was the earlier staged source: its focused launch tests passed 4 cases and the wider workspace suite was reported as 36 passing. Corrected graph revision `5a9df45` is now source-published and remote-verified; 37 workspace tests and clippy passed locally, including native-root, Flow-ID, and working-directory corrections. Independent review and Start/store wiring remain underway. These receipts do not establish remote compilation, installation, or live Start acceptance.
- Paired Flow revision `96e87d` is source-published. Independent checks passed 4 CLI tests and 36 Nexus tests; the initial workspace suite reported 42 passing with clippy. Subsequent retry-profile and native-skill improvements are underway and unvalidated. This does not change the blocked remote-build, deployment, daemon-parity, or live-acceptance grades.
- Signal revision `100e7e2` publishes new Start journal types. Publication does not establish remote compilation, installation, or daemon parity.
- The existing running Flow daemon's parity with these source revisions is unknown. No new deployment, native Claude/Codex launch acceptance, or end-to-end Resolve acceptance is claimed.
- The living's rulings remain pending for Registered-seat resolution behavior and successor forwarding. Questions were submitted to Psyche High `836818`; submission is not a ruling.
- All three requested flashbook manuscripts were authored in the main native transcript and handed to Psyche Medium `e88ca4` and Psyche High `836818`. The handoffs reached only `Submitted`; no target-side acknowledgement, illustration, or rendered-book receipt is claimed.

## Sources

- Main native transcript: `/home/li/.codex/sessions/2026/09/23/rollout-2026-09-23T21-22-21-01a0cfb8-108c-76a0-901e-f4847764b62a.jsonl`.
- Lines 88-93: user-delivered Flow contract and pending living rulings.
- Lines 571 and 575-576: questions submitted for living rulings and the flashbook request.
- Lines 661, 703-719: exact Psyche routes, `Submitted` handoff status, and authored-manuscript status.
- Lines 751 and 806: independent composer and adapter review results and their acceptance limits.
- Lines 889-890: main flow's earlier bounded timeout observation.
- Lines 923-928: user instruction to retain the blocker, ownership, preservation constraints, and requested Field High coordination.
- Lines 958-972: user-relayed live diagnosis and the passive lookup result for `9e735b`.
- Lines 1000-1006: newest user relay naming the durable checkpoint, revision `199c9ec`, Terra `df09b6`, and the still-pending repair.
- Durable Field source: `field/0ad137/reports/prometheus-route-20260923.md` at revision `199c9ec`, especially lines 7-18. This is the newer source of the detailed network diagnosis; this report does not present its contents as independently re-witnessed.
- Field High target transcript: `/home/li/.codex/sessions/2026/09/23/rollout-2026-09-23T21-27-52-01a0cfbd-1e70-7913-886d-a919e735b32f.jsonl`, lines 700 and 703. Line 700 records the presented report as the target-side `UserMessage`; line 703 records Field High's read acknowledgement and continued limits. The accepted turn is `01a0d078-52c9-78c0-882c-9581c60ae31f`.
- Latest user-source ownership update, relayed by the main flow: fresh living direction asks `9e735b` to own the coordinated repair with `9ddcbc` and `df09b6`. It is authority for recording the requested handoff, not evidence that the transfer was accepted or the repair completed.
