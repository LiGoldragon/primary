# Lojix Full Test-Backed Audit

Task and scope: audit the Lojix operating-system deploy/readiness path, including agent doctrine readiness, interface alignment, local tests, VM smoke evidence, live read observability for `lojix "(Query (ByNode (goldragon ouranos None)))"`, and remediation. Live host state was not changed: no `meta-lojix Deploy` was submitted against `goldragon ouranos`, no service was restarted, and no live Lojix state was cleaned or rewritten.

## Findings

1. Agent deploy readiness is not green. `/home/li/primary` fails its generated-skills check with stale generated output, and the loaded/generated operating-system doctrine still documents `Home`/`System` deploy variants while current source/schema and CriomOS docs use `Host`/`UserEnvironment`.

2. Current Lojix source and schema align on `Host`/`UserEnvironment`, but live/generated doctrine and at least one VM deploy test are stale. `meta-signal-lojix/schema/lib.schema` defines `DeployRequest [(Host HostDeployment) (UserEnvironment UserEnvironmentDeployment)]`; `signal-lojix/schema/lib.schema` defines `HostComposition [CompleteHost BaseHost]`, `HostDeployAction [...]`, `UserEnvironmentAction [...]`, and `SourceRevisionPolicy [RequireImmutable ResolveAndRecord]`. The generated `.agents` and `.claude` operating-system skill files in `/home/li/primary` still describe `Home` and `System`.

3. The strongest VM deploy smoke test passes, but it proves the legacy path, not the current interface. `CriomOS-test-cluster` `lojix-deploy-smoke` uses `lojix-0.3.4`, submits `(Deploy (System (... FullOs ... Boot ...)))`, receives `(Deployed ...)`, and asserts the old rendered generation tuple shape. This is valuable proof that the old VM path can build/copy/activate/query in a contained test, but it is not proof that current `Host`/`UserEnvironment` requests, `DeployAccepted`, `SourceRevisionPolicy`, or current generation rendering work.

4. The live `GenerationUnknown (0 0)` is not a simple query-shape bug. The single-wrapped user query is accepted by the installed `lojix` client; the double-wrapped `((ByNode ...))` form is rejected by the client decoder. Other nodes and `ByEventLog` also return `QueryRejected (GenerationUnknown (0 0))`, while `ByTestRun` returns `TestRunsQueried ([] (688 688))`.

5. The live daemon is healthy enough to answer ordinary queries and has a durable state file, but the generation/event-log read planes are not readable through the current daemon. `lojix-daemon.service` is active, ordinary and owner sockets exist, `/var/lib/lojix/lojix.sema` exists, and `ByTestRun` can read a nonzero marker. Generation/event-log reads collapse to marker zero, matching source code paths that return marker zero when `Store::matching_live_generations` or `Store::event_log_in_range` errors.

6. `goldragon ouranos` is the right live node identity for this machine. `hostname` and `/etc/hostname` are `ouranos`; local configuration and generated input paths use `goldragon/ouranos`. The failure also reproduces for `goldragon zeus`, `goldragon prometheus`, and `fieldlab mercury`, so spelling is not the primary cause.

7. Source-level Lojix tests are mostly strong, but the cross-contract dependency-boundary tests fail under `--features nota-text`. The narrower frame/round-trip tests pass for `signal-lojix` and `meta-signal-lojix`; full `cargo test --features nota-text` fails in both on `nota_text_feature_is_the_only_text_projection_opt_in`.

8. `CriomOS-test-cluster` is not currently a clean evaluation surface. The worktree is dirty and `nix flake show` fails when it reaches an auto-generated `vm-alpha` check because `fixtures/horizon/alpha.json` is not present in the Git repository. Separate pure check builds also hit a fixed-output Rust channel hash mismatch.

## Evidence

Commands consulted:

- `sed -n ... /home/li/primary/.agents/skills/operating-system-operations/SKILL.md`
- `rg ... /home/li/primary/.agents/skills/operating-system-operations/SKILL.md /home/li/primary/.claude/... /git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md /git/github.com/LiGoldragon/CriomOS/README.md /git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md`
- `rg ... /git/github.com/LiGoldragon/lojix /git/github.com/LiGoldragon/signal-lojix /git/github.com/LiGoldragon/meta-signal-lojix`
- `systemctl status lojix-daemon.service --no-pager --lines=80`
- `systemctl cat lojix-daemon.service --no-pager`
- `journalctl -u lojix-daemon.service --since '2 hours ago' --no-pager -n 200`
- `lojix "(Query (ByNode (goldragon ouranos None)))"` and alternate read-only query variants
- `find /run/lojix /var/lib/lojix ... -printf ...`
- `strings -a /var/lib/lojix/lojix.sema | rg ...`
- `cargo test --features nota-text` in `signal-lojix`, `meta-signal-lojix`, and `lojix`
- `cargo test --features nota-text --test round_trip --test frame` in `signal-lojix` and `meta-signal-lojix`
- `nix build .#checks.x86_64-linux.skills .#checks.x86_64-linux.generation-requests-use-active-manifest .#checks.x86_64-linux.skill-editor-source-of-truth-guardrails .#checks.x86_64-linux.default --no-link --print-build-logs` in `skills`
- `nix build .#checks.x86_64-linux.generated-skills-current .#checks.x86_64-linux.default --no-link --print-build-logs` in `/home/li/primary`
- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.daemon-startup-rejects-nota .#checks.x86_64-linux.build --no-link --print-build-logs` in `lojix`
- `nix build .#checks.x86_64-linux.daemon-binary .#checks.x86_64-linux.fmt --no-link --print-build-logs` in `lojix`
- `nix build .#checks.x86_64-linux.lojix-deploy-smoke --dry-run` and then `timeout 1800s nix build .#checks.x86_64-linux.lojix-deploy-smoke --no-link --print-build-logs` in `CriomOS-test-cluster`

