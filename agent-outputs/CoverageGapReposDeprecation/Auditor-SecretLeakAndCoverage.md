# Independent Audit — Secret Leak + Coverage (t5vj integration, folds, manifest, retirements)

Separate-auditor pass on the t5vj record integration, ~40 INTENT->ARCHITECTURE
folds, 4 authored ARCHITECTURE.md, `protocols/repos-manifest.nota`, and 3
retirements. Read-only: no audit target was edited. Bar: prior "secret-leak
audit PASS".

## Executive verdict

- **SECRET LEAK: PASS.** No secret value, credential, token-as-value, gopass
  path-as-value, private key, or `<REDACTED>`-style placeholder was written to
  any canonical surface. Only mechanism / pattern / handle-path descriptions and
  Spirit record-id citations.
- **COVERAGE COMPLETENESS: PASS with one HIGH defect** (cloud INTENT.md on main —
  H1).
- **MANIFEST: PASS on structure/counts; one MEDIUM correctness gap** (doctrine-home
  staleness beyond the two named — M1).
- **SECTION-NAMING VARIANCE: ACCEPTABLE (not worth a normalization pass).**
- **HYGIENE: PASS.**

Highest-priority dimension (secret leak) clears the bar. One HIGH coverage defect
(trivial fast-forward fix) and one MEDIUM manifest staleness are the only
action items.

## CRITICAL

None.

## Dimension 1 — SECRET LEAK: PASS

Audited the true canonical surface of each repo (for `cloud` that is
`origin/main` = `efae1776`, NOT the stale on-disk working copy — see L2):

- `cloud`, `lojix`, `horizon-rs`, `CriomOS`, `CriomOS-home`, `goldragon`
  ARCHITECTURE.md — every secret touch is mechanism/handle only:
  sops-nix-held SSID/passphrase, gopass-fed tokens, credential-by-handle,
  `NIX_CONFIG` access-tokens, "the token value itself never enters source".
- Secret-referent record IDs appear ONLY as Spirit provenance citations, never
  as values: `iprx`/`nsi2` as `(Spirit \`iprx\`)` / `(Spirit \`nsi2\`)` on cloud
  origin/main; `2qhw` as `(Spirit \`2qhw\`)` in lojix §7. `wn7q` and `2qhw`
  values are not present anywhere. `go41`, `nz0t`, `osoo` do not appear as IDs in
  the target files; their non-secret substance is folded (OS report evidence).
- `go41` (secret-flagged, OS domain): its non-secret substance is redacted into a
  **single** "## Secrets scoping" section in CriomOS-home/ARCHITECTURE.md — once,
  not duplicated. Verified one heading, one occurrence.
- Dump redaction placeholders (`<REDACTED-GOPASS-PATH>`, `<REDACTED-BACKUP-SSID>`,
  `<REDACTED-BACKUP-WIFI-PASSWORD>`) were NOT reproduced. Independent grep for
  `<REDACTED`, literal `chrome-browser/playwright-...`, `hetzner/api-token`, and
  `cloudflare.com/api-token` in the OS + goldragon files: none.
- `goldragon/ARCHITECTURE.md` describes `secrets/` and "router SAE passwords" as
  material that "stays out of any public surface" — mechanism/naming-convention
  only, no value.

Borderline item (NOT a leak, logged for transparency — see L3): cloud origin/main
writes the gopass handle-path `cloudflare.com/api-token` and env-var name
`CF_API_TOKEN`. Both are handle/variable identifiers, which the redaction rule
explicitly permits ("only mechanism/pattern/handle-path descriptions") and the
secrets doctrine classes as non-secret.

## Dimension 2 — COVERAGE COMPLETENESS: PASS w/ one HIGH defect

Residual `INTENT.md` under `/git/github.com/LiGoldragon/`:

1. `CriomOS-test-cluster/INTENT.md` — EXPECTED. Removal + authored ARCHITECTURE
   are on bookmark `intent-curator/architecture-md` (also mirrored in the
   `CriomOS-test-cluster-arch` working dir); `main` legitimately still None.
2. `lojix-primary-5rzf-7/INTENT.md` — EXPECTED. Dirty jj workspace
   (`M README.md`, change `primary-5rzf-7-code-kill`); the live `lojix` main is
   clean (INTENT removed, ARCHITECTURE present).
3. `cloud/INTENT.md` — **DEFECT (see H1).**

Spot-checked 9 folded repos' `main` trees (agent, domain-criome, clavifaber,
repository-ledger, mentci, mirror, nota-config, meta-signal-agent, lojix): all
show INTENT.md removed + ARCHITECTURE.md present, and a Direction section present.
cloud is the sole anomaly.

## Dimension 3 — MANIFEST: PASS on structure; MEDIUM staleness gap

- Parses: RepoManifestStandup ran a real `nota::Document::parse` -> "PARSE OK: 1
  root object". Independent balance check: parens 256/256, brackets 121/121.
