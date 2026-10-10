<!-- to-the-living:start -->
Presentation.{ «The new flows, as they run» }

Two audits answer your four questions: this seat's own (Source A, from a subflow that read transcripts, logs and the running system) and Mind Secondary Sol's (Source B, a read-only report with no live probe). Each finding is marked seen (an audit looked at the thing itself), recorded (taken from a log or receipt) or inferred (an audit's own reasoning).

[diagram: launch route]
launcher
   |
   v
flow-id + continuation file
   |
   v
Herdr pane + title
   |
   v
native harness
   |
   v
hm-register
(Flow Nexus sockets: exist, not called)

## 1. How the topic-flow setup was done

Both found: a flow starts through the launcher, which gives the flow an id and a continuation record, makes a Herdr pane, starts the native harness and registers the seat with the messenger. The inspected launcher source does not call the Flow Nexus. The topic change adds a root topic (default Core, to become core), a topic kept in the continuation record, and topic-aware titles.

Only A: seen in the launch subflows' transcripts, the five topic flows ran a launcher from a commit that never reached main. This machine's Primary checkout is detached and holds 151 commits found on no remote. Seen: on main the Secondary profile of Psyche is marked unresolved; inferred by A that main's launcher would have refused all four Opus Secondaries. Seen: the launcher picks 18 skills from the Curriculum Nexus, and the messenger store is written under an Orchestrate lock.

Only B: recorded in a Field receipt, the topic change was published as five assembled suites with a remote content match. B did no live probe and keeps this seat's launch facts as attributed, not seen.

Open between them: B's receipt says the published change matches the remote; A saw that the launcher in use is not on main. Whether these are the same code is unreconciled.

## 2. Whether it was done properly

Both found: word-based flow ids and word titles are not implemented.

Only A, seen against your vision:
- ids are still hex, not words, and topicless flows omit core, as in `{ Psyche Secondary 445410 }` and `{ Psyche Primary f5a6e9 }`;
- no flow holds core Primary; the oldest Psyche Primary still has the old title and no continuation record;
- the metaflow record has aspect and layer only as prose, no state, past or queue, and is kept per flow, not per metaflow;
- lineage is lost: two successors have an empty predecessor field;
- no hook reports to Flow, and retirement is manual.

Only B: nothing measured against the vision; B only says the launch evidence it holds is attributed.

## 3. Where the Nexus stands

Both found: Flow sockets exist, and the inspected launcher source does not call them; B established this from that source alone, with no live probe, so it does not establish that no launch touches Flow. The Flow Nexus design (Launch, Wake, Refresh, End, Current over a metaflow record) is a proposal, not deployed. The private Clojure Flow is offline and is not a Nexus; the Rust bridge is a candidate only.

Only A, seen: Flow, a newer Flow, Message-next, Orchestrate, Curriculum (twice), Lojix and a stray debug Flow from a temporary directory all run. The stable Message socket is absent and the legacy message daemon has failed. Version mismatch: the command-line clients on PATH are newer (Flow 0.23, Message 0.19) than the running servers, and the knowledge skill describing the Nexuses names versions that are not the ones running.

Only B, recorded: Astra reports no active native implementation. The Clojure Flow has eleven tests; the Rust bridge five, historical. An earlier continuation exercise proved continuation records, not Flow Start or Replace.

## 4. Why the flows do not use it

Both found: the inspected launcher source uses the direct Herdr, harness and messenger route (B made no live probe, so this bounds the source, not every launch), and the Flow Nexus design is not yet implemented or deployed.

Only A, seen: Flow's code has no metaflow, and its Start request carries no layer or topic. Deployed servers lag the newer source, no hook reaches Flow, and the messenger writes to panes directly. Recorded: the design is unruled. Unknown to A: why the upgrades were never deployed, and why the Primary checkout diverged and stayed unpushed. A did not call Flow's List, which may write, so it does not know whether Flow holds a row for any of today's flows.

Only B: absence of a launcher call does not prove no other component uses Flow, and it does not claim a cause.

Inferred, this seat's: the Nexus is unused because it cannot yet express what a launch needs (layer, topic, metaflow); the unknowns above stay unknown.

## 5. Distillation: topic flows into vision-flow

Target: psyche-skills/skills/vision-flow.md

Removed: none.

Added, as a new section after «Starting flows» and before «Repository and skills»:

    ## Topics and flow titles

    Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

And one line at the end of «Sources»:

    445410 flow

Source: flows/445410/vision/flow.md, entries «The Core topic», «Topic flow titles» and «The title names the topic, Core included» and «Topic names are camelCase expressions» (2026-10-09).

Ruling: land this addition? (a) land, (b) amend, (c) refuse.
<!-- to-the-living:end -->
