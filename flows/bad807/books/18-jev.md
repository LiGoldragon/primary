<!-- to-the-living:start -->
Presentation.{ «Jev» }

> Extend the proposals for how we can use it now, maybe for different parts of what we're trying to design in our communication/flow handling system. How this [Jev] could be used to make decisions, or to guide decisions, or to give data that will maybe make another [Jev] call put out data that will eventually come out as a decision somewhere

-- psyche, typed, 2026-10-04.

One edition of «Jev: what Mind and Psyche agree on» and «Jev in the flow-handling system».
Everything below his quotes is the flow's proposal: the types, the decision points, the ranking.
Tools, plugins, infrastructure and trends stay in «Our open-source stack and Jev», a separate report.

## 1. What Jev is to him

TypeSafe's model, `typesafe/jev-1.13` on OpenRouter. His three records:

```
2026-09-19  statistical decisions on reaping and retired responses
            "I think this is where we're going to start using JEV"
2026-09-24  an ultra-low power tier: "Maybe Jev redefines what is actually ultra-low power"
2026-09-25  the monitor flow: "let's get this set up today, I'll get OpenRouter credentials"
```

He never chose its first caller.

```
Asks      a state and named typed questions, all answered in one pass
Answers   Noul: one probability · Choice: a pick, a confidence, a probability per option
          Score: 0 to 10, a confidence
Never     prose, a rationale, or a shape outside the three
Price     $0.042 per million input tokens, output free; every reply carries its cost
Apart     answers in one call never see each other: a chain is two calls
Weak      arithmetic, counting, dates, text in the state that steers it
```

## 2. How it is now

```
Reaping     no program asks a model whether to reap; agents judge, Flow reaps on Replace
judge       0.2.0 on main has no Jev code
            a branch holds a Decisions client for alpha/decisions, 21 tests reported by its executor
            nothing published, pinned in Home, or deployed; the rollout held by a reuse investigation
Gateways    alpha/decisions: the branch client, unpublished
            v1/systemone: the community crate typesafe-system-one 0.1.1, not on disk, unverified
Key         the credential store answers "missing or inaccessible"; not proven absent
```

<figure><svg role="img" aria-label="Jev enters as a library dependency of one caller" viewBox="0 0 700 200" width="700" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12"><rect width="700" height="200" fill="#fff"/><rect x="10" y="75" width="150" height="50" rx="6" fill="#eef" stroke="#447"/><text x="85" y="96" text-anchor="middle">the one caller</text><text x="85" y="113" text-anchor="middle" font-size="10">his choice: ruling 1</text><rect x="230" y="75" width="150" height="50" rx="6" fill="#efe" stroke="#474"/><text x="305" y="96" text-anchor="middle">Jev client</text><text x="305" y="113" text-anchor="middle" font-size="10">Rust dependency</text><rect x="450" y="15" width="230" height="50" rx="6" fill="#fee" stroke="#744"/><text x="565" y="36" text-anchor="middle">OpenRouter v1/systemone</text><text x="565" y="53" text-anchor="middle" font-size="10">community crate, unverified</text><rect x="450" y="135" width="230" height="50" rx="6" fill="#fee" stroke="#744"/><text x="565" y="156" text-anchor="middle">OpenRouter alpha/decisions</text><text x="565" y="173" text-anchor="middle" font-size="10">branch client, unpublished</text><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#333"/></marker></defs><line x1="160" y1="100" x2="230" y2="100" stroke="#333" marker-end="url(#a)"/><line x1="380" y1="90" x2="450" y2="45" stroke="#333" stroke-dasharray="4" marker-end="url(#a)"/><line x1="380" y1="110" x2="450" y2="155" stroke="#333" stroke-dasharray="4" marker-end="url(#a)"/><text x="415" y="105" text-anchor="middle" font-size="10">one fixture each,</text><text x="415" y="117" text-anchor="middle" font-size="10">one live call each</text></svg><figcaption>Figure 1. Jev enters as a library dependency of one caller; the gateway is one of two candidates, chosen by witness.</figcaption></figure>

## 3. The five agreed points

Mind and Psyche agreed on all five.

```
1  No bespoke CLI, no Home pin. Jev is a Rust library dependency of the one caller only;
   the branch client stays an unpublished experiment.
2  The gateway is chosen by witness: one offline contract fixture per gateway, then one minimal
   live call each, pinned to jev-1.13, once the key exists. Whichever answers typed questions wins;
   if both, the smaller surface, the community crate, unless its audit shows a defect with file and line.
3  The key is unestablished; he is asked whether it exists and where it sits.
4  The first caller is his to choose, not assumed: the monitor and the retired-response path he named.
   Flow's Replace stays the executor; a judgment program is new, under Field.
5  No verdict policy and no change to reaping until he rules one.
```

## 4. Eight decision points

Each state is a struct the flow proposes; none exists today. No state carries a transcript.
Sums, ages and comparisons are made in code; only their results enter the state.

