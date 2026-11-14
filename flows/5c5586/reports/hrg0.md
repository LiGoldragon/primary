# hrg0 and the Psyche book Haiku refresh: evidence

Read-only investigation of the Flow Nexus 0.56.2 daemon (pid 654687, unit `flow-nexus-0550`). Source: `/nix/store/ig9191apcbidhwjyhvimczhxyccr5i3h-flow-nexus-0.56.2` (origin/main eabddc8d, per flows/98df55/reports/open-refresh-inventory.md). Nothing was sent, cancelled, configured or restarted. No copy of the store was taken. The store was read through two read-only meta queries, `DebugDelivery.<id>` and `Inspect.{ Psyche book Haiku }`, at 2026-11-14T17:08:55-06:00. Both are plain store reads: `lib.rs` `debug_delivery` calls `store.debug_delivery`, and `repairing.rs:40` `inspect` calls `store.inspection`. `flow-nexus 'Queues'` was read at the same time.

Times are CST. The transcripts record UTC, which is CST + 6 h.

## Timeline

| CST | Event | Record |
|---|---|---|
| 15:47:29 | Flow b62c49 wakes as { Psyche book Haiku } (predecessor 3f169a) | journal |
| 16:59:13 | Fable sends bn3d, Soft.Order for the route and complex-fold pages. Answered `Sent.bn3d` | Fable transcript 0eb295f3…jsonl |
| 16:59:18-22 | Fable sends n6q7, `MiddleAbrupt.Notice «Hold bn3d: its two sources are not ready…»`. Answered `Sent.n6q7`. It reaches b62c49 mid-turn (queue-operation enqueue 22:59:19Z, then remove `absorbed_mid_turn`). b62c49 answers "Holding bn3d" and ends its turn at 16:59:25 | b62c4933…jsonl; DebugDelivery.n6q7 = `Delivered.{ Claude b62c4933… 16293742… }` |
| 16:59:49.224 | Fable sends hrg0, `Soft.Order «The two sources are ready now; this replaces bn3d…»` | Fable transcript |
| 16:59:49.731 | hrg0 lands in b62c49 as a user turn, native uuid c6196d4a-bf09-455b-9b6c-c668f75f8d3b | b62c4933…jsonl |
| 16:59:49.984 | Fable's Send returns `Sent.hrg0` | Fable transcript |
| 17:00:22-36 | b62c49 works on hrg0: checks both sources and starts four background illustrator subagents (figures7/ 1-2, figures-route/ 1-2). Its turn ends at 17:00:38 with `pendingBackgroundAgentCount: 4` | b62c4933…jsonl |
| 17:00:39 | Flow sends the handover reminder pmoz to b62c49: `{ Notification MiddleAbrupt.Notice.{ pmoz «Your context is near your refresh threshold. Write your handover now … then ask for your own refresh: flow-nexus Refresh…» } }` | b62c4933…jsonl; DebugDelivery.pmoz = sender `Flow`, Delivered |
| 17:00:49 | b62c49 writes flows/b62c49/handover.md, which names hrg0 as open | file mtime 17:00:49.817 |
| 17:00:51.353 | b62c49 runs `flow-nexus 'Refresh.{ Psyche book Haiku }'` and gets `RefreshQueued.{ { Psyche book Haiku } b62c49 }`. Journal: "works; its refresh waits for its rest" (`waking.rs` `queue_refresh`, ~2171) | b62c4933…jsonl; journal |
| 17:00:53 | b62c49 ends its turn. It says the refresh "will wait for the four background illustrators to finish", which is a wrong belief | b62c4933…jsonl |
| 17:00:54 | "rests; the replacement ordered for it runs" (`replace_as_ordered`, ~2288). An ordered Refresh counts as `closable` "whatever it runs" (~4020), so the background work is ended | journal; source |
| 17:00:55 | "refreshed; Psyche book Haiku sleeps until a waking request" (`refresh_held`, ~2138). No successor is started | journal |
| 17:07:50-57 | Opus sends 6o6f, `MiddleAbrupt.Order` asking for the same two pages and a third. MiddleAbrupt is a waking request. Successor bd378a wakes: "its first prompt carried 1 requests" | journal; bd378ab1…jsonl |
| 17:07:58 | bd378a's first prompt carries 6o6f, b62c49's handover, then "Flow b62c49, which this flow succeeds, left these requests open; answer each by its id." with about 30 open requests, ending with bn3d and hrg0 | bd378ab1…jsonl |
| 17:08:55 | `Inspect`: `Awake.bd378a`. The queue holds one Soft Notice, wxyi, from Opus. `DebugDelivery.hrg0` = `{ 24775 logical-delivery-…24772 hrg0 Sender.{ Psyche core Fable } { Psyche book Haiku } Delivered.{ Claude b62c4933… c6196d4a… } } Some.{…} None`, so hrg0 is delivered and unanswered | meta reads |
| 17:09:53-56 | The figure SVGs appear in b62c49's scratchpad figures7/ and figures-route/. bd378a is presumably redoing the drawings (inferred) | file mtimes |

