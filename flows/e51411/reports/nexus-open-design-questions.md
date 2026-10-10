# Open design questions for the nexuses

Date: 2026-09-25. Read-only research by a subflow of Psyche Medium e51411. It follows the living's words that day: "If you need a refresh we need to go fully on finishing the design. Anything that's not clear about all of the nexuses ..." (flows/e51411/vision/nexus.md).

Method: I read the psyche first: `Vision/`, `Intent/`, `vision-raw/`, and the `flows/*/vision/` and `flows/*/notion/` records that bear on Flow, Message, Psyche, Mind, Field, persona and storage. Then I read the nexus skills, the Flow and Message reports, and the READMEs, ARCHITECTURE and DESIGN files and contract sources in `/git/github.com/LiGoldragon/`. Newer records weigh more. A question is listed only where the records disagree, stop short, or say it is unclear. Nothing here is a ruling. "Records say" gives the living's words or the code's own statements, with the short flow ID and date. "Options" lists only options that some record names.

Current system (from code; no live check was made): CriomOS-home's newest commit (04446e78, 2026-09-24) pins Flow `7cc19af` and Message `8aa6d7b`. On that line, the ordinary Flow contract has `Start`, `Restart`, `ResolveRecipient`, `Send`, `Stop` and `List`. Two more Flow contract lines are not integrated: a v3 refresh line (`fa326ac`, which has `Refresh` with handover and archive) and a v4 escalation line (`755186e`, which has `ResolveDelivery`).

---

## 1. Flow

### F1. Which contract line is Flow: Restart, or Refresh with handover and archive?
- **Example:** The deployed contract has `Restart` (a resume of the same thread, allowed only when the caller is the target) and no Refresh. The unintegrated v3 line replaces `Restart` with `Refresh`, which has handover byte selection, archive receipts and predecessor close. The v4 escalation line is built on v3. The three lines cannot all be merged as they stand, and `UPGRADES.md` says mixed v3/v4 operation is unsupported.
- **Records say:** A refreshed flow needs "a flow handover in its transcript somewhere, a recent transcript not too old" (d8df70, 2026-09-24). "The handoff is in the transcript and the tool gets it from that ... we don't need to make a copy" (e51411, recovered from 47764b, 2026-09-24). "flow is to start or refresh a flow" (da1e3f, 2026-09-17). Flows "automatically refresh" eventually (e51411, from 9ddcbc, 2026-09-24).
- **Options:** Keep `Restart` and add `Refresh` beside it, or replace it as v3 did. No record chooses.

### F2. How does the refresh lock work, and who holds messages during it?
- **Example:** When a seat is replaced, messages sent to it can land in the old pane. The living once saw Codex's reports land in a concluded predecessor's window (fd0f97, 2026-09-17).
- **Records say:** In b81560 (2026-09-19), Message blocks the old flow's inbox and outbox and "caches both sides". Flow then tells Message "this pane is stable". In d8df70 (2026-09-24), "The old seat stops receiving first. That's how we get a lock", and the old flow "just blocks until the new pane ... is ready to receive and then the old one in the same swoop". Vision/flowNexus says "A replaced session is reaped by the refresh itself".
- **Open:** Which Nexus owns the lock. Whether the old flow stops receiving before the new one starts, or in the same step. The records give both orders.

### F3. Can any flow refresh or redeploy any other, or only itself?
- **Example:** Deployed `Restart` is allowed only when the caller's Flow ID and session equal the target's (flow DESIGN.md). Under that rule a Field seat cannot refresh Psyche Medium, even though the living keeps asking Field to relaunch seats.
- **Records say:** "Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it" (d8df70, 2026-09-24). "Why can't anybody deploy anyone? ... It can respawn itself from any point" (e51411, from 00f95a, 2026-09-24). Refresh should not reawaken the old flow unless the successor fails to start (fd0f97, 2026-09-17).
- **Options:** Self-refresh only, checked by caller identity. Or anyone may refresh anyone. Or authority by role (aspect, power level). The records do not say how caller-process checks and "anybody can redeploy anyone" fit together.

