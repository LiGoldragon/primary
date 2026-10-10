# Assistant role registration — 2026-06-01

## What changed

The workspace now has an `assistant` role for personal-affairs support for the psyche.

## Surfaces updated

- `orchestrate/roles.list` includes `assistant`, so `tools/orchestrate` can claim, release, and show `orchestrate/assistant.lock`.
- `reports/assistant/` exists as the assistant report lane.
- `skills/assistant.md` defines the role discipline.
- `skills/skills.nota` indexes the assistant role.
- `AGENTS.md`, `orchestrate/AGENTS.md`, and `skills/role-lanes.md` name the role and its report lane.
- `orchestrate-cli` tests were updated so the registry fixtures match the current lane set plus `assistant`.

## Intent captured

Spirit record `1425` records the psyche's decision: assistant is a workspace role/lane for this agent, helping with personal affairs and carrying orchestration support plus `reports/assistant/`.

## Verification

Verified:

```sh
cd orchestrate-cli && cargo fmt && cargo test --quiet
cd orchestrate-cli && cargo build --release --bin orchestrate --quiet
tools/orchestrate status
tools/orchestrate claim assistant /home/li/primary/reports/assistant -- assistant report-lane smoke test
tools/orchestrate release assistant
```
