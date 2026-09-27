# Recovery roster witness

Observed on 2026-09-26 at 18:25:35 America/Mexico_City from the live Herdr
snapshot, and checked again during this recovery. This receipt records only
facts observed locally. `done` is Herdr's settled lifecycle and
`interactive_ready=true` is its interactive-route evidence.

| Seat | Native session | Native model / effort | Terminal title | Herdr pane | Flow row | Message reply |
| --- | --- | --- | --- | --- | --- | --- |
| Field Astra `22e12b` | `01a0e02b-9036-7361-9078-55222e12bb1f` | unverified / unverified | `field-packet-56ae53` | `w1:pA` | Active; Codex endpoint Ready; Herdr Available | not independently witnessed here |
| Field Luna `184bd8` | `01a0e021-aa68-72a2-a8df-7d6184bd8c00` | unverified / unverified | `field-packet-56ae53` | `w1:p7` | Active; Codex endpoint Ready; Herdr Available | not independently witnessed here |
| Field Luna `19ff9f` | `01a0dfef-25bd-7dc3-9f6d-50d19ff9f733` | unverified / unverified | `FieldV2.{ Luna 19ff9f } | primary` | `w1:p3` | intentionally incomplete predecessor; remains unbound | not independently witnessed here |
| Field Sol `9ac67c` | `01a0e029-558a-7852-b5df-1919ac67c6d7` | unverified / unverified | `field-packet-56ae53` | `w1:p9` | Active; Codex endpoint Ready; Herdr Available | not independently witnessed here |
| Mind Astra `6fe957` | `01a0dfdc-a500-7271-8f54-e446fe9578dd` | unverified / unverified | `MindV2.{ Astra 6fe957 } | primary` | `w1:p2` | Pending; Codex endpoint Unavailable; Herdr Available | delegated historical witness: old Message task Presented and native recovery reply |
| Mind Luna `139366` | `01a0e032-e8aa-7131-90c4-a54139366ece` | unverified / unverified | `primary` | `w1:pD` | Active; Codex endpoint Ready; Herdr Available | not independently witnessed here |
| Psyche Fable `8904b1` | `8904b10d-7f06-4e44-9342-3a8a2d7e17bd` | `claude-fable-5-1` / `medium` | `✳ PsycheV2.{ Fable 8904b1 }` | `w1:p8` | Active; Claude endpoint Unavailable; Herdr Available | not independently witnessed here |
| Psyche Opus `dc53b4` | `dc53b4be-338b-4601-ab3c-a0e155fc8fa9` | `claude-opus-5-5` / `medium` | `✳ PsycheV2.{ Opus dc53b4 }` | `w1:pC` | Active; Claude endpoint Unavailable; Herdr Available | not independently witnessed here |
| Psyche Sonnet `38f337` | `38f33758-72c0-4c2a-ad49-8ffeb8e310fa` | `claude-sonnet-5` / `medium` | `✳ PsycheV2.{ Sonnet 38f337 }` | `w1:pF` | Active; Claude endpoint Unavailable; Herdr Available | not independently witnessed here |

All nine rows above had a live Herdr agent with `interactive_ready=true` in
the snapshot. Their observed settled states were `idle` for `19ff9f` and
`6fe957`, and `done` for the other seven.

## Claude daemon limitation

The three Psyche Claude sessions are live foreground `claude --remote-control`
processes, and `claude agents --json --all` lists each as `kind: interactive`.
They are absent from `~/.claude/daemon/roster.json`; that roster was last
written on 2026-09-19, its supervisor PID no longer exists, and its control
socket is absent. Flow correctly withholds the Claude endpoint because its
readiness gate requires the daemon job state, roster worker, rendezvous socket,
control socket, and live worker PID together.

`claude daemon run` can start an on-demand supervisor, but no supported
adoption operation was found for these foreground sessions. Restarting only
re-adopts any surviving *background* roster workers and does not establish the
required daemon ownership for the three foreground Psyche seats. The installed
`claude agents --json --all` diagnostic briefly performs that on-demand
supervisor probe; its subsequent status was `not running`. No foreground seat
was restarted, replaced, or interrupted.

Source witnesses: `herdr api snapshot` captured at 18:25:35; `flow
'List.{}'`; current Claude process argument vectors; `claude daemon status`;
and `claude agents --json --all`.

The Mind Astra Message entry is a delegated historical witness reported by the
Mind Luna packet worker: it observed an old Message task `Presented` to
`6fe957` and a native terminal recovery-task reply. It is not a new Message
query or reply witnessed by this receipt writer. Astra remains reachable by
Herdr and the pre-existing Message path even though Flow 0.12.2 keeps the
imported Flow row Pending.
