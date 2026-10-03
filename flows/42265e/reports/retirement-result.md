# Native retirement result: Fable 9fb0ad

## Authority and acceptance evidence

This operation was performed by Field's delegated host executor on 2026-10-03
under the direct retirement grant. The accepted handover source is
`flows/edf227/witnesses/retirement-of-9fb0ad.md`. It records that Fable
`edf227` was registered as the successor and carried the handover of Fable
`9fb0ad`.

Immediately before the close, the read-only native-controller sequence was:

1. `herdr pane get w1:p1M` identified an idle Claude pane titled
   `Psyche.{ Fable 9fb0ad }`.
2. `herdr pane get w1:p1Q` identified the successor Claude pane titled
   `Psyche.{ Fable edf227 }`.
3. `FLOW_ID=42265e hm-list` showed `9fb0ad` as the Fable route and `edf227`
   as the registered successor route. Both were idle; this was native
   liveness, not a new model turn.

The pane identities, titles, route names, and handover source agree. No raw
native identifier, transcript payload, or checksum is reproduced here.

## Supported controller operation and result

The supported Herdr lifecycle command was `herdr pane close w1:p1M`.
Its controller receipt was a successful `cli:pane:close` reply with result
type `ok`.

Post-close read-only verification used `herdr pane get w1:p1M` and
`FLOW_ID=42265e hm-list`. The first returned `pane_not_found`; the second no
longer listed `9fb0ad` and still listed `edf227`. The native predecessor pane
and Messenger route are therefore both absent, while the accepted successor
route remains. The close operation preserves the native transcript/recovery
assets; no PID kill or deletion command was issued.

## Non-operations and rejected calls

No message was sent to Fable during this retirement. An attempted
`hm-retire 9fb0ad` wrapper call was rejected before execution because the
wrapper required `--session`, `--pane-id`, `--terminal-id`, `--name`,
`--agent`, `--native-thread`, `--evidence`, and `--evidence-sha256`.
The route had already disappeared after the supported pane close, so that
rejected wrapper was not retried.

Earlier, before the corrected target was supplied, the next-controller client
`flow-next-meta` was sent `Retire.38de5b`; it replied
`RetireRejected.UnknownFlow`. That controller/endpoint did not own the
unrelated row. This was a rejected, no-change request and is not retirement
evidence for `9fb0ad`; it must not be repeated.
