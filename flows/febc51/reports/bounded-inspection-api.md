# Bounded pinned API source packet
Read-only excerpts, not a new design or source patch. redb HEAD 1bd09903b9658f0d43e49ca89080facb5ea43e94. Held Sema diff is in successor-readonly-receipts.json. No compile claim.

## /git/worktrees/redb-config-d05351-independent/source/src/db.rs
```rust
2150:     Read(E),
2151: }
2152: 
2153: /// A borrowed read view. Its native transaction and any tables opened from it cannot escape the
2154: /// outer inspection callback.
2155: #[cfg(not(redb_no_std))]
2156: pub struct ScopedRead<'view> {
2157:     transaction: &'view ReadTransaction,
2158: }
2159: 
2160: #[cfg(not(redb_no_std))]
2161: impl ScopedRead<'_> {
2162:     /// Runs `read` with one table from this view. The table is never returned to the caller.
2163:     pub fn with_table<K, V, T, E, F>(
2164:         &self,
2165:         definition: TableDefinition<K, V>,
2166:         read: F,
2167:     ) -> core::result::Result<T, E>
2168:     where
2169:         K: Key + 'static,
2170:         V: Value + 'static,
2171:         E: From<TableError>,
2172:         F: FnOnce(ReadOnlyTable<K, V>) -> core::result::Result<T, E>,
2173:     {
2174:         let table = self.transaction.open_table(definition).map_err(E::from)?;
2175:         read(table)
2176:     }
2177: }
2178: 
2179: /// An existing clean database held under the same exclusive ownership from inspection through
2180: /// writer promotion.
2181: #[cfg(not(redb_no_std))]
2182: pub struct Inspection {
2183:     identity: FileIdentity,
2184:     mem: Arc<TransactionalMemory>,
2185:     transaction_tracker: Arc<TransactionTracker>,
2186:     #[cfg(feature = "experimental-multiprocess")]
2187:     writer_lock: Option<Arc<WriterLock>>,
2188: }
2189: 
2190: #[cfg(not(redb_no_std))]
2191: pub trait ExistingFileInspecting {
2192:     fn inspect_file(&self, file: File) -> core::result::Result<Inspection, InspectionError>;
2193: }
2194: 
2195: #[cfg(not(redb_no_std))]
2196: pub trait InspectedReading {
2197:     fn identity(&self) -> &FileIdentity;
2198: 
2199:     fn with_read<T, E, F>(&self, read: F) -> core::result::Result<T, ReadFailure<E>>
2200:     where
2201:         F: for<'view> FnOnce(ScopedRead<'view>) -> core::result::Result<T, E>;
2202: }
2203: 
```

