# Field obsolete-Flow retirement audit

Authority: living's audit-only directive to Field High 6fb948. This commissions evidence gathering and tool review, not closure. Field High accepts or rejects candidate evidence; each destructive close requires a subsequent explicit authorization naming the exact target and operations.

## Owners

- Terra 0347d0: candidate census, transcript/history and work-ownership audit; document both positive evidence and unresolved obligations.
- Luna c88918: review and improve fail-closed tooling within owned, reserved paths. Exercise fixtures and dry runs only; no production close, route removal, lock release, or reap.
- Field High 6fb948: reconcile evidence, protected exceptions, and acceptance. No new controller or writer is created by this audit.

## Candidate acceptance criteria

Every candidate needs a timestamped evidence packet identifying source paths and receipts, with separate findings for:

1. **Transcript and work:** last substantive activity, unfinished tasks, pending results, promises, reserved scopes and dependencies. Each obligation must be completed or explicitly accepted by an identified live owner with a relay receipt. Silence, age, idle/done state, context size, or a missing lookup is insufficient.
2. **Native identity:** exact harness, native UUID, Flow ID, model/effort where relevant, process PID and start incarnation. Distinguish historical session identity from the process currently occupying a pane. Never reconstruct an absent attestation as fact.
3. **Herdr:** exact session, agent name, pane, terminal, process binding and current state. Detect reused panes, mismatches, and multiple possible owners. Unknown or ambiguous evidence blocks acceptance.
4. **HM and remote access:** exact route-to-native/pane binding, consumers and pending delivery/late-result obligations. A replacement must have independently witnessed readiness and accepted work/relay before it can satisfy continuity. An `/rc` footer proves feature enabled only, not authenticated external access or successor readiness.
5. **Locks:** current reservation inventory, owner, exact paths/scope, and explicit completion or owner handoff evidence. Never release a foreign lock or infer release from a missing process. Lock ownership does not transfer with a title or role.
6. **Retained/crossover status:** explicit check against owner instructions, holds, living retirement decisions, and late-result routes. Retained or active means protected. A successor's existence alone does not make the predecessor obsolete.

Classify each result as **protected**, **blocked by missing/conflicting evidence**, or **eligible for explicit closure review**. Eligibility does not execute or authorize closure. Show proposed actions individually (native exit, pane close, agent deregistration, route removal, archive), with distinct impacts; never bundle them into a broad reap. Archive location, provenance, and retrieval must be documented before any authorized destructive action. Transcript deletion is not authorized.

Immediately before any later authorized action, recheck the entire exact binding and relevant locks; abort on changes, activity, ambiguity, stale evidence, missing tool support, or a failed check. Tool tests must cover reused pane/PID, UUID mismatch, active work, retained route, lock ownership, missing evidence, and partial action failure. Default to no action and retain an audit receipt.

## Reported tooling blockers — coordinator finding

The coordinator reports that `reap-flow` archives source when roster lookup is unavailable and creates no HM retirement marker. Candidate discovery reportedly lacks retained-route, work-lock, and native-session gates. These are supplied findings for Terra/Luna to verify against exact source revisions, not claims of a controller-run reproduction.

Acceptance explicitly requires:

- Roster lookup failure, missing binding, or ambiguity prevents **all live mutations, including source archival**. A successful archive is not retirement evidence.
- Discovery checks retained routes, current work locks/obligations, and exact native sessions before labeling anything eligible; missing evidence yields blocked, never obsolete.
- An explicit, durable HM retirement marker must be supported and observed for any later authorized retirement. Merely creating a marker is insufficient: tests must prove the routing, wake and registration paths respect it and cannot silently reawaken the retired identity. Unknown enforcement blocks acceptance.
- Partial failures preserve a truthful recoverable state; never mark an active identity retired, remove an active route, or claim no-reawakening from an archive alone. Test failure before and after each proposed action without live mutation.

All live mutations remain held pending evidence-backed, per-flow decisions. No candidate list, tool patch, dry run, or previous branch authorization lifts this hold.

## Protected exceptions

- Current Field High 6fb948 and controller reservation 4639; 03e825 remains crossover/late-result relay. Prior 4494 release does not retire 03.
- Retained 6db4fe and its worker/Ouranos relay, VM 4373 and Curriculum 3825. No automatic reap or transferred collaboration-handle assumption.
- Active Field Sol 753e69, Terra 0347d0, Luna c88918 and their work; prepared Field High 0ad137 remains protected pending explicit succession/retirement decisions.
- Mind High 4b0f60 and its Network Nexus ownership, route and handles. Its readiness-only refresh gate remains native-verified occupancy greater than 40%; last-input ratios are not occupancy. Preserve the other active Mind seats.
- Incumbent Psyche High 1b8ac0 at p6 until living retirement; successor 836818 at p9 is active. Its pane-specific original-attestation waiver authorized the Remote Control/bootstrap operation only and is not retirement authority. Preserve pC/f4b263 and the extra 836818c directory; neither is obsolete by inference.
- Psyche Low 0625c3, Medium b80e55 and the partial Ultra session/cursor and launcher ownership. Partial or failed startup is not closure permission.
- Operator 9ddcbc and consumer lock 3776; reported Flow/Message 2836/2862/2864, Mind 3830, Low 3847, and protected 1834/1835/542442. Reconcile current owner evidence rather than treating this historical list as a fresh lock inventory. Preserve every other active or unresolved reservation.
- All retained routes, held seats, unresolved worker results and source-owner boundaries. Six diverging integration branches remain pending the living's decision; this audit does not authorize integration, reload, cleanup, or retirement.

## Additional protected boundaries reported by 9ddcbc

Read-only owner observation at **2026-09-22T20:36:43Z**; no lifecycle authority accompanies it. Reobserve before any later individually authorized action.

- Sol 753e69 holds active Lojix locks 4045, 4051, 4062, 4070, 4072, 4164, 4240, 4251. Retained 6db4fe additionally holds 4285 alongside 3825/4373. Retained 9ddcbc holds 3776 and has unmerged CriomOS-home work at e1096a16. Neither retained operator is a replaceable role slot.
- 0ab019 is the only reported retained contact path to f72ab7, whose 2836/2862/2864 locks protect Flow/signal-flow/Message. Preserve that contact path.
- 98ac2e and 9e7ea5 are retained Mind crossover routes. 395aed is stale/corrupted crossover evidence requiring exact transcript/job/lock preflight, not an approved cleanup candidate.
- 553901 has no verified HM route, but locks 1834/1835 still protect its Flow/Message primary scopes. Absent route does not release them.
- b81560 is closed/no-resume: do not resume it. Its Flow, HM and transcript remain preserved; registration retirement is not inferred from session closure.

Assess physical pane, native process/session, HM registration, Flow record, transcript, locks, child handles, unmerged work and successor continuity separately. A later explicitly authorized **pane-only** close needs exact empty-shell/exited-session evidence and preserved successor continuity, followed by a `pane_not_found` postcondition. It does not remove Flow/HM/transcripts/routes or authorize another action. No lock alone, ghost label, done/idle/STALE state, missing HM, silence or context proxy proves obsolescence. Preserve the stable app-server; no batch/full-manifest cleanup. Submitted messages are neither read receipts nor work acceptance.
