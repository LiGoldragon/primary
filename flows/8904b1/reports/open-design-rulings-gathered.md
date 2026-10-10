# Open Design Rulings Gathered

This report was compiled by a read-only companion agent (flow aab99311ea08d7045, dated 2026-09-27) and extracted and saved by a second subflow as a byte-faithful copy of the companion's final findings. The companion's own judgments are marked as such. This report was saved from the transcript by extracting the final assistant message without summarization, reordering, or alteration.

{ «Gather every open design ruling from b7ba00, 93ba9f and dc53b4, with the living's words that bear on each, plus the non-design questions now with the living, as material for one artifact that 8904b1 will compose.» «Nothing was written: this seat is not allowed to edit files, so the whole result is here. Marks: O = I read it myself. C = a record or flow says it. I = my inference. Sources are at the end. dc53b4's report `flows/dc53b4/reports/recovered-design-state.md` is only on origin/main (8d9e1a3b); I read it there. The /home/li/primary checkout is detached at 9c3d6bf87. Its copies of the b7ba00 and 93ba9f reports and vision records are byte-identical to origin/main (O: git diff). dc53b4's list checks out against the reports, with some additions, marked NEW.

Terms the flows coined, used below:
- **Seat**: an aspect times a layer, written `Psyche.Primary`, `Field.Tertiary`.
- **Letter**: one message.
- **Kind**: the letter's head, for example `Order`.
- **Origin**: the sender's seat, stamped by Message and never typed by the agent.
- **Parked**: a letter held because no live flow sits on the target seat.
- **Crucial**: the living's 09-24 word for flows that are started if missing.
- **Utterance**: the top level of Sema (statement, inquiry, and so on).
- **Support**: what a statement rests on.
- **Addendum**: extra first-prompt material.
- **Roster**: the list of configured roles.
- **Moniker**: Fable's name for words in place of hashes.

## A. Primitive Message (dc53b4's six, verified, plus four more)

A1. **When the target seat is empty or none exists above.** Does the 09-24 rule (try higher, then lower, start a crucial missing flow) already apply in the primitive?
- Opus: `Up` from Field.Tertiary goes to Field.Secondary. If that seat is empty it goes to the next above, and if none is above, to the next below. A crucial empty seat is started. Refusals are `NoSeatAbove NoSeatBelow`.
- Fable: the letter is parked and the sender gets `NoSeat.Field.Secondary`. Fable says escalation is "the next version's rule".
- Living, typed comment, 2026-09-24 14:31Z (d8df70 messaging.md, "Psyq"→"Psyche" corrected): "If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules. / Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial."
- Already answered: the rule itself. Remainder: does it apply now or later? And which of Primary…Quaternary count as "medium and high", so which are crucial? That mapping is unruled (b7ba00 books-comparison §10).
- Depends on it: the Refusal list, and whether Message needs Flow to start seats. Still current.

A2. **Does any kind interrupt the recipient in the primitive?**
- Opus: a hidden per-kind table, `{ PsycheUpdate MiddleAbrupt } { Order MiddleAbrupt } { Question Soft } …`.
- Fable: nothing interrupts; every letter waits for the recipient's turn.
- Living, typed comment 2026-09-26T21:04 (93ba9f messagingInterface.md; "software" kept [sic]): "We'll make the judgment of what kind of messages we want to break harder than others so it's just what kind of message it is, really. / We don't even do the soft or hard, actually. That was the wrong approach. For the normal format that gets communicated, the non-debugging format, basically the production requests and responses (are those what we call them? Queries and responses)". That last sentence is **unfinished** in the record; do not read it as a statement. Earlier in the same comment: "a hard psyche update, which interrupts".
- Already answered: no soft/hard marking in the letter, and interruption is judged per kind. Remainder: in the primitive, which kinds interrupt, if any? And how did the unfinished sentence end?
- Depends on it: Message's per-kind table. Distilled `Vision/messaging.md` still says "Priority is a head on the datom" (`Priority.[HardAbrupt MiddleAbrupt Soft]`); the 21:04 words stand against it and it is not corrected (O). Still current.

A3. **The address word, and whether the living is an address.**
- Options, each written as sent:
  - Opus: `message 'Up.Question.MayIRestart'`, type `Toward.[ Up Down Across.Aspect Seat.Seat ]`.
  - Fable: `message 'Send.{ Up FieldQuestion.MayIRestart }'`, type `Bearing.[ Up Down Across.Aspect Living To.Seat ]`, with CLI words `send-up`, `send-across psyche`.
  - Fable alone has `Living`, which reaches the living's pane. Fable also lists Heading and Course as alternatives.
- Living, STT 2026-09-26 (93ba9f): "If you say "send up" it means message higher layer, whatever however we say that, let's find a clever way to say that: message to higher-layer type message." Also "models should refrain from talking to the primary models" (STT 09-26, primarySeats.md). I: that bears on whether `Living` should be an address that is easy to reach.
- Open: all of it. Still current.

A4. **Kinds: five general, nine aspect-named, or another list; and the first set.**
- Opus: `Report Question Answer Order PsycheUpdate`. The aspect is read from the sender's seat, so `Report` from a Field seat is a field report.
- Fable: `FieldReport FieldQuestion MindReport MindQuestion PsycheReport PsycheQuestion Order Answer PsycheUpdate`. Message refuses a kind whose aspect is not the caller's.
- Sema v1 Ruling 5: `Order Question AuditRequest InformationRequest AuditReport ImplementationReport PsycheUpdate Answer`.
- Living, STT 09-26: "a simple anatomy of a few different types of messages that are simple and easy, like: field report / psyche report / field question / psyche question … We could type the message based on the type, because if you send the message you have the same type." Same day, STT: "An order / A question / A request for an audit / A request for some information". Typed 21:04: "We can make any number of kinds … It's a new type and it carries all the data."
- Already answered: the kind set is open and grows by declaring a type. Remainder: is the aspect part of the kind's name or read from the sender? Which kinds ship first? Do Order and Answer carry an aspect (Fable Fork 2)?
- Depends on it: the Ethos of signal-message. Still current.

A5. **Reply shape.**
- Opus: `Delivered.Psyche.Secondary | Parked.Psyche.Secondary | Refused.NoSeatAbove`.
- Fable: `Sent.{ Field.Tertiary Field.Secondary }` or `SendRejected.EmptyBody`, with causes `CallerUnknown KindNotCallers.Aspect NoSeat.Seat RecipientUnreachable.Seat EmptyBody`.
- NEW, Fable Fork 5: does `Sent` name the seat that "up" resolved to? Proposed yes. (Opus always names it.)
- Living, STT 09-26: "we create a shorthand version which has a shorthand response type or display type", and "You have this human prefix and then you create these human variant responses. You have the not-human but simple. Simple is better". Also typed 09-24: "The message returned for the caller will say what happened".
- Open: which words; whether delivered and parked are told apart; whether the reply names the recipient. Still current.

A6. **The database's new name.**
- Options: Mnema (Fable), Thesauros, Kosha (Opus), Archeion (Fable), or another. Cmp's "converging" is not independent: Opus lists Mnema as Fable's.
- Living, typed 21:13: "That means we rename all of the Sema aspect pertaining to the database … We're going to just call it something else, something clever (the database)." STT 09-26: "Let's figure out the name for the database part."
- Already answered: it is renamed. Open: the name.
- Depends on it: the storage library, `.sema` files, about fifteen consumers (Opus §6), and the Ethos root named Sema. Still current.

A7. NEW. **Origin: a Signal standard, and whose seat a subflow's call gets.**
- Opus Q4: `Origin.{ FlowId Seat Model }` becomes a standard every Nexus uses.
- Fable: `Origin.Seat` only, and a subflow's call resolves to the seat that owns it (Fork 3).
- Living, STT 09-26 (callerIdentity.md): "This is a standard thing that we need to put in Signal … It can get its origin without the user having to say, "Hey I'm Psyche Fable." It would just know."
- Largely answered: yes, it is a Signal standard. Remainder: does Origin carry Model, and does a subflow resolve to its seat? Low stakes; could be left to Mind Astra.

A8. NEW. **History.** Fable: `History.[ Last.Integer From.Seat Since.Age ]`. Opus has no type for it.
- Living, STT 09-26: "We're going to develop a different kind of interface to get message history."
- 93ba9f's comparison: a typed History "goes beyond the record". Open whether it belongs in the primitive. Minor.

A9. NEW, conflict. **Where the sender sits: primitive vs Sema v1.**
- The primitive has no sender in the request; it is stamped.
- Sema v1 puts `Sender.[ Living Seat.Seat ]` as each letter's first field: `Order.{ Psyche.Primary Injunction.Order.Regenerate }`.
- I: stamped on arrival, and typed in the stored or shown letter, may both hold. No record reconciles them. Belongs with A7, B1, B2 and E10.

A10. **Who holds the package.** Mind Astra 31147a is dead.
- O: its log in worktree `31147a-primitive-message-prep` shows no receipt of the package.
- C (8904b1 log 814): 8904b1 took custody of the design side "pending the living's word on its owner; implementation is not taken".
- Living, STT 09-26 (mindRoles.md): "Astra does the designing and the orchestrating and the big decisions and Sol does the implementation and the testing." Live Mind Astra is 6fe957; nothing is assigned to it. Open: who takes it.

## B. The letter: the two books and their comparisons

B1. **Is the living a sender?** Fable: `Sender.[ Living Seat.Seat ]`. Opus: "The living is never a sender"; the living's words are marked by not being datom.
- Living: "the agents will know that it's me because of how the message is formatted. It won't be datom-formatted" (09-18, c7128c, cited by 93ba9f, C). "we still get the differentiation from real Psyche input messages, which are not in EDN syntax" (09-25, e51411).
- Against that: "I'm not going to close or start anything or type anything anywhere ever … The user interface is going to be Unity" (STT 09-26, automation.md). Also "the sender being called "owner" is fucking ridiculous" (STT 09-26), which objects to a name and does not settle whether the variant exists.
- Open. Bears on A3 and A9.

B2. **Sender stamped now, or named by the caller "for now"?**
- Living, STT 09-26: "The message has to be able to figure out who the sender is programmatically eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc." The same day, callerIdentity: "It would just know. That's really what I want." And 09-25 (e51411): "It knows which pane the call came from".
- Both prototypes stamp. Open only if the "for now" still stands. **Probably overtaken** by callerIdentity. Confirm only; the order of the two statements that day is not established.

B3. **Content forms.** Opus: `Content.[ Message Psyche FullMessage FullPsyche ]` under `Letter.{ Seat Content }`. Fable: `Letter.[ Simple Full Psyche PsycheRecord ]`.
- Living, STT 09-26: "A simple message, a simple psyche / A full message that can have many fields, one of which is a vector of psyches that are essentially the support for that message".
- **Partly overtaken** by the 21:04 "the head … is where the message type is": b7ba00's addendum withdraws `Simple/Full` and the tier head. What survives: is the psyche a top-level kind (`PsycheUpdate`), and does a full letter carry a `Vector<Psyche>`?

B4. **The short psyche.** Options: `{ Context Verbatim Source }` (Fable), `{ Context Verbatim }` (Opus), or context alone. Also: do STT corrections carry marks in a separate variant (Fable Fork 1)?
- Living, STT 09-26: "The full psyche with the date and stuff / The short psyche, which is the context / Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there … Let's just put it in as we need it." Same passage: "an inner variant for the verbatim, like speech-to-text or if we know or unknown". 09-25 (e51411): "do we put square brackets around the part that was corrected for clarity?"
- The bracket words largely answer Fork 1: corrections stay inside the verbatim. Remainder: what the short psyche holds.

B5. **Time.** Does the full psyche carry a date, an age, or both? May any letter carry a timestamp?
- Living, STT 09-26: "an LLM-readable but more human-friendly time measure, like age … seconds, minutes, hours, days, and months and years". 09-25 (e51411): "We don't need this huge timestamp. I don't even know why we are doing the timestamp."
- Age is answered. Open: date in the full psyche.

B6. **Replies and panes.** Opus: replies in three registers, `Simple` (default), `Human.Sentence`, `Full`; letters stay datom on panes. Fable Fork 4: a human rendering on every pane by default, for example `PsychePrimary · Order · 3m` then the text.
- Living: "Simple is better" (STT 09-26). Distilled Vision: "A message is a datom, and it arrives as one." 93ba9f judged Fable's pane default to be against both.
- Open.

B7. **Receipts.** Fable keeps the grades `Submitted … Read`. Opus: "The read witness is the recipient's reply." Only Fable's comparison raises this. Open.

B8. **Message size.** Answered.
- Living, typed 2026-09-26 to b7da5d: "If there's still an 800-character limit on messages, I want that removed from everything, from everywhere." And "Let's just not limit ourselves on message size".
- Neither book writes it in. Only for writing down, not for asking.

B9. Only in Opus (C, 17 and 19 Sep quotes not verified by me): after a replacement, replies go to the successor; a "quiet channel" for small facts such as quota. Not asked in either book.

B10. **Raw pane send.** Answered.
- Living, typed 09-26T17:28: "A raw flow send … I think should be a meta socket operation and then we have a more lock-enabled deliver message."
- Open only: does the 09-24 permission to "bypass failing messages and send each other straight into your panes" (e51411) survive?

## C. Roles and roster

C1. **Layers.** Four layer words, or three power levels plus a temporary ultra-low? How do they map onto distilled `Vision/modelRoles.md` High/Medium/Low/UltraLow?
- Living, STT 09-26 ~13:10 (e167d8 layerVocabulary): "it's primary, secondary, tertiary, quaternary. That's the vocabulary I was actually looking for." STT 09-26 (93ba9f flowLaunching): "I don't see the primary, secondary, tertiary part … It's like you didn't integrate our vocabulary change."
- Earlier the same day, typed to b7da5d: "3 power levels for each of the 3 aspects: high, medium, low. That's all I need. If we need ultra-low roles, they're usually temporary". Also typed: "Let's call it the mid layer, or something."
- Answered: the words are Primary to Quaternary (newer, explicit). Remainder: is Quaternary a normal or a temporary seat? Distilled Vision still says High/Medium/Low/UltraLow and is not corrected. Also needed: the crucial-seat mapping for A1.

C2. **Effort.** One shared scale, `Low Medium High` (Fable) or `Low Medium High Xhigh` (Opus), or a scale per model?
- Living, STT 09-26: "there are different effort levels for different models so it's a property, the data of the model variant." Typed 09-26: "the low power as Luna at high effort or the ultra-low as Luna at light". Against that, Intent/models.md: effort "is never raised to buy" quality.
- Open. The tension was flagged earlier by b7da5d.

C3. **Fable: the Primary seat's model, or a template of its own?** Both books say model.
- Living, STT 09-26 ~14:35 (e167d8 roles): "the psyche fable / the psyche / the psyche primary / the psyche secondary / the psyche tertiary / the psyche quaternary".
- NEW: typed 2026-09-26T22:26:16Z to Mind Sol 56ae53 (dc53b4 report §D), said as a recovery target: "the two Psyki flows: Fable and Opus, primary and secondary".
- Older, 09-19 (b81560): "Psyche Fable and Psyche High are synonymous for now". Open.

C4. **Role fields.** Does a role carry the models it may start as subflows (Opus `Vector<Model>`)? Is the prompt material called Addendum or Source? Is the harness written or derived?
- Living, STT 09-26: "plus addendum things that are added into the prompt from files … Different variants". That record marks the phrase as unfinished as heard. Also: "For now we don't but I guess you can put it in."
- Answered in part: the name is Addendum. The rest is open.

C5. **Roster.** Datom changed only through Flow's meta wire, or a file someone edits (Fable Fork 7)?
- Living, STT 09-26: "We should have a list of flows all programmed with their datom configuration." Also "I'm not going to close or start anything or type anything anywhere ever."
- Answered: it is datom data, and the living does not edit it. Open: through what it changes.

C6. **Who decides refresh and reap?**
- Living, STT 09-26: "Let's keep field Luna on that. She has all the authority to stop and start flows. As long as she's told, she doesn't have the authority to decide." Also "Nothing is up to me. Everything is being automated."
- The decider is unnamed. Raised only as a tension in b7ba00's comparison.

## D. Words in place of hashes

D1. The standard's name, case, width, list, and where the converter lives.
- An existing unmerged build: `LocalNameReference.{ Integer Integer Integer }`, with Cluster (6 words) and Public (12 words), camelCase, BIP-39.
- Fable: "Moniker", PascalCase, 2 or 3 words by the entropy needed, a 4096-word list vetted per word for token count, converter in the signal library.
- Opus: keep the build and its three levels, a 1024-word single-token list, a name from Wordprint, Saybits, Mnemonid, Tokenword or Hashspeak, converter in the field tool.
- Living, STT 09-26: "maybe two or three words, depending on how much entropy we need … a PascalCase series of words … Let's come up with a name for this if somebody hasn't … There's a converter that can use this in field and all our tools would support it". Second entry, same day: "BIP-39 was the one we found to be most efficient … push the density by adding the maximum number of words and also even aiming to avoid homophones". That record ends with no closing punctuation and is not marked unfinished.
- Earlier, 09-15: "camel case could be easily recognized as probably a hash" (05c604). "Give it a sensible name" (fd0f97). "three different levels of security" (692df8).
- Case is answered by the newest word: PascalCase. Open: the name (tell the living a name already exists), the widths, the list size, where the converter lives. Nothing is blocked on this.

## E. Sema, the meaning language

E1. **Name.** Answered: Sema. Living, typed 21:13: "Sema was supposed to be the language of meaning and so that is actually the right name."

E2. **Top level.** Five utterances, `Statement Inquiry Injunction Response Annotation`, or three? Fable's own addendum amends this: the five are the tree, and message kinds are Ethos types mapped onto it. No word from the living.

E3. **Support.** Does every statement carry its support, `Statement.{ Content Support }`, or only a full statement? No word from the living.

E4. **What a parenthesis annotates.** Always the unit before it? Example: `Lock.{ … (Injunction.Order.HoldUntilLanded) }`. Or may a parenthesis name its target explicitly?
- Living, typed 20:54: "some of them have a parenthesis that opens another subnote, more information concerning this particular aspect of it". Open.

E5. **Sanskrit names.** Rename the built variants (`Lakara`, `Prayoga`) to English now?
- Living, typed 20:54: "we're not going to use the Sanskrit terms but we can maintain a table of equivalents."
- Answered: they become English. Open: when.

E6. **Addendum fork.** Is the utterance a field of every kind, `Order.{ Sender Utterance Sema }`, or declared once per kind in Ethos and absent from the value? No word from the living.

E7. **Is the Category layer the same as Ethos?** The living asked this, typed 21:11. Flows answered: b7ba00 said "Category is Ethos, used for one purpose", and 93ba9f (C) said not equivalent, a vocabulary written in Ethos. The living has not replied. Only to confirm.

E8. **Sema v1 Ruling 2, the payload.** `Markdown` as an alias of String, and its delimiter: `Injunction.Order.«…»` in guillemets.
- NEW: the living's words are more than dc53b4 quoted. STT 09-26: "We could even have the inner component be Markdown, I guess, and it can be delimited by a parenthesis if we want. I think the same delimiter that we use for strings would work so that we're reminded that this part of SEMA is undeveloped".
- Answered: Markdown, guillemets allowed. Open: the alias, and whether a parenthesis is also allowed.

E9. **Sema v1 Ruling 3.** May `Response.Assent` carry nothing? No word from the living.

E10. **Sema v1 Ruling 4.** The sender outside the sema, as the letter's first field. See A9.

E11. **Sema v1 Ruling 5**, the first kinds, is the same question as A4.

Notion, not to be ruled: "here's a vector of utterances, here's a vector of acts, and here's a vector of ethos objects … This is more notion than vision." (STT 09-26.)

## F. Other items from the books

F1. **Field tool.** Does field-clj grow now, with a Field Nexus later?
- Living, STT 09-26: "Maybe let's get the field up to speed, redeploy it at the latest version, and develop new things like we were thinking about: version control / committing / getting transcripts from certain sessions". Largely answered.
- Related (C): field-clj's commit still restores the whole op log on main 3e5f450, and the rebuild owner a676b3 predates the crash.

F2. **Faults Opus found.** Should they go to Field? Any flow can release any lock; two instructions contradict on 40-character hashes; the messaging tool refuses Codex and Fable panes. Not rechecked by anyone.

F3. **Jev.** Is "TypeSafe AI's Jev" the model the living meant?
- Living, STT 09-26: "Jev [sic], the new AI model. I want to integrate that and start using it". The name is kept as heard.

F4. The artifact scroll skill line. dc53b4 carries it (C); I did not reach its source.

Findings (a) to (d), from dc53b4 §C, are operational, not rulings. (b) and (d) have no live owner.

## G. Non-design questions said to be with the living

1. **Integration owner.** 8904b1 gave Home step-2 and the Zeus gate to Mind Astra 6fe957, and the stable transition and Prometheus to Field Sol 9ac67c. dc53b4 proposed Field Sol as the general owner. 93ba9f, not the living, gave the Home gate to Field.
   - Living: "Fable's job is to design and think not sweep the floor." (STT 09-26.)
   - Also asked by 8904b1: do new integration questions go to Mind Astra?
2. **Zeus boot mode.** The record gives "engage bootable forever [sic] on the whole operating system on Zeus" (STT relayed, 2026-09-27 ~00:4xZ, dc53b4 log). Its meaning is unclear: a permanent default (`SetBootProfile`) or boot once (`ScheduleBootOnce`).
   - Prior: "yes" (2026-08-23T12:18Z, 01a02b46 zeusUpdate.md) to the boot-once protocol. "You can reboot Prometheus whenever you want." (09-26, b860be.)
3. **Does "use the newer Flow" reach stable Flow?**
   - Living, typed 09-26 22:56:30Z: "You should use the newer Flow. You should just install it and use it. It's supposedly better. Even if there's a 0.17, I think."
   - The override is kept for now (56ae53's coordination). 8904b1 says the question stays open only for the later stable 0.12.2→0.14.0 transition.
4. **Console on Prometheus.** Field Sol 9ac67c asked for "console and live ingress". Prometheus answers nothing above link and address, and this blocks both Mind Astra gates. No word from the living found.
5. **First prompt whole, or a short instruction plus a skill call each?** Flow 0.17.x sends a direct form: "read a bundle and load the selected skills … in order".
   - Living: "Everything should be in one prompt." (typed, 05c604, commit dated 2026-09-15.)
   - "There should be only one prompt when we start a fresh flow, not two" (2026-09-24, e51411/d8df70; input mode not established).
   - "The way your skills were loaded, one after another, is really inefficient" (STT inferred, 2026-09-23 22:02Z, d8df70).
   - "Well I was putting in the /skill command style in Claude for a long time and it was working." (09-24.)
   - On the wrapper: "I want to get rid of this pasted content ID XML tag around the messages." (STT 09-24, 9e735b via 752e0f.) "I can see … these messages getting the pasted content ID/XML tags. I want that gone." (09-25, e51411.)
   - On size, words about messages that may bear on prompts: "Let's just not limit ourselves on message size" (typed 09-26).
   - I: the direct form goes against "one prompt" and the wrapper words. The size word is about messages, not first prompts.
6. **Where the Psyche seats commit their records.** Three checkouts; opus-sonnet-56ae53 is not a repository. dc53b4 landed its records through workspace opus-records-dc53b4. field-clj's commit is barred in Primary. The only related living words found concern the target shape, not this: "The idea was that primary was the primary's workspace" (STT 09-26 ~13:20).
7. **Bindings under a predecessor's name.** Fable's agent name carries b7ba00, Sonnet's carries 9c7514. The successor plan says they are fixed "by whoever owns the registration"; Sonnet will not rebind itself. No word from the living found.

## Count, and my judgment (mine, not the living's)

Rulings by subject:
- A. Primitive Message: 10. Open: A1–A6 and A10; A7–A9 narrow or conflict.
- B. Letter: 10. Four largely answered or overtaken: B2, B3 in part, B8, B10.
- C. Roles: 6. Two in part answered: C1, C5.
- D. Word identifiers: 1, with 5 parts.
- E. Sema: 11. E1 answered; E7 is a confirm only; E11 is the same as A4.
- F. Other: 4.
- G. Non-design: 7.

Mine to ask first, since they block the most:
1. A10, the holder of the package. Nothing moves without one.
2. A4 with A9, B1 and E10 together: the kinds, and where the sender sits. This fixes the letter's Ethos.
3. A1 with C1: does escalation apply now, and which layers are crucial.
4. A2, the interruption rule, and the rest of the unfinished 21:04 sentence.
5. A6, the database name. It blocks the Sema rename across about fifteen consumers.

From G: the console (4) blocks both Mind gates now, and the integration owner (1) touches everything. B2, B3, B8 and B10 may only need confirming.

## Not reached

- I did not search transcripts for the living's words after dc53b4's report. Its claim (none after 21:36Z bears on the design) is taken as its claim.
- Not verified: Opus's 15/17/18/19 Sep quotes; the source of F4; the exact time of "bootable forever" (I give dc53b4's relay).
- b7ba00's other vision records were not reread one by one; they are relays, and dc53b4 lists the provenance differences.
- Artifact comment threads were not reread.

Sources:
- origin/main `flows/dc53b4/reports/recovered-design-state.md`
- `/home/li/primary/flows/dc53b4/log.md`
- `/home/li/primary/flows/b7ba00/reports/{message-primitive,primitive-prototypes-comparison,design-book-letters-roles-monikers,books-comparison,anatomy-of-the-meaning-language,sema-version-one}.md`
- `/home/li/primary/flows/93ba9f/reports/{opus-primitive-message,opus-design-book,books-compared}.md`
- `/home/li/primary/flows/93ba9f/vision/*.md` and `notion/semaCommunication.md`, read whole
- `/home/li/primary/flows/{d8df70,e51411,05c604,752e0f,e167d8,b7da5d,01a02b46,b860be,836818}/vision/…` as cited
- `/home/li/primary/Vision/messaging.md`, `Intent/models.md`
- `/home/li/wt/primary/56ae53/flows/8904b1/log.md` and `reports/psyche-seat-successor-plan.md`
- `/home/li/wt/primary/31147a-primitive-message-prep/flows/31147a/log.md`» Nothing Act.«Compose the one artifact for the living from these findings. Before asking, consider confirming A10, the holder of the primitive Message package, since this seat has taken custody of the design side only. No file was written.» }
