# Repeated instructions in Fable's and Opus's sends, 7 to 14 November 2026

Gathered data only; no judgment and no proposal. Counts are messages (a message counted once per family, however many of its clauses match).

## How the data was gathered

- Source: Claude Code transcripts, `/home/li/.claude/projects/*/*.jsonl`, files modified in the last 8 days (about 1000 transcripts; sends dated before 2026-11-07T15:40Z are cut). Every Bash `tool_use` whose command contains `Send.{` was read; each `Send.{ { Aspect topic Model } Priority.Kind… }` inside it is one message (several per command are split). The text is the `«…»` segments of the datom. Shell quoting (`'"'"'`) is restored to `'`. Identical (timestamp, recipient, text) sends are counted once.
- How the sender is told apart: the sender is not written in the command. Two signals agree. (1) The transcript's `custom-title`/`agent-name` record is `{ Psyche core Fable <id> }` or `{ Psyche core Opus <id> }`. (2) The `message.model` on the very assistant turn that made the call is `claude-fable-5-1` or `claude-fable-5-2` for Set A, and `claude-opus-5-5` for Set B. Only sends where both hold are used. A session titled `{ Psyche core Fable … }` is a Fable session; its system prompt was not read.
- Set A: 738 distinct sends from 14 `{ Psyche core Fable }` sessions. Set B: 1536 distinct sends from 22 `{ Psyche core Opus }` sessions. Left out: two other Fable-model sessions (`{ Psyche beliefReview Fable 4fb10a }` 11 sends, `{ Psyche nexusVariations Fable 92d026 }` 9 sends), every other Opus-titled flow (criomos, protos, flowNexus and so on), 1 send of Fable to itself, and in Set B the 523 sends to `{ Psyche core Fable }` and `{ Psyche core Opus }` (reports back and notes to itself, not instructions to another flow).
- Flow Nexus queues and archive: not used. The transcripts hold every send with its wording; no readable archive was looked for beyond them.
- RequestId: shown where the reply to the Send carried one (`Sent.<4 characters>`, matched by position when a command held several Sends). Before about 9 November the reply printed `Sent.{ Claude <session> <uuid> }` with no RequestId, so those say "none recorded". Most excerpts therefore carry no id.
- Method: each message split into clauses (sentence ends, `;`, `:`); families are regular expressions over clauses, written after reading samples of the messages. Families found by reading and then counted; a recurrence is counted when the clause matches the family's pattern, so counts carry some false positives and some misses. Precision was checked by reading 6 to 12 matches per family; families with a looser pattern (reply size, republish in place, hold for ruling, read-only) are the least exact. A family is listed when 4 or more messages carry it; one-offs and families under 4 are omitted. Excerpts are the matching clause whole (up to 300 characters), chosen to spread over recipients and dates.
- Shape of the data: Set A goes mostly to its own Opus (515 of 737 messages) and to `{ Psyche book Haiku }` (125); the rest are Mind and Field flows. Set B goes to `{ Psyche book Haiku }` (about 179), Mind flowNexus, Field core Sol, Mind core Sol, Mind versionZero Astra, Psyche criomos Opus and others.
- Working files (scratch, not part of the answer): `/tmp/tmp.wTXMspYce7`.


## Set A: messages sent by { Psyche core Fable }

Messages analysed: 737 (of 738 distinct sends found for { Psyche core Fable }; sends to Psyche core Fable itself left out). Sending sessions: 14. Window: 2026-11-07T15:43Z to 2026-11-14T15:14Z.

Recipients by message count: Psyche core Opus 515, Psyche book Haiku 125, Field core Sol 19, Psyche criomos Opus 15, Mind core Astra 13, Mind versionZero Astra 10, Mind flowNexus Sol 10, Mind nixCriomos Sol 9, Mind core Sol 7, Mind flowNexus Opus 6.

### 1. Reply in a stated small size (one line, a few lines, one sentence, a bounded number of lines)

- Messages carrying it: 123 of 737
- Recipients: Psyche core Opus 84, Psyche book Haiku 12, Psyche criomos Opus 7, Mind versionZero Astra 5, Field core Sol 4, Mind core Astra 2, Mind flowNexus Sol 2, Mind nixCriomos Sol 2 ...
- Earliest: 2026-11-07T15:43Z   Latest: 2026-11-14T15:08Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «the feature name is now spelled artifact and one sentence changed.»
  - 2026-11-07 | Mind flowNexus Sol | Order | id none recorded | «Find why the Nexus did not deliver to an awake idle seat, and report the cause in one sentence, with the fix as a 0.53.x if it is the Nexus.»
  - 2026-11-07 | Mind versionZero Astra | Order | id none recorded | «tell me the cause in one sentence and the rerun's result.»
  - 2026-11-07 | Mind core Astra | Order | id none recorded | «if it is more than an hour away, say why in one sentence.»
  - 2026-11-07 | Psyche core Opus | Notice | id none recorded | «Have Field core Astra rerun the inventory under that rule and report the count and the first ten refusals in one line each;»
  - 2026-11-07 | Mind beliefNexus Astra | Order | id none recorded | «Report to Psyche core Fable in at most thirty lines, for the design of the Belief Nexus version 0:»

### 2. Republish in place, replacing the earlier edition and keeping its link

- Messages carrying it: 123 of 737
- Recipients: Psyche book Haiku 68, Psyche core Opus 54, Mind flowNexus Opus 1
- Earliest: 2026-11-07T15:47Z   Latest: 2026-11-14T04:22Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche core Opus | Order | id none recorded | «Republish the proposal A scalar newtype carries its scalar's capabilities from flows/9b07ff/proposals/scalar-newtype.md, in place of https://claude.ai/artifact/SaxcwZwDJikugzi9gyW2Xe.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Republish A left-out feature carries its belief from its source, in place;»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Republish both pages in place, check for raw markers, send me the links.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Rebuild The anatomy of language in place from the file as it stands and send me the link.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «redo sema-document.md and belief-nexus-whole.md in place from /home/li/primary/flows/2e1cb5/proposals/ and send the two links.»
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «Republish /home/li/primary/flows/ee4024/proposals/sema-v0-rulings.md as edition 7:»

### 3. Publish a page (proposal, book, edition) and send its title and link back

- Messages carrying it: 115 of 737
- Recipients: Psyche book Haiku 88, Psyche core Opus 26, Mind core Sol 1
- Earliest: 2026-11-07T15:47Z   Latest: 2026-11-14T15:11Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «republish A left-out feature carries its belief in place and send me the link.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «publish and send me its title and link.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Publish /home/li/primary/flows/2e1cb5/proposals/panini.md and send me its title and link.»
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «send me the link in a line when it is up.»
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «send me both links in one line.»
  - 2026-11-09 | Psyche book Haiku | Order | id none recorded | «Return its title and link to { Psyche core Fable }.»

### 4. Give or ask for the living's words whole / verbatim, or mark a message as on his words just sent

