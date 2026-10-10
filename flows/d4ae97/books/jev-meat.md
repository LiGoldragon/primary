<!-- to-the-living:start -->
Presentation.{ «fuzzy-jev: what it is» }

# fuzzy-jev: what it is

Everything below was measured on 2026-10-05. Both crates were downloaded from crates.io, counted with tokei, built, and their offline tests run. Both repositories were cloned.

## Your five questions

### fuzzy-jev 0.6.0

| Question | Answer |
|---|---|
| What is it? | A Rust client for Jev that sends typed questions to OpenRouter's `POST /api/alpha/decisions` and checks the typed answers that come back. On top of that it adds a fuzzy-logic rule engine (AND, OR, NOT, hedges, Mamdani outputs), SVG drawings of the rules, and a `jev` command-line tool. |
| Who makes it | Daniel Saad (GitHub `dsaad68`), alone. Unofficial: not TypeSafe or OpenRouter. MIT. |
| How big? | `.crate` file: 179,051 bytes. 42 files. 7,404 lines of Rust in 18 files (5,892 of them code). The part that talks to Jev is 1,111 lines. |
| What stack? | Rust 2021. reqwest 0.13 (rustls), serde and serde_json. It is async, and the command-line build adds tokio. It builds natively and for wasm32. Library name: `jev`. |
| When released? | First on crates.io 2026-09-23 (0.2.0). Latest 2026-10-01 (0.6.0). Six versions in nine days. |
| How many commits? | 51, all by one person, from 2026-09-22 to 2026-10-01. 1 star, 0 forks. |

### typesafe-system-one 0.1.1

| Question | Answer |
|---|---|
| What is it? | An async Rust client for TypeSafe's System One API (`POST {base}/v1/systemone`), with typed Noul, Choice and Score questions and answers, retries and logging. It talks to TypeSafe by default; pointed at `https://openrouter.ai/api` it uses OpenRouter's System One route. |
| Who makes it | hailey (GitHub `haileyok`), alone. Unofficial: the crate says it is "not affiliated with TypeSafe". MIT. |
| How big? | `.crate` file: 62,455 bytes. 23 files. 5,475 lines of Rust in 16 files (4,281 of them code), of which `src/` is 3,546 lines. |
| What stack? | Rust 2021, minimum Rust 1.88. reqwest 0.13 (rustls), tokio, serde, serde_json, thiserror, tracing, fastrand, httpdate. Async only. |
| When released? | 0.1.0 and 0.1.1, both on 2026-09-26, 58 minutes apart. Nothing since. |
| How many commits? | 5 in the repository (4 touch the Rust half), all on 2026-09-26. 7 stars, 1 fork. The same repository also holds a Go client. |

### Jev itself

