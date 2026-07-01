# Implementation Plan

## Goal
Replace `lojix-run` and legacy Lojix request vocabulary with a direct, typed, non-legacy Lojix deploy/observe interface, updating all public schemas, runtime code, tests, docs, and consumers without wrappers or compatibility translation.

## Evidence-backed Observations

### Spirit and doctrine observations
- Public Spirit already contains the broad rule needed here: record `10pz` says, “Design replaceably, not additively: do not preserve an older shape for backward-compatibility's sake when it manufactures legacy”; evidence: `agent-outputs/ReplaceableDesignIntent/IntentMaintainer-ReplaceableDesignRecord.md:49-61`.
- Workspace architecture says backward compatibility is not a constraint for systems being born and should bind only at explicitly declared boundaries; evidence: `ARCHITECTURE.md:63-75`.
- I did not find a public Lojix-specific Spirit record for “delete `lojix-run` and forbid direct legacy deploy syntax.” Proposed wording for later capture if desired: “Lojix deploy interfaces must be direct typed contracts, not wrappers or compatibility translators; delete legacy request syntax and update consumers rather than preserving `lojix-run`, `FullOs`, `OsOnly`, `HomeOnly`, or wrapper-era reporting paths.”

### Current surfaces carrying legacy names, compatibility concepts, or wrapper assumptions
- `signal-lojix/schema/lib.schema` still exposes the public deployment discriminator as `DeploymentKind [FullOs OsOnly HomeOnly]`, uses it in `Generation`, and allows filtering by it in `NodeSelector`; evidence: `signal-lojix/schema/lib.schema:63-93`.
- `signal-lojix/src/schema/lib.rs` is the generated Rust surface carrying the same enum and field names; evidence: `signal-lojix/src/schema/lib.rs:168-171`, `:270-295`.
- `meta-signal-lojix/schema/lib.schema` explicitly frames the deploy surface as reconstructing legacy `lojix-cli` syntax and preserves `FullOs/OsOnly/HomeOnly`, `SystemAction`, `HomeMode`, and `Deployed AcceptedDeploy`; evidence: `meta-signal-lojix/schema/lib.schema:27-34`, `:60-70`, `:94`, `:107-128`, `:134-146`.
- `meta-signal-lojix/src/schema/lib.rs` is generated from that schema and carries `HomeMode`, `deployment_kind`, `system_action`, `home_mode`, `Deployed`, and `AcceptedDeploy`; evidence: `meta-signal-lojix/src/schema/lib.rs:165-213`, `:257-265`, `:461-470`.
- `meta-signal-lojix/tests/round_trip.rs` and `tests/frame.rs` use `DeploymentKind::OsOnly`, `SystemAction::Eval`, and assert `(Deployed ...)` output; evidence: `meta-signal-lojix/tests/round_trip.rs:15-28`, `:47-96`; `meta-signal-lojix/tests/frame.rs:12-23`, `:42-51`.
- `lojix/schema/nexus.schema` keeps internal materialization names `FullOs` and `OsOnly`, imports `DeploymentKind`, `SystemAction`, and `HomeMode`, and preserves the home/system split as `ActivationProfile [(System SystemAction) (Home HomeActivationProfile)]`; evidence: `lojix/schema/nexus.schema:61-90`.
- `lojix/schema/sema.schema` persists `DeploymentKind`, imports `AcceptedDeploy`, has event-log read types that are not exposed correctly by ordinary `Query`, and writes `DeploySubmitted AcceptedDeploy`; evidence: `lojix/schema/sema.schema:33`, `:48`, `:57-60`, `:66-73`, `:85`.
- `lojix/src/schema_runtime.rs` translates home deploys into `DeploymentKind::HomeOnly`, maps old public kinds into `MaterializationShape`, defaults missing active deploys to `FullOs`, and maps `FullOs`/`OsOnly` to booleans; evidence: `lojix/src/schema_runtime.rs:920-939`, `:1010-1017`, `:2037-2055`, `:2465-2467`, `:3341-3357`.
- `lojix/src/schema_runtime.rs` currently resolves a flake revision but then ignores the resolved payload when continuing the pipeline; evidence: resolution creation at `lojix/src/schema_runtime.rs:2817-2834` and ignored payload at `:2843-2854`.
- `lojix/src/schema_runtime.rs` has first-class system and home activation code, so wrapper fallback/postchecks are not the right deploy substrate; evidence: system activation `lojix/src/schema_runtime.rs:3750-3810`, home activation `:4001-4056`.
- `lojix/src/schema_runtime.rs` contains a real `read_event_log`, but ordinary `Query` routes all non-`ByTestRun` selections to generation reads, and `ByEventLog` matches all generations instead of returning event-log data; evidence: `lojix/src/schema_runtime.rs:1531-1541`, `:2737-2751`, `:2770-2795`.
- `lojix/src/bin/meta-lojix.rs` comments omit current `Test` even though the meta schema exposes it, and still name the reply as a single printed reply rather than an admission/status procedure; evidence: `lojix/src/bin/meta-lojix.rs:1-6`, `meta-signal-lojix/schema/lib.schema:60-78`.
- `lojix/ARCHITECTURE.md`, `README.md`, and `skills.md` still describe parity with or coexistence beside legacy `lojix-cli`; evidence: `lojix/ARCHITECTURE.md:43-47`, `:287-288`; `lojix/README.md:28-30`; `lojix/skills.md:65-68`.
- `lojix/tests/*` fixtures hard-code `DeploymentKind::OsOnly`, `Deployed`, and old materialization names; evidence: `lojix/tests/engine_routing.rs:140-174`, `:191-225`; `lojix/tests/horizon_materialization_contract.rs:23-28`; `lojix/tests/build_smoke.rs:56-113`; `lojix/tests/durable_resume.rs:29-31`; `lojix/tests/deploy_job_survival.rs:33-35`.
- `CriomOS-home/packages/lojix-run/lojix-run.py` is a wrapper with a hand parser, legacy-head translator, exact-ref rewriting, `meta-lojix` subprocess invocation, root home fallback, non-fatal postchecks, Niri mutation, pi symlink checks, and chat/report log summaries; evidence: `CriomOS-home/packages/lojix-run/lojix-run.py:21-58`, `:65-120`, `:123-188`, `:196-243`, `:250-320`, `:322-394`, `:397-428`, `:430-539`, `:541-615`.
- `CriomOS-home/packages/lojix-run/default.nix`, `checks/lojix-run/default.nix`, `flake.nix`, and `modules/home/profiles/min/default.nix` package, test, expose, and install `lojix-run`; evidence: `CriomOS-home/packages/lojix-run/default.nix:1-30`; `CriomOS-home/checks/lojix-run/default.nix:1-69`; `CriomOS-home/flake.nix:356-357`; `CriomOS-home/modules/home/profiles/min/default.nix:264-267`.
- `CriomOS-home/skills.md` recommends `lojix-run`, legacy `HomeOnly ... Activate`, `FullOS`, exact-ref wrapper behavior, postchecks, and wrapper redaction as current operating procedure; evidence: `CriomOS-home/skills.md:185-229`.
- `CriomOS-home/RISK.md` still names the authorized `lojix-run` / `meta-lojix` activation path; evidence: `CriomOS-home/RISK.md:68-70`.
- Generated operating-system doctrine still teaches direct `meta-lojix` but with legacy `FullOs`, `OsOnly`, `HomeOnly` concepts and `(Deployed ...)` admission wording; evidence: `skills/modules/operating-system-operations/full.md:11-35`; `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md:16-40`.
- `CriomOS` current docs still direct operators to `lojix-cli` and contain old deploy syntax; evidence: `CriomOS/README.md:3-29`, `CriomOS/docs/GUIDELINES.md:256-272`. Historical `CriomOS/reports/*` also contain old names, but treat those as archival unless the implementation scope explicitly includes report cleanup.

