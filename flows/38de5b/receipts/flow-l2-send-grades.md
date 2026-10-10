# Flow 0.11.0: exact Send grades, no presentation marker (L2)

An Opus subflow of 38de5b did this on 2026-09-25, landing L2 of `reports/message-in-flow.md`. Fresh clones in the scratchpad (`l2-sendgrades-38de5b`); Orchestrate lock 6598, released before return.

## Revisions pushed (each confirmed by `git ls-remote origin main`)

- signal-flow `cf3648f1e1733857bc5ff472824e2561745589c5`, 4.0.1 → **5.0.0**.
- meta-signal-flow `5926ae78b6d9644db33eeecc6fc458dc9f482422`, 6.0.2 → 6.0.3 (repin only).
- flow `1d7a0e3fb9aab8a16fc18b497a64f8b451cec02e`, 0.10.7 → **0.11.0**. Main had moved to 0.10.7 (8df890b) before I started on flow; the work sits on it, no conflict.

## What was added to the contract (signal-flow `ethos/signal.ethos`)

- `SendOutcome.[ Accepted.FlowId Presented.PresentationReceipt ]` gains `Uncertain.FlowId`: typed, reaction not observed.
- `SendRejection.DeliveryRefused` is replaced by `NotDelivered`. Every `SendRejected` now means nothing was typed.
- `PresentationReceipt.{ FlowId HerdrPaneId PresentationMarker PresentationReadUnixMilliseconds }` becomes `{ FlowId HerdrPaneId PresentationObservedUnixMilliseconds }`. The `PresentationMarker` and `PresentationReadUnixMilliseconds` types are removed.
- `SendRequest` is unchanged: no `Presentation.[ Transport Observe ]` field was added (the report's L2 proposed one). Flow chooses the method itself from the recipient's state: it observes a settled recipient and queues to a working one. L3's grade table still applies (Accepted → Transported, Presented → Presented, NotDelivered → Held, Uncertain → Uncertain).
- Text examples with round-trip tests: `SendRejected.NotDelivered`, `Sent.Accepted.908786`, `Sent.Presented.{ 908786 w1:p3 1727200000123 }`, `Sent.Uncertain.908786`.
- **Version: I took 5.0.0, not the brief's 4.1.0.** The brief set 4.1.0 on the premise of *adding* variants. The change instead removes and renames a variant and a field, which breaks the wire. This repo also bumped major even for an additive change (5ca97ce, 4.0.0). L1's planned signal-flow bump is therefore 6.0.0, not 5.0.0.
- meta-signal-flow imports only FlowNode, FlowId, FlowAspect, PowerLevel, ModelName, HarnessKind and the Herdr and session names, all unchanged. Its own wire text did not change, so it takes a patch. The repin was needed because flow links both contracts.

## Flow behaviour (`crates/flow-nexus/src/herdr.rs`, `lib.rs`)

- Flow snapshots the pane first. If the snapshot shows no ready route, Send answers RouteUnavailable before any prompt, as before.
- **Settled recipient** (idle or done): `herdr --session S agent prompt <pane> <BareInput> --wait --until working --until idle --until done --until blocked --timeout 10000`. This is the same observation messenger-clj uses. Herdr 0.8.2 needs a lifecycle change within 5 s, otherwise it answers `agent_prompt_stalled`.
  - The answer is Presented only when the success reply is `agent_prompted` for the exact pane and the route still matches afterwards.
  - Any other result after input may have been typed is Uncertain.
- **Working recipient**: a plain `agent prompt` with no wait answers Accepted. A Pending flow stays Pending and is not refused; 0.10.x refused it.
- **NotDelivered** covers three cases, where nothing was typed:
  - Herdr's before-input error codes: `agent_blocked`, `agent_not_found`, `agent_not_ready`, `agent_target_ambiguous`, `empty_agent_prompt` and `agent_prompt_failed`. I read these from the Herdr source (`src/app/api/agents.rs` `handle_agent_prompt`, `src/api/wait.rs` `prompt_agent`).
  - A prompt process that cannot be spawned.
  - A route or claim that fails revalidation.
- Any unrecognised failure is graded Uncertain, which is conservative: nothing that may have been typed is ever graded NotDelivered.
- **Promotion**: a Pending flow becomes Active only on a Presented Send.
  - If recording the promotion fails, the answer is still Sent.Presented and the flow stays Pending. It is no longer SendRejected.PersistenceRefused after text was typed.
- **Marker removed**: `presentation_marker`, the `FLOW_PRESENTED_…` append, the pane wait-output and the pane read are gone, along with the atomic sequence. The pane receives the BareInput byte for byte.
- A behaviour change for Active flows: a Send to a settled Active flow now waits up to about 5 s and answers Presented, where it used to answer Accepted.

## Fixtures

The fixture Herdr answers as 0.8.2 does: success JSON on stdout, error JSON on stderr with exit 1. It appends the typed bytes to a file, so the tests compare exact text.

- `observed_send_promotes_a_pending_flow_and_types_only_the_bare_input`: Presented, Pending becomes Active, the typed text equals `bare prompt`, exactly one prompt with the observed argv, and no wait-output or pane read.
- `working_pending_flow_takes_the_send_as_accepted_and_stays_pending`: Accepted, stays Pending, one prompt with no wait.
- `refusal_before_input_types_nothing_and_is_not_delivered`: runs for each of the six codes. Each answers NotDelivered, zero bytes are typed, one prompt call is made and the flow stays Pending.
- `typed_prompt_whose_reaction_is_unobserved_is_uncertain_once`: runs for stalled, timeout, not_running and an unlisted code. Each answers Uncertain, with exactly one prompt and no retry, the text typed, and the flow still Pending.
- `reaction_reported_for_another_pane_is_uncertain_and_keeps_pending`.
- `active_send_to_a_working_flow_is_accepted_without_claiming_presentation`.
- `active_send_to_a_settled_flow_is_observed_presented`.
- Six old tests were replaced: the Pending witness, queued, failed-wait, the two marker tests and the active Send test.
- `grep -rn "FLOW_PRESENTED\|presentation_marker\|PresentationMarker\|DeliveryRefused\|wait-output --match"` over the flow tree (excluding target and .git) returns nothing.
- Two other markers remain in the crate. Both belong to Start and are outside Send: the launch receipt footer `LaunchReceipt::MARKER` (`FLOW_LAUNCH_RECEIPT_V2`) and the `flow-id` claim-file marker. L2 does not touch them.

## Checks

- Tests:
  - signal-flow: 9 before and 9 after (the send test was rewritten), all passing.
  - meta-signal-flow: 5 passing.
  - flow before, on 0.10.7: 6+3+102+1+1. After: 6+3+103+1+1, 0 failed.
- `cargo clippy --all-targets` on flow: 0 warnings. On signal-flow, the two warnings from the generated code, "large size difference between variants", were already there before the change.
- `cargo fmt --check` is clean in all three repos.
- Local `nix build` (`--option builders '' --option substituters https://cache.nixos.org --option max-jobs auto`) passes: `/nix/store/1b5kxjs2r0zf1czh8z7mzdm2vg795fyr-flow-0.11.0`. Its `flow-nexus --version` prints `flow-nexus 0.11.0`. The first attempt failed because the prometheus builder and cache timed out.
- Not deployed. No live Send was made: the vision forbids probe sends. Field's deploy step activates it.

## Residual

- If the recipient turns to working between Flow's snapshot and Herdr's prompt, Herdr skips its effect gate. The answer is then Presented without a fresh reaction. The window is only that short gap.
- A scratch-clone slip: I ran `git stash` and `git stash pop` once inside my own signal-flow clone to compare clippy output before and after. It never touched primary.

## Sources

- `reports/message-in-flow.md` L2; the messaging skill (grades); messenger-clj `src/messenger_clj/core.clj:214-226`; herdr source `/git/github.com/herdrdev/herdr` (`src/app/api/agents.rs`, `src/api/wait.rs`, `src/cli.rs` `print_response`, `src/cli/agent.rs`).
