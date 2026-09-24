# Multiple slash commands in one Claude Code prompt: which get expanded

## Question

When one prompt contains several `/skill` slash commands, does the harness
expand all of them into the model's context, or only the leading one? The
living says stacking several `/skill` commands in one prompt has worked for a
long time. Psyche Medium e51411 believed, untested, that only a leading
`/command` expands and the rest passes through as plain text.

## Method

Model: `claude-haiku-4-5-20251001`. Working directory: `/home/li/primary`
(so `.claude/skills/{spirit,psyche,behavior,herdr,main-flow}` are in scope).
Every prompt told the model explicitly not to call the Skill tool itself, so
any skill content that shows up in the transcript can only have entered
through harness slash-command expansion, never through a model-initiated
tool call. Every transcript below was checked for a `tool_use` block named
`Skill`; none was found in any of the four session files cited (`grep`/parse
for `"name":"Skill"` matches only the tool's schema listing inside the
`prompt_snapshot` system attachment, never an actual `tool_use`).

Witness is the session JSONL under
`~/.claude/projects/-home-li-primary/<session-id>.jsonl`. A slash command
that the harness itself expands shows up as a `user` entry containing
`<command-name>/x</command-name>` immediately followed by a second `user`
entry whose text begins `Base directory for this skill: .../.claude/skills/x`
— that second entry is the injected skill file content. Anything that does
not produce that pair, and instead appears only as literal prompt text (or
inside a `<pasted_content>` block), did not expand.

Two modes were tested:

1. **Headless**: `claude -p --model claude-haiku-4-5-20251001 "<prompt>" </dev/null`, run directly from the shell, stdin closed on every invocation.
2. **Interactive**: a herdr TUI session. A brand-new pane was split off from
   the current workspace with `herdr pane split --current --direction right
   --cwd /home/li/primary` (pane ids `wD:pG`, later recreated as `wD:pH`
   after the first pane inherited `CLAUDE_CODE_CHILD_SESSION=1` from this
   flow's own process and silently disabled its own transcript — that pane
   was closed with `herdr pane close` and a second one opened where
   `CLAUDE_CODE_CHILD_SESSION` was unset in the pane's shell first). A
   `claude --model claude-haiku-4-5-20251001` agent was started in that pane
   with `herdr agent start`, driven with `herdr agent prompt --wait`, read
   with `herdr agent read`, and the pane was closed with `herdr pane close`
   when done. No existing pane, seat, or flow was typed into, read from
   destructively, or otherwise touched; `herdr pane list` after cleanup shows
   only the panes that existed before this test.

## Case 1 — several commands on one line, non-`main-flow` leader

Prompt (headless and interactive, identical text):
```
/spirit /psyche /behavior Do not call the Skill tool yourself under any circumstances. Just reply with the single word OK when you are done reading whatever came before this sentence.
```

**Headless** (`claude -p`), transcript
`~/.claude/projects/-home-li-primary/ce59348f-1047-47f5-810c-25ea59f20690.jsonl`:
- `/spirit` expanded: yes — `<command-name>/spirit</command-name>` followed by the injected `spirit` skill body.
- `/psyche` expanded: no — appears only inside `<command-args>/psyche /behavior Do not call the Skill tool ...</command-args>`, i.e. as literal text tacked onto the `/spirit` invocation's arguments.
- `/behavior` expanded: no — same `<command-args>` literal text, never injected.
- Assistant's only reply: `OK`. No `Skill` tool_use anywhere in the file.

**Interactive** (herdr pane, session
`e400ecb6-e75f-4c6a-898b-aebb1b544010.jsonl`, lines 8–24):
- `/spirit` expanded: yes.
- `/psyche` expanded: **yes** — its own `<command-name>/psyche</command-name>` / `<command-args>Do not call the Skill tool...</command-args>` pair, followed by the injected `psyche` skill body.
- `/behavior` expanded: **yes** — same pattern, injected `behavior` skill body.
- The pane's rendered scrollback shows this literally as three separate `❯` prompt blocks, each repeating the trailing instruction text, then a single `● OK` — i.e. the interactive input line was split into three separate slash-command submissions before the model ever answered.

This single case already disconfirms both starting beliefs at once, depending on mode: headless confirms "only the leading command expands, the rest is literal"; interactive flatly contradicts it — all three expanded.

## Case 2 — `/main-flow` leads, other slash commands and brief text follow, one line

Prompt:
```
/main-flow /herdr /spirit Do not call the Skill tool yourself under any circumstances. Just reply with the single word OK when done.
```

**Headless**, transcript `d12c0254-cfd0-4d9f-bc7a-1d6f1ac11950.jsonl`:
- `/main-flow` expanded: yes.
- `/herdr` expanded: no — literal text inside `/main-flow`'s `<command-args>`.
- `/spirit` expanded: no — same, literal text inside the `<command-args>`.

**Interactive**, same herdr session, lines 54–61:
- `/main-flow` expanded: yes.
- `/herdr` expanded: **yes** — its own command-name/command-args pair, injected `herdr` skill body.
- `/spirit` expanded: **yes** — its own pair, injected `spirit` skill body.
- Pane scrollback again shows three separate `❯` blocks followed by one `● OK`.

Same pattern as case 1: headless expands only the leader; interactive expands every space-separated `/command` on the line.

## Case 3 — slash commands on separate lines, in the middle of a longer prompt

Prompt (real newlines):
```
Here is some context before anything.
/spirit
/behavior
Now here is more text placed in the middle of the prompt.
/psyche
Do not call the Skill tool yourself under any circumstances. Just reply with the single word OK when done.
```

**Headless**, transcript `38824c2b-44ac-46a5-9460-82dd2720aef1.jsonl`:
- `/spirit` expanded: no.
- `/behavior` expanded: no.
- `/psyche` expanded: no.
- The entire prompt (including all three `/word` lines) appears verbatim as one plain `user` text message. No `<command-name>` entry at all. Only `attachment` entries (environment/system-reminder metadata) surround it — no skill content anywhere.

This shows headless expansion requires the `/command` to be the very first characters of the whole submitted string; a `/command` that isn't in first position, even alone on its own line, is never recognized, headless.

**Interactive**, same herdr session, lines 67–70:
- `/spirit` expanded: no.
- `/behavior` expanded: no.
- `/psyche` expanded: no.
- The whole thing lands as a single literal block wrapped as
  `<pasted_content id="894e">...</pasted_content>`. The herdr pane's status
  line explicitly read "paste again to expand" afterward, and the rendered
  scrollback showed the multi-line block as one grey/quoted paste rather than
  as separate `❯` command entries — i.e. Claude Code's terminal input
  recognized this multi-line block as a bracketed paste and treated it as
  opaque pasted text, not as command input, so none of the embedded
  `/spirit`, `/behavior`, `/psyche` tokens were parsed as commands at all,
  including the ones that would have been "first" on their own line.

So the interactive multi-command expansion seen in cases 1–2 is specific to
a single line of typed/submitted text containing multiple space-separated
`/command` tokens — it does not generalize to slash commands placed on their
own lines inside a multi-line submission, which the terminal instead treats
as a single opaque paste.

## Summary of findings

| Case | Mode | Skill(s) tested | Expanded? |
|---|---|---|---|
| 1: `/spirit /psyche /behavior ...` one line | headless `-p` | spirit / psyche / behavior | yes / no / no |
| 1: same | interactive | spirit / psyche / behavior | yes / yes / yes |
| 2: `/main-flow /herdr /spirit ...` one line | headless `-p` | main-flow / herdr / spirit | yes / no / no |
| 2: same | interactive | main-flow / herdr / spirit | yes / yes / yes |
| 3: commands on separate lines mid-prompt | headless `-p` | spirit / behavior / psyche | no / no / no |
| 3: same | interactive | spirit / behavior / psyche | no / no / no (submitted as one opaque paste block) |

No `Skill` tool_use call appears in any of the four transcript files
(`ce59348f-...`, `d12c0254-...`, `38824c2b-...`, `e400ecb6-...`); every
expansion witnessed above is the harness's own `<command-name>` /
`<command-args>` injection mechanism, not a model-initiated tool call.

**Disconfirmation of Psyche Medium e51411's belief** (only a leading
`/command` expands, the rest is literal): true for headless `claude -p`, but
false for the interactive harness — in interactive mode, every
space-separated `/command` token on a single submitted line expanded
independently (cases 1 and 2), each injecting its own skill body before the
model's single turn began.

