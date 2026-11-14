# Lojix survey, appendix: full lists and transcripts

Companion to `lojix-survey.md` in this directory. Everything here is observed from origin/main of lojix (da0ad8a), signal-lojix (bd5d250), meta-signal-lojix (1b0aaeb) and ethos-zero (970459d), unless a line says it is inference.

## A. Method

- Every `struct`, `enum`, `type` and `trait` declaration, and every `runtime_text!`, `runtime_newtype!`, `flow_text!` and `flow_newtype!` invocation, was listed from each Rust file of the lojix workspace, stopping at the file's `#[cfg(test)]` module. Associated types inside traits and impls are not counted. That gives 545 declarations: 385 data types (380 structs, enums and newtypes, and 5 type aliases) and 160 traits.
- The three Ethos files of the Lojix graph (signal-lojix `ethos/signal.ethos`, meta-signal-lojix `ethos/signal.ethos`, lojix `ethos/ingress.ethos`) were generated with ethos-zero 28 (`/nix/store/383qv46b…-all-workspace-members/bin/ethos-zero`, built from `github:LiGoldragon/ethos-zero/970459d` on the remote builder). signal-lojix needed the three marker declarations rewritten as one-field structs first (section G). A hand type is a "wire twin" when its name equals a type that output declares.
- Shapes were compared field by field and variant by variant after normalising `std::` paths and treating `u64` and `i64` alike (the difference is noted per row).
- The stored closure is every type reachable by field from the ten runtime_model record families the store registers (lib.rs `LojixRecord` impls).

## B. Wire twins in runtime_model.rs and runtime_flow.rs

"Stored" marks a runtime_model type in the stored closure. "Same bytes" is inference from rkyv 0.8's layout rules: a one-field struct or newtype archives as its field, `u64` and `i64` archive as the same eight bytes for values below 2^63, and an enum's tag follows declaration order, so a reordered enum archives differently.

