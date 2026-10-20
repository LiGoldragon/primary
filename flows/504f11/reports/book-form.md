# The new book form: what book-build.clj and book-check.mjs expect

Read-only survey, 2026-10-17. Sources: `tools/book-build.clj` (usage comment lines 1-23, `build`, ethos check lines 948-1076), `tools/book-build-test.clj`, `tools/book-check.mjs`, `tools/book-check.test.mjs`, `flows/804eb9/orders.md`, `flows/a275c0/log.md`.

Example book (most recent whole-module book that passes both tools, built with --ethos-zero, 13:26 on 2026-10-17): `/home/li/primary/flows/a275c0/books/03-nexus-vision-3.md` (html beside it). It passes `node tools/book-check.mjs` (I ran it: `{"checked":true,...}`). Other books modified today either carry prose (d68c82/63, 65, 66, 39bd0c/09) or are proposal-only with no module shown (804eb9/*, which the 804eb9 orders say should become module-whole).

The builder's usage text does NOT describe the new form; it still says "to-the-living form: Crystallization heading, `### Proposal N:`, `File:` lines". The authority for the form is book-check.mjs (which refuses the rest) plus the builder's code paths. `File:` lines are the retired form (checker: `file-line-in-body`).

## 1. Markup

### Book title and Presentation line
```
<!-- to-the-living:start -->            (optional for the checker; the end marker `<!-- to-the-living:end -->` also ends a shown module)
Presentation.{ «The Nexus: the vision, 3rd edition» }

# The Nexus: the vision, 3rd edition
```
- Presentation line first, exactly `Presentation.{ «Title» }` (checker regex `^Presentation\.\{ «[^»]*» \}$`, single spaces), before the `# ` title and before any module/proposal. The builder uses it as `<title>`; the line itself is not rendered. The `# Title` becomes `<h1 class="book-title">`; only one `# ` heading is allowed, before any module or proposal. No other text outside a module or proposal is allowed (`text-outside-proposal-without-module`; `heading-outside-proposal-without-module`). `>` quote blocks refuse (`quote-block-in-book`).

### A module shown whole
- Heading: `## <repo> › <path>`, `›` is U+203A with spaces. Example `## psyche-context › vision/nexus.md`.
- Checker restricts the location to `^(psyche-context|mind-context|field-context) › (spirit|intent|vision|knowledge|compensation|inquiry|role|raw)/NAME.md$`. A code module (`## flow › crates/x/a.rs`) outside a proposal is REFUSED by the checker (`heading-outside-proposal-without-module`, then `text-outside-proposal-without-module`; I tested this). The builder alone accepts any `## X › Y` heading (renders an `<article class="module">` sheet labelled "as it stands" with the path as a chip), so a code module is currently buildable but not checkable. Code is therefore shown (as the file will read) in the proposal's own fence, not as a whole module. Raise this with the owner if whole code modules are wanted.
- Body: the module's text, front matter (`---...---`) stripped, otherwise byte-for-byte equal (after trim) to `git show <origin main>:<path>` in `/git/github.com/LiGoldragon/<repo>`. Else `context-module-differs`; unreadable gives `context-module-unavailable`. It runs until the next `## Proposal`/`### Proposal` heading, the next `*-context › ` heading, or the end marker. The module's own headings (`## A Nexus is the whole`, `###`...) stay inside it and are demoted by the builder to h3/h4. Nothing of the book's own may follow it.
- Psyche-context vision module as rendered text: write the module's Markdown directly (raw, as in the example), or wrap it in ONE `markdown`/`md`/`text` fence (the checker unwraps a wrapper that is the whole module; the builder renders a first `text`/`markdown`/`md` fence in a `.md` module as HTML text, never a `<pre>`; test `markdown-is-rendered-as-text-never-a-pre`). The raw form is what the example uses. Markdown in a plain/`text` code block inside a proposal is refused (`markdown-in-code-block`).
- A code block inside the module (as in the example): an unlabelled fence. In a module view the builder types it: `ethos` if either ethos-zero accepts it, else `datom` if the text reads as a datom (balanced `{ [ < (` and «» with `;` comments), else it is a diagram and needs `fig-N.svg`. A labelled fence (```rust, ```ethos, ```clj) is code of that language.
- Several modules: repeat the `## repo › path` heading; each closes the previous sheet.

### The proposal under it
```
## Proposal N: <title> · <repo> › <path>
## Proposal N: <repo> › <path>
## Proposal N: <title> · <repo> › <path>, a new file
```
- `##` or `###` both pass; the location is required in the heading (checker regex `^Proposal \d+: (?:.+ · )?[^\s›·]+ › [^\s,]+(?:, a new file)?$`; otherwise `proposal-heading-without-location`). No `File:` line.
- Body: unfenced change lines, one sentence per line: `+ added line`, `- removed line` (sign, one space; the checker counts `^\+ \S`). A run of `-` lines is word-diffed against the `+` run after it (green/red). A context line is written with two leading spaces inside a ```text fence only. Every proposal must hold at least one `+ ` line or an Archive/Destroy line (`no-change-in-proposal`). End with `Ruling: land, amend, or reject.` (a book line the builder turns into a ruling card).
- Code changes: a labelled fence with signed lines (```rust, ```ethos, ```clj); lines over 52 columns refuse in code fences except `- ` lines (`code-over-52-columns`); in unfenced `+` prose there is no limit.
- Archive and Destroy: a paragraph that starts `**Archive** ...` or `**Destroy** <the quoted words>` inside the proposal; the builder wraps it and the fence/record after it in a record panel of that class; the checker counts it as the proposal's change. (Last use in a new-form checker test: `## Proposal 2: flows › a/b.md` then `**Archive** the record.`)
- A new file: put `, a new file` after the path in the heading; the proposal body is all `+` lines (front matter lines `+ ---` included). The builder gives it no special handling; the heading text is the target chip.

### A diagram that needs the Illustrator
A ```figure fence (or any unlabelled fence outside a proposal, or a fence holding a boxed sketch with an edge) is never drawn by the builder: the n-th diagram in the book needs `fig-n.svg` in the `--figures DIR`, else the build stops with `diagram n ("...") has no figure fig-n.svg from --figures`. Write the ASCII box-and-arrow sketch in a ```figure fence (example: Proposal 11; its first line starts `+--` so it is not mistaken for a change). A proposal fence whose lines carry `+ `/`- ` signs is a diff, not a diagram. Numbering counts every diagram in document order, module fences included.

## 2. What --ethos-zero checks
- `--ethos-zero REF` names the ethos-zero for PROPOSED code; `--ethos-zero-real REF` names the one for REAL code (a quoted fence outside any proposal). Both default to the pinned `github:LiGoldragon/ethos-zero/07714b01...` (main). REF may be a flake reference (realised once with `nix build --max-jobs 0`, i.e. no local build), a store path, or an executable. 804eb9 orders: `--ethos-zero github:LiGoldragon/ethos-zero/ethos-proposals`.
- Each checked block is written to a temp `block.ethos` and run as `ethos-zero Check.<file>`. A refusal prints `book-build: ethos block ("<first line>") refused by ethos-zero: Rejected....` and the build exits 1 after collecting all refusals. A whole file is needed: a fragment without the `Library`... root is refused.
- Blocks checked: (a) every ```ethos fence anywhere; (b) in a proposal, any ```text or unlabelled fence when the proposal heading's location (or last path extension) ends `.ethos`, unless it is an unsigned diagram. Proposed = inside a proposal or any signed fence; real = outside a proposal and without signed lines. A fence with signs is checked AS IT READS AFTER the change: `- ` lines dropped, `+ ` lines lose the sign, text-fence context loses two spaces.
- NOT checked: ```rust/```clj/etc fences; unfenced `+`/`-` ethos lines; text fences in proposals for non-`.ethos` locations; every UNLABELLED or ```text fence in a module view. An unlabelled module fence is typed (ethos, datom, diagram) and never refused for syntax (an old-syntax unlabelled block just fails to be `ethos`, then shows as datom if balanced, else needs a figure; unbalanced text makes the build fail with the missing-figure error).
- Current file in an old syntax shown as it stands: if its fence is labelled ```ethos it IS checked (as real, refused by the pinned main or `--ethos-zero-real`). The exemption is to write it as an unlabelled fence inside the module view (the example does this for its `Library`/`Signal` block with `;` comments; the labelled form would be refused). A removed (`-`) old-syntax line inside a proposal fence is also exempt, since removed lines are dropped before the check. Context lines (two-space) are kept and checked. There is no flag or comment to switch the check off; the only whole-check bypass is the test hook `*ethos-check*`. Use `--ethos-zero-real <older ethos-zero>` to check real code against an old syntax.

## 3. Excerpt (flows/a275c0/books/03-nexus-vision-3.md, lines 1-10 and 205-216)
```
<!-- to-the-living:start -->
Presentation.{ «The Nexus: the vision, 3rd edition» }

# The Nexus: the vision, 3rd edition

## psyche-context › vision/nexus.md

## A Nexus is the whole

A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.
...
## Proposal 1: Memory names the store · psyche-context › vision/nexus.md

- implementation; signal and sema are designed against it as if new, the
+ implementation; Signal, Operation and Memory are designed against it as if new, the

- The nexus and sema documents are undesigned; when they are designed
+ The Operation and Memory documents are undesigned; when they are designed

- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database

Ruling: land, amend, or reject.
```

## 4. Commands
```
cd /home/li/primary
bb tools/book-build.clj SOURCE.md OUT.html --figures FIGDIR \
   --ethos-zero github:LiGoldragon/ethos-zero/ethos-proposals [--ethos-zero-real REF] [--code tools/book-code.html]
node tools/book-check.mjs /ABSOLUTE/PATH/SOURCE.md     # exit 0 prints {"checked":true,...}; 1 prints {"errors":[{line,reason}]}; 2 usage
bb tools/book-build-test.clj                           # builder tests
node --test tools/book-check.test.mjs                  # checker tests
```
The checker needs an absolute path and reads each shown module from `/git/github.com/LiGoldragon/<repo>` at origin/main (`git ls-remote`), so it compares against main, not the working tree. Check first, then build; send the html path.
