# Seat receipt — Psyche Opus 077114 (successor of b87854)

Launched by a subflow of Psyche Medium b87854, because b87854 itself could not
persist (`flows/b87854/handover.md`, `flows/b87854/receipts/remote-title.md`).

## Identity

- Flow ID: `flow-id claude --flows-root /home/li/primary/flows --parent-session 077114f4-2c00-473c-9c77-5f0a948766f2` → `077114`.
- Claude session uuid: `077114f4-2c00-473c-9c77-5f0a948766f2`; pid `3055457`.
- Herdr: session `messaging-build`, workspace `wD`, tab `wD:tM`, pane `wD:pY`,
  terminal `term_65c588e0314a38b`. The tab was created fresh with
  `herdr --session messaging-build tab create --workspace wD --cwd /home/li/primary --no-focus`,
  next to b87854's tab `wD:tF`. No existing pane was split, moved or closed.
- Herdr agent name: `herdr --session messaging-build agent rename wD:pY psyche-opus-077114`.

## Startup prompt

`flows/b87854/refresh-inject.md` — one line, no hashes, so that Claude Code's
interactive parser sees it as command input rather than an opaque paste
(`flows/e51411/reports/one-block-startup-prompt.md`,
`flows/e51411/reports/multi-skill-first-prompt.md`).

## Launch

The Herdr server itself carries the child-session markers, so the new pane's
plain shell inherited them:

    herdr --session messaging-build pane run wD:pY 'echo MARKERS child=${CLAUDE_CODE_CHILD_SESSION:-none} sid=${CLAUDE_CODE_SESSION_ID:-none} cpid=${CLAUDE_PID:-none}'
    MARKERS child=1 sid=108ab020-3394-4fe2-8ae3-304ea1d20843 cpid=2883797

They were cleared in the pane's shell first, and then again on the exec line:

    herdr --session messaging-build pane run wD:pY 'unset CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_SESSION_ID CLAUDE_PID; echo CLEARED child=${CLAUDE_CODE_CHILD_SESSION:-none} sid=${CLAUDE_CODE_SESSION_ID:-none} cpid=${CLAUDE_PID:-none}'
    CLEARED child=none sid=none cpid=none

    herdr --session messaging-build pane run wD:pY 'env -u CLAUDE_CODE_CHILD_SESSION -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PID CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 claude --model claude-opus-5-5 --effort medium --remote-control --dangerously-skip-permissions "$(< /home/li/primary/flows/b87854/refresh-inject.md)"'

`/proc/3055457/environ` carries no `CLAUDE_CODE_CHILD_SESSION`, no
`CLAUDE_CODE_SESSION_ID` and no `CLAUDE_PID`; it does carry
`CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1`. So the child markers reached neither
the pane's shell nor the claude process.

## Persistence — verified

- `~/.claude/sessions/3055457.json` exists: `sessionId` `077114f4-…`,
  `kind` `interactive`, `version` `2.1.280`,
  `bridgeSessionId` `session_01Wy3PhKVz8KEtd35fYULSxt`.
- Transcript `~/.claude/projects/-home-li-primary/077114f4-2c00-473c-9c77-5f0a948766f2.jsonl`
  exists and grew across the session: 331454 → 345066 → 762675 → 796231 bytes.

Both were absent for b87854. The `nested_marker` suppression is gone.

## Skills — the stacked-command limit

The 20 launch skills do **not** all expand from one submission. Claude Code
2.1.280 prints, on screen:

    Stacked command limit (5) reached — remaining input passed as arguments

Six expanded at launch — `/spirit`, `/psyche`, `/main-flow`,
`/psyche-interraction`, `/flow-aspect`, `/behavior` — each with the brief
attached as its `<command-args>` / `ARGUMENTS` tail, so the brief itself
arrived intact and complete. The other fourteen arrived as literal argument
text and injected no skill body.

This is a limit neither `flows/e51411/reports/multi-skill-first-prompt.md` nor
`flows/e51411/reports/one-block-startup-prompt.md` could have seen: both tested
five commands or fewer.

The remaining fourteen were then loaded as three further one-line submissions
of five, four and five commands. Batch 3 was submitted once while the seat was
still working and never appeared in the transcript; re-submitted once the seat
was idle, it expanded. All twenty `<command-name>` entries with their injected
`Base directory for this skill:` bodies are now present in the transcript.

**Consequence for the next launcher:** a one-line startup prompt carries at most
five or six skills. The rest must follow as further single-line submissions of
five, sent after the seat is idle.

## Title

    herdr --session messaging-build agent prompt wD:pY '/rename Psyche Opus 077114'

