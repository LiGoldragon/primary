# Final source-ledger index and exact gaps

This index supersedes earlier broad/contradictory statements in `source-ledger.md`; the specialized ledgers below are the pinned source evidence. Scope is read-only Flow916 source mapping plus pinned prepared dependency roots. No implementation, writer grant, or body approval.

## Pinned evidentiary artifacts

| Artifact | SHA-256 |
|---|---|
| `engine-consumer-ledger.md` | `b80fa70ca7b7f246fbb400a538d29e3292bcf7d8e1ea0281808a1d8edaf442bf` |
| `engine-api-query-results.txt` | `da883448234a2cff507bc693f02eb4e6d5e1bd72285761de073cecd0e19540df` |
| `engine-own-query-results.txt` | `061fbfc0ed95c368484df8c483bf9462a6f143e4614866e90ae88b08cb471303` |
| `codec-full-query-results.txt` | `9388d2eaeb664745ada0e9969afca9e313ed66030782eb7aa8444a24a74336f1` |
| `runtime-leaf-consumer-ledger.md` | `d41ff05d15eb0308e56a8fdfac6eb1cfe6584c2fb0fcd29f26953b20b3321cb1` |
| `adapters-writers-resume-ledger.md` | `b1a4fc4f3bba580981b7a74ec0fbf987978d2ad9ec939d39ac45fe20dcaa33e3` |
| `schema-consumer-delta.md` | `5c4f0c7676ae6fdde8ad53a35d7308644cee4d4572a0820fc35d1e8133a108c` |
| `codec-derive-impact.md` | `39207e3e76ecd9c7dcd72212b74570156e8d4327bd66cb3d5aa71c04bad2adcb` |
| `codec-redb-local-refs.txt` | `a5c3b9c07566125440ae20ea5c6ab398d22a4b7362d79c60dfde9fb93cf47293` |

| `adapter-envelope-consumers.md` | `adb8ace3db25ee1eff3418e3a30d5e83e407623891e05799c6104ec6ab448886` |
| `adapter-envelope-query-results.txt` | `811e43860fa3434b39d407c902b3c12dfcb3d29e14a29c63132f96421f058283` |

## Coverage bounds

- Engine: exact 217 Flow/Engine query matches plus separate 73-line Engine-own query; inline test modules classified, fixture callers separated from production. The 217 artifact is the exact source query receipt.
- Codec: 92 direct `datom_form`/`protosize` query matches across pinned Datom/Protos sources and Flow workspace; output serialization versus text-reading calls classified to the stated limits. Some raw query paths are Cargo pinned checkout paths, not independently prepared-root receipts; immutable-base equivalence is not independently established by this report. Budget literal coverage is separately listed in the adapters ledger, not proved exhaustive by the 92-call artifact.
- Runtime: every authored leaf name from the controlling runtime proposal has a separate row, including all five parser caps, all seven pane leaves, all six transport leaves, all three retry leaves, and Effort’s twelve coordinates.
- Writers/Resume: all observed configuration method definitions/callers and native Resume symbols are mapped; public Resume symbols are intentionally absent in Flow916 and planned destinations are quoted from the controlling proposal.
- Configuration schema: v5→candidate v6 wrapper, descriptors, catalog, readback, writes, retained Nexus/AddressHold are pinned separately.

## Allocation state

Core’s final allocation request closes the prior allocation gap: Flow workspace `0.52`; signal `44`; meta `60`; sema `0.2`; sema-engine `0.19`; datom/protos `0.33`; datom-codec-derive retained `0.32`; four Memory coordinates including configuration v6; owned redb `https://github.com/LiGoldragon/redb.git` `refs/heads/flow-052-opening`, registry-derived package `4.3.0`. These are recorded allocations, not implementation authorization.

## Exact unresolved gaps

1. RESOLVED by new eighth authored proposal `052-adapter-envelopes.md`: exact shared/ordinary/meta/composer/hook layouts and Nix wrapper producer. `adapter-envelope-consumers.md` and its 30-hit query map current literals, raw composer callers and producer/projection obligations. Earlier missing-layout claims are historical, superseded.
2. Generated Resume/Observe symbols do not exist in Flow916 by design; planned names/routes are recorded. This is an implementation obligation, not missing authored design or nonexistent compiled-code evidence.
3. Remaining source precision: full per-receiver/per-inline-test semantic classification and independently prepared-root receipts for every dependency ReaderBudget/Budget/direct-forming consumer are not claimed beyond the explicit artifacts/locations. The fresh checker must judge whether these bounded gaps prevent consumer closure; this index does not assert whole-world completeness.
4. Runtime compound-expression leaves are anchored without invented symbols (RetryMultiplier is existing doubling at send_tool.rs610). Some other rows retain broad source ranges with symbol corrections appended; their per-leaf source/oracle precision remains for fresh independent judgment, not self-certification.
5. No future compile, archived-byte, fault, capsule, or fresh independent-review result is claimed here; those are release/verification stages after body work, not prebody source evidence.
