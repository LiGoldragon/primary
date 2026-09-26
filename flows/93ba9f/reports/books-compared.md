# The two design books compared with the living's words

**Sources.** Opus's book and today's 93ba9f vision are not in /home/li/primary. They are only in `/home/li/wt/primary/93ba9f/flows/93ba9f/` (reports/opus-design-book.md, vision/*.md). Fable's book is at `/home/li/primary/flows/b7ba00/reports/design-book-letters-roles-monikers.md`. Its sources are `flows/b7ba00/vision/*`, which are relays of 93ba9f's records.

**The books do not agree independently on the parts that matter.** Fable saw 93ba9f's drafts before it wrote. Where they match on the sender as a seat, no message ID, a vector of psyches, and Seat / Model-carrying-Effort / Role / Roster, the agreement shows two books following one source. It is not confirmation.

## 1. The letter

**Priority as the outer head.** Both books agree, and so does distilled `Vision/messaging.md` ("Priority is a head on the datom"). Settled.

**No message ID; history is its own interface.** Both books agree, though not independently. The living: "We shouldn't get the message ID. We're going to develop a different kind of interface to get message history" (STT, 09-26, 93ba9f). Fable already types `History.[ Last Since Between From ]`. The living said history would be designed later, so that type goes beyond the record. Opus leaves it as prose, which fits the record better.

**Who the sender is.** This is the biggest split.
- Opus: the sender is always a seat, and "The living is never a sender."
- Fable: `Sender.[ Living Seat.Seat ]`.

The older records support Opus:
- "the agents will know that it's me because of how the message is formatted. It won't be datom-formatted" (09-18, c7128c).
- "the differentiation from real Psyche input messages, which are not in EDN syntax" (09-25, e51411).

Today's words point the other way: "Nothing is up to me … The user interface is going to be Unity" (STT, 09-26, 93ba9f). Once Unity is the interface, the living's words come in through the machinery, and "not datom" may stop working as the mark. That conflict belongs to the living.

**Who writes the sender.** The living, 09-26: "eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc." Fable follows the "for now": the caller names the seat. Opus has Message stamp it from the calling process now. Opus has support from 09-25: "It knows which pane the call came from so we can use the database to know the aspect and the model" (e51411). The records conflict on timing: derivable now (09-25) or eventually (09-26).

**The four content forms.** The living named them: "A simple message, a simple psyche … A full message … The full psyche with the date and stuff" (09-26).
- Opus follows those names: `Message`, `Psyche`, `FullMessage`, `FullPsyche`.
- Fable renames them `Simple`, `Full`, `Psyche`, `PsycheRecord`, which drifts from the living's words.
- Fable has a structural hole. The sender sits inside `Simple` and `Full`, so a `Letter.Psyche` has no sender at all.
- Opus's letter is `Letter.{ Seat Content }`, and every variant has a sender.

Opus is better supported here.

**The short psyche.** The living said the short psyche is "the context", then hedged: "Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there." They also said a psyche "maybe even has an inner variant for the verbatim, like speech-to-text or if we know or unknown."
- Fable puts `Source` in the short psyche, which follows "inner variant for the verbatim".
- Opus keeps `Source` for the full psyche only.
- Neither book tests the literal reading, that the short psyche carries only the context. Both keep Context and Verbatim, as 09-25 did ("first is the context and then the verbatim", e51411).

This needs a ruling.

**Age and date.** Fable follows "the full psyche with the date and stuff": `PsycheRecord` carries a `Moment`. Opus's `FullPsyche` has an Age and no date, which departs from 09-26. Fable's `Full` message, though, carries both Age and Moment. That puts back the timestamp the living attacked on 09-25: "This timestamp is fucking huge … I don't even know why we are doing the timestamp" (e51411). The records conflict: a date in the full psyche (09-26) against no timestamps (09-25).

**Message kinds.** Both books keep the living's four. Opus adds `Report`; Fable adds `Report` and `Answer`. The living named neither.

**Reply registers.** The living: "a human response … human variant responses. You have the not-human but simple. Simple is better."
- Opus: replies come as Simple, Human or Full, and Simple is the default. This matches.
- Fable reads "human" as how panes display messages and proposes the human rendering by default on every pane (Fork 4). That goes against "Simple is better". It also goes against distilled Vision ("A message is a datom, and it arrives as one") and against the 09-18 and 09-25 rule that the machine format is what tells a machine message from the living's words.

Opus is better supported.

**Raw send.** Both books agree: raw typing is a meta-socket operation and ordinary messages go through a locked deliver. This is backed by 09-21 ("raw is on meta, so it's not usually accessible", 1b8ac0) and 09-26 (93ba9f).

**Only in Opus.** Escalation (09-24, d8df70), replies following a successor, and a quiet channel. These are grounded in earlier records, and Fable omits them.

**Only in Fable.** STT correction marks stay inside the verbatim. This matches "we just put the correction in … square brackets" (09-25, e51411).

**Where neither book follows the living.**
- Both use `Psyche` as the name of an aspect (`Seat.Psyche`) and of a content variant. Opus's pane example `Soft.{ Psyche.Primary Psyche.{…} }` shows how ambiguous that reads.
- Neither book deals with the psyche message size rule. 09-25 said split at 800 characters (e51411). 09-26 said "I want that removed from everything" (e167d8). The newer word is an explicit correction, so it stands, but it should be written into the letter's anatomy.

## 2. Roles

**Where they agree, not independently.** Effort is carried by the model variant, the harness is derived rather than written, the layers are Primary through Quaternary, a launch is refused for a second live flow on a seat or an undeclared effort, and high effort is not forbidden, only undeclared.

**Effort values.** Opus has `Low Medium High Xhigh`, taken from Curriculum's datom. Fable has `Low Medium High`. The living, 09-26: "there are different effort levels for different models so it's a property, the data of the model variant." Both books still use one shared `Effort` enum for every model, so neither follows "different effort levels for different models". Two more records bear on this:
- Intent (distilled): effort "is never raised to buy quality."
- e167d8, 09-26: "Luna at high effort or the ultra-low as Luna at light". The Field already flagged this against Intent.

**Harness.** The living: "I guess you can put it in." Both books leave it out. Fable at least surfaces it (Fork 5).

**Addendum or Source.** The living said "addendum things … (different sources). Different variants." Fable's name, `Addendum`, is the living's own word. Opus's `Source` also collides with the psyche's `Source` (STT, Typed, Unknown). Fable is better here.

**Which models a role may launch.** Opus's `Role` carries `Vector<Model>` for the subflows it may start. Distilled `Vision/modelRoles.md` supports this: "Each tier has a ceiling on what subflows it may launch." Fable's `Role` has no such field. Opus is better here.

**Is the layer vocabulary settled?** Only Fable surfaces the conflict (Fork 2). Opus is silent. The records disagree:
- "3 power levels for each of the 3 aspects: high, medium, low … ultra-low roles are usually temporary" (typed, 09-26, e167d8/roles).
- "primary, secondary, tertiary, quaternary" (STT, 09-26 ~13:10, e167d8/layerVocabulary).
- Distilled Vision still has "High, Medium, Low, and Ultra Low".
- Intent separates tier words from effort words.

**Is Fable a seat or the primary seat's model?** Both books choose the model. Fable surfaces the question (Fork 6). Opus asserts it with "Psyche Fable and Psyche High are synonymous for now" (09-19, b81560). That record uses the old High/Medium words, which do not map to Primary. It also sits against the newer template list: "the psyche fable, the psyche, the psyche primary … quaternary" (09-26 ~14:35, e167d8), which names Fable next to the four layers. It is unresolved.

**Is the roster a datom file or Ethos?** This is Fable's Fork 7: types in Ethos, and the roster as a datom file "the living edits". Two records cut against it:
- "I'm not going to … type anything anywhere ever" (09-26).
- Distilled Vision: the model is "declared once, as typed configuration in Flow, mutated only through the meta wire".

The datom-data half is supported ("a list of flows all programmed with their datom configuration", 09-26). The idea that the living edits it by hand is not.

## 3. Word identifiers

**Converter direction.** Both books agree that the hash stays the source of truth and the words are a projection of its random bits. This matches "We know which part of the hash we're using that's random, right?" (09-26).

**The name.** Fable proposes "Moniker". Opus lists candidates and does not choose. The living: "come up with a name for this if somebody hasn't." Only Opus found that a flow has already built this: `LocalNameReference`, `ClusterNameReference` and `PublicNameReference`, on an unmerged signal-library branch, in answer to "Give it a sensible name" (fd0f97). Fable missed that code. The living should know a name already exists before a new one is chosen.

**Case.** Fable uses PascalCase, which is the newest word: "a PascalCase series of words" (09-26). Opus keeps the built code's camelCase, which follows 05c604 ("camel case could be easily recognized as probably a hash"). Opus does not flag that this goes against the newer word, so here Opus fails the newest-weighted rule.

**How many words.**
- Fable uses two or three words, chosen by how much entropy the use needs. That follows 09-26: "maybe two or three words, depending on how much entropy we need for these short ID things."
- Opus uses 3, 6 or 12 words by security level. That follows 692df8: "three different levels of security in terms of how bad a collision is."
- Fable's rule that secure identifiers stay hashes covers the public level in another way.

Both books are grounded. The records differ in scope: short handles (09-26) against identifier types in general (692df8).

**The word list.**
- Fable: 4096 words, measured on a Llama-3 tokenizer. Its sources lack today's follow-up quote.
- Opus: 1024 words without homophones, each a single token in o200k and cl100k.

The living, 09-26: "BIP-39 was the one we found to be most efficient … push the density by adding the maximum number of words and also even aiming to avoid homophones." 05c604 also asked for "more bit density". Density favours Fable's 4096. "The only cost we're worried about is the LLM token cost" (692df8) favours whichever list gives more bits per token, and that measure fits Opus's single-token rule. Opus's own research found a 4096-word list whose words are each one o200k token, so the two aims may both be met. No one measured the tokenizer current Claude models use, because it is not public.

**Where the converter lives.** Opus puts it in the field tool; Fable puts it in the signal library. The records give both: "a converter that can use this in field and all our tools would support it" (09-26), and "in the signal library" (fd0f97). The library belongs in signal and field exposes it. Neither book says both.

## 4. The field tool

**Fable has no section on the field tool at all,** even though its own records include the request ("develop … version control, committing, getting transcripts", 09-26). Opus covers it: field-clj grows now, the Field Nexus is written later, with an Ethos index of calls and a separate API per harness. That fits "whichever is most ready" and "a different API also for different harnesses" (09-26, e167d8), and "redeploy it at the latest version" (09-26). Opus's book is the only one to follow the living here.

## 5. Record conflicts found along the way

- b7ba00's records mark two quotes as STT: the Ethos names comment and the raw-send comment. 93ba9f's records mark both as typed artifact comments (15:17 and 17:28). The relay changed how the words were heard, and b7ba00's copies should be corrected.
- "A message is one tag, the sender's Flow ID, and the text" (09-25, e51411) stands against "Datom doesn't have tags, has variants" (09-26). Both books follow the newer word, and the older record should carry a note.

## Rulings the living must make

1. **Sender.** Is the sender only ever one of the twelve seats, with the living's own words marked by not being datom (09-18, 09-25)? Or is `Living` a sender variant, since Unity (09-26) will bring the living's words in through the machinery?
2. **Stamping the sender.** Should Message derive the sender from the calling pane now, as 09-25 says is possible, or should the caller name its seat until that is built, as 09-26's "for now" reads?
3. **Content forms.** Four content variants named after your words (Message, Psyche, FullMessage, FullPsyche), with the sender outside them so a shared psyche also has one? Or Fable's Simple / Full / Psyche / PsycheRecord?
4. **Short psyche.** Is it context and verbatim with a Source for how the words were heard, context and verbatim only, or context alone?
5. **Time.** Does the full psyche carry a date ("the full psyche with the date"), an age, or both? May a full message carry a timestamp at all, given the 09-25 "I don't even know why we are doing the timestamp"?
6. **Kinds.** Order, Question, AuditRequest, InformationRequest: do Report and Answer join them?
7. **Replies and panes.** Do replies come as Simple, Human and Full with Simple the default, and do machine messages arrive on panes as datom, as Vision/messaging says? Or does a human rendering become the pane default?
8. **Effort.** Is effort one shared scale, and does it include Xhigh, or does each model carry its own effort type? And is "Luna at high effort / Luna at light" still meant, given Intent's "never raised to buy quality"?
9. **Layers.** Four layers, Primary through Quaternary, or three power levels plus a temporary ultra-low? How do they map onto the High/Medium/Low/UltraLow in distilled Vision?
10. **Fable.** Is "the psyche fable" the Primary seat's model, or a template of its own, next to "the psyche" and the four layers?
11. **Role fields.** Does a role carry the models it may launch as subflows (Vision's delegation ceiling)? Is the prompt material called Addendum or Source? Is the harness written ("you can put it in") or derived?
12. **Roster.** Is the roster datom data changed only through Flow's meta wire, or a file someone edits?
13. **Word identifiers.** Does the standard keep the name already built (LocalNameReference and its siblings) or take a new one (Moniker or another)? Is it PascalCase (09-26) or camelCase (05c604)? Two or three words by entropy, or 3/6/12 by security level? A 4096-word list for density, or a list judged by bits per token?
14. **Field tool.** Does field-clj grow now (safe commit, transcripts in both harnesses, one observe view), with the Field Nexus later?
