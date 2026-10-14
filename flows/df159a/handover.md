# { Psyche Flow Primary df159a } — handover

Judgment only. Facts and words live in log.md, books/, reports/, and the published pages; a tool fetches them.

## State
- The Flow book series is complete: ten batches, books 01–13. This seat published book 10 revision (Version 2), book 11 (Versions 1–3), book 12 (Versions 1–3), book 13 (Versions 1–2). URLs and version ids in log.md. Books 10–12 accepted by Psyche Flow Secondary da2038; book 13 Version 2 sent, acceptance pending.
- Envelopes: books/batch-08-psyches.edn, batch-09, batch-10. Owner work (machine-module changes implied by psyche lines, never in a book): reports/book-11-p15-machine-proposal.md, reports/book-12-owner-work.md, reports/book-13-owner-work.md — all sent to the Secondary, which dispatches to owners.
- Page builder: tools/book-build.clj run by bb, tests tools/book-build-test.clj (committed). Build with absolute paths. Witness: headless Chrome on the local html wrapped in the artifact skeleton, 320/375 px, light/dark; the published URL does not load headless.
- Committing: nothing in Primary commits itself; the seat's turn-end hook messages Field PrimaryCommitting Quaternary when Primary is dirty. Pending dirt at any moment is whatever the last turn left.
- 2026-10-14: book 14 «Short-term prototypes: Clojure now?» at https://claude.ai/artifact/8crUcAX5LKJANvvFsts1hy (Version 6, final: P1–P3; P4 withdrawn to the Communication pair, its material in the refs file; account sent). Book 12 second edition at https://claude.ai/artifact/FBGQe51sX8Tr89Ryi1Cy3g (Version 4, final per two Secondary audits; account sent). Book 12 P1 and P3 landed in psyche-context vision-flow.md (67d358d7bb86); book 13 held by Core; book 12 first edition commented (never changed again).
- tools/book-code.html: whole-file ownership handed to the committer 89fbc1 by this seat (witnessed behaviour; hunks authored by other seats). Rendering today: word-level diff renderer and in-code word marks landed by others in tools/book-build.clj and tools/book-code.html (uncommitted). Republished word-level: books 11, 10, batches 04, 06; in-code marks republished on those four (11 v5, 10 v4, 04 v5, 06 v5). Batch 01 editions restored to pre-word-diff rendering (sources have bare + lines outside fences). Batches 02, 03, 05 and the rectification book stay as published (sources not buildable by the current builder).
- His 2026-10-14 words after commenting on book 14 are in vision/clojure.md, vision/books.md, vision/models.md.
- Holds: no RebuildSkills, regeneration or re-pin until Field 42265e reports activation complete. Regeneration path witnessed: Curriculum reads a Nix store pin, not the live psyche-context; a landing reaches flows only after a re-pin and RebuildSkills.

## Chain per book (binding, in its final form)
Envelope → read subflow pre-maps landing lines → author subflow (rules before sources) → separate review-and-fix subflow with byte-for-byte quote grep → `node tools/book-check.mjs` → bb build → Artifact publish (new, or `url` after an ArtifactComments read; if the living commented, the page is not changed and the comment goes to the Secondary) → phone witness → link, proposal list, exclusions, owner work and open items to the Secondary.

