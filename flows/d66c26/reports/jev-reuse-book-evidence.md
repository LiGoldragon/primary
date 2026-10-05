# Jev Rust reuse evidence

This packet is factual input for Fable's recommendation and Sonnet's book. It does not approve an implementation or choose a caller.

## Current provider contract

OpenRouter currently offers TypeSafe Jev as `typesafe/jev-1.13` and the moving alias `~typesafe/jev-latest`. The public model page lists 32K context and $0.042 per million input tokens with output free. Jev is a typed decision model, not a chat-completions model.

OpenRouter documents two Jev surfaces using the same OpenRouter key and account:

- Decisions: `POST https://openrouter.ai/api/alpha/decisions`, with `model`, `state`, and `questions`.
- System One: `POST https://openrouter.ai/api/v1/systemone`, for a TypeSafe SDK pointed at `https://openrouter.ai/api`.

The official TypeSafe SDKs named by the provider are JavaScript/TypeScript and Python. No official TypeSafe Rust SDK or official generated Rust OpenAPI client was found in this bounded audit.

## Community Rust candidate

[`typesafe-system-one` 0.1.1](https://docs.rs/typesafe-system-one/latest/typesafe_system_one/) is an MIT-licensed, async Rust 1.88+ crate from the public [`haileyok/typesafe-client`](https://github.com/haileyok/typesafe-client) repository. It describes itself as unofficial and unaffiliated with TypeSafe. Its maintenance and release posture is not assessed here.

It models Jev's three typed question forms (`Noul`, `Choice`, `Score`) and typed responses. It is not a generic OpenAI chat client.

### Source-level compatibility audit

This is source inspection of the repository's moving `main` branch only. No dependency was fetched, compiled, installed, or called. It is not an immutable audit of the published 0.1.1 crate artifact, and equivalence between this source revision and that release remains to be checked before pinning a dependency.

- `ClientBuilder` accepts an API key, base URL, and default model. Its documented OpenRouter example sets `base_url("https://openrouter.ai/api")` and `default_model("~typesafe/jev-latest")`.
- The transport appends the fixed path `/v1/systemone` to that base URL, yielding `https://openrouter.ai/api/v1/systemone`, the official OpenRouter System One endpoint.
- It posts JSON with SDK-owned `Authorization`, `Accept`, and `Content-Type` headers taking precedence over caller headers. The source uses the configured API key as the bearer credential.
- `SystemOneRequest` carries `state`, optional `model`, and a map of named typed questions. The response decoder recognizes Noul, Choice, and Score answers, retaining an unrecognized future answer type as raw data rather than silently treating it as a known result.
- Its README claims the OpenRouter setup and asks for an OpenRouter key in that example. This aligns with OpenRouter's TypeSafe-SDK gateway documentation, but end-to-end compatibility has not been witnessed with our account or a live request.

The crate's direct-TypeSafe defaults (`https://api.typesafe.ai`, `jev-latest`, `TYPESAFE_API_KEY`) must be explicitly overridden for OpenRouter. Do not infer that a direct TypeSafe key exists.

## Direct Decisions candidate: `fuzzy-jev` 0.6.0

This is a separate community option found in Fable's [ecosystem report](/home/li/primary/flows/bad807/reports/jev-ecosystem.md). On 2026-10-04, this review inspected the **released crates.io artifact**, not an installed dependency or a moving repository checkout: [`fuzzy-jev` 0.6.0](https://crates.io/crates/fuzzy-jev/0.6.0), published 2026-10-01. The downloaded artifact SHA-256 was `d1b1a4e0c61e72dea37907c6634315e53f0467ac7adede496181902a4608f84f`, matching the registry checksum. Its embedded `.cargo_vcs_info.json` names source commit `6e55c5b8ed527e934efb0b51d322805ae7be2aa2`; this is release provenance, not a claim that current repository `main` is equivalent.

The artifact's normalized manifest declares MIT, Rust 2021, library crate name `jev`, package name `fuzzy-jev`, and default feature `cli`; its repository field is [`dsaad68/fuzzy-jev`](https://github.com/dsaad68/fuzzy-jev). It contains a native and wasm transport, CLI, fuzzy-rule engine, SVG rendering, skill material, fixtures, and a live-test source. No build, package installation, fixture execution, or live request occurred in this review.

### What the released crate actually transports

- It fixes `DECISIONS_URL` to `https://openrouter.ai/api/alpha/decisions`, sends a JSON `POST`, and applies `Authorization: Bearer …` when its supplied key is nonempty. That is the provider-documented Decisions surface, which OpenRouter says is suitable for plain HTTP callers; it removes the **System One gateway path** uncertainty of `typesafe-system-one`. It does not establish that this account has a usable key or that a live call succeeds.
- Its request type is `model`, arbitrary JSON `state`, and a named map of typed `noul`, `choice`, or `score` questions. It accepts structured JSON for instructions and criteria, validates known question bounds before transmission, and defaults to `~typesafe/jev-latest`; callers can set a model.
- Its response type retains model, answers, usage, optional id and provider. It decodes the three Jev answer forms and checks that requested answers are present, type-matching, and valid against the submitted choice/score criteria. This is meaningful typed reply support, not a chat wrapper.
- It uses a 60-second default request/read timeout and explicitly does not resend after a timeout or other failure. That avoids automatic duplicate decisions, but leaves retry, idempotency, timeout handling, and any cost policy to the adopting caller. The transport reads the complete HTTP response before decoding; only its rendered error message is shortened.

### Fit and boundaries

`fuzzy-jev` is the strongest **already-released Rust direct-Decisions transport** witnessed in this review. Reusing its transport can avoid both a bespoke `/api/alpha/decisions` client and the question of whether a System One client is configured with the right gateway URL. That is a technical candidate, not approval to adopt it.

It also embeds a fuzzy-rule interpretation layer. Its README describes using Jev probabilities as rule degrees and deriving outputs from those rules. That layer represents decision policy and must not be imported merely because the transport is reused. The package's default `cli` feature likewise brings command dependencies; a Rust caller would need an explicit dependency and feature-selection decision. Its `with_url` override can direct bearer credentials to a caller-chosen URL, so any adopter must decide whether that flexibility is acceptable.

### Candidate comparison

| Candidate | Evidence inspected | API path / typed support | What remains unproven or requires a decision |
| --- | --- | --- | --- |
| `fuzzy-jev` 0.6.0 | Immutable released crate artifact and its embedded VCS pointer | Direct documented `POST /api/alpha/decisions`; typed request and checked typed response | Live OpenRouter/account compatibility; retry/cost/timeout policy; whether to take only its transport or its fuzzy-policy/CLI scope |
| `typesafe-system-one` 0.1.1 | Moving repository source only | Typed System One client; documented OpenRouter base URL plus `/v1/systemone` | Published-artifact/source equivalence; live gateway/account compatibility |
| Unpublished custom alpha adapter | Local source/fixtures reviewed; reported offline checks attributed to executor | Intended direct Decisions client | No published/installable artifact; live compatibility; its necessity now that a released direct client exists |

The limited recommendation is to place `fuzzy-jev` first in any actual dependency evaluation that needs OpenRouter Decisions from Rust, because its 0.6.0 artifact itself was inspected and its endpoint matches the provider documentation. Before an implementation owner selects it, audit the exact API surface the existing caller needs, decide whether the added fuzzy-rule/CLI scope is acceptable, and make a benign account-authorized compatibility test through the approved secret path. No model policy, consumer, book decision point, guide, cost ceiling, JSON convention, or change-sharing rule is authorized by this package evidence.

## Other source outcomes

- `typesafe-systemone` 0.2.0 is another unofficial direct-TypeSafe Rust client, but its inspected source has five commits and zero stars and no inspected OpenRouter example.
- `jev-sdk` 0.1.0 documents a client on docs.rs, but its linked GitHub source returned 404 during this audit; it is not a dependency candidate.
- Rig exposes a Jev module behind a feature flag, but it is a broader framework and this audit did not establish its OpenRouter gateway configuration.

## Current local status, attributed to Root

Root reports an unpublished custom judge at `dbd86891612ce5d2e370d7a95f2598dfa3bf15e5`. Its source and fixture code were reviewed. The reported 21/21 offline-test pass and Cargo release are executor-reported and were not rerun by this review; Nix evaluation is also executor-reported. It is not installed. `gopass` metadata exited 10 because the OpenRouter item is missing or inaccessible, so the user key is unknown. No default judge or reaping path was touched. This does not establish custom client necessity.

If a dependency route is selected, the stated local target is the existing caller's `judge/src/lib.rs` and `Cargo.toml`; Home has not changed. Whether that caller should use Jev, what state it may send, and what decision policy consumes a response are product decisions for Fable and the caller owner, not facts supplied by this packet.

## Sources

- OpenRouter, [Jev guide](https://openrouter.ai/docs/guides/community/jev), [Jev model page](https://openrouter.ai/typesafe/jev-1.13), [Decisions API](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request), and [TypeSafe SDK gateway](https://openrouter.ai/docs/guides/community/typesafe-sdk).
- TypeSafe, [quick start](https://docs.typesafe.ai/introduction/quickstart) and [primitives](https://docs.typesafe.ai/primitives).
- System One community candidate, [crate documentation](https://docs.rs/typesafe-system-one/latest/typesafe_system_one/), [repository](https://github.com/haileyok/typesafe-client), [Rust README](https://github.com/haileyok/typesafe-client/blob/main/rust/README.md), [transport source](https://github.com/haileyok/typesafe-client/blob/main/rust/src/client.rs), [request source](https://github.com/haileyok/typesafe-client/blob/main/rust/src/request.rs), [response source](https://github.com/haileyok/typesafe-client/blob/main/rust/src/answers.rs), and [Cargo manifest](https://github.com/haileyok/typesafe-client/blob/main/rust/Cargo.toml).
- Direct Decisions community candidate, [`fuzzy-jev` 0.6.0 crate](https://crates.io/crates/fuzzy-jev/0.6.0), [registry download artifact](https://crates.io/api/v1/crates/fuzzy-jev/0.6.0/download), and [source repository](https://github.com/dsaad68/fuzzy-jev). The 0.6.0 artifact and embedded VCS pointer, rather than a moving GitHub checkout, are the basis for the claims above.