| file | type | wire crate | stored | shape against ethos-zero 28 output |
|---|---|---|---|---|
| runtime_model | ClusterName | signal-lojix | yes | same |
| runtime_model | NodeName | signal-lojix | yes | same |
| runtime_model | UserName | signal-lojix | yes | same |
| runtime_model | PinLabel | signal-lojix | yes | same |
| runtime_model | CommandProgram | signal-lojix | yes | same |
| runtime_model | CommandArgument | signal-lojix | yes | same |
| runtime_model | FailureDetail | signal-lojix | yes | same |
| runtime_model | ClosurePath | signal-lojix | yes | same |
| runtime_model | FlakeReference | signal-lojix | yes | same |
| runtime_model | NixStoreUri | signal-lojix | yes | same |
| runtime_model | SshDestination | signal-lojix | yes | same |
| runtime_model | FlakeAttribute | signal-lojix | yes | same |
| runtime_model | NixBuilderSpec | signal-lojix | yes | same |
| runtime_model | NixSystem | signal-lojix |  | same |
| runtime_model | ProposalSource | signal-lojix | yes | same |
| runtime_model | SecretsDirectory | signal-lojix | yes | same |
| runtime_model | ImmutableRevision | signal-lojix | yes | same |
| runtime_model | DeploymentOutputSelector | signal-lojix | yes | hand newtype, wire one-field struct (same bytes) |
| runtime_model | DeploymentIdentifier | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | GenerationIdentifier | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | TestRunIdentifier | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | SubscriptionToken | signal-lojix |  | same (hand u64, wire i64) |
| runtime_model | EventLogPosition | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | ExitCode | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | CommitSequence | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | StateDigest | signal-lojix | yes | same (hand u64, wire i64) |
| runtime_model | DatabaseMarker | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | AdmissionMarker | signal-lojix | yes | hand newtype, wire one-field struct (same bytes) |
| runtime_model | TerminalMarker | signal-lojix | yes | hand newtype, wire one-field struct (same bytes) |
| runtime_model | TransitionMarker | signal-lojix | yes | hand newtype, wire one-field struct (same bytes) |
| runtime_model | GenerationLookup | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | DeploymentLookup | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | SubscriptionClose | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | SubscriptionClosed | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | QuickCheck | meta-signal-lojix |  | same |
| runtime_model | RejectedWatch | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | RejectedDeploy | meta-signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_model | DeploymentTransport | signal-lojix | yes | same |
| runtime_model | DeploymentInputMode | signal-lojix | yes | same variants, different order |
| runtime_model | ActivationBackend | signal-lojix | yes | same variants, different order |
| runtime_model | TestExecutionProfile | signal-lojix |  | field names differ: optional_deployment_transport / deployment_transport_option |
| runtime_model | SecretsInput | signal-lojix | yes | same |
| runtime_model | SourceRevisionPolicy | signal-lojix | yes | same variants, different order |
| runtime_model | GenerationArtifact | signal-lojix | yes | same variants, different order |
| runtime_model | ActivationEffect | signal-lojix | yes | same variants, different order |
| runtime_model | GenerationSlot | signal-lojix | yes | same variants, different order |
| runtime_model | TestMode | signal-lojix | yes | same |
| runtime_model | TestRunPhase | signal-lojix | yes | same variants, different order |
| runtime_model | FailureStage | signal-lojix | yes | same variants, different order |
| runtime_model | TestOutcome | signal-lojix | yes | same |
| runtime_model | NodeSelector | signal-lojix |  | STRUCTURAL: wire holds RequestedGenerationArtifact (same variants as GenerationArtifact, other order); hand holds GenerationArtifact |
| runtime_model | EventLogRange | signal-lojix |  | field names differ: from / first_event_log_position, until / second_event_log_position |
| runtime_model | TestRunLookup | signal-lojix |  | field names differ: optional_test_run_identifier / test_run_identifier_option |
| runtime_model | Selection | signal-lojix |  | same variants, different order |
| runtime_model | Generation | signal-lojix |  | STRUCTURAL: wire closure path is Option<ClosurePath>; hand is ClosurePath (raise drops a non-canonical store path to None) |
| runtime_model | DeploymentEnvironment | signal-lojix | yes | same |
| runtime_model | RequestedDeploymentAction | signal-lojix | yes | same |
| runtime_model | DeploymentLifecycle | signal-lojix | yes | same variants, different order |
| runtime_model | DeploymentFailureStage | signal-lojix | yes | same variants, different order |
| runtime_model | DeploymentTerminalReason | signal-lojix | yes | same variants, different order |
| runtime_model | DeploymentFailure | signal-lojix | yes | field names differ: optional_failure_evidence / failure_evidence_option |
| runtime_model | FailureEvidence | signal-lojix | yes | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | FailedCommand | signal-lojix | yes | field names differ: optional_exit_code / exit_code_option |
| runtime_model | DeploymentTerminal | signal-lojix | yes | same variants, different order |
| runtime_model | DeploymentRequestIdentity | signal-lojix | yes | field names differ: optional_immutable_revision / immutable_revision_option |
| runtime_model | DeploymentRecord | signal-lojix | yes | field names differ: optional_admission_marker / admission_marker_option, optional_terminal_marker / terminal_marker_option, optional_deployment_terminal / deployment_terminal_option |
| runtime_model | GenerationListing | signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | DeploymentPhase | signal-lojix | yes | same variants, different order |
| runtime_model | DeploymentPhaseEvent | signal-lojix | yes | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | CacheRetentionTransition | signal-lojix | yes | same variants, different order |
| runtime_model | CacheRetentionTransitionEvent | signal-lojix | yes | field names differ: optional_generation_slot / generation_slot_option, optional_pin_label / pin_label_option |
| runtime_model | TestRunRecord | signal-lojix |  | field names differ: node / first_node_name, host / second_node_name, optional_closure_path / closure_path_option |
| runtime_model | TestRunListing | signal-lojix |  | same |
| runtime_model | DeploymentWatch | signal-lojix |  | field names differ: optional_deployment_identifier / deployment_identifier_option, optional_cluster_name / cluster_name_option, optional_node_name / node_name_option |
| runtime_model | CacheRetentionWatch | signal-lojix |  | field names differ: optional_cluster_name / cluster_name_option, optional_node_name / node_name_option |
| runtime_model | SubscriptionOpened | signal-lojix |  | same |
| runtime_model | HostDeployAction | signal-lojix | yes | same variants, different order |
| runtime_model | HostComposition | signal-lojix | yes | same |
| runtime_model | UserEnvironmentAction | signal-lojix | yes | same variants, different order |
| runtime_model | HostSelection | signal-lojix |  | same |
| runtime_model | NodeSelection | meta-signal-lojix |  | same variants, different order |
| runtime_model | TestRun | meta-signal-lojix |  | same |
| runtime_model | TestRequest | meta-signal-lojix |  | same |
| runtime_model | ExtraSubstituter | meta-signal-lojix | yes | field names differ: url / first_string, public_key / second_string |
| runtime_model | HostDeployment | meta-signal-lojix | yes | STRUCTURAL: hand carries horizon_definition_option inside (9th field); wire carries it beside, in ActualizedDeploySubmission |
| runtime_model | UserEnvironmentDeployment | meta-signal-lojix | yes | STRUCTURAL: hand carries horizon_definition_option inside (9th field); wire carries it beside, in ActualizedDeploySubmission |
| runtime_model | PinRequest | meta-signal-lojix |  | same |
| runtime_model | UnpinRequest | meta-signal-lojix |  | same |
| runtime_model | RetireRequest | meta-signal-lojix |  | same |
| runtime_model | DeployHandle | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | AcceptedTest | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | AppliedPin | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | AppliedUnpin | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | AppliedRetire | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | EventLogPage | signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | DeploySubmission | meta-signal-lojix | yes | same variants, different order |
| runtime_model | QueryRejectionReason | signal-lojix |  | same variants, different order |
| runtime_model | WatchRejectionReason | signal-lojix |  | same variants, different order |
| runtime_model | UnwatchRejectionReason | signal-lojix |  | same |
| runtime_model | RejectedQuery | signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | RejectedUnwatch | signal-lojix |  | same |
| runtime_model | PinRejectionReason | meta-signal-lojix |  | same variants, different order |
| runtime_model | UnpinRejectionReason | meta-signal-lojix |  | same variants, different order |
| runtime_model | RetireRejectionReason | meta-signal-lojix |  | same variants, different order |
| runtime_model | TestRejectionReason | meta-signal-lojix |  | same variants, different order |
| runtime_model | RefusedDeploy | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | DeployRefusalReason | meta-signal-lojix |  | same |
| runtime_model | RejectedPin | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | RejectedUnpin | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | RejectedRetire | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | RejectedTest | meta-signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | ConfigurationReceipt | signal-lojix |  | marker or flag wrapping and field names differ (same bytes at this level) |
| runtime_model | ConfigurationRejectionReason | signal-lojix |  | same |
| runtime_model | ConfigurationRejection | signal-lojix |  | field names differ: reason / configuration_rejection_reason |
| runtime_model | Input | signal-lojix |  | name only: hand root unrelated to the wire root (unused) |
| runtime_model | Output | signal-lojix |  | name only: hand root unrelated to the wire root (unused) |
| runtime_flow | NixStoreUri | signal-lojix |  | same |
| runtime_flow | SshDestination | signal-lojix |  | same |
| runtime_flow | FlakeAttribute | signal-lojix |  | same |
| runtime_flow | NixBuilderSpec | signal-lojix |  | same |
| runtime_flow | NixSystem | signal-lojix |  | same |
| runtime_flow | DeploymentOutputSelector | signal-lojix |  | hand newtype, wire one-field struct (same bytes) |
| runtime_flow | DeploymentTransport | signal-lojix |  | same |
| runtime_flow | DeploymentInputMode | signal-lojix |  | same variants, different order |
| runtime_flow | ActivationBackend | signal-lojix |  | same variants, different order |
| runtime_flow | ExtraSubstituter | meta-signal-lojix |  | field names differ: url / first_string, public_key / second_string |
| runtime_flow | TestExecutionProfile | signal-lojix |  | field names differ: optional_deployment_transport / deployment_transport_option |
| runtime_flow | Input | signal-lojix |  | name only: hand root unrelated to the wire root (unused) |
| runtime_flow | Output | signal-lojix |  | name only: hand root unrelated to the wire root (unused) |

