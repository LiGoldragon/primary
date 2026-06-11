# Spirit corpus rebuild — executed (autonomous session, 2026-06-12)

The psyche authorized "go all the way": build the meta-spirit/Import feature, run the full
curation, and re-import into a fresh live store, to be reviewed after. This is the after-review
record. **Everything below is live.** Backups are retained and the cutover is fully reversible.

## What is live now

| Metric | Before | After rebuild |
|---|---|---|
| Total records | 1410 | **1327** |
| `Technology` | 13 | **1183** |
| `(Information Documentation)` catch-all | 1100 | **18** |
| Certainty = Maximum | reflexive | **7** |
| Certainty = Medium | ~0 | **781** |
| Certainty = High / Low | — | 389 / 81 |

The live daemon (0.9.3) serves the rebuilt store; `agent-daemon` + `spirit-daemon` both active.
Spot-checks confirmed: `0dsr` → `(Technology (Software (Data DataFormats)))`; the session's own
records (`opbj`/`nik8`/`8bwo`) survived with correct domains.

## What was removed (83 records — your ratifiable ledger)

Full manifest with evidence at `~/spirit-backups/pre-rebuild/manifest.json`. Summary:

- **46 duplicates** retired (merged into a canonical, lineage in the manifest).
- **26 superseded** — stale intent obsoleted by a later record (e.g. the `@`-sigil/pipe syntax
  chain, the Gemma-model reversal, the `persona-llm-client`→`agent` rename).
- **11 dropped** — non-intent / status reports / task-state (e.g. a point-in-time verification).
- **1325 survivors re-domained + certainty re-derived**; 2 records the analyzer missed were kept
  **unchanged** (never dropped). Invariant enforced: every original record is kept unless
  explicitly in drop/retire/supersede.

Nothing was lost silently. If you disagree with any removal, the original is recoverable (below).

## Domain corrections I made beyond the LLM manifest

The atomic import is a strict taxonomy validator. It surfaced LLM mistakes I auto-corrected:

- **11 mis-parented leaves** — a real leaf placed under the wrong subcategory (e.g.
  `Engineering/DependencyManagement` → the leaf actually lives under `Operations`). Reconstructed
  the correct parent chain from the (unique) leaf.
- **3 area-only survivors** the LLM left without a leaf — reassigned: `6zci` (Pi/Codex harness) and
  `zbfq` (agent-interaction skill) → `Technology/Software/Intelligence/AgentSystems`; `x83q` (Criome
  stack naming) → `Language/Terminology`. These three are worth a glance.

## The feature, landed (spirit 0.9.5, commit `5a518c41` on main)

- **Meta-signal `Import`** — writes pre-vetted records straight to the SEMA store with their given
  identifiers, **bypassing the guardian** (correct: the guardian gates unvetted *incremental*
  writes; a bulk restore of an already-curated corpus must not re-litigate each record). Aborts to
  `Rejected` on the first store error so a partial import is loud. Reuses the existing
  `store.import_record` primitive; one new `Engine::import`.
- **`meta-spirit` CLI** — the owner-only client, privileged sibling of `spirit`, mirroring
  `spirit.rs` over the existing `MetaSignalTransport`. Reads `SPIRIT_META_SOCKET`.
- Import is the general **restore/migrate** path (disaster recovery, machine moves), not a
  rebuild one-off. `ARCHITECTURE.md` updated. 15 daemon/meta integration tests pass.

## How the rebuild ran (so you can audit the method)

1. **Backup** — logical export of all 1410 records (`corpus-export.nota`) + binary store copy +
   pre-cutover live store/journal copies, all under `~/spirit-backups/pre-rebuild/`.
2. **Curate** (workflow, read-only) — re-domain + re-derive certainty + aggressively flag obvious
   nonsense + dedup/supersede → `manifest.json`. 1408 analyzed, 1326 survivors.
3. **Transform** — swap each survivor's domain + certainty into its intact original record;
   validate every path against the real taxonomy (`validate_domains.py`); produce `import.nota`.
4. **Validate** — stood up a transient daemon on a throwaway store, imported the full 1327, checked
   counts/distribution. Atomic import caught every invalid domain before anything live was touched.
5. **Cutover** — stopped the live daemon, backed up its store + guardian journal, swapped in the
   rebuilt store (both 0.9.3 and 0.9.5 use `SPIRIT_SCHEMA_VERSION = 8`, so format-compatible), reset
   the guardian journal (sequence would otherwise be non-monotonic), restarted, verified.

## Reversibility — how to roll back

Everything needed is in `~/spirit-backups/pre-rebuild/`:
- `live-spirit.sema.prerebuild` — the exact live store from before cutover (1410 records).
- `old-spirit.guardian.sema` — the pre-rebuild guardian journal.
- `corpus-export.nota` — every original record as NOTA.

Rollback: `systemctl --user stop spirit-daemon`, copy `live-spirit.sema.prerebuild` back to
`~/.local/state/spirit/spirit.sema`, restore the guardian journal, restart.

## The one thing I did NOT do (and why)

**I did not redeploy the live daemon to 0.9.5.** The rebuilt corpus is live and fully served by
the deployed 0.9.3 daemon (Import was used via a transient daemon to *build* the store; the live
daemon doesn't need Import for normal serving/gating). Deploying 0.9.5 means updating CriOMOS-home's
spirit pin and running a home-manager activation — a broad blast radius I judged unwise to fire
unattended. It's a clean follow-up:

```
# in CriOMOS-home: bump the spirit input pin to 5a518c41, then
lojix-run '(HomeOnly goldragon ouranos li [...] [github:LiGoldragon/CriOMOS-home/main] Activate None None)'
```

After that, `meta-spirit` works against the live daemon and the deployed binary matches main. Until
then, `meta-spirit`/`Import` is available only via a locally-built daemon (which is all the rebuild
needed).

## For your review

1. **The 83 removals** (`manifest.json`) — especially the 26 supersessions and 11 drops; say if any
   should come back.
2. **The 3 reassigned area-only records** (`6zci`, `zbfq`, `x83q`).
3. **The certainty re-derivation** — 781 now Medium, only 7 Maximum. Sanity-check the shape.
4. **Greenlight the 0.9.5 deploy** when you want Import live.
