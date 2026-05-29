# 3 — Topic: cloud + deployment (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2.
The cloud-component / cloud-deploy surface — Cloudflare DNS + provider
APIs, the `cloud` component triad + criome domain, browser-control →
local-AI (Gemma) redirection, HF prefetch, sops-nix / gopass secret
handling. The canonical lanes are NEW (`cloud-designer`,
`cloud-operator`, both born 2026-05-27); the older substance lives in
system-operator + second-designer + third-designer and should FORWARD
into the new cloud lanes.*

## The structural finding (priority = forward, not trim)

The cloud topic split into dedicated lanes on 2026-05-27. The two new
lanes are **under the 12-report cap** (cloud-operator 11, cloud-designer
6) and carry the current substance. The maintenance action here is
mostly the inverse of the schema topic: the OLDER cloud reports
scattered in system-operator / second-designer / third-designer should
**forward** into the cloud lanes (where future cloud agents will look),
then the source reports retire. The prior sweep (designer/386/12 §3 +
§3) flagged exactly this consolidation as overdue; the cloud lanes now
exist to receive it.

## Recency rank (newest canonical at top)

**Current surface (KEEP — the new cloud lanes):**

1. `cloud-designer/6/` (05-28) — secret-deploy + Gemma: sops-nix infra,
   llama + models, deploy mechanism, execution. **KEEP — newest cloud
   design; the secret-handling discipline here is a MIGRATE candidate
   to a `skills/secret-handling.md` (see below).**
2. `cloud-operator/11` (05-28) — also the newest Lojix audit (dual-
   topic). **KEEP (covered in sub-report 2).**
3. `cloud-designer/5/` (05-27) — browser + local-AI + HF prefetch
   design. **KEEP — current design.**
4. `cloud-designer/4/` (05-27) — fully-working prototype cycle (the
   operator checklist cloud-operator/10 implemented from). **KEEP.**
5. `cloud-designer/3` (05-27) — cloudflare CLI prototype. **KEEP.**
6. `cloud-operator/10` (05-27) — audited cloud/domain prototype impl
   (built from cloud-designer/4). **KEEP — current impl.**
7. `cloud-operator/9` (05-27) — Cloudflare DNS tool impl (first working
   path, old hand-written NOTA stack). **KEEP — current impl; note it
   uses the pre-schema-next stack, so it's a future schema-next-port
   candidate, not stale yet.**
8. `cloud-designer/1` (05-27) — cloud-designer lane bootstrap. **KEEP
   for now (lane-origin record); retire once the lane is fully
   integrated into workspace docs (its own stated exit condition).**

**Stale / forward band (by lane):**

### cloud-designer + cloud-operator — internal redundancy

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `cloud-designer/2/` cloud-component design recap | 05-27 | Recap superseded same-day by `/4/` (fully-working prototype cycle, which re-surveys spirit + reports + repos) | DROP — `/4/` is the fuller successor recap |
| `cloud-operator/8` cloud-component design recap | 05-26 | Duplicate of cloud-designer/2's recap from the operator side; superseded by cloud-operator/10 (real impl) | DROP — superseded by the implemented prototype |

**2 cloud-lane reports** DROP (both superseded recaps). The cloud lanes
are otherwise clean and under cap.

### system-operator — cloud-foundation reports (FORWARD to cloud lanes)

These are the **pre-lane-split** cloud-foundation reports. All authored
under the now-**retired** `system-specialist`/`second-system-assistant`
lanes (e.g. 158's header literally reads "Lane: system-specialist
assistant"):

| Report | Date | Disposition |
|---|---|---|
| `156` Cloudflare API surface research | 05-23-era | FORWARD → cloud-operator (API research feeds the DNS tool) then DROP |
| `157` provider API scope research | 05-23-era | FORWARD → cloud-operator then DROP |
| `158` signal-foundation for cloud triads | 05-23 | FORWARD → cloud-designer (the triad-signal foundation) then DROP |
| `159` cloud repo scaffold prototype | 05-23-era | FORWARD → cloud-operator (scaffold superseded by real `cloud` repo per cloud-operator/9) then DROP |
| `160` cloud-domain criome birth design | 05-23-era | FORWARD → cloud-designer (criome domain design) then DROP — likely already absorbed in cloud-designer/4 |
| `139` arca daemon content-addressed store architecture | 05-17 | KEEP-or-MIGRATE — this is the **arca CAS** architecture, arguably its own topic; if arca is live it migrates to `repos/arca/INTENT.md`, else it's historical. Not strictly cloud. Flag for system-operator. |

**5 system-operator reports** FORWARD-then-DROP (156-160) + 1 (`139`)
keep-or-migrate. Most of 156-160's substance is **probably already
absorbed** in cloud-designer/4's survey (which states it mined existing
intent + reports + prototypes) — the cloud-designer agent should
confirm absorption before the system-operator agent drops them. This is
a **cross-lane forward**: system-operator owns the drop, but cloud-
designer/cloud-operator confirm the substance landed first.

### second-designer — cloud-component design

| Report | Date | Superseded by | Recommendation |
|---|---|---|---|
| `196` cloud-component production design | 05-25 | cloud-designer/4 (fully-working prototype cycle) + cloud-operator/10 | FORWARD → cloud-designer then DROP — production-design substance now in the live cloud lanes |

**1 second-designer report** FORWARD-then-DROP.

### third-designer — cloud-criome research

| Report | Date | Superseded by | Recommendation |
|---|---|---|---|
| `22/` cloud-criome design research | 05-24 | cloud-designer/2+4 (criome domain design) + system-operator/160 | FORWARD → cloud-designer then DROP — research absorbed by the cloud lane's design cycle |

**1 third-designer report** FORWARD-then-DROP.

## MIGRATE candidate (permanent doc)

`cloud-designer/6/` documents a **never-show secret-handling
discipline** (gopass env-var wrapping + sops-nix cluster secrets,
"handle secrets without ever seeing them"). Per its own directive this
is meant to land in **skills** — recommend MIGRATE the discipline to a
`skills/secret-handling.md` (or an existing system/deploy skill).
Checked: no `skills/secret*.md` exists today. This is a genuine
permanent-doc gap, not a report-keep. Flag for the cloud-designer /
system-designer to create the skill; the report retires once the
discipline is in the skill.

## Stale-flag count for this topic

**~10 reports** flagged stale/forward: cloud-lane 2 (internal recap
dups), system-operator 5 (forward 156-160) + 1 keep-or-migrate (139),
second-designer 1 (196), third-designer 1 (22/). Plus 1 MIGRATE
candidate (cloud-designer/6 secret discipline → new skill).

## Drop ownership by lane (handoff)

- **When `cloud-designer` next does maintenance, the cloud drops it
  owns are:** 2/ (recap superseded by 4/). Plus: CONFIRM absorption of
  inbound system-operator/156-160 + second-designer/196 + third-
  designer/22 before those lanes drop them. MIGRATE: the cloud-
  designer/6 secret-handling discipline → a new skills/secret-handling.md.
- **When `cloud-operator` next does maintenance, the cloud drop it owns
  is:** 8 (recap superseded by 10). Otherwise clean + under cap.
- **When `system-operator` next does maintenance, the cloud forwards it
  owns are:** 156, 157, 158, 159, 160 (forward to cloud lanes, then
  drop once cloud-designer confirms absorption). Keep-or-migrate: 139
  (arca CAS).
- **When `second-designer` next does maintenance, the cloud forward it
  owns is:** 196 (→ cloud-designer).
- **When `third-designer` next does maintenance, the cloud forward it
  owns is:** 22/ (→ cloud-designer).
