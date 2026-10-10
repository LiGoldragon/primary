# Listener Usability Fix Work Graph

## Task And Scope

Created the next Listener usability-fix tracker graph for:

- live mic-level responsiveness;
- safer Listener record shortcut;
- Listener cancel shortcut;
- cancel semantics that stop capture without transcription/API spend/clipboard write while retaining the capture artifact;
- audits, activation, and live smoke evidence.

Authorized tracker mutations were performed. No source code, documentation,
Nix files, runtime services, transcript text, clipboard text, secrets, or audio
contents were inspected or changed by this tracker-weaver run.

## Evidence Consulted

Named evidence files read:

- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/RustAuditor-ReAudit.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/NixAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/OperatingSystemImplementer-LiveActivationEvidence.md`

Observed facts from those files:

- Listener `0.4.0` is live after activation.
- `$XDG_RUNTIME_DIR/listener/status.sock` exists after daemon restart.
- Noctalia has `listener-level` adjacent to `whisrs-level`.
- Whisrs remains active side by side with its bindings preserved.
- Speech detection/transcription was not disproven by the evidence; the open live smoke blocker was human observation.
- The live Listener status path is a local UI-safe JSON socket with state and level only.
- Current evidence does not include cancel semantics or a typed cancel command.
- The deployed meta-lojix accepts the legacy `Deploy (Home (...))` shape, not the checked-out source `UserEnvironment` variant.

Interpretation:

- The new live meter complaint should be treated as a correctness/usability bug in the feedback path and blocks closing the older smoke evidence.
- The next graph should make diagnosis of the live feedback boundary explicit before assigning the live-level fix.
- Cancel and scout can start independently; the Home shortcut work should wait until the typed cancel target and live-level fix are known.

## Graph Created

Parent epic:

- `primary-zddv` - `Listener: usability fixes for live level, shortcuts, and cancel retention`

Child beads:

- `primary-zddv.1` - `Listener: scout frozen live level/status path`
- `primary-zddv.2` - `Listener: implement typed cancel with retained capture artifact`
- `primary-zddv.3` - `Listener: fix live mic-level responsiveness at diagnosed boundary`
- `primary-zddv.4` - `CriomOS-home: safer Listener record shortcut and cancel shortcut`
- `primary-zddv.5` - `Listener: audit cancel contract and live status fixes`
- `primary-zddv.6` - `CriomOS-home: audit Listener usability shortcut and widget integration`
- `primary-zddv.7` - `Listener: activate audited usability-fix generation`
- `primary-zddv.8` - `Listener: live smoke usability fixes without private content disclosure`

Existing bead updated:

- `primary-acmr.6` now depends on `primary-zddv.8`.
- `primary-acmr.6` notes now record that the successor usability graph is required because the live level meter feels frozen/stuck and cancel/safer shortcut behavior is required before closing the live smoke path.

## Dependency Edges

Edges added:

- `primary-zddv.1` blocks `primary-zddv.3`
- `primary-zddv.2` blocks `primary-zddv.4`
- `primary-zddv.3` blocks `primary-zddv.4`
- `primary-zddv.2` blocks `primary-zddv.5`
- `primary-zddv.3` blocks `primary-zddv.5`
- `primary-zddv.4` blocks `primary-zddv.6`
- `primary-zddv.5` blocks `primary-zddv.7`
- `primary-zddv.6` blocks `primary-zddv.7`
- `primary-zddv.7` blocks `primary-zddv.8`
- `primary-zddv.8` blocks `primary-acmr.6`

Operational order:

1. Scout the live level/status path.
2. Implement typed cancel with retained artifact.
3. Fix the live mic-level responsiveness at the diagnosed boundary.
4. Update CriomOS-home shortcuts after cancel and level-fix targets exist.
5. Audit Rust/contract behavior.
6. Audit CriomOS-home shortcut/widget integration.
7. Activate the audited generation.
8. Run live smoke tests for mic taps, cancel no-spend/no-clipboard with artifact retained, and normal record/transcribe/copy when a non-private phrase is available.

## Final Tracker Status

Readback results:

- `primary-zddv`: open epic with 8 open children.
- `primary-zddv.1`: open, ready.
- `primary-zddv.2`: open, ready.
- `primary-zddv.3`: open, blocked by `primary-zddv.1`.
- `primary-zddv.4`: open, blocked by `primary-zddv.2` and `primary-zddv.3`.
- `primary-zddv.5`: open, blocked by `primary-zddv.2` and `primary-zddv.3`.
- `primary-zddv.6`: open, blocked by `primary-zddv.4`.
- `primary-zddv.7`: open, blocked by `primary-zddv.5` and `primary-zddv.6`.
- `primary-zddv.8`: open, blocked by `primary-zddv.7`.
- `primary-acmr.6`: remains blocked, now additionally blocked by `primary-zddv.8`.
- `primary-jwx0`: remains blocked by `primary-acmr.6`.
- `primary-c8w0`: remains blocked by `primary-jwx0`.

No beads were closed.

## Commands Run

Doctrine and evidence reads:

- `sed -n ... /home/li/primary/.agents/skills/work-tracking/SKILL.md`
- `sed -n ... /home/li/primary/.agents/skills/reporting/SKILL.md`
- `sed -n ...` for the seven dispatch-named evidence files listed above.

Tracker read/help commands:

- `bd create --help`
- `bd dep --help`
- `bd update --help`
- `bd list --help`
- `bd show primary-acmr.6 --json`
- `bd list --parent primary-zddv --all --long --no-pager`
- `bd dep tree primary-zddv.8`
- `bd ready --parent primary-zddv --explain --plain`
- `bd list --parent primary-zddv --ready --long --no-pager`
- `bd show primary-zddv --json`
- `bd vc status`

Mutation commands:

- `bd create "Listener: usability fixes for live level, shortcuts, and cancel retention" ...`
- `bd create "Listener: scout frozen live level/status path" ...`
- `bd create "Listener: implement typed cancel with retained capture artifact" ...`
- `bd create "Listener: fix live mic-level responsiveness at diagnosed boundary" ...`
- `bd create "CriomOS-home: safer Listener record shortcut and cancel shortcut" ...`
- `bd create "Listener: audit cancel contract and live status fixes" ...`
- `bd create "CriomOS-home: audit Listener usability shortcut and widget integration" ...`
- `bd create "Listener: activate audited usability-fix generation" ...`
- `bd create "Listener: live smoke usability fixes without private content disclosure" ...`
- `bd dep primary-zddv.1 --blocks primary-zddv.3`
- `bd dep primary-zddv.2 --blocks primary-zddv.4`
- `bd dep primary-zddv.3 --blocks primary-zddv.4`
- `bd dep primary-zddv.2 --blocks primary-zddv.5`
- `bd dep primary-zddv.3 --blocks primary-zddv.5`
- `bd dep primary-zddv.4 --blocks primary-zddv.6`
- `bd dep primary-zddv.5 --blocks primary-zddv.7`
- `bd dep primary-zddv.6 --blocks primary-zddv.7`
- `bd dep primary-zddv.7 --blocks primary-zddv.8`
- `bd dep primary-zddv.8 --blocks primary-acmr.6`
- `bd update primary-acmr.6 --append-notes ...`

Tracker VC status:

- `bd vc status` reported branch `main`, commit `ql0738gv`.

No source commits were made or pushed by this tracker-weaver run.

## Dispatch Status

No workers were dispatched by this role. The first ready workers are:

- Scout for `primary-zddv.1`.
- Runtime/contract implementer for `primary-zddv.2`.

Suggested first scout brief:

- Use `primary-zddv.1`.
- Read this report and the dispatch-named evidence.
- Observe live `listener/status.sock` state/level frames and Noctalia widget behavior without reading transcript text, clipboard text, audio contents, or secrets.
- Map the frozen meter to Listener PCM publication, status socket cadence/backpressure, QML parsing/reconnect/animation, or activation/version mismatch.

Suggested first implementation brief:

- Use `primary-zddv.2`.
- Implement typed Listener cancel semantics with retained artifact.
- Prove cancel does not call transcription/OpenAI or clipboard delivery.
- Preserve normal start/stop/status/transcribe/copy and Whisrs separation.

## Blockers And Follow-Up

Open blockers:

- `primary-zddv.3` waits for live-path scout evidence.
- `primary-zddv.4` waits for cancel and level-fix implementation.
- `primary-zddv.5` waits for cancel and level-fix implementation.
- `primary-zddv.6` waits for CriomOS-home shortcut/widget implementation.
- `primary-zddv.7` waits for both audits.
- `primary-zddv.8` waits for activation.
- `primary-acmr.6`, `primary-jwx0`, and `primary-c8w0` remain open.

Next orchestrator action:

- Dispatch `primary-zddv.1` and `primary-zddv.2` in parallel if worker capacity allows.
