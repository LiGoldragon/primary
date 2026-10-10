# Two design books compared — Fable b7ba00 and Opus 93ba9f

Subflow of Fable b7ba00, 2026-09-26. Fable = `flows/b7ba00/reports/design-book-letters-roles-monikers.md`. Opus = `flows/93ba9f/reports/opus-design-book.md` (read from `main`). Drafts = Opus's `letter-anatomy-2.md` (98f8df482) and `roles-anatomy-2.md` (b86fcae04). Records dated 09-26 are the newest; 09-15 identifier dates are the commit dates of their files (inference: the records carry no date inside). Marks: **O** observation, **I** inference, **U** unknown.

## 1. Sender
- Living: "The message has to be able to figure out who the sender is programmatically eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc." and "the sender being called "owner" is fucking ridiculous" (b7ba00/vision/messaging.md, 09-26); "We could make a set of all of them and variants." (same, 09-26); "It knows which pane the call came from so we can use the database to know the aspect and the model." (e51411/vision/messaging.md, 09-25); "the two enums, aspect and model, from the database, stand" (e51411/notion/message.md, 09-25, the recorder's summary of "I changed my mind").
- Fable: `Sender.[ Living Seat.Seat ]`, `Seat.[ Psyche.Layer Mind.Layer Field.Layer ]`; the caller names it for now, derived later. Seat type coincides with the roles draft; `Living` and "caller names it" are not in the draft (the letter draft stamped it: "the caller never writes it").
- Opus: `Letter.{ Seat Content }`; the caller never writes it, Message stamps it from the process's bound seat; "The living is never a sender": the living's words are plain text, not datom.
- Closer: Opus, on derivation, matches 09-25 "which pane the call came from". Whether the living is a sender is a **conflict**. Fable reads "owner is ridiculous" as a rename. Opus reads 09-25 "differentiation from real Psyche input messages, which are not in EDN syntax" (e51411) as no sender variant at all. I: the 09-26 words object to the name "owner" and do not settle whether the variant exists.
- O: both take a seat (aspect × layer) as the sender. The 09-25 record takes aspect × model. Neither book names that older record.

## 2. Message id and history
- Living: "We shouldn't get the message ID. We're going to develop a different kind of interface to get message history. We're not going to get by message ID" (b7ba00 messaging, 09-26).
- Fable: no id anywhere. `History.[ Last.Int Since.Age Between.{ Seat Seat } From.Sender ]`. Removing the id coincides with the draft. The typed History is not in the draft (the draft said "designed later").
- Opus: no id. History is asked for by what a flow knows ("my last letters to Field Sol"), written in prose, with no type. A successor knows what its predecessor sent (cited 19 Sep, not in this record set, **U**).
- Closer: they are equivalent on the id. Fable goes further with a typed History. O: `Between.{ Seat Seat }` cannot name the living.

## 3. Psyche as content: short, full, source
- Living: "You should have, at the top level, even a psyche … it maybe even has an inner variant for the verbatim, like speech-to-text or if we know or unknown … The full psyche with the date and stuff / The short psyche, which is the context … Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there … Let's just put it in as we need it." (b7ba00 messaging, 09-26); "first is the context and then the verbatim" (e51411, 09-25); speech-to-text errors are corrected before a psyche travels, and "do we put square brackets around the part that was corrected" (e51411, 09-25).
- Fable: short `Psyche.{ Context Verbatim Source }`; full `PsycheRecord.{ Psyche Moment Heard Topic }`; `Source.[ Stt Typed Unknown ]`. Fork 1: corrections stay inside the verbatim in brackets. Not in draft (the draft had a bare `Psyche.{ PsycheContext PsycheVerbatim }`).
- Opus: short `Psyche.{ Context Verbatim }`; full `FullPsyche.{ Context Verbatim Source Age Seat }`; `Source.[ SpeechToText Typed Unknown ]`. Silent on corrections.
- Closer: Fable on "the date" (Moment). Fable's Source is nearer an "inner variant for the verbatim", because it sits with the verbatim in the short form. Opus's name "FullPsyche" is nearer "the full psyche". Both diverge in one way: neither ties Source *into* Verbatim as its variant; both make it a sibling field. Only Fable answers the bracket-correction question.
- O: Opus uses `Source` for two different types (psyche capture, and role prompt source), a name collision.

## 4. Age and time
- Living: "an LLM-readable but more human-friendly time measure, like age … seconds, minutes, hours, days, and months and years" (b7ba00, 09-26); "We don't need this huge timestamp. I don't even know why we are doing the timestamp." (e51411, 09-25).
- Fable: `Age.[ Seconds … Years ]` in `Full` and on the pane; `Moment.{ Date Time }` kept in `Full` and `PsycheRecord`. Not in draft.
- Opus: the same `Age`, only in `FullPsyche`; rule 2 is "No IDs, no timestamps".
- Closer: they are equivalent on Age. On Moment, Fable follows "full psyche with the date" (09-26) and Opus follows "don't need this huge timestamp" (09-25). **Tension in the records**, see the closing list.

## 5. Message kinds
- Living: "An order / A question / A request for an audit / A request for some information" (b7ba00, 09-26).
- Fable: those four; Fork 3 proposes `Report` and `Answer`. Not in draft (the letter draft asked "what other kinds").
- Opus: those four plus `Report` in the type (marked proposed); Question 2.
- Closer: they are equivalent on the four. Both diverge by one or two additions, which the living has not named. Opus writes Report into the type before the ruling; Fable keeps it as a fork.

## 6. Simple vs full
- Living: "maybe we even have the soft message, the soft psyche. These are shorthand … Simple is better: A simple message, a simple psyche / A full message that can have many fields, one of which is a vector of psyches that are essentially the support" (b7ba00, 09-26); "A lot of this data … belongs in the data portion of a variant" (b7ba00 flowAnatomy, 09-26).
- Fable: `Simple.{ Sender Kind Text }`, `Full.{ Sender Kind Text Vector<Psyche> Age Moment }`, `Letter.[ Simple Full Psyche PsycheRecord ]`, `Delivery.[ Soft.Letter … ]`. The tier as outer head coincides with the draft; `Vector<Psyche>` echoes the draft's `Psyches`.
- Opus: `Message.{ Kind Text }`, `FullMessage.{ Kind Text Vector<Psyche> }`, `Content.[ Message Psyche FullMessage FullPsyche ]`, `Letter.{ Seat Content }`, `Delivery.[ … ]`. Rendered as `Soft.{ Psyche.Primary Message.{ Question «…» } }`.
- Closer: Opus. Its variant names are the living's nouns (message, psyche, full message, full psyche), and "soft message" reads directly off its form. Fable's `Soft.Simple` loses "message". O: a psyche letter in Fable (`Letter.Psyche`) carries no sender. Opus carries the sender once, outside the content.

## 7. Display, shorthand, and responses
- Living: "we create a shorthand version which has a shorthand response type or display type" (b7ba00, 09-26); "not necessarily a short response but a human response. You have this human prefix and then you create these human variant responses. You have the not-human but simple. Simple is better" (same); "the differentiation from real Psyche input messages, which are not in EDN syntax" (e51411, 09-25).
- Fable: a display type chosen by the reader's harness, in two renderings, human (`PsychePrimary · Order · 3m` plus the text) and machine. Fork 4 proposes human by default on every pane. Not in draft.
- Opus: every operation replies in three registers, Simple (a single variant, the default), Human (one sentence), and Full (only on request). Letters stay datom on panes.
- Closer: Opus. "Simple is better" and "response type" point at replies, and Opus types them. Fable's display type answers "display type" but not "response type". I: a human rendering on flow panes would erase the mark that sets the living's plain-text input apart (e51411 09-25; Opus cites 18 Sep, **U**). This is a **conflict**.

## 8. Tiers and raw send
- Living: "A raw flow send … should be a meta socket operation and then we have a more lock-enabled deliver message. Maybe that is a safer operation for messages to use." (b7ba00, 09-26); "You're all allowed to bypass failing messages and send each other straight into your panes." (e51411, 09-24).
- Fable: raw send is a Flow meta-socket operation, and messages use the locked `Deliver`. Not in draft.
- Opus: the locked `Deliver` and `Command` already exist on the rebuild, and a raw operation for the privileged socket is suggested. Adds the tier semantics (Soft waits for rest, MiddleAbrupt lands at the next tool call, HardAbrupt interrupts; cited 17 Sep, **U**).
- Closer: equivalent. Neither book says whether the 09-24 pane-bypass fallback survives 09-26.

## 9. Receipts
- Living: "The message returned for the caller will say what happened" (d8df70, 09-24). There are no other receipt words in this set.
- Fable: grades `Submitted … Read` stay in signal-message and return to the sender's call and to History, never to the pane. Not in draft.
- Opus: replies as Simple variants (`Delivered`, `Parked`, `Held.RecipientWorking`, `Refused.ComposerOccupied`); "The read witness is the recipient's reply."
- Closer: both agree with d8df70. They **diverge**: Opus's "read witness is the reply" may retire the `Read` grade, which Fable keeps (**I**).

## 10. Undeliverable letters, escalation, the quiet channel
- Living: "If a message can't be delivered, then we try a higher power … if there's nothing higher then we try lower … we can start a flow if it's missing … All the medium and high flows are considered crucial." (d8df70, 09-24).
- Fable: omitted.
- Opus: covers it (the higher seat of the same aspect, then the lower; crucial seats are started). Adds a quiet channel for small information such as quota, and replies routed to a successor (19 Sep, **U**).
- Closer: Opus. Fable is silent. I: "medium and high" is the older power vocabulary; mapped to the layers, it needs a ruling on which layers are crucial.

## 11. Layer vocabulary
- Living: "it's primary, secondary, tertiary, quaternary. That's the vocabulary I was actually looking for." (e167d8 layerVocabulary, 09-26 ~13:10); "I don't see the primary, secondary, tertiary part … It's like you didn't integrate our vocabulary change." (b7ba00 flowAnatomy, 09-26); "3 power levels for each of the 3 aspects: high, medium, low … If we need ultra-low roles, they're usually temporary" (e167d8 roles, 09-26, typed).
- Fable: four layer words. Fork 2 names the three-versus-four tension and puts Quaternary under "a roster question". Coincides with draft.
- Opus: four layer words, with `Field.Quaternary Luna.Low` in the roster example. Silent on the tension.
- Closer: equivalent types. Only Fable surfaces the conflict.

## 12. Effort and model
- Living: "there are different effort levels for different models so it's a property, the data of the model variant" (b7ba00 flowAnatomy, 09-26); "the low power as Luna at high effort or the ultra-low as Luna at light" (e167d8 roles, 09-26); "It's just the default, which is medium, but datom is explicit." (e167d8 roles, 09-26 ~14:35).
- Fable: `Effort.[ Low Medium High ]`, `Model.[ Fable.Effort … Luna.Effort ]`. The shape coincides with the draft; dropping `Xhigh` is not in the draft. O: "each model carries its own scale" is asserted, but one shared `Effort` is typed.
- Opus: `Effort.[ Low Medium High Xhigh ]` (from the Curriculum models list, per the draft), with the same Model shape.
- Closer: equivalent on the shape. Both diverge on the scale: the living's word "light" is in neither, and only the draft keeps a per-model scale open.

## 13. Harness
- Living: "I don't know if we need to specify the harness unless we use more than one harness for the same model. For now we don't but I guess you can put it in." (b7ba00 flowAnatomy, 09-26).
- Fable: derived from the model; Fork 5. Opus: not written (the draft says so; the book is silent). Coincides with draft. The two are equivalent.

## 14. Role, roster, addendum
- Living: "We should have a list of flows all programmed with their datom configuration … plus addendum things that are added into the prompt from files, I guess, or from a certain reference in mind … Different variants" (b7ba00 modelFlows, 09-26); "You just start the same old premade templates, like: the psyche fable / the psyche / the psyche primary / … quaternary" (e167d8 roles, 09-26 ~14:35); "Psyche Fable and Psyche High are synonymous for now, right? If there's a new model that replaces Fable, then Psyche High would route to someone else." (b81560/vision/operational-herderMessagingReport.md, 09-19).
- Fable: `Addendum.[ File Vision Skill Mind ]`, `Role.{ Seat Model Vector<Addendum> }`, `Roster.Vector<Role>`. Fork 6: Fable is the Primary seat's model. Fork 7: the roster is a datom file over Ethos types. Coincides with draft (Source renamed Addendum; Fork 6 was the draft's Question 1).
- Opus: `Role.{ Seat Model Vector<Model> Vector<Source> }`, which adds the models a role may launch as subflows. Fable is a model, citing the 09-19 words. Not in either draft.
- Closer: Fable on the name (the living's "addendum") and on "list … with their datom configuration" as data. Opus's subflow-model vector is its own addition, with no words behind it in this set. Both answer Fork 6 the same way. The 09-26 template list, which names "the psyche fable" and "the psyche" apart from the four layers, still stands against that answer.

## 15. Launch guards, refresh, reap
- Living: "somebody launched too many flows that were on the same role and then launched the flow with too high an effort … let's make sure the code makes sure it doesn't happen again" and "Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped" (b7ba00 modelFlows, 09-26); "she doesn't have the authority to decide. She has the authority to do it once she's told" (same); "Nothing is up to me. Everything is being automated … Let's just teach the system to close panes" (same).
- Fable: `Launch.{ Role Predecessor }`, `LaunchRejected.[ UnknownRole SeatOccupied.FlowId EffortUndeclared ]`; Field executes and does not decide. One seat per flow coincides with the draft; the typed rejections and Predecessor are not in the draft.
- Opus: refuses a second live flow on a seat and any model or effort outside the roster; replacing stops the old flow first; a refresh reaps its ancestor.
- Closer: equivalent. Both diverge the same way. Neither says what detects a "big context" or an "abandoned" flow, or who decides when "everything is automated" and Field may not decide.

## 16. Word identifiers
- Living: "a series of words, maybe two or three words, depending on how much entropy … a PascalCase series of words … Let's come up with a name for this if somebody hasn't … There's a converter that can use this in field and all our tools would support it … We know which part of the hash we're using that's random, right?" (b7ba00 wordIds, 09-26); "BIP39. Is there a newer one that has more bit density?" and "camel case could be easily recognized as probably a hash" (05c604, 09-15); "three different levels of security in terms of how bad a collision is" and "a UTF-8 base for hashes" (692df8, 09-15); "Let's do the name-based hash thing in the signal library. Give it a sensible name" (fd0f97, 09-15).
- Name: Fable proposes "Moniker". Opus lists Wordprint, Saybits, Mnemonid, Tokenword, and Hashspeak, and notes "Monikers". Opus observes an existing unmerged build (`LocalNameReference` and the rest), which answers "if somebody hasn't". Fable omits the build.
- List size: Fable wants 4096 words (12 bits each), keeping only single-token words. Opus wants 1024 (10 bits) and reports only about 1024 capitalized single-token words survive vetting. **Conflict.** If Opus's count holds, Fable's list cannot be filled (**U**, not checked here).
- Width: Fable uses 2 words (24 bits) for a flow, 3 (36) for a commit or transcript, and keeps secure ids as hashes. Opus uses 3/6/12 words for local, cluster, and public, and gives flows 3 words (30 bits). Closer to 692df8: Opus, with three collision levels. Closer to "two or three words": Fable.
- Case: Fable uses PascalCase (09-26). Opus uses camelCase (09-15, and the build). Closer: Fable, to the newest words. **Tension in the records.**
- Tokens: Fable measures six hex at 3.5 tokens and two words at 3.8 (Llama-3 BPE). Opus measures six hex at 4.3, up to 7, and three words at exactly 3 (tokenizer **U**). The measurements disagree, and neither uses a Claude or Codex tokenizer (**I**).
- Converter: Fable puts it in the signal library and has every tool accept either form. Opus puts it in the field tool. Each follows one record (fd0f97 09-15 vs wordIds 09-26). I: the two can coexist, a library in signal and a CLI in field.
- The random part: Fable takes the first 24 or 36 bits. Opus notes message ids are a clock and lock ids a counter, so "almost nothing … is really a hash". Only Opus flags that non-hash ids break "the random part".
- Neither book addresses the 692df8 "UTF-8 base" or "alpha-numeric … with symbols".

## 17. Covered by one book only
- Opus only: the field tool (section 6; the living's `designBook.md` 09-26 asks for "version control / committing / getting transcripts"), and found faults (any flow can release any lock; the 40-character hash contradiction; the messaging tool refusing Codex and Fable panes).
- Fable only: the token measurement, the full migration list against the Ethos ("nothing kept for compatibility"), and History, LaunchRejected, and Predecessor as types.
- Both omit: the 800-character psyche split and "allow big message size" (e51411 09-25); "models should refrain from talking to the primary models … a preparation ritual" (b7ba00 reachingTheLiving 09-26); "Fable's job is to design and think" (b7ba00 fableRole 09-26); the single-datom-call tool notion (e51411 notion 09-25).

## (1) Conflicts the living must rule on
1. Is the living a sender variant (Fable, `Living`) or marked only by non-datom text (Opus)?
2. Is the sender named by the caller for now (Fable) or always stamped from the calling process (Opus)?
3. Content naming: `Simple/Full/Psyche/PsycheRecord` (Fable) or `Message/FullMessage/Psyche/FullPsyche` (Opus). Also, where do Source, Moment/Age, and Heard/Seat sit?
4. Pane form: human rendering by default (Fable) or datom letters with Simple/Human/Full reply registers (Opus).
5. Receipts: keep the grades through `Read` (Fable) or let the recipient's reply be the read witness (Opus)?
6. Effort scale: `Low Medium High` (Fable) or `+Xhigh` (Opus); and "light".
7. Role: subflow models as `Vector<Model>` (Opus only). Prompt source named Addendum (Fable) or Source (Opus).
8. Word ids: name; list size 4096 vs 1024; widths 2/3 vs 3/6/12; PascalCase vs camelCase; merge the existing build (Opus) or write it anew (Fable, by omission); converter in signal or in field.

## (2) Agreed; distillation can proceed
No message id, and history by who and when. `Seat.[ Psyche.Layer Mind.Layer Field.Layer ]` with Primary through Quaternary. Owner is gone. The tier is the outer head, `Delivery.[ HardAbrupt Soft MiddleAbrupt ]` over the letter. The psyche is top-level, in a short and a full form, with capture Source `[ SpeechToText/Stt Typed Unknown ]`. `Age.[ Seconds … Years ]`. The four kinds are the living's own; a fifth needs a ruling. A full message carries `Vector<Psyche>`. Effort is the model variant's data. The harness is derived, not written. `Roster.Vector<Role>` with Seat, Model, and prompt additions as variants (File, Vision, Skill, Mind). Fable is a model, not a seat. One live flow per seat; launches outside the roster, or at an undeclared effort, are refused. Raw pane send is a privileged meta-socket operation beside the locked Deliver. Words replace hashes; the hash stays authoritative; there is one converter.

## (3) Tensions inside the records that neither book may silently resolve
- Sender as aspect × model (e51411 notion, 09-25) vs aspect × layer (b7ba00 messaging, 09-26). Both books take the newer; the older is not discarded.
- "3 power levels … high, medium, low; ultra-low … temporary" (e167d8 roles, 09-26) vs four layer words (e167d8 layerVocabulary, 09-26 ~13:10). Only Fable names this.
- Premade templates "the psyche fable / the psyche" beside the layers (e167d8 roles, 09-26) vs "Psyche Fable and Psyche High are synonymous" (b81560, 09-19). Both books silently side with the 09-19 words.
- "Luna at high effort" for the low seat (e167d8 roles, 09-26) vs the medium default and pre-approved high (same file, ~14:35). The tension was flagged by b7da5d.
- "full psyche with the date" (09-26) vs "don't need this huge timestamp" (09-25), which spoke about a message.
- Pane bypass as fallback (e51411, 09-24) vs raw send as a meta-socket operation (b7ba00, 09-26).
- camelCase for ids (05c604, 09-15) vs a PascalCase series (wordIds, 09-26).
- The converter in the signal library (fd0f97, 09-15) vs "a converter … in field" (wordIds, 09-26).
- "Everything is being automated" vs "Field Luna … doesn't have the authority to decide" (both modelFlows, 09-26). The decider of refresh and reap is unnamed.
- "Medium and high flows are crucial" (d8df70, 09-24) is in the old power words and has no mapping onto the layers.

## Sources
- `flows/b7ba00/reports/design-book-letters-roles-monikers.md` (working tree)
- `flows/93ba9f/reports/opus-design-book.md` (`jj file show -r main`)
- `flows/93ba9f/reports/letter-anatomy-2.md` @98f8df482; `roles-anatomy-2.md` @b86fcae04
- `flows/b7ba00/vision/*.md`; `flows/e167d8/vision/{roles,layerVocabulary}.md`; `flows/e51411/vision/messaging.md`; `flows/e51411/notion/message.md`; `flows/d8df70/vision/messaging.md`; `flows/{05c604,692df8,fd0f97}/vision/identifiers.md`
- `flows/b81560/vision/operational-herderMessagingReport.md`: located to source Opus's quote "Psyche Fable and Psyche High are synonymous". Opus's 15, 17, 18, and 19 Sep quotes otherwise come from outside this record set and are unverified here.
