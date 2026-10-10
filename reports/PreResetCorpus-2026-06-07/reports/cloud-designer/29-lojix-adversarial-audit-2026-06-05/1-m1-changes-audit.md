# 29.1 — lojix M1 changes adversarial audit (DIMENSION 1)

cloud-designer sub-agent, 2026-06-05. ADVERSARIAL read of this session's M1
edits to `schema_runtime.rs` + the meta contract. Posture: broken/risky until
proven. Every claim cites `file:line` against the pushed `triad-port` copies.
Known-deferred items (copy/activate addressing A2/A3, M3 materialization,
reply-carries-no-store-path) are assessed for *latent* risk but not re-reported
as flaws.

Canonical files audited:
`/git/github.com/LiGoldragon/lojix/triad-port/src/schema_runtime.rs`,
`/git/github.com/LiGoldragon/lojix/triad-port/src/schema/nexus.rs`,
`/git/github.com/LiGoldragon/meta-signal-lojix/triad-port/schema/lib.schema`,
`/git/github.com/LiGoldragon/lojix/triad-port/tests/build_smoke.rs`.
Legacy parity reference:
`/git/github.com/LiGoldragon/lojix-cli/src/build.rs`,
`/git/github.com/LiGoldragon/lojix-cli/src/activate.rs`,
`/git/github.com/LiGoldragon/lojix-cli/src/deploy.rs`.

## Headline flaw list (tight, for the synthesizer)

