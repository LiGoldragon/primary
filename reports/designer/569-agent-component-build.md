# 569 — agent component build (LLM-API-call triad)

Designer build of the `agent` component: an LLM-API-call substrate that makes
OpenAI-compatible provider HTTP calls in an API style — the call substrate the
gated Spirit guardian will use to judge intent. Authorized by the psyche; scope
shaped by Spirit `iucr` (LLM-API caller, not a harness; harness backends
deferred) and `f8k7` (providers as a generic OpenAI-compatible API =
configuration, not a contract change).

## What was built

Three repos, all building (`cargo build`) and tested green.

| Repo | Where | Build | Tests |
|---|---|---|---|
| `signal-agent` | `~/wt/.../signal-agent` (branch `agent-llm-call-rewrite`) | clean | 6 round-trip pass |
| `meta-signal-agent` | `~/wt/.../meta-signal-agent` (branch `agent-llm-call-rewrite`) | clean | 5 round-trip pass |
| `agent` (new) | `/git/github.com/LiGoldragon/agent` (local, `main` bookmark) | clean (+`live-provider`) | 4 fixture round-trip pass |

The two contracts were rewritten from their retired `.concept.schema` /
`signal_channel!` harness-delivery skeletons onto the modern schema-rust-next
`WireContract` stack, discarding the message-delivery / backend-spawn framing.
The `agent` daemon is greenfield on the kameo/schema-derived emitted-daemon
shell (the `message` + `cloud` daemon pattern).

## Contract shape landed

**`signal-agent`** (ordinary working contract) — `schema/lib.schema`:

- `Call(Prompt) -> Completed(Completion) | CallRejected(CallRejection)` — the
  single-shot call.
- `StreamCall(Prompt)` opens `CompletionStream`; events `TokenStreamDelta` then
  a terminal `CompletionStreamDelta` (stop reason + usage); `StreamOpened` reply.
- `CancelStream(StreamToken) -> StreamCancelled`.
- A `Prompt` = optional system text + `ChatTranscript` + `PromptOptions`
  (model?, provider?, temperature, max-output-tokens, `OutputMode`). `OutputMode`
  is `FreeText | JsonObject` — `JsonObject` is the structured-verdict mode the
  guardian wants. Closed enums throughout; no concrete provider named.

**`meta-signal-agent`** (owner-only meta policy) — `schema/lib.schema`:

- `ConfigureProvider(ProviderConfiguration)` — add/update a provider =
  `name + endpoint + default_model + api_key_handle`. This IS the
  "add a provider = configuration" record; no per-provider type.
- `RetireProvider`, `SetDefaultProvider`, `Start`, `Stop`.
- The key handle is an env-var NAME — the secret value never crosses the wire.

**`agent` daemon** — runtime triad on the emitted shell:

- Working tier = dependency `signal_agent::schema::lib`; meta tier (0o600) =
  `meta-signal-agent` decoded by `handle_meta_connection`.
- Nexus plane declares the one external effect, `CallProvider(Prompt)`. The
  call path: `Call` → `NexusWork::SignalArrived` → `decide` emits
  `CommandEffect(CallProvider)` → the generated **async** runner awaits
  `run_effect`, which resolves the registry and makes the HTTPS call — off the
  engine mailbox, never a blocking handler. Result → `EffectCompleted` → reply.
- `Provider` is a dyn-compatible async trait. `FixtureProvider` (offline, no key)
  is the default; `OpenAiCompatibleProvider` (reqwest, `rustls-tls`) is behind
  the `live-provider` feature. One client serves every configured provider.
- `ProviderRegistry` (engine-held policy state) resolves a prompt to a
  `ProviderCall`; `EnvironmentKeySource` resolves the key handle at call time
  (tests inject a literal key source). Keys never logged/persisted; `ProviderApiKey`
  `Debug` is redacted.
- One-argument binary startup (`AgentDaemonConfiguration` rkyv), with optional
  `bootstrap_providers` seed; no NOTA parsed by the daemon. Thin `agent` CLI.

## Decisions made (flagged, not blocking)

1. **Provider call as the async Nexus effect, not a sync engine call.** `cloud`
   does its provider IO synchronously inside the engine (`ureq` + `Mutex`); I
   used the async `run_effect` seam instead, which is the discipline-correct
   shape (no blocking in a handler). This is the main design choice.
2. **`Provider` returns a boxed future** (`Pin<Box<dyn Future + Send>>`) so the
   trait is dyn-compatible and one engine type holds either backend. RPITIT
   async-trait isn't dyn-compatible.
3. **Provider registry held in the engine, SEMA plane stateless.** Mirrors
   `cloud` (its `Store` is engine-held, not in the emitted SEMA plane). The redb
   durable projection of the registry is deferred; on restart the registry is
   re-supplied by meta `Configure`.
4. **Contract deps pinned by `path` to the worktrees.** The contracts are on a
   feature branch, not main; `git`/`branch = main` deps would not resolve. The
   `agent` Cargo.toml carries a dev-pin comment to switch to git deps once the
   operator integrates the contracts to main.
5. **Streaming contract-complete but daemon-stubbed.** `StreamCall` /
   `CancelStream` exist in the contract; the daemon replies `RequestUnimplemented`
   for now (the single-shot `Call` path is live). The emitted daemon's streaming
   subscription runner is the next increment.

## What's stubbed / deferred

- Harness backends (Claude Code / Codex / Pi sessions) — deferred by psyche
  decision; absent.
- Daemon-side streaming reply (token-delta push) — contract present, daemon
  stubbed.
- Durable redb projection of the provider registry — registry is in-memory.
- The `agent` repo's Nix flake build (package/checks) — left as devShell-only
  because crane can't vendor the out-of-tree path-dep contracts; wire the
  standard crane checks once deps move to git/main.

## Open questions for the psyche

1. **Remote + integration.** The new `agent` repo is **local-only** (no GitHub
   remote created — I did not assume that authority). The two contract rewrites
   are on the `agent-llm-call-rewrite` feature branch, unpushed (designers don't
   push code-repo main). Do you want a `github.com/LiGoldragon/agent` remote
   created, and should the operator integrate the contract branches to main
   (which then lets the `agent` deps switch from path to git)?
2. **MiMo endpoint.** I used a placeholder MiMo endpoint (`api.mimo.example`) in
   examples. DeepSeek's (`api.deepseek.com/v1`) is real. What is MiMo/Xiaomi's
   actual OpenAI-compatible base URL and the key-handle env-var name you want
   seeded?
3. **Streaming priority.** Is daemon-side streaming (token deltas) needed for the
   guardian's first use, or is the single-shot `Call` with `JsonObject` verdict
   enough for now? That decides whether the streaming runner is the next slice.
4. **Registry durability.** Is in-memory-registry-re-supplied-on-restart
   acceptable for the guardian's deployment, or do you want the redb-backed
   provider registry (SEMA plane) before this goes live?

## Files

- `~/wt/github.com/LiGoldragon/signal-agent/` — `schema/lib.schema`, `src/lib.rs`,
  `tests/round_trip.rs`, `examples/canonical.nota`, `INTENT.md`, `ARCHITECTURE.md`.
- `~/wt/github.com/LiGoldragon/meta-signal-agent/` — same layout.
- `/git/github.com/LiGoldragon/agent/` — `schema/{nexus,sema}.schema`, `build.rs`,
  `src/{engine,provider,registry,config,schema_daemon,client,error}.rs`,
  `src/bin/{agent,agent_daemon}.rs`, `tests/fixture_round_trip.rs`, `INTENT.md`,
  `ARCHITECTURE.md`.
