# Spirit Guardian design feedback

Operator feedback, no subagents. Scope: the Guardian mechanism, prompt shape,
training/evaluation design, message flow, and process lifecycle. Grounded in
designer reports 578, 581, 582, 584; operator reports 354, 355, 356; current
`spirit` and `agent` source.

## Short take

The high-level design is right: Spirit should own the gate, an agent/model should
own semantic judgment, the verdict should be typed, and failures should fail
closed. That is the correct separation of authority.

The current implementation is a useful v1, not the full Guardian. It gates only
`Propose`, asks a single prompt through the `agent` API-call component, parses a
typed verdict, then either admits or rejects. That is operationally valuable, but
it is not yet the invariant from 578: "the live intent store is always mutually
consistent by construction."

The weakest parts are not the Unix socket plumbing. The weak parts are:

- the gate does not cover every write path that can change durable intent;
- retrieval still undersupplies the model;
- the prompt is under-specified for a typed semantic court;
- "training" is currently absent unless we count a prompt as training;
- the deployed `agent` component is not yet the leased harness architecture from
  the design.

My view: keep the current v1, but do not mentally promote it to the final
Guardian. The next layer should be evaluation-first and flow-correct before any
fine-tuning or elaborate model training.

## Intended Guardian model

The design in 578 is coherent because it separates four jobs:

- Spirit stores live intent as forward arrows.
- Spirit daemon owns admission authority and durable mutation.
- An LLM Guardian judges semantic consistency.
- Subscription/archive/history carry motion without polluting the live query
  surface.

The key premise is simple: if live Spirit is the psyche-at-rest, then no durable
write can bypass the gate unless the write is explicitly outside the guarded
surface. If a normal user-facing capture can write unguarded, the store is not
consistent by construction; it is merely usually consistent when callers choose
the right command.

The best piece of the design is the typed verdict. The Guardian should not return
"looks okay" prose. It should return a closed value: accept or reject, with a
closed reason enum, referenced records, and a short explanation. That makes the
boundary testable. It also lets clients react: revise, ask the psyche, rename a
supersede target, clarify privacy, or drop the proposal.

The second-best piece is the state/stream split. Clarification and correction are
motions; the live record is the resting arrow. The event tells subscribers what
changed, while archive/journal state preserves recoverability outside the normal
intent query surface.

## Current implementation

Current source has these important pieces:

- `Propose Entry` exists as a Signal operation.
- `GuardianVerdict [Accept (Reject)]` exists in the Nexus schema.
- public `GuardianRejected GuardianRejection` exists in the Signal schema.
- `AgentGuardian` calls `signal-agent::Call(Prompt)` over a Unix socket.
- `agent` calls an OpenAI-compatible provider and returns `Completed`.
- Spirit parses the completion as `GuardianVerdict`.
- failures map to `GuardianRejected`, so `Propose` fails closed.
- deterministic duplicate detection still runs after the model accepts.

That is a good v1 skeleton.

But the scope is narrow:

- `Record` still writes directly.
- `Clarify` calls the store directly.
- `Supersede` calls the store directly.
- `Retire` calls the store directly.
- `ChangeRecord`, `ChangeCertainty`, `BumpImportance`, and `Remove` are direct
  SEMA writes.

Some of those direct paths may be legitimate maintenance operations, but the
product surface needs a hard distinction between "guarded durable capture" and
"owner maintenance." Right now that distinction is semantic convention, not
authority.

The current Guardian also does not independently classify the operation. If a
caller says `Clarify`, the Guardian is not asked whether the change is actually a
clarification. If a caller says `Supersede`, the replacement is not checked
against the rest of the store. That is the exact side door the design was trying
to close.

## Message flow today

The successful guarded path today is:

1. A client sends a single NOTA input such as `Propose`.
2. The CLI parses it into generated `signal::Input`.
3. The CLI sends binary rkyv Signal over the working socket.
4. The daemon decodes `Input` and runs Signal admission validation.
5. Nexus receives `SignalArrived(Input::Propose)`.
6. Nexus lowers that to `NexusEffectCommand::Propose`.
7. Nexus asks `Store::guardian_records_for(&entry)` for context records.
8. Spirit builds a `signal-agent::Prompt`.
9. Spirit opens one Unix stream to `agent-daemon`.
10. Spirit sends `signal-agent::Input::Call(Prompt)`.
11. `agent` resolves provider/model/key handle.
12. `agent` makes the provider call.
13. For `OutputMode::Nota`, `agent` checks the model output parses as any NOTA
    document and retries once if not.
