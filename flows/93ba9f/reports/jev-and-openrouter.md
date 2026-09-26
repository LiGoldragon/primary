# Jev and OpenRouter

Research for the living's request to integrate "Jev, the new AI model" (heard
as "Jev"/"Jeff") into a design where Ethos types / datom text are translated
to JSON for a model, with an eye toward future models trained directly on
datom/Ethos.

## 1. Identifying the model

The transcription "Jev" (or "Jeff") matches a real, very recently released
model called **Jev**, made by a startup called **TypeSafe AI** (also styled
TypeSafe). Confidence: **high**. It fits every detail in the ask:

- Released **2026** (early access 2026-09-15; "Jev 1.13" listed on OpenRouter
  2026-09-18; a companion "Jev Router" 2026-09-25 — i.e. released *this
  week*, which lines up with the living hearing about it now).
- It is explicitly a **structured/schema-constrained** model — not a
  general text generator. That is almost certainly why the living connected
  it to "our own specified language ... translated to JSON."
- It is available on **OpenRouter**.

Other candidates considered and set aside:
- **JEPA** (Meta's Joint Embedding Predictive Architecture family) — an
  architecture concept, not a single released product with an OpenRouter
  listing; doesn't match "recently released 2026 model" as well as Jev does.
- Nothing else matching "Gev"/"Jeph"/"Jevv" turned up as a distinct 2026
  model in search results.

Given how cleanly "Jev" matches (name, timing, structured-output framing,
OpenRouter presence), I'm confident this is the model the living means, but
the name is STT-derived and TypeSafe AI is a very new company (surfaced from
stealth the same day, with a $40M seed round led by DCVC), so independent
confirmation with the living before deep integration work is still
warranted.

## 2. What Jev is

- **Maker:** TypeSafe AI (announced from stealth 2026-09-15 alongside Jev).
- **Category:** TypeSafe calls it a **"System One" model** — not a
  replacement for LLMs, but a fast, narrow layer for the many small
  structured decisions around an LLM-based system: classification, routing,
  filtering, safety checks, evaluation, tool-call arguments — cases where
  the *shape* of the answer is known in advance and only the *value* is in
  question.
- **How it works:** instead of generating text token-by-token, Jev takes a
  block of **state** (a string or a JSON object/array) plus one or more
  **typed questions**, and answers all of them in a single parallel pass,
  returning typed values with calibrated probabilities — never prose, and
  (per TypeSafe's marketing) never an invalid or "hallucinated" value,
  because the output space is closed by construction.
- **Question types (the only three shapes it can return):**
  - `choice` — pick one of a fixed list of options; returns the pick plus a
    probability per option and a confidence value.
  - `score` — a rating on an ordered scale (0–10 max); returns a
    probability-weighted score, per-level probabilities, and a legend.
  - `noul` — a yes/no proposition; returns a single probability.
- **Grammar/schema support:** **No custom grammars or JSON Schemas.** Every
  Jev response is one of exactly the three typed shapes above — there is no
  way to hand it an arbitrary schema (e.g. a datom grammar) and have it
  natively emit that shape. This is the single most important fact for
  bridging design (see §3).
- **Input limits:** text/JSON only — no images, audio, or video. Single
  round-trip only (no multi-step reasoning, no chain-of-thought, no
  rationale returned).
- **Context window:** 32,000 tokens.
- **Pricing:** $0.042 per million input tokens; output is free (there is
  effectively no generated text to bill for). Latency is reported as
  70–500ms per call.
- **Benchmarks claimed:** TypeSafe/OpenRouter marketing claims it matches
  top models (e.g. "GPT-6 Astra") on decision-style benchmarks like DeepSWE
  routing tasks, at a fraction of the cost/latency — take this with the
  usual grain of salt for a launch-week press claim from a brand-new vendor.
- **On OpenRouter:** yes.
  - Model id: `typesafe/jev-1.13` (also aliased `typesafe/jev-latest`).
  - A second, separate listing exists: `typesafe/jev-router` — described as
    a routing-oriented variant, reachable through OpenRouter's normal Chat
    Completions API (unlike Jev 1.13, which uses a dedicated endpoint — see
    below). Its pricing/context page did not yield further specifics in
    this pass.
  - **Jev 1.13 is not called through the normal `/chat/completions`
    endpoint.** It has its own dedicated OpenRouter route:
    `POST https://openrouter.ai/api/alpha/decisions` (note: `alpha` — this
    is an early, possibly-unstable API surface), authenticated the same way
    as any OpenRouter call (`Authorization: Bearer $OPENROUTER_API_KEY`).
    An OpenRouter TypeScript SDK also exposes it as
    `openrouter.alpha.decisions.create(...)`. TypeSafe's own JS/Python SDKs
    can also be pointed at `https://openrouter.ai/api` with an OpenRouter
    key.

## 3. Bridging to our language (Ethos / datom)

Short answer: **translation is required in both directions; Jev cannot be
handed an Ethos/datom grammar and made to emit it directly.**

- Jev's output space is closed to exactly `choice` / `score` / `noul`. It
  cannot be configured with a custom JSON Schema, BNF/EBNF grammar, or any
  other user-defined structure — so a plan of "give it the datom grammar and
  let it emit datom" is not supported by this model. This is a deliberate
  design choice (TypeSafe's pitch is that closing the output space to three
  primitives is *why* it can't produce invalid output), not a missing
  feature that a config flag would unlock.
- The practical integration shape is therefore:
  1. **Ethos → JSON (state):** serialize the relevant datom/Ethos-typed
     content into a plain string or JSON object/array to hand Jev as
     `state`. This is compatible with the project's existing idea of
     "translate Ethos types to JSON for the model" — Jev is consistent with
     that half of the plan.
  2. **Decision → Ethos/datom (back-translation):** frame whatever judgment
     is needed as one or more `choice`/`score`/`noul` questions whose
     *option sets* are drawn from Ethos types (e.g. a Choice question whose
     options are the variants of an Ethos sum type, a Noul question for a
     boolean-shaped Ethos field, a Score question for a bounded numeric
     field). The typed answer + probabilities Jev returns would then need a
     small adapter to reconstitute the corresponding datom fragment — Jev
     itself never sees or emits datom syntax.
  3. Anything requiring free-form structured output beyond these three
     shapes (e.g. emitting a full nested datom tree, or arbitrary novel
     Ethos records) is out of scope for Jev and would need a conventional
     LLM with JSON-Schema-constrained or tool-call output instead (this is
     what most large frontier models, including Claude and GPT-family
     models, already support natively via `response_format`/schema or tool
     definitions — worth keeping as the fallback path for anything richer
     than a closed-set decision).
- On "future models trained on datom/Ethos": Jev's approach (fixed
  primitive output shapes with calibrated probabilities) is a reasonable
  reference architecture to study if the goal is eventually training a
  small, fast, non-hallucinating decision layer *over* Ethos-typed data —
  but Jev itself is a fixed third-party product, not something we can train
  or extend with a custom grammar.

## 4. Setting up OpenRouter

This section is for the living to carry out directly — no API key should
ever be pasted into a chat with an AI agent, logged, or stored in plain
text in the repo.

### Sign up

1. Go to **https://openrouter.ai/** and click "Sign in" / "Sign up."
2. Sign up with email, Google, or GitHub. No credit card is required just
   to create an account — new accounts reportedly start with a small
   ($1-ish) free credit balance, and OpenRouter's `:free`-suffixed models
   are usable with a $0 balance for initial testing (Jev is not free, so
   real credits are needed to call it).

### Add credits

1. In the dashboard sidebar, open **Credits**.
2. Click **Add Credits**. $5–$10 is a reasonable starting amount (this is
   far more than needed for Jev given its $0.042/M-input-token pricing and
   free output — a few dollars would cover a very large number of calls).
3. Optionally turn on **Auto Top-Up** so a low balance doesn't interrupt a
   running integration.

### Create an API key

1. In the sidebar, open **API Keys**.
2. Click **+ New Key**, name it something identifiable (e.g. `criomos-jev`).
3. OpenRouter shows the full key **once**. Copy it immediately.

### Store the key — never in chat, never in plain text in the repo

Store it in gopass right away, from a terminal, without it ever touching
chat history, shell history with the value inline, or a log:

```
gopass insert openrouter/api-key
```

(gopass will prompt interactively for the secret value — paste it there,
not into any chat window or command argument.)

To use it later, pipe it directly into the consuming program's own
supported stdin/argument interface rather than expanding it with command
substitution into a visible argv or env line, e.g. for a one-off curl test
via a config file read from stdin:

```
{ printf 'header = "Authorization: Bearer '; gopass show -o openrouter/api-key; printf '"\n'; } | curl -K - https://openrouter.ai/api/alpha/decisions ...
```

or, for tools that natively support reading a bearer token from a file
(many HTTP clients and SDKs do via an `_FILE`/`--header-file`-style option),
prefer that native file/stdin interface over environment-variable
interpolation. The point is the same either way: the secret should flow
straight from gopass into the consumer, never sitting in a chat message,
a shell history line, or a script literal.

### Minimal example call to Jev

Once the key is in gopass, a smoke-test call (run locally by the living,
not pasted anywhere with the real key inline) looks like this in shape —
using `typesafe/jev-1.13` on the dedicated decisions endpoint:

```bash
gopass show -o openrouter/api-key | curl -sS https://openrouter.ai/api/alpha/decisions \
  -H "Authorization: Bearer $(cat -)" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "typesafe/jev-1.13",
    "state": "The customer says: \"My invoice for last month looks wrong, can you check it?\"",
    "questions": {
      "category": {
        "type": "choice",
        "instructions": "Route this message to the right team.",
        "criteria": {
          "options": ["billing", "technical", "account"]
        }
      },
      "is_urgent": {
        "type": "noul",
        "instructions": "Does this message need a same-day response?"
      }
    }
  }'
```

(The `$(cat -)` pattern above is illustrative of feeding the key through a
pipe rather than an inline literal; on a system where `curl` doesn't
support that composition cleanly, use whatever templating the calling
script/SDK offers for reading a bearer token from a file or stdin, and keep
the raw key out of argv entirely.)

A response, per TypeSafe's documented shape, would return a typed choice
(`billing`/`technical`/`account`) with a probability per option and a
confidence value, plus a probability for the `is_urgent` proposition — no
generated prose, nothing to parse.

## Sources

- [Jev (AI model) — Wikipedia](https://en.wikipedia.org/wiki/Jev_(AI_model))
- [What is Jev? TypeSafe AI's System One decision model — Sanity](https://www.sanity.io/glossary/jev-typesafe-ai-model)
- [Jev: TypeSafe's System One Model That Never Hallucinates — DataCamp](https://www.datacamp.com/blog/system-one-models-jev)
- [Jev means structured output is interesting again — Sean Goedecke](https://www.seangoedecke.com/jev-means-structured-output-is-interesting-again/)
- [Jev by TypeSafe AI: 200x Faster Structured-Output Model (2026) — explainx.ai](https://explainx.ai/blog/typesafe-ai-jev-system-one-models-launch-2026)
- [Jev vs. LLMs: When AI Moves from Generation to Decision-Making — Towards Data Science](https://towardsdatascience.com/jev-vs-llms-when-ai-moves-from-generation-to-decision-making/)
- [Jev 1.13 — API Pricing & Providers — OpenRouter](https://openrouter.ai/typesafe/jev-1.13)
- [Jev Router — API Pricing & Providers — OpenRouter](https://openrouter.ai/typesafe/jev-router)
- [Typesafe API and Models — OpenRouter](https://openrouter.ai/typesafe)
- [What Is Jev? TypeSafe's Decision Model Explained for Developers — OpenRouter blog](https://openrouter.ai/blog/insights/what-is-jev/)
- [OpenRouter announcement thread on X](https://x.com/OpenRouter/status/2100744709589316009)
- [How to Get an OpenRouter API Key — Puter developer docs](https://developer.puter.com/tutorials/how-to-get-openrouter-api-key/)
- [How to Get an OpenRouter API Key (and Add Credits) — SheetXAI](https://www.sheetxai.com/help/how-to-get-an-openrouter-api-key-and-add-credits)
- [OpenRouter Top-Up & Usage Guide (2026) — CodePick](https://codepick.dev/en/guides/openrouter-guide/)

## Confidence notes

- Model identity (Jev / TypeSafe AI): **high confidence** — name, release
  week, structured-output framing, and OpenRouter listing all line up
  tightly with the living's description.
- Specific numeric claims (pricing, latency, benchmark comparisons): drawn
  from launch-week marketing and secondary write-ups about a brand-new
  vendor; treat as **directionally reliable, not verified against a primary
  spec sheet**. Worth re-checking OpenRouter's live pricing page before
  committing budget.
- The "no custom grammar" conclusion in §3 is stated consistently across
  multiple independent sources (OpenRouter's own blog post is explicit:
  "Every Jev response is one of the three typed shapes... no flexibility
  beyond these primitives") — **high confidence**.
