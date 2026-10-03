---
description: Review-only candidate for the authored Codex harness knowledge. It is not deployed skill text.
---

Use the installed Codex version paired with its generated protocol schema and pinned source revision. Record the version and source hash with every protocol integration.

Initialize an app-server connection before requests. `hooks/list` takes optional `cwds` and returns `data`; it lists configured hooks for each cwd. It does not load skills.

The twelve hook event names are `preToolUse`, `permissionRequest`, `postToolUse`, `preCompact`, `postCompact`, `sessionStart`, `sessionEnd`, `userPromptSubmit`, `subagentStart`, `subagentStop`, `stop`, and `interrupt`.

`hook/started` and `hook/completed` notifications carry `run`, `threadId`, and nullable `turnId`. A command hook receives serialized event JSON on stdin only where the tagged Codex source proves that behavior. Do not infer command input, environment, or per-thread hook installation from the JSON schema.

Approval server requests are `item/commandExecution/requestApproval`, `item/fileChange/requestApproval`, and `item/permissions/requestApproval`. Reply only with the matching typed response. Command decisions include acceptance, session acceptance, an execpolicy or network amendment when offered, decline, and cancel. File decisions have no amendment variant. Permissions replies carry structured `permissions`, `scope` with default `turn`, and nullable `strictAutoReview`. These replies do not grant Flow authority or override host policy.

Thread start and resume use the thread-level sandbox enum. Turn start uses structured `sandboxPolicy`. Preserve the selected policy; schema acceptance does not prove runtime enforcement.

Rate-limit reads and updates are account allowance data, separate from token usage and approvals. Start a collector from a read snapshot and merge sparse updates. Re-read after reconnect because this interface defines no notification cursor, ordering, or replay guarantee.

Keep Flow identity allocation out of deployed Codex harness knowledge. Current Flow allocation choices are pending the living. UUIDv7 collision behavior is an explicit design question, not an implementation fact.
