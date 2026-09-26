# Primitive Message — Fable vs. Opus, by point

Comparing `flows/b7ba00/reports/message-primitive.md` (Fable) and `flows/93ba9f/reports/opus-primitive-message.md` (Opus), against the living's words in `vision/messaging.md` (last two entries) and `vision/callerIdentity.md`. Both written independently, same day, same source utterance.

## 1. Kinds and payload

Living: "a very primitive version... with just a few different types of messages... just a string as the basic form... field report, psyche report, field question, psyche question." Fable: nine kinds — `FieldReport/Question`, `MindReport/Question`, `PsycheReport/Question`, `Order`, `Answer`, `PsycheUpdate.{Context Verbatim}` — one per aspect, payload `Markdown.String`. Opus: five kinds — `Report`, `Question`, `Answer`, `Order`, `PsycheUpdate.Psyche` — generic, aspect not baked into the kind name, payload also Markdown. Conflict: Fable bakes aspect into the kind (nine names); Opus keeps five kinds and reads aspect from the sender's seat at render time. Both keep the payload a plain string as the living asked. Opus is nearer the living's "few different types... simple and easy" (fewer kinds); Fable is nearer the literal examples ("field report... psyche question" as compound names).

## 2. Aspect in the kind — sender's or recipient's

Living: "if you send the message you have the same type." Fable: aspect is the sender's, explicit fork (Fork 1) with the alternative (recipient's) named but not chosen. Opus: doesn't type the aspect into the kind at all — "the kind is the same type on both ends," aspect comes from the sender's seat carried in the letter. Agreement in substance: both make the aspect track the sender, never the recipient. Difference is only mechanism (typed vs. carried-in-letter). Equivalent to the living's word.

## 3. Origin / caller identity

Living (`callerIdentity.md`): a Nexus reads the calling process, asks Flow which flow used the CLI, "It would just know... Even Flow can really benefit... 'Refresh Flow, who called it?'" Fable: `ResolveCaller.Pid → Caller.{FlowId Seat} | CallerUnknown`, stamped as `Origin.Seat`, refuses unknown callers, subflows resolve to the owning seat (Fork 3), names it "the Signal standard." Opus: same mechanism (`SO_PEERCRED` → pane → flow), names it `Origin.{FlowId Seat Model}`, proposes lifting it from Flow into shared Signal, notes a process outside any pane gets refused or the meta socket, and explicitly retires the old power words (`High Medium Low UltraLow`) in favor of `Seat`. Agreement: both stamp origin via Flow, both cite Flow's own `Refresh` as the same mechanism, both refuse unknown callers. Opus adds `Model` to the origin and the explicit retirement of power words; Fable adds the subflow-liability rule explicitly as a fork. No conflict — each covers what the other omits (Opus: Model field, power-word retirement; Fable: explicit subflow rule). Both equivalent to the living's words.

## 4. The address — "send up"

Living: "If you say 'send up' it means message higher layer... The message logic has to figure out where that's supposed to go so it can ask the flow... the message will go to the right place as long as we know where it comes from." Fable: `Bearing.[Up Down Across.Aspect Living To.Seat]`, resolved via `ResolvePeer.Seat`; if no live flow holds the seat, held and reported `NoSeat.Seat` (explicitly *not* deciding escalation now). Opus: `Toward.[Up Down Across.Aspect Seat.Seat]`, resolved via `ResolveToward.{Seat Toward}`; explicitly rules empty-seat handling — climb further up, then down, per "the living, 24 September" — and says a crucial seat is started rather than skipped. Conflict: Fable defers the no-seat/escalation behavior to a later version; Opus claims it is already ruled (cites a prior living record) and encodes climb-and-start. This is a live conflict for the living/Astra to resolve — did the 24 September ruling already settle the primitive's behavior, or is it out of scope for "primitive"? Also a naming fork: "Bearing" (Fable, with CLI kept as `send-up`/`send-down`) vs. "Toward" (Opus) — both are proposals, neither is the living's own word, so this sub-point is open. Fable also adds `Living` as a bearing (reaching the living's pane) which Opus's `Toward` does not enumerate — a gap in Opus.

## 5. Request and reply shapes

Living: no explicit shape given beyond "figure out where that's supposed to go" and (from the broader messaging thread) "very little noise... don't want all these hashes." Fable: `Send.{Bearing Letter} → Sent.{Origin Seat} | SendRejected.[CallerUnknown KindNotCallers.Aspect NoSeat.Seat RecipientUnreachable.Seat EmptyBody]`. Opus: `Send.{Toward Kind} → Sent.[Delivered.Seat Parked.Seat Refused.Refusal]`, with `Refusal.[NoSeatAbove NoSeatBelow SeatEmpty CallerUnknown]`, and the CLI-typed examples show the reply as one word plus seat. Agreement: request is one call carrying address + kind/letter; no sender field, no id, no priority in either — matching "very little noise." Conflict/difference: Fable's success reply is a single shape (`Sent`) with rejection as a separate variant; Opus's success has two live outcomes (`Delivered` vs. `Parked`) folded into one `Sent` type alongside `Refused`. Opus's three-way outcome (delivered/parked/refused) is closer to the "streamlined... shorthand response type" instruction — one word plus seat, minimal reading. Fable's is closer to the living's emphasis (elsewhere) that Message should distinguish rejection causes explicitly (`KindNotCallers.Aspect`, `EmptyBody` — gaps in Opus's `Refusal` list).

## 6. History