Totals for runtime_model.rs: 114 twins (77 derived, 37 macro newtypes) plus `Input` and `Output`, whose names meet the generated roots by accident. Of the 114: 45 agree in shape at their own level (every integer newtype differs as `u64` against `i64`), 25 have the same variants in another order, 13 differ only in field names, 11 are a hand newtype against a generated one-field struct, 16 differ only by marker or flag wrapping and field names, and 4 differ in structure (NodeSelector, Generation, HostDeployment, UserEnvironmentDeployment).

## C. The other wire twins

| file | type | generated twin | shape |
|---|---|---|---|
| src/lib.rs | TestDefaults | signal-lojix TestDefaults | different: `cluster`, `default_vm_host`, `default_mode`, `test_flake`, `test_nix_system`, `test_output_selector` as bare `String`, then `horizon_definition`; the legacy startup archive's shape |
| src/lib.rs | TestMode | signal-lojix TestMode | same variants, same order; doc comment calls it "a daemon-local mirror" |
| src/schema_runtime.rs | TestDefaults | signal-lojix TestDefaults | runtime projection, converted by `impl From<&signal_lojix::TestDefaults>` (line 1351) |
| src/bootstrap.rs | 18 Bootstrap* types | lojix ingress.ethos | 9 same, 9 differ only in field names (hand drops the `bootstrap_` prefix); converted by `impl From<ingress::BootstrapRequest> for BootstrapRun` |

