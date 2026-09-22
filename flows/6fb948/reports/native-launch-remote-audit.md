# Native launch and remote-access audit

Date: 2026-09-22. Scope is read-only: current runtime, current source, and
the bounded `6fb948` replacement evidence. This report does not claim a
deployment, a successful login, or external remote visibility.

## Decision-grade findings

| Layer | Grade | Evidence | Meaning |
| --- | --- | --- | --- |
| Claude fresh-seat provisioning | blocked | `fable-restart-20260922/state.json` records failure before first bootstrap input | The old batch path cannot make a valid fresh Claude seat until its zero-turn contract is repaired. |
| Claude replacement currently in `wD:pC` | auth-blocked | live pane shows the exact Fable process/session and `Login expired`; native login UI awaits user completion | The pane and model binding are real, but it is not remotely usable or bootstrap-ready until the account authentication completes. |
| Claude Remote Control | degraded / per-session | p5 and p7 visibly show green `/rc`; p7 nevertheless says `Login expired` | `/rc` proves the UI feature is enabled, not that the account token works or that a remote client can open the named session. |
| Codex remote control | runtime present, external reachability unproved here | user service is active and runs `codex app-server --remote-control` | A local app-server connection or manually generated code does not prove the living can see the thread remotely. |
| deployed Flow Nexus | Codex-only source; runtime unreachable | `/home/li/.local/bin/flow-nexus` exists and its socket paths exist, but a direct `flow` client receives `Connection refused` | It has no Claude adapter, remote-control readiness, Herdr pane binding, or Messenger handoff; its present daemon is not accepting ordinary-client requests. |
| Flow CLI POC | fixture-only | `tools/flow-cli-poc/README.md` says it is not production Nexus/provisioning | Do not route native Claude refreshes through it as if it were a production launcher. |

## Actual failure chain

1. `native-batch-refresh.mjs` created `wD:pC`, reserved native UUID
   `f4b2633d-52d8-4363-b584-795fe727cd93`, prepared its `CLAUDE_JOB_DIR`, and
   started the Fable process. This is corroborated by the failed-state ledger
   and current Herdr `process-info`; it is not a guessed binding.
2. The batch controller immediately invoked
   `tools/claude-native-seat-refresh.py --refresh` without a bootstrap mode.
   In `refresh()` at lines 651–669, an empty transcript is rejected unless the
   manifest is marked disposable or the special `--bootstrap-running-empty`
   route is used. A fresh interactive Claude session has no transcript before
   its first native input. The recorded exception is therefore deterministic,
   not an account or model failure.
3. The controller's ordinary fresh path does not pass
   `--bootstrap-running-empty` at `native-batch-refresh.mjs:191`. Its special
   retained continuation has a narrower recovery contract and is not the
   ordinary start path. This mismatch made the script require a nonexistent
   zero-turn transcript.
4. The current `wD:pC` replacement later received `/rename`, then `/spirit`.
   The visible UI responded `Login expired · Please run /login` and opened the
   native subscription OAuth screen. No credentials, code, or OAuth URL belong
   in this report. The observed process is Fable 5.1, medium, with the
   expected UUID; it is not a phantom or a shell-command injection.
5. The independent remote-control check found green `/rc` in p5 and p7. p7
   also had the expired-login error. This directly disproves the prior rule
   “local pane or remote-control flag means remotely ready.”

## Components and ownership boundary

The source copies used by the failing runtime are exactly the current working
copies (`cmp` matched all four), but the failure stack executed the deployed
paths below. A source edit alone is not a deployment claim.

| Component | Authoritative current path | Present behavior | Repair owner |
| --- | --- | --- | --- |
| Claude batch launcher | `/home/li/primary/tools/native-batch-refresh.mjs` | Creates a new Herdr tab/pane; requires `HERDR_ENV=1`; has no ordinary existing-pane target and calls helper without fresh-bootstrap mode | launcher component |
| Claude bootstrap/receipt helper | `/home/li/primary/tools/claude-native-seat-refresh.py` | Uses transcript entries as the receipt source; rejects an empty fresh transcript on ordinary refresh | launcher component |
| historical one-turn starter | `/home/li/primary/tools/claude-single-turn-start.py` | Explicitly raises at lines 102–106; dead code below includes `--remote-control PsycheHigh` | retire from candidate use or replace only after its isolation contract is implemented |
| Codex native launcher | `/home/li/primary/tools/native-seat-launch.mjs` | Uses the Codex app-server socket, not Claude or Herdr remote control | Codex launcher component |
| Flow ordinary client | `/home/li/primary/flow/crates/flow/src/main.rs` | One Datom argument over `FLOW_SOCKET` | Flow component |
| live Flow Nexus | `/home/li/primary/flow/crates/flow-nexus/` and `/home/li/.local/bin/flow-nexus` | Starts/resumes Codex through `codex app-server proxy`; ordinary and meta sockets currently refuse connection | Flow component |
| POC supervisor | `tools/flow-cli-poc/` | SQLite + fixture/one-turn prototype; declared non-production | not a deployment target |