Living (messaging.md): "We're going to develop a different kind of interface to get message history. We're not going to get by message ID." Fable: addresses this directly — `History.[Last.Integer From.Seat Since.Age] → Letters.Vector<Stamped>`, `Stamped.{Origin Seat Moment Letter}`, no id anywhere. Opus: does not propose a history interface at all — a clear gap. Fable is nearer the living's words and is the only one of the two that covers this point.

## 7. Pane rendering

Living: "I saw one message coming from it and it had a bunch of fields in there that I don't want to see" and wants age as a human-readable measure ("seconds, minutes, hours, days"). Fable: pane shows `Kind · Origin · Age` then the body (e.g. `FieldReport · Field.Primary · 2m`), with an explicit `Age` variant type. Opus: pane shows `Kind.{Seat Body}` rendered as e.g. `Report.{ Field.Tertiary «...» }` — no age field shown or modeled. Gap in Opus: age is absent, though the living asked for it by name in the immediately preceding vision entry ("simple and full... age... seconds, minutes, hours, days, and months and years"). Fable is nearer the living's words here.

## 8. Interruption / priority

Living: "Priority leaves the letter... soft and hard was the wrong approach... The database can know it... I don't think it's going to matter [to the model]." Fable: "Whether a kind interrupts the recipient is the database's judgment per kind... the primitive version interrupts nothing." Opus: keeps a per-kind interruption table (`{PsycheUpdate MiddleAbrupt} {Order MiddleAbrupt} {Question Soft} {Report Soft} {Answer Soft}`) held in Message's database. Conflict: Opus's table still uses the Soft/MiddleAbrupt vocabulary the living called "the wrong approach" and disclaimed needing at all for the primitive; Fable drops interruption behavior entirely for this version. Fable is nearer the living's words (which say not to burden the primitive with this and that soft/hard was already rejected); this is a conflict for the living/Astra to rule — is a database-held table using retired vocabulary acceptable since it's invisible to the agent, or should it be absent until redesigned?

## 9. The database's name

Living: no direct ruling yet ("Let's figure out the name for the database part"). Fable proposes **Mnema** (alternatives Thesauros, Archeion). Opus proposes **Thesauros, Kosha, or Mnema** (Fable's own proposal), leaving it open among three. Agreement: Mnema is the one name both books surface; Opus explicitly credits it as Fable's. This is the strongest converging signal and the natural default if the living doesn't rule directly.

## 10. What each omits

Fable's explicit "deliberately absent" list: priority/tiers, message ids/acks by id, named sender, full Sema payload, escalation of undeliverable letters, non-string/non-psyche bodies. Opus has no such explicit list but in practice omits: a history interface (gap, §6), age (gap, §7), the `Living`-bearing/meta-pane case (gap, §4), and explicit rejection-cause enumeration for malformed sends (`EmptyBody`, `KindNotCallers`). Fable omits Opus's `Model` field on `Origin` and Opus's explicit power-word retirement note, and defers the empty/no-seat climb rule Opus claims is already settled (§4).

## 11. Who builds

Living (general standing instruction, both books agree): Astra designs/orchestrates, Sol implements/tests. Fable: "This prototype and 93ba9f's go to Mind Astra together; Astra reconciles them... Sol lands and tests it with a disposable seat." Opus: same division, plus a four-step build order (Signal origin standard → Flow seat/roster/ResolveToward → Message send/letter/table/reply → deploy on the Next pair, retiring messenger-clj). No conflict; Opus's version adds a concrete build sequence Fable's omits — a gap in Fable, not a disagreement.

---

## Agreed — Mind Astra can take as settled

1. Payload is a plain Markdown string; no message id, no named sender, no priority field on the letter (§1, §5).
2. Origin is stamped by Message/Flow via peer-credential resolution, never typed by the caller; unknown callers are refused; Flow's own `Refresh` uses the same lookup (§3).
3. The aspect shown to the reader ("field report," "psyche question") always tracks the sender's seat, never the recipient's (§2).
4. The address is a small closed set of directions — up, down, across-aspect, an explicit seat — resolved by Message asking Flow, not typed as a raw destination (§4).
5. **Mnema** is the converging proposal for the database's new name, with the living not having ruled (§9).
6. Astra designs/orchestrates, Sol implements/tests, both prototypes merge into one Ethos before landing (§11).

## Conflicts for the living or Astra to rule

1. Whether the primitive should already implement climb-and-start no-seat/escalation behavior (Opus, citing a 24 Sept ruling) or defer it to a later version (Fable) (§4).
2. Whether an interruption table may exist in the primitive at all, and whether it may use the Soft/MiddleAbrupt vocabulary the living called wrong, even if hidden from the agent (Opus) vs. omitting interruption entirely for now (Fable) (§8).
3. Naming: "Bearing" vs. "Toward" for the address type; kind granularity: nine aspect-named kinds (Fable) vs. five generic kinds with aspect read from the seat (Opus) (§1, §4).
4. Reply shape: single `Sent`/`SendRejected` split (Fable) vs. three-way `Delivered`/`Parked`/`Refused` (Opus) (§5).

## Gaps in both

1. Neither settles whether `Order`/`Answer` should carry an aspect (Fable's Fork 2 is open; Opus's `Order`/`Answer` are aspect-free without discussion).
2. Neither fully specifies malformed-send handling: Opus's `Refusal` list omits `EmptyBody`/wrong-aspect-for-kind; Fable doesn't enumerate `NoSeatBelow`/`SeatEmpty` separately from `NoSeat`.
3. Neither states what happens to in-flight `Parked`/held letters when a seat that was empty later fills.
