# Field Low refresh handoff — GC and twelve-seat state

This is the concise source handoff for the receipt-first successor of Field Low
`2fe3f1`. Its predecessor remains live and crossover-only until the successor
has native context, identity, routing, and explicit acceptance receipts.

The current native is `01a0c019-fedc-7ad3-abfe-c3f2fe3f13f5`, Herdr
`messaging-build/wZ:p2/term_65bee70e7730341`, HM Flow `2fe3f1` under the
display name `field-terra`. The name repair did not create a new Flow.

GC completed pane-only closures of `wD:p1` (closed `b81560` shell), `wD:p2`
(exited `c8d79f` predecessor shell), and `wP:p1` (interrupted unbound remote
Sol shell). Their Flow records and transcripts remain. `b81560` is permanently
no-resume. No remaining safe ghost candidate was observed.

Refresh queue, one seat at a time: this Field Low successor, Field Ultra Low
`c88918` (70%), Field Medium `9ddcbc` (68%), Field High `1cb440` (45%), then
Psyche Low `0625c3` (60%, route rebind required). No batch controller and no
predecessor retirement or route withdrawal is authorized.

Mind Low `e798f3` and Ultra `23d977` replied to fresh liveness probes after
about 303 seconds, proving responsiveness with queue latency; do not relaunch
them. Mind Medium needs an authorized typed Sol profile. Psyche Ultra needs a
new Haiku main seat from Psyche Medium's corrected authority; it must remember
`b80e55` at depth one. Do not infer Haiku's delegation ceiling.

The third priority—message reception while bindings change—remains deferred
until the lifecycle is stable.
