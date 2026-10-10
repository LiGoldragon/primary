# Message Ethos Proposal

Status: proposal for review. No Signal contract, generated Rust, skill, relay, or deployment is changed.

## Ground

The existing Signal Ethos fixture is a sweet-form `Signal` file with four sibling sections: imports, queries, responses, and types. Ethos uses `Name.Type` for aliases, `Name.{ ... }` for structs, and `Name.[ ... ]` for enums. Datom is positional: the type supplies every position; braces are structs, brackets are vectors, and a capitalized head is a variant payload. This report does not promote the fixture into a new contract.

## Candidate Signal

The following is a candidate shape, not a settled contract. It gives the ordinary response a compact form and provides an explicit query for expanded provenance.

```text
Signal
[ signal-standard:[ Identifier36 Identifier64 Hash256 ] ]
[ Submit.TypedPromptEnvelope  GetFull.FullProvenanceQuery ]
[ Accepted.CompactReceipt Full.FullProvenance Unknown.ProvenanceLookupFailure Ambiguous.ProvenanceCandidates ]
[ PromptVariant.[ HumanPrompt PeerMessage DeliveryReceipt ]
  SourceEventIdentifier.Hash256
  RawPromptText.String
  TypedPromptEnvelope.{ PromptVariant SourceEventIdentifier RawPromptText }
  CompactReference.Identifier36
  FullProvenanceQuery.CompactReference
  CompactReceipt.{ CompactReference }
  FullProvenance.{ Hash256 SourcePath SourceEventIdentifier SourceTime RawPromptText }
  ProvenanceLookupFailure.[ MissingReference InvalidReference ]
  ProvenanceCandidates.Vector<FullProvenance> ]
```

The import and nominal identifier types are hypothetical future definitions from the proposed identifier library. The import path and primitives are absent today; this report does not claim that the Ethos library or Rust types exist. The names and initial variants are open. In particular, whether this belongs beside the ordinary producer contract or in `meta-signal-message`, and whether `Intent` is a separate message variant, remain rulings for the owners.

## Compact and full forms

The default receipt contains only a scoped abbreviated reference:

```text
Accepted.{ a1b2c3 }
```

`a1b2c3` is a display abbreviation, never a claim of global uniqueness. It is a legacy six-character illustration, not a selected 36-bit encoding. Its resolution scope and length are open. Resolution must yield exactly one durable record in the selected scope. Zero matches is `Unknown`; more than one is `Ambiguous` with queryable candidates. The full hash, path, source event, source time, raw prompt, and other provenance fields live in storage and are returned only by the explicit full-provenance query. A compact response must never silently select one collision.

The full response is therefore conceptually:

```text
Full.{ «full hash» «source path» «source event» «source time» «raw prompt» }
```

This rendering is illustrative only until the field order, exact types, and wire encoding are ruled. It uses guillemets because the values may contain spaces or delimiters; no new wire lexeme is invented here.

## Authentic prompt grounding

The existing producer contract already declares `PromptVariant`, `SourceEventIdentifier`, `RawPromptText`, `PromptInterpretationSelection`, and `TypedPromptEnvelope`. Its current `SourceEventIdentifier.String` declaration is legacy fixture evidence; the candidate above gives the field a future nominal hash type without claiming the legacy contract has changed. A real relayed prompt must be rendered from stored values. No invented prompt text is included here. The source records available to the parent flow identify the latest user event by its existing source identifier; the actual payload must be copied from that record at implementation time rather than reconstructed in this proposal.

## Pending rulings

- `Intent?`: whether intent is a distinct variant or metadata on an existing envelope.
- Owner repository: ordinary `signal-message` beside the Rust provenance seam, or `meta-signal-message`.
- Initial variants: exact compact/full/lookup names and payloads.
- Abbreviation: length and resolution scope; collision and missing-record behavior above are proposed safety semantics.

Claude owns any future Signal skill proposal. No Signal skill is added here.

## Existing fixture Signal appendix

The following is the complete existing fixture file, copied verbatim. It is
reported as observed source, including references whose definitions are not
resolved by this read; it is not repaired or promoted here.

