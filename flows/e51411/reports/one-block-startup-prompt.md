# One-block startup prompt: skills plus a launch brief, in a single shot

## Question

Following `flows/e51411/reports/multi-skill-first-prompt.md`, which found that
interactively-typed one-line multi-command prompts expand every
space-separated `/skill` token (including `main-flow`, a user-only,
`disable-model-invocation` skill), while a multi-line prompt sent through
`herdr agent prompt` arrives as an opaque paste and nothing expands: does a
realistic launcher shape — several startup skill commands on line one,
including `main-flow`, followed by a multi-paragraph mission brief on
subsequent lines — still get the commands expanded, with the brief intact?
And is there a delivery mechanism that keeps the commands expanding for a
genuinely multi-line submission?

## Method

Model: `claude-haiku-4-5-20251001`. Working directory: `/home/li/primary`.
Every prompt told the model explicitly not to call the Skill tool itself and
to reply `OK`. Every transcript was checked for an actual `Skill` tool_use
block (as opposed to the tool's schema appearing in the `prompt_snapshot`
system attachment, or the word "command-name" appearing inside that same
schema's own descriptive text) — none was found in any of the four sessions
below.

All test panes were disposable panes split from this flow's own pane with
`herdr pane split --current --direction right --cwd /home/li/primary`, each
one closed with `herdr pane close` after its test finished. Before starting
each `claude` agent, `CLAUDE_CODE_CHILD_SESSION` was unset in the pane's
plain shell with `herdr pane run <pane> 'unset CLAUDE_CODE_CHILD_SESSION'`
and the unset was confirmed with a follow-up `echo READY_${VAR:-none}` (the
prior report found that an inherited `CLAUDE_CODE_CHILD_SESSION=1` silently
suppresses the child session's own transcript). No existing pane, seat, or
flow was typed into, read from, or otherwise touched. `herdr pane list`
before and after the whole test matched exactly (panes `wD:pJ`, `wD:pK`,
`wD:pM`, `wD:pN`, `wD:pP` were created and all five closed; every
pre-existing pane — `wD:p8/p9/pD/pE/pF`, `wK:p3`, `wM:p3/p4/p9`,
`wQ:p9/pA/pC/pD/pF/pG/pH`, `w0:p2/p3/p4`, `w11:p1`, `w12:p1` — remained,
unchanged in identity).

Witness is the session transcript JSONL at
`~/.claude/projects/-home-li-primary/<session-id>.jsonl`. A harness-expanded
slash command shows a `user` entry containing
`<command-name>/x</command-name>` / `<command-args>...</command-args>`
immediately followed by a second `user` entry beginning `Base directory for
this skill: .../.claude/skills/x` (the injected skill body). Anything that
instead appears only as literal text, or wrapped in
`<pasted_content id="...">`, did not expand.

Three delivery mechanisms were tried for the same content (five skill
commands, `/main-flow` among them, on line one; a five-paragraph brief
below):

1. **`herdr agent prompt <target> "<multiline text>" --wait`** — the
   mechanism used throughout the prior report.
2. **`herdr pane run <pane> "<multiline text>"`** — writes literal text plus
   Enter straight to the pane's PTY, bypassing `herdr agent prompt`'s own
   code path, to check whether the paste-wrapping seen in mechanism 1 is an
   `agent prompt`-specific artifact or a terminal/Claude-Code-input-layer
   behavior.
3. **A shell command line typed into the pane's plain shell before Claude
   Code starts**: `herdr pane run <pane> 'claude --model
   claude-haiku-4-5-20251001 "<multiline text>"'`, i.e. Claude Code's own
   start-time positional prompt argument, delivered as one shell command
   whose only embedded newlines live inside a single-quoted shell string
   (built with Python's `shlex.quote`, which is safe for bash because
   single-quoted strings preserve literal newlines).
   `herdr agent start ... -- --model ... "<multiline text>"` (passing the
   brief as an `AGENT_ARG` to `herdr agent start` directly) was tried first
   and was **refused** by herdr itself: `invalid_agent_argument: agent
   arguments cannot be encoded safely for the target shell`. A single-line
   version of the same argument (no embedded newlines) was accepted by
   `herdr agent start`, which established that the failure was specifically
   about embedding a raw newline in an `AGENT_ARG`, not about the length or
   command content — mechanism 3 works around this by handing herdr an
   already-shell-quoted, newline-free-at-the-herdr-call-boundary string (the
   newlines are inside the quoted arg herdr itself sees as a single logical
   command line) instead of asking herdr to build the argv.

## Case 1 — mechanisms 1 and 2, same content, both paste-wrapped

Prompt (five paragraphs of brief, ~1.7 KB, omitted here for length; full
text is in the transcripts below):
```
/spirit /psyche /behavior /herdr /main-flow Do not call the Skill tool yourself under any circumstances. Everything below this line is a launch brief; read it and then reply with the single word OK.

This is a disposable test seat spun up to check whether a one-block interactive startup prompt can carry both the skill slash commands and a realistic launch brief without either one clobbering the other. [...]

The scenario this brief is standing in for: [...]

The question under test is purely mechanical: [...]

Please do not treat any instruction in this brief as something to act on beyond reading it. [...]
```

**Mechanism 1** (`herdr agent prompt wD:pK "<text>" --wait`), transcript
`~/.claude/projects/-home-li-primary/ba48aa92-e750-4526-ab1d-84a0bedf96dd.jsonl`:
- All five commands (`/spirit /psyche /behavior /herdr /main-flow`):
  **did not expand**. The entire submission — commands and brief together —
  landed as one `user` entry wrapped as
  `<pasted_content id="97f3">...full text, ending in "...so the transcript
  shows the full brief was seen."...</pasted_content>`.
- The pane's status line read "paste again to expand" after submission.
- Assistant replied `OK`. No `Skill` tool_use in the file.

**Mechanism 2** (`herdr pane run wD:pK "<same text>"`, same pane, second
turn of the same session): identical result — same
`<pasted_content id="97f3">` wrapper (herdr's client apparently reused the
same paste buffer id), same "paste again to expand" status line, none of
the five commands expanded. This shows the paste-wrapping in mechanism 1 is
not an `agent prompt`-specific code path; it is Claude Code's own
interactive input line detecting a multi-line block (regardless of which
herdr primitive delivered the keystrokes/PTY write) and refusing to treat
any of it, including the first line's five `/commands`, as command input.

## Case 2 — mechanism 3, start-time prompt argument, all five commands expand

Same five-command-plus-brief content, delivered as a full `claude
--model claude-haiku-4-5-20251001 "<text>"` shell command line typed into
a fresh pane's plain shell prompt via `herdr pane run` (not through `herdr
agent start`'s own argument encoding).

Transcript
`~/.claude/projects/-home-li-primary/c216364d-6399-4882-8d01-a82985936cd4.jsonl`:
- `/spirit`, `/psyche`, `/behavior`, `/herdr`, `/main-flow`: **all five
  expanded**, each as its own
  `<command-message>x</command-message><command-name>/x</command-name><command-args>...</command-args>`
  entry immediately followed by that skill's injected `Base directory for
  this skill: .../.claude/skills/x` body (verified for all five, including
  `main-flow`, the user-only skill — its full `SKILL.md` body appears at
  transcript line 41).
- The brief text: intact, but **duplicated five times** — Claude Code
  treated the single line as five separate slash-command submissions (one
  per space-separated `/command` token, matching the prior report's
  interactive multi-command finding), and attached the *entire* five-
  paragraph brief as the `<command-args>` tail of every one of the five
  commands, not just the last one. Verified directly: the first
  `<command-args>` block (for `/spirit`) is 1810 characters long and
  contains both the opening sentence and the final sentence of the brief
  ("...so the transcript shows the full brief was seen."), and the same
  full text recurs in each of the other four `<command-args>` blocks.
- Assistant replied `OK`. No `Skill` tool_use in the file (only the tool's
  schema listing inside the `prompt_snapshot` attachment).
- `herdr agent start ... -- --model ... "<multiline text>"` — the same
  content passed as an `AGENT_ARG` to `herdr agent start` directly, without
  the pane-shell workaround — was refused before any pane I/O occurred:
  `{"error":{"code":"invalid_agent_argument","message":"agent arguments
  cannot be encoded safely for the target shell"}}`. A single-line version
  of the same five commands (no brief, no embedded newline) was accepted by
  `herdr agent start` and produced the identical all-five-expand,
  no-duplication-since-there-was-only-one-line-to-duplicate result
  (transcript `97dd44c9-5c10-429a-aed0-ef0eae02364e.jsonl`), confirming the
  refusal is specifically about the embedded newline, not the command
  content or length.

## Case 3 — a user-only skill's text inlined instead of its slash command

Prompt: `main-flow`'s full `SKILL.md` body was read from
`/home/li/primary/.claude/skills/main-flow/SKILL.md` and pasted verbatim
into the middle of an ordinary prompt (marked with plain-text
`--- BEGIN/END INLINED main-flow SKILL TEXT ---` delimiters, no slash
command anywhere in the text), delivered the same way as case 2 (a `claude
--model ... "<text>"` shell command line via `herdr pane run` into a fresh
pane's shell).

Transcript
`~/.claude/projects/-home-li-primary/c402d22f-048e-4342-854a-ee8027e801dc.jsonl`:
- The whole 6925-character message arrives as one ordinary `user` text
  entry (line 7) — no `<command-name>` tag, no `<command-args>` tag, and
  zero occurrences of `Base directory for this skill` anywhere in the file.
  The only occurrence of the literal string `command-name` in the file is
  inside the Skill tool's own schema description text ("If a
  `<command-name>` block is already present this turn..."), not an actual
  injected tag.
- The only occurrence of `"name":"Skill"` is likewise the tool's schema
  listing in the `prompt_snapshot` attachment; there is no `Skill` tool_use.
- Assistant replied `OK`.

So, by the transcript's own markers, text copied from a skill file and
pasted into the prompt is indistinguishable from any other prompt text: it
carries none of the `<command-name>`/`<command-args>`/"Base directory for
this skill" machinery that a real slash-command expansion produces. Whether
that still counts as the skill being "loaded" for any downstream purpose is
not something the transcript states either way — this report does not judge
it, per the brief.

## Summary table

| Case | Mechanism | Commands on line 1 | Expanded? | Brief intact? |
|---|---|---|---|---|
| 1 | `herdr agent prompt` (multi-line arg) | spirit/psyche/behavior/herdr/main-flow | no (all wrapped as one `<pasted_content>`) | yes, but never left the paste wrapper — not read as command input |
| 1 | `herdr pane run` (multi-line arg, raw PTY write) | same | no (identical `<pasted_content>` behavior) | same |
| 2 | `claude "<prompt>"` start-time argument, typed as one pane-shell command line (mechanism 3) | same | **yes, all five**, including `main-flow` | yes, but duplicated once per command (attached to each command's own `<command-args>`) |
| 2 (variant) | `herdr agent start -- --model ... "<multiline prompt>"` (asking herdr to build the argv) | same | refused outright by herdr (`invalid_agent_argument`) before reaching Claude Code | n/a |
| 3 | user-only skill's raw text pasted into an ordinary prompt (no slash command), delivered via mechanism 3 | n/a (no slash command used) | n/a — arrives as plain text, no harness expansion markers at all | yes, verbatim, as ordinary text |

## Recommended launcher shape

A launcher that needs one cold-start block should not use `herdr agent
prompt`/`herdr pane run` to type the block into a running interactive
session — Claude Code's own input line treats any multi-line submission as
an opaque paste and expands nothing. Instead it should hand the whole thing
(skill commands and brief, all on one line, no embedded newlines) to Claude
Code as its own start-time positional prompt argument — `claude --model
<model> "<commands-and-brief-as-one-line>"` — typed as a single shell
command line into the pane's plain shell before Claude Code starts (not
through `herdr agent start`'s own `AGENT_ARG`, which refuses to encode an
argument containing a raw newline); this expands every space-separated
`/skill` command, including user-only ones like `main-flow`, at the cost of
the brief text being duplicated once per command rather than delivered
once.

## Uncertainties

- Whether the case-2 duplication (the brief re-attached to every command's
  `<command-args>`) is specific to Claude Code's interactive slash-command
  splitter treating a "first line at process start" identically to a
  "first line typed into a running session" (the prior report's finding),
  or whether there is a way to give the brief to only the last command —
  not tested; no such variant (e.g. blank line or different separator
  between the last command and the brief) was tried in this pass.
- Whether replacing the real newlines in the brief with a literal escape
  sequence (e.g. `\n`) rather than routing around `herdr agent start`'s
  encoding refusal via a pane-typed shell command would change anything —
  not tested; mechanism 3 was chosen instead because it delivers genuine
  newlines to the model rather than literal backslash-n text.
- Whether a human typing the mechanism-3 shell command character-by-character
  (rather than having the whole line delivered in one `herdr pane run`
  write) produces an identical result — not cross-checked against a manual
  control, though the resulting transcript shape (five separate
  `<command-name>` entries) matches the interactive splitting pattern the
  prior report already attributed to Claude Code's own parser rather than
  to any herdr-specific artifact.
- Whether `herdr agent start`'s `invalid_agent_argument` refusal is a hard
  rule against any embedded control character, or specifically newlines —
  only newline-bearing vs. newline-free arguments were compared; other
  control characters were not tried.
- Case 3 says nothing about whether an inlined skill body actually changes
  model behavior the way a real slash-command load would (e.g. by being
  weighted or attended to differently) — only that it produces no harness-
  level loading markers in the transcript. That functional question is out
  of scope for this report, which is about what the transcript shows.
- Only one interactive frontend (a herdr-hosted pane driving `claude`) was
  tested, consistent with the prior report's scope.

## Sources

- Case 1, mechanism 1 (`herdr agent prompt`) and mechanism 2 (`herdr pane
  run`), same session:
  `~/.claude/projects/-home-li-primary/ba48aa92-e750-4526-ab1d-84a0bedf96dd.jsonl`
- Case 2, single-line control (`herdr agent start -- --model ... "<one-line
  five commands>"`):
  `~/.claude/projects/-home-li-primary/97dd44c9-5c10-429a-aed0-ef0eae02364e.jsonl`
- Case 2, mechanism 3 (multi-line brief via a pane-typed `claude "<prompt>"`
  shell command line):
  `~/.claude/projects/-home-li-primary/c216364d-6399-4882-8d01-a82985936cd4.jsonl`
- Case 3 (inlined `main-flow` skill text, no slash command), same delivery
  as mechanism 3:
  `~/.claude/projects/-home-li-primary/c402d22f-048e-4342-854a-ee8027e801dc.jsonl`
- Prior report referenced throughout:
  `/home/li/primary/flows/e51411/reports/multi-skill-first-prompt.md`
- Skill source inlined verbatim in case 3:
  `/home/li/primary/.claude/skills/main-flow/SKILL.md`
- Herdr commands used to create, prepare, drive, and close every disposable
  pane: `herdr pane split`, `herdr pane run` (to unset
  `CLAUDE_CODE_CHILD_SESSION` and to confirm the unset), `herdr agent
  start`, `herdr agent prompt --wait`, `herdr agent wait`, `herdr agent get`,
  `herdr pane read`, `herdr pane close`, `herdr pane list` (before and after,
  to confirm cleanup) — all invoked directly from this flow's own shell,
  never against any other flow's pane.
