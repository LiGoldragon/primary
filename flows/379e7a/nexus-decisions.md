# Nexus integration and deploy — decisions (379e7a, Opus subflow)

## 2026-10-19 17:55 — Base the integration on aa034f-next
- Found: aa034f-next (042df6d, 0.35.23) already carries aa034f-rules (eabe7f2) and aa034f-sleep (b972355); all branches share base dcb63e6 (0.35.21), which descends from main 67b80b3.
- Decision: branch 379e7a-nexus from origin/aa034f-next, merge aa034f-integration (bae1fcd) and 4201a3-report-metadata (647689a), bump to 0.35.24.

## 2026-10-19 17:55 — Leave aa034f-books out
- Found: 40f87a3 pins a different signal-flow 23.0.0 (ce1f761d) and meta-signal-flow 29.0.0 (dc165fdf) than aa034f-next (c7dcc074, 2b03b506), upgrades the events table, and makes the Claude Stop hook block turn ends (including "Flow unreachable blocks the Stop").
- Decision: not merged. Two incompatible 23.0.0 contracts cannot both ship; a Stop-blocking hook is a behaviour change outside the requested fixes and can trap every Claude seat if the Nexus is unreachable.

## 2026-10-19 17:55 — Message must repin with aa034f-next
- Found: aa034f-next pins signal-flow 23.0.0 c7dcc074, which removes `End.Address` ahead of `Current`, `Metaflows` and `IdentifyThread` in the Signal query enum and removes `Ended`/`OffRoute` refusals. Message main (fbbf731, deployed as message 0.20.0) pins signal-flow 22.0.0 e6ccbddb and maps `Ended`/`OffRoute` in message-nexus. A 0.35.23 Nexus would read a 22.0.0 Message's queries with shifted variants.
- Decision: repin Message to signal-flow c7dcc074 / meta-signal-flow 2b03b506, drop its Ended/OffRoute mapping, and deploy it together with Flow.

## 2026-10-19 18:05 — Repin Message's contracts too (cascade)
- Found: signal-message 14.0.0 (f518214) and meta-signal-message 0.13.0 (f1ddba8) pin signal-flow 22.0.0 and flow-ethos 9e417bb; Message would link two signal-flow copies.
- Decision: branches `379e7a-flow-23` in signal-message (15.0.0, ff8d215), meta-signal-message (0.14.0, 2114534) and message (0.20.1); each only repins. Lockfiles resolved with nixpkgs cargo `update -p` on Prometheus (the profile cargo there refuses everything; resolution is not compilation).
- Cut corner: signal-message keeps `Refused.Ended` and `Refused.OffRoute`, and Message's operation keeps `Failed.Ended`/`Failed.OffRoute`; they are no longer produced. Removing them needs a regeneration pass; left for the Message owner.

## 2026-10-19 18:05 — Flow merge resolutions
- Branch 379e7a-nexus: 8975960 merges aa034f-integration into aa034f-next; 80d8c29 merges 4201a3-report-metadata. Version 0.35.24 (Cargo.toml, Cargo.lock workspace crates, flake.nix). UPGRADES.md gains a 0.35.24 entry carrying the Codex-attach and report-metadata notes.
- tests/waking.rs: the first-turn-send test keeps integration's launch-order assertions and drops its `refresh` step (Refresh is gone in 0.35.22); doc comments lose "Refresh'd". flake.nix keeps both sides' exactTest entries.

## 2026-10-19 18:15 — be70e0a installed as a rebased overlay
- Found: ~/.local/bin/hm-* are copies of the 0.4.0 store wrappers with /home/li/.local/share/messenger-overlay-4201a3 ahead of the jar; that overlay's public.clj would shadow be70e0a's public.clj. The overlay's Unidentified fallback is still needed while flows born before the 0.35.21 store live.
- Decision: messenger-clj be70e0a built remotely (/nix/store/nfl9f0gk…-messenger-clj-0.4.0); new overlay /home/li/.local/share/messenger-overlay-379e7a = be70e0a's public.clj plus the Unidentified fallback, be70e0a's flow_bridge.clj plus the relay guard, the relay scripts re-pointed; wrappers regenerated from the be70e0a store wrappers with that classpath. The 4201a3 overlay stays for rollback.
- Cut corner: the overlay additions are still not in messenger-clj source.

## 2026-10-19 18:28 — Approval pipeline owns the refresh-due row and its executor at rest (approval subflow)
- Found: retraining (approval pipeline) and the 2d9fbb6 P4 threshold refresh need the same act: a flow marked due, closed at its next rest instead of drained, its queue waking a fresh flow composed from the deployed modules.
- Decision: branch 379e7a-approval (worktree /home/li/worktrees/flow-379e7a-approval, from 379e7a-nexus) adds store table `flow_nexus_refresh_due` (FlowId → cause `[ Retrain.Commit ]`) and the executor in `waking.rs` settle_rested: a due flow resting by Herdr (Idle/Done) or by its Codex thread is closed, recorded Stopped, its metaflow Asleep, and woken fresh when work is queued. P4 adds a `Threshold` cause and the message hold on the same row; it does not add a second executor. Design: flows/379e7a/approval-pipeline.md.
- Decision: no meta-signal-flow change on this branch. The pipeline's setup values (psyche-context checkout, deploy executable) enter through the Start datom as `Option<LandingWatch>`; the deploy executable is the module-deploy work's product, run as `Deploy.{ Repository Commit }`.

# Flow vision 2d9fbb6 (P2, P4, P5, P6) — decisions (379e7a, Opus subflow)

## 2026-10-19 18:40 — Base and worktrees
- Found: 379e7a-nexus (fb5251b, 0.35.24) exists; the shared checkout /git/github.com/LiGoldragon/flow carries another flow's uncommitted work.
- Decision: branch 379e7a-vision from 379e7a-nexus in /home/li/worktrees/flow-379e7a-vision (orchestrate lock VisionImplementation); contract work in separate worktrees of meta-signal-flow. Rebase onto 379e7a-nexus as it moves.

## 2026-10-19 18:40 — P2: a start is one model call
- Found: modules are already inlined by Curriculum (system prompt + first USER message, "These are your skills, given here; do not reload them."); witnessed in e9ca21's transcript: one 59 KB user row, then the first model call. The gap is the oversize path: when the first USER message does not fit one message, each part is submitted only after the seat answered the one before ("answer only that you are waiting"), one model call per part, for both harnesses.
- Decision: parts go back to back with no answer between them. Claude: every part but the last is pasted into the composer with no submit; the last is submitted with them, one user message. Codex: every part but the last is appended with `thread/inject_items` (no turn; present in the deployed 0.161.0-alpha.2), the last starts the first turn. The "wait for part n" headers go; the receipt reads one submitted message.