### F4. What does Stop archive, where does it go, and is it searched differently?
- **Example:** Deployed `Stop` closes the pane and marks the row `Stopped`. It archives nothing. The v3 line has `ArchiveReceipt`, `ArchivePath` and `ArchiveIndexId` only inside Refresh.
- **Records say:** "Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently" (d8df70, 2026-09-24, a question the living asked and that has no answer on record). Also "an intermediary spot that at least only picks the important things" (9993b5, 2026-09-17) and "Start storing this in the mind component, in the memory ... how to let things go, how to delete" (b7da5d, 2026-09-24).
- **Options:** The archive belongs to Flow (v3), or to Mind's memory (b7da5d). No record chooses.

### F5. Is a flow container (a Herdr session) a Flow record, and how does V2 fit "one Herdr session"?
- **Example:** The contract has a `HerdrSessionName` string on each flow but no container type. The seats were once split across `messaging-build` and `default`.
- **Records say:** "It's a flow container that has many flows in it: many typed flows", and bind the container first, then its flows as one vector (d8df70, 2026-09-24). "there shouldn't be two Her[drs] sessions" (d8df70, 2026-09-24). The V2 notion asks for "another container, another flow container ... fully flow-controlled", with seats shown as "Psyche V2 Fable <id>" (e51411 notion, 2026-09-25).
- **Open:** Whether a container is its own record with its own identity and version tag. Whether V2 means a second container on the same Flow Nexus or a second Flow Nexus. How "one Herdr session" squares with a V2 container. The V2 record is a Notion.

### F6. Where does the title live, and what fields make up a launch?
- **Example:** `LaunchProfile` has aspect, power, model, effort, skills and an instruction prompt, but no title (flow-message-basics, e51411, 2026-09-24). Pane titles still carry state.
- **Records say:** "using header pane titles for storing data is like you should just use a registry ... That's what Flow's database should be" (e51411, from 5f38bc, 2026-09-24). Titles are aspect, model and Flow ID, with the version dropped (e51411, 2026-09-24). Flow composes "the first prompt and eventually ... the system prompt" (836818, 2026-09-23). Vision/flowNexus says Flow sets up the "system prompt, training files and instruction prompt".
- **Open:** Whether the title is derived from registry fields or stored. When and how the system prompt joins the launch profile.

### F7. Subflows: Flow-launched flows, or harness subagents?
- **Example:** This report was written by a harness subagent, which is the facility that Vision/flowNexus says is replaced.
- **Records say:** Vision/flowNexus (distilled, 2026-09-09) says "The harness subagent facility is replaced", with request IDs and an ultra-low Field flow routing a flow's ending questions. Later: "You're wasting your time by not using subagents", and "skills that only certain subagents can see ... For them the skill is the subagent" (e51411, from 6288d1 and 9ddcbc, 2026-09-24).
- **Open:** Whether the 2026-09-24 words give harness subagents a lasting place or a temporary one. No record retires the distilled line.

### F8. What starts a refresh automatically?
- **Example:** There is still no single call that reports the context size of every flow (b7da5d, 2026-09-25). No component watches the threshold.
- **Records say:** Refresh at 30% of context, "200,000 to 300,000 tokens" (f55ec8, 2026-09-16; b80e55, 2026-09-20). "the flows to just automatically refresh" (e51411, 2026-09-24). "without the user having to notice" (9993b5, 2026-09-17).
- **Open:** Which component measures context and fires the refresh: Flow, Field's census, or the flow itself.

### F9. How does an imported flow become deliverable?
- **Example:** Rows bound from running sessions stay `Pending` or registered-unconfirmed. The code now promotes a row to `Active` only after a `Send` whose marker is read back in the pane (flow DESIGN.md at 7cc19af). 00f95a marked the earlier `MetaConfirmExisting` unsafe.
- **Records say:** "bootstrap by hand for now", with an import tool later (d8df70, 2026-09-24). Session hooks register and unregister, and process exit is the unregister signal (d8df70, 2026-09-23).
- **Open:** Whether hooks, the import tool, or Send-promotion is the lasting path into the registry. The records name all three and rank none.

