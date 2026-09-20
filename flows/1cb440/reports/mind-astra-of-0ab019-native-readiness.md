# Mind Astra of 0ab019 — native succession receipts

This records the native successor launch and its gates. It does not transfer
ownership, retire `0ab019`, or withdraw either endpoint.

## Profile and first turn

`tools/native-seat-launch.mjs` now contains the named
`mind-astra-of-0ab019` profile at `gpt-6-astra` / medium. The isolated source
change was committed and pushed as Primary `4b59889a199a1e29bcfee20b452d0fb20beb0a08`.

The new native thread is `01a0bcaa-6dcb-7c93-a9e2-49f98ac2e0e5`; its first
turn is `01a0bcaa-7249-7480-bf42-4079a3904e1e`. The retained first-turn receipt
is `.native-seat-receipts/mind-astra-of-0ab019-mind-astra-of-0ab019.json`.
Its matching rollout is
`/home/li/.codex/sessions/2026/09/20/rollout-2026-09-20T04-34-40-01a0bcaa-6dcb-7c93-a9e2-49f98ac2e0e5.jsonl`.

The launcher verified the rollout against the receipt: Astra / medium,
15 typed structured skills including `main-flow`, and the 29-source manifest.
The verified rollout SHA-256 is
`a9d9c00b6ac40e275e9d5ca935153c624d79628d6c180c218c1141b66981ba04`.
The receipt-only response made no tool call, identity claim, task delegation,
or seat mutation.

## Identity, tool, and endpoint

The authorized activation turn is
`01a0bcab-527d-7673-90f5-48a05bbd3780`. It claimed the distinct Flow identity
`98ac2e` through `flow-id codex --flows-root /home/li/primary/flows`. The same
turn has completed ordinary structured witnesses for `flow-id` and
`agent_intercom.intercom_whoami`, then one benign acknowledgement child. These
are separate from receipt-only verification.

The existing native UUID was remotely attached, without starting another model
session, with Herdr's supported Codex remote attach. Its live endpoint is:

- Flow: `98ac2e`
- name: `mind-astra-of-0ab019`
- session: `messaging-build`
- pane: `wK:p1`
- terminal: `term_65be107ba098b31`
- native thread: `01a0bcaa-6dcb-7c93-a9e2-49f98ac2e0e5`

`hm.py register` recorded that exact native thread in the HM registry. A
disposable route probe was submitted to that binding and the attached target
replied exactly `HM_READY 98ac2e-01a0bcaa` in its terminal transcript.

## Acceptance and remaining continuity gate

The target explicitly accepted inherited Mind work and continuity obligations
while retaining `0ab019` as active owner/crossover; it also said routes,
workers, and ownership remain unchanged.

Readiness/routing reports were submitted to `0ab019` and `f38926`. Those
messages are **Submitted**, not read receipts. The final pre-crossover gate is
still open: `0ab019` must relay each complete return from the retained
`night_messaging_build` and `night_meaning_roundtrip` streams to `98ac2e`, and
both endpoints must acknowledge the relays. This report therefore records no
ownership transfer.

## Sources

- `flows/0ab019/reports/night-refresh-handoff.md`
- `flows/1cb440/reports/mind-astra-clean-refresh-preparation.md`
- `tools/native-seat-launch.mjs`
- `/home/li/.local/state/hacky-messenger/98ac2e.json`
