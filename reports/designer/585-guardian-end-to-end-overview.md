# The Guardian, end to end — mechanism, prompts, training, lifecycle (designer's take)

A whole-overview take on the Spirit guardian for the psyche, written solo (no
subagents) and grounded in the audits (`581`, `582`) plus a verbatim read of
`src/guardian.rs` and the agent component. Opinionated by request — this is my read,
not a neutral description. Where something isn't built or designed yet, I say so.

## 0. The one-paragraph version

The guardian is the daemon's admission gate: *can this proposed forward-intent arrow
enter a store that stays mutually consistent at rest?* The **plumbing is good**
(fail-closed, typed verdict, NOTA enforced, secrets clean). The **judgment is weak**,
and — this is the load-bearing opinion — its weakness is *not* the model. It's three
fixable things upstream of the model: the gate covers only one of four write paths,
the retrieval bundle it judges against is wrong, and the prompt is under-specified and
non-deterministic. Fix those and the same model becomes a good guardian. "Training" is
the longest-horizon piece and shouldn't start with fine-tuning; it should start with a
decision-log that turns the guardian's own verdicts plus your corrections into a
dataset. The lifecycle that shipped (a direct synchronous socket call) is a reasonable
v1 with one real bug; the designed broker is the right long-term shape but premature.

## 1. The mechanism — what the guardian *is*

It is the gate on **durable capture**. A client `Propose`s an `Entry`; the guardian
returns a **binary** verdict — `Accept`, or `Reject` with a *typed reason* and the
*record references* that justify it. No discretion, no rewriting, no "confidence
score": yes or no, and which records are implicated. That minimalism is right — the
guardian's job is to keep the store consistent at rest, not to be smart.

Today it gates **`Propose` only**. `Record` is a raw un-gated write; `Clarify`,
`Supersede`, `Retire` bypass it entirely; and `Supersede` does *no* recheck of its
replacement. **My strongest mechanism opinion: the gate must cover every write that
changes the live arrow set** — at minimum `Propose`, `Clarify`, `Supersede`. The
design premise was "the daemon *is* the guardian"; a gate on one of four doors isn't
that. `Supersede` writing its replacement blind is the sharpest hole — it's a
side-door for exactly the inconsistency the guardian exists to prevent.

**Mechanism decision (psyche): the model checks everything.** I had proposed layering
— cheap deterministic pre-checks, the LLM only as a last resort. The psyche chose the
cleaner shape instead: a *single locus of judgment*, the model. So all *judgment* is
the model's — consistency, duplicate, trample, non-intent, compound — and only pure
structural admission (is this parseable, non-empty NOTA?) stays upstream as input
validation, which isn't "checking" in the judgment sense. Concretely, this folds the
existing deterministic duplicate check *into* the verdict: the model returns
`Reject Duplicate`, and the daemon bumps importance as a mechanical consequence of that
verdict (the model judges; the daemon acts). The trade is conscious — determinism and
reliability now rest *entirely* on the model — so three things become non-negotiable
rather than nice-to-have: (1) **complete retrieval**, because the model can only catch
a duplicate or contradiction it is actually *shown* (so category-only retrieval is now
a *correctness* bug, not a performance one); (2) **temperature 0**; and (3) **the
decision-log → training flywheel** (§3), which is how a single-judge model becomes
consistent over time. Layering would have bought determinism from carve-outs; here it
must come from temp-0 + retrieval + training.

## 2. The prompts

The current system prompt is one terse paragraph: *"You are Spirit's guardian. Judge
whether a proposed forward intent arrow can enter a mutually-consistent intent store.
Reply with exactly one NOTA GuardianVerdict. Accept form: … Reject form: … Reject on
contradiction, compound intent, non-intent, unclear privacy, unclear category, or
retrieval insufficiency."* The agent then appends a generic "respond in NOTA"
instruction. Temperature is unpinned (provider default ~1.0). The candidate `Entry`
and the retrieved records are pasted in as raw NOTA under two labels.