bootstrap.rs also holds a third layer of the same request, 13 `*Validated` types (ValidatedBootstrapRun, BootstrapModeValidated, BootstrapBootOnceValidated, BootstrapInputValidated, BootstrapDirectInputValidated, BootstrapHorizonInputValidated, BootstrapSecretsInputValidated, BootstrapTestPlanValidated, BootstrapHermeticTestValidated, BootstrapActivationBackendValidated, BootstrapRemoteBackendValidated, BootstrapSshPolicyValidated, BootstrapLocalBackendValidated).

runtime_flow.rs repeats 11 wire names a second time inside lojix (a third copy counting the wire): NixStoreUri, SshDestination, DeploymentTransport, DeploymentInputMode, FlakeAttribute, DeploymentOutputSelector, ActivationBackend, NixBuilderSpec, NixSystem, ExtraSubstituter, TestExecutionProfile. Its macros derive no rkyv.

## D. The stored closure

84 types are reachable from the ten runtime_model families; 61 of them are wire twins and 23 are Lojix's own.

- Own (23): ContainerLifecycleRecord, ContainerName, ContainerState, DeployJob, DeployJobPhase, DeployResumeStage, DeploymentOutboxRecord, EventLogEntry, GcRoot, IdentifierAllocation, LiveGeneration, LoggedEvent, OutboxDeliveryState, OutboxRetryCount, PendingTransitionIntent, PersistedFlakeInputOverride, PersistedFlakeInputReference, PhaseReceipt, SourceRevisionRecord, StateMarker, StoredTestRun, TransitionIntentState, TransitionOrdinal.
- Twins (61): ActivationBackend, ActivationEffect, AdmissionMarker, CacheRetentionTransition, CacheRetentionTransitionEvent, ClosurePath, ClusterName, CommandArgument, CommandProgram, CommitSequence, DeploySubmission, DeploymentEnvironment, DeploymentFailure, DeploymentFailureStage, DeploymentIdentifier, DeploymentInputMode, DeploymentLifecycle, DeploymentOutputSelector, DeploymentPhase, DeploymentPhaseEvent, DeploymentRecord, DeploymentRequestIdentity, DeploymentTerminal, DeploymentTerminalReason, DeploymentTransport, EventLogPosition, ExitCode, ExtraSubstituter, FailedCommand, FailureDetail, FailureEvidence, FailureStage, FlakeAttribute, FlakeReference, GenerationArtifact, GenerationIdentifier, GenerationSlot, HostComposition, HostDeployAction, HostDeployment, ImmutableRevision, NixBuilderSpec, NixStoreUri, NodeName, PinLabel, ProposalSource, RequestedDeploymentAction, SecretsDirectory, SecretsInput, SourceRevisionPolicy, SshDestination, StateDigest, TerminalMarker, TestMode, TestOutcome, TestRunIdentifier, TestRunPhase, TransitionMarker, UserEnvironmentAction, UserEnvironmentDeployment, UserName.
- Of those twins, 17 enums carry their variants in another order on the wire: ActivationBackend, ActivationEffect, CacheRetentionTransition, DeploySubmission, DeploymentFailureStage, DeploymentInputMode, DeploymentLifecycle, DeploymentPhase, DeploymentTerminal, DeploymentTerminalReason, FailureStage, GenerationArtifact, GenerationSlot, HostDeployAction, SourceRevisionPolicy, TestRunPhase, UserEnvironmentAction.
- Foreign types in the closure: `horizon_lib::HorizonDefinition` (inside HostDeployment and UserEnvironmentDeployment, inside DeployJob) and, through lib.rs's NexusConfigurationRecord, `nexus::ConfigurationState<signal_lojix::LojixNexusConfiguration>` with its `Option<HorizonDefinition>`.
- StoredTestRun has exactly the fields of the hand TestRunRecord, a twin inside the hand model.

