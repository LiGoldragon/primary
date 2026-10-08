# Jev and Ethos: material for the design flow

Gathered 2026-10-08 by an Opus research subflow of Psyche Opus d4ae97. Nothing was called on Jev; no key was read. "Witnessed" means read in source or measured here today. "Claimed" means taken from a vendor page or an earlier report without re-checking.

## 1. The order, in his words

> Also I want to marry Jev System 1 and its siblings, the System 1 models, to probably a subset of the Ethos specification so it could talk to an Ethos contract. Like I said it's only a subset because it doesn't have all the types yet. Let's get that also going, where we're designing in another flow.

> Basically the guiding principle in designing the ethos and the datom payload is also keeping in mind what the datom payload looks like, considering that the datom will probably be more expensive because machines will have to output them. It's funny because System 1 models actually make that cheaper, which is interesting.

-- psyche, STT, 2026-10-08, `flows/d4ae97/vision/ethos.md`.

Earlier records on the same topic, all witnessed as files:

| Date | What he said, in short | Record |
|---|---|---|
| 2026-09-19 | "JEV, with its success, is showing that this is the way to go": every CLI takes a datom payload; Ethos is "made for high cognitive density per amount of LLM … tokenized cost" | `flows/b81560/vision/operational-flowDatomCLIAndSignalLibrary.md` |
| 2026-09-19 | Jev for "statistical decisions with data" in reaping retired flows | `flows/b81560/vision/operational-retiredResponseAndReaping.md` |
| 2026-09-24 | "Maybe Jev redefines what is actually ultra-low power" | `flows/752e0f/vision/models.md` |
| 2026-09-26 | "our own specified language that we could even translate into JSON (which is, I'm guessing, what Jev speaks)… If he doesn't understand ethos but he might actually understand ethos, then we can give him another ethos-to-something-else specification. Eventually there are going to be models like Jeff trained on Datom with ethos" | `flows/93ba9f/vision/jev.md` |
| undated | Jev to judge whether items may enter a database, merge overlapping text, write commit messages, check the system is running | `flows/aa887c/vision/jev.md` |
| 2026-10-04 | Jev "in the middle of" typed communication through Nexus; Jev calls chained, one's data feeding another's decision | `flows/bad807/notion/voices.md`, `flows/bad807/vision/jev.md` |

No record found in `vision-raw/` or `Vision/` mentions Jev or System 1 (grep over both, witnessed).

## 2. What Jev is

Detailed in `flows/d4ae97/books/jev-meat.md` and `flows/bad807/reports/jev-ecosystem.md`; the facts this design needs:

- **Jev** is TypeSafe AI's model, launched 2026-09-15; version answering now `jev-1.13` (dated 20260917). TypeSafe calls it "the first System One model" (claimed, TypeSafe models page via jev-meat).
- **It writes no text.** "No text generation, no parsing" (claimed, docs.typesafe.ai/introduction, fetched today). Given a state and typed questions, it answers each with numbers only.
- **Three question kinds, no fourth** (claimed, TypeSafe api page via jev-ecosystem; witnessed in fuzzy-jev `src/types.rs:31`):

| Kind | Asks | Criteria | Answer | Limit |
|---|---|---|---|---|
| Noul | is this true? | optional yes/no descriptions | `noul`: probability 0–1 | — |
| Choice | which option? | map option name → description (or null) | `choice` (name), `confidence`, `probabilities` per option | ≤ 255 options |
| Score | which level? | ordered list of level descriptions, lowest first | `score` (expected level, may fall between), `confidence`, `probabilities` per level, `legend` | 2–10 levels |

