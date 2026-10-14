---
name: inquiry-context-module-size
description: Open measurements for context module size and instruction adherence.
dependencies: [knowledge-context-module-size]
---

The useful module-size threshold remains open. Measure it with matched
workloads rather than adopting a universal number.

1. For one model and task family, does adherence change when identical
   requirements are serialized as one module or several modules while total
   tokens, order, privilege, examples, and context occupancy are held
   constant?
2. Does cumulative loaded instruction length have an independent effect after
   holding constraint count, semantic complexity, output length, and position
   constant?
3. How do module boundaries and labels interact with instruction hierarchy,
   including conflicts and privilege?
4. How do results differ across current Claude and Codex model versions and
   their actual loading mechanisms?
5. Which metric should govern a module: per-constraint pass rate,
   all-constraints pass rate, sequential depth, task success, or budget and
   cost?

The measurements should retain the current direction: preserve one coherent
home for each statement, avoid duplicate statements, and do not proliferate
modules without a tested reason.