14. `agent` replies `Completed(Completion)` or `CallRejected`.
15. Spirit parses the completion text as `GuardianVerdict`.
16. `Accept` continues to deterministic duplicate guard and then writes the
    record.
17. `Reject`, malformed output, socket error, or agent rejection returns
    `GuardianRejected`.

That flow has a solid binary/process boundary and the right fail-closed posture.
The most important caveat is that the model call is currently a synchronous
Spirit-side socket call inside the Nexus effect path. The SEMA read/write paths
have explicit `block_in_place` treatment for multi-thread runtimes; the Guardian
call should receive the same kind of boundary or become a proper async effect.

## Spin up and spin down

Current deployed shape:

- `agent-daemon` starts from one binary rkyv archive.
- `agent-daemon` has provider seed configuration and resolves the real key from
  an environment handle at call time.
- `spirit-daemon` starts from one binary rkyv archive.
- Spirit's startup config optionally includes Guardian agent socket/provider/model
  settings.
- For each guarded call, Spirit opens a fresh Unix connection to `agent-daemon`
  and closes it after the reply.

That is simple and serviceable.

It is not yet the 578 harness lifecycle:

- no agent daemon leasing a per-component harness;
- no warm Spirit Guardian harness pool;
- no lease id;
- no capability token on the direct channel;
- no durable lease lifecycle journal;
- no per-call model grant injected into a harness;
- no harness process that is compiled with `signal-spirit` and owns the whole
  Spirit-specific prompt/verdict discipline.

The current `agent` repo is intentionally only an LLM API-call component. Its
own intent says harness backends are deferred. So the design should name this as
the v1 shortcut, not blur it with the full harness architecture.

## Retrieval

Retrieval is the Guardian's real substrate. A brilliant prompt cannot judge a
record it was never shown.

Current `guardian_records_for` now uses the new `Domain` field, which is an
improvement over the failed gerund categories. But it still does only this:

- partial domain match on the proposed domains;
- any keyword;
- any text;
- any referent;
- default nonzero certainty floor;
- any privacy and importance.

The missing pieces are important:

- keyword spans from the proposal should be used as retrieval leads;
- full-text terms from the description should be used as retrieval leads;
- referents should be used when present, because the most relevant conflict is
  often "same concrete thing, adjacent domain";
- retrieval should probably be a union of leads, not only an intersection;
- the bundle should be ranked and capped before prompting.

The new domain/referent model gives the Guardian a better index, but the Guardian
does not yet consume the full index. In particular, ignoring referents leaves
real precision on the floor. If the proposal governs `spirit`, records about
`spirit` should be candidates even when the domain filing differs.

## Prompt

The current prompt has the right shape at the top:

- it tells the model it is Spirit's Guardian;
- it says the job is admitting a forward intent arrow into a mutually consistent
  store;
- it shows the accepted `Accept` form;
- it shows a rejected form;
- it names broad rejection criteria.

But it is too thin for reliable judgment.

Problems:

- The reason enum is not fully listed and defined.
- Each reason lacks examples and boundary rules.
- The prompt does not explain operation-specific criteria because only `Propose`
  is wired.
- The prompt still says "unclear category" while the generated reason is now
  `UnclearDomain`; that is small, but it is exactly the kind of prompt/schema
  drift the design says should not exist.
- The agent-level NOTA retry checks "is this any NOTA?", not "is this the exact
  `GuardianVerdict` type?"
- Temperature is unset, so the provider default controls determinism.
- The prompt asks for a semantic court decision but gives the model almost no
  precedents.

I would harden it like this:

- generate the verdict grammar and closed reason list from the schema;
- include a compact rubric for each reason;
- include two or three positive and negative examples from fixture files;
- set temperature to zero or the provider's deterministic equivalent;
- make the retry type-aware: "your NOTA parsed, but not as GuardianVerdict";
- keep explanation short and bounded;
- include the operation being judged and the exact authority rule for that
  operation.

Do not ask the model to expose chain-of-thought. The useful output is the verdict,
the reason, the referenced records, and a concise explanation. If we need deeper
analysis for debugging, that should be a separate trace/evaluation mode, not the
production verdict.

## Training and evaluation

There is no real Guardian training yet. There is prompting, a NOTA parse retry,
and a live model. That is not bad; it is just not training.

