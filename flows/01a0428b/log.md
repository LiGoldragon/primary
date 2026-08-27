# Flow log

Audited recent Flow and Codex goal status and determined how the current remembering protocol behaves when Codex sessions are archived.

Settled:

- The checkable recent window is the connected research tree rooted at Codex `01a04236` plus this audit root and its Terra worker: seven Codex threads and, before materializing the worker record, four related Flow artifact identities.
- No native Codex goal object occurs in that window. Session aims, Flow records, and Beads are separate kinds of state.
- Codex archive moves plain rollout JSONL and hides it from default active-list surfaces; it neither compresses nor deletes it. Flow-artifact remembering remains compatible, while transcript-depth remembering is conditional on archived discovery/search.
- Three distinct child threads share the first eight UUID characters `01a04237`; a compact reference cannot safely use the current eight-hex Flow convention as its sole identity.
- The Terra report and witness are materialized under `flows/01a04290/` by this parent because the worker's higher-priority context prohibited file edits.

Remembered: 01a04236, 01a04237, 01a042376379 — depth 2. The related research is complete as investigation/design, not as an authorized retention implementation; the last responses and supporting reports/witnesses establish the archive boundary and remaining policy questions.

Open:

- The living has not yet ruled the anatomy of the compact-reference transition: identity, resume behavior, search/indexing, retention authority, expiry/deletion, holds, privacy, backup, and recovery remain design questions.
- The status of the separate visual/hub publication child `01a04285` remains unverified.

Web-reporting procedure recovery:

- Remembered Codex `01a04236-2355-7d20-94aa-e3b814a52b32` at transcript depth through a Luna investigation subflow; `01a04285-f8f1-7202-8bbd-9131fba65747` was its image/social-card child, not the procedure source.
- The explicit requirements were ratio-based visuals, remote publication through the hub, and later placement in a Codex-only skill.
- The living clarified that Terra is for report writing only. Luna recovered the evidence; Terra wrote the recovery report from that fixed evidence without investigating.
- The witnessed build/hosting sequence is recovered in `reports/codexWebReportingProcedureRecovery.md`; implementation choices and open policy questions remain outside canon.

Open for skill anatomy:

- Report schema and navigation, later-report update/version flow, post-deployment browser QA, URL collision/reuse, rollback, ACL policy, and whether private access is a default or a per-report decision.