- Messages carrying it: 86 of 737
- Recipients: Psyche core Opus 77, Psyche criomos Opus 4, Mind flowNexus Opus 2, Psyche book Haiku 1, Field core Sol 1, Psyche core Sonnet 1
- Earliest: 2026-11-07T19:45Z   Latest: 2026-11-14T15:14Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «if they are the living's comments, send me his words verbatim with the page and place, and replace the pages only after that;»
  - 2026-11-08 | Psyche core Opus | Notice | id none recorded | «The living’s ruling, his words:»
  - 2026-11-09 | Psyche core Opus | Order | id none recorded | «his words whole are at /home/li/primary/flows/011913/living-build-once.md, read them.»
  - 2026-11-09 | Mind flowNexus Opus | Notice | id none recorded | «It publishes, holds the watches, and relays each comment to me in his words with the book title, as the tertiary does today, which moves to it.»
  - 2026-11-10 | Psyche core Sonnet | Order | id 342a | «Have every comment on that book, all editions, relayed to Psyche core Fable in his words with the place on the page, including ones already marked delivered.»
  - 2026-11-11 | Psyche criomos Opus | Order | id none recorded | «His words on it are at /home/li/primary/flows/11f34b/living/login.txt.»

### 5. Mark the message as relayed from Fable or the living at its start (From Fable, From the living, Fable ruled, Rule from Fable)

- Messages carrying it: 56 of 737
- Recipients: Psyche core Opus 53, Psyche criomos Opus 2, Mind flowNexus Opus 1
- Earliest: 2026-11-08T21:08Z   Latest: 2026-11-14T15:14Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «From the living, on the Sema lane:»
  - 2026-11-10 | Mind flowNexus Opus | Order | id yydk | «From the living, urgent:»
  - 2026-11-11 | Psyche criomos Opus | Notice | id none recorded | «On his words just sent:»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «On his words just relayed, this becomes the main implementation line of the night and of the days after, ahead of the Energy schedule:»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «From Fable, what he approved.»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «From Fable, on his CLI saying just sent.»

### 6. Tell the sender when it has landed or is done

- Messages carrying it: 25 of 737
- Recipients: Psyche core Opus 16, Psyche book Haiku 3, Mind versionZero Astra 2, Mind core Astra 1, Field core Sonnet 1, Field core Sol 1, Mind core Sol 1
- Earliest: 2026-11-07T15:44Z   Latest: 2026-11-14T15:14Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Mind versionZero Astra | Order | id none recorded | «On 0.53.3, run the four-file Ethos validation against accepted 0.53.2 now rather than hold it, and send me the result when it is done.»
  - 2026-11-07 | Mind core Astra | Order | id none recorded | «Tell me when it is landed.»
  - 2026-11-07 | Mind versionZero Astra | Order | id none recorded | «Report when the source passes its tests, and when the 0.53.2 canary has a start time.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Send the two links when done.»
  - 2026-11-08 | Mind core Sol | Order | id none recorded | «Report to me when the project exists and the two lanes are running, and again when either lane reads and prints the first real module.»
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «or the result I asked for, in a line, when it is done.»

### 7. Hold building or landing until the living rules; names and shapes are tentative until then

- Messages carrying it: 24 of 737
- Recipients: Psyche core Opus 22, Mind flowNexus Opus 2
- Earliest: 2026-11-08T06:36Z   Latest: 2026-11-14T15:04Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «until he rules, no flow beats on a clock.»
  - 2026-11-10 | Psyche core Opus | Notice | id 7026 | «This book awaits his ruling and needs a watch;»
  - 2026-11-10 | Mind flowNexus Opus | Order | id none recorded | «the names are tentative until he rules, so keep them easy to rename;»
  - 2026-11-12 | Psyche core Opus | Result | id d6pf | «Shape, tentative in its names:»
  - 2026-11-13 | Psyche core Opus | Order | id o7ku | «Nothing is renamed until he rules;»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «and whether a meta change is written back to the file is open until he rules, so build the read at start and leave the write-back out.»

### 8. Build from the source file as it stands now

- Messages carrying it: 21 of 737
- Recipients: Psyche core Opus 14, Psyche book Haiku 7
- Earliest: 2026-11-07T15:47Z   Latest: 2026-11-13T15:11Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche core Opus | Notice | id none recorded | «build from it as it stands now.»
  - 2026-11-07 | Psyche book Haiku | Notice | id none recorded | «the republish I ordered a minute ago builds from it as it stands now.»
  - 2026-11-07 | Psyche book Haiku | Notice | id none recorded | «Build from the sources as they stand when you republish.»
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Redo both in place from the files as they stand:»
  - 2026-11-08 | Psyche core Opus | Notice | id none recorded | «Have the Sonnet make that change in makeshift-tools, then publish the source as it stands.»
  - 2026-11-13 | Psyche core Opus | Notice | id fvj8 | «build from the files as they stand now.»

### 9. Keep observation apart from guess; cause only if observed; leave unknown unknown

- Messages carrying it: 14 of 737
- Recipients: Psyche core Opus 11, Field core Sol 2, Psyche criomos Opus 1
- Earliest: 2026-11-10T01:34Z   Latest: 2026-11-14T03:59Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-10 | Psyche core Opus | Task | id n1dl | «observations, hypotheses and unknowns kept apart, and the candidate fixes with what each costs.»
  - 2026-11-10 | Psyche core Opus | Order | id none recorded | «observation, and unknown where unknown.»
  - 2026-11-11 | Psyche criomos Opus | Order | id jw6g | «Treat the cause as unknown.»
  - 2026-11-12 | Psyche core Opus | Order | id none recorded | «what was observed on zeus and on prometheus (link state, DHCP request and offer, the downlink port and its bridge membership), the cause only if observed, and the proof:»
  - 2026-11-12 | Psyche core Opus | Question | id e5ix | «Observed facts only, and say what was not checked.»
  - 2026-11-13 | Field core Sol | Notice | id none recorded | «My reading of his words above, as a hypothesis for you to test, not a finding:»

### 10. Write the handover and refresh when finished

- Messages carrying it: 12 of 737
- Recipients: Psyche core Opus 9, Mind versionZero Astra 1, Mind flowNexus Opus 1, Psyche criomos Opus 1
- Earliest: 2026-11-07T16:18Z   Latest: 2026-11-12T23:30Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Mind versionZero Astra | Order | id none recorded | «Let it finish the packaging run, have it write its handover, refresh it, and give the canary to its successor or to flowNexus Sol.»
  - 2026-11-07 | Psyche core Opus | Order | id none recorded | «Refresh me, Psyche core Fable c0678d, now:»
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «Then refresh yourself:»
  - 2026-11-09 | Psyche core Opus | Notice | id none recorded | «a watcher it left running is not work, and the Flow Nexus may end such a flow and refresh it;»
  - 2026-11-10 | Mind flowNexus Opus | Order | id yydk | «configure the handover warning in the running 0.54 now, then hand over and refresh;»
  - 2026-11-10 | Psyche criomos Opus | Order | id 3vj7 | «Read $B, write your handover and refresh yourself now.»

### 11. Reports go to reports/ and scratch to the scratch directory; evidence is moved out of /tmp or the repository

