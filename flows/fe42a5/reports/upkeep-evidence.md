# Upkeep evidence — Mind core fe42a5

## Scope

Read `flows/1add4b/vision/flow-nexus.md` and `design.md` directly. Work toward the refuted Flow Nexus version 1 proposal stopped; no cutover/runtime/source activation occurred. This audit makes no claim that all raw records were exhausted. No audio, transcripts of dictation, credentials or secret-bearing process environments were inspected.

## Speech: current deployment gap witnessed

- `/proc/3286720/exe` resolves to `/nix/store/drrrcy4vbli1yyw2ikfcf5xhm6cbrsq5-wispr-flow-1.6.774+criomos.11/lib/wispr-flow/electron/wispr-flow`.
- Read-only subflow reports helper PID3287663 and audio service PID3287872; app is under `app-wispr-flow-3286720.scope`, not a `wispr.service` or `whisrs.service` user unit. Its bounded structured-error journal query returned no matching lines; absence of those lines proves no cause.
- Both subflow and coordinator independently counted markers in shipped `lib/wispr-flow/electron/resources/app.asar` bytes:

| Package store basename | `WISPR_LINUX_DICTATION_ADMISSION` | `WISPR_LINUX_DICTATION_BUSY_PTT_BEGIN` | `__wisprDictationAdmission` |
|---|---:|---:|---:|
| `drrrcy4vbli1yyw2ikfcf5xhm6cbrsq5-wispr-flow-1.6.774+criomos.11` (running) | 0 | 0 | 0 |
| `b8zlr6p584jwcppilp77wxzjv95g5q6y-wispr-flow-1.6.774+criomos.12` (store only) | 1 | 1 | 11 |

- Canonical `/git/github.com/LiGoldragon/CriomOS-home` committed HEAD `437455a4a5a0b47d71b23c6f37b3188f250dcb0d`, `git show HEAD:flake.lock`, pins Wispr `e97b9587a7186ad74c5d84b2da6abfb86645b68d`. This is committed-source evidence, not proof of the running Home generation.
- `git log --ancestry-path e97b958..5062179` in `/home/li/worktrees/wispr-flow-linux-stt-codex` shows `06619a8` (serialize admission), `0ebdd6c` (delayed tails), `5062179` (active controls). These repairs are later than the committed Home pin.
- Therefore source success on `5062179` cannot establish this live app includes the repair. Existing deployment task `primary-bie3.6.3` already covers landing it; no duplicate hand was commissioned. Field core Secondary received this evidence (delivery279, accepted Queued; consumption unwitnessed).

The historical `agent-outputs/SpeechToTextReliability/Scout-SituationalMap.md` describes Whisrs buffering, not this observed Wispr runtime; it is not tonight's root-cause witness.

### Remaining hypothesis and validation boundary

`stt-codex/scripts/patches/linux-dictation-admission.sh:85` reserves UUID ownership; lines162–175 mark the completion tail and release the matching UUID in its outer `finally`. A nonsettling completion can retain ownership. A small copied-logic Node probe showed busy remains true without release; it did not execute the whole patched app, reproduce a real hang, or establish tonight's cause. No timeout/watchdog patch was justified or added.

Both subflow and coordinator ran `bash -n` on `linux-dictation-admission.sh`, `linux-status-bridge.sh`, `scripts/build-linux.sh`, and `node --check scripts/wispr-status-bridge.cjs`: pass. Bats is unavailable; no Bats suite or real dictation test ran. No paid transcription request was made.

## Raw-record problem list

| Problem | Raw source | Present evidence and disposition |
|---|---|---|
| Speech unavailable/meaning lost | `flows/e51411/vision/speech.md`; `flows/74e4d1/vision/speech.md` | Deployment gap above witnessed; cause of all failures unknown. `primary-swaf.1` open; no restart counts as closure. Emotion/hesitation preservation remains a separate vision subject. |
| Suspend battery drain | `flows/1add4b/vision/flow-nexus.md` | `bd query` finds open `primary-7a7`, assigned Field core Primary; Orchestrate snapshot retains `LaptopSuspendFix` lock24672. Owner/lock is not a successful suspend witness. Listed with existing owner, not duplicated. |
| Harness text shown as the Primary's own words | `flows/b0d3ae/vision/psyche-primary.md:19–37` | Open `primary-hbhi` records transcript line275 finding and acceptance criterion. No repair/fresh-session witness here; listed. No configuration edit made. |
| Zeus link needs unplug/replug | `flows/d5b96b/vision/cluster-survey.md`, 2026-09-29 | Raw recurring failure; current network state/closure unknown. Asked existing Field route for evidence; no network alteration. |
| Slow, unreliable book communication | `flows/4a8a28/vision/conversation.md` | Raw complaint; no measured present latency or closure here. Listed, not declared currently reproduced. Morning account kept short. |
| Tests using themselves as oracle | `flows/7c3f0c1d/vision/testTravesties.md` | Raw complaint, no exact current offending test independently established. Listed for review, not labeled a proven present defect. |
| Home source/deployed pin mismatch | `flows/6f51ad/vision/home.md` | Historical record alone is insufficient; this speech pin/bundle comparison supplies a new narrow witness. No broad Home deployment failure inferred. |
| Queue batching, registration probes, model selection, hand-started flows | `flows/9aaaba/vision/flow.md`; `flows/6f51ad/vision/registration.md`; `flows/546f78/vision/models.md`; `flows/36b71b/vision/flow.md` | Audit found old submodule code/docs, not established deployed behavior. Retained as historical checks for tomorrow; no Flow design or runtime change tonight. |

`handoffs/listener-desktop-integration.md:116` explicitly lacks real-world deployment/feedback witnesses, but concerns an older Listener path; it does not prove today's Wispr failure.

## Modular builds: corrected premise and held simplification

Actual `nix config show` reports `substituters = http://nix.prometheus.goldragon.criome https://cache.nixos.org/`, `builders-use-substitutes = true`, and a Prometheus public key. `/etc/nix/nix.conf` resolves to `/nix/store/kcb3ccv3xknqasmsr36y0s15wqchkp60-nix.conf`. This is configuration presence on this host only: no successful cache hit, serving health, cross-machine reuse or dependency-bump derivation count was tested.

`rust-build/lib/default.nix:30–109` owns Crane, filtering and artifact normalization. Canonical `flow/flake.nix:4–41` still duplicates build policy; `orchestrate/flake.nix:24–31` already consumes rust-build. The candidate centralization was sent to Mind core Primary (delivery253, refined302; accepted Queued, consumption unwitnessed). Direct read found Flow has five toolchain components while the shared default adds `rust-analyzer` and archive normalization; behavior-equivalence and net reduction need proof. No edit undertaken awaiting judgment.

No crate2nix implementation or before/after derivation-count witness exists in this audit. Git dependencies, feature-separated client/Nexus resolutions and tests still need a design. This work continues only where total code is removed, under the latest order.

## Accounting

Production source: **0 lines removed / 0 added**. No fix claimed, no runtime change, no activation, no heavy build. Only this evidence and its short account were authored, plus Beads working-state updates. Report path reservation: Orchestrate lock24929, owner fe42a5. Beads store verified `/home/li/primary/.beads/embeddeddolt`; `primary-po9k` claimed. Primary/Field messages report queue admission, not consumption.