- Counts: 116 `(Repo ...)` records; 102 Active; 11 Content; 3 Deprecated records.
  (A `grep '(Deprecated'` returns 4 — the 4th is the schema-doc comment on line
  21, not a record.) 102 + 11 + 3 = 116.
- Retirements: `persona-pi`, `WebPublish`, `AnaSeahawk-website` all marked
  `(Deprecated [|remote archived + local deleted|])`, consistent with the
  retirement evidence (remotes archived, local clones deleted, references clean).
- NOTA hygiene: positional records, bare atoms for canonical strings
  (`github:LiGoldragon/<name>` is one atom), named enum variants — good.

Staleness (answer to "is that the only staleness?" — **NO**): see M1.

## Dimension 4 — SECTION-NAMING VARIANCE: ACCEPTABLE (verdict)

Observed forms for the folded Direction section:

- `## 0.5 · Direction` — lojix, mentci, mirror, nota-config, signal-frame,
  meta-signal-{agent,cloud,lojix,mind,spirit} (the G-P slice).
- `## Direction` — agent, domain-criome, clavifaber, repository-ledger.
- `## Direction and Principles` — cloud (origin/main).
- Content-local sub-headings (`### Direction: the LojixOS split`, `## Profile
  ladder direction`) in CriomOS / CriomOS-home — pre-existing content, not fold
  markers; correct.

VERDICT: acceptable, not worth a dedicated normalization pass. The variance
tracks each repo's local heading convention — numbered-section repos take
`0.5 ·` to slot before `§1`; prose-heading repos take a bare `## Direction` —
which is exactly architecture-editor's "match local conventions". The content is
semantically consistent and human-discoverable. Sole caveat: if any coverage
tool keys off the literal `§0.5`/`0.5 · Direction` anchor (the handover used that
phrasing as the canonical name), the plain-`## Direction` repos would be missed;
normalize only in that case. Low severity.

## Dimension 5 — HYGIENE: PASS

- `grep '^---$'` across every edited ARCHITECTURE.md (lojix, horizon-rs, CriomOS,
  CriomOS-home, goldragon, signal-standard, substack-cli), cloud origin/main, and
  the manifest: zero forbidden horizontal rules.
- Manifest: positional NOTA + bare atoms for canonical strings (confirmed).

## Findings (severity-ranked)

### HIGH

**H1 — cloud/INTENT.md not eliminated on origin/main.** cloud is a live mainline
repo (not the CriomOS-test-cluster branch exception, not a dirty workspace), yet
`origin/main` (`efae1776`) still carries `INTENT.md`. The removal commit
`704213b0` ("docs: remove INTENT.md ... redundant") exists and is pushed on
bookmark `intent-curator-fold`, and is a clean fast-forward descendant of
`main` — but `main` was never advanced to it. The direction substance itself DID
land (t5vj `## Direction and Principles` + `## Packaging` on `efae1776`), so this
is purely a stranded deletion. Fix is one step: fast-forward `cloud/main` to
`704213b0` and push. Until then it is exactly the "any OTHER residual INTENT.md
is a defect" case.

### MEDIUM

**M1 — Manifest doctrine-home staleness beyond the two named.** In addition to
`signal-standard` (`None`; known) and `CriomOS-test-cluster` (`None`; correct for
`main` since authored only on a branch), TWO more records are stale:
- `goldragon` — recorded `(OtherDoc README.md)`, but ARCHITECTURE.md is committed
  on main ("goldragon: add ARCHITECTURE.md"). Should be `Architecture`.
- `substack-cli` — recorded `(OtherDoc README.md)`, but ARCHITECTURE.md is
  committed on main ("substack-cli: author ARCHITECTURE.md"). Should be
  `Architecture`.
Both were authored this session (12:41-12:42) just before the manifest write
(12:46); the standup's doc-presence scan appears to predate the authoring.
Manifest is meant to be the authoritative inventory, so these two doctrine-home
fields are wrong.

### LOW / informational

**L1 — Section-naming variance.** See dimension 4. Acceptable; normalize only if
tooling depends on the exact `§0.5` anchor.

**L2 — cloud local /git checkout out of sync.** The jj working copy sits on
`3b38cdd8` (pre-t5vj), behind `main`/`origin/main` (`efae1776`), so the on-disk
files look pre-session. Canonical surface (origin/main) is correct; this is
local-state drift, related to H1 and the concurrent cloud-maintainer work.

**L3 — cloud gopass handle-path in prose.** `cloudflare.com/api-token` +
`CF_API_TOKEN` on cloud origin/main. Permitted (handle-path description, no
value); logged as the closest-to-the-line item, not a leak.

## What could not be exhaustively verified

- Every one of the ~116 repos' `origin/main` trees was not swept for residual
  INTENT.md; the working-copy `find` plus a 9-repo main-tree spot-check localized
  the only anomaly to cloud. A repo whose fold is stranded on a bookmark AND whose
  working copy is on main would be caught; one stranded like cloud but with a
  fold-era working copy would show in `find` (none other did).
- NOTA parse was taken from the standup's recorded real-parser run plus an
  independent bracket/paren balance; a fresh parser run was not re-executed here.
