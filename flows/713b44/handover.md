# Harness release 3kyf — checkpoint of 713b44

Open obligations: Psyche task **3kyf** (first Codex Harness release) and order **daxc** (SessionId consumers). Neither is complete. Original custody/history is in `flows/074047/handover.md`, then `flows/92d3be` and `flows/de6298`. No gate, publication, registry change, runtime deployment, or metadata generation occurred in this flow.

## Custody and exact sources

Psyche doo6 confirmed sole successor custody; Core b7lv accepted it. Released predecessor 420/432 and reacquired the exact paths as **436** (core/tests) and **437** (library/contracts), owner713b44. Core separately acquired **438**, translatorBudget713b44, for the isolated native budget prerequisite. Own handover directory is under **441**. Preserve these reservations across continuation; no duplicate transfer is required. All source workers stopped at clean committed checkpoints.

Paths are under `/git/worktrees/`:

| Worktree | Branch | HEAD |
| --- | --- | --- |
| codex-harness-nexus-mend-de6298 | mend-de6298 | `caee921994acb85600684f074f301e130c7750fc` |
| codex-harness-nexus-tests-mend-de6298 | mend-de6298 | `f6befbfa6ff7399badd9eb2e8d277eb4e10a4bf1` |
| harness-nexus-library-074047 | harness-sessionid-lock432 | `bf8613a0ea18ec34976b07ddb02e8ee60d53b88c` |
| signal-codex-harness-nexus-074047 | signal-refusal-lock432 | `54cbda97402267efa182eab2ac979fa0459958ee` |
| meta-signal-codex-harness-nexus-074047 | meta-refusal-lock432 | `4ee447e94d737557d137b423f1c8bddb7bbd4898` |
| translator-budget-713b44 | translator-budget-713b44 | `5873b662f7c1218dfe90261acc206634e8ffa302` |

These are SOURCE-WIP except the separately accepted native-budget source packet. The whole Harness cohort remains incomplete/non-compiling expected: daemon, translator and tests have not adopted all changed APIs. Existing canonical refs and all published0.1 revisions/registrations remain unchanged.

Core wwlx confirmed source version allocation: library/core/daemon/translator/tests **0.2.0**, ordinary/meta **0.5.0**. Source manifests now reflect it (core commitd3fb278; testsf6befbf). Local core path requirements in daemon/translator also take0.2.0. Locks and generated dependency metadata intentionally still contain older versions; no Cargo.lock/Cargo.nix/flake.lock regeneration was authorized or performed.

## What was implemented

Psyche fum4/rnjb replaced partial ordinary replies with `ReportedWithFaults.Vector<ReportFault>`. ReportFault holds LaneFailed, Unread, Unwatched, MemoryFault and FoldRefusal with typed causes. Fault-free remains Reported; ReportRefused is only for a Report never committed. Core `PerformanceFailure` carries the primary failure and prior ordered fault vector through recursive attempts so an enclosing committed Report retains both.

Psyche rl5h required per-target native lifetimes. Core `watching.rs` now owns an independent native watcher per placement, stages candidates, drops stages on failed fold/commit, merges successful targets only AFTER commit, and retains prior active handles on a failed replacement. Uninstalled generations are ignored. New failed attachment P stays Pending. Psyche8h98 clarified existing Q keeps its persisted Watched cursor/registration even when no handle is live; Unwatched(Q) describes runtime standing, and later placement resumes its cursor. No extra Memory demotion was added.

An independent read-only audit found Active handles were accidentally dropped by the first merge implementation38b4c2f. Corrected by explicit Active/Staged ownership partition in **caee9219**. The exact correction received bounded SOURCE PASS, not compile/runtime/resource proof:
`/tmp/immutable-watch-correction-recheck.zMbVjE/immutable-watch-correction-recheck.md`.
Earlier failure report remains `/tmp/immutable-watch-correction-audit.PBSUo4/immutable-watch-correction-audit.md` and describes the superseded38b4 candidate.

Core receipt: `/tmp/fault-core-correction-receipt.GisYsa`; final partition receipt: `/tmp/fault-core-watch-merge-correction.OyF7y2`. Resource unknown: native handles grow with distinct placements; no ceiling/runtime test was run.

