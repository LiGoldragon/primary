# Heartbeat upkeep: current source/test state

## Coffee-short account
Flow 0.42.1 had task reminders but no sanity heartbeat. Flow 0.44.0 now sends changed-only reminders without counting its own traffic. Tests pass; this flow read the heartbeat, then observed 32.27 quiet seconds at a 10-second period. **Removed 25 lines; added 1,079.** The operator’s full preservation receipt is separate.

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

## Final immutable source/test receipts
Source owner: Field flow Secondary24eb5c; implementation subflow `/root/heartbeat_code` has finished. Earlier audit hand owns no edits.

* **Flow0.44.0:** base `d3ab87ee18b1dd30947d5f0089f5abb4bafa80d5` → pushed `88ae787cdc809822c83b2b77690c8278c74ab938`, branch `heartbeat-24eb5c`, worktree `/home/li/worktrees/flow-heartbeat-24eb5b`. Clean. Held0.43 source was not merged.
* **Meta49.0.0:** base `dba1e407c314dc4b8552e7d9abad1eddd2ea836b` → pushed `4665a3629dd06713122eebd38422b55d904d4ffa`, branch `heartbeat-24eb5c`, worktree `/home/li/worktrees/meta-heartbeat-24eb5b`. Clean. Flow pins matching contract-code commit `9f56b26df724b153226c0d96db7e72b501b210ec`; later4665a36 is documentation only. Ordinary signal remains7b737d9/v38. Matching meta49 clients are mandatory for the new Configuration shape.
* **Remote full check:** `nix build --store ssh-ng://prometheus.goldragon.criome .#checks.x86_64-linux.default -L`, exit0, output `/nix/store/jvxn8d7lmvpsiqwy7kwgqkx6zw6j8ss3-flow-workspace-test-0.44.0`; flow-nexus559 passed/0 failed/6 environment-dependent ignored, workspace/default_start/docs green.
* **Remote package:** `nix build --store ssh-ng://prometheus.goldragon.criome .#packages.x86_64-linux.default -L`, exit0, output `/nix/store/gnnynd78qrrmr7zg9y2na2iilzfv8cs4-flow-0.44.0`. This is the final correctly labelled package, not earlier intermediate0.42-labelled output.
* Production-path tests use the actual durable store, admission and tick operations: quiet startup/two unchanged samples; ordinary admission; generated-purpose queue/count exclusion; one outstanding/coalesced latest; failure keeps baseline; known terminal clearance/unknown receipt hold; sleeping/unknown recipients skipped; disable/deselect/reselect retains unknown outstanding. Root read those tests and the actual durable eligibility method. An unused parallel in-memory algorithm and its self-confirming tests were removed.
* Period validation, typed configuration and atomic ordinary-purpose recording on BOTH admission paths are tested. No simulated tick is called a timed runtime witness.

### Owned line counts
| Repository | Files | Added | Removed |
|---|---:|---:|---:|
| Flow, d3ab87→88ae787 | 13 | 1045 | 19 |
| meta-signal-flow, dba1e40→4665a36 | 6 | 34 | 6 |
| **Total** | **19** | **1079** | **25** |

Counts are actual `git diff --numstat` sums, including tests/generated contract/docs, excluding this Primary report. Net code/source addition1054 lines; no claim of net removal.

### Actual new Memory ledger
All three families begin at version1; existing archived rows retain their shapes.

| Typed record | Table | Family | Schema |
|---|---|---|---|
| StoredMetaHeartbeatConfiguration | flow_nexus_meta_heartbeat_configuration | flow-nexus-meta-heartbeat-configuration | flow-nexus-meta-heartbeat-configuration-v1 |
| LogicalDeliveryPurpose | flow_nexus_logical_delivery_purposes | flow-nexus-logical-delivery-purpose | flow-nexus-logical-delivery-purpose-v1 |
| StoredHeartbeatStanding | flow_nexus_heartbeat_standings | flow-nexus-heartbeat-standing | flow-nexus-heartbeat-standing-v1 |

Absent config means disabled. New purpose-family epoch begins deployment/first use, independently of heartbeat enable; older deliveries are not reinterpreted as newly counted admissions. New standing baselines without broadcast. Durable baseline/outstanding survive reopen and recipient selection churn.

## Preservation and sole Home execution
Source preservation is COMPLETE. Executor Mind core Secondary directly witnessed both source paths/admin at2026-10-31T05:11:59.671774Z and independently verified exact local+origin88ae787/4665a36 retention and clean worktrees at05:41:18–19Z. Both were outside the unrelated75→1 cleanup inventory. Continuation stays the SAME paths; no removal, relocation or new worktree. Source writer finished/quiescent; no source rework remains.

Flow backing `/home/li/primary/flow/.git`; meta backing `/git/github.com/LiGoldragon/meta-signal-flow/.git`. Lock24937 was released on the explicit release-condition-met order; a crossed later preserve-lock instruction was met by immediately reserving the SAME paths as **24947**, no source bytes changed.

Latest explicit PsychePrimary1add4b execution ruling supersedes earlier strict atomic/preaction preservation proof/post-write rollback gates. The SAME eligible Field core/Home operator executes ONE coherent Flow0.44 + matching ordinary/meta PATH/hooks + retained Wispr.12 activation/restart. A bounded closed-socket interval/caller failure-and-retry is accepted; no steady-state mixed pair. No further approval gate is asserted here. Field flow performs no parallel live operation.

