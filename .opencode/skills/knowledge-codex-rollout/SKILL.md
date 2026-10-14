---
name: knowledge-codex-rollout
description: Where assistant text and completed-turn answer copies are recorded in version-qualified Codex JSONL rollouts.
---

In the inspected Codex 0.161.0-alpha.2 rollout, an assistant text message is a JSONL row with outer `type: "response_item"`, and `payload.type: "message"`, `payload.role: "assistant"`. Its text is in the ordered `payload.content` entries whose type is `output_text`, under each entry's `text` field. Function calls, tool outputs and reasoning records are different payload types.

`payload.phase: "commentary"` marks interim assistant text; `"final_answer"` marks terminal answer text. The exact protocol source warns that providers do not consistently emit phase: an absent phase means unknown, not a proven final answer.

A completed turn can also have an outer `event_msg` row with `payload.type: "task_complete"`, the `turn_id`, and `payload.last_agent_message`. That field is optional. The protocol also defines `agent_message` events with `message` and optional phase as another representation. Multiple representations of one answer are not separate assistant outputs.

The last physical line need not contain assistant text. Tool records, accounting and completion events can follow it; a still-active turn can already have newer commentary. “Latest assistant text in this file” and “answer of the latest completed turn” therefore select different records. A completed turn is identified by its own completion and turn boundary, rather than by choosing any final-looking string anywhere in the file. Historical or interrupted records can lack the newer fields.

## Actual transcript witness

In `rollout-2026-10-02T12-07-29-01a0fdcc-c1a1-7f43-8c23-06d41fa34438.jsonl`, inspected on 2026-10-13, line 29380 is an assistant `response_item` with phase `final_answer`. Its one output-text block has 405 characters. Line 29383 is the corresponding `task_complete`: its `last_agent_message` is byte-identical to that text (SHA-256 `93c3404eb890e1861e4b6824e0c572f2a504c3c7dc1d72bd3ce26b2f6031634b`). Later rows already contain commentary from the next active turn. The date in the filename is the session's creation date, not the date of every appended row.

Source: exact Codex tag `rust-v0.161.0-alpha.2`, commit `5ccfcfe0fe510784521a3328b93f1c2fccc5e7a1`, `codex-rs/protocol/src/models.rs`, `protocol.rs` and `legacy_events.rs`. The full witness path, row shapes and equality check are retained in `/home/li/private-repos/flow-evidence/41fa34/harness-knowledge-20261013/codex-rollout-text-match.json` and `codex-rollout-shapes.json`. No transcript was edited.
