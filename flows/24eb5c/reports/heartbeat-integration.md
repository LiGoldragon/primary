# Heartbeat upkeep: current source/test state

## Coffee-short account
Deployed NEXT0.42.1 contains deadline reminders but no sanity heartbeat. A minimal configured sampler is now being added in isolated source: it compares recipient evidence, sends only changes, and excludes its own generated traffic. The meta-contract checks pass; Flow tests exposed new-family recognition gaps, corrected in source. Durable baseline/outstanding and actual known-pane sampling are still being completed. **No runtime change or heartbeat receipt witness yet.** Owned final removed/added code counts await the final patch; the runtime remains unchanged.

## Immutable diagnosis
Runtime PID4090634 executes `/nix/store/79pwswrvy664x2aflh3wnawscky9chsz-flow-0.42.1/bin/flow-nexus`. Cutover receipt `/home/li/witnesses/20261031T012056Z-flow-0421-onepass/coordinator-handoff.md` identifies source **d3ab87ee18b1dd30947d5f0089f5abb4bafa80d5**, available in `/home/li/primary/flow` Git objects. Other `repos/flow` and rejected `repos/flow-nexus` trees were not used for implementation.

At d3ab87, `crates/flow-nexus/src/main.rs:158–177` starts send-tool serving, wake recovery, task reminders, signal watcher and sockets. Whole-tree heartbeat/sanity/echo-chamber search found no implementation. `reminding.rs:39–98` handles deadline Task reminders, not changed-flow sanity evidence. Pinned meta contract **dba1e407c314dc4b8552e7d9abad1eddd2ea836b**, generated signal.rs:122–131, has no heartbeat Configure family. Current typed Configuration read succeeded and was retained at `/home/li/witnesses/24eb5c-heartbeat-client/next-config.json`.

The heartbeat is **absent in deployed0.42.1**, not a malfunctioning worker. No positive heartbeat generation/eligibility/admission/delivery/consumption witness is claimed.

## Latest authorized implementation boundary
One configured sampler establishes a startup baseline without broadcasting. Period and recipient selection are typed runtime configuration. Each tick samples authoritative NEXT state. Shared awake count and recipient's own accepted ordinary-message count/ordinary queue length form evidence. Actual known working-pane count is displayed with explicit coverage; heartbeat-induced pane transitions do not confer eligibility when existing correlation cannot distinguish them. No new turn framework, public ACK grammar, ordinary Send wire change or content matching.

* Private Memory purpose `Ordinary|Heartbeat` attaches atomically at admission. Both `accept_tool_send` and `accept_logical_delivery` must record it with the same commit as the logical delivery.
* Count fresh successfully admitted ordinary logical requests once, labelled **messages sent (accepted)**. State the deployment counting window; allocation counters are not message totals.
* Exclude generated heartbeat queue/send/receipt bookkeeping from triggers. Arbitrary machine Order/Notice, including unsolicited ACK, remains ordinary actual traffic. Guarantee: generation/delivery alone cannot sustain a heartbeat; arbitrary conversations are not suppressed.
* One durable evidence record per Address contains last successfully admitted baseline, latest observation, optional outstanding identity. While outstanding only latest coalesces. Immutable native payloads are never rewritten. A later tick can send at most one merged follow-up.
* Baseline advances only on typed successful admission. Failure keeps the previous baseline. Compare raw ordinary queue length, not growth delta; rendered growth is current length minus baseline length.
* Outstanding clears only on existing settled native-input receipt or known terminal disposition. Unknown/read failure remains outstanding. Queue absence is not a receipt.
* Reminder supplies counts and asks only private judgment on echo chambers, increasing jargon/nonsense and ACK answering ACK. It requests no reply/verdict workflow.

## Sources, scopes and insertion points
All following source references are at d3ab87 before patch.

