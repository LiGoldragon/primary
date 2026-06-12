# Intent-justification guardian — built, schema-first (designer)

The court-of-law intent gate (designs 604/605, lean spec 607, prompt spec 608)
is now **implemented on `main` across three repos**, not just specified. This
report is the build record and the hand-back: what landed, how it is wired, the
flash-vs-pro eval, the deploy, and the open seams. Psyche directive this session:
carte blanche — implement every blocker and the rest, schema-driven, typed (no
"bullshit types"), most-modern deps, deploy latest first, super-train and test
the Pro guardian, extract repetition toward the schema macro.

Ratified intent this session: [No stringly-typed types — value enums break a
field into its possibilities and still carry their data] (Spirit `jh0r`); [The
schema creates the data types and they must be used in the logic flow, not
ignored] (`n5p2`); [Extract repetition into the schema macro; the more the schema
generates the better] (`xprx`). These sit beside the standing court-of-law
records (`z3ka`, `woku`, `so3b`, `u62s`, `ans1`, `2t89`, `4jgt`, `88mw`, `gad7`,
`bwqe`, `i59i`).

## What landed

### 1. Typed Justification — the stringly blob is gone (`signal.schema`)

`Justification { StatementText, context }` (two free strings) became the typed
court record:

```
QuoteText     String
Antecedent    String
VerbatimQuote { QuoteText * antecedent (Optional Antecedent) }
Testimony     (Vec VerbatimQuote)
Reasoning     String
Justification { Testimony * Reasoning * }
```

Testimony is the evidence (raw psyche words, no stored asterisks); a bare
affirmation carries its `Antecedent`; Reasoning is the one argued-case prose
field (lean Phase-1; typed warrant sub-sections stay Phase-2). The claim is the
operation's `Entry`, never a justification sub-field (operator 375 #1). All seven
gated operations pick up the new type through the schema — no per-call-site
re-declaration. The generated codec round-trips it; the bracket-bearing wire test
now asserts the `([(quote None)] reasoning)` shape.

### 2. The five reason atoms (`GuardianRejectionReason`)

`MissingTestimony`, `TestimonyFabricated`, `InsufficientWarrant`, `Overstated`,
`ImportanceUnsupported` joined the enum (the BLOCKER from 608). The
burden-of-proof design is now nameable. The guardian prompt renders the **closed
reason set and the `(Accept)` / `(Reject (<Reason> [..]))` grammar straight from
the enum via `NotaEncode`**, so the prompt can never drift from the wire type the
daemon parses (`4jgt`). `GuardianRejectionReason::admission_gloss` is an
exhaustive match — a new variant will not compile until it is glossed.

### 3. Multi-replacement Supersede — correctness (`gad7`)

`Supersession` now carries `Replacements (Vec Entry)` (was one `replacement
Entry`); `SupersessionReceipt`/`IntentSuperseded` carry `RecordIdentifiers`. The
store retires the target set and proposes every replacement in one atomic verdict;
the guardian judges whether the replacement set *together* preserves the retired
kernel, rejecting a collapse-to-one as `ClarifyLosesMeaning`. "Replace X and Y
with these" needs no new verb — it is this `Supersede`.

### 4. Typed reasoning controls in the agent contract (signal-agent + agent)

Per operator 373 #1, the guardian no longer relies on a provider default for
thinking. signal-agent (`0.2.0 -> 0.3.0`) gained value enums `ReasoningEffort
[Low Medium High]` and `ThinkingMode [Enabled Disabled]` on `PromptOptions`; the
agent provider (`0.1.0 -> 0.2.0`) sends them as the OpenAI-compatible
`reasoning_effort` string and the DeepSeek top-level `thinking {type}` object,
omitted when unset. The guardian asks for **thinking enabled, high effort** —
which also improves exact-format adherence (the research finding). Both landed on
`main` (signal-agent `33c2ecac`, agent `5a2cd5ab`).

### 5. The over-trained guardian prompt (`guardian_prompt.rs`, rewritten)

A specialized clean-context judge (`2t89`), temperature 0, with:

- the **9-gate directed checklist** (Gate 0 retrieval-sufficiency through Gate 8
  cross-record collision; first unmet gate wins; one reason);
- the **ordinal burden ladder** — certainty read off the *quote's* modality, never
  the agent's prose; importance judged independently from recurrence/blast-radius;
- the **NOTA output law** + verdict grammar rendered from the type;
- a closed reason catalogue rendered from the enum with one-line glosses;
- an **over-trained few-shot** of contrastive pairs (the burden pair — same quote
  at Low accept vs High reject `Overstated`; orthogonal axes; testimony
  production; deictic affirmation with/without antecedent; sharpen-vs-trample;
  multi-replacement preservation; destructive psyche-authorization), each ending
  in exact NOTA;
