# Release-train flow audit v1

Session `nextgen-recrystallization`, lane `TrainFlowAudit`. Read-only audit by a
Fable generalist (Opus 4.8). This report is the durable pickup surface for
Codex, who works the synchronizer side and does not receive chat.

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