The Flow Nexus itself is not the immediate Fable repair: its `RunningNexus`
only calls the Codex adapter, and restart is an app-server resume of a Codex
thread. The executable `/home/li/.local/bin/flow-nexus` is present as PID
3727637 and `/tmp/flow-nexus.sock` plus `/tmp/flow-nexus-meta.sock` exist, but
the actual `flow` client receives `Connection refused`; this is stale or
unreachable runtime, not a live service claim. Adding Claude would be a
separate adapter and Signal-contract change, not a shell wrapper substitution.

## Minimum executable repairs

1. **Fix the fresh Claude controller contract first.** In the ordinary
   Claude branch of `native-batch-refresh.mjs`, call the helper with an
   explicit fresh-bootstrap mode and the immutable launch-state/receipt
   attestation it requires, or refactor that mode into a single
   `fresh-interactive` entry point. The proof rule must be: exact Herdr
   pane/terminal + exact native UUID + empty transcript before first input,
   then the transcript records caused by `/rename`, each injected skill, and
   the bootstrap acknowledgement. Never require the transcript before sending
   the first native command.
2. **Make remote readiness a separate structured observation.** Record
   `feature_enabled`, `account_authenticated`, `remote_session_name`,
   `remote_url_or_absent`, `observed_at`, and `evidence_surface`. Green `/rc`
   satisfies only `feature_enabled`. Login-expired is an explicit failed
   `account_authenticated`. A manual code or a process flag satisfies neither
   external visibility nor client attachment.
3. **Preserve the live replacement boundary.** Let the authorized Fable auth
   worker finish pC's native login UI. After it returns to the session, inspect
   its visible TUI and then invoke `/remote-control` only if the marker is
   absent. Read back its rendered remote URL/name if Claude exposes one. Do
   not resume the failed old Fable, start another process, or paste a prompt
   while auth is pending.
4. **Bind Flow to Herdr only through a real adapter.** A production Claude
   `Start` receipt must include Herdr session/workspace/pane/terminal,
   Claude UUID, fresh transcript locator, model/effort, and remote-readiness
   observation. Its implementation belongs beside a Claude adapter in the
   Flow component and its typed Signal contract, not in the fixture POC or a
   bare `herdr pane run` command.
5. **Add one end-to-end acceptance test per harness.** Use a disposable
   account-authenticated Claude seat and actual Claude remote client surface:
   verify a new `Flow Start` produces one exact pane/session, native context
   receipt, final title, and visible remote session; then test the expired-auth
   branch reports `account_authenticated=false` without reading secrets. For
   Codex, create a Flow-started thread through its live app-server, then prove
   it is visible on the actual remote client. Fixtures may cover parsing and
   failure edges but cannot certify these outcomes.

## Do not repeat these mistakes

* Do not treat a pane, process, `--remote-control`, `/rc`, CLI help, or a
  generated pairing code as external remote visibility.
* Do not send a shell command through an active Codex agent input route. A
  mutation must use a verified shell pane/command execution path; the earlier
  `wQ:pE` injection was not a shell execution and supplies no test evidence.
* Do not select a transcript by “latest” or manufacture a zero-turn one.
  Missing is a first-class state, and fresh bootstrap must create the first
  receipt event.
* Do not claim the Flow POC, source checkout, or compiled binary was deployed
  merely because the source exists. The actual deployed Flow root is the
  separate repository `/home/li/primary/flow`; its current daemon is
  `/home/li/.local/bin/flow-nexus`.

## Vision used and limits

The newest relevant records state that refresh should operate through the Flow
CLI with a safe Messenger switch (`flows/1b8ac0/vision/refresh.md`, 2026-09-21,
STT, transcript `1b8ac00b:1033`); Flow CLI startup should create Herdr jobs and
reuse Herdr's list/attach interface (`flows/108ab0/vision/operational-flowCliListAttachProvenance.md`,
2026-09-17, typed); and the supported Claude outcome is desktop-app access
(`flows/01a04524/vision/claudeRemoteControl.md`, typed provenance not recorded
there). An older record warns that prior Remote Control claims were unreliable
(`flows/9e7c9f/vision/remoteControl.md`, 2026-09-13, STT). The present runtime
observation supports that caution: feature enabled and authenticated access
are distinct. These records direct the target, but they do not prove a
finished Claude adapter or a successful external client attachment.

## Handoff state

Prom connectivity was reported independently as proved at 19:14 UTC (root SSH
uptime six minutes and USB `10.44.0.148`/MAC `84` match). This audit did not
retest it. Root context was reported at 49.1%, above the living's 40% refresh
threshold; carry this report and the pC auth-pending state to the clean High
successor. The OAuth authorization material is deliberately absent.
