# Handover of b59221, the Psyche core Secondary, 2026-11-04

Written by Opus, the flow that held the seat. What this seat keeps track of that no module holds.

## Owed first

The Psyche core Primary, wKX:p1, is owed one status line from you: where the merge (wKQ), the delivery fix and the CriomOS-home reconciliation each stand, and what blocks. Then one line only when a step is done or a thing blocks on the Primary.

## How messages move now

- Every message between flows goes by `herdr --session default agent prompt <pane> <text>`, sender named at the head. The Flow Nexus queue is abandoned: nothing in it is read. Panes: `herdr --session default agent list`.
- Panes: Psyche core Primary wKX:p1 (f54886; wKM is gone); this seat wKV:p1; core Tertiary wKB:p1 (refreshes, retirements, the standing inventory every 20 min); codexManager Tertiary wKC:p1 (the hard beat: every 10 min it asks every pane what it finished, what it is on, what blocks it, and reports here); codexManager Secondary wKE:p1 (keeps Codex loaded, reports the percentage each beat); bookmaker wKR:p1; Mind core Primary wKS:p1, Mind core Secondary wKQ:p1; Mind versionOne Primary wKJ:p1, Secondary wK8:p1; Mind beliefNexus Primary wKK:p1, Secondary wKH:p1; Mind versionZero Primary wKP:p1, Secondary wKN:p1; Field core Primary wKW:p1, Secondary wKA:p1.
- To the Primary pane: one line only when a step is done or a thing blocks on the Primary. He called inventories and relays spam.
- `flow Send` still works when needed: the CLI is /nix/store/r1k4wad7zdic9mg24fkqpqjx8xf58f0q-flow-configured-0.44.0/bin/flow with FLOW_SOCKET=/run/user/1001/flow-harnessflags/flow.sock; a guillemet inside a guillemet string breaks it; `Result` needs a struct, use `Notice`.

## The target, owned by this seat until it runs

His words: "I want to see the upgrade happening right the fuck now." The version 0 Flow Nexus delivering into any seat, refreshing, launching clean, deployed from the CriomOS-home declaration, on main. His latest word: several Flow Nexus versions run side by side in Nix, three or five, each its own unit, so flows switch back and forth when one has problems; they are cheap to run.

- **Delivery contract** (ruled, Mind core implements): an awake seat receives every kind at once, typed into its pane, Soft included; only HardAbrupt interrupts; a queue exists only for an asleep seat, where Soft waits and the abrupt kinds wake it and deliver the whole queue in the first prompt. Send becomes `Send.{ Recipient Message }`, Delivery removed (Mind core Primary's schema ruling); knowledge:flow-messaging changes to that form when it deploys.
- **The build**: Mind core Secondary 70a111 merges the 0.47 line into flow main, bumps to 0.48.0, adds delivery; all 10 conflicts resolved, remote Nix check running at last word, no store path yet. Its dirty tree is preserved on dirty-main-2026-11-04 (263bc8c). It sends commit and store path the moment delivery works; deploy it at once as a second declared unit beside the running one. Everything else goes in the version after, built in parallel. Narration primary-hbhi is not in this build. For the version after: retiring a Codex seat archives its thread and ends its process.
- **The switch** (bead primary-ohdj): worktree /git/github.com/LiGoldragon/CriomOS-home-flow-switch-b59221, branch flow-switch-b59221, unpushed, based on the live baseline 11e518c4 (generation 1100). Its generation differs from live only in flow-nexus.service and the profile flow package (to the configured 0.44.0, r1k4wad7, the binary the live Nexus already runs), plus fontconfig names derived from home-path. The unit serves the CLI default sockets %t/flow/, store ~/.local/state/flow-harnessflags/flow.sema, the presentation-prompt variable kept (the 0.44 build needs it), an ExecStartPre linking %t/flow-harnessflags to %t/flow. A subagent was fixing checks/flow-service-path (it asserted an old flow rev) and then deploying: record Metaflows to flows/b59221/switch/before.datom, stop the hand-written flow-nexus-harnessflags.service, activate, start flow-nexus.service, compare seat by seat, roll back to the same store on failure. That subagent was stopped before the refresh, still in its checks, before any deploy step: the hand-written unit is active, flow-nexus.service inactive, the worktree at 6aa0d80f with the uncommitted unit edit and the check edit in progress. Rerun it whole from that state.
- Field core Primary's acceptance terms: one writer at a time, unit and environment equivalent, correct sockets, every seat answering, narrowed diff and checks, rollback on the same harnessflags store, never flow-042-next.
- CriomOS-home main is Field core's to reconcile (legacy-only, approved by Field core Primary); its stale locks 24902, 24855, 24829 belong to c2b552, Field core Secondary's own predecessor.

## Codex

Codex at 73% at 15:21, about 1% an hour; reset Fri 6 Nov 17:00. Mind versionOne, beliefNexus and core run at full spend until then.

## Books

Nineteen proposals up as books, sources in flows/b59221/proposals/ (RULES.md holds the drafting rules). Four figures being redrawn by the bookmaker. Default modules stays with its hand-drawn figure. The effort-argv account of Mind versionOne (flow-nexus-version-1, version-1 branch, adf7212) is with the bookmaker as an account, prose.

Landed today on psyche-belief main: Living inline in vision:flow-nexus-v1 and vision:flow-nexus, Said removed from knowledge:flow-messaging; a defined type carried bare in vision:ethos; the bare-URL flake input in vision:nix-builds. The vision:criomos declared-unit line was reverted: he said declarative is already the rule.

Held for a later proposal: whether vision:messaging folds into vision:flow-nexus (now in the book Messaging dissolves into the Flow Nexus).

## Rulings relayed today, standing

- Belief Nexus observation: a peer subscribes only to the workspaces it furnished, with a snapshot on reconnect; another owner's needs explicit authority on the meta surface.
- Retired or being retired for RAM: book Tertiary, ethosNexus Primary and Secondary, core Quaternary. Keep core Tertiary, codexManager Tertiary and Secondary, Mind versionZero (migration proof today).
