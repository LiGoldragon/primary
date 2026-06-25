---
name: helper-only
description: Trigger for helper-only, no-reading, subagent-first, and exact helper brief generation workflows where the main thread must learn through helpers only.
---

# Helper-Only

Use this skill when the user asks for helper-only, subagent-only, main-thread
no-reading, learn through helpers only, subagent-first exploration, or an exact
helper brief.

Before spawning a subagent, run:

```sh
tools/helper-only-brief --harness codex --task "$ARGUMENTS"
```

Use the generated packet unchanged unless the user has supplied a narrower
authority, lane, source, or mode that must be passed to the command.

## Lead Packet

- Keep the main thread's workspace reads to this skill, the generated brief, and
  the helper's final return.
- Do not inspect broad source trees, reports, repo docs, or task files yourself.
- Dispatch meaningful reading to the helper with the full generated envelope.
- Treat the helper as the context carrier: it reads `AGENTS.md`,
  `skills/skills.nota`, triggered skills, named sources, and command output.
- Ask the user only for authority, private scope, or a real judgment fork.

## Helper Packet

The helper receives:

- The exact user task and generated brief.
- Harness, mode, authority, cwd, lane, and source manifest.
- Required startup reads and forbidden paths/actions.
- Current `jj st` dirty state when available.
- Return schema requiring files read or changed, commands run, findings,
  blockers, dirty-state changes, and next concrete action.

## Forbidden Lead Actions

- No broad workspace reading.
- No `private-repos/` inspection unless explicitly authorized by the user.
- No `/nix/store` filesystem search.
- No raw `git`; use `jj` for status and version-control work.
- No silent expansion from read-only to edit or report authority.

## Dispatch Shape

Send the generated Markdown brief directly to the subagent. If the request asks
for implementation, prefer:

```sh
tools/helper-only-brief --harness codex --mode implement --authority edit --task "$ARGUMENTS"
```

If the request asks for exploration only, keep the defaults.
