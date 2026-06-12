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
Honest read: once the importance confound was fixed and empty-testimony made
deterministic (below), Flash and Pro both score 12/13 on this small suite, so the
gap narrowed; Pro keeps the edge on the hardest reasoning case (`overclaim-maximum`)
and on raw semantic robustness, matches the psyche's explicit lean for a
well-trained judge, and the 3x cost is immaterial at guardian traffic volume. A
larger eval + the decision-journal flywheel would sharpen the choice further.

### The eval drove a third fix: empty testimony is now deterministic

Run 2 exposed that **even Pro intermittently admits a quote-less record** (it
rejected the empty-testimony case in run 1, admitted it in run 2, at temperature
0) — the model overlooks an empty `[]` testimony vector. That is the single most
important safety gate (no quote-less records), so it is now a **deterministic
code-level pre-check**: `AgentGuardian::guard` rejects `MissingTestimony` before
the model call when `GuardianOperation::testimony_is_empty()`. This matches the
guardian's own charter — "code validates structure, the model judges semantics"
— and makes the gate 100% reliable. The model still judges the *semantic*
bare-affirmation-without-antecedent case.

### Prompt design independently validated

A 12-agent research-and-authoring workflow (NOTA/structured-output literature,
DeepSeek reasoning docs, per-operation example generation) converged on exactly
the prompt this session hand-built: frozen-prefix/volatile-tail ordering,
grammar-by-example with the closed reason set shown concretely, over-specifying
the double-nest with labeled WRONG forms, a separate referent verdict namespace,
respond-with-only-the-value, certainty-as-burden on modal strength, orthogonal
axes, the destructive-op psyche-authorization gate, paired look-alike-reason
discriminators, and parse-and-retry-as-outer-frame failing closed. Its broader
example bank is on file for the next few-shot expansion/ablation.

## Deploy

All three contract repos and the home config landed on `main`, validated, and
activated:

| Repo | main | What |
|---|---|---|
| signal-agent | `33c2ecac` (0.3.0) | ReasoningEffort / ThinkingMode on PromptOptions |
| agent | `5a2cd5ab` (0.2.0) | reasoning_effort + thinking in the chat-completions body |
| spirit | `a2ba6ee6` (0.11.0) | typed justification, burden judge, multi-supersede, journal v2 |
| CriomOS-home | `fa765d0e` | pins bumped; guardian → deepseek-v4-pro, 180s timeout |

Validation before activation: `cargo build` + the non-live suite (process_boundary
12/12, generated_signal_plane 23/23, runtime_triad, observer_tap, meta_configure,
collect_removal_candidates, operator_271, instrumentation) all green; `cargo
clippy --all-targets --features agent-guardian` clean; `nix build .#default` green
(all six bins at 0.11.0); the flash-vs-pro live eval. Deploy by
`lojix-run '(HomeOnly goldragon ouranos li [...] [github:LiGoldragon/CriomOS-home/main] Activate ...)'`.

A deploy-safety fix was needed: the stored `GuardianOperation` embeds the new
typed `Justification`, so the live `spirit.guardian.sema` (old rkyv layout) would
have broken the new daemon. The journal filename now carries its schema version
(`spirit.guardian.v2.sema`), so the daemon opens a fresh transitional journal
rather than reading incompatible bytes. The main intent store is untouched (the
stored `Entry` is unchanged), so the daemon self-resumes the live corpus.

### Live verification (post-activation)

- `spirit Version` → **`0.11.0`**; `spirit-daemon` + `agent-daemon` both active.
- Empty-testimony capture → **`(GuardianRejected (MissingTestimony …))`** — the
  deterministic structural gate fires live (no DeepSeek call, no corpus residue).
- A deliberately over-claimed capture (Maximum certainty on a deeply-hedged quote)
  through the live **Pro** guardian → **`(GuardianRejected (InsufficientWarrant …))`**
  — a correct reject: a quote that does not license the claim at all fails the
  warrant gate (Gate 4) before the magnitude gate; a quote that licenses the claim
  but at a lower rung trips `Overstated` (Gate 7). The verdict (reject) is robust;
  the exact reason atom on hedged-over-claims is the kind of precision the
  decision-journal flywheel and few-shot expansion will sharpen.
- `spirit.guardian.v2.sema` created fresh and recording; the old 21 MB journal is
  untouched. The version fix works.

## Adversarial review caught a real data-loss bug (fixed in 0.11.1)

A 6-agent adversarial review of the diff earned its keep: it found a **critical
data-loss bug** on the supersede path. `Store::supersede` archived and removed the
entire retired set *before* proposing the replacements, with no transaction — so a
propose failure mid-operation (identifier-mint exhaustion, rkyv encode, IO) would
permanently destroy the retired intent records while replacing nothing. Verified
in source against sema-engine (each assert/retract is its own committed write).

Fixed in **0.11.1**: snapshot the targets, **propose every replacement first**,
then archive + remove — so a failure leaves the retired records intact and the
caller can safely retry. (A single `WriteTransaction` spanning the whole supersede
is the eventual end state; propose-first is the mandatory fix that converts data
loss into a safe retryable failure.) Folded into the same patch: the
`IntentSuperseded` event no longer drops the whole retirement notification on one
missing lookup; `GuardianVerdict::Accept` renders a **bare** atom, so the few-shot
now teaches bare `Accept` matching the wire form (pinned by a new verdict-grammar
regression test); and Gate 4 (warrant) is tightened so a hedged-but-on-point quote
is judged for over-claim at Gate 7 rather than pre-empted as `InsufficientWarrant`
(the exact drift seen in the live smoke test).

The review's other HIGH flag — an empty-replacements Supersede as a silent
mass-delete — was a **non-issue**: `Supersession::validate()` (wired at admission,
engine.rs) already rejects empty replacements before any store mutation; the
reviewer read store/guardian but not the validator. The remaining LOW findings
(orphaned old journal file, referent-side testimony asymmetry, DeepSeek-external
API assertions) are documented non-issues or deliberate design choices.

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
