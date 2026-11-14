# Engine consumer ledger — exact 217-match classification

Scope query artifact: `engine-api-query-results.txt`; all 217 matches copied verbatim in the machine artifact. Inline `#[cfg(test)] mod tests` context was checked: `store.rs:8871-14601` and identified test-only callsites in `send_call.rs:655,672,689`, `send_outcome.rs:661,672,674,682,716`, and `store_check.rs:187`; the remaining Flow hits before test modules are production. The query itself has no external `tests/` paths.

## Approved route and oracle

Opening calls use `Engine::open(EngineOpen...)` / `Engine::open_recovering` with `EngineOpen.with_family`, then `register_table`/`upgrade_table`; planned oracle: catalog/schema admission and reopen fixtures. Writes use `Engine::begin_atomic_commit` → typed assert/mutate/retract → `Engine::commit_atomic`; planned oracle: one receipt, atomic rows/log/counters, fault boundaries. Upgrade calls use `MemoryUpgrades::upgrade_table`; planned oracle: predecessor fixture/readback and no partial writes.

## Per-file exact callsites

### `crates/flow-nexus/src/store/nexus_configuration.rs` — owner: FlowStore sub-family owner: nexus_configuration.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/nexus_configuration.rs:284` — `        match self.upgrade_table::<StoredMetaNexusConfigurationV3, StoredMetaNexusConfiguration>(`
- `crates/flow-nexus/src/store/nexus_configuration.rs:294` — `                match self.upgrade_table::<`
- `crates/flow-nexus/src/store/nexus_configuration.rs:304` — `                        match self.upgrade_table::<`

### `crates/flow-nexus/src/store/counters.rs` — owner: FlowStore sub-family owner: counters.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/counters.rs:88` — `        let commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/counters.rs:93` — `        self.engine.commit_atomic(commit)?;`

### `crates/flow-nexus/src/store/repair.rs` — owner: FlowStore sub-family owner: repair.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/repair.rs:106` — `        let commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/repair.rs:111` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/repair.rs:142` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store/repair.rs:144` — `                .begin_atomic_commit()`

### `crates/flow-nexus/src/store/send_call.rs` — owner: FlowStore sub-family owner: send_call.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/send_call.rs:621` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store/send_call.rs:623` — `                .begin_atomic_commit()`
- `crates/flow-nexus/src/store/send_call.rs:655` — `            Engine::open(EngineOpen::new(path, SchemaVersion::new(1))).expect("store opens");`
- `crates/flow-nexus/src/store/send_call.rs:672` — `            Engine::open(EngineOpen::new(path, SchemaVersion::new(1))).expect("store opens");`
- `crates/flow-nexus/src/store/send_call.rs:689` — `            Engine::open(EngineOpen::new(path, SchemaVersion::new(1))).expect("store opens");`

### `crates/flow-nexus/src/store/address_hold.rs` — owner: FlowStore sub-family owner: address_hold.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/address_hold.rs:417` — `            let commit = self.given_back(&hold.flow_id, self.engine.begin_atomic_commit())?;`
- `crates/flow-nexus/src/store/address_hold.rs:418` — `            self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/address_hold.rs:437` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/address_hold.rs:458` — `            .commit_atomic(commit)`

### `crates/flow-nexus/src/store/queue_delivery.rs` — owner: FlowStore sub-family owner: queue_delivery.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/queue_delivery.rs:66` — `            self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/queue_delivery.rs:611` — `            .upgrade_table::<StoredDeliveryRequestV5, StoredDeliveryRequest>(descriptor.clone())`
- `crates/flow-nexus/src/store/queue_delivery.rs:623` — `            .upgrade_table::<StoredDeliveryRequestV4, StoredDeliveryRequest>(descriptor.clone())`
- `crates/flow-nexus/src/store/queue_delivery.rs:635` — `        match engine.upgrade_table::<StoredDeliveryRequestV3, StoredDeliveryRequest>(descriptor) {`
- `crates/flow-nexus/src/store/queue_delivery.rs:643` — `                    .upgrade_table::<StoredDeliveryRequestV2, StoredDeliveryRequest>(from_v2)`
- `crates/flow-nexus/src/store/queue_delivery.rs:664` — `        match engine.upgrade_table::<QueueDeliveryAttemptV6, QueueDeliveryAttempt>(descriptor) {`
- `crates/flow-nexus/src/store/queue_delivery.rs:675` — `        match engine.upgrade_table::<QueueDeliveryAttemptV5, QueueDeliveryAttempt>(from_v5) {`
- `crates/flow-nexus/src/store/queue_delivery.rs:682` — `                match engine.upgrade_table::<QueueDeliveryAttemptV4, QueueDeliveryAttempt>(from_v4)`
- `crates/flow-nexus/src/store/queue_delivery.rs:968` — `        let mut commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/queue_delivery.rs:1028` — `            self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/queue_delivery.rs:1174` — `        let commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/queue_delivery.rs:1284` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1363` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1409` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1412` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/queue_delivery.rs:1426` — `                    .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1461` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1504` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1582` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1633` — `                        .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1696` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:1711` — `            self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/queue_delivery.rs:2684` — `            .commit_atomic(`
- `crates/flow-nexus/src/store/queue_delivery.rs:2687` — `                    .begin_atomic_commit()`
- `crates/flow-nexus/src/store/queue_delivery.rs:3116` — `            let mut engine = Engine::open(EngineOpen::new(&fixture.path, SchemaVersion::new(1)))`