## Recommended Non-legacy Vocabulary and Request Shapes

Use current domain semantics, not old compatibility names.

1. Replace public `DeploymentKind [FullOs OsOnly HomeOnly]` with two explicit concepts:
   - `HostComposition [CompleteHost BaseHost]`
     - `CompleteHost`: host system closure with embedded home environment and all-firmware input materialization.
     - `BaseHost`: host system closure without embedded home environment and without broad all-firmware materialization.
   - `GenerationArtifact [CompleteHost BaseHost UserEnvironment]`
     - Used for live-generation records and query filters. `UserEnvironment` replaces the old `HomeOnly` record concept but is justified as the artifact that Home Manager activation produces.
2. Replace `SystemDeployment` / `HomeDeployment` request names only if the team accepts the clearer domain names:
   - Recommended: `DeployRequest [(Host HostDeploy) (UserEnvironment UserEnvironmentDeploy)]`.
   - Acceptable if the team wants smaller churn: keep top-level `(System ...)` and `(Home ...)` because the split is a current artifact/effect split, not a compatibility translation. If retained, still replace `FullOs`, `OsOnly`, and `HomeOnly`.
3. Replace deploy actions and modes with names that describe effects:
   - `HostDeployAction [Evaluate Realize SetBootProfile ActivateNow TestActivation ScheduleBootOnce]`
     - Maps from old `Eval`, `Build`, `Boot`, `Switch`, `Test`, `BootOnce`.
   - `UserEnvironmentAction [Realize SetProfile ActivateNow]`
     - Maps from old home `Build`, `Profile`, `Activate`.
   - Replace public `ActivationKind` with `ActivationEffect [BootProfile LiveActivation TestActivation BootOnceProfile ProfileOnly]` or an equivalent generation-effect enum. Do not keep `Switch` as the public generic name unless it is explicitly scoped to NixOS switch-to-configuration semantics.