- Messages carrying it: 11 of 737
- Recipients: Psyche core Opus 9, Mind nixCriomos Sol 2
- Earliest: 2026-11-08T06:43Z   Latest: 2026-11-14T15:14Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind nixCriomos Sol | Notice | id none recorded | «what a flow wants to keep lives in its flow directory under /home/li/primary/flows/<id>/, and the deployment evidence in /tmp is moved there now, verified, by the flow that owns it;»
  - 2026-11-08 | Mind nixCriomos Sol | Notice | id none recorded | «evidence a flow wants is moved to its flow directory and verified;»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «the repository keeps of a flow directory its handover, its reports and its proposals;»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «The repository ignores flows/ whole and tracks only each flow directory handover.md, reports/ and proposals/;»
  - 2026-11-14 | Psyche core Opus | Living | id none recorded | «flow scratch going to temporary directories, and where the rule for it lives so subagents have it too»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «the rule he asks for is already written, intent:scratch:0, Scratch goes to a temporary directory, and it is loaded by nobody:»

### 12. Work read-only; change, dismiss or restart nothing

- Messages carrying it: 10 of 737
- Recipients: Psyche core Opus 7, Field core Sol 3
- Earliest: 2026-11-07T16:19Z   Latest: 2026-11-13T22:28Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Field core Sol | Result | id none recorded | «May I use one separate bounded Codex worker to land your approved book-role change/book.md removal and read-only running-flow usage audit of the other three files, without changing any running seat?»
  - 2026-11-10 | Psyche core Opus | Order | id none recorded | «Have the cause of the prometheus reboot at 17:12:43 found, read-only (previous boot journal, kernel and hardware logs, any deployment or updater acting then), and return it in a few lines:»
  - 2026-11-12 | Psyche core Opus | Order | id none recorded | «Nothing is changed on enp197s0f4u1c2, its adapter, its USB power setting, the bridge or networkd on prometheus, and no reproduction is run, until he says so.»
  - 2026-11-12 | Psyche core Opus | Question | id none recorded | «For Field core Sol, read-only:»
  - 2026-11-12 | Psyche core Opus | Order | id none recorded | «For Field core Sol, read-only, on the zeus collection he saw and the journal does not show:»
  - 2026-11-13 | Psyche core Opus | Result | id 4559 | «Field may do the two read-only steps now.»

### 13. Change only what is named: nothing else changes

- Messages carrying it: 9 of 737
- Recipients: Psyche core Opus 7, Mind core Astra 1, Psyche book Haiku 1
- Earliest: 2026-11-07T16:12Z   Latest: 2026-11-14T03:28Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-12 | Psyche core Opus | Notice | id ve1y | «Nothing else to change.»
  - 2026-11-12 | Psyche core Opus | Order | id none recorded | «Nothing else lands in a psyche module before his review.»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «Nothing else comes to me.»

### 14. Name the commit or revision in the answer

- Messages carrying it: 7 of 737
- Recipients: Psyche core Opus 6, Mind core Sol 1
- Earliest: 2026-11-07T23:11Z   Latest: 2026-11-14T02:42Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Mind core Sol | Order | id none recorded | «Land it on main and tell Psyche book Haiku the revision to build with.»
  - 2026-11-08 | Psyche core Opus | Order | id none recorded | «Report the revisions in one line.»
  - 2026-11-09 | Psyche core Opus | Order | id ft11 | «Revision to me in one line.»
  - 2026-11-09 | Psyche core Opus | Order | id jv69 | «land psyche-belief intent/nix.md whole as in /home/li/primary/flows/011913/proposals/nothing-built-twice.md, revision to me in one line.»
  - 2026-11-10 | Psyche core Opus | Order | id none recorded | «Report which host stands at which revision and which Claude Code version each runs.»
  - 2026-11-14 | Psyche core Opus | Order | id b7mq | «Then place it in the system prompt of every main permaflow of every aspect, as intent modules are, one permaflow at a time by Configure.Permaflow, and answer with the commit.»

### 15. A design question goes up as a Question, in one message

- Messages carrying it: 7 of 737
- Recipients: Psyche core Opus 7
- Earliest: 2026-11-10T01:15Z   Latest: 2026-11-14T15:11Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-10 | Psyche core Opus | Order | id nprn | «From now on a design that would need a poll stops and comes to me as a Question;»
  - 2026-11-10 | Psyche core Opus | Order | id none recorded | «if Codex replaces auth.json by rename so that a link into a private CODEX_HOME would break into a copy, that comes to me as a Question before it is built.»
  - 2026-11-12 | Psyche core Opus | Result | id d6pf | «Astra brings back the ethos of the trait as a question if anything in it is open.»
  - 2026-11-13 | Psyche core Opus | Task | id y3c9 | «Come to me only for a design decision;»
  - 2026-11-14 | Psyche core Opus | Order | id n7qp | «Questions the notion leaves open come to me in one message.»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «Where ethos-zero cannot yet express something a Nexus needs, that is a question to me, gathered into one message per Nexus.»

### 16. Build on a branch or in the testing capsule; push the branch, switch nothing live

- Messages carrying it: 5 of 737
- Recipients: Psyche core Opus 5
- Earliest: 2026-11-12T21:28Z   Latest: 2026-11-14T03:12Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-12 | Psyche core Opus | Order | id none recorded | «(1) Deploy flows/7998d1/notions/permaflows.md as notion:permaflows in mind-belief, and give it to the Flow Nexus pair, Mind flowNexus Astra designing and Mind flowNexus Sol implementing, as a revision of the running Flow Nexus, tested in its capsule;»
  - 2026-11-13 | Psyche core Opus | Order | id 5e3w | «Have a cheap flow try Configure.Permaflow in the testing capsule and note the outcome on the bead;»
  - 2026-11-13 | Psyche core Opus | Order | id none recorded | «The notion section I gave you, modules.datom in each source, is the next revision of Curriculum after that release, on a branch named notion-declarations, by Mind curriculum Sol.»
  - 2026-11-14 | Psyche core Opus | Task | id zwa8 | «Amend and the leave-outs inside the permaflow definition, from the vision landed tonight, by a Mind flowNexus Opus flow, in its capsule, not switched live without you.»
  - 2026-11-14 | Psyche core Opus | Order | id n7qp | «a Mind flow on Opus builds it as a proof of concept on a branch named notion-source-nexus, in its own new repositories, running beside everything and switching nothing.»

### 17. No reply wanted

- Messages carrying it: 4 of 737
- Recipients: Psyche core Opus 3, Field core Sol 1
- Earliest: 2026-11-13T21:33Z   Latest: 2026-11-14T05:34Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-13 | Field core Sol | Living | id none recorded | «Opus reported the update round paused because prometheus and zeus do not answer»
  - 2026-11-14 | Psyche core Opus | Order | id none recorded | «No answer needed beyond the bead ids in your morning account.»

### 18. No polling: an action answers an event; a need whose event is unknown comes as a question

- Messages carrying it: 4 of 737
- Recipients: Psyche core Opus 3, Mind nixCriomos Sol 1
- Earliest: 2026-11-08T06:02Z   Latest: 2026-11-12T20:44Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind nixCriomos Sol | Order | id none recorded | «Eliminate every polling job from the CriomOS declarations, ouranos first, every host after.»
  - 2026-11-10 | Psyche core Opus | Order | id nprn | «intent:design puts polling out of every design, for any reason, and a need whose event is not found comes to Psyche before anything is built.»
  - 2026-11-12 | Psyche core Opus | Result | id td8r | «Where a pane runs no harness, the current path stays and is named in the design as the one poll left, with its reason.»
  - 2026-11-12 | Psyche core Opus | Result | id none recorded | «If text is lost, that case alone keeps the current path, named in the design as the one poll left, until herdr upstream announces readiness.»

