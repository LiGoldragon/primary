# Live code tools versus text search — bounded measurements

2026-11-19. Task l0mm; researchTools 6ac03a. **Six measured pairs, twelve fresh native Codex sessions, on Flow and Lojix. No consistent saving across tools or corpora.** The live language server worked, but its call hierarchy remained partial; text reads supplied the missing relationships. This replaces the earlier zero-result interim record.

## Scope and method

- Same immutable corpus, question, native provider/model/effort and fifteen-minute allowance within each pair; controls first, sessions sequential, no resumed histories. Native receipts verify OpenAI `gpt-6-luna`, `xhigh` throughout. This follows the current Luna/xhigh constraint rather than the older Medium plan.
- Native reads/listing/text search in every arm. Separate treatments: live LSP for tracing; ast-grep outline for overview; fixed ranked map for overview. Four frozen questions and eight compound fact units per question. No answerer received the key or another answer.
- The host was Ouranos, following Opus 5hnk’s local-measurement instruction. Sources were chmod read-only archives; all 277 Flow and 72 Lojix source blobs still match their published git objects after the trial. Isolation was explicit tool policy, **not an OS sandbox claim**: measured sessions used the functioning full-access runner. Call audits found no oracle reads or web calls.

| Corpus | Published revision | Rust files / lines |
| --- | --- | ---: |
| Flow | `a044e39ac2bc19cdcd3d435c75448d8697c6a17d` | 199 / 145,715 |
| Lojix | `5d75a4032079cd942a3d4f5ba676da9ade5e8249` | 44 / 28,805 |

Lojix was the previously frozen second active corpus, chosen for repeated method names and explicit Kameo admission/completion hops. It is **smaller than Flow**, including generated/historical Rust in the counts. These measurements therefore cover the approved Flow/Lojix matrix, not the literal larger-than-Flow condition in the original brief.

## Measured figures

Seconds include native answerer startup, retrieval, reasoning and final answer; they exclude package acquisition, map generation and analyzer startup/indexing. Native input counts are cumulative across model calls, including repeated context; cached input is a subset, not an additional count. Output includes reasoning. Tool text is counted once per emitted text block with `tiktoken 0.12.0` / `o200k_base`: a reproducible **proxy**, not a verified tokenizer for this native model. It includes tool envelopes and the common instruction-file read.

| Corpus / comparison | Arm | Seconds | Native input | Cached input | Native output | Tool-text proxy | TP / FP / FN |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Flow / lsp | control | 193.7 | 302,902 | 251,776 | 9,965 | 20,403 | 8 / 0 / 0 |
| Flow / lsp | tool | 688.8 | 604,246 | 557,056 | 18,803 | 32,607 | 7 / 0 / 1 |
| Flow / outline | control | 273.5 | 1,581,241 | 1,472,640 | 13,891 | 89,743 | 4 / 0 / 4 |
| Flow / outline | tool | 258.2 | 1,257,774 | 1,154,688 | 13,176 | 84,255 | 4 / 1 / 4 |
| Flow / map | control | 254.6 | 791,330 | 702,720 | 13,265 | 76,823 | 4 / 0 / 4 |
| Flow / map | tool | 282.8 | 961,428 | 847,872 | 14,956 | 99,297 | 6 / 0 / 2 |
| Lojix / lsp | control | 180.7 | 244,296 | 206,080 | 9,317 | 28,378 | 8 / 1 / 0 |
| Lojix / lsp | tool | 308.8 | 733,920 | 656,896 | 16,087 | 49,622 | 8 / 0 / 0 |
| Lojix / outline | control | 192.3 | 561,276 | 470,784 | 10,033 | 52,532 | 6 / 0 / 2 |
| Lojix / outline | tool | 280.7 | 1,087,890 | 978,176 | 14,484 | 63,823 | 6 / 0 / 2 |
| Lojix / map | control | 230.0 | 809,207 | 723,328 | 11,822 | 73,872 | 6 / 0 / 2 |
| Lojix / map | tool | 221.8 | 1,113,378 | 916,992 | 11,248 | 91,878 | 6 / 1 / 2 |

