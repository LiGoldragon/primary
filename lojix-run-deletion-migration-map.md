# lojix-run deletion migration map

Task: read-only investigation of how visible `lojix-run` behavior can be removed by direct current `lojix` / `meta-lojix` use, Lojix component changes, documentation/operator procedure, or deletion with no replacement. Scope was public repos and generated public doctrine only; `private-repos/` was not inspected.

## Spirit and doctrine grounding

Observations:

- Public Spirit search for legacy compatibility/wrapper direction found `10pz`: replace rather than preserve older compatibility shapes when they manufacture legacy. This supports deleting `lojix-run` legacy syntax rather than carrying it forward.
- Public Spirit search for `meta lojix` found only broad `zn2l` self-improving-engine direction; public searches for direct Lojix deploy/parity records returned no matching public record. Local Lojix docs cite several Spirit ids, but `Lookup 75pw`, `vudl`, `tvbn`, `ssk2`, and `up9q` returned `(Error [record not found])`, so this report treats those as local-doc citations, not public Spirit evidence.
- Local `lojix/INTENT.md:10-20` says `lojix` is the new deploy stack with `lojix-daemon`, `lojix`, `meta-lojix`, and `lojix-write-configuration`; it aims for parity with legacy `lojix-cli` and retirement of the legacy stack.
- Local `lojix/INTENT.md:24-42` says there are two CLIs, one per socket, and every external operation is typed Signal with no untyped wire escape hatch.
- Local `lojix/ARCHITECTURE.md:62-76` assigns reads/watches to ordinary `signal-lojix` and deploy/retention mutations to owner/meta `meta-signal-lojix`.

Interpretation:

- The intended end state is direct typed Lojix usage plus Lojix component improvements where the component is missing first-class behavior. It is not another wrapper and not legacy `FullOs` / `OsOnly` / `HomeOnly` top-level syntax.

## Exact current request shapes replacing legacy forms

Use `meta-lojix`, not `lojix-run`, for deploy submission. Evidence: `lojix/src/bin/meta-lojix.rs:1-6` says `meta-lojix` is the owner/meta-socket client for `Deploy` / `Pin` / `Unpin` / `Retire`; `lojix/src/client.rs:116-124` says `MetaClient` speaks `meta-signal-lojix` policy; `meta-signal-lojix/schema/lib.schema:60-68` lists `Deploy` as a meta input.

Current typed forms:

- Legacy `FullOs` system deploy becomes:

  ```sh
  meta-lojix "(Deploy (System (<cluster> <node> FullOs <proposal-source> <criomos-flake-ref> <action> <builder> [] None)))"
  ```

- Legacy `OsOnly` system deploy becomes:

  ```sh
  meta-lojix "(Deploy (System (<cluster> <node> OsOnly <proposal-source> <criomos-flake-ref> <action> <builder> [] None)))"
  ```

- Legacy `HomeOnly` home deploy becomes:

  ```sh
  meta-lojix "(Deploy (Home (<cluster> <node> <user> <proposal-source> <criomos-flake-ref> <mode> <builder> [])))"
  ```

Evidence:

- Generated operating-system doctrine gives the direct forms at `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md:26-38` and repeats the actions/modes/builder rule.
- `meta-signal-lojix/schema/lib.schema:107-128` defines `DeployRequest` as `(System SystemDeployment)` or `(Home HomeDeployment)` with fields in the same order.
- `signal-lojix/schema/lib.schema:63-64` defines `DeploymentKind [FullOs OsOnly HomeOnly]` and `SystemAction [Eval Build Boot Switch Test BootOnce]`.
- `meta-signal-lojix/schema/lib.schema:94-97` defines `HomeMode [Build Profile Activate]`, `ExtraSubstituter`, and `Builder`.
- `meta-signal-lojix/tests/round_trip.rs:15-28` constructs a current `SystemDeployment` with `deployment_kind`, `source`, `flake`, `system_action`, `builder`, empty `substituters`, and `build_attribute: None`.

Ambiguities:

