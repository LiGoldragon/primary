# Handover — Whole-Engine Testing Readiness: the `-next` Rename Migration (2026-07-03)

Focus-scoped freshness aid. Overall lane: bring the whole persona/criome engine
to continual assembly testing and operation, VM-cluster testing on
`prometheus`. Immediate active thread, and the sole remaining blocker on the
whole-engine gate / `w46v`: the engine-wide `-next` crate-rename migration
(bead `ekvt`). Resume there first.

## Settled psyche direction

- Continually test the whole persona/criome engine and enter operation;
  VM-cluster testing on `prometheus` (sole permanent builder).
- Universal tools carry zero project data; mechanical cross-repo propagation
  belongs in a tool, not hand-repeated.
- Drop `-next` from all `*-next` crates everywhere: rename the repos too, drop
  from dep keys and `use` paths, no alias shims (grounded in recorded intent
  `10pz`: replace, don't keep a compat shape).
- Cluster data is accessed only through horizon/lojix (exposed as a
  system-generated derivation, e.g. `/etc/horizon.json`), never read directly
  by any other tool — a psyche correction; document it in skills/docs.
- A tool's criome-instance config lives with the graph it describes
  (synchronizer config → `persona` once the datom coupling is removed).
- Psyche flagged: does not want sprawling `jj` worktrees/workspaces.

## Confirmed / completed

- Synchronizer: universal, independently audited PASS, PUBLIC
  (`github.com/LiGoldragon/synchronizer`), tool bug fixed (main `8eec5a46`),
  proven on live runs. Full law + schema at its `ARCHITECTURE.md`.
- `w46v`: wire skew RESOLVED at signal-frame 0.3.0 (router-daemon builds +
  passes wire checks; the `Caller.identity` concern is gone). persona inputs
  normalized `git+ssh`→`github:` (persona main `ac629103`). Remaining blocker =
  the `-next` migration (bead `ekvt`); `w46v` depends on `ekvt`.
- `oeng` retired + references scrubbed.
- Orchestrate: was down, restored (running pid at rev `8f9b4170`);
  `systemd --user` supervisor unit landed (CriomOS-home `faf8c230`); live
  cutover deferred (kill the running daemon first).
- `dw95`: decision (e) resolved as COMPLETE-not-retire (it is the shared
  VM-host substrate the mirror front builds on); guest network fix verified +
  guests made loginable (sshd), landed CriomOS main `17caaf88`; live prometheus
  redeploy deferred (vehicle `1e6b.2`; must re-stage a BootOnce from
  `17caaf88`, NOT the sshd-less staged gen-50).
- a/c/d resolved: (a) nixos-test builder capability landed (CriomOS
  `f8eb6ff7`), ouranos Switch deferred; (c) runtime demo debris cleaned; (d)
  `nix copy` inner loop verified + sanctioned.
- Cheap-fixes: doctrine ones → skills; #6/#8/#12 done; component-repo ones
  remain low-priority.
- 13G Jul-1 demo debris cleaned (9 workspaces forgotten, dir removed).
- Beads filed this arc: `ekvt` (P1, the `-next` migration), `wgae`, `oftl`,
  `nlks`.

## The in-flight `-next` migration — active thread

- Tool: `LiGoldragon/rename-propagator` (main ~`d4ef1e69`) — sibling to the
  synchronizer, boundary-anchored token substitution, discovers the rename map
  from each producer's `[package]` name+repository (zero project data),
  independently audited GO. It does file EDITS only — commit/push/lock-regen/
  verify are hand-driven, not in the tool.
- Scope: 3 families `nota-next`→`nota`, `schema-next`→`schema`,
  `schema-rust-next`→`schema-rust`. ~89 repos; run config 86 (3 authorized
  exclusions). Plan artifacts under `agent-outputs/RenamePropagator/`:
  `DryRunPlan.nota`, `DryRunReview.md`, `criome-sweep.nota`,
  `StageAndVerify-Evidence.md`. ~2376 edits, 4 flagged pins (all in `mind`),
  219 residue hits.
- Done: the 3 GitHub repo renames (redirects active). Producers staged to
  `drop-next` branches: `nota` (main already clean), `schema` drop-next
  `ef499e25` verify GREEN, `schema-rust` drop-next `4732e4a3` verify FAILED.
  Nothing landed to any `main`. Exclusions: `CriomOS-test-cluster` (dirty
  unrelated WIP → bead `nlks`), and the 2 non-canonical `CriomOS-home` jj
  worktrees.
- Structural blocker: the tool keeps `branch=main` on rewritten deps, so
  staged consumers reference producer MAINs, which aren't rewritten this pass —
  a multi-level consumer's isolated verify fetches the old `-next` source and
  fails in the no-network build sandbox. `schema-rust` failed because
  `schema`'s main still declares `nota-next`. Every multi-level consumer would
  fail the same way. This is the coordinated-multi-repo problem the
  synchronizer's harness solves; rename-propagator lacks it.
- Open decision (resume here): how to land the coordinated set.
  - A — bottom-up progressive verify-and-land: verify each producer, land it
    to main so the next level sees it, then consumers per graph; no tool
    change; producers-before-consumers.
  - B — extend rename-propagator into a full harness that cross-references
    producers' `drop-next` branches during verify so the whole set verifies
    before any land; cleaner/durable, but more tool-building and touches the
    synchronizer.
  - Orchestrator recommendation on record: A now, B as a follow-up bead.
    Psyche has NOT chosen yet.
- Secondary items the executor resolves under either option:
  - `spirit`'s `NOTA_NEXT_REF` var appears in 2 scripts + `nix_integration.rs`
    + README — rename the live var everywhere but keep any `-next` string
    LITERAL where it's a boundary-migration guard.
  - Generated-file count is 39 on disk vs. the review's 28 — regenerate all
    stale-header files except the 2 in excluded `rename-propagator`.
  - `synchronizer`'s own single stale `nota-next.git` dep (Cargo.toml:21):
    update on synchronizer main as a normal fix (synchronizer is excluded from
    the sweep because its tests use the names as data).
  - Landing conditions from the audit: act on the 4 `mind` flagged pins
    (advance to post-rename revs, verify `mind` builds); regenerate generated
    schema files with a drift check; LEAVE `dependency_boundary.rs` guard
    literals; exclude `synchronizer`/`sema-engine`.

## Open / deferred

- The A/B landing decision above (resume here first).
- Deferred live activations (watched window): ouranos System Switch for
  nixos-test; ssh Home Activate (coordinate with the Colemak change; back up
  `~/.ssh/config` first); orchestrate systemd cutover (kill the running daemon
  first).
- `dw95` live prometheus redeploy + reachability verify (vehicle `1e6b.2`;
  re-stage BootOnce from CriomOS `17caaf88`).
- Cluster-data rework (after the `-next` migration reaches horizon-rs): switch
  synchronizer builder-resolution to read the system-projected
  `/etc/horizon.json` (via `/run/current-system/...`, user-readable) through
  horizon-rs types, delete the hand-rolled datom decoder, move synchronizer
  config to `persona`, document the "cluster data only via horizon/lojix"
  doctrine.
- Workspace/bookmark sprawl cleanup in a quiet single-agent window (deferred
  cheap-fix #7 + the 2 `CriomOS-home` worktrees): ~3 stale jj workspaces and
  20+ stale `operator/report-*` bookmarks. (Not created this session; workers
  used disposable staging branches.)
- `nlks`: sweep `CriomOS-test-cluster` for `-next` once its WIP is resolved.
- Noted follow-ups (bead or note): make rename-propagator a full landing
  harness; migrate synchronizer onto the shared `manifest-surface` crate; a
  NOTA codec quirk (strict decoder rejects a slash-bearing content token it
  itself encoded); rename-propagator's line-based pin-detector → structural
  parsing; `oftl` (horizon-rs nixos-test convergence); `wgae` (lojix Home
  Build with no observable execution).

## Pointers

- Beads: `ekvt` (P1; `w46v` depends on it), `w46v`, `dw95`, `nlks`, `wgae`,
  `oftl`, `vcqx` (open, blocked-on-psyche, dropped).
- Field-readiness lane also carries `vp6d` (P1, continuous-testing entry
  point, separate from `ekvt`) — see `reports/field-readiness/02-kink-ledger.md`
  (+ its 2026-07-03 closeout delta) for the READY-WITH-KINKS verdict and kink
  detail.
- Evidence dirs: `agent-outputs/RenamePropagator/`,
  `agent-outputs/W46vGoLive/`, `agent-outputs/SynchronizerUniversality/`,
  `agent-outputs/FieldReadiness/`, `agent-outputs/PersistentSpiritMirror/`.
- `github.com/LiGoldragon/synchronizer/ARCHITECTURE.md`.
- Mains/commits: rename-propagator main ~`d4ef1e69`; synchronizer main
  `8eec5a46` (+ public remote); persona `ac629103`; goldragon `e8b658fa`;
  CriomOS `17caaf88`; CriomOS-home `faf8c230`. Renamed GitHub repos: `nota`
  (was nota-next), `schema` (was schema-next), `schema-rust` (was
  schema-rust-next) — redirects active.
