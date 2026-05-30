# 2 — Topic: deploy stack — lojix / horizon / CriomOS + cloud (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2.
Consolidates the prior sweep's two slots
(`/home/li/primary/reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/2-lojix-horizon-criomos.md`
+ `/home/li/primary/reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/3-cloud-and-deployment.md`)
into ONE topic now that the two arcs share a single substance spine: the
deploy stack — production lojix-cli on `main` + the lean lojix daemon +
the CriomOS / CriomOS-home / goldragon side + the cloud-component triad
+ the self-hosted-AI deploy on prometheus. Designer surface lives in
cloud-designer + system-designer; implementation in cloud-operator,
system-operator (the LIVE deploy node), cluster-operator. Schema-derived
horizon design is sub-agent A's topic; this one carries the DEPLOY side
and flags the boundary every place a report straddles.*

## Topic arc since 44 — three era shifts in 48 hours

Three axes have shifted since
`/home/li/primary/reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`
landed: (1) **schema port has crossed gate 1** per
`/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`
(collections + horizon-next + three-engine drive landed 2026-05-28;
`/167` stays load-bearing on the deploy side because lojix/horizon
production replacement still goes through it); (2) **backup-network
deploy is mostly DONE in code with one explicit intent divergence** —
cloud-operator's CriomOS `c250d9a` bridges the backup AP into
`br-lan`, diverging from Spirit 1145 (High, "deliberately
independent of kea/dnsmasq"), reviewed in
`/home/li/primary/reports/cloud-designer/11-backup-network-implementation-review-2026-05-29.md`;
(3) **local-AI deploy is critical-path-blocked on llama.cpp `b9404`**
per `/home/li/primary/reports/cloud-designer/14-gemma4-multimodal-llamacpp-design-2026-05-29.md`
— deployed `llama-cpp-8470` predates the `gemma4` arch (Spirit 1201),
and Pi client auth is already fixed
(`/home/li/primary/reports/cloud-designer/13-pi-local-gemma-execution-and-decisions-2026-05-29.md`).

Shape: production lojix-cli stays on `main` per INTENT.md §"two
deploy stacks", the lean lojix daemon advances through the
schema-derived stack (handed to sub-agent A), the cloud-component
triad ships in raw form first (record 914-916), and prometheus is the
center node carrying the self-hosted-AI capability.

## Current canonical surface

Reports that remain load-bearing (newest first, by topic cluster):

### Live cloud / self-hosted-AI deploy

- `/home/li/primary/reports/cloud-designer/15-lane-agglomeration-audit-and-maintenance-2026-05-29.md`
  — cloud-designer's own lane-agglomeration ledger covering Arc A
  (Cloudflare triad, DORMANT), Arc B (local-AI deploy, ACTIVE blocked
  on llama.cpp), Arc C (browser-on-local-AI). 8-gap audit list is the
  live decision queue. KEEP (§3a guard — competing-design rationale).
- `/home/li/primary/reports/cloud-designer/14-gemma4-multimodal-llamacpp-design-2026-05-29.md`
  — Gemma 4 multimodal research + operator fix path; Strix Halo /
  Vulkan reality + quant ladder. KEEP — operator's active reference.
- `/home/li/primary/reports/cloud-designer/13-pi-local-gemma-execution-and-decisions-2026-05-29.md`
  — Pi client auth execution log + open psyche decisions. KEEP.
- `/home/li/primary/reports/cloud-designer/11-backup-network-implementation-review-2026-05-29.md`
  — backup-net review with Path A / Path B competing designs. KEEP
  (§3a guard, psyche call pending).

### Live lojix / horizon production replacement

- `/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`
  — sub-agent A's anchor; cross-listed here because horizon-next IS
  the deploy-substrate replacement. KEEP.
- `/home/li/primary/reports/system-designer/34-mvp-and-sandbox-audit/`
  — active bead queue (B-0 through B-23) for MVP lean-stack cutover;
  5 most-important psyche decisions still open. KEEP — /49 explicitly
  defers to this queue.
- `/home/li/primary/reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md`
  — operator artifact `/40`/`/41`/`/42` worked against; per
  `/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md`
  §"Horizon Schema State" still load-bearing evidence. KEEP.
- `/home/li/primary/reports/cloud-operator/11-lojix-horizon-criomos-intent-implementation-audit-2026-05-28.md`
  — newest cross-cutting audit reading lojix + horizon + CriomOS
  against full intent. KEEP — carries 9 named remaining-divergence
  findings feeding BOTH schema and deploy stacks.
- `/home/li/primary/reports/cluster-operator/1-bird-zeus-local-update-authority-design.md`
  — design report for narrow per-user per-node update authority. Only
  live cluster-operator report; foundational `SystemUpdateGrant`
  pattern with open psyche questions. KEEP-or-MIGRATE — see below.

### Permanent docs that absorb deploy-side substance

- `/home/li/primary/INTENT.md` §"two deploy stacks" + §"Production work
  belongs in worktrees, not the canonical checkout" + §"Persona is
  LLM-mediated end-to-end".
- `/home/li/primary/skills/secrets.md` — the never-show + gopass-wrap
  + sops-nix discipline (per cloud-designer/15 §gap-7 a migration
  candidate from /6, already landed there).
- `/home/li/primary/skills/component-triad.md` — the cloud triad
  invariants and single-argument-NOTA rule (per cloud-designer/15
  Arc A).
- The live cluster state itself: CriomOS commit `c250d9a` (backup
  network), goldragon `c8b5840`/`0298d21` (secrets), CriomOS-home
  `8aa75035`+`36f5de89` (Pi/Gemma fix), `lojix-cli` `4c66b8a`
  (artifact wiring). The deployed gens are the canonical state for
  what landed; reports document the WHY, not the WHAT.

## Stale / forward / migrate / keep bands by lane

### cloud-designer (4 reports; all KEEP per the lane's own /15 verdict)

Per `/home/li/primary/reports/cloud-designer/15-lane-agglomeration-audit-and-maintenance-2026-05-29.md`
§"Context-maintenance verdicts", reports 1-10 + 12 already retired
into /15 with landing evidence. Live surface: 11, 13, 14, 15. This
sweep ratifies /15's retirement by reference. All four kept reports
already named in §"Current canonical surface" above; /15 itself is
flagged for sub-agent D as the lane's own maintenance ledger
(retires when next sweep covers same scope — THIS slot only covers
cross-lane deploy topic, so /15 KEEPS through this sweep).

### cloud-operator (7 reports — 2 DROP, 3 KEEP, 2 flag-for-sub-agent-D)

Cloud-operator has NOT yet self-swept (its /12 is a SKILL-UPDATE
ledger, not a content-retirement sweep). This sweep flags candidates.

| Report | Date | Verdict | Landing |
|---|---|---|---|
| `/home/li/primary/reports/cloud-operator/6-recent-intent-reports-branch-read-2026-05-26/` | 05-26 | DROP | Branch-read overview pre-dating the lane-split AND the schema-port era; entirely superseded by /49 + the live source state. Landing: `/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md` §"Recent intent surface" + live `nota-next`/`schema-next`/`schema-rust-next`/`horizon-next` repos. |
| `/home/li/primary/reports/cloud-operator/7-refresh-intent-reports-visual-audit-2026-05-26/` | 05-26 | DROP | Visual audit / like-and-dislike refresh of /6's branches; superseded by /49 + live schema stack. Free-function findings now in AGENTS.md hard overrides; bracket-string ambiguity resolved per /49. |
| `/home/li/primary/reports/cloud-operator/9-cloudflare-dns-tool-2026-05-27.md` | 05-27 | KEEP | First-working Cloudflare DNS path on old NOTA stack. Per /15 Arc A this IS the live cloud-component impl baseline. |
| `/home/li/primary/reports/cloud-operator/10-audited-cloud-domain-prototype-2026-05-27.md` | 05-27 | KEEP | Audited domain prototype impl, companion to cloud-designer/4. Per /15 still load-bearing. |
| `/home/li/primary/reports/cloud-operator/11-lojix-horizon-criomos-intent-implementation-audit-2026-05-28.md` | 05-28 | KEEP | Newest cross-cutting audit, 9 named divergence findings. Cross-listed with sub-agent A (D1/D2/D5 schema-language; D3/D7/D8/D9 deploy-substrate). |
| `/home/li/primary/reports/cloud-operator/12-context-maintenance-skill-update-2026-05-28/` | 05-28 | KEEP + flag for sub-agent D | Skill-edit ledger; the skill update IS the permanent landing — no substance to migrate. DROP once lane's next maintenance pass confirms. |
| `/home/li/primary/reports/cloud-operator/13-pi-harness-abort-investigation-2026-05-28/` | 05-28 | KEEP-or-MIGRATE | Small operational investigation; not deploy-stack-load-bearing. If follow-up resolved → DROP into bd item; otherwise KEEP. Flag for sub-agent D (workspace-side). |

**Cloud-operator drop count this sweep:** 2 clean (6, 7), 2
flag-for-handoff (12, 13). Lane reduces 7 → 5 active reports.

### system-operator (deploy-side cross-cuts)

Per `/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md`,
the system-operator lane just ran its own deep maintenance pass —
absorbing /169 and /172, keeping only `1`, `2`, `139`, `166`, `167`,
and `173` itself. THIS sweep ratifies that retirement by reference;
no additional system-operator drops in the deploy topic.

| Report | Verdict | Cross-lane note |
|---|---|---|
| `/home/li/primary/reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md` | KEEP | Cross-listed with sub-agent A. The deploy-side use: this IS the live working evidence of the schema-emitted horizon path that will eventually replace `horizon-rs`/lean-horizon as the deploy-substrate root. /173 confirms it stays. |
| `/home/li/primary/reports/system-operator/166-dji-mic-profile-churn-fix-2026-05-28.md` | KEEP | NOT deploy-stack; speech runtime. Flag for sub-agent D. |
| `/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md` | KEEP + flag for sub-agent D | The lane's just-ran successor ledger. Its retirement gating depends on the NEXT system-operator maintenance pass. Per `skills/context-maintenance.md` §"Successor sweeps retire maintenance ledgers" — keep until the next sweep. |

### cluster-operator (1 report)

`/home/li/primary/reports/cluster-operator/1-bird-zeus-local-update-authority-design.md`
— KEEP with MIGRATE-on-next-occasion recommendation. Foundational
`SystemUpdateGrant` authority-pattern design; enumerates option
(A)/(B)/(C) for action granularity AND for soul-repo topology, so §3a
guard applies. MIGRATE the settled parts (the noun, sudo-rule shape,
CriomOS helper pattern, `lojix-cli` `SystemTarget::Local`/`Remote`
split) into `/git/github.com/LiGoldragon/horizon-rs/INTENT.md` +
`/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md` +
`/git/github.com/LiGoldragon/lojix-cli/INTENT.md` when the psyche
resolves the open questions OR the pattern is implemented. Until
then KEEP. Lane at 1 report; no maintenance pressure.

### system-designer (this dispatcher's lane)

The dispatcher's lane is the FRAME / METHOD slot for this sweep —
sub-reports 1-4 are written by other sub-agents; slot 5 is the
dispatcher's overview. The deploy-stack-relevant system-designer
report in scope here is `/34/` (the MVP/sandbox audit bead queue).
Verdict: KEEP — still load-bearing (per /49 explicit deferral). No
drops in this slot.

The dispatcher's prior sweep
(`/home/li/primary/reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`)
retires once THIS sweep's handoffs reissue; per `skills/context-maintenance.md`
§"Successor sweeps retire maintenance ledgers" the dispatcher actions
that retirement in the overview slot (5), not here.

## Landing evidence (for every Drop recommendation)

| Report dropped | Landing — successor report or permanent home |
|---|---|
| `/home/li/primary/reports/cloud-operator/6-recent-intent-reports-branch-read-2026-05-26/` | `/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md` §"Recent intent surface" + live `/git/github.com/LiGoldragon/{nota-next,schema-next,schema-rust-next,schema-core,horizon-next}/`. Schema-stack design now in `/home/li/primary/INTENT.md` §"schema-driven stack" + §"Three schema types, three runtime planes" + §"Recurring architectural patterns" + /49. |
| `/home/li/primary/reports/cloud-operator/7-refresh-intent-reports-visual-audit-2026-05-26/` | Same as /6. Free-function findings now in AGENTS.md hard override "Every Rust function is a method or associated function"; bracket-string ambiguity resolved per /49; 3-block vs 5-block root resolved per /49 (ASSchema landed; macros-as-data per record 1109-1116). |

cloud-operator/12, /13 and system-operator/173 are KEEP-with-handoff
(not drops); landing gated on each lane's NEXT sweep.

## Drop ownership / handoff

Dispatcher executes drops only in its own lane; other lanes apply on
their next maintenance pass.

### cloud-designer (next maintenance)

No drops; lane's own /15 is the active ledger. Live decision queue
from /15 (cross-listed for the overview's psyche-attention items):
gap-1 lane scope (split Arc A out?), gap-2 Arc A fate (revive / merge
`ec2d3493` Cloudflare branch / park?), gap-3 backup-network
independence (Path A or Path B), gap-4 Gemma 4 llama.cpp `b9404`
(critical path, operator-implementing), gap-5 quant set (BF16 +
UD-Q4-K-XL + optional Q8?). Migration candidates: deploy-safety rule
→ `/home/li/primary/skills/nix-discipline.md`; audit-loop discipline
→ `/home/li/primary/skills/audit-loop.md`; browser-on-local-AI 3-tier
→ `cloud/ARCHITECTURE.md` or `criome-config/ARCHITECTURE.md`.

### cloud-operator (next maintenance)

Drops it owns: `/home/li/primary/reports/cloud-operator/6-recent-intent-reports-branch-read-2026-05-26/`
+ `/home/li/primary/reports/cloud-operator/7-refresh-intent-reports-visual-audit-2026-05-26/`
(both with landing in /49 + live source). Re-evaluate next sweep: /12
(skill-update ledger landed), /13 (small operational — resolve
follow-up or bd item). Keeps: 9, 10, 11.

### system-operator (next maintenance)

Lane just self-swept
(`/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md`).
This sweep RATIFIES; no additional drops in deploy topic. /173 itself
re-evaluates on lane's next sweep.

### cluster-operator (next maintenance)

KEEP + recommend MIGRATE eventually:
`/home/li/primary/reports/cluster-operator/1-bird-zeus-local-update-authority-design.md`
— migrate settled `SystemUpdateGrant` design into the three
production-side INTENT/ARCHITECTURE docs (named above) when the
psyche resolves open questions OR the pattern lands. Until then KEEP
under §3a guard.

## Cross-topic edges (flagged for the overview)

- `/home/li/primary/reports/cloud-operator/11-lojix-horizon-criomos-intent-implementation-audit-2026-05-28.md`
  cross-cuts SCHEMA (A) and DEPLOY (here). D1/D2/D5 schema-language;
  D3/D7/D8/D9 deploy-substrate. KEEP by both.
- `/home/li/primary/reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md`
  — the operator artifact /42 audits. KEEP both topics.
- `/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`
  — sub-agent A's anchor; deploy-side uses it as the
  schema-substrate-replacement closure (horizon-next IS the deploy
  substrate replacement once gate 2 lands).
- `/home/li/primary/reports/system-operator/166-dji-mic-profile-churn-fix-2026-05-28.md`
  — NOT deploy-stack (speech runtime). Flag for sub-agent D.
- `/home/li/primary/reports/cloud-operator/13-pi-harness-abort-investigation-2026-05-28/`
  — NOT deploy-stack (Pi-harness operational). Flag for sub-agent D.

## Per-lane handoff summary

- **cloud-designer:** 0 drops; psyche-attention items gap-1..gap-5 +
  3 migration candidates carry to overview.
- **cloud-operator:** 2 drops (6, 7) with landing; 2 flag-for-handoff
  (12, 13); 3 active KEEP (9, 10, 11).
- **system-operator:** 0 additional drops (lane just self-swept). KEEP
  /167 cross-listed.
- **cluster-operator:** 0 drops; MIGRATE-when-resolved recommendation
  for /1 into horizon-rs + CriomOS-side INTENT/ARCHITECTURE docs.
- **system-designer (dispatcher):** 0 drops; /34/ (MVP bead queue)
  stays as the deferred-to-by-/49 active queue.

Topic carries ~2 confirmed drops + ~4 deferred-to-next-sweep + ~9
active KEEPs. Cloud-designer's own /15 already absorbed most of the
05-27/28 churn; this sweep RATIFIES with one critical addition:
flagging cloud-operator/6 + /7 as droppable now that the schema arc
has landed.