```
Point  Question                               Proposed caller             Kind      Drives
2.1    does this message need its recipient?  Flow Nexus, in Vet          Noul      guide, rides with Vetted
2.2    does queued context bear on the flow?  Message Nexus, at enqueue   Score     data for 2.3
2.3    wake now, inject at next wake, or drop Message Nexus, at rest      Choice    guide, then action once ruled
2.4    is a seat working, idle, abandoned,    Flow Nexus, on Stopped      Choice    guide to the main flow
       or past its successor?
2.5    has the work moved off the brief?      Flow Nexus, at turn end     Noul      guide: request a successor
2.6    what are his words, under which topic? the main flow               Choice×2  guide; data for 2.5
2.7    is a skill Psyche's, Mind's, Field's?  one batch over the skills   Choice    data: a placing table
2.8    how much does a proposal infer?        the main flow, before books Score     guide: split or narrow
```

Two chains: 2.2 feeds 2.3, and 2.6 feeds 2.5.

<figure><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 170" width="700" font-family="sans-serif" font-size="13"><defs><marker id="c2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="170" fill="#fff"/><g stroke="#333"><rect x="5" y="40" width="90" height="56" rx="6" fill="#e3ecfb"/><rect x="117" y="40" width="80" height="56" rx="6" fill="#fdf0d8"/><rect x="219" y="40" width="110" height="56" rx="6" fill="#f3efe0"/><rect x="351" y="40" width="80" height="56" rx="6" fill="#fdf0d8"/><rect x="453" y="40" width="110" height="56" rx="6" fill="#e2f4e6"/><rect x="585" y="40" width="110" height="56" rx="6" fill="#eee"/></g><g text-anchor="middle"><g font-weight="bold"><text x="50" y="64">state</text><text x="157" y="64">Jev</text><text x="274" y="64">data</text><text x="391" y="64">Jev</text><text x="508" y="64">decision</text><text x="640" y="64">action</text></g><g font-size="11"><text x="50" y="84">a queued item</text><text x="157" y="84">Score</text><text x="274" y="84">6.4, in memory</text><text x="391" y="84">Choice</text><text x="508" y="84">Inject</text><text x="640" y="84" font-size="10">rides next message</text></g></g><g stroke="#333" stroke-width="1.6" marker-end="url(#c2)"><line x1="95" y1="68" x2="115" y2="68"/><line x1="197" y1="68" x2="217" y2="68"/><line x1="329" y1="68" x2="349" y2="68"/><line x1="431" y1="68" x2="451" y2="68"/><line x1="563" y1="68" x2="583" y2="68"/></g><text x="160" y="125" font-size="12" fill="#555">2.2, per queued item</text><text x="380" y="125" font-size="12" fill="#555">2.3, per wake: its state holds every 2.2 score</text><text x="350" y="155" text-anchor="middle" font-size="12" fill="#555">the same shape: 2.6 topics → 2.5 handover</text></svg><figcaption>Figure 2. One call's score is data; a second call's choice is the decision; a seat or a Nexus acts on it.</figcaption></figure>

<figure><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 230" width="700" font-family="sans-serif" font-size="13"><defs><marker id="c3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="230" fill="#fff"/><rect x="120" y="10" width="570" height="150" rx="10" fill="#f4f7fc" stroke="#2b4a8b" stroke-width="2"/><text x="405" y="32" text-anchor="middle" font-weight="bold">Flow Nexus or Message Nexus</text><rect x="10" y="60" width="90" height="50" rx="6" fill="#eee" stroke="#555"/><text x="55" y="90" text-anchor="middle">event</text><g stroke="#333"><rect x="140" y="55" width="130" height="60" rx="8" fill="#e3ecfb"/><rect x="320" y="55" width="150" height="60" rx="8" fill="#fdf0d8"/><rect x="530" y="55" width="140" height="60" rx="8" fill="#e2f4e6"/></g><g text-anchor="middle"><text x="205" y="82" font-weight="bold">Signal</text><text x="205" y="100" font-size="11">Report · Vet · Weigh</text><text x="395" y="82" font-weight="bold">Operation</text><text x="395" y="100" font-size="11">Weigh: builds the Call</text><text x="600" y="82" font-weight="bold">Memory</text><text x="600" y="100" font-size="11">Decision, cost</text></g><rect x="320" y="175" width="150" height="45" rx="8" fill="#fff" stroke="#b07a12" stroke-width="2"/><text x="395" y="203" text-anchor="middle" font-weight="bold">Jev on OpenRouter</text><g stroke="#333" stroke-width="1.6" marker-end="url(#c3)"><line x1="100" y1="85" x2="138" y2="85"/><line x1="270" y1="85" x2="318" y2="85"/><line x1="470" y1="75" x2="528" y2="75"/><line x1="528" y1="100" x2="472" y2="100"/><line x1="380" y1="115" x2="380" y2="173"/><line x1="410" y1="173" x2="410" y2="117"/></g><text x="300" y="150" font-size="11" text-anchor="end">State, Questions</text><text x="420" y="150" font-size="11">Answered</text><text x="600" y="140" text-anchor="middle" font-size="11">read back as state</text><text x="600" y="152" text-anchor="middle" font-size="11">for the next call</text></svg><figcaption>Figure 3. A call is an operation's body; memory keeps each Decision for a later call. Drawn for ruling 6 (a); under (b) the downward arrow passes through the Nexus's CLI side.</figcaption></figure>

