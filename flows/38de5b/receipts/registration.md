# Herdr messaging registration

Witness by Psyche Fable 38de5b, 2026-09-25.

## Method

Read `flows/e51411/witnesses/astra-registration.md` and `tools/hacky-messenger/README.md`/`hm.py`
(under the `messaging` / `testing-session-registry` skills) for the exact `hm-register`
invocation used on this cluster. Determined this flow's Herdr agent name and native
thread from `herdr agent list`, matching `agent_session.value` against
`$CLAUDE_CODE_SESSION_ID = 38de5bbb-be48-4bae-883e-2d622fb79c9e`: pane `wD:pR`, name
`psyche-fable-refresh-5f38bc`, terminal `term_65c500aa730757c`, session `messaging-build`.

## Blocker encountered and cleared

At first read, `herdr agent get wD:pR` showed `launch_pending: true` and no
`interactive_ready` field (matching the brief's expectation that this Herdr omits
`interactive_ready`). A first `hm-register ... --readiness-probe` attempt was refused
before the probe could run:

```
$ FLOW_ID=38de5b hm-register 38de5b psyche-fable-refresh-5f38bc --session messaging-build \
    --native-thread 38de5bbb-be48-4bae-883e-2d622fb79c9e \
    --readiness-probe HM_READY_38de5b_20260925_1508 \
    --rollout /home/li/.claude/projects/-home-li-primary/38de5bbb-be48-4bae-883e-2d622fb79c9e.jsonl

hm: {"error":{"code":"agent_not_ready","message":"agent wD:pR is not an active named agent"},"id":"cli:agent:prompt"}
```

`herdr agent explain wD:pR` showed state `working`, rule `osc_title_working`, evidence
`"◐ Psyche Fable 38de5b"`. The refusal was `launch_pending: true`, a distinct Herdr
flag from `interactive_ready`; a bounded background poll (32 checks, 3s apart, ~96s)
of `herdr agent get wD:pR` showed it clear to unset and `interactive_ready` flip to
`true` on its own (no action taken on it by this flow). At that point the readiness
probe was no longer needed.

## Registration

```
$ FLOW_ID=38de5b hm-register 38de5b psyche-fable-refresh-5f38bc --session messaging-build \
    --native-thread 38de5bbb-be48-4bae-883e-2d622fb79c9e

Registered 38de5b: psyche-fable-refresh-5f38bc (messaging-build)
```
Exit 0.

## Readback

`~/.local/state/hacky-messenger/38de5b.json`:
```json
{"session": "messaging-build", "name": "psyche-fable-refresh-5f38bc", "pane_id": "wD:pR", "terminal_id": "term_65c500aa730757c", "agent": "claude", "native_thread": "38de5bbb-be48-4bae-883e-2d622fb79c9e"}
```

`hm-list`:
```
FLOW	AGENT	SESSION	STATE
38de5b	psyche-fable-refresh-5f38bc	messaging-build	working
```

`herdr agent get wD:pR` (title readback, taken after registration):
```
terminal_title_stripped: Psyche Fable 38de5b
name: psyche-fable-refresh-5f38bc
```

The read-back title is exactly `Psyche Fable 38de5b`, matching the required title
verbatim.
