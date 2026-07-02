# Listener Internal Transcription Status Work Graph

## Task And Scope

Create and coordinate the next Listener work graph for internal async OpenAI
transcription plus persistent visual feedback.

Authorized tracker mutation scope:

- create Listener graph beads for scout, runtime/contract implementation,
  OS/UI implementation, audits, and real smoke test;
- update existing blocked `primary-jwx0` without erasing prior blocker
  evidence;
- do not close any implementation, audit, smoke-test, or closeout bead without
  worker/auditor evidence.

No source, documentation, Nix, or runtime implementation work was performed.

## Evidence Consulted

Named evidence files read:

- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- `/home/li/primary/agent-outputs/ListenerDirectSttConfig/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryJwx0/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryId8a/NixAuditor-Review.md`

Tracker readback consulted:

- `bd search Listener --json`
- `bd show primary-jwx0 --json`
- `bd show primary-c8w0 --json`
- `bd list --label listener --all --long --no-pager`

Observed facts:

- `primary-jwx0` was already blocked, with evidence for the original missing
  backend blocker and the later stopgap direct OpenAI command deployment.
- The stopgap CriomOS-home path uses `listener-openai-transcribe` through
  `LISTENER_TRANSCRIPTION_PROGRAM`; the new psyche alignment rejects that
  separate command/program shape as the final production architecture.
- `primary-c8w0` remains open and depends on `primary-jwx0`.
- Prior evidence names Listener commits with typed conflicts at or after
  `fb54c101` and signal-listener at or after `16b54472`.
- CriomOS-home stopgap direct OpenAI command exists at
  `84dbf53811fc31459fb443954a067d33ad8e648c` and must be removed from the
  normal production path when Listener owns transcription internally.

## Graph Created

Parent epic:

- `primary-acmr` — `Listener: internal transcription and persistent status feedback`

Child beads:

- `primary-acmr.1` — `Listener: scout Whisrs status cue and Listener state surfaces`
- `primary-acmr.2` — `Listener: implement internal OpenAI transcription actor and state events`
- `primary-acmr.3` — `Listener: audit internal transcription actor and typed state surface`
- `primary-acmr.4` — `Listener: add persistent status-bar recording feedback in CriomOS-home`
- `primary-acmr.5` — `Listener: audit CriomOS-home status-bar integration`
- `primary-acmr.6` — `Listener: run real spoken smoke test for internal transcription and status feedback`

Existing bead updated:

- `primary-jwx0` — appended a note that `primary-acmr` is the successor graph
  after psyche rejected the separate command/program production shape.
  `primary-jwx0` remains blocked and now depends on `primary-acmr.6`.

## Dependency Order

Dependency edges added:

- `primary-acmr.1` blocks `primary-acmr.2`
- `primary-acmr.1` blocks `primary-acmr.4`
- `primary-acmr.2` blocks `primary-acmr.3`
- `primary-acmr.2` blocks `primary-acmr.4`
- `primary-acmr.3` blocks `primary-acmr.4`
- `primary-acmr.4` blocks `primary-acmr.5`
- `primary-acmr.3` blocks `primary-acmr.6`
- `primary-acmr.5` blocks `primary-acmr.6`
- `primary-acmr.6` blocks `primary-jwx0`

Operational order:

1. Scout current Whisrs status cue and Listener state surfaces.
2. Implement Listener-owned internal OpenAI transcription as an async
   state-bearing actor and expose typed state/events.
3. Audit the runtime/contract actor and typed state surface.
4. Implement CriomOS-home persistent status-bar feedback and remove the stopgap
   command from the normal production path.
5. Audit the Nix/UI/status-bar integration.
6. Run the real operator-spoken smoke test with no synthetic or replayed speech.
7. Use that evidence to unblock `primary-jwx0`; `primary-c8w0` remains blocked
   behind `primary-jwx0`.

## Final Tracker Status

Readback results:

