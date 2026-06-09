# 572 — gated Spirit + agent component: implementation handover

designer, 2026-06-09. Companion to `571` (schema-grammar handover). This hands off
the **other** active thread before a context reset: the gated-Spirit "guardian"
design and the `agent` LLM-call component that is its model substrate. Self-contained
for a fresh-context agent. The design rationale lives in `567`; this captures the
current build state, the decisions made, and what to build next.

## The two threads, and where each lives

1. **Gated Spirit (the guardian)** — design in `567`; the consumer. NOT built yet
   (it waits on the new production Spirit reaching parity — operator's track).
2. **The `agent` component** — the LLM-call substrate the guardian uses. **Built
   and landed on main this session** (details below). This supersedes the parts of
   `569` that describe a JSON-mode, local-only state.
3. (Schema-grammar spec is the third thread — see `571`. Independent of these two.)

## Decisions captured this session (Spirit records — the source of truth)

Query any with `spirit "(Observe (RecordIdentifiers ((Exact [<id>]) WithProvenance)))"`.

| id | kind | gist |
|---|---|---|
| `8g9n` | Principle | Hard deletion of intent is inevitable on a long timeline; design it as a deliberate recoverable-to-a-horizon collection stage, not a forbidden act. |
| `icpa` | Principle | Spirit's overriding goal is to be maximally **clutter-free** — a curated store, not a capture-everything log. |
| `mrkv` | Decision | **Capture blocks**: the guardian is a gate, not an advisor; clutter is resolved/refused at the door. |
| `qoku` | Clarification | Routing intent through a third-party hosted inference API is **not** the publication-leak the privacy rule guards; it's acceptable. |
| `wa4j` | Decision | Strategy: get one or two components (Spirit foremost) excellent before spreading; the missing reliable intent source is the #1 gap in LLM dev. |
| `750r` | Decision | Gate Spirit with a **strong** open-weight model, not a small one — intent is too important to under-resource. |
| `iucr` | Decision | The `agent` component is an **LLM-API-call** component (provider HTTP calls), not a harness front door; harness backends deferred. |
| `f8k7` | Decision | Providers modeled as a **generic OpenAI-compatible** API = configuration, not a contract change per provider. |
| `kgvc` | Clarification | **Importance** is psyche-declarable and distinct from certainty; a one-off can be high-importance. (Rename of "weight".) |
| `l98v` | Decision | The agent component takes **NOTA directly** from the model (the model emits NOTA), not JSON the daemon translates. |
| `go8m` | Decision | Spirit's intent-resolution operations are **typed combined actions** (one atomic call); simplest = add a record while deprecating a list of records by identifier. |
| `42az` | Correction | Size effort to the request; don't reflexively run expensive multi-agent workflows (see also `skills`/the memory rule below). |

(Open-weight model research that informed `750r` is in `568`.)

## The agent component — current state (on main, green)

Three repos, all on **main**, build + tests + clippy green:

- **`agent`** (daemon) — `main` = `ae9e46dd`. Greenfield kameo/schema-derived
  daemon. The provider HTTPS call runs as an **async Nexus effect** (`CallProvider`),
  off the engine mailbox. `Provider` trait with `FixtureProvider` (offline default,
  no key) + `OpenAiCompatibleProvider` (reqwest, behind the `live-provider`
  feature). `ProviderRegistry` is engine-held, in-memory, re-supplied via the meta
  tier on restart. Deps on git/main (no longer worktree paths).
- **`signal-agent`** — `main` = `a0e8f24`. `Call(Prompt) -> Completed(Completion) |
  CallRejected(CallRejection)`. `OutputMode` is **`FreeText | Nota`** (the JSON
  `JsonObject` mode was removed). New `CallRejectionReason::InvalidNotaOutput`.
  Streaming (`StreamCall`/`CancelStream`) is contract-complete but daemon-stubbed
  (`RequestUnimplemented`).
- **`meta-signal-agent`** — `main` = `e39dcc8`. `ConfigureProvider` (endpoint +
  model + env-var key handle) / `RetireProvider` / `SetDefaultProvider` / lifecycle.

**NOTA-direct mechanism** (the `l98v` decision, implemented): for `OutputMode::Nota`
the daemon injects a "respond with one valid NOTA expression" instruction
(`provider.rs ProviderCall::with_nota_instruction`), calls the provider, validates
the completion parses via `nota_next::Document::parse`, and retries once with the
parse error (`with_nota_correction`) before rejecting with `InvalidNotaOutput`
(`engine.rs complete_nota`, `NOTA_OUTPUT_ATTEMPTS = 2`). This runs inside the async
effect seam, not a blocking handler.

**DeepSeek**: wired generically — configure a provider with endpoint
`https://api.deepseek.com/v1`, model `deepseek-chat`, key handle `DEEPSEEK_API_KEY`.
A real call needs the key in the daemon's env; the gated live test
(`tests/fixture_round_trip.rs::live_provider_completes_when_key_present`, behind
`--features live-provider`) exercises it. No real call has been run.

**Stubbed/deferred**: daemon-side streaming (token deltas); a redb/SEMA-backed
provider registry (currently in-memory); harness backends (Claude Code/Codex/Pi —
deferred per `iucr`). One trivial leftover: `agent/ARCHITECTURE.md` still says
"JsonObject" in one line — sweep it.

## What to build next — the gated-capture path (NOT yet built)

This is the actual guardian, per `567`. It depends on the **new production Spirit**
(operator was bringing the schema-derived spirit to parity — the psyche said it was
"ready today"; confirm it landed before building on it).

The flow to implement, in Spirit's runtime:
1. On `Record`, Spirit's Nexus emits a **`Scout` effect** (a new `NexusEffectCommand`,
   same shape as the agent daemon's `CallProvider` — an async effect, off the
   mailbox).