| # | Severity | Flaw | Concrete fix |
|---|---|---|---|
| F1 | High (correctness, divergence from legacy) | `nix build` is fed the eval'd **`.drv` path**, not `<flake>#<attr>`. The two-step eval-then-`build <drv>` diverges from the legacy single-step `nix build <flake>#<attr>` and silently DROPS substituters/overrides at build time. | Either build the attribute directly (`nix build <flake>#<attr>`, parity with `build.rs:298-304`), or if keeping the drv path, append `^*` and route substituters; verify `nix build <drv>` realizes (see F1 detail). |
| F2 | High (silent-wrong) | `run_nix_build` IGNORES `command.substituters` entirely — the field is threaded into `NixBuildCommand` (`nexus.rs:90-95`) then never used (`schema_runtime.rs:1122-1140`). A deploy that names extra caches builds from source / fails to fetch. | Emit `--option extra-substituters <urls> --option extra-trusted-public-keys <keys>` from `command.substituters`, mirroring `build.rs:330-339`. |
| F3 | High (silent-wrong, eval path) | On the **`build_attribute` override path the production override-inputs are silently absent AND on the production path they are ALSO absent** — `run_nix_eval` emits `nix eval … <flake>#<attr>.drvPath` with NO `--override-input horizon/system/deployment/secrets` (`schema_runtime.rs:1111-1119`). The contract comment claims override injection happens (`lib.schema:81-84`) but the code never does it. Production deploys eval the wrong (un-materialized) derivation. | Known-deferred as M3 materialization — but the *risk* is that a production (non-fixture) `Deploy` today reaches `Deployed` having eval'd a meaningless/garbage drv with no error. Add an explicit guard: reject a System deploy with `build_attribute: None` until M3 lands, instead of silently eval'ing an un-overridden attribute. |
| F4 | High (state leak on long-lived daemon) | `record_deploy_submitted` sets `self.active_deploy = Some(...)` UNCONDITIONALLY (`schema_runtime.rs:764`) with no in-flight guard. A second `Deploy` arriving mid-pipeline OVERWRITES the live cursor; the first deploy's chain is silently abandoned and the second hijacks it. The daemon is single-threaded per the runner, but the runner's continuation loop for deploy-1 spans multiple `decide` calls, and the socket loop can interleave a deploy-2 frame between them. | Guard: if `self.active_deploy.is_some()`, reject the new Deploy with `DeploymentInFlight` BEFORE the sema write, rather than clobbering. |
| F5 | Medium (correctness, copy target) | `run_copy_closure` / `run_activate_generation` ssh to the **bare `node_name`** (`schema_runtime.rs:1143,1158,1261-1283`). Legacy addresses the node's `criome_domain_name`, never the bare name (`deploy.rs:106` `SshTarget::from_node`). KNOWN-deferred as A3 — assessed: the early-termination (F-note below) means Build-only never reaches this, so it is currently unreachable, BUT any activating action (Switch/Boot/Test) submitted today silently ssh-es to a wrong/unroutable host. | Already tracked A3; add a guard rejecting activating actions until A3 lands, so they cannot be submitted into a wrong-address path. |
| F6 | High (literal `$CLOSURE`, activate is a no-op-or-wrong) | `activate_system` ships the LITERAL shell string `nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"` (`schema_runtime.rs:1280`). `$CLOSURE` is **never exported** — no env var is set on the ssh invocation, and the freshly-built `closure_path` is NOT interpolated. The activate either fails (unbound var under `set -u`) or sets the profile to an empty/garbage path. Also it omits the legacy `&& switch-to-configuration <action>` step entirely (`activate.rs:58-65`). | Interpolate the real store path into the command, and run `switch-to-configuration <action_word>` keyed off `activation_kind` (parity with `activate.rs:39-69`). KNOWN-deferred A2, but flag: the current literal is actively wrong, not merely incomplete. |
| F7 | Medium (smoke tests prove less than claimed) | The eval/build smokes assert ONLY that the engine reached `meta::Output::Deployed` (`build_smoke.rs:57,71`). They assert NOTHING about the realised path — the reply carries no store path (`AcceptedDeploy` has only id+marker, `lib.schema:114`), and the tests never inspect `nix`'s output. A silently-wrong eval (e.g. eval succeeds but yields the wrong drv, or `first_line` grabs a warning line) still reaches `Deployed` and the test passes GREEN. | The reply must carry the realised drv/store path (extend `AcceptedDeploy` or add a deploy-result field), and the smoke must assert it `starts_with("/nix/store/")` and ends `.drv` (eval) / not `.drv` (build). |
| F8 | Medium (silent-wrong, `first_line` fragility) | Eval/build/metadata parsing takes `first_line` of stdout (`schema_runtime.rs:1310-1312`). `nix flake metadata --json` emits a JSON object across MANY lines — `first_line` grabs `{` as the "revision" (`resolve_flake_auth:1102-1106`). The revision is inert today (never used downstream), so it is silent-wrong-but-harmless NOW; it becomes a real bug the moment revision is consumed. | Parse the JSON for `.revision` (or drop the field until used). At minimum note it is structurally wrong, not a valid first-line parse. |
| F9 | Low/Medium (inert-field silent-wrong risk) | On the `build_attribute` path, `source` (`ProposalSource`) and `deployment_kind` are carried into the pipeline (`schema_runtime.rs:159,163; nix_eval_command:231-239`) but `deployment_kind` is passed to `NixEvalCommand` and NEVER read in `run_nix_eval` (`1111-1119`); `source` is used only by `resolve_flake_auth` which on the fixture path resolves `/dev/null` and the result is inert. So a deploy with a real `source`/`deployment_kind` that DISAGREES with the baked-in fixture is accepted with no error. | Document that on the override path these are inert, OR validate that `build_attribute.is_some()` implies the caller accepts no projection — reject the combination of `build_attribute: Some` with a non-placeholder `source` to prevent the silent disagreement. |

## F1 detail — the eval'd drv vs `<flake>#<attr>` build semantics

This is the most important correctness divergence introduced this session.

Legacy (`build.rs`): for `Eval` it runs
`nix eval --refresh --raw <flake>#<attr>.drvPath` (`build.rs:292-297`); for
`Build`/`Boot`/`Switch`/`Test` it runs **`nix build --refresh --no-link
--print-out-paths <flake>#<attr>`** directly on the SAME attribute
(`build.rs:298-304`). There is no eval-then-build-the-drv handoff — eval and
build are independent invocations of the same attribute, and BOTH carry the
`--override-input …` and `--option extra-substituters …` tails
(`build.rs:306-339`).

New engine (`schema_runtime.rs`): eval runs
`nix eval --refresh --raw <flake>#<attr>.drvPath` (`eval_drv_path:1223-1233`),
captures the **drv path** as `closure_path` (`run_nix_eval:1113-1117`), then
build runs `nix build --no-link --print-out-paths <drv-path>`
(`nix_build_command:253-260` feeds `evaluated.closure_path` →
`build_closure:1235-1245`). So build is handed a `/nix/store/….drv`, not
`<flake>#<attr>`.