Key observed outputs:

- Live `ByNode`: `(QueryRejected (GenerationUnknown (0 0)))`.
- Double-wrapped `ByNode`: `CliRejected ... expected Selection to hold 2 root objects, found 1`.
- Live `ByTestRun`: `(TestRunsQueried ([] (688 688)))`.
- Live `ByEventLog`: `(QueryRejected (GenerationUnknown (0 0)))`.
- `lojix-daemon.service`: active, started July 4, with ordinary and owner sockets.
- `/var/lib/lojix/lojix.sema`: present; `/var/lib/lojix/generated-inputs/goldragon/ouranos/...` present.
- `skills` flake checks named above: passed.
- `/home/li/primary` `generated-skills-current`: failed with stale generated `.agents/skills/micro-components/SKILL.md`.
- `lojix` cargo and Nix checks named above: passed; ignored tests remain for slow/network daemon paths.
- `signal-lojix` and `meta-signal-lojix` full `cargo test --features nota-text`: failed dependency-boundary tests; round-trip/frame tests passed.
- `CriomOS-test-cluster` `lojix-deploy-smoke`: passed but with legacy `lojix-0.3.4`, `System FullOs Boot`, `Deployed`, and legacy generation rendering.

## Root Cause Ranking For `GenerationUnknown (0 0)`

1. Most likely: live state schema/table incompatibility in the generation and event-log tables after daemon/schema evolution. Evidence: `ByTestRun` reads the same store with marker `(688 688)`, while generation/event-log reads return marker `(0 0)` through source paths that use marker zero on store read errors. The state file contains cluster/node strings and generated inputs show prior deploy materialization, so the system is not simply unused.

2. Likely: legacy deployments were admitted/recorded under old `System`/`FullOs`/`Boot` schema, then the daemon was upgraded to a schema expecting `GenerationArtifact`, `ActivationEffect`, source revision fields, and current table layouts. Current read projection cannot decode or match those older live-generation/event-log rows.

3. Possible: no live-generation rows exist in the current table while other tables have data. This is less likely because source unit tests say an empty live set should return `Queried([])`, not `GenerationUnknown`.

4. Unlikely: wrong node or cluster identifier. `goldragon ouranos` matches the host, and the same rejection appears for other identifiers.

5. Unlikely: query-shape bug. The installed client accepts the single-wrapped form and rejects the double-wrapped form.

6. Unlikely: daemon down or socket misrouting. The daemon answers `ByTestRun` and socket/status checks are healthy.

## Validation Model

Currently proven:

- Current Lojix source builds and its main Rust/Nix checks pass.
- Current source parser/codec tests accept current schema variants.
- Current source records source revision through event/state paths in unit tests.
- A contained VM can build, copy, activate, and query a generation through the legacy Lojix path.
- Live daemon admission is not equivalent to activation proof; current doctrine is right on this principle.

Not proven:

- Agents will load the corrected operating-system deploy doctrine from a coherent generated primary surface.
- Current installed `meta-lojix`/daemon path accepts and completes `Host` or `UserEnvironment` deploys in a VM.
- Current `DeployAccepted` and `SourceRevisionPolicy` are exercised by any VM deploy smoke.
- Live `goldragon ouranos` has a queryable current generation ledger after the schema changes.
- Any live profile currentness or reboot persistence for `goldragon ouranos`.

## Remediation Plan

Read-only next commands:

- `lojix "(Query (ByTestRun (goldragon ouranos None)))"`
- `lojix "(Query (ByEventLog (0 1)))"`
- `systemctl status lojix-daemon.service --no-pager --lines=80`
- `journalctl -u lojix-daemon.service --since '24 hours ago' --no-pager | rg 'lojix|GenerationUnknown|decode|sema|store|QueryRejected'`
- In clean worktrees, rerun `nix build .#checks.x86_64-linux.generated-skills-current --no-link --print-build-logs` for `/home/li/primary` and `nix build .#checks.x86_64-linux.lojix-deploy-smoke --no-link --print-build-logs` after updating the test shape.

Low-risk state-changing follow-ups:

- Back up `/var/lib/lojix/lojix.sema`, then run a purpose-built read-only or migration-inspection tool that opens the live store with the exact installed schema and reports table decode health and row counts. This should be a tool, not ad hoc raw-state surgery.
- After backup and explicit approval, run a migration/reconciliation command that either upgrades legacy live-generation/event-log rows or intentionally archives incompatible old rows and initializes current-schema tables.

Larger design fixes:

- Update operating-system doctrine source and all generated agent surfaces to `Host`/`UserEnvironment`, `RequireImmutable`/`ResolveAndRecord`, and `DeployAccepted`.
- Fix `CriomOS-test-cluster` `lojix-deploy-smoke` to use current Lojix input and current deploy/query schema. It should assert admission separately from activation/profile/query evidence.
- Add a VM test that starts from a legacy store fixture and verifies the upgraded daemon either migrates it or reports a precise `StateSchemaMismatch`/`LedgerMigrationRequired` error instead of `GenerationUnknown (0 0)`.
- Add a non-live `lojix inspect-store` or equivalent ordinary read/debug command that reports table health without mutating state.

Recommended next action: fix the generated doctrine readiness first, then repair the VM deploy smoke to the current interface. Only after those pass should live state remediation be attempted, because right now the test surface that should prove the remediation path is itself stale.

