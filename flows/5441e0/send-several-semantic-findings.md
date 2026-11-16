# SendSeveral419 semantic audit — incomplete, acceptance held

Immutable reviewed input419c750b59b5e514aad5162b3b466e04e66062b1, accepted-a044 parent, owner348. This extends the earlier startup-only compatibility review; it is NOT complete whole-feature acceptance. Source only, no executable test or runtime operation.

## Concrete queued cancellation interaction

Existing queue_operations.rs:cancel (around184) calls withdraw_queued for one queued request that has not reached its seat, then archives it. The419 delta leaves this path unchanged. delivery_group.rs:oldest_delivery_group (110 onward) finds original durable membership by the first remaining logical ID, then requires that ID to equal the original group's first member and the entire original membership vector to equal the queue prefix. For group[A,B], CancelA leaves[B], but durable group remains[A,B]; selection refuses first-member mismatch. CancelB leaves[A], which refuses missing member/length. Both wake and regular full-queue drain use these selectors; later ordinary work cannot advance past the damaged unit.

This is a concrete source-level path conflict, not an observed production failure. The handling of cancelling one member before group delivery was not ruled in the supplied SendSeveral proposal/tuhc. Requested Psyche ruling rather than invent whole-group cancellation, fragment delivery, new recovery or quiet permanent blockage. Candidate remains unchanged/uptake held. Required disconfirming fixture after ruling: admit group, cancel first/middle/last queued member, retain later ordinary request, reopen and exercise actual selector/wake/drain and cancellation notification semantics.

## Other verified facts / remaining review

Admission reuses one atomic store transaction with per-batch ID exclusion and duplicate-answer binding refusal. Contract adapter schedules one WakeDue only after a successful nonempty reply; direct send_several_requests fixtures do not test that seam. mark_queue_retryable on rejected startup touches a later Queued/Retryable suffix but does not change selected Uncertain members; an unchanged-suffix lifecycle oracle would be false. Accepted receipt seams and fixture preservation are independently passed by Core; preservation is not whole-feature semantics.

Coreh9g2 lists production fixture-plan gaps: Started is not receipt, no fresh-start or post-Started/pre-parking barrier, fragment control must exclude independently authoritative full-launch receipt, existing fresh-Claude rejection control absent, actual handler path not yet covered, asleep starts cannot prove awake aggregate interruption. Owner revised PLAN ONLY, no hook/fixture implementation authorized. Complete admission/handler/group/startup review and final exact-source verdict remain owed after policy boundary resolves; no generated/dependency/gate/main/live acceptance is given.
