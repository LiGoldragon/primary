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
