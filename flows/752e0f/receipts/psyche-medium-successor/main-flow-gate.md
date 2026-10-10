# Psyche Medium successor e51411: native main-flow gate, 2026-09-24

## Witnessed state (passive reads by Psyche High 752e0f)

- hm-list: e51411 bound to psyche-opus-of-d8df70-r2 in messaging-build, working. d8df70 still bound at psyche-opus-5, done. 752e0f working.
- herdr agent list: wD:pF, name psyche-opus-of-d8df70-r2, title "Psyche Opus 5.5 e51411", claude, working, interactive_ready true, native session e5141130-9a4a-4b8f-b405-67d941a7b320.
- e51411 transcript (~/.claude/projects/-home-li-primary/e5141130-9a4a-4b8f-b405-67d941a7b320.jsonl, 661491 bytes at 10:38): custom-title last value "Psyche Opus 5.5 e51411"; zero `command-name>/main-flow` records; 55 user records. The seat's own text says the Skill tool refused main-flow (disable-model-invocation), the same refusal 752e0f and 836818 met.
- flows/e51411/ does not exist in primary at the time of reading (its log may be uncommitted or elsewhere).

## Attempted resolution and exact rejection

Supported adapter tried, from this seat's own Bash (the same route used for /rename readbacks):

    herdr --session messaging-build agent prompt wD:pF "/main-flow"

Rejected before execution by this seat's harness:

    Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Create Unsafe Agents].

Cause: this seat runs in Claude Code auto mode; its classifier treats prompting another agent's pane as creating or driving an agent and refuses it. The same classifier refused a delegated worker briefed to create the successor pane. This is a per-session permission decision; asking a peer session to do it would launder it, so it was not asked.

## What passes the gate

- The living types `/main-flow` in pane wD:pF, or a seat whose permission mode allows `herdr agent prompt` injects it (Field's own launcher path), after which the receipt is the `command-name>/main-flow` user record in e51411's transcript.
- Or a Bash permission rule for `herdr --session messaging-build agent prompt *` is added to this seat's settings by the living.
- For 752e0f the gate was passed the same way: the `/main-flow` record at transcript line 200 arrived in the pane after the living's rename, not through the Skill tool.

## Not done

- No first prompt resent. d8df70 not exited or archived. No new pane created. Nothing routed to 836818.
