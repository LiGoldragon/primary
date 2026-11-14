# Decoded facade: pinned signature compatibility, not independent PASS

Scope: Primary proposal 052-redb-scoped-value-correction.md SHA25656f9f535fff33a7cab2e82602714ed7fb5437a47a9de8e7fd55c2e16913a7630, redb1bd09903, held Sema diff, unchanged Engine9884905. No source edits, builds, new worker or status RPC performed.

## Exact pinned bounds and signatures

redb source/src/types.rs152–180:
```rust
pub trait Value: core::fmt::Debug {
    type SelfType<'a>: core::fmt::Debug + 'a where Self: 'a;
    type AsBytes<'a>: AsRef<[u8]> + 'a where Self: 'a;
    fn fixed_width() -> Option<usize>;
    fn from_bytes<'a>(data: &'a [u8]) -> Self::SelfType<'a> where Self: 'a;
    fn as_bytes<'a, 'b: 'a>(value: &'a Self::SelfType<'b>) -> Self::AsBytes<'a>
    where Self: 'b;
    fn type_name() -> TypeName;
}
pub trait Key: Value { /* compare and default separator/minimum */ }
```
Both ReadOnlyTable<K,V> and TableDefinition<'name,K,V> require K:Key+'static,V:Value+'static. Those static type bounds discharge the GAT Self:'value/Self:'entry clauses for arbitrary callback lifetimes; they do not turn decoded references into static references. TableDefinition has a distinct name lifetime, unrelated to the read view.

Pinned Result<T=(),E=StorageError> is core::result::Result<T,E>. Native table-opening error is TableError; get/iter/entry errors are StorageError. ScopedRead opens native ReadOnlyTable privately; the proposed public facade must not expose that type. Existing outer with_read returns Result<T,ReadFailure<E>> with Begin(TransactionError) and Read(E).

The proposal's method signatures are source-compatible in their bounds with these pinned traits (not compiled proof):
```rust
// Inside a facade with K: Key + 'static, V: Value + 'static:
fn with_value<'key, R, E>(
    &self,
    key: impl core::borrow::Borrow<K::SelfType<'key>>,
    f: impl for<'value> FnOnce(Option<V::SelfType<'value>>) -> core::result::Result<R,E>,
) -> core::result::Result<R,E>
where E: From<StorageError>;

fn for_each<E>(
    &self,
    f: impl for<'entry> FnMut(K::SelfType<'entry>,V::SelfType<'entry>)
        -> core::result::Result<(),E>,
) -> core::result::Result<(),E>
where E: From<StorageError>;
```
R and E stay outside each binder. A facade reference supplied under a fresh with_table callback lifetime must likewise keep returned R/E independent of that lifetime. Exact facade declaration/with_table definition and compiler behavior remain independent-check obligations; no unchecked sketch here replaces them. No extra Clone/Send/'static result bound follows from Value/Key. Do not add such bounds merely to make tests compile.

## Concrete current compatibility gap

Held SemaInspectionError src/lib.rs495–504 has Redb(InspectionError), Read(TransactionError), Table(#[from]TableError), DatabaseHeaderDecode{source:rancor::Error}. It has NO From<StorageError>. The proposed E:From<StorageError> is therefore NOT met by this current observation error type. Existing held `table.get(...)?` already needs this conversion, so held source is not compile evidence. Ordinary sema::Error has distinct Storage/Transaction/Table #[from] variants; SemaInspectionError does not. Rust does not chain StorageError→TableError→SemaInspectionError automatically. Pinned TableError::Storage(StorageError) and From<StorageError> for TableError exist (error.rs195/237), preserving the native payload if Primary chooses an explicit conversion. Primary must select/approve the inspection error conversion; this report makes no source change or design choice.

## Finite consumers

- Sema header: with_value for &str key database and &[u8] value; within callback rkyv::from_bytes::<DatabaseHeader,rancor::Error> produces an owned record. Missing key→None; TableDoesNotExist→None, other native errors retained.
- Sema schema: &str schema_version/u64; callback may return Option<u64> directly. Schema is Option<u64>, not fabricated zero.
- Engine catalog: current sema Table<&str,TableRegistration> physically uses redb byte values; for_each must turn key &str into String and bytes into owned TableRegistration before returning/accumulating. Existing Table::iter returns Vec<(K::Owned,V)>, with &'static str Owned=String. No raw archive reference may leave.
- Engine counters: &str→rkyv bytes decoded into owned u64 (unlike Sema META's native redb u64).
- Engine versioning policy: &str→rkyv bytes decoded into owned VersioningPolicy.
- Older-layout startup reads VERSIONED_COMMIT_LOG and COMMIT_LOG through current typed iter; both must decode owned finite records inside callback if included in the approved plan. No repair/write is implied.

## Proposed independent check ownership and acceptance — not launched

Owner appointment is pending Primary/Core and exact old reviewer reconciliation. Existing reviewer /root/review_protos_slice native01a1adff-cafa-77a1-aa73-aa98b4dd4794 status remains UNKNOWN; prior completed durable report does not prove current native availability. Do not claim continuity or start an overlapping replacement. Flow owner's ONE documented supported protocol/status recovery remains theirs alone.

Once explicitly cleared, appoint ONE nonauthor Rust-capable independent checker for only the exact facade signature/escape/finite-consumer contract. Needs Rust GAT/HRTB/error-conversion reasoning, compile-fail harness and rkyv consumer familiarity; use an implementation-capable worker as a tester, not a new designer. Checker may write disposable review fixtures/report only in a specifically authorized isolated review root; never modify eight implementation roots, reparent the sole writer, transfer locks, publish, or perform remote/ref/runtime effects. Immutable inputs: proposal hash above, pinned redb1bd/tree, exact held Sema diff hash/receipt, Engine9884905. Pin all fixture/toolchain/dependency identities and verify input unchanged before/after. A separate fixture implementing proposed signatures is proof only of that fixture, not implemented-body acceptance.

Required negative cases: escape facade/reference; return raw table/AccessGuard/Range through public capabilities; return borrowed bytes/text; return future capturing scoped facade; capture borrowed decoded data into caller state. Assert intended lifetime/capability diagnostic, not arbitrary compiler failure. A misspelled symbol, unresolved dependency or unsupported toolchain is GAP, not expected failure.

Required positives: get missing/present; owned Vec<u8>/String/u64; owned decoded DatabaseHeader; catalog Vec<(String,TableRegistration)>; counter/policy owned decode; application decode errors; native StorageError/TableError/TransactionError retaining distinct payloads. Cover normal and experimental-api-5 feature shapes, since native inherent get differs. Prove no public constructor/Clone/Deref/AsRef/raw accessor/native iterator on facade. Outer read must remain one scope for finite observation. Future carrying only owned decoded results is permitted; only a future retaining scoped borrow must fail.

Checker returns exact command/output/diagnostics and PASS/GAP per contract, not whole-candidate acceptance. No independent PASS exists yet. Path-replacement, recovery/v9/corrupt, promotion/first-mutation/sync fault obligations remain separately open. Affected bodies and all Protos push/retry remain HOLD.
