# Do LLMs write Clojure/Lisp well, and does homoiconicity help? (2026 evidence check)

Prompted by the living's claim: "AI is really good at Clojure because of how Lisp is homoiconic." Below, measured evidence is kept separate from argument/opinion, with a source for each claim.

## 1. Benchmarks: Clojure/Lisp vs Python/TypeScript

**Measured, but thin and not favorable to the "good at Clojure" claim:**

- MultiPL-E (the standard multilingual code-gen benchmark, extending HumanEval/MBPP) does include Clojure among its ~18-22 target languages, alongside Racket (a Scheme-family Lisp), Python, TypeScript, and others. (nuprl.github.io/MultiPL-E; arxiv.org/abs/2208.08227)
- However, the public MultiPL-E leaderboard (llm-stats.com/benchmarks/multipl-e) reports only aggregate cross-language scores, not a per-language breakdown for Clojure vs. Python/TypeScript. I could not find a 2025-2026 published per-language table that isolates Clojure or Racket performance. This means the specific comparative number the living is implicitly asking for ("is Clojure a language LLMs are unusually good at?") is **not established by any benchmark I could find**.
- What *is* documented, repeatedly, as measured/observed behavior rather than benchmark score: LLMs frequently hallucinate nonexistent Clojure functions/vars, a problem attributed to Clojure's small share of training data relative to Python/JS/TS. This is stated as an empirical observation project maintainers built tooling to fix, not a formal benchmark, but it is a converging practitioner report, not just one person's opinion. (github.com/ruped/clojurellm-data; mccormick.cx/news/entries/advantages-of-generating-clojure-with-llms; iwillig.me one-year report)
- General low-resource-language-for-code literature (not Clojure-specific) confirms the mechanism: models perform worse on languages under-represented in pretraining corpora, and low-resource fine-tuning/distillation is an active research area. (arxiv.org/pdf/2410.03981 "Survey on LLM-based Code Generation for Low-Resource... Languages"; arxiv.org/pdf/2308.09895 "Knowledge Transfer from High-Resource to Low-Resource... Languages")

**Verdict on this point:** the evidence that exists points opposite to the living's framing — Clojure is a smaller-corpus language and LLMs do worse on raw generation of it than on Python/TypeScript due to data scarcity, not better because of Lisp-ness. No credible 2025-2026 benchmark shows Clojure/Lisp outperforming Python/TypeScript for LLMs.

## 2. Does homoiconicity / s-expression regularity plausibly help?

**No experimental validation found. What exists is argument, not measurement:**

