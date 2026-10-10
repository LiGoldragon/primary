# Recovered design state: Primitive Message, the design books, b7ba00's findings

Carried for Psyche Opus dc53b4 by one review subflow, 2026-09-26 (host time CST, UTC−6; transcript times in Z). This account makes no rulings on design questions. Marks: **O** observation (read or run by this subflow), **C** claim (a record or flow says so; not independently witnessed here), **I** inference (this subflow's reading).

Where things were read: flow records from `origin/main` (records workspace `opus-records-dc53b4`, fetched; 93ba9f and b7ba00 records there are byte-identical to `/home/li/wt/primary/93ba9f` and `/home/li/wt/primary/b7ba00`, O). Recovery-flow records from linked worktrees, because they are not on origin/main: 56ae53 and 9ac67c logs from `/home/li/wt/primary/field-packet-56ae53/`, 8904b1 log from `/home/li/wt/primary/56ae53/flows/8904b1/log.md`. c56100 has no flow directory with files anywhere found (O). Artifact comment threads were read with the Artifact comment reader. The living's words after 21:36Z were searched directly in Claude and Codex transcripts: the `transcript` tool is not installed (O).

## A. Primitive Message: the six pending rulings

93ba9f's last words to the living (T93:1900, 21:36:02Z, per `reports/predecessor-recovery.md`) put six questions. For each question: the living's words, what each prototype proposes, and what only the living can rule.

Sources used for every item:
- Opus = `flows/93ba9f/reports/opus-primitive-message.md` (artifact Qz8dpKBzJfbQgAbdUmfZCe).
- Fable = `flows/b7ba00/reports/message-primitive.md` (artifact Dkzn57DKYhMyYc8GiKjRTP).
- Cmp = `flows/b7ba00/reports/primitive-prototypes-comparison.md`.

None of these three artifacts has a comment thread (O).

### A1. With no seat above, does the letter go to the next seat below?

**The living's words**

> If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules.
>
> Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

-- living, typed comment on "What Waits for the Living", 2026-09-24 14:31Z, question 5, to Psyche Medium d8df70. Two records hold these words:
- `flows/d8df70/vision/messaging.md:64-69`. Its heading says "input mode not established", but its attribution line says it is a comment. The transcription correction "Psyq" → "Psyche" was applied.
- `flows/836818/vision/flowNexus.md`, section "The living's answers to the six questions, 2026-09-24": "psyche, typed as comments".

Older and related:

> So that was another failure. You're supposed to communicate laterally to the same power, which would have meant field low, but obviously, if there isn't one and our system is very flawed, then you would need to contact one power higher.

-- psyche, STT; session 0625c31b line 1908, 2026-09-20T20:14:01Z; `flows/0625c3/vision/lateralThenUpRouting.md`.

The primitive-Message request itself, which sets the scope:

> Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages … If you say "send up" it means message higher layer … The message logic has to figure out where that's supposed to go so it can ask the flow, "Where does Luna field Luna send the message when it sends up?" or maybe the flow figures it out.

-- psyche, STT, 2026-09-26, to 93ba9f; `flows/93ba9f/vision/messagingInterface.md`.

**What each proposes**
- Opus §5: `Up` from Field.Tertiary goes to Field.Secondary; if that seat is empty, the next above; if none is above, the next below (citing 24 September). A crucial empty seat (every medium and high one) is started, not skipped. Refusals include `NoSeatAbove` and `NoSeatBelow`.
- Fable §4: an empty target is held and the sender told `NoSeat.Seat`. "The living's earlier word on undeliverable letters (try higher, then lower) is the next version's rule, not this one's." §8 lists escalation as deliberately absent.
- Cmp §4 and Conflict 1: whether the primitive already implements climb-and-start, or defers it.
- 8904b1's triage (its log, line 148) C: the 09-24 word already speaks to this.

**I.** The 09-24 words are in the old vocabulary (Psyche Medium/High, "power"). The seats have since been renamed Primary…Quaternary. The words also describe an undeliverable message (delivery failure), and Opus reads them as also covering "no seat exists above" (address resolution). Whether those are the same case is not stated in the words.

**Remainder for the living:** does the 24 September rule (try higher, then lower, start a crucial missing flow) already apply in the primitive Message, or is it for a later version?

### A2. Should the primitive interrupt nothing?

**The living's words.** From the comment on Two Books Compared (5vspDLuChyZbZ1MmPfw1u4), thread bf161595, anchored at "Priority is a head on the datom":

> Arguably the audit report is all going to be the same: the soft or the hard. Do we really even need to tell it if it's soft or hard? Do we even need to tell the model if it's a soft or hard message? I don't know. I don't think so. The database can know it, so if he wants to know he can find out but I don't think it's going to matter. We'll make the judgment of what kind of messages we want to break harder than others so it's just what kind of message it is, really.
>
> We don't even do the soft or hard, actually. That was the wrong approach. For the normal format that gets communicated, the non-debugging format, basically the production requests and responses (are those what we call them? Queries and responses)

-- living, typed artifact comment, 2026-09-26T21:04. Re-read here from the live thread (O): it still ends mid-sentence with no closing text, and there is no later reply in the thread. Logged in `flows/93ba9f/vision/messagingInterface.md` and `flows/b7ba00/vision/messaging.md:77-95`.

Earlier in the same comment:
- "a hard psyche update, which interrupts / a soft psyche update / a psyche update, where maybe there's a middle ground of interrupt"

Distilled `Vision/messaging.md:8-10` still holds "Priority is a head on the datom", `Priority.[HardAbrupt MiddleAbrupt Soft]` (O).

**What each proposes**
- Opus §5: a per-kind table in Message's database: `{ PsycheUpdate MiddleAbrupt } { Order MiddleAbrupt } { Question Soft } { Report Soft } { Answer Soft }`.
- Fable §5: "Whether a kind interrupts the recipient is the database's judgment per kind, as the living ruled; the primitive version interrupts nothing and lets every letter wait for the recipient's turn."
- Cmp §8 frames it as whether a hidden table using the Soft/MiddleAbrupt words the living called wrong may exist, or none at all. Cmp paraphrases the living as "Priority leaves the letter... soft and hard was the wrong approach". The first phrase is b7ba00's heading, not the living's words (O: the heading at `b7ba00/vision/messaging.md:77`).

**I.** Both prototypes agree that no interruption marking appears in the letter. They differ on whether any kind breaks in during the primitive at all. The living's words hold two things side by side: the database judges how hard each kind breaks in ("break harder than others"), and "We don't even do the soft or hard". The unfinished sentence may have been heading toward a rule for production messages.

**Remainder for the living:** in the primitive, does any kind interrupt (and which, by kind), or does every letter wait? And how did the 21:04 sentence about "production requests and responses" end?

### A3. The address word: `Toward` or `Bearing`?

**The living's words**

> If you say "send up" it means message higher layer, whatever however we say that, let's find a clever way to say that: message to higher-layer type message.

-- psyche, STT, 2026-09-26, to 93ba9f; `flows/93ba9f/vision/messagingInterface.md`.

Nothing since.

**What each proposes**
- Opus: `Toward.[ Up Down Across.Aspect Seat.Seat ]`.
- Fable: `Bearing.[ Up Down Across.Aspect Living To.Seat ]`, with CLI words `send-up`, `send-down`, `send-across psyche`. Fable also has a `Living` address, which Opus lacks (Cmp §4).

**Remainder for the living:** which word (`Toward`, `Bearing`, or another), and is `Living` an address?

### A4. Five generic kinds or nine aspect-named kinds?

**The living's words.** The primitive request (STT, 2026-09-26, above):

> a simple anatomy of a few different types of messages that are simple and easy, like: field report / psyche report / field question / psyche question … We could type the message based on the type, because if you send the message you have the same type.

Earlier the same day (STT, to 93ba9f): "We have certain kinds of messages like: An order / A question / A request for an audit / A request for some information".

At 21:04 (typed comment): "this is where the message type is. We can make any number of kinds … a psyche update … an implementation report … an audit report".

Fable's book, thread 1fa9256a on 4aaZsqHKN19SLUxk1UHwjE, 20:54Z, anchored at "Proposed: add Report and Answer":

> Well maybe it's even more broad than that. Let's go through some anatomies …

This led to the meaning language (Sema).

**What each proposes**
- Opus: five kinds (`Report Question Answer Order PsycheUpdate`). The aspect is read from the sender's seat, which the letter carries.
- Fable: nine kinds (`FieldReport … PsycheQuestion`, plus `Order`, `Answer`, `PsycheUpdate`). Message refuses a kind whose aspect is not the caller's.
- Fable's Sema v1 (`sema-version-one.md` Ruling 5) proposes a third list: Order, Question, AuditRequest, InformationRequest, AuditReport, ImplementationReport, PsycheUpdate, Answer.
- Open gap in both: whether Order and Answer carry an aspect (Fable Fork 2).

**Remainder for the living:** is the aspect part of the kind's name, or read from the sender? And which kinds ship first? There are three candidate lists.

### A5. Replies: `Sent`/`SendRejected` or `Delivered`/`Parked`/`Refused`?

**The living's words**

> Even if the ordinary message API is complex, we create a shorthand version which has a shorthand response type or display type.

-- STT, 2026-09-26.

> You have this human prefix and then you create these human variant responses. You have the not-human but simple. Simple is better

-- STT, 2026-09-26.

Both are in `flows/93ba9f/vision/messagingInterface.md`. Nothing since.

**What each proposes**
- Opus: `Sent.[ Delivered.Seat Parked.Seat Refused.Refusal ]`, with `Refusal.[ NoSeatAbove NoSeatBelow SeatEmpty CallerUnknown ]`.
- Fable: `Sent.{ Origin Seat } | SendRejected.[ CallerUnknown KindNotCallers.Aspect NoSeat.Seat RecipientUnreachable.Seat EmptyBody ]`.
- Cmp §5: Opus separates delivered from parked; Fable lists more rejection causes.

**Remainder for the living:** should the reply say whether the letter was delivered or parked, and under which words?

### A6. Is the database named Mnema?

**The living's words**

> Let's figure out the name for the database part.

-- STT, 2026-09-26, to 93ba9f.

> Originally that was the idea. Sema was supposed to be the language of meaning and so that is actually the right name. It's cool that you brought it up. That means we rename all of the Sema aspect pertaining to the database. It's not that it's not true in the way it's going to store Sema, but not only Sema. We're going to just call it something else, something clever (the database).

-- typed artifact comment on Noema 29ygc6gwx83B81XZLg8Dby, thread 69b8ff09, 2026-09-26T21:13. O: re-read live, no later reply.

**What each proposes**
- Opus: Thesauros, Kosha or Mnema.
- Fable: Mnema (alternatives Thesauros, Archeion). Sema v1 Ruling 1 is the same question.
- Cmp: Mnema is "converging".

**I.** Both books naming Mnema is not independent agreement: Opus lists Mnema as "Fable's proposal".

**Remainder for the living:** the database's new name: Mnema, Thesauros, Kosha, Archeion, or another.

### Gaps both prototypes leave to Astra (Cmp)

- Whether Order and Answer carry an aspect.
- Malformed-send refusals.
- Letters parked for an empty seat that later fills.

C (dc53b4 log): the package went to Mind Astra 31147a, which is now dead. No live Mind Astra has been assigned to carry it forward.

## B. The design books: open forks and rulings

"Since" means after the book was written. The dates of the living's words below are all 2026-09-26: the comments at 20:54, 21:04, 21:11 and 21:13, and the STT on Sema v1 and the primitive Message. Nothing from the living after 21:36Z bears on any item here (see D). Artifact threads read, O:
- P1PUozuFzS5kMNPgYEMA5q: none.
- DQjhVz7j5pNaoXGYv4zmEN: none.
- 29ygc6gwx83B81XZLg8Dby: two threads (21:11, 21:13).
- 5vspDLuChyZbZ1MmPfw1u4: one thread (21:04).
- 4aaZsqHKN19SLUxk1UHwjE: one thread (20:54).

### B1. 93ba9f design book (`reports/opus-design-book.md`, P1PUozuFzS5kMNPgYEMA5q): five questions

1. Is the letter redraw the right shape: priority as the head, seat as sender, four content variants? Since then: the 21:04 comment says the head is the message's kind, not the priority ("That was the wrong approach"). The priority half is answered against the book. The seat and content-variant halves are open.
2. Is `Report` a fifth kind? Since then: 21:04 lists "an implementation report / an audit report" and "any number of kinds". No specific answer.
3. Three reply registers (simple, human, full), simple by default? Nothing since.
4. Merge the built word-name anatomy with a 1,024-word list, and which name? Nothing since.
5. Send the lock, instruction and messaging-tool faults to Field now? Nothing since. Status of those faults: not checked here.

### B2. Fable design book (`flows/b7ba00/reports/design-book-letters-roles-monikers.md`, 4aaZsqHKN19SLUxk1UHwjE): eight forks, five rulings asked

Forks:
- Fork 1: Source carries STT correction marks, or three bare variants? Nothing since.
- Fork 2: four layer words as the type, with ultra-low a roster matter? Nothing since. Records conflict (see B4 item 9).
- Fork 3: add Report and Answer? Since then: the 20:54 comment, anchored on this fork: "maybe it's even more broad than that", which led to the meaning language. Not a yes or no.
- Fork 4: human rendering by default on every pane? Nothing since.
- Fork 5: write Harness now or derive it? Nothing since. The prior word: "I guess you can put it in".
- Fork 6: is Fable a layer above Primary, or Primary's model? Nothing since.
- Fork 7: roster as a datom file the living edits, or Ethos? Nothing since. Records cut against "the living edits": the automation vision says "I'm not going to … type anything anywhere ever".
- Fork 8: PascalCase or camelCase? Nothing since.

Rulings asked (1–5): kinds; human default; layer words; roster as datom; "Moniker", PascalCase, 4096-word list. Nothing since beyond Fork 3.

### B3. Fable Noema book (`anatomy-of-the-meaning-language.md`, 29ygc6gwx83B81XZLg8Dby)

1. Name Noema (Fork 1). Since then: 21:13 comment, "Sema … is actually the right name". **Answered: Sema.**
2. Five top-level utterances (Fork 2). Amended by Fable's own 21:04 addendum. Nothing since from the living.
3. Support on every statement (Fork 3). Nothing since.
4. A parenthesis annotates the unit before it (Fork 4). Nothing since.
5. Rename the built Sanskrit variants now (Fork 5). Nothing since.
6. Addendum fork: is the utterance a field of every kind, or declared once per kind in Ethos? Nothing since.
7. The living's own question at 21:11, "Is this category part of the language equivalent with our ethos?", was answered by 93ba9f in its transcript (T93:1735: not equivalent; a Vaiśeṣika vocabulary written in Ethos) (C, per predecessor-recovery). No reply from the living.

### B4. Fable "Sema, version one" (`sema-version-one.md`, DQjhVz7j5pNaoXGYv4zmEN): five rulings plus two Mind items

1. The database's new name, Mnema proposed. Open; same as A6.
2. `Markdown` as an Ethos alias of String. Since then: the living's STT said "We could even have the inner component be Markdown, I guess". Whether it is an alias is not stated.
3. `Response.Assent` carries nothing. Nothing since.
4. Sender outside the sema, as the letter's first field. Nothing since. Related: 93ba9f's open "sender as first field inside each kind?" (T93:1625/1673, C).
5. First kinds to ship. Open; same as A4.

Mind items, not for the living:
- What refers to Ethos's root named Sema.
- The recall rows of the equivalents table.

### B5. Two Books Compared (`flows/93ba9f/reports/books-compared.md`, 5vspDLuChyZbZ1MmPfw1u4): rulings 1–14

1. Sender: `Living` as a variant, or the living marked only as non-datom? Nothing since.
2. Stamp the sender from the calling pane now, or the caller names it for now? Since then: the primitive request and caller-identity words (STT, 2026-09-26): "It can get its origin without the user having to say, 'Hey I'm Psyche Fable.' It would just know." Both prototypes stamp. I: this points toward stamping, but the "for now" word is not withdrawn.
3. Content forms (Opus names or Fable names). Nothing since.
4. Short psyche: what it carries. Nothing since.
5. Time: date, age or both; timestamps at all? Nothing since.
6. Kinds: do Report and Answer join? Since then: 20:54 and 21:04 ("any number of kinds"). No specific answer.
7. Replies and panes: Simple/Human/Full, and datom on panes? Nothing since. Note: 21:04 is anchored on this section's quote, but its words concern the head, not the registers.
8. **Effort:** one shared scale with Xhigh, or per-model effort types? Is "Luna at high effort / Luna at light" still meant, given Intent's "never raised to buy quality"? Nothing since. Relevant earlier word: "there are different effort levels for different models so it's a property, the data of the model variant" (STT, 2026-09-26, `flowLaunching.md`).
9. **Layers:** Primary…Quaternary, or three power levels plus a temporary ultra-low, and how do they map to distilled Vision's High/Medium/Low/UltraLow? Nothing since from the living. Related: b7ba00 `meaningLanguage.md` holds a typed word relayed from Field Sol b7da5d's record: "Let's call it the mid layer, or something. Let's go with Panini and look into astrological anatomy". There is also `flows/b7da5d/vision/layerVocabularyAndReview.md`.
10. **Fable:** the Primary seat's model, or a template of its own? Nothing since. Related: the 56ae53 recovery target (typed, 2026-09-26, after 21:36Z) says "the two Psyki flows: Fable and Opus, primary and secondary". I: this bears on it, since it pairs Fable with primary and Opus with secondary. It was said as a working recovery target and logged as such.
11. **Role fields:** subflow models; Addendum or Source; harness written or derived? Nothing since.
12. **Roster:** datom changed through Flow's meta wire, or a file someone edits? Nothing since.
13. **Word identifiers:** name, case, width, list size? Nothing since.
14. **Field tool:** does field-clj grow now, with the Field Nexus later? Nothing since. Related: the finding in C(c).

### B6. Fable's own comparison (`flows/b7ba00/reports/books-comparison.md`): eight conflicts

These overlap B5 items 1–8 and 13 (sender, stamping, content naming, pane form, receipt grades, effort, role fields, word ids). Its item 5, receipts (keep the grades through `Read`, or let the reply be the read witness), is not in B5. Nothing since.

### B7. Other open items (C, predecessor-recovery §3)

- Jev identity: "is TypeSafe AI's Jev the model you meant?" Artifact SXXpmqirStmWw5ZBNw2f4M.
- The artifact scroll skill line, T93:1667.
- The unfinished 21:04 sentence.

Nothing since on any of them.

## C. The four design findings b7ba00 held for Psyche Opus

Source of the four findings: `flows/93ba9f/log.md` (entry "b7ba00 handed over integration…"), and `flows/b7ba00/log.md` lines 23–54.

### (a) A check read a retyped Lojix revision; a check must read the lock

- C (b7ba00 log 51–54, e167d8 log 225): CriomOS main e6a83edc's `checks/lojix-ownership/default.nix:186` asserted a hardcoded "c4bba4fa…" against the lock's f090da07. b7ba00 ruled a fast-forward to 6d14ffb, which reads the lock.
- O: in a fresh clone of LiGoldragon/CriomOS, `origin/main` is d04257a8 (2026-09-26 17:03 −06:00). Its `checks/lojix-ownership/default.nix` derives from `flake.lock` (line 200: `assert (rootLocked "lojix").rev == inputs.lojix.rev;`), and "c4bba4fa" occurs 0 times. Commits 7556680 ("derive expectations from the lock files", 09-25) and 66aad7c are ancestors of main, as are 6d14ffb and e6a83edc.
- **Status: fixed in CriomOS source (O).** No bead exists (O). The general rule "a check must read the lock" is not found written as a skill or rule; this subflow did not search skills for it.
- A side bead from the same trace, CriomOS-unm (criome-deps E0432), was not checked here.

### (b) Lojix self-deploy orphans the in-flight row

- O: bead **primary-8sd** [P1 bug, OPEN, assignee b7da5d]: "Lojix self-deploy handoff orphans the in-flight row: 38 stuck in Copying after its own TestActivation replaced the Nexus (7.0.0 → 8.1.0)". Notes: "Design gap: a deployment that replaces the Nexus needs a handoff/terminal write before switch or recovery on restart." It was read with `bd --readonly --sandbox`.
- O: a related older bead, **primary-mjl.6** [P0 bug, IN_PROGRESS, assignee li, updated 2026-08-11], covers terminal deployment truth across daemon and client upgrades. Its acceptance criteria include "Lost child, lost event, locked store, and partial activation have checkable recovery states."
- **Status: open, unfixed.** The assignee b7da5d is a stale pre-crash route (C, dc53b4 log). No live owner was found in the 8904b1, 56ae53 or 9ac67c records, and no Lojix change for it was found. The Lojix repository itself was not searched.

### (c) A field-clj refusal rewinds the whole op log

- O: LiGoldragon/field-clj `origin/main` 3e5f450 (2026-09-26 09:56 −06:00). `src/field_clj/jj.clj:79` still runs `jj op restore <operation>`. README:102 documents: "`jj op restore` restores the whole repository view. If another writer made an operation in the same workspace between the recorded operation and the refusal, that operation is undone too." The remote has only `main` and `deps-hash-b860be`, so there is no rebuild branch.
- C (e167d8 log 155): Mind Sol a676b3 planned the safe #commit (landing workspace, three-way merge, Datalevin lease, fast-forward only; ETA 2–3 h). No later record of its landing was found.
- No bead exists (O: searches for field-clj, rewind, restore).
- **Status: not fixed on main. The rebuild owner a676b3 is pre-crash; no live owner found.** The standing rule still holds (C, 93ba9f log): field-clj #commit is not used in primary, and records land from an own jj workspace.

### (d) Beads auto-export runs raw git and may have moved HEAD

- C (b7ba00 log 23, 45, 49): `bd`'s auto-export ran `git add` in the colocated checkout and failed on `.jjconflict-base-0` deletions. b7ba00 raised it as a hypothesis for the 10:06:23 import-git-head that replaced its working copy. b7ba00 called it "unverified".
- No bead exists (O: searches for beads, export, git add, colocated). No owner or assignment was found. `/home/li/primary/.beads` holds `export.jsonl` and `export-state.json` beside the embedded Dolt store (O).
- **Status: unverified hypothesis, unassigned.**

### Integration ownership as of now (C, 8904b1 log, not on origin/main)

- 8904b1 ruled, on 56ae53's request:
  - Home step-2 integration owner (messenger pin, Home checks, Home main move; later the Flow 0.17.4 Home pin and gates): **Mind Astra 6fe957**.
  - Breaking stable Flow 0.12.2 → 0.14.0 host transition: **Field Sol 9ac67c**. Section "Field Sol 9ac67c accepts the stable Flow transition and Prometheus", line 665.
  - Restoring the Prometheus builder and access path: **Field Sol 9ac67c**.
  - Zeus evaluate/build gate: transferred to **Mind Astra 6fe957**, who accepted and holds lock 7707 (transcript, 01:20Z and 01:23Z).
- 8904b1's own words (line 713): "Conflict in the record, not resolved: 93ba9f, not the living, gave the Home merge and deploy gate to Field Sol; this seat gave the Home pins and gates to Mind Astra." And line 712: the living's word that Fable designs and thinks, not merges, sits against 8904b1 ruling on integration.
- The living has not ruled on who owns integration. dc53b4's proposal (Field Sol 9ac67c) is still open with the living.
- None of these assignments names findings (a)–(d).

## D. The living's words after 2026-09-26 21:36Z in the recovery flows

**Method.** The main user turns were extracted from every Claude transcript and every Codex (`.codex`, `.codex-next`) rollout with records after 21:36Z. Subagent threads were excluded, and machine relays (`#msg`, `#psyche`, launcher prompts) were set aside. They were cross-checked against the 56ae53, 9ac67c, 8904b1 and dc53b4 logs.

**Finding (O):** none of the living's words after 21:36Z speaks to the primitive Message, the letter shape, the design books, Sema, the database name, or findings (a)–(d). All of them concern power-failure recovery, seat count, Flow version, and Prometheus/Zeus networking. Verbatim, in time order (Codex session 01a0de4c = Mind Sol 56ae53 unless marked):

- 22:24:48Z: "Okay, we had a catastrophic power failure … If you find a flow that's old, above 200,000 tokens … you should just get maybe a sonnet agent to put together a restart prompt from the transcript of that abandoned session and refresh it. I think it is better. Just give it a bunch of fresh psyche rather than reanimate a 200,000- to 300,000-token session." (full text: `flows/56ae53/log.md`)
- 22:26:16Z: "I should have at least 9 flows by the time you're all done … We should have: - the two Psyki flows: Fable and Opus, primary and secondary - the three Codex flows: primary, secondary, mind, and field / I want Sonnet too because I like talking to Sonnet to ask silly questions to the psyche. … Put the psyche in their middle stratum context layer with the subagent using the messaging tool". This bears on B5 item 10 (roles/templates).
- 22:38:22Z: "… maybe somebody can run an opus job on retrieving the Psyche opus context together and launching it. Using Psyche opus to recover all of the right context to go back and finish everything that he hadn't finished". This is the mandate for this recovery.
- 22:56:30Z: "You should use the newer Flow. You should just install it and use it. It's supposedly better. Even if there's a 0.17, I think."
- 22:59:56Z, Codex 01a0dfef (a Field seat, cwd /home/li/primary): "Hey, you should help restart all of the flows. We should have nine flows. Talk to mine Sol." Then 23:05:55Z: "I told you to help. Still help." and 23:06:13Z: "Can't you talk to him?"
- 23:47:27Z: "So it's been hours now, and you've only started two more flows. Are you fixing something to start flows? … where do we have a hacky closure version flow launch thing that we can use, or what's happening?"
- 00:37:58Z, 00:41:01Z and 00:43:24Z, to Field Sol 9ac67c: the Zeus/Prometheus network and update instructions, including "engage bootable forever on the whole operating system on Zeus" (logged in `flows/9ac67c/log.md` and dc53b4's log).
- Relayed at 00:39Z by 9ac67c as living words: "Can you tell me what's wrong with the check in your stack, in your asp check, in the field, right? … We need to make this more reliable." I: this is about the Wi-Fi access point, not finding (a).
- Shorter working questions to 56ae53 at 22:27–22:55Z (e.g. "Are you using the new Flow Nexus with the CLI?"): all logged verbatim in `flows/56ae53/log.md`.

**Artifact comments.** No comment on any of the six artifacts read is later than 21:13Z (O).

## E. Psyche records of 93ba9f and b7ba00 (origin/main)

Every entry is dated 2026-09-26 unless marked. Flags: **[A]** Primitive Message, **[B]** books and letter shape, **[C]** findings, **[D]** later words, **[Own]** integration ownership, **[Roles]** roles and templates, **[Zeus]** the Zeus/boot question. No record in either flow mentions Zeus, boot, or "bootable" (O: grep). **No record bears on [Zeus].**

### 93ba9f: 15 vision files, 1 notion (all heard directly by 93ba9f)

- **automation:** STT. "Nothing is up to me. Everything is being automated." [B: books-compared 1 and 12] Bearing: "I'm not going to close or start anything or type anything anywhere ever. … The user interface is going to be Unity".
- **callerIdentity:** STT. "It can get its origin without the user having to say, 'Hey I'm Psyche Fable.' It would just know." [A, B] Bearing: "This is a standard thing that we need to put in Signal."
- **datomVocabulary:** STT, two entries. "Datom doesn't have tags, has variants." [B: letter shape]
- **ethosNames:** typed artifact comment, 15:17. "There are these open-ended variants, which we call names." [B]
- **fableRole:** STT. "Fable's job is to design and think not sweep the floor." **[Own]**
- **fieldTool:** STT. "Maybe let's get the field up to speed, redeploy it at the latest version, and develop new things like we were thinking about: version control, committing, getting transcripts from certain sessions" [B14, C(c)]
- **flowLaunching:** STT, four entries. [Roles] Bearing:
  - "Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped."
  - "We should have a list of flows all programmed with their datom configuration."
  - "there are different effort levels for different models so it's a property, the data of the model variant."
  - "I don't see the primary, secondary, tertiary part."
  - "Let's keep field Luna on that. She has all the authority to stop and start flows."
- **jev:** STT. "I want to integrate that and start using it" [B7]
- **meaningLanguage:** 20:54 typed comment, 21:13 typed comment, 21:11 typed comment, and two STT entries. [A6, B3, B4] Bearing:
  - "we rename all of the Sema aspect pertaining to the database … We're going to just call it something else, something clever (the database)."
  - "The first version of sema could be that it just has one or two layers of variants … the payload at the end being a string … this then becomes the basis for how agents start to communicate with the message component."
  - "We could even have the inner component be Markdown".
- **messagingInterface:** STT ×6, typed comment 17:28, typed comment 21:04. [A1–A6, B] This is the core record for A and B. Bearing: see A. Also "the sender being called 'owner' is fucking ridiculous … for now the sender is psyche primary or psyche secondary, etc." and "A raw flow send … should be a meta socket operation".
- **mindRoles:** STT. "Astra does the designing and the orchestrating and the big decisions and Sol does the implementation and the testing." [A: who builds; Own]
- **presentation:** STT, two entries. "Really the best way to reach me is to create a Claude artifact." [B7: scroll skill line] Bearing: "I like the scroll-down format not the page swipe/accordion thing".
- **primarySeats:** STT. "models should refrain from talking to the primary models." [Roles]
- **psycheSharing:** STT. "you each do your own. You give him all the psyche material" [B]
- **sessionClosing:** STT. "Let's just teach the system to close panes, to close sessions itself."
- **wordIdentifiers:** STT, two entries. "They would become a PascalCase series of words instead of hashes" [B: word ids] Bearing: "BIP-39 was the one we found to be most efficient … avoid homophones".
- **notion/semaCommunication:** STT, notion. "It's like a complete communication: here's a vector of utterances, here's a vector of acts, and here's a vector of ethos objects" [B4]

### b7ba00: 11 vision files, 1 notion

All relayed, none heard directly (8904b1 log 702, C). Nearly all are copies of the 93ba9f records above; only what differs is listed here.

- **fableRole, callerIdentity, mindRoles, types, designBook, reachingTheLiving, wordIds, flowAnatomy:** relays of 93ba9f's fableRole, callerIdentity, mindRoles, ethosNames, psycheSharing and fieldTool, presentation and primarySeats, wordIdentifiers, and flowLaunching. Flags as for the 93ba9f originals.
- **messaging:** relays of messagingInterface and datomVocabulary. [A, B]
- **modelFlows:** e167d8's relay of the emergency ("there's more than one Fable … a big leak"; STT ~14:15), plus relays of flowLaunching and automation. [Roles]
- **meaningLanguage:** relays of 93ba9f meaningLanguage plus older entries a psyche hunt found. [B3, B5-9]
  - 09-26 typed, via b7da5d's record: "Let's call it the mid layer, or something. Let's go with Panini and look into astrological anatomy". [Roles/B5-9]
  - 09-24 typed: "The biggest gain is when you have the meaning language in Datom specified".
  - 09-19 STT, five entries from f38926. Among them: "There's a root variant, so you can have a vector of these or a single of these"; "we're going with Vaiśeṣika here"; "a Pascal-case sentence expression".
  - 09-17 typed: "the string will become the next more efficient string type".
  - Two undated STT entries from 5851f4, on the Aṣṭādhyāyī.
  - 08-11 typed: "once we open the Meaning delimiter … all the delimiters and structured parsing spectrum is available".
- **notion/sema:** relay of semaCommunication. [B4]

### Provenance discrepancies between the two flows' copies (O)

For each passage, 93ba9f's mark comes first, then b7ba00's:
- Raw-send comment: typed comment 17:28, but b7ba00 marks it STT.
- Ethos-names comment: typed comment 15:17, but b7ba00 `types.md` marks it STT.
- The two Sema-v1 passages: STT, but b7ba00 marks them "typed (artifact comment)".
- The complete-communication notion: STT, but b7ba00 marks it "typed (artifact comment)".

93ba9f heard these directly, and b7ba00 only through relays. books-compared §5 already flagged the first two as b7ba00 errors. The Sema-v1 and notion mismatches are new here and point the same way (I).

## Remaining gaps

- The rest of the 21:04 comment ("Queries and responses") does not exist anywhere searched. Only the living has it.
- Nothing in the records shows who carries the primitive-Message package after 31147a died. It is unassigned (C, dc53b4 log).
- For finding (b), the Lojix repository was not searched for a fix in progress. For (a), CriomOS-unm and the general "a check reads the lock" rule were not checked.
- The 8904b1, 56ae53 and 9ac67c records read here are worktree copies, not on origin/main. They may differ from what later lands.
- There are no c56100 records anywhere.
- The `transcript` tool is absent. The Codex parse used `item_completed`/`UserMessage` events of main threads only, so a living word inside a subagent thread, or in a Codex format not parsed here, would be missed.
- The five items on the Opus book's list (B1 q5: lock ownership, contradictory hash instructions, messenger refusing Codex) were not re-checked for fixes.

## Sources

- `flows/93ba9f/log.md`; `flows/93ba9f/reports/opus-primitive-message.md`, `opus-design-book.md`, `books-compared.md`; `flows/93ba9f/vision/*.md`, `notion/semaCommunication.md` (origin/main; identical to /home/li/wt/primary/93ba9f).
- `flows/b7ba00/log.md`; `flows/b7ba00/reports/message-primitive.md`, `primitive-prototypes-comparison.md`, `design-book-letters-roles-monikers.md`, `anatomy-of-the-meaning-language.md`, `sema-version-one.md`, `books-comparison.md`; `flows/b7ba00/vision/*.md`, `notion/sema.md` (origin/main).
- `flows/dc53b4/log.md`, `flows/dc53b4/reports/predecessor-recovery.md`.
- `flows/d8df70/vision/messaging.md:64-69`; `flows/836818/vision/flowNexus.md`; `flows/0625c3/vision/lateralThenUpRouting.md`; `flows/e167d8/log.md` 155, 216, 223, 225; `Vision/messaging.md`.
- `/home/li/wt/primary/56ae53/flows/8904b1/log.md` (lines 78–93, 147–156, 594–606, 665, 702–715); `/home/li/wt/primary/field-packet-56ae53/flows/56ae53/log.md`, `flows/9ac67c/log.md`; `/home/li/wt/primary/roster-repair-medium-c56100/flows/56ae53/vision/model-flow-emergency.md`.
- Artifact comment threads: 5vspDLuChyZbZ1MmPfw1u4 (bf161595), 29ygc6gwx83B81XZLg8Dby (69b8ff09, b3595cc6), 4aaZsqHKN19SLUxk1UHwjE (1fa9256a); none on Qz8dpKBzJfbQgAbdUmfZCe, Dkzn57DKYhMyYc8GiKjRTP, P1PUozuFzS5kMNPgYEMA5q, DQjhVz7j5pNaoXGYv4zmEN.
- Beads (`bd --readonly --sandbox`, /home/li/primary): primary-8sd, primary-ql9, primary-mjl.6; searches for lojix-ownership, field-clj, rewind, restore, op log, HEAD, beads, export, git add, colocated, criome-deps.
- LiGoldragon/CriomOS origin/main d04257a8, `checks/lojix-ownership/default.nix`, ancestry of 6d14ffb, e6a83edc, 7556680. LiGoldragon/field-clj origin/main 3e5f450, `src/field_clj/jj.clj:79`, README:100–102, remote refs.
- Transcripts: Codex rollouts in `/home/li/.codex-next/sessions/2026/09/26–27` (sessions 01a0de4c = Mind Sol 56ae53, 01a0dfef, 01a0e029 = Field Sol 9ac67c); Claude transcripts under `/home/li/.claude*/projects` with records after 21:36Z.
