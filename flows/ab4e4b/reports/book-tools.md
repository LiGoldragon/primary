# Book authoring implementation — 18zt

**Superseded disposition:** Fable rejected adoption after reading the preview (ukke/zl75). Main remains fd83f44 only. My isolated source/docs commits below were returned to uncommitted changes at his instruction; their historical test evidence is retained, not an adopted grammar. See `flows/ab4e4b/alternatives-difference.md`. No alternatives publication was requested. The actual earlier publication is now recovered: all three diagrams were visible, but the preview freshly redrew their SVGs; preserved Mermaid text does not mean identical illustrations. The difference account quantifies both the card changes and the changed figures.

## Custody and revisions

The original commits and foreign work are preserved. Changes are local; no push, deployment, or generated skill/manifest edit was made.

- Tools: `flow-ab4e4b-book-tools`, **b9e8ae097463793d62f720d207500b25af16deec**, worktree `/tmp/book-ab4e4b.gqmYkw/tools`.
- Authored knowledge: `flow-ab4e4b-book-knowledge`, **0151579df73b0b9f27ab3153362db7eaebde72a5**, worktree `/tmp/book-ab4e4b.gqmYkw/mind`; only `knowledge/book/0.md` changes from the predecessor.
- Separate urgent r2tc fix: local makeshift-tools **main fd83f4431e392b57389847565ca80e9ed7a98971**, worktree `/tmp/book-ab4e4b.gqmYkw/removed-main`. Only the removed-only Ethos correction and its regression were landed on main. It is merged into the authoring branch without rewriting predecessor commits. Psyche book Haiku and Psyche core Opus were notified; r2tc answered `Sent.al27`.

## Implemented shape

`python3 book-tools.py` remains the entry point and delegates to `book-tools.clj`, beside the existing checker/builder. Start and Edit use the actual module reader, description parser, view boundaries and checker.

- Start writes a **draft Proposal**, title and complete authenticated module views/descriptions. The draft parses; publication still refuses `missing-proposal` until a change exists. No Account conversion or kind switch occurs.
- Edit accepts a selected module and exact unique anchor, with stdin text for `--after` or `--replace`. Replacement preserves surrounding words and displays ordinary removed/added lines. Missing/duplicate anchors identify the anchor and view. Refusals preserve the source, and accepted writes are atomic. Other views remain byte-identical. Empty/no-op replacements are refused. A fenced-code anchor rewrites its enclosing fence through the same ordinary marks; two-space context lines retain exact current paragraph breaks. Markdown module views are supported; non-Markdown edits are explicitly refused.
- A set is `### Proposal N alternatives: question · repo › path`, with `#### Alternative A: title` cards. Every card body is checked through the **ordinary proposal grammar**, including additions, removals, replacements, context and comments. Review kind is retained. Unique consecutive letters, at least two options and nonempty cards are checked. The command supports ordinary signed bodies as well as one-line additions.
- A neutral enclosure and letter identify the set. Inner margins retain their ordinary meaning/colours. Cards stack on a phone and form a grid on a wider screen. There is no alternatives change colour.
- Authored knowledge documents the commands, grep-based anchor workflow, draft/publication distinction, source grammar and the separately ruled removed-only Ethos behavior. `modules.datom` and generated skill trees are untouched.

## Evidence

The final gate ran on Prometheus from an archive of committed tools revision b9e8ae0: `/tmp/book-ab4e4b-b9e8ae0`. **All eight files passed: 164 tests, 1,254 assertions, exit 0.** Log: `/tmp/book-ab4e4b.gqmYkw/committed-gate.log`, SHA256 `1e98a9d351a1bd66fc89d45df9c3bacf77e2e6da7ebc39e05bdb0fd7b5a2e981`.

The gate is `bb test`, with Chromium `/nix/store/ibmk5b6m5p95q0mkgx1b7zg3a1wwggyz-chromium-157.0.8103.38/bin/chromium` selected through its existing `CHROMIUM` interface. Prometheus lacks the laptop's two grammar directories; the isolated gate's **configuration file only** points at copies under `/tmp/book-ab4e4b-grammars/tree-sitter-{ethos,dotos}`. Authored scripts are the committed files. Before these fixtures were supplied, missing highlighting/browser dependencies caused visible failures; none were counted as passes. An existing checker test's network dependency was replaced with its explicit module fixture, and the obsolete assertion forbidding alternatives styles now checks the ruled enclosure/ordinary-margin behavior.

New author fixtures cover multiple modules, both edit modes, missing/duplicate anchors, atomic refusal, no-op replacement, descriptions, group validation, signed card replacements, Review cards, multiline stdin, CRLF modules and unlabelled/backtick/tilde code fences. New Chromium fixtures check 390px and 1200px, dark/light, letters, wrapping, ordinary font size, replacement marks, neutral enclosure and grid alignment. Existing phone/theme/static/checker/builder gates also pass.

The real Python CLI additionally started and edited a temporary view of actual origin-main `mind-belief › knowledge/book/0.md`; the real standalone checker accepted the edited source. Receipt: `/tmp/book-ab4e4b.gqmYkw/live-reader.log`.

Independent Luna testing of a content-addressed intermediate snapshot found a genuine fenced-code-anchor gap: the command safely refused the result because a heading had been inserted inside code. That gap was fixed and received six real-checker/builder combinations covering both modes and three fence forms. CRLF draft normalization itself was sound.

## Exact example and before-landing preview

Converted source: `/home/li/primary/flows/ab4e4b/proposals/balancing-alternatives.md`. Its three figure assets are beside it in `figures-balancing-alternatives/`, supplied by Psyche book Haiku. The original `flows/655f27/proposals/balancing-alternatives.md` is untouched.

Rendered preview: **`/tmp/book-ab4e4b.gqmYkw/balancing-alternatives.html`**, SHA256 `d7a2b013a8171d6853c7c952f6608d2060b948ed151db99774a23c95577eb13f`. It was built and handed to Psyche core Opus (`Sent.58d1`) and Mind core Sol **before the authoring commit**. The exact committed builder rebuilt it with identical bytes afterward.

A source-preservation oracle confirms the four question titles, all fourteen option bodies and all three Mermaid fences are unchanged; only their grouping/lettered presentation changed. Evidence: `/tmp/book-ab4e4b.gqmYkw/example-preservation.json`. The actual preview DOM contains four sets, fourteen cards and three figures. At 390px it has no horizontal overflow; at 1200px it uses a two-column grid. Both screenshots were visually inspected: `/tmp/book-ab4e4b.gqmYkw/preview-390.png` and `preview-1200.png`; DOM receipt `preview-check.log` is alongside them.

The exact Fable page named by r2tc, `flows/d6c615/proposals/belief-nexus-0.md`, also builds with its existing figures after the separate main fix. Render: `/tmp/book-ab4e4b.gqmYkw/belief-nexus-0.html`; gate evidence `removed-grammars-tests.log` records 96 tests / 506 assertions passing. Publication remains the bookmaker's responsibility.
