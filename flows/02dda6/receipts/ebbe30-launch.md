# ebbe30 launch receipt

Quaternary 02dda6 launched Psyche Primary Fable ebbe30 on 2026-10-07.

## Retained worktree

- Path: `/tmp/claude-1001/-home-li-primary/02dda640-dc5f-46ed-9c70-f22f047db2d4/scratchpad/pub`
- Detached at origin/main `b58610ce540c7eae2e65e4c966c06b99b1755ef3`, a descendant of `53f1f71d2862469ba3f631d6d03cd1aee3e4173c`.
- Live dependency: the seat's UserPromptSubmit reminder hook re-reads the system prompt below. The worktree is retained for ebbe30's full live lifetime; 02dda6 owns its lifecycle.

## Command

Run from the worktree root:

```
node tools/claude-main-flow-launch.mjs \
  --brief ../brief.txt \
  --layer Primary --aspect Psyche \
  --effort medium \
  --workspace /home/li/primary \
  --system-prompt-file \
    tools/main-flow-mode/system-prompt.md
```

- Brief file: `/tmp/claude-1001/-home-li-primary/02dda640-dc5f-46ed-9c70-f22f047db2d4/scratchpad/brief.txt` (the Mind-supplied brief, verbatim).
- System prompt passed (resolved): `/tmp/claude-1001/-home-li-primary/02dda640-dc5f-46ed-9c70-f22f047db2d4/scratchpad/pub/tools/main-flow-mode/system-prompt.md`
- Settings: `/home/li/.claude/jobs/native-ebbe3021-295e-4d65-9564-2ad57da817e8/main-flow-settings.json`
- Exit 0; every launcher step passed.

## Seat

- Profile: `claude-fable-5-1`, effort medium (selectVoiceProfile: existing chosen launch).
- Session: `ebbe3021-295e-4d65-9564-2ad57da817e8`
- Transcript: `/home/li/.claude/projects/-home-li-primary/ebbe3021-295e-4d65-9564-2ad57da817e8.jsonl`
- Flow dir: `/home/li/primary/flows/ebbe30`
- Title: `Psyche.{ Fable ebbe30 }` (transcript and Herdr terminal title)
- Herdr: session default, workspace w1, tab w1:t27, pane w1:p2M
- Agent: `psyche_primary_ebbe30`, bound to the session id
- hm-register: `Registered ebbe30: psyche_primary_ebbe30 (default)`; hm-list: `working`
- Bridge: https://claude.ai/code/session_01VhRJSAnxwrzmwP8GBeDvYM
- Transcript: every assistant row `claude-fable-5-1`, effort and perTurnEffort medium; 18 skills in 3 batches, each answered `READY`; brief accepted once.

## Hash checks

- Launcher `tools/claude-main-flow-launch.mjs`: `aea193a6f23a52d51ffcdfbe26e8a1bdb44d41c5d317d2aabd1a2b6265ae9704` in shared tree, 53f1f7 and worktree: match.
- model-display-name, native-voice-profiles, native-main-flow-launch-shared, standing-skill-selection, reminder-hook.py: shared tree and origin/main match.
- System prompt: worktree (published) `255ceceebb919b2b405df15e09f3b7c9775d1a87e809ae215632927082c8424d`; shared tree `aa9147b43390373bcdcaf7c84793d04c290bbcc6460a591f116834dc13865930` (unpublished edit): mismatch, so the published one was passed.

## Sources

- Launcher output: `/tmp/claude-1001/-home-li-primary/02dda640-dc5f-46ed-9c70-f22f047db2d4/scratchpad/launch.log`
- Native transcript above; `herdr pane list`; `hm-list`.
- Provenance receipt handle: unavailable.
