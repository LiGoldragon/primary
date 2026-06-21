# Big trim — COMPLETE

The Spirit intent-store audit and trim is applied to production and validated.

## Result

| Metric | Before | After |
|---|---|---|
| Active records | 1323 | **613** (−54%) |
| Records with referents | 7% (93% empty) | **99%** (608/613) |
| Total description text | ~448 KB | ~246 KB (−45%) |
| Mini-essays (≥800 chars) | 72 | 34 |
| Distinct referents | 58 | 843 (kebab) |

- **737 records nominated** (certainty Zero — hidden from queries, fully
  recoverable). Active 1262 → 613 = the 649 final nominations (plus 80 done
  earlier). Total in store: 1350 (613 active + 737 hidden) — nothing deleted.
- Merges verified (e.g. `kasm`+`ut6z`+… → `kasm` survives with the unified
  arrow + kebab referents; `ut6z` nominated). Survivors carry kebab referents
  (`j6r4`→`[spirit certainty certainty-rubric]`, `cws0`→`[spirit intent-log]`).

## What was deployed (production, ouranos)

- **spirit 0.15.0 owner-import bypass** (`mjjjcmvby7w…`, commit `7fc267cb` on
  spirit main): meta-socket `Import` auto-registers referents (guardian-free,
  owner-trusted), **upserts in place** (overwrite existing id), and **enforces
  lowercase kebab-case on new referent registration** (existing names
  grandfathered). Deployed via lojix home activation (CriomOS-home `main`,
  which another lane had already repinned to `7fc267cb`).
- Net effect: bulk owner curation costs no paid-guardian calls; future
  referents are kebab-only.

## Bugs found and fixed along the way

1. **Insert-only import** — `import_record` used SEMA `assert` (rejects an
   existing key), so the bypass could only restore into empty keys, never
   overwrite a live record. Every survivor upsert failed `InternalError`.
   Fixed → `mutate` when the id exists, `assert` when new.
2. **NOTA double-escape + parser hang** — `enc_str` escaped `|]` but not `\`,
   double-escaping descriptions that contain block-string syntax (records
   *about* NOTA). The daemon's parser **hung** on the malformed escape
   (record `f8m3` consistently stalled batch 009). Fixed encode to match
   nota-next `escape_pipe_text` (`\`→`\\`, `|]`→`\|]`) and the parser-side
   unescape (`\X`→`X`). The parser hang on bad escapes is itself a nota-next
   robustness bug worth a separate fix.
3. One invalid plan domain (`Technology.Software.Networking`) remapped to a
   valid taxonomy variant.

## Execution mechanics

The terminal/harness repeatedly died (killing harness-tied background jobs and
the partial trim). Root mitigation: ran the trim as a **`systemd-run --user`
transient unit** (owned by the user systemd manager — survives terminal/harness
death) and monitored with short non-blocking reads only (no `sleep`-loops /
`timeout`, which destabilize the harness). The final run: 590 imports +
649 nominations, 0 failures.

## Archive / recoverability (the trimmed bits)

- `archive/trimmed-zero-records.{json,nota}` — full content of all 737
  nominated records (the trimmed bits).
- `raw/records.json` / `raw/all-active.nota` — pre-audit snapshot (all 1323).
- Pre-trim store backups: `~/.local/state/spirit-audit-backup/`
  (`spirit.sema.pre-bigtrim`, etc.).
- Daemon versioned commit log retains full history incl. testimony.
- Nominated records are at certainty Zero — restore by raising certainty.

## Residuals (minor, optional follow-up)

- **34 mini-essays remain** (≥800 chars) — large merges that concatenated
  rather than condensed; could be condensed in a follow-up pass.
- **2 non-kebab referents** (`CriomOS`, `Horizon`) on records added
  concurrently (outside the audit snapshot); normalize to `criomos`/`horizon`
  when convenient.
- **5 active records have no referents** (name no particular) — acceptable.
- ~23 active records are concurrent additions not in the audit plan (untouched).
- Spirit intent not yet recorded for the kebab-referent rule + bsrv carve-out
  (`3-synthesis-and-handoff.md` §8) — record once confirmed.