## 2. Message

### M1. Does Message deliver through Flow `Send`, or keep its own Herdr path?
- **Example:** Flow `Send` and Message's `deliver_herdr` both run `herdr agent prompt` and both check the route. That is two writers into one pane, with two receipt vocabularies.
- **Records say:** "Flow basically exposes everything from the harness, and then message makes use of it ... we can use it raw to send messages" (e51411, 2026-09-24). This is newer than "no, message, not flow-send. use the message nexus!" (da1e3f, 2026-09-17).
- **Open:** Whether Message sits on top of Flow `Send`, or Flow `Send` is only the raw fallback.

### M2. What are the delivery grades on the wire, and what proves Read?
- **Example:** The messaging skill defines Submitted, Transported, Presented, Read and Completed. Message's contract has `ReceiptKind.[Accepted ...]` and `Parked`. Flow `Send` returns `Accepted` or `Presented`. The subflow return type has no Completed.
- **Records say:** "An interrupt witness is not a delivery witness ... a submission is never a read receipt" (Vision/messaging). "a witness screenshot taken of that pane when the message goes in" (b81560, 2026-09-19).
- **Open:** One grade vocabulary across Message, Flow and the skills. What target-side event counts as Read. No record defines a read mechanism.

### M3. How long is a message held, where, and what happens when the hold ends?
- **Example:** The skill says a `Held` result is not retried: "the held attempt and its declared successor rule own later delivery". No deployed rule of that kind exists, and Message parks with no expiry.
- **Records say:** "the message can sort of be held ... We can wait a few seconds at least to see if there's a new flow" (d8df70, 2026-09-23). Process exit has "advantages ... in terms of retaining messages" (d8df70, 2026-09-23). "develop a way to receive messages while they're being changed" (b80e55, 2026-09-20).
- **Open:** How long a hold lasts. Whether the held queue lives in Message or in Flow. Whether an expired hold escalates (M4) or reports back to the sender.

### M4. Escalation when a message cannot be delivered: who does it, and with what limits?
- **Example:** The v4 `ResolveDelivery` line puts escalation in Flow, with a caller-supplied hop limit and "no default hop limit". It sits unmerged on `mind-sol-6288d1-escalation-contract`.
- **Records say:** "If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules. ... we can start a flow if it's missing ... All the medium and high flows are considered crucial" (d8df70, 2026-09-24).
- **Open:** Whether escalation belongs to Flow or to Message. The hop limit. Whether escalation may ever cross aspects: the v4 line forbids it, and the records never mention aspect. The "bunch of rules" is not written.

### M5. Fallback to a direct pane prompt: does it belong in the product?
- **Example:** testing-message-route says "Do not ... reroute, or fall back to another channel". The living has since allowed it.
- **Records say:** "You're all allowed to bypass failing messages and send each other straight into your panes. I just want you guys to be able to communicate with fallback" (e51411, 2026-09-24; its record notes "The skill line is owed").
- **Open:** Whether Message itself falls back to Flow `Send` or a pane prompt, or whether fallback stays a flow-level permission.

### M6. Priority: is it on the wire?
- **Example:** `signal-message` has no Priority type. Hard, middle and soft delivery exist only in hm-send practice.
- **Records say:** `Priority.[HardAbrupt MiddleAbrupt Soft]` is "a head on the datom" (Vision/messaging). "don't wake flows unnecessarily" (6db4fe, 2026-09-21).
- **Open:** Whether Priority is a Message record, and who may send HardAbrupt.

### M7. Which registry is authoritative while hm-send and Message both run?
- **Example:** hm-send keeps its own registry from session hooks. Flow keeps the Flow store. A seat can be routable in one and `UnknownFlow` in the other, as e51411, 00f95a and 752e0f were on 2026-09-24.
- **Records say:** Flow Nexus should "adhere to all of the discoveries" of "the hacky part of the hacky stack" (d8df70, 2026-09-23). "Why aren't we using Flow?" (d8df70, 2026-09-24).
- **Open:** When hm-send retires. Whether its registry hooks move into Flow.

## 3. Psyche Nexus

