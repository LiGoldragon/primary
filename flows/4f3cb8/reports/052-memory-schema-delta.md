# 052 private Memory declarations and frozen edges

Proposal only; all new coordinates below require allocation. Base is immutable Flow916b54574ae0024b893a9f4252f2e97704db48c1 and its pinned dependencies. Main lifecycle StoredMetaflow-v6 is DISTINCT from meta-metaflow-configuration-v5: no lifecycle migration follows from this configuration change.

## Exact current records retained

`StoredMetaNexusConfiguration { nexus: ConfigureNexus }` retains its exact archive shape, ten-field resolved ConfigureNexus, key `nexus`, MemoryVersion4, family `flow-nexus-meta-nexus-configuration`, schema `flow-nexus-meta-nexus-configuration-v4`. Per-value meta splitting changes neither field order nor stored representation. Actual table descriptor/registration is retained, not renamed. Frozen V2/V3 mirrors and transformations remain exact; no new runtime defaults are sourced from them.

AddressHold-v5 remains exact. Main lifecycle, queue, send-call, delivery/current/event/outcome families are retained unless the final actual consumer ledger demonstrates a changed reachable archived type. Dedicated Resume vocabulary is not a reason to extend shared Refusal. Predecessor-produced archives and full readback/reopen tests witness these claims; source resemblance alone does not.

## Three new private rows

The Ethos (Memory ownership of generated wire values, not an additional copy of their fields):

```ethos
Memory
[ :meta_signal_flow:RuntimePolicy          ; resolved missing-policy vocabulary, one owner
  :signal_flow:[ ResumeHead ResumeAttempt ] ] ; dedicated Resume observation vocabulary
[ StoredRuntimePolicy.{ RuntimePolicy }   ; singleton resolved policy
  StoredResumeHead.{ ResumeHead }         ; one sequence/active head per FlowId
  StoredResumeAttempt.{ ResumeAttempt } ] ; one retained attempt per FlowId/generation
```

The intended private Rust projections, using the pinned existing archive machinery:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(crate) struct StoredRuntimePolicy {
    pub(crate) runtime_policy: meta_signal_flow::RuntimePolicy,
}
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(crate) struct StoredResumeHead {
    pub(crate) resume_head: signal_flow::ResumeHead,
}
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(crate) struct StoredResumeAttempt {
    pub(crate) resume_attempt: signal_flow::ResumeAttempt,
}
```

These carry the pinned `EngineRecord` and `MemoryDefinition` contracts; `EngineStoredValue` is supplied by the existing blanket implementation for archive-capable Clone records, not a duplicate implementation. The table below specifies every trait result. Table descriptors use these precise record types with the existing TableName/TableDescriptor/FamilyName machinery; no raw reserved-table mutation is introduced.

| Private record | TableName | FamilyName | MemoryVersion / SchemaHash label | EngineRecord key |
|---|---|---|---|---|
| StoredRuntimePolicy | flow_nexus_runtime_policy | flow-nexus-runtime-policy | 1 / flow-nexus-runtime-policy-v1 | RecordKey::new("policy") |
| StoredResumeHead | flow_nexus_resume_heads | flow-nexus-resume-head | 1 / flow-nexus-resume-head-v1 | exact head FlowId string |
| StoredResumeAttempt | flow_nexus_resume_attempts | flow-nexus-resume-attempt | 1 / flow-nexus-resume-attempt-v1 | versioned ResumeAttemptId projection below |

Resume attempt key is canonical decimal UTF-8 byte length of FlowId, colon, exact FlowId bytes, colon, canonical positive generation: `3:abc:2` for `{abc,2}`. Checked generation conversion/overflow refuses before reservation; key construction is injective over the declared fields. It is one record-owned capability, not a generic Engine composite-key invention. Tests include embedded separator/non-ASCII identifiers, minimum generation and exhaustion.

Only the store-private configuration capability constructs/stages StoredRuntimePolicy after full snapshot validation. Only the store-private Resume admission capability stages head/attempt changes and matching AddressHold changes together. Public observation values are projections, not writable record handles. Their current archive shapes are pinned by these schemas; a later change to embedded public vocabulary must freeze these exact mirrors and allocate an explicit successor.

An old store has no RuntimePolicy row. Required values are supplied from explicit startup changes and validated, or opening refuses; no all-default constructor/seed. Optional DefaultContinuity may resolve None. An old store has no Resume history; registration adds empty new families, not fabricated past attempts or a head for every historical flow. The first explicit Resume initializes its head and positive sequence in the same reservation transaction.

## Member Continuity successor

Exact916 current record is `StoredMetaMetaflowConfiguration { metaflow: ConfigureMetaflow }`, address-derived record key, MemoryVersion5, table `flow_nexus_meta_metaflow_configuration`, family `flow-nexus-meta-metaflow-configuration`, schema `flow-nexus-meta-metaflow-configuration-v5`.

Freeze that COMPLETE current payload under `ConfigureMetaflowV5` and `StoredMetaMetaflowConfigurationV5`, preserving all concrete field types/order and archive derives. It must not refer to the newly changed live ConfigureMetaflow. The current successor wrapper keeps the same one-field shape over the new live ConfigureMetaflow whose existing Continuity position becomes Option<Continuity>. Candidate MemoryVersion6/schema `flow-nexus-meta-metaflow-configuration-v6`; table/family/address key unchanged.

V5 -> V6 copies address, system/user modules, flow kind, tool set, purpose, records and root unchanged, and maps exactly `previous.continuity` to `Some(previous.continuity)`. It does not recompute continuity from address or DefaultContinuity. New declarations may explicitly hold None. Launch resolves member Some else configured default exactly once; both absent -> NotConfigured, while Define accepts the declaration.

Historical V1–V4 mirrors and transformations remain frozen. Existing conversion bodies targeting the old current V5 must be bound to that frozen result, then composed with the one V5->V6 edge. Preserve each old transform's exact prior semantics, including historical address-derived Continuity, without exposing those functions as current runtime default suppliers. Pinned source now confirms ALL V1/V2/V3/V4 transforms directly target current V5 (metaflow_declaration.rs84,180,232,282), not a sequential V1->V2->V3->V4 chain. Keep those exact direct transforms targeting frozen V5, then compose V5->V6 in the opening-owned prepared conversion. No intermediate transaction. Existing descriptor advertises V1..V4; successor admits V1..V5, dispatching by exact archived identity rather than trial mutation. Registration/consumer anchors: store.rs4076,4106,4339,4367,4931; full consumer ledger must cover both configuration-only and full opens.

The frozen payload, in EXACT generated field order (root is SECOND, not the last struct-literal assignment):

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(super) struct ConfigureMetaflowV5 {
    pub(super) address: flow_ethos::Address,
    pub(super) root_option: Option<String>,
    pub(super) system_modules: signal_flow::SystemModules,
    pub(super) user_modules: signal_flow::UserModules,
    pub(super) flow_kind: signal_flow::FlowKind,
    pub(super) tool_set: signal_flow::ToolSet,
    pub(super) continuity: meta_signal_flow::Continuity,
    pub(super) purpose: String,
    pub(super) records: Vec<String>,
}
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(super) struct StoredMetaMetaflowConfigurationV5 {
    pub(super) metaflow: ConfigureMetaflowV5,
}
```

