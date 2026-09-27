# Native title set — 8904b10d-7f06-4e44-9342-3a8a2d7e17bd

Method: read-only claim check, then `herdr agent prompt w1:p8 "/rename PsycheV2.{ Fable 8904b1 }"`,
then readback via `herdr agent get w1:p8` and the session's own JSONL transcript.

## Claim check

`flows/.8904b1.flow-id` (read-only):

    version=1
    harness=claude
    identity=8904b10d7f064e4493423a8a2d7e17bd
    alias=8904b1
    uuid-version=uuid-v4

`identity` matches session UUID `8904b10d-7f06-4e44-9342-3a8a2d7e17bd` with dashes stripped; `alias` matches
Flow ID `8904b1`. Witnessed directly by reading the file; no entry for this pair was found in
`sessions/index.md` or `flows/index.md`, only in the dedicated claim-marker file itself.

## Model-display map

`config/model-display-names.json`: `"claude-fable-5-1": "Fable"`. Confirmed for the exact identifier
`claude-fable-5-1` (also present, separately, as `claude-fable-5-1[1m]`, unused here).

## Target identification

`herdr agent list` showed exactly one agent with `agent_session.value == 8904b10d-7f06-4e44-9342-3a8a2d7e17bd`:
pane `w1:p8`, terminal `term_65c6b8fc88ee08`, tab `w1:t6`, cwd `/home/li/wt/primary/56ae53`. Unambiguous.

## Mechanism

`herdr agent prompt w1:p8 "/rename PsycheV2.{ Fable 8904b1 }"` — Claude Code's native `/rename` slash
command, delivered through Herdr's supported Claude integration (the same primitive
`tools/claude-native-seat-refresh.py` uses for title finalization). This is the only supported
title-write path for this harness; it acted on the existing session only, no new session/pane/seat
was created.

## Readback

Herdr readback (`herdr agent get w1:p8`), immediately after:

    "terminal_title": "◑ PsycheV2.{ Fable 8904b1 }",
    "terminal_title_stripped": "PsycheV2.{ Fable 8904b1 }"

Native transcript readback (session JSONL, `type":"custom-title"` record):

    {"type":"custom-title","customTitle":"PsycheV2.{ Fable 8904b1 }","sessionId":"8904b10d-7f06-4e44-9342-3a8a2d7e17bd"}

Also present, in the same transcript, the CLI's own local-command echo:

    <local-command-stdout>Session renamed to: PsycheV2.{ Fable 8904b1 }</local-command-stdout>

Both readbacks equal `PsycheV2.{ Fable 8904b1 }` exactly (the `terminal_title` field carries a leading
spinner glyph that is not part of the stored title; `terminal_title_stripped` and the transcript
`customTitle` carry the bare string).

## Power / model alongside

`herdr agent get` reported `agent_status: "working"` (this subflow's own turn was in flight) and
`agent: "claude"`; no separate power or model field is emitted by this call. No power declaration was
requested or made as part of this action.

## Left undone / ambiguous

Nothing. The rename was accepted and processed synchronously (as a local CLI command, not queued
behind the busy model turn), so an in-session readback was possible despite the pane showing
`agent_status: working` throughout.

## Sources

- `/home/li/wt/primary/56ae53/flows/.8904b1.flow-id`
- `/home/li/wt/primary/56ae53/config/model-display-names.json`
- `/home/li/wt/primary/56ae53/tools/claude-native-seat-refresh.py`
- `herdr agent list`, `herdr agent get w1:p8`, `herdr agent prompt w1:p8 "/rename …"`
- `/home/li/.claude/projects/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd.jsonl`