**My take: right job named, wrong job enforceable.** It asks the correct question and
demands the correct typed output — but it can't reliably *answer*, for reasons that are
all prompt-level, not model-level:

- **Six undefined criteria.** "compound", "non-intent", "unclear" — named, never
  defined, no examples. The model invents each meaning, and invents differently across
  runs and across a provider/model swap (which the deployment can do silently).
- **The output grammar is under-specified for reliable parsing.** The closed set of
  legal rejection reasons is never given to the model, and the mandatory double-`Reject`
  nesting is shown by one example, not stated. A model that picks a reason atom not in
  the enum, or single-nests, emits valid NOTA that *fails the typed parse* → maps to
  `HarnessMalformed` → reject. So a legitimate arrow gets bounced on a formatting slip,
  and the agent's retry loop only checks "is it any NOTA," not "is it a
  `GuardianVerdict`." Fail-closed, but lossy.
- **Unpinned temperature.** A consistency gate wants determinism; nothing here wants
  creative sampling. The same proposal can Accept on one run and Reject the next. This
  is *why* 581 called "zero discretion realized by a non-deterministic guardian" a
  premise gap — it's a sampled yes/no.

The fixes are cheap and high-leverage: pin temperature to 0; generate the closed
reason set + exact verdict grammar *from the enum* into the prompt (so prelude and
parser can't drift); add a small few-shot block of real accept/reject/clarify-trample
examples; define the boundary cases the corpus actually hits (forward-law-vs-negation,
task-order-vs-intent, "an empty bundle is admissible, not 'retrieval insufficiency'");
and make the retry type-aware against `GuardianVerdict`.

## 3. The training — not designed yet; here's how it should work

Today: **no training.** Zero-shot, a general local model (CriOMOS Gemma) reading the
prompt. That's fine as a starting point, but "the training of the guardian" should be
understood as a **data flywheel, not a fine-tune** — at least not first.

The insight: *the training data is the intent layer itself.* Every guardian decision
is a labelled example — `(candidate, retrieved-bundle) → verdict`. Every time you
override a verdict, that's a *gold* correction. The accept/reject/supersede/clarify
history is a growing supervised dataset of the psyche's actual judgment. So the move
is to **build the decision-log now** — persist, for every gated operation: the
candidate entry, the exact bundle the guardian saw, the verdict + reason, and any
later override. It's observability *and* the training set, for free.

**Where it lives: in Spirit, not the agent.** The agent is a *generic* model-caller —
it sees only opaque prompt + completion text, never the structured decision and never
the *later override* (which happens back in Spirit when you correct a verdict), and it
must stay thin and spirit-signal-free (vend-not-ferry). The decision-log is
intrinsically Spirit's: it is the history of decisions over Spirit's *own* intent
records, it sits naturally alongside Spirit's existing operation archive (commit
`3d59bd6`), it is the **privacy boundary** (decisions touch private intent, which must
not leak into a generic caller), and it is the **training set for Spirit's own
guardian** — co-located with the intent layer it learns from. The agent at most keeps a
generic usage/latency log for *budget* accounting — telemetry, not the decision-log.

Then escalate only as signal accumulates:

1. **Few-shot from blessed examples** (now). Curate ~dozen accept/reject/trample cases
   from the corpus into the prompt. Biggest gain per effort; no training infra.
2. **Retrieval-augmented examples** (next). Alongside the consistency-bundle, retrieve
   the most *similar past decisions* and show them as few-shot, so the guardian is
   anchored on precedent, not just the prompt.
3. **Fine-tune a small fast local guardian** (later, maybe never). Once the decision-log
   has real volume and the psyche-override signal is rich, fine-tune a small model on it
   — fast, cheap, deterministic, and it has *learned the psyche's judgment* rather than
   guessing from a paragraph. This is also where the **auditor role** closes the loop:
   the auditor reviews guardian decisions, the psyche confirms, and confirmations become
   the gold labels.

**My take: do not fine-tune yet.** It's premature (insufficient data), and it would
bake in the *current weak prompt's* behavior. Fix the prompt and retrieval first, log
every decision starting now, and let the dataset accrue. The guardian should get better
as the intent layer matures — the system trains itself on your judgments. Fine-tuning
is an optimization you reach for when few-shot + good retrieval stop being enough, not
the starting move.