* Ordinary admissions: `sending.rs:319–348`; atomic logical commit `store/logical_delivery.rs:1241–1405`, plus the separate tool fresh-admission commit. Purpose and counter evidence must cover both paths.
* Awake metaflows: `FlowStore::list_metaflows`, `store.rs:5083–5094`, scoped to this NEXT Memory and its State.Awake rows. Never used as a Working proxy.
* Actual known panes: `ReadsHerdrPanes::session_snapshot`, `herdr.rs:434–435,747`; existing `pane.rs:347–359` maps actual working status. Deduplicate bound native pane identities, sample each relevant session once, name missing/unobserved/remote-no-pane coverage. Failed observation is not zero. Working pane state is display-only when causal trigger exclusion is unavailable.
* Ordinary queue: recipient queue membership filtered by private purpose, same definition on both comparison cuts. First baseline has no prior-growth observation. Mixed read views must not be called one atomic instant.
* Existing wake notification: LaunchChanges `store.rs:3153–3190` is a condition variable, not typed eligibility or a message metric.
* Existing receipt: `reporting.rs:166–169` correlated PromptSubmitted; `waking.rs:1240–1262` checks session/digest; `find_receipt` at2316–2382 reads exact Claude input history/Codex queued-turn history; `settle_received` at1210–1237 records and settles it. These prove native input receipt, not model understanding. Actual recipient response/transcript is separate test evidence, not a new production ACK protocol.
* Reuse Flow-origin Soft.Notice admission/wake (`reminding.rs:60–65` pattern). No queue replacement/withdrawal to rewrite submitted input. No recursive dispatch/write-gate acquisition.

## Current implementation receipts
Source owner: Field flow Secondary24eb5c, active implementation subflow `/root/heartbeat_code`. Earlier audit hand is completed and owns no edits.

* Flow active path `/home/li/worktrees/flow-heartbeat-24eb5b`, branch `heartbeat-24eb5c`, base d3ab87. Initial correction commits **f601943**, **7c4e0c2**, **a99c69f**; later edits ongoing. Package version **0.44.0**, beyond held/published0.43; held0.43 changes were not merged.
* Meta active path `/home/li/worktrees/meta-heartbeat-24eb5b`, branch `heartbeat-24eb5c`, base dba1e40; pushed **9f56b26df724b153226c0d96db7e72b501b210ec**, contract **49.0.0**, beyond published48. Configure.Heartbeat and ConfigurationSnapshot carry typed HeartbeatConfig. Matching meta clients are required; ordinary signal remains pinned7b737d9/v38.
* Remote meta command: `nix build --store ssh-ng://prometheus.goldragon.criome .#checks.x86_64-linux.default -L`: reported green, 19 contract tests plus event/greeting/queue/repair suites.
* Four new pure Flow heartbeat tests reported green. Full Flow remote suite initially failed legacy store/config tests because new family IDs lacked recognition mapping; a99c69f adds mappings, rerun pending. Compile/test completion is not yet claimed.
* Root review required corrections to initial in-memory purpose/postcommit update, queue-absence settlement, always-unknown panes and startup-only config. The writer reports atomic durable purpose, terminal-state settlement and live config corrections applied; durable standing and pane sampling remain pending validation. No partial patch is accepted as done.

## Preservation and deployment gate
Orchestrate **24937** reserves both active source paths. Cleanup executor `{ Mind core Secondary }` received direct active-writer inventory **1068**, copied Mind flow Secondary1069; administrative-backing addendum1116. Explicit preserve receipt was requested; no quiescence/transfer was given. Flow backing is `/home/li/primary/flow/.git`, meta backing `/git/github.com/LiGoldragon/meta-signal-flow/.git`. Foreign canonical dirty source is untouched.

Deployment remains unperformed and separately judged. Required before any restart: final immutable Flow/meta revisions, remote package and test outputs, actual schema/new-family ledger and old-store defaults, Memory backup and verified rollback boundary, exact unchanged sockets/store paths and seat/queue/history preservation through the existing runtime owner. An old binary reading a modified store is not assumed safe; rollback may require the pre-upgrade Memory snapshot.

Runtime acceptance after approval: named existing `{ Field flow Secondary }` receives one relevant ordinary change; capture event/time, evidence, typed admission, exact native input transcript receipt. Then at least two COMPLETE configured unchanged periods generate no heartbeat. Also test burst/outstanding coalescing, admission failure baseline retention, unknown receipt/metric handling, unrelated recipient isolation and no generated-only feedback. No synthetic live probe or deployment is authorized by this report.
