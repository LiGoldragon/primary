# Book workflow audit

The living's request reached Field through Psyche Secondary 445410. Sources: flows/445410/vision/books.md and messaging.md, flows/445410/log.md (one-proposal review disposition), flows/d4ae97/vision/books.md, and the diagram relay from ebbe30.

## Findings and corrections

- vision-book already required a distillation section. Its authored vision was preserved. The old book procedure did not load that skill or refuse a source missing the section. The procedure now loads it and compensation-book-distillation, runs tools/book-check.mjs before rendering, and returns a defect to the author without inventing a proposal.
- operation-flashbook cut a transcript at a heading and next rule, disagreeing with tools/book-fetch.mjs --block. It now uses the exact marked Presentation block or explicit source file.
- operation-book and operation-flashbook now specify the book-subflow route. Non-Claude callers hand a source to the qualified book-making seat, rather than substituting a hand-rendered page.
- subagents/book.md permitted updating uncommented artifacts, while trial-presentation-book preserved every older artifact. Every revised presentation now creates a fresh artifact, including uncommented prior pages.
- operation-book/flashbook omitted the bounded post-completion voice answer. Both now return the completed title and URL with that short answer. trial-presentation-book suppresses intermediate publication chatter and preserves proposal-by-proposal review where applicable.
- operation-flashbook's independent font palette disagreed with the shared tools/book-code.html stylesheet. The shared unchanged stylesheet is now the renderer's authority.
- compensation-book-distillation said no path reaches a book while requiring exact target files. It now distinguishes operational socket/store paths from the authored proposal target.
- ASCII is source-only. The existing Haiku figure delegation remains; real code is never reflowed. The available real-book-agent witness confirms claude-haiku-5-5 at depth 2, but did not include a rendered preview. Phone text fit and contrast are therefore not claimed from that witness.

## Validation

Source publication: mind-skills b605cd0, field-skills d7225ae. Independent Mind Secondary operation review requested two corrections (actual tools/ path and short voice answer); both applied before publication.

Curriculum EditSkills, RebuildSkills and CheckSkills passed. All authored skill bytes matched the selected durable skill-source revisions. Full immutable Primary candidate 2c974f passed all nine x86_64-linux flake checks on Prometheus. After preserving an unrelated current-remote 73ada7 lane advance, final candidate db73ed passed both book-publication-fixtures and generated-skills-current on Prometheus. Primary main is db73ed, non-force; shared HEAD/index and foreign paths were preserved.

Eight source/preflight tests and nine transcript-fetch tests passed. The real first Word ids for flows source is refused for missing distillation; its real second edition passes. Process fixtures cover failure stdout/stderr and source preservation. Structural checking does not establish the merits of a proposal or actual visual layout.

The five generated skill surfaces and all 24 role packets match the immutable sources; vision-book appears exactly once in every role packet. Existing conversations are not claimed retroactively reloaded.

Installed hm-send resolves to immutable messenger-clj 0.3.0. Messages to the qualified Psyche Secondary route445410 returned Transported, not a read or book-publication receipt. Messenger routes and databases were not migrated.

Evidence: /home/li/private-repos/flow-evidence/42265e/book-publication-audit/{authored-source-receipts.json,source-alignment.json,full-remote-check.json,final-remote-check.json,standing-book-rule-coverage.json,publication-receipt.json}.
