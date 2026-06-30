# Handover — per-repo doctrine coverage gap + `repos/` deprecation

Fresh-context session. Two-part focus: (1) close the per-repo doctrine
campaign's coverage gap; (2) deprecate the `repos/` symlink surface.

## Settled psyche intent

- Doctrine in force: no `ESSENCE.md`, no per-repo or workspace `INTENT.md`. A
  repo's durable direction lives in its `ARCHITECTURE.md` or in code (a stub
  with an explanatory comment counts). This is matter — it lives in the
  `repo-intent` / `architecture-editor` / `intent-manifestation` /
  `intent-clarification` / `push-not-pull` skills and `AGENTS.md`, not Spirit.
- `private-repos/` access is open (inspect/edit like any untracked repo); the
  leak gate stands — private content stays out of public reports, public
  Spirit, public commits, and chat.
- Secret-adjacent record content is redacted in place: integrate the non-secret
  substance, never the value.
- Deprecate `repos/`. The `repos/` symlink surface is stale (never re-synced as
  new repo families were added) and caused a ~47% coverage miss in the per-repo
  campaign. The psyche wants it deprecated.

## Confirmed facts

- `/git/github.com/LiGoldragon/` holds 116 repos. The campaign covered the 62
  symlinked under `repos/` and missed 54. 43 of the 54 still carry an
  `INTENT.md`. (agent-outputs/PerRepoDoctrineCoverageGap/Scout-SituationalMap.md)
- Missed families: the cloud surface (`cloud`, `signal-cloud`,
  `meta-signal-cloud`), `domain-criome`, much of `meta-signal-*`, and the
  `mentci` / `mirror` / `lojix` / `repository-ledger` families. All 54 missed
  repos are clean (no dirty tree). `CriomOS-test-cluster` and `signal-standard`
  carry `INTENT.md` but have no `ARCHITECTURE.md` fold target.
- Root cause is the stale `repos/` symlinks; workers can target
  `/git/github.com/LiGoldragon/<name>` directly.
- The 31 deferred code/config records (bead `primary-t5vj`) all map to LIVE
  repos: cloud-daemon → `cloud`; cloud-node/trust → `goldragon` (jj-only data
  repo, push-immediately; its `cloud-node-data` branch already homes `5pf6` /
  `zeqq`); deploy → live `lojix` (NOT the retired `lojix-cli`); OS →
  `CriomOS` / `CriomOS-home`. None warrant "drop." Cloud subset is 10 records:
  `150a 16l0 7kyx 8fe9 iprx m3eg mbmy nsi2 5pf6 zeqq`.
  (agent-outputs/SpiritArchiveRehoming/Scout-CloudRecordHomeVerdict.md)
- Secret-flagged ids: `go41` redacted into CriomOS-home; `wn7q` and `2qhw` never
  written anywhere. Secret-adjacent referents `nz0t` / `nsi2` / `iprx` / `osoo`
  route intent to the config surface, never the value.

## Completed this session (pointers, do not redo)

- Doctrine cutover landed: `ESSENCE.md` + workspace `INTENT.md` eliminated,
  content in `ARCHITECTURE.md §0.5`; skills + `AGENTS.md` reversed. Pushed.
- `private-repos/` access opened in `AGENTS.md` + skills. Pushed.
- `INTENT.md` eliminated across the 62 covered repos (incl. recovered `system`
  direction). Pushed.
- ~457 archived records rehomed into ~30 covered repos + workspace
  `ARCHITECTURE.md`; secret-leak audit PASS. Pushed.
- `lojix-cli` retired (remote archived, local deleted); `schema-cc` retired
  (superseded by in-tree `schema-next/schema-cc/`); `persona-mind`→`mind` rename
  landed.
- Spirit early pass: epic `primary-6obv` — Phase 1 (`primary-ay9d`), the T4
  record beads, and the ESSENCE-cutover beads (`lsip`, `sfr3`) CLOSED. Epic OPEN
  at 12/19.
- The 505 archived records are extracted to the local, non-committed dump
  `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`; routing at
  agent-outputs/SpiritArchiveRehoming/RoutingManifest.md.

## Open for the focus

- The 43 missed repos still have `INTENT.md` to eliminate → `ARCHITECTURE.md`
  (author one for `CriomOS-test-cluster` and `signal-standard`).
- The 31 `t5vj` code/config records await integration into their live homes
  above; bead `primary-t5vj` is DEFERRED with this note.
- `repos/` deprecation is intent only — not executed.

## Live uncertainties / suspicions (preserved as such)

- The `/tmp` dump is non-committed and may not survive a fresh environment; it
  may need re-extraction (read-only scratch-daemon restore of the
  `preremoval-631` snapshot — method recorded under
  agent-outputs/SpiritArchiveRehoming/).
- The 505-record routing was bounded to the 62 covered repos; whether other
  deferred or mis-routed records belong in the now-found missed repos is
  unverified — the routing never saw them.
- Remote liveness of the 54 missed repos was not checked; Spirit was not queried
  for them.
- Skill and agent surfaces churned under concurrent activity during the session
  (skill/agent-type names flip-flopped); verify current state rather than trust
  any snapshot.

## Still-open original tracks (in epic `primary-6obv`, not this focus)

- Testimony-gated re-captures: T1 `smwa`, T2 `bvsd`, T8 `e191` — need raw psyche
  testimony at execution time.
- T5 `7wld` (human-facing Spirit manual), T6 `g28b` (certainty-vs-importance,
  observation-only), T7 `zpgw` (appeals + whole-cleanup audit).

## Agent-output pointers

- agent-outputs/PerRepoDoctrineCoverageGap/Scout-SituationalMap.md — the 54
  missed repos with `INTENT.md`/`ARCHITECTURE.md` status.
- agent-outputs/SpiritArchiveRehoming/Scout-CloudRecordHomeVerdict.md — `t5vj`
  record homes.
- agent-outputs/SpiritArchiveRehoming/RoutingManifest.md — the 505-record
  routing.
- reports/legacy-disposition/SITUATION-2026-06-30-parked-spirit-tracks.md — the
  original 8-track situation.
