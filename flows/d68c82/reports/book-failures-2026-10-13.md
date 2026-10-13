# Book failures, 2026-10-13

Subflow of d68c82, read-only except this file. Witnessed: files read, `book-check.mjs` run, HTML counted with comments and scripts stripped, Fable 33752b's transcript read. The published artifact was not fetched: no Artifact tool in this subflow. Its local twin, `flows/33752b/books/39-tools-not-scripts.html`, was read instead. The `flow-evidence` skill could not be loaded: no Skill tool in this subflow. Provenance receipt: unavailable.

## 1. «Tools instead of scripts»

- Source: `/home/li/primary/flows/33752b/books/39-tools-not-scripts.md`, 108 lines. Author: Fable 33752b. It wrote the block in its own reply and dispatched the `book` subagent at 2026-10-13T18:00:13Z (transcript line 4895). The log is at `flows/33752b/log.md:185-186`.
- Proposals: five, each `Target: <a tool or owner in prose>`, for example "Target: the transcript tool, Mind." None names a file. None carries removed lines, added lines, `As it stands`, `Added:` or `+`/`-` lines. Proposal 5 is "what is not built".
- Code: none. Every fence is an ASCII figure (6 of them).
- Rendered HTML: 5 `article.proposal`, 0 `div.add`, 0 `div.del`, 0 `div.ctx`, 0 `<pre><code>`, 5 SVG figures. The only `add`/`del` strings are inside the `book-code.html` header comment.
- Verdict, witnessed: the source lost them, not the renderer. `subagents/book.md:60-62` paints a panel only for `+`/`-` lines or "a block introduced as added or removed". This source has neither. `node tools/book-check.mjs …/39-tools-not-scripts.md` returned `{"checked":true}`.
- Inputs, witnessed. The Mind Tools packet as received by Fable was 21,115 characters with 0 code fences (transcript line 4891). d68c82's relay as logged by Fable reads "the living wants it as a book of tool proposals (new tools or features), figures as flows." It names no file, line or code. Fable's prompt context at composition was about 443,094 cached input tokens (lines 4893-4895). That is over the 200,000 no-further-work line. The manual compaction followed at 18:09Z.

## 2. Last ten books in the index

| book (source) | proposals | green blocks | red blocks | ctx blocks | code blocks | figures | subject is code? |
|---|---|---|---|---|---|---|---|
| 8 Why Fable was not refreshed (d68c82/books/8-…) | 4 | 3 | 2 | 0 | 0 | 1 | no (prompt lines) |
| 39 Tools instead of scripts | 5 | 0 | 0 | 0 | 0 | 5 | yes |
| 38 Three lines, 3rd ed. | 3 | 3 | 3 | 0 | 0 | 1 | no |
| 37 Short term and long term | 11 | 0 | 0 | 0 | 0 | 12 | partly (Flow, messaging, locking, committer) |
| 36 Three lines, 2nd ed. | 4 | 4 | 4 | 0 | 0 | 1 | no |
| 35 Crystallization | 3 | 1 | 0 | 0 | 0 | 1 | no |
| 33 What you review is psyche | 2 | 2 | 0 | 0 | 0 | 2 | no |
| 32 Figures that move | 2 | 2 | 2 | 0 | 0 | 1 | partly (the figure brief) |
| 31 Three lines | 3 | 3 | 3 | 0 | 0 | 1 | no |
| 30 Short-term and long-term vision | 3 | 3 | 1 | 0 | 0 | 1 | no |

Unless noted, books are in `flows/33752b/books/`. Counts are taken from the HTML with comments stripped. No book among the ten has a code block or a context panel.

## 3. The instruction lines

### a. No rule says a book about code shows code. One rule tells the author to keep code-like content out.

`/git/github.com/LiGoldragon/field-context/skills/compensation-book-distillation.md:8`:

> A book opens with its context as figures, with any text a few short lines inside them, then goes straight to the proposals. Its only operational fact is whether the work is on the production or a development branch. How the system runs today is knowledge, landed without the living's review; no runtime version, socket or store path, or operational command reaches a book; the authored file targeted by a proposal stays named.