- **Answers are independent.** One answer never conditions another in the same request; question ids are not shown to the model (claimed, TypeSafe primitives; repeated in fuzzy-jev `types.rs` doc comment, witnessed).
- **Input** is a state (text, JSON object, or array of text) plus instructions and criteria, each of which may be a string, object or array; paths into state are named in backticks (claimed, TypeSafe api/advanced pages).
- **Numbers arrive rounded to two decimals** (witnessed: fuzzy-jev `ROUNDING = 0.005`, `types.rs`).
- **Price**: $0.042 per million input tokens; **output free** (claimed, TypeSafe and OpenRouter, via jev-meat). OpenRouter's example: 476 input tokens, 70 output tokens, $0.000019992.
- **Context**: 64k per request, 32k for state plus the longest question (claimed).
- **Known weak spots** (TypeSafe's own list, claimed): literal reading, math and counting, date comparison, indirection, large state, injection through state, contradictory criteria, **a bias toward the first Choice option**, generation.

### "System 1 models", and the siblings

- In TypeSafe's docs: "System One models are built for fast, focused judgments … a judgment a knowledgeable person makes in a second" (claimed, primitives page fetched today). The name evokes Kahneman's System 1/System 2; TypeSafe's pages fetched today do not name System 2.
- "System One API" (`POST /v1/systemone`) is becoming a shared wire format (claimed, jev-ecosystem §5). Siblings that speak it: **Cloudflare Clef / Clef-flash** (open weights, Apache-2.0, from Qwen3.8-27B, 2026-10-01), community open models (autotrust JEV-27B-VL, JEV-9B), open replicas (SemIf-OpenJev, NanoJev, kev, firelex/jeff at 0.8B), shims turning any model into a System One endpoint (AnyJev, llama-system1, jev-bridge), and OpenAI's announced Decision API on Luna. All claimed, from jev-ecosystem.
- In his records, "System 1 models" appears only in the 2026-10-08 entries above. Reading it as "Jev and the models that speak the same System One contract" is this report's inference. Open-weight siblings matter for the chartered private part (CLAUDE.md): an open-source System One seat could be self-hosted, where Jev cannot (no weights).

### fuzzy-jev 0.6.0 (the crate studied before)

Daniel Saad's unofficial Rust client for OpenRouter's `/api/alpha/decisions`; the Jev-talking part is 1,111 lines (jev-meat, witnessed then). Its contract mechanism, witnessed today in `~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/fuzzy-jev-0.6.0/src/types.rs`:

- `Question` is a serde-tagged enum `Choice | Score | Noul`; `instructions` and criteria are `serde_json::Value`.
- `Options(Vec<(String, Value)>)` keeps option order; duplicates refused; > 255 options refused; Score > 10 levels refused.
- `DecisionResponse::check_against(questions)` is its schema check: every question answered, answer of the question's own kind, every option/level given a probability, no unknown option, probabilities a distribution within rounding, the chosen option the most probable, Score's expectation possible from its probabilities.
- Unknown answer kinds are kept as `Answer::Other(Value)`.
- No derive from Rust types. Questions are built by hand, by CLI flags (`spec.rs`: `--choice 'id=Instructions|a:desc|b'`), or from a JSON/TOML questions file.

So fuzzy-jev has no schema language of its own: its "contract" is the request's question set, and the check of the reply against it.

### Prior art for "types generate the questions": jev-driver

`jev-driver` 0.1.0 (Shearerbeard, Apache-2.0, 2026-10-02) derives Jev questions from Rust types (claimed, its GitHub README, fetched today):

```rust
#[derive(JevChoice)]
#[jev(id = "department", instructions = "Which team should handle `ticket`?")]
enum Department { Billing, Technical, #[jev(option = "other")] Other }

#[derive(JevScore)]
#[jev(id = "frustration", instructions = "How frustrated does the customer appear?")]
enum Frustration { #[jev(criteria = "Calm and neutral")] Calm, #[jev(criteria = "Concerned but civil")] Concerned, #[jev(criteria = "Very angry or strong language")] Angry }

#[derive(JevNoul)]
#[jev(id = "is_urgent", instructions = "Does `ticket` convey time pressure?", yes = "Explicit deadline or costly delay", no = "No time pressure expressed")]
struct IsUrgent;

#[derive(JevQuestions)]
#[jev(state = TicketState)]
struct TicketTriage { department: Department, is_urgent: IsUrgent, frustration: Frustration }
```

The answer decodes into the same enums plus probabilities and confidence. This is close to "Ethos generating Jev's schema": unit enum → Choice or Score, marker → Noul, struct → one request.

## 3. Ethos and datom today (the other side)

Witnessed from the vision-ethos, vision-datom, knowledge-ethos skills and `/git/github.com/LiGoldragon/ethos-zero` (16.0.0, head `c2653dd`, 2026-10-03) and `datom-codec` (head `4dff16b`):

- Roots: Library, Signal, Operation (proposed), Memory. `Name.Type` alias, `Name.{ }` struct (positional, fields named after types), `Name.[ ]` enum. Inline types allowed about three deep.
- Intrinsics: String, Integer (`i64`), Decimal (`datom_codec::Decimal`, finite, point mandatory), Boolean (`bool`, datom `True`/`False`), Meaning, Vector, Option, Result, Self.
- Kinds (traits), associations, capabilities: behaviour, not data.
- **No generics** ("in ethos there are no generics, only kinds"); **no map** (vision-datom: a map is a struct or a vector of structs); **no tuple**; **no omittable fields** yet; **no documentation strings** other than `;` comments, which the vision makes mandatory on every section and on every line with a next layer.
- Variants are ordered by seniority, the first most senior (psyche, 2026-10-07, `flows/d4ae97/vision/ethos.md`).
- Datom is positional, typed from the position down; the text carries only data.

## 4. The type map

How each Ethos construct could be carried by a System One question set (output side: Jev filling a value of that type). "Carried" means Jev can decide the whole value; "partial" means it decides a part and code or another call must finish it.

| Ethos construct | System One counterpart | Status | Note |
|---|---|---|---|
| Boolean | Noul, then a threshold | carried | Threshold is caller policy, not in the type |
| Enum of unit variants, ≤ 255 | Choice; option name = variant name | carried | Descriptions needed per variant; first-option bias meets seniority order |
| Enum of unit variants, ordered, 2–10 | Score; level = variant position | carried, if order is meant | Ethos has no marker saying "this enum is a scale" |
| Enum with payload variants | Choice picks the variant; payload needs its own questions | partial | Needs a second call (answers in one call are independent) unless every payload is itself carried and asked speculatively |
| Struct of carried positions | one request, one question per position (fan-out) | carried | Positions cannot condition each other |
| Alias, new type | transparent | carried | |
| Option<T> | Noul "is it present?" + T's questions | partial | Two-step, or ask T speculatively |
| Result<T E> | Choice Ok/Err + payload | partial | As payload enums |
| Vector<T> of fixed candidates | one Noul per candidate (subset selection) | partial | Only when candidates are known before the call |
| Vector<T>, open length | — | not carried | No variable-length output |
| Integer | — (Score or Choice over a small fixed range only) | not carried | Counting and math are listed weak spots |
| Decimal | Jev's own probabilities, confidence, score are decimals | not carried as a free value | Only Jev's meta-answers are decimal |
| String | — (Choice among given strings only) | not carried | Jev does not generate |
| Meaning | — | not carried | |
| Kinds, capabilities, associations, imports | — | not applicable | Behaviour, not data |
| Signal Query / Response enums | Response enum of unit variants is a Choice | carried for unit replies | e.g. a reaping verdict `Reap` / `Keep` |

Input side: every Ethos-typed value can be sent as state, as datom text (Jev accepts text state). Whether Jev reads datom positions as well as JSON keys is **untested**; datom has no field names, so the state carries no labels unless the instructions say what each position is. Jev's listed weak spots include literal reading and indirection.

The direction this repeats, in the wire's own JSON: Jev's request and reply contain maps (`questions`, `criteria`, `probabilities`) and untyped `Value`s. Datom has neither; an Ethos description of the wire contract must turn each map into a vector of structs or into positions known from the type.

## 5. The subset

The Ethos subset a System One model can fill today: **Boolean, unit-variant enums (≤ 255; ordered ones ≤ 10 as Score), and structs, aliases and new types composed only of those**, with Option, Result and payload enums only by chaining calls. Everything with open content (String, Integer, Decimal as a value, Meaning, open Vectors) is outside it.

Said another way: a System One model fills the **discriminants** of a type, the heads in a datom, never its leaves. In datom terms it can write `{ True Payments }` but not `«12 Rue de la Paix»`.

## 6. What a bridge would need

Jev never emits datom text. So "Jev emitting datom that an Ethos schema validates" means: code receives Jev's numbers, applies the caller's thresholds, builds the Ethos-typed Rust value, and datomizes it. The model's output is numbers; the datom is written by code, at no model-output cost. That is the precise sense in which "System 1 models actually make that cheaper" holds (inference from the price table and the no-text design).

Pieces a bridge would need, either direction:

1. **Ethos → questions (generation).** For a type in the subset, ethos-zero (or a sibling generator) emits the question set: struct → request, unit enum → Choice or Score, Boolean → Noul. jev-driver's derives are the Rust-side prior art.
2. **Words for the model.** Jev needs `instructions` per question and a description per option or level. Ethos holds no such strings except comments. Source candidates: the mandatory `;` comments, a separate Library of question texts, or variant names alone (Choice accepts `null` descriptions).
3. **Scale versus choice.** Some marker or rule for when an enum is an ordered scale (Score) rather than a set (Choice). Seniority order exists but means rank, not scale.
4. **The answer type.** Ethos has no generics, so `Answer<T>` (choice + confidence + probabilities) cannot be written once. Either a per-type generated answer struct, a kind (e.g. a Decidable kind with the probabilities as an associated type), or the decision-only form (threshold applied, only the value kept).
5. **Positional probabilities.** Because the type knows its variants in order, Jev's `probabilities` map can become `Vector<Decimal>` in variant order, which datom requires (no maps).
6. **Validation.** fuzzy-jev's `check_against` already does the reply-against-question check; an Ethos bridge would add "answer composes into the Ethos type" through datom-codec's `Compositional`.
7. **Chaining.** Payload enums, Option and Result need a second call per level; the generator would plan the call sequence (his chained-calls words, `flows/bad807/vision/jev.md`).
8. **State form.** Datom as state needs either labels in the instructions or a test showing Jev reads positional datom.
9. **Thresholds and fallback.** Confidence gating is caller policy (earlier ruling in jev-meat: deciding what an answer may do stays with the caller). Where it is written (Ethos, config datom, code) is open.

## 7. Datom output cost, measured

Token counts with OpenAI's tiktoken (`o200k_base`, `cl100k_base`), run today via nix. **Claude's and Jev's own tokenizers were not measured**; OpenRouter's example reports 70 output tokens for the reply measured as 54 here, so counts differ by tokenizer and envelope.

| Sample | Chars | o200k | cl100k |
|---|---|---|---|
| Jev reply, two answers, JSON minified (`{"answers":{"is_bug":{"type":"noul","noul":0.96},"team":{…probabilities…}}}`) | 175 | 54 | 54 |
| Same content as Ethos-typed datom `{ 0.96 { Payments 0.75 [ 0.0 0.16 0.84 ] } }` | 44 | 27 | 27 |
| Decision only, JSON `{"is_bug":true,"team":"payments"}` | 33 | 10 | 10 |
| Decision only, datom `{ True Payments }` | 17 | 4 | 4 |
| Lock reply, JSON `{"Locked":{"lock_id":42,"lock_name":"primary-docs"}}` | 52 | 15 | 15 |
| Lock reply, datom `Locked.{ 42 primary-docs }` | 26 | 8 | 8 |
| Person (vision-datom example), JSON with field names | 158 | 48 | 47 |
| Person, datom | 80 | 31 | 32 |
| Jev questions (request side), JSON | 356 | 72 | 71 |
| Same questions as hypothetical datom | 295 | 66 | 71 |

Findings:
- On records, datom is about half the tokens of JSON (27 vs 54, 8 vs 15, 4 vs 10); the saving is field names and quotes.
- On the request side, where prose instructions dominate, datom saves little (66 vs 72) or nothing (71 vs 71).
- For a System One model the record side costs no model output at all (output free; code writes the datom). The request side is what is billed, at $0.042 per million input tokens: the 72-token question set costs about $0.000003.
- For a frontier text model emitting datom, output tokens are the billed side; halving them is the saving his 2026-10-08 words point at. Frontier output prices were not looked up here.

## 8. Open questions for the designer

1. Is "System 1 models" meant as Jev plus every System One-compatible model (Clef, open replicas, OpenAI Decision API), or Jev alone? Does an open-weight sibling serve the chartered private part?
2. Which direction first: Ethos generating the question set (contract → Jev), or an Ethos description of the System One wire itself (Jev's request and reply as Ethos types), or both?
3. Where do instructions and option descriptions live: Ethos comments promoted to data, a separate text Library, or variant names alone?
4. How does an enum say it is a Score scale rather than a Choice? Does seniority order double as scale order, given Jev's first-option bias?
5. Which answer form is kept in datom: decision only (`{ True Payments }`), or with confidence and positional probabilities? With no generics, is the answer type generated per type or expressed through a kind?
6. Where do thresholds live, and who owns the fallback when confidence is low?
7. Payload enums, Option, Result: chain calls, ask speculatively in one call, or exclude from the subset?
8. Is the state sent to Jev written in datom? A live test of Jev reading positional datom (versus JSON with keys) is needed before relying on it; no key access is established.
9. "It doesn't have all the types yet": does he mean Jev lacks String/Integer/Vector output (as found here), or that Ethos lacks types Jev has (none found: every Jev answer shape maps onto Ethos intrinsics once maps become positions)?
10. Does a decision type become its own root or section (as Signal has queries and responses), so ethos-zero can generate the question set the way it generates Query and Response?

## Sources

- Psyche records: `flows/d4ae97/vision/ethos.md`, `flows/93ba9f/vision/jev.md`, `flows/aa887c/vision/jev.md`, `flows/bad807/vision/jev.md`, `flows/bad807/notion/voices.md`, `flows/b81560/vision/operational-flowDatomCLIAndSignalLibrary.md`, `flows/b81560/vision/operational-retiredResponseAndReaping.md`, `flows/752e0f/vision/models.md`, `flows/e51411/notion/v2.md`.
- Earlier reports: `flows/d4ae97/books/jev-meat.md`, `flows/d4ae97/books/jev-pages-copy.md`, `flows/bad807/reports/jev-ecosystem.md`, `flows/d66c26/reports/jev-reuse-book-evidence.md`.
- Source read: fuzzy-jev 0.6.0 in the local cargo registry (`src/types.rs`, `src/spec.rs`, `llms.txt`); ethos-zero `ethos-zero.ethos`, `src/generation.rs`; datom-codec `src/composition.rs`, `src/decimal.rs`.
- Skills: vision-ethos, vision-datom, knowledge-ethos.
- Web, fetched today: [docs.typesafe.ai/primitives.md](https://docs.typesafe.ai/primitives.md), [docs.typesafe.ai/introduction.md](https://docs.typesafe.ai/introduction.md), [github.com/Shearerbeard/jev-driver](https://github.com/Shearerbeard/jev-driver), [docs.rs/jev-driver](https://docs.rs/jev-driver/latest/jev_driver/).
- Token counts: tiktoken via `nix shell` (python3 with tiktoken), script in the session scratchpad.