4. Replace admission output names:
   - `Deployed AcceptedDeploy` becomes `DeployAccepted DeployHandle` or `DeployAccepted DeployAdmission`.
   - The payload remains deployment id + marker, but the head must not imply terminal build/copy/activation success.
5. Replace event/status queries so reporting is typed, not wrapper text:
   - Add an ordinary output that can carry event-log pages, e.g. `DeploymentEventsQueried EventLogPage`, or make `QueryResult [(Generations GenerationListing) (DeploymentEvents EventLogPage) (TestRuns TestRunListing)]`.
   - Keep `WatchDeployments` if it is domain-correct, but ensure one-shot event-log reads work through `lojix`.
6. Add explicit source revision policy instead of hidden exact-ref rewriting:
   - Required field on deploy requests, e.g. `SourceRevisionPolicy [RequireImmutable ResolveAndRecord]`.
   - `RequireImmutable` rejects mutable branch-like refs for effect-bearing deploys.
   - `ResolveAndRecord` resolves before build, records the exact revision/ref in durable deployment state/events, and uses the resolved ref for the build path.

## Former `lojix-run` Behavior Disposition

- Legacy `(FullOs ...)`, `(OsOnly ...)`, `(HomeOnly ...)` translation: direct Lojix use after schema rename; delete translator and do not reintroduce legacy heads anywhere.
- Builder normalization: direct typed request; operators write `None` or `(Some <builder-node>)` according to the generated schema.
- Legacy substituter handling: direct typed `Vec ExtraSubstituter`; add docs/tests for non-empty values if needed, but no host-label shorthand.
- One argument inline/file handling: already handled by `lojix`/`meta-lojix` via `ComponentArgument`; use `.nota` request files for text requests.
- `meta-lojix` subprocess invocation: delete; call `meta-lojix` directly.
- Exact local branch rewriting: replace with explicit operator exact refs or first-class Lojix `SourceRevisionPolicy`; no silent local checkout probing.
- Run directories, line counts, hashes, redacted failure tails: replace with typed `DeployAccepted` plus `lojix` status/event queries and operator redaction helpers. Do not add another wrapper for summaries.
- Store-path stdout inference: delete. `meta-lojix` replies with typed admission, not a raw closure path.
- Root home fallback: delete. If root-assisted home activation is genuinely needed, model it as an explicit Lojix privilege/activation strategy and make failure typed/fatal.
- System/home postchecks: deploy-critical profile/live-state verification belongs inside Lojix activation effects before generation commit; non-critical task checks belong in explicit operator procedure.
- Niri reload: explicit operator procedure after home activation; do not hide as deploy side effect.
- `/home/$user/.pi/agent/packages/pi-continue` symlink check: delete with no Lojix replacement.
- Wrapper environment overrides `LOJIX_RUN_*`: delete with wrapper; use existing `LOJIX_ORDINARY_SOCKET` / `LOJIX_OWNER_SOCKET` only where current clients need socket selection.