## 4. The flow & lifecycle — message flow, spin-up, spin-down

**What ships today (direct synchronous socket).** Two long-running user services:
`spirit-daemon` (self-resumes from persisted SEMA state on restart; virgin-starts-and-
waits if unconfigured) and `agent-daemon` (holds the provider config + the LLM key,
read from gopass into its process env; takes one binary rkyv startup archive). The flow
on a `Propose`:

1. CLI sends `Propose Entry` over `spirit.sock`.
2. Signal admission validates the entry shape.
3. Nexus lowers it to a `Propose` effect → `guard_propose`.
4. `guardian_records_for` retrieves the "relevant" existing records.
5. Spirit opens a Unix socket to `agent-daemon`, sends `Call(Prompt)`.
6. Agent calls the configured provider (CriOMOS-local Gemma), validates the completion
   is NOTA, returns `Completed(Completion)`.
7. Spirit parses the text as `GuardianVerdict`.
8. `Accept` → record; `Reject` (or any failure) → `GuardianRejected` (fail-closed).
9. The duplicate guard runs (today *after* the LLM — should be before).

Spin-up/down is coarse: the services are always-on; per call it's just a socket
connect/round-trip/close. **The one real bug: the blocking guardian call runs inside
spirit's single serializing engine mailbox with no `block_in_place`**, so the *whole
daemon stalls* for the full LLM round-trip on every gated `Propose`. The SEMA path does
this correctly; the guardian path doesn't. Cheap fix, should be first.

**What was designed but not built (578 §4a — the broker).** The agent-daemon as a
*broker that vends warm harnesses* rather than ferrying payloads. Flow: spirit asks the
broker for a harness → broker vends a warm, pre-loaded harness (compiled with spirit's
signal contract + prelude) and returns a `HarnessLease` (lease-id, endpoint, capability
token, expiry, budget grant) → spirit talks **directly** to the harness in Spirit
signal → harness calls the model → verdict → lease ends. The broker stays on the
*control* path (keys, budget, rate-limits, warm-pool) but never on the *data* path
(never sees the spirit payload). Spin-up: a warm pool, leased per call; spin-down:
lease expiry, harness returned or torn down.

**My take on the lifecycle.** The broker is the right long-term shape — one place for
model governance instead of every component reinventing keys/budget/pools — but it's
premature with a single consumer. The direct-socket v1 is honest and its failure modes
are typed and fail-closed. So: fix the blocking-in-mailbox bug now; cap/rank the
retrieval bundle and add an agent-side call timeout; and build the broker when the
*second* model-consumer arrives — which it will, because **the guardian is the first of
N**: the auditor is the next LLM-judgment consumer, and at two consumers the broker pays
for itself. Until then, carry the gap explicitly (no lease auth, no budget accounting).

## 5. The overarching take

- The guardian's quality is bottlenecked by **prompt + retrieval + gate-coverage**, not
  the model. Spend there first; the model is fine.
- **The model checks everything** (psyche decision) — one locus of judgment, with only
  structural admission upstream. So determinism rests entirely on temperature 0 +
  complete retrieval + the training flywheel; category-only retrieval becomes a
  *correctness* bug, since the model can't catch what it isn't shown.
- The **gate must cover every live-arrow-changing write** (propose/clarify/supersede),
  and supersede must recheck.
- **Build the decision-log now.** It's the observability you'll want *and* the training
  set you'll need; both are free if you capture from the start.
- **Don't fine-tune yet, don't build the broker yet.** Few-shot + pinned temperature +
  good retrieval now; broker and fine-tune when the auditor (the second consumer / the
  loop-closer) lands.

The through-line: a guardian is only as good as *what it's shown* and *what it's asked*.
Get the bundle right and the question right, keep the model on a short deterministic
leash, and log everything it decides — then it can be trained, later, on the one dataset
that actually encodes the psyche's judgment: the intent layer itself.
