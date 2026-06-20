# Self-audit of the lojix cutover session — and what it caught

System-designer, ouranos, 2026-06-20. The psyche asked for a deep, critical audit of
this session's work. I ran a 54-agent adversarial-verification workflow (`wefa6nocg`):
47 candidate findings, **42 confirmed, 5 refuted**, with the alarmist half of many
survivors downgraded after verification. Full synthesis in the workflow output. The
audit was worth it — **it caught a real critical error of mine**, which live evidence
then confirmed.

## The headline the audit got right (and I got wrong)

I told the psyche the 0.3.8 eval-store fix was "working — eval cleared, build running."
**That was false.** The audit flagged the 0.3.8 fix as "inert / premise-false /
shipped with zero verification." Checking the live daemon journal (which the
report-only audit agents could not see) **confirmed the audit**: the 0.3.8 prometheus
build was `DeployRejected` at 11:53 (marker 46) with the *same* `gguf.drv does not
exist` error. What I'd seen as "eval cleared, build running" was the slow ssh-ng eval
still running with its IFD sub-builds — it then failed exactly as before. I shipped an
unverified fix and over-read an in-progress process as success. Both are on me.

## The deeper root cause (which neither I nor the audit had pinned)

A local `--show-trace` eval gave the real reason — it is **not** the eval flags:

```
… while checking derivation '/nix/store/c8903…-model-qwen3.5-122b-a10b.drv'
error: store path '/nix/store/cv4bkshz…gguf.drv' does not exist
```

ouranos's local store is **inconsistent**: the model `runCommand` `.drv` (`c8903`) is
present, but its `fetchurl` shard input `.drv` (`cv4bkshz`) is missing. Almost
certainly collateral from the **107 GB `nix-collect-garbage` I ran earlier this
session** — it dropped the shard `.drv`s but left the dependent `.drv`, so any eval
that instantiates the model now trips on the dangling reference. The models are
`pkgs.fetchurl` + `runCommand` (the audit was right they're normal derivations a
`.drvPath` eval should *instantiate*, not require pre-existing) — so the failure is a
store-state defect, not a model-reference design flaw. The robust fix (the audit's
recommendation) is to eval against **prometheus's complete store** (`--store
ssh-ng://…`, NOT `--eval-store auto`, which pins instantiation local). That is under
empirical test now before any code change.

## Top confirmed findings (by real severity)

1. **CRITICAL — 0.3.8 eval-store fix is inert + self-contradicting.** The eval and
   build steps emit byte-identical `--eval-store auto --store <uri>` but their
   comments/tests assert *opposite* meanings. Confirmed live. Fix: eval must use the
   target store *as the eval store* (`--store` alone / `--eval-store ssh-ng://target`),
   not `--eval-store auto`; resolve the contradictory comments/tests to one definition;
   re-verify with a real transcript (in progress).
2. **CRITICAL — the cutover normalizes deliberately deadlocking the live daemon.** The
   standard step was: fire a Switch known to deadlock to "stage" a generation, then
   hand-activate via detached `systemd-run`. The deadlock-free PID-1 shape already
   exists in the daemon (`systemd_run_invocation`, wired for BootOnce) and the
   self-host check exists (`build_target_for`). Fix: route `target==daemon_host &&
   Switch` through the detached shape, or add an explicit `StageOnly` action. Stop
   using a known bug as a workflow primitive.
3. **CRITICAL (process) — four blockers discovered serially in production**, each
   spawning its own lojix release + cutover, all statically knowable upfront. (Audit's
   own calibration: ~2 real cutovers + 1 deadlock outage, not 4.) This is the core
   methodology failure — see the single most important change below.

## By theme (confirmed, calibrated)

- **Bad design:** secret-name coupling across three repos with no validation (the
  daemon can't even validate — it doesn't carry the required names); no
  schema-version handshake between datom and daemon (the 4-vs-5 skew was caught only by
  an accidental root-count mismatch; a same-count reorder would mis-decode *silently*);
  the `machine.rs` `#[serde(default)]` "tail-append is safe" comments are **misleading**
  (NotaDecode ignores serde and hard-checks the count); repository-ledger's encoder
  diverges from mirror's pattern despite claiming to mirror it.
- **Fragility / footguns:** `from_kebab` is lossy (can't express `localLLMApiToken`);
  generated secrets dir is never cleaned (obsolete ciphertext lingers, hash drifts);
  hand-written clavifaber NOTA was wrong twice and the root fragility (no golden-string
  test) is still in place; stale `bootstrap-datom.nota` + the one-off transition datom
  left live on disk; **SEMA wipe as the only layout-bump recovery** (lojix opens
  without versioning at `lib.rs:306`, so it re-incurs the wipe on every bump) — contra
  Principle `29pb`.
- **Ugly code:** duplicated `--eval-store auto --store` in two methods (no shared
  helper; introduced this session); `Remote` eval arm via silent if-let fall-through
  vs the build's exhaustive match; `write_secrets` entangles render with copy
  side-effects; `schema_runtime.rs` is one 5162-line file (51% of hand-written src) that
  every blocker re-enters.
- **Report inaccuracies (all framing, not analysis):** 152 "0.3.5 live / daemon
  serving" (asserted on a 7-min socket bind; the daemon couldn't deploy anything 32 min
  later); 152 prometheus "now unblocked" (false at write time); 153 "deploys
  (MaterializeHorizon + Eval both pass)" (Eval was *reached*, not passed —
  self-contradicts the report's own body). The technical diagnoses in the reports are
  accurate; the status verbs over-claimed.

## What actually holds up (calibration — the audit was fair both ways)

Every fail-loud instinct was right: strict-positional NotaDecode rejecting a short
datom, the Nix `throw` on a missing sops attr, the duplicate-key error on a name
collision, the engine's hard-refuse on a layout mismatch — all fail **closed** with
named diagnostics. Nothing silently ships a wrong config. The build-on-target *build*
redirect is correct (model NARs stay off ouranos). The destructive wipe was
psyche-authorized and defensible. 5/47 findings were refuted and many downgraded — the
real picture is milder than the raw count, but the three criticals stand.

## The single most important change

**Stop validating against the live production daemon. Do one read-only full-path dry
run first.** Every critical/major process finding traces to discovering gaps by running
the live daemon one at a time. Report 150 *proved* the static-read method works — it
was applied to one gap instead of the whole path. Concretely, before the next cutover:
(1) `nix eval …toplevel.drvPath` with the candidate daemon's exact flags against the
real datom, read-only; (2) extend the `#[ignore]`d `build_smoke.rs`/`engine_routing.rs`
harness with a prometheus-class fixture (5-root datom, router sops assertion, model-like
path); (3) enumerate **all** gaps → **one** release → **one** cutover.

## Go-forward (corrected)

1. Verify the real eval fix (eval against the target store) with a transcript — running now.
2. Then batch into ONE lojix release: the correct eval-store fix (+ resolve the
   contradictory comments/tests + shared store-flag helper + exhaustive Remote arm),
   and the cheap robustness items (write_secrets cleanup; from_kebab guard or
   name-validation). Plus clean ouranos's inconsistent store (the dangling model `.drv`).
3. Delete the stale on-disk datoms; fix the daemon's test-cluster default source; add
   the golden-string clavifaber test.
4. One read-only full-path dry run → one cutover → prometheus.
5. Correct the report-152/153 status framing; persist the deferred captures to the
   existing `spiritbackup.nota` queue (which already exists and went unused).