Adversarial consequences:
1. **Substituters dropped at build (F2).** Because build addresses a bare drv,
   not the flake attribute, the `substituters` field is structurally orphaned
   (and indeed never read). Legacy threaded them on the build invocation.
2. **`--refresh` semantics differ.** Legacy build re-locks the flake; building a
   pinned drv does not. For fixtures this is fine; for a moving `github:` ref it
   silently builds a stale eval.
3. **`nix build <drv>` validity is unverified by me.** `nix build` of a
   `.drv` store path is accepted by modern Nix only with the `^*`/`^out` output
   selector in many configurations (`nix build /nix/store/x.drv^*`); a bare
   `nix build /nix/store/x.drv` can error or build nothing depending on the Nix
   version's experimental-features. The smoke "passed" per report 28, so it
   works on the author's Nix — but this is fragile and version-dependent and
   diverges from the legacy direct-attribute build. **I cannot confirm from the
   files that bare-`.drv` build is robust across Nix versions.** Fix: prefer
   building `<flake>#<attr>` directly (legacy parity) so substituters +
   overrides ride along, and reserve the eval'd drv for the `Eval`-action
   reply only.

## (b) DeployAction mapping audit — produces_closure / activates / target_attribute

Checked each variant against legacy `SystemAction::produces_closure/activates`
(`build.rs:25-36`) and `HomeMode::activates` (`build.rs:45-49`):

- `produces_closure` (`schema_runtime.rs:105-110`): `false` only for System
  `Eval`; Home always `true`. MATCHES legacy exactly (`build.rs:26-28`). Note
  Home `Build` produces a closure but does NOT activate — handled correctly by
  the separate `activates()` (below). Correct.
- `activates` (`schema_runtime.rs:115-128`): System Boot/Switch/Test/BootOnce
  true; Home Profile/Activate true. MATCHES legacy (`build.rs:30-35`,
  `build.rs:46-48`). **Test counts as activates AND produces a closure** — the
  task flagged this. Assessed: that is CORRECT and matches legacy (`Test`
  realises + runs `switch-to-configuration test`, `activate.rs:58-59`). The
  real risk is downstream: an activating `Test` reaches `copy_closure` →
  `activate_system` which ssh to a bare node (F5) and ship a literal `$CLOSURE`
  (F6). So `Test` is correctly classified but lands in a broken activate. Not a
  classification bug; a downstream-readiness bug already covered by F5/F6.
- `target_attribute` (`schema_runtime.rs:134-143`): System →
  `nixosConfigurations.target.config.system.build.toplevel`; Home →
  `homeConfigurations.{user}.activationPackage`. MATCHES legacy
  `target_attr` (`build.rs:181-193`) MINUS the `--override-input` tail (F3).
  No wrong mapping in the attribute string itself.

No mis-mapped variant found in `DeployAction`. The enum is faithful to legacy;
the breakage is in what the effects DO with the result (F1/F2/F3/F6), not in the
action's decisions.

## (c) Early-termination + state-clearing audit

Traced `finish_deploy_pipeline` (`schema_runtime.rs:529-542`) on each
terminating path:

- System `Eval`: `ClosureEvaluated` → `produces_closure()==false` →
  `finish_deploy_pipeline` (`648-658`). It sets `active_operation=None` (530)
  and `active_deploy.take()` (531). **State correctly cleared.** Verified.
- System/Home `Build`: `ClosureBuilt` → `activates()==false` →
  `finish_deploy_pipeline` (`660-671`). Same clearing. Correct.
- Full activating chain: ends via `advance_after_phase`
  `ActivatedRecorded → finish_deploy_pipeline` (`519`). Correct.

State-leak findings:
- **F4 (the real leak):** the clearing on FINISH is fine, but there is NO guard
  on START (`record_deploy_submitted:751-777` always overwrites
  `active_deploy`). On a long-lived daemon a second Deploy clobbers an
  in-flight first. This is the genuine cross-deploy leak.
