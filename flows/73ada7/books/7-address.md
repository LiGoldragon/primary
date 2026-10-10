<!-- to-the-living:start -->
Presentation.{ «How a metaflow is named on the wire» }

## The case

Message hands Flow a request for a metaflow in two steps: it asks for the lock with Lock.Metaflow, then hands the request under it with Deliver.{ Lock Sender Request }, where the Lock is a metaflow with the time it lapses and the Sender is the sending metaflow. So the metaflow is what both inputs carry. Flow's buildable design declares one Metaflow in its Library: a variant per aspect, Psyche, Mind or Field, each holding Details, which are the topic and the layer together with the metaflow's State (awake with its current flow, asleep, or ended), its Past flows and its Queue of waiting requests (flows/f5a6e9/reports/flow-buildable-design.md:56-71). Yet where a metaflow is named, in Launch, it is written short, aspect, topic and layer only, as in Psyche.{ flow Primary } (the same design, 265-270), and Message's design sends the short form, as in To.Mind.{ nexus Secondary } (flows/73ada7/reports/build/message-design.md:293 and 518-521). One name stands for two shapes, and the two designs leave it unseparated. vision-flow already writes a flow's title from its aspect, topic, layer and flow id, and writes a voice as an aspect with a rank, Psyche.Primary, with no topic. The Message and Flow these designs describe are in development; neither is in production. That under the present declaration a Lock or a Sender would have to carry a State, a Past and a Queue, which Message neither knows nor holds, is this flow's inference.

## Distillation

### D1. What names a metaflow, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, the paragraph at line 24, which opens "Every flow has a topic; a flow with no special topic has the topic core" and closes "A flow's title names its aspect, topic, layer and flow id". Nothing in it is removed; a sentence is added at its end. The paragraph before it says voices are addressed by name and a flow id is for the ledger; the one after it gives the routes to the vision-aspects skill.

**Option (a), the address is its own type, the record another.**

Added: A metaflow is named by its aspect, topic and layer, Psyche.{ core Secondary }, and that name is a type of its own, the metaflow's address; what Flow keeps of a metaflow, its state, its past flows and its queue, is a separate record found by that address. Lock, Deliver and every other request that names a metaflow carry its address.

Rests on: flows/d4ae97/vision/flow.md:165-183 (2026-10-08), on a flow being aspect, topic and layer, the aspect its first field, a struct; flows/4ddfe1/vision/flow-names.md:3-7 (2026-10-09), on addressing every metaflow as psyche secondary or psyche primary; flows/01e496/vision/flowIdentity.md:3-9 (2026-10-02), on flows addressable by their continuous name; flows/41fa34/vision/clojure-flow.md:4 and flows/d4ae97/vision/flow.md:153-158 (2026-10-08), on metaflow addressing by metaflow name; flows/f5a6e9/vision/flow.md:27-33 (2026-10-07), on referring to metaflows and keeping the current flow and maybe its predecessor in the metaflow's memory; flows/d4ae97/notion/flow.md:12-21 (2026-10-08), a notion, on a metaflow record without vectors, of one size, pointing at the current flow, with other registries holding other data. With this, Lock.Metaflow takes the three fields and Deliver's Lock and Sender each carry them; that the Library's Details then splits into the address and a Memory record keyed by it, whose name the ruling would give, is this flow's reading.

**Option (b), one metaflow in a simple and an extended form.**

Added: A metaflow has a simple form, its aspect, topic and layer, Psyche.{ core Secondary }, and an extended form that adds its state, its past flows and its queue; both are the same metaflow, defined in ethos as forms of one type. Lock, Deliver and the common requests use the simple form; the extended form is for debugging and for other components.

Rests on: flows/edf227/vision/signalForms.md:3-7 (2026-10-03), on the simplified form, without the flow id, being the same data in another container, defined in ethos in Signal as formats, the simple form for common queries and the extended for the technical side; flows/62022e8f/vision/multiFormConcepts.md:3-12 (2026-08-30), on one concept written at different arities with fields omitted by arity, a simple and a complex form; flows/b7ba00/vision/messaging.md:39-56 (2026-09-26), on simple and full forms of a message and of a psyche. No record or landed skill this flow read gives the ethos form of one type at two arities, and whether ethos-zero accepts it is not observed here.

**Option (c), one Metaflow as it stands.**

Added: A metaflow is a variant of its aspect holding its details, its topic, its layer, its state, its past flows and its queue; a request that names a metaflow carries it whole.

Rests on: flows/73ada7/notion/metaflow.md:3-9 (2026-10-09), a notion, on every metaflow being a variant of psyche, mind or field, the struct holding its details such as the name of its topic; flows/f5a6e9/vision/flow.md:63-68 (2026-10-07), on psyche, mind and field having similar payloads, the variant one of the fields. This is the Library as Flow's design declares it; that it puts on every Lock and Sender data only Flow holds is this flow's inference.

**Ruling D1.** (a) A separate address type. (b) One type, simple and extended forms. (c) One Metaflow as it stands. (d) Amend, by line.

## Voice

One choice. Message asks Flow for a lock on a metaflow, then hands the request under that lock, so both name a metaflow. Flow's design has one Metaflow that holds its topic and layer and also its state, its past flows and its queue, while the launch and Message write only aspect, topic and layer. A makes that short name a type of its own and keeps the rest in a record found by it. B keeps one metaflow with a simple and an extended form, as you said on the 3rd for the form without the flow id. C keeps the one full Metaflow. Which one? This flow's reading: under C, every lock would carry a queue Message does not have.
<!-- to-the-living:end -->