| Question | Answer |
|---|---|
| What is it? | TypeSafe AI's model that does not write text. You give it a state (text or JSON) and typed questions, and it answers each one with a number: a yes-probability (Noul), a pick from options with probabilities (Choice), or a level on a scale (Score). |
| Who makes it | TypeSafe AI, San Francisco. Its docs call Jev "TypeSafe's flagship model and the first System One model". |
| How big? | Not published: TypeSafe gives no parameter count, architecture, weights or paper. |
| Where to get it | Through TypeSafe, OpenRouter (`typesafe/jev-1.13`, `~typesafe/jev-latest`), OpenCode Zen and Vercel. |
| When released? | Public launch 2026-09-15, according to press and blogs. The version answering today is dated 2026-09-17 (`typesafe/jev-1.13-20260917`, from OpenRouter's example reply). |
| Price | $0.042 per million input tokens. Output is free. OpenRouter's example call: 476 input tokens for $0.000019992. |

## Side by side, measured

| | fuzzy-jev 0.6.0 | typesafe-system-one 0.1.1 |
|---|---|---|
| `.crate` size | 179,051 B | 62,455 B |
| Files in the crate | 42 | 23 |
| Rust (tokei, including doc comments) | 18 files / 7,404 lines | 16 files / 5,475 lines |
| Other languages in the crate | HTML+CSS 1 file / 1,731 lines; Markdown 7 / 2,560; TOML 6 / 296; JSON 4 / 90; text 1 / 41 | Markdown 1 / 428; TOML 1 / 113 |
| Languages in the repository (GitHub bytes) | Rust 370,807, HTML 99,452, Python 21,381 | Rust 194,023, Go 108,249, Python 5,735 |
| Direct dependencies | 3 always (reqwest, serde, serde_json) + 6 for the command line (clap, tokio, anyhow, toml, terminal_size, unicode-width) | 8 (reqwest, tokio, serde, serde_json, thiserror, tracing, fastrand, httpdate) |
| All dependencies, counted with `cargo tree` | 113 with defaults; 86 with `default-features = false` | 101 |
| Features | `default = ["cli"]`; `cli`; `command` | `default = []`; `native-tls` |
| Endpoint | `https://openrouter.ai/api/alpha/decisions` (fixed; can be overridden with `with_url`) | `{base_url}/v1/systemone`; default base is `https://api.typesafe.ai` |
| Default model | `~typesafe/jev-latest` | `jev-latest` |
| Timeout | 60 s per request | 10 s per attempt |
| Retries | none, ever ("one that timed out may have been answered, and billed") | 2 retries by default, on 408, 429, 500–599, timeouts and connection errors; 30 s budget |
| Checks the reply | yes: every question answered, right type, valid against the criteria | decodes typed answers; keeps an unknown answer type as raw data |
| crates.io downloads | 81 | 24 |
| Offline tests, run here | 140 passed, 1 live test skipped | 116 passed, 2 live tests skipped |
| Published crate matches repository `main` | yes: `src/` identical, no commits after the release | yes: `rust/src/` identical, no commits after the release |

## Release dates (crates.io API)

| fuzzy-jev | Published (UTC) | `.crate` bytes |
|---|---|---|
| 0.2.0 | 2026-09-23 21:14 | 101,916 |
| 0.3.0 | 2026-09-24 06:03 | 113,559 |
| 0.3.1 | 2026-09-24 07:48 | 120,934 |
| 0.4.0 | 2026-09-26 12:02 | 168,447 |
| 0.5.0 | 2026-09-26 15:47 | 172,445 |
| 0.6.0 | 2026-10-01 21:49 | 179,051 |

A `v0.1.0` tag exists on GitHub (2026-09-22), but 0.1.0 was never published to crates.io.

| typesafe-system-one | Published (UTC) | `.crate` bytes |
|---|---|---|
| 0.1.0 | 2026-09-26 22:10 | 61,698 |
| 0.1.1 | 2026-09-26 23:08 | 62,455 (published from GitHub Actions) |

## Repositories

| | github.com/dsaad68/fuzzy-jev | github.com/haileyok/typesafe-client |
|---|---|---|
| Created | 2026-09-22 | 2026-09-26 |
| Commits | 51 | 5 (4 touch `rust/`) |
| Contributors | 1 (Daniel Saad) | 1 (hailey) |
| First / last commit | 2026-09-22 / 2026-10-01 | both 2026-09-26 |
| Stars / forks / open issues | 1 / 0 / 0 | 7 / 1 / 0 |
| Tags | v0.1.0 … v0.6.0 | rust/v0.1.0, rust/v0.1.1, go/v0.1.0, go/v0.1.1 |

## Where the fuzzy-jev lines go

| Part | Files | Lines (wc) | Built with `default-features = false`? |
|---|---|---|---|
| Talking to Jev | `lib.rs`, `types.rs`, `error.rs`, `models.rs` | 1,111 | yes |
| Fuzzy rules and SVG | `rules/mod.rs`, `output.rs`, `graph.rs`, `svg.rs` | 3,074 | no (needs the `command` feature) |
| Command line and browser explorer | `cli/*.rs`, `main.rs`, `explore.html` | 3,080 | no |
| Printing, rule files, agent skill | `print.rs`, `spec.rs`, `skill.rs` | 1,251 | no |

With `default-features = false`, only the 1,111 lines that talk to Jev are compiled. The rules, drawings and command line are left out.

## The public API, quoted

fuzzy-jev, `src/lib.rs:58` and `:66`:

```rust
pub const DECISIONS_URL: &str = "https://openrouter.ai/api/alpha/decisions";

pub struct Client {
    http: reqwest::Client,
    key: String,
    url: String,
    model: String,
    timeout: Duration,
}
```

fuzzy-jev, `src/lib.rs:118` (the one call):

```rust
pub async fn decide<K: Into<String>>(
    &self,
    state: impl Serialize,
    questions: impl IntoIterator<Item = (K, Question)>,
) -> Result<DecisionResponse> {
```

fuzzy-jev, `src/types.rs:31`:

```rust
pub enum Question {
    Choice { instructions: Value, criteria: Options },
    Score { instructions: Value, criteria: Vec<Value> },
    Noul {
        instructions: Value,
        #[serde(skip_serializing_if = "Option::is_none")]
        criteria: Option<NoulCriteria>,
    },
}
```

fuzzy-jev, `src/lib.rs:9` (its own example):

```rust
let client = Client::new(&std::env::var("OPENROUTER_API_KEY").unwrap_or_default());
let reply = client
    .decide(
        "Help! My payouts have been failing for 3 days.",
        [
            ("is_urgent", Question::noul("Does this message convey urgency?")),
            ("department", Question::choice("Which team should handle this?", [("billing", "Payments"), ("technical", "Bugs")])),
            // … a third, Score question
        ],
    )
    .await?;
```

typesafe-system-one, `src/client.rs:318` and `:351`:

```rust
pub async fn system_one(&self, request: SystemOneRequest) -> Result<SystemOneResponse, Error> {
// …
let path = "/v1/systemone";
let url = format!("{}{}", self.inner.base_url, path);
```

typesafe-system-one, `README.md:383` (how to point it at OpenRouter):

```rust
let openrouter = Client::builder()
    .api_key("sk-or-...")
    .base_url("https://openrouter.ai/api")
    .default_model("~typesafe/jev-latest")
    .default_header("X-Agent-Client", "my-app")
    .build()?;
```

## What Jev answers

This is the example from OpenRouter's Decisions API reference, shortened to two questions.

```json
{
  "model": "typesafe/jev-1.13",
  "state": {
    "customer_tier": "enterprise",
    "ticket": "My checkout page shows a blank screen after I click Pay. I have tried two browsers."
  },
  "questions": {
    "is_bug": {
      "type": "noul",
      "instructions": "Is the customer reporting a software defect?",
      "criteria": {
        "true": "The customer describes broken or unexpected product behavior.",
        "false": "The customer is asking a question or requesting a feature."
      }
    },
    "team": {
      "type": "choice",
      "instructions": "Which team should own this ticket?",
      "criteria": {
        "account": "Login, permissions, or profile issues.",
        "frontend": "Rendering, layout, or browser compatibility issues.",
        "payments": "Checkout, billing, or payment processing issues."
      }
    }
  }
}
```

The reply:

```json
{
  "answers": {
    "is_bug": { "type": "noul", "noul": 0.96 },
    "team": {
      "type": "choice",
      "choice": "payments",
      "confidence": 0.75,
      "probabilities": { "account": 0, "frontend": 0.16, "payments": 0.84 }
    }
  },
  "id": "gen-dec-1789738314-X5e5eKGQdvR9rblyX250",
  "model": "typesafe/jev-1.13-20260917",
  "provider": "TypeSafe",
  "usage": { "cost": 0.000019992, "input_tokens": 476, "output_tokens": 70 }
}
```

A Score question gets `score` (a decimal between levels, such as `1.99`), `legend`, `probabilities` and `confidence`. OpenRouter lists these error codes: 400, 401, 402, 403, 404, 413, 429, 500, 502, 503, 524 and 529.

## How a call travels

<svg viewBox="0 0 340 560" width="100%" style="max-width:420px" role="img" aria-label="A call goes from judge through fuzzy-jev to OpenRouter and Jev, and the answer comes back the same way" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="13">
  <defs>
    <marker id="down" viewBox="0 0 10 10" refX="5" refY="9" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,0 L5,10 z" fill="#3a6ea5"/></marker>
    <marker id="up" viewBox="0 0 10 10" refX="5" refY="9" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,0 L5,10 z" fill="#2e8b57"/></marker>
  </defs>
  <rect x="10" y="10" width="320" height="78" rx="10" fill="#fdf1d6" stroke="#c99a2e"/>
  <text x="20" y="32" font-weight="bold">judge (our code, blocking)</text>
  <text x="20" y="52">builds the state and questions,</text>
  <text x="20" y="70">gets the OpenRouter key from gopass</text>
  <line x1="110" y1="88" x2="110" y2="128" stroke="#3a6ea5" stroke-width="2" marker-end="url(#down)"/>
  <text x="118" y="112" fill="#3a6ea5">runs it in a tokio runtime</text>
  <rect x="10" y="132" width="320" height="98" rx="10" fill="#e3eefb" stroke="#3a6ea5"/>
  <text x="20" y="154" font-weight="bold">fuzzy-jev Client</text>
  <text x="20" y="174">request(): checks each question,</text>
  <text x="20" y="192">refuses duplicate ids</text>
  <text x="20" y="212">send(): JSON + Bearer key, 60 s, no retry</text>
  <line x1="110" y1="230" x2="110" y2="270" stroke="#3a6ea5" stroke-width="2" marker-end="url(#down)"/>
  <text x="118" y="254" fill="#3a6ea5">POST /api/alpha/decisions</text>
  <rect x="10" y="274" width="320" height="62" rx="10" fill="#efe6f8" stroke="#7b55a8"/>
  <text x="20" y="296" font-weight="bold">OpenRouter</text>
  <text x="20" y="316">checks the key, bills, routes to TypeSafe</text>
  <line x1="110" y1="336" x2="110" y2="370" stroke="#3a6ea5" stroke-width="2" marker-end="url(#down)"/>
  <rect x="10" y="374" width="320" height="62" rx="10" fill="#fbe4e4" stroke="#b44a4a"/>
  <text x="20" y="396" font-weight="bold">Jev 1.13 (TypeSafe)</text>
  <text x="20" y="416">one number per question, no text</text>
  <path d="M260,374 C300,340 300,300 260,276" fill="none" stroke="#2e8b57" stroke-width="2" marker-end="url(#up)"/>
  <path d="M260,274 C300,250 300,200 260,232" fill="none" stroke="#2e8b57" stroke-width="2" marker-end="url(#up)"/>
  <text x="196" y="262" fill="#2e8b57" font-size="11">+ id, provider, cost</text>
  <rect x="10" y="456" width="320" height="94" rx="10" fill="#e2f4e9" stroke="#2e8b57"/>
  <text x="20" y="478" font-weight="bold" fill="#1f5f3b">Back in fuzzy-jev, then judge</text>
  <text x="20" y="498">check_against(): a missing or wrong-type</text>
  <text x="20" y="516">answer is an error, not a guess</text>
  <text x="20" y="536">judge decides what the number may do</text>
</svg>

On the way down, the call goes from judge to fuzzy-jev, OpenRouter and Jev (blue). On the way back (green), OpenRouter adds `id`, `provider` and `usage.cost`. fuzzy-jev then checks the reply against the questions that were asked, at `src/lib.rs:174`, before judge sees it. typesafe-system-one would take the same route through OpenRouter's `/api/v1/systemone` instead, and would retry on its own.

## What using it would mean for judge

judge lives at `/git/github.com/LiGoldragon/judge`. It is version 0.2.0, Rust 2024, and blocking: it uses reqwest 0.12 with `blocking`. Its README says "Calls are single-attempt; adapters own any domain-specific retry."

| Fact about judge today | Measured |
|---|---|
| Jev code on `main` | none |
| Jev code on an unmerged branch (3 commits, 2026-10-04) | +1,158 lines: 298 in `lib.rs` (typed request, reply and client), 510 for an `openrouter-decisions` command, 337 of tests |
| Dependencies with `live-provider` | 97 crates |
| After adding `fuzzy-jev = { version = "=0.6.0", default-features = false }` plus `tokio` (`rt`), in a scratch copy | 105 crates. It builds. |
| Crates that appear twice | reqwest (0.12 and 0.13), base64, getrandom |
| New crates | aws-lc-rs and aws-lc-sys (C crypto, compiled at build time), rustls-platform-verifier, rustls-native-certs, openssl-probe |

What would change:

```rust
// judge/src/lib.rs, the shape of the change, not written yet
let runtime = tokio::runtime::Builder::new_current_thread().enable_all().build()?;
let client = jev::Client::new(secret).with_model("typesafe/jev-1.13");
let reply = runtime.block_on(client.decide(state, questions))?;
```

- **Removed from judge:** its own Decisions request, reply and client types (most of the 298 lines in `lib.rs`).
- **Kept in judge:** the secret boundary (gopass `platform.openrouter.ai/api-key`), the command line, and the decision of what an answer is allowed to do.
- **Matches judge already:** fuzzy-jev's no-retry rule is judge's single-attempt rule. typesafe-system-one retries timeouts and 5xx by default, which can pay for one decision twice.
- **New cost:** an async runtime inside a blocking crate, a second reqwest, and aws-lc-sys, which needs a C toolchain in the Nix build.
- **Not tested:** no live call has been made. The OpenRouter key could not be read by the earlier review, so whether it exists is unknown.

## Rulings

1. **If judge reuses a crate, use fuzzy-jev 0.6.0 pinned exactly, with `default-features = false` and the model pinned to `typesafe/jev-1.13`.** That compiles only the 1,111 lines that talk to Jev. It calls the Decisions route that judge already targets, and it never retries, which is judge's own rule. Do not use typesafe-system-one for judge: it brings 16 crates judge does not already have, against 5 for fuzzy-jev, goes through the System One route, and retries by default.
2. **Do not take fuzzy-jev's fuzzy rules.** They are a decision policy: they turn answers into actions. Deciding what an answer may do stays with judge and its owner, and the opt-out of default features already keeps those rules out of the build.

## Sources

- crates.io API: `/api/v1/crates/fuzzy-jev`, `/api/v1/crates/typesafe-system-one` and their `/versions`; `.crate` downloads for 0.6.0 and 0.1.1.
- GitHub API and clones: [dsaad68/fuzzy-jev](https://github.com/dsaad68/fuzzy-jev), [haileyok/typesafe-client](https://github.com/haileyok/typesafe-client).
- OpenRouter: [Decisions API reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request).
- TypeSafe: [models](https://docs.typesafe.ai/models.md).
- Launch date: [flaviocopes](https://flaviocopes.com/jev/) and [DataCamp](https://www.datacamp.com/blog/system-one-models-jev). These are secondary sources.
- Earlier reports: `flows/d66c26/reports/jev-reuse-book-evidence.md`, `flows/bad807/reports/jev-ecosystem.md`.
<!-- to-the-living:end -->
