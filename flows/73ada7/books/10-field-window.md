<!-- to-the-living:start -->
Presentation.{ «When Field may answer Psyche» }

## The case

Message hands every request to Flow with its Sender, and Flow checks the route before it places the request: a request off the vision-aspects routes is refused OffRoute (flows/f5a6e9/reports/flow-buildable-design.md:213-215 and 248-252). One of those routes has an exception: Field reaches Psyche through Mind, unless Psyche has just spoken to Field. Message's design tests Field's Tertiary sending to Psyche's Primary and expects OffRoute (flows/73ada7/reports/build/message-design.md:487), but nothing says how long the exception lasts once Psyche has spoken, so Flow cannot tell when to let a Field request through to Psyche and when to send it back. Flow's design keeps a Lock and a Queue on its records and no memory of who last spoke to whom; whichever option is ruled, Flow keeps one more fact on a Field metaflow, the Psyche metaflow that last delivered to it. That is this flow's reading of what each option needs. Message and Flow as designed are in development, none of it in production.

## Distillation

### D1. How long Psyche's having spoken opens the route, in vision-aspects

Target: `psyche-skills/skills/vision-aspects.md`, the paragraph at line 8 under «Flows of one topic talk at the same layer across aspects». It stands as: Flows of the same topic talk at the same layer across aspects: Psyche sees and Mind implements, so a Psyche topic Secondary and the Mind Secondary of that topic speak directly. Field reaches Psyche through Mind, unless Psyche has just spoken to Field. This holds for every aspect. Nothing is removed; one sentence is added after "unless Psyche has just spoken to Field."

**Option (a), until Field's next reply.**

Added: Psyche has just spoken to Field until Field's next request to that Psyche metaflow; that one request goes directly, and the one after it goes through Mind.

Rests on: flows/73ada7/vision/flow.md:15 (2026-10-09, raw), the living's comment on «The new flows, as they run», on Field going through Mind and not to Psyche directly unless Psyche just spoke to it; psyche-skills/skills/vision-aspects.md:8 (in the file at 2026-10-09), where that comment landed. Message's design gives one reply as its example (flows/73ada7/reports/build/message-design.md:609-611), unruled. That keying the window to the Psyche metaflow, and not to one flow id, lets the reply reach that metaflow's successor after a refresh, as psyche-skills/skills/vision-flow.md:54-56 (in the file at 2026-10-07) has a subflow reply to the successor of whoever it was meant to answer, is this flow's reading.

**Option (b), while Psyche's request to Field is open.**

Added: Psyche has just spoken to Field while a request Psyche delivered to that Field metaflow is open; Field answers it directly as often as it needs, and once the request is closed Field goes through Mind.

Rests on: flows/73ada7/vision/flow.md:15 (2026-10-09, raw), on the exception itself; psyche-skills/skills/vision-flow.md:68-74 «The requester holds only a request ID» (in the file at 2026-10-07), on a requester holding a request ID by which it follows a subflow's work while the subflow is alive and receives a message when it is done. That a request between voices would carry the same kind of ID is this flow's inference: Flow's Deliver carries Lock, Sender and Request and no request ID (flows/f5a6e9/reports/flow-buildable-design.md:213-216), and no record says what closes a request, so this option needs both.

**Option (c), for a span held in Flow's configuration.**

Added: Psyche has just spoken to Field for a span after Psyche's last delivery to that Field metaflow; the span is held in Flow's configuration, seeded from its built-in default and changed over the meta Configure.

Rests on: flows/73ada7/vision/flow.md:15 (2026-10-09, raw), on the exception; psyche-skills/skills/vision-nexus.md:89-94 «Configuration» (in the file at 2026-10-07), on the default constant seeding a new store and changed values being accepted through the meta Configure. «How long Flow's lock lasts» asks the same question of the lock's span, unruled. That a span measures time and not whether Field has answered, so Field could answer twice within it or not at all, is this flow's inference; no record proposes a value.

**Ruling D1.** (a) Until Field's next reply. (b) While Psyche's request to Field is open. (c) For a span in Flow's configuration. (d) Amend, by line.

## Voice

One choice. Your rule lets Field answer Psyche directly when Psyche has just spoken to it, and Flow needs to know how long that lasts. A lets one reply through and sends the next one by Mind. B keeps the route open while Psyche's request to Field is open; this flow's reading is that requests between voices would then need an ID and a way to close, which nothing has yet. C keeps it open for a span in Flow's configuration, the way «How long Flow's lock lasts» asks about the lock. Which one?
<!-- to-the-living:end -->