### Paired differences

| Corpus / tool | Time change | Tool-text change | Correct key units |
| --- | ---: | ---: | --- |
| flow-lsp | +255.5% | +59.8% | 8 → 7 / 8 |
| flow-outline | -5.6% | -6.1% | 4 → 4 / 8 |
| flow-map | +11.1% | +29.3% | 4 → 6 / 8 |
| lojix-lsp | +70.9% | +74.9% | 8 → 8 / 8 |
| lojix-outline | +46.0% | +21.5% | 6 → 6 / 8 |
| lojix-map | -3.6% | +24.4% | 6 → 6 / 8 |

Precision is TP/(TP+FP); recall is TP/8. Exact ratios, per-unit masks, answers, prompts, native session IDs, receipt paths and transcript hashes are in [the results dataset](live-code-tools-results.json).

## Correctness adjudication

The original key was manually source-audited, not independently audited. Each compound unit receives credit only when its required relationships are stated; a citation alone does not supply an omitted relationship. Correct extra facts earn no extra recall; labelled unknowns earn no false positive. The low overview recall is partly this strict compound-unit rule, not a claim that the whole answer is wrong.

**Oracle correction:** The frozen question and key call the owner helper Daemon::submit_deploy. At this revision it is RequestServable::submit_deploy implemented for RequestWorker (daemon.rs:102-108,452-475,548-561). Daemon holds configuration. Both Lojix tracing arms corrected the premise. Unit 1 is scored against the actual receiver and unchanged signature, not against the mistaken name. The original frozen key remains unchanged and is retained in the results dataset.

- Flow tracing: control covers all eight units. Final LSP answer omits the two `sent_by` implementation bodies (unit 2), although it identifies both implementers.
- Flow outline/control and map/control: units 1, 2, 7, 8 credited. Units 3–6 are incomplete: reply decoding/textualization; explicit authenticated-peer forwarding to `send_request`; full receiver/trait/gate relationship; and payload-budget enforcement. Outline/control mentions the gate, but still leaves the compound receiver/trait unit incomplete.
- Flow outline/tool has the same credited units plus one false claim: `wake_due` acts only for asleep recipients. `waking.rs:1616` first calls `drain_awake`. Flow map/tool additionally states the adapter forwarding and payload-budget relationships, earning units 4 and 6.
- Both Lojix tracing answers cover all eight corrected units. Control adds an unsupported guarantee that the accepted handle returns before pipeline effects run; `daemon.rs:710–718` spawns before the actor reply and establishes no such ordering.
- All four Lojix overview answers earn units 1, 2, 3, 4, 6, 7. They omit `UnexpectedFrame` on actor ask failure (unit 5) and the specifically saturating decrement (unit 8). Map/tool additionally assumes the client already holds the identifier when the pipeline finishes; reply-before-completion is not guaranteed.

## What the tools established

**Live rust-analyzer:** manually started temporary stdio servers with a small Unix-socket client. Both measured tool arms invoked definition, implementation, hover, workspace symbols and recursive outgoing hierarchy. Flow’s hierarchy confirmed Request-to-Message measurement but omitted source-visible projection/serialization edges. Lojix’s tree reached `ActorRef::ask`; source types and `Message<AdmitDeploy>` establish the handler hop, not a direct call edge. Both arms continued with source reads.

Analyzer: pinned nixpkgs `0e251e24a4f24e036a084b6b4b2d2491af4167f4#rust-analyzer`, version `2026-06-15`, artifact `/nix/store/vhm51xj9fmy2i7bz2z0i8y89arrmh72y-rust-analyzer-2026-06-15`. Toolchain: Flow’s locked build-base `4ea69d1fc87c95e7c1f54d02b21166ffb3285edd#toolchain`, artifact `/nix/store/m3avjwfs2crh6gk1xy2aky9k52nd0ham-rust-stable-with-components-2026-10-15`.

