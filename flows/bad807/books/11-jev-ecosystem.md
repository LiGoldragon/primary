<!-- to-the-living:start -->
Presentation.{ «Our open-source stack and Jev: use, tools, plugins, infrastructure, trends» }

> We should get a book going on what our open-source stack looks like. Let's make a full report on: how Jev is used; what kind of tools are already out there to make it easy to use or integrate; what kind of plugins exist; what kind of infrastructure; what's really trending.

-- psyche, 2026-10-04.

A research worker read public docs, registries and threads on 2026-10-04. Nothing was installed or called.
"Read" means seen on the project's own page or registry. **Unverified** means one secondary page only.
Star counts and versions move daily. Everything about our own stack comes from our records.

## 1. Our stack today

| Part | What the records show |
|---|---|
| Claude Code, Codex | the public part: the seat pair |
| pi | an agents tree, generated |
| OpenCode | 1.18.16 on Ouranos, with a local model service |
| Herdr | 0.8.2; flows bind to it at start |
| messenger-clj | proof of concept for send and register; flows use its `hm-*` commands |
| Nexuses | Orchestrate 0.37, Flow 0.23, Message 0.19, Lojix 8.1; receipt not yet available |
| Provider plan | proposed, not seen running: OpenRouter door, Prometheus llama.cpp router |
| Jev | not installed; the OpenRouter key is missing or inaccessible |

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 400" width="700" font-family="sans-serif" font-size="13"><rect width="700" height="400" fill="#fff"/><text x="110" y="26" text-anchor="middle" font-weight="bold" fill="#1b2230">Seats (public part)</text><rect x="20" y="38" width="180" height="40" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="110" y="63" text-anchor="middle" fill="#1b2230">Claude Code</text><rect x="20" y="88" width="180" height="40" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="110" y="113" text-anchor="middle" fill="#1b2230">Codex</text><rect x="20" y="138" width="180" height="40" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="110" y="163" text-anchor="middle" fill="#1b2230">pi</text><rect x="20" y="188" width="180" height="40" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="110" y="213" text-anchor="middle" fill="#1b2230">OpenCode · local model</text><text x="350" y="26" text-anchor="middle" font-weight="bold" fill="#1b2230">Running beneath</text><rect x="240" y="38" width="220" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="350" y="57" text-anchor="middle" fill="#1b2230">Herdr 0.8.2</text><text x="350" y="74" text-anchor="middle" font-size="11" fill="#3d4a5c">flows bind at start</text><rect x="240" y="90" width="220" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="350" y="109" text-anchor="middle" fill="#1b2230">messenger-clj</text><text x="350" y="126" text-anchor="middle" font-size="11" fill="#3d4a5c">hm-* commands, proof of concept</text><rect x="240" y="142" width="220" height="86" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="350" y="162" text-anchor="middle" font-weight="bold" fill="#1b2230">Nexuses</text><text x="350" y="181" text-anchor="middle" fill="#1b2230">Orchestrate 0.37 · Flow 0.23</text><text x="350" y="199" text-anchor="middle" fill="#1b2230">Message 0.19 · Lojix 8.1</text><text x="350" y="218" text-anchor="middle" font-size="11" fill="#3d4a5c">receipt not yet available</text><text x="590" y="26" text-anchor="middle" font-weight="bold" fill="#1b2230">Providers (proposed)</text><rect x="490" y="38" width="200" height="44" rx="6" fill="#f3efe0" stroke="#8a7a2b" stroke-dasharray="5 3"/><text x="590" y="57" text-anchor="middle" fill="#1b2230">OpenRouter</text><text x="590" y="74" text-anchor="middle" font-size="11" fill="#3d4a5c">open-weight and Jev door</text><rect x="490" y="90" width="200" height="44" rx="6" fill="#f3efe0" stroke="#8a7a2b" stroke-dasharray="5 3"/><text x="590" y="109" text-anchor="middle" fill="#1b2230">llama.cpp router</text><text x="590" y="126" text-anchor="middle" font-size="11" fill="#3d4a5c">on Prometheus, private door</text><rect x="490" y="142" width="200" height="86" rx="6" fill="#fdecea" stroke="#b23b3b" stroke-dasharray="5 3"/><text x="590" y="174" text-anchor="middle" font-weight="bold" fill="#1b2230">Jev</text><text x="590" y="194" text-anchor="middle" fill="#1b2230">not installed</text><text x="590" y="213" text-anchor="middle" font-size="11" fill="#3d4a5c">key missing or inaccessible</text><rect x="10" y="246" width="680" height="146" rx="8" fill="#fdf6e3" stroke="#b07a12" stroke-dasharray="6 4"/><text x="350" y="268" text-anchor="middle" font-weight="bold" fill="#1b2230">Where Jev would slot in, only as his words place it</text><g font-size="12"><rect x="22" y="280" width="155" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="99" y="299" text-anchor="middle" fill="#1b2230">Reaping guide</text><text x="99" y="315" text-anchor="middle" font-size="11" fill="#3d4a5c">Flow · retired responses</text><rect x="187" y="280" width="155" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="264" y="299" text-anchor="middle" fill="#1b2230">Monitor flow</text><text x="264" y="315" text-anchor="middle" font-size="11" fill="#3d4a5c">Field</text><rect x="352" y="280" width="155" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="429" y="299" text-anchor="middle" fill="#1b2230">Power tier</text><text x="429" y="315" text-anchor="middle" font-size="11" fill="#3d4a5c">ultra-low power</text><rect x="517" y="280" width="160" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="597" y="299" text-anchor="middle" fill="#1b2230">Ethos to JSON</text><text x="597" y="315" text-anchor="middle" font-size="11" fill="#3d4a5c">datom bridge</text><rect x="104" y="334" width="155" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="181" y="353" text-anchor="middle" fill="#1b2230">Datom CLIs</text><text x="181" y="369" text-anchor="middle" font-size="11" fill="#3d4a5c">"Jev validates this"</text><rect x="269" y="334" width="155" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="346" y="353" text-anchor="middle" fill="#1b2230">Typed messages</text><text x="346" y="369" text-anchor="middle" font-size="11" fill="#3d4a5c">through Nexus</text><rect x="434" y="334" width="155" height="44" rx="20" fill="#fff" stroke="#b07a12"/><text x="511" y="353" text-anchor="middle" fill="#1b2230">Chained decisions</text><text x="511" y="369" text-anchor="middle" font-size="11" fill="#3d4a5c">one call feeds the next</text></g></svg>