- The exact NOTA text for a non-empty `Vec ExtraSubstituter` is not shown in the consulted CLI docs/tests; visible examples use `[]`. The schema names the fields (`url`, `public_key`) at `meta-signal-lojix/schema/lib.schema:96`, and runtime consumes them at `lojix/src/schema_runtime.rs:964-973` and emits Nix extra-substituter options at `lojix/src/schema_runtime.rs:4340-4365`. If non-empty substituters are needed, verify the generated NOTA parser shape in `meta-signal-lojix` rather than preserving wrapper host-label syntax.
- Direct equivalence for the wrapper's local branch exactification is intentionally not a request-shape feature. Direct callers can pass exact flake references. If server-side exactification is wanted, that is a Lojix runtime contract change, not a client wrapper compatibility feature.

## Behavior-by-behavior migration map

| Visible `lojix-run` behavior | Current wrapper behavior and evidence | Replacement classification | Recommendation / smallest Lojix change |
|---|---|---|---|
| Legacy top-level request translation | `Request` rewrites original heads `FullOs`, `OsOnly`, `HomeOnly` to `Deploy` at `CriomOS-home/packages/lojix-run/lojix-run.py:21-29`. `LegacyDeployTranslator.text()` maps `HomeOnly` to `(Deploy (Home ...))` and system kinds to `(Deploy (System ...))` at `lojix-run.py:123-167`. | Direct current Lojix usage; delete compatibility syntax. | Replace call sites/docs with the exact current `meta-lojix` shapes above. Do not add legacy heads to Lojix schema. This follows public Spirit `10pz`. |
| Builder normalization | Legacy builder field `None` stays `None`; bare value becomes `(Some <atom>)` at `lojix-run.py:176-181`. | Direct current usage / docs. | Operators write `None` or `(Some <builder-node>)` directly; generated doctrine already says this at `.agents/skills/operating-system-operations/SKILL.md:38`. |
| Legacy substituter handling | Wrapper maps absent/empty/`None` to `[]`, accepts already-bracketed list, and rejects old host labels with `legacy substituter host labels cannot be translated...` at `lojix-run.py:183-188`. | Direct current usage; likely docs/tests gap for non-empty examples. | Keep deletion. If non-empty substituters are operator-facing, add schema/contract tests or docs in `meta-signal-lojix`/`lojix` showing exact NOTA text for `Vec ExtraSubstituter`; do not revive host-label shorthand. |
| One argument / inline or file source | Wrapper takes exactly one argument, treats strings starting `(` as inline, otherwise reads path text at `lojix-run.py:592-609`. | Direct current Lojix usage, with minor operator procedure. | `lojix`/`meta-lojix` already take one component argument: `lojix/src/bin/lojix.rs:1-5`, `meta-lojix.rs:1-6`, and `lojix/src/client.rs:64-82,124-142`. Difference: current clients treat `.nota` paths as text and other paths as signal files (`client.rs:73-80,133-139`). Rename text request files to `.nota` or pass inline. |
| Invoking `meta-lojix` | Wrapper shells `[self.meta_lojix, self.request.text]` at `lojix-run.py:301-309`, with env override at `lojix-run.py:274`. | Direct current Lojix usage. | Use `meta-lojix` directly. `lojix/Cargo.toml:22-28` ships `meta-lojix` and `lojix-write-configuration`; `lojix/flake.nix:65-72` packages the default with `--features nota-text`. |
| Local branch exactification | Wrapper rewrites `github:LiGoldragon/CriomOS/main` and `github:LiGoldragon/CriomOS-home/main` to `...?rev=<jj main commit>` from local checkouts when possible at `lojix-run.py:196-214,216-243`. | Documentation/operator procedure; possible Lojix runtime policy if strict reproducibility is required. | Prefer explicit exact flake refs in the request. Generated doctrine already says use pinned flake revisions for effect-bearing deploys when branch resolution/cache freshness is uncertain (`.agents/skills/operating-system-operations/SKILL.md:12`). If Lojix should enforce/record exactness, smallest component change belongs in `lojix` daemon runtime: resolve mutable `FlakeReference` server-side, record the resolved ref/revision in durable deploy state/events, and evaluate that exact ref. Evidence: `lojix/schema/nexus.schema:77-78` has `ResolvedFlake`; current runtime resolves flake metadata at `schema_runtime.rs:2817-2834` but `EffectResult::FlakeResolved(_)` ignores the payload and continues with `pipeline.flake` at `schema_runtime.rs:2189-2203`. |
| Run directory and request/stdout/stderr capture | Wrapper creates `$XDG_STATE_HOME/lojix-runs/<timestamp>-<kind>-<node>` and writes original/rewritten requests and stdout/stderr logs at `lojix-run.py:246-268`; it hashes/log-counts stdout/stderr in summary at `lojix-run.py:405-428`. | Lojix component observation API and/or operator shell procedure; not a wrapper. | For durable deploy evidence, use Lojix's event/subscription/query surfaces, not per-client log files. The schema already defines `WatchDeployments`, `ByEventLog`, `DeploymentPhaseEvent`, and `EventLogPosition` at `signal-lojix/schema/lib.schema:23-24,93-103,140-150`. Runtime records phase transitions at `schema_runtime.rs:2424-2449`. However, the current ordinary query path routes every `Query` except `ByTestRun` to generation listing at `schema_runtime.rs:1531-1541`; `ByEventLog` then matches all live generations at `schema_runtime.rs:2737-2751`, while real `read_event_log` exists but is not reached from ordinary `Query` (`schema_runtime.rs:2770-2795`). Smallest Lojix change: fix ordinary event-log query routing/output in `signal-lojix`/`lojix` query API so operators can retrieve typed phase events after submit. |
| Success/failure summary | Wrapper prints `lojix_run=success|failed`, request kind, cluster/node/user/action/mode, run directory, line counts, hashes, and `root_home_fallback=success` at `lojix-run.py:397-428`; failure prints redacted tails at `lojix-run.py:541-563`. | Mostly deletion / Lojix observation API; some operator procedure. | `meta-lojix` already prints one typed reply (`meta-lojix.rs:10-20`), and current deploy replies are typed `Deployed`/`DeployRejected` (`meta-signal-lojix/schema/lib.schema:69-78,134-146`). Do not reproduce ad-hoc key=value summary. If operator reports need non-secret evidence, add a typed `DeployStatus`/event-log read surface or docs saying which `lojix` queries to run and how to report markers/ids. |
| Store-path redaction in chat-facing failure tails | Wrapper redacts store hashes from tails using `STORE_HASH_PATTERN` and `Redactor.tail()` at `lojix-run.py:15,552-563`; checks verify redaction at `checks/lojix-run/default.nix:39-56`. | Lojix component logging hygiene plus operator procedure. | Keep raw build output out of chat/reports via procedure. For component-level parity, add redaction or structured error detail in `lojix` daemon logs/typed failures. Current `NixCommand::run` returns failure strings containing command args and stderr at `schema_runtime.rs:4388-4404`, and `fail_pipeline` logs details to stderr at `schema_runtime.rs:2309-2313`; daemon also logs terminal output with `Debug` at `daemon.rs:573-583`. |
| Success store-path extraction and postcheck trigger | Wrapper only recognizes success stdout that is exactly one `/nix/store/...` line, or fallback home generation, at `lojix-run.py:311-320`. | Delete / replace with current Lojix query semantics. | This is mismatched with current typed `meta-lojix`: `finish_deploy_pipeline()` replies `(Deployed ...)`, not a raw store path (`schema_runtime.rs:2037-2055`; output shape at `meta-signal-lojix/schema/lib.schema:134-146`). Thus postchecks may not run for current typed deploys unless fallback fabricated a store path. Use `lojix "(Query (ByNode ...))"` after submit; schema returns `Generation` with `ClosurePath` at `signal-lojix/schema/lib.schema:81-91`. |
| Root home fallback | On failed `HomeOnly` `Profile`/`Activate`, if stderr contains a copied home-manager generation, wrapper SSHes as root and runs `nix-env --set` plus activation under `runuser`; if that succeeds it replaces the failed return code with success at `lojix-run.py:279-286,322-352,355-394`. | Unsafe to reproduce as wrapper behavior. If needed, fix Lojix activation contract/runtime. | Do not preserve success override or hidden root mutation. Lojix already has first-class `HomeActivation` that sets profile and runs activation locally or over user SSH (`schema_runtime.rs:4001-4056`) with local-context detection (`schema_runtime.rs:4078-4104`). If root-assisted activation is truly required, make it an explicit typed Lojix activation mode or privilege strategy in schema/runtime, with failures reflected as `DeployRejected`, not a client-side fallback. |
| System postchecks | After successful system `Boot`/`Switch`/`Test`/`BootOnce`, wrapper SSHes root and compares `/nix/var/nix/profiles/system` and `/run/current-system` with the deploy path at `lojix-run.py:436-463`. | Lojix runtime verification, not non-fatal wrapper. | If these checks are required, fold them into the activation effect before `RecordGenerationActivated`: system activation already sets profile and switches at `schema_runtime.rs:3771-3788`, handles BootOnce/self-switch units at `schema_runtime.rs:3795-3999`, and commits live generation only after activation at `schema_runtime.rs:2236-2240,2454-2507`. A profile/current-system mismatch should fail the deploy pipeline rather than print a non-fatal postcheck. |
| Home postchecks | After successful home `Profile`/`Activate`, wrapper SSHes root and checks home profile symlink, failed user units, niri reload, and pi symlink at `lojix-run.py:465-539`. | Split: generic activation verification can be Lojix; desktop/app-specific checks should be docs/operator procedure or deleted. | Home profile verification belongs with Lojix activation if needed (`schema_runtime.rs:4001-4056`). `failed_user_units` may be a documented operator check for task-specific validation. `niri msg action load-config-file` is runtime UI procedure, not deploy correctness; `CriomOS-home/skills.md:224-229` already documents activation then niri reload. `/home/$user/.pi/agent/packages/pi-continue` is agent-specific and should not live in Lojix. |
| Niri reload | Wrapper finds a niri socket and runs `niri msg action load-config-file`, writing temp logs under `/tmp/lojix-run-niri.*`, at `lojix-run.py:496-524`. | Documentation/operator procedure; unsafe to hide in deploy tool. | Do not reproduce inside Lojix. Keep/update explicit operator docs for Niri reload after home activation (`CriomOS-home/skills.md:224-229`). This is a session/app reload, not a deployment contract. |
| Pi symlink check | Wrapper prints whether `/home/$user/.pi/agent/packages/pi-continue` is a symlink at `lojix-run.py:487-491`. | Delete with no replacement in Lojix. | Agent-specific check does not belong in generic deploy component. If still useful, move to pi/agent docs or a task-specific verification checklist, not Lojix. |
| Non-fatal postcheck failure | `remote_print()` prints `postcheck=failed` and redacted stderr but does not change process status at `lojix-run.py:526-539`; postchecks run only after a zero deploy return at `lojix-run.py:295-299`. | Unsafe to reproduce. | Lojix should make deploy-critical verification fatal in the deploy pipeline; non-critical operator checks should be manual/docs. |
| Target domain derivation | Wrapper derives `root@<node>.<cluster>.criome` from request fields at `lojix-run.py:57-62,337-348,526-529`. | Direct Lojix runtime usage. | Lojix already derives target SSH forms: deploy pipeline `resolved_target()` uses `SshTarget::root_at_node` at `schema_runtime.rs:1126-1134`; build-on-target docs use `ssh-ng://root@<node>.<cluster>.criome` at `ARCHITECTURE.md:18-29`. |

