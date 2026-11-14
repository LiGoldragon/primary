# Flow Nexus v1: field and capability review

For Mind flowNexus Primary ee0934, from Secondary 7a6502. Implements the anatomy requested in deliveries 20980/20981; machine working proposal, not psyche. No runtime bodies are authorized by this document.

## Existing infrastructure

Exact signatures and immutable source locations are in `flows/7a6502/reports/nexus-apis.md` and `flows/7a6502/reports/memory-signal-apis.md`.

The usable actor contracts are `nexus::Remembering`, `nexus::Operating<M>` and `nexus::Signaling`. Memory changes and reads already pass through the Memory actor; Signal owns only an Operation handle. `nexus::Configurable<Configuration>` supplies the first-Configure transition, whose persistence remains our responsibility. The Memory kernel supplies schema-guarded opening and typed transactions; it has no `Memorizable` root capability. Signal supplies typed validated archives and bounded length-prefixed transport, not process authority. These are source observations, not a compatibility build.

The current Nexus serving path loses caller credentials before Operation: `Door::serve` passes a byte frame to `Signaling::decode`, and `intend` accepts only the decoded query. `Entering` binds one socket; its Memory `Admission` constructor is private. A client-claimed PID cannot repair that gap. Delivery 21209 asks whether to compose a Flow-owned multi-socket authenticated Kameo entry or request an upstream infrastructure extension. This decision precedes the serving bodies.

## Configuration field shapes

These are proposed additions to the single shared Library, replacing the initial meta-owned Configuration. Every namespace/profile reference is checked atomically by Configure; attempts retain resolved values rather than a pointer back to mutable configuration. Peer, Holder and Ownership leave the boundary-one schemas.

The Ethos:

```ethos
Library
[]                                                       ; imports
[ MetaflowName.String                                    ; types: one configured running system
  OrdinarySocketPath.String
  MetaSocketPath.String
  MemoryPath.String
  SocketConfiguration.{ OrdinarySocketPath MetaSocketPath } ;   separate authority surfaces
  ModelProfileName.String
  HarnessProfileName.String
  ModelIdentifier.String
  HarnessVersion.String
  ExecutablePath.String
  Tokens.Integer
  LayerAssignment.{ Aspect Layer ModelProfileName }        ;   configured layer-to-model binding
  ModelProfile.{ ModelProfileName ModelIdentifier          ;   reference resolves against one harness profile
                 HarnessProfileName Tokens }
  ModuleId.String
  ModuleKind.[ Spirit Intent Vision Knowledge Role ]
  ModuleSourcePath.String
  ModuleSource.{ ModuleId ModuleKind ModuleSourcePath }     ;   an actual configured registry entry
  ModuleContent.{ ModuleId ModuleKind Text.String }         ;   captured content, not a mutable reference
  ToolName.String
  HarnessModuleName.String
  HarnessModule.{ HarnessModuleName Option<ToolName>        ;   stock prompt section and taught tool remain one object
                  Text.String }
  PermissionMode.[ AcceptEdits Auto BypassPermissions Manual DontAsk Plan ]
  SettingSource.[ User Project Local ]
  HookExecutablePath.String
  HookEvent.[ SessionStart UserPromptSubmit Stop SessionEnd PermissionRequest ]
  HookConfiguration.{ HookExecutablePath Vector<HookEvent> } ;   installed adapter receives external JSON on stdin
  ClaudeSettings.{ PermissionMode Vector<SettingSource>     ;   corresponding CLI flags, hooks supplied by --settings
                   HookConfiguration }
  HarnessSettings.[ ClaudeCode.ClaudeSettings CodexUnavailable ] ;   one selected adapter, Codex remains unproven
  HarnessProfile.{ HarnessProfileName HarnessVersion        ;   exact executable and version, no PATH selection
                   ExecutablePath Vector<HarnessModule>
                   HarnessSettings }
  IdentityAlphabet.String
  IdentityPolicy.{ IdentityAlphabet }
  HomePath.String
  TranscriptDirectory.String
  WorkingDirectory.String
  HerdrExecutablePath.String
  HerdrSocketPath.String
  HerdrSessionName.String
  NamespaceIdentity.String
  CapsuleConfiguration.{ HomePath TranscriptDirectory       ;   effective paths/binding inside the configured namespace
                         WorkingDirectory HerdrExecutablePath
                         HerdrSocketPath HerdrSessionName
                         NamespaceIdentity }
  Configuration.{ MetaflowName MemoryPath                   ;   one authoritative complete configuration
                  SocketConfiguration Vector<Declaration>
                  Vector<LayerAssignment> Vector<ModelProfile>
                  Vector<HarnessProfile> Vector<ModuleSource>
                  IdentityPolicy CapsuleConfiguration } ]
[]                                                       ; traits: proposed Rust capability bindings below
[]                                                       ; associations
```

