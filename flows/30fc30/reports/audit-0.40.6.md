# Audit of the merged Flow tree, 0.40.6

Tree: origin/main-integration-851681 at b202ad9. Audited 2026-10-29 by a tester subflow of { Psyche flow Primary 30fc30 } against vision:flow, vision:messaging, vision:remembering, vision:nexus, vision:datom and the book Flow, whole (flows/30fc30/books/flow-whole.md). Paths are relative to the tree root. A line of vision is named for each defect.

## D0. The tree does not build
`nix develop -c cargo test --workspace` fails in crates/flow-nexus: E0422 store/metaflow.rs:817; E0425 src/tests/repairing.rs:131,134,135 (undefined `root`); E0599 codex.rs:2631,2743, launching.rs:392,975, performing.rs:537, send_tool.rs:1114, waking.rs:1650,1665, lib.rs:271 (missing imports: ConfiguresHerdrCli, BuildsConfiguredEffects, DeclaresSendTool path, ConfigureNexus); E0282 store.rs:5316. No flow-nexus test runs on this revision. The other five crates pass 30 tests. With the imports repaired in a scratch copy: 585 pass, 1 flaky under the parallel run (store::metaflow::tests::unknown_sender_and_expired_lease_do_not_append, metaflow.rs:835, passes alone).
Vision broken: compensation:nix-workflow «Build and deploy reproducible source»; compensation:testing «Expose every durable test through a Nix check».

## D1. The sender carries a flow id
The pane receives `[ Soft.{ Notice { { Psyche core Secondary } e167d8 } Words.«…» } ]`: the sender is `Sender.{ Address FlowId }` (meta-signal-flow ethos/signal.ethos:499, Letter at :506), rendered by delivery/body.rs (witness: the_pane_text_begins_with_the_priority_head, body.rs:312).
Vision broken: vision:flow line «In the chat a flow is named by its metaflow, and the flow id almost disappears from it; the id is for the ledger and for finding the transcript»; the living, 2026-10-29 (flows/787230/vision/messaging.md): «we should know who messaged you without Flow ID»; 2026-10-22 standing order (flows/b7a16a/vision/messaging.md): «no extraneous useless fields … like useless Flow ID fields». Flow, whole proposal 4: a request is its sender, as an address, and its content.
Fix: the sender position is the Address alone; the `Words.` wrapper goes with it (a Body is a String).

## D2. A woken metaflow's queue is not in the first prompt
waking.rs:2521 starts the fresh flow with an empty brief and records `delivered: 0` (:2556-2563); the queue goes in afterwards through Drain (drain_woken, :1658), and a Soft cohort waits for the seat to rest (:2178-2188). Witness: tests/waking.rs a_queued_order_wakes_fresh_then_drains_the_whole_queue (:1265) ends with all four requests still queued; an instrumented run shows no `agent prompt` at all. With a declared purpose the start is two model turns; with none, nothing is ever delivered.
Vision broken: vision:flow «A metaflow asleep is woken … and receives its whole queue, oldest first, in the first prompt»; «so that its start is one model call»; operation.ethos's own comment (Wake «starts a fresh flow that carries it in its first prompt»).
Fix: Wake composes the queue into the first prompt, after the modules and records, and leaves the queue in the same write.

## D3. Machine text that is not datom reaches the prompt
Part headers «Startup message, part N of M …» and the Codex launch brief header «# Flow launch / Harness: Codex / …» (seed/texts.datom:17-32), the Codex developer item `Flow: <id>` (codex.rs:1248-1262), and the launch section's `Flow ID: pending` line are plain text typed into the pane or injected into the thread.
Vision broken: vision:messaging «The message body is a datom … The datom is the whole message»; the living, 2026-10-27 and 2026-10-29 (flows/bf8ae0, flows/2933ce vision/messaging.md): every message injected into a pane is datom, so his are the ones that are not.
Fix: every text Flow puts into a prompt is a datom of a Signal type (a Part, a Launch, an Identity), the living's words being the only non-datom text.

## D4. A Codex flow's system prompt says `Flow ID: pending` for its whole life
launching.rs:385-388 carries the id only when a FlowId was reserved; Codex reserves none (a_codex_launch_reserves_no_flow_id), so the template seed/texts.datom:4 stays `pending` and the id arrives only as the developer item.
Vision broken: the living, 2026-10-21 (flows/c068b8/vision/flow.md): «It should be told what its flow ID is when it starts»; Flow, whole proposal 2: the flow reads its id in its first prompt and its environment.
Fix: for Codex, the id claimed at Bind is carried into the first prompt as datom before the first turn, and the system prompt names no pending id.

## D5. A Codex Soft cohort is settled on the turn/start answer
waking.rs:2331-2379: submit_queued_turn returns the turn/start response and settle_received_cohort marks the cohort Delivered on it (store/queue_delivery.rs:1370-1395, :1504); the eprintln at :2365-2369 says «native USER receipt pending» while settlement happens. Witness: tests/send_tool.rs:2270 settles with a fake app-server whose thread/turns/list is empty, so no USER row exists and the queue slot is gone anyway.
Vision broken: vision:messaging «Inducing an interrupt, placing prompt text, submitting it, and the recipient consuming it are four separate observations. None of them stands for another, and a submission is never a read receipt».
Fix: a Codex cohort is Delivered only when thread/turns/list shows the userMessage equal to the cohort text; until then the attempt is outstanding.

## D6. An Abrupt cohort typed into a Codex pane is settled on pane observation
delivery.rs:1029-1055 settles Presented when Herdr reports the prompt placed and the composer clear; native history (codex.rs:1379 queued_turn_after) is read only for outstanding or uncertain attempts.
Vision broken: the same lines of vision:messaging.
Fix: as D5, the receipt is the turn history.

## D7. A remembering carries no open beads
starter.ethos RememberedFlows carries flow ids alone; no Open variant, no beads. The Psyche core Primary 554e1a was launched today with none.
Vision broken: vision:remembering «A flow's remembering includes the open beads of its address»; Flow, whole proposal 11 (Open.ContentCap).
Fix: Remembering gains Open; the composition adds the open beads of the address to the first prompt.

## Witnessed
Whole queue as one cohort: tests/waking.rs explicit_delivery_hands_over_every_queued_request_in_order; tests/queue_drain.rs a_large_accepted_cohort_reaches_the_native_boundary_as_one_vector. Delivery to a resting awake flow without a further turn end: tests/waking.rs a_request_to_an_idle_awake_claude_flow_is_delivered_into_its_pane; tests/send_tool.rs:2270 for Codex. Claude Flow ID at launch: composition a_launch_carries_its_flow_id_first_in_its_launch_section; herdr::launch claude_environment_preparation_exports_the_reserved_flow_id. Claude transcript datom retrievable: flow-native both_native_paste_shapes_unwrap_to_the_exact_body; claude.rs a_receipt_is_one_exact_main_user_row_after_the_cursor; herdr/launch a_pasted_part_is_read_through_its_wrapper. All of these on the scratch copy with the imports repaired; none on b202ad9 as it stands (D0).

## Order of the fixes
D0 first, on its own commit. Then D1, D2, D3 and D4 together as the first-prompt and message-shape release; then D5 and D6 as the Codex receipt release; then D7. One release, one fix, each with its test seen failing first.