## /git/worktrees/redb-config-d05351-independent/source/src/table.rs
```rust
625: pub trait ReadableTable<K: Key + 'static, V: Value + 'static>: ReadableTableMetadata {
626:     /// Returns the value corresponding to the given key
627:     fn get<'a>(&self, key: impl Borrow<K::SelfType<'a>>) -> Result<Option<AccessGuard<'_, V>>>;
628: 
629:     /// Returns a double-ended iterator over a range of elements in the table
```
```rust
795: 
796:     /// Returns a double-ended iterator over all elements in the table
797:     fn iter(&self) -> Result<Range<'_, K, V>> {
798:         #[cfg(feature = "experimental-api-5")]
799:         let range = self.range(..);
800:         #[cfg(not(feature = "experimental-api-5"))]
801:         let range = self.range::<K::SelfType<'_>>(..);
802:         range
803:     }
804: }
805: 
```
```rust
866: /// A read-only table
867: pub struct ReadOnlyTable<K: Key + 'static, V: Value + 'static> {
868:     name: String,
869:     tree: Btree<K, V>,
870:     transaction_guard: Arc<TransactionGuard>,
871: }
872: 
873: impl<K: Key + 'static, V: Value + 'static> TableHandle for ReadOnlyTable<K, V> {
874:     fn name(&self) -> &str {
875:         &self.name
876:     }
877: }
878: 
879: impl<K: Key + 'static, V: Value + 'static> ReadOnlyTable<K, V> {
880:     pub(crate) fn new(
881:         name: String,
882:         root_page: Option<BtreeHeader>,
883:         hint: PageHint,
884:         guard: Arc<TransactionGuard>,
885:         mem: PageResolver,
886:     ) -> Result<ReadOnlyTable<K, V>> {
887:         Ok(ReadOnlyTable {
888:             name,
889:             tree: Btree::new(root_page, hint, guard.clone(), mem)?,
890:             transaction_guard: guard,
891:         })
892:     }
893: 
894:     /// This method is like [`ReadableTable::get()`], but the [`AccessGuard`] is reference counted
895:     /// and keeps the transaction alive until it is dropped.
896:     #[cfg(not(feature = "experimental-api-5"))]
897:     pub fn get<'a>(
898:         &self,
899:         key: impl Borrow<K::SelfType<'a>>,
900:     ) -> Result<Option<AccessGuard<'static, V>>> {
901:         self.tree.get(key.borrow())
902:     }
903: 
904:     /// This method is like [`ReadableTable::get()`], but the returned [`OwnedAccessGuard`] is
905:     /// reference counted and keeps the transaction alive until it is dropped.
906:     pub fn get_owned<'a>(
907:         &self,
908:         key: impl Borrow<K::SelfType<'a>>,
909:     ) -> Result<Option<OwnedAccessGuard<V>>> {
910:         Ok(self
911:             .tree
912:             .get(key.borrow())?
913:             .map(|x| OwnedAccessGuard::new(x, self.transaction_guard.clone())))
914:     }
915: 
916:     /// This method is like [`ReadableTable::range()`], but the iterator is reference counted and keeps the transaction
917:     /// alive until it is dropped.
918:     #[cfg(not(feature = "experimental-api-5"))]
919:     pub fn range<'a, KR>(&self, range: impl RangeBounds<KR>) -> Result<Range<'static, K, V>>
920:     where
```
```rust
984: impl<K: Key + 'static, V: Value + 'static> ReadableTable<K, V> for ReadOnlyTable<K, V> {
985:     fn get<'a>(&self, key: impl Borrow<K::SelfType<'a>>) -> Result<Option<AccessGuard<'_, V>>> {
986:         self.tree.get(key.borrow())
987:     }
988: 
989:     #[cfg(feature = "experimental-api-5")]
990:     fn range<'a>(&self, range: impl KeyRange<'a, K>) -> Result<Range<'_, K, V>> {
991:         let (lower, upper) = range.key_bounds();
992:         self.range_in_bounds(lower, upper)
993:     }
994: 
995:     #[cfg(not(feature = "experimental-api-5"))]
996:     fn range<'a, KR>(&self, range: impl RangeBounds<KR> + 'a) -> Result<Range<'_, K, V>>
997:     where
998:         KR: Borrow<K::SelfType<'a>> + 'a,
999:     {
1000:         let (lower, upper) = encode_bounds::<K, KR, _>(&range);
1001:         self.range_in_bounds(lower, upper)
1002:     }
1003: 
1004:     fn first(&self) -> Result<Option<(AccessGuard<'_, K>, AccessGuard<'_, V>)>> {
```
```rust
1146: impl<'a, K: Key + 'static, V: Value + 'static> Iterator for Range<'a, K, V> {
1147:     type Item = Result<(AccessGuard<'a, K>, AccessGuard<'a, V>)>;
1148: 
1149:     fn next(&mut self) -> Option<Self::Item> {
1150:         self.inner.next().map(|x| {
1151:             x.map(|entry| {
1152:                 let (page, key_range, value_range) = entry.into_raw();
1153:                 let key = AccessGuard::with_page(page.clone(), key_range);
1154:                 let value = AccessGuard::with_page(page, value_range);
1155:                 (key, value)
1156:             })
1157:         })
1158:     }
```
```rust
1182:     inner: AccessGuard<'static, V>,
1183:     _transaction_guard: Arc<TransactionGuard>,
1184: }
1185: 
1186: impl<V: Value + 'static> OwnedAccessGuard<V> {
1187:     pub(crate) fn new(inner: AccessGuard<'static, V>, guard: Arc<TransactionGuard>) -> Self {
1188:         Self {
1189:             inner,
1190:             _transaction_guard: guard,
1191:         }
1192:     }
1193: 
1194:     /// Access the stored value
1195:     pub fn value(&self) -> V::SelfType<'_> {
1196:         self.inner.value()
1197:     }
1198: }
1199: 
1200: /// A [`Range`] which also keeps the transaction alive
```

