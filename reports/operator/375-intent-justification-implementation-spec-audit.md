# Audit of designer 605 — intent justification implementation spec

## Gate outcome

No new operator Spirit capture. The prompt asked for an audit of designer's updated implementation spec, and designer already captured the two cited records. I verified `so3b` and `ans1` exist. The audit does find one mismatch in `ans1`; that needs correction before implementation, but I am not unilaterally rewriting designer's capture from a forwarded handoff.

## Verdict

605 is a strong implementation spec and is mostly ready to hand to operator. It incorporates the important corrections from operator feedback 374: no citation-signal enum, no `Distinguish` verb, no duplicate claim field in the report body, explicit heuristic-only testimony fabrication, binary guardian, and no hand-rolled NOTA parsing.

I would not implement until the findings below are resolved. Most are small spec edits, but two are load-bearing: quote marker storage and the `ans1` intent mismatch.

## Findings

### 1. High — `ans1` conflicts with 605 on whether `Claim` is a justification slot

The live Spirit record `ans1` says the upgraded justification has named sub-fields including "claim". Report 605 correctly says the claim is the proposed `Entry` already carried by the operation and `Justification` does not re-declare it.

That mismatch matters because the intent layer outranks the report. A future agent querying Spirit could reasonably add a `Claim` field even though the implementation spec says not to.

Recommendation: correct or supersede the `ans1` wording so it says the claim is the operation's `Entry`, not a `Justification` sub-field. The implementation should follow 605's report body: one stored `Entry`, one argued case for it.

### 2. High — `QuoteText` should not store literal asterisk delimiters

605 says `QuoteText` is the psyche's exact words with `*asterisks*` preserved, and the guardian checklist asks for at least one `*verbatim*` quote. Once `VerbatimQuote` is a typed record, the vector element is already the structure. Literal asterisks become presentation markers, not data.

If the daemon stores asterisks in `QuoteText`, agents will start treating a prompt-rendering convention as part of the source utterance. That creates exactly the subtle parsing surface 605 is trying to avoid: the guardian may judge marker presence rather than typed testimony presence, and later authentication will have to strip local markup before comparing against source text.

Recommendation: store raw psyche wording in `QuoteText` without delimiter markers. The guardian prompt renderer wraps or labels each typed quote as testimony when composing the prompt. The daemon validates "has testimony" by `Testimony` vector length, not by scanning for `*`.

### 3. High — the rejection reason set is still too overloaded

605 adds `TestimonyFabricated` and `Overstated`, but the checklist still says missing testimony rejects as `RetrievalInsufficient` / `NonIntent`. That overloads existing reasons:

- `RetrievalInsufficient` is about the live-record bundle being too thin to judge duplicate/contradiction/target-sensitive operations.
- `NonIntent` is about the candidate not being durable intent.
- Missing testimony is an evidentiary production failure.

Recommendation: add exact rejection reasons before prompt work:

- `MissingTestimony`
- `InsufficientWarrant`
- `Overstated`
- `TestimonyFabricated`
- `ImportanceUnsupported`

Then generate the reason list into the prompt and test that no free-text reason is accepted. This gives agents repairable denials instead of generic refusal.

### 4. High — the decision journal tuple is too thin for the training flywheel

605 says `src/store.rs` should store `(testimony, context, verdict, reason)` tuples as precedent. That is not enough to train or audit Guardian decisions.

At minimum the separate decision journal needs:

- proposed operation and proposed `Entry`
- full typed `Justification`, including warrant and stakes basis
- retrieved live-record bundle or stable references to reconstruct it
- verdict, reason, explanation, raw model output, parse/retry status
- provider, model, prompt version, and cache/usage metadata when available
- later override/correction, if any

Without the candidate entry and bundle, the journal cannot reproduce why a duplicate, contradiction, overstatement, or operation-soundness rejection happened. Without raw verdict and prompt version, malformed-output and prompt-regression audits lose the evidence.

Recommendation: keep the journal separate from the live store, but make the record complete enough to replay the case.

### 5. Medium — `Warrant` as one `StatementText` may be understructured

605 wants the Warrant to map testimony to each judged field, but schemas it as one `StatementText`. That can work if the design deliberately wants shallow typing, but it means the daemon cannot know whether the agent supplied a domain warrant, certainty warrant, privacy warrant, or operation warrant. The guardian has to infer missing sections from prose.