## Tasks

1. **Freeze the vocabulary decision before editing schemas**
   - File: design alignment artifact or issue, not code.
   - Changes: Confirm whether top-level deploy variants become `(Host ...)` / `(UserEnvironment ...)` or retain `(System ...)` / `(Home ...)` with renamed internals. Confirm exact final enum names from the recommendation above.
   - Acceptance: A single approved vocabulary table maps old names to new names and states which concepts are retained for current domain semantics.

2. **Replace ordinary signal schema names and query output shapes**
   - File: `signal-lojix/schema/lib.schema`
   - Changes: Replace `DeploymentKind [FullOs OsOnly HomeOnly]` with `GenerationArtifact [CompleteHost BaseHost UserEnvironment]` or the approved names. Update `Generation`, `NodeSelector`, and any query/event types. Add an event-log output shape so `ByEventLog` does not pretend to return `GenerationListing`.
   - Acceptance: Schema text contains no `FullOs`, `OsOnly`, or `HomeOnly`; ordinary query can represent generation queries, event-log reads, and test-run reads without overloading one output incorrectly.

3. **Regenerate and update signal-lojix generated Rust and tests**
   - File: `signal-lojix/src/schema/lib.rs`
   - File: `signal-lojix/tests/round_trip.rs`
   - File: `signal-lojix/tests/frame.rs`
   - Changes: Regenerate generated Rust through the repo’s schema build process; update tests for the renamed artifact/filter/output shapes.
   - Acceptance: `rg 'FullOs|OsOnly|HomeOnly|DeploymentKind' signal-lojix` returns no old public names except migration notes if intentionally kept outside shipped docs; signal-lojix tests pass.

4. **Replace meta deploy schema names and admission wording**
   - File: `meta-signal-lojix/schema/lib.schema`
   - Changes: Delete legacy provenance language; import/use the new ordinary artifact/composition and action names. Rename `HomeMode`, `SystemAction` usage, `Deployed AcceptedDeploy`, and `AcceptedDeploy` to `DeployAccepted DeployHandle` or approved equivalents. Add required `SourceRevisionPolicy` or approved exact-ref policy field to deploy requests.
   - Acceptance: Schema has no legacy compatibility comments, no `FullOs`/`OsOnly`/`HomeOnly`, no output head `Deployed` for admission, and no optional/defaulted exact-ref behavior.

5. **Regenerate and update meta-signal generated Rust and contract tests**
   - File: `meta-signal-lojix/src/schema/lib.rs`
   - File: `meta-signal-lojix/tests/round_trip.rs`
   - File: `meta-signal-lojix/tests/frame.rs`
   - Changes: Regenerate generated Rust; update fixtures to use `CompleteHost`/`BaseHost`, new action names, new `DeployAccepted` output, and exact-ref policy.
   - Acceptance: `rg 'FullOs|OsOnly|HomeOnly|Deployed|AcceptedDeploy|HomeMode|SystemAction' meta-signal-lojix` returns no old public deploy vocabulary except if `SystemAction` remains only as a deleted-name note in test comments, which should be avoided.