- parse-and-retry with a type-aware correction turn.

### 6. Flash-vs-Pro eval harness (`tests/guardian_live_scenarios.rs`)

A measurement harness (not pass/fail) runs 13 discriminating cases — 4 contrastive
pairs — through the **real new stack** (in-process new agent engine + reasoning
controls + real DeepSeek) against both models, printing a per-model scorecard of
exact-verdict and exact-reason agreement. It is the empirical basis for the
production model and for few-shot ablation.

## Eval result (flash vs pro) — Pro wins, and the data tuned the prompt

13 discriminating cases (4 contrastive pairs) through the real new stack against
both models, exact verdict + exact reason vs gold:

| Run | Model | Verdict | Reason | Notable |
|---|---|---|---|---|
| 1 | flash | 11/13 | 7/9 | admitted empty testimony; importance confound |
| 1 | **pro** | **12/13** | **8/9** | caught empty testimony; one format slip (`HarnessMalformed`) |
| 2 | flash | 12/13 | — | only miss: still admits empty testimony |
| 2 | **pro** | **(clean)** | — | importance fix + 2nd retry applied |

Two findings drove fixes, both landed:

- **Pro catches what Flash misses.** On the empty-testimony case Flash *admitted*
  the write (no quote at all) while Pro correctly rejected `MissingTestimony`;
  Pro also got `overclaim-maximum` as `Overstated` where Flash did not. This is
  the operator-373 thesis confirmed on the real admission cases — and the safety
  argument for Pro: a guardian that admits quote-less records corrupts the layer.
- **Run 1 exposed two of my own faults, now fixed.** (a) An importance confound:
  the guardian rejected ordinary `Medium`-importance records for "unsupported
  importance"; the prompt now states Minimum/Low/Medium are ordinary defaults and
  only an *elevated* rung needs recurrence/blast-radius evidence (matches
  `intent-log.md` "Minimum is the default"). Run 2 confirmed `firm-high` and
  `overclaim-maximum` flipped to correct. (b) Pro's lone `HarnessMalformed` was a
  double-nest format slip that failed *closed* into a spurious reject; the
  guardian now does **two** format-correction retries (was one), each feeding back
  the malformed text and the parse error.

**Production model: `deepseek-v4-pro`, thinking enabled, reasoning effort high.**
The eval is the repeatable basis for future ablation of the few-shot.

## Deploy

spirit bumped, built, `cargo test` + `clippy -D warnings` + `nix build` green,
pushed `main`; CriomOS-home pins bumped (agent `5a2cd5ab`, spirit new) and the
guardian model set per the eval; `lojix-run` activation; live version + corpus
verified. (Status recorded at deploy time.)

## Schema-macro extraction (the `xprx` direction) — scoped, not yet done

The repeated shape worth pushing into the emitter: the **verdict-type triad**
(`GuardianVerdict [Accept (Reject)]` + `Reject { Reason * Explanation * }` + the
`from_harness_rejection` / `reject` constructors + the closed-set-into-prompt
rendering) recurs once per guardian and again per referent-guardian, and would
recur for any future admission gate. Emitting "a binary verdict over a closed
reason enum, with its NOTA grammar and harness-fallback constructors" from
`schema-rust-next` is the clean win. It is a separate-repo emitter change with
real blast radius; this session rendered the grammar *from* the enum in-repo (the
correctness half) and leaves the emitter extraction as the next concrete step.

## Open seams (engineer these next)

- **Retrieval completeness is the shakiest foundation.** Operator's b9cf532 sends
  a relevance-ranked, capped bundle and inserts named targets, so duplicates
  (always share domain) and target-soundness are judgeable. A *differently-worded*
  contradiction in another domain can still be missed — the guardian only catches
  what it is shown. `RetrievalInsufficient` is a correctness gate; making
  retrieval provably complete is upstream of the prompt.
- **Replayable decision journal (operator 375 #4) — partially deferred.** The
  journal stores operation + bundle + verdict + marker; it does not yet store raw
  model output, parse/retry status, provider/model/prompt-version. That is the
  training-flywheel substrate and the next addition.
- **TestimonyFabricated is heuristic-only** until verbatim authentication exists
  (needs the full-stack capture/UI rewrite — out of reach now).
- **Few-shot ablation pending real eval volume** — over-trained now; trim only
  when removing a pair regresses neither verdict nor reason match.

## Files

spirit: `schema/signal.schema`, `src/{engine,nexus,store,daemon,guardian_journal,
guardian_prompt}.rs`, `tests/*` (typed justification + multi-supersede + eval).
signal-agent: `schema/lib.schema`, regenerated. agent: `src/{provider,registry}.rs`.
CriomOS-home: `modules/home/profiles/min/spirit.nix`, `flake.lock`.