Daemon emitter now uses SessionId. Existing ListenerFailure Display/Error bodies moved from daemon (orphan implementations) to owning core `diagnosing.rs`, commit7495296. Core flake generation check now covers translator_settings and formatting includes settings_actor (1959bc9).

Meta schemas now include Open, Opened, ConfiguredUnopened, OpeningFailed and OpenRefused(NotReady). OpeningFailure has Listener with generated `Listener_Data::{Meta,Public}(Diagnostic)`, UnwatchableDirectory, MemoryFault and ActorUnavailable. ConfigurationField was moved into its own authored `ethos/library.ethos` namespace because same-named variants in signal resolved to payload types; all six field tags are now unit variants and NotReady carries their vector. New module is generated/re-exported; meta flake generation check covers it (f1057c4). Outputs Configured/Subscribed/Opened remain first, matching positional success mapping for Configure/Subscribe/Open.

Static checks only: pinned Ethos Check/generation comparisons, rustfmt, diff checks, TOML parsing, and Nix syntax parsing of the two changed flakes. No local cargo, Nix evaluation/build, compilation, tests or gate was run.

## Approved opening behavior — not implemented yet

Psyche2wuv/dra3/wqjq/m5od ruled:
- Partial Configure commits, answers Configured, and attempts no native opening work.
- A ready Configure tries native watch placement then public listener; postcommit failure is ConfiguredUnopened.OpeningFailure.
- Manual Open before readiness is OpenRefused.NotReady with typed missing-field names; otherwise Opened only when a public listener exists, or OpeningFailed.
- Only next Configure or manual Open retries after failure; no retry loop. Meta stays alive.
- Native watch placement is the prerequisite for listener publication. Initial rollout replay is ordinary event processing: lane/unread/fold faults are ReportFault diagnostics and never prevent Opened.

Read-only implementation plans:
`/tmp/daemon-integration-plan.iq7W65/daemon-integration-plan.md` and `/tmp/opening-integration-plan.46bRFG/opening-integration-plan.md`. They predate final watcher API; preserve the new per-target anatomy rather than restoring old constructors. Their version-directory uncertainty is resolved: update existing isolated member manifests, preserve old published registrations; no new parallel source layout was requested.

Next source work: generate typed internal opening/configuration outcomes and readiness/missing-field projection; actor owns sole Opened and startup follow-on; replace daemon old locks/OnceLock/API with runtime-before-bind, actor wrapper/PublicOpening and receiver ownership; adapt translator meta Open plus remaining test constructors/PerformanceFailure callers; source-test the approved sequence. No free/inherent helpers, own locks, empty behavior markers or orphan impls. Preserve SessionRecord and Codex SessionStart names. Tentative app-server notification types remain out of scope.

Psyche **rllq** ruled admitted actor/reply loss with unknown commit status gets its own outcome: ReportUncertain.ActorUnavailable or ConfigureUncertain.ActorUnavailable, never refusal or a claimed committed answer. The caller does not resend; read state afterward by Inspect/subscription. These source schemas are committed at ordinary54cbda97402267efa182eab2ac979fa0459958ee and meta4ee447e94d737557d137b423f1c8bddb7bbd4898. Ordinary defines one ActorUnavailable.String scalar newtype, imported by meta and reused by uncertain/opening/refusal payloads; native diagnostic contents must be preserved by future projections. Generated success-output positions remain unchanged. Core/translator must preserve native admission/reply-loss distinction before projecting it. Open handshake question **4y1e** to Core/shared owner: contract ETHOS currently includes only signal.ethos, not new internal library schema/imported definitions; accepted transitive identity mechanism is unknown. Do not invent a shared fingerprint protocol.

## Native budget prerequisite and strict metadata hold

Core granted exact isolated source from published translator **2739d586e1455a001661fc85a8a61b6219aa99df**, not events WIP. Fresh remote audit found origin/main exactly at accepted base; canonical local main diverges and was ignored. Own source **5873b662** changes only native TextBudgeting for ValidTextBudget returning *self, named serving fixture, and serving0.3.0->0.3.1. Dependency declarations/root/client versions unchanged. Core ex6u independently SOURCEPASSed this exact diff/version proposal.

