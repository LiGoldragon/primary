# Builder rebuild, 2026-10-19

Target: the uncommitted working-copy change to `tools/` (book-build.clj, book-check.mjs, book-build-test.clj, book-check.test.mjs, book-code.html), against HEAD. Nothing under `tools/` or elsewhere in Primary was edited or committed.

## Method

- Every `bb`, `node` and rebuild ran on the configured remote builder, `prometheus.goldragon.criome`.
- HEAD's tools came from `git archive HEAD tools`; the working tools were copied as they stand.
- 217 books have both a `.md` source and a published `.html`. For each, `--figures` was given the inline SVGs of its published html, in order, as `fig-N.svg` (137 books). Both builders used the same default ethos-zero pin.
- Deviations, each needed to run a fixed input on the builder: (a) `book-build-test.clj:442` reads `/home/li/primary/flows/39bd0c/books/09-what-a-book-is.md` by absolute path, so that one file was placed at the same path on the builder; (b) `book-check.test.mjs` reads three books under `flows/504f11` and `flows/d68c82`, copied into the staged tree. (c) The builder has no `/git/github.com/LiGoldragon` repositories; the 93 check passed through the production CLI, which read no context module for that book.

## Results

- Suite 1, `bb tools/book-build-test.clj`: pass. 54 tests, 230 assertions, 0 failures, 0 errors.
- Suite 2, `node --test tools/book-check.test.mjs`: pass. 17 of 17.
- Rebuild, 217 books: identical 0; differs 70; refused 147.
  - Differs, 60: the only change is the appended page CSS from book-code.html (16582 to 20190 bytes). Every page carries it, so none is byte-identical.
  - Differs, 10: body changes, each an intended rendering (listed in the table).
  - Refused, 147: 70 refused by both builders; 75 refused only by the working builder for lacking a diagram (HEAD builds them); 2 refused only by HEAD (the working builder builds them).
- book-check of `flows/d68c82/books/93-book-dynamics-3.md` with the new checker: `{"checked":true}`, exit 0, no errors.

## Regressions judged as defects

- `tools/book-build.clj:1630`: `-main` binds `*require-figures*` true, so the CLI refuses every book with no diagram ("a book carries figures: this book has no diagram"). This refuses 75 books HEAD builds. The rule is "A sizable book carries several figures", which does not require a figure of every book. The tests call `build` directly, so they never exercise this binding.
- `tools/book-build-test.clj:442`: a hard-coded absolute path into `/home/li/primary/flows/39bd0c`, absent on any other setup. Introduced by this change (absent at HEAD). It should be a path relative to the test's root.

## Noted, not judged as defects

- `33752b/35-crystallization`: an uncaught NullPointerException at `book-build.clj:1634` (the `spit` line) in both builders. Shared, not a regression.
- `288af9/08-main-flow-roles`: a new refusal, "undrawn ASCII diagram ... give it its own fence with a fig-N.svg". HEAD refused this book for an ethos block. It is the only book the message refuses. Whether it is intended is the living's ruling, since the brief says looser checks.

## Table

Each row: the book, the result, and its nature or refusal message (HEAD's and/or the working builder's, first line).