Operator postchecks: **24 Awake, 9 queued, 8 Past lists AND same durable rows**. On difference, latest ruling directs restore0.42.1 store+BINARY+matching clients, report LOSS, retain failed-state evidence if feasible. Earlier lossless postwrite rollback requirement is superseded, not pending. Existing source has no reverse migration: restore is an explicitly directed rollback policy, not a claim that postbackup work survives it.

Final artifact/pins/tests/counts sent directly SAME Field core Secondary/Home lane1728, corrected execution support1817; Mind flow copied1737/1821. Home build91557 was reported underway with pins verified and no0.44 runtime yet. This report is not an activation receipt. Existing artifact owner is asked to retain finalgnny in its normal remote registry profile beforeGC; no new profile/hand was created by this seat.

## Actual recipient and quiet-period witness
Existing recipient **{ Field flow Secondary }, run24eb5c**, read these actual Nexus Soft.Notice inputs in its native context:

| Native transcript line | UTC time | Evidence |
|---:|---|---|
| 954 | 2026-10-31T05:47:58.149Z | Awake24→24, WorkingKnown0→Known0, own accepted0→1, ordinary queue0→0, growth+0 |
| 998 | 2026-10-31T05:49:58.029Z | Awake24→24, WorkingKnown0→Known0, own accepted1→3, ordinary queue0→0, growth+0 |

Transcript: `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/30/rollout-2026-10-30T19-26-41-01a18f90-eb7c-7812-b38c-ca624eb5c7a1.jsonl`. Raw records retained in `/home/li/witnesses/24eb5c-heartbeat-client/runtime-heartbeat-inputs.json`. This is recipient input actually read, not merely transport acceptance or a requested ACK. No heartbeat ACK/test reply was sent.

Typed meta Configuration independently roundtrips **Some.{10[{FieldflowSecondary}]}**. The first attempted quiet window was correctly rejected as evidence: a new ordinary registry notice1873 was queued, changing this recipient's ordinary evidence. After that notice/question drained and the corresponding merged heartbeat arrived, the measured quiet window was:

**2026-10-31T05:50:06.603592Z → 05:50:38.876019Z, 32.272427seconds.**

That exceeds three configured10second periods and contains at least two complete configured periods. Start/end matching-meta `Inspect.{ Field flow Secondary }` both exit0 and are byte-identical, stateAwake24eb5c with empty queue. Raw Metaflows snapshots are also retained. No new heartbeat input appeared in the native transcript during the window; no ordinary test input/ACK was introduced. Working-pane-only changes are display-only in this version.

Captures under `/home/li/witnesses/24eb5c-heartbeat-client/`: `quiet2-start-inspect.json`, `quiet2-end-inspect.json`, `quiet2-start-metaflows.json`, `quiet2-end-metaflows.json`, `runtime-044-config.json`. These are recipient-side witnesses, not a claim that this flow independently re-read every private sampler record or the operator's full durable-state preservation check.

## Independently witnessed activated runtime and PATH
At2026-10-31T05:51:55Z, `/proc/132355/exe` resolves to:

`/nix/store/8gv3824gv0nrb6r00r5qs2xfy0inm8q1-flow-0.44.0/bin/flow-nexus`.

Its actual arguments retain `/run/user/1001/flow-042-next/flow.sock`, `/run/user/1001/flow-042-next/flow-meta.sock`, and `/home/li/.local/state/flow-042-next/flow.sema`. Both `/home/li/.nix-profile/bin/flow` and `flow-meta` resolve to that SAME8gv package. Ordinary `--version` prints0.44.0. Meta has no `--version` operation: its exact package provenance and successful new typed Configuration response are the meta-version witness, not invented CLI output.

The Home-built8gv path differs from standalonegnny because Home follows its own nixpkgs input. Field core/Home operator reports verified SAME Flow88ae787/meta code9f56b26 provenance. Root directly witnessed the executable/client paths and behavior; it does not claim to have reconstructed the Home build independently. Standalonegnny remains the source owner's independently tested artifact, not the activated Home closure.

Purposeful authorized final-account Notice sent through activated PATH flow CLI to Mind flow Secondary at05:51:55Z with exact NEXT socket: **exit0, stdout `SendAccepted.{ 2035 Queued }`, empty stderr**. Raw `runtime-044-path-send.json` records executable, query, status, output and runtime exe. This is real decoded reporting traffic, not an ACK requested by the heartbeat.

Operator session/seat/queue preservation remains distinguished: Field core reports24Awake and immediate1queue/Past surface byte-equality; the complete24Awake9queued8Past+same durable-row receipt is not independently witnessed by this seat. Its account also retains an earlier reported21second mixed incident/old transient override before recovery; final matching paths are the direct witness here. No parallel runtime action was performed by Field flow.

## Retention disposition
Standalonegnny availability independently witnessed remotely: NAR `sha256-1K8mE3FgzTRrJqaRb8YjFcBBGMKFl40wLLWp/5Gs2BA=`, size23015928. No verified existing registry-profile identity was supplied. Primary directed recording this evidence, no ad hoc root/profile or broader search, no activation gate. Proper single declarative registry/lifecycle/owner follow-up is separate; no retention implementation was created during this transition.

**Complete here:** source/tests/package, actual changed-recipient native heartbeat, measured quiet window, matching ordinary/meta PATH provenance, purposeful decoded Send. **Separate operator receipt:** complete activation/preservation reconciliation and its incident account. All exact recipient/runtime receipts were sent directly to SAME Field core/Home lane1977/2066 and Mind flow1981/2035. No obsolete approval gate remains.
