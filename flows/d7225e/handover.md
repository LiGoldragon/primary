# Handover — Mind flowNexus Sol

Active task **k0le**, from Mind flowNexus Astra, 45 minutes from **2026-11-12 04:46:35 UTC** (return Done with evidence or precise blocker by **05:31:35 UTC**). Implement A/B/G subscription lifetime correction only; no deployment. **No Rust bodies or source edits yet.**

## Custody and next action

Opus answered Question **3t2g**: base **f1162330e78c3c9aee229896aaca060e98982c90**, Flow 0.54.4. I created clean dedicated worktree **/git/worktrees/flow-0545-lifetimes-d7225e**, branch **0.54.5-lifetimes-d7225e**. Opus grants exclusive custody of all Flow files this lifetime scope touches, tests, shared cancellation type and 0.54.5 bump/UPGRADES; he edits nothing in Flow meanwhile. Contract changes need his prior agreement. He owns merge/deploy after Astra acceptance. Do not touch historical normal checkout (foreign flake.lock edits).

Opus notice p9t4 confirms custody survives refresh and successor startup now declares **intent:anatomy, knowledge:nix-rust-builds, knowledge:orchestrate** live. Refresh was queued successfully for d7225e.

**Awaiting Astra review of Question w4v9**, which points to **/home/li/primary/flows/d7225e/subscription-lifetime-plan.md**, already sent before bodies. Also awaiting applicable **Rust doctrine and Orchestrate lock instructions injection**; this harness has no skill loader, and Astra expressly says do not invent lock syntax or begin bodies before instructions. Astra notices rcwo/9udl confirm this arrangement. Next: receive review/instructions, claim exact paths, implement approved plan, test on builder, report immutable candidate and gaps. No subagents were requested/used.

## Plan already sent

Shared `ObservationCancellation` with typed PeerClosed/NexusStopped cause and eventfd; a connection-owned watcher/guard runs around streaming work, watches downstream EOF plus Nexus stop, announces launch_changes to wake existing Launch condvar, and shuts down/joins on every return. Agent and Launch receive cancellation; Herdr subscription acknowledgement and event waits receive it too, giving cancellation priority even over buffered upstream lines. Cancellation is distinct from upstream Gone and **must never record a live flow Exited**. Consider consolidating current duplicate observation watchers into that one lifetime capability without changing unrelated policy. Plan is pending review, not decided code.

Required tests: quiet Agent disconnect, withheld ack on peer close/stop, pending Launch disconnect, normal state/upstream Gone, buffered upstream cancellation. Event/barrier synchronization, bounded deadlines, no polling. Builder regressions and isolated resource comparisons baseline vs candidate. Opus requests all `checks.x86_64-linux` green via nix-fast-build on Prometheus, immutable commit and log in flow directory; push branch after Astra acceptance and handoff to Opus. Follow any clarified publication sequence.

## Source/evidence pointers

Audit **/home/li/primary/flows/d7225e/leak-class-audit.md**, source map beside it; task **sfs1** already Done (njfy, queued). Baseline source still clean in **/git/worktrees/flow-0543-5e88e5** at f1162330. A: `lib.rs:1463-1466`, `observe_agent.rs:151-213,247-285`; B: `herdr/events.rs:57-137`; G: `lib.rs:1457-1461`, `launching.rs:1323-1348`. Existing watchers `lib.rs:1262-1430`; eventfd/poll helpers `event_wait.rs`; LaunchChanges condvar in `store.rs:1500+`. Note cancellation must be inspected before consuming buffered lines, not only when BufReader is empty. Read appropriate current source ranges before edits.

Three builder reproductions/scripts and JSON evidence beside audit: observer-retention (10 closed clients leave +10 threads/+20 FDs until fake upstream closes); observer-handshake (SIGTERM blocked awaiting ack, releases in 33ms once ack supplied); hook-content retained across restart (deferred C). Earlier leak-comparison.md confirms 0.54.3 21.2GiB vs fixed125MiB over3min with fixture. Existing tests in audit were read, not rerun.

Builder **prometheus.goldragon.criome**; heavy work there, root commands via `ssh root@...`. Isolated stores at `/tmp/flow-leak-d7225e` and `/tmp/flow-audit-d7225e`; all test services stopped. Original leaking store on laptop **~/.local/state/nexus/main/flow.sema.leaking-1111** untouched. Known baseline binary `/nix/store/cjp3p3vdm1d4fhv2yb0xrisipccxr7li-flow-configured-0.54.4/bin/flow-nexus-daemon`. Isolation used private sockets/copied state, PrivateNetwork, empty /run, inaccessible /home/li, memory cap/no swap, fake Herdr. Preserve production.

## Important corrections and deferred rulings

The normal repository checkout is **adopt-049-bdcb05 at53782fba**, not advanced main (local main is unrelated old0.48; origin/main f1162330). Corrected that label in audit/map and notified Astra (mxl7); no audit finding depended on the wrong label.

Astra 9udl relays new Psyche rules for *subsequent, separate work*: versioned memory upgrade strips persisted assistant content after tracing transient consumers; unanswered requests survive bounds until Result/Done; answered-history configurable length/default/expiry; every bound configurable; producer gets typed capacity refusal; slow observer typed overflow then resubscribe/opening state, no silent drops/producer slowdown. Keep these out of current lifetime scope. Queued-Codex incident separate, cause unknown.

Primary edits only in flows/d7225e; never stage/commit/push Primary (standing committer owns it). Other-repo changes normally committed/pushed by owner. User requires worker read NON_MANAGEMENT_AGENTS.md; it requires exact Orchestrate path claims before shared edits. Relevant ordinary Rust standards already inspected: /git/github.com/LiGoldragon/standards/good-rust-practices.md and traits-as-ontology.md (trait-first; no production free functions except main; meaningful data types; no ad-hoc tuples). Astra is arranging missing instruction injection.
