# Independent redb inspection/promotion gate

**GAP — capability escape correctness defect plus required evidence gaps.** No candidate acceptance or remote effect follows.

Nonauthor reviewer/native01a1adff-cafa-77a1-aa73-aa98b4dd4794, read-only, started23:29:44UTC. Rootbefore/afterclean exactHEAD1bd09903b9658f0d43e49ca89080facb5ea43e94/treedfa8072d141ed3be2527b3d6453622e64f07be91, against4936637registrybase. ProposalSHA9a18c31e42274d4971eb026f85a7170178259a2e77c719da8030043d6a762155/finalgate6e1cb5a31fe7f4646fdb97ca3df2e0eaef963a1e1c8e11b8c72d00dfbcc23b6f unchanged. Importmanifestitself0567c50356b0ca848b81cc633bdfa4cddf9b4ef295cb10b7f5434e5c4cbf9286 remainsprovenanceinventory, notcandidatechecksum. Parent lands reviewer findings.

## Blocking capability defect

`source/src/db.rs:2161–2178` makes ScopedRead::with_table public and passes OWNED ReadOnlyTable<K,V> into unconstrained FnOnce, returning its resultT. HRTB `InspectedReading::with_read:2197–2202,2306–2319` constrains only ScopedRead<'view>. ReadOnlyTable has no view lifetime and owns Arc<TransactionGuard> (`source/src/table.rs:866–891`). Caller can return detached table:

```rust
inspection.with_read(|view| {
    view.with_table(TABLE, |table| Ok::<_, TableError>(table))
})
```

Owned guards/iterators can similarly escape. This violates accepted only-owned-decoded-values/no-table-iterator-transaction-escape contract. Four existing fixtures do not test compile-failure of escape. Exact capability abstraction needs Primary/Core judgment; no self-redesign authorized.

## Missing required evidence

1. No committed path-replacement fixture. Fourdb.rs2531–2642 tests cover read/promote,empty,recovery,unknownbytes only. Discarded uncommitted test/aborted run gives no proof. Source suggests same-FD promotion: Inspection private Arc<TransactionalMemory>2182–2189, FileBackend owns File, promote2323–2341 moves same memory; acceptedgate stillrequires pathname replacement proof.
2. No promotion fault/first-mutation tests. Inspection `TransactionalMemory::new(...allow_initialize=false...)` takesexclusive lockbefore read (page_manager1078–1149,lock_for_open698–769), thenloadsallocator only. promote2324–2328 firstcallsbegin_writable; firstpersistentaction page_manager1458–1470 writes+flushesrecoveryrequiredheader. Subsequentbegin/syncfailuresmapWriterOpening. Noinjectedfailureproves prepromotionbytesunchanged,exactboundaryclassification orfinalsyncfailure. Known230testPASSdoesnotfill.
3. Classificationfixtures onlyEmptyExisting,RecoveryRequired,invalidmagicUnsupportedFormat. NoUpgradeRequired/v9 orambiguous/corruptformatfixture, thoughdb2227–2242 mapsUpgradeRequired andStorage::Corrupted→UnsupportedFormat.

## Supported bounded portions

PrivateInspectionfields; same retained memory/backendthroughpromotion; defaultExclusiveWriter/continuousbackendheldlock; cleanfixtureindependentlyopensexactpathname→DatabaseAlreadyOpen; noinit/repair/begin_writableduringinspect; promotionfirstcallbegin_writable; existingempty/recovery/unknownrefusalfixturescomparebytes. Suppliedallfeatureslib230PASS accepted asknownreceipt, notrerun orsubstitutedforindependentsourcegate.

Workerreceivedblocker andpreservesfrozenredb1bd plusuncommittedSemaadapterforjudgment. DependentSemabodies/compile/commitheld, no selfpatch. Protos2c76clean/refcustodySTOP;Datom10pathsheld. Reviewerno writes/ref/remoteeffects.