## 5. The two to build first

The flow's ranking. Both sit in Flow Nexus, so one caller holds the one dependency.

### First: the reaping guide, 2.4

His words name it the start: "this is where we're going to start using JEV" (2026-09-19).
Its whole state already sits in Flow's memory.

```
flow/Cargo.toml
  Now       no Jev client
  Proposed  the Jev client crate, the winner of point 2; held by the reuse investigation

flow/crates/flow-nexus/ethos/operation.ethos
  Now       Operation runs Compose to Release; no machine call; Failed has nine refusals
  Proposed  Weigh.ReapingState → Weighed.Decision, and Failed gains JevRefused

flow/crates/flow-nexus/src/performing.rs
  Now       perform matches Compose to Release
  Proposed  Weigh builds one Call and asks Jev; nothing else changes

flow/crates/flow-nexus/src/store.rs
  Now       flows, their state, roles and replacements; no decision kept
  Proposed  the last Decision kept beside them, with its cost

signal-flow/ethos/signal.ethos
  Now       Observe.ObserveSelection → AgentObserved.AgentObservation; no Weigh
  Proposed  Weigh.FlowId → Weighed.{ FlowId Decision }, read by the main flow before it reaps
```

```
ReapingState.{ AgentState FlowLifecycle HasSuccessor SuccessorStoppedLater StopAge }
{ Standing { «Is this seat still needed?» Choice.[ { Working «mid-task» } { Idle «awaits a message» }
  { Abandoned «no one will wake it» } { PastSuccessor «its successor runs» } ] } }
```

### Second: the message gate, 2.1

The landed line in compensation-messenger-clj, his rule:
"Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work."
The gate reaches Message's deliveries only; hm-send writes to Herdr directly until its sends move onto Message.

```
meta-signal-flow/ethos/signal.ethos
  Now       Vet.DeliveryRequest → Vetted.FlowId
  Proposed  Vet.DeliveryRequest → Vetted.{ FlowId Option<Decision> }

message/crates/message-nexus/src/flow_edge.rs
  Now       vet reads Vetted(flow_id)
  Proposed  vet reads the Decision too and keeps it with the message's receipts

flow/crates/flow-nexus/src/delivery.rs
  Now       Vet answers what Deliver would refuse
  Proposed  Vet also asks 2.1's question; Deliver does not read the answer until a policy is ruled
```

## 6. Two tensions

```
Jev's state   is JSON text
Nexus rule    "a Nexus never handles text"
Either        (a) the state stays a typed struct; the caller's Jev dependency renders it at the network edge
Or            (b) the Nexus hands the typed state to its CLI side, which calls Jev:
                  the datom-file book's way b, the Nexus asks and the CLI answers
```

```
Changeover share  sixty percent (2026-09-14) against thirty or forty (2026-09-16)
Used by           2.5, as the moment its call is made; the share itself stays in code
```

## 7. Rulings

1. The first caller.
   (a) A Field monitor that asks "is this seat dead?" before a reap is requested; Replace still reaps.
   (b) The retired-response path: a flow with a successor still answers; Jev judges whether it needs reaping.
   (c) Neither yet: Jev set up with a fixture only.
   (d) The reaping guide in Flow, 2.4. The use book's recommendation.
   (b) and (d) coincide: one record of his words, and PastSuccessor is his retired response.
   (d) also asks (a)'s question as Abandoned; it differs from (a) only in its seat, Flow Nexus, not a new Field program.
2. The key. Does an OpenRouter key exist, and in which store? Name the place, never the value.
3. The five points of section 3: one yes, or amend by number.
4. Guide or decide.
   (a) Guides everywhere; every executor unchanged. The flow's recommendation, and point 5 as it stands.
   (b) Decides where the next turn undoes the act (2.3, the delivery tier); guides elsewhere.
   (c) Decides past a line he sets per point, such as a Noul above 0.9: TypeSafe's confidence-gated pattern.
5. The cost ceiling per day, summed from each reply's cost. $1 buys some 24,000 calls of 1,000 tokens.
   (a) $0.10. (b) $1, the flow's recommendation; today's traffic is unmeasured. (c) $5.
6. The text state.
   (a) Rendered to text at the network edge, inside the caller's Jev dependency. The use book's recommendation.
   (b) The Nexus hands the state to its CLI side, which calls Jev, as the datom-file book's way b.
7. The changeover share for 2.5: sixty percent, or thirty to forty. He sets it; the flow has no recommendation.
<!-- to-the-living:end -->
