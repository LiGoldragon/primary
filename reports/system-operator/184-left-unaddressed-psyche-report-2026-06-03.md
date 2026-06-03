# Left unaddressed — short psyche report — 2026-06-03

## What is now closed

The Ghostty-to-editor problem is closed at the practical layer. Clean `file://` links, chooser fallback, VSCodium-as-default, and dirty plain-path terminal links now route to Codium after the latest CriomOS-home/CriomOS pushes and Home activation.

## Still unaddressed

1. **Primary history hygiene.** Commit `597060b18a73` (`system-operator: record VSCodium editor default`) still needs audit because it appears tied to the `push-privacy-access-gate-2026-06-02` branch and may have combined unrelated privacy/access-gate work with the system-operator report update. Current Primary `main` has moved forward, but the branch/commit still needs explicit repair or confirmation.

2. **Prometheus local AI toolkit finishing pass.** The durable prefetch completed with no failures, but the results still need to be mined: collect full SRI hashes/store paths, select only llama-router-compatible GGUF winners, add those winners to `CriomOS-lib/data/largeAI/llm.json`, and keep Parakeet/Qwen embedding-reranker/FLUX out until their runtimes are designed.

3. **Remaining Gemma quant checks.** Gemma 4 is usable through Prometheus llama.cpp, Pi, and browser-use, but the remaining quantized variants still need direct runtime tests: the 26B Q8, 31B Q4, and 31B Q8 variants.

4. **Browser live-tab automation.** The Playwright Extension path is selected for supervised real-account work, but the harmless selected-tab prototype and CriomOS-home wrapper are not done.

5. **Cloud/domain Cloudflare work.** The prototype direction remains blocked by no live token and incomplete provider work: redirect read/write still needs Cloudflare Rulesets/Page-Rules implementation, and the full runtime still needs persistence growth, actor split, nonblocking provider actors, and daemon-to-daemon projection handoff.

6. **Spirit-next production handover test.** Bead `primary-jew3` (Spirit-next production-copy handover acceptance test) remains open.

7. **Optional editor jump-to-line emitter.** The opener can now handle common dirty `:line[:column]` paths, but a fully reliable link-to-line experience should still be solved at the emitter layer with editor-specific URLs when desired.

## Psyche-facing shape

The system-operator thread is no longer blocked on the editor-link issue. The next highest-value cleanup is the Primary history audit, because it protects the workspace record. After that, the work naturally splits into three fronts: Prometheus local-AI completion, browser selected-tab proof, and cloud/domain runtime/provider continuation.
