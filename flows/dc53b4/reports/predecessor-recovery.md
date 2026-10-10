# Predecessor recovery: 93ba9f (and the end of e167d8)

Carried for Psyche Opus dc53b4. Bounded reading only (tail, targeted search, per-record extraction). Record numbers are JSONL line numbers.

- T93 = `/home/li/.claude/projects/-home-li-primary/93ba9ff6-d24a-4dd0-a5c7-f98fab5ca9de.jsonl` (1901 records, 17:24:36Z to 21:36:02Z on 2026-09-26)
- TE = `/home/li/.claude/projects/-home-li-primary/e167d857-17e7-441b-b38b-54941a77a77a.jsonl` (3796 records; last content 18:04:48Z)
- 93ba9f flow records were read from commit `6bc3925fb` ("93ba9f: log mind handoff"), which is on `origin/main`.

## 0. Where the records are

- `/home/li/primary` is on a detached HEAD that is **behind origin/main**. `flows/93ba9f/` in that checkout is an **empty directory**, and HEAD `d695c5271` does not contain `6bc3925fb`. The 93ba9f files (log, 15 vision files, 1 notion file, 10 reports) exist on `origin/main` and in `/home/li/wt/primary/93ba9f/flows/93ba9f/`. Read them from there, not from the primary working tree.

## 1. After the last log line ("Both primitive-Message prototypes published ... delivered to Mind Astra 31147a")

The log line was written at T93:1891 (21:35:09Z) and pushed as `6bc3925f`. Everything that follows it:

- T93:1894 (21:35:17Z), 93ba9f to the living: Mind Astra has the whole package (eight statements, both prototypes, the brief) and started work. It is the only live Mind Astra. Four Mind seats are done and idle: astra 26c50c, f5a74e; sol a676b3, `mind-sol-of-00f95a-56ae53`. "Open for you: the four prototype questions; Fable's rulings on Sema; the name for the database."
- T93:1897 (21:35:53Z), #msg from Fable b7ba00: the comparison of the two prototypes landed at `flows/b7ba00/reports/primitive-prototypes-comparison.md` on primary main. Settled for Astra: Markdown payload; no id, named sender or priority in the letter; origin stamped from peer credentials through Flow, unknown callers refused, the same lookup serving Flow's Refresh; the reader sees the sender's seat; a small closed address set (up, down, across an aspect, explicit seat) resolved by Message through Flow; Mnema converging for the database; Astra designs, Sol implements. Fable "is sending the same to Mind Astra 31147a with both artifact links; you hold the living's channel for the rulings."
- T93:1900 (21:36:02Z), 93ba9f's last words to the living. Six rulings:
  1. With no seat above, does the message go to the next seat below (the living, 24 September)? Fable yields to that ruling.
  2. Interruption: 93ba9f's per-kind table still uses the soft/abrupt words the living called the wrong approach. Fable's primitive interrupts nothing. Should the primitive interrupt nothing?
  3. Address word: `Toward` (Opus) or `Bearing` (Fable)?
  4. Kinds: five generic kinds (Report, Question, Answer, Order, PsycheUpdate) with the aspect read from the sender, or nine aspect-named kinds (`FieldReport`, `PsycheQuestion`, ...)?
  5. Replies: `Sent`/`SendRejected` or `Delivered`/`Parked`/`Refused`?
  6. Is the database Mnema?
  Gaps Astra will cover: whether Order/Answer carry an aspect; malformed-send refusals; what happens to parked letters when an empty seat later fills.