6. **Update Lojix internal schemas to the new names**
   - File: `lojix/schema/nexus.schema`
   - File: `lojix/schema/sema.schema`
   - Changes: Rename `MaterializationShape [FullOs OsOnly (Home ...)]`, `ActivationProfile`, `NixEvalCommand` fields, `LiveGeneration`, deploy submission/output imports, and event-log read/write types to match the new contracts.
   - Acceptance: Lojix internal schemas compile/regenerate and no longer import or persist old public names.

7. **Update Lojix runtime deploy pipeline**
   - File: `lojix/src/schema_runtime.rs`
   - Changes: Replace home submission’s synthetic `DeploymentKind::HomeOnly` with `GenerationArtifact::UserEnvironment`. Replace materialization mapping with `HostComposition::CompleteHost` / `BaseHost`. Replace action/mode matches with new effect names. Preserve the current first-class activation behavior, but with new typed names.
   - Acceptance: Grep for old names in `lojix/src/schema_runtime.rs` is empty; unit tests prove CompleteHost includes home/all firmware and BaseHost excludes embedded home/broad all firmware.

8. **Make exact reference handling first-class**
   - File: `lojix/src/schema_runtime.rs`
   - File: `lojix/schema/nexus.schema`
   - File: `lojix/schema/sema.schema`
   - Changes: Use the resolved flake payload instead of ignoring it; record requested ref, resolved revision/ref, and policy in deployment state/events. Reject mutable refs under `RequireImmutable` if that policy is selected.
   - Acceptance: Tests show `ResolveAndRecord` records and builds from a resolved revision, and `RequireImmutable` rejects mutable branch refs. No client-side local checkout probing exists.

9. **Fix typed deployment reporting/observation**
   - File: `lojix/src/schema_runtime.rs`
   - File: `signal-lojix/schema/lib.schema`
   - New File: `lojix/tests/event_log_query.rs` if no suitable test file exists.
   - Changes: Route `Selection::ByEventLog` to `SemaReadInput::ReadEventLog`; map `SemaReadOutput::EventLogRead` to the new ordinary output shape. Keep `DeployAccepted` as admission only, and document/query terminal status via events/generation reads.
   - Acceptance: A test records deployment phase events and verifies `lojix` ordinary query returns those events, not an unrelated generation listing.

10. **Make deploy-critical verification fatal inside Lojix or document it as manual**
    - File: `lojix/src/schema_runtime.rs`
    - File: `lojix/tests/engine_routing.rs` or new focused activation tests.
    - Changes: If system profile/current-system or home profile verification is required for correctness, perform it inside activation effects before `GenerationActivated`. If not required, document explicit operator checks and do not model them as non-fatal postchecks.
    - Acceptance: There is no non-fatal postcheck equivalent. Deploy-critical mismatch fails the deploy pipeline or is explicitly out-of-band documentation.

11. **Rename admission output throughout Lojix daemon/client/tests**
    - File: `lojix/src/daemon.rs`
    - File: `lojix/src/schema_runtime.rs`
    - File: `lojix/src/bin/meta-lojix.rs`
    - File: `lojix/tests/deploy_job_survival.rs`
    - File: `lojix/tests/build_smoke.rs`
    - File: `lojix/tests/engine_routing.rs`
    - Changes: Replace `Deployed`/`AcceptedDeploy` semantics with `DeployAccepted`/`DeployHandle` names. Update comments so they say admission occurs before pipeline completion.
    - Acceptance: Tests assert `DeployAccepted` for admission and separately assert terminal events/generation state when applicable.

12. **Delete `lojix-run` from CriomOS-home**
    - File: `CriomOS-home/packages/lojix-run/lojix-run.py`
    - File: `CriomOS-home/packages/lojix-run/default.nix`
    - File: `CriomOS-home/checks/lojix-run/default.nix`
    - File: `CriomOS-home/flake.nix`
    - File: `CriomOS-home/modules/home/profiles/min/default.nix`
    - Changes: Remove the wrapper package, source, check attr, and installed package entry. Do not replace it with a new wrapper package.
    - Acceptance: `command -v lojix-run` is not provided by the home profile, `rg 'lojix-run' CriomOS-home` has no live package/check/doc references except historical reports if intentionally excluded.