### P1. Where does the psyche live: a git repository of files, or a Nexus store?
- **Example:** Today the psyche is Markdown in Primary. Vision/psyche says psyche data belongs in a dedicated repository. The `psyche` repo is an empty "quick-new MVP" scaffold that replaces Spirit and defines no records (psyche ARCHITECTURE.md, 2026-08-14).
- **Records say:** "the psyche log is obviously going in Psyche ... it gets its own sort of mind-like component" (1a6ca4, 2026-09-05). "Use components like Psyche instead of this makeshift file system ... make everything with easy, minimal Datom object syntax" (fd0f97, 2026-09-17). "psyche data, becomes its own repo" with raw/<flow-id> plus vision, intent, spirit and notion (b05237, 33ba2b, 2026-09-18). "Psyche Nexus is going to replace how we log Psyche" (e51411, 2026-09-25).
- **Options:** A Sema store in Psyche Nexus. A git repository. Or the repository as a projection of the store. No record rules on how the two relate.

### P2. What exactly does Psyche Nexus replace: Psyche logging only, or Mind logging too?
- **Example:** If both Psyche Nexus and Mind Nexus take in Mind's records, a Mind witness has two homes.
- **Records say:** "Psyche Nexus is going to replace how we log Psyche and Mind. Mind Nexus is going to replace how we log the Mind and the field" (e51411, 2026-09-25). e51411's reading note calls "and Mind" a possible slip, unconfirmed. "This is why Psyche needs to be separate from Mind: if you're searching Psyche, you want to search all layers" (9993b5, 2026-09-17).
- **Open:** Whether "and Mind" stands. This needs the living's word.

### P3. How do the living's words enter Psyche Nexus from any seat?
- **Example:** d8df70's logging audit recovered many unlogged words from Field and Mind seats. Every record here says "input mode not established".
- **Records say:** In 5f38bc (2026-09-24), the living first proposed that every utterance be "reported to a psyche worker", then revised it in the same turn: "All Flows should log the psyche according to what they understand ... When the psyche gets relayed it doesn't get logged again". Unity "will just take all the user input and therefore mark it as such and pass it through a psyche logging Flow". "Everybody that faces the psyche should be trained in psyche" (752e0f, 2026-09-24). "we need the typed messages that are easily distinguishable from psyche-typed stuff" (33ba2b, 2026-09-18). "better just to talk to Psyche, and then Psyche dispatches" (9993b5, 2026-09-17).
- **Options:** Each facing flow writes the entry with its own context. Or code captures input (a harness hook, later Unity) and a logging flow interprets it. Or both: code capture, then flow annotation. No record names the entry call or how relays are deduplicated.

### P4. How does Psyche Nexus know which flow and which input mode an entry came from?
- **Example:** Entries carry a flow ID only because the writing agent says so. Input mode (typed, STT, comment) is usually unknown.
- **Records say:** "the reference known which Flow actually did the log from the CLI, knowing the process, and asking whatever nexus can tell it which Flow is which process? Maybe it's persona ... or maybe the Flow can know it too" (f55ec8, 2026-09-16). The caller-identity chain is kept in the CLI (9993b5, 2026-09-17). "One checks the origin process of the call" as a standard signal handshake (b05237, 2026-09-18).
- **Open:** Whether Flow or persona resolves process to flow. Whether the handshake carries input mode.

### P5. Retrieval and injection: who selects "relevant and recent"?
- **Example:** The refresh inject lists are hand-built (refresh-inject.md).
- **Records say:** "Give him the raw that's relevant and recent" (752e0f, 2026-09-24). "Harness ... takes vision data and creates the corresponding skills" (b05237, 2026-09-18). Distilled vision stands only after the living reviews it (psyche skill).
- **Open:** Whether Psyche Nexus serves queries by subject and date, and whether it records review state (raw, distilled, approved). Whether Harness or Curriculum generates skills from it.

### P6. Chronology: in Psyche or in Mind?
- **Records say:** "We need a way to keep track of chronology ... of psyche input" (9993b5, 2026-09-17). "Create a chronology of what happened ... and the direction of the psyche's vision. Start storing this in the mind component" (b7da5d, 2026-09-24).
- **Open:** Whether the psyche's own chronology is a Psyche Nexus view or Mind memory.

