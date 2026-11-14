# Per-address declaration delta — bounded existing source ledger

Parent read-only source pointers, codec worker uninterrupted. These locations describe current prepared Flow916/meta base, not a new operation/result design. New declaration bodies are explicitly held pending authored contract/dependent-persistence review/independent delta gate. Existing approved codec/backend slices continue.

## Wire anatomy and dispatch

- Meta `ethos/signal.ethos:308`: `ConfigureMetaflow.{ Address Option<Root> SystemModules UserModules FlowKind ToolSet Continuity Purpose Records }`.
- `:320–330`: ConfigurationChange is an enum of family changes; current declaration variant is `Metaflows.Vector<ConfigureMetaflow>`. Other vector policies are separate variants. `:331` ConfigureOutcome.[Replaced Unchanged]. `:339` ConfigureRejection.[StoreRefused DuplicateEntry CodexModelsOverlap LeaveOutNotForHarness TopicRefused.Topic MinutesRefused.MinutesRefusal CountersRefused.CountersRefusal]. `:207` Query.Configure.ConfigurationChange; `:227,232` Configured/ConfigureRejected reply wrappers.
- Snapshot `:332` retains `Metaflows.Vector<ConfigureMetaflow>` as observed committed declarations. Changing an operation does not itself determine changing this observation collection.
- Normal meta dispatch `flow-nexus/src/lib.rs:352–375` Configuration returns snapshot; Configure passes change to store.configure_change and maps outcomes/rejections. Configure-only dispatch `main.rs:265ff` does the same under authorized peer guard; all exact current variants must be made exhaustive under the delta.
- `store.rs:4264,4390ff` configuration-only trait/impl and `:5297,5347ff` running trait/impl reach `configure_meta_change:8677ff`, apart from Counters' retained special family capability.

## Current replacement behavior and read consumers

- `store.rs:8686–8703` validates topic in every Address named by relevant variants; current Metaflows iterates all entries. `:8758–8769` maps every declaration to StoredMetaMetaflowConfiguration and calls generic replace_configuration_family.
- Generic `replace_configuration_family:~8580–8672` computes declared keys, rejects repeated keys before write, reads all committed rows, retracts omitted keys, mutates unequal rows, asserts missing rows, leaves identical rows unchanged, then one atomic commit. Outcomes Unchanged/Replaced. This is the exact currently-destructive whole-family path the new ruling removes ONLY for declarations.
- `store/metaflow_declaration.rs:394–419` ReadsMetaflowDeclarations::metaflow_declaration(&self,address:&Address)->Result<Option<ConfigureMetaflow>,StoreError> queries one `address_record_key`, returns None/one cloned declaration/invariant failure on several.
- Production callers of that one-address read: `launching.rs:229`; `waking.rs:626,1471,1664`; `store/successor.rs:174`; `store/metaflow.rs:23`; `sending.rs:544,1270,1406`; `lib.rs:330`. These consume presence/absence for launch/wake/succession/admission. Removal existence/active-seat semantics are not resolved by this ledger.
- `store.rs:8516` snapshot read loads all declaration rows; `:8550ff` maps/sorts them by Address key. `ConfiguredFamilies:4208–4239` has Vec<ConfigureMetaflow> and creates ConfigurationSnapshot, but derives only Debug/Clone/PartialEq/Eq, not Archive. Main lifecycle Metaflow storage (`self.metaflows`) is distinct from configuration table (`meta_configuration_tables.metaflows`).

## Direct persisted embedding and frozen histories

- `store/metaflow_declaration.rs:21–45`: table `flow_nexus_meta_metaflow_configuration`, family `flow-nexus-meta-metaflow-configuration`, schema v5; `StoredMetaMetaflowConfiguration { metaflow: ConfigureMetaflow }` derives Archive and is keyed by existing address_record_key. Thus the shared payload is directly persisted; operation-only enum changes and payload changes have different reachability.
- V4 frozen payload/wrapper `:52–103`; V3 `:148–198`; V2 `:203–250`; V1 `:255–300`. Current upgrades construct latest ConfigureMetaflow; table-opening upgrade chain `:~302–389` reaches those histories. Accepted unchanged packet already requires exact frozenV5/rootSECOND before v6 CONFIG, not main lifecycle migration.
- Finite direct-type query in `declaration-direct-embedding-query.txt` covers meta Query/Response, ConfigurationChange/Snapshot and ConfigureMetaflow spellings under `flow-nexus/src/store`. Production direct declaration embedding is the wrapper above. Other matches are wrapper histories/readers or fixtures; `store/counters.rs` mentions ConfigureOutcome as return, not an archived row field. This query is a direct-type receipt, not a claim that transitive enum reachability has been exhaustively audited.

## Existing startup/producers and fixtures

- Current actual Start is only ordinary_socket_path/meta_socket_path/store_path: `flow-nexus/ethos/startup.ethos:6–10`, generated startup10–14. Current source has NO accepted future startup change-vector implementation yet; new multiple-per-address atomic startup semantics must enter the already-designed052 opening plan, not be inferred as existing behavior.
- `capsule/configure.datom:13` contains one whole-family Configure.Metaflows vector for four test addresses. Header says one Configure datum per line applied in order over meta socket; this is the exact current producer shape.
- Clojure `configure-lines:995–1001` reads placeholder-expanded config lines, `configure!:1003–1008` sends each. `configure-only:~980` runs `flow-nexus --configure-only start` before sending. Existing one-line replay is not one startup transaction.
- Producers transforming the whole-family string: `on-demand-secondary:371–376`, `workspace-configuration:378–389`, `seat-declaration:778ff`, `takeover-configuration:1409–1436` (vector append/rewrite; :old removes root for older binary and omits DefaultMinutes). These all need explicit producer updates, not a rename of the wire variant alone.
- Direct producer fixture locations from bounded literal query: `capsule/flow-capsule-test.clj:124–125,135–149,266,277,374–386`; source test consumers `flow-nexus/src/tests/rehearsing.rs:217–229`, `tests/secondary.rs:135–157`, `store.rs:9139` plus declaration tests/configuring fixtures. Historical bytes and legacy takeover generation must remain explicitly separated from current052 producer shape.

## Exact scope boundary

Core ruling to design against: define/replace/remove ONE declaration per Address; startup may contain multiple explicit per-address operations in one validated transaction, omission preserves unrelated rows, duplicate/conflicting operations for one Address refuse; other vector families unchanged. This ledger does not choose operation/result names, existence semantics, removal interaction with active seats, or schema reachability. Those remain Primary/Core design+independent gate; no declaration-delta source edit is authorized.
