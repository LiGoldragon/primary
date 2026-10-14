# Handover: Psyche Core Tertiary comment relay (7c89aa)

## Role
When the living says he commented on a book: read every comment on it with ArtifactComments, recover each full anchored passage from the artifact page (the listing truncates it), send the comments whole as one `--psyches` envelope per book to the Core Secondary d68c82 (title, section, full passage, his exact words, author, time, input mode), then append to the ledger. No watch, timer, poll, reply, resolve or publishing. Nothing new means nothing sent; never resend.

## Paths
- Ledger: /home/li/primary/flows/7c89aa/comment-relay-ledger.jsonl (48 lines; last relayed threads: b31380b8, 8b0844df, d318c400 of "Dense and visual", 2026-10-14T14:15 to 14:19). Read it before every send; write lines only after a `Transported` or `Presented` receipt.
- Psyche records: /home/li/primary/flows/7c89aa/vision/flow-ids.md and /home/li/primary/flows/7c89aa/vision/books.md (verbatim, logged when spoken).
- Reads of comments go through general-purpose subflows (read-trivial lacks the Artifact tool).

## Method that works
Send from a file: `FLOW_ID=7c89aa timeout 100 hm-send d68c82 --psyches --stdin < file.edn 2>&1`, then append ledger lines only if the output has Transported or Presented. A stray `2>&1` after a heredoc terminator once hung a send; do not build the send as a heredoc inside `$(...)`.

## State
- Active writes: none. Active subflows: none (every subflow has reported). One hung background shell was stopped.
- The "Flow philosophy and artifacts" envelope (4 items) has no hm-send receipt; delivery is inferred from d68c82's log; its ledger lines say so.
- The ledger's newest lines are not yet confirmed committed by the Primary committer (89fbc1).

## Open judgments
1. The living's "Crystallization" book screenshot ("This book is visually broken") is not yet relayed; waiting for his word whether to send it.
2. Proposed line for `compensation-prose` (flows named by role in chat, ids only in messages that need a target) awaits his approval or hand-off to the owning flow.
3. Committer backlog order (catch up all commits and merges, lose nothing) is unanswered; the cause of the backlog and of its earlier false "clean" receipts are unknown.
4. Whether a comment's input mode can be learned (typed or spoken): the tool does not say, so none is corrected and the envelope states it.