## Behaviors unsafe to reproduce

- Root fallback success override: it mutates home profile/activation as root after a failed Lojix run and converts the process result to success (`lojix-run.py:279-286,337-352`). This can hide the real failure mode and diverge Lojix state from host state.
- Hidden runtime mutation after deploy: niri reload is an application/session operation, and pi symlink probing is agent-specific (`lojix-run.py:496-524,487-491`). These should not be generic Lojix deploy side effects.
- Non-fatal postcheck failures: wrapper prints `postcheck=failed` but keeps success status (`lojix-run.py:526-539`). Deploy-critical verification should be fatal in Lojix; non-critical checks should be explicit operator procedure.
- Legacy syntax preservation: public Spirit `10pz` says to replace older shapes rather than preserve compatibility paths that manufacture legacy.
- Chat-facing raw log handling by ad-hoc wrapper: if redaction/hashing is required, it should be a Lojix logging/observation contract, not a separate deploy client.

## Component-level gaps to close in Lojix before/with deletion

Observations:

1. Current deploy submission shape exists and should be used directly (`meta-signal-lojix/schema/lib.schema:107-128`; generated doctrine `.agents/skills/operating-system-operations/SKILL.md:26-38`).
2. Current `meta-lojix` replies are typed, not raw store paths (`meta-lojix.rs:10-20`; `schema_runtime.rs:2037-2055`).
3. Event-log data is recorded but ordinary `ByEventLog` does not currently return it through the visible query path (`schema_runtime.rs:1531-1541,2737-2751,2770-2795`).
4. Current failure logging can include raw stderr/details (`schema_runtime.rs:4388-4404,2309-2313`; `daemon.rs:573-583`).
5. Activation code is in Lojix runtime for system and home (`schema_runtime.rs:3750-4105`), so deploy-critical verification belongs there if required.