- After that the transcript ends with no further records. The power failure left 93ba9f idle. It had no background agents: every one of its 46 Agent dispatches has a completion notification, and T93:1895 shows no pending count.
- **Not in log.md**, from the final hour: the Jev research artifact `https://claude.ai/artifact/SXXpmqirStmWw5ZBNw2f4M` (T93:1717). The subflow identified the model as TypeSafe AI's Jev (`typesafe/jev-1.13`, `typesafe/jev-router` on OpenRouter), a decision model with JSON in and a choice or score out. The OpenRouter key goes into gopass. Question pending: "is TypeSafe AI's Jev the model you meant?" The source report is `reports/jev-and-openrouter.md` (commit cd24a19f).
  - Two Books Compared: `https://claude.ai/artifact/5vspDLuChyZbZ1MmPfw1u4` (T93:1551).
  - Fable's Noema book: `https://claude.ai/artifact/29ygc6gwx83B81XZLg8Dby` (T93:1634). Fable's "Sema, version one": `https://claude.ai/artifact/DQjhVz7j5pNaoXGYv4zmEN` (T93:1836). Its source is `flows/b7ba00/reports/sema-version-one.md`, with five rulings: the database name (Mnema, Thesauros, Archeion), Markdown as an Ethos alias of String, Response.Assent bare, sender outside the sema, and the first kinds to ship (Order, Question, AuditRequest, InformationRequest, AuditReport, ImplementationReport, PsycheUpdate, Answer). It also has two Mind items: what refers to Ethos's root named Sema, and the recall rows of the equivalents table.
  - Opus design book `P1PUozuFzS5kMNPgYEMA5q`, Fable design book `4aaZsqHKN19SLUxk1UHwjE`, Letter `K2PeBs7pNVXm8sQB45YmEN`, Configured Flow Roles `9TJJz1T2sZcbgSBAcdmCGz` (T93:1560 brief).
  - A skill line proposed for the living's approval (T93:1667): *"The page scrolls vertically only: no page swipe, carousel, tabs or accordions; a long code line scrolls inside its own box, never the page."* No answer is recorded.
  - Category answer (T93:1735): Category is not equivalent to Ethos. It is a Vaiśeṣika vocabulary written in Ethos (`meaning.ethos`) and adds no construct. The action stub is separate from the built Pāṇini `Act`. The Sema rename reaches Ethos's root form named Sema.
  - Three-layer answer (T93:1762): Utterance (new), Act (Pāṇini, built) and Category (Vaiśeṣika, built), with Annotation beside them. These are layers of meaning, not three levels of nested variants.

## 2. The living's words to 93ba9f not logged verbatim

Method: extracted every `user` record from T93, removing skill expansions, task-notification bodies, `#msg`/`#psyche` relays and pasted content. That left 30 typed prompts (17:25Z–21:25Z). Each was split into sentences and each sentence was matched, normalised, against `vision/*`, `notion/*` and `log.md` of 93ba9f at `6bc3925fb`. Every miss was then checked by hand, since the logs carry transcription corrections. Artifact comments fetched by subflows (T93:378, 1576, 1612, 1696) were checked the same way. All comments written to 93ba9f's artifacts on 09-26 are logged in messagingInterface, ethosNames or meaningLanguage.

Counts: 30 prompts inspected, 25 judged psyche or instruction with content, 25 captured. The misses below are all captured except as noted. **No unlogged vision or notion was found.** The only uncaptured items are these:

| Where | Words (verbatim) | Judgement |
|---|---|---|
| T93:897, 2026-09-26T18:39:46Z | "But what is the other variant? You keep saying text. What's the other variant other than text for the last field there, because if you're putting text. That's a variant name." | Working question and correction. It has a vision kernel ("text" is a variant name, so it implies siblings), which restates T93:869, already logged in messagingInterface.md. **Absent from records.** |
| T93:1759, 2026-09-26T21:18:18Z | "Oh did you say there that the structure we had found before had three layers of variants basically?" | Clarifying question (context). Answered at T93:1762. Absent. |
| T93:1602, 21:04:42Z | "I made another comment." | Working notice. Absent; the comment itself is logged. |
| T93:1678, 21:14:09Z | "I've made some comments again." | Working notice. Absent; the comments are logged. |
| T93:218, 17:25:05Z | "Launch receipt confirmed. Begin the brief in your first prompt now." | Launcher (machine), not the living. |

The remaining hand-checked misses are captured with transcription corrections: T93:368 "closure" is logged as "[Clojure]" in datomVocabulary.md, T93:587 "strut" as "[struct]" in flowLaunching.md, T93:913 "self variant" as "soft variant" in messagingInterface.md:53, T93:1639 "Jev/Jeff" with [sic] in jev.md, and T93:1786 "Sonet [Sonnet]" in log.md.

**Unfinished living sentence.** Logged in messagingInterface.md but never answered: the 21:04 comment on Two Books Compared ends mid-sentence: "For the normal format that gets communicated, the non-debugging format, basically the production requests and responses (are those what we call them? Queries and responses)". 93ba9f and Fable both asked how it ended (T93:1625, 1673). There is no reply.

