# Retained Codex receipt cohorts: evidence and bounded correction proposal

## Evidence

Exact serving Flow source: `52e5687d13446e3cd22583ff31d717f6250e0534`. No implementation or runtime mutation has been made. New clean detached worktree `/git/worktrees/flow-codex-cohort-5441e0` is reserved by lock335 to5441e0; heartbeat/SendSeveral remain separate.

Supported ReadQueueDeliveries shows seven Uncertain attempts on ab4e4b's current thread `01a1e0f7-c34a-77f1-bf22-c73ab4e4b921`. A bounded read-only native proxy connection used only initialize, thread/read and thread/turns/list, the exact methods/schema in52e codex.rs1344–1480. It retained metadata and hashes, not raw native turn content. All12 native turns were returned without pagination remainder:

- Completed turn `01a1e0fc-238c-7513-b0fb-b659843af930` contains wtdi/tq5c/od5g/zl75, alongside e1y9/r2tc/usel and other requests. User text SHA256 `1c29fac2c7092166ca1023ea1c39a08c804522af5e50e7183aaa94a69e49df61`.
- Completed turn `01a1e150-aa66-7930-a0f4-f72b7a4a1840` contains qvhm/35qa/yin7, alongside j96f/9wgm/6l4f. User text SHA256 `749fc2cc16d8ececbc44ded000acb4c39781cf17652740bd2a49791027527171`.
- Supported DebugDelivery independently reports e1y9/r2tc/usel Delivered with native receipts for the FIRST exact turn, and j96f/9wgm/6l4f Delivered with receipts for the SECOND exact turn. Thus these are partly receipted native batches, not seven never-submitted messages.

Source proof: waking.rs3041+ typed_group starts from store.unsettled_deliveries and admits only Prepared/Uncertain/ReceiptRecorded; store/queue_delivery.rs1379+ excludes Settled/Read. Therefore already-settled members of the actual payload disappear from reconstruction. cohort_runs renders the shrunken group or singleton; codex.rs328+ accepts only one userMessage text item EXACTLY equal to the rendered candidate. Neither is the original batch. recover_typed then reconstructs PendingLetter after failed lookup; codex_turns.rs standing LetterAwaited blocks rest/refresh. reconcile_typed checks only the latest cohort, so older letters can remain even after another receipt succeeds.

Limit: native history is not a direct dump of Flow's in-memory letter ledger or stored history anchors/counters. At the read instant the native thread was active (Psyche had resumed its work manually); no idle claim is made. The observed lost cohort members and resulting receipt mismatch are proven; the exact seven live in-memory letter entries remain an inference from the source recovery path. No clearing, forced refresh, cancellation, restart, new flow or ledger edit was used.

Evidence: `/tmp/flow-5441e0-codex-rest/` (projection, metadata-only history, read-only script, eight sibling DebugDelivery receipts, exact source extract).

## Proposed invariant and scope — awaiting Core review

A native submission's receipt is checked against its ORIGINAL complete ordered payload, independently of how many members later become Settled or Read. Only still-unreceipted eligible members change state; already terminal history and existing receipts remain byte-for-byte intact. A receipt for another thread, anchor or payload never settles a member. Native turn completion alone never discards an uncertain letter.

Bounded source-only proposal: expose retained attempts for an address separately from unsettled work; reconstruct the existing cohort using the same address/flow/thread/history-anchor and consecutive native-request identities, INCLUDING its Settled/Read members. Keep the full comparison cohort separate from the pending settlement targets. Reconcile every disjoint unresolved cohort at a turn-end event, rather than only the latest, without resubmission. Receipt matching remains exact. Preserve unrelated admission/closure/reminder/continuity logic.

Expected files: `crates/flow-nexus/src/store/queue_delivery.rs` (read capability), `src/waking.rs` (cohort reconstruction/settlement selection/event recovery), `tests/unit/queue_drain.rs` and `tests/unit/codex_turns.rs` (regressions). If fixture plumbing requires another file, name it before edits. No Cargo/wire/configuration/schema/version changes proposed.

Existing fully parked cohorts retain their attempt identities and evidence across Settled/Read, so partial-settlement reconstruction needs no history rewrite or wire expansion. HOWEVER source also submits the full payload BEFORE park_cohort durably creates every sibling. A crash inside that interval can leave an unrepresented suffix. This proposal does not claim that the original entire payload is universally reconstructible across that distinct crash window. A universal pre-I/O durable cohort identity/payload would require a storage/transaction design boundary; raise it before expanding this release. Also refuse ambiguous historical cohort reconstruction rather than inventing missing membership.

## Acceptance regressions

1. A multi-request payload receives only some member receipts/answers; surviving uncertain members still match the ORIGINAL exact native text, settle once, and release pending letters. Original terminal members/receipts remain unchanged.
2. Two separate partially settled cohorts (the production shape), turn end after restart: both reconcile; no older letter remains solely because only latest was checked. Queued on-demand refresh proceeds after actual rest and retains open requests.
3. Crash/reopen after native submission and complete parking, before any receipt; crash after the first member receipt; repeat recovery after complete settlement: same original cohort, no retransmission, duplicate settlement or history change.
4. Wrong thread, anchor missing, changed/reordered/partial text, ambiguous receipt, unresolved original membership and interrupted native turn: retain uncertainty; never clear by turn completion alone.
5. Settled/Read siblings are comparison evidence, not newly open work. Different anchors, flows, threads or nonconsecutive IDs never merge. Existing Claude cohort/startup and native receipt tests remain green.

Final exact52e-descendant must receive independent Core review and a new whole immutable Prometheus gate. No main/publication/runtime repair is authorized by this proposal.

## Implementation submitted for independent review

Corei9i0 approved the bounded four-file implementation. Exact unpublished candidate `124014803eb621e62892034fcde10c176ecfe177` has exact52e parent, in lock335's worktree. Only the four named files changed. Retained comparison membership includes Settled/Read; consecutive IDs nominate candidates but never authorize settlement without the original exact native payload match. Store writes skip completed comparison members, preserving their existing receipt/history. Event reconciliation visits all pending cohorts. The missing-suffix crash case remains uncertain.

Four new fixtures cover partial settlement/recovery/idempotence, two-cohort event reconciliation, the explicitly unsupported missing-suffix crash shape, and Codex ledger release by both exact cohort receipts. Formatting and diff checks passed. No build or test execution pass is claimed yet. Corezhpw received the immutable candidate and separate production/fixture diffs before the whole gate. Dedicated Read-phase byte preservation and a fully integrated mocked Codex refresh remain coverage gaps to resolve with review. Seven live in-memory letter entries remain inferred; lost membership and exact-payload mismatch are proven separately above.