## /git/worktrees/redb-config-d05351-independent/source/src/tree_store/btree_base.rs
```rust
200: pub struct AccessGuard<'a, V: Value + 'static> {
201:     page: EitherPage<'a>,
202:     offset: usize,
203:     len: usize,
204:     on_drop: OnDrop,
205:     _value_type: PhantomData<V>,
206: }
207: 
```
```rust
259:     /// Access the stored value
260:     pub fn value(&self) -> V::SelfType<'_> {
261:         V::from_bytes(&self.page.memory()[self.offset..(self.offset + self.len)])
262:     }
263: 
```

## /git/worktrees/redb-config-d05351-independent/source/src/types.rs
```rust
435: impl Value for &[u8] {
436:     type SelfType<'a>
437:         = &'a [u8]
438:     where
439:         Self: 'a;
440:     type AsBytes<'a>
441:         = &'a [u8]
442:     where
```
```rust
703: impl Value for &str {
704:     type SelfType<'a>
705:         = &'a str
706:     where
707:         Self: 'a;
708:     type AsBytes<'a>
709:         = &'a str
710:     where
```

## /git/worktrees/sema-config-d05351-independent/src/lib.rs
```rust
280: /// need an owned shape.
281: pub trait OwnedTableKey: redb::Key + 'static {
282:     type Owned;
283: 
284:     fn owned_key(value: Self::SelfType<'_>) -> Self::Owned;
285: }
```
```rust
317: impl OwnedTableKey for &'static str {
318:     type Owned = String;
319: 
320:     fn owned_key(value: Self::SelfType<'_>) -> Self::Owned {
321:         value.to_string()
322:     }
323: }
324: 
325: impl OwnedTableKey for String {
326:     type Owned = String;
327: 
328:     fn owned_key(value: Self::SelfType<'_>) -> Self::Owned {
329:         value
330:     }
331: }
332: 
333: impl OwnedTableKey for &'static [u8] {
334:     type Owned = Vec<u8>;
335: 
336:     fn owned_key(value: Self::SelfType<'_>) -> Self::Owned {
337:         value.to_vec()
338:     }
```
```rust
360:     /// `Ok(None)` if the table doesn't exist yet (it gets
361:     /// created lazily on first write).
362:     pub fn get<'txn>(
363:         &self,
364:         txn: &'txn ReadTransaction,
365:         key: impl std::borrow::Borrow<K::SelfType<'txn>>,
366:     ) -> Result<Option<V>> {
367:         let table = match txn.open_table(self.definition()) {
368:             Ok(table) => table,
369:             Err(redb::TableError::TableDoesNotExist(_)) => return Ok(None),
370:             Err(other) => return Err(other.into()),
371:         };
372:         let Some(guard) = table.get(key)? else {
373:             return Ok(None);
374:         };
375:         Ok(Some(self.decode_value(guard.value())?))
376:     }
377: 
378:     /// Insert `value` at `key`, overwriting any existing value.
379:     pub fn insert<'txn>(
380:         &self,
```
```rust
411:     /// both keys and values, so the redb transaction can close
412:     /// before callers use the rows.
413:     pub fn iter(&self, txn: &ReadTransaction) -> Result<Vec<(K::Owned, V)>>
414:     where
415:         K: OwnedTableKey,
416:     {
417:         let table = match txn.open_table(self.definition()) {
418:             Ok(table) => table,
419:             Err(redb::TableError::TableDoesNotExist(_)) => return Ok(Vec::new()),
420:             Err(other) => return Err(other.into()),
421:         };
422:         let mut rows = Vec::new();
423:         for entry in table.iter()? {
424:             let (key_guard, bytes_guard) = entry?;
425:             rows.push((
426:                 K::owned_key(key_guard.value()),
427:                 self.decode_value(bytes_guard.value())?,
428:             ));
429:         }
430:         Ok(rows)
431:     }
432: 
433:     /// Snapshot typed rows whose keys fall inside `range`.
```
```rust
470: const META: TableDefinition<&str, u64> = TableDefinition::new("__sema_meta");
471: const DATABASE_HEADERS: TableDefinition<&str, &[u8]> = TableDefinition::new("__sema_headers");
472: const DATABASE_HEADER_KEY: &str = "database";
473: const SCHEMA_VERSION_KEY: &str = "schema_version";
474: 
475: pub struct Sema {
476:     database: Database,
477:     path: PathBuf,
478: }
479: 
480: /// The Sema-owned view of one redb inspection. The redb owner remains private and can only be
481: /// consumed by promotion.
482: pub struct SemaInspection {
483:     inspection: redb::Inspection,
484:     path: PathBuf,
485: }
486: 
487: /// Sema metadata observed without ensuring tables or writing a schema declaration.
488: #[derive(Debug, Clone, PartialEq, Eq)]
489: pub struct SemaObservation {
490:     pub database_header: Option<DatabaseHeader>,
491:     pub schema: Option<u64>,
492: }
493: 
494: #[derive(Debug, Error)]
495: pub enum SemaInspectionError {
496:     #[error("redb inspection: {0:?}")]
497:     Redb(redb::InspectionError),
498:     #[error("redb inspection read: {0}")]
499:     Read(redb::TransactionError),
500:     #[error("redb inspection table: {0}")]
501:     Table(#[from] redb::TableError),
502:     #[error("database header decode failed during inspection: {source}")]
503:     DatabaseHeaderDecode { source: rancor::Error },
504: }
505: 
506: #[derive(Debug, Error)]
507: pub enum SemaPromotionError {
508:     #[error("redb promotion: {0:?}")]
509:     Redb(redb::PromotionError),
510: }
511: 
512: pub trait ExistingSemaInspecting {
513:     fn inspect_sema_file(
514:         &self,
515:         file: File,
516:         path: PathBuf,
517:     ) -> std::result::Result<SemaInspection, SemaInspectionError>;
518: }
519: 
520: pub trait InspectedSemaObserving {
521:     fn identity(&self) -> &FileIdentity;
522:     fn observe(&self) -> std::result::Result<SemaObservation, SemaInspectionError>;
523: }
524: 
525: pub trait InspectedSemaPromoting {
526:     fn promote(self) -> std::result::Result<Sema, SemaPromotionError>;
527: }
528: 
529: impl ExistingSemaInspecting for redb::Builder {
530:     fn inspect_sema_file(
531:         &self,
532:         file: File,
533:         path: PathBuf,
534:     ) -> std::result::Result<SemaInspection, SemaInspectionError> {
535:         let inspection = self.inspect_file(file).map_err(SemaInspectionError::Redb)?;
536:         Ok(SemaInspection { inspection, path })
537:     }
538: }
539: 
540: impl InspectedSemaObserving for SemaInspection {
541:     fn identity(&self) -> &FileIdentity {
542:         self.inspection.identity()
543:     }
544: 
545:     fn observe(&self) -> std::result::Result<SemaObservation, SemaInspectionError> {
546:         self.inspection
547:             .with_read(|view| {
548:                 let database_header = match view.with_table(DATABASE_HEADERS, |table| {
549:                     let Some(stored) = table.get(DATABASE_HEADER_KEY)? else {
550:                         return Ok(None);
551:                     };
552:                     rkyv::from_bytes::<DatabaseHeader, rancor::Error>(stored.value())
553:                         .map(Some)
554:                         .map_err(|source| SemaInspectionError::DatabaseHeaderDecode { source })
555:                 }) {
556:                     Err(SemaInspectionError::Table(redb::TableError::TableDoesNotExist(_))) => None,
557:                     result => result?,
558:                 };
559:                 let schema = match view.with_table(META, |table| {
560:                     Ok(table.get(SCHEMA_VERSION_KEY)?.map(|stored| stored.value()))
561:                 }) {
562:                     Err(SemaInspectionError::Table(redb::TableError::TableDoesNotExist(_))) => None,
563:                     result => result?,
564:                 };
565:                 Ok(SemaObservation {
566:                     database_header,
567:                     schema,
568:                 })
569:             })
570:             .map_err(|failure| match failure {
571:                 ReadFailure::Begin(error) => SemaInspectionError::Read(error),
572:                 ReadFailure::Read(error) => error,
573:             })
574:     }
575: }
576: 
577: impl InspectedSemaPromoting for SemaInspection {
578:     fn promote(self) -> std::result::Result<Sema, SemaPromotionError> {
579:         let database = self
580:             .inspection
581:             .promote()
582:             .map_err(SemaPromotionError::Redb)?;
583:         Ok(Sema {
584:             database,
585:             path: self.path,
586:         })
587:     }
588: }
589: 
590: impl Sema {
591:     /// Open or create a sema database at `path` with a
592:     /// declared schema. The kernel writes the schema version
```

