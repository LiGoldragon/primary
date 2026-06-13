# 616 — SEMA VC: reconciling the two audits, plus questions & suggestions

*The psyche asked me to consider the system-designer lane's reports on the
SEMA version-control work and bring my most important questions and
suggestions. This reconciles my independent Opus review (designer/615) with
SD's independent Opus audit (system-designer/102), the grand design
(system-designer/95 + its open-decisions brief 95/9), and the field evidence
from cloud-designer/42 (lojix as a second consumer of the engine). Two
independent Opus reviews of the same code largely converge — which is the
strongest correctness signal available; the divergences and the gaps each
missed are where the value is.*

## TL;DR

Both audits reach the same verdict: **the architecture is sound; the system is
half-deployed; the one risk that matters is that nothing is backed up off-host.**
The local intent corpus is fully authoritative, tamper-evident, and durable *on
this one disk* — but the `29pb` "state loss is unacceptable" promise is met only
in tests. Beyond that shared core, the audits diverge on exactly one severity
(the single-writer gap), each caught one thing the other missed, and a *third*
lane (cloud-designer, building lojix on the engine) surfaced a cross-table
atomicity gap neither audit centered. Three things need your judgment; three
suggestions follow.

## Cross-audit reconciliation

Where my 615 and SD's 102 land on the same findings — convergence is high-confidence:

| Finding | My 615 | SD 102 | Reconciled verdict |
|---|---|---|---|
| Nothing ships to the mirror; remote durability is test-only | flaw #9, **High** | D4-1, **High** | **Confirmed by both.** The #1 live gap. |
| Migration v8→v9 fold is faithful + crash-safe; `ebee6e44` pin correct | "doubt resolved", good | D2-2/D1-1, Info | **Both clear it.** The outage was deploy-coupling, not migration logic. |
| Single-writer is convention, not structure | flaw #2, **High** | D3-2, **Low** | **Severity diverges — see below.** |
| Old-version (v1–v6/v7) migration paths untested | flaw #5, High (risk) | D2-1/D2-3, High/Medium | **Both flag.** You ruled old versions disposable → resolves to "delete + reject". |
| `RecordKey` stringifies a typed u64 | flaw #7, Low | D3-1, Low | **Both flag.** Make it a closed sum. |
| "Exclusive DB / read-only by construction" is doc, not type | flaw #6, Medium | (implied by D3) | I weight it higher; cheap to seal. |
| Fold law / hash chain / checkpoints / layout guard sound | good patterns | D3-4/D3-5, Info | **Both confirm.** The strongest layer. |
| No back-compat cruft; discipline (no free fns, typed errors) held | good patterns | D6, Info | **Both confirm.** |

## Where the two audits diverge — the single-writer gap

This is the one real disagreement, and it is exactly the actor-model question:

- **SD rated it Low (D3-2):** "Cannot bite production — the single kameo actor
  serializes." True for spirit *today*.
