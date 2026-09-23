# Flow recovery status, 2026-09-23

## Current blocker

The configured Prometheus route is still blocked, so remote Nix compilation and deployment are unproved. The latest user relay points to the durable Field checkpoint at `field/0ad137/reports/prometheus-route-20260923.md`, revision `199c9ec`: strict root SSH and hostname verification succeed over USB `10.44.0.148`; configured Yggdrasil TCP ports 22 and 80 time out; Prometheus serves `/nix-cache-info` locally; and Ouranos has IPv6 disabled on the USB profile, preventing local Ygg peer discovery. The earlier relay additionally reported USB port 80 timing out, Prometheus seeing only a different `200:17f7:…` peer through `br-lan` with no sessions, and Ouranos `201:6de1:…` disconnecting during the Wi-Fi transition. Field classifies this as an overlay peer/path fault distinct from local cache operation.

These are user-relayed Field observations, not observations independently repeated by this flow. The main flow's earlier bounded read-only probe independently observed only that the configured Prometheus IPv6 TCP ports 22 and 80 and cache-info request timed out. It did not compile remotely and did not use a local fallback.

Terra `df09b6` owns the active machine, route, and session repair; Sol owns storage and repositories. Delivery acceptance is not repair completion, and the builder path is not fixed. Preserve the wired default route and DNS, controller lock `4639`, and all existing locks. Do not weaken authentication, change the builder URL or key, restart services, mutate routes, introduce a local build fallback, or launch competing seats.

Field High `9e735b` was the requested coordinator. A passive route lookup found no exact HM registration or live Herdr binding for that identity, so no message was sent and no substitute recipient was chosen. The later durable checkpoint records `9e735b` as coordinating the active Terra repair; this flow has no independent delivery receipt for that coordination.

## Flow implementation status

- Composer revision `be898a4` is source-published. Independent review passed 4 focused and 27 package tests and byte/hash negative checks. This establishes the composer boundary only.
- Adapter revision `073c052` is staged. Its focused launch tests passed 4 cases; the wider workspace suite was reported as 36 passing. Durable one-shot submission, binding persistence, official transcript ownership, workspace selection, Flow-ID derivation, and integration remain under correction.
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
