# 15 · cloud-designer lane — agglomeration, audit, and maintenance ledger (2026-05-29)

One synthesis of the whole cloud-designer lane: the greater picture, the
two topic arcs agglomerated from reports 1-14, an audit of the gaps in
design intent, and the context-maintenance verdicts that retire the
superseded reports into this ledger. Supersedes the prior maintenance
ledger (report 7). After this sweep the lane keeps **11, 13, 14, 15**;
the rest retire (substance captured below + in git history + permanent
docs).

## The greater picture — what this lane actually designs

The cloud-designer lane has, in practice, become the designer of the
**goldragon cluster's self-hosted AI capability** — a local-first /
sovereign AI stack: our own models (Gemma 4 multimodal) on our own
hardware (prometheus, AMD Strix Halo gfx1151), served by a llama.cpp
router behind an auth token, with resilient admin networking so the
headless router node can never be locked out, consumed by our own agents
(Pi coding agent, browser-use automation) instead of third-party cloud
APIs. That is the through-line of reports 5-14 and the live intent
(1011-1017, 1022-1023, 1032-1033, 1105, 1140-1146, 1195-1196, 1206,
1217-1222).

**This is NOT the lane's originally-named scope.** Report 1 + intent
872/873 + Spirit `cloud` records 281-294 named the lane for **cloud-
component design** — the `cloud` triad (`cloud` / `signal-cloud` /
`owner-signal-cloud`) managing external cloud-provider APIs, Cloudflare
DNS as first ground. That is a different domain that happens to share the
word "cloud." The lane drifted from component-design to deploy-design
when the psyche handed it the Gemma/token work end-to-end (record 1017).
**The scope is still formally undefined (report 1's open question),
now spanning two unrelated arcs.** This is gap #1 below.

## Arc A — Cloud component (Cloudflare triad) · DORMANT

Agglomerates reports 1, 3, 4.

- **State:** the `cloud` triad is *fully working in the Cloudflare-DNS-
  via-flarectl sense* — `PreparePlan → ApprovePlan → ApplyPlan` drives
  correct flarectl argv for create/update/delete; Validate/Observe/owner
  ops exercised e2e (26 tests). cloud-operator's main commit `58862593`
  converged with the designer prototype; the designer branch
  `designer-cloudflare-cli-prototype-2026-05-27` @ `ec2d3493` added the
  gopass-wrapped flarectl + 11 e2e tests, **pushed but never merged**.
- **Parked work:** a 13-gap next-cycle slate (Tier-1 ≈ 40 lines:
  gopass fail-loud, pin redirect-observation, TTL/priority; plus
  CredentialHandleUnknown verification; larger items: real Validate,
  diff-aware PreparePlan, Plan→Mutate state machine, HTTP↔CLI fallback).
  Detail in git history of `4-fully-working-prototype-cycle-…/`.
- **Triad invariants** live permanently in `skills/component-triad.md`;
  the 0.1.0 deferral list in `cloud/ARCHITECTURE.md`.
- **Three open psyche questions, unanswered since 05-27:** (1) execute
  the Tier-1+B2 slate or pivot to a bigger item? (2) land the
  convergent branch via PR or keep it a designer reference branch?
  (3) name the `mine→implement→audit→grow` discipline as
  `skills/audit-loop.md`? (migration candidate — the method insights
  "convergent prototyping isn't waste" + "dead reply variants are a
  contract smell" want that skill.)
- **Status:** no Arc-A work since 2026-05-27. Parked. Needs a psyche call
  on revive-vs-park (gap #2).

## Arc B — Local-AI cluster deploy · ACTIVE, blocked on llama.cpp

Agglomerates reports 5, 6, 8, 9, 10 (+ live in 11, 13, 14).

**The stack, as designed and mostly deployed:**
- **Node:** prometheus (Strix Halo gfx1151, Vulkan, unified memory,
  llama-server router mode `--models-dir`/`--models-preset`/`--models-max`,
  110 G cap). Early reports called it "atlas"; the deployed node is
  prometheus.
- **Models:** `gemma-4-31b` (dense, BF16 63 GB) + `gemma-4-26b-a4b`
  (MoE, BF16 52 GB), multi-shard from Unsloth, mmproj-F16 for vision.
  In `CriomOS-lib/data/largeAI/llm.json` @ de676a8e.
- **Secrets:** `localLlmApiToken` minted blind in gopass
  (`goldragon.criome/local-llm-api-token`), sops-encrypted to prometheus
  (`goldragon/secrets/local-llm-api-token.sops`), wired into
  `lojix-cli/artifact.rs`, consumed by `llm.nix` via
  `--api-key-file`. Discipline permanent in `skills/secrets.md`.
- **Deploy safety (the incident lesson, report 8):** a live `Switch` on
  the router node twice severed our ssh (it restarts the hostapd/dnsmasq
  we administer through). **Rule: BootOnce/Boot, never Switch, on the
  router node until out-of-band console exists; build on prometheus.**
  Permanent home: intent 1105/1117/1125 + the `restartIfChanged=false`
  guard landed in CriomOS `c250d9a`. (Migration candidate: state this
  explicitly in `skills/nix-discipline.md` — gap #7.)
- **Resilient backup network (records 1140-1146):** USB wifi + USB
  ethernet as an independent admin path that survives a router-stack
  switchover. Implemented in `c250d9a` — but **bridged into `br-lan`**,
  so it still depends on kea/dnsmasq, which **does not meet record
  1145's "deliberately independent of kea/dnsmasq."** Full review +
  Path A (independent stack) vs Path B (bridged + no-bounce) in **report
  11 (kept)**. Unresolved (gap #3).
- **What landed:** HF prefetch utility (`tools/nix-prefetch-huggingface`
  + `lib/fetchHfModel.nix`, bead `primary-3dqf`); the secrets; gen 45
  booted with Gemma + auth; the Pi client auth fix (report 13).
- **What's BLOCKED:** Gemma 4 does not serve — deployed `llama-cpp-b8470`
  (2026-03-22) predates the `gemma4` architecture. Fix designed in
  **report 14 (kept)**: target the latest `b9404` (has gemma4 + every
  fix incl. the 26B-A4B image fix #21497); the operator's bump failed
  only on Nix packaging (stale `npmDepsHash`); stay on Vulkan. This is
  the critical-path gap (#4).

**Pi-as-consumer (report 13, kept):** Pi's `criomos-local` provider now
uses the command-backed gopass key (`!gopass show …`), Gemma is in the
inventory, default switched to local Gemma. Open: the default points at
the not-yet-working Gemma (resolves when llama.cpp is fixed); Phase B
(pi 0.77 + claude 2.1.156) staged on a dangling jj change, on hold.

**Quant variants (records 1220/1221/1222):** decided — deploy multiple
quants as separate router models, quant in the modelId
(`gemma-4-26b-a4b-bf16`, a 4-bit, optional 8-bit), prefetch + hash on
prometheus over LAN. Designed-not-implemented; I owe the `llm.json`
entry spec once the psyche picks the set (gap #5). Quant ladder (BF16
dominated by Q8; UD-Q4_K_XL the sweet spot) detailed in report 14.

## Arc C — Browser-on-local-AI · operator implementing now

Sub-arc of B. Three-tier design (cloud orchestrator → local browser-use
→ local Gemma actor → Chrome dev port 9222) in report 5; renewed intent
1217-1219 (attach to a visible/supervised tab, supervised scout mode,
package browser-use in the home profile with a local-Gemma wrapper). The
system-operator is implementing the CriomOS-home packaging now (I
released the lock). `pi-models.nix` is the auth template. **Blocked on
the same llama.cpp fix** — browser-use leans on Gemma's vision for
screenshots. The cloud-side GPT-5.5 orchestrator wiring (report 5's P1)
is still an open psyche question.

## Audit — gaps in design intent

1. **Lane scope formally undefined, spanning two arcs.** Cloud-component
   (Arc A) vs local-AI-deploy (Arc B) under one "cloud" name. Needs a
   psyche scope decision — and possibly a lane split/rename (e.g. this
   lane becomes the local-AI/deploy designer; Arc A moves to a
   component-design lane or parks).
2. **Arc A parked with 3 unanswered questions + an unmerged branch.**
   Revive, merge `ec2d3493` via PR, or formally park?
3. **Backup-network independence unresolved (report 11).** The
   implementation bridges into `br-lan` (depends on kea/dnsmasq),
   diverging from record 1145. Path A (independent dumb stack) vs Path B
   (accept bridged + no-bounce, relax 1145)?
4. **Gemma 4 not functional — critical path.** Blocked on the operator's
   llama.cpp `b9404` build fix (report 14). Everything downstream (Pi
   default, browser-use, vision) waits on this.
5. **Quant variants designed, not implemented.** Need the psyche's quant
   set, then the `llm.json` spec.
6. **Vision end-to-end unverified.** The router-mode `mmproj=` preset key
   is the one unconfirmed link (report 9/14) — needs an image-request
   test once llama.cpp serves Gemma.
7. **Deploy-safety + 3-tier architecture want permanent homes.** The
   router-node deploy-safety rule → `skills/nix-discipline.md`; the
   browser-on-local-AI 3-tier architecture → an architecture doc; the
   audit-loop discipline → `skills/audit-loop.md`.
8. **Out-of-band console for prometheus still missing** (bead
   `primary-lome`) — the standing exposure behind the whole deploy-safety
   posture.

## Context-maintenance verdicts

Landing gate satisfied for every Drop: substance is in this ledger +
git history + the named permanent doc.

| Report | Verdict | Landing |
|---|---|---|
| 1 lane-bootstrap | DROP | origin in intent 872/873; AGENTS.md rows landed; scope Q → this ledger gap #1 |
| 2 recap | (already dropped, report 7) | — |
| 3 cloudflare prototype | DROP | superseded by 4; essence → Arc A above |
| 4 prototype cycle | DROP | Arc A above + branch `ec2d3493` + git; triad invariants in `skills/component-triad.md` |
| 5 browser-local-AI | DROP | Arc B/C above; HF utility landed; design → arch (gap #7) |
| 6 secret-deploy + Gemma | DROP | discipline in `skills/secrets.md`; deploy executed (gen 45); essence → Arc B |
| 7 maintenance ledger | DROP | this ledger is the successor sweep |
| 8 deploy incident | DROP | lesson → Arc B + intent 1105/1117/1125 + `c250d9a`; migrate to nix-discipline (gap #7) |
| 9 prometheus handoff | DROP | deploy-event log, consumed (gen 45); state in 13/14 |
| 10 backup net + boot | DROP | checklist executed (`c250d9a`); review in report 11 |
| 11 backup net review | **KEEP** | recent; competing design alternatives (Path A/B) — §3a guard; open gap #3 |
| 12 Pi/Gemma 401 handoff | DROP | superseded by 13 |
| 13 Pi execution | **KEEP** | current canonical Pi surface; open items live |
| 14 Gemma 4 llama.cpp | **KEEP** | current; the operator's fix path; quant ladder |

## Consolidated open questions for the psyche

- **Lane scope/identity** (gap #1): is cloud-designer = local-AI-deploy
  designer? Split Arc A out, or keep both?
- **Arc A fate** (gap #2): revive / merge the Cloudflare branch / park?
- **Backup-network independence** (gap #3): Path A or B?
- **Quant set** (gap #5): `-bf16` + `-ud-q4-k-xl` (+ optional `-q8`)?
- **browser-use cloud orchestrator** (Arc C / report 5 P1): the GPT-5.5
  ↔ browser-use wiring shape.

## Migration candidates (this sweep flags; not yet executed)

- Router-node deploy-safety rule → `skills/nix-discipline.md`.
- `mine→implement→audit→grow` + its two insights → `skills/audit-loop.md`.
- Browser-on-local-AI 3-tier architecture → a `cloud`/local-AI
  `ARCHITECTURE.md` section.

## Anchors

- Kept reports: 11 (backup-net review), 13 (Pi execution), 14 (Gemma 4).
- Permanent homes: `skills/secrets.md`, `skills/component-triad.md`,
  `cloud/ARCHITECTURE.md`, `CriomOS/{modules/nixos/llm.nix,
  packages/llama-cpp-strix-halo.nix}`, `CriomOS-lib/data/largeAI/llm.json`.
- Intent: 872/873 (lane), 1011-1017/1022-1023/1032-1033 (secret+Gemma
  deploy), 1105/1117/1125 (deploy safety), 1140-1146 (backup net),
  1195-1196/1206 (local-AI consumption + full multimodal),
  1217-1222 (browser-use + quant variants + prefetch-on-prometheus).
