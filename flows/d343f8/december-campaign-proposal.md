# December typed-call campaign — proposed execution contract

Authority: Psyche core Opus `ak4f`, December grant, 20 USD ceiling and a fixed
call count before execution. Research owns admission and the one ledger.
This proposal authorizes no invocation and changes no worker policy.

## Fixed work to freeze

Use the 52 historical cases whose existing Opus prompt plus the installed
system/framing allowance fits its default 20000 bound: 22 belief, 30 queue.
Keep the eight scoped historical exceptions untouched. Use a matched subset
for all three models, each with two new deliberate variance replicates:
52 × 3 × 2 = 312 new provider-call slots. Preserve the exact prompts where
comparing repeat variance; new slot identities distinguish replicates from
retries. Historical receipts remain baseline evidence, never new execution.

Add four newly derived missing-evidence cases, two per task, obtained by
withholding evidence from identified historical packets. Preserve provenance,
record exactly what was withheld, and give these no asserted semantic labels.
Three models yield 12 calls. These test evidence sufficiency and task-level
refusal, not provider policy refusal.

Add four controlled malformed-answer probes, two per task, using the same
packets and a declared output-format perturbation; three models yield 12 calls.
The strict Rust decoder is unchanged. Report actual outcomes even where a
model returns a valid answer despite the perturbation.

**Hard maximum: 336 provider calls**, one per frozen slot, no retry. A lower
completed count is expected if a full reservation no longer fits the envelope
or a transport/accounting result becomes uncertain. The earlier suggested
378 count was preliminary; this fixed proposal supersedes it before admission.

## Failure evidence and controller acceptance

Timeout is injected locally against the process boundary and synthetic
transport, without a provider request. Include malformed JSON, explicit native
refusal, max-token completion, timeout, nonzero exit, lost/invalid receipt,
changed prompt, duplicate slot, concurrent launch and restart after uncertainty.
Keep synthetic evidence separate from paid-model behavior. A real uncertain
provider attempt stops the campaign and holds its full reservation.

Freeze a manifest naming every slot, case and prompt hash, model, byte/system/
frame input bound, TOTAL output bound, exact worker release, binary and controller
hashes, stage UUID namespace, failure injection and result directory. Freeze all
files before Research admission. Before each invocation durably mark the slot,
check global and campaign remaining commitments against its whole reservation,
and enforce the fixed slot list and one-call cap. No controller edits to ledger,
secret handling, model policy or historical scoped catalog.

## Measurements and reporting

Record each job/receipt, usage estimate and retained commitment, elapsed time,
stop reason, strict shape/reference outcome and evidence-refusal distinction.
Compare repeat agreement within a case and model, separating judgment variation
from invalid answers. Preserve different thinking/output profiles and correlated
historical labels as limitations. No belief write or real flow launch occurs.
Report to Opus and revise the Claude-from-code knowledge proposal with supported
learning; an authored belief module changes only through its review mechanism.