Pinned Root/Purpose/RecordPath are String aliases; Records is Vec<RecordPath>. Unchanged embedded enum leaves are pinned to their exact existing layouts; if any changes in this composition, freeze that leaf too rather than importing the new shape into a historical mirror. Frozen wrapper EngineRecord uses the existing address key, MemoryVersion5 and exact v5 schema label. Live successor ConfigureMetaflow keeps this order and replaces only continuity with Option<Continuity>; its private current wrapper retains the one metaflow field. The explicit archive fixture must compare the generated predecessor payload against this authored mirror; derives and field order are a design, not proof of byte equivalence.

## Opening and commit boundary

Family registration, selected legacy conversions, new validated policy row and explicit startup replacements form ONE opening-owned prepared plan against the same retained backend/read view. Existing typed preparation/materialization machinery is reused. Reject overlapping coordinates, missing required policy and incompatible catalog/schema before mutation. One Sema transaction includes selected rows/catalog/log/counters; no incremental upgrade commits followed by config commit.

Physical file mutation and logical atomicity are distinct. Read-only existing-store inspection cannot repair/init/begin_writable. Validated same-handle promotion is the first permitted writer transition; exact first mutation is fault-tested separately. A successful logical commit returns a committed receipt even if later optional maintenance fails. No error after commit is represented as rollback.

## Required allocation/consumer receipt

Allocate together, before bodies: new three families; configuration successor V6; ordinary Resume/Observe contract; meta settings/runtime-policy/validation contract; shared flow-ethos nominal ProcessIdentity relocation; Flow package; changed Engine/Sema, codec pair, and owned registry-source redb fork versions. Ordinary44/meta60 and other local-absent candidates are NOT reservations. All dependency revisions must be real coherent published/available immutable references, with explicit reproducible Cargo/Nix sources; workspace patch success alone cannot establish identity cohesion.

Final ledger must name authored/generated contract and enum consumers, table descriptors, registration/read/upgrade/write/readback entry points, all guarded config/admission writers, CLI/Nix/hook/adapter constructors and standalone default+datom feature graphs. Predecessor fixtures cover exact Nexus-v4 and metaflow-v5, every older supported migration edge, unchanged ProcessIdentity-bearing binding/container/resolver/queue, and retained send/lifecycle records. Body-stage tests execute these contracts; prebody review verifies the exact plan, bases/custody, allocation and consumer obligations, not nonexistent compiled source.
