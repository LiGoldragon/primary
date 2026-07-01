# Repos Manifest Standup — Implementation Evidence

## Task and scope

Stand up the authoritative repos inventory approved at the review gate
(`reports/legacy-disposition/PROPOSAL-2026-07-01-repos-manifest-and-active-set.md`),
and supersede the three overlapping inventory surfaces. Primary workspace.

## Sources consulted

- Approved design: `reports/legacy-disposition/PROPOSAL-2026-07-01-repos-manifest-and-active-set.md`
  (§2 manifest design, §2b schema, §2c worked example, §1 active-set classification).
- Classification source (per brief, no live-read of the three retiring repos):
  `agent-outputs/RepoManifestDiscovery/Scout-MissedRepos.md`,
  `Scout-CoveredRepos.md`, `Scout-DependencyGraph.md`.
- Convention mirrored: `repos/skills/manifests/skills-roster.nota`,
  `module-dependencies.nota`; skill `nota-design`.
- NOTA grammar ground-truth: `/git/github.com/LiGoldragon/nota-next/src/parser.rs`
  (`parse_atom` confirms `:` `/` `.` `-` are valid bare-atom characters, so
  `github:LiGoldragon/<name>` is one atom).

## Changed / created files

- CREATED `protocols/repos-manifest.nota` — the authoritative inventory. NOTA,
  positional `(Repo ...)` records mirroring the manifests convention. One record
  per repo, all 116.
- REWROTE `RECENT-REPOSITORIES.md` — retired its stale table (still listed absent
  `lojix-cli` / `persona-spirit`); now a superseded stub pointing to the manifest.
- EDITED `protocols/active-repositories.md` — intro now names the manifest as the
  authoritative inventory and reframes this file as the attention map + role
  narrative; "manifest wins on disagreement". Rich per-repo prose preserved
  (it is cited by workspace `ARCHITECTURE.md` §0.5).
- EDITED workspace `ARCHITECTURE.md` — §1 file tree adds `repos-manifest.nota`
  and marks `RECENT-REPOSITORIES.md` as a superseded stub; §3 "Repos surface"
  names the manifest authoritative and states coverage runs filter `Active` and
  iterate `/git/github.com/LiGoldragon/<name>` directly; §4 "Boundaries" adds the
  manifest to the owned list. The `repos/` symlink surface is left intact (its
  deprecation is owned by a separate worker).

## Manifest schema (as built)

`(Repo <name> <remote> (Family <family>) <status> <doctrine-home> [<flag> ...])`

- status enum: `Active` | `Content` | `(Deprecated <disposition-pipe-text>)`.
- doctrine-home: `Architecture` | `(OtherDoc <path>)` | `(CodeStub <path>)` | `None`.
- fact-flags: `IsFork` `IsPrivate` `BuildTimeConsumed` `DataRepo`.
- Family rule: `signal-*` -> Signal, `meta-signal-*` -> MetaSignal, every other
  repo groups by subsystem/cluster (Nota Schema Sema Persona Cloud DomainCriome
  Criome Mentci Mirror Lojix RepositoryLedger CriomOS Content Tooling Fork).

## Classification counts (116 repos = 62 covered + 54 missed)

- Active: 102
- Content: 11 (ArtificialIntelligence, BookOfGoldragon, BookOfLuna, TheBookOfSol,
  caraka-samhita, criomos-horizon-config, goldragon, library, lore, qmkBinaries,
  kibord)
- Deprecated: 3 (persona-pi, WebPublish, AnaSeahawk-website) — disposition
  "remote archived + local deleted"; psyche-authorized retirement per the gate.

Fact-flags applied: IsFork {kameo, whisrs, AnaSeahawk-website};
IsPrivate {signal-mentci-client, meta-signal-mentci-client};
BuildTimeConsumed {tree-sitter-nota, tree-sitter-schema};
DataRepo {goldragon, criomos-horizon-config}.

## Classification decisions grounded in the proposal

- `arca`, `forge` — Active (committed 2026-06-30; §1b "do NOT deprecate").
- `tree-sitter-nota`/`-schema` — Active + BuildTimeConsumed (§1b build-time caveat;
  never retire on dependency-absence).
- `kameo`, `whisrs` — Active forks (§1d; fork is a fact, not a status).
- `kibord` — Content (§1b reclassify from code-orphan to content).
- `criomos-horizon-config`, `goldragon` — Content + DataRepo (§1c config/data).
- Family taxonomy uses the layer rule for signal-*/meta-signal- (the proposal
  leads its family list with Signal | MetaSignal) and subsystem/cluster families
  otherwise; the proposal's family list ends with "..." authorizing this.

## Checks run (exact)

- Membership cross-check: expected 116 set vs `ls /git/github.com/LiGoldragon`
  (113 dirs). Result: zero unexpected extras in /git; the only three in the 116
  set absent from /git are exactly AnaSeahawk-website, persona-pi, WebPublish —
  the retiring repos whose clones the concurrent retirement worker already
  deleted. Set validated.
- Doc-file presence scan (metadata only; ARCHITECTURE/README/AGENTS/CLAUDE) over
  the 113 present repos to ground each `doctrine-home`; the three retiring repos
  sourced from the scout files instead.
- Record/status tallies: `(Repo ...)` records = 116; Active = 102; Content = 11;
  Deprecated records = 3. Paren balance 256/256, bracket balance 121/121.
- Real NOTA parse: throwaway `nota::Document::parse` example against the file →
  `PARSE OK: 1 root object(s)` (the top-level vector of 116 records). Temp example
  removed; `nota-next` working copy left with no changes.

## Boundaries respected

- Did not live-read the three retiring repos (already deleted locally anyway).
- Did not touch the `repos/` symlink surface (separate deprecation worker owns it).
- Preserved unrelated peer changes in the shared primary working copy (additive
  agent-output files, the proposal, `lojix-run-deletion-migration-map.md`).

## Follow-ups / unblocks

- This manifest is the standup that the `repos/` deprecation worker is blocked on:
  once committed and pushed, `repos/` is no longer the coverage iteration surface.
- Not in scope here (carried from the proposal): the coverage-gap INTENT->
  ARCHITECTURE folds, authoring ARCHITECTURE for CriomOS-test-cluster /
  signal-standard (both `doctrine-home None` in the manifest, marking the gap),
  and resolving the dangling `persona-spirit` flake input in CriomOS-test-cluster.
