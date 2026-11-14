## Controlling scope

I understand the controlling design as follows:

- `Start` receives bare `Place` only: store, ordinary socket, and meta socket identities.
- A new Place receives new Memory. There is no 051 Memory import, migration, seed, startup overlay, automatic replay, or behavioral Rust default.
- Replay is external and explicit: one Configure datom per file, with each declaration committed atomically.
- The outer translator receives separate explicit Nix-produced configuration for parser limits, frame limits, transport, and native timeouts. Those values are not Start fields or Memory defaults.
- Runtime policy is sparse Memory: one generated, typed Setting-keyed leaf per row. Keys and values derive from the Configure vocabulary so unrelated keys and values cannot be paired.
- Address-based settings retain the complete Address, including topic.
- Model is `Configure.Model.{ Address Native.String }`; there is no layer/aspect fallback.
- Continuity is a separate per-Address setting:
  - `Continues`
  - `Ends.IdleMinutes`, with positive checked minutes.
- Absent Continuity performs no idle close and does not block launch.
- Missing operation-specific settings produce typed named readiness before dependent effects, preserving existing seats and queues.
- Resume retains the existing FlowId, native session, and transcript. There is no Fable gate or security substitute.

Controlling design SHA:

`89f56154d752c7db2fd8c410026e72ab453e3a048b523ab908a03feb9d6dd993`

## Exact admitted slice

The admitted implementation slice is only:

1. Correct redb candidate `1bd09903…` to the approved scoped decoded-value facade.
2. Adapt the directly held Sema inspection diff to that facade.
3. Add and run the authorized repository unit, compile-fail, path, format, promotion, first-mutation, and sync-failure tests.
4. Make local commits in the existing redb and Sema roots after parent verification.

The admitted documents match:

- Next-worker brief: `24ccd74103ffeb747085e739056a9a3d688d6d88309dbd1c808fa796b39d795f`
- Admission packet: `5eb059c9c9f902414fa21d77e4b243385bf6193f76ce37a47d451a1ac58cde7f`
- Facade contract: `224a0f66b60571b19bc0da4f12582f2894645c3a79bfbce608d8e375941c8e65`
- Bounded pinned API packet: `3f629f373f969f731d54918fe9bac5e99ffcf1f0334f3e795d24e38d4cb34f2d`

The exact facade is:

- Native `ReadOnlyTable<K,V>` remains private.
- `with_table` lends only `&ScopedTable<K,V>` under a fresh callback lifetime.
- No public constructor, raw getter, `Clone`, `Deref`, native guard, range, iterator, transaction, or backend capability exists.
- `with_value` lends only decoded `Option<V::SelfType<'value>>` to an HRTB callback.
- `for_each` lends decoded key/value pairs one entry at a time to an HRTB callback.
- Results are owned outside the bound lifetime.
- Bounds remain `K: Key + 'static`, `V: Value + 'static`; `R` and `E` remain outside the lifetime binder.
- Table opening preserves `TableError`; value and iteration operations preserve `StorageError`; transaction opening remains `ReadFailure::Begin(TransactionError)`.
- Sema adds distinct `SemaInspectionError::Storage(redb::StorageError)` without flattening.

## Read-only fixture evidence inspected

- Fixture report: `b4aa410b7b423cf5ae649fa2fdb3a14e205c7fccbf6ba3da8dafff5013c01f86`
- Actual-import extension: `c34e9448bc824c48e5042a419d7366526449dbcd15c3bd2bd981d3599943f298`
- Fixture `src/lib.rs`: `d8b1164555b1baad53bea66b4d07f3c8708b6e0086655a1c916384f816069df8`
- Positive tests: `a3accc036f401db321c5a0ce2c1b478e11bc6fbf07a9a8a947f1476aef9131e7`
- Actual Sema/Engine import test: `9c310dce55e22c3124c1fd53fa76c289edb2ed5812d7a6d0a39ee47619aa09e4`
- Current fixture Cargo manifest: `3c46a67133f7c2adf998ced6e37ddd130fde8478f5a6e5fd4727e8cf893056c1`
- Current fixture lock: `3770a27efe381f1e25732bf7d12f3c52d0f60848761ebd9dccf55369364596e3`
- Negative-file hash ledger: `2afab45ee6ef190eb69e0a422f6ea9da5a00cf565b6609c7f50a9a442b5879a5`

These fixtures establish the signature and capability shape under normal and `experimental-api-5`, including actual predecessor Sema/Engine owned-record decoding. They do not accept repository bodies or satisfy the remaining path/fault tests.

## Role and capability

I remain the same implementation-capable worker:

