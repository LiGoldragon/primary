# Release-train flow audit v1 + delta audit + dogfood run 2026-07-15

Session `nextgen-recrystallization`. This report is the durable pickup surface
for Codex, who works the synchronizer side and does not receive chat. It now
carries three passes: the original **v1** audit (lane `TrainFlowAudit`, read the
sections below), a dated **Delta audit — 2026-07-15 ~20:15 UTC** (lane
`TrainDeltaAudit`) re-verifying v1's defects against the code merged to
`synchronizer` main, and a **Dogfood run — 2026-07-15 (first non-synthetic
closure)** (lane `TrainDogfood`) recording the first real end-to-end run of the
train library against the live six-crate stack — which found a new **defect 10**
and refined the evidence for defects 2, 5, 6, 7. Read the sections in that order;
the dogfood section is the freshest and most concrete. All three are read-only /
harness-only work by a Fable generalist (Opus 4.8).

**Mid-flight caveat:** the audited surfaces were mid-flight on 2026-07-15 while
Codex was actively working them. Line citations below reflect the on-disk state
I read that day and may have drifted since. Re-anchor by symbol name if a line
number no longer matches.

## Mid-flight notice (observation)

I read the freshest on-disk working state in
`/home/li/primary/worktrees/LanguageFamilyNextgen/synchronizer/` (module files
last modified 2026-07-15 15:39). The train code is pushed to
`origin/release-train-p0-p2 @ dfae1fda` ("synchronizer: emit portable release
train artifacts"), 6 commits ahead of the stale `repos/synchronizer` checkout
(still at `ae75e8a2`). Observation date 2026-07-15.

Two parallel synchronizer working directories are nested under primary
(`repos/synchronizer-release-train-p0-p2/` and
`worktrees/LanguageFamilyNextgen/synchronizer/`) such that a bare `git` command
resolves up to the primary repo. I judged the code from file contents, not git
state. I ran no builds, edits, or git mutations against the synchronizer
surfaces, to avoid contending with Codex's active `target/` and branches.

Audited surfaces:

- Deployed skill `/home/li/primary/.claude/skills/release-train-development/SKILL.md`
- Skill source `/git/github.com/LiGoldragon/skills/modules/release-train-development/full.md`
- Design `/home/li/primary/reports/synchronizer/release-train-epic-architecture-v1.md`
- Implementation `worktrees/LanguageFamilyNextgen/synchronizer/src/release_train.rs`
  (+ `src/main.rs`, `src/driver.rs`, `src/configuration.rs`, `src/git_repository.rs`,
  `tests/release_train.rs`, `tests/release_train_run.rs`,
  `release-trains/language-family-poc.nota`, `release-trains/README.md`)

## A. Doctrine fit — PASS

- The skill source (`full.md`) is terse, full-English, no `---` rules, five short
  sections. It matches workspace skill conventions.
- The deployed `SKILL.md` is a generated bundle: it inlines the four declared
  dependency modules (`manifests/module-dependencies.nota:70` →
  `[feature-development version-control nix-discipline testing]`) as preamble
  sections, then appends the release-train section as
  `## release train development` (line 203+). Diffing the deployed section against
  source shows byte-identical text except headings demoted `##`→`###` by the
  bundler. No content drift.
- The bundling (and the `# feature development` H1 at line 6) is the standard
  generator behavior — `feature-development/SKILL.md` opens the same way. The
  apparent "duplicated ambient protocol" is not this skill's defect; it is how
  every multi-dependency skill deploys.
- No contradiction with edit-coordination, version-control, testing, or
  nix-usage; the release-train section defers to them rather than restating
  conflicting rules.

## B. Design fidelity — MOSTLY FAITHFUL, with real gaps

Faithful to the glance-approved boundaries:

- **Never-writes-main.** `ReleaseTrainName::candidate_branch()` = `train/<name>`
  (release_train.rs:34); `materialize_candidate` only ever pushes that branch via
  `push_train_branch` (release_train.rs:676-694). Strong.
- **Resolved-commit-only build identity.** `ResolvedReleaseTrain` carries only
  commits + narHash attestations; JSON/flake projections emit
  `github:owner/comp/<commit>` + `narHash`, and tests assert no `path:` / `/tmp`
  (release_train.rs:465-505; tests 148-168). Strong.
- **Locks-per-component, never merged.** `ComponentLockIdentity` holds separate
  `cargo_lock_blake3` / `flake_lock_blake3` (release_train.rs:233-256). Faithful
  as a type.
- **Fail-loud validators.** membership / undeclared-edge / missing-member /
  unadmitted-external / expected-base / exact-selector / attestation-mismatch are
  all typed `ReleaseTrainError` variants with unit tests (release_train.rs:360-441;
  tests 179-264). Faithful.
- **Domain-separated closure identity.** BLAKE3 over
  `b"LiGoldragon.release-train.resolved.v1\0"` + canonical payload
  (release_train.rs:507-514). Matches the design's identity-class table.
- **Separate `release-trains/<name>.nota`.** Present at
  `release-trains/language-family-poc.nota` with a README, kept out of operational
  `synchronizer.nota`. Faithful.

Silent weakenings (design-fidelity defects):

1. **Expected-base is silently relaxed and laundered in the live path.** The
   design's `ExpectedBase` means "the exact commit on which a selected branch must
   be based… a branch that has silently rebased elsewhere is not equivalent." The
   library validator `validate_selectors` enforces `observed_base == expected_base`
   (release_train.rs:401). But the live `execute()` constructs each
   `ResolvedSelector` with `observed_base = component.expected_base()`
   (release_train.rs:610) — it copies expected into observed rather than recording
   the truly observed base — while `resolve_selector` only checks
   `base_is_ancestor(expected, selected)` (release_train.rs:663). Net effect: in
   any live run the equality validator is a tautology, and drift is guarded only by
   the weaker ancestor test. The two validation layers do not compose.
2. **The integration flake does not orchestrate component checks.** Design
   (report lines 198-200) requires the generated flake to "invoke each component's
   own flake/package/check interface at the matching candidate commit… report
   component check output and closure identity together." The generated flake's
   `outputs` is only `releaseTrain = builtins.fromJSON (readFile
   ./release-train.lock.json)` (release_train.rs:482) — correct portable inputs,
   but zero check orchestration and no `follows`. It is an input skeleton, not the
   test surface the design specifies.

## C. Factual accuracy — the skill/README document capabilities the CLI does not deliver end-to-end

The library pieces exist and are real (git methods `remote_branch_tip` /
`base_is_ancestor` / `push_train_branch` / `commit_file_edits` have real
`GitComponentRepository` impls at git_repository.rs:181-358, no `todo!` /
`unimplemented!`). But the wiring is incomplete:

- **The one documented CLI entry point emits no closure.** `synchronizer
  release-train <config> <intent>` (README + main.rs:32) runs
  `ReleaseTrainRun::execute()` then `render_report` (main.rs:90-97). It never
  calls `resolve_closure`, never runs discovery-based membership validation, never
  computes attestations, never emits `release-train.lock.json` or the integration
  flake. Those live only in library/test code (`resolve_closure`,
  `write_integration_artifacts`), reachable from Rust callers/tests, not from the
  command the skill and README tell a user to run.
- **Discovery is not wired to the drift validators.** `execute()` never calls
  `DependencyGraph::discover` (no `discover` / `DependencyGraph` reference in
  release_train.rs). The `discovered_internal_components` /
  `discovered_external_components` sets that drive `validate_membership` are only
  ever hand-fed — by unit tests, and by the live-run test which builds `members`
  from its own selectors so the check passes trivially
  (tests/release_train_run.rs:146-152). So "discovery validates intent; fail on
  undeclared dependencies" (glance-approved recommendation #3) is implemented as a
  validator but is not reachable from any real run.
- **README overstates current behavior.** It says the command "resolves it… emits
  an immutable closure before testing" and lists `release-train.lock.json →
  fixed-input integration flake` as outputs of that command
  (release-trains/README.md:4-6, 23-28). The command does none of that today.

The skill text itself is written at doctrine level ("Emit an immutable typed
closure… Generate canonical release-train.lock.json") and is defensible as *what
to do*, but it reads as *current capability* and is not qualified as
library-only / not-yet-CLI-wired.

## P0–P2 implementation status

| Stage | Design intent | Status | Evidence |
| --- | --- | --- | --- |
| **P0** contract + resolution + drift fixtures + closure hash + canonical JSON | Freeze typed contract, resolve-only, prove drift failures | **Implemented & unit-tested** | `ReleaseTrainIntent` / `ResolvedReleaseTrain`, domain-separated identity, all drift `ReleaseTrainError` variants; tests/release_train.rs:127-264 |
| **P1** `ReleaseTrainRun`, candidate materialization, per-component Cargo/flake edits | Isolated `train/<name>` commits + valid locks | **Partial.** Real git-boundary methods; run resolves selectors, checks ancestor base, pushes empty `train/<name>` bootstrap commits, then reuses cascade. Proven only against synthetic `FixtureRepository`, never a real remote. Discovery→membership validation and real attestation/lock capture are not wired into the run — closure emission is a manual caller step. Candidate commit is empty (`commit_file_edits(selected, &[], …)`, release_train.rs:687); locks come from the downstream cascade, not captured into `ComponentLockIdentity`. | release_train.rs:596-713; tests/release_train_run.rs:53-161 |
| **P2** canonical `release-train.lock.json` + integration flake + portable Nix checks | First deterministic all-component Nix test surface | **Partial.** JSON + flake generation exist, portable inputs asserted by string-match. No check orchestration in the flake, and no test builds it with Nix (no train flake check derivation; tests only string-match). "Remote-builder invocation / integration Nix builds consume only pushed refs" is unproven at the Nix level. | release_train.rs:460-505; no `nix` / flake-check coverage in tests/ for the train |
| P3–P5 | source-index / TextualJson / Spirit | **Not started** (correctly deferred). `VendorSnapshotReference` is a data-only placeholder (release_train.rs:260-271). | — |

## D. Usability for slice two — a fresh lane cannot complete the loop from the skill as written

Following the skill + README literally, a slice-two lane would:

- Author `release-trains/<name>.nota` — works (fixture format proven decodable,
  tests/release_train.rs:127-136; live seed present).
- Run `synchronizer release-train …` — gets candidate `train/<name>` branches + a
  cascade report, then stops. No closure, no `release-train.lock.json`, no
  integration flake, no drift-on-discovery check, no Nix evidence.
- To actually get the portable closure + Nix artifacts, the lane must write Rust
  that calls `MaterializedReleaseTrain::resolve_closure(...)` and
  `write_integration_artifacts(...)`, hand-supplying discovered topology,
  attestations, and lock identities — none of which the skill mentions.

Missing for a self-serve slice-two ride: (a) a CLI path that emits the closure +
JSON + flake; (b) discovery wired to membership validation; (c) real narHash/lock
capture into the closure; (d) an integration flake that runs component checks;
(e) a Nix check that actually builds the generated flake as evidence; (f) worked
command examples and a non-synthetic fixture.

## E. Gaps / defects (hand-off ready)

1. **[High] CLI emits no closure or Nix projection.** `synchronizer release-train`
   stops at candidate branches + report (main.rs:90-97). *Fix:* extend the CLI (or
   a `resolve` / `materialize` / `project` subcommand set matching the design's
   operation list, report lines 296-305) to run resolve → discover → validate →
   emit `ResolvedReleaseTrain`, `release-train.lock.json`, and the integration
   flake, and print the closure identity.
2. **[High] Discovery not wired to drift validators.** `execute()` never calls
   `DependencyGraph::discover`; `validate_membership` is fed only by tests
   (release_train.rs:333-388). *Fix:* in the run, discover the graph at resolved
   commits and pass real internal/external sets into `resolve_closure`; add a
   live-run test that a genuinely undeclared discovered edge fails.
3. **[High] No Nix-level proof of P2.** Portability is asserted by Rust
   string-match only; nothing builds the generated flake (no train flake check).
   *Fix:* add a flake check derivation (or named stateful check) that consumes a
   fixture `release-train.lock.json` and builds/evaluates the generated
   integration flake; this is the design's required P2 acceptance evidence
   (report lines 345-356).
4. **[Medium] Expected-base check laundered in the live path.** `execute()` sets
   `observed_base = expected_base` (release_train.rs:610), making the equality
   validator (release_train.rs:401) a no-op live; only the weaker ancestor check
   runs. *Fix:* record the actually-observed base commit in `ResolvedSelector`,
   reconcile the ancestor-vs-equality semantics into one rule, and test a live
   base-drift rejection.
5. **[Medium] Integration flake does not orchestrate component checks.** `outputs`
   exposes only `releaseTrain = fromJSON(...)` (release_train.rs:482). *Fix:*
   generate per-component check outputs at each candidate commit + closure-identity
   output, per report lines 198-200.
6. **[Medium] README/skill describe library-only behavior as current CLI
   behavior.** README:4-6,23-28 and the skill's "Emit… Generate…" imply the
   command does the full closure. *Fix:* qualify the skill/README to state which
   steps are CLI vs library today, or (better) land #1 so the docs become true.
7. **[Low] Real attestations/locks not captured into the closure by the run.**
   `MaterializedReleaseTrain` requires the caller to supply narHash/lock
   identities; the live path never computes them (nar_hash_source exists but is
   unused for closure emission). *Fix:* capture real prefetch narHash and
   per-component lock content into the closure during materialization.
8. **[Low] Closure identity depends on serde_json formatting stability.**
   Acceptable bootstrap choice (report line 263 sanctions a deterministic JSON
   adapter), but flag for the P4 TextualJson migration so identity semantics are
   preserved.
9. **[Low/Cosmetic, generator-wide] Bundle H1 is `# feature development`.**
   Deployed skills take the first bundled dependency's H1; not this skill's defect,
   but a skill-editor could have the generator title the bundle by the primary
   module. Out of scope for this skill.

## Verdict — NO-GO for slice two riding the train as its integration/build mechanism now

Continue the interim git-pin pattern for slice two.

**Single strongest reason:** the end-to-end path is not closed — the one
documented command produces no resolved closure and no Nix projection,
discovery-driven drift validation is unwired, and no test builds the generated
integration flake with Nix, so there is currently zero portable Nix evidence
that a train closure builds. Riding it now would mean a slice-two lane
hand-writing Rust glue to reach P0/P2 functions the skill never mentions, with
the fail-loud guarantee (recommendation #3) effectively bypassed.

**Constructive middle path (recommended):** slice two should author its
`release-trains/<name>.nota` intent and dogfood P1 (resolve selectors,
materialize `train/<name>`, exercise `resolve_closure`) to generate real fixtures
and pressure-test the validators — while keeping the pinned-git-dep pattern as
the actual green build path until defects 1–3 land (CLI closure emission,
discovery-wired drift validation, and a Nix check that builds the generated
flake). The contract and validators are solid; the train is close, but it is not
yet a usable integration surface.

## Delta audit — 2026-07-15 ~20:15 UTC

Second read-only pass (lane `TrainDeltaAudit`, Fable generalist, Opus 4.8),
prompted by a report that "the train-release machinery is ready now." Verdict is
unchanged: **NO-GO**. Surfaces were idle (last write 16:53) so this is a settled
read, not mid-flight.

### What actually changed since v1

The delta is essentially nil in substance. v1 read
`origin/release-train-p0-p2 @ dfae1fda`; that branch has now been fast-forwarded
onto **`synchronizer` main @ `dfae1fd` "synchronizer: emit portable release
train artifacts"** (committed 2026-07-15 16:11 +0200) **unchanged**. The worktree
at `worktrees/LanguageFamilyNextgen/synchronizer` is byte-identical to committed
main (0-diff on `src/main.rs`, `src/release_train.rs`, `src/driver.rs`; no
added/removed src files).

- The three train commits are `9104058` (immutable closure), `d2be11c` (execute
  scoped trains), `dfae1fd` (portable artifacts). `git log --stat 9104058^..dfae1fd`
  shows the **final commit `dfae1fd` touched only `tests/release_train_run.rs`
  (+41 lines)** — nothing else moved after v1.
- **No `train/*` branches** exist on any synchronizer checkout.
  `land-release-train-integration` is stale (2026-07-07, predates the train work,
  3 behind main) — not the "ready" surface.
- **No generated artifacts** in the tree. The one intent seed is
  `release-trains/language-family-poc.nota` (NOTA pinned at `18e2e8d0…`, Schema
  bases still zero placeholders). No `release-train.lock.json`, no integration
  flake.

The "ready now" report reflects a merge-to-main, not a fix of the gating defects.

### Delta table (defects 1–9, current code on main @ dfae1fd)

| # | Defect (sev) | Status | Current-code citation |
| --- | --- | --- | --- |
| 1 | CLI emits no closure/lock/flake (High) | **UNFIXED** | `main.rs:90-97` `execute_release_train` calls `ReleaseTrainRun::execute()` then `render_report(materialized.report())` and stops. `resolve_closure`/`write_integration_artifacts`/`to_integration_flake`/`to_canonical_json` are called **only from tests** (`tests/release_train.rs:147-162`, `tests/release_train_run.rs:152-156`), never from `src/` outside their defs. |
| 2 | Discovery not wired to drift validators (High) | **UNFIXED** | `execute()` (`release_train.rs:596-640`) never calls `DependencyGraph::discover` (it appears only in `driver.rs:313` cascade + topology/version tests). The sole end-to-end closure test builds `members` from its **own** selectors and passes `BTreeMap::new()` for externals (`release_train_run.rs:146-152`) — membership passes tautologically. Fail-on-undeclared unreachable in a real run. |
| 3 | No Nix-level proof of P2 (High) | **UNFIXED** | `flake.nix:43-54` checks are `build/test/fmt/clippy` (crane Cargo). Nothing builds or evaluates the generated integration flake. The `test` check's flake assertions are **string-match only** (`release_train_run.rs:159-160`, `release_train.rs:153`). Zero portable Nix evidence a closure builds. |
| 4 | Expected-base laundered live (Medium) | **UNFIXED** | `release_train.rs:608-613` still sets `observed_base = component.expected_base().clone()`, so the equality validator (`:401`) is a tautology live; only the weaker `base_is_ancestor` (`:663-664`) runs. Identical to v1's `:610`. |
| 5 | Flake orchestrates no component checks (Medium) | **UNFIXED** | `to_integration_flake` (`:465-487`) `outputs` is only `releaseTrain = builtins.fromJSON (readFile ./release-train.lock.json)` — no per-component checks, no `follows`. Input skeleton, not a test surface. |
| 6 | Docs describe library as CLI (Medium) | **PARTIALLY FIXED** | Top-level `README.md:48-57` now attributes closure/lock.json/flake to "the typed `release_train` module" (not the command) and adds "not yet run against live component repositories." But `release-trains/README.md:4-6` still says the command "resolves it… emits an immutable closure before testing," and deployed `SKILL.md` still reads as unqualified current capability. |
| 7 | Real narHash/locks not captured by the run (Low) | **UNFIXED** | `execute()` returns `MaterializedReleaseTrain` with no attestations/locks; `resolve_closure` requires the caller to supply them. `nar_hash_source` in boundaries is unused for closure capture. Test synthesizes them (`release_train_run.rs:124-145`). |
| 8 | Closure identity ties to serde_json formatting (Low) | **UNFIXED (deferred by design)** | `payload_identity` uses `serde_json::to_vec` (`:508`). Sanctioned bootstrap; flag for P4 TextualJson. |
| 9 | Bundle H1 `# feature development` (Low/cosmetic) | **UNFIXED (generator-wide, out of scope)** | Deployed `SKILL.md:6`. |

### Executed evidence

- Git: canonical `/git/github.com/LiGoldragon/synchronizer` — `main @ dfae1fd`; no
  `train/*` refs; `land-release-train-integration` stale. `git log --stat
  9104058^..dfae1fd` → final commit = tests-only +41. Worktree == main (0-diff).
- `cargo test --test release_train --test release_train_run` against a scratch
  `CARGO_TARGET_DIR` (worktree `target/` untouched): **6/6 pass** —
  `undeclared_internal_component_is_a_loud_train_failure`,
  `external_component_requires_exact_immutable_admission`,
  `moved_expected_base_is_a_loud_selector_failure`,
  `…closure_is_canonical_and_contains_only_immutable_nix_sources`, the
  intent-shape test, and
  `live_train_resolution_materializes_scoped_candidate_branches_from_pushed_truth`.
  No stubs in the train path (`git_repository.rs:181-358` are real impls).
- **The passing tests prove the validators fire only when hand-fed discovered
  sets, and that the library closure chain runs on synthetic fixtures. They do
  not prove any gating defect: no CLI reaches those functions, no run discovers
  topology, and no Nix build touches the generated flake.**

### Renewed verdict — NO-GO for slice three riding the train

Since v1 the machinery advanced by a merge-to-main plus one fixture test with
trivial membership; **all three gating defects (1, 2, 3) are unchanged in the
code.** A slice-three lane following the deployed skill/README would still get
candidate `train/<name>` branches + a cascade report and then have to hand-write
Rust glue to reach `resolve_closure`/`write_integration_artifacts`, supplying
discovered topology and attestations itself, with the fail-loud guarantee
bypassed and no Nix proof the closure builds.

Shortest gate list before GO:

1. **Defect 1** — wire the CLI (or a `resolve`/`project` subcommand) to run
   resolve → discover → validate → emit `ResolvedReleaseTrain` +
   `release-train.lock.json` + integration flake, printing the closure identity.
2. **Defect 2** — call `DependencyGraph::discover` at resolved commits inside the
   run and pass the real internal/external sets into `resolve_closure`; add a
   live-run test where a genuinely undeclared discovered edge fails.
3. **Defect 3** — add a flake check derivation that consumes a fixture
   `release-train.lock.json` and builds/evaluates the generated integration flake.
4. (Should land with 1) **Defect 4** — record the actually-observed base in
   `ResolvedSelector` so the equality validator stops being a live no-op.

### Interim dogfood plan (since NO-GO)

Continue the pinned-git-dep pattern as the green build path for slice three.
Optional dogfood that generates real fixtures without gating the slice: author
`release-trains/<slice-three>.nota` and, in a throwaway Rust harness/test, drive
`ReleaseTrainRun::execute()` → `resolve_closure(...)` → `write_integration_artifacts(...)`
against real pushed commits to pressure-test the validators and produce the first
non-synthetic `release-train.lock.json`. Do **not** invoke `synchronizer
release-train …` expecting a closure — it only pushes `train/<name>` candidate
branches and cascades locks (no dry-run/resolve-only mode exists, so a live
invocation writes branches). Feed the resulting fixtures back as the acceptance
surface for defects 1–3.

### Trip hazards for the next auditor

1. The nested synchronizer working copies under `primary` make a bare `git`
   command resolve up to the primary repo. Read the train tree via the canonical
   ghq clone `/git/github.com/LiGoldragon/synchronizer` plus explicit worktree
   paths, not bare `git` from inside the worktree.
2. That ghq checkout sits **detached at the pre-train `ae75e8a`** while `main` is
   at `dfae1fd`. A naive `grep src/release_train.rs` there finds none of the train
   code because the file is not in that checked-out tree. Grep the worktree at
   `worktrees/LanguageFamilyNextgen/synchronizer` (== main) or `git show main:…`.

## Dogfood run — 2026-07-15 (first non-synthetic closure)

Third pass (lane `TrainDogfood`, Fable generalist, Opus 4.8): the first
**non-synthetic** end-to-end run of the train library, driving it as a pinned
git dependency (`github.com/LiGoldragon/synchronizer@dfae1fda`) against the real
six-crate language-family stack on GitHub. This is a genuine caller's-seat
record of where the documented CLI/skill strands a user versus what the library
actually requires. It surfaced one **new High defect (10)** and hard-confirmed
defects 2, 5, 6, 7 with concrete evidence. The harness is read-only on the
synchronizer repo; it pushes only `train/<name>` candidate branches to the six
member crates, never writes any `main`, never merges.

Full evidence artifacts (public harness repo
`github.com/LiGoldragon/release-train-dogfood`, main `16a248e9`):
`repos/release-train-dogfood/README.md` (defect-mapped friction ledger),
`repos/release-train-dogfood/run-evidence.txt` (stage-by-stage capture),
`repos/release-train-dogfood/integration/` (the generated
`release-train.lock.json` + `flake.nix`), and the authored intent at
`release-trains/language-family-slice-three.nota`.

### Run summary

Train `language-family-slice-three`: six `Mainline` members, zero immutable
externals. `ReleaseTrainRun::execute()` ran against the real remotes and pushed
six `train/language-family-slice-three` candidate branches:

| crate | selected (`main` tip) | candidate (train tip) |
| --- | --- | --- |
| content-identity | `6cc0408c…` | `3f705566f36d171d9fa98167ba2b71f6e9a9f93d` |
| name-table | `c3237f77…` | `1c1d6ff6f5824402dcef3b1005b14465b4e90cdb` |
| raw-discovery | `a4e8c6df…` | `b6cc1c8d80a8b4812ddf29317d3f50e04d5fc838` |
| structural-codec | `104f9245…` | `3a1d56770502ffe7f3745187c118fc79db1a4f9a` |
| core-schema | `33e5be27…` | `361c19fb43d87ec4945b726f64fe7bd932a0fcc6` |
| structural-codec-derive | `348bd89f…` | `e77619494e7dd4c14d570ed002c83a6d88b4b9f0` |

- **Real discovery.** `DependencyGraph::discover` found 6 internal components and
  21 Cargo edges forming a valid DAG with ascent
  `content-identity, raw-discovery → name-table → structural-codec → core-schema
  → structural-codec-derive`.
- **Real attestation.** Six narHashes from `nix flake prefetch` + six per-component
  Cargo/flake lock blake3 identities, hand-captured by the harness.
- **Real closure.** `resolve_closure` returned a typed `ResolvedReleaseTrain`,
  identity `42df158c9708d7f06c980a9431a51c4952d92560d9bfa9ce27de45b9288e6cea`.
- **Real artifacts.** `write_integration_artifacts` emitted
  `integration/release-train.lock.json` + `integration/flake.nix` (zero `path:`),
  committed in the harness repo (`main 16a248e9`).

### Defect 10 (High, NEW) — the generated integration flake does not evaluate under Nix

`ResolvedReleaseTrain::to_integration_flake` (`release_train.rs:471`) emits each
input as `{ url = "github:…/rev"; narHash = "sha256-…"; }`. `narHash` is **not a
valid flake input attribute** (it belongs in `flake.lock`), so Nix rejects the
generated flake outright:

```
error: unexpected flake input attribute 'narHash', at flake.nix:4:5
```

The P2 artifact is therefore not merely untested (v1/delta defect 3) — **it is
not evaluable at all**. The `release-train.lock.json` payload is valid
(`builtins.fromJSON` reads it); the flake wrapper around it is invalid.

*Fix validated in this run (use as the acceptance fixture):* move the narHash
into the input URL as a query parameter —
`url = "github:owner/repo/rev?narHash=sha256-…"`. With that single change,
`nix flake metadata` locks and narHash-verifies all six candidate inputs (plus
their transitive `rust-build`/`fenix`/`nixpkgs` inputs), and
`nix eval path:…#releaseTrain.identity` returns
`42df158c…` — the library's own closure identity. So the six candidate commits
are genuinely portable, fetchable, and narHash-verified by Nix; the only blocker
to a portable P2 artifact is the invalid input-attribute emission.

### Refined evidence for existing defects

- **Defect 2 (discovery↔closure gap) — exact API shape.** `DependencyGraph`
  exposes no accessor for its component set (the `components` field is private;
  only `edges()`, `dependencies_of()`, `ascent_levels()` are public), so the
  `discovered_internal_components` set must be hand-assembled from the manifest
  list the caller passed in. And `discover()` deliberately drops every edge that
  points outside the configured set, so it **never produces the
  `discovered_external_components` commit map** at all. Both membership arguments
  to `resolve_closure` were hand-built in the harness. A fix wants `discover()`
  (or a `DependencyGraph` method) to yield the exact `(internal set, external
  commit map)` `resolve_closure` consumes, and `ReleaseTrainRun::execute` to wire
  it so undeclared-edge / unadmitted-external failures are reachable from a real
  run.
- **Defect 7 (run captures no closure attestations/locks) — confirmed.**
  `execute()`'s `nar_hash_source` serves only flake-lock bumps; it computes
  nothing for the closure. All six narHashes and six lock blake3s in this closure
  were computed by the harness (`DogfoodHarness::attest_selectors`), not by the
  run.
- **Defect 5 (no component-check orchestration) — confirmed even post-fix.** Even
  the *corrected* flake's `outputs` is only `releaseTrain = builtins.fromJSON …`.
  Nix proves the inputs are fetchable and narHash-verified; it does **not** build
  the six components or run their checks at the candidate commits, and there is no
  closure-identity-plus-check co-report. A green eval is not a green build of the
  train.
- **Defect 6 (docs overstate CLI) — confirmed against real outputs.**
  `release-trains/README.md` lists `release-train.lock.json` and the integration
  flake as outputs of the CLI command; running the real chain confirms the
  command produces neither (the whole harness crate exists only because that Rust
  does not ship — stages c–f are all caller glue the CLI should own, per
  defect 1).

### P1 observation worth Codex's attention — empty, non-cross-pinning candidates

With an all-`Mainline` train where every consumer already pins every producer's
current `main` tip, the cascade reported every component `AlreadyAligned`, so
each candidate is a **pure empty *materialize* commit** on the component's
selected `main` tree — each candidate narHash equals the corresponding `main`
narHash, and the candidates **do not cross-pin each other's candidate commits**.
No lock rewrite fires because the resolver targets each producer at its `main`
tip, which the consumers already pin. (Verification was `NotAttempted` by design:
the builder-host resolver pointed at an absent cluster proposal — a
`RoleResolution` failure in the cascade report — so no ssh / `nix build` ran.
Note also that `execute()` entangles the closure path with the full StagedCascade
ssh-build verify in one entry point.) This means an all-`Mainline` dogfood
exercises resolution/discovery/attestation/closure/emission end-to-end but does
**not** produce a train whose candidates differ from their mains; a train that
actually cross-pins needs producer branches ahead of what consumers pin.
