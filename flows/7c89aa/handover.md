# Handover: psyche core tertiary comment relay (7c89aa)

## Role
When the living says he commented on a book (or names a topic with comments): read every comment on it with ArtifactComments (through a general-purpose subflow; read-trivial lacks the Artifact tool), recover each full anchored passage from the artifact page (the listing truncates it), send new comments whole as one `--psyches` envelope per book to the Core Secondary d68c82 (book title and URL, section, full passage, his exact words, author, time, input mode), then append to the ledger. His direct speech goes as `--psyche` or as the first pair of the book's envelope. Nothing new means nothing sent; never resend. No watch, timer, poll, reply, resolve, publishing, restart or fix of anything; orders for work go to the Secondary to route. When he names a book loosely (speech-to-text), find it by title in the artifact list; if he names none, scan books updated since the ledger's last entry.

## Paths
- Ledger: /home/li/primary/flows/7c89aa/comment-relay-ledger.jsonl, 112 lines. Last entry: "Drawing ideas", thread b00f1917, 2026-10-16T17:49. Read it before every send (grep 8-character thread prefixes); write lines only after a Transported or Presented receipt.
- Psyche records, verbatim: flows/7c89aa/vision/flow-ids.md, books.md, ethos-in-clojure.md, fable.md.
- Send method: write the EDN to a file, then `FLOW_ID=7c89aa timeout 100 hm-send d68c82 --psyches --stdin < file 2>&1`, then ledger lines only on a Transported or Presented receipt. Never build the send as a heredoc inside `$(...)`.

## State
- No relay, write, subflow or lock is in flight. Every subflow has reported.
- Waiting deliveries: none. Every send returned Transported; receipts reading "working" mean the Secondary was busy when it arrived. A Transported receipt does not prove a read. The "Flow philosophy and artifacts" envelope of 2026-10-14 had no receipt (its command hung); delivery was inferred from the Secondary's log, and its ledger lines say so.
- Nothing has been relayed twice; the next successor must not resend any ledger thread.
- The committer (89fbc1) published the ledger and records through 2026-10-16 at the last report; the newest lines may not yet be committed.

## Open judgments
1. The "Crystallization" screenshot ("This book is visually broken", 2026-10-13) was never relayed; the living has not said whether to send it.
2. Proposed compensation-prose line (flows named by role in chat, ids only in messages that need a target) awaits his approval or hand-off to the owning flow. A newer order of his: flow titles and every pane or tab are the datom struct, topics uncapitalized.
3. The comment tool does not say typed or spoken; no corrections are made and the envelope states it.
4. The committer's backlog order of 2026-10-13: its cause was never established.
