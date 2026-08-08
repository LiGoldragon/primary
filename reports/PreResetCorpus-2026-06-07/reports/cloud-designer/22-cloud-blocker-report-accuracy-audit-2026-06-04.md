# Accuracy audit — cloud-operator report 14 (cloud schema triad engine blocker)

*The psyche asked: "is this report accurately identifying blockers?
`reports/cloud-operator/14-cloud-schema-triad-engine-blocker-2026-06-04.md`".
This is the verified answer. Method: a five-agent workflow — four
independent investigation angles (schema imports, resolver mechanism,
empirical reproduction, runtime targets + bead) each producing
file:line / exact-error evidence, then an adversarial completeness
judge. All four angles reported high confidence and converged. The
reproductions ran against the COMMITTED canonical checkouts and were
cleaned up (all five repos verified `working copy has no changes`
afterward).*

## Verdict: partially accurate — directionally right, but misidentifies the primary blocker and gets the bead state materially wrong

Report 14 correctly identifies a **real** schema-next bug (the
nested-import resolver loss) and quotes its error variant verbatim.
But that bug is **not** the primary blocker — lowering the actual
committed cloud schemas fails earlier, for more fundamental reasons
the report does not name. And the report's central premise about
*why* it's blocked — "bead `primary-1tsw` is claimed by the operator
with uncommitted in-progress edits" — is flatly false: that bead is
**closed**, assigned to **designer**, and its work is **committed on
`schema-next` main**.

## Claim-by-claim

| Claim | Verdict | Note |
|---|---|---|
| C1 — generated triad engine not done | **confirmed** | `cloud/next` has no `build.rs`; only a hand-written engine scaffold behind a feature gate |
| C2 — SEMA schema lowers with current generator | **refuted / overstated** | Lowers only in a synthetic / next-wired tree. Against canonical `/git`, fails with `Io "No such file: signal-cloud/schema/lib.schema"` |
| C3 — blocker is in schema-next, not file names | **overstated** | Backwards for the *first* failure: that one IS in the file state (missing/misnamed module schemas) |
| C4 — nexus imports `cloud:sema:*` roots | **confirmed** | `nexus.schema:12-15` (ReadInput/ReadOutput/WriteInput/WriteOutput) |
| C5 — sema imports signal-cloud + meta-signal-cloud types | **confirmed** | `sema.schema:7-32` |
| C6 — schema-next drops resolver through nested imports | **confirmed** | `resolution.rs:206` calls bare `module_source.lower(engine)` → `engine.rs:252` builds a fresh `&ImportResolver::new()`. `lower_with_resolver` exists (`module.rs:203-213`) but is never called from `resolve()` |
| C7 — direct root import lowers in isolation | **confirmed** (mechanism) | True when the target module has no onward imports + correct file names |
| C8 — error is `UnresolvedImportCrate { crate_name: "signal-cloud" }` | **confirmed variant; framing wrong** | Variant + field exact (`engine.rs:127-129`). But reproduces verbatim only in a synthetic correctly-named tree — it is the *downstream* blocker, not the current one |
| C9 — bead `primary-1tsw` claimed by operator, uncommitted edits in tree | **refuted (materially false)** | Bead is **CLOSED**, assignee **designer**, work **committed** on `schema-next` main `3f7813cf`; `jj status` clean; no uncommitted multi-module edits anywhere. The only uncommitted cloud-stack work is the hand-written `cloud/next` engine scaffold |
| C10 — hand-written engine exists, not the generated one | **confirmed** (in spirit) | The `cloud/next` scaffold |
| C11 — no-regret: finish `primary-1tsw`, then generate | **insufficient / mis-scoped** | Step one is already done (moot). `NexusRuntime`/`SemaRuntime` targets are real (`schema-rust-next/src/lib.rs:293-314`), but generation cannot run until several unnamed gates clear (below) |

## The corrected blocker hierarchy — what actually fires, in order

The report names one blocker (schema-next resolver). The audit found a
**stack** of them; the resolver bug is item 4, not item 1.

1. **Type-name content drift (deepest).** `cloud/schema/sema.schema`
   imports `signal-cloud:lib:PlanQuery, :Validated, :Observed,
   :PlanResult` and `nexus.schema` imports `signal-cloud:lib:Input,
   :Output` — but the next-worktree `signal-cloud` `lib.schema` does
   **not define those names** (it has roots `[Observe Validate]` /
   `[Observed Validated RequestUnsupported RequestRejected]`, and types
   `ObservationResult`, `ValidationReport`, `Plan`). So even with the
   resolver fixed, files reachable, and crates registered, resolution
   hits `ImportedTypeNotFound` (`resolution.rs:207-216`). The cloud
   daemon schemas and the contract schemas are **mutually
   inconsistent** — this is more fundamental than the resolver bug and
   the report names it nowhere.
