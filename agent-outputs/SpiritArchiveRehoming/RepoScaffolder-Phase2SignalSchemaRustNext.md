# Phase 2 Append — signal + schema-rust-next ARCHITECTURE Integration

## Task and scope

Integrate archived Spirit intent records into two sub-repo ARCHITECTURE.md
files, each processed and pushed independently:

- `repos/signal/ARCHITECTURE.md` (22 routed records)
- `repos/schema-rust-next/ARCHITECTURE.md` (16 routed records)

Both repos are `/git/github.com/LiGoldragon/<name>`, each with its own
git + jj. Integration is thematic synthesis into existing sections, not a
raw dump. Dedupe against existing content; drop what is already captured.

## Inputs consulted

- Routing manifest: `/home/li/primary/agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`
- Record dump: `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`
- Both target ARCHITECTURE.md files (read in full before editing).

## Secret handling

No `[SECRET]`-flagged record routes to either repo in scope. The three
secret ids in the archive (`go41`, `wn7q`, `2qhw`) route to CriomOS-home,
CriomOS, and lojix-cli respectively — none in this task. **Zero
redactions applied.**

## Pre-flight gate (both repos)

- `@` empty, on top of `main`; working copy clean.
- `jj git fetch`: nothing changed.
- `main@origin & ~::main` empty → main NOT behind origin.
- Both safely basable on main; neither claimed by another role.
- Push was fast-forward (move-forward of the `main` bookmark). Neither
  repo skipped.

## signal — 22 records integrated

New section added before `## Status`: **"Target Signal direction"**,
synthesizing the forward-direction records consistent with the existing
doc's framing of this crate as the legacy sema/criome envelope that will
cut over to `signal-frame`.

Sub-sections and their source records:

- Signal is binary only — `5fdr` (NOTA-free contracts), reinforced by the
  consumer-side NOTA-derive split.
- Signal is message triage — `u7fj`, `sjcy`, `isia` (triage-only engine,
  thin CLI clients, CLI as complete typed text edge).
- Origin route / Communicate — `07pn`, `jl3k`, `3got` (implicit
  return-address metadata, correlation/lifecycle at data-type level,
  Communicate wire trait + mail-queue + database marker).
- Short header — `wv2a`, `44dp`, `2qia`, `cqxg`, `dcqz`, `yzwg`, `x2yz`,
  `sqnx` (64-bit eight-enum prefix, root/sub layout, per-component
  root-verb namespace, golden-ratio owner/public split, sub-enum bit
  packing, tap-anywhere extension tiers, universal U8/U16 primitives,
  version-at-database-not-header, signal-X versioned libraries, SignalCore
  namespace retained).
- Schema as protocol substrate — `r2jx`, `pdbn`, `u7tj`, `zrrv`, `lvy9`
  (signal-frame.schema declarative substrate, root object carries frame
  behavior, schema-files-with-contract layout, multi-surface daemon root
  enumerator, real-time streaming as a Signal capability).
- Authorization at the wire — `q33b`, `d5v6` (Permission variant vs
  current two-socket approach, universal Magnitude type).

Section touched: new `## Target Signal direction` inserted before
`## Status`. No existing prose contradicted; the "Wire format" /
"Cross-cutting context" pointers to `signal-frame` already framed the
target, so the new section deepens that without duplication.

Commit: `262b9357` (change `ukollulonzlt`).
Push: fast-forward; `main` and `main@origin` both at `262b9357`. **Pushed.**

## schema-rust-next — 16 records integrated

The existing ARCHITECTURE.md is already very detailed and covers most
records. Four records carried genuinely new substance (added); twelve were
confirmed already captured (deduped/dropped).

Added substantive content:

- `5zgi` — same-shape sibling-variant consolidation by semantic family
  (new bullet in Constraints).
- `3nla` — no emitted `Interact` / `InteractionActor` trait surface; a
  method call on an actor IS the interaction; two-languages distinction +
  effect-table dispatch + actor fan-out as method returns survive (new
  bullet in Constraints).
- `6th4` — hybrid help-catalog model: schema-owned rkyv catalog,
  type-attached accessors for daemon-free local resolution, schema-daemon
  registry indexed by identity + content hash, one structural level per
  request (refined the existing Help constraint).
- `bybe` — single-element-brace newtype, NOTA-transparent emission,
  `Topic@String` / `Topic@{ String }` authoring surface (refined the
  existing `TypeDeclaration` bullet).

Already captured, deduped/dropped (no edit needed):

- `4d8f` — auto/central regeneration on schema change (GenerationDriver +
  update env var).
- `4np2`, `77i8` — token-based lowering, each noun renders itself, single
  driver emits Rust+NOTA+rkyv (string-to-token migration documented
  complete).
- `bkcd` — rkyv universal base, NOTA opt-in per consumer (`NotaSurface`,
  binary-only daemons).
- `czw0`, `zjmc` — triad engine mechanism, runner, kameo actors, lifecycle
  hooks (daemon_emit, NexusRunnerAdapter, on_start/on_stop already there).
- `gb3d`, `l8ox`, `lk22`, `ntsg` — public/local visibility boundary,
  fully-qualified identifiers, one module per .schema file, lib.schema
  entry / per-crate schema folder (all explicitly present).
- `sarw` — alias-vs-newtype emission rules (present verbatim in
  TypeDeclaration constraints).
- `m91k` — its signal-side substance (Tier-1 header, golden-ratio
  two-namespace shape) belongs to and was integrated into the signal doc;
  its VersionProjection/upgrade substance is already in the schema-rust-next
  UpgradeFrom/AcceptPrevious constraints.

Sections touched: `## Constraints` (two new bullets + two refinements
to existing bullets).

Commit: `d0d2472c` (change `zmuyvvns`).
Push: fast-forward; `main` and `main@origin` both at `d0d2472c`. **Pushed.**

## Checks run

- Pre-flight divergence/cleanliness check per repo (passed).
- jj commit + bookmark move + fast-forward push per repo (succeeded;
  origin verified matching for both).
- Edit-coordination: claimed both ARCHITECTURE.md paths under the
  `repo-scaffolder` lane before editing; released after push.
- No content-build/test check run: these are documentation-only
  ARCHITECTURE.md edits with no parser, codegen, or flake surface touched.

## Blockers, unknowns, follow-up

- None. Both repos integrated, committed, and pushed independently.
- No records skipped; no repo skipped.
