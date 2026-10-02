# Book agent regeneration witness

Method: read the generator and data, regenerated into Primary, launched the
`book` agent from this session (CLAUDE_CODE_SESSION_ID 91ea9f9f-e4da-49dd-8102-9f235e68f41a).

## Cause (witnessed)
- Generator: `curriculum-deploy` (/git/github.com/LiGoldragon/curriculum-deploy), run as
  `target/debug/curriculum-deploy 'Generate.{ «/git/github.com/LiGoldragon/Curriculum» «/home/li/primary» }'`.
- It read only `Curriculum/skills/*.md` and `Curriculum/roles.datom`. It never read Primary `subagents/*.md`, so book's body was only the three universal modules.
- `roles.datom` declared `{ book write trivial ... [ ClaudeAgent ] }`; trivial resolves to claude-haiku-4-5. Not a stale run: a baseline regeneration before any edit produced no drift (stub was the faithful output).

## Fix
- curriculum-deploy fb171e3b: a Claude role packet appends `<workspace>/subagents/<name>.md` when it exists (new test `authored_subagent_procedure_is_carried_into_its_claude_role`; full suite green with CURRICULUM_TEST_DATA_ROOT set).
- Curriculum 2898f80a: book is `write demanding` -> model opus.
- Regenerated .claude/agents/book.md (13818 bytes, model 'opus', full procedure) landed in Primary commit 1b640291 (snapshotted by a concurrent flow's commit "Regenerate book agent from Curriculum before rename"); an immediate re-run produced no further drift. Both repos pushed.
- Not done: no version bump of curriculum-deploy (0.6.3); Curriculum pin in Primary/consumers not advanced; subagents/book-reader.md has no role, so no reader agent is generated; Codex/Pi packets do not carry procedures.

## Test
Agent tool, subagent_type `book`, prompt `Update the page.`: it again asked which page, 0 tool uses, 3.5 s. This session started before regeneration and the harness loads agent definitions at session start, so it ran the old Haiku stub. The test is inconclusive for the new file; a fresh session is needed.
