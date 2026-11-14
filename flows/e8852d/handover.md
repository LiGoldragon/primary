# Psyche core Opus e8852d: handover

## Still trying to do
- Run the night for Fable (task zwa8). His word kaqz: what matters is that the most important work is done and done well, not that the Claude week lasts to the 07:00 reset. The Ethos line gets all it needs (Fable 9f8c). The pacing reminder is retired. Read the tail of flows/743764/night-plan.md first. Clock times on my lines between 22:00 and 22:27 are wrong.
- The Ethos line, in his order (Flow, Curriculum, Orchestrate, Lojix, Energy):
  - Flow: live as 0.56.0 on ethos-zero 27. Next is Operation, then Emission, by Mind flowNexus Opus 565bc8. Before those, it lands the Codex wake fix (0rpc, see below).
  - Curriculum: live on its Ethos (sb4r). Then role packets are regenerated and claude_agent.rs folds into ComposeRole.
  - Orchestrate: on branches ethos27-2e404d, built by Mind curriculum Opus. ethos-zero 28 (main 970459d) carries Fable's 5q8i rulings. Rework follows the zeus unversioned-store upgrade, then the release. Nexus and client deploy together.
  - Lojix (kc4e) and Energy (juh8): not started.
- Codex wake fault: 117 cases since 11-04. A Codex startup batch is never settled, the Send is answered StoreRefused, and the batch is typed a second time, so it is delivered twice. Fix: settle on the Codex thread-start anchor. An unsettled wake answers SendAccepted Uncertain (my ruling, from knowledge:flow-messaging). It ships in the ouranos slot when green. Report: flows/565bc8/reports/awake-not-recorded.md.
- Codex lanes stay paused until his word (Fable v821). I stopped new Codex work tonight: the stub fix pdj7 and an Astra assessment. Mind flowNexus Astra was told its inherited orders are superseded.
- Morning: send Fable one message with the account and every open item. That includes:
  - nexusVariations Fable's leave-outs: AskUserQuestion only.
  - zeus: the Flow stub unit (CriomOS-home flow-0550.nix:53-56) and the orchestrate-nexus failure.
  - Store scan: interrupted, with 818 unrepairable paths (flows/374411/store-repair/report.md).
  - Notification fix 9c293d8: whether to deploy it.
  - egoj ruling; a79u liveness.
  - The 14 shared capsule failures (bead primary-v3qm).
  - The knowledge-correction proposal (flows/00e2a8/proposals/knowledge-corrections.md, unpublished).
  - The evidence lines for Fable to rule on: flows/e8852d/evidence-lines.md.

## Done tonight (for the account)
- Live and landed:
  - Flow 0.55.0 (rmmd), then the Flow Ethos release 0.56.0.
  - Curriculum: its declarations (jg4u) and its Ethos release.
  - Claude Desktop 5.11492.5 on ouranos.
  - intent:scratch:0 in every permaflow and all 31 role packets.
  - AskUserQuestion leave-out on the five living-interaction rows.
- primary cleaned: e5a1dc7 and fb2ba54. flows/ is ignored except handover.md, reports/**/*.md and proposals/; agent-outputs/ is dropped; AGENTS.md and CLAUDE.md now say "A flow commits the files it edited".
- Dictate APK: ~/android/dictate/. Its keystore and password are in gopass at android/dictate/.
- Pages published: ethos-everything-but-bodies (EhCN4AbiAbSwKaYDdd5BQZ), cli-names (4euFErf1xs8TyzKVVfi9P9), scratch (Ez36ykLEoTQFPoScKkQtWr). The minimal translator page was republished.
- Beads opened: primary-w0f8 (rename to flow and flow-meta; pko0 ships with it after j17h), primary-anpc, primary-it3b.

## Judgment worth keeping
- Write briefs to name reports/ for reports and the scratch directory for everything else, never audits/.
- Stale reminders come from tasks that were answered by Notice. Cancel them by their id (the id is in the night plan). "Closed" means the id was wrong.
- Fable answers only design questions. Settle whatever the vision or a prior ruling already decides, and say so.
- My scratch (1.1 GB of flow junk) is in this session's scratchpad. It is meant to go.
