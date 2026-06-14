# Designer review — operator's structural-forms-integration (8 repos)

Designer review of the operator integration, per the Designer-Operator protocol
(operator integrated, designer reviews). 8 parallel reviewers, each **independently
re-ran the build and tests** at the commit (did not trust the operator's claim).
Net: the integration is on the correct branch and 6 of 8 repos are faithful; **two
repos carry real regressions** that operator's own verification missed.

## Correction up front — the "not on main" finding is mine, not operator's

Every reviewer flagged "commit not on main, only on `origin/structural-forms-integration`."
That is **the intended state**, not a divergence: the psyche's directive was
*"implement the best of all ideas into a **new branch** for all affected components
which will need to be remerged whenever main changes,"* and operator named that
branch `structural-forms-integration` and pinned the integration-stack repos to
each other's branch (the correct intermediate). **I gave the reviewers a wrong
premise** ("operator integrated to main"; I misread "pushed structural-forms-integration"
as a push to main), so 6 of 8 "concern/divergent" verdicts are that artifact. The
branch is right; the remerge-to-main (and dropping the cross-repo branch pins once
the nota-next leaf derives land on nota-next main) is the pending step the directive
itself describes. The verdicts below are re-read with that corrected.

## Verdicts (corrected)

| Repo | Source faithful? | Tests (re-run by reviewer) | Real issue |
|---|---|---|---|
| nota-next `00d00504` | **Yes** — both leaf shapes (HeadedAtom + PascalHeadBody), clean octopus merge | 69 pass | none |
| triad-runtime `7a84034b` | **Yes** — reaction frame byte-identical to designer prototype (all 4 pieces) | 10 + doctest pass | none |
| schema-rust-next `573375da` | **Yes** — emission golden matches the prototype shape | suites pass | none |
| signal-spirit `e85830b1` | **Yes** — deps aligned, no `[patch]` path-seams, wire contract intact (rustfmt-only diff) | 7 pass | none |
| meta-signal-spirit `cc576705` | **Yes** — Configure/Import contract intact, **no MirrorTarget**, deps aligned | pass | none |
| sema-engine `1afcd012` | **Yes** — full engine-decomposition stack (CommitLog + Outbox planes) | suites pass | none (merge commit, benign) |
| schema-next `2bb0228e` | **grammar yes, quality NO** | 181 pass | **3 reconciliation fold-ins reverted** |
| spirit `d2cf86fd` | **store decomp yes** | default pass / **--all-features FAIL** | **testing-trace regression** |

The good news is substantial: the reaction frame is faithfully integrated and
consistent across its three lanes; the meta-signal split held with **no MirrorTarget**
leaking into the contract (operator's deliberate drop was correct); the deps are
coherent across the integration branch; and the wire/contract surfaces are intact.

## Real regression #1 — schema-next dropped three reconciliation fold-ins

The **wire decisions landed faithfully**: full-English heads `Vector`/`Optional`/
`ScopeOf` (no abbreviations), flat `(Map K V)` across all lowering paths + encoders
+ fixtures, the generics/`Application` form — and 181 tests pass. But the
integration **reverted the three code-quality improvements** that the designer
reconciliation (`631`, branch `next/typeref-structural-generics` `17b4ebc7`)
explicitly folded in — it looks integrated from raw `schema-generics`, not from the
reconciled branch:

- **(c) derive-single-source REVERTED.** The redundant hand-written
  `NotaDecode`/`NotaEncode` machine codec on `TypeReference` is **back**
  (`schema.rs:1457-1521`, ~65 lines of string-dispatch; operator's own doc-comment
  calls it "the canonical-only … machine codec"). The reconciled branch had thin
  delegators onto the single structural source of truth.
- **(d) thiserror REVERTED.** `SchemaError` is back to a plain enum with a lazy
  `write!("{self:?}")` Display and hand-written `From` impls; `thiserror` is not
  even a dependency. The reconciled branch had 51 `#[error]` attrs + `#[from]`.
- **(e) HeadedAtom seam DROPPED.** `(Bytes N)` is decoded by hand
  (`from_fixed_bytes_width`, `parse::<u64>()`) instead of via the
  `#[shape(head="Bytes", atom)]` HeadedAtom seam — so the reconciliation's "consume
  both nota-next leaf derives" is only half-true here.

These compile and pass tests — they're **intent/quality regressions invisible to
the test suite**, which is exactly why they slipped. The grammar a consumer sees is
correct; the internal "the derive is the single source of truth" property the
reconciliation bought is lost.

## Real regression #2 — spirit testing-trace is broken

Default-feature `cargo test` is green (46 + 3 + 4 + 1), but **`cargo test --all-features`
(the `testing-trace` feature) fails 2 tests** in `instrumentation_logging.rs`
(`testing_trace_builds_record_activations_by_default`,
`testing_trace_records_real_signal_nexus_and_sema_activations`). The test file is
byte-identical to base `adeba15` and **base passes** — so this is a behavior
regression introduced by the integration, not a stale test. Root cause: the store
decomposition changed `Store.database` from an owned `SemaDatabase` to
`Arc<SemaDatabase>` (`store/mod.rs:81`) — and that `Arc` store-sharing slice
**originated in the very 0.13.x surface operator said it dropped** (commit
`37bafef`). So MirrorTarget/version-bump were correctly dropped, but the `Arc`
store-sharing edit from that same risk surface **did land**, and it bypasses the
`SemaEngine::apply` trait default that fires `trace_sema_write_applied()` — the
`SemaWriteApplied` trace event is no longer emitted. **Operator's "cargo tests pass
on all" claim is false for spirit under `--all-features`** (the verification ran
default + `nota-text`, not `--all-features`, so it missed this).

## Action items for operator (before this branch lands on main)

1. **schema-next:** carry forward `17b4ebc7`'s three fold-ins — restore the thin
   delegators (drop the re-introduced hand codec), re-apply `SchemaError`→thiserror,
   and route `(Bytes N)` through the HeadedAtom seam. (Or, if there was a reason to
   drop them, state it — but the reconciliation `631` was the agreed target.)
2. **spirit:** fix the `testing-trace` regression — route the `Arc<SemaDatabase>`
   shared-store write through the `SemaEngine::apply` hook so `SemaWriteApplied`
   fires again, and **run `cargo test --all-features`** as part of verification.
3. **Pending (per the directive, not a defect):** remerge to main when ready, and
   drop the cross-repo `structural-forms-integration` branch pins once the nota-next
   leaf derives land on nota-next main.

## The review loop worked

Designer review caught two regressions operator's own verification missed —
because operator integrated schema-next from the wrong source branch (raw
`schema-generics`, not the reconciled `17b4ebc7`) and verified spirit on the wrong
feature set (default/`nota-text`, not `--all-features`). Neither breaks the default
build; both are real; both are fixable before main. That is exactly what the
Designer-Operator review protocol is for.
