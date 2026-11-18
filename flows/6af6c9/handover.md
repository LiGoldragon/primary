# Handover, Field book Haiku, flow 6af6c9

## Pursuing

Publishing the presentations other flows hand this flow, fixing their form where the checker or builder refuses it, sending each title and link back to the orderer (no link on success, per Fable's and Sonnet's later rules; a message only when a page cannot be published), and relaying the living's comments on books awaiting his ruling.

## Where it stands

- Published this session, each with its comment watch armed and its entry Watched or Unwatched in `flows/book/open-books.datom`:
  - StaleLines.1, CodexFirst.1, LivingReading.1, Overruling.1, Naming.1, Reset.1, CodexHarness.6, Identifier.1, PageLink.1.
- Retitled in place with "Purified ·": Overruling.1 and Naming.1 (no comments on either).
- Not retitled: living-interaction-split (2G33kxeFsVTcxDQN1pdyFZ); checker refuses it at line 7 (context-module-unavailable). Sonnet told (qfhs).
- Drawn but not yet published: none.
- Figures being drawn by an illustrator run when this handover was written: Reset.2 (btej, fig-1), PurifiedMark.1 (vg95, fig-1), MessengerNexus.1 (raoh, figs 1 and 2). Check `scratchpad/reset2-figs`, `scratchpad/pmark-figs`, `scratchpad/messenger-figs` for `fig-N.svg`; if absent, redo that illustrator run. Then build with `bb book-build.clj SOURCE OUT.html --figures DIR` and publish.
- Open, not started: abhv (Fable): publish roles.md as Roles.1, with the form the checker takes, exact origin text for every removed and moved line, no wording changed. Then retitle CodexFirst.1 and Reset.2 to start with "Superseded". Reset.2 is not yet published, so retitle it after publication.
- Partly answered: gn52, 3dih (Fable, Identifier.1). Identifier.1 was published under cm63 (Opus) after the builder accepted the fence as `ethos sketch`; Fable's "text" label fallback was refused earlier. Confirm to Fable that Identifier.1 is published, or say nothing per the no-success rule.

## What works

- Checker: `bb book-check.clj SOURCE` in /git/github.com/LiGoldragon/makeshift-tools; passing prints `{"checked":true}`.
- Figures: extract each mermaid fence (strip the + or - margin) to a directory as fig-N.mmd; illustrator run; SVGs in the same directory.
- Build: `bb book-build.clj SOURCE OUT.html --figures DIR`. Publish with Artifact, same file path to redeploy the same link.
- Retitle: change the Presentation line and the `#` heading in the source, rebuild to the same HTML path, republish the same path. Check comment threads first with ArtifactComments read.
- Labels: a page already labelled keeps its label; no label command runs on existing sources.

## What does not

- Builder refuses an Ethos fence whose name is declared in a later proposal (Identifier.1 case; the label `ethos sketch` cleared it).
- Checker refuses a second comment inside one proposal; fold the text into the first comment.
- Checker context refusal on living-interaction-split (line 7).

## Next step

1. Check the three illustrator runs' output (Reset.2, PurifiedMark.1, MessengerNexus.1); build and publish each; no link sent on success.
2. Do abhv (Roles.1), then the two retitles to "Superseded" (CodexFirst.1 and, after publishing, Reset.2).

## Watched links, bare

https://claude.ai/artifact/W4n6CSdxsMm8Ha5nNL6G3c
https://claude.ai/artifact/TZtTHQfe6AJvHbUHj7WKxD
https://claude.ai/artifact/DEm6dUWgj5f3GHhZZGboxt
https://claude.ai/artifact/SiB5T5kBpk5yEcF7bLVQyY
https://claude.ai/artifact/MHNf5XF1yLVcomJfC9AACw
https://claude.ai/artifact/VsdCTSWzZU8LMLRSEN6Mc1
https://claude.ai/artifact/9viQxP1m959uNtG8sSE286
https://claude.ai/artifact/Gh4d5y56RYSjGjDqGLpz4H
https://claude.ai/artifact/BJU5iTEWUq1PC1vbWP62dr
