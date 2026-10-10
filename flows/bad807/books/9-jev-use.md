<!-- to-the-living:start -->
Presentation.{ «Jev in the flow-handling system: where a typed decision helps now» }

> Extend the proposals for how we can use it now, maybe for different parts of what we're trying to design in our communication/flow handling system. How this [Jev] could be used to make decisions, or to guide decisions, or to give data that will maybe make another [Jev] call put out data that will eventually come out as a decision somewhere

-- psyche, typed, 2026-10-04.

Everything designed below is the flow's proposal, not his words: the types, the decision points, the chain, the ranking.
It keeps the agreement of «Jev: what Mind and Psyche agree on»:

```
Jev enters     as a Rust library dependency of one caller
Verdict policy none until he rules one
Reaping        Flow's Replace stays the executor
```

## 1. One Jev call

```
Model     typesafe/jev-1.13 on OpenRouter, POST /api/alpha/decisions
Asks      a state (a JSON object) and named typed questions, all answered in one pass
Answers   Noul: one probability · Choice: a pick, a confidence, a probability per option · Score: 0 to 10, a confidence, a probability per level
Never     prose, a rationale, or a shape outside the three
Price     $0.042 per million input tokens, output free; 32K context; 70 to 500 ms, as marketed
Cost      every reply carries usage.cost, so a caller can sum its own spend
Apart     answers in one call never see each other: a chain is two calls
Weak      arithmetic, counting, dates, the first Choice option, text in state that steers it
```

From TypeSafe's own list of weak spots: sums and dates stay in code, and only their results enter the state.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 120" width="700" font-family="sans-serif" font-size="13"><defs><marker id="c1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="120" fill="#fff"/><rect x="10" y="15" width="230" height="40" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="125" y="40" text-anchor="middle" font-size="12">State: typed fields, no transcript</text><rect x="10" y="65" width="230" height="40" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="125" y="90" text-anchor="middle" font-size="12">Questions: Noul · Choice · Score</text><rect x="290" y="35" width="120" height="50" rx="8" fill="#fdf0d8" stroke="#b07a12"/><text x="350" y="58" text-anchor="middle" font-weight="bold">Jev</text><text x="350" y="76" text-anchor="middle" font-size="11">one pass</text><rect x="490" y="15" width="200" height="40" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="590" y="40" text-anchor="middle">Decision per question</text><rect x="490" y="65" width="200" height="40" rx="6" fill="#f3efe0" stroke="#8a7a2b"/><text x="590" y="90" text-anchor="middle">Cost, from usage</text><g stroke="#333" stroke-width="1.6" marker-end="url(#c1)"><line x1="240" y1="35" x2="288" y2="52"/><line x1="240" y1="85" x2="288" y2="70"/><line x1="410" y1="52" x2="488" y2="35"/><line x1="410" y1="70" x2="488" y2="85"/></g></svg><p>Figure 1. One call: a state and questions in, a decision per question and the cost out.</p>

The flow's proposal, as an ethos Library. Every name not given as a variant is a String; Probability, Confidence, Measure and Cost are decimals.

```
Library
[]
[ Call.{ State Vector<Asked> }                     ; the state, rendered to JSON at the network edge
  Asked.{ QuestionName Question }
  Question.{ Instruction Kind }
  Kind.[ Noul
         Choice.Vector<Alternative>
         Score.Vector<Meaning> ]                   ; the legend: what the low and high ends mean
  Alternative.{ AlternativeName Meaning }
  Answered.{ Vector<Answer> Cost }
  Answer.{ QuestionName Decision }
  Decision.[ Noul.Probability
             Choice.{ AlternativeName Confidence Vector<Weight> }
             Score.{ Measure Confidence } ]               ; the per-level probabilities are left out
  Weight.{ AlternativeName Probability } ]
[]
[]
```

One reply, in a position expecting Answered:

```
{ [ { RequiresAction Noul.0.08 }
    { Placing Choice.{ Mind 0.81 [ { Psyche 0.12 } { Mind 0.81 } { Field 0.07 } ] } } ] 0.0000252 }
```

