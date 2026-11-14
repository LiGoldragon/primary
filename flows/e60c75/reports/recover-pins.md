# Exact configuration-wrapper packet
HEAD: `916b54574ae0024b893a9f4252f2e97704db48c1`, clean. Scope is the declared-metaflow configuration family (`StoredMetaMetaflowConfiguration`), not lifecycle `StoredMetaflow`.

## Current + frozen v4 wrappers
`crates/flow-nexus/src/store/metaflow_declaration.rs:21-103`
```rust
pub(super) const META_METAFLOW_CONFIGURATION_TABLE_NAME: TableName =
    TableName::new("flow_nexus_meta_metaflow_configuration");
pub(super) const META_METAFLOW_CONFIGURATION_FAMILY: &str =
    "flow-nexus-meta-metaflow-configuration";
pub(super) const META_METAFLOW_CONFIGURATION_SCHEMA: &str =
    "flow-nexus-meta-metaflow-configuration-v5";

/// One declared metaflow, keyed by its Address.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(crate) struct StoredMetaMetaflowConfiguration {
    pub metaflow: ConfigureMetaflow,
}

impl EngineRecord for StoredMetaMetaflowConfiguration {
    fn record_key(&self) -> RecordKey {
        RecordKey::new(FlowStore::address_record_key(&self.metaflow.address))
    }
}

impl MemoryDefinition for StoredMetaMetaflowConfiguration {
    fn memory_version() -> MemoryVersion {
        MemoryVersion::new(5)
    }

    fn schema_hash() -> SchemaHash {
        SchemaHash::for_label(META_METAFLOW_CONFIGURATION_SCHEMA)
    }
}

/// The archived declaration before a metaflow named its launch workspace.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(super) struct ConfigureMetaflowV4 {
    pub(super) address: Address,
    pub(super) system_modules: Vec<String>,
    pub(super) user_modules: Vec<String>,
    pub(super) flow_kind: signal_flow::FlowKind,
    pub(super) tool_set: signal_flow::ToolSet,
    pub(super) continuity: Continuity,
    pub(super) purpose: String,
    pub(super) records: Vec<String>,
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub(super) struct StoredMetaMetaflowConfigurationV4 {
    pub(super) metaflow: ConfigureMetaflowV4,
}

impl EngineRecord for StoredMetaMetaflowConfigurationV4 {
    fn record_key(&self) -> RecordKey {
        RecordKey::new(FlowStore::address_record_key(&self.metaflow.address))
    }
}

impl MemoryDefinition for StoredMetaMetaflowConfigurationV4 {
    fn memory_version() -> MemoryVersion {
        MemoryVersion::new(4)
    }

    fn schema_hash() -> SchemaHash {
        SchemaHash::for_label("flow-nexus-meta-metaflow-configuration-v4")
    }
}

impl UpgradeFrom<StoredMetaMetaflowConfigurationV4> for StoredMetaMetaflowConfiguration {
    type Refusal = std::convert::Infallible;

    fn upgrade_from(previous: StoredMetaMetaflowConfigurationV4) -> Decision<Self, Self::Refusal> {
        let previous = previous.metaflow;
        Decision::Ready(Self {
            metaflow: ConfigureMetaflow {
                address: previous.address,
                system_modules: previous.system_modules,
                user_modules: previous.user_modules,
                flow_kind: previous.flow_kind,
                tool_set: previous.tool_set,
                continuity: previous.continuity,
                purpose: previous.purpose,
                records: previous.records,
                root_option: None,
            },
        })
    }
}
```

## Descriptor and upgrade registration
`metaflow_declaration.rs:303-319`
```rust
pub(super) trait DescribesMetaflowDeclarationTable {
    fn descriptor() -> TableDescriptor<StoredMetaMetaflowConfiguration>;
}

impl DescribesMetaflowDeclarationTable for StoredMetaMetaflowConfiguration {
    fn descriptor() -> TableDescriptor<StoredMetaMetaflowConfiguration> {
        TableDescriptor::new(
            META_METAFLOW_CONFIGURATION_TABLE_NAME,
            FamilyName::new(META_METAFLOW_CONFIGURATION_FAMILY),
            SchemaHash::for_label(META_METAFLOW_CONFIGURATION_SCHEMA),
        )
        .with_predecessor::<StoredMetaMetaflowConfigurationV1>()
        .with_predecessor::<StoredMetaMetaflowConfigurationV2>()
        .with_predecessor::<StoredMetaMetaflowConfigurationV3>()
        .with_predecessor::<StoredMetaMetaflowConfigurationV4>()
    }
}
```