## /git/worktrees/sema-engine-config-d05351-independent/src/engine.rs
```rust
45: const CATALOG: sema::Table<&'static str, TableRegistration> =
46:     sema::Table::new("__sema_engine_catalog");
47: pub(crate) const COUNTERS: sema::Table<&'static str, u64> =
48:     sema::Table::new("__sema_engine_counters");
49: pub(crate) const LATEST_COMMIT_SEQUENCE_KEY: &str = "latest_commit_sequence";
50: pub(crate) const LATEST_SNAPSHOT_KEY: &str = "latest_snapshot";
51: const NEXT_SUBSCRIPTION_KEY: &str = "next_subscription";
52: const LATEST_CHECKPOINT_KEY: &str = "latest_checkpoint";
```
```rust
140:     }
141: 
142:     fn open_unrecovered(request: EngineOpen) -> Result<Self> {
143:         let storage = sema::Sema::open_with_schema(request.path(), request.schema())?;
144:         // Every validation runs before the first engine write: an open
145:         // that rejects a store must not mutate the store it rejects.
146:         let layout_plan = Self::validated_storage_layout(&storage)?;
147:         let registrations = match storage.read(|transaction| CATALOG.iter(transaction)) {
148:             Ok(rows) => rows
149:                 .into_iter()
150:                 .map(|(_key, registration)| registration)
151:                 .collect(),
152:             // A catalog row that no longer decodes is a pre-family-identity
153:             // registration; surface the layout break, not a byte error.
154:             Err(sema::Error::RkyvDecode { table, .. }) if table == CATALOG.name() => {
155:                 return Err(Error::StorageLayoutMismatch {
156:                     stored: LAYOUT_BEFORE_SLOT,
157:                     expected: STORAGE_LAYOUT,
158:                 });
159:             }
160:             Err(other) => return Err(other.into()),
161:         };
162:         // Every validation — layout, versioning policy, declared families —
163:         // reads only. Their writes then land in one transaction: a virgin
164:         // store gets its layout slot stamped, an older versioned store its
165:         // refolded derived slots and re-stamp, a first versioned open its
166:         // policy row, and the declared families new to the catalog their
167:         // rows. Open is single-threaded, so this is the only writer.
168:         let policy = Self::validated_versioning_policy(&storage, request.versioning_policy())?;
169:         let mut catalog = Catalog::new(registrations);
170:         let mut declared = Vec::new();
171:         for declaration in request.families() {
172:             if let Some(registration) = catalog.admit(declaration)? {
173:                 declared.push((declaration.keying(), declaration.table(), registration));
174:             }
175:         }
176:         Self::persist_open(
```
```rust
3228:     fn validated_storage_layout(storage: &sema::Sema) -> Result<LayoutOpenPlan> {
3229:         let stored = storage.read(|transaction| COUNTERS.get(transaction, STORAGE_LAYOUT_KEY))?;
3230:         match stored {
3231:             // Current layout: idempotent open, nothing to do.
3232:             Some(layout) if layout == STORAGE_LAYOUT => Ok(LayoutOpenPlan::Current),
3233:             // Forward skew: a layout newer than this build wrote derived
3234:             // state this engine cannot interpret. Refusing to downgrade
3235:             // an unknown-newer store is the only safe move.
3236:             Some(layout) if layout > STORAGE_LAYOUT => Err(Error::StorageLayoutMismatch {
3237:                 stored: layout,
3238:                 expected: STORAGE_LAYOUT,
3239:             }),
3240:             // Older layout. Slice A's bump to layout 5 was purely
3241:             // additive — it added the CHAIN_HEAD and log-count derived
3242:             // slots without touching the data tables or the versioned
3243:             // log format. So if the store opted into versioning and its
3244:             // versioned log is non-empty, the missing derived slots are
3245:             // recomputable from that log alone: refold them and
3246:             // re-stamp. With no versioned log present this is a
3247:             // pre-versioning store whose derived state is not log-
3248:             // recoverable, so it hard-fails (the previous-engine
3249:             // StoreMigration owns pre-v9 stores); state loss is
3250:             // unacceptable (Spirit 29pb).
3251:             Some(layout) => {
3252:                 if CommitLog::versioned_log_present(storage)? {
3253:                     Ok(LayoutOpenPlan::RebuildDerivedSlots(
3254:                         CommitLog::refolded_derived_slots(storage)?,
3255:                     ))
3256:                 } else {
3257:                     Err(Error::StorageLayoutMismatch {
3258:                         stored: layout,
3259:                         expected: STORAGE_LAYOUT,
3260:                     })
3261:                 }
3262:             }
3263:             None => {
3264:                 // No layout slot: either a virgin store or a layout-1
3265:                 // store from before the slot existed. Any engine counter
3266:                 // proves prior engine writes, hence layout 1.
3267:                 let has_engine_history = storage.read(|transaction| {
3268:                     Ok(COUNTERS
3269:                         .get(transaction, LATEST_COMMIT_SEQUENCE_KEY)?
3270:                         .or(COUNTERS.get(transaction, LATEST_SNAPSHOT_KEY)?)
3271:                         .or(COUNTERS.get(transaction, NEXT_SUBSCRIPTION_KEY)?)
3272:                         .is_some())
3273:                 })?;
3274:                 if has_engine_history {
3275:                     return Err(Error::StorageLayoutMismatch {
3276:                         stored: LAYOUT_BEFORE_SLOT,
3277:                         expected: STORAGE_LAYOUT,
3278:                     });
3279:                 }
3280:                 Ok(LayoutOpenPlan::StampFresh)
3281:             }
3282:         }
3283:     }
3284: 
3285:     /// Carry out the open-time layout plan inside the open's one write
```
```rust
3310:     fn validated_versioning_policy(
3311:         storage: &sema::Sema,
3312:         requested: Option<&VersioningPolicy>,
3313:     ) -> Result<Option<VersioningPolicy>> {
3314:         let recorded = storage
3315:             .read(|transaction| VERSIONING_POLICY.get(transaction, VERSIONING_POLICY_KEY))?;
3316:         match (recorded, requested) {
3317:             (Some(_), None) => Err(Error::VersioningPolicyRequired),
3318:             (Some(recorded), Some(requested)) if recorded == *requested => Ok(None),
3319:             (Some(_), Some(_)) => Err(Error::VersioningPolicyMismatch),
3320:             (None, None) => Ok(None),
3321:             (None, Some(requested)) => Ok(Some(requested.clone())),
3322:         }
3323:     }
3324: 
3325:     /// Land the whole durable effect of an open in one write transaction:
3326:     /// the layout plan, the first versioning-policy row, and the declared
3327:     /// families new to the catalog (with an identified family's counter).
```