## 2. Eight decision points

Each state below is a struct the flow proposes; none exists today. No state carries a transcript.
A message body or his words in a state can steer Jev; one more reason each point starts as a guide.

### 2.1 Does this message need its recipient?

```
Decision  whether a message requires the recipient's action, delivers a result it awaits, or reports a blocker
Caller    today: the sending seat, by the line in compensation-messenger-clj; hm-send has no gate
          proposed: Flow Nexus, inside Vet, which Message asks before each delivery
State     MessageState.{ SenderRole RecipientBrief Body }
Kind      Noul
Drives    a guide: the probability rides back with Vetted; Deliver is unchanged until a policy is ruled
Cost      per message, about 600 tokens of state
```

```
{ RequiresAction { «Does this message require the recipient to act, deliver a result it awaits, or report a blocker?» Noul } }
Noul.0.08
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">Flow · Vet</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Noul</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">guide: Vetted carries it</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m1)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">MessageState</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 2. 2.1: Vet asks Jev one Noul; the probability rides back as a guide.</p>

### 2.2 Is queued context on-topic for the flow it waits for?

```
Decision  how much a queued item bears on the flow it waits for
Caller    today: none; his words on context injection describe the queue, Message parks only addressed messages
          proposed: Message Nexus, when an item enters a parked recipient's queue
