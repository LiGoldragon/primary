# 149 — Cleanup ledger 2026-05-13

*Designer ledger consolidating the 2026-05-13 cleanup pass.
Supersedes /147 (the first-half cleanup snapshot taken before
the big consolidation). Records what was deleted, what was
absorbed into ARCH, what beads moved, and what outstanding
items the cleanup surfaced.*

---

## 0 · TL;DR

| Surface | Before | After |
|---|---|---|
| Designer reports | 28 | 6 |
| Open beads | 50 | 42 |
| Stale cross-references in surviving reports | several | none in deleted ranges |
| Reports absorbed into `persona/ARCHITECTURE.md` | n/a | 6 (/110, /114, /115, /119, /125, /127) |
| Reports absorbed into `criome/ARCHITECTURE.md` | n/a | 1 (/141) |
| Reports consolidated into /148 prototype-one | n/a | 5 (/142, /143, /144, /145, /146) |
| Reports deleted as stale/superseded | n/a | 13 (the first-pass /112, /113, /122, /126, /128, /131, /132, /133, /134, /135, /136, /137, /138) |

Surviving designer reports (6):

| # | Title | Why kept |
|---|---|---|
| /129 | sandboxed-persona-engine-test | Active spec; no clean migration target — `persona-engine-sandbox` is not a separate repo. |
| /139 | wifi-pki-migration-designer-response | Active cross-role guidance to system-specialist /117; concrete shape decisions for horizon-rs + clavifaber. |
| /140 | jj-discipline-after-orphan-incident | Historical incident record cited from `~/primary/skills/jj.md`. |
| /148 | persona-prototype-one-current-state | Consolidates /141-/146 thread; prototype-one acceptance roadmap. |
| /149 (this) | cleanup ledger | The record of today's cleanup. |
| /150 (next) | signal-network design draft | Per user direction; replacing `primary-uea`. |

---

## 1 · Substance migrations into ARCH

The persona/ARCH and criome/ARCH absorption is the structurally
important move. Each migration is a one-way irreversible promotion
of report substance to architecture truth.

### 1.1 · Into `persona/ARCHITECTURE.md`

| Source | ARCH section | Substance |
|---|---|---|
| /114 §0 (panoramic vision) | §0.5 | Already covered before today; verified intact. |
| /119 status banner (deferred record) | §0.7 (new) | persona-system paused; FocusTracker is real; plan substance frozen. |
| /115 §1, §3, §6 | §1.5 | Already covered before today; verified intact. |
| /125 §1.1-1.2 (filesystem-ACL trust) | §1.6.1 (new) | Socket-mode table; rationale for filesystem ACL over crypto-first. |
| /125 §2 (origin types) + /115 §6 | §1.6.2 (new) | `ConnectionClass` + `MessageOrigin` closed enums; `signal-persona-auth` placement. |
| /125 §3 (channel choreography) | §1.6.3 (new) | Router-holds / mind-decides; `Channel` record; structural-channels pre-install table; adjudication sequence diagram. |
| /125 §3.5 (cross-engine routes) | §1.6.4 (new) | Cross-engine routes collapse into channels. |
| /125 §4 (multi-engine upgrade) | §1.6.5 (new) | Engine-level upgrade replaces hot-swap. |
| /127 D1, D2, D6 | §5 (expanded boundary table) + §5.1, §5.2, §5.3 (new) | Lock-and-cache injection; transcript typed observations; terminal-cell control-plane vs data-plane; HarnessKind closed; MessageBody grows by variants. |
| /110 (cluster-trust placement) | §7 (expanded constraint) | Cluster-trust is a new sibling component — not in criome, not in persona, not inside ClaviFaber. |
| New constraints from /125 §7 and /127 §7 | §7 (appended) | Socket modes; MessageOrigin stamping; channel choreography invariants; terminal injection invariants; HarnessKind closure; MessageBody discipline. |
| New invariants | §8 (appended) | Filesystem-ACL trust; `ConnectionClass`/`MessageOrigin` is provenance not authority; authority comes from channel state; HarnessKind closed; terminal-cell data plane non-mailboxed. |

### 1.2 · Into `criome/ARCHITECTURE.md`

| Source | ARCH section | Substance |
|---|---|---|
| /141 §0-§N | criome/ARCH §0-§N | Already absorbed before today (per its archaeology note citing /141 explicitly). Cluster-trust folded in (subsuming /110). |

### 1.3 · Into `/148`

| Source | /148 section | Substance |
|---|---|---|
| /142 (supervision-in-signal-persona) | /148 §2, §4, §5, §6 | Supervision relation; ComponentProcessState; two reducers; typed Unimplemented variants. |
| /143 (prototype-readiness gap audit) | /148 §3, §4, §5, §6, §8 | SpawnEnvelope record; ComponentProcessState; reducer tables; Unimplemented variants; Witness 1. |
| /144 (final cleanup after DA/36) | /148 §3, §8 | SpawnEnvelope vs ResolvedComponentLaunch; ComponentName disambiguation; two-witness acceptance. |
| /145 (component vs binary naming correction) | /148 §7 | `-daemon` suffix is binary-only; component names stay bare. |
| /146 (introspection component) | /148 §10 + persona/ARCH §0.6 | persona-introspect planned; three-layer contract placement; deferred until two introspection slices land. |

---

## 2 · Reports deleted (25)

Today's deletions, grouped by reason:

**Stale / superseded by /142+ thread** (5):
- /122, /126, /128, /132, /134

**Discipline statement / one-shot analysis** (4):
- /112, /131, /133, /147

