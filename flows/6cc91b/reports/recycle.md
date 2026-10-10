# Recycle inventory since the new moon

Assumption: new moon = 2026-09-11 (per the living's framing in this task; no file in the
repo records an actual lunar date, so the given date is used as-is). Source: `grep -l
'2026-09-1[1-9]' flows/*/log.md`, `flows/index.md`, `/home/li/secondary/flows/*`, plus a
directory listing that caught three undated flows the grep missed. Layers per
`vision/pairHierarchy.md` and `vision/layerZero.md`: core (law, self-hosted, private),
primary (ideas, top authority), secondary (stable middle, memory/execution, horizontal
deployment), tertiary (fast mercurial voice layer), quaternary (janitors: monitoring,
cleanup, reporting, cheap long jobs). Live-session check: `claude agents --json` (Codex
threads' liveness is unknown to me — no equivalent list was available).

## Flows

**024bc7** — Claude, live (session 024bc757, status busy). Purpose: cross-harness
wake/injection engineering and open-source-model scouting. Last entry 2026-09-13 (host
memory note). Open threads: (a) Claude<->Codex wake/injection plumbing (daemon attach,
intercom wake) — **secondary**, it is the durable inter-agent mechanism; (b) third-model
research for the open-source stack — **primary**, a direction decision; (c) periodic
ChatGPT web-chat transcript checking design — **quaternary**, a cheap recurring watch job.

**14dc94** — harness not stated in log (references only Codex transcripts as evidence).
Not live. Purpose: reconcile overnight 33a4d4 deployment (Chroma/location). Last entry:
closeout, deployment 4 Completed/Succeeded, no reboot performed. Open thread: confirm the
unrebooted state persists / decide if a reboot is still owed — **quaternary**, a
verification/maintenance check.

**162eb3** — Claude, live (session 162eb3b7, idle). Purpose: skeptical-audit post-mortem
and main-flow/subflow generation ruling. Last entry 2026-09-12. Open threads: (a)
curriculum-deploy generation fix, blocked on the roles.datom migration lock 851 —
**secondary**, mechanical deploy work; (b) proposed main-flow/subflow skill lines awaiting
the living's approval — **primary**, a pending top-authority decision.

**34d94e** — Codex, liveness unknown (was "primary Codex main"; 6cc91b's log records it
superseded today by fresh flow 82c299, so this thread is likely retired rather than open).
Purpose: model-council evaluation, Message/Orchestrate integration POC, hook-ordering
proof, OpenCode packaging. Last entry 2026-09-14. Open threads, if still live: (a)
third-seat model council (Kimi/OpenCode/Pi, DeepSeek/GLM arms) — **primary**, a model-
selection decision; (b) Message/Orchestrate durable-relay and registry-guard POC —
**secondary**, infra execution; (c) OpenCode adapter/provider-driver build-out —
**secondary**; (d) live-hook human-proof step awaiting the living's go-live —
**tertiary**, the one point that needs the living's voice before it can close.

**753090** — harness not stated in log. Not live. Purpose: diagnose/repair Wispr Flow
dictation. Last entry 2026-09-13, paused awaiting the living's explanation of an inversion
(non-subscriber weekly-limit gate misreported as a capture failure). Open thread: root-
cause explanation and, if warranted, an adapter status-contract fix — **secondary**, a
concrete bug on the execution/memory layer, once unblocked.

**8325c1** — Codex. Not live. Purpose: audit overnight Claude work (f6db8d) and existing
Ethos/Datom anatomy. Last entry 2026-09-13. Open threads: (a) exact ClosureCopy/Ethos-kinds
proposal, not yet authored/approved — **primary**, awaiting a design ruling; (b) prevalence
-first Lojix/substrate pattern census, presentation pending — **quaternary**, an audit/
reporting job.

**9e7c9f** — Claude, live (session 9e7c9f1f, idle). Purpose: cross-harness subflow
launching, Codex remote-control server, removed Claude cloud remote server; landed two
psyche-distillation lines. Last entry 2026-09-13, landed and pushed. Open thread: none
outstanding that the log states — closed.

**bcd02a** — Codex. Liveness unknown (Codex thread list unavailable to me). Purpose:
Claude<->Codex pair-wake POC, live-Claude injection witness, pair rebootstrap. Last entry
2026-09-13 (fresh-pair final checks; the flagged quarantined live_claude_ingress tool
output was not opened for this report). Open threads: (a) same-live-session relay is
witnessed both ways but automatic fanout and human-draft locking are unimplemented —
**secondary**, mechanism hardening; (b) the process-environment-read incident's proposed
guard against `ps eww`-style reads is unlanded — **quaternary**, a safety/cleanup fix.

**d1c570** — Claude, live (session d1c5705d, idle). Purpose: /spirit review of protos/
datom/ethos/signal architecture against vision. Last entry 2026-09-13, presenting forks
(arity, newtypes) to the living. Open thread: the living's rulings on those forks and the
Datom/newtype distillation — **primary**, an open design decision awaiting the top layer.

**fe34eb** — Claude. Not live. Purpose: audit distilled protos/nexus vision, land Vision
edits, realize the signal-repository merge. Last entry 2026-09-12, signal realization
landed; orchestrate left untouched with an uncommitted non-compiling checkout from flow
857335. Open thread: land orchestrate onto the new signal/protos stack (bead
primary-xqb.8.3) — **secondary**, execution/deployment debt.

**f6db8d** — Claude. Not live (wound down on the living's order, session-limited). Purpose:
Wave 6 whole-stack cutover (protos/datom/ethos/signal arity, 26 repositories landed).
Last entry 2026-09-12, idle, no lock held. Open threads: (a) CriomOS-home landings, the
users contract blocker — **secondary**; (b) final sweep onto signal 7.0.0 and the
mirror-pair repin — **secondary**; (c) Orchestrate exchange-layer move — **secondary**;
(d) MS2130 UVC kernel-patch review, not started — **quaternary**, a gating/review chore.
All four are stalled mid-flight, not actively worked.

**dc1c58** — harness not stated (native `claude` worker processes; no date string in the
log, but its mtime is today, within scope). Purpose: Castañeda/Torres literature
collection for the Book of Soul; a Claude remote-control partner session. Not confirmed
live. Open threads: (a) literature/source curation, the four "mitad" labels still
unidentified — **primary**, original-content curation the living directs; (b) the Claude
remote-control partner's phone-side access/persistence — **secondary**, infra to verify;
(c) contradicted commit/push closure claim — **quaternary**, needs a cleanup/verification
pass.

**82c299** — Codex, referenced live in 6cc91b's own log as the current primary Codex main
(successor to 34d94e); its own log.md is empty so far. Purpose: bootstrap core, tertiary
and quaternary per the living's five-point program. Open thread: that bootstrap itself —
spans **core/tertiary/quaternary** by its own charter, not yet witnessed done.

**51fadd, 0a65d9** — empty flow directories (claimed, nothing written). No harness, no
purpose recoverable, not live by any evidence found. Not assigned to a layer; flagged
below as orphaned claims, not threads.

**6cc91b** (this flow, self) — Claude, live, busy. Purpose: the living's five-point
recycling/layering/bootstrap program itself. Open threads: bootstrapping core/tertiary/
quaternary via Codex 82c299, drafting the open-source stack, harness-prompt agreement
search, this inventory — all **primary**, since this is the flow the living is directing
ideas through.

**57a7aa / 348e7b** (secondary, /home/li/secondary/flows) — Claude/Codex, 57a7aa live
(session 57a7aa02, busy). Purpose: bootstrap the secondary pair itself. Open thread:
confirm the Claude-half readiness handshake (pending a second direct-prompt turn per
348e7b's log) — **secondary**, by definition the stable-middle layer's own bring-up.

## Layer table

| Layer | Open threads | Source flow |
|---|---|---|
| core | bootstrap charter (unwitnessed) | 82c299 |
| primary | third-model direction; skill-line approvals; ClosureCopy/Ethos-kinds proposal; arity/newtype rulings; model-council selection; literature/source curation; this recycling program | 024bc7, 162eb3, 8325c1, d1c570, 34d94e, dc1c58, 6cc91b |
| secondary | wake/injection plumbing; curriculum-deploy fix; Message/Orchestrate POC; OpenCode build-out; Wispr adapter fix; relay/fanout hardening; orchestrate landing debt; CriomOS-home/final-sweep/exchange-layer work; remote-control partner persistence; secondary-pair bring-up; bootstrap charter | 024bc7, 162eb3, 34d94e, 753090, bcd02a, fe34eb, f6db8d, dc1c58, 57a7aa/348e7b, 82c299 |
| tertiary | live-hook human-proof step; bootstrap charter | 34d94e, 82c299 |
| quaternary | web-chat transcript watch; deployment-persistence check; process-env-read guard; Lojix/substrate census; MS2130 review; commit/push cleanup; bootstrap charter | 024bc7, 14dc94, bcd02a, 8325c1, f6db8d, dc1c58, 82c299 |

## Unassigned or contested

- 82c299's bootstrap charter is claimed by three layers at once (core, tertiary,
  quaternary) by its own mandate — not an error, but not yet split into per-layer threads
  either; it should be decomposed once 82c299 writes its own log.
- 51fadd and 0a65d9 belong to no layer: empty claims, no content, no evidence of being
  alive or abandoned.
- 34d94e's threads are listed but its liveness (superseded by 82c299 today) is unconfirmed
  from Codex's side; they may already be closed rather than open.
- 753090 and 14dc94 have no stated harness in their own logs; assignment above is by
  content, not by a harness label.