13. **Update CriomOS-home operator docs and risk note**
    - File: `CriomOS-home/skills.md`
    - File: `CriomOS-home/RISK.md`
    - Changes: Replace wrapper instructions with direct `meta-lojix` submission, `lojix` event/generation query, explicit redaction helper usage, explicit Niri reload procedure, and no legacy `HomeOnly` syntax.
    - Acceptance: Docs contain no `lojix-run`, no `HomeOnly`, and no wrapper-based exact-ref/postcheck/reporting advice.

14. **Update generated operating-system doctrine at the source**
    - File: `skills/modules/operating-system-operations/full.md`
    - Generated File: `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md` after regeneration, if this workspace owns generated outputs.
    - Changes: Replace old direct examples with the new `meta-lojix` request shapes, new action names, exact-ref policy, and `DeployAccepted` admission warning.
    - Acceptance: Generated doctrine has no `FullOs`, `OsOnly`, `HomeOnly`, or `(Deployed ...)` admission wording.

15. **Update Lojix docs**
    - File: `lojix/ARCHITECTURE.md`
    - File: `lojix/README.md`
    - File: `lojix/skills.md`
    - Changes: Remove parity-with-legacy framing that is now complete or misleading. Document direct contract shapes, owner/ordinary socket split including `Test` if still present, admission/status semantics, exact-ref policy, and no-wrapper reporting.
    - Acceptance: Docs do not direct readers to legacy `lojix-cli` or imply compatibility preservation. Any mention of `lojix-cli` is historical retirement context only, not current procedure.

16. **Update current CriomOS consumer docs**
    - File: `CriomOS/README.md`
    - File: `CriomOS/docs/GUIDELINES.md`
    - File: `CriomOS/modules/nixos/metal/default.nix`
    - Changes: Replace `lojix-cli`, old examples, and `OsOnly/home-off` comments with the new direct Lojix terms. Do not rewrite historical reports unless separately scoped.
    - Acceptance: Current docs/comments no longer teach `lojix-cli`, `FullOs`, `OsOnly`, or `HomeOnly` as current deploy surface.

17. **Run cross-repo validation**
    - File: all touched repos.
    - Changes: No code change beyond prior tasks; run validation.
    - Acceptance: Expected validation evidence includes `cargo test` for `signal-lojix`, `meta-signal-lojix`, and `lojix`; schema generation checks; `nix flake check` for `CriomOS-home` if feasible; targeted grep proving old vocabulary deletion; and docs grep proving no live wrapper instructions remain.