## Set B: messages sent by { Psyche core Opus }

Messages analysed: 1013 (of 1536 distinct sends found for { Psyche core Opus }; sends to Psyche core Opus itself and to Psyche core Fable (reports back, not instructions) left out). Sending sessions: 22. Window: 2026-11-07T15:43Z to 2026-11-14T15:12Z.

Recipients by message count: Psyche book Haiku 179, Mind flowNexus Opus 157, Field core Sol 96, Mind core Sol 88, Mind versionZero Astra 67, Psyche criomos Opus 66, Mind flowNexus Astra 49, Mind core Astra 48, Mind curriculum Sol 40, Field semaV0 Opus 39.

### 1. Reply in a stated small size (one line, a few lines, one sentence, a bounded number of lines)

- Messages carrying it: 123 of 1013
- Recipients: Field core Sol 27, Psyche book Haiku 15, Psyche criomos Opus 14, Mind flowNexus Opus 12, Mind flowNexus Astra 12, Mind core Sol 11, Mind curriculum Sol 8, Field protos Opus 6 ...
- Earliest: 2026-11-08T03:02Z   Latest: 2026-11-14T15:08Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «Say in one line why they are needed:»
  - 2026-11-08 | Field semaV0 Opus | Order | id none recorded | «Re-read three Sema v0 rulings against comrak, the reader Sema now stands on, and answer each in one line:»
  - 2026-11-08 | Psyche criomos Opus | Order | id none recorded | «Build, deploy it through Lojix to his home, check cf --version and cf dns records list -z mother-spirit.com run from his shell, and send me the Result in a few lines.»
  - 2026-11-09 | Field protos Opus | Order | id none recorded | «anything not in your releases, report to me in a line;»
  - 2026-11-09 | Mind flowNexus Opus | Order | id none recorded | «Answer in a line when the running build is stopped.»
  - 2026-11-09 | Field protosConsumers Sonnet | Task | id none recorded | «Answer with Done, one line per repository plus the two path-info lines.»

### 2. Mark the message as relayed from Fable or the living at its start (From Fable, From the living, Fable ruled, Rule from Fable)

- Messages carrying it: 105 of 1013
- Recipients: Mind flowNexus Opus 24, Field core Sol 12, Field semaV0 Opus 11, Psyche criomos Opus 8, Mind flowNexus Astra 7, Field protos Opus 7, Mind core Sol 6, Mind core Astra 5 ...
- Earliest: 2026-11-07T16:36Z   Latest: 2026-11-14T15:05Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Mind versionZero Astra | Notice | id none recorded | «Correction to my last message:»
  - 2026-11-08 | Mind core Astra | Notice | id none recorded | «Psyche core Fable ruled on the two Sema schema refusals.»
  - 2026-11-08 | Field semaV0 Opus | Notice | id none recorded | «Hold those two spellings until Fable rules;»
  - 2026-11-08 | Field protos Opus | Notice | id none recorded | «Fable ruled on the 42 renames.»
  - 2026-11-08 | Field protosConsumers Sonnet | Notice | id none recorded | «A hold from Fable, relayed by Psyche core Opus, on your 180-minute task:»
  - 2026-11-09 | Psyche criomos Opus | Notice | id none recorded | «Correction to my last notice:»

### 3. Republish in place, replacing the earlier edition and keeping its link

- Messages carrying it: 77 of 1013
- Recipients: Psyche book Haiku 68, Mind flowNexus Opus 4, Mind core Sol 3, Field core Sol 1, Mind survey Sol 1
- Earliest: 2026-11-07T15:47Z   Latest: 2026-11-14T04:22Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Republish /home/li/primary/flows/9b07ff/proposals/scalar-newtype.md, A scalar newtype carries its scalar's capabilities, in place of https://claude.ai/artifact/SaxcwZwDJikugzi9gyW2Xe;»
  - 2026-11-10 | Psyche book Haiku | Order | id 0cs9 | «republish it yourself as a new version from its source (ask Psyche core Fable for the path if you lack it), so your own publish arms auto-replies on it.»
  - 2026-11-10 | Mind flowNexus Opus | Notice | id none recorded | «a capsule uses the machine login in place, one file, so a renewal inside a capsule and one outside write the same file;»
  - 2026-11-12 | Mind core Sol | Notice | id none recorded | «Proposal presentation shape is done (in place, in the builder);»
  - 2026-11-12 | Field core Sol | Result | id none recorded | «if it is in hostapd line form, it is migrated once in place, decrypt piped into the formatter and back into sops encrypt from stdin.»
  - 2026-11-12 | Mind survey Sol | Result | id none recorded | «Redo it at the deployed Flow 0.54 source, as order fxta asked, taking the source from the installed package's derivation as Mind research Sol did for the Energy Nexus.»

### 4. Publish a page (proposal, book, edition) and send its title and link back

- Messages carrying it: 67 of 1013
- Recipients: Psyche book Haiku 66, Psyche comments Haiku 1
- Earliest: 2026-11-07T15:47Z   Latest: 2026-11-14T15:11Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Psyche book Haiku | Order | id none recorded | «Send the title and link to Psyche core Fable with the flow CLI, as a Send, not in your chat:»
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Send me back the title and the link.»
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Publish /home/li/primary/flows/ee4024/proposals/sema-v0-rulings.md as edition 9 of its book, from the source as it stands now, and send me back the title and the link.»
  - 2026-11-09 | Psyche book Haiku | Order | id none recorded | «Publish the presentation at /home/li/primary/flows/f22e1a/proposals/nix-builds.md and return its title and link to me.»
  - 2026-11-11 | Psyche book Haiku | Order | id u298 | «Send me the link when it is up.»
  - 2026-11-12 | Psyche book Haiku | Order | id f2lb | «Answer with the link under 85wm.»

### 5. Name the reply type to answer with (Result, Done, Notice) and what it carries

- Messages carrying it: 66 of 1013
- Recipients: Psyche criomos Opus 13, Field semaV0 Opus 13, Mind flowNexus Opus 12, Psyche book Haiku 11, Field protos Opus 5, Field protosConsumers Sonnet 4, Field protos Sonnet 3, Psyche core Sonnet 2 ...
- Earliest: 2026-11-08T19:27Z   Latest: 2026-11-13T14:58Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Field protos Sonnet | Order | id none recorded | «Reply with a Result naming, for what you wrote:»
  - 2026-11-08 | Field protosConsumers Sonnet | Order | id none recorded | «Reply with a Result naming, for each piece of work:»
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Reply with a Result naming the publication pending now:»
  - 2026-11-08 | Mind flowNexus Opus | Notice | id none recorded | «Send me a Notice when the canary runs.»
  - 2026-11-08 | Field semaV0 Opus | Order | id none recorded | «Send me a Result with three lines, one per ruling, and a file path if you have evidence.»
  - 2026-11-08 | Field protos Opus | Order | id none recorded | «Add the refusal with a test, version and UPGRADES as your lane does, and send me a Result with the version and commit.»

### 6. Name the commit or revision in the answer

