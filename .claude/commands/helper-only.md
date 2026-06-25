---
name: helper-only
description: Compatibility command for deterministic helper-only workflows.
disable-model-invocation: true
context: fork
agent: helper-only-explorer
---

# Helper-Only

Run the deterministic brief generator and use its output as the complete
subagent instruction. The main thread must not inspect workspace files beyond
the command and generated dynamic context.

!`tools/helper-only-brief --harness claude --task "$ARGUMENTS"`

Dispatch the generated packet unchanged. The helper-only-explorer agent performs
startup reads, task reads, and command work inside the authority named by the
brief, then returns the requested schema.
