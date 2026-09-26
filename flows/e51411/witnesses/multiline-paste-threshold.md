# Claude Code multi-line input wrapping threshold — 2026-09-25

## Method

Created a disposable Herdr pane (never used by any live flow), split off
the current pane (`herdr pane split --current --direction right`), and in
it unset `CLAUDE_CODE_CHILD_SESSION` and `CLAUDE_JOB_DIR` before starting
a fresh interactive session with
`herdr agent start disposable-haiku-test --kind claude --pane <id> --
--model claude-haiku-4-5-20251001 --dangerously-skip-permissions`. cwd
was `/tmp`, so the session's transcript lives under
`~/.claude/projects/-tmp/c17b2de4-1233-4591-b477-eaf16af89b05.jsonl`.

For each case, one `herdr agent prompt <pane> "<text>"` call submitted a
single multi-line string as a fresh prompt (never appended to a prior
one). The text always began with the instruction "If the text you are
reading right now arrived inside pasted_content tags, reply with exactly
one word: WRAPPED. Otherwise reply with exactly one word: PLAIN. Say
nothing else.", padded with literal `x` characters on the same first
line, followed by additional all-`x` lines, so each line hit an exact
target character count and the total line count matched the case.

Each result was confirmed two ways: (1) Haiku's own printed answer, and
(2) inspecting the corresponding `user`-role record in the session's
transcript JSONL for a literal `<pasted_content id="...">...
</pasted_content id="...">` wrapper around the submitted text (a plain
non-wrapped submission has that exact string as its `message.content`
verbatim, with no `pasted_content` tag). Both signals agreed on every
case below. The pane was closed afterward (`herdr pane close <id>`); no
existing flow or pane was touched.

## Table

| Case | Lines | Chars/line | Total chars | Haiku said | Transcript shows `<pasted_content>` | Verdict |
|---|---|---|---|---|---|---|
| (a) | 2 | 800 | 1601 (1659 w/ wrapper tags) | WRAPPED | yes | WRAPPED |
| (b) | 3 | 800 | 2402 (2460 w/ wrapper tags) | WRAPPED | yes | WRAPPED |
| (c) | 3 | 300 | 902 (960 w/ wrapper tags) | WRAPPED | yes | WRAPPED |
| (d) | 3 | 1200 | 3602 (3660 w/ wrapper tags) | WRAPPED | yes | WRAPPED |
| (e) | 2 | 1200 | 2401 (2459 w/ wrapper tags) | WRAPPED | yes | WRAPPED |

(Prior, already-known baseline, not re-tested here: 1 line of ≤800 chars
arrives plain; 1 line of 801 chars is wrapped; 4+ lines are wrapped at
any length.)

## Conclusion — the exact rule

Line count alone decides wrapping once there is more than one line:
**any input of 2 or more lines is wrapped in `<pasted_content>`,
regardless of how long or short each line is.** This was true down to
300-char lines (900 chars total, case c), well under the 800-char
single-line threshold, and held equally at 800 and 1200 chars/line and
at both 2 and 3 total lines. There is no separate "long line" carve-out
for 2- or 3-line inputs — the per-line-length threshold (≤800 plain,
>800 wrapped) applies **only** to single-line (1-line) input. The
combined rule across all now-known cases:

- 1 line, ≤800 chars: plain.
- 1 line, >800 chars: wrapped.
- 2+ lines, any length per line: wrapped.