## 2026-10-19 18:40 — P4: refresh threshold per model, no handover
- Decision: meta-signal-flow 30.0.0, `ConfigureThreshold.{ ModelName Refresh.Integer }`, one per model (Layer and Handover gone). Compaction is judged against the flow's model's threshold.
- Decision: a flow whose last measured context is at or past its model's threshold is given no new message: Drain and the hand-over to a resting seat keep the request queued, and meta Deliver is refused `PastThreshold`. When the seat rests, Flow closes its pane and records it Stopped and the metaflow Asleep in the same event (reaped), then wakes the metaflow fresh if work is queued; the queued work is the successor's first prompt. With nothing queued the metaflow stays Asleep and the next Order, Question or living's words wakes the successor. The metaflow is held in the waking set while the refresh runs.
- Decision: Codex context is measured from the app-server's `thread/tokenUsage/updated` (`last.inputTokens`), recorded as Claude's is.
- Values (deployed through CriomOS-home's flow-deployment): every Claude model 200000, every OpenAI model 150000. Source: the living, d68c82 vision/flow.md, 2026-10-14: "at 150,000, 160,000 tokens on OpenAI's models, we're seriously looking at refreshing, and the same for Claude at 200,000."
- Message pins meta-signal-flow for types only; its live path uses ordinary Lock/Deliver, so 30.0.0 does not break it at runtime. Its pin goes stale.

## 2026-10-19 18:40 — P5: presentation composed by Flow
- Decision: Flow appends one fixed line to every first prompt and to every hand-over whose requests include the living's words (Psyche, Psyches): end the turn with a presentation. A message from another flow gets no line.

## 2026-10-19 18:40 — P6: compaction during continuous work
- Decision: a compaction the harness made on its own (Claude transcript `compact_boundary` with trigger auto; Codex `contextCompaction` item in a turn Flow did not ask to compact) is continuous work. Flow logs a warning, records the compaction once (keyed by flow and boundary), and starts an investigation: the configured Investigation seat (meta `Configure.Investigation.{ Address SystemModules UserModules HerdrSession }`) is started fresh with the investigation as its brief, or, when Awake, handed it as a queued Order (sender Unknown: SentBy has no Flow variant; adding one changes flow-ethos and every contract pinning it).
- Deployed Investigation seat: { Psyche compaction Tertiary }, Psyche Tertiary modules from config/main-flow/psyche.edn, its finding to Psyche core Secondary.
- No signal-flow change: no hook Event is added; the Claude transcript is read at each Report the flow's hook sends, from the last offset read.

## 2026-10-19 18:32 — BLOCKER: Psyche book Secondary successor cannot start
- `flow-start Psyche book Secondary -p 7cd214` (and `Book`) refuses: "no single declaration for Psyche book Secondary in /home/li/primary/config/main-flow/metaflow". No Psyche-book-Secondary.edn exists in the working tree or in git history (7cd214 was born without one). Needs: a declaration (modules and raw-psyche-paths are the living's/Core's choice) or a ruling to copy Psyche-Ethos-Secondary.edn with topic book. Also no handover.md in flows/7cd214. Held b7d1ce43 / cdfe8dc4 untouched (not found in any store searched; hm-repair needs a live flow).

## 2026-10-19 18:55 — Nexus architecture (send subflow, lock 23959 NexusSend)
- Found (code read, flow-nexus caller.rs + herdr.rs:661): a Claude seat in Herdr's default session carries only HERDR_PANE_ID; Flow places it by walking to its Herdr server ancestor, recognised by comparing executables with `herdr` resolved on the Nexus's PATH. The deployed unit's PATH starts with ~/.local/bin, where 4201a3's shim `herdr` (a bash script, 15:28) resolves first, so no ancestor ever matches: ResolveCaller answers CallerUnknown and Identify Unidentified for every Claude seat (witnessed: `flow 'ResolveCaller.None'` from 379e7a → CallerUnknown while Flow holds 379e7a Active at w3G:p1). One cause of Unidentified; the synthetic-id Bind of short-lived hm-register processes is another candidate (not witnessed).
- Decision: the Herdr server ancestor is recognised by listening on a listed Herdr session socket, not by its executable path, so no PATH or shim can break it again.
- Decision: vision/flow.md:40 ("Flow ... is used raw to send messages, until Message sends through Flow's socket") — flows send through Flow's ordinary socket: `flow 'Send.{ Address.{ Mind core Secondary } Soft.Order.«...» }'`. Message stays deployed, out of the flows' send path; whether it re-enters is a question for the living.
- Decision: signal-flow 24.0.0 (branch 379e7a-send, 8796628) appends Send, Launch, BindSeat, Message.[ HardAbrupt MiddleAbrupt Soft ], Refusal.OffRoute, StartRejection.Undeclared. Append-only: no discriminant moves and no earlier type changes, and neither Flow nor Message checks the contract greeting, so Message 0.20.x (signal-flow 23) keeps working unrepinned.
- Decision: meta-signal-flow 30.0.0 (branch 379e7a-send, 4dcbfa8) appends Configure.Metaflows.[ { Address SystemModules UserModules } ]; the snapshot carries it. Conflicts by number with the VisionMetaContract branch's 30.0.0: whichever lands second renumbers to 31.0.0 and merges.
- Decision: topic-context, raw-psyche-paths and first-prompt-template of config/main-flow are not modules and are not declared in Flow; a Launch's brief carries what a caller wants said. Listed as a question for the living in nexus-architecture.md.

# Messenger Unidentified — decisions (379e7a, Opus subflow, lock 23947 FlowCallerIdentify)

## 2026-10-19 18:47 — Cause, witnessed
- Witnessed: `flow 'ResolveCaller.None'` from 379e7a's pane → `CallerUnknown`; the same call with `HERDR_SESSION=default` in its own environment → `CallerResolved.{ 379e7a Psyche Medium claude-opus-5-5 }`. Flow holds 379e7a Active at w3G:p1 (`ResolveRecipient.379e7a`). The Nexus unit's PATH resolves `herdr` to /home/li/.local/bin/herdr (4201a3's shim, 15:28); the Herdr server (pid 4957) runs /nix/store/9x03…-herdr-0.8.2/bin/herdr. Flow 0.35.21's walk compares those two and never matches, so every pane-identified sender is Unidentified to Message.
- Witnessed: the 18:09 relink of ~/.local/bin/hm-* to the store messenger-clj 0.4.0 (vj6pcq, via activate-messenger-clj) dropped 4201a3's overlay, whose guard sent `Current.Awake.flow-…` targets on the pane route and whose relay bound senders through Flow `Bind`. Inference (when Mind core Secondary became Awake.flow-…17 is not recorded): that is why ca28a4's 16:46 send to Mind core Secondary was Transported and 379e7a's 18:26 send went to Message and was refused.
- Read in code (fb5251b waking.rs drain_awake, store/metaflow.rs): Mind core Secondary (Awake.flow-…17) and Mind context Secondary (Awake.flow-…2d) are relay `Bind`s of dead processes with no flow row. A request Message delivers to them is `Queued` and never typed: drain_awake finds no node, and the metaflow is not Asleep, so no wake runs.

## 2026-10-19 18:47 — Fix: Flow 0.35.25, branch 379e7a-identify 6db1f10 (on fb5251b)
- Decision: the Herdr server ancestor is the process listening on exactly one listed session socket; `herdr_binary` and the fixture's `server_binary` are removed. Test `tests::a_pane_id_names_the_session_its_server_serves_whatever_herdr_path_names` (the fixture's herdr CLI is a script, not the server binary, and a non-server shell sits between peer and server). Negative control: the same test against the old walk fails with `left: None`, the production symptom.
- Decision: a binding ends with its process. A metaflow Awake as an id with no flow row, whose recorded binding's process no longer runs, is forgotten (metaflow, binding, lock retracted in one write → `Current.Unknown`) when nothing is queued and no past id names a flow row; otherwise it is rested Asleep with its work kept. `Current` rests before answering; the Nexus start already rests every metaflow. Tests `tests::waking::an_address_held_only_through_an_ended_binding_is_forgotten`, `tests::waking::an_ended_binding_holding_work_rests_asleep`.
- Witness: remote builder, workspace tests 434 passed 0 failed; fmt, clippy -D warnings, no-free-functions, no-inherent-methods, three exact checks pass. Package /nix/store/zwmmr9im…-flow-0.35.25.
- Overlap: NexusSend (23959) holds the same caller fix uncommitted in /home/li/worktrees/flow-379e7a-send; 6db1f10 carries it committed and tested.
- Hand-off: 6db1f10 descends from fb5251b. Deploying it is a pin bump in the LocalBinEradication Home worktree: flake.nix:122 flow.url, checks/flow-service-path/default.nix:28 rev, flake.lock. Home's declared herdr is the same store path the running server uses (9x03…, evaluated), so with 0.35.24 alone identification works again once ~/.local/bin leaves the unit's PATH, but sends to the two Mind Secondaries would be Queued into nothing; 0.35.25 makes them Unknown, so hm-send takes their live pane routes.

## 2026-10-19 19:10 — One executor for a refresh at rest (approval subflow)
- Found: P4 (18:40) and the approval pipeline (18:28) both close a seat at its rest, Stopped and Asleep in one event, then wake it fresh when work is queued.
- Decision: 379e7a-approval's executor is `refresh_at_rest` in waking.rs, reached from `settle_rested` when the flow is due (`KeepsLandings::refresh_due`); it answers `AtStop::Refreshed(Address)`, and `settle_stopped` wakes the metaflow once the gate is released. A Claude seat is closed only when Herdr shows it Idle or Done (a main turn that ended under running background agents shows Working). P4's past-threshold test is a second reason for the same predicate, not a second close path; whichever branch merges second unifies them.
- Decision: the approval pipeline's Order and reports are sent as Psyche core Secondary (SentBy has no Flow variant), the same constraint P6 names.

## 18:49 STOP — order from the living, overrides every brief of 379e7a
No test sends to every live Secondary, and never any send that wakes a Fable flow (any Primary) for testing. Witness messaging with ONE send to a flow that needs that message anyway (Mind core Secondary only if it is carrying real work for it), or to a Quaternary/Haiku test flow started for the purpose and ended after. No broadcast, ever.

## 2026-10-19 19:20 — Flow main is 0.36.0 (approval subflow)
- Flow main fast-forwarded fb5251b → 7d9ecbd (Flow 0.36.0, the approval pipeline). Checks on prometheus: clippy, fmt, no-free-functions, no-inherent-methods, and the workspace tests (399 lib tests, 6 new) pass. The vision, send and identify branches rebase onto it.
- Breaking for every deployment: the Start datom has a fourth position, `None` or `Some.{ ContextRepository DeployBinary }`; CriomOS-home's ExecStart and initialize-declared-flow's configure-only start must write it.

# Skills from the one pin, topic binding (379e7a, Opus subflow)

## 2026-10-19 18:50 — Seat decisions recorded as given
- Binding: every topic metaflow loads its vision-<topic> module and its dependencies; every Flow-topic metaflow also loads vision-subflows and vision-flow; Psyche core Secondary and every Field metaflow also load vision-criomos. Topic-less modules are installed as skills as well.
- Skills: every psyche-context vision/intent/spirit module and every mind-context/field-context module is a skill in each harness's skill directory, generated by a Nix derivation from the single pinned cohort and activated through CriomOS-home. The five committed trees leave Primary; the Primary change is staged in a worktree for the standing committer.
- One pin: psyche-context is pinned once, at CriomOS-home primary.inputs.psyche-context; Primary flake.nix and shared.edn hold no revision of their own.

## 2026-10-19 18:50 — How the decisions were applied
- Generator: CriomOS-home packages/context-skills (babashka), the retired Curriculum projection's rendering (five surfaces .claude .agents .codex .pi .opencode; {% if %}/{% raw %} directives; user-only → Claude disable-model-invocation and Codex agents/openai.yaml; OpenCode name line). Module types as Curriculum's registry: vision intent spirit knowledge inquiry compensation role raw; mind-context evidence/ is not a module type and is not installed.
- Home: modules/home/profiles/min/context-skills.nix links each surface to ~/primary/<surface>; option criomosHome.contextSkills.enable defaults to criomosHome.curriculum.enable (true for li on ouranos in CriomOS), so no CriomOS change.
- Collision: CriomOS sets home-manager backupFileExtension "backup", so if the Home deploys before the Primary removal lands, each tracked tree is moved to <surface>.backup and the link placed; activation does not fail. The shared checkout then shows the tracked files deleted until the committer lands the removal.
- Binding applied only where vision-<topic> exists exactly: Chronos, Ethos, Flow, Nexus (Psyche); flow (Mind, + vision-subflows); vision-book already reaches every aspect through its system defaults, so Mind books and Psyche book need nothing. No exact module, left unbound: Psyche Communication, Spirit, Core (P, T); Mind Core, context, Prototyping; Field Illustrator, Publisher beyond vision-criomos.
- shared.edn :repositories removed (it was a second pin, read only by launch-config validation and an uncalled system-module reader). That reader now reads the installed skill tree.
- Primary flake: context inputs carry no revision; flake.lock set to the CriomOS-home cohort (psyche 2d9fbb6, mind e3fcd4f, field bc5fa7c) for Primary's own checks.
- Untracked declarations in the shared checkout: Field-Core-Secondary.edn and Field-Core-Tertiary.edn copied into the worktree with vision-criomos added; Mind-Core-Tertiary.edn (no topic module) and Psyche-Book-Secondary.edn (lock 23941, sibling) not taken.
- Ordering hazard: Primary launch-config before this change dereferences shared.repositories per aspect, so a flow-start packaged from Primary a459999f (CriomOS-home 379e7a-localbin) fails once the shared checkout carries the new shared.edn. That package's primary pin must move to the landing commit before or with it.

## 18:50 379e7a: deploy ordering (for the single ouranos deploy)
CriomOS-home 51cff7f5 (context-skills generator, psyche-context 2d9fbb6) is on main: include it. Primary change (worktree /home/li/worktrees/primary-379e7a-skills, branch 379e7a-skills: skill trees removed, bindings, shared.edn without :repositories) must land in Primary BEFORE or WITH the deploy, and the packaged flow-start's primary pin must move to that landing commit; otherwise launch breaks. Lock 23956 holds both worktrees until the Primary landing.

## 2026-10-19 18:45 — Home pins messenger-clj a7a40d1, not be70e0a
- Found: while this work ran, CriomOS-home main gained 5a52224e "Pin guarded messenger stale-pane migration" (messenger-clj a7a40d1, which contains be70e0a), plus Curriculum and context pins.
- Decision: CriomOS-home b858226f pins only Flow fb5251b and Message 975beac on top of that main; the messenger pin stays a7a40d1. The installed wrappers follow Home: /nix/store/8ynapd3j…-messenger-clj-0.4.0 (a7a40d1) with the 379e7a overlay rebuilt on a7a40d1's public.clj. be70e0a is installed as part of a7a40d1.
- Deployments built from that Home source (getFlake + callPackage of packages/flow-deployment and packages/message-deployment; the flow-service-path check evaluates the same flow-deployment derivation qk2qsy…): flow-deployment ag4n7k5x…, message-deployment 80ka6c10…. Checks flow-service-path, message-service-path, messenger-clj-package pass (generated user-environment inputs for ouranos).

## 2026-10-19 18:50 — Switch
- Rollback record flows/379e7a/rollback-20261019T185048.txt; old wrappers, herdr shim, GC roots for old and new deployments, and a copy of ~/.local/state/flow-03521 taken with flow-nexus stopped are in ~/.local/state/flow-rollback-379e7a-20261019T185048.
- Stopped message-nexus and flow-nexus; relinked both units and ~/.local/bin/{flow,flow-meta,flow-hook,message,message-meta,message-mcp-send}; started. Initializer: Replaced, Unchanged, Replaced, Unchanged. Flow 0.35.24 opened the 0.35.21 store (upgrade in place).
- message-nexus failed its first start "Flow bind failed: Broken" while the Nexus was typing queued work into 5ec12c's pane; systemd restarted it 2 s later and it stayed up.
- hm-* replaced by the 379e7a overlay wrappers; ~/.local/bin/herdr shim (report-metadata) removed, since 0.35.24 carries 647689a.
- Profile: `nix profile remove` + `add` of the two deployments started in the background (slow profile).

# Ouranos declarative deploy — decisions (379e7a, Opus subflow, lock 23967 OuranosDeploy)

## 2026-10-19 18:55 — One Flow pin carries the identify fix and flow-start
- Found: NexusSend worktree head is f36d61a "WIP send", unpushed; not green. 379e7a-identify 6db1f10 and 379e7a-localbin 2d4cf44 (flow-start launcher) both descend from fb5251b and touch disjoint files.
- Decision: Flow branch 379e7a-deploy 7e0dbc9 = 6db1f10 merged with 2d4cf44. Home's separate flow-start-source input is removed; flow-start reads `${inputs.flow}/launcher`. Send through Flow's socket is not in this deploy.

## 2026-10-19 18:55 — Home and CriomOS branches
- Decision: CriomOS-home 379e7a-deploy 9026e49b = 379e7a-localbin fdbabe05 merged with main bae3b479 (ca11a1bc psyche-context 2d9fbb6, 51cff7f5 context skills, Curriculum/field-context pins), Flow pinned to 7e0dbc9 (flake.nix, checks/flow-service-path). psyche-context main head is 2d9fbb6.
- Decision: CriomOS 379e7a-deploy 97b7e3b = 379e7a-localbin 2386339 merged with 42265e's field-ouranos-suspend-20261019 03c9fad, Home pinned to 9026e49b. Lock 23790 is no longer held; lojix deployment 124 (42265e BaseHost TestActivation of 03c9fad) shows Copying with no terminal and no copy process; 42265e is idle. Told Field core Secondary (Transported) that one deploy carries its fix.

## 18:53 379e7a: Primary landed
Primary origin/main 56058cd22 carries the skills change (trees removed, bindings, shared.edn without :repositories). Pin the packaged flow-start's primary to 56058cd22 or newer in the deploy. Shared checkout /home/li/primary is still detached at 6bedcf115 with untracked copies; do not reset it blindly — other flows' uncommitted work lives there.

## 18:54 URGENT 379e7a: exclude CriomOS 03c9fad from the permanent deploy
Field core Secondary 42265e: commit 03c9fad1a10e29ede13550ebbeacc5e1beda4ff9 (experimental runtime-PM delta) did NOT fix the suspend drain (real 44 s suspend: S0ix 0 -> 0). Before activating 97b7e3b or any cohort containing it: remove only that delta (revert 03c9fad on the CriomOS branch you activate), keep main 8d38ffdc model wake policy and everything else. Evidence: /home/li/private-repos/flow-evidence/42265e/suspend-drain-20261019/. Lojix Deployment124 row "Copying" is a stale observer row, not a running copy. Field will not start another ouranos switch: this deploy is the only one.

## 2026-10-19 19:05 — Codex start under 0.35.24 fails live; fix as 0.35.25
- Witnessed: three `flow-start Mind Prototyping Secondary` attempts (18:52, 18:53, 18:54) refused `HarnessSpawnRefused.{ Herdr timeout «timed out waiting for agent startup» }`, threads 01a156cb, 01a156cc, 01a156cd archived with no turn. The pane showed the Codex TUI exit with "thread/resume failed: invalid paginated history lineage for <thread>: missing source rollout (code -32600)"; Herdr lost the agent and its 30 s start wait ran out. Each thread's rollout file was written only when it was archived.
- Probe (scratchpad codexexp/exp.py, against the live app-server): thread/start + thread/name/set leaves no rollout and the TUI resume fails; adding `thread/section/move { threadId, sectionId: null }` writes the rollout at once and the TUI resumes with no error. Codex source (rust-v0.149.1, thread_manager.rs move_thread_to_section): "Explicit placement must work before the first turn materializes the thread."
- Decision: Flow 0.35.25 sends thread/section/move after the name readback (archive on failure moves to request id 6); tests updated (fake frames id 5, expected method lists).
- Possible causes for bae1fcd's claim "accepts it once the thread is named": a different codex build when it was written, a thread still loaded in the opening connection at resume time, or a fake-only witness. Not determined.

## 2026-10-19 19:55 — Approval pipeline: Flow 595479e, Home branch 379e7a-approval, one value for the integrator (approval subflow)
- Flow main 595479e: a landing's orders to one metaflow are written in its one row (two changes to Mind core Secondary had failed `duplicate key flow_nexus_metaflows/Mind:4:core:Secondary`); a change with no recorded implementer fails the step and queues nothing; the watch follows remote refs. Checks on prometheus: fmt, clippy, laws, 400 lib tests, package with tests.
- Witnessed on prometheus (staging, real commits): a live Curriculum (deployed curriculum-0.1.0, Mind e3fcd4f, Field bc5fa7c) serving psyche-context 6c8e266 with main at 2d9fbb6 → landings dc8c4cf and 2d9fbb6 recorded; one deploy (`Deploy.{ … 2d9fbb6… }`) moved Curriculum; both witnessed at 2d9fbb6; the seat launched with Psyche core Secondary's real modules (intent-main-flow among them) marked by dc8c4cf and refreshed at rest (pane closed, Stopped, metaflow Asleep); 3 Orders to Mind core Secondary; 2 Results to Psyche core Secondary. Log: prometheus /tmp/379e7a-approval/staging/witness.log.
- CriomOS-home branch 379e7a-approval (on main eee938fe): Flow pin 595479e; the Nexus ExecStart carries `Some.{ /git/github.com/LiGoldragon/psyche-context <context-deploy> }`; initialize-declared-flow's configure-only start writes `None`; packages/context-deploy (pins the landing as psyche-context in CriomOS-home main, that Home in CriomOS main, then submits `criomosHome.flow.landingDeployRequest` through lojix-meta and follows `lojix WatchDeployments` to `Some.Succeeded`); checks/context-deploy.
- Needed from the ouranos deploy integrator: set `criomosHome.flow.landingDeployRequest` to the exact `lojix-meta 'Deploy.Host.{ … github:LiGoldragon/CriomOS?rev=@CRIOMOS_REVISION@ … ActivateNow … }'` request it deploys ouranos with. Until it is set, every landing is pinned in CriomOS-home and CriomOS and its deploy step fails with that reason, reported to Psyche core Secondary.

## 2026-10-19 19:00 — Flow 0.37.0 = main 0.36.0 + identify + send (send subflow, lock 23959)
- Decision: branch 379e7a-send rebuilt on origin/main 7d9ecbd (0.36.0, approval) with origin/379e7a-identify 6db1f10 merged (3f17c49); the identify branch's caller walk (ListedSessions) replaces this branch's own, which is dropped. Send, Launch, BindSeat and Configure.Metaflows on top as Flow 0.37.0 (9c840a3), then e8f84ad. Remote checks: tests 405 lib (+ the rest) pass, clippy -D warnings, fmt, no-free-functions, no-inherent-methods pass. Package /nix/store/kl33x1c2…-flow-0.37.0.
- Found: main's packages.default (0.36.0) failed its own tests — the approval landing tests need git, which only checks.default gave. Fixed in e8f84ad (nativeCheckInputs git on the package).
- The living's 18:49 STOP order governs the live witness: one send to a flow that needs the message, or to a Quaternary test flow started for it and ended after; no pairwise sends.

## 2026-10-19 19:10 — Context skills go in; the five clean skill trees move aside at activation
- Found: Home main links ~/primary/{.claude,.agents,.codex,.pi,.opencode}/skills from the store (51cff7f5); Primary origin/main 56058cd22 removes those trees and gitignores them, but the shared checkout is detached at its parent 6bedcf115, so the five trees are present, tracked and clean (0 dirty), and Home Manager would refuse to clobber them. The LocalBinEradication subflow's deploy branches (Home 59fa04b5, CriomOS 79158b7) answer this by dropping context-skills.
- Found: the generated set (/nix/store/4iq6gq…-context-skills) carries every skill name the trees hold (0 missing per surface) and more (170 vs 133 in .claude/skills, vision-criomos included).
- Decision: deploy with context skills. Right before the Home activation, the five trees move to ~/.local/state/379e7a-skills-backup (they are committed in 6bedcf115, so nothing is lost); restored if activation fails. The shared checkout's HEAD stays where it is: advancing it to 56058cd22 belongs to the Primary publisher.
- Decision: system BaseHost (matches current generation 123), Home UserEnvironment `homeConfigurations.li.activationPackage` (the selector deployment 127 succeeded with); proposal /nix/store/dspiiriyy…/horizon-definition.datom, secrets /git/github.com/LiGoldragon/goldragon/secrets. Rollback pins: lojix generation 123 `rollback-379e7a`, 98 `rollback-379e7a-home`.

## 19:15 379e7a decisions for the single ouranos deploy (from LocalBinEradication's report)
- Before Home activation remove: nix-profile entries flow-deployment, message-deployment, curriculum-resolver-deployment, harness-home-profile, artifact-auto-open-session-vars, activate-messenger-clj; foreign links ~/.config/systemd/user/{flow,message}-nexus.service and their default.target.wants links, curriculum-nexus.service.d/50-declared-runtime.conf; dangling ~/.config/herdr/config.toml. Keep a record for rollback.
- hm-* overlay: not ported. Flow's identify fix (6db1f10, in 7e0dbc9) makes it unnecessary; hm-* is the prototype being retired (vision flow.md ~40).
- After activation remove from ~/.local/bin: flow, flow-hook, flow-meta, flow-start, herdr, hm-*, messenger-clj, the four message* entries, flow-next*.bak, message-next-meta, message-write-configuration; ~/.local/share/messenger-overlay-*. cloud-maintainer-chrome: package it declaratively or remove; nothing stays in ~/.local/bin.
- default-opener.nix: xdg-open is declared as a package on PATH, not a file in ~/.local/bin; ~/.local/bin leaves PATH entirely.
- Home declarations of flow-next, flow-next-meta, message-next (Flow 0.17.4): removed.
- No more hand-linking under any lock: the 18:50 hand deploy of Flow 0.35.24 / Message 0.20.1 (lock 23928) is to be replaced by this activation.
- CriomOS 97b7e3b: revert 03c9fad (see URGENT above); BaseHost deployment 130 failed evaluation — fix before switching.

## 2026-10-19 20:05 — Home main 34bbd529 carries the approval pipeline (approval subflow)
- CriomOS-home main fast-forwarded eee938fe → 34bbd529: Flow pinned 595479e (0.36.0), Nexus ExecStart with the landing watch, configure-only start with `None`, packages/context-deploy, checks/context-deploy. Checks on prometheus (system input from ouranos's lojix generated-inputs): context-deploy, flow-service-path pass.
- context-deploy refuses before anything is pinned until `criomosHome.flow.landingDeployRequest` is declared; once armed it holds CriomOS-home and CriomOS flake.nix/flake.lock through orchestrate while it pins, so it never races a flow editing them.
- The integrator's ouranos deploy of Home main now deploys Flow 0.36.0. The identify (0.35.25, 6db1f10) and Codex section/move (0.35.25) branches rebase onto Flow main 595479e.

## 2026-10-19 19:25 — Sibling subflows took over Flow main and the Home deploy
- Found: Flow main moved past fb5251b to 0.36.0 (7d9ecbd approval pipeline, 7e0dbc9 merge 379e7a-localbin, ed5305e merge 379e7a-deploy), all from this same session's other subflows; CriomOS-home main 34bbd529 pins Flow 595479e. Locks OuranosDeploy, NexusSendHome, VisionHome, ApprovalHome (all 379e7a) hold the Home deploy and the next Flow (0.37.0). A Home generation (home-manager-1058, 19:19, Flow 0.35.25 ypz088…) was activated; ~/.config/systemd/user/flow-nexus.service and message-nexus.service links are gone while both services still run 0.35.24 / 0.20.1 from this deploy. `nix profile` add finished 19:18 (profile manifest lists ag4n7k5x… and 80ka6c10…, but harness-home-profile's flow binaries shadow them in ~/.nix-profile/bin).
- Decision: do not deploy over the sibling's activation. Released locks NexusDeploy, NexusDeployMessenger, MessengerOverlay, NexusContracts. The Codex rollout fix is ported onto Flow main as branch 379e7a-codex-materialize (0.36.1) for whichever flow deploys next.
- "Profile and ~/.local/bin pointing at the same build": left to the sibling deploy (Home b69b163b "Flow tools reach PATH only through the Home profile").

## 2026-10-19 20:30 — One Flow and one Home for the ouranos deploy (approval subflow)
- Found: the OuranosDeploy integrator pins Flow 0.35.25 (7e0dbc9, origin/379e7a-deploy) in Home 9026e49b and CriomOS 97b7e3b; Flow main had moved to 0.36.0 (the approval pipeline) from the same base fb5251b.
- Done: Flow main ed5305e merges origin/379e7a-deploy into 0.36.0 (version conflicts only; UPGRADES carries both entries). Checks on prometheus: fmt, clippy, laws, 403 lib tests, package. CriomOS-home main 2ec3c77d pins it (with the localbin commits main already carried); context-deploy and flow-service-path pass.
- For the integrator: Home main 2ec3c77d holds everything Home 9026e49b holds plus the pipeline, except that main's flow-start reads the launcher from `inputs.flow-start-source` where 9026e49b reads it from the Flow pin. Repinning CriomOS to Home 2ec3c77d deploys one Flow, 0.36.0. Arming the pipeline is one value: `criomosHome.flow.landingDeployRequest`.

## 19:27 379e7a: the deploy takes the approval pipeline
- Pin CriomOS to CriomOS-home main 2ec3c77d or newer (Flow main ed5305e, 0.36.0: approval pipeline + 0.35.25 identify fix). One Flow, not two.
- Set criomosHome.flow.landingDeployRequest to the exact lojix-meta Deploy.Host request this deploy uses for ouranos (CriomOS?rev=@CRIOMOS_REVISION@ … ActivateNow), committed in CriomOS-home, so every landing deploys itself.
- Nexus start datom has a fourth position: Some.{ repository deploy-executable } for psyche-context.
- After activation: one real landing run end to end (the next psyche-context landing), witnessed per step; context-deploy's pin/push/lojix-watch path is untested — witness it then.
- The P4 threshold close-at-rest (2d9fbb6 implementation) merges with the pipeline's close-at-rest into one path.

# Flow vision 2d9fbb6 — convergence and deploy hand-off (379e7a, Opus subflow, locks 23912 23983 23985)

## 2026-10-19 19:25 — P4 joins 0.36.0's refresh at rest
- Decision: no second close path. `settle_rested`'s `refresh_due` is the landing's row OR `past_threshold` (the flow's last measured context at or past its model's threshold); both end in `refresh_at_rest`. A Drain hands a past-threshold seat nothing new; meta Deliver is refused `PastThreshold`.

## 2026-10-19 19:25 — P2 is one message, overflow into the system prompt
- Found: Codex's 1 << 20 limit is the sum over a turn's items (codex app-server `validate_v2_input_limit`), so splitting into items does not help; the system prompt travels in no argument for either harness (Claude memfd file, Codex baseInstructions).
- Decision: when USER modules and brief do not fit one message, leading USER modules join the end of the system prompt until the rest fits; `SystemTooLarge` is no longer produced. The parts machinery (PromptPart vector, PartsSubmitted) now always carries one part; its removal is a signal-flow change left open.

## 2026-10-19 19:40 — One Flow head for the single deploy: Flow 0.37.0 7b38cfa
- Found: four Flow lines in flight (main 595479e approval; 379e7a-deploy 7e0dbc9 identify + flow-start launcher; 379e7a-send e8f84ad, its own "0.37.0" with meta-signal-flow 30.0.0 4dcbfa8; this vision work, also "0.37.0" with its own meta 30.0.0 498374a).
- Decision: branch 379e7a-vision 7b38cfa = main 595479e + 379e7a-deploy + 379e7a-send + vision, one Flow 0.37.0. Contracts: signal-flow 24.0.0 (8796628, send's), meta-signal-flow 31.0.0 (a5ba4ab = send's 30.0.0 + per-model thresholds + `Investigation.Address` + `PastThreshold`). The vision's 498374a is superseded. Checks on prometheus: workspace tests (422 lib), fmt, clippy, no-free-functions, no-inherent-methods pass; the exact-test checks run.
- Decision: the Investigation seat is an Address, launched from its `Metaflows` declaration through send's `declared_launch` (no module lists in the Investigation configuration).

## 2026-10-19 19:45 — Home: declared thresholds, Investigation and Metaflows (CriomOS-home 379e7a-vision, on main 34bbd529)
- Flow pin 7b38cfa (flake.nix, flake.lock, checks/flow-service-path). The initializer adds `Configure.Thresholds` (every Claude model 200000, every OpenAI model 150000), `Configure.Investigation.{ Psyche compaction Tertiary }`, and `Configure.Metaflows` generated by packages/flow-deployment/metaflows.clj from config/main-flow (every declared metaflow: aspect defaults plus its own additions, as flow-start composes them) plus the Investigation seat from Psyche's defaults. No Home branch declared Metaflows before; it is the whole family.
- New check flow-declared-configuration runs the real initializer through the real configure-only Nexus and re-declares thresholds, Investigation and Metaflows to `Configured.Unchanged`. flow-service-path counts seven declarations. Both pass on prometheus (getFlake + callPackage), as does context-deploy.
- Hand-off to the ouranos deploy integrator: Home main carrying this commit is what the next CriomOS pin should name; lojix 132 (system 97b7e3b) succeeded, UserEnvironment 133 and 134 failed (133: "Refusing Herdr adoption: /home/li/.config/herdr/config.toml is an unmanaged symlink"; 134: no reason recorded). This flow runs no deployment of its own while that one is open.

## 19:40 — send subflow: deploy hand-off, hm-* retirement staged, skills to Field (locks 23959, 23984)
- Found: the vision subflow converged Flow into 7b38cfa (main + deploy + send e8f84ad + vision; witnessed `git merge-base --is-ancestor e8f84ad origin/379e7a-vision`), with meta-signal-flow 31.0.0 (a5ba4ab, on send's 30.0.0 4dcbfa8). Its Home branch declares Metaflows the same way as send's (metaflows.clj from config/main-flow). The OuranosDeploy integrator holds the single ouranos deploy.
- Decision: no second deploy from this subflow. CriomOS-home branch 379e7a-send (4f7d4fdb: Flow pin, Metaflows, flow-start removed) is superseded by the vision Home branch, and stays only as a reference.
- Decision: hm-* leave PATH only after flows can send another way. Home branch 379e7a-retire-hm (on main e2a5fb38; see 20:15) removes the messenger-clj Home module and its check. The messenger-clj input stays for the Field monitors (off). Deploy it after (1) Flow 0.37.0 is live, (2) Field lands field-context 379e7a-send (bec85a0) and the context cohort pin moves to it, and (3) running flows are retrained. Before that, a flow whose skill names hm-send would have no send command.
- field-context 379e7a-send bec85a0 rewrites compensation/messenger-clj.md for the Flow CLI (Send, BindSeat, Launch, Stop, replies, routes, the 18:49 test-send rule) and replaces every hm-* use in compensation/psyche-interraction.md, compensation/stale-lock.md, role/comment-relay.md and role/psyche-core-tertiary.md. Field owns field-context (README), so this is a branch for Field to review and land. Renaming the module id from compensation-messenger-clj is left to Field, since config/main-flow names it.
- mind-context knowledge/flow-seats.md, flow-caller.md, refresh.md and flow-receipt.md describe the hm-send route and flow-start as dated observations. They are Mind's to refresh after the deploy.
- No psyche-context module names hm-* or flow-start (grep of origin/main 2d9fbb6), so no psyche proposal is needed for the retirement.

## 2026-10-19 19:45 — Deploying Flow 0.37.0 to ouranos (user environment only)
- Flow main 2ca790c (0.37.0). CriomOS-home main 0faeecac = acfe84b1 (vision Home) + 379e7a-deploy ef507d1d (messenger-clj cb0e384); flow-start reads the Flow pin's launcher, the flow-start-source input is gone. Checks pass on prometheus: flow-declared-configuration, flow-service-path, flow-id, message-service-path, messenger-clj-package, context-deploy; flow-start builds against the Flow pin.
- CriomOS 379e7a-vision 53d0864 = 379e7a-deploy 4bae05d (the system lojix 132 runs) with only the Home pin moved to 0faeecac. Deploy: lojix-meta Deploy.UserEnvironment ActivateNow from that revision, after 138 (Current). No system switch.
- Rehearsal: the new initializer on the 0.35.21 rollback store copy answered Replaced/Unchanged for all seven declarations. psyche-context main = served cohort 2d9fbb6, so the approval pipeline starts with no landing.

## 2026-10-19 19:55 — Deploy carries Flow 0.37.0, messenger-clj cb0e384 and Primary 56058cd
- Found: Home activation refused on hand-made state: a dangling ~/.config/herdr/config.toml link (target GC'd), flow-nexus/message-nexus unit and default.target.wants links, the curriculum-nexus drop-in, and six nix-profile entries (flow-deployment, message-deployment, activate-messenger-clj, curriculum-resolver-deployment, harness-home-profile, artifact-auto-open-session-vars) colliding with home-manager-path. Each moved to ~/.local/state/379e7a-predeploy-backup (profile entries recorded there by store path) and the activation then succeeded.
- Found: messenger-clj a7a40d1 refuses every seat-route migration with ProcessUnavailable (procfs read through slurp); cb0e384 (e529c53) reads it directly. CriomOS pins messenger-clj itself and Home follows it, so both pins moved.
- Found: Primary 56058cd's tools compose vision-criomos into the Psyche core Secondary start and also read the current checkout's config; Home's primary input moved to it.
- Found: lojix deployment 139 (VisionImplementation sibling, CriomOS 53d0864 on this branch) activated Flow 0.37.0 and my 140 replaced it. Flow 2ca790c (0.37.0) contains 7e0dbc9 and 6db1f10 and its checks build green, so it is the newest green head: Home d4136f3e = main 0faeecac + Primary 56058cd; CriomOS fea07c5 = 379e7a-deploy + 379e7a-vision.

## 2026-10-19 20:05 — URGENT: Flow down since ~19:58; fixing forward (vision subflow)
- Witnessed: lojix 139 (19:45, CriomOS 53d0864, Home 0faeecac, Flow 0.37.0) Current, Flow 0.37.0 upgraded ~/.local/state/flow-03521/flow.sema. Then lojix 140 (CriomOS d11c15f = 4bae05d + Home 796a82e0, built on ef507d1d, Flow 0.35.25) activated over it. Flow 0.35.25 refuses the upgraded store: `family registration "flow_nexus_compactions" is not an authored Flow Memory v2 identity`; flow-nexus restart counter 118 at 20:04.
- Decision: fix forward, no store rollback (the pre-upgrade bytes are gone; the 18:50 copy is 0.35.21 and older than the queues). Home = 0faeecac + 796a82e0 merged; CriomOS = d11c15f with that Home pin; deploy now. DO NOT deploy any Home that does not contain CriomOS-home 0faeecac: every Flow before 0.37.0 refuses this store.

## 20:10 — send subflow: Flow 0.37.1 deployed; live witnesses (locks 24008, 24009)
- Found (witnessed): on the deployed 0.37.0 (lojix 139), `flow 'Launch.{ { Field publisher Quaternary } «…» }'` composed its declaration and opened thread 01a156fc…, then answered `StartRejected.HarnessSpawnRefused.{ Herdr.{ Some.timeout «timed out waiting for agent startup» } … Archived }`. The Codex rollout fix 7f5ed64 (0.36.1, NexusCodexFix) was not in 0.37.0.
- Done: Flow main fc53f4f = 2ca790c + 7f5ed64, 0.37.1 (remote: 422 lib tests, clippy, fmt, no-free-functions, no-inherent-methods, package). CriomOS-home main 9829b366 pins it (flow-service-path and flow-declared-configuration pass remotely). CriomOS branch 379e7a-codex037 2c48bc2 = 379e7a-vision 53d0864 with only the Home pin moved. lojix-meta `Deploy.UserEnvironment.{ goldragon ouranos li /nix/store/dspiiriyy…-horizon-definition/horizon-definition.datom SecretsDirectory./git/github.com/LiGoldragon/goldragon/secrets github:LiGoldragon/CriomOS?rev=2c48bc2… { ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome } Horizon { homeConfigurations.li.activationPackage } HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [] }` → deployment 141 Succeeded. flow-nexus restarted 20:07:47 on flow-0.37.1; `flow` resolves to the same package; no system switch.
- Witnessed live, under the living's 18:49 rule (Quaternary test flows, one send, stopped after):
  - `flow 'ResolveCaller.None'` → `CallerResolved.{ 379e7a Psyche Medium claude-opus-5-5 }`; `flow 'BindSeat.{ Psyche core Secondary }'` → `Bound.379e7a`.
  - Claude start through the daemon (0.37.0): `Start.{ witness-379e7a-claude-2 [ spirit-core intent-main-flow ] [] { Psyche test Quaternary } claude-haiku-5-5 … }` → `Started.{ 508d15 … w3Q:p1 … Flow.{ 379e7a … } }`; its transcript answers on claude-haiku-5-5. The first try with only spirit-core was `ContextRefused.ComposerRejected` (Curriculum: "startup requires explicit Spirit and seat-intent SYSTEM context").
  - One send: `flow 'Send.{ Address.{ Psyche test Quaternary } Soft.Order.«…» }'` → `Queued` at 19:46:08. The seat's transcript shows a user turn at 19:46:08.98 carrying `{ Sender.{ Psyche core Secondary } Order.«…» }`, answered "Received." at 19:46:09.9. `Stop.508d15` → `Stopped.508d15`; its pane is gone.
  - Codex start from the loaded configuration (0.37.1): `flow 'Launch.{ { Field publisher Quaternary } «…» }'` → `Started.{ fc48d0 01a15710-…-eb8fc48d0563 … w3T:p1 … }`; its rollout shows model gpt-6-luna, effort low, answer "Model: gpt-6-luna". `Stop.fc48d0` → `Stopped.fc48d0`; its pane is gone.
  - Refusals: `Send` to `{ Mind flow Secondary }` → `Refused.OffRoute`; `Launch` of `{ Mind nowhere Secondary }` → `StartRejected.Undeclared`.
- Gap seen: the drained queue opens with "…while no flow of it was running", also when it is handed to an Awake resting seat (composition.rs QUEUED_WORK_OPENING).
- Gap seen: a metaflow's `:voice` override in config/main-flow (Field publisher Quaternary: claude-haiku) is not represented in Flow, so its Launch runs the layer's configured model (gpt-6-luna).
- 20:10 resolved. Outage window, from the flow-nexus journal: 19:59:36 (first refusal of the 0.37 store by 0.35.25, after lojix 140) to 20:06:06 (a 0.37 Flow started again by lojix 141/142, another flow's deploy). lojix 143 (mine) failed at fetch (Home commit not yet on GitHub). lojix 144 Succeeded 20:10 from CriomOS 379e7a-vision 265a2a9 = d11c15f with Home e2a5fb38 (Home main: 9829b366 Flow 0.37.1 fc53f4f + 796a82e0 Primary 56058cd). Running: flow-0.37.1, message-nexus active; metaflows intact.
- Cause of the outage, in order: 139 upgraded the store to 0.37.0; 140 was built from a Home line (ef507d1d → 796a82e0) that did not carry 0faeecac; Flow's store refuses downgrade by design. Possible contributing causes: two flows deploying the same user environment from different Home lines with only this file to coordinate; no check in the deploy path that the Flow being activated can open the live store; my deploy at 19:45 recorded here but not acknowledged by the integrator before theirs.

## 2026-10-19 20:11 — Codex start witnessed on the sibling deploy (0.37.1)
- 379e7a-codex-materialize (7f5ed64, 0.36.1, check 641 test results ok) was merged into main by a sibling as Flow 0.37.1 (fc53f4f) and deployed through Home; flow-nexus runs flow-0.37.1 since 20:10:18, message-nexus message-0.20.1; ~/.nix-profile/bin/flow-nexus resolves to the same flow-0.37.1; the ~/.local/bin flow/message/hm-* links are gone (Home profile only).
- `flow 'Launch.{ { Mind prototyping Secondary } «…» }'` at 20:11:10 → Started.{ e4b21d 01a15713… pane w3V:p1 } in 10 s; the rollout shows task_started 02:11:14Z and the user turn; Herdr pane label, display agent and terminal title = { Mind prototyping Secondary e4b21d }, agent codex, working.
- Released locks NexusIntegrate and NexusCodexFix.

## 20:15 — send subflow: one staged retirement branch
- CriomOS-home 379e7a-retire-hm 439967b4 (on main e2a5fb38): removes the messenger-clj Home module and its check, and the flow-start package and its Home binding. The messenger-clj input stays for the Field monitors (off). flow-service-path passes remotely; field-monitoring evaluates. Deploy it once field-context carries the Flow CLI messaging module (branch 379e7a-send bec85a0, Field to land), the context cohort pin moves to it, and running flows are retrained. Until then hm-send and flow-start stay on PATH from Home 9829b366.

## 2026-10-19 20:15 — Final deploy and witnesses
- Deployed: CriomOS 379e7a-deploy f0cbc06 (Home 7bab4cf8, tree-identical to the vision sibling's e2a5fb38): lojix 145 Home Succeeded, 146 system BaseHost Succeeded, system generation 192, flow-nexus 0.37.1, message-nexus 0.20.1, messenger-clj cb0e384. Rollback: system generations 190/191 kept; lojix pins rollback-379e7a (123) and rollback-379e7a-home (98); moved state in ~/.local/state/379e7a-predeploy-backup.
- Open: the shared Primary checkout stays at 6bedcf115, so `flow-start` composes without vision-criomos until the Primary publisher advances it to 56058cd22 (witnessed with FLOW_WORKSPACE at that commit: the Psyche core Secondary start carries vision-criomos). Flow Send to Mind core Secondary answers Refused.Unknown: Flow forgets that seat's dead binding and the live Codex seat is not bound in Flow; hm-send reaches it.
