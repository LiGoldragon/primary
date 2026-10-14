# { Psyche Flow Primary c5f24b } — handover

Judgment only. Facts and words live in log.md, books/, and the published pages; a tool fetches them.

## State
- Batch 06 (09-context-modules, 10 proposals) at https://claude.ai/artifact/UQiKz4ZHVfgREo6CHHRmkU Version 3, accepted by Psyche Flow Secondary da2038.
- Batch 07 (10-messaging-between-flows, 6 proposals) at https://claude.ai/artifact/YBBK3jSZuoivFtB25Eg82s Version 1, sent to the Secondary with seven open questions; return or acceptance pending. Batch 08 is the successor's; not seen here.
- Chain per batch: envelope extracted from this transcript into books/batch-NN-psyches.edn → author (a type with the Skill tool; rules before sources, landing points pre-mapped by a read subflow) → review-and-fix in one subflow → page built by scratchpad build09.py (book-agnostic: md → html, figures auto-drawn from ASCII, tail from tools/book-code.html; the scratchpad dies with the session, so the next seat rebuilds it from flows/c5f24b/books/09-context-modules.{md,html} as this seat did from 08) → Artifact publish (new, or `url` set on a return after an ArtifactComments read) → 320/375 px light/dark witness in headless Chrome on the local file wrapped in the artifact skeleton (the published URL does not load headless) → link, facts, open questions to the Secondary.
- tools/book-code.html carries two unstaged CSS lines from this seat (diff panel min-width, overflow-wrap) fixing a 320 px overflow; the committer lands them.

## Open decisions (his; numbered choices in the books)
- Book 09: subaspect/topic layout vs flat skills/ (P2); metaflow module per layer and subagent section home (P3); hook-injected queue scope (P4); registry hash form, blake3 over tree/commit/tarball (P5–P6); vision in the user prompt (P7); flow-ethos vs vision-flow-ethos name (P8); «[ethos] environment» reading (P9); umbrella name for the three variants, metaflow or diverge (P10).
- Book 10: orchestrate reservation kept for repair! or removed (P1); which hooks duplicate goes (P2); L12 «one run of a voice» (P3); routing guidance vs hard-enforced, three rulings (P4); the intent module's wording (P5); session-reader role home (P6).
- Open questions sent to the Secondary with each book (log.md); none in the books.
- Inherited, unruled: batch 04/05 items in flows/288af9/summary.md; batches 01–03 in flows/563761/summary.md.

## Rules that bind every Flow book from this seat
- Those in flows/563761/summary.md and flows/288af9/summary.md, plus the Secondary's batch 06 return in its final form: no narration at all; every landing and every text-changing choice shows its lines; a choice without his words is labelled machine choice with a one-line reason, a reading labelled machine reading; Ethos marked «Ethos, the Ethos metaflow's. Apart.»; no long-term mark unless cited words say so; Destroy/Archive in the `**Destroy**`/`**Archive**` paragraph form (classes record destroy/archive); a file shown standing exists now, else builds-on or (uncommitted); a machine fact (Mind's, Curriculum's) labelled so, never as his; a term he has not used explained once; a speech-to-text error shown bracketed with the proposed reading as a choice.
- A statement already landed is context, never re-proposed. A tension between his dated words is surfaced with both sides cited and rulings as choices, never resolved by the machine.
- A URL in a message is copied from the publish receipt.

## Next bounded work
- The Secondary's return on book 10 (batch 07) is the successor's: fix in place at the same URL after an ArtifactComments read, phone check, link back; if he commented on the page, the page is not changed and the comment goes to the Secondary. Then batch 08 from the Secondary, same chain.

## Topics to split
- Shared page build: build09.py should live in Primary tools/ (a committer landing), not a scratchpad; its Destroy/Archive and figure renderers are the only non-trivial parts.
- Deterministic work as intent (book 10 P5) touches every seat skill, not vision-flow.
- Flow knowledge / session reading (book 10 P6) is a subflow-role topic, not messaging.
- messenger-clj lock/queue (book 10 P1) is Flow's, per his 2026-10-11 words; the orchestrate reservation in messenger-clj is a leftover.

## Measured
- Field measured 148,145 input tokens at 01:04 UTC. Report measured figures only.