- Native: `01a1adee-75af-7043-a7cc-1ffa6eedf393`
- Original parent: `01a1adda-fc98-7f13-bc6a-1692aed8d121`
- Composition custodian: `febc51`
- Owning Flow: `2aed8d`

After the original parent verifies this response, I may edit and locally test/commit only the redb scoped facade and direct held Sema adapter in their existing roots. I may run local unit, compile-fail, and fault tests using isolated temporary outputs.

I have no authority for another worker or child, daemon/native/capsule/deploy activity, networking, publication, push, tags, registry-manifest changes, path overrides, Protos retry, or the wider 052 implementation.

## Current custody and held work

Fresh observation at `2026-11-06T01:07:49Z` agrees with custody record SHA:

`7f26d20deda454dadfa488e1ee13c12042bb6b57521bd8991619af732973032f`

Locks remain owned by Flow `2aed8d` with the exact sole-worker reason:

- `25623`: Flow root
- `25624`: Sema, Sema Engine, signal-flow, meta-signal-flow
- `25625`: redb
- `25626`: Datom and Protos

Root state:

- Flow: clean `916b54574ae0024b893a9f4252f2e97704db48c1`
- Sema: base `51d7927c872f0df12791bad8d39a4db6433b01a1`; retained `src/lib.rs` diff, `+115/-1`, diff SHA `8c52893dd0eec40cd6bae1d2440e73df086542e8f6436c7bb47e76da7ea45795`
- Sema Engine: clean `9884905ff9c660ad97a35c524e42532d5c7bac90`
- signal-flow: clean `ce083f2ba9cc0bd928735ba4cc09e59965982e30`
- meta-signal-flow: clean `281f5aa1b88cd43609c127cdf6f3c12645faf58b`
- redb: clean rejected correction baseline `1bd09903b9658f0d43e49ca89080facb5ea43e94`, tree `dfa8072d141ed3be2527b3d6453622e64f07be91`
- Datom: base `4dff16b4f7412febc3b71aac8b49680cd20988cb`; exactly ten held modified files, diff SHA `f92ecbf7695d87e56430c2f853d90b19aff2350699b76145b1b6e11a4c04130d`
- Protos: clean `2c76ccf1ed7ba646a62962131bd60f8886daac54`, tree `b6551eb8afb2d4089c84e93c0bb411e3534d1b0a`

The redb registry import manifest remains unchanged at:

`0567c50356b0ca848b81cc633bdfa4cddf9b4ef295cb10b7f5434e5c4cbf9286`

Disposition:

- Correct redb `1bd09903…`; do not treat it as accepted.
- Retain and adapt the Sema WIP; do not discard unrelated evidence or wrap the escaping facade again.
- Preserve Protos `2c76ccf1…`.
- Preserve the Datom ten-file diff without retrying its dependency work.
- Keep the other roots unchanged.
- Do not revive work solely supporting the removed 051 migration/startup batch.

## Prior blockers

1. **Exact facade contract — resolved.**  
   Contract `224a0f66…`, bounded API packet `3f629f…`, and read-only fixture evidence settle the capability surface.

2. **Precise slice admission — resolved, conditional on parent verification of this response.**  
   Only redb facade correction, direct held Sema adaptation, repository tests, and local commits are admitted.

3. **Held-diff disposition — resolved.**  
   Redb is the rejected correction baseline; Sema WIP is retained and adapted; Protos and Datom remain preserved; other roots remain clean.

4. **Fixture and fault-test capability — resolved for this bounded slice.**  
   Compile-fail escape tests, positive finite consumers/error propagation, path replacement, recovery/v9/corrupt refusal, and injected promotion/write/sync failures are admitted locally.

5. **Immutable dependency materialization — still open.**  
   Fixture evidence does not materialize repository dependencies.

## Remaining immutable dependency gaps

- The local redb candidate has no authorized published immutable source or usable approved remote pin. Direct dependent Sema builds cannot claim PASS until that exists.
- The earlier single authorized Protos remote attempt remains unresolved. Its status must not be inferred from my no-effect report, and I have no retry authority.
- Datom remains pinned/blocked behind exact Protos materialization and cannot claim a coherent dependent build.
- No coherent whole 052 dependency graph or artifact exists yet.
- No remote, ref, publication, or registry effect is authorized in this slice.

One documentation discrepancy is recorded: the admission packet names implementation-ledger SHA `7d00ea0c…`, while the current ledger file hashes to `e53bc308d01e66cef66d9e25e42dddfccc9e052704cb886352d84d7d84517cae` after its appended Core-approved section. I do not use that mutable ledger discrepancy to expand authority; the directly admitted brief, admission packet, contract, fixtures, current custody, and this Core message control.

No source edit, build, test, commit, child, runtime, ref, or remote effect occurred during this response.