Readbacks:

- `~/.claude/sessions/3055457.json` → `"name":"Psyche Opus 077114"`,
  `"nameSource":"user"`, `"formerNames":[{"name":"PsycheV2.{ Sonnet 9c7514 }", …}]`,
  `bridgeSessionId` present — so the name reached the registry record and the
  Remote Control bridge, which is exactly what b87854 could not do.
- `herdr --session messaging-build pane get wD:pY` →
  `terminal_title_stripped: "Psyche Opus 077114"`.

### Sibling panes: two titles did change

Before the rename, three panes all displayed `PsycheV2.{ Sonnet 9c7514 }`:
`wD:pQ` (b87854), `wD:pW` (9c7514), `wD:pY` (this seat, whose name was derived
from the pane title at startup with `nameSource: "peer"`). After the rename all
three read `Psyche Opus 077114`.

Unchanged: `wD:p8`, `wD:p9`, `wD:pD` (d8df70), `wD:pF` (e51411), `wD:pR`
(38de5b), `w17:p1` (88475f).

So the repaint followed the former name, not the pane: every terminal showing
`PsycheV2.{ Sonnet 9c7514 }` was repainted with the new one. This is the same
cross-session hazard `flows/b87854/receipts/remote-title.md` documented and that
`tools/canonical-title-alignment.mjs` already refuses to apply for Claude —
here observed in the opposite direction. `wD:pQ` and `wD:pW` were already
mistitled before this rename; they are now mistitled differently. Neither was
prompted or touched: the brief forbids sending to `wD:pQ`, so no corrective
`/rename` was injected there. A freshly created pane also came up already
painted `Psyche Opus 077114`, which shows the repaint is a live name-sync and
not a one-shot.

## Registration — blocked, not faked

    hm-register --session messaging-build --native-thread 077114f4-2c00-473c-9c77-5f0a948766f2 077114 psyche-opus-077114
    messenger-clj: Agent is not interactively ready

`herdr --session messaging-build agent get wD:pY` carries no `interactive_ready`
key at all. `hm-list` shows the seat as `-  psyche-opus-077114  messaging-build
done` — visible as a live agent, with no Flow route bound.

### Cause found, and witnessed

`interactive_ready` is not a property of the harness or the model. It is set by
Herdr when Herdr itself starts the agent and observes it reach an interactive
prompt. It is absent for any agent whose process was typed into the pane's own
shell, however healthy that agent is.

Witness, with a disposable pane created and closed for the purpose (`wD:pZ` /
tab `wD:tN`, opened with `tab create`, closed with `pane close`; `pane list`
before and after differ only by that pane):

    herdr --session messaging-build agent start hm-probe-test --kind claude --pane wD:pZ --timeout 120000 -- --model claude-haiku-4-5-20251001
    → "interactive_ready":true, "name":"hm-probe-test"

The same field is `true` on `w17:p1` (88475f), which `flows/88475f/log.md`
records as registered — and 88475f was started through the launcher, not typed
into a shell. b87854, e51411's own reports, and this seat were all typed in.

So `flows/b87854/receipts/seat.md`'s conclusion — that Claude seats on this
Herdr endpoint can never report `interactive_ready`, and that `hm.py`'s
Codex-shaped `--rollout` is the only other door — is **too strong**. A Claude
seat does report it, when Herdr starts it.

**Fix for the next launch:** put the pane at a clean shell prompt with the child
markers unset, then start the seat with

    herdr --session messaging-build agent start psyche-opus-<ID> --kind claude --pane <PANE> \
      --executable <wrapper that does `exec env -u CLAUDE_CODE_CHILD_SESSION -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PID CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 claude "$@"`> \
      -- --model claude-opus-5-5 --effort medium --remote-control --dangerously-skip-permissions "<the one-line prompt>"

`herdr agent start` refuses an argument containing a raw newline
(`invalid_agent_argument`), which is a further reason the startup prompt must be
one line. It was not used for this launch because the `interactive_ready`
dependency was only established afterwards.

Registering `077114` was not forced: no rollout file was fabricated and no
registry JSON was hand-written. The seat is **not** registered in
`~/.local/state/hacky-messenger/`. Re-launching it through `herdr agent start`
would make it registrable, at the cost of discarding the orientation and the
state presentation it has already given the living; that is the living's or the
main flow's call, not this subflow's.

## Seat state at handover

Orientation completed and the current state presented to the living in `wD:pY`.
Ends its turn with the open questions it is waiting on; `agent_status: done`,
registry `status: idle`, context 11%.