## E. Lists by category (data types only)

Store records that are not wire twins (37):
- runtime_model.rs (23): the "own" list in D.
- lib.rs (2): NexusConfigurationRecord (family `nexus-configuration`); LegacyStartupConfiguration (the rkyv startup archive named by `LOJIX_CONFIGURATION`, read by lojix-reset-store and lojix-migrate-configuration, written by lojix-write-configuration).
- quarantine.rs (2): QuarantinedRow (family `quarantined-row`, holds the original row bytes as `Vec<u8>`); UnreadRow (an empty record used only to retract an unreadable row).
- bootstrap.rs (10, rkyv, the bootstrap journal and evidence files): BootstrapEvidenceStatus, BootstrapEvidenceMode, BootstrapEffectStage, BootstrapEffectEvidence, BootstrapTerminalEvidence, JournalStage, JournalEventKind, JournalEvent, JournalFlakeOverride, BootstrapJournalConfiguration.

Operation and decision state (44):
- runtime_model.rs (14): MemoryReadInput, MemoryReadOutput, MemoryWriteInput, MemoryWriteOutput, ActivationCommit, ContainerTransition, AppliedActivation, ContainerReceipt, RejectionReport, RejectionReason, OrdinaryIngress, OrdinaryEgress, MetaIngress, MetaEgress.
- runtime_flow.rs (8): SignalInput, SignalOutput, NexusWork, NexusAction, OriginRoute, Nexus<Root>, NexusRunnerAdapter, NexusRunnerNextStep (alias); plus the traits Routable, Routed, NexusEngine.
- schema_runtime.rs (14): SchemaRuntime, RuntimeConfiguration, MetaOperation, ResolvedTestRun, TestPipeline, TestStage, TestSubmissionOutcome, ClusterProjection, DeploySubmissionOutcome, DeployPipeline, DeployStage, DeployAction, DeployJobResumption, meta::DeployRejectionReason.
- daemon.rs (8): WatchTurn, ListenerRole, RequestWorker, DeployJobs, AdmitDeploy, DeployAdmission, DeployCompleted, ReconcilePersistedJobs.

Emission, the shapes of external calls (77):
- runtime_flow.rs (33): EffectCommand and its ten commands (FlakeAuthRequest, HorizonMaterializationCommand, NixEvalCommand, NixBuildCommand, CopyClosureCommand, ActivateGenerationCommand, PathInfoGcCommand, HermeticCheckCommand, BringUpTestVmCommand, TearDownTestVmCommand); EffectResult and its results (ResolvedFlake, MaterializedInputs, EvaluatedClosure, BuiltClosure, CopiedClosure, ActivatedGeneration, GarbageCollected, CheckBuilt, TestVmBroughtUp, TestVmTornDown); EffectFailure, EffectStage; BuildTarget, TargetStoreBuild, ClosureOrigin, UserEnvironmentMaterialization, MaterializationShape, FlakeInputReference, FlakeInputOverride, UserEnvironmentActivationProfile, ActivationProfile.
- schema_runtime.rs (38): StageFailure, ReportedOutput, ProcessEnd, EffectExecution, NixCommand, NixFlakeMetadata, EvalRefresh, FlakeReferencePolicy, HermeticCheck, LiveTestVm, HorizonMaterialization, MaterializationRoot, MaterializedInputSet, GeneratedInputDirectory, GeneratedInputName, DeploymentInput, ClusterSecretsDirectory, ClusterSecretFile, NixSystemName, NarHash, SshTarget, RemoteUserActivationAuthority, ShellCommand, ShellArgument, ClosureCopy, TargetStoreRealization, TargetGcRoot, TargetGcRootDirectory, Activation, DetachedSelfActivation, HostActivation, UnitJournal, DetachedActivationUnit, DetachedActivationObserver, DetachedActivationFailure, DetachedActivationOutcome, DetachedActivationProxies, UserEnvironmentActivation.
- bootstrap.rs (6): BootstrapCommand, ProcessBootstrapExecutor, BootOnceUnit, UnitState, FlakeOverride, SshIdentity.