| Book | Result | Nature or refusal |
|---|---|---|
| 081064/archive-mover | differs | only the appended page CSS (book-code.html); body identical |
| 081064/bytes | refused | HEAD: proposal heading not understood: "### Terms" ; work: proposal heading not understood: "### Terms" |
| 081064/ethos-nexus | refused | HEAD: proposal heading not understood: "### The ethos it uses" ; work: proposal heading not understood: "### The ethos it uses" |
| 081064/prototype-name | refused | HEAD: proposal heading not understood: "### The code" ; work: proposal heading not understood: "### The code" |
| 081064/sources-registry-2 | refused | HEAD: diagram 2 (" The generated code carries no `use`") has no figure fig-2.svg from --figures ; work: diagram 2 (" The generated code carries no `use`") has no figure fig-2.svg from --figures |
| 081064/type-ethos | refused | HEAD: diagram 2 ("; the head: a type file, one type") has no figure fig-2.svg from --figures ; work: diagram 2 ("; the head: a type file, one type") has no figure fig-2.svg from --figures |
| 081064/vector-delimiter | refused | HEAD: diagram 2 ("  EventsRead.{ FlowId Vector<Event> }") has no figure fig-2.svg from --figures ; work: diagram 2 ("  EventsRead.{ FlowId Vector<Event> }") has no figure fig-2.svg from --figures |
| 0c85a3/module-naming-implementation-second-edition | differs | only the appended page CSS (book-code.html); body identical |
| 0c9a77/01-identity-naming | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 0c9a77/02-flow-short-long-3 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 17ac8a/01-communicating-with-the-living-2 | differs | only the appended page CSS (book-code.html); body identical |
| 17ac8a/02-communicating-with-the-living-3 | differs | only the appended page CSS (book-code.html); body identical |
| 288af9/08-main-flow-roles | refused | HEAD: ethos block ("Address.{ Aspect Topic Layer }") refused by ethos-zero: Rejected.{ { 2 3 } Structural.ProtosError.{ Extent.{ 37 37 } Multiple } } ; work: undrawn ASCII diagram ("flow harness system prompt") in a markdown view; give it its own fence with a fig-N.svg |
| 33752b/10-aspects-same-layer-2 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/14-aspects-same-layer-3 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/18-nuts-and-bolts | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/20-anatomy-audit | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/21-two-field-lines | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/23-cleaning-skills | refused | HEAD: proposal heading not understood: "### A. One flow's order, or one past case, written as a rule" ; work: proposal heading not understood: "### A. One flow's order, or one past case, written as a rule" |
| 33752b/25-cleaning-skills-2 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/26-shoelaces | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/27-makeshift | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/28-makeshift-core-2 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/29-context-modules-2 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/3-ethos-whole | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/30-short-long-vision | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/31-three-lines | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/32-figures-that-move | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/33-review-is-psyche | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/35-crystallization | refused | HEAD: ----- Error -------------------------------------------------------------------- ; work: ----- Error -------------------------------------------------------------------- |
| 33752b/36-three-lines-2 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/37-short-long | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/38-three-lines-3 | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/39-tools-not-scripts | differs | only the appended page CSS (book-code.html); body identical |
| 33752b/40-compaction-request | refused | HEAD: proposal heading not understood: "### Line 1" ; work: proposal heading not understood: "### Line 1" |
| 33752b/41-flow-short-long | refused | HEAD: proposal heading not understood: "### What the prototype does" ; work: proposal heading not understood: "### What the prototype does" |
| 33752b/42-compaction-request-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 33752b/43-flow-short-long-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 33752b/44-books-and-reviews | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 33752b/45-books-and-reviews-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 33752b/46-communicating-with-the-living | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 39bd0c/09-what-a-book-is | refused | HEAD: ethos block ("Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: diagram 2 ("+--------------------+") has no figure fig-2.svg from --figures |
| 445410/1-a-book-then-a-voice | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 445410/1-distillation-books-first-review | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 445410/2-speech-beyond-its-text | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 445410/3-the-special-representation | refused | HEAD: ethos block ("Represented.{") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 445410/4-the-new-flows-as-they-run | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 445410/5-aspects-talk-at-the-same-layer | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 445410/6-the-lock-queue | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 504f11/01-chronos-golden-example | differs | only the appended page CSS (book-code.html); body identical |
| 504f11/02-chronos-golden-example-2 | differs | only the appended page CSS (book-code.html); body identical |
| 504f11/03-chronos-golden-example-3 | differs | only the appended page CSS (book-code.html); body identical |
| 504f11/04-chronos-golden-example-4 | refused (HEAD only; working builds it) | HEAD: diagram 6 ("Types") has no figure fig-6.svg from --figures |
| 55a2b4/12-flow-cli-deployment-long-term-3 | differs | only the appended page CSS (book-code.html); body identical |
| 55a2b4/14-short-term-prototypes-clojure | differs | only the appended page CSS (book-code.html); body identical |
| 55a2b4/15-flow-nexus-whole | refused | HEAD: ethos block ("Said.{ Context.String Verbatim.String }") refused by ethos-zero: Rejected.{ { 2 5 } Structural.ProtosError.{ Extent.{ 48 48 } Multiple } } ; work: ethos block ("Said.{ Context.String Verbatim.String }") refused by ethos-zero: Rejected.{ { 2 5 } Structural.ProtosError.{ Extent.{ 48 48 } Multiple } } |
| 563761/04-identity-naming-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 563761/05-metaflow | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 563761/06-refresh-handover | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 563761/07-launch | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 65f93a/01-ethos-vision | refused | HEAD: ethos block ("+ type") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } ; work: ethos block ("+ type") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } |
| 65f93a/02-ethos-vision-2 | refused | HEAD: ethos block ("+ type") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } ; work: ethos block ("+ type") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } |
| 65f93a/03-ethos-vision-3 | refused | HEAD: ethos block ("+ type") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } ; work: ethos block ("+ type") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [ 0 ] Root } } |
| 65f93a/04-ethos-vision-4 | refused | HEAD: ethos block ("- [ FilePath.String   ; types: an alias") refused by ethos-zero: Rejected.{ { 1 1 } Structural.ProtosError.{ Extent.{ 0 40 } Unclosed.«[» } } ; work: ethos block ("- [ FilePath.String   ; types: an alias") refused by ethos-zero: Rejected.{ { 1 1 } Structural.ProtosError.{ Extent.{ 0 40 } Unclosed.«[» } } |
| 65f93a/05-ethos-syntax | refused | HEAD: ethos block ("- Library") refused by ethos-zero: Rejected.{ { 1 1 } Structural.ProtosError.{ Extent.{ 0 0 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 65f93a/06-sealed-types | refused | HEAD: ethos block ("+ Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 65f93a/07-ethos-syntax-2 | refused | HEAD: ethos block ("Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 65f93a/08-sealed-shared | refused | HEAD: ethos block ("Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 65f93a/09-sealed-shared-2 | refused | HEAD: ethos block ("Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| 73ada7/10-field-window | refused | HEAD: proposal heading not understood: "### D1. How long Psyche's having spoken opens the route, in vision-aspects" ; work: proposal heading not understood: "### D1. How long Psyche's having spoken opens the route, in vision-aspects" |
| 73ada7/11-meta-owner | refused | HEAD: proposal heading not understood: "### D1. How a Nexus knows the owner of its meta socket, in vision-nexus" ; work: proposal heading not understood: "### D1. How a Nexus knows the owner of its meta socket, in vision-nexus" |
| 73ada7/7-address | refused | HEAD: proposal heading not understood: "### D1. What names a metaflow, in vision-flow" ; work: proposal heading not understood: "### D1. What names a metaflow, in vision-flow" |
| 804eb9/ethos-book | refused | HEAD: diagram 1 ("┌──────────────────────────────────────────┐") has no figure fig-1.svg from --figures ; work: diagram 1 ("┌──────────────────────────────────────────┐") has no figure fig-1.svg from --figures |
| 804eb9/ethos-v1-2 | refused | HEAD: diagram 6 ("Library") has no figure fig-6.svg from --figures ; work: ethos block ("+ [ Library.{") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [] Root } } |
| 804eb9/ethos-v1-3 | refused | HEAD: diagram 10 ("Library") has no figure fig-10.svg from --figures ; work: ethos block ("+ Library.{") refused by ethos-zero: Rejected.{ { 6 37 } Conceptual.{ [ 1 2 0 1 1 1 1 ] Yield } } |
| 804eb9/ethos-v1 | refused | HEAD: diagram 5 ("Library") has no figure fig-5.svg from --figures ; work: ethos block ("+ [ Library.{") refused by ethos-zero: Rejected.{ { 1 1 } Conceptual.{ [] Root } } |
| 804eb9/joint-ethos-extendable-enum | differs | a `+ ## heading` line now renders as an added h4, not raw paragraph text |
| 875960/1-meta-harness-base | refused | HEAD: proposal heading not understood: "### Proposal 1 — the base, in vision-flow" ; work: proposal heading not understood: "### Proposal 1 — the base, in vision-flow" |
| 875960/2-meta-harness-persona | refused | HEAD: proposal heading not understood: "### Proposal 1 — a vision-persona skill, opened with the base" ; work: proposal heading not understood: "### Proposal 1 — a vision-persona skill, opened with the base" |
| 875960/3-persona-root | refused | HEAD: proposal heading not understood: "### Proposal 1 — «What the root does», in vision-persona" ; work: proposal heading not understood: "### Proposal 1 — «What the root does», in vision-persona" |
| 875960/4-flow-whole-ethos | refused | HEAD: proposal heading not understood: "### Proposal 1 — vision-flow, the vision whole" ; work: proposal heading not understood: "### Proposal 1 — vision-flow, the vision whole" |
| 875960/5-flow-whole-ethos-2 | refused | HEAD: proposal heading not understood: "### Proposal 1 — vision-flow, the vision whole" ; work: proposal heading not understood: "### Proposal 1 — vision-flow, the vision whole" |
| 875960/6-flow-whole-ethos-3 | refused | HEAD: proposal heading not understood: "### Proposal 1 — new wording, from your comments of 20:23 to 20:32" ; work: proposal heading not understood: "### Proposal 1 — new wording, from your comments of 20:23 to 20:32" |
| 875960/7-flow-whole-ethos-4 | refused | HEAD: proposal heading not understood: "### Proposal 2 — vision-flow-ethos, Flow in ethos" ; work: proposal heading not understood: "### Proposal 2 — vision-flow-ethos, Flow in ethos" |
| 875960/8-caller-witnessed | refused | HEAD: proposal heading not understood: "### Proposal 1 — the shared library, in ethos" ; work: proposal heading not understood: "### Proposal 1 — the shared library, in ethos" |
| 875960/9-flow-anatomy | refused | HEAD: proposal heading not understood: "### Ruling 1 — the one form that governs every trait" ; work: proposal heading not understood: "### Ruling 1 — the one form that governs every trait" |
| 984e88/01-chronos | refused | HEAD: proposal heading not understood: "### 3.1 The purely solar and purely lunar formats" ; work: proposal heading not understood: "### 3.1 The purely solar and purely lunar formats" |
| 984e88/02-chronos | refused | HEAD: ethos block ("+ Library                        ; shared by all") refused by ethos-zero: Rejected.{ { 1 8 } Conceptual.{ [ 1 ] Arity.{ 4 17 } } } ; work: ethos block ("+ Library                        ; shared by all") refused by ethos-zero: Rejected.{ { 1 8 } Conceptual.{ [ 1 ] Arity.{ 4 17 } } } |
| a275c0/01-nexus-vision | differs | a one-text diff now renders as context and inline word-level del/ins, not raw - and + paragraphs |
| a275c0/02-nexus-vision-2 | refused | HEAD: ethos block ("[ FlowId.Integer                         ; types") refused by ethos-zero: Rejected.{ { 27 10 } Structural.ProtosError.{ Extent.{ 1020 1438 } Unclo ; work: ethos block ("[ FlowId.Integer                         ; types") refused by ethos-zero: Rejected.{ { 27 10 } Structural.ProtosError.{ Extent.{ 1020 1438 } Unclo |
| a275c0/03-nexus-vision-3 | refused | HEAD: diagram 2 ("Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal") has no figure fig-2.svg from --figures ; work: ethos block ("+ ; what the three parts share") refused by ethos-zero: Rejected.{ { 3 1 } Structural.ProtosError.{ Extent.{ 38 38 } Multiple } } |
| c5f24b/09-context-modules | refused | HEAD: ethos block ("-   Subaspect.[ Vision Intent Knowledge Operation Trial Compensation ]") refused by ethos-zero: Rejected.{ { 1 3 } Conceptual.{ [ 0 ] Root } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| c5f24b/10-messaging-between-flows | refused | HEAD: ethos block ("-   Lock.{ Sender Recipient }") refused by ethos-zero: Rejected.{ { 2 5 } Structural.ProtosError.{ Extent.{ 33 33 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d4ae97/haiku-quaternary | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d55c56/1-spirit-whole-picture | refused | HEAD: diagram 1 ("The purpose of a thinking machine is to") has no figure fig-1.svg from --figures ; work: diagram 1 ("The purpose of a thinking machine is to") has no figure fig-1.svg from --figures |
| d55c56/2-makeshift-spirit | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/10-what-compaction-keeps | refused | HEAD: proposal heading not understood: "### 1. A flow is refreshed, not compacted" ; work: proposal heading not understood: "### 1. A flow is refreshed, not compacted" |
| d68c82/11-only-psyche-reaches-you | refused | HEAD: proposal heading not understood: "### 1. Only psyche lines are put to the living" ; work: proposal heading not understood: "### 1. Only psyche lines are put to the living" |
| d68c82/12-dense-and-visual | refused | HEAD: proposal heading not understood: "### 1. A book shows each change once" ; work: proposal heading not understood: "### 1. A book shows each change once" |
| d68c82/13-sitrep-1 | refused | HEAD: proposal heading not understood: "### 1. Situational reports" ; work: proposal heading not understood: "### 1. Situational reports" |
| d68c82/14-sitrep-2 | refused | HEAD: proposal heading not understood: "### 1. A repeated use case grows a tool" ; work: proposal heading not understood: "### 1. A repeated use case grows a tool" |
| d68c82/15-clojure-translation | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/16-subflows | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/17-subflows-kind | refused | HEAD: diagram 3 ("{:aspect #field [] :role #operator []") has no figure fig-3.svg from --figures ; work: diagram 3 ("{:aspect #field [] :role #operator []") has no figure fig-3.svg from --figures |
| d68c82/18-battery-sleep | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/19-context-modules-layout | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/2-sources-in-the-commit-message | refused | HEAD: diagram 1 ("## Sources") has no figure fig-1.svg from --figures ; work: diagram 1 ("## Sources") has no figure fig-1.svg from --figures |
| d68c82/20-context-modules-2 | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/21-code-as-code | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/22-watching-the-cluster | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/23-nix-links | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/24-names-are-data | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/25-fable-care | differs | a one-text diff now renders as a context paragraph and an added paragraph |
| d68c82/26-nix-links-2 | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/27-git-servers | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/28-compaction-2 | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/29-fable-care-2 | differs | a one-text diff now renders as a context paragraph and an added paragraph |
| d68c82/3-what-you-rule-on | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/30-one-registry | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/31-monitoring-systems | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/32-wording | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/33-drawing-ideas | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/34-where-today-stands | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/35-drawing-ideas-2 | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/36-drawing-ideas-3 | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/37-short-hashes | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/38-ethos-nexus-chronos | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/39-lost-orders | refused | HEAD: diagram 1 (" your order") has no figure fig-1.svg from --figures ; work: diagram 1 (" your order") has no figure fig-1.svg from --figures |
| d68c82/4-five-landed-lines | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/40-useless-messages | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/41-figures-as-code | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/42-lost-orders-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/43-context-design | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/44-spirit-stronger | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/45-figures-as-code-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/46-no-invented-words | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/47-loose-texts | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/48-context-design-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/48-illustrator-refresh | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/49-today-as-psyche | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/5-commit-queue | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/50-lean-flows | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/51-real-code | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/52-manager | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/53-flow-design | refused | HEAD: ethos block ("Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/54-heartbeat | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/55-illustrator-refresh-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/56-tighten-ship-1 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/57-whole-context-start | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/58-today-as-psyche-2 | refused | HEAD: ethos block ("Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/59-fresh-wake | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/6-back-on-the-grid | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/60-flow-in-production | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/61-every-comment-reaches-its-metaflow | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/62-illustrator-refresh-3 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/63-illustrator-refresh-4 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/64-last-response-datom-object | refused | HEAD: ethos block ("+ Library.{") refused by ethos-zero: Rejected.{ { 13 24 } Conceptual.{ [ 1 1 7 1 3 1 ] Name.⟦ } } ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/65-switching-to-flow | differs | a module section renders as a framed "as it stands" article |
| d68c82/66-last-response-datom-object-2 | refused | HEAD: ethos block ("+ Library.{") refused by ethos-zero: Rejected.{ { 13 24 } Conceptual.{ [ 1 1 7 1 3 1 ] Name.⟦ } } ; work: ethos block ("+ Library.{") refused by ethos-zero: Rejected.{ { 13 24 } Conceptual.{ [ 1 1 7 1 3 1 ] Name.⟦ } } |
| d68c82/7-mining-today | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/8-why-fable-not-refreshed | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/83-book-dynamics | differs | a four-backtick markdown fence renders as module content, not a paragraph |
| d68c82/84-book-dynamics-2 | differs | a four-backtick markdown fence renders as module content, not a paragraph |
| d68c82/86-flow-definition | differs | a four-backtick markdown fence renders as module content, not a paragraph |
| d68c82/87-ethos-open-enum | differs | a four-backtick markdown fence renders as module content, not a paragraph |
| d68c82/9-green-and-code | refused | HEAD: proposal heading not understood: "### 1. A book about code shows the code" ; work: proposal heading not understood: "### 1. A book about code shows the code" |
| d68c82/91-subflows | differs | a four-backtick markdown fence renders as module content, not a paragraph |
| d68c82/92-ethos-custom-representation | refused (HEAD only; working builds it) | HEAD: diagram 11 ("{ 7 renew }") has no figure fig-11.svg from --figures |
| d68c82/95-flow-ethos-2 | differs | only the appended page CSS (book-code.html); body identical |
| d68c82/r-chronos | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-clojure-now | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-communicating-living | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-compensation-core | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-context-modules-prompt-3 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-context-modules-prompt | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-fable-care | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-flow-cli-deployment | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-flow-nexus-whole | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-launch | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-main-flow-roles | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-messaging | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-metaflow-roles | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-metaflow | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-names-are-data | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-nexus-ethos-design | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-refresh-handover | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-sitrep-evening | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-subflows-kind | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-watching-the-cluster | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| d68c82/r-wording | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| da2038/1-clojure-and-data | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| da2038/2-compensation-core | differs | only the appended page CSS (book-code.html); body identical |
| da2038/3-pod-controller | refused | HEAD: ethos block ("+ Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: ethos block ("+ Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } |
| da2038/4-raw-psyche-clearing | differs | only the appended page CSS (book-code.html); body identical |
| da2038/5-flow-sleeping-and-waking-seats | differs | only the appended page CSS (book-code.html); body identical |
| da2038/6-metaflow-roles | refused | HEAD: ethos block ("+ Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } ; work: ethos block ("+ Library.") refused by ethos-zero: Rejected.{ { 2 1 } Structural.ProtosError.{ Extent.{ 9 9 } Multiple } } |
| da2038/7-how-flow-is-used | differs | only the appended page CSS (book-code.html); body identical |
| da2038/8-flow-vision-and-production | refused | HEAD: proposal heading not understood: "### Sessions not running keep no harness: partly" ; work: proposal heading not understood: "### Sessions not running keep no harness: partly" |
| df159a/11-nexus-ethos-design | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| df159a/12-flow-cli-deployment-long-term-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| df159a/12-flow-cli-deployment-long-term | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| df159a/13-flow-philosophy-artifacts | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| df159a/14-short-term-prototypes-clojure | differs | only the appended page CSS (book-code.html); body identical |
| ebbe30/1-spirit-three-skills | refused | HEAD: diagram 1 ("Before doing or thinking anything, list what is") has no figure fig-1.svg from --figures ; work: diagram 1 ("Before doing or thinking anything, list what is") has no figure fig-1.svg from --figures |
| ebbe30/10-how-a-psyche-seat-works | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| ebbe30/12-the-golden-ethos-2nd | refused | HEAD: diagram 2 ("Library") has no figure fig-2.svg from --figures ; work: diagram 2 ("Library") has no figure fig-2.svg from --figures |
| ebbe30/13-the-golden-ethos-3rd | refused | HEAD: diagram 2 ("The anatomy of an ethos file, written in ethos.") has no figure fig-2.svg from --figures ; work: diagram 2 ("The anatomy of an ethos file, written in ethos.") has no figure fig-2.svg from --figures |
| ebbe30/14-the-golden-ethos-3rd-b | refused | HEAD: diagram 2 ("The anatomy of an ethos file, written in ethos.") has no figure fig-2.svg from --figures ; work: diagram 2 ("The anatomy of an ethos file, written in ethos.") has no figure fig-2.svg from --figures |
| ebbe30/2-distilled-lines-gone-stale | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| ebbe30/6-context-modules | refused | HEAD: diagram 1 ("   skills ──► Flow ──► the flow's context") has no figure fig-1.svg from --figures ; work: diagram 1 ("   skills ──► Flow ──► the flow's context") has no figure fig-1.svg from --figures |
| ebbe30/7-next-stable-last | refused | HEAD: diagram 1 ("  next ──promote──► stable ──retire──► last") has no figure fig-1.svg from --figures ; work: diagram 1 ("  next ──promote──► stable ──retire──► last") has no figure fig-1.svg from --figures |
| ebbe30/8-next-stable-last | differs | only the appended page CSS (book-code.html); body identical |
| ebbe30/9-lojix-broad-vision | differs | only the appended page CSS (book-code.html); body identical |
| edf227/deployed | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| edf227/flow-2 | refused | HEAD: diagram 1 ("Library") has no figure fig-1.svg from --figures ; work: diagram 1 ("Library") has no figure fig-1.svg from --figures |
| edf227/the-deployment-in-four-parts-2 | refused | HEAD built it ; work: a book carries figures: this book has no diagram (no ASCII diagram fence and no figure) |
| f5a6e9/18-speech-across-aspects | refused | HEAD: proposal heading not understood: "### 1. `psyche-skills/vision/flow.md`, line 24" ; work: proposal heading not understood: "### 1. `psyche-skills/vision/flow.md`, line 24" |

## Rerun after the two fixes, 2026-10-19

- `tools/book-build.clj:1630`: `-main` no longer binds `*require-figures*`; the "ASCII diagram has no figure" refusal is unchanged. `tools/book-build-test.clj:442` reads the fixture `tools/fixtures/what-a-book-is.md` (a copy of `39bd0c/09-what-a-book-is.md`) through `tools-dir`.
- Same method, on `prometheus.goldragon.criome`, from a fresh stage of HEAD tools and the working tools.
- Suite 1: 54 tests, 230 assertions, 0 failures, 0 errors, with no file placed outside the staged tree. Suite 2: 17 of 17.
- Rebuild, 217 books: identical 0; differs 145; refused 72 (70 refused by both builders; 2 refused only by HEAD, `504f11/04-chronos-golden-example-4` and `d68c82/92-ethos-custom-representation`). Refused only by the working builder: 0.
