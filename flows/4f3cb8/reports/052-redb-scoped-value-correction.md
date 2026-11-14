# Redb inspection: scoped decoded values, no table or guard escape

Correction to independently rejected local candidate1bd09903b9658f0d43e49ca89080facb5ea43e94. Affected redb/Sema bodies remain held until exact API review and Core clearance. Frozen accepted ownership requirements remain unchanged.

## Observed defect

ScopedRead::with_table passes an owned ReadOnlyTable to a callback with arbitrary return T. ReadOnlyTable owns an Arc<TransactionGuard> and has no view lifetime. Therefore returning the table escapes the inspection scope. Merely passing &ReadOnlyTable is insufficient: its inherent get returns AccessGuard<'static,V>, and other raw guard/range APIs expose ownership. HRTB around the outer view cannot remove those capabilities.

## Smallest corrected surface proposed

Keep the owned ReadOnlyTable PRIVATE inside a scoped facade. Only the owning inspection constructs that facade. with_table lends a facade reference for the callback; it never hands out ReadOnlyTable, AccessGuard, Range, transaction, backend, or a mutable reference. The facade has no public constructor, Clone, Deref, AsRef/raw getter, conversion into native handle, or handle-bearing iterator.

Its ONLY value access capabilities are:

1. `with_value(key, callback)` — internally gets a guard; lends the decoded `Option<V::SelfType<'value>>` to a higher-ranked callback; drops the guard before returning the callback's owned result.
2. `for_each(callback)` — internally owns the range and each pair of guards; lends decoded `K::SelfType<'entry>` and `V::SelfType<'entry>` for each callback invocation; drops both guards per iteration and the range before returning. The callback can accumulate owned decoded results in caller-owned state; the API never returns an iterator.

Schematic signatures, to be checked against exact pinned key/value/error bounds before bodies:

```rust
// R/E are chosen outside the bound lifetime, not lifetime-indexed results.
fn with_value<'key, R, E>(
    &self,
    key: impl Borrow<K::SelfType<'key>>,
    f: impl for<'value> FnOnce(Option<V::SelfType<'value>>) -> Result<R, E>,
) -> Result<R, E>
where E: From<StorageError>;

fn for_each<E>(
    &self,
    f: impl for<'entry> FnMut(K::SelfType<'entry>, V::SelfType<'entry>) -> Result<(), E>,
) -> Result<(), E>
where E: From<StorageError>;
```

with_table likewise lends only `&ScopedTable<...>` under a fresh callback lifetime; its error bound retains native TableError. The outer with_read preserves native transaction errors and application errors through the already approved typed conversion pattern. Neither method exposes the native guard even for Value types whose decoded value is owned. Any required extra operation must be justified by the finite consumers rather than exposing the raw table for convenience.

For current built-ins, &[u8] and &str decode to scope-borrowed data and u64 to an owned scalar. A callback may decode bytes into an owned rkyv application record or copy bytes/text; it cannot return their borrowed references or an owned native guard because none is available. The generic redb API cannot police arbitrary user-defined Value implementations with independently owned user data; the property promised is that the inspection lends NO backend/transaction-owned handles. Sema/Engine's finite owned record types complete that boundary toward Flow.

## Actual consumers

SemaInspection::observe currently needs only DATABASE_HEADERS<&str,&[u8]> key database, decoded within callback to owned DatabaseHeader, and META<&str,u64> key schema_version to Option<u64>. Missing table remains a typed absence, malformed bytes/read failures stay typed errors. No ensure/write/reopen is introduced.

Engine's required finite observation needs catalog iteration and counter/version-policy lookups from ONE scoped read; use for_each to build an owned finite catalog observation and with_value for scalar/record values. No Engine inspection implementation exists yet, so no speculative raw facade is necessary. Layout/CommitLog inspection must use the same owned-decoding boundary where actually required; no automatic upgrade/repair during inspection.

## Independent acceptance

- Compile-fail examples returning table reference, raw table/guard/range, decoded borrowed bytes/text or a future holding the scoped facade across return. These must fail because the API lacks the capability/lifetime, not merely because examples voluntarily refrain.
- Positive compile/run cases owned bytes, string, u64, DatabaseHeader and finite catalog records; application decoding errors and all native read/open/transaction errors preserved.
- Same retained File/backend/lock promotion and private owner proof stay intact.
- Keep the independent candidate's other genuine missing tests: pathname replacement while retained handle stays authoritative; recovery/v9/corrupt refusal; injected promotion/first-write/sync failure with truthful pre-mutation versus WriterOpening outcomes. The discarded path fixture has no evidence credit.

Request narrow Core judgment on this decoded-value callback surface, then independent exact signature/consumer review before affected bodies resume. No general database abstraction rewrite, shared raw table escape, extra writer or remote effect is proposed.

## Exact pinned bounds and native error choice

Use `K: redb::Key + 'static, V: redb::Value + 'static` for ScopedTable and TableDefinition; TableDefinition's name lifetime is independent of callback/view lifetimes. Those type bounds satisfy Value::SelfType's `Self:'a` condition without making borrowed decoded values static. Keep R/E outside the callback lifetime binder; do not impose extra Clone/Send/static-result bounds for convenience. Table open errors are redb::TableError; get/iteration/entry errors are redb::StorageError. Outer read remains Result<R,ReadFailure<E>>, with Begin(TransactionError)/Read(E).

Chosen Sema observation error addition: `SemaInspectionError::Storage(#[from] redb::StorageError)`, alongside its existing Redb(InspectionError), Read(TransactionError), Table(#[from]TableError) and DatabaseHeaderDecode{source:rancor::Error}. Preserve the native storage payload directly and distinctly; do not depend on an implicit transitive From conversion or flatten it into text. This is a new unpersisted error variant in the already changed inspection API, not a Memory/schema extension.

Finite Engine catalog/counter/policy values are rkyv byte records: decode to owned TableRegistration/u64/VersioningPolicy inside callbacks. Only Sema's META schema uses native redb u64. Source compatibility report: /home/li/primary/flows/febc51/reports/decoded-facade-signature-compatibility.md SHA9e330abd74df017d2b64cb341ed588fdf4fe773fde635ca176a8cf972a899ff2. Compiler/independent proof remains pending. A disposable fixture proves the proposed signature fixture, not acceptance of future repository bodies.
