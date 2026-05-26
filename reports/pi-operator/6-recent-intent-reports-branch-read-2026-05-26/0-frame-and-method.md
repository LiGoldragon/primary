# Frame and method — recent intent, reports, and working branches

## Request

Psyche asked the pi-operator lane to read recent intent, operator reports, designer reports, nota-designer material, and their working branch state, using subagents.

## Method

This is a subagent meta-report directory. The orchestrator will dispatch asynchronous, read-only subagents with fresh context to gather:

- recent Spirit intent records and the guidance implications;
- recent operator reports plus operator branch state;
- recent designer reports plus designer branch state;
- recent nota-designer reports plus nota-designer branch state.

Subagents are read-only: they should inspect files and version-control state, then write their findings into this directory. The orchestrator synthesis lands as the highest-numbered file.

## Constraints

- No source edits are authorized by this read/synthesis task.
- Subagents must not launch their own subagents.
- `jj` commands must be headless and non-interactive.
- Findings should distinguish what is in Spirit intent, what is in reports, and what is in branch/workspace state.