**Bearing on the living's claim** (stacking several `/skill` commands in one
prompt has worked for a long time): supported only for the interactive
harness with all commands packed onto one line. It is not supported for
headless `-p` runs, and it is not supported for commands spread across
separate lines even interactively — those become one opaque pasted block and
none of the embedded commands expand, including the first.

## Uncertainties and caveats

- Only one interactive frontend was tested: a herdr-hosted pane driving
  `claude` via `herdr agent start` / `herdr agent prompt`. This delivers text
  to the pane's PTY; it was not verified whether a human typing the same
  multi-command line character-by-character (rather than having it delivered
  in one shot by `herdr agent prompt`) produces identical splitting, though
  the resulting transcript pattern (three separate `<command-name>` entries,
  three separate rendered `❯` blocks) is the same shape the interactive CLI
  itself produces for genuinely typed slash commands elsewhere in this
  project's session history, so this is judged to reflect Claude Code's own
  interactive slash-command parser rather than an herdr-specific artifact —
  but it was not cross-checked against a manually-typed control.
- The first interactive pane (`wD:pG`) silently produced no transcript file
  because it inherited this flow's own `CLAUDE_CODE_CHILD_SESSION=1`
  environment variable; that pane's on-screen result (visually identical
  three-block splitting) was discarded in favor of the second pane
  (`wD:pH`/session `e400ecb6-...`) where the variable was unset first and a
  transcript was produced. This confirms the harness's transcript-disable
  behavior for nested Claude Code invocations, an incidental finding not
  otherwise part of this question.
- Not tested: three or more skills on one line beyond three, skills mixed
  with `--` style flags, or a leading command whose own argument text itself
  contains a literal `/` that could be misparsed. Not tested: whether the
  headless `<command-args>` literal text, if it itself begins a fresh
  headless invocation, would then expand (out of scope — this only concerns
  one prompt, one invocation).

## Sources

- Headless case 1: `~/.claude/projects/-home-li-primary/ce59348f-1047-47f5-810c-25ea59f20690.jsonl`
- Headless case 2: `~/.claude/projects/-home-li-primary/d12c0254-cfd0-4d9f-bc7a-1d6f1ac11950.jsonl`
- Headless case 3: `~/.claude/projects/-home-li-primary/38824c2b-44ac-46a5-9460-82dd2720aef1.jsonl`
- Interactive cases 1–3 (one continuous herdr-hosted session): `~/.claude/projects/-home-li-primary/e400ecb6-e75f-4c6a-898b-aebb1b544010.jsonl`
- Skill sources referenced: `/home/li/primary/.claude/skills/{spirit,psyche,behavior,herdr,main-flow}`
- Herdr commands used to create, drive, and close the disposable interactive pane: `herdr pane split`, `herdr agent start`, `herdr agent prompt --wait`, `herdr agent read`, `herdr pane close` (invoked directly from this flow's own shell, not against any other flow's pane).