- `primary-acmr`: open epic, six open children.
- `primary-acmr.1`: open and ready; no blocking dependencies.
- `primary-acmr.2`: open, blocked by `primary-acmr.1`.
- `primary-acmr.3`: open, blocked by `primary-acmr.2`.
- `primary-acmr.4`: open, blocked by `primary-acmr.1`, `primary-acmr.2`, and
  `primary-acmr.3`.
- `primary-acmr.5`: open, blocked by `primary-acmr.4`.
- `primary-acmr.6`: open, blocked by `primary-acmr.3` and `primary-acmr.5`.
- `primary-jwx0`: still blocked; now additionally blocked by `primary-acmr.6`.
- `primary-c8w0`: still open and blocked by `primary-jwx0`.

No beads were closed.

## Commands Run

Tracker command surface discovery:

- `bd --help`
- `bd create --help`
- `bd dep --help`
- `bd update --help`
- `bd list --help`

Read commands:

- `bd search Listener --json`
- `bd show primary-jwx0 --json`
- `bd show primary-c8w0 --json`
- `bd list --label listener --all --long --no-pager`
- `bd show primary-acmr --json`
- `bd dep tree primary-acmr.6`
- `bd ready --parent primary-acmr --explain --plain`
- `bd vc status`

Mutation commands:

- `bd create "Listener: internal transcription and persistent status feedback" ...`
- `bd create "Listener: scout Whisrs status cue and Listener state surfaces" ...`
- `bd create "Listener: implement internal OpenAI transcription actor and state events" ...`
- `bd create "Listener: audit internal transcription actor and typed state surface" ...`
- `bd create "Listener: add persistent status-bar recording feedback in CriomOS-home" ...`
- `bd create "Listener: audit CriomOS-home status-bar integration" ...`
- `bd create "Listener: run real spoken smoke test for internal transcription and status feedback" ...`
- `bd dep primary-acmr.1 --blocks primary-acmr.2`
- `bd dep primary-acmr.1 --blocks primary-acmr.4`
- `bd dep primary-acmr.2 --blocks primary-acmr.3`
- `bd dep primary-acmr.2 --blocks primary-acmr.4`
- `bd dep primary-acmr.3 --blocks primary-acmr.4`
- `bd dep primary-acmr.4 --blocks primary-acmr.5`
- `bd dep primary-acmr.3 --blocks primary-acmr.6`
- `bd dep primary-acmr.5 --blocks primary-acmr.6`
- `bd dep primary-acmr.6 --blocks primary-jwx0`
- `bd update primary-jwx0 --append-notes ...`

Non-mutating command issue:

- A concurrent parallel read produced the embedded Dolt exclusive lock error;
  the same read was retried sequentially and succeeded.
- `bd ready --no-pager` failed because `bd ready` does not support that flag;
  it did not mutate tracker state and was rerun as
  `bd ready --parent primary-acmr --explain --plain`.

Beads VC status after tracker mutation:

- `bd vc status` reported branch `main`, commit `up7mpsdd`, and no
  uncommitted tracker changes.

## Dispatch Status

No workers were dispatched by this tracker-weaver run; no dispatch tool or
worker launch surface was part of the assigned role packet.

First expected worker:

- Scout for `primary-acmr.1`.

First worker brief should route:

- evidence files named in this report;
- no secret or transcript disclosure;
- map Whisrs status-bar/wavelength cue and Listener state surfaces only;
- output a situational map under `agent-outputs/ListenerInternalTranscriptionStatus/`.

## Blockers And Follow-Up

Open blockers:

- `primary-acmr.2` through `primary-acmr.6` are intentionally blocked by graph
  dependencies.
- `primary-jwx0` remains blocked until `primary-acmr.6` produces real
  operator-spoken smoke-test evidence.
- `primary-c8w0` remains blocked by `primary-jwx0`.

Next orchestrator action:

- Dispatch `primary-acmr.1` to a scout.