State     QueuedState.{ RecipientBrief ItemKind ItemHeading }
Kind      Score
Drives    data: the score is kept in Message's memory for the call in 2.3
Cost      per queued item, about 400 tokens
```

```
{ Bearing { «How much does this item bear on the flow's brief?» Score.[ «none» «touches a word» «touches its topic» «changes its next step» ] } }
Score.{ 6.4 0.71 }
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">Message · enqueue</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Score</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#f3efe0" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">data: kept for 2.3</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m2)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">QueuedState</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 3. 2.2: a queued item gets a Score, kept as data.</p>

### 2.3 The chain: wake now, inject at the next wake, or drop

```
Decision  what to do with the recipient's queue when its turn ends
Caller    proposed: Message Nexus, when Flow shows the recipient at rest
State     WakeState.{ AgentState Vector<Measure> ItemCount }   ; the measures are 2.2's scores
Kind      Choice
Drives    a guide, then an action once ruled: Soft delivery now, injection with the next message, or nothing
Cost      per wake, about 300 tokens
```

```
{ Waking { «What should the waiting context do?» Choice.[ { Wake «worth a turn now» } { Inject «rides in with the next message» } { Drop «bears on nothing» } ] } }
Choice.{ Inject 0.77 [ { Wake 0.14 } { Inject 0.77 } { Drop 0.09 } ] }
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">Message · at rest</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Choice</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">Wake · Inject · Drop</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m3)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">2.2's scores</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 4. 2.3: scores in, Wake, Inject or Drop out.</p>

### 2.4 Is a seat dead, idle, or past its successor?

```
Decision  whether a seat is still needed
Caller    today: the main flow, by trial-reaping; Flow reaps mechanically on Replace
          proposed: Flow Nexus, when a Report.{ FlowId Stopped } lands
State     ReapingState.{ AgentState FlowLifecycle HasSuccessor SuccessorStoppedLater StopAge }   ; the comparison and the age band made in code
Kind      Choice
Drives    a guide to the main flow, never the executor: Replace and Retire still end the seat
Cost      per turn of any seat, about 200 tokens
```

```
{ Standing { «Is this seat still needed?» Choice.[ { Working «mid-task» } { Idle «awaits a message» } { Abandoned «no one will wake it» } { PastSuccessor «its successor runs» } ] } }
Choice.{ PastSuccessor 0.92 [ { Working 0.01 } { Idle 0.04 } { Abandoned 0.03 } { PastSuccessor 0.92 } ] }
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">Flow · Stopped</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Choice</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">guide → main flow → Replace</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m4)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">ReapingState</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 5. 2.4: a stopped seat is judged; the main flow decides.</p>

### 2.5 Should a flow hand over?

```
Decision  whether the work has moved away from the flow's brief
Caller    today: the seat itself, by trial-succession, "refresh before compaction"; no flow can read its context size
          proposed: Flow Nexus, at QueueTurnEnd
State     ChangeoverState.{ Brief Vector<TopicName> }   ; the topics are 2.6's last answers
Kind      Noul
Drives    a guide to the seat's Mind: request a successor with a fresh prompt
Cost      per turn, about 500 tokens
```

The share is arithmetic and stays in code: it only decides when the call is made. His figures differ: sixty percent (2026-09-14), thirty or forty (2026-09-16).

```
{ Shifted { «Has the work moved away from the brief?» Noul } }
Noul.0.64
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">Flow · turn end</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Noul</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">guide → successor request</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m5)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">2.6's topics</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 6. 2.5: the topics in, a Noul out as a guide.</p>

### 2.6 Which topic do the living's words belong to?

```
Decision  what kind of words these are, and under which topic a record of them goes
Caller    today: the main flow, by hand, through the psyche skill
State     RecordState.{ Context Verbatim Vector<TopicName> }   ; the names in Vision/ and the flow's vision/
Kind      Choice, twice in one call
Drives    a guide: the seat still writes the record, and it can be data for 2.5
Cost      per turn of the living, about 2,000 tokens with the topic list
```

```
{ Sort { «What is this?» Choice.[ { Vision «what the system should be» } { Notion «turned over, binding nothing» } { Instruction «an order for now» } { Question «answered, not logged» } ] } }
{ Topic { «Which topic holds it?» Choice.[ { messaging «what flows send» } { jev «the decision model» } { New «no topic fits» } ] } }
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">main flow · his words</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Choice ×2</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">guide: the record's file</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m6)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">RecordState</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 7. 2.6: two Choices in one call name the record's file.</p>

### 2.7 Which aspect does a skill belong to?

```
Decision  whether a skill is Psyche's, Mind's, or Field's
Caller    today: no one yet; his order relayed; psyche-skills, mind-skills and field-skills exist
State     SkillState.{ SkillName Description Prefix LineCount }
Kind      Choice
Drives    data: a placing table for a book he rules on, not a move
Cost      per launch: one batch over the 70 files in Curriculum/skills
```

```
{ Placing { «Whose skill is this?» Choice.[ { Psyche «his vision» } { Mind «judging and routing» } { Field «doing the work» } ] } }
Choice.{ Field 0.69 [ { Psyche 0.06 } { Mind 0.25 } { Field 0.69 } ] }
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">one batch</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Choice</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#f3efe0" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">data: a placing table</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m7)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">SkillState</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 8. 2.7: one batch builds a placing table.</p>

### 2.8 Is a proposal small enough to be accepted whole?

```
Decision  how much a proposal infers beyond its quote
Caller    today: the main flow, before a book is presented
State     ProposalState.{ Now Proposed Grounding ClaimCount }
Kind      Score
Drives    a guide: a high score asks the flow to split or narrow before he sees it
Cost      per proposal, about 700 tokens
```

```
{ Inference { «How much does Proposed say that Grounding does not?» Score.[ «nothing» «a word» «a clause» «a new rule» ] } }
Score.{ 2.1 0.83 }
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 74" width="700" font-family="sans-serif" font-size="12"><defs><marker id="m8" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="74" fill="#fff"/><rect x="8" y="14" width="170" height="44" rx="6" fill="#e3ecfb" stroke="#2b4a8b"/><text x="93" y="41" text-anchor="middle">main flow · book</text><rect x="300" y="14" width="110" height="44" rx="6" fill="#fdf0d8" stroke="#b07a12"/><text x="355" y="34" text-anchor="middle" font-weight="bold">Jev</text><text x="355" y="50" text-anchor="middle">Score</text><rect x="490" y="14" width="205" height="44" rx="6" fill="#e2f4e6" stroke="#2e7d32"/><text x="592" y="41" text-anchor="middle" font-size="11">guide: split or narrow</text><g stroke="#333" stroke-width="1.6" marker-end="url(#m8)"><line x1="178" y1="36" x2="298" y2="36"/><line x1="410" y1="36" x2="488" y2="36"/></g><text x="238" y="30" text-anchor="middle" font-size="11">ProposalState</text><text x="449" y="30" text-anchor="middle" font-size="11">answer</text></svg><p>Figure 9. 2.8: a Score asks the flow to split or narrow.</p>

## 3. The chain, and where the calls sit

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 170" width="700" font-family="sans-serif" font-size="13"><defs><marker id="c2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="170" fill="#fff"/><g stroke="#333"><rect x="5" y="40" width="90" height="56" rx="6" fill="#e3ecfb"/><rect x="117" y="40" width="80" height="56" rx="6" fill="#fdf0d8"/><rect x="219" y="40" width="110" height="56" rx="6" fill="#f3efe0"/><rect x="351" y="40" width="80" height="56" rx="6" fill="#fdf0d8"/><rect x="453" y="40" width="110" height="56" rx="6" fill="#e2f4e6"/><rect x="585" y="40" width="110" height="56" rx="6" fill="#eee"/></g><g text-anchor="middle"><g font-weight="bold"><text x="50" y="64">state</text><text x="157" y="64">Jev</text><text x="274" y="64">data</text><text x="391" y="64">Jev</text><text x="508" y="64">decision</text><text x="640" y="64">action</text></g><g font-size="11"><text x="50" y="84">a queued item</text><text x="157" y="84">Score</text><text x="274" y="84">6.4, in memory</text><text x="391" y="84">Choice</text><text x="508" y="84">Inject</text><text x="640" y="84" font-size="10">rides next message</text></g></g><g stroke="#333" stroke-width="1.6" marker-end="url(#c2)"><line x1="95" y1="68" x2="115" y2="68"/><line x1="197" y1="68" x2="217" y2="68"/><line x1="329" y1="68" x2="349" y2="68"/><line x1="431" y1="68" x2="451" y2="68"/><line x1="563" y1="68" x2="583" y2="68"/></g><text x="160" y="125" font-size="12" fill="#555">2.2, per queued item</text><text x="380" y="125" font-size="12" fill="#555">2.3, per wake: its state holds every 2.2 score</text><text x="350" y="155" text-anchor="middle" font-size="12" fill="#555">the same shape: 2.6 topics → 2.5 handover</text></svg>

Figure 10. One call's score is data; a second call's choice is the decision; a seat or a Nexus acts on it. Two calls, because answers in one call never see each other.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 230" width="700" font-family="sans-serif" font-size="13"><defs><marker id="c3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="230" fill="#fff"/><rect x="120" y="10" width="570" height="150" rx="10" fill="#f4f7fc" stroke="#2b4a8b" stroke-width="2"/><text x="405" y="32" text-anchor="middle" font-weight="bold">Flow Nexus or Message Nexus</text><rect x="10" y="60" width="90" height="50" rx="6" fill="#eee" stroke="#555"/><text x="55" y="90" text-anchor="middle">event</text><g stroke="#333"><rect x="140" y="55" width="130" height="60" rx="8" fill="#e3ecfb"/><rect x="320" y="55" width="150" height="60" rx="8" fill="#fdf0d8"/><rect x="530" y="55" width="140" height="60" rx="8" fill="#e2f4e6"/></g><g text-anchor="middle"><text x="205" y="82" font-weight="bold">Signal</text><text x="205" y="100" font-size="11">Report · Vet · Weigh</text><text x="395" y="82" font-weight="bold">Operation</text><text x="395" y="100" font-size="11">Weigh: builds the Call</text><text x="600" y="82" font-weight="bold">Memory</text><text x="600" y="100" font-size="11">Decision, cost</text></g><rect x="320" y="175" width="150" height="45" rx="8" fill="#fff" stroke="#b07a12" stroke-width="2"/><text x="395" y="203" text-anchor="middle" font-weight="bold">Jev on OpenRouter</text><g stroke="#333" stroke-width="1.6" marker-end="url(#c3)"><line x1="100" y1="85" x2="138" y2="85"/><line x1="270" y1="85" x2="318" y2="85"/><line x1="470" y1="75" x2="528" y2="75"/><line x1="528" y1="100" x2="472" y2="100"/><line x1="380" y1="115" x2="380" y2="173"/><line x1="410" y1="173" x2="410" y2="117"/></g><text x="300" y="150" font-size="11" text-anchor="end">State, Questions</text><text x="420" y="150" font-size="11">Answered</text><text x="600" y="140" text-anchor="middle" font-size="11">read back as state</text><text x="600" y="152" text-anchor="middle" font-size="11">for the next call</text></svg>

Figure 11. A call is an operation's body, as in «The Nexus», proposal 6. Signal never calls Jev; memory keeps each Decision so a later call can read it.

## 4. The first two to build

The flow's ranking. Both live in one caller, Flow Nexus, so the agreement's one dependency holds.

### First: the reaping guide, 2.4

His words name it the start: "this is where we're going to start using JEV" (2026-09-19). Its whole state already sits in Flow's memory.

```
flow/Cargo.toml
  Now       no Jev client
  Proposed  the Jev client crate; which one is held by a reuse investigation

flow/crates/flow-nexus/ethos/operation.ethos
  Now       Operation has no machine call
  Proposed  Weigh.ReapingState → Weighed.Decision, and Failed gains JevRefused

flow/crates/flow-nexus/src/performing.rs
  Now       perform matches Compose to Release
  Proposed  Weigh builds one Call and asks Jev; nothing else changes

flow/crates/flow-nexus/src/store.rs
  Now       a flow's harness events and its Replacing record
  Proposed  the last Decision kept beside them, with its cost

signal-flow/ethos/signal.ethos
  Now       Observe.ObserveSelection → AgentObserved.AgentObservation
  Proposed  Weigh.FlowId → Weighed.{ FlowId Decision }, read by the main flow before it reaps
```

### Second: the message gate, 2.1

His words: "a rule again that guides messaging better so that we don't end up getting these noisy messages that wake or disturb flows" (2026-10-04). It reaches Message's deliveries only; hm-send writes to Herdr directly until its sends move onto Message.

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

## 5. Two things not settled

The flow's reading of two tensions in its own proposal.

```
Jev's state  is JSON text
Nexus rule   "a Nexus never handles text"
Proposed     the state stays a typed struct in the Nexus; the JSON is made at the network edge
Proposed     a Nexus never calls Jev; a CLI or side program does
```

```
Changeover share  sixty percent (2026-09-14) against thirty or forty (2026-09-16)
Used by           2.5, as the moment its call is made
```

## 6. Rulings

1. The first decision point.
   (a) The reaping guide in Flow: 2026-09-19, "this is where we're going to start using JEV". The flow's recommendation.
   (b) The message gate: 2026-10-04, "noisy messages that wake or disturb flows".
   (c) The living's words sorted and routed: 2026-10-04, "the main failure of machines is their inability to seem to differentiate between content types".
2. Whether Jev guides or decides.
   (a) Guides everywhere: each answer a probability a seat reads; every executor unchanged. The flow's recommendation, and the agreement as it stands.
   (b) Decides where the act is undone by the next turn (2.3 wake or inject, the delivery tier); guides where it is not (2.4 reaping, 2.6 records, 2.7 placing).
   (c) Decides at a line he sets per point, for example a Noul above 0.9 or a Choice whose confidence passes his line: TypeSafe's confidence-gated pattern.
3. The cost ceiling per day. $1 buys about 24 million input tokens, some 24,000 calls of 1,000 tokens.
   (a) $0.10 a day.
   (b) $1 a day. The flow's recommendation: room for every point here at today's traffic, which no one has measured.
   (c) $5 a day.
4. The edge rendering and who calls Jev.
   (a) The edge rendering is acceptable. The flow's recommendation.
   (b) A Nexus never calls Jev directly; only a CLI or side program does. The flow's recommendation.
5. The changeover share in 2.5: sixty percent, or thirty to forty. He sets it; the flow has no recommendation.
<!-- to-the-living:end -->
