# Context of 33752b when it wrote «Three lines from the chat, second edition»

Flow measured: 33752b, Psyche Core Primary (Fable, Claude).
Book: «Three lines from the chat, second edition», source
`/home/li/primary/flows/33752b/books/36-three-lines-2.md`, page
https://claude.ai/artifact/LJwdWFHBuGxXEw7m7nYcxX.

Source read: 33752b's live transcript under
`/home/li/.claude/projects/-home-li-primary/` (file name not relayed:
no provenance receipt handoff exists for this thread, so that receipt
evidence is unavailable). Line numbers below are lines of that file.

## The writing turn (witnessed)

The book text was composed by 33752b itself in one API call at
2026-10-13 17:43:00 UTC (11:43 CST; the brief's "~17:40" is UTC),
transcript lines 4563-4565: the presentation text (line 4564), then an
Agent call to a `book` subflow with "source verbatim below" (line 4565),
which wrote the `.md` at 11:43 local and published it.

Usage of that call (line 4563):

    input_tokens                 2
    cache_creation_input_tokens  598
    cache_read_input_tokens      407,643
    total context                408,243
    output_tokens                2,713 (463 thinking)

One auto-compaction happened before it, at line 2146
(2026-10-12 18:27 UTC; 321,583 tokens before, 19,888 after). The first
call after it (line 2178) carried 55,608 tokens. So the 408,243 are
a 55,608-token base plus 352,635 tokens accumulated over 238 API calls
in the 23 hours since.

## Figure: the context as stacked parts

Stacked in context order, top first. Tail topics are grouped; in the
transcript they interleave. R relevant, A adjacent, N noise.

```
 33752b context at 17:43:00 UTC
 408,243 tokens
+--------------------------------------------+
| BASE AFTER COMPACTION            55.6k     |
|  system prompt, agent list   1.8k  R       |
|  tools Agent Bash Read Write 3.9k  R       |
|  tool Artifact              14.9k  N       |
|  9 other tool schemas       10.2k  N       |
|  skills: book, psyche, etc.  8.7k  R       |
|  skills: commit, msgr, launch 5.8k N       |
|  compaction summary          5.9k  N (1k R)|
|  git status, CLAUDE.md, misc 4.7k  N       |
+--------------------------------------------+
| TAIL: 23 HOURS OF WORK          352.6k     |
|  committer, Herdr, nuts and                |
|  bolts                      70.1k  N       |
|  anatomy/values audits,                    |
|  Field lines, handover      44.1k  N       |
|  skills cleanup ed1/ed2,                   |
|  landing and revert         67.8k  N       |
|  makeshift, short/long,                    |
|  Mind Flow mission          50.6k  N       |
|  figures, review-is-psyche,                |
|  hm-send, inventory         26.1k  N       |
|  Spirit crystallization                    |
|  packet + book              44.5k  A       |
|  shoelaces, context modules,               |
|  flowchart and term probes  31.9k  A       |
|  Three lines ed1             5.2k  R       |
|  his comments, provenance,                 |
|  Ethos wording, Field note  12.2k  R       |
+--------------------------------------------+
        |
        v
 R  32.7k   8%
 A  76.4k  19%
 N 299.1k  73%
```

## Method

Tail (352.6k, measured): for each pair of consecutive API calls, the
growth in total context (input + cache creation + cache read) is the
tokens added by the records between them. Each delta is split over
those records in proportion to their text length. Harness bookkeeping
records (prompt snapshots, deferred-tool records, file-history
snapshots, queue operations) are excluded as not sent. Thinking text is
stored empty in the transcript, so any retained thinking is spread over
the other records of its segment.

Base (55.6k, estimated): the parts after compaction were measured in
characters (191,424 total, read from the prompt snapshot at line 2181
and the attachments at lines 2147-2177) and converted at one uniform
3.44 characters per token, the ratio that makes them sum to the
witnessed 55,608. Per-part figures in the base are therefore estimates;
the base total is witnessed.

Relevance is judged against the job of that turn: write the second
edition from the first edition, the living's seven comments on it, the
Secondary's four instructions on them, the provenance and record-
correction lines, Ethos Primary's wording, and Field's note that new
books need a Crystallization heading. "Adjacent" is material on a
subject one proposal touches, of which only a small kernel was needed
(estimated at about 3k of the 76.4k). This classification is my
inference.

## Base after compaction: 55.6k

| Part | Chars | Tokens (est.) | Class |
|---|---|---|---|
| System prompt (main-flow seat text) | 2,120 | 0.6k | R |
| Agent listing (subagent types) | 4,147 | 1.2k | R |
| Tool schemas, 14 tools | 99,326 | 28.9k | |
| of which Artifact | 51,122 | 14.9k | N |
| SendFeedback | 8,350 | 2.4k | N |
| ScheduleWakeup | 7,427 | 2.2k | N |
| Agent | 7,274 | 2.1k | R |
| AskUserQuestion | 5,432 | 1.6k | N |
| ReadNotifications | 3,943 | 1.1k | N |
| Bash | 3,286 | 1.0k | R |
| Skill | 3,005 | 0.9k | N |
| ToolSearch | 2,143 | 0.6k | N |
| Read | 2,009 | 0.6k | R |
| ReportFindings | 1,969 | 0.6k | N |
| ListAgents | 1,715 | 0.5k | N |
| Edit | 989 | 0.3k | N |
| Write | 662 | 0.2k | R |
| Re-injected skills, 24 bodies | 49,639 | 14.4k | |
| of which book/psyche-related, 13 | 29,781 | 8.7k | R |
| of which unrelated, 11 | 19,858 | 5.8k | N |
| Compaction summary (Oct 10-12 work) | 20,124 | 5.9k | N, ~1k R |
| Deferred tools, CLAUDE.md, git status, env, files, misc | 16,068 | 4.7k | N |

Skills judged relevant: operation-book, trial-presentation-book,
compensation-book-distillation, vision-book, vision-distillation,
operation-psyche-distillation, knowledge-psyche, spirit,
knowledge-vocabulary, compensation-prose, compensation-correction,
compensation-design, operation-psyche-interraction (Proposals 3 and 4
target its lines).

Skills judged noise for this turn: operation-main-flow (5,125 chars),
compensation-messenger-clj (3,078), compensation-primary-commit (2,073),
operation-orchestrate (1,891), compensation-behavior (1,738),
compensation-launch (1,643), compensation-orders (1,061),
compensation-default-effort (944), operation-edit-coordination (851),
compensation-understanding (773), compensation-truth (681).

Witnessed in the same attachment: these bodies are the startup copies
of 2026-10-10. The vision-book body in context still reads "Every book
has a distillation section: it proposes the lines that move the
living's words into skills", while 33752b's own subflow had renamed the
term to crystallization at 17:35 and Field's message at 17:42 said new
books require a Crystallization heading.

The compaction summary covers pre-compaction work: the book on psyche
abuse, the PrimaryPublish lock and commit procedure, messenger usage,
psyche-skills landing paths, and the arrangement with d68c82. Its book
rules paragraph (about 1k) bears on the job; the rest does not.

No skill was loaded through the Skill tool after compaction.

## Tail by origin: 352.6k (measured)

| Origin | Tokens |
|---|---|
| Messages from other flows (#msg), direct or queued | 81.4k |
| Subflow completion notifications (task-notification) | 65.2k |
| 33752b's own chat text (presentations, book sources) | 60.8k |
| 33752b's Bash calls (log and psyche appends, hm-send bodies) | 49.4k |
| 33752b's Agent briefs | 33.8k |
| of which to book subflows | 15.1k |
| Agent results returned in-line | 25.3k |
| of which from book subflows | 15.3k |
| Relayed psyche (#psyche, #psyches) | 11.5k |
| Harness reminders (batching, hook context, token count, skill list) | 20.1k |
| Bash and TaskStop results | 3.4k |
| The living, direct in this chat | 0.9k |

The living's own words reach this flow almost only as relays: 11.5k of
#psyche against 81.4k of #msg and 65.2k of notifications.

## Tail by topic: 352.6k (measured), relevance (inference)

| Lines | Topic | Tokens | Class |
|---|---|---|---|
| 2147-2299 | who commits Primary; the living's complaints | 12.3k | N |
| 2300-2471 | committer design revisions 1-5, persistence, Herdr restart | 24.6k | N |
| 2472-2659 | «Our abstraction beside another's», «Nuts and bolts» | 33.3k | N |
| 2660-2862 | anatomy and values audits, «Anatomy audit» | 24.9k | N |
| 2863-2955 | «Two Field lines without a source» | 8.2k | N |
| 2956-3034 | «Handover and the seat without a shovel» | 10.9k | N |
| 3035-3092 | skills-cleanup packet | 17.0k | N |
| 3093-3112 | «Context modules» ed1 | 3.7k | A |
| 3113-3482 | skills cleanup eds 1-2, landing, revert, page overwrite | 50.8k | N |
| 3483-3590 | over-correction research, «Tripping over the shoelaces» | 13.3k | A |
| 3591-3744 | makeshift thread with Spirit; cleanup ed2 replaced | 24.4k | N |
| 3745-3828 | «Context modules» ed2 | 9.4k | A |
| 3829-3909 | makeshift, «Short-term and long-term vision» | 7.7k | N |
| 3910-4039 | Mind Flow mission package | 16.1k | N |
| 4040-4064 | lost flowcharts, visualization research | 3.4k | A |
| 4065-4086 | distillation-term inventory | 2.2k | A |
| 4087-4131 | «Three lines from the chat» ed1: order, text, publish | 5.2k | R |
| 4132-4168 | Mind mission accepted | 2.4k | N |
| 4169-4285 | «Figures that move», short/long landing, «What you review is psyche» | 16.3k | N |
| 4286-4337 | figures retarget, Field figure witness | 5.8k | N |
| 4338 | Spirit recrystallization packet, one queued #msg | 33.5k | A |
| 4339-4420 | «Crystallization» book | 11.0k | A |
| 4421-4524 | his comments on ed1, provenance fix, Ethos wording | 11.9k | R |
| 4525-4560 | hm-send identifier order, short/long inventory | 4.0k | N |
| 4561-4562 | Field: new books need Crystallization | 0.2k | R |

## Totals

| Class | Base | Tail | Total | Share |
|---|---|---|---|---|
| Relevant | 15.3k | 17.4k | 32.7k | 8.0% |
| Adjacent | 0 | 76.4k | 76.4k | 18.7% |
| Noise | 40.3k | 258.8k | 299.1k | 73.3% |
| Total | 55.6k | 352.6k | 408.2k | |

Noise share: 73% strict. Counting the adjacent material beyond its
~3k kernel as noise too: about 91% (roughly 35k of 408k bore on the
book).

## Biggest causes and what would have removed each

1. One long-lived Primary carrying every topic since compaction:
   twenty topics over 23 hours, 258.8k tokens of unrelated work in the
   tail. Removal: a fresh flow per book, given only the packet for that
   book (first edition, his comments verbatim, the Secondary's
   instructions, target texts as they stand). That context would be
   about 35-50k instead of 408k.
2. Whole packets and messages delivered into the Primary's own
   context: 81.4k of #msg and 65.2k of subflow notifications in the
   tail, including the 33.5k Spirit packet (one message), cleanup
   packets of 8.5k, 3.5k and 3.6k, and five committer-design
   revisions. Removal: a packet goes to the subflow that consumes it,
   by path, and the Primary receives only the order and the result;
   notifications carry a one-line status rather than the subflow's
   full return.
3. The Primary composing books itself and carrying each one two or
   three times: 60.8k of its own chat text (presentations are whole
   book sources), 15.1k of book-subflow briefs repeating those sources
   verbatim, 15.3k of book-subflow returns, and 49.4k of Bash calls
   whose bodies re-append relayed psyche and messages to its log.
   Removal: a book-author subflow composes and publishes from the
   packet; the Primary writes only the order and logs by path.
4. Tool schemas the seat never uses: 28.9k, of which Artifact alone is
   14.9k, though publishing is delegated to a book subflow. Removal: a
   Primary seat tool set of Agent, Bash, Read, Write (3.9k); drop
   Artifact, SendFeedback, ScheduleWakeup, AskUserQuestion,
   ReadNotifications, ReportFindings, ListAgents, ToolSearch.
5. Skills as a frozen startup bundle: 14.4k re-injected at compaction,
   5.8k of it unrelated to books (commit, messenger, launch, orchestrate
   locks), and stale: the vision-book copy in context still names a
   "distillation section" in "skills" after the rename to
   crystallization and context modules. Removal: smaller, task-scoped
   skills loaded fresh for the book task, so the context holds the
   current text once.

## Possible causes of the muddle beyond volume (hypotheses, not witnessed)

- Competing terms present at once: the stale skill copy (distillation,
  skills), the living's comments (crystallization, context, modules),
  and Field's checker note. The second edition names targets in a mix
  ("psyche-context, vision-book", "the main-flow context (today
  tools/main-flow-mode/system-prompt.md in Primary; its move ... is
  with Field)").
- Four unrelated proposals arrived as separate relays over 25 minutes
  (fault line, flowchart, provenance, record correction) and were
  joined into one book under the first edition's title.
- Operational routing facts from the Secondary's instructions (where
  the file lives today, who moves it) entered proposal text.
- Context size itself: 408k tokens with the relevant 8% spread across
  two places in the tail (lines 4087-4131 and 4421-4562), separated by
  300 lines of other work.