### `crates/flow-nexus/src/store/metaflow_declaration.rs` — owner: FlowStore sub-family owner: metaflow_declaration.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/metaflow_declaration.rs:339` — `            .upgrade_table::<StoredMetaMetaflowConfigurationV4, StoredMetaMetaflowConfiguration>(`
- `crates/flow-nexus/src/store/metaflow_declaration.rs:352` — `            .upgrade_table::<StoredMetaMetaflowConfigurationV3, StoredMetaMetaflowConfiguration>(`
- `crates/flow-nexus/src/store/metaflow_declaration.rs:365` — `            .upgrade_table::<StoredMetaMetaflowConfigurationV2, StoredMetaMetaflowConfiguration>(`
- `crates/flow-nexus/src/store/metaflow_declaration.rs:378` — `            .upgrade_table::<StoredMetaMetaflowConfigurationV1, StoredMetaMetaflowConfiguration>(`

### `crates/flow-nexus/src/store/send_outcome.rs` — owner: FlowStore sub-family owner: send_outcome.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/send_outcome.rs:446` — `        match self.upgrade_table::<StoredSendOutcomeV5, StoredSendOutcome>(descriptor.clone()) {`
- `crates/flow-nexus/src/store/send_outcome.rs:454` — `        match self.upgrade_table::<StoredSendOutcomeV4, StoredSendOutcome>(descriptor.clone()) {`
- `crates/flow-nexus/src/store/send_outcome.rs:462` — `        match self.upgrade_table::<StoredSendOutcomeV3, StoredSendOutcome>(descriptor.clone()) {`
- `crates/flow-nexus/src/store/send_outcome.rs:470` — `        match self.upgrade_table::<StoredSendOutcomeV2, StoredSendOutcome>(descriptor.clone()) {`
- `crates/flow-nexus/src/store/send_outcome.rs:478` — `        match self.upgrade_table::<StoredSendOutcomeV1, StoredSendOutcome>(descriptor) {`
- `crates/flow-nexus/src/store/send_outcome.rs:551` — `        let counter_mutation = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/send_outcome.rs:557` — `        self.engine.commit_atomic(counter_mutation.assert(`
- `crates/flow-nexus/src/store/send_outcome.rs:661` — `            let mut engine = Engine::open(`
- `crates/flow-nexus/src/store/send_outcome.rs:672` — `                .commit_atomic(`
- `crates/flow-nexus/src/store/send_outcome.rs:674` — `                        .begin_atomic_commit()`
- `crates/flow-nexus/src/store/send_outcome.rs:682` — `            let mut engine = Engine::open(`
- `crates/flow-nexus/src/store/send_outcome.rs:716` — `            let mut engine = Engine::open(EngineOpen::new(&store_path, SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store/send_outcome.rs:763` — `        let mut engine = Engine::open(`
- `crates/flow-nexus/src/store/send_outcome.rs:834` — `            let mut engine = Engine::open(EngineOpen::new(&store_path, SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store/send_outcome.rs:881` — `        let mut engine = Engine::open(`
- `crates/flow-nexus/src/store/send_outcome.rs:957` — `            let mut engine = Engine::open(EngineOpen::new(&store_path, SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store/send_outcome.rs:995` — `        let mut engine = Engine::open(`

