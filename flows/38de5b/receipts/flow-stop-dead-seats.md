# Flow Stop of dead seats b860be and 88475f

Subflow of 38de5b, 2026-09-26 ~15:35Z. Live Flow 0.12.2 (flow repo 34aaf78, signal-flow 74a47ed).

## Method

Read-only liveness probes first, then `flow 'Stop.<id>'` only because both seats were dead on every probe, then `flow 'List.{}'`.

- `herdr --session <s> agent get <pane>` for s in default, fms-9bc4f7, messaging-build (every running session in `herdr session list`).
- `flow 'ResolveRecipient.<id>'` (refreshes the Herdr route live).
- `pgrep -af <thread-id-prefix>` for the native thread.
- Stop payload: signal-flow 74a47ed `ethos/signal.ethos` declares `Stop.StopRequest` and `StopRequest.FlowId` (`FlowId.String`); generated `pub type StopRequest = FlowId;`. Query composed as `Stop.<id>`.

## Liveness

| Seat | Pane | herdr agent get (3 sessions) | ResolveRecipient HerdrRoute | pgrep |
|---|---|---|---|---|
| b860be (b860be42-d89d-4eee-a0c2-216ec0107a86) | w1A:p1 | agent_not_found in all three | Unavailable | no process |
| 88475f (88475fd7-e328-4e11-9094-db2139a08fe0) | w17:p1 | agent_not_found in all three | Unavailable | no process |

ResolveRecipient replies verbatim:

    RecipientResolved.{ b860be b860be42-d89d-4eee-a0c2-216ec0107a86 Claude Unavailable Unavailable { e167d8 e167d857-17e7-441b-b38b-54941a77a77a fable-successor-of-da88cf } Active }
    RecipientResolved.{ 88475f 88475fd7-e328-4e11-9094-db2139a08fe0 Claude Unavailable Unavailable { e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 handover-successor } Active }

## Stop

2026-09-26T15:35:32Z, verbatim replies:

    $ flow 'Stop.b860be'
    StopRejected.RouteUnavailable
    $ flow 'Stop.88475f'
    StopRejected.RouteUnavailable

List rows afterwards, verbatim (still Active; List shows the stored route, not the refreshed one):

    { b860be b860be42-d89d-4eee-a0c2-216ec0107a86 Claude Unavailable Available.{ messaging-build claude-bccd531237a4454d86f45447 w1A:p1 term_65c5d073c6e318f } { e167d8 e167d857-17e7-441b-b38b-54941a77a77a fable-successor-of-da88cf } Active }
    { 88475f 88475fd7-e328-4e11-9094-db2139a08fe0 Claude Unavailable Available.{ messaging-build claude-86b6e54cb9618d95d6d8ceaa w17:p1 term_65c5883e612c88a } { e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 handover-successor } Active }

## Why Stop cannot retire a dead seat at 0.12.2

flow 34aaf78 `crates/flow-nexus/src/lib.rs` `Query::Stop`: after the lifecycle check it calls `self.herdr.refresh_route(node)` and returns `StopRejected.RouteUnavailable` unless the route is `Available`; only then does it close the pane and `record_stopped`. A seat whose pane is gone can therefore never reach `record_stopped` through Stop. This is by design, not an error in the probe.

The flow checkout at 0.16.0 (9aa9bf8) adds a meta-socket `Retire.<FlowId>` query ("A seat Flow lost. Retire keeps the row, its origin and ...") and a Retired lifecycle, which is the path for exactly these seats. It is not in the live 0.12.2.

## Not done

No Start, Replace, Send, or meta query was issued. No registry row changed.
