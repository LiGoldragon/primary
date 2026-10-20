# Comment routing: re-witness and book, 2026-10-17

Subflow of d68c82. Host clock at check: 2026-10-17 11:00 -06:00.

## Re-witness (counts only)

- da2038's list (unrelayed-comments-2026-10-17.md, written 10:58 -06:00) sorts 66 threads: section A 10, B 35, C 11, D 10. B + C = 46.
- Relay ledger flows/7c89aa/comment-relay-ledger.jsonl: 164 lines, 145 distinct threads. Every line targets d68c82 (154 relayedTo d68c82, 4 to d68c82, 6 relayedTo "Psyche Core Secondary"). Newest entry 2026-10-17T16:41.
- Section B: 35 of 35 thread ids are in the ledger, so d68c82 received them. 0 of 35 ids, and 0 of 26 checkable comment phrases (9 comments too short to phrase-check), appear in flows/da2038/. d68c82/log.md records relays to da2038 only for batch-09 comments (log:1195, section D) and the no-quotes psyches (log:1225); none for the 7 section B books.
- Section A: 0 of 10 ids are in the ledger or any flow file. Phrases from 6 of the 10 now appear in da2038 files written at 10:59 -06:00, after its audit, by da2038 itself (d68c82/log.md:2110), not by relay.
- Section C: 0 of 11 ids in the ledger (pre-ledger).
- Not re-witnessed: section D's 10 and the claim of no forward for section C.

## Role modules (field-context origin/main 95121c6; local checkout is detached at 5070467)

- role/comment-relay.md: sends one --psyches envelope with hm-send "to the registered Psyche core Secondary"; the caller names only the book, or books updated since the last ledger entry.
- role/comment-relay-description.md: relays new threads "to the Psyche core Secondary".
- role/psyche-core-tertiary.md: acts on the living's notice; no watch or timer; "The Psyche core Secondary routes the relayed comments."
- Brief: flows/7c89aa/handover.md and continuation.json say the same: relay only to d68c82, only for named books, no watch, timer or poll.
- No module sends a topic's comments on to the metaflow that owns it.

## Book

- Source: /home/li/primary/flows/d68c82/books/61-every-comment-reaches-its-metaflow.md
- References: /home/li/primary/flows/d68c82/references/61-every-comment-reaches-its-metaflow.md
- Page: /home/li/primary/flows/d68c82/books/61-every-comment-reaches-its-metaflow.html
- book-check.mjs: checked true. book-build.clj: exit 0. Phone width 390 px: rendered in headless Chrome, all four diffs readable, no overflow.
- Proposals: 4 (field-context role/comment-relay.md, role/comment-relay-description.md, role/psyche-core-tertiary.md, compensation/main-flow.md).
- Published: no. This subflow has no Artifact tool. d68c82 publishes the built page.

## Open

- Which seat of the owning metaflow is the target (its Secondary, or a same-layer Tertiary) is left open by the proposals.
- The Skill tool was not available in this subflow, so flow-evidence was not loaded before writing this receipt.
- Beads: none opened or closed.
