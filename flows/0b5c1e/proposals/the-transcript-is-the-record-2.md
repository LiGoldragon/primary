Presentation.{ «The transcript is the record» }

# The transcript is the record

*Created by Opus, drafted by Sonnet.*

### Proposal 1: The rule and a shorter last line · psyche-belief › intent/energy.md

**Comment** The rule is added; the last line loses its clause about files.

+ ```mermaid
+ flowchart TB
+     subgraph A["intent:energy proposed"]
+         t["the transcript"] -- "is the record of" --> w["a flow's work"]
+         a2["a flow"] -- "writes" --> p["a proposal for the living, a record of his words a later flow needs, the report its briefer asked for by name"]
+         a3["a flow the living is not conversing with"] -- "writes nothing in" --> c2["its chat"]
+     end
+ ```

  A text for the living is as small as its point: a comment on a proposal is a sentence or two, and the chat gives him one line.

+ The transcript is the record of a flow's work. A flow writes a proposal for the living, a record of his words a later flow needs, and the report its briefer asked for by name.
+
- A flow the living is not conversing with writes nothing in its chat: its work is what it writes to files and sends to flows.
+ A flow the living is not conversing with writes nothing in its chat.

### Proposal 2: The rule · mind-belief › intent/energy.md, a new file

**Comment** Mind has no energy module, so this one is created. Mind's default system modules gain intent-energy, which every Regular Mind metaflow takes first.

+ The transcript is the record of a flow's work. A flow writes a proposal for the living, a record of his words a later flow needs, and the report its briefer asked for by name.

### Proposal 3: The rule · field-belief › intent/energy.md, a new file

**Comment** Field has no energy module, so this one is created. Field's default system modules gain intent-energy, which every Regular Field metaflow takes first.

+ The transcript is the record of a flow's work. A flow writes a proposal for the living, a record of his words a later flow needs, and the report its briefer asked for by name.

### Proposal 4: The rule · primary › AGENTS.md

  Worker agents (non-management) *must* read @NON_MANAGEMENT_AGENTS.md.

+ The transcript is the record of a flow's work. A flow writes a proposal for the living, a record of his words a later flow needs, and the report its briefer asked for by name.

### Proposal 5: The relay keeps its state on the comment · field-belief › role/comment-relay.md

**Comment** The ledger lines go. The relay marks a relayed comment on the artifact, so the lines that left replying and resolving to the book flow go too.

- The calling Psyche core Tertiary names only the book, or the books updated since the last ledger entry. Carry out the whole comment relay; return only the printed receipt and the relayed thread ids.
+ The calling Psyche core Tertiary names only the book. Carry out the whole comment relay; return only the printed receipt and the relayed thread ids.

- A relay message is written for its reader and holds the book's title, where on the page (the section and the quoted text), and the living's words whole. Thread ids stay with the book flow, which alone replies or resolves. The relay goes through the Flow Nexus as a prompt to Psyche core Secondary: `flow 'Send.{ Address.{ Psyche core Secondary } Wake MiddleAbrupt.Psyches.[ { «context» «verbatim» } … ] }'`, «context» being the title and the place on the page, «verbatim» the living's words.
+ A relay message is written for its reader and holds the book's title, where on the page (the section and the quoted text), and the living's words whole. The relay goes through the Flow Nexus as a prompt to Psyche core Secondary: `flow 'Send.{ Address.{ Psyche core Secondary } Wake MiddleAbrupt.Psyches.[ { «context» «verbatim» } … ] }'`, «context» being the title and the place on the page, «verbatim» the living's words.

- Read FLOW_DIRECTORY/comment-relay-ledger.jsonl before sending. Check each thread prefix against the ledger. An ambiguous prefix is a blocker: resolve it to the full thread identity before sending. Do not infer missing provenance.
+ An ambiguous thread prefix is a blocker: resolve it to the full thread identity before sending. Do not infer missing provenance.

- Append ledger lines only after `flow` prints `Queued` or `Delivered`. Record the book, full thread identity and prefix, author, time, exact words, context and printed receipt. Keep the existing ledger lines. A refused send is not delivered: leave it pending and return that printed reply and the affected thread ids. Never resend a comment already recorded as delivered.
+ Once `flow` prints `Queued` or `Delivered`, mark the comment on the artifact itself with a reply or a resolve. A refused send is not delivered: leave the comment unmarked and return that printed reply and the affected thread ids. Never resend a marked comment.

- On a later notice, read all comments and relay only the new ones. A refreshed session keeps the same ledger. Return only the receipt and thread ids. Never reply to or resolve a comment, publish a book, or decide its ruling.
+ On a later notice, read all comments and relay only the unmarked ones: an unmarked comment is new. Return only the receipt and thread ids. Never publish a book or decide its ruling.

Pre-approved, his words: "all of this logging that agents are doing everywhere, I want this totally eradicated: every single trace of it."

### Proposal 6: The ledger leaves the brief · field-belief › role/psyche-core-tertiary.md

- Ask the appropriate flow to relay the comments; if it is unavailable, delegate comment relay to the Curriculum-composed comment-relay subflow. Its brief names only the book, or the books updated since the last ledger entry.
+ Ask the appropriate flow to relay the comments; if it is unavailable, delegate comment relay to the Curriculum-composed comment-relay subflow. Its brief names only the book.

### Proposal 7: Directories deleted · every repository › witnesses, migration, evidence and unrequested reports, a deleted file

**Destroy** The repositories' witnesses, migration, evidence and unrequested reports directories are deleted, one commit per repository.