## 4. Mind Nexus

### N1. What does Mind Nexus store and replace?
- **Example:** flows/<id>/log.md, reports/, witnesses/, Beads, and the index are all Markdown or ad hoc today.
- **Records say:** "replace a lot of the files and the readmes ... reporting and keeping track of which repositories are involved, what kind of knowledge and witnesses ... summaries of transcripts" (1a6ca4, 2026-09-05). "the Flow's memory will live in mind" (9993b5, 2026-09-17). Technical chronology, "what landed, what ran, what tested, what was deployed" (33ba2b, 2026-09-18). The archive is "the memory" (b7da5d, 2026-09-24).
- **Open:** Which of today's files map to which records, and the enum vocabulary for them: "The more we specify a language of enums, the better" (9993b5, 2026-09-17).

### N2. "How the Mind, the Field and Psyche interact with the system": is Mind Nexus a gateway?
- **Records say:** Mind Nexus replaces "not just log, but how the Mind interacts with the system, how the field interacts with the system, and how Psyche interacts with the system" (e51411, 2026-09-25). Elsewhere, "the Mentci nexus that can pretty much talk to everything if it has the right permission" (b81560, 2026-09-19) and "Mentci talks to persona" (c8d79f, 2026-09-19).
- **Open:** Whether Mind Nexus is the interaction surface for the aspects, and if so, how it differs from Mentci and persona. The words stop short.

### N3. Does Field get its own data home, or does Mind hold it?
- **Records say:** "Psyche data, mind data, and then we're going to have the field now, so field data" as three repositories (b05237, 2026-09-18). Mind Nexus replaces "how we log the Mind and the field" (e51411, 2026-09-25).
- **Open:** Whether the newer words fold field data into Mind or only its logging.

### N4. Size, retention and forgetting
- **Example:** The field repo keeps receipts with "no retention deletion policy". sema-engine has a "finite retention" policy record but no rule for Mind.
- **Records say:** "mind will become our most bloated component ... distributable or archivable" (9993b5, 2026-09-17). "how to let things go, how to delete, and how to recondense and resummarize" (b7da5d, 2026-09-24).
- **Open:** Who decides what is condensed or deleted, and when.

### N5. Is the existing `mind` repository the Mind Nexus?
- **Example:** `mind` (last changed 2026-08-13) is a persona-era work-graph daemon with Thought and Relation records, `signal-mind` 3.0.0.
- **Records say:** "anything that has already been built that did not take the shape of The nexus is going to be rewritten" (e06e4c07, 2026-08-19, distilled in Vision/nexus). The psyche repo keeps the old stacks segregated (019ffc53).
- **Open:** Whether Mind Nexus reuses or re-authors `mind` and `signal-mind`.

## 5. Field and persona

### R1. Who owns flow lifecycle: Flow, Field, or persona?
- **Example:** e51411's log says "Field owns lifecycle". Field's README says it "does not own flow lifecycle actions". Flow has Start and Stop.
- **Records say:** "Get the low-power Field to take charge of bringing up and maintaining the 12 flows ... ghosts are collected" (b80e55, 2026-09-20). "persona manages all of the clusters ... always a harness instance of each of the triad" (05c604, 2026-09-17). "Flow keeps track of the flow's progression, so that's where it goes" after "This goes in persona, maybe" (fd0f97, 2026-09-17). Flow starts missing crucial flows (d8df70, 2026-09-24).
- **Options:** Flow executes, and Field or persona decides policy. Records do not divide the roles.

### R2. What is Field Nexus, and does it exist yet?
- **Example:** The `field` repository holds Node scripts that are read-only inventory. It has no Nexus, sockets or Sema store.
- **Records say:** "a field nexus that will be our system monitor ... call the field CLI, which will create a signal with a traceback to its caller" (b05237, 2026-09-18). Census of panes, harnesses, liveness and transcripts, "ported eventually to the field nexus", with transcripts possibly "a separate nexus" (b80e55, 2026-09-20). "Field is for repair" (836818, 2026-09-24). "compensation is Field" (752e0f, 2026-09-24).
- **Open:** Field Nexus's contract. Whether the transcript service sits inside it or apart. The living left that open themself: "unless we keep that as a separate nexus".