I would not start with fine-tuning. The Guardian does not need creativity. It
needs consistency, recall against relevant records, and stable classification.
The first training-like artifact should be an evaluation corpus.

The evaluation corpus should be real files, not inline Rust strings:

- candidate proposal;
- existing record bundle;
- expected verdict;
- expected reason;
- expected referenced records;
- notes on why the case matters.

The first cases should cover:

- clean new proposal;
- exact duplicate;
- paraphrase duplicate;
- contradiction;
- non-intent task instruction;
- compound record;
- unclear privacy;
- unclear domain;
- clarify that genuinely preserves meaning;
- clarify that tramples meaning;
- clarify that loses an important aspect;
- supersede with correct target;
- supersede that misses another conflicting target;
- missing target;
- same referent across different domains;
- same domain across different referents.

Then run layers:

1. deterministic unit tests over retrieval and prompt construction;
2. fixture-provider tests for typed parse and fail-closed behavior;
3. local Gemma eval in a sandbox against the corpus;
4. regression dashboard over accept/reject/reason accuracy;
5. only after the corpus is stable, consider prompt tuning or fine-tuning.

Fine-tuning before this corpus exists would hide design uncertainty inside model
weights. The better design move is to make the Guardian's cases visible and
repeatable first.

## Full design flow I would aim for

The mature flow should be:

1. Client submits `Propose`, `Clarify`, or `Supersede`.
2. Signal admission checks structural validity.
3. Nexus builds a typed `GuardianRequest` from the operation, candidate entry,
   targets, database marker, and retrieval policy.
4. Store retrieval gathers records by domain, referent, keyword, full text, and
   operation-specific target neighborhood.
5. Retrieval ranks and caps the bundle, preserving "more records available" as
   a typed fact so the Guardian can say retrieval was insufficient.
6. Spirit leases a component-specific Guardian harness from the agent daemon.
7. Spirit sends the request directly to the harness over the leased channel.
8. The harness renders the prompt from a versioned template and schema-generated
   verdict grammar.
9. The harness calls the model, type-checks the exact verdict, retries with exact
   type errors if needed, and returns typed verdict.
10. Spirit admits or rejects.
11. On admit, Store mutates durable state and emits the corresponding event.
12. On reject, the caller gets a typed refusal and no state change.
13. Lease accounting closes with token usage and outcome.

This is bigger than the current implementation, but the shape is clean. The
agent daemon stays on the control path; the component-specific harness owns the
payload and prompt; Spirit owns durable state.

## Biggest design risks

The first risk is a false sense of safety. A fail-closed prompt around `Propose`
is safer than no prompt, but it is not a store-wide invariant.

The second risk is retrieval theater. If the bundle is wrong, the Guardian is
performing judgment on a partial world. Domain plus referent plus text is the
minimum credible substrate.

The third risk is prompt drift. A hand-written prompt string can drift from the
schema. The verdict grammar and reason list should be generated or at least
checked against generated types.

The fourth risk is conflating the `agent` API-call component with the future
harness. The current `agent` component is good at what it is. It is not the
component-specific Guardian process described in 578.

The fifth risk is over-training too early. Until the test corpus and operation
semantics are stable, training makes the system less inspectable, not more
reliable.

## What I would do next

First, fix reach: every user-facing durable capture must use the guarded path, or
the raw paths must be explicitly owner/maintenance-only. In particular,
`Clarify` and `Supersede` need Guardian paths because their correctness depends
on semantic judgment.

Second, fix retrieval: use domain, referent, keyword, and full text as a union of
evidence, then rank and cap. This should happen before prompt tuning.

Third, harden the prompt and parser loop: deterministic temperature, schema-derived
reason list, type-aware retry, operation-specific rubric.

Fourth, create the Guardian evaluation corpus as files and run it against local
Gemma. That is the real beginning of Guardian training.

Fifth, only after the above is stable, build the lease/harness architecture. The
current direct `agent` call is fine as a v1 proving path; it should not become the
permanent abstraction by accident.

## Bottom line

The Guardian design is directionally beautiful: typed daemon gate, model as
semantic judge, fail-closed verdict, clean state/stream split. The implementation
has the first vertical slice, and it is useful.

But the essence of a Guardian is not "an LLM was asked before one command." The
essence is "no ordinary durable intent mutation can enter the live store without
semantic admission against the relevant world." The current system is not there
yet. The shortest path there is not a smarter model; it is better write coverage,
better retrieval, a stricter prompt contract, and a visible evaluation corpus.