## Files to Modify
- `signal-lojix/schema/lib.schema` - replace public generation/deploy artifact names and event-log query output.
- `signal-lojix/src/schema/lib.rs` - regenerated schema Rust.
- `signal-lojix/tests/round_trip.rs` - update ordinary contract fixtures.
- `signal-lojix/tests/frame.rs` - update frame fixtures if output shapes change.
- `meta-signal-lojix/schema/lib.schema` - replace deploy request vocabulary, admission output, exact-ref policy, and delete legacy provenance comments.
- `meta-signal-lojix/src/schema/lib.rs` - regenerated schema Rust.
- `meta-signal-lojix/tests/round_trip.rs` - update deploy/admission fixtures.
- `meta-signal-lojix/tests/frame.rs` - update deploy/admission frame fixtures.
- `lojix/schema/nexus.schema` - update internal command/effect vocabulary.
- `lojix/schema/sema.schema` - update durable state/read/write vocabulary.
- `lojix/src/schema_runtime.rs` - update runtime mappings, exact-ref use, event-log routing, activation verification.
- `lojix/src/daemon.rs` - update admission output naming and comments.
- `lojix/src/bin/meta-lojix.rs` - update documented accepted meta verbs and admission wording.
- `lojix/tests/durable_resume.rs` - update generation artifact fixture names.
- `lojix/tests/deploy_job_survival.rs` - update admission and artifact names.
- `lojix/tests/build_smoke.rs` - update fixture deploys and `DeployAccepted` assertions.
- `lojix/tests/engine_routing.rs` - update action names and home/host deploy fixtures.
- `lojix/tests/horizon_materialization_contract.rs` - update materialization names and assertions.
- `lojix/ARCHITECTURE.md` - remove legacy framing and document new direct contract/status semantics.
- `lojix/README.md` - remove legacy `lojix-cli` current-role text.
- `lojix/skills.md` - remove legacy `lojix-cli` current-role text.
- `CriomOS-home/packages/lojix-run/lojix-run.py` - delete.
- `CriomOS-home/packages/lojix-run/default.nix` - delete.
- `CriomOS-home/checks/lojix-run/default.nix` - delete.
- `CriomOS-home/flake.nix` - remove `lojix-run` check attr.
- `CriomOS-home/modules/home/profiles/min/default.nix` - remove `lojix-run` package from deployment packages.
- `CriomOS-home/skills.md` - replace wrapper and legacy request instructions.
- `CriomOS-home/RISK.md` - remove authorized `lojix-run` activation path wording.
- `skills/modules/operating-system-operations/full.md` - update generated doctrine source.
- `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md` - regenerated doctrine output if in scope.
- `CriomOS/README.md` - update current deploy entrypoint examples.
- `CriomOS/docs/GUIDELINES.md` - update deploy guidance.
- `CriomOS/modules/nixos/metal/default.nix` - update `OsOnly/home-off` comment.

## New Files
- `lojix/tests/event_log_query.rs` - focused event-log query/status test, if no existing Lojix test file is a better home.

## Dependencies
- Task 1 blocks all schema edits.
- Tasks 2 and 4 must precede generated Rust/test updates in tasks 3 and 5.
- Tasks 2 through 6 must precede Lojix runtime/test updates in tasks 7 through 11.
- Task 9 depends on ordinary signal output changes from task 2 and SEMA schema updates from task 6.
- Task 12 should land after direct Lojix docs and minimum runtime/status replacement are ready, unless the team accepts a temporary gap where operators use raw `meta-lojix` plus manual `lojix` queries.
- Tasks 13 through 16 depend on the final request vocabulary from task 1 and should be updated in the same implementation slice as schema/runtime changes to avoid stale instructions.
- Task 17 depends on all implementation tasks.

## Risks
- Renaming wire schemas is intentionally breaking. Do not soften this with aliases, compatibility decoders, or legacy NOTA heads.
- `CompleteHost` / `BaseHost` names must be validated with the psyche/team before implementation; the names are recommended because they describe current materialization semantics better than `FullOs` / `OsOnly`.
- Event-log query repair may require a broader `signal-lojix` output redesign than expected because current `Output::Queried` only carries `GenerationListing`.
- Exact-ref policy can become another hidden wrapper if implemented as silent best-effort resolution. It must be explicit in the typed request and durable event/state.
- Root-assisted home activation may still be needed operationally. If so, model it explicitly in Lojix runtime; do not resurrect client-side fallback.
- Generated files may be owned by schema build tooling; implementers must regenerate rather than hand-edit generated Rust where applicable.
- Historical reports and archives contain many old names. This plan treats current docs/source/tests as in scope and archival cleanup as out of scope unless separately requested.

## Compatibility Temptations Not To Add
- No `lojix-run` successor wrapper.
- No parser that accepts `(FullOs ...)`, `(OsOnly ...)`, or `(HomeOnly ...)` anywhere.
- No aliases from old enum names to new enum names.
- No `Deployed` output as an admission synonym.
- No client-side local `jj` probing or branch-ref rewriting.
- No non-fatal postcheck summary that lets a failed verification keep a successful deploy status.
- No root fallback that mutates profiles after a failed Lojix deploy.
- No Niri reload, pi symlink probe, or agent-specific check as a generic Lojix deploy side effect.
- No host-label shorthand for substituters.
- No raw-log key=value reporting surface that competes with typed Lojix events/queries.
