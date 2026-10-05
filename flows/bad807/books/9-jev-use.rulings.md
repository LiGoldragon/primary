# «Jev in the flow-handling system: where a typed decision helps now»: rulings

## Summary

Every line below is the flow's proposal; none is his word.

1. A Jev Library in ethos: `Call`, `Asked`, `Question` with `Kind.[ Noul Choice Score ]`, `Answered`, `Decision`; the state rendered to JSON only at the network edge.
2. Eight decision points: 2.1 message needs its recipient (Noul, Flow's Vet); 2.2 queued item bears on the flow (Score, Message at enqueue); 2.3 wake, inject or drop (Choice over 2.2's scores, Message at rest); 2.4 seat standing (Choice, Flow on Stopped); 2.5 hand over (Noul over 2.6's topics, Flow at turn end); 2.6 what the living's words are and their topic (two Choices, main flow); 2.7 a skill's aspect (Choice, one batch); 2.8 a proposal's inference (Score, before a book).
3. First build, 2.4 the reaping guide: `flow/Cargo.toml` gains the Jev client crate (which one is held by d66c26's reuse investigation); `flow/crates/flow-nexus/ethos/operation.ethos` gains `Weigh.ReapingState` → `Weighed.Decision` and `Failed.JevRefused`; `flow/crates/flow-nexus/src/performing.rs` performs it; `flow/crates/flow-nexus/src/store.rs` keeps the last Decision and its cost; `signal-flow/ethos/signal.ethos` gains `Weigh.FlowId` → `Weighed.{ FlowId Decision }`. Replace and Retire stay the executors.
4. Second build, 2.1 the message gate, in the same caller: `meta-signal-flow/ethos/signal.ethos` `Vetted.FlowId` → `Vetted.{ FlowId Option<Decision> }`; `flow/crates/flow-nexus/src/delivery.rs` Vet asks the question; `message/crates/message-nexus/src/flow_edge.rs` reads and keeps the Decision. Deliver does not read it until a policy is ruled.

## Rulings

1. The first decision point.
   (a) The reaping guide in Flow: 2026-09-19, b81560, "this is where we're going to start using JEV, the new model that essentially deals with these statistical decisions with data". The flow's recommendation.
   (b) The message gate: 2026-10-04, relayed by d66c26, "a rule again that guides messaging better so that we don't end up getting these noisy messages that wake or disturb flows".
   (c) The living's words sorted and routed: 2026-10-04, "the main failure of machines is their inability to seem to differentiate between content types".
2. Whether Jev guides or decides.
   (a) Guides at every point: each answer a probability a seat or a Nexus records; every executor unchanged. The agreement as it stands: no verdict policy until he rules one. The flow's recommendation.
   (b) Decides where the next turn undoes the act (2.3 wake or inject, the delivery tier); guides where it does not (2.4 reaping, 2.6 records, 2.7 placing, 2.8 proposals).
   (c) Decides at a line he sets for each point, for example a Noul above 0.9 or a Choice whose confidence passes his line: TypeSafe's confidence-gated pattern, `flows/bad807/reports/jev-ecosystem.md`.
3. The cost ceiling per day, summed from each reply's usage.cost. At $0.042 per million input tokens, $1 buys about 24 million tokens, some 24,000 calls of 1,000 tokens.
   (a) $0.10 a day.
   (b) $1 a day. The flow's recommendation: room for every point here; today's message and turn counts are unmeasured.
   (c) $5 a day.
