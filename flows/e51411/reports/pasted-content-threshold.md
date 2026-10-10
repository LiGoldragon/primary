# The `<pasted_content id=...>` wrap: length OR line count, either alone sufficient

## Question

When Herdr's `herdr agent prompt` delivers text into an interactive Claude
Code session, what exactly makes Claude wrap it as `<pasted_content
id=...>` rather than plain user text? Is it a newline, the length, or both?
What is the length threshold?

## Method

Model: `claude-haiku-4-5-20251001`, `--dangerously-skip-permissions`,
`CLAUDE_CODE_CHILD_SESSION` confirmed unset before launch (`echo
READY_${CLAUDE_CODE_CHILD_SESSION:-none}` printed `READY_none`) so the child
session wrote its own transcript. One disposable pane, `wD:pS`, created with
`herdr pane split --current --direction right --cwd /home/li/primary` from
this flow's own pane, closed with `herdr pane close wD:pS` at the end.
`herdr pane list` before and after matched exactly except for `wD:pS`
itself; no other pane, seat, or flow was touched.

The model was told once, "whenever you receive a message, reply with only
the word OK and nothing else" (it complied for a few turns, then began
refusing after the 4-line case — irrelevant to the mechanical finding, since
what is being read is the *user*-turn content in the transcript, not the
assistant's reply).

Witness: session transcript
`~/.claude/projects/-home-li-primary/30a92230-2a8e-4527-a824-a09071e1ed19.jsonl`.
Each user turn's `message.content` was checked for the literal string
`pasted_content`. Every text sent was tagged with a unique marker (e.g.
`L801:xxx...`, `M4L0:aaa...`) so it could be found unambiguously in the
transcript regardless of wrapping.

Single-line texts of 600, 700, 750, 800, 850, 900 characters were sent via
`herdr agent prompt wD:pS "<text>" --wait`, then the boundary was bisected
(825, 812, 806, 803, 802, 801) down to the exact single-character crossover.
Two short multi-line texts (2 lines of 40 characters each; 5 lines of ~25
characters each) were sent the same way, then 3-line and 4-line variants
were added once the first two showed line count itself might matter. A
900-character single line was also sent via `herdr agent send-keys wD:pS
<char> <char> ... enter` (one shell argument per character, built with
Python; `send-keys` rejected the whole string as one argument with
`invalid_key`, confirming it only accepts single keys/characters, not a
text blob, as one token).

## Results

| Text | Length (chars) | Lines | Mechanism | Result |
|---|---|---|---|---|
| `L600:xxx...` | 600 | 1 | `agent prompt` | plain |
| `L700:xxx...` | 700 | 1 | `agent prompt` | plain |
| `L750:xxx...` | 750 | 1 | `agent prompt` | plain |
| `L800:xxx...` | 800 | 1 | `agent prompt` | **plain** |
| `L801:xxx...` | 801 | 1 | `agent prompt` | **wrapped** |
| `L802:xxx...` | 802 | 1 | `agent prompt` | wrapped |
| `L803:xxx...` | 803 | 1 | `agent prompt` | wrapped |
| `L806:xxx...` | 806 | 1 | `agent prompt` | wrapped |
| `L812:xxx...` | 812 | 1 | `agent prompt` | wrapped |
| `L825:xxx...` | 825 | 1 | `agent prompt` | wrapped |
| `L850:xxx...` | 850 | 1 | `agent prompt` | wrapped |
| `L900:xxx...` | 900 | 1 | `agent prompt` | wrapped |
| `M2A:.../M2B:...` | 81 (incl. `\n`) | 2 | `agent prompt` | plain |
| `M3L0../M3L2..` | ~76 | 3 | `agent prompt` | plain |
| `M4L0../M4L3..` | ~103 | 4 | `agent prompt` | **wrapped** |
| `M5L0../M5L4..` | 129 | 5 | `agent prompt` | wrapped |
| `SK900:xxx...` | 900 | 1 | `send-keys` (per-character keys + `enter`) | wrapped, arrived intact |

## The rule

Either condition alone is sufficient to trigger the `<pasted_content
id="...">` wrapper in Claude Code's interactive input line — it is length
**or** newline count, not a combination requirement:

- **Length**: a single-line submission wraps once it exceeds **800
  characters**. 800 characters stayed plain; 801 wrapped. The threshold is
  exactly 800/801, not merely "within 10" of it.
- **Line count**: a submission of **4 or more lines** wraps regardless of
  how short each line is (a 4-line, 103-character text wrapped; a 3-line,
  76-character text and a 2-line, 81-character text both stayed plain).
- **Mechanism-independent**: the same rule holds whether the text is typed
  through `herdr agent prompt` (which writes to the PTY as one submission)
  or through `herdr agent send-keys` sending the same 900 characters as 900
  separate single-character key arguments followed by `enter` — the latter
  arrived as `<pasted_content id="ea2f">` too, with the full 900-character
  payload intact inside the wrapper (verified as a 958-character
  `message.content` string, the extra bytes being the wrapper tag and
  surrounding newlines). Note: submitting a large `send-keys` burst needed
  two `enter` presses — the pane's compose box showed `[Pasted text #11 +1
  lines]` (still uncommitted) after the first `enter`, and only the second
  `enter` actually sent the turn — consistent with Claude Code's terminal
  input layer treating a fast burst of keystrokes as a paste event the same
  way it treats a single multi-line `agent prompt` write, independent of
  which herdr primitive produced the keystrokes.
- Every message this session sent was, by construction, single-block
  (either one line or delivered as one shell argument), so this cannot
  distinguish "line count" from "any embedded control byte" as the multi-
  line trigger — only line count (1–5 lines) was varied, not other control
  characters.

## Sources

- Transcript for all cases above:
  `~/.claude/projects/-home-li-primary/30a92230-2a8e-4527-a824-a09071e1ed19.jsonl`
- Pane: `wD:pS`, created by `herdr pane split --current --direction right
  --cwd /home/li/primary` from this flow's own pane, closed with `herdr
  pane close wD:pS`; `herdr pane list` before and after matched except for
  this one pane.
- Prior method reference: `flows/e51411/reports/one-block-startup-prompt.md`.
- Herdr commands used: `herdr pane split`, `herdr pane run` (env unset and
  confirmation), `herdr agent get`, `herdr agent prompt --wait`, `herdr
  agent send-keys`, `herdr agent wait`, `herdr pane read`, `herdr pane
  close`, `herdr pane list` (before and after).
