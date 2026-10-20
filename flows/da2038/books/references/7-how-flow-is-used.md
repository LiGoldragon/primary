# References: How Flow is used

Sources read (not shown in the book):

- Flow main 67b80b3 (0.35.11): crates/flow/src/main.rs, crates/flow-meta/src/main.rs (tests hold the CLI datoms), crates/flow-nexus/ethos/send_tool.ethos and src/send_tool.rs, src/waking.rs (WakePolicy), src/composition.rs (RendersQueuedWork), src/store/metaflow.rs (Lock, Deliver), src/metaflow.rs (Identify, peer checks), DESIGN.md, UPGRADES.md.
- signal-flow 6a49664: ethos/signal.ethos, tests/contract.rs. meta-signal-flow a918b7d: ethos/signal.ethos, tests/contract.rs.
- message-test: checks/message-flow-not-message.nix, message-flow-queued.nix, message-flow-up.nix (Lock, Deliver, Identify shapes; Current, Metaflows).
- Production evidence, read only: flow-evidence/42265e/direct-starter-retry-20261017/first-tool-03510 (report.md, proof/*launch-status.datom, refresh.stdout) and model-identity-reconciliation (report.md, models-intent.json, configure-models.stdout, configuration-after.stdout).

Records the proposals draw from:

- P1 vision/flow.md, lean flow: flows/da2038/vision/flow.md, "A lean flow: every removable part of the startup is a named module; a metaflow row sets which are removed by default, a call overrides" (psyche, STT, 2026-10-16, relayed by Psyche Core Secondary).
- P1 three repositories: flows/da2038/vision/flow.md, "Context modules, raws included, live only as raw modules in the three aspect context repositories; nowhere else, enforced by how the code is written" (2026-10-16).
- P1 injection: flows/da2038/vision/flow.md, "The flow starter injects every context module's text into the prompt, queued across messages if needed, naming them as the skills given, not to be reloaded" (2026-10-16).
- P2, P3: the living's request to Flow Secondary, in this flow's transcript, to review the knowledge on Flow (command lines, examples, how it is used). Existing module: mind-context/skills/knowledge-flow.md (dated observations of 0.24, three paragraphs, not touched).

Findings kept outside the book: Flow's README still shows `flow --system-modules …` and `flow 'List.{}'`; the 67b80b3 CLI refuses the first (test a_start_carrying_a_source_path_or_a_flag_is_refused) and signal-flow 20 has no List query. Message's test 17 comment says an Identify from a plain client is answered; Flow's dispatch_metaflow_peer refuses it NotMessage. Local cargo is disabled in this environment, so no example was parsed by running Flow's types; each example matches, whitespace-normalised, a test fixture or a production reply, except the placeholders listed in the return note.
