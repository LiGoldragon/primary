Presentation.{ «Nexuses» }

A Nexus is a kind of thing, not one program: the style of long-running component that speaks Signal and keeps a Sema, and every component from now on is one. Each is reached by sockets, has a stable and a next version, and owns one domain.

**1. A Nexus is a kind**
Module: vision, vision-nexus. Action: edit.
Text: "A Nexus is a kind of thing, not one program: the style of component that speaks Signal and keeps a Sema. Every component built from now on is a Nexus; what was built otherwise is rewritten."
Rests on: 9 Sep, 19 Aug.

**2. A Nexus never receives text**
Module: vision, vision-nexus. Action: edit.
Text: "A Nexus only receives Signal. Its client turns datom into Signal."
Rests on: 15 Sep.

**3. Never polls, never grows without limit**
Module: vision, vision-nexus. Action: edit.
Text: "A Nexus never polls: it is told of each change and goes quiet when nothing changes. It serves one domain; when its features grow too many, part of it splits off."
Rests on: 27 Aug.

**4. Start with no arguments**
Module: vision, vision-nexus. Action: edit.
Text: "A Nexus starts with no arguments. Its defaults are built in and saved to a new database; an existing database brings its saved settings back. Changes arrive on the meta socket."
Rests on: 26 Aug.

**5. Stable and next**
Module: vision, vision-nexus. Action: edit.
Text 1: "Each service runs a stable and a next side by side on different sockets. When every flow is on next, next becomes stable and the newer version goes onto next."
Text 2: Text 1, plus "Each version gets its own socket named from that version; stable and next only point to one."
Rests on: 26 and 30 Sep. Name 1 or 2.

**6. The core library keeps the layers apart**
Module: vision, vision-nexus. Action: edit.
Text: "The Nexus core library refuses at compile time any path from the Signal layer straight to the Sema layer. Everything passes through the Nexus layer."
Rests on: 14 Sep.

**7. Datom reaches a prompt**
Module: vision, vision-nexus. Action: edit.
Text 1: "The client or harness hook at the far end turns Signal into datom."
Text 2: "A separate datom Nexus translates for every other Nexus."
Rests on: 19 Aug, 3 Oct. Name 1 or 2.

**8. Record shapes change, the database follows**
Module: vision, vision-nexus. Action: edit.
Text 1: "Each Nexus carries its own upgrade from one record shape to the next."
Text 2: "One shared mechanism in the Nexus library upgrades every database."
Rests on: 25 Sep, 3 Oct. Name 1 or 2.

**9. Split out what each Nexus owns**
Module: vision, new name nexus-roster. Action: split from vision-nexus.
Text: "Orchestrate reserves paths. Flow launches, names and locks flows. Message carries messages between seats, drawing on Flow. Mind keeps the system's checked facts, each with a date and a trust level. Psyche keeps his words only. Horizon answers what the cluster looks like now. Transcript serves session records. Curriculum builds the skills. Field queries the system. Edit edits datom by structure."
Rests on: 25 Aug to 2 Oct, as the book quotes.

**10. Where Curriculum keeps skill text**
Module: vision, nexus-roster. Action: edit.
Text 1: "Curriculum holds only its own state, seeded from Nix; skill texts live in a separate data store."
Text 2: "Curriculum's own database holds the skill texts."
Rests on: 17 Sep. Name 1 or 2.

**11. Topics become variants**
Module: vision, nexus-roster. Action: edit.
Text: "Subjects, topics and subtopics are typed variants inside a Nexus such as Mind. A new variant is submitted, approved, added to Ethos, and the Nexus is rebuilt."
Rests on: 3 Oct.

**12. Update the running-Nexus facts**
Module: knowledge, knowledge-nexus. Action: edit.
Text: "Four Nexuses run: orchestrate 0.37.0, flow 0.23.0 and message 0.19.0 each as stable and next, and lojix 8.1.0. The older message service no longer runs. No Mind, Psyche, Horizon, Transcript, Curriculum, Field or Edit Nexus runs."
Rests on: witnessed today; the skill names older versions.