**e167d8's end.** The last living prompt to e167d8 (TE:3672, 17:19:07Z, "I don't understand your questions. ... Start on a fresh Flow. ...") is logged in `flows/e167d8/vision/userInterface.md` and `flows/e167d8/log.md` on origin/main. e167d8 received no living words after launching 93ba9f (TE:3725–3796 hold only the 93ba9f reap message, the subflow result and the handoff).

## 3. Unfinished work at the crash (ranked)

| # | Work | State at crash | Owner then | Evidence |
|---|---|---|---|---|
| 1 | Primitive Message build: Astra designs, Sol implements, on the points both prototypes agree on; forks come back to Psyche Opus | The package was Presented to **mind-astra-31147a** (pane w19:p5, codex) at 21:35Z, and it began working. No reply was witnessed. Fable also sent its comparison to 31147a. | Mind Astra 31147a, then Sol | T93:1890, 1897; opus-primitive-message.md; flows/b7ba00/reports/message-primitive.md, primitive-prototypes-comparison.md |
| 2 | Rulings pending the living | 6 prototype rulings (§1). Fable's 5 Sema-v1 rulings. Database name (Mnema, Thesauros, Kosha, Archeion). Jev identity. Artifact scroll skill line. The unfinished "queries and responses" sentence. The sender placement ("sender as first field inside each kind?", T93:1625/1673). | Psyche Opus | T93:1625, 1667, 1673, 1717, 1833, 1900 |
| 3 | Books-compared 14 rulings | Rulings 1–5 were presented (T93:1533). Several are overtaken: the head is the kind (21:04 comment), priority is gone, a Markdown payload, and the caller is stamped from the process (21:25). Still open: 8 effort scale and Xhigh, 9 layer mapping, 10 Fable seat or template, 11 role fields, 12 roster mutation path, 13 word-identifier standard (name, PascalCase, 2 or 3 words, list), 14 field-clj growth now. | Psyche Opus | reports/books-compared.md:120–135 |
| 4 | Flow 0.17.1 deploy chain | 0.17.1 (ac216c89) is proven in the sandbox. Field Sol b7da5d was told to bump the Home bookmark to 0.17.1. 0.17.2 (gate only) is on s1-e167d8. RetractionWitness is deferred to Flow 0.18 with a Message wire release. Scenarios 5, 6 and 8–12 were not re-run. | Field Sol b7da5d (now stale) | log.md; reports/flow-0171-proof.md, flow-gate-fixture.md |
| 5 | Integration handed from b7ba00 to b7da5d | Home 0.17 pair as bookmark integration-b7ba00-home, check on Prometheus, CriomOS repin, ouranos second deploy, three beads. Design findings (a)–(d) are held for Psyche Opus: a check must read the lock; Lojix self-deploy orphans the in-flight row; field-clj refusal rewinds the op log; beads auto-export raw git is a suspected cause of the HEAD move. | b7da5d (stale) | log.md "b7ba00 handed over integration" |
| 6 | messenger-clj Held/RepairRequired on most sends; Codex BindingRefused (Herdr 0.8.2 never fills agent_session) | Open defect; route repair undecided. A held HM message to Luna **must not be repaired** (it would duplicate the reap order). | unassigned | log.md; T93:1890 (0.2.5 has no `#psyches` plural) |
| 7 | Launch guard, role roster (one live seat per role, effort from template) | The design is in the books. b7ba00 was told to hold the implementation until the design lands. | unassigned | reports/roles-anatomy-2.md; vision/flowLaunching.md |
| 8 | Word identifiers | Research landed. Open: verify against the current Claude tokenizer, hand-prune, 2 vs 3 words, the name. | Psyche Opus | reports/word-identifiers-research.md |
| 9 | Field tool (version control, commit, transcripts) and field redeploy | Ordered by the living at T93:913 and proposed in design book §6. **Not dispatched.** | unassigned | opus-design-book.md §6; vision/fieldTool.md |
| 10 | field-clj `#commit` rebuild | a676b3 was "done" at 21:35Z; the result was not read by 93ba9f. | Mind Sol a676b3 | T93:1890 |
| 11 | Reaping and archiving | Luna e71dab ran the reap census, then cleared to close e167d8. The e167d8 and e167d8-cleanup workspaces are to be forgotten. Leftover seats 26c50c, f5a74e and 98eb43 were seen done. | Field Luna e71dab | log.md |
| 12 | persona-test suite move into the message-flow runner | Not started | unassigned | log.md (e167d8 handoff item 5) |
| 13 | Found on the way: anyone can release any Orchestrate lock; two instructions contradict on 40-char hashes; messenger refusals | Asked "Should these go to the Field now?" No ruling. | Psyche Opus | opus-design-book.md §7 Q5 |

