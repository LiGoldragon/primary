# Recovery roster: native-context and reply witness

Audited 2026-09-27 from the named native transcript files. This supersedes the
earlier Herdr snapshot for context and reply facts. A native reply proves only
that the named native thread produced it; it does not prove a Flow, Messenger,
remote-control, or laptop route.

| Seat | Native thread and model / effort | Title evidence | Accepted recovery context | Fresh native reply |
| --- | --- | --- | --- | --- |
| Mind Sol `56ae53` | `01a0de4c-554d-7343-bbc5-e4256ae5366f`; `gpt-6-sol` / `medium` | launch receipt: `MindV2.{ Sol 56ae53 }` | expanded `psyche` skill, Vision/raw-vision paths, `main-flow`, predecessor/handoff/recovery | 01:51:26Z |
| Mind Astra `6fe957` | `01a0dfdc-a500-7271-8f54-e446fe9578dd`; `gpt-6-astra` / `medium` | native Codex app-server thread-name readback: `MindV2.{ Astra 6fe957 }` | same four context classes | 01:51:32Z |
| Mind Luna `139366` | `01a0e032-e8aa-7131-90c4-a54139366ece`; `gpt-6-luna` / `medium` | transcript: `MindV2.{ Luna 139366 }` | same four context classes | 01:42:55Z |
| Field Luna `184bd8` | `01a0e021-aa68-72a2-a8df-7d6184bd8c00`; `gpt-6-luna` / `medium` | transcript: `FieldV2.{ Luna 184bd8 }` | same four context classes | 01:50:59Z |
| Field Sol `9ac67c` | `01a0e029-558a-7852-b5df-1919ac67c6d7`; `gpt-6-sol` / `medium` | transcript: `FieldV2.{ Sol 9ac67c }` | same four context classes | 01:51:31Z |
| Field Astra `22e12b` | `01a0e02b-9036-7361-9078-55222e12bb1f`; `gpt-6-astra` / `medium` | transcript: `FieldV2.{ Astra 22e12b }` | same four context classes | 01:48:39Z |
| Psyche Fable `8904b1` | `8904b10d-7f06-4e44-9342-3a8a2d7e17bd`; `claude-fable-5-1` / `medium` | native `custom-title.json`: `PsycheV2.{ Fable 8904b1 }` | first accepted prompt 23:56:07Z, 34,369 bytes: same four context classes | 01:47:05Z |
| Psyche Opus `dc53b4` | `dc53b4be-338b-4601-ab3c-a0e155fc8fa9`; `claude-opus-5-5` / `medium` | native `custom-title.json`: `PsycheV2.{ Opus dc53b4 }` | first accepted prompt 00:13:46Z, 57,634 bytes: same four context classes | 01:41:53Z |
| Psyche Sonnet `38f337` | `38f33758-72c0-4c2a-ad49-8ffeb8e310fa`; `claude-sonnet-5` / `medium` | native `custom-title.json`: `PsycheV2.{ Sonnet 38f337 }` | first accepted prompt 00:21:03Z, 70,475 bytes: same four context classes | 01:42:08Z |

For the six Codex threads, the verdict comes from accepted native user content:
each has the expanded `psyche` skill, a `Vision/`, `vision-raw/`, or
`flows/*/vision/` source, `main-flow`, and predecessor/handoff/recovery
language. Mind Sol's immediate predecessor (`00f95a`) is explicit in its native
launch receipt. This audit does not infer an immediate predecessor identity for
the other five merely from that language.

## Evidence paths

Codex native transcripts are under
`/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T*.jsonl`, keyed
by the six UUIDs above. Mind Sol's separate native launch receipt is
`flows/00f95a/mind-sol-refresh/launch-receipt.json`.

Mind Astra's title was read from the native Codex app-server thread record for
`01a0dfdc-a500-7271-8f54-e446fe9578dd`; its thread name is exactly
`MindV2.{ Astra 6fe957 }`. Herdr terminal titles are separate pane metadata and
were not used for this title claim.

Claude native transcripts are under `/home/li/.claude/projects/`, keyed by the
three UUIDs above; their native `custom-title.json` files provide the title
readback.

## Separate route and remote-control gaps

The native evidence does not establish a current Flow or Messenger reply for
any row, a current endpoint-ready result, or remote laptop access. The earlier
Herdr `interactive_ready` and settled states are historical route observations.
The Claude daemon adoption and endpoint-readiness gap remains; the three fresh
Claude replies do not repair that gate. No native transcript was used to claim
a connected laptop client or enabled remote-control surface.

No successor profile or source manifest in `flows/` referenced this receipt
path when this update was prepared, so it was not hash-pinned.
