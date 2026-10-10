# Field status — 2026-09-21

**Scope.** This is a current-state report from the latest available receipts, not a replay of the prior handoff. Timestamps below are observation times; no row asserts live state after its cited observation. **Receipt grades:** A = exact primary witness or remote receipt; B = direct report backed by named evidence; C = claim/proposal; U = unknown.

## Twelve-cell census

The latest complete census was observed at **2026-09-21 15:31:26 UTC**. It recorded 18 Herdr records, 15 exact HM routes, three unmatched Herdr records, and ten unmatched registrations. Those are diagnostic counts, not a healthy twelve-cell result. An exact route proves tuple agreement only; it does not prove current duty, harness health, or availability.

| Aspect | High | Medium | Low | Ultra-low | Current gap / receipt |
| --- | --- | --- | --- | --- | --- |
| Psyche | Fable `1b8ac0`; responsiveness seen in snapshot | older Opus `b80e55`; done UI | Sonnet `0625c3`; retained and route repaired after the snapshot | no uniquely designated Haiku seat | Ultra-low unfilled. The older snapshot's Psyche Low mismatch is stale: later exact HM tuple and target Read witness repair it. A/B |
| Mind | Astra `4b0f60`; designated, liveness unverified | Sol `2c61af`; native, exact HM/Herdr, target role acceptance | Terra `e798f3`; prior reply is over 17 h old | Luna `23d977`; prior reply is over 17 h old | Mind Astra's specific coordination/assignment acceptance for `2c61af` remains pending, so the Medium role is not fully accepted. A/B |
| Field | Astra `6db4fe`; coordination accepted, deployment/currentness gate open | Sol `7091ea`; live bound successor, refresh transfer held | Terra `0347d0`; exact route, final designation/acceptance not located | Luna `c88918`; done UI | Field high/medium transfer gates remain open; current availability is unknown in all cells. A/B |

**Owner / next action:** Field Astra `6db4fe` coordinates the refresh and canonical naming work; Mind Astra `4b0f60` must accept or otherwise resolve the Mind Medium assignment. **Currentness:** the census is a 15:31 UTC point-in-time observation; it cannot establish present responsiveness.

## Defects and held work

| Item | Claim versus witness | Owner / next action | Grade and currentness |
| --- | --- | --- | --- |
| Duplicate Field Sol roles | **Witness:** audit found Field Medium census operator `9ddcbc` using Sol, crossover `395aed` retained, and `7091ea` working. No retirement eligibility was found; the topology is structurally nonconforming. | Field Astra: classify/resolve the duplicate assignment, complete Flow-ID naming script, coordinate fresh Sol successor. | B; reported in the 2026-09-21 Field checkpoint. No script or launch receipt exists. |
| Psyche Low | **Witness:** the living retained `0625c3`; launch of a replacement is HOLD. Exact `psyche-low` route is `messaging-build/wS:p1/term_65bedce5d2b213a`, and `HM_ROUTE_READ_0625C3_3a74` reached the target as Read. | Field Low `0347d0`: keep launch preparation halted. | A; later recheck supersedes the stale census mismatch. |
| OpenCode | **Witness:** source is ready at Goldragon `8c4d03de`, CriomOS `d8c765db`, CriomOS-home `7721387e`; Ouranos has no CLI, service, or listener. **Claim withheld:** source readiness is not a deployed service. | Field: integrate/validate the Lojix consumer repair, then clear Home activation and `message-daemon.service` collision gates before test-service deployment. Living sign-in follows deployed test service. | B; deployment currentness unproved. |
| Lojix contract | **Witness:** consumer repair is published proposal `lojix-horizon-contract-7091ea` `ac672dab`; workspace check passed before a conflicted rebase was abandoned; Lojix main remains `c4bba4fa`. | Field contract owner: obtain remote producer Nix gate and full pre-socket Lojix request, then integration decision. | B; proposal is unintegrated; no Realize or activation receipt. |
| HM naming / Nix gate | **Witness:** `hm-rebind` landed at primary `6c6b6d8f`; 19 direct tests passed. **Gap:** its Nix check did not finish in the initial 60-second bound. The Flow-ID title tool is dry-run only; apply is disabled pending rollback, partial-failure, readback, guarded rebind, and target-read tests. | Field Astra/title-script owner: finish the Nix gate and complete guarded mutation tests before enabling apply. | B; no apply or full Nix receipt. |
| Pane echo | **Witness:** PsycheHigh saw two outgoing messages appear as prompts in its own pane and in the targets; registry showed distinct panes. **Inference:** focus-sensitive Herdr injection leak is a hypothesis only. | Field: run an isolated reproduction and preserve exact input/output witnesses. | B for observation; C for cause. Untested. |
| Low-power branches/worktrees | **Witness:** survey found reachable local divergence and three dirty Mind worktrees. | Preserve and inspect under owner/lock; do not reap or clean from this survey alone. | B; no lost-work claim, and no cleanup receipt. |

## Sources

- `flows/6db4fe/reports/twelve-flow-health.md` — 2026-09-21 15:31:26 UTC census, topology counts, cell evidence and gaps.
- `flows/7091ea/log.md` — 2026-09-21 Field checkpoint: duplicate-Sol audit, Psyche Low hold/read repair, OpenCode/Lojix state, naming/Nix gap, pane echo, and worktree survey.
- `flows/6db4fe/reports/mind-sol-native.md` and `flows/6db4fe/reports/refresh-handoff-current.md` — Mind Medium native/route receipts and pending Astra acceptance; title-script and Field refresh gates.
- `flows/1b8ac0/log.md` — pane-echo observation and the later Psyche Low retention/route-repair context.