### `crates/flow-nexus/src/store/metaflow.rs` — owner: FlowStore sub-family owner: metaflow.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/metaflow.rs:36` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store/metaflow.rs:38` — `                .begin_atomic_commit()`
- `crates/flow-nexus/src/store/metaflow.rs:177` — `        let commit = self.engine.begin_atomic_commit().mutate(`
- `crates/flow-nexus/src/store/metaflow.rs:197` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/metaflow.rs:254` — `        let commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/metaflow.rs:260` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/metaflow.rs:328` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/metaflow.rs:331` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/metaflow.rs:349` — `            taken.written(self, self.engine.begin_atomic_commit()),`
- `crates/flow-nexus/src/store/metaflow.rs:351` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/metaflow.rs:370` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/metaflow.rs:372` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/metaflow.rs:605` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/metaflow.rs:611` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/metaflow.rs:666` — `        let commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/metaflow.rs:672` — `        self.engine.commit_atomic(commit).expect("metaflow seeded");`

### `crates/flow-nexus/src/store/delivery.rs` — owner: FlowStore sub-family owner: delivery.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/delivery.rs:231` — `                .upgrade_table::<DeliveryConfigurationV1, DeliveryConfiguration>(`
- `crates/flow-nexus/src/store/delivery.rs:324` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/delivery.rs:329` — `        self.engine.commit_atomic(commit)?;`

### `crates/flow-nexus/src/store/successor.rs` — owner: FlowStore sub-family owner: successor.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/successor.rs:153` — `        match self.upgrade_table::<SuccessorIntentV1, SuccessorIntent>(descriptor) {`
- `crates/flow-nexus/src/store/successor.rs:231` — `        let commit = self.owing_successor(intent, self.engine.begin_atomic_commit())?;`
- `crates/flow-nexus/src/store/successor.rs:232` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/successor.rs:265` — `        let commit = self.successor_given(address, self.engine.begin_atomic_commit())?;`
- `crates/flow-nexus/src/store/successor.rs:266` — `        self.engine.commit_atomic(commit)?;`

### `crates/flow-nexus/src/store/logical_delivery.rs` — owner: FlowStore sub-family owner: logical_delivery.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/logical_delivery.rs:417` — `            .upgrade_table::<CurrentLogicalDeliveryV4, CurrentLogicalDelivery>(descriptor.clone())`
- `crates/flow-nexus/src/store/logical_delivery.rs:427` — `            .upgrade_table::<CurrentLogicalDeliveryV3, CurrentLogicalDelivery>(descriptor.clone())`
- `crates/flow-nexus/src/store/logical_delivery.rs:437` — `            .upgrade_table::<CurrentLogicalDeliveryV2, CurrentLogicalDelivery>(descriptor.clone())`
- `crates/flow-nexus/src/store/logical_delivery.rs:446` — `        match engine.upgrade_table::<CurrentLogicalDeliveryV1, CurrentLogicalDelivery>(descriptor) {`
- `crates/flow-nexus/src/store/logical_delivery.rs:461` — `            .upgrade_table::<LogicalDeliveryEventV4, LogicalDeliveryEvent>(descriptor.clone())`
- `crates/flow-nexus/src/store/logical_delivery.rs:471` — `            .upgrade_table::<LogicalDeliveryEventV3, LogicalDeliveryEvent>(descriptor.clone())`
- `crates/flow-nexus/src/store/logical_delivery.rs:481` — `            .upgrade_table::<LogicalDeliveryEventV2, LogicalDeliveryEvent>(descriptor.clone())`
- `crates/flow-nexus/src/store/logical_delivery.rs:490` — `        match engine.upgrade_table::<LogicalDeliveryEventV1, LogicalDeliveryEvent>(descriptor) {`
- `crates/flow-nexus/src/store/logical_delivery.rs:731` — `        let mut commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/logical_delivery.rs:797` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/logical_delivery.rs:819` — `                    .begin_atomic_commit()`
- `crates/flow-nexus/src/store/logical_delivery.rs:821` — `                self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/logical_delivery.rs:941` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/logical_delivery.rs:988` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store/logical_delivery.rs:1092` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/logical_delivery.rs:1100` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store/logical_delivery.rs:1142` — `            self.engine.commit_atomic(`
- `crates/flow-nexus/src/store/logical_delivery.rs:1144` — `                    .begin_atomic_commit()`
- `crates/flow-nexus/src/store/logical_delivery.rs:1323` — `        let mut commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store/logical_delivery.rs:1344` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/logical_delivery.rs:1451` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store/logical_delivery.rs:1533` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/logical_delivery.rs:1549` — `        self.commit_logical_transition(id, state, self.engine.begin_atomic_commit())`
- `crates/flow-nexus/src/store/logical_delivery.rs:1571` — `                    self.engine.begin_atomic_commit(),`
- `crates/flow-nexus/src/store/logical_delivery.rs:1600` — `            self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store/logical_delivery.rs:1631` — `        self.engine.commit_atomic(commit)?;`

### `crates/flow-nexus/src/store/events.rs` — owner: FlowStore sub-family owner: events.rs

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store/events.rs:266` — `        match engine.upgrade_table::<FlowEventsV3, FlowEvents>(descriptor) {`
- `crates/flow-nexus/src/store/events.rs:286` — `        let events = match engine.upgrade_table::<FlowEventsV2, FlowEvents>(from_v2) {`
- `crates/flow-nexus/src/store/events.rs:293` — `                match engine.upgrade_table::<FlowEventsV1, FlowEvents>(from_v1) {`

### `crates/flow-nexus/src/store.rs` — owner: FlowStore opening/configuration/lifecycle owner

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store.rs:286` — `// compatibility decision; Engine::open must not silently refold an occupant.`
- `crates/flow-nexus/src/store.rs:3640` — `            .upgrade_table::<StoredMetaModelConfigurationV1, StoredMetaModelConfiguration>(`
- `crates/flow-nexus/src/store.rs:3654` — `        let mut commit = self.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:3669` — `            self.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:3679` — `            .upgrade_table::<StoredMetaLeaveOutConfigurationV1, StoredMetaLeaveOutConfiguration>(`
- `crates/flow-nexus/src/store.rs:3698` — `        let mut commit = self.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:3715` — `            self.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:3725` — `        match self.upgrade_table::<StoredMetaflowV5, StoredMetaflow>(descriptor) {`
- `crates/flow-nexus/src/store.rs:3740` — `        match self.upgrade_table::<StoredMetaflowV4, StoredMetaflow>(from_v4) {`
- `crates/flow-nexus/src/store.rs:3752` — `        match self.upgrade_table::<StoredMetaflowV3, StoredMetaflow>(from_v3) {`
- `crates/flow-nexus/src/store.rs:3762` — `        match self.upgrade_table::<StoredMetaflowV2, StoredMetaflow>(from_v2) {`
- `crates/flow-nexus/src/store.rs:3769` — `                match self.upgrade_table::<StoredMetaflowV1, StoredMetaflow>(from_v1) {`
- `crates/flow-nexus/src/store.rs:3790` — `            .upgrade_table::<address_hold::AddressHoldV4, address_hold::AddressHold>(descriptor)`
- `crates/flow-nexus/src/store.rs:3803` — `        match self.upgrade_table::<address_hold::AddressHoldV3, address_hold::AddressHold>(from_v3)`
- `crates/flow-nexus/src/store.rs:3814` — `        match self.upgrade_table::<address_hold::AddressHoldV2, address_hold::AddressHold>(from_v2)`
- `crates/flow-nexus/src/store.rs:3822` — `                match self.upgrade_table::<address_hold::AddressHoldV1, address_hold::AddressHold>(`
- `crates/flow-nexus/src/store.rs:3845` — `        match self.upgrade_table::<send_call::SendCallV5, crate::generated::send_tool::SendCall>(`
- `crates/flow-nexus/src/store.rs:3857` — `        match self.upgrade_table::<send_call::SendCallV4, crate::generated::send_tool::SendCall>(`
- `crates/flow-nexus/src/store.rs:3869` — `        match self.upgrade_table::<send_call::SendCallV3, crate::generated::send_tool::SendCall>(`
- `crates/flow-nexus/src/store.rs:3878` — `                match self.upgrade_table::<send_call::SendCallV2, crate::generated::send_tool::SendCall>(descriptor.clone()) {`
- `crates/flow-nexus/src/store.rs:3889` — `                    .upgrade_table::<send_call::SendCallV1, crate::generated::send_tool::SendCall>(`
- `crates/flow-nexus/src/store.rs:3916` — `        match self.upgrade_table::<FlowRecordV5, FlowRecord>(descriptor) {`
- `crates/flow-nexus/src/store.rs:3950` — `        match self.upgrade_table::<StoredLaunchOutcomeV8, StoredLaunchOutcome>(descriptor) {`
- `crates/flow-nexus/src/store.rs:3957` — `        match self.upgrade_table::<StoredLaunchOutcomeV7, StoredLaunchOutcome>(from_v7) {`
- `crates/flow-nexus/src/store.rs:3964` — `        match self.upgrade_table::<StoredLaunchOutcomeV6, StoredLaunchOutcome>(from_v6) {`
- `crates/flow-nexus/src/store.rs:3971` — `        match self.upgrade_table::<StoredLaunchOutcomeV5, StoredLaunchOutcome>(from_v5) {`
- `crates/flow-nexus/src/store.rs:3978` — `        match self.upgrade_table::<StoredLaunchOutcomeV4, StoredLaunchOutcome>(from_v4) {`
- `crates/flow-nexus/src/store.rs:3985` — `        match self.upgrade_table::<StoredLaunchOutcomeV3, StoredLaunchOutcome>(from_v3) {`
- `crates/flow-nexus/src/store.rs:3992` — `        match self.upgrade_table::<StoredLaunchOutcomeV2, StoredLaunchOutcome>(from_v2) {`
- `crates/flow-nexus/src/store.rs:4046` — `            self.upgrade_table::<StoredLaunchAttemptV1, StoredLaunchAttempt>(descriptor)`
- `crates/flow-nexus/src/store.rs:4048` — `            self.upgrade_table::<StoredLaunchAttemptV2, StoredLaunchAttempt>(descriptor)`
- `crates/flow-nexus/src/store.rs:4056` — `            self.upgrade_table::<StoredLaunchAttemptV3, StoredLaunchAttempt>(descriptor)`
- `crates/flow-nexus/src/store.rs:4172` — `        let mut commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:4188` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:4324` — `        let mut engine = Engine::open(`
- `crates/flow-nexus/src/store.rs:4345` — `            .upgrade_table::<delivery::DeliveryConfigurationV1, DeliveryConfiguration>(`
- `crates/flow-nexus/src/store.rs:4454` — `                    .begin_atomic_commit()`
- `crates/flow-nexus/src/store.rs:4466` — `                    .begin_atomic_commit()`
- `crates/flow-nexus/src/store.rs:4473` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:4899` — `        let mut engine = Engine::open(`
- `crates/flow-nexus/src/store.rs:5044` — `        let mut engine = Engine::open(EngineOpen::new(path, SchemaVersion::new(1)))?;`
- `crates/flow-nexus/src/store.rs:5670` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store.rs:5672` — `                .begin_atomic_commit()`
- `crates/flow-nexus/src/store.rs:5796` — `            .begin_atomic_commit()`
- `crates/flow-nexus/src/store.rs:5809` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:5883` — `            self.commit_atomic(`
- `crates/flow-nexus/src/store.rs:5884` — `                self.begin_atomic_commit()`
- `crates/flow-nexus/src/store.rs:6209` — `        let mut commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:6248` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:6432` — `            self.engine.begin_atomic_commit(),`
- `crates/flow-nexus/src/store.rs:6440` — `            .commit_atomic(commit.mutate(self.launch_attempts, stored))?;`
- `crates/flow-nexus/src/store.rs:6690` — `        let commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:6703` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:7139` — `        let commit = self.engine.begin_atomic_commit().mutate(self.flows, flow);`
- `crates/flow-nexus/src/store.rs:7141` — `            .commit_atomic(self.ended_at_address(flow_id, commit)?)?;`
- `crates/flow-nexus/src/store.rs:7156` — `        let commit = self.engine.begin_atomic_commit().mutate(self.flows, flow);`
- `crates/flow-nexus/src/store.rs:7158` — `            .commit_atomic(self.ended_at_address(flow_id, commit)?)?;`
- `crates/flow-nexus/src/store.rs:7179` — `        let commit = self.engine.begin_atomic_commit().mutate(self.flows, flow);`
- `crates/flow-nexus/src/store.rs:7199` — `            .commit_atomic(self.ended_at_address(flow_id, commit)?)?;`
- `crates/flow-nexus/src/store.rs:7219` — `        let mut commit = self.engine.begin_atomic_commit().mutate(self.flows, flow);`
- `crates/flow-nexus/src/store.rs:7226` — `        self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:7250` — `        self.engine.commit_atomic(`
- `crates/flow-nexus/src/store.rs:7252` — `                .begin_atomic_commit()`
- `crates/flow-nexus/src/store.rs:7343` — `        let mut commit = self.engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:7365` — `            self.engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:7650` — `        let mut engine = Engine::open(EngineOpen::new(path, SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:8643` — `        let mut commit = engine.begin_atomic_commit();`
- `crates/flow-nexus/src/store.rs:8670` — `        engine.commit_atomic(commit)?;`
- `crates/flow-nexus/src/store.rs:8993` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:9091` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:9227` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:9486` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:10227` — `            let mut engine = Engine::open(EngineOpen::new(self.path(), SchemaVersion::new(schema)))`
- `crates/flow-nexus/src/store.rs:10346` — `            let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:10391` — `            let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:10422` — `            let mut engine = Engine::open(EngineOpen::new(self.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:11323` — `            let mut engine = Engine::open(EngineOpen::new(&path, SchemaVersion::new(2)))`
- `crates/flow-nexus/src/store.rs:11494` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:11567` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:11595` — `        let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:12639` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:12712` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:12814` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:12917` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13014` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13087` — `        let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13228` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13318` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13415` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13532` — `            let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13742` — `        let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13763` — `        let mut engine = Engine::open(EngineOpen::new(fixture.path(), SchemaVersion::new(1)))`
- `crates/flow-nexus/src/store.rs:13867` — `            let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:14228` — `            let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:14273` — `            let mut engine = Engine::open(EngineOpen::new(`
- `crates/flow-nexus/src/store.rs:14601` — `                Engine::open(EngineOpen::new(&path, SchemaVersion::new(1))).expect("store opens");`

### `crates/flow-nexus/src/store_check.rs` — owner: Flow verifier/open owner

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `crates/flow-nexus/src/store_check.rs:187` — `            let mut engine = Engine::open(EngineOpen::new(&path, SchemaVersion::new(2))).unwrap();`

### `/git/worktrees/sema-engine-config-d05351-independent/src/error.rs` — owner: sema-engine API declaration/engine implementation (not an application consumer)

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `/git/worktrees/sema-engine-config-d05351-independent/src/error.rs:198` — `        "a durable compaction intent is pending in phase {phase:?}; open through Engine::open_recovering"`

### `/git/worktrees/sema-engine-config-d05351-independent/src/engine.rs` — owner: sema-engine API declaration/engine implementation (not an application consumer)

All listed locations are production/source matches from the exact query; intended route is the approved route above; planned oracle is the corresponding owner-family reopen/atomic test.

- `/git/worktrees/sema-engine-config-d05351-independent/src/engine.rs:119` — `    /// Call [`Engine::open_recovering`] from a supervised owner when a family`
- `/git/worktrees/sema-engine-config-d05351-independent/src/engine.rs:3869` — `            Engine::open(`

## Query provenance

Exact command:
```text
grep -R -n "\.begin_atomic_commit\|\.commit_atomic\|\.upgrade_table::<\|Engine::open\|Engine::open_recovering" crates/flow-nexus/src /git/worktrees/sema-engine-config-d05351-independent/src --include='*.rs'
```

The query returned 217 lines: 214 Flow source matches and 3 sema-engine source matches. Inline test classification is recorded above; external test directories were not included in the original command.

## Inline test classification

Exact test-only matches and enclosing test context: `crates/flow-nexus/src/store.rs:8993,9091,9227,9486,10227,10346,10391,10422,11323,11494,11567,11595,12639,12712,12814,12917,13014,13087,13228,13318,13415,13532,13742,13763,13867,14228,14273,14601` are under `#[cfg(test)] mod tests` beginning `store.rs:8871`; `store/send_call.rs:655,672,689`, `store/send_outcome.rs:661,672,674,682,716`, and `store_check.rs:187` are under their inline test modules. Their owner is test fixture/open/commit setup; oracle is existing test expectation, not production route. The production `store.rs` calls before line 8871 retain FlowStore owners.

## Engine own source query

A second exact query `grep -R -n "Engine::open\|open_unrecovered\|begin_atomic_commit\|commit_atomic\|upgrade_table" /git/worktrees/sema-engine-config-d05351-independent/src /git/worktrees/sema-engine-config-d05351-independent/tests` produced 73 lines in `engine-own-query-results.txt`. These are Engine implementation/tests, not application consumers; declarations are `src/engine.rs:121,133,142`, `src/atomic.rs:302,308`, `src/memory/upgrade.rs:39,61`.