Packet `/tmp/translator-budget-713b44.RfmtVR/native-budget-source-packet.md`; independent Core audit `/tmp/translator-budget-source-audit.jQdRLB/report.md`.

Proposed metadata packet `/tmp/translator-budget-metadata-request-revised.21Do6J/j0uc-bounded-metadata-request.md` is **HELD, START NONE**. Core3otc conditional grant was narrowed by u3xz: max-jobs0/builders-empty is not a proven strict no-build guarantee (preferLocalBuild); **no Nix shell or tool realization**. Require already-realized exact pinned executable store paths/closures/provenance, invoked directly, or separate cache-copy admission. No tool lookup/realization/generation actually started.

Field hl6p has no accepted cargo/toolchain/patched-crate2nix0.15.0 paths/provenance for locked build-base **dc7c8e7a727cf0def64bbfa22b2115adbf7864e8**; treat UNKNOWN/MISSING. User-unit CPU2/MemoryMax4GiB/RuntimeMax900/KillModecontrolgroup enforcement also unestablished. No PID/logdir/reservation exists. Field verifies only li@prometheus uid1001/gid100 and private mktemp700; its native-matrix custody is not global competing-job clearance. Core notifiedc1cb. Obtain fresh phase/serial slot and enforceable unit plus owned PID/logdir BEFORE announced START to Core and Field. One generation-only phase would allow expected Cargo.lock/Cargo.nix serving0.3.1 delta only, hashes unchanged; unexpected diff stops. Preserve evidence and clean only owned exact processes/scratch. No pub/registry/consumer pins/gates are granted.

Final consumer pin must be the eventual accepted published metadata-inclusive commit, not stale-lock source5873b662. All serving, belief, capsule, Harness and Harness-tests immutable whole gates remain owed; old root/client registrations are preserved. Subscription owner was informed of isolated source work but received no adoption pin.

## Flow consumer and shared dependency boundaries

Mind harnessEvents Sol confirmed snapshot/delta agreement: Subscribe returns fresh snapshot before ordered changes; Observed includes Tokens; ContextSize drives context deltas, Compacted/Ended remain events; disconnect implies no rest. Flow reads no rollout. Subscription payloads unchanged: Subscribed.Stream<Observations Changed>, Changed.Transition.{FlowId Event State} plus Malformed. Flow owns harness-independent transitions/reconnect; producer owns observation/folding/duplicate TurnEnded suppression.

Flow side branch last reported `/git/worktrees/flow-harness-events-e73b30`, fe5a6930871707a7086c9a647867a519734220ef, lock435; later successors7d3036/3db748 may have advanced it. Ask its current address, not an assumed source head. It owns Blocked mapping and reconnect rest/cooling semantics ruled by Psyche yeur; no producer payload change requested.

Current direct flow-ethos pin in library/ordinary is **062ef9e14abbf6552b257e9ce7e1c22f5bc00c27**, FlowId.String at crates/flow-ethos/ethos/library.ethos; meta reaches it transitively. Final nominal FlowId identity against Flow consumer is NOT AGREED. Core query **wipa** asks accepted target revision/version; no arbitrary pin advance. Identifiable/identify remain deferred by gcyd; ClaimIdentity remains, no new hash/Identifier.

Shared **f2wj remains unaccepted**: subscription owner76b588, no exact accepted release packet supplied. Never adopt old events WIP be5. PRE-METADATA inventory `/tmp/tmp.Jh69A0iBlk/Harness-source-dependency-plan.md` records older intermediate heads/pins/features; update from this checkpoint plus subsequent source work before proposing final coherent pins. Accepted earlier build-base7fca4d583adfd2354903c59cbc7f5e928e1baa76 registered Kameo0.22.2/macros0.21.1; do not assume a newer accepted registry.

Next complete chain: finish source actor/daemon/translator/tests -> exact committed coherent dependency/type-identity packet to Core/FlowEvents -> separately granted metadata/registry/publication phases -> immutable builder whole gates on published commits -> independent release audit arranged by Psyche -> Field deployment. Mind harnessNexus Opus remains HELD; do not wake it. Keep3kyf/daxc open until their real acceptance conditions are met.
