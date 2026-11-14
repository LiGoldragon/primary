# Bounded Wake type and persisted reachability packet

Independent readonly reviewer/native01a1adff-cafa-77a1-aa73-aa98b4dd4794 completed23:29UTC. Relevant Flow916b545/treef5f01e, signaltree191072 andmetatree907f3b unchanged/clean. This is placement evidence, not a design/allocation ruling.

Local `flow-nexus/ethos/operation.ethos:67–130`/generatedoperation112–178: Operation.Wake(Address); Outcome.Woken(FlowId)|Failed(Failed_Data). Generated typesderiveArchive but no currentstoreEngineRecord reaches Operation/Outcome/Failed_Data (structurally traced, no fields/references understore orstore.rs).

```rust
// generated/operation.rs:140–157
pub enum Failed_Data {
    CompositionRefused(signal_flow::CompositionRefusal),
    StoreRefused,
    ConflictingBinding,
    Unstarted,
    HerdrRefused,
    CodexRefused,
    UnknownFlow,
    ClaimRefused,
    NotAsleep,
    NotAwake,
    NothingQueued,
    AddressAwake,
    ContextRefused(signal_flow::ContextRefusal),
    LeaveOutRefused(signal_flow::LeaveOutRefusal),
    SpawnRefused(signal_flow::HarnessSpawnRefusal),
    LaunchRefused(signal_flow::NativeLaunchRefusal),
}
// waking.rs:468–488
pub enum WakeRefusal {
    StoreUnreadable,
    NotAsleep,
    NothingQueued,
    SessionLive,
    HerdrUnreadable,
    Unplaceable,
    FreshNotStarted(Failed_Data),
    StartRejected(signal_flow::StartRejection),
    AwakeNotRecorded,
}
```

Performsdispatch performing216–217,515; AnswersWakeRefusal490–525 maps Undeclared/unmatchedStartRejected→Failed.Unstarted,Unplaceable→HerdrRefused. wake1829–1840 projects only Outcome. No exact NotConfigured owner here yet.

Queue flow: waking2540–2557 reads existing Asleepmetaflow/queue;2595–2621 only FreshRefusal::Rejected marks unchangedqueueRetryable(WakeRefused(StartRejection)); earlyWakePlan2592–2593 returnsUnplaceable beforemark.1838 statesnothingtaken/workstillqueuedoldestfirst. sending1323–1328 ignores wake result;1393–1423 reconstructsfromstore absentdecl→Undeclared elseCompositionUnconfigured, retrymarksqueue, publicresultPrivateSendResponse::Failed(NotSent(debugOutcome)) ratherthan exactlocalfailure.

Shared types: signalgeneratedStartRejection644–662 containsUndeclared/noNotConfigured; Refusal804–826 containsNotConfigured; RetryCause987–1004 WakeRefused(StartRejection), DeliveryState Retryable(RetryCause)|Failed(Refusal); DeliverySnapshot1040–1046 storesstate; PrivateSendResponse1071–1076 Refused(Refusal); publicResponse1280–1314 Woken/StartRejected/RefreshRejected/Refused.

Persisted shared paths: CurrentLogicalDelivery+LogicalDeliveryEvent EngineRecordV5 (store/logical_delivery95–110,224–239) containDeliverySnapshot→DeliveryState→RetryCause→StartRejection andFailed→Refusal. StoredSendOutcome EngineRecordV6(send_outcome42–60)→SendOutcomeRecord→OrdinarySendOutcome::Refused(Refusal)(metagenerated693–712); frozenV5history63+ demonstratesversionedsharedRefusalstorage. Thus addinglocalFailed_Data/sourceWakeRefusalvariant has a differentreachabilityboundary fromalteringsharedStartRejection/Refusal. No variantname/designallocated bythisreport.
