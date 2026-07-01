# Listener Tracker Graph

## Task And Scope

Tracker-weaver task for the approved Listener orchestration lane. Scope was limited to durable tracker graph creation or advancement for the first speech-to-text slice: repository scaffolding, typed Listener contract, signal-* contract, component vertical slice, and audit/closeout.

Approved intent in the dispatch was treated as the authority. No implementation, repository scaffolding, code editing, closure, deletion, commit, or push was performed.

## Commands Consulted

- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,220p' /home/li/primary/.agents/skills/work-tracking/SKILL.md`
- `bd --help`
- `bd where`
- `bd context`
- `bd list --limit 50`
- `bd search Listener --limit 50`
- `bd search Whisrs --limit 50`
- `bd show primary-ipjx`
- `bd show primary-oil`
- `bd search speech --limit 50`
- `bd create ...`
- `bd dep ... --blocks ...`
- `bd show ...`
- `bd dep tree primary-qvud.5`
- `bd list --label listener --limit 50`
- `orchestrate "(Observe Roles)"`
- `orchestrate "(Claim (tracker-weaver [(Path /home/li/primary)] [Listener tracker graph mutation]))"`
- `orchestrate "(Release tracker-weaver)"`

## Existing Tracker Context

Observed existing Whisrs-related beads:

- `primary-ipjx`: open P1 epic for Whisrs durable RecordingSession redesign after repo-intent repair.
- `primary-oil`: open P3 task for Whisrs feature-gap refresh.

Interpretation: these are not the target for the approved Listener work because the dispatch explicitly says to start a fresh Listener component family and not extend the forked Whisrs. The new graph therefore references the Whisrs constraint in bead text but does not attach work under the Whisrs beads.

Observed related non-Whisrs bead:

- `primary-9s3j`: open P2 task, "Teach speech-to-text tool workspace vocabulary"; not part of this first Listener vertical slice.

## Tracker Items Created

- `primary-qvud` — epic: Listener first vertical slice: durable capture to clipboard.
- `primary-qvud.1` — task: scaffold the three Listener family repos: `listener`, `listener-contract`, and `signal-listener`.
- `primary-qvud.2` — task: define first-slice typed Listener contract records and compatibility tests.
- `primary-qvud.3` — task: define `signal-listener` control/status/delivery contract over the typed contract.
- `primary-qvud.4` — task: implement durable default-input capture, stop-triggered batch transcription, and clipboard delivery through a configurable output mechanism.
- `primary-qvud.5` — task: audit and close out the first slice from named evidence after implementation.

## Dependency Edges Added

- `primary-qvud.1` blocks `primary-qvud.2`
- `primary-qvud.1` blocks `primary-qvud.3`
- `primary-qvud.2` blocks `primary-qvud.3`
- `primary-qvud.1` blocks `primary-qvud.4`
- `primary-qvud.2` blocks `primary-qvud.4`
- `primary-qvud.3` blocks `primary-qvud.4`
- `primary-qvud.4` blocks `primary-qvud.5`

## Final Tracker Status

`bd list --label listener --limit 50` reported:

- Total Listener issues: 6
- Open: 6
- In progress: 0
- Closed: 0
- Deferred: 0

All created beads remain open. No closure was requested or attempted.

## Blockers And Local Convention Notes

No final blocker.

Local convention note: the tracker uses embedded Dolt at `/home/li/primary/.beads/embeddeddolt`, and concurrent `bd` commands can fail with an exclusive-lock error. Initial parallel read attempts produced:

`failed to open database: embeddeddolt: another process holds the exclusive lock on /home/li/primary/.beads/embeddeddolt; the embedded backend supports only one writer at a time`

The graph was created cleanly after switching to strictly sequential `bd` commands.

## Recommended Next Sequencing

1. Work `primary-qvud.1` first: create the three repos and record their paths/checks.
2. Work `primary-qvud.2`: define and test `listener-contract`.
3. Work `primary-qvud.3`: define and test `signal-listener`, consuming the typed contract.
4. Work `primary-qvud.4`: build the Listener vertical slice against the contracts.
5. Work `primary-qvud.5`: audit named evidence and close or leave open the Listener beads accordingly.