### R3. What is persona's scope: a host service supervisor, cluster layers, or an identity across machines?
- **Example:** `persona` ARCHITECTURE (2026-09-12) describes a host-level engine-management daemon for the old Persona ecosystem.
- **Records say:** "the persona is basically the root orchestrator, the system D of this whole concept" (6cc91b notion, 2026-09-13). "persona service ... it checks all the services and makes sure they're running" (6fb948, 2026-09-23). "One persona is one unified whole that could spawn multiple machines ... one machine can run parts of several personas", with trust overlapping across networks (752e0f, 2026-09-25). "probably persona to start managing all this" (e51411, 2026-09-25). vision-raw/persona.md is empty.
- **Open:** Persona's first concrete duties and contract. How it relates to Field Nexus (both check services) and to Flow.

### R4. Does persona hold the layers of authority?
- **Records say:** The onion of layers "eventually will have representation in one of the nexuses, like in Persona, the different layers of authority" (6cc91b, 2026-09-14). Aspects and power levels are in Flow's contract as `FlowAspect` and `PowerLevel`.
- **Open:** Whether authority (who may refresh, escalate or configure whom) is persona's record or Flow's. This ties to F3 and M4.

### R5. The private part and the soul
- **Records say:** Chartered, NOT ACTIVE until an open-source seat runs (CLAUDE.md, from 6cc91b, 2026-09-14). "the soul ... the private part of the persona" (bcd02a notion, 2026-09-13).
- **Open:** Only whether persona's records should reserve room for it now. Nothing more is asked.

## 6. Records and schema evolution

### S1. When is a store "live", after which it may not be discarded?
- **Example:** Message failed on its preserved schema-v3 store. Flow 0.4 needed a fresh store and rebinding. After each wipe the live flows had to be bound again.
- **Records say:** "We don't need to keep old stores of Flow and message. We're not even live yet. Stop treating this like it's a fucking migration" (d8df70, 2026-09-24). "We're going to need to handle database upgrades or the database when the records change. We're going to need to specify a better way do that" (e51411, 2026-09-25).
- **Open:** What marks the line into live. Whether it is drawn per Nexus: Psyche and Mind stores hold the living's words and memory, while Flow's registry can be rebuilt from running processes.