*Our stack as the records show it; dashed boxes are proposed or absent, and the slots are his words, not a design.*

Public projects already sit at three of these seams: Herdr routing (jev-herdr), Codex and OpenCode routing, pi auto-approval.

## 2. How Jev is used

### One call

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 260" width="700" font-family="sans-serif" font-size="13"><defs><marker id="j2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="260" fill="#fff"/><rect x="10" y="16" width="190" height="72" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="105" y="40" text-anchor="middle" font-weight="bold" fill="#1b2230">state</text><text x="105" y="59" text-anchor="middle" font-size="12" fill="#1b2230">text, JSON or text array</text><text x="105" y="76" text-anchor="middle" font-size="11" fill="#3d4a5c">no image, audio, video</text><rect x="10" y="102" width="190" height="146" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="105" y="124" text-anchor="middle" font-weight="bold" fill="#1b2230">questions (named keys)</text><rect x="24" y="136" width="162" height="30" rx="14" fill="#fff" stroke="#2b4a8b"/><text x="105" y="156" text-anchor="middle" font-size="12" fill="#1b2230">noul: is this true?</text><rect x="24" y="172" width="162" height="30" rx="14" fill="#fff" stroke="#2b4a8b"/><text x="105" y="192" text-anchor="middle" font-size="12" fill="#1b2230">choice: up to 255 options</text><rect x="24" y="208" width="162" height="30" rx="14" fill="#fff" stroke="#2b4a8b"/><text x="105" y="228" text-anchor="middle" font-size="12" fill="#1b2230">score: 2 to 10 levels</text><rect x="258" y="88" width="170" height="84" rx="8" fill="#fdf0d8" stroke="#b07a12"/><text x="343" y="114" text-anchor="middle" font-weight="bold" font-size="15" fill="#1b2230">Jev</text><text x="343" y="134" text-anchor="middle" font-size="12" fill="#1b2230">jev-1.13.0</text><text x="343" y="153" text-anchor="middle" font-size="11" fill="#3d4a5c">keys hidden, answers apart</text><rect x="486" y="16" width="204" height="152" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="588" y="38" text-anchor="middle" font-weight="bold" fill="#1b2230">answers (same keys)</text><rect x="498" y="50" width="180" height="30" rx="14" fill="#fff" stroke="#2e7d32"/><text x="588" y="70" text-anchor="middle" font-size="12" fill="#1b2230">noul: 0 to 1</text><rect x="498" y="88" width="180" height="30" rx="14" fill="#fff" stroke="#2e7d32"/><text x="588" y="108" text-anchor="middle" font-size="12" fill="#1b2230">choice + probabilities</text><rect x="498" y="126" width="180" height="30" rx="14" fill="#fff" stroke="#2e7d32"/><text x="588" y="146" text-anchor="middle" font-size="12" fill="#1b2230">score + legend + probs</text><rect x="486" y="182" width="204" height="66" rx="6" fill="#f3efe0" stroke="#8a7a2b"/><text x="588" y="206" text-anchor="middle" font-weight="bold" fill="#1b2230">model + usage</text><text x="588" y="226" text-anchor="middle" font-size="12" fill="#1b2230">input billed, output free</text><text x="588" y="241" text-anchor="middle" font-size="11" fill="#3d4a5c">choice and score add confidence</text><g stroke="#333" stroke-width="1.6" fill="none" marker-end="url(#j2)"><line x1="200" y1="52" x2="256" y2="108"/><line x1="200" y1="175" x2="256" y2="152"/><line x1="428" y1="115" x2="484" y2="92"/><line x1="428" y1="150" x2="484" y2="210"/></g></svg>