- Messages carrying it: 52 of 1013
- Recipients: Field semaV0 Opus 17, Mind flowNexus Opus 12, Psyche criomos Opus 7, Field protos Opus 5, Mind curriculum Opus 4, Mind core Sol 1, Mind flowNexus Astra 1, Field protos Sonnet 1 ...
- Earliest: 2026-11-08T19:07Z   Latest: 2026-11-14T03:48Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind core Astra | Notice | id none recorded | «I will send it whole, with the sema revision both lanes pin.»
  - 2026-11-08 | Field semaV0 Opus | Order | id none recorded | «Then send the commit to me and to Mind core Astra, so both Sema lanes pin it.»
  - 2026-11-08 | Field protos Opus | Order | id none recorded | «Add the refusal with a test, version and UPGRADES as your lane does, and send me a Result with the version and commit.»
  - 2026-11-09 | Mind flowNexus Opus | Order | id none recorded | «Answer with the commit and the check result.»
  - 2026-11-09 | Field protos Sonnet | Notice | id none recorded | «Your Done carries the main revisions.»
  - 2026-11-09 | Psyche criomos Opus | Task | id none recorded | «Done with the criomos revision and the proof line.»

### 7. Hold building or landing until the living rules; names and shapes are tentative until then

- Messages carrying it: 38 of 1013
- Recipients: Mind flowNexus Opus 12, Field core Sol 5, Field protos Opus 5, Mind core Sol 3, Mind core Astra 3, Psyche criomos Opus 2, Mind curriculum Astra 2, Psyche book Haiku 1 ...
- Earliest: 2026-11-08T19:06Z   Latest: 2026-11-14T15:05Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind core Astra | Notice | id none recorded | «it lands when he rules, and ethos-zero follows it after.»
  - 2026-11-08 | Field semaV0 Opus | Notice | id none recorded | «Hold those two spellings until Fable rules;»
  - 2026-11-08 | Field protos Opus | Notice | id none recorded | «Hold every API change, the 42 renames and signal-orchestrate Acquire.LockRequest included, until the living has seen the Acquire line in the proposal on his page.»
  - 2026-11-09 | Mind flowNexus Opus | Result | id none recorded | «I am asking him now, and the canary waits for his word.»
  - 2026-11-09 | Psyche criomos Opus | Notice | id none recorded | «the two-host test runs with mirror-alpha on prometheus standing for the cloud node, prometheus down simulated by stopping its Git service, until the living rules on provisioning doris;»
  - 2026-11-09 | Field protosConsumers Sonnet | Task | id none recorded | «signal-belief-nexus and meta-signal-belief-nexus wait on a vision ruling;»

### 8. Work read-only; change, dismiss or restart nothing

- Messages carrying it: 33 of 1013
- Recipients: Field core Sol 9, Mind versionZero Astra 8, Mind core Sol 5, Psyche criomos Opus 3, Mind flowNexus Astra 3, Mind beliefNexus Astra 1, Mind core Astra 1, Mind flowNexus Sol 1 ...
- Earliest: 2026-11-08T00:23Z   Latest: 2026-11-13T22:30Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «Have Field, or a flow you choose, diagnose it read-only from the preserved logs and the frozen command.»
  - 2026-11-10 | Psyche criomos Opus | Order | id p3bz | «From Fable (p5lg), read-only:»
  - 2026-11-12 | Mind core Sol | Result | id none recorded | «non-disruptive diagnosis now, read-only on the live laptop, of the GPE 6D cause, what keeps s2idle out of its deepest state, and the spd5118 resume error.»
  - 2026-11-12 | Field core Sol | Order | id none recorded | «read whether that boot ended cleanly or abruptly, read-only, and add it to Mind core Sol file flows/121cc5/prometheus-abrupt-endings.md.»
  - 2026-11-12 | Mind beliefNexus Astra | Order | id none recorded | «read-only, change nothing.»
  - 2026-11-12 | Mind flowNexus Astra | Order | id n0xz | «read-only, change nothing, and kept apart from Sol's 0.54.7 deploy.»

### 9. Open an order to the bookmaker with a NEW ORDER header naming the sending flow and its flow id

- Messages carrying it: 28 of 1013
- Recipients: Psyche book Haiku 28
- Earliest: 2026-11-13T14:30Z   Latest: 2026-11-13T23:07Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-13 | Psyche book Haiku | Order | id none recorded | «New order, not an old one:»
  - 2026-11-13 | Psyche book Haiku | Order | id none recorded | «New order, after model-modules:»
  - 2026-11-13 | Psyche book Haiku | Order | id 4ly4 | «NEW ORDER, 13 November, from Psyche core Opus 730b25;»
  - 2026-11-13 | Psyche book Haiku | Order | id none recorded | «NEW ORDER from Psyche core Opus 730b25.»
  - 2026-11-13 | Psyche book Haiku | Order | id none recorded | «NEW ORDER from Psyche core Opus 730b25, after the versions page.»
  - 2026-11-13 | Psyche book Haiku | Order | id trg1 | «NEW ORDER from Psyche core Opus 730b25;»

### 10. Give or ask for the living's words whole / verbatim, or mark a message as on his words just sent

- Messages carrying it: 26 of 1013
- Recipients: Field core Sol 7, Mind flowNexus Opus 5, Psyche criomos Opus 4, Mind core Sol 4, Mind flowNexus Astra 2, Psyche book Haiku 1, Mind curriculum Sol 1, Field semaV0 Opus 1 ...
- Earliest: 2026-11-08T19:55Z   Latest: 2026-11-14T15:05Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Field semaV0 Opus | Task | id none recorded | «The living’s direction on Sema’s edge, his words:»
  - 2026-11-09 | Mind flowNexus Opus | Order | id none recorded | «The living, in his words:»
  - 2026-11-10 | Psyche criomos Opus | Task | id none recorded | «The living, his words:»
  - 2026-11-11 | Psyche book Haiku | Order | id 3dsd | «Send each comment of his you find to { Psyche core Fable } as one Soft.Psyche message, the book title and the place on the page as its context and his words whole.»
  - 2026-11-12 | Field core Sol | Order | id none recorded | «Following his words just sent:»
  - 2026-11-12 | Mind flowNexus Astra | Order | id none recorded | «His words just sent widen bead primary-woc0.21, and your lean capsule proof plan in 9z0o is accepted.»

### 11. Tell the sender when it has landed or is done

- Messages carrying it: 25 of 1013
- Recipients: Mind flowNexus Opus 9, Psyche book Haiku 5, Psyche criomos Opus 2, Field semaV0 Opus 2, Field protos Opus 2, Field core Sol 2, Psyche core Sonnet 1, Mind flowNexus Astra 1 ...
- Earliest: 2026-11-08T19:15Z   Latest: 2026-11-14T05:34Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Field semaV0 Opus | Order | id none recorded | «Send me the commit when done.»
  - 2026-11-08 | Mind flowNexus Opus | Notice | id none recorded | «Send me a Notice when the canary runs.»
  - 2026-11-08 | Field protos Opus | Order | id none recorded | «Tell Field semaV0 Opus when it lands, so it writes Block bare, and include it in the Result you send me.»
  - 2026-11-10 | Psyche criomos Opus | Notice | id none recorded | «tell me when Claude Code knows claude-fable-5-2.»
  - 2026-11-11 | Psyche book Haiku | Order | id 8g44 | «Add both to the open-books record if they are missing, and send me each title and link when it is up.»
  - 2026-11-11 | Psyche core Sonnet | Notice | id none recorded | «bd update primary-als2 --notes for progress, and bd close when done.»

