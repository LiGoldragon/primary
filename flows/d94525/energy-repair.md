# Energy Codex observation repair
GPT-6.1 Sol; Field core Sol supplied runtime provenance and sanitized provider/readback evidence.
Cause: Flow upgraded to ordinary contract 64 while Energy retained 63, so the rejected handshake stopped turn-end-triggered Codex updates on November 15.
Evidence: journal peer digest -9080287517047382240 equals independently computed contract-64 source digest; contract 63 is 4918182474762796509.
Live baseline: Energy f069745f0d5c79ff612c78a61c1e31067e119114; Flow 37980e10bcb8325d9a68c580e0d22c73061bb267, independently traced by Field.
Repair: energy-nexus ca043ebc25bf9ca429b7639df752e71011c7be97, branch codex-observation-d94525; contract-64 pin, translator 0.5.1 and lock only. No state migration or configuration change.
Gate: remote nix-fast-build against the published revision, checks.x86_64-linux whole, exit 0; 123 tests passed, two existing ignored. Log: /tmp/energy-observation-d94525-gate.log.
Readback: stored November 15 09:36 local sample exists at 62% used; one 14:38 local request returned it while direct provider reported 69%. Query freshness uses observed turn ends, so a broken subscription leaves the cached answer apparently current.
Correction: journal silence never established absent November 14 readings; successful readings are silent. No provider authentication/source failure was demonstrated.
Switch owner: Field core Sol, coordinated slot. Acceptance: subscription acknowledgment, then an advancing Codex reading after an observed turn end. Preserve Memory and configured targets; redeem nothing.
Evidence: flows/374411/energy-runtime-survey/report.md and read-codex-evidence.md. Deployment and live freshness remain pending.