`store.rs:4308-4317` constructs the descriptor:
```rust
let meta_metaflows_descriptor = <metaflow_declaration::StoredMetaMetaflowConfiguration as metaflow_declaration::DescribesMetaflowDeclarationTable>::descriptor();
```
`store.rs:4324-4339` registers its family:
```rust
let mut engine = Engine::open(
    EngineOpen::new(path, SchemaVersion::new(FLOW_SCHEMA_VERSION))
        .with_family(&state_descriptor)
        .with_family(&configuration_descriptor)
        .with_family(&runtime_configuration_descriptor)
        .with_family(&delivery_configuration_descriptor)
        .with_family(&meta_nexus_descriptor)
        .with_family(&meta_models_descriptor)
        .with_family(&meta_thresholds_descriptor)
        .with_family(&meta_leave_outs_descriptor)
        .with_family(&meta_send_servers_descriptor)
        .with_family(&meta_investigation_descriptor)
        .with_family(&meta_default_minutes_descriptor)
        .with_family(&meta_harness_flags_descriptor)
        .with_family(&meta_heartbeat_descriptor)
        .with_family(&meta_metaflows_descriptor),
)?;
```

Catalog recognition exact `store.rs:8088-8104`:
```rust
"flow_nexus_meta_metaflow_configuration" => &[
    (
        metaflow_declaration::META_METAFLOW_CONFIGURATION_FAMILY,
        SchemaHash::for_label("flow-nexus-meta-metaflow-configuration-v1"),
    ),
    (
        metaflow_declaration::META_METAFLOW_CONFIGURATION_FAMILY,
        SchemaHash::for_label("flow-nexus-meta-metaflow-configuration-v2"),
    ),
    (
        metaflow_declaration::META_METAFLOW_CONFIGURATION_FAMILY,
        SchemaHash::for_label("flow-nexus-meta-metaflow-configuration-v3"),
    ),
    (
        metaflow_declaration::META_METAFLOW_CONFIGURATION_FAMILY,
        SchemaHash::for_label("flow-nexus-meta-metaflow-configuration-v4"),
    ),
],
```

## Readback
`metaflow_declaration.rs:391-419`
```rust
pub(crate) trait ReadsMetaflowDeclarations {
    /// The declaration of the metaflow at `address`, if Flow's configuration
    /// holds one.
    fn metaflow_declaration(
        &self,
        address: &Address,
    ) -> Result<Option<ConfigureMetaflow>, StoreError>;
}

impl ReadsMetaflowDeclarations for FlowStore {
    fn metaflow_declaration(
        &self,
        address: &Address,
    ) -> Result<Option<ConfigureMetaflow>, StoreError> {
        let records = self
            .engine
            .match_records(QueryPlan::key(
                self.meta_configuration_tables.metaflows,
                RecordKey::new(FlowStore::address_record_key(address)),
            ))?
            .records()
            .to_vec();
        match records.as_slice() {
            [] => Ok(None),
            [stored] => Ok(Some(stored.metaflow.clone())),
            _ => Err(StoreError::StateInvariant),
        }
    }
}
```

## Singleton/replacement write
`store.rs:8758-8760` is the declaration-family write:
```rust
ConfigurationChange::Metaflows(metaflows) => FlowStore::replace_configuration_family(
    engine,
    tables.metaflows,
    metaflows
        .into_iter()
        .map(|metaflow| StoredMetaMetaflowConfiguration { metaflow })
        .collect(),
```
Each row is keyed by `FlowStore::address_record_key(&self.metaflow.address)`; there is no singleton constant for this family (one row per Address).

## EngineStoredValue blanket
Dependency source `/git/worktrees/sema-engine-config-d05351-independent/src/record.rs:149-179`:
```rust
pub trait EngineStoredValue:
    Archive
    + Clone
    + for<'serialize> RkyvSerialize<
        Strategy<Serializer<AlignedVec, ArenaHandle<'serialize>, Share>, rancor::Error>,
    >
where
    Self::Archived: RkyvDeserialize<Self, HighDeserializer<rancor::Error>>
        + for<'validation> CheckBytes<
            Strategy<Validator<ArchiveValidator<'validation>, SharedValidator>, rancor::Error>,
        >,
{
}

impl<RecordValue> EngineStoredValue for RecordValue
where
    RecordValue: Archive
        + Clone
        + for<'serialize> RkyvSerialize<
            Strategy<Serializer<AlignedVec, ArenaHandle<'serialize>, Share>, rancor::Error>,
        >,
    RecordValue::Archived: RkyvDeserialize<RecordValue, HighDeserializer<rancor::Error>>
        + for<'validation> CheckBytes<
            Strategy<Validator<ArchiveValidator<'validation>, SharedValidator>, rancor::Error>,
        >,
{
}
```