*One Jev call: a state and named typed questions go in; one typed answer per key comes out, with the model and its usage.*

### Request and answer shape (read)

```
POST https://api.typesafe.ai/v1/systemone
{ "state": <text | object | array>,
  "model": "jev-latest",
  "questions": { "<your key>": { "type": "noul|choice|score",
                                 "instructions": <text | object | array>,
                                 "criteria": <by kind> } } }
→ { "model": "jev-1.13.0", "answers": { "<your key>": {...} },
    "usage": { "input_tokens": n, "output_tokens": n } }
```

### Noul: is this true?

```json
"is_urgent": {"type":"noul","instructions":"Does this convey urgency?",
  "criteria":{"true":"Explicitly time-sensitive","false":"No urgency expressed"}}
→ "is_urgent": {"type":"noul","noul":0.95}
```

### Choice: which option?

```json
"department": {"type":"choice","instructions":"Which team should handle this?",
  "criteria":{"billing":"Payments, invoicing, refunds","technical":"Bugs, outages",
              "sales":"Pricing, upgrades, new accounts"}}
→ "department": {"type":"choice","choice":"billing",
   "probabilities":{"billing":0.88,"technical":0.12,"sales":0.0},"confidence":0.81}
```

### Score: which level?

```json
"frustration": {"type":"score","instructions":"How frustrated is the customer?",
  "criteria":["Calm","Frustrated","Very angry"]}
→ "frustration": {"type":"score","score":1.05,
   "legend":{"0":"Calm","1":"Frustrated","2":"Very angry"},
   "probabilities":{"0":0.0,"1":0.95,"2":0.05},"confidence":0.92}
```

All three use TypeSafe's own example state: "Help! My payouts have been failing for 3 days."

### Prices and limits (read)

| Item | As published |
|---|---|
| Price | $0.042 per million input tokens; output free; same on OpenRouter and OpenCode Zen |
| Context | 64k per request; 32k for state plus the longest question (OpenRouter shows 32K) |
| Rate | 100K tokens/s, 80 requests/s, "can change without notice" |
| Errors | 401, 422, 429, 529; the SDKs retry and honour `retry-after` |
| Models | `jev-latest` and `jev-preview` both point to `jev-1.13.0`; pin the versioned ID |
| Limits | no fine-tuning; one set of weights; not trained on customer traffic |