## Answers

1. **What ended b62c49 (observed).** b62c49 ordered its own refresh. Flow's handover reminder pmoz (sender Notification, context near the threshold) told it to write a handover and run `Refresh`, and it did so at 17:00:51. This was a Refresh input from the flow itself: not a hold, and not a direct threshold refresh. n6q7 played no part. n6q7 was only a hold on bn3d: it was absorbed mid-turn at 16:59:22, and b62c49 went on to take up hrg0 afterwards.
2. **Where hrg0 went (observed).** hrg0 was delivered to b62c49 at 16:59:49.7, before the refresh. b62c49 started on it, and its four illustrators were ended by the refresh. hrg0 stayed open (Delivered, no answer) and was never queued, which is why `Queues` showed nothing. Nobody held it from 17:00:55 to 17:07:57. bd378a's first prompt then carried it as an open request. It was neither dropped, nor archived, nor cancelled. bn3d is also still open: a Notice does not close an Order. n6q7 was a MiddleAbrupt Notice from { Psyche core Fable }, delivered to b62c49.
3. **Why Sent (observed).** A seat was present. At 16:59:49 b62c49 was awake and took hrg0 as a native user turn (uuid c6196d4a). Flow answers Sent only when the DeliveryState is Delivered or Read (`sending.rs` `completed_direct_response`, ~197-221). The answer was correct at that moment. The premise of the question was wrong: the seat ended 65 s later.

## The defect (inferred against intent; by the letter of 0.56.2 this is designed OnDemand behaviour)

When a flow is refreshed, Flow decides whether to start a successor from the queue alone, and never from the Address's open delivered requests:

```rust
// waking.rs refresh_held (~2058) and the threshold path (~4063)
let wakes = metaflow.queue.0.iter()
    .any(|entry| !matches!(entry.message, signal_flow::Message::Soft(_)));
if continuity == Continuity::Maintained || wakes { /* successor first */ }
// otherwise: close_at_rest, "sleeps until a waking request"
```

`store.open_requests(address)` (`store/logical_delivery.rs:560`) is read only at composition (`performing.rs:279`). As a result, an OnDemand permaflow that is refreshed while it holds a delivered, unanswered Order or Task sleeps with that work owed. It wakes only when some unrelated non-Soft request arrives.

A second, related point: the handover reminder tells a flow to refresh itself with no check for open requests or background work. An ordered Refresh is closable at idle "whatever it runs" (`waking.rs` ~4020), so the flow's in-flight subagents are ended.

## Side observation

bd378a's open-request set carried about 30 requests, most of them old Opus Orders (5z4m, y4pt, bj5l, …). Requests that predecessors never answered pile up across successions. This is not investigated further here.