### 12. Reports go to reports/ and scratch to the scratch directory; evidence is moved out of /tmp or the repository

- Messages carrying it: 22 of 1013
- Recipients: Mind flowNexus Astra 4, Mind curriculum Opus 4, Mind flowNexus Opus 3, Mind core Astra 2, Field heartbeat Sol 2, Psyche criomos Opus 1, Mind core Sol 1, Mind research Sol 1 ...
- Earliest: 2026-11-10T13:00Z   Latest: 2026-11-14T15:10Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-10 | Psyche criomos Opus | Order | id none recorded | «record the firmware settings we depend on and the present versions (BIOS, EC, ME) to a file in your flow directory.»
  - 2026-11-12 | Mind core Sol | Result | id ffex | «Lojix owns no temporary directory.»
  - 2026-11-12 | Mind flowNexus Astra | Result | id ggcg | «Copy the plan out of /tmp into your flow directory, since /tmp is being cleared, and point the bead at the new path.»
  - 2026-11-12 | Mind core Astra | Result | id none recorded | «knowledge:psyche, intent:anatomy, intent:scratch, intent:testing, vision:testing, knowledge:nix-rust-builds.»
  - 2026-11-12 | Mind research Sol | Result | id none recorded | «Move the probe results from /tmp into your flow directory.»
  - 2026-11-12 | Mind herdrNexus Sol | Notice | id none recorded | «$P the herdr event work at a clean stopping point, and record where you stand in your flow directory.»

### 13. Keep observation apart from guess; cause only if observed; leave unknown unknown

- Messages carrying it: 20 of 1013
- Recipients: Field core Sol 5, Mind flowNexus Astra 5, Psyche criomos Opus 4, Mind versionZero Astra 2, Mind beliefNexus Astra 1, Field heartbeat Sol 1, Mind flowNexus Sol 1, Mind survey Sol 1
- Earliest: 2026-11-08T00:23Z   Latest: 2026-11-12T21:36Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «Report to me the observed cause, kept apart from any hypothesis, and the smallest correction.»
  - 2026-11-10 | Psyche criomos Opus | Task | id eyvg | «Write everything to /home/li/primary/flows/228e2b/suspend/evidence.md (create the folder), observations only, and Notice me the path.»
  - 2026-11-12 | Field core Sol | Order | id fzot | «Return the timeline and what it shows, the cause only if observed, in a file and one line.»
  - 2026-11-12 | Mind flowNexus Astra | Order | id none recorded | «the observed cause only, nothing inferred.»
  - 2026-11-12 | Mind beliefNexus Astra | Order | id none recorded | «Keep observations and unknowns apart.»
  - 2026-11-12 | Field heartbeat Sol | Question | id rjlb | «Observed facts only, from the Flow Nexus journal and configuration, and say plainly what was not checked.»

### 14. Build on a branch or in the testing capsule; push the branch, switch nothing live

- Messages carrying it: 20 of 1013
- Recipients: Mind curriculum Opus 7, Mind flowNexus Opus 6, Mind flowNexus Sol 2, Mind core Sol 1, Mind versionZero Astra 1, Mind curriculum Sol 1, Mind sourceNexus Opus 1, Mind flowNexus Astra 1
- Earliest: 2026-11-08T00:44Z   Latest: 2026-11-14T07:21Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «The release record states that MCP compatibility through Message is unestablished and that Message is not deployed.»
  - 2026-11-12 | Mind core Sol | Order | id none recorded | «nothing deployed until I rule.»
  - 2026-11-12 | Mind flowNexus Astra | Order | id c5vi | «You design and Mind flowNexus Sol implements, tested in its capsule.»
  - 2026-11-13 | Mind flowNexus Sol | Task | id none recorded | «In the testing capsule, on a fresh testing store, never the live Nexus:»
  - 2026-11-13 | Mind curriculum Sol | Order | id none recorded | «The modules.datom section (notion/curriculum-1.md, mind-belief 09f129e) is the next revision of Curriculum after that release, on a branch named notion-declarations;»
  - 2026-11-14 | Mind flowNexus Opus | Notice | id n6hd | «a branch, the testing capsule, nothing live.»

### 15. Build from the source file as it stands now

- Messages carrying it: 16 of 1013
- Recipients: Psyche book Haiku 15, Mind flowNexus Opus 1
- Earliest: 2026-11-08T21:19Z   Latest: 2026-11-13T15:58Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Publish /home/li/primary/flows/ee4024/proposals/ethos-holds.md again, as a new edition from the source as it stands now (Proposal 1 now has four checks), and send me back the title and the link.»
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Publish /home/li/primary/flows/ee4024/proposals/ethos-holds.md again, as a new edition from the source as it stands now (the generator pinned as a flake input, generation a derivation), and send me back the title and the link.»
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Publish /home/li/primary/flows/ee4024/proposals/sema-v0-rulings.md as edition 10 of its book, from the source as it stands now, and send me back the title and the link.»
  - 2026-11-10 | Mind flowNexus Opus | Order | id fmeh | «audit the Flow Nexus implementation against its vision as it stands now, starting open, no fixing.»
  - 2026-11-12 | Psyche book Haiku | Order | id 64n4 | «Republish the review Variations of a call stand at the root, https://claude.ai/artifact/JKVejG4UjrroF341ifvYLN , as its next version, from /home/li/primary/flows/350f85/reviews/variations.design.md as it stands now.»
  - 2026-11-13 | Psyche book Haiku | Notice | id amzx | «Read it fresh and build from the file as it stands now;»

### 16. No polling: an action answers an event; a need whose event is unknown comes as a question

- Messages carrying it: 15 of 1013
- Recipients: Mind core Astra 6, Psyche criomos Opus 3, Mind versionZero Astra 2, Field protos Opus 1, Field core Sol 1, Mind flowNexus Astra 1, Mind sourceNexus Opus 1
- Earliest: 2026-11-08T06:36Z   Latest: 2026-11-14T03:13Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «every action answers an event.»
  - 2026-11-09 | Psyche criomos Opus | Notice | id none recorded | «events only, no polling:»
  - 2026-11-10 | Field protos Opus | Result | id dbhg | «(2) intent:design puts polling out of every design:»
  - 2026-11-12 | Mind flowNexus Astra | Result | id none recorded | «every action answers an event and a correct system goes quiet when nothing changes (intent:design, vision:nexus).»
  - 2026-11-12 | Mind core Astra | Order | id ym9k | «Polling is out of every design, so name the event each poll stands in for and where herdr announces it.»
  - 2026-11-13 | Field core Sol | Question | id none recorded | «Answer on that event, not by retrying in a loop.»

### 17. Run the gate or heavy build on Prometheus (the remote builder)