2. The Scout effect calls the **`agent` component as a Signal peer**: a
   `Call(Prompt)` with `OutputMode::Nota`, the prompt carrying the proposed record
   + its neighborhood (the few topic/embedding-near existing records) + the verdict
   schema. The agent returns a NOTA verdict.
3. Spirit composes a **blocking** typed reply (`mrkv`): the verdict tells the
   thinking agent whether the record is original / a duplicate / a contradiction /
   precedent, with the relevant records' summaries (not just ids) so it can act
   without a second query.
4. The thinking agent resolves via the **typed combined actions** (`go8m`): e.g.
   `AddRecordDeprecating(new, [uids])` — one atomic op. Reinforcement of a pure
   duplicate = no new row (bump the existing record); a distinct-but-related
   statement = new atomic row + a relation edge.

Design specifics in `567`: clutter-free (`icpa`) is the overriding goal; capture
blocks but the failure mode is **refuse, not admit** (model down → wait/refuse,
never admit unvetted); blocking ≠ losing (the agent resolves-and-resubmits). The
guardian model is a **strong** open-weight (`750r`) — the agent component is
provider-agnostic, so point it at whatever is chosen (DeepSeek/MiMo are the
candidates; note: for grammar-constrained NOTA output, a self-hosted model unlocks
GBNF/grammar-constrained decoding, otherwise it's prompt + validate-and-retry as
already built).

**Explicitly deferred** (psyche: "running too far ahead, get it working"): the
two-layer raw/curated store, decay/recall mechanics, the "what counts as a recall
event" question, auto-retirement aggressiveness. Build the blocking-scout path
first; these come later.

## Embeddings note

The guardian narrows to the neighborhood cheaply via embeddings (an encoder pass +
ANN), then the model judges the handful. Per the review thread, the embedding
**index** is component-owned SEMA state (lives in Spirit); only the **model
inference** is the peer call (the agent component). At ~1700 records a brute-force
cosine scan is sub-millisecond — an ANN index (HNSW) is premature.

## Pointers

- **Design + rationale:** `reports/designer/567-spirit-intent-lifecycle-forgetting-well.md`
  (the guardian design, capture-blocks addendum, the open-questions resolved
  in-session). `565` is the broader engine-makeover context.
- **Agent build report:** `569` (original build; superseded on the NOTA-direct +
  on-main points by this file).
- **Open-weight model options:** `568`.
- **Schema-grammar thread (independent):** `571`.
- **Spirit CLI:** `skills/spirit-cli.md`. The records table above is the decision
  index.
- **Memory discipline (learned this session):** harness/agent-private memory is
  forbidden (AGENTS.md hard override); durable truth lands in Spirit / skills /
  reports. The `42az` correction (size effort to the request) and the
  no-pre-production-breakage-hedging principle live in Spirit, not a private store.