```text
Signal
[]
[ Submit.MessageSubmission SubmitStamped.StampedMessageSubmission QueryInbox.InboxQuery AssignAgentIdentity.AgentIdentityAssignment BindAgentEndpoint.AgentEndpointBinding QueryAgentRegistry.AgentRegistryQuery QueryThread.ThreadQuery SubscribeThread.ThreadSubscription QueryThreads.ThreadIndexQuery ]
[ SubmissionAccepted.SubmissionAcceptance SubmissionRejected.SubmissionRejection InboxListing.InboxListingReply AgentIdentityAssigned.AssignedAgentIdentity AgentEndpointBound.BoundAgentEndpoint AgentRegistryListing.AgentRegistryListingReply AgentRegistryRejected.AgentRegistryRejection MessageRequestUnimplemented.MessageRequestUnimplementedReply Error.ErrorReport ThreadListing.ThreadContents ThreadSubscribed.ThreadSubscriptionAcknowledgment ThreadIndexListing.ThreadIndexEntries ThreadRejected.ThreadRejection ]
[Messages.Vector<InboxEntry> EngineIdentifier.String MessageSocketPath.WirePath IdentityProvenance.[Seated Reseated] InternalComponentInstanceOrigin.{ComponentName ComponentInstanceName} MessageRecipient.String ComponentIngresses.Vector<ComponentMessageIngress> ThreadRelation.{RepositoryName FeatureBranchName} InboxQuery.MessageRecipient BoundAgentEndpoint.AgentIdentifier MessageKind.[Send Inbox] MessageOperationKind.[QueryThreads Submit QueryThread SubscribeThread QueryInbox QueryAgentRegistry SubmitStamped AssignAgentIdentity BindAgentEndpoint] InboxEntry.{MessageSlot MessageSender MessageBody ThreadSelection StampedAt} ThreadRelationSelection.[None Related.ThreadRelation] ResumeIdentity.String StampedAt.TimestampNanos UnixUserIdentifier.Integer MessageRequestUnimplementedReply.{MessageOperationKind MessageUnimplementedReason} ComponentName.String RepositoryName.String ThreadIndexQuery.[All] ProcessPinSelection.[Pinned.HarnessProcessPin None] ParticipantName.String HarnessStartTime.Integer AgentDeathMark.[NotDead Killed] SocketMode.Integer EndpointSelection.[Bound.AgentEndpoint None] HarnessProcessPin.{HarnessPid HarnessStartTime} OwnerIdentity.[UnixUser.UnixUserIdentifier System.SystemPrincipal] ResumeSelection.[Resumed.ResumeIdentity None] ThreadSubscriptionAcknowledgment.{ThreadName ParticipantName} HostName.String ThreadRejectionReason.[UnknownThread StoreRejected] ThreadEntries.Vector<ThreadEntry> MessageUnimplementedReason.[DependencyMissing.DependencyKind NotInPrototypeScope ResourceUnavailable.ResourceKind] MessageBody.String ThreadIndexEntries.{Threads} MessageCount.Integer AgentEndpoint.{AgentEndpointKind EndpointPath} Host.HostName DependencyKind.[Mind Router Harness Terminal] AgentIdentityAssignment.{AgentIdentifier ProcessPinSelection ResumeSelection} AgentRegistryListingReply.{Entries} AgentRegistryEntry.{AgentIdentifier EndpointSelection ResumeSelection AgentDeathMark ProcessPinSelection} ComponentMessageIngress.{InternalComponentInstanceOrigin IngressSocketPath SocketMode} SubmissionAcceptance.MessageSlot ThreadSummary.{ThreadName ThreadRelationSelection Participants MessageCount} AgentRegistryRejection.AgentRegistryRejectionReason TimestampNanos.Integer AssignedAgentIdentity.{AgentIdentifier IdentityProvenance} ErrorReport.ErrorMessage Entries.Vector<AgentRegistryEntry> MessageSubmission.{MessageRecipient MessageKind MessageBody ThreadSelection} IngressSocketPath.WirePath MessageOrigin.[External.ConnectionClass InternalComponentInstance.InternalComponentInstanceOrigin Internal.ComponentName] MessageSlot.Integer ErrorMessage.String InboxListingReply.{Messages} ThreadRejection.ThreadRejectionReason SubmissionRejectionReason.[RecipientNotFound StoreRejected] ThreadSelection.[Named.ThreadName None] ResourceKind.[RouterSocket Store PeerCredentials MessageSocket] AgentEndpointKind.[HarnessSocket PtySocket] HarnessPid.Integer AgentIdentifier.String ConnectionClass.[Owner Network.NetworkPeer OtherPersona.OtherPersonaEngine System.SystemPrincipal NonOwnerUser.UnixUserIdentifier] AgentEndpointBinding.{AgentIdentifier AgentEndpoint HarnessPid HarnessStartTime} ThreadSubscription.{ThreadName ParticipantName ThreadRelationSelection} Participants.Vector<ParticipantName> AgentRegistryQuery.[All ByAgent.AgentIdentifier] AgentRegistryRejectionReason.[UnknownAgentIdentifier StoreRejected] OtherPersonaEngine.{EngineIdentifier Host} EndpointPath.WirePath SubmissionRejection.SubmissionRejectionReason MessageSocketMode.SocketMode SupervisionSocketMode.SocketMode FeatureBranchName.String ComponentName.[Introspect Terminal System Mind Spirit Message Harness Router Orchestrate] WirePath.String ThreadEntry.{MessageSlot MessageSender MessageBody StampedAt} NetworkPeer.String StampedMessageSubmission.{MessageSubmission MessageOrigin StampedAt} SupervisionSocketPath.WirePath MessageDaemonConfiguration.{MessageSocketPath MessageSocketMode SupervisionSocketPath SupervisionSocketMode RouterSocketPath ComponentIngresses OwnerIdentity} RouterSocketPath.WirePath ThreadName.String SystemPrincipal.String Threads.Vector<ThreadSummary> ThreadQuery.ThreadName ThreadContents.{ThreadName ThreadRelationSelection Participants ThreadEntries} PromptVariant.[HumanPrompt PeerMessage DeliveryReceipt] SourceEventIdentifier.String RawPromptText.String PromptInterpretationSelection.[Interpreted.MessageBody None] TypedPromptEnvelope.{PromptVariant SourceEventIdentifier RawPromptText PromptInterpretationSelection}]
```

## Sources

- `/home/li/primary/Vision/signal.md`
- `/home/li/primary/Vision/datom.md`
- `/home/li/primary/Vision/ethos.md`
- `/home/li/wt/github.com/LiGoldragon/signal-message/messenger-fixture-34d94e/ethos/signal.ethos` (existing fixture; its whole one-line types section is the source appendix, with unresolved/undefined references observed and not repaired)
- `/home/li/primary/flows/34d94e/reports/auditMessaging.md`
- `/home/li/primary/flows/6cc91b/vision/typedPrompts.md`
- `/home/li/primary/flows/692df8/vision/signal.md`