"No … operational command reaches a book" excludes a tool's CLI line. A proposed tool's interface is exactly such a line, for example `transcript 'Query.{ … }'`. This is the flow's inference.

`/git/github.com/LiGoldragon/psyche-context/skills/vision-book.md:14`:

> A book carries psyche only. Compensation, knowledge and operation skills are the machines' own: they write them and prove them by tests.

A tools book has no psyche file to target, so the author targeted tools in prose. The only code rule, `/git/github.com/LiGoldragon/mind-context/skills/operation-psyche-distillation.md:27`, is scoped to distilled statements:

> A statement about code carries the code: a distilled statement on a syntax, a type, a kind, or a wire form shows example code, because machines think in code and the next machine to read it must understand.

`vision-crystallization.md` has no code line. Grepping the three context repos for "carries the code" finds only this file.

Lacking: a sentence, in `compensation-book-distillation` or `vision-book` (for the living's ruling), saying a proposal whose subject is code shows the code: the type, the wire form, the call. It would sit beside or replace the "operational command" clause above. Line 14 of `vision-book` needs a ruling on where a book of tool or code proposals lands.

### b. Proposals without file, removed or added lines

The rule exists. `compensation-book-distillation.md:6`:

> Every book the living reads is distillation proposals, 99% of it: each section names the file, the lines removed and the lines added, and asks a ruling; around the changed lines it shows the file as it stands, whole when short, otherwise the parts above and below, so the landing can be situated; a new file is shown whole with the explanation around it; a book carries no survey; its context serves the proposals that follow. Concise machine results and concrete blockers may be sent outside a book.

It does not reach the author:

- `/home/li/primary/tools/main-flow-mode/spirit-system-prompt.mjs:32-36` composes the seat prompt from `spirit-*`, `vision-design`, `intent-psyche-interaction` and startup `intent-*` only. No book module is included.
- Fable's transcript shows `operation-book` loaded once, 2026-10-10T19:15:59Z (line 264). An auto-compaction followed on 2026-10-12T18:27Z (line 2145). Whether the dependency `compensation-book-distillation` was in context on 10-13 is unknown.
- `/home/li/primary/tools/main-flow-mode/system-prompt.md` has no book line.

Lacking: the seat prompt, or the module set for a book-writing seat, carries no book-format module.

Latent, witnessed: `/git/github.com/LiGoldragon/psyche-context/skills/spirit-core.md:3` reads

> dependencies: [compensation-behavior, compensation-correction, knowledge-vocabulary, compensation-book-crystallization]

No `compensation-book-crystallization` exists. The file is still `field-context/skills/compensation-book-distillation.md`, and the generated `.agents/skills/spirit-core/SKILL.md:3` still names `compensation-book-distillation`. The next regeneration loses the book dependency.

### c. The checker passes a book with no change in it

`/home/li/primary/tools/book-check.mjs:6`:

> // This checks source structure, not the merits of a proposed crystallization.

and lines 54 and 58:

> if (section && line.trim() && !/^Presentation\./.test(line)) section.content = true;
> if (!hasCrystallization) errors.push({ reason: "missing-crystallization" });

Any nonblank line satisfies the check. There is no check for a target path, a removed/added marker, or a green block.

`/home/li/primary/subagents/book.md:24-26`:

> defects to the caller and publishes nothing. Every book has a nonempty
> crystallization section proposing skill lines and their authored targets.
> Never invent that section or a proposal on the caller's behalf.

The renderer may not add a missing change, so it rendered none, as instructed. `book.md:58-62` holds the diff-rendering rule. It is intact, not dropped:

> - A change is a `<div class="diff">`: removed lines in `<div
>   class="del">`, added lines in `<div class="add">`, unchanged context in
>   `<div class="ctx">`. A line marked `+` or `-` in the source goes in the
>   matching panel without its mark; a block introduced as added or removed
>   goes whole in that panel. "Removed: none" puts no removal panel.

There is no fixed source marker. Authors used "As it stands:/Crystallized:", "Replaced by:", "Added:", "Removed:", or nothing, and the renderer guesses from that prose.

`/git/github.com/LiGoldragon/mind-context/skills/operation-book.md:15` states the green/red rule, but nothing enforces it:

> A presentation renders as a web page, never raw Markdown or prose in a code block. A proposed change shows its additions in green and its removals struck through in red, in one consistent style across books.

### d. Commit 4a7c92e (2026-10-12)

`subagents/book.md` lost these lines:

> -Load `vision-book`, `compensation-book-distillation`, `operation-book`
> -and, for drawings,
> -`operation-flashbook-illustration` through the Skill tool, and the tool
> -`ArtifactComments` with ToolSearch.

The diff, code and phone-width rules stayed: `book.md:55-74` and `110-130`. Only `compensation-book-distillation:8` was copied in, as `book.md:9`. `book.md` is the renderer, not the author, so this did not cause book 39's missing change. The renderer has no rule against publishing a book with zero `div.add`.

### e. Figure weight

`vision-book.md:16`, landed today in commit 8bd55fe, ends:

> A sizable book carries several figures.

Book 37 has 12 figures and 0 green blocks. Book 39 has 5 figures and 0 green blocks. The relay asked for "figures as flows". Whether the figure emphasis displaced the change blocks is the flow's hypothesis, not witnessed.

## 4. Failure types, one example each

1. **No green block.** In 39 every proposal is prose after `Target:`; in 37, 11 proposals render 0 `div.add`.
2. **No code where the subject is code.** 39 proposes a transcript query, an identity surface and an evidence tool, with no type, wire form or call shown. 0 of 10 books have a code block.
3. **Target not a file.** 39: "Target: the transcript tool, Mind." 37: "Target: vision-messaging." That is a module name with no path or section. 36: "Target: the main-flow context (today tools/main-flow-mode/system-prompt.md in Primary; its move into a user-only psyche context module … is with Field)."
4. **A change described instead of given.** 35, Proposal 1: "Crystallized: the module keeps its seven sections with the one word changed". 32, Proposal 2: "Crystallized: the same brief carries the grammar of Proposal 1 in its own words, and the drawer returns the sketch instead of a figure when the sketch has no relation to draw."
5. **No surrounding file context.** 0 `div.ctx` in all ten books, against `compensation-book-distillation:6` ("around the changed lines it shows the file as it stands").
6. **Survey or narrative in place of proposals.** 39 opens with transcript tallies ("about two thousand inline Python calls, thirteen thousand heredocs…"), and its Proposal 5 lists what is not built. 8 has three sections of explanation ("Why I did not compact or restart Fable" and others) before its crystallization. 37 attaches "Readjusts:" inventories of repositories.
7. **Inconsistent change markers.** "As it stands/Crystallized" (31, 32, 35), "Replaced by:/Added:" (36, 38), "Removed:/Added:" (30), none (37, 39).
8. **Book composed above the context threshold.** 39 was written at about 443k tokens (33752b transcript, lines 4893-4895). d68c82's own log, line 506 (the noise-analysis entry), records "I kept sending work above the 200k no-further-work line."
9. **Missing figures: not observed.** Every book has at least one SVG.

## Possible causes of 39, in order of the chain

What was read, in order:

1. The living's raw order (`flows/d68c82/vision/tools.md:4`).
2. d68c82's relay, "book of tool proposals … figures as flows".
3. Mind Tools' 21k-character prose packet, with no code.
4. Fable's seat context: about 443k tokens, no book module in the composed prompt, last book-skill load 10-10.

What was written: the source with prose targets (18:00Z), the book subagent's render (faithful), then publication.

Candidate causes, not exclusive:

- (i) The packet carried no code to show.
- (ii) `vision-book:14` leaves a code book no file to target.
- (iii) `compensation-book-distillation:8` keeps operational commands out of books.
- (iv) The format rule (`:6`) is not in the seat's composed context.
- (v) `book-check.mjs` passes any nonblank crystallization.
- (vi) Context saturation at about 443k tokens.
- (vii) The relay emphasised figures over changes.