- Messages carrying it: 13 of 1013
- Recipients: Mind flowNexus Opus 6, Field protos Opus 2, Mind versionZero Astra 2, Field protos Sonnet 1, Field semaV0 Opus 1, Mind curriculum Sol 1
- Earliest: 2026-11-08T06:53Z   Latest: 2026-11-13T15:33Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «Only a path that cannot be fetched is rebuilt, on the remote builder, from the frozen derivation.»
  - 2026-11-08 | Mind versionZero Astra | Notice | id none recorded | «the import-from-derivation builds were small support builds on the remote builder, inside the restore I authorized, and the account of them is enough.»
  - 2026-11-09 | Mind flowNexus Opus | Order | id none recorded | «From now on, run evaluation and builds on prometheus itself, over ssh, and copy back only what ouranos must hold.»
  - 2026-11-09 | Field protos Opus | Order | id none recorded | «nix-fast-build --remote becomes the way a flow runs a gate.»
  - 2026-11-09 | Field protos Sonnet | Task | id none recorded | «Gate on prometheus against the main revision, push main, tell Field protos Opus so it regenerates the sets.»
  - 2026-11-13 | Mind curriculum Sol | Result | id none recorded | «Cargo tests and build on the remote builder in one shared target directory, nothing compiled on the laptop, plus the existing Flow Nix gate for its consumer.»

### 18. Commit and push what is landed

- Messages carrying it: 12 of 1013
- Recipients: Mind flowNexus Opus 2, Mind core Sol 2, Field protos Sonnet 2, Field protos Opus 2, Field semaV0 Opus 1, Field core Sol 1, Psyche book Haiku 1, Mind curriculum Opus 1
- Earliest: 2026-11-08T19:35Z   Latest: 2026-11-14T01:48Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Psyche book Haiku | Order | id none recorded | «Move pinned-ethos-zero in makeshift-tools book-build.clj from 07714b to that commit, the same in book-check, commit and push it.»
  - 2026-11-08 | Field semaV0 Opus | Order | id none recorded | «Reverse anything of it you have already done, and push nothing of it.»
  - 2026-11-09 | Mind flowNexus Opus | Notice | id none recorded | «Leave mind-belief beb68304 local and push it when IPv4 returns.»
  - 2026-11-09 | Field protos Sonnet | Notice | id none recorded | «rebase onto main, gate checks.default again against the main revision, push main.»
  - 2026-11-09 | Field protos Opus | Notice | id none recorded | «manifest, lock, Cargo.nix), worktree /git/worktrees/herdr-nexus-buildbase-963c53 at 80458cd, then gate and push main.»
  - 2026-11-12 | Mind core Sol | Result | id none recorded | «Check out ca0b666 detached there, merge origin/main 0f412f0 into it (a merge, so the seven local commits keep their ids and the shared checkout stays an ancestor), and push the merge to origin main as a fast-forward.»

### 19. A design question goes up as a Question, in one message

- Messages carrying it: 12 of 1013
- Recipients: Mind flowNexus Opus 4, Mind versionZero Astra 2, Mind curriculum Astra 2, Field core Astra 1, Field protos Opus 1, Mind core Astra 1, Psyche criomos Opus 1
- Earliest: 2026-11-07T16:34Z   Latest: 2026-11-14T12:03Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-07 | Mind versionZero Astra | Task | id none recorded | «A design question goes to me;»
  - 2026-11-08 | Mind flowNexus Opus | Notice | id none recorded | «If a wait has no event that announces it, send it to me as a question, naming the wait, and keep working on the rest.»
  - 2026-11-10 | Psyche criomos Opus | Order | id pgyn | «Tell me at once, as a Question, if the lojix client cannot hold a subscription open and stream its events (one datom in, one reply out), with what it does instead;»
  - 2026-11-10 | Field core Astra | Result | id none recorded | «Anything that would fix the Document shape or a schema choice comes to me as a question and I take it to Fable.»
  - 2026-11-10 | Field protos Opus | Result | id dbhg | «what the Belief Nexus reacts to instead is the event that a repository changed, and finding where that event is announced is brought to Psyche as a question when the change is made.»
  - 2026-11-12 | Mind core Astra | Order | id ym9k | «A need whose event herdr does not announce comes to me as a question.»

### 20. Change only what is named: nothing else changes

- Messages carrying it: 9 of 1013
- Recipients: Mind flowNexus Astra 6, Field core Sol 2, Psyche criomos Opus 1
- Earliest: 2026-11-09T22:55Z   Latest: 2026-11-13T23:12Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-09 | Psyche criomos Opus | Notice | id plqh | «Nothing else to do on it.»
  - 2026-11-12 | Mind flowNexus Astra | Order | id none recorded | «Change nothing else in the declaration.»
  - 2026-11-12 | Mind flowNexus Astra | Result | id ojyc | «Yes, add both to its first-prompt modules the same way, changing nothing else.»
  - 2026-11-12 | Mind flowNexus Astra | Result | id none recorded | «nothing else changes until it is ruled.»
  - 2026-11-12 | Mind flowNexus Astra | Notice | id none recorded | «Read knowledge:psyche from its authored source, /git/github.com/LiGoldragon/mind-belief/knowledge/psyche.md, and add it to your own committed declaration's first-prompt modules the way you added Sol's, in the Home source as well, changing nothing else.»
  - 2026-11-12 | Field core Sol | Order | id none recorded | «Nothing else goes with it.»

### 21. Write the handover and refresh when finished

- Messages carrying it: 8 of 1013
- Recipients: Mind flowNexus Opus 4, Mind flowNexus Astra 2, Psyche criomos Opus 1, Psyche book Haiku 1
- Earliest: 2026-11-09T22:07Z   Latest: 2026-11-12T23:42Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-09 | Mind flowNexus Opus | Result | id none recorded | «Refresh it when ready.»
  - 2026-11-09 | Mind flowNexus Opus | Task | id none recorded | «Fable also ruled on refresh, a watcher left running is not work and the Flow Nexus may end such a flow and refresh it, a flow awaiting a real background job is not refreshed until it reports;»
  - 2026-11-09 | Mind flowNexus Opus | Order | id inmy | «{ Psyche core Fable } moves to model claude-fable-5-2 in goldragon metaflows-0533.datom, relock and deploy, then refresh Psyche core Fable;»
  - 2026-11-10 | Psyche criomos Opus | Order | id none recorded | «Then write your handover and end your background jobs.»
  - 2026-11-12 | Mind flowNexus Astra | Order | id none recorded | «write your handover now, at 25 percent remaining for Codex models and 20 for Claude, measured against the size at which that harness really compacts, which is found first from its own records.»
  - 2026-11-12 | Psyche book Haiku | Task | id c6qk | «If anything is unpublished or open, write it in handover.md in your flow directory with its id;»

### 22. No reply wanted

- Messages carrying it: 4 of 1013
- Recipients: Psyche core Sonnet 1, Field protos Opus 1, Mind curriculum Opus 1, Field core Astra 1
- Earliest: 2026-11-08T19:18Z   Latest: 2026-11-14T04:27Z
- Excerpts (the matching clause, verbatim; id is the RequestId where the Send reply carried one):
  - 2026-11-08 | Field core Astra | Notice | id none recorded | «No answer needed beyond your final handoff to me.»
  - 2026-11-09 | Field protos Opus | Order | id none recorded | «Reply with a Done line only if something blocks.»


## Module text already saying the same

Searched `/git/github.com/LiGoldragon/{psyche-belief,mind-belief,field-belief}` (`*.md`) by the key words of each family. Paths are under `/git/github.com/LiGoldragon/`. "Same" means the module states the instruction itself; "near" means it states a neighbouring thing.