### Weak spots TypeSafe names itself (read)

Literal reading, math and counting, date comparison, indirection, large or irrelevant state,
hostile text in state, contradictory criteria, bias toward the first Choice option, generation.
Its advice: arithmetic and dates in code, filter state first, reorder options to check consistency.

### Patterns people use (read)

| Pattern | Shape |
|---|---|
| Fan-out | 13 questions in one call: 12.2× cheaper, 10× faster, same answers (TypeSafe's figure) |
| Confidence gating | the answer says what; confidence says whether to act |
| Intent routing | to code, a specialist model, or a human |
| Composite scoring | atomic scores; weights kept in code |
| Classification | beam search over Choice; fall back to the parent class |
| Extraction | regex or a model proposes; Jev picks; code normalises |
| Rerank and search | one question per candidate, or a Choice over line IDs |
| Skill selection | one of 182 agent skills, in two requests |
| Guardrails | pass, review, block or route |

TypeSafe says Jev is not a replacement model for a coding agent: the agent writes code that calls Jev.

## 3. Tools

### Official, from TypeSafe

| Name | Language | License | Covers | Checked |
|---|---|---|---|---|
| typesafe-sdk 0.7.2 | Python | MIT | sync and async clients, retries | read |
| @typesafe-ai/sdk 0.6.0 | JS (npm) | MIT | `choice()`, `noul()`, `score()` | read |
| skills | agent skill | MIT | Claude Code plugin; teaches the agent to write Jev code | read |
| system-one-adapter | Python | MIT | same client backed by other models, for comparison | read |
| n8n-nodes-typesafe-ai | JS (npm) | MIT | n8n node | read |

No weights, no training code, no CLI, and no Rust, Go or Clojure SDK from TypeSafe.

### Rust clients (all unofficial)

| Name | License | Covers | Checked |
|---|---|---|---|
| typesafe-system-one 0.1.1 | MIT | System One; OpenRouter base URL documented | read |
| typesafe-sdk 0.2.0 | MIT | TypeSafe direct; most downloaded, about 1.2k | read |
| fuzzy-jev 0.6.0 | MIT | OpenRouter `alpha/decisions` | read |
| jev-driver 0.1.0 | Apache-2.0 | derive macros `JevChoice`, `JevScore`, `JevNoul` | read |
| jev 0.1.2 | see crate | TypeSafe plus self-hosted compatible servers | read |
| jevkit-cli 0.4.2, nu_plugin_jev 0.1.1 | see crate | a CLI; a Nushell plugin | read |

### Other languages

| Language | Name | License | Covers | Checked |
|---|---|---|---|---|
| JS (npm) | @patdown/jev 0.9.0, jev-systemone 0.1.1 | see npm | Effect client; TypeSafe and Zen | read |
| Python | jev 0.3.0 | see PyPI | compiles a function into Jev questions | read |
| Go | typesafe-client, typesafe-sdk-go 0.2.0 | MIT | System One | read |
| Clojure | **none found** | — | — | searched |
| Others | Java, Kotlin, Swift, C#, Elixir, Ruby, PHP, C++ | mostly MIT | various | listed only |

Standalone CLIs: `@jev-harness/cli` (`jev ask`, `eval`, `jev-gate`), jev-axi, jev-kit, jev-repl.

## 4. Plugins

| Harness | Name | Language | License | Covers | Checked |
|---|---|---|---|---|---|
| Claude Code | fast-jev-compaction | — | MIT | Jev scores each tool call; about 7.4k stars | read |
| Claude Code | jev-router, jev-enforce, claude-x-jev, jevmem | — | — | routing, CLAUDE.md enforcement, memory | listed only |
| Claude Code, Codex, pi, OpenCode | jev-code 0.4.1 | — | MIT | tool; OpenRouter and Vercel | read |
| Claude Code, Codex, pi | jev-use 0.6.0 | — | MIT | hands silent steps to Jev | read |
| Codex | jev-codex-router, codex-systemone-router | JS (npm), — | — | per-turn model and effort | listed only |
| pi | pi-jev-auto-mode, pi-jev-guard and four more | JS (npm) | — | auto-approval, bash gating, subagent routing | listed only |
| OpenCode | opencode-jev-router, opencode-smart-reasoning and four more | JS (npm) | — | subagent routing, effort, shell permission | listed only |
| Herdr | jev-herdr | — | MIT | Jev picks model and effort for Claude Code agents; 0 stars | read |
| Any (MCP) | jev-mcp 0.13.0 | — | MIT | judgment tools; about 490 stars | read |
| Cursor | **none found** | — | — | — | searched |

| Framework | Name | License | Covers | Checked |
|---|---|---|---|---|
| Vercel AI SDK | @ai-sdk/typesafe-ai 3.0.12 | Apache-2.0 | first-party provider | read |
| LangChain | langchain-typesafe 0.0.1a3, @langchain/typesafe 0.0.2 | MIT | classifier; experimental router middleware | read |
| Effect | @effect/ai-typesafe 4.0.1 | — | provider | read |
| Mastra | mastra-jev-moderation | MIT | 9 of 9 hostile, 0 of 49 real blocked, per its author | unverified |
| Tracing | openinference-instrumentation-typesafe 0.1.0 | Apache-2.0 | OTel tracing of the TS SDK | read |
| Testing | jevkit-vitest, jev-shadow, Jev-Calibration | — | replay cassettes; shadow runs; recalibration | listed only |

Mastra's upstream processor was closed unmerged. No Langfuse or Helicone integration was found.

## 5. Infrastructure

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 410" width="700" font-family="sans-serif" font-size="13"><defs><marker id="j3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="410" fill="#fff"/><g font-weight="bold" text-anchor="middle" fill="#1b2230"><text x="115" y="24">Clients and plugins</text><text x="350" y="24">Gateways</text><text x="585" y="24">Models</text></g><g fill="#e3ecfb" stroke="#2b4a8b"><rect x="10" y="38" width="210" height="46" rx="6"/><rect x="10" y="92" width="210" height="46" rx="6"/><rect x="10" y="146" width="210" height="46" rx="6"/><rect x="10" y="200" width="210" height="46" rx="6"/><rect x="10" y="254" width="210" height="46" rx="6"/></g><rect x="10" y="308" width="210" height="46" rx="6" fill="#fdecea" stroke="#b23b3b" stroke-dasharray="5 3"/><g text-anchor="middle" fill="#1b2230"><text x="115" y="57">Official SDKs</text><text x="115" y="111">Rust crates</text><text x="115" y="165">Frameworks</text><text x="115" y="219">Harness plugins</text><text x="115" y="273">MCP servers</text><text x="115" y="327">Clojure client</text></g><g text-anchor="middle" font-size="11" fill="#3d4a5c"><text x="115" y="75">Python · TypeScript</text><text x="115" y="129">several, all unofficial</text><text x="115" y="183">AI SDK · LangChain · Effect</text><text x="115" y="237">Claude Code · Codex · pi · OpenCode</text><text x="115" y="291">jev-mcp and others</text><text x="115" y="345">none found</text></g><g fill="#e2f4e6" stroke="#2e7d32"><rect x="260" y="38" width="180" height="46" rx="6"/><rect x="260" y="92" width="180" height="46" rx="6"/><rect x="260" y="146" width="180" height="46" rx="6"/><rect x="260" y="200" width="180" height="46" rx="6"/></g><rect x="260" y="254" width="180" height="46" rx="6" fill="#f3efe0" stroke="#8a7a2b" stroke-dasharray="5 3"/><g text-anchor="middle" fill="#1b2230"><text x="350" y="57">TypeSafe direct</text><text x="350" y="111">OpenRouter</text><text x="350" y="165">OpenCode Zen</text><text x="350" y="219">Vercel AI Gateway</text><text x="350" y="273">Cloudflare</text></g><g text-anchor="middle" font-size="11" fill="#3d4a5c"><text x="350" y="75">v1/systemone</text><text x="350" y="129">alpha/decisions · v1/systemone</text><text x="350" y="183">also a free jev-1.13-free</text><text x="350" y="237">typesafe-ai/jev</text><text x="350" y="291">unverified</text></g><rect x="480" y="38" width="210" height="100" rx="8" fill="#fdf0d8" stroke="#b07a12"/><text x="585" y="78" text-anchor="middle" font-weight="bold" font-size="15" fill="#1b2230">Jev 1.13</text><text x="585" y="98" text-anchor="middle" font-size="11" fill="#3d4a5c">TypeSafe · closed, no weights</text><g fill="#ece6f7" stroke="#5b3f99"><rect x="480" y="160" width="210" height="46" rx="6"/><rect x="480" y="214" width="210" height="46" rx="6"/><rect x="480" y="268" width="210" height="46" rx="6"/></g><rect x="480" y="322" width="210" height="46" rx="6" fill="#f3efe0" stroke="#8a7a2b" stroke-dasharray="5 3"/><g text-anchor="middle" fill="#1b2230"><text x="585" y="179">Clef, Clef-flash</text><text x="585" y="233">Local servers</text><text x="585" y="287">Open replicas</text><text x="585" y="341">OpenAI Decision API</text></g><g text-anchor="middle" font-size="11" fill="#3d4a5c"><text x="585" y="197">Cloudflare · open weights</text><text x="585" y="251">Ollaya · llama-system1 · AnyJev</text><text x="585" y="305">SemIf-OpenJev · NanoJev · jeff</text><text x="585" y="359">on Luna · announced</text></g><g stroke="#333" stroke-width="1.5" fill="none" marker-end="url(#j3)"><line x1="220" y1="190" x2="258" y2="190"/><line x1="440" y1="61" x2="478" y2="70"/><line x1="440" y1="115" x2="478" y2="90"/><line x1="440" y1="169" x2="478" y2="110"/><line x1="440" y1="223" x2="478" y2="128"/></g><line x1="440" y1="277" x2="478" y2="190" stroke="#333" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#j3)"/><text x="350" y="396" text-anchor="middle" font-size="12" fill="#1b2230">Purple: open models speaking the System One shape. Dashed: unverified, absent or other shape.</text></svg>

*The landscape around the model: clients reach Jev through four gateways; open models copy its request shape.*

### Gateways

| Host | Model ID | Endpoint | Checked |
|---|---|---|---|
| TypeSafe | `jev-latest` | `api.typesafe.ai/v1/systemone` | read |
| OpenRouter | `typesafe/jev-1.13` | `/api/alpha/decisions` (alpha), `/api/v1/systemone` | read |
| OpenCode Zen | `jev-1.13`, `jev-1.13-free` | `opencode.ai/zen/v1/systemone` | read |
| Vercel AI Gateway | `typesafe-ai/jev` | AI Gateway | read |
| Cloudflare | `typesafe/jev` | AI Gateway, Workers AI | **unverified** |

That all hosts take the same request shape comes from one survey page: **unverified** per host.

### Local serving

Jev itself cannot be self-hosted. What exists is open models and servers that speak its shape.

| Name | Language | License | Covers | Checked |
|---|---|---|---|---|
| Clef, Clef-flash | model | Apache-2.0 | open weights, about 27B, 64k context, vLLM and Workers AI | read |
| JEV-27B-VL, JEV-9B, JEV-27B | model | see HF | community models; about 726k downloads | read |
| Ollaya | — | — | "Ollama for Jev-style decision models" | read |
| llama-system1 1.1.0 | JS (npm) | — | llama.cpp `/v1/systemone` shim | read |
| Laya servers | — | — | local Jev-compatible server; upstream gone | **unverified** |
| AnyJev, simple-jev, jev-bridge, lichen | mixed | Apache-2.0, MIT | any open model as a Jev endpoint | read |
| SemIf-OpenJev, NanoJev, kev, jeff | — | MIT | open replicas; SemIf on one 3090; jeff 0.8B, about 30 ms | read |

### Nix, limits, batching, caching

- **Nix.** No nixpkgs package. One flake, jev-nixos-setup: no license, 0 stars.
- **Rate limits.** The SDKs back off on 429 and 529; raw callers must do it themselves.
- **Batching.** Many questions on one state per call. No server-side batch API.
- **Caching.** None on the server. jevkit-vitest replays tests; jev-cache is experimental, 1 star.
- **Cache saving.** Only input is billed, so a cache saves only repeated input (the worker's inference).

## 6. Trending

Jev launched on 2026-09-15. Stars below are about three weeks of growth.

| Theme | Leading examples |
|---|---|
| Browser and computer-use agents | browser-use/jev-ultrafast (about 22k), jev-mcp |
| Coding-agent plumbing | fast-jev-compaction (about 7.4k), jevgrep (about 2.2k), the pi and OpenCode plugins |
| Open replicas and local models | SemIf-OpenJev (about 4.7k), NanoJev (about 2.5k), Clef, kev, Jeeves |
| Trading bots | jev-trader (about 2.8k) |
| Database predicates | pg-jev, DuckDB vgi-typesafe, MySQL `AILIKE` |
| Awesome-lists | more than 20, the largest about 2.1k stars |

- **Vercel.** "Nearly 13% of paid teams within 24 hours", per InfoQ (**unverified**).
- **OpenAI.** Announced a Decision API built on Luna.
- **Cloudflare.** Copied the API on purpose with Clef.
- **A wire format.** "System One" is becoming a protocol several vendors serve.

### Loudest criticisms

| Criticism | Where |
|---|---|
| "Can't hallucinate" is too strong: a confident, valid, wrong answer is possible | HN launch thread; InfoQ |
| Latency claims compare unlike work; no paper | HN launch thread |
| A strong classifier sold as a "frontier model" | HN; one review (**unverified**) |
| No weights, no paper, prior open work uncredited | Towards Deep Learning; arcturus-labs |
| A new vendor receives your data | HN |

Open problems: forced choice on ambiguous items (**unverified** study), unstable limits, weak non-English accuracy,
prompt injection through state, first-option bias, OpenRouter's endpoint still alpha.

## 7. Rulings

1. **Which client or gateway to evaluate first.** By witness, as the Jev agreement holds: one offline fixture per candidate,
   then one minimal live call each, pinned to `jev-1.13`, once the key exists.
   (a) typesafe-system-one over OpenRouter `v1/systemone`. The flow's recommendation: the agreement's smaller surface.
   (b) fuzzy-jev over OpenRouter `alpha/decisions`.
   (c) typesafe-sdk (Rust) against TypeSafe direct.
   (d) jev-driver's derive macros over any of the above.
   (e) OpenCode Zen, with its free `jev-1.13-free`.
2. **Whether to pursue local serving.** The report found Clef, the JEV community models, Ollaya, llama-system1 and AnyJev.
   (a) Not yet: witness the public gateway first. The flow's recommendation.
   (b) Try llama-system1 on the proposed Prometheus llama.cpp router with an open decision model.
   (c) Try Clef on vLLM.
3. **Whether this book becomes a standing report.**
   (a) Yes, renewed monthly from fresh registry and thread reads. The flow's recommendation: the scene moves daily.
   (b) Renewed only when you ask.
   (c) No; this edition stands alone.

## Sources

- TypeSafe docs: docs.typesafe.ai (api, models, primitives, jaggedness, coding agents, agent skill); github.com/typesafe-ai
- Registries: crates.io, npm, PyPI, Hugging Face, GitHub search, HN Algolia
- Gateways: opencode.ai/docs/zen, vercel.com/i/jev-integrations, openrouter.ai/typesafe/jev-1.13, blog.cloudflare.com/clef-decision-models
- Frameworks: ai-sdk.dev typesafe-ai provider, docs.langchain.com typesafe provider
- Press: InfoQ, flaviocopes.com/jev, jev-ai.org, awesome-typesafe-jev, The New Stack
- Our records: the provider plan, the Jev reuse audit, the census of Herdr, the messenger and OpenCode logs, his Jev records
<!-- to-the-living:end -->