- **Failure paths DO clear:** `fail_pipeline` (`714-727`) and
  `reject_active_or_meta` (`544-570`) both null `active_deploy`. But they do
  **NOT** clear `active_operation` consistently — `fail_pipeline` leaves
  `active_operation` set (it only touches `active_deploy:715`). So after an
  effect failure, `active_operation` stays `Some(Deploy)`; the next Pin/Unpin
  whose `decide_meta_input` overwrites it (`401-412`) recovers it, but a stray
  `WriteRejected` arriving before any new op would mis-route via
  `reject_active_or_meta`'s `unwrap_or(Deploy)`. Minor, but it is a real
  `active_operation` leak on the failure path. Fix: `fail_pipeline` should also
  `self.active_operation = None`.
- **`budget_exhausted_reply` does NOT clear state** (`1358-1365`): on
  continuation-budget exhaustion it replies `DeployRejected` but leaves
  `active_deploy`/`active_operation` populated, so the NEXT deploy hits F4's
  clobber path with stale state. Fix: clearing belongs here too (but the method
  is `&self` — needs a `&mut` redesign or clear-on-next-submit).

## (d) Do the smoke tests prove what they claim?

No — they can pass spuriously. Detail in F7/F8 above. Concretely:

- The eval smoke (`build_smoke.rs:55-65`) only matches `Deployed` and prints
  the id; it never sees the drv. `flake metadata` succeeding + `nix eval`
  emitting a wrong/empty `first_line` still flows to `Deployed`
  (`run_nix_eval` only fails on non-zero exit; a zero-exit-empty-stdout yields
  `closure_path: ""`, which `finish_deploy_pipeline` happily reports as
  `Deployed`).
- The build smoke (`67-79`) is the same shape — reaching `Deployed` does not
  prove a `/nix/store/…` closure was realised, because the reply has no path
  field and the test asserts none.
- The daemon-socket smoke (`86-158`) proves the wire/2-socket/pipeline plumbing
  (genuinely valuable) but is ALSO Eval-only and asserts only `Deployed`
  (`149-157`). It never exercises Build, copy, or activate, so F2/F5/F6 are
  untested by ANY smoke.
- All three are `#[ignore]` (network+nix), so CI proves nothing; only a manual
  `--ignored` run does. That is fine for the M1 bar but means the green-test
  claim rests on a hand-run that asserts only reachability, not correctness.

Fix: thread the realised path into the reply and assert its shape; add at least
one Build smoke that asserts a non-`.drv` `/nix/store` path.

## (e) `source` / `deployment_kind` inertness on the build_attribute path

Covered as F9. Summary: both fields ride into `DeployPipeline` and
`NixEvalCommand` but neither materially affects the override-path eval. The
silent-wrong risk is a caller supplying a real `source`/`deployment_kind`
alongside a `build_attribute` and assuming projection happened — it did not.
The fixture smoke uses `source: "/dev/null"` + `deployment_kind: OsOnly`
(`build_smoke.rs:31-32`) which masks this: `OsOnly` is never consulted on the
override path, so the test would pass identically with `FullOs`. Recommend
rejecting `build_attribute: Some` combined with a non-placeholder `source`, or
documenting the inert contract loudly in the schema (`lib.schema:79-85` half-
documents it but says the daemon "evals/builds `<flake>#<build_attribute>`
with no override-inputs" — which is accurate, so the schema is honest; the
runtime just doesn't guard the contradictory-input case).

## Net assessment

The M1 enum/termination scaffolding (`DeployAction`, stage cursor, finish-on-
finish clearing) is faithful to legacy and structurally sound. The breakage
is concentrated in the **effect bodies** and **missing guards**:

- F1/F2: the build invocation diverges from legacy and drops substituters —
  the single highest-value correctness fix.
- F4: the missing in-flight guard is the genuine long-lived-daemon state leak.
- F6: the activate literal `$CLOSURE` is actively wrong (not merely deferred).
- F7/F8: the smokes assert reachability, not realised-path correctness, so they
  cannot catch F1/F8 regressions.

Everything else (F3/F5/F9) overlaps the known-deferred M2/M3 surface; the
actionable ask there is to **add reject-guards** so production / activating
deploys cannot silently flow into the un-materialized or wrong-address paths
and (per F7) falsely report `Deployed`.