This is not necessarily wrong; the psyche previously worried about inline declarations going too deep. But if the desired failure mode is "reject because the certainty mapping is missing," typed sections would make the failure clearer.

Recommendation: either keep one Warrant text and add hard few-shot tests for missing field mappings, or split `Warrant` into typed prose slots: domain, kind, certainty, privacy, optional referents, and optional operation. `StakesBasis` is already separated correctly.

### 6. Medium — the gated-operation list is incomplete or ambiguous

605 says the new `Justification` is used by every gated op and lists `Record`, `Propose`, `Clarify`, `Supersede`, `Retire`, `ChangeRecord`, and `RegisterReferent`. Current Spirit also has write roots such as `Remove`, `ChangeCertainty`, `BumpImportance`, and `CollectRemovalCandidates`. Some carry justifications today; some may be mechanical maintenance actions.

The spec should state the authority rule rather than only an example list: every working-socket operation that changes the live intent corpus is guardian-gated unless it is a purely mechanical consequence of an already-gated verdict. Owner-only meta `Import` remains the explicit bypass.

Recommendation: enumerate each write root and mark it `guardian-gated`, `mechanical`, or `owner-only bypass`.

### 7. Medium — "psyche record" needs an operational definition

605 says retiring a psyche record requires a verbatim psyche quote. In Spirit, ordinary records are psyche-derived by design, but there are also owner-only imports, migration records, and possible future machine-generated archive/journal records.

Recommendation: for now, treat every live intent record on the working socket as psyche-derived and require psyche quote authorization for destructive retirement/supersession. If future machine-only records enter the live store, add a typed provenance field rather than infer provenance from path or operation history.

### 8. Low — the Duke number should be labelled precisely

605 cites Duke Judicature as "50.1 / 73.4 / 90.1." The article does mention 50.1 percent as a court-referenced minimum for preponderance, but the survey mean it reports is 54.4 percent for preponderance, alongside 73.4 for clear-and-convincing and 90.1 for beyond reasonable doubt.

Recommendation: if 605 wants "survey numbers," use 54.4 / 73.4 / 90.1. If it wants the legal shorthand threshold, write "50.1 as the common legal minimum; Duke survey mean 54.4." Since the design forbids numeric gates, this is only citation hygiene.

Sources checked: Duke Judicature, "Legal Standards By The Numbers"
(`https://judicature.duke.edu/articles/legal-standards-by-the-numbers/`); arXiv 2509.15739
(`https://arxiv.org/abs/2509.15739`); arXiv 2503.00841
(`https://arxiv.org/abs/2503.00841`).

### 9. Low — the `TestimonyFabricated` live test will be probabilistic

Because source authentication is deferred, `TestimonyFabricated` is a heuristic. A live DeepSeek test with "agent-prose-shaped quote" is useful, but it may be model-sensitive and should not become the only proof that the rejection reason works.

Recommendation: pair the live scenario with a prompt/shape test that proves the reason exists, is emitted in the closed enum list, and parses correctly. Treat the semantic live test as guardian behavior coverage, not as source-authentication proof.

## What is solid

The main structure is right:

- no citation-signal enum
- no `Distinguish` write verb
- `Entry` is the claim
- typed `VerbatimQuote` with optional antecedent
- separate `StakesBasis`
- binary guardian with no downgrade remedy
- `TestimonyFabricated` explicitly heuristic-only
- no daemon-side NOTA parsing of testimony markers
- current LLM-judge evidence correctly translated into "keep the case dense"

The arXiv 2509.15739 reference supports the density constraint: it reports that performance degrades on longer inputs or disrupted discourse flow. The arXiv 2503.00841 reference supports the structured claim/evidence direction in legal reasoning. Those references are useful as design pressure, not authority over the local type shape.

## Implementation-ready version of the spec

I would hand this to operator after these edits:

1. Correct `ans1` or explicitly state that 605 supersedes the "claim sub-field" wording.
2. Change `QuoteText` wording to raw psyche text; asterisks are prompt-rendering markers.
3. Add the missing rejection reasons and remove `RetrievalInsufficient` from the no-testimony path.
4. Make the decision journal replayable.
5. Enumerate write roots by gate status.
6. Decide whether `Warrant` remains one prose field or becomes typed prose sections.

After that, the build can proceed schema-first: update `schema/signal.schema`, regenerate, adapt call sites, rewrite `guardian_prompt.rs`, and extend the live Guardian suite.