## /git/worktrees/sema-engine-config-d05351-independent/src/commit_log.rs
```rust
245:     pub(crate) fn refolded_derived_slots(storage: &sema::Sema) -> Result<DerivedSlots> {
246:         let entries: Vec<VersionedCommitLogEntry> = storage
247:             .read(|transaction| VERSIONED_COMMIT_LOG.iter(transaction))?
248:             .into_iter()
249:             .map(|(_sequence, entry)| entry)
250:             .collect();
251:         // Recompute and verify the whole chain from genesis. A tampered
252:         // or forked log surfaces as a typed VersionedChainBroken here,
253:         // aborting the open before any derived slot is written.
254:         crate::fold::CanonicalView::fold(&[], &entries, None)?;
255:         let commit_count = storage
256:             .read(|transaction| COMMIT_LOG.iter(transaction))?
257:             .len() as u64;
258:         Ok(DerivedSlots {
259:             head: entries.last().map(VersionedCommitLogEntry::entry_digest),
260:             versioned_count: entries.len() as u64,
261:             commit_count,
262:         })
263:     }
264: 
265:     /// Whether the versioned log holds any entry — the open-time test
266:     /// for whether an older-layout store opted into versioning and so
267:     /// can refold its derived slots from the log alone.
268:     pub(crate) fn versioned_log_present(storage: &sema::Sema) -> Result<bool> {
269:         Ok(storage.read(|transaction| Ok(!VERSIONED_COMMIT_LOG.iter(transaction)?.is_empty()))?)
270:     }
```

## Current needed inspection reads
Sema held observe: only __sema_headers/database get → Option<owned DatabaseHeader> and __sema_meta/schema_version get → Option<u64>; missing table means None. PathBuf is only stored/copied into promoted Sema, never used to reopen or decide identity in this diff.
Engine has no new inspection implementation. Current open_unrecovered uses CATALOG.iter → owned Vec<(String, TableRegistration)>, COUNTERS.get for layout and three history counters → Option<u64>, VERSIONING_POLICY.get → Option<VersioningPolicy>. Older-layout branch requires VERSIONED_COMMIT_LOG.iter for presence and refolding, and COMMIT_LOG.iter for refolding; outputs are owned decoded rows. This records current calls, not authority to expand the finite accepted plan.
Key/value access on Range items is AccessGuard::value on the first/second guard. Borrowing ReadOnlyTable alone still exposes inherent static get/get_owned; no raw table facade has been approved.
Independent gaps retained: escaping capability; path replacement fixture; promotion first-mutation/fault/sync evidence; v9/ambiguous/corrupt fixtures.
