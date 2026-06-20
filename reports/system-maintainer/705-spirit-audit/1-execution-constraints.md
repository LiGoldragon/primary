# Execution constraints discovered at pipe-clean

The rebuild plan is excellent: **1323 → 591 active records (55% reduction)**,
partition perfect (every id accounted for exactly once), referents designed
for all 591, all kebab-valid. `raw/plan2.json` holds the rendered operations.

But executing it against the live daemon surfaced three hard constraints.

## 1. The guardian is paid cloud inference (DeepSeek)

Every content write (`Supersede`, `ChangeRecord`, `Retire`, `Remove`) is
judged by the agent guardian, which is `agent-daemon` → `deepseek-v4-flash`
at `api.deepseek.com` — **paid cloud inference**. Per host-safety, this
needs explicit psyche approval for a bulk run. `ChangeCertainty Zero`
(nominate) is the only mutating op that bypasses the guardian (free, instant).

## 2. ~24 s per guardian-judged write, serialized

Measured: first call 48 s (cold), steady state ~24 s/op. Concurrency does
**not** help — the guardian serializes (8 concurrent ops completed
sequentially at ~24 s spacing). So wall-time is roughly linear:

| Work | Guardian ops | Est. wall-time |
|---|---|---|
| Merges (269 `Supersede`) → the core consolidation | 269 | ~1.8 h |
| Removals (81 `ChangeCertainty Zero`) | 0 (free) | seconds |
| Referents-on-everything + condensing (317 `ChangeRecord`) | 317 | ~2.1 h |
| **Full plan** | **~587** | **~3.9 h** |

Count reduction to 591 needs only the 269 merges + 82 removals; the 317
`ChangeRecord`s are purely the "referents on everything" + mini-essay
condensing (they modify kept records, don't change the count).

## 3. ~37% guardian rejection rate (fixable)

On an 8-op probe, 5 accepted, 3 rejected:
- **`NonReferent`** (×2): the referent-guardian rejects abstract concepts
  used as referents (`certainty`, `certainty-rubric`, `intent-maintenance-skill`)
  — it only admits named particulars. Fix: filter proposed referents to
  registered names + clear particulars; retry-on-reject dropping the
  offender, falling back to already-registered referents only.
- **`InsufficientWarrant`** (×1): the guardian intermittently finds the
  blanket authorization quote insufficient for a specific change (DeepSeek
  non-determinism — the same quote was accepted on 5 other records). Fix:
  retry; strengthen per-op reasoning.

## Already executed at pipe-clean (a few paid calls)

- `btio`+`r57r` merged → new `cws0` (the removal-discipline arrow).
- 5 referent-adds applied: `rvnf`, `icpa`, `tfpd`, `ek8w`, `tbg6`.
- `2qac` nominated (certainty→Zero) — consistent with plan2.
- 3 rejections logged (`raw/exec-log.jsonl`).

## Recoverability

All trims are recoverable: the daemon's versioned commit log is the
authoritative replayable history (removals land as `Retract` tombstones
retaining justification), plus the file archive (`raw/records.json` = all
1323 originals; `archive/trimmed-records.md` generated post-run).
