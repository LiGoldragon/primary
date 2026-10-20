# Flow's tests: references (unrendered)

Asked by the living. His words, direct speech 2026-10-19: "I don't really care that it has 400 tests passing. I bet you 399 of those tests are absolute fucking garbage tests. I don't really trust tests. I think thinking machines pretend to do good work by adding tests that don't fucking mean anything."

## Audit (flow origin/aa034f-next 2c390fb)
- 433 #[test] (408 in flow-nexus). 6 #[ignore]: store.rs:8809 and :10546 (need old stores), tests/send_tool.rs:958, :1090, :1239, :1351 (need a scratch codex app-server); the only real-system witnesses, never run.
- flake.nix: 156 checks per system; 151 are exactTest (entries at lines 194-495) re-running tests `default` (cargoTest --workspace) already runs; 2 run one test under two names (tests::a_flow_whose_pane_left_herdr_is_listed_exited_and_keeps_its_row, tests::a_receipt_that_contradicts_the_launch_rejects_it).
- Sample of 61 tests: ~64% meaningful (internal logic vs scripted fakes), 18% tautological, 13% fake-bound, 5% duplicate.
- Both of 2026-10-19's real failures passed every test:
  1. Codex first turn before Herdr attach: the fake in crates/flow-nexus/src/herdr/launch.rs (~2904-2925) returns `agent start` instantly; real Herdr 0.8.2 (src/cli/agent.rs:548-610) waits for idle. Two flake checks assert the broken order: codex.rs:2389 (a_codex_thread_is_opened_lean_and_given_its_first_turn_before_attach), herdr/launch.rs:3826 (a_codex_first_turn_given_before_the_tui_attached_is_observed).
  2. Remote Control name: only argv text echo checked (herdr/launch.rs:3556-3600).
- Fakes contradict real Herdr: report-metadata prints nothing on success (herdr src/cli.rs:748-760); every fake prints {"result":{}}; Flow parses with run_json (herdr/launch.rs:1556-1566 and 1608) -> PaneLabelRefused live (a shim currently masks it). run_status already exists in the RunsHerdr trait (launch.rs:548).
- Tautological examples: codex.rs:2303 and 2062; lib.rs:1877; lean.rs:225 and 263; version echo main.rs:381 (crates/flow-nexus/src).

## Context witnessed
- psyche-context origin/main spirit/core.md lines 33-35 (disconfirming evidence; evidence by origin); intent/main-flow.md line 25 ("a thing is verified only by a witness"); vision/messaging.md lines 25-28 (an interrupt witness is not a delivery witness).
- herdr 0.8.2 on this host: `herdr pane read`, `pane get`, `workspace get` exist.
- Unknown: how a script starts a flow (Start is a typed Signal request; no plain CLI); what makes the fake agent idle (the TUI attach, presumed).
