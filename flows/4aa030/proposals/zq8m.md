# zq8m — a successor takes open work at refresh

Authority: Psyche zq8m and5r29; Astra6rs4/rc2y places this before x0t5, ujg2 and R1. This is a source proposal, not an implementation or live action. The separate Home/consumer publication follow-up remains pending exact-candidate host Evaluate receipts.

## What already works

Accepted public Flow379 carries the permaflow's unanswered requests into a successor's first prompt. The retained open-request lookup is authoritative; it is not the permaflow queue. The hrg0 account is `flows/5c5586/reports/hrg0.md`.

Source379 `waking.rs` makes the immediate-successor decision twice: `refresh_held` around2096–2123, and the threshold-at-stop path around4150–4158. Both use only Maintained continuity or a queued non-Soft message. Thus a delivered unanswered request can be carried by a future successor yet fail to cause that successor to start now. Existing `wake_is_due` around1702 is a different decision, for an already-asleep flow; it is outside this release.

## Proposed next shape

One shared runtime capability decides whether a refresh owes an immediate successor, from the held metaflow/continuity and authoritative open requests. Its reasons are Maintained continuity, queued waking work or unanswered delivered work; absence of all three retains existing OnDemand sleep. Both refresh decision sites call the same capability. The queue and open-request records stay separate, and no request is requeued, settled, cancelled or copied into a second store family.

The decision is made under the existing dispatch/refresh custody before closing the predecessor. An open-request read failure keeps the predecessor and follows the existing typed store-failure path; a failed read never means an empty request set. The existing successor-first operation still owns launch intent, composition, confirmation, queue delivery and predecessor reap. First-prompt composition remains the existing open-request composition path.

This release introduces no configuration, wire vocabulary, memory family, native endpoint migration, warm-resume policy or policy enablement. x0t5 remains separate and must show its ruled Ethos before implementation.

## Acceptance evidence

- OnDemand, delivered unanswered Order, empty waking queue: explicit refresh starts and confirms a successor before predecessor reap. The successor's actual first prompt carries that same Order id/text exactly once.
- The same condition through queued refresh-at-idle and through threshold refresh reaches the same immediate-successor capability.
- OnDemand with no open work keeps its existing sleep branch; an answered Order is not open work. A Soft Notice alone is not promoted to an Order.
- Open-request ownership survives successor launch refusal; there is no false success, settlement or duplicate first-prompt request.
- Existing Maintained/queued-waking successor and no-policy regression fixtures remain green.

Use existing NexusFixture/staged-successor/first-prompt capture machinery in `tests/unit/refresh_and_compaction.rs` and the relevant ordered-refresh fixtures. Keep the test oracle on actual successor launch/prompt and original request identity, not merely a boolean predicate.

## Custody, gate and release

After a fresh public-main check, reserve a NEW isolated Flow worktree from then-current accepted main379, preserving282 and every unrelated owner. Expected edits are the shared succession decision and its two consumers in `crates/flow-nexus/src/waking.rs`, plus bounded existing unit-fixture files; exact additional paths require reservation before writing. No body has been edited yet. Please identify any required Rust-doctrine packet not already furnished with vision:code/vision:nexus.

Commit/push the candidate before the full immutable Prometheus gate; the existing20-attribute gate is the whole release gate, including compiled fixtures/lints. Return exact source delta, fixture matrix, published revision and gate terminal to Astra for review. Main promotion, consumer pinning and any later deployment each retain their separate authority. No timer, polling loop or live refresh experiment is part of the proof.