Other (68): lib.rs Ingress, Error, EventLogRetention, Store, LojixDirectory and the aliases NexusConfiguration, NexusConfigurationState, Result; schema_runtime.rs HorizonUserName; daemon.rs Daemon, LojixRuntime, OwnerPeerAuthority; inspection.rs (11); reconstruction.rs (3 and the alias StoreFamilyIdentity); inspected_text.rs InspectedText, PercentEncodedText, NixStorePath, PathFault, OfferedPath; deployment_watch.rs DeploymentWatchers, DeploymentWatcher, DeploymentWatchStream; quarantine.rs StoreOpening; legacy_store.rs (4); client.rs SocketExchange; the two clients' Client and HorizonProposal; tools ConfigurationWriterCli, SocketMode, HorizonArtifact, ConfigurationWriterError, ConfigurationMigration; adapters.rs WireShapeError; bootstrap.rs BootstrapTerminal, BootstrapError, BootstrapCrashPoint, NeverCrash, EphemeralJournal and the 13 `*Validated` types.

Unused (13, no reference anywhere in the workspace's Rust outside their declaration): runtime_model.rs LiveSetTable, DeploymentRecordTable, IdentifierAllocationTable, DeploymentOutboxTable, PendingTransitionIntentTable, GcRootsTable, EventLogTable, ContainerLifecycleTable, TestRunTable, Input, Output; runtime_flow.rs Input, Output.

Traits (160): lib.rs 24, schema_runtime.rs 60, bootstrap.rs 25, daemon.rs 10, inspection.rs 6, reconstruction.rs 6, deployment_watch.rs 4, inspected_text.rs 4, quarantine.rs 3, runtime_flow.rs 3, clients 6, client.rs 2, adapters.rs 2, legacy_store.rs 1, tools 4.

## F. External calls the daemon makes today

All daemon calls go through `NixCommand` (schema_runtime.rs line 8102), whose `Effect::run` spawns `tokio::process::Command` with the program resolved by `EffectExecution` (the service PATH in production, a fixture directory in focused tests), reads stdout and stderr, and returns `Result<String, StageFailure>`. Remote calls are `ssh <destination> <shell text>`, the text built by `ShellCommand` and `ShellQuoting`.

| call | where | how |
|---|---|---|
| `nix flake metadata --no-write-lock-file --json` | flake admission, flake auth | local process |
| `nix eval --raw [--refresh]` of the toplevel drvPath | eval stage | local process, never `--store` |
| `nix hash path --type sha256 --sri` | materialized input hashing | local process |
| `nix build --no-link --print-out-paths` (with substituter options; or `--option max-jobs 0 --builders <spec>`) | local or offloaded build, hermetic check | local process |
| `nix copy --to <store>` (closure, or derivation closure for a target-store build), `nix path-info` | copy stage, target-store realization | local process |
| `nix build` in the target store, GC root on the target | target-store realization | local process and ssh |
| `switch-to-configuration boot/switch/test`, `systemd-run --unit … --wait` (BootOnce), `systemd-run … --remain-after-exit` (retained test activation), `bootctl set-default ''`, `bootctl set-oneshot ''`, `journalctl --unit … --lines 200` | host activation | ssh with shell text |
| `nix-env -p ~/.local/state/nix/profiles/home-manager --set`, `/run/current-system/sw/bin/systemd-run --user --wait --pipe …`, `hostname -s` | user-environment activation | local process or ssh |
| systemd over D-Bus: `GetUnit`, `StopUnit`, the `UnitNew` signal, `ActiveState` changes, and reads of `ActiveState`, `Result`, `ExecMainCode`, `ExecMainStatus` | detached same-host activation and its observer | zbus, async |
| files: generated flake inputs (horizon, system, deployment) and copied `.sops` secrets under `<state>/generated-inputs/<cluster>/<node>/<shape>/` | horizon materialization | std::fs |
| bootstrap: `nix-store`, `nix`, `ssh` | lojix-bootstrap only | `std::process::Command`, synchronous; unit state awaited by a 100 ms sleep loop (bootstrap.rs lines 658 and 2886) |

## G. ethos-zero 28 transcripts

`<scratch>` is this flow's scratch directory. `s1` is signal-lojix with only the three markers rewritten as `X.{ DatabaseMarker }`; `s2` is `s1` with its outputs reordered to pair by position (with a second watch output, `CacheRetentionWatching`, as one possible reading); `m2` is meta-signal-lojix with its outputs reordered.

```
Rejected.{ <scratch>/wt/signal-lojix/ethos/signal.ethos { 68 19 } Conceptual.{ [ 1 3 44 1 ] Wrapping.{ AdmissionMarker DatabaseMarker } } }
Checked.<scratch>/wt/meta-signal-lojix/ethos/signal.ethos
Checked.<scratch>/wt/lojix/ethos/ingress.ethos
Checked.<scratch>/try/horizon.ethos
Checked.<scratch>/try/s1.ethos
Checked.<scratch>/try/s2.ethos
Checked.<scratch>/try/m2.ethos
```

Generated `Answering` for signal-lojix as it stands (with only the marker fix), showing what positional pairing makes of today's output order:

```rust
fn configure(&self, lojix_nexus_configuration: &LojixNexusConfiguration) -> Result<ConfigurationReceipt, Output>;
fn watch_deployments(&self, deployment_watch: &DeploymentWatch) -> Result<ConfigurationRejection, Output>;
fn query(&self, selection: &Selection) -> Result<TestRunListing, Output>;
fn watch_cache_retention(&self, cache_retention_watch: &CacheRetentionWatch) -> Result<RejectedUnwatch, Output>;
fn unwatch(&self, subscription_close: &SubscriptionClose) -> Result<RejectedQuery, Output>;
```

and for meta-signal-lojix as it stands:

```rust
fn configure(…) -> Result<signal_lojix::ConfigurationReceipt, Output>;
fn reverse_configuration(&self) -> Result<signal_lojix::ConfigurationRejection, Output>;
fn retire(…) -> Result<signal_lojix::ConfigurationReceipt, Output>;
fn pin(…) -> Result<RejectedPin, Output>;
fn deploy(…) -> Result<RejectedDeploy, Output>;
fn test(…) -> Result<RefusedDeploy, Output>;
fn unpin(…) -> Result<DeployHandle, Output>;
```

Probes of what 28 accepts (scratch files, Check or Generate):
- `Memory [] [ Routed<Root>.{ Integer Root } ]`: `Rejected … Conceptual.{ [ 1 1 0 ] Expected.Declaration }`. A generic declaration is not accepted.
- `Memory [] [ Unread.{} Row.{ String Vector<Integer> } ]`: Checked. An empty struct is accepted; `Vector<Integer>` generates `Vec<i64>`.
- `Memory [ :std:path:PathBuf ] [ Row.{ PathBuf } ]`: Checked; the generated derives would need `PathBuf` to archive, which it does not (inference, not compiled).
- An `Operation` file generates its declared types and the two enums `Operation` and `Outcome`, and no trait or dispatch.
- An `Emission` file generates `Emitted` and `Emittable<Translator>` with a synchronous `fn emit(&self, translator: &Translator) -> Self::Outcome`.
- The intrinsics are String, Integer (i64), Decimal, Boolean, Meaning, Vector, Option, Result, Self and Sized (ethos-zero `src/lib.rs` line 481); there is no byte or unsigned type.
