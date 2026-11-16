# SendSeveral419 semantic audit — incomplete, acceptance held

Immutable reviewed input419c750b59b5e514aad5162b3b466e04e66062b1, accepted-a044 parent, owner348. This extends the earlier startup-only compatibility review; it is NOT complete whole-feature acceptance. Source only, no executable test or runtime operation.

## Concrete queued cancellation interaction

Existing queue_operations.rs:cancel (around184) calls withdraw_queued for one queued request that has not reached its seat, then archives it. The419 delta leaves this path unchanged. delivery_group.rs:oldest_delivery_group (110 onward) finds original durable membership by the first remaining logical ID, then requires that ID to equal the original group's first member and the entire original membership vector to equal the queue prefix. For group[A,B], CancelA leaves[B], but durable group remains[A,B]; selection refuses first-member mismatch. CancelB leaves[A], which refuses missing member/length. Both wake and regular full-queue drain use these selectors; later ordinary work cannot advance past the damaged unit.

This is a concrete source-level path conflict, not an observed production failure. The handling of cancelling one member before group delivery was not ruled in the supplied SendSeveral proposal/tuhc. Requested Psyche ruling rather than invent whole-group cancellation, fragment delivery, new recovery or quiet permanent blockage. Candidate remains unchanged/uptake held. Required disconfirming fixture after ruling: admit group, cancel first/middle/last queued member, retain later ordinary request, reopen and exercise actual selector/wake/drain and cancellation notification semantics.

## Other verified facts / remaining review

Admission reuses one atomic store transaction with per-batch ID exclusion and duplicate-answer binding refusal. Contract adapter schedules one WakeDue only after a successful nonempty reply; direct send_several_requests fixtures do not test that seam. mark_queue_retryable on rejected startup touches a later Queued/Retryable suffix but does not change selected Uncertain members; an unchanged-suffix lifecycle oracle would be false. Accepted receipt seams and fixture preservation are independently passed by Core; preservation is not whole-feature semantics.

Coreh9g2 lists production fixture-plan gaps: Started is not receipt, no fresh-start or post-Started/pre-parking barrier, fragment control must exclude independently authoritative full-launch receipt, existing fresh-Claude rejection control absent, actual handler path not yet covered, asleep starts cannot prove awake aggregate interruption. Owner revised PLAN ONLY, no hook/fixture implementation authorized. Complete admission/handler/group/startup review and final exact-source verdict remain owed after policy boundary resolves; no generated/dependency/gate/main/live acceptance is given.

## Policy answer — implementation still pending

Psyche r267 rules: Cancel withdraws only the request it names. A group cancelled in part before delivery sends the surviving members together, in written order, without the cancelled one; cancellation blocks neither the group nor later queued work. All cancelled sends nothing. A delivered member uses ordinary cancellation. VersionZero received the exact rule and must propose bounded source/fixture changes before bodies. Original native submission history and retained receipt comparison remain distinct from effective pre-submission membership; missing/corrupt membership must not be treated as cancellation without durable evidence. Source419 and its acceptance hold are unchanged.

## Cancellation plan review

Read `/tmp/send-several-implementation-44f3be.TuR4zW/cancellation-plan-348.md` whole. Approved representation: positive matching current Withdrawn state and retained exact logical/request/address evidence; commit_archive_request retains that state and the retained request. No new cancellation-cause schema is required for this evidence. Generic Archived, missing binding, missing row or other terminal state is insufficient. Bodies remain held: asked Psyche whether sleeping atomic premark (before native I/O) is the submission cutoff for ordinary uncertain cancellation. That is a policy boundary, not silently inferred from source; serial seam fixtures do not establish concurrent race/crash guarantees.

## Simplified-recipient policy answer

Psyche3vro: a simplified group may have at most one awaiting request (Order/Question/Task), at any position; other Living/Notice/Result/Done members are context. Its response answers that one awaiting request; with none, no request is answered. Two or more are refused atomically at admission, naming the second. Regular recipients are unchanged. VersionZero must propose bounded selector/binding/admission/fixture and contract-impact changes before bodies. Existing first-member binding does not satisfy this policy; typed second-member refusal may require an ordinary65/paired85 vocabulary amendment, coordinated with Core before generation. Current953 stays immutable; no full-feature or uptake/gate acceptance.

## Resumed governing-plan review: 0k7j
Read the current governing-cutoff, typed-refusal and authority sections of simplified-plan-348.md. Release only a behavior-preserving typed admission-origin/shared read-only mode-evidence abstraction tranche; return exact diff before singleton grouping or Simplified behavior changes. Unknown mode is a local typed unresolved result, not guessed Regular. Correct declaration/cutoff consistency requires shared transaction/dispatch guard or checked evidence, an implementation proof still owed.

Existing Failed(Refusal) sender observations are not automatically the ruled whole Withdrawn outcome. Existing Notice.String is not a typed routed refusal. Sent consolidated existing policy questions to Psyche core Opus: sender observation versus routed result and required terminal lifecycle, unresolved-mode refusal meaning, aggregate payload/ID-capacity versus written-order member precedence. No new schema/family/recovery/string substitute was authorized. Current953 and accepted receipt seams remain preserved; this is not whole-feature semantic acceptance.