Initialization disabled check-on-save, checks, build scripts, procedural macros and cache priming; two analyzer threads, target directories in scratch. Offline reconnaissance lacked dependencies; the measured servers loaded Cargo metadata online and reported healthy/quiescent. Cargo’s dependency cache was populated; source archives stayed unchanged. This is limited semantic coverage, especially for generated/procedural information. Settings follow [rust-analyzer’s initialization documentation](https://rust-analyzer.github.io/book/configuration.html).

**Outline:** installed Nix ast-grep `0.51.0`, `ast-grep outline -l rust --items structure --color never PATH`; no rewriting.

**Ranked map:** Nix-built Python tool `/nix/store/kw4dbzhnzdk6xciz72lbxbc1pbizadcg-ranked-rust-map`, built on Prometheus with no Node. It obtains ast-grep definitions, forms a lexical symbol-reference file graph, applies PageRank (40 iterations, damping 0.85), and includes whole-file outlines that fit a fixed 16,000-byte budget. Maps are 16,000 / 15,974 bytes, or 4,282 / 4,027 o200k proxy tokens. This is a simple equivalent of [Aider’s graph-ranked map concept](https://aider.chat/docs/repomap.html), not Aider itself or a resolved call graph. No question-specific ranking or tuning after answers.

## Failures, replacement policy and cleanup

Seventeen native sessions were attempted: twelve retained, five excluded for infrastructure failures. Two initial read-only runners could not execute any source reads because bubblewrap was absent. Two tool arms lost their server to a faulty completion watcher. A Flow replacement exposed missing-position handling in the first client and terminated that server. Those failures remain in the dataset; the client now validates query variants and positions, and the final replacement was fresh with the identical question/grant prompt. Controls were retained; no arm was chosen by its score or speed. The corrected Flow arm is consequently an integration measurement of the revised client, and replacement/order effects further limit causal comparison.

The two early server stops and the first-client crash were defects in this experiment’s harness, not evidence that rust-analyzer failed. An orchestration cleanup command also exited nonzero when it tried to stop an already-ended Flow server; explicit final cleanup handled the remaining servers.

**Cleanup verified:** seven manual analyzer starts, all seven server logs end with clean analyzer exit 0; all server sessions have ended and both runtime sockets are absent. No service, profile installation, mount or synchronizer was added. The exposed analyzer/Cargo/rustc exit-126 wrappers remain unchanged; the trial used explicit temporary package paths. Nix outputs are unlinked store artifacts. Scratch remains at `/tmp/research-tools-6ac03a.A0E7wt`; it is temporary. Published source revisions, full answers, original key, erratum, map outputs and tool sources are retained in the results dataset; native transcripts remain at the recorded persistent paths.

## What one pair can and cannot show

Each cell shows one observed workflow with this model, prompt, corpus, client and host state. It cannot estimate variance, establish statistical significance, separate model sampling from tool causation, measure cold-start total cost, or generalize to other repositories or models. Controls always ran first; caches and the busy host were not randomized. Shared-server concurrency, filesystem alternatives, freshness after edits, compiler/proc-macro completeness and power-cut durability were not measured.

Observed trade-offs: Flow outline was about 6% faster with about 6% less emitted tool text, but added a false claim. Flow ranked-map retrieved more key relationships at greater time/text cost. Lojix ranked-map was about 4% faster with more tool text and an unsupported ordering claim. Both live-LSP cells were slower and emitted more tool text than their controls. This study supports no general default-tool change.

## Draft knowledge — bounded by these results

Use a live semantic query for a precise definition, implementation or inferred type, then verify the relationship in source. Treat a partial outgoing hierarchy as partial: Flow’s projection/codec chain and Kameo actor dispatch still required source reasoning here. Use an outline or fixed ranked map as a navigation aid, not as proof of runtime order or a call graph. Retain text search and exact source ranges. No command demonstrated a repeatable saving across both corpora in this small trial.
