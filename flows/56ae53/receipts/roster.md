# Recovery roster: bounded native and registry witness

Audited 2026-09-27. This is a nine-seat roster. A native reply witnesses that
one native session replied; it does not establish a Flow row, a Messenger
route, remote control, or access from a laptop.

| Seat | Native-session and reply witness | Title evidence | Context / bootstrap limit |
| --- | --- | --- | --- |
| Mind Sol `c56100` | `01a0e0a1-7075-7cc2-928d-13fc56100504`; native reply: “Native context is present.” | Launcher prompt says its V2 title was set and read back; no separate adapter readback was audited here. | The current Mind Sol. The transcript carries structured skill delivery, but this receipt does not restate a full first-prompt audit. |
| Mind Astra `6fe957` | `01a0dfdc-a500-7271-8f54-e446fe9578dd`; native reply witnessed. | Native Codex app-server thread-name readback: `MindV2.{ Astra 6fe957 }`. | Not re-audited in this correction. |
| Mind Luna `139366` | `01a0e032-e8aa-7131-90c4-a54139366ece`; native reply witnessed. | Transcript: `MindV2.{ Luna 139366 }`. | Not re-audited in this correction. |
| Field Luna `184bd8` | `01a0e021-aa68-72a2-a8df-7d6184bd8c00`; native reply witnessed. | Transcript: `FieldV2.{ Luna 184bd8 }`. | Not re-audited in this correction. |
| Field Sol `9ac67c` | `01a0e029-558a-7852-b5df-1919ac67c6d7`; native reply witnessed. | Transcript: `FieldV2.{ Sol 9ac67c }`. | Not re-audited in this correction. |
| Field Astra `22e12b` | `01a0e02b-9036-7361-9078-55222e12bb1f`; native reply witnessed. | Transcript: `FieldV2.{ Astra 22e12b }`. | Not re-audited in this correction. |
| Psyche Fable `8904b1` | Unique native Claude session `8904b10d-7f06-4e44-9342-3a8a2d7e17bd`; native reply witnessed. | Native `custom-title.json`: `PsycheV2.{ Fable 8904b1 }`. | Provider creation versus resumption, first-prompt contents, and psyche middle-stratum contents are unknown. Later native skill expansions repair working context only; they do not prove bootstrap. |
| Psyche Opus `dc53b4` | Unique native Claude session `dc53b4be-338b-4601-ab3c-a0e155fc8fa9`; native reply witnessed. | Native `custom-title.json`: `PsycheV2.{ Opus dc53b4 }`. | Provider creation versus resumption, first-prompt contents, and psyche middle-stratum contents are unknown. |
| Psyche Sonnet `38f337` | Unique native Claude session `38f33758-72c0-4c2a-ad49-8ffeb8e310fa`; native reply witnessed. | Native `custom-title.json`: `PsycheV2.{ Sonnet 38f337 }`. | Provider creation versus resumption, first-prompt contents, and psyche middle-stratum contents are unknown. |

## Mind Sol provenance and registry limits

`56ae53` is the predecessor provenance for `c56100`, retained through its flow
directory, handoff, and native transcript `01a0de4c-554d-7343-bbc5-e4256ae5366f`.
It is not the current Mind Sol row and does not occupy a ninth seat here.

The existing recovery receipt records `c56100` as **HM Bound**, idle, in
`recovery-56ae53` at `w1:p3`; its observation was a transported Opus reply
whose passive pane read did not confirm arrival. That establishes only the
recorded HM binding state and its limited message witness.

**Flow Imported Pending** is a separate registry state. This audit neither
read a Flow List row for `c56100` nor promotes the HM binding to a Flow claim.
Conversely, an imported-pending row would not establish an HM binding. The two
labels remain separate until each has its own current witness.

## Evidence paths

The current Mind Sol native transcript is
`/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T20-11-11-01a0e0a1-7075-7cc2-928d-13fc56100504.jsonl`.
The bounded HM witness is `flows/dc53b4/log.md`. The Claude session UUIDs and
native title files are the named native records; this correction does not
infer provider creation or a launcher bootstrap from them.

## Historical intended/reply roster versus current qualified count

The prior native-context/reply audit used a different, historical nine-seat
enumeration.  It included predecessor Mind Sol `56ae53` and recorded these
native-reply timestamps: `56ae53` 01:51:26Z; `6fe957` 01:51:32Z; `139366`
01:42:55Z; `184bd8` 01:50:59Z; `9ac67c` 01:51:31Z; `22e12b` 01:48:39Z;
`8904b1` 01:47:05Z; `dc53b4` 01:41:53Z; and `38f337` 01:42:08Z.  Its
provenance is the named native transcript audit in historical receipt revision
`e56c89effcff308b6087b6c04853e701a5f01fcc`, not a current Messenger route
snapshot.  This preserves the predecessor and reply evidence without treating
it as current route evidence.

The current local qualified count is a different observation: eight default
HM bindings (`6fe957`, `139366`, `184bd8`, `9ac67c`, `22e12b`, `8904b1`,
`dc53b4`, `38f337`) plus Mind Sol `c56100`, HM-bound in
`recovery-56ae53`.  The latter has native Herdr session
`01a0e0a1-7075-7cc2-928d-13fc56100504`, `interactive_ready=true`, and title
`MindV2.{ Sol c56100 }`; it is idle.  This establishes nine local HM-bound
live seats across Mind, Field, and Psyche.  The predecessor `56ae53` remains a
separate stale `messaging-build` route and is not part of this qualified count.

Neither enumeration proves an external laptop attach, a current Flow row for
every seat, or a recent target-side accepted reply.  Current Flow rows and
remote access require their own witnesses; the historical timestamps above are
preserved only as native-reply provenance.

## 2026-09-27 current stable-Flow addendum

A fresh stable `List.{}` readback found all nine qualified local HM-bound seats
`Active`: default-session `6fe957`, `139366`, `184bd8`, `9ac67c`, `22e12b`,
`8904b1`, `dc53b4`, and `38f337`, plus `c56100` in `recovery-56ae53`.  The
corresponding current routes are the eight default agent/pane bindings and
`c56100` at `recovery-56ae53 / mind_sol_c56100 / w1:p3 /
term_65c6d6c5c3aac3`.  This is a local stable-Flow state observation only.

Field's durable receipt
`flows/9ac67c/receipts/stable-flow-send-c56100-20260927.md` records
`Sent.Presented.{ c56100 w1:p3 1790492832474 }` and its immediate matching
stable-Flow `Active` row.  Presentation and the Active row do not prove that
the native harness read or answered that prompt; no recent accepted reply is
claimed for the other eight seats.

Several endpoint fields remain `Unavailable`, including c56100 and Astra's
Codex endpoints and the foreground Psyche Claude endpoints.  This addendum
does not establish external remote control: laptop attachment remains
unverified, and the retained Prometheus/Zeus reachability probes remain
unverified/failed.  Those network facts require separate fresh witnesses.