The one payloaded `HarnessSettings` choice above combines the requested harness selector and typed launch settings, so they cannot disagree. Confirm this projection rather than storing a second independent selector. PermissionMode lists the installed CLI's six choices; no configured default is chosen here. Module kinds must represent the actual configured registry classification; no absent registry reference is authored by this proposal.

### External-interface fit

Installed Claude 2.1.294 help exposes `--model`, `--system-prompt`, `--disallowed-tools`, `--settings`, `--setting-sources` and permission-mode selection. Exact store executables and commands are in the external-interface report. Proposed inputs map to those interfaces; this is help evidence, not a session witness.

Command hooks receive JSON through stdin and are configured by event in settings. Proposed translation: SessionStart supplies session/transcript evidence; UserPromptSubmit begins Working; Stop supplies an idle indication; SessionEnd supplies harness-end evidence. A PermissionRequest causes launch failure rather than user interaction. Hook-derived state still requires process-incarnation authentication and independent process-exit reconciliation. These event meanings need adapter execution witnesses. [Claude hooks reference](https://code.claude.com/docs/en/hooks).

Herdr exposes a socket API and event subscriptions. A configured exact socket endpoint can be used without environment-based routing; whether to use that API directly or its session-selecting CLI belongs to adapter approval. The actual server, rather than only its client, must run in the metaflow namespace for its child panes to inherit isolation. [Herdr socket API](https://herdr.dev/tui/docs/socket-api/).

Deployment-only namespace mappings stay outside running Configuration. The running capsule records its effective namespace identity and paths. No credential file, environment selector or copied authentication material is part of this shape.

## Durable evidence fields

Replace the generic Phase and optional reserved FlowId. The proposed phase payloads prevent combinations that the initial scaffold permitted:

The Ethos:

```ethos
Library
[]                                                       ; imports
[ HostBootIdentity.String                                ; types: process incarnation, not a PID alone
  PidNamespaceIdentity.String
  ProcessId.Integer
  ProcessStartTicks.Integer
  ProcessIncarnation.{ HostBootIdentity PidNamespaceIdentity ;   compare peer and target in the same namespace
                       ProcessId ProcessStartTicks }
  ProcessBinding.{ FlowId ProcessIncarnation }
  PaneId.String
  CapsuleHandle.{ PaneId NamespaceIdentity }
  PromptContent.{ System.String First.String }             ;   exact bytes captured before execution
  ResolvedLaunch.{ Declaration ModelProfile HarnessProfile  ;   no mutable profile references during attempts
                   IdentityPolicy CapsuleConfiguration
                   Vector<ModuleContent> PromptContent }
  StartWitness.{ ProcessBinding SessionId TranscriptPath }  ;   authenticated session/process evidence
  ExitWitness.{ ProcessIncarnation }
  LaunchPhase.[ Reserved                                   ;   identity and snapshot already live on LaunchAttempt
                Prepared.CapsuleHandle
                Submitted.CapsuleHandle
                Started.StartWitness
                Cleanup.CapsuleHandle
                RecoveryRequired.CapsuleHandle
                Complete ]
  EndPhase.[ Intended.StartWitness                         ;   exact target before the termination effect
             StopRequested.StartWitness
             Exited.ExitWitness
             RecoveryRequired.StartWitness
             Complete ]
  LaunchAttempt.{ RequestId FlowId Address ResolvedLaunch    ;   FlowId reservation and this insertion are one transaction
                  LaunchPhase }
  EndAttempt.{ RequestId FlowId EndPhase }
  Permaflow.{ Address Vector<FlowId> } ]                    ;   ordered history explicitly requested by the living
[]                                                       ; traits
[]                                                       ; associations
```

Payload review questions: must Cleanup/RecoveryRequired also represent a partly created namespace with no pane yet? Must the start/exit witness retain an adapter-specific handle in addition to the pane, session and process incarnation? The answers should determine a typed resource sum before bodies. A bare Complete phase is valid only with the finalized Flow/history record in the same committed Memory change.

These are proposed field shapes, not final schema edits. Memory storage record ownership and the shared typed meta projection must be chosen together: the new ruling requires every record type writable through meta. A complete set therefore includes configuration/first-Configure metadata, Flow, Permaflow, ProcessBinding, launch/end attempts, address reservations and queue state. The private RequestId remains visible only in typed meta Debug/projections permitted by that ruling; ordinary observations remain free of it.

## Capability signatures for approval

The following propose the implementation surface requested by the responsibility table. Associated types bind to the concrete vocabulary above; asynchronous context binds to the approved Memory handle and adapter composition. They add no bodies or marker substitutes.

```rust
pub trait Identifiable {
    type Identity;
    type Failure;
    fn identify(&self) -> Result<Self::Identity, Self::Failure>;
}

pub trait Reservable {
    type Proposal;
    type Reservation;
    type Rejection;
    fn reserve(&mut self, proposal: Self::Proposal)
        -> Result<Self::Reservation, Self::Rejection>;
}

pub trait Preparable {
    type Preparation;
    type Handle;
    type Failure;
    fn prepare(&self, preparation: Self::Preparation)
        -> impl Future<Output = Result<Self::Handle, Self::Failure>> + Send;
}

pub trait Launchable {
    type Submission;
    type Witness;
    type Failure;
    fn launch(&self, submission: Self::Submission)
        -> impl Future<Output = Result<Self::Witness, Self::Failure>> + Send;
}

pub trait Authenticatable {
    type Observation;
    type Authenticated;
    type Rejection;
    fn authenticate(&self, observation: Self::Observation)
        -> Result<Self::Authenticated, Self::Rejection>;
}

pub trait Startable {
    type Context;
    type Progress;
    type Failure;
    fn advance(&mut self, context: &mut Self::Context)
        -> impl Future<Output = Result<Self::Progress, Self::Failure>> + Send;
}

pub trait Stoppable {
    type Context;
    type Progress;
    type Failure;
    fn stop(&mut self, context: &mut Self::Context)
        -> impl Future<Output = Result<Self::Progress, Self::Failure>> + Send;
}

pub trait Reconcilable {
    type Context;
    type Reconciliation;
    type Failure;
    fn reconcile(&mut self, context: &mut Self::Context)
        -> impl Future<Output = Result<Self::Reconciliation, Self::Failure>> + Send;
}
```

Proposed bindings: IdentityPolicy → Identifiable<Identity = FlowId>; the component's data-bearing Memory store → Reservable with one atomic reservation proposal; CapsuleConfiguration → Preparable; resolved HarnessProfile → Launchable; ProcessBinding → Authenticatable; persisted LaunchAttempt/EndAttempt → Startable/Stoppable; a persisted recovery record → Reconcilable. The actor engine implements the actual existing `Remembering`, `Operating` and `Signaling` interfaces rather than a second actor protocol. Concrete Context structure and generic capability constraints await the serving/authority decision above; these unconstrained draft associated types are not claimed to enforce architecture yet.

## Remaining decisions before bodies

1. Resolve the existing Nexus credential/multi-socket API gap without weakening caller authority.
2. Approve/refine configuration and evidence sums, including partial capsule creation and configured hook failure semantics.
3. Decide typed complete-meta writes and validation/reconciliation rules for imported active records; fresh next still starts empty with declarations/models alone.
4. Authorize a fresh test repository for the external acceptance scenarios rather than placing component tests with production code.

Compilation of the initial anatomy and actual adapter/isolation evidence remain separate acceptance obligations. No v0 implementation is involved in this review.