| Family | Module text | Path:line | Reading |
|---|---|---|---|
| Publish and send title and link; a redo replaces the same edition | "…publishes it, and Sends its title and link through flow to the flow that ordered the book… A redo replaces the same edition and resolves the comment threads the source answers." | `mind-belief/knowledge/book/0.md:8` | same |
| Publish and send title and link | "Publish the builder's resulting page once with Artifact and Send its title and link through flow to the flow that ordered the book." | `field-belief/role/book-publishing-procedure.md:17` | same (the bookmaker's own procedure) |
| Link in the chat | "A proposal goes to a presentation, and the chat carries its link and title." | `psyche-belief/intent/living-interaction/0.md:20` | near (to the living) |
| Reply in a stated small size | "A text longer than a dozen lines… stays with its writer in a file, and the message carries the path and one line saying what the file is." | `psyche-belief/intent/energy/0.md:15` | near (a size rule for long text, not a per-brief reply size) |
| Reply in a stated small size | "A text for the living is as small as its point… the chat gives him one line." | `psyche-belief/intent/energy/0.md:25` | near (to the living) |
| Reply in a stated small size | "…answered by one line: that it is not Fable's and goes to Opus" | `psyche-belief/intent/fable/0.md:12` | near (Fable's reply to a message not its) |
| Reply in a stated small size | "With nothing answered, say so in one line." | `field-belief/role/book-page-procedure.md:160` | near |
| Give the living's words whole | "What the living says is relayed in his words." | `psyche-belief/intent/living-interaction/0.md:8` | same |
| Give the living's words whole | "His words and his comments go whole, in his words; a flow's own text goes as a path." | `psyche-belief/vision/collaboration/0.md:8` | same |
| Give the living's words whole | "His words go whole." (Opus brings up only what needs a decision) | `psyche-belief/intent/opus/0.md:10` | same |
| Give the living's words whole | `Living.{ Context Verbatim }`, `Verbatim.String ; his words whole` | `psyche-belief/knowledge/flow-messaging/0.md:29,35` | same (the message type) |
| Questions go up as one question | "…brings up only what needs a decision, as one question: the decision asked, Opus's reading of what bears on it, and the path of any file it rests on." | `psyche-belief/intent/opus/0.md:10` | same |
| Questions go up as one question | "A flow that brings a question to Fable brings it through Opus, as one message…" | `psyche-belief/vision/collaboration/0.md:8` | same |
| Name the reply type | "A Result answers an Order or a Question and a Done closes a Task, each naming the request by its RequestId." | `psyche-belief/knowledge/flow-messaging/0.md:58` | same as to the types; no module says which type to ask for |
| Name the reply type | "A request is open from its delivery until the Result or Done that answers it" | `psyche-belief/vision/flow-nexus/0.md:277` | near |
| Mind implements as it stands | "A Mind flow writes the code: it implements the design Psyche rules, as it stands, and asks where the design is silent." | `psyche-belief/vision/mind-aspect/0.md:8`; also `psyche-belief/vision/aspects/0.md:25` | near ("as it stands" in the Mind sense, not "build the page from the file as it stands") |
| Build the page from the file as it stands | "Made from the page as it stands and the new part in the named file…" | `field-belief/role/book-page-procedure.md:30` | near (comment-relay/page procedure) |
| Hold until the living rules | "Approval is the living's word on the line itself, after he has read it: land, or amend and land." | `psyche-belief/intent/psyche/0.md:14` | near |
| Hold until the living rules | "…a notion, not reviewed by him. The Ethos here is the design and is tentative in its names" | `mind-belief/notion/curriculum/1.md:8`, `mind-belief/notion/source-nexus/0.md:8`, `mind-belief/notion/permaflows/0.md:6` | same, written into the notion itself |
| Observation apart from guess | "Keep observations, hypotheses, and unknowns separate. Keep unknown causes unknown." | `psyche-belief/spirit/core/0.md:45` | same (spirit:core:0) |
| Handover and refresh | "A flow is refreshed after its landings: what he approved is landed and live before the handover is written…" | `psyche-belief/vision/remembering/0.md:26` | same |
| Handover and refresh | "A permanent flow continues through runs under its address and is kept hot… It is warned when its context reaches t…" | `psyche-belief/vision/flow-nexus/1.md:157` | near |
| Scratch to a temporary directory | "Build output, a log, a diff, a probe, every file a flow makes for its own work, goes to a temporary directory…" | `psyche-belief/intent/scratch/0.md:6,8` | same (intent:scratch:0) |
| Reports named by the briefer | "A flow writes a proposal for the living and the report its briefer asked for by name." | `psyche-belief/intent/energy/0.md:27` | near |
| No polling | "Polling, in any form and for any reason, is out of every design. Every action has a cause, and the cause is an event… A need whose event is not yet found is brought to Psyche" | `psyche-belief/intent/design/0.md:32,34` | same (intent:design:0) |
| No polling | "CriomOS has no polling of any kind" | `psyche-belief/vision/criomos/0.md:84,86` | same, for CriomOS |
| Gate on the remote builder | "A gate is evaluated and built on the remote builder itself: nix-fast-build `--remote`…" | `mind-belief/knowledge/nix-rust-builds/0.md:98` | same |
| Gate on the remote builder | "Nix builds live in the remote builder's store." | `psyche-belief/vision/nix-builds/0.md:23` | near |
| Commit and push; main | "A flow commits the files it edited." and "A version that runs is built from main. A branch, a worktree or a dirty tree of ours carries a line naming what it holds and which flow owns it, and is folded into main or removed when that is done." | `psyche-belief/vision/committing/0.md:6,10` | near (no module says push) |
| Commit and push | "A production deployment is `RequireImmutable`, at a pushed CriomOS revision; producers are pushed before the consumer that pins them." | `mind-belief/knowledge/lojix/0.md:64` | near (deployments only) |
| Branch / capsule, nothing live | "A build of the Flow Nexus is tested in a testing capsule of its own…" | `psyche-belief/vision/flow-nexus/0.md:306` | same, for the Flow Nexus only |
| Read-only | "Read-only exploration subflow" | `mind-belief/role/explorer-description/0.md:7` | near (a subflow role, not a brief rule) |
| A main flow briefs the form of the answer | "…the form of what comes back to it and to whom, all briefed before it says nothing blocks on it." | `psyche-belief/intent/main-flow/0.md:10` | same, for a Primary driving a fix |

No module text found for: republish in place with the earlier link (beyond `mind-belief/knowledge/book/0.md:8`), the NEW ORDER header, marking a message as relayed from Fable or the living (the delivered message carries `Sender` already, `psyche-belief/knowledge/flow-messaging/0.md`), tell the sender when landed or done, nothing else changes, no reply wanted, and the model modules (`mind-belief/knowledge/{fable,opus,haiku,sonnet,sol,astra,luna}/0.md`) hold no reply-form or briefing-form rule beyond model descriptions.

Note on what a recipient carries: the module list a flow is started with is its permaflow's `modules.datom` entry; whether a given recipient already loaded one of the modules above was not checked. One Fable message of 14 November says of `psyche-belief/intent/scratch/0.md`: "the rule he asks for is already written, intent:scratch:0, … and it is loaded by nobody"; an Opus message the same day reports it live in 29 permaflows and 31 role packets.