- A 2025 arXiv paper, "From Tool Calling to Symbolic Thinking: LLMs in a Persistent Lisp Metaprogramming Loop" (arxiv.org/abs/2506.10021), argues homoiconicity gives LLMs "easily parseable and manipulable structures" and that Lisp's minimal, regular syntax lets a model spend its capacity on semantics rather than parsing irregular grammar. **The paper states this explicitly about itself: "This paper presents a conceptual framework intended to guide future implementations rather than report experimental results."** and "this design remains conceptual and has yet to be implemented or empirically validated." This is the single most direct source on the homoiconicity-helps-LLMs idea, and it is openly speculative.
- Older, pre-LLM writing on homoiconicity and program synthesis (SIGPLAN blog, 2020; Wikipedia; various blog essays) argues the same general point — code-as-data makes Lisp a natural target for program synthesis/metaprogramming — but predates LLM-era practice and is philosophical/pedagogical, not measurement of any model.
- On the specific, narrower claim "regular parens reduce syntax errors": this is contradicted by practitioner reports on the *opposite* known failure mode — LLMs frequently produce **unbalanced parentheses** when writing Lisp/Clojure, described as "the notorious parenthesis problem." Tooling exists specifically to patch this failure (auto-repair of delimiters via parinfer/cljfmt-style tools, e.g. "brepl", clojure-mcp's built-in delimiter repair). That such fix-up tooling is considered necessary and widely used is itself evidence that paren balancing is a real, common LLM weakness in Lisp — not a strength conferred by regular syntax. (github.com/bhauman/clojure-mcp; search results referencing "brepl" and parenthesis-repair hooks)
- Token efficiency: mentioned in an HN discussion and by Chris McCormick's blog post as a plausible advantage — Clojure's conciseness could mean more information per token, aiding limited context windows — but neither source offers a token-count comparison or benchmark; both are argument/anecdote. (mccormick.cx article; HN thread "LLM coding workflow going into 2026")

**Verdict on this point:** homoiconicity-helps-LLMs is a real, circulating hypothesis among Lisp-adjacent researchers and practitioners, but as of September 2026 it has zero empirical validation that I could find. The one paper making the argument explicitly disclaims having tested it. Meanwhile the most concrete, repeatedly-reported *symptom* in this space (unbalanced parens) runs counter to the "regular syntax reduces syntax errors" version of the claim, and needed dedicated tooling to control.

## 3. REPL-driven agent loops and tooling: this is where the real, measured-ish wins are

This is the strongest part of the story, and it's about **tooling and workflow**, not language syntax per se:

- **clojure-mcp** (github.com/bhauman/clojure-mcp) is an MCP server giving agents a live nREPL connection plus Clojure-aware structural editing (`clojure_edit`, sexp-level replace), automatic delimiter repair before evaluation, and cljfmt/clj-kondo-style validation. Its own documentation frames this as directly reducing hallucination and syntax breakage by grounding generation in REPL feedback rather than blind text generation.
- **Practitioner report at real scale** (Ivan Willig, "One year of LLM usage with Clojure," iwillig.me, Feb 2026; also github.com/iwillig/awesome-clojure-llm): a team working a 250,000-300,000 line Clojure codebase with an LLM-based agent (Korey) reports that adopting Clojure MCP "greatly reduced AI hallucinations" and prevented invalid-paren code from landing, and that REPL-driven exploration (using `clojure.repl/dir`, `doc`, `source` to let the model inspect live library state) worked better than maintaining static "skill" docs. This is a first-person operational report, not a controlled experiment, but it is concrete and it's the only quantified-ish, at-scale data point I found on this whole question.
- The same report is explicit that Clojure/Lisp starts from a *disadvantage* in raw model familiarity (Python/JS/TS dominate pretraining), and that the REPL/tooling loop is what closes the gap — it argues you shouldn't abandon a language just because a model is statistically less fluent in it, since tools can compensate. That is an argued position, not a benchmarked one.
- Other Clojure-specific agent tooling exists (Calva Backseat Driver, hugoduncan's clojure-repl-mcp, Gaiwan's MCP SDK, the "Mycelium" LLM-coding framework) showing an active 2025-2026 ecosystem building around the REPL-as-agent-loop idea — this is evidence of investment/interest, not evidence of superior outcomes vs. Python tooling (whose agent ecosystem — LangChain, AutoGen, CrewAI, LangGraph — is far larger).
- **clj-kondo** and **cljfmt** are used inside these tool loops as linting/formatting safety nets that catch and often auto-fix the errors models do make; **Babashka** shows up as a fast-starting Clojure runtime useful for scripting/agent tasks but I found no direct claims tying it to LLM effectiveness specifically. **Malli** did not surface in any source discussing LLMs or agent tooling at all — no evidence found either way; this is a gap, not a null result.

## Bottom line, stated plainly

- **Measured/benchmarked:** Clojure is included in MultiPL-E, but no found benchmark shows it outperforming Python/TypeScript for LLMs; the low-resource-language literature and multiple practitioner reports instead document Clojure as *harder* for raw generation due to smaller training corpus, and paren-imbalance is a named, tooled-around failure mode.
- **Argued/opinion, not measured:** that homoiconicity or s-expression regularity helps LLMs — the one paper making this case (arXiv 2506.10021) explicitly says it is conceptual, untested. Token-efficiency-from-conciseness is plausible but unquantified.
- **Real and reasonably well-evidenced (practitioner-scale, not benchmark-scale):** REPL-driven agent loops via clojure-mcp-style tooling measurably reduce hallucination and syntax breakage in practice, per a large-codebase, year-long usage report. This is a tooling/workflow win, not a language-intrinsic "Lisp-way-of-thinking" win — the same report frames it as compensating for a training-data disadvantage, not exploiting a homoiconicity advantage.

**Recommendation for the living's proposal:** the case for using Clojure/EDN-like data languages (Ethos, Protos, Datom) to "keep models in the Lisp way of thinking" is not supported by current benchmark evidence and rests on an explicitly speculative paper plus plausible-but-unverified arguments about conciseness and REPL loops. The one solid, repeatable finding is that a live REPL + structural-edit + auto-repair tool loop (clojure-mcp pattern) meaningfully helps agents work in Lisp-like languages despite the models' underlying data disadvantage — so if EDN-like formats are adopted, investing in equivalent tooling (structural editors, delimiter repair, live evaluation) would matter far more than any claimed intrinsic homoiconicity benefit.

## Sources

- https://nuprl.github.io/MultiPL-E/
- https://arxiv.org/pdf/2208.08227 (MultiPL-E paper)
- https://llm-stats.com/benchmarks/multipl-e
- https://github.com/ruped/clojurellm-data
- https://mccormick.cx/news/entries/advantages-of-generating-clojure-with-llms
- https://arxiv.org/pdf/2410.03981 (Survey on LLM-based Code Generation for Low-Resource and Domain-Specific Programming Languages)
- https://arxiv.org/pdf/2308.09895 (Knowledge Transfer from High-Resource to Low-Resource Programming Languages for Code LLMs)
- https://arxiv.org/html/2506.10021 (From Tool Calling to Symbolic Thinking: LLMs in a Persistent Lisp Metaprogramming Loop)
- https://blog.sigplan.org/2020/03/25/homoiconicity-lisp-and-program-synthesis/
- https://en.wikipedia.org/wiki/Homoiconicity
- https://github.com/bhauman/clojure-mcp
- https://www.iwillig.me/blog/one-year-of-llm-usage-with-clojure/
- https://github.com/iwillig/awesome-clojure-llm
- https://news.ycombinator.com/item?id=46570115 (LLM coding workflow going into 2026)
- https://news.ycombinator.com/item?id=47196763 (Mycelium: a Clojure framework designed to facilitate LLM coding)
- https://news.ycombinator.com/item?id=48287184 (live Clojure REPL discussion)
- https://www.freshcodeit.com/blog/llm-agents-in-clojure
- https://github.com/babashka/babashka
