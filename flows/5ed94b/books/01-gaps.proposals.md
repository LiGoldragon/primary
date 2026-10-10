Presentation.{ «Where flows do a program's work by hand» }

Flows still do by hand what a program should do: publishing, waiting on locks, claiming ids, stamping times, relaying comments. Each costs context, money and mistakes, and some have lost work. Every fix below is one edit to one context module, so you can say yes or no to each in a breath. Each is marked: does the program exist today?

1. Intent, create: "Anything deterministic is done by code, never by a model, to save the context, cost and noise a model would incur."
   Rests on: your 16:17 words, "anything that is deterministic into code".
   Program: not applicable; this is the rule the rest follow.

2. Operation "compensation-primary-commit", replace whole text with: "A flow names its paths to the publisher. It does not lock, commit, copy, push or release by hand."
   Rests on: "flows never type jj in Primary" and your wish for one command.
   Program: built, not yet reviewed or in use. One lane publish cost a flow 26 deleted files.

3. Operation "edit-coordination", edit the last rule to: "When a lock is refused, ask to be told on release, then stop. The program wakes you."
   Rests on: your no-polling rule and the cost of asking holders.
   Program: does not exist. Locks refuse and name the holder, but nothing announces a release.

4. Operation "stale-lock", edit: "The program decides whether a holder is alive and frees its lock. A flow never judges it."
   Rests on: "deterministic into code".
   Program: does not exist. Locks have no lease and no check of the holder.

5. Operation "orchestrate", edit: "Never write a lock request by hand. Name the paths and the reason to the lock tool."
   Rests on: "save the context, cost, and noise".
   Program: does not exist. Only the raw client; curly quotes in a reason have stalled cleanup.

6. Operation "main-flow", replace the flow-id line with: "The id is in the prompt." Also remove "put the id in every subflow brief".
   Rests on: "no reason for us to make the model check the flow ID".
   Program: half exists. Launching can hand over the id; for Codex seats it is not built.

7. Operation "main-flow", remove the line that adds the flow's own row to the index.
   Add to Knowledge "knowledge-flow": "The flow's row in the index is written by Flow when the flow starts."
   Rests on: "deterministic into code".
   Program: does not exist. Flow already holds flow rows, so it could.

8. Operation "trial-succession", split: keep the judgement (what the successor must know); move the launching, handover and closing of the old seat to one line: "Ask Flow to replace the seat. It launches, registers and closes."
   Rests on: "deterministic into code".
   Program: built and deployed, but seats are not started through it, so it is unused.

9. Operation "trial-reaping", replace with: "Name the abandoned seat. One command closes, archives and deregisters it."
   Rests on: "deterministic into code".
   Program: partly. The pieces exist but ask for arguments no flow can supply.

10. Operation "trial-generated-projection", remove, once the regenerator's check runs on every commit.
    Rests on: "save the context, cost, and noise".
    Program: the check exists but nothing runs it on commit. Remove only after that is wired.

11. Operation "file-editing", edit: "The log is appended by a tool that stamps its own time. Never write the log file, and never guess a time."
    Rests on: "deterministic into code"; stamps ran up to an hour fast.
    Program: does not exist. Five log entries have been dropped by a rewrite, and times were guessed in several flows.

12. Operation "operation-relaying-the-living", edit: "Comments on a book arrive in your message. You do not fetch them."
    Rests on: your question about a hook for comments, and "I did comment".
    Program: does not exist. A fetch tool exists, but nothing wakes a flow on a new comment.

13. Operation "compensation-messenger-clj", edit: "State changes are read from Flow. Send a message only to hand over words, never to report state."
    Rests on: "Why is everybody bothering you with things that you shouldn't be bothered with?"
    Program: half. Messages deliver; shared state others can read does not exist.

14. Operation "lojix", edit: "Name what to deploy. The program builds the request and the retry. Never write fields by hand."
    Rests on: "things actually happening as I ask them".
    Program: does not exist. One failed deployment cost hours.

15. Operation "flow-evidence", edit: "Receipts and checksums are kept by code. A flow never holds a hash."
    Rests on: "no hashes in a model's context".
    Program: does not exist.