**Audit on retired component** (1):
- /113 (persona-wezterm audit; persona-wezterm retired)

**Closed thread; substance in skills/code** (4):
- /135, /136, /137, /138 (NotaEnum policy thread → `~/primary/skills/contract-repo.md`)

**Absorbed into persona/ARCH** (6):
- /110, /114, /115, /119, /125, /127

**Absorbed into criome/ARCH** (1):
- /141

**Consolidated into /148** (5):
- /142, /143, /144, /145, /146

Git history preserves all 25 deleted reports per
`~/primary/skills/reporting.md` §"Hygiene". Future readers
finding a stale `designer/N` reference can use `jj log` /
`git log` to retrieve the deleted content.

---

## 3 · Bead state changes

### 3.1 · Closed (8 total today)

| Bead | Reason |
|---|---|
| `primary-2y5.4` | Engine manager catalog design absorbed into /148 §3-§5 + persona/ARCH §1.5. |
| `primary-2y5.6` | Superseded by `primary-devn`; in-flight skeleton work continues under that umbrella. |
| `primary-tlu` | `Persona*` prefix sweep done for live workspace; remaining hits in retired repos. |
| `primary-0ty` | Discipline statement (anti-pattern A); rule lives in `~/primary/skills/skill-editor.md`. |
| `primary-9iv` | Premise stale: persona-orchestrate retired; persona-sema retired; source `/93` deleted. Current persona-mind work tracked by `primary-hj4` + `primary-nurz`. |
| `primary-915` | criome Ractor→Kameo migration shipped (verified: no ractor dep; kameo = 0.20 active). |
| `primary-q3y` | lojix-cli Ractor→Kameo migration shipped (verified: no ractor dep). |
| `primary-92n` | nexus migration not done; closed-and-refiled with concrete file pointers per user direction. |
| `primary-oba` | Two of three blockers resolved (primary-9h2 disavowed, skills/designer.md + skills/operator.md shipped); residual docs integration folds into `primary-obm`. |

### 3.2 · Refiled with concrete file pointers (4 new)

Per user direction 2026-05-13 (Ractor verification sweep):

| Bead | Scope |
|---|---|
| `primary-iqbh` | nexus Ractor migration (4 files: daemon.rs, connection.rs, listener.rs, main.rs). Replaces `primary-92n`. |
| `primary-54ll` | hexis Ractor migration (3 files: proposer.rs, reconciler.rs, supervisor.rs). New — hexis wasn't in the original Ractor sweep. |
| `primary-9lun` | lojix-archive Ractor migration (8 files). New. |
| `primary-3te3` | forge: remove orphaned ractor dep (zero source usage). Quick cleanup. |

---

## 4 · Outstanding items surfaced by the cleanup

### 4.1 · Designer-shaped

- **/150 signal-network design draft** (per user direction; replacing `primary-uea`). Landing next as a draft sketch — not a final spec.

### 4.2 · System-specialist-shaped

- **`primary-tpd`** — *"Review headscale and Yggdrasil roles in CriomOS"* — user said they'll get system specialist on it (Yggdrasil's DHT shape is the puzzle).
- **`primary-obm`** — lore review + Nix migration. Open; carries the residual docs-integration work that closed `primary-oba` is no longer tracking.

### 4.3 · Operator-shaped Ractor cleanup

- `primary-iqbh` nexus (4 files; concrete pointers).
- `primary-54ll` hexis (3 files).
- `primary-9lun` lojix-archive (8 files; though may be subsumed by `primary-sff` lojix-core extraction).
- `primary-3te3` forge (orphaned dep; quick).

### 4.4 · Not-yet-decided

- `persona-introspect` daemon implementation — substance specified in `persona/ARCHITECTURE.md` §0.6 + `~/primary/skills/contract-repo.md`. Not on prototype-one critical path. First slice (terminal introspection records) tracked as track 21 inside `primary-devn`.

---

## 5 · Cap discipline outcome

The designer subdir was at 28 reports (cap 12) before today's
cleanup. After:

```
129 — sandboxed-persona-engine-test
139 — wifi-pki-migration-designer-response
140 — jj-discipline-after-orphan-incident
148 — persona-prototype-one-current-state
149 — cleanup ledger (this report)
150 — signal-network design draft (next)
```

**6 reports.** Half the soft cap. The discipline now in place:

- Architecture rationale → `<repo>/ARCHITECTURE.md` directly.
- Skills/discipline rules → `~/primary/skills/<name>.md`.
- Incident records → designer reports (when cited from skills).
- Prototype-implementation roadmaps → designer reports while
  the prototype is in flight (retire when the prototype is
  done).
- Cross-role responses → designer reports while the response
  is active (retire when the recipient role's work has
  absorbed the guidance).

Future designer work should push substance to its
canonical home as soon as it's stable, not let it accumulate
in reports. The DA/17 + /147 + /149 cleanup pattern is the
recovery path when the discipline slips.

---

## See also

- `~/primary/skills/reporting.md` §"Hygiene — soft cap, supersession, periodic review" — the discipline this pass implements.
- `~/primary/skills/beads.md` §"Periodic audit" + §"Anti-pattern A" — bead-side discipline.
- `~/primary/reports/designer-assistant/17-pre-today-report-cleanup-agglomeration.md` — the 2026-05-11 cross-role cleanup precedent.
- `~/primary/reports/designer/148-persona-prototype-one-current-state.md` — the consolidation that closed the /141-/146 thread.
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` — the absorption target for foundation reports.
- `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md` — the absorption target for the criome BLS substrate.
