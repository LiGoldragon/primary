# Spirit Archive Rehoming — Phase 2 Append Handoff (sema, introspect, upgrade, horizon-rs, sema-engine)

Integration handoff for the Phase 2 append batch covering five sub-repos. Each
repo was processed independently with its own commit and fast-forward push.

## Task and scope

Integrate the archived Spirit intent records routed to five sub-repo
`ARCHITECTURE.md` files, then commit and push each through that repo's own
`jj`. Records were synthesized into existing sections (no raw dump), deduped
against existing content, and `[SECRET]`-flagged records redacted to non-secret
substance only. None of the 50 records in this batch carried a `[SECRET]` flag
(the three flagged ids `go41`, `wn7q`, `2qhw` route to other repos), so no
redaction was required.

Routing input: `agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`.
Record descriptions: `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`.

## Pre-flight gate (verified per repo before commit)

All five repos passed the gate: default `jj` workspace `@` empty and sitting
directly on `main`; local `main` equal to `main@origin` (not behind, not
divergent). Fast-forward push only; no force, no rebase needed. Sibling
worktrees on `upgrade` (2), `horizon-rs` (2), and `sema-engine` (6) are
separate clean workspaces and were not touched — work landed on each
default-workspace `main`.

## Result per repo

All five repos: COMPLETED, integrated, committed, fast-forward pushed.

### sema  (`/git/github.com/LiGoldragon/sema/ARCHITECTURE.md`)

- Records integrated (12): `ycwf`, `twlp`, `qkrg`, `py4h`, `wrjl`, `gvgu`,
  `29pb`, `i4ak`, `iir4`, `0yx5`, `rj9y`, `x0ja`.
- Dropped as already-captured (1): `edqu` (subsumed by the sharper `wrjl`).
- Sections touched: opening scope note; Deletion durability; Versioning (new
  "Content-addressed migration" subsection); new "Version control — the
  reusable system" section.
- Verification: `nix run .#test-doc` passed (4 doctests, 0 failed).
- Commit: change-id `rvxtzsst`, git `1515af44`. Push: fast-forward success
  (`main` `14d78deb -> 1515af44`).

### introspect  (`/git/github.com/LiGoldragon/introspect/ARCHITECTURE.md`)

- Records integrated (9): `4frx`, `js6b`, `bwid`, `cd76`, `m5jl`, `q13r`,
  `rpog`, `so0p`, `tdfp`, `tpvu` (11 ids; `4frx`+`js6b` merged as one
  trace-client-library point).
- Folded as partial delta only (1): `jaz4` (persist-to-SEMA already covered by
  the existing `component_trace_events` table + listener; only the
  client-sink-alongside-NOTA delta folded in).
- Sections touched: §0 Intent, §1 Owned surface, §5 Status.
- Commit: change-id `wvrntnqm`, git `7b53b37e`. Push: fast-forward success
  (`main` `28769fd2 -> 7b53b37e`).

### upgrade  (`/git/github.com/LiGoldragon/upgrade/ARCHITECTURE.md`)

- Records integrated (11): `tmji`, `c9fv`, `5cyn`, `c6j4`, `7tqc`, `rq3p`,
  `9pil`, `i1jw`, `lilh`, `88eq`, `thi1`.
- Dropped as already-captured (0): each carried distinct delta; the existing
  schema-self-cutover paragraph was not restated.
- Sections touched: Role; new "Migration as a Deployment Prerequisite";
  new "Schema-Diff-Driven Upgrade Codegen"; Invariants (provenance);
  new "Upgrade-Testing Pipeline", "Version-Divergence Recovery",
  "Upgrade Substrate".
- Commit: change-id `lyvopxrl`, git `5098cbae`. Push: fast-forward success
  (`main` `7cd35fd0 -> 5098cbae`).

### horizon-rs  (`/git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md`)

- Records integrated (7): `a2t4`, `q4gd`, `qkvx`, `1924`, `iwbt`, `tdvr`,
  `rxcp`.
- Dropped as already-captured (2): `242o` (duplicate of cluster-authored
  node-I/O policy); `y1v5` (horizon facet already captured; best-VM-tech
  substance is CriomOS-owned, not horizon-rs).
- Sections touched: new "Minimal on two axes"; new "Typed all the way
  through"; "What goes in a ClusterProposal" (table + prose); "VM hosting is
  cluster-data-generated"; new "RAW and PRETTY split (horizon-next)".
- Default-workspace siblings (`horizon-leaner-shape`,
  `horizon-re-engineering`) untouched.
- Commit: change-id `vvplrtnx`, git `425168ad`. Push: fast-forward success
  (`main` `624b3a5c -> 425168ad`).

### sema-engine  (`/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md`)

- Records integrated (6): `fosp`, `2uhh`, `en7k`, `7l7l`, `duis`, `y3ag`
  (4 genuine new deltas + 2 reinforcements of already-present material:
  `fosp` exclusive-DB-boundary core and `y3ag` sink-delivery were already
  present and were extended, not restated).
- Dropped fully as already-captured (0).
- Sections touched: Direction; Constraints; new "Sema short header —
  symmetric with the wire side" section after Boundary.
- Sibling worktrees (6) untouched; landed on default-workspace `main`.
- Commit: change-id `npswsyuv`, git `59480257`. Push: fast-forward success
  (`main` `18bc3905 -> 59480257`).

## Checks run

- Pre-flight `jj` gate (workspace position, `main` vs `main@origin`) per repo:
  pass for all five.
- Markdown well-formedness per repo (no `---` rules, clean headings): pass.
- `sema` only: `nix run .#test-doc` (doctests) passed; the other four were
  doc-only edits with no repo-local doc-check surface invoked.
- Fast-forward push per repo: success for all five; no non-fast-forward
  rejections, no force pushes.

## Edit coordination

Five `ARCHITECTURE.md` paths claimed under the `repo-scaffolder` lane before
editing, released after all pushes landed. No overlap with any other active
role's claims at dispatch time.

## Skips, blockers, follow-up

- No repo was skipped: every repo was clean, on `main`, and FF-push-safe.
- `[SECRET]` redactions: none in this batch.
- Records intentionally not integrated and why: `edqu` (sema, subsumed by
  `wrjl`); `242o` and `y1v5` (horizon-rs, duplicate / CriomOS-owned). These
  are dedup/ownership decisions, not deferrals — their substance is either
  already captured here or belongs to a different owning repo.
- No downstream TODOs were introduced; all integrated text reflects existing
  accepted direction folded into the owning ARCHITECTURE surfaces.