- **I rated it High (615 flaw #2):** the engine is published as "native version
  control as **one reusable library**"; its `&self` writers compile fine and a
  second consumer that doesn't front it with a single actor forks the chain. The
  guarantee should live in the engine, not be borrowed from each consumer's
  discipline.

**The tie-breaker is already on disk: lojix is a second consumer** (cloud-designer/42
S3, `196ab501`) — it adopted spirit's `Store`-on-`Engine` pattern verbatim. The
engine *is* being reused right now, so the reusable-library framing is the
operative one, not a hypothetical. That argues for the higher severity. (The
psyche agreed with this framing in chat.)

The happy reconciliation: **SD's recommended fix for D3-2 — move the
sequence/digest reads inside the write transaction — also closes my flaw #1.**

## What each audit caught that the other missed

- **My 615 caught, SD did not:** the **O(n)-per-write full-log decode.**
  `latest_versioned_entry_digest` (`engine.rs:1997`) rkyv-decodes the *entire*
  versioned log on every write just to read the last 32-byte digest — O(n²) over
  the store's life, for an append-only log. SD's D3-2 looks at the *same read*
  but only as a concurrency issue (Low); the performance dimension isn't in their
  findings. Three of my readers converged on it independently. It's not in SD's
  bead list — it should be added, and the single in-txn fix above kills it for free.
- **SD's 102 caught, I did not:** (a) **D4-2, High — the mirror's TCP ingress
  binds `0.0.0.0:7474` with zero auth at any layer**, defeating the design's
  bind-to-tailnet trust boundary (my review didn't examine the mirror's network
  security); (b) **D2-1, High — the v7→v9 fold imports zero referents**, so any
  v7 record with a referent aborts migration (latent; live store is v8); (c)
  **D6-1 — three god-impl files over 1800–2118 lines** against the explicit
  "no thousand-line files" bar (my review didn't weigh file size).

Two independent audits, near-total agreement, and each filled a blind spot in
the other. That is the case for running both.

## The field finding neither audit centered: cross-table torn writes

cloud-designer/42 (S3) is the most valuable corroboration, because it comes from
*actually building a second component* on the engine rather than reading it. lojix's
`record_activation` must write two related rows (a live-set row, then its gc-root
row). It does so as **two sequential keyed asserts**, because **`CommitRequest`
is single-table** — so a crash between them leaves a torn write (a live row with
no gc-root) and there is no reopen reconciliation.

This refines a claim I made in 615. I praised "every write lands data + log +
versioned entry + outbox + counters in one transaction" — true, but that
atomicity is **per-record / per-family**. The engine has **no multi-table atomic
commit**, so any consumer that needs two *families* to move together is exposed.
spirit hasn't hit it yet; lojix already has. The named right-layer fix (Spirit
`fosp`: sema-engine is the exclusive DB boundary) is a **sema-engine multi-table
atomic commit** — the highest-value engine improvement, because every
multi-family consumer needs it and the alternative is per-consumer
reopen-reconciliation hacks.

Also worth correcting a likely misread of the commit subject: cloud-42's "S3" is
the *stage* (S0…S6), persisting to a **local** `lojix.sema` file — not Amazon S3.
So lojix inherits the *same* single-local-file durability gap as spirit. There is
no off-host backup anywhere yet.

## The vision gap: grand DVCS vs shipped versioned-log

The grand design (system-designer/95) imagined a full DVCS: branches, merge /
rebase, conflict policies, an RFC-6962 signed history tree, BLS attestation, and
federation (96). What **shipped** is a versioned, hash-linked, payload-bearing
**append-only log + checkpoints + crash-safe migration + an idle mirror**. That
is a coherent, valuable subset — but it is a subset, and the open-decisions brief
(95/9) names the fork that frames everything else:

| Open decision (95/9) | SD's safe-default recommendation |
|---|---|
| 1. Where the branch/policy/attestation layer lands | A new `sema-vcs` crate over `sema-engine` (keep the engine crypto/policy-free) |
| 2. Default conflict policy | Typed-conflict (record, never silently clobber); per-family opt-in to last-writer |
| 3. Cross-schema merge | Same-schema-only first; refuse cross-schema loudly |
| 4. Multi-LCA / criss-cross merge | Refuse loudly now; git-ort virtual base only when a real case appears |

These only matter *if* you want branches and merge. The deployed system has none
of that machinery and doesn't need it for "durable, tamper-evident, migratable
intent with an off-host copy." So the framing question below is upstream of all four.

## Questions for the psyche

1. **How much of the grand DVCS do you actually want — or is "versioned log +
   off-host backup" the real target?** If the goal is durable, tamper-evident,
   migratable state with a remote copy (which is what `29pb`/`iir4`/`fosp` literally
   say), then the priority is *closing the durability loop and the atomicity gap*,
   and the branch/merge/conflict-policy machinery (95/9 decisions 1–4) can stay
   deferred indefinitely. If you do want true DVCS (branches you merge), then 95/9
   decision 1 (the `sema-vcs` crate) should be made *first*, because it frames
   where every other type lands. My lean: **ship the durable-log target; defer the
   DVCS** until a concrete branching need appears.

2. **The single-writer gap: SD rated it Low, I rated it High, you agreed with me —
   does it get bumped on the bead list?** lojix being a live second consumer is the
   evidence for High. The fix is cheap and also closes the O(n) write cost.

3. **Old versions are disposable (you confirmed) — so: delete the v1–v6 (and v7?)
   migration readers and make the version probe loudly reject any pre-current
   store, rather than carry untested migration code?** Both audits flagged the
   untested old paths; deleting them is cleaner than witnessing them. Quick operator
   bead — confirm and it's done.

## Suggestions (ordered, reconciled with SD's bead list)

1. **Close the durability loop — but auth before shipper, and there's a cheap
   interim.** This is the #1 risk both audits name. Ordering matters: SD's D4-2
   (rebind the mirror off `0.0.0.0` to tailnet + land attestation) must come
   *before* D4-1 (wire spirit's shipper), or the shipper feeds an unauthenticated
   ingress. **Interim safety net now:** a periodic off-host push of the single
   self-contained `spirit.sema` file (it's a rebuildable view; one file is the
   whole corpus) — zero network exposure, satisfies `29pb` today while the proper
   shipper path lands. Do not soften the intent; close the gap.

2. **Add a sema-engine multi-table atomic commit** (the cross-table torn-write
   fix). Highest-value *engine* improvement: lojix already needs it, spirit will,
   and `fosp` puts atomic multi-family writes squarely in the engine's lane. The
   interim per-consumer reopen-reconciliation is a stopgap, not the right layer.

3. **Fold the O(n)-per-write fix into SD's D3-2 bead.** Cache the chain-head digest
   in a `COUNTERS` slot updated inside the write transaction; that one change makes
   single-writer structural (closes SD D3-2 / my flaw #2) *and* removes the
   full-log decode (my flaw #1, absent from SD's beads). One fix, three defects closed.

SD's lower-priority designer beads (split the god-impl files, `RecordKey` closed
sum, the naming warts, surface the `StoreSchemaHash` on `Version`) I agree with as
filed — they're low-risk discipline cleanup and don't need re-litigating.