### e167d8's eight questions: what happened

1. **Leftover seats** (26c50c, 98eb43, f5a74e): not asked. They were folded into the living's reap order (T93:485), and all three were seen done.
2. **Role-template text**: not approved. The living redirected at T93:453 ("We should have a list of flows all programmed with their datom configuration ...") and T93:587 (effort is the model variant's data). This is re-derived as roles-anatomy-2 and books-compared rulings 8, 10, 11 and 12, which are open.
3. **compensation-nix line**: never raised.
4. **Stable/next skill section**: never raised as a question. 93ba9f cited it as living vision (T93:1209).
5. **Layer words**: the living had already ruled "primary, secondary, tertiary, quaternary" (e167d8 layerVocabulary, ~13:10) and rebuked 93ba9f at T93:587: "It's like you didn't integrate our vocabulary change." Sub-conflicts (a)–(e) remain open as books-compared ruling 9.
6. **Letter shape**: answered by the living in depth. No message ID. "owner" is "fucking ridiculous". The sender is a seat, derived from the calling process. The head is the message kind, not priority. "We don't even do the soft or hard, actually." The payload is Markdown in string delimiters. This is logged in messagingInterface, callerIdentity and meaningLanguage.
7. **Low-seat effort**: partly answered. At T93:453 the living said: "It's not that we don't allow high effort. It's just that we haven't made any flow ... that uses high effort." "Luna at high/light" is still open as ruling 8.
8. **Oracle-package composer**: never raised.

## 4. Open forks in the design book and the prototype

- **Design book** (`reports/opus-design-book.md`, artifact P1PUozuFzS5kMNPgYEMA5q): its Q1–Q3 (priority head, four content variants, three reply registers) are **superseded** by the 21:04 head-is-kind comment and by the 21:25 primitive order. Q4 (merge the built word-name anatomy with a 1,024-word single-token list, and the name) and Q5 (send the found faults to Field) are still open.
- **Primitive prototype** (`reports/opus-primitive-message.md`, artifact Qz8dpKBzJfbQgAbdUmfZCe): `Send.{ Toward Kind }`, `Toward.[ Up Down Across.Aspect Seat.Seat ]`, five kinds, an `Origin.{ FlowId Seat Model }` Signal standard, Flow `ResolveToward`, and a per-kind interrupt table in Message's database. Open forks against Fable's version: the six rulings in §1 (escalation with no seat above, interrupt table vs none, Toward vs Bearing, 5 generic vs 9 aspect-named kinds, reply words, Mnema). Fable adds a `Living` address. Its own questions: Toward as "send up", 5 kinds, database name, Origin as the Signal standard for every Nexus.

## 5. Against current knowledge

- The primitive-Message package went to **Mind Astra 31147a**. dc53b4's live roster has Mind Astra **6fe957**, and 31147a is not live. Neither the package nor Fable's comparison reached a live Mind Astra, as far as the records show.
- The Fable sources for the prototype, the comparison and Sema v1 are under `flows/b7ba00/` (a stale seat). The live Fable is 8904b1.
- `/home/li/primary` does not hold the 93ba9f records (see §0).
- 93ba9f's log paraphrases the "Pass all of this new stuff to Fable" instruction, but it is verbatim in log.md with "[Sonnet]". No contradiction.

## Sources

- T93 records 218–1901 (typed prompts at 297, 341, 368, 453, 485, 587, 628, 653, 714, 736, 770, 815, 869, 897, 913, 957, 1557, 1602, 1639, 1678, 1723, 1748, 1759, 1767, 1786, 1803; comment results 378, 1576, 1612, 1696; replies 1533, 1544, 1591, 1625, 1634, 1667, 1673, 1717, 1735, 1762, 1861, 1870, 1894, 1900; relays 1863, 1897, 1833)
- TE records 3672, 3725–3796
- `git show 6bc3925fb:flows/93ba9f/{log.md,vision/*,notion/*,reports/opus-design-book.md,reports/opus-primitive-message.md,reports/books-compared.md}`
- `git show origin/main:flows/e167d8/summary.md` (eight questions); `git grep origin/main -- flows/e167d8` for the capture of TE:3672