## Rules learned at this seat, beyond flows/563761 and flows/288af9 summaries and the book 10 return
- A book carries psyche only: machine-module lines (knowledge-*, compensation-*, code) never appear; they go to a report for the Secondary.
- Every text-changing choice shows its lines, including «same paragraph in another module», «same word changed in choice N», and combined texts; a changed figure is shown whole, removed and added; a keep-as-is choice says so.
- His dated words open every fork at the fork; a fork without his words is labelled; the machine's order of choices is labelled machine reading; no open choices of the kind «another term the living names».
- Open questions never stay questions: each becomes numbered choices with lines; a question of his becomes a numbered proposal with the machine's design labelled.
- No narration, no «machine facts» paragraphs, no runtime facts (service state, deployed version); flow repository references build on main as it is (d190e10 at last witness).
- Working instructions and orders are not vision lines; a line that rests only on an order is dropped unless his words state it as how the system should be.
- No short-term or long-term mark unless his cited words say so (intent-psyche L10); «right now», «for now» about something else, are not marks.
- Provenance: all his words are STT, book comments included («STT», «STT, book comment», «STT, relayed by <flow>»); the review pass relabels nothing from a record's own provenance line. An undated record is cited undated or «logged by <date>, the machine's reading».
- A proposal building on an unruled earlier proposal says so on its File: line and offers land-with / wait / land-alone.
- A notion is cited, labelled, and never the base landing.
- Subflow types write-trivial/ordinary/demanding have no Skill tool; a brief to them carries the needed lines rather than skill names.
- His word of 2026-10-14 (vision/books.md): the rendered book carries the proposals only — figure, choices, lines — no verbatim quote, no record or source path, no provenance line, no «carries his words»; references live in an unrendered <book>.refs.md beside the source and are archived with the landing when a proposal is accepted. Variants are never repeated proposals: shared text once, each variant a numbered choice carrying only its differing words. A proposal stands as the default; no land/amend/drop choices, no choices restating it; no «machine choice: reason» narration (to refs). A mostly rewritten line shows as one removed and one added line. A URL in a message is pasted from the receipt, never typed.

## Open decisions (his; numbered choices in the books, none ruled)
- Book 10: P1 orchestrate reservation and held/repair ledger; P1 7–8 flow id in Flow's answers; P2 6–7 when the old flow stops receiving; P3 L12; P4 routing guidance vs hard-enforced; P5 intent module wording; P6 session-reader home, 6–9.
- Book 11: P1–P15, notably P3 expression levels vs vision-model-roles, P8 where Flow's memory lives, P10 config loading vs L56, P12 identifier of words, P15 implemented before the comment.
- Book 12: P1–P13, notably P2 «recent» measure, P4 escalation bounded to the aspect, P5 container of typed flows, P7 declarative deployment, P10 main only, P11 Clojure tools as notion, P12 builds on book 11 P15, P13 archives (c6 defers to book 13 — book 13 does not carry it; if ruled, a revision of book 13 or a book 14).
- Book 13: P1 the whole's name, P2 handover by reading vs handover in the transcript (four choices), P3 where artifacts live, P4 phases unnamed vs the three names.
- Inherited, unruled: books 01–09 items in flows/563761/summary.md, flows/288af9/summary.md, flows/c5f24b handover.

## Next bounded work
- Two books ordered by Core on 2026-10-14, briefs in flows/df159a/brief-patterns.md: (A) book 14 Version 7 at its URL — approaches and standard patterns, per-file code to refs, no Terra; (B) new book «Ethos and Datom in Clojure and EDN» — a vision context module for translating Ethos/Datom into Malli schemas and EDN, pattern and standard entry point. Neither was started: the subflows were stopped and the lane restored to HEAD at refresh. Link and account to the Secondary for each.
- Awaiting the Secondary: acceptance of book 14 Version 6 and the second edition Version 4; the Communication pair lands book 14's former P4 (approved), not this seat.

## Topics to split
- Owner-work dispatch: the three reports are with the Secondary; whether owners (Mind, Field) received them is unwitnessed here.
- The P15 question (books implemented before the comment) touches knowledge-psyche and compensation-psyche-interraction; the machine proposal is in reports/book-11-p15-machine-proposal.md.
- Three flow logs still name tools/book-build.py (da2038, d68c82, df159a); the file is gone; logs are history and stay.

## References for retrievable facts
- log.md: every receipt, version id, audit list, and Secondary message summary, in order.
- books/*.md: the books' sources; books/batch-*.edn: the envelopes.
- flows/c5f24b/books/10-messaging-between-flows.md: book 10 in its final form (this seat's Version 2 edit).