Recommended smallest changes:

- Query/observation API: fix `ByEventLog` routing and output shape so operators can retrieve typed deployment phase events. Likely touches `signal-lojix` schema if the ordinary `Output` needs an event-log page variant, plus `lojix/src/schema_runtime.rs` routing/tests.
- Daemon runtime: if exact flake resolution is required, use/record `ResolvedFlake` rather than ignoring it after metadata resolution. Likely belongs in `lojix/src/schema_runtime.rs` and deploy event/durable state; docs should say whether mutable branch refs are accepted, resolved, or rejected.
- Daemon runtime/logging: replace raw stderr debug logging with structured, redacted typed failure details or documented operator-safe evidence. Likely belongs in `NixCommand::run`, `fail_pipeline`, daemon terminal logging, and tests.
- Daemon runtime: fold system/home profile verification into activation effects before committing `GenerationActivated` if that verification is required for correctness. Do not implement it as non-fatal postcheck.
- Docs/tests: add non-empty `ExtraSubstituter` NOTA examples if operators need them; current visible examples cover only `[]`.

## Docs/check/package references to remove or update for deletion

- Delete package implementation: `/git/github.com/LiGoldragon/CriomOS-home/packages/lojix-run/default.nix` and `/git/github.com/LiGoldragon/CriomOS-home/packages/lojix-run/lojix-run.py`. Also remove the generated/untracked pycache under that package directory if cleaning the tree.
- Remove home profile package inclusion: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:264-270` includes `inputs.lojix...default` and the wrapper package; remove only the wrapper line, keep current `lojix` package.
- Remove check: `/git/github.com/LiGoldragon/CriomOS-home/checks/lojix-run/default.nix` and `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:357` check attr.
- Update `CriomOS-home/skills.md:214-222`, which currently directs use of `lojix-run`; replace with direct `meta-lojix`/`lojix` procedure and safe reporting guidance. Keep/update the explicit Niri reload procedure at `skills.md:224-229` if still desired.
- Update stale risk note `/git/github.com/LiGoldragon/CriomOS-home/RISK.md:68-70` referencing the authorized `lojix-run` / `meta-lojix` activation path.
- Generated primary operating-system skill already uses direct `lojix`/`meta-lojix` and does not mention `lojix-run` (`/home/li/primary/.agents/skills/operating-system-operations/SKILL.md:16-50`); no wrapper deletion update found there.
- Historical `agent-outputs/` references were observed but should not be rewritten as live docs unless the parent explicitly scopes archival cleanup.

## Commands consulted

- `spirit '(PublicTextSearch [legacy compatibility wrappers lojix])'`, `spirit '(PublicTextSearch [meta lojix])'`, related public Spirit searches and lookups.
- `rg -n --hidden --glob '!private-repos/**' --glob '!**/.git/**' --glob '!**/target/**' 'lojix-run|FullOs|OsOnly|HomeOnly' ...` over `/home/li/primary` and public Lojix/CriomOS repos.
- `nl -ba` / `sed` reads of `CriomOS-home/packages/lojix-run/lojix-run.py`, `default.nix`, `checks/lojix-run/default.nix`, `modules/home/profiles/min/default.nix`, `skills.md`, `RISK.md`.
- `nl -ba` / `sed` reads of `lojix/INTENT.md`, `ARCHITECTURE.md`, `skills.md`, `Cargo.toml`, `flake.nix`, `src/bin/{lojix,meta-lojix}.rs`, `src/client.rs`, `src/schema_runtime.rs`, `src/daemon.rs`, `schema/nexus.schema`, and selected tests.
- `nl -ba` / `sed` reads of `signal-lojix/schema/lib.schema`, `meta-signal-lojix/schema/lib.schema`, and selected generated/test files.
- `jj status --no-pager` in `/home/li/primary`, `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/lojix`, `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`; reran final status after writing this report for `/home/li/primary`, `CriomOS-home`, and `lojix`.

## Unknowns and residual risks

- I did not inspect `private-repos/` by request.
- I did not run live `lojix`/`meta-lojix` commands against the daemon, run builds, or run tests; this is source/doc evidence only.
- Non-empty `ExtraSubstituter` NOTA syntax needs parser-backed verification if it becomes operator-facing.
- The exact desired Lojix redaction/reporting contract is not specified in visible docs; this report identifies where raw output currently enters runtime logs and recommends making any replacement typed and component-owned.
- Current public repo state before this report already had unrelated dirty files in `/home/li/primary` and an existing untracked pycache in `CriomOS-home`; I did not modify them.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Read-only investigation only; wrote the requested report at /home/li/primary/lojix-run-deletion-migration-map.md and did not edit implementation/docs/repos."
    },
    {
      "id": "criterion-2",
      "status": "satisfied",
      "evidence": "Report cites exact source paths and line ranges for wrapper behavior, current typed schemas, Lojix runtime behavior, docs/check/package references, and unsafe behaviors."
    }
  ],
  "changedFiles": [
    "/home/li/primary/lojix-run-deletion-migration-map.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "spirit '(PublicTextSearch [legacy compatibility wrappers lojix])' and related public Spirit searches/lookups",
      "result": "passed",
      "summary": "Found public replacement-over-compatibility record 10pz; direct Lojix public records mostly not found."
    },
    {
      "command": "rg -n --hidden --glob '!private-repos/**' --glob '!**/.git/**' --glob '!**/target/**' 'lojix-run|FullOs|OsOnly|HomeOnly' ...",
      "result": "passed",
      "summary": "Located wrapper implementation, package/check/docs references, current generated doctrine, schemas, and runtime references."
    },
    {
      "command": "nl -ba / sed reads of relevant public files",
      "result": "passed",
      "summary": "Collected line-number evidence from CriomOS-home, lojix, signal-lojix, and meta-signal-lojix."
    },
    {
      "command": "jj status --no-pager in primary and relevant public repos",
      "result": "passed",
      "summary": "Observed pre-existing dirty files in primary and CriomOS-home; lojix/signal-lojix/meta-signal-lojix clean before report write."
    },
    {
      "command": "final jj status --no-pager in /home/li/primary, /git/github.com/LiGoldragon/CriomOS-home, and /git/github.com/LiGoldragon/lojix",
      "result": "passed",
      "summary": "Primary shows this report plus three unrelated pre-existing added files; CriomOS-home still shows only the pre-existing pycache; lojix remains clean."
    }
  ],
  "validationOutput": [
    "No tests or live deploy commands run; investigation was source/doc only by request.",
    "Initial /home/li/primary jj status showed three unrelated added files before this report.",
    "Initial CriomOS-home jj status showed pre-existing added packages/lojix-run/__pycache__/lojix-run.cpython-313.pyc.",
    "Initial lojix, signal-lojix, and meta-signal-lojix jj status reported no working-copy changes."
  ],
  "residualRisks": [
    "Non-empty ExtraSubstituter NOTA shape not verified with parser.",
    "No live daemon observation was performed.",
    "Final /home/li/primary working copy includes this report plus pre-existing unrelated dirty files; no staging operation exists in jj and none was performed."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one investigation report; no implementation files changed.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "private-repos was not inspected; historical agent-output references were observed but not treated as live docs to update."
}
```