2. **Canonical-vs-next schema split.** The resolvable `lib.schema`
   (signal-cloud) and `meta-signal-cloud.schema` (owner-signal-cloud,
   package renamed `meta-signal-cloud`) exist **only in the
   `~/wt/.../next` worktrees** (today's wire-only commits). The `/git`
   canonical checkouts carry only `*.concept.schema`. Yet
   `cloud/schema/{nexus,sema}.schema` live on `/git` main and reference
   contract modules that only exist on next. The report treats
   `cloud/schema/*` as "real runtime files that lower today" without
   flagging they cannot resolve against the canonical contract
   checkouts.
3. **Missing module schema files on canonical.** Because of (2), a
   canonical-checkout build fails first with `Io "No such file:
   signal-cloud/schema/lib.schema"` — `signal-cloud` exposes only
   `signal-cloud.concept.schema`. The package loader expects
   `<schema_dir>/<module>.schema` (`module.rs:42-49`); `concept.schema`
   is not a module name an import like `signal-cloud:lib:Observation`
   will load.
4. **schema-next nested-resolver bug (the report's named blocker).**
   Real and present at `resolution.rs:206`: a directly-imported module
   is lowered with a fresh empty resolver, so its own nested imports
   resolve against nothing → `UnresolvedImportCrate`. The fix is one
   line (call `module_source.lower_with_resolver(engine, self)` —
   `module.rs:203-213` already provides it). But this fix alone does
   **not** unblock cloud generation; it only matters once items 1-3 are
   resolved.
5. **No cloud `build.rs` / no auto-discovery wiring.** `cloud/next` has
   no `build.rs`; neither `signal-cloud` nor `owner-signal-cloud`
   declares a Cargo `links` key or emits `DEP_<LINKS>_SCHEMA_DIR`, so
   `schema-rust-next`'s auto-discovery (`build.rs:271-280`) returns
   `None`. Even after a resolver fix there is no wiring to feed contract
   schema dirs to a cloud generation step.
6. **`meta-signal-cloud` repo not created (deployment gate).**
   `cloud/next/Cargo.toml` confirms "the meta-signal-cloud GitHub repo
   is not created yet"; the contract is carried by a local path dep
   into `owner-signal-cloud/next`. Not a resolver-name blocker (see the
   subtlety below), but a real gate to productionizing the generated
   engine that C11 omits.

## Root cause the resolver bug survived: test-coverage gap

The only multi-module test
(`tests/lowering.rs:229 package_loader_reads_all_schema_modules_in_crate`)
uses a fixture where the nested module imports nothing further, so the
resolver-loss path is **never exercised**. `primary-1tsw` could close
green while `resolution.rs:206` still drops the resolver. Any fix
should add a `nexus → sema → third-crate` test.

## The meta-signal-cloud subtlety, resolved precisely

My going-in hypothesis was that `meta-signal-cloud:*` imports can't
resolve because no repo by that name exists. The audit refined this:

- **NOT a resolver-name blocker.** Resolution matches by registered
  Cargo **crate-name string** (`resolution.rs:185`), not by repo
  directory. `owner-signal-cloud/next/Cargo.toml`'s package name **is**
  `meta-signal-cloud` (lib `meta_signal_cloud`), and `cloud/next`
  registers it by path. So `meta-signal-cloud:meta-signal-cloud:*`
  imports resolve fine **when** the dep is wired and the module file
  exists.
- **But the gates are real**: the `meta-signal-cloud.schema` module
  file exists only on next (not canonical `/git`), and no
  `meta-signal-cloud` repo exists. So the concern was directionally
  right — just located in deployment + canonical-vs-next, not in the
  resolver's name matching.

## What report 14 should be corrected to say

- **C9 is the load-bearing error to fix**: `primary-1tsw` is closed
  (assignee designer), committed on `schema-next` main `3f7813cf`. The
  "operator's in-progress worktree" does not exist; the uncommitted
  cloud work is the hand-written `cloud/next` engine scaffold. Drop the
  "finish/commit `primary-1tsw`" framing entirely.
- **Reframe the primary blocker**: not the schema-next resolver, but
  the cloud-schema ↔ contract-schema **type-name mismatch** plus the
  **canonical-vs-next split**. The resolver fix is a real-but-secondary
  one-liner.
- **Name the full gate list** (items 1-6 above) so the operator's next
  step is scoped correctly.

## Sequenced fix path (replacing C11)

1. Reconcile the cloud daemon schemas against the actual contract
   `lib.schema` / `meta-signal-cloud.schema` type names (resolve the
   `Input`/`Output`/`PlanQuery`/`Validated`/`Observed`/`PlanResult`
   drift) — blocker 1.
2. Land the contract module schemas (`lib.schema`,
   `meta-signal-cloud.schema`) on the **canonical** checkouts the build
   resolves against, or point the build at next — blocker 2/3.
3. Fix `resolution.rs:206` → `lower_with_resolver`, and add the
   `nexus → sema → third-crate` regression test — blocker 4 + root
   cause.
4. Wire cloud schema discovery (`build.rs` + Cargo `links` /
   `DEP_<LINKS>_SCHEMA_DIR`, or explicit path registration) — blocker 5.
5. Create/rename the `meta-signal-cloud` repo before productionizing —
   blocker 6.
6. Then run `schema-rust-next`'s `NexusRuntime`/`SemaRuntime` targets.