### S2. What mechanism upgrades a store when record types change?
- **Example:** Flow kept its v5 rows by putting new data in a separate table (flow README). sema hard-fails on a `SchemaVersion` mismatch and "migration is a coordinated rebuild (delete the old database ...)" (sema ARCHITECTURE.md).
- **Records say:** Sema "matters more than nexus, because operational editing should yield the migration with the edit" (Vision/sema, distilled 2026-09-09). "We should have a migration system also" (6cc91b, 2026-09-13). Every Nexus opens its default Sema store, and a populated store resumes (Vision/nexus).
- **Options named in the design docs:** (a) Manual `SchemaVersion` with delete-and-rebuild (sema, today). (b) Additive layout bumps upgraded in place at open (sema-engine layouts 4 to 5). (c) Content-addressed schema hashes with typed reducers from old records to new, both kept until the old is retired (sema "future work"). (d) Migrations derived from the schema diff, with hand-written code only for ambiguous changes (upgrade ARCHITECTURE.md). (e) Separate additive tables that leave old rows untouched (Flow's practice). These docs predate the current Nexus shape. No psyche record picks one.

### S3. How does a live Nexus hand over to its next version?
- **Records say:** Zero-downtime self-update, recompiling one Nexus at a time (nexus-rationale; e06e4c07, 2026-08-19). The persona-era design has an `upgrade` daemon and a `signal-version-handover` protocol between two sibling daemons (mirror, divergence, marker), all still placeholders.
- **Open:** Whether the handover protocol is kept, and whether it becomes a standard part of every Nexus through the `nexus` library.

### S4. Wire contract evolution: recompile everyone, or accept old messages?
- **Example:** The v4 escalation contract says "mixed v3/v4 operation is unsupported ... switch them in one attended cutover".
- **Records say:** "If we add a new thing to the cluster of nexuses, then everybody has to recompile to be able to talk to it, but that's okay" (b81560, 2026-09-19). The contract crate's semver is the wire's semver (nexus skill). The upgrade doc says "an old-version message is upgraded, accepted, and logged rather than rejected".
- **Open:** Lock-step cutover or tolerance of old versions. The records name both.

### S5. Roll forward, or countdown rollback?
- **Records say:** "There's no rolling back because if we roll back we fall off the cliff" (d8df70, 2026-09-24). "have an automatic countdown rollback on some of these really big, potentially breaking things" (05c604, 2026-09-15).
- **Open:** Whether the first is about the not-live period only. If so, the second governs once stores are live. The newer words do not say that they withdraw the older ones.

### S6. Where is the record schema written, and is the migration part of it?
- **Records say:** Sema's root "declares record types; the remaining sections are to be decided" (Vision/sema). "The nexus and sema documents are undesigned" (Vision/nexus). The migration section in Ethos "is operational ... not vision" (564f55, 2026-09-09).
- **Open:** The Sema document's remaining sections, including whether it has a version or migration section.

## 7. Cross-cutting (short)

- **C1. The Nexus Core term.** The nexus skill still says "The decision-making engine inside it is Nexus Core". The living ruled "the nexus-core runtime concept overthinking" (fe34eb, 2026-09-10). The skill line and the ruling disagree.
- **C2. Protocol and actor standards.** "The protocol is to be decided" (Vision/signal). "The standards of their use are still to be designed" for Kameo actors (Vision/nexus).

---

## Count

Flow 9, Message 7, Psyche Nexus 6, Mind Nexus 5, Field and persona 5, records and schema 6, cross-cutting 2. Total 40.

## Most blocking

1. S1 and S2: no rule for when a store becomes live or for how it upgrades. Psyche and Mind cannot keep data until this is settled, and each Flow or Message redeploy drops the live flow bindings.
2. F1 and F2: three Flow contract lines diverge (Restart, Refresh with archive, v4 escalation). The refresh lock has no single owner, so automatic refresh cannot be built.
3. M3 and M4: hold duration, escalation owner and hop limit are undefined, and the escalation contract is unmerged. Undeliverable messages have no end state.
4. P1 and P3: Psyche Nexus has no storage home (repository or store) and no entry path for the living's words from any seat.
5. R1 with P2 and N2: lifecycle ownership among Flow, Field and persona, and the split between Psyche Nexus and Mind Nexus ("and Mind"), are unresolved. Their vocabularies cannot be drawn until these are settled.

## Sources

Psyche, distilled: `/home/li/primary/Vision/nexus.md`, `Vision/flowNexus.md`, `Vision/messaging.md`, `Vision/psyche.md`, `Vision/sema.md`, `Vision/signal.md`, `Vision/archive-ethosMonolith.md`, `Vision/sources/sema.md`, `Intent/data.md`, `vision-raw/persona.md` (empty), `vision-raw/flowDaemon.md`.

Psyche, raw and notion, by flow:
- e51411: `vision/nexus.md`, `authority.md`, `launch.md`, `mainFlow.md`, `messaging.md`, `refresh.md`, `titles.md`, `security.md`, `speech.md`; `notion/v2.md`.
- d8df70: `vision/flowLifecycle.md`, `flowTool.md`, `messaging.md`, `deployment.md`, `building.md`, `launch.md`.
- 836818: `vision/flowNexus.md`, `nexusAnatomy.md`, `messaging.md`, `refresh.md`.
- 752e0f: `vision/persona.md`, `psycheLogging.md`, `livingInput.md`, `messaging.md`, `layers.md`, `psycheInjection.md`, `psycheVoice.md`, `unity.md`, `awareness.md`, `flowDeploy.md`, `refresh.md`, `work.md`.
- b80e55: `vision/nexusComponentDeploymentAndTriadRoles.md`, `fieldNexusSystemQuery.md`, `visualizationPipelineAndFlowLifecycle.md`, `ghostCollectionAndFlowMaintenance.md`, `refreshThresholdAndCacheSnapshot.md`, `retirement.md`.
- b7da5d: `vision/contextSize.md`, `freshFlowsAndArchive.md`, `systemStatus.md`, `meaningLanguage.md`.
- 9993b5: `vision/mindMemory.md`, `structuredLog.md`, `psycheVsMind.md`, `flowAnatomy.md`, `transparentRefresh.md`, `callerIdentity.md`, `transcriptArchive.md`, `psycheChronology.md`, `middleLayerRouting.md`, `typedString.md`, `flowIdLayers.md`.
- Others: `flows/1a6ca4/vision/psyche.md`, `mind.md`, `personaMetaHarness.md`; `flows/fd0f97/vision/psyche.md`, `flowLifecycle.md`, `launch.md`, `persona.md`; `flows/f55ec8/vision/psycheTool.md`, `flowRefresh.md`; `flows/33ba2b/vision/psycheDataArchitecture.md`; `flows/b05237/vision/operational-theField.md`, `operational-threeDataReposAndPrimaryNext.md`, `operational-signalOriginHandshake.md`, `operational-logOnMainNowMigrateLater.md`; `flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md`; `flows/da1e3f/vision/operational-flowVsMessage.md`; `flows/5f38bc/vision/illustratedTranscriptPresentationAndPsycheLogging.md`; `flows/05c604/vision/persona.md`, `layers.md`, `deployment.md`, `nexus.md`; `flows/6cc91b/vision/migration.md`, `pairHierarchy.md`; `flows/6cc91b/notion/persona.md`; `flows/bcd02a/notion/persona.md`; `flows/6fb948/vision/personaServiceAndNexusImagery-20260923.md`; `flows/c8d79f/vision/operational-mentciTalksToPersona.md`; `flows/6db4fe/vision/messaging.md`; `flows/e06e4c07/vision/archive-nexus.md`; `flows/fe34eb/vision/nexus.md`; `flows/564f55/vision/archive-sema.md`, `archive-datom.md`; `flows/019ffc53/vision/threeStacks.md`.

Reports and logs: `/home/li/primary/flows/e51411/reports/flow-message-basics.md`, `flows/e51411/log.md`, `flows/b7da5d/log.md`, `flows/752e0f/log.md`.

Skills, read as evidence: `/home/li/primary/.claude/skills/nexus/SKILL.md`, `nexus-rationale/SKILL.md`, `messaging/SKILL.md`, `testing-message-route/SKILL.md`, `subflow/SKILL.md`.

Repositories under `/git/github.com/LiGoldragon/`:
- `flow`: `README.md`, `DESIGN.md` at `7cc19af`.
- `signal-flow`: `ethos/signal.ethos` at `7ba21d0`, `03ea165`, `fa326ac`, `755186e`; `UPGRADES.md` at `755186e`.
- `message`: `README.md`, `ARCHITECTURE.md`; `README.md` at `8aa6d7b`.
- `signal-message`: `ARCHITECTURE.md`; `ethos/signal.ethos` at `1c023b5`.
- Single documents: `meta-signal-message/ARCHITECTURE.md`, `psyche/ARCHITECTURE.md`, `signal-psyche/ARCHITECTURE.md`, `meta-signal-psyche/ARCHITECTURE.md`, `field/README.md`, `nexus/ARCHITECTURE.md`, `sema/ARCHITECTURE.md`, `sema-engine/ARCHITECTURE.md`, `sema-storage/ARCHITECTURE.md`, `upgrade/ARCHITECTURE.md`, `signal-upgrade/ARCHITECTURE.md`, `signal-version-handover/ARCHITECTURE.md`, `persona/ARCHITECTURE.md` (headings and TL;DR), `signal-persona/ARCHITECTURE.md`, `mind/ARCHITECTURE.md` (headings and TL;DR), `signal-mind/README.md`.
- `CriomOS-home` `flake.lock` at `04446e78`.
