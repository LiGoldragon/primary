# Psyche native launch gate — 2026-09-21

## Result

Neither requested Psyche seat was launched. This Codex subflow is outside a
Herdr-managed pane: `test "${HERDR_ENV:-}" = 1` exited 1 and no Herdr caller
context was present. The supported `tools/native-batch-refresh.mjs start`
explicitly rejects this condition with `Herdr-managed pane required; start
this command inside Herdr`. The installed `herdr --skill` also directs a caller
outside Herdr to stop before control commands. No `start`, tab creation, agent
start, bootstrap, title mutation, route binding, or retirement was attempted.
The second seat was held because the first could not start through the
supported path.

## Prepared evidence and grades

The source/profile work is committed at `3b31089d51fe` and the launch/title
controller changes at `0a76db3b5521`. Current profile fixtures both passed.
All six Psyche Low and seven Psyche Ultra Low declared source hashes matched
current bytes. Profile SHA-256 values are:

| Seat | Profile SHA-256 | One-seat controller validation | Bootstrap / title / identity / acceptance |
| --- | --- | --- | --- |
| `psyche-low-of-0625c3` | `6a0e8eab33186c72edf82cc3547e9ca3333ca59f2cec94626e85de26a9a140fd` | `valid:true`, Sonnet 5 medium, `messaging-build/wS` manifest | Not attempted; no receipt |
| `psyche-haiku-of-b80e55` | `16a189c2cd36c4fa52a388646cece2c910cf02abeed4fcb4d6e63780c47e1bf1` | `valid:true`, Haiku 4.5 medium, `messaging-build/wS` manifest | Not attempted; no receipt |

The validation was read-only with temporary manifests, each containing exactly
one fresh Claude seat. It checked the controller's audited profile contract
and installed native skill paths. It did not prove an actual native skill
expansion or source acknowledgement. The source audit timestamps in the
profiles are 2026-09-21T16:09:44Z; recheck currentness immediately before
each live launch.

## Existing state and executor evidence

`flows/7091ea/log.md` records the repaired existing `psyche-low` HM route to
`0625c3` at `messaging-build/wS:p1`, terminal
`term_65bedce5d2b213a`, native session
`0625c31b-798d-44f7-a116-44a7966fe618`, with a target Read witness.
That is a prior point-in-time receipt, not a live read from this subflow. The
new profile's unique launch identity avoids binding over this route. Leave the
existing seat and route unchanged.

Committed `flows/6db4fe/reports/field-astra-refresh.md` reports native Field
Astra main `03e825` in Herdr `messaging-build/wQ:p9` with HM target read and
accepted work. `flows/6db4fe/reports/field-sol-refresh.md` likewise reports
native Field Sol main `753e69` in `messaging-build/wQ:pA`. These show that a
Herdr-managed Field executor has existed. They cannot establish that either
pane is presently live or that its caller is inside Herdr. This subflow sent
no status prompt and did not inspect panes, because it has no Herdr caller
context. The exact present HM binding for either executor and for `0625c3`
must be read by an eligible Herdr-managed executor before action.

## Exact handoff to a Herdr-managed executor

1. Confirm `HERDR_ENV=1` and the caller's Herdr pane/session. Read the existing
   `0625c3` pane/transcript and HM registration without sending a heartbeat.
   Confirm an available Herdr workspace and exact live binding; `wS` was
   validated as a manifest value, not witnessed live here.
2. Re-read each current profile, first-turn file, declared source, and
   controller. Re-run the profile fixture and a **single-seat**
   `native-batch-refresh.mjs validate` immediately before each start. Acquire
   an exact write lock for the manifest, state and receipt paths.
3. Start **Psyche Low alone** with `native-batch-refresh.mjs start` from that
   Herdr pane. Use `messaging-build`, a checked workspace, the absolute
   `psyche-low-native/profile.json`, `fresh:true`, `predecessor:null`, agent
   `psyche-low-of-0625c3`, label and native title `Psyche Low`, model
   `claude-sonnet-5`, effort `medium`. Use a new state file. Wait for the
   controller's exact bootstrap, native-main-flow, model/effort, source
   acknowledgement and `/rename` transcript readback receipt. Then let the
   new main claim its own Flow ID and inspect its own transcript/pane for role
   acceptance. Do not bind the legacy `psyche-low` route.
4. If any startup or title gate fails, stop before a second launch and report
   the exact failed phase and state file; preserve the created seat for
   diagnosis. If Low passes, repeat as a separate one-seat attempt for
   `psyche-haiku-of-b80e55`, label/title `Psyche Ultra Low`, model
   `claude-haiku-4-5`, effort `medium`, using the absolute
   `psyche-haiku-native/profile.json` and a different new state file. Have it
   claim its own Flow ID and accept the role in its own transcript.
5. Bind no legacy route and retire nothing. Any new route requires an exact
   native session/pane/terminal/harness tuple, a checked target, and an
   isolated harmless route test before binding. Report bootstrap, title,
   identity, and acceptance grades separately.

No native receipt, claimed Flow ID, current pane read, or live route test for
either requested seat exists from this attempt. The launch remains open.
