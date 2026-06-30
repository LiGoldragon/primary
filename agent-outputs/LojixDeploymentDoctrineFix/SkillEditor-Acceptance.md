# SkillEditor Acceptance — Lojix Deployment Doctrine Fix

## Task and scope

Fix the runtime/role doctrine gap for quick system-fix agents that need current Lojix/CriomOS deployment doctrine, remove stale `lojix-cli` instructions from active doctrine, reconcile generated primary surfaces, validate, commit, and push.

## Evidence consulted

- `/git/github.com/LiGoldragon/lojix/README.md`: current stack is `lojix-daemon`, `lojix`, `meta-lojix`, and `lojix-write-configuration`; `lojix-cli` is legacy.
- `/git/github.com/LiGoldragon/lojix/src/bin/lojix.rs`: ordinary client takes exactly one NOTA argument.
- `/git/github.com/LiGoldragon/lojix/src/bin/meta-lojix.rs`: privileged owner/meta client takes exactly one NOTA argument.
- `/git/github.com/LiGoldragon/lojix/src/client.rs`: sockets and argument handling; `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET` can redirect clients.
- `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema`: ordinary `Query`, `ByNode`, deployment kind, action, and generation listing shapes.
- `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema`: privileged `Deploy` request shape for `System` and `Home` deployments.
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`: `FullOs` materializes home and all firmware; `OsOnly` omits both.
- `/git/github.com/LiGoldragon/CriomOS/skills.md`: real CriomOS checks use lojix-projected inputs; push before build/switch; full Criome domains for manual reachability.
- `/git/github.com/LiGoldragon/lojix-cli/README.md`: repo is archived/read-only and replacement is `github:LiGoldragon/lojix`.

Verified command shapes with the current `lojix` binaries and invalid socket env vars so parsing succeeded without daemon mutation:

```sh
LOJIX_OWNER_SOCKET=/tmp/nonexistent-lojix.sock cargo run --quiet --features nota-text --bin meta-lojix -- '(Deploy (System (goldragon ouranos FullOs /proposal github:LiGoldragon/CriomOS Switch None [] None)))'
LOJIX_OWNER_SOCKET=/tmp/nonexistent-lojix.sock cargo run --quiet --features nota-text --bin meta-lojix -- '(Deploy (Home (goldragon ouranos li /proposal github:LiGoldragon/CriomOS Activate None [])))'
LOJIX_ORDINARY_SOCKET=/tmp/nonexistent-lojix.sock cargo run --quiet --features nota-text --bin lojix -- '(Query (ByNode (goldragon ouranos None)))'
```

Each returned only `(CliRejected [io error: No such file or directory (os error 2)])`, proving parse/CLI shape reached socket connection.

## Changed files

### `/git/github.com/LiGoldragon/skills`

- `modules/lojix-deployment/full.md` added compact runtime deployment doctrine.
- `manifests/active-outputs.nota` added `lojix-deployment` runtime skill and added it to `general-code-implementer` and `criomos-implementer` role composition.
- `manifests/module-dependencies.nota` indexed the new module.
- `manifests/skills-roster.nota` added the compatibility roster entry.
- `tests/generation.rs` updated skill counts and expected role composition.
- `skills/archive/system-operator.md` and `skills/archive/system-maintainer.md` removed stale active-sounding `lojix-cli` guidance from archived manuals.

### `/home/li/primary`

- `flake.lock` updated the `skills` input to `41d6f41f7cb5264468c65825f80efa3a0c476437`.
- Added `.agents/skills/lojix-deployment/SKILL.md`.
- Added `.claude/skills/lojix-deployment/SKILL.md`.
- Updated `.claude/agents/criomos-implementer.md`, `.codex/agents/criomos-implementer.toml`, `.pi/agents/criomos-implementer.md`.
- Updated `.claude/agents/general-code-implementer.md`, `.codex/agents/general-code-implementer.toml`, `.pi/agents/general-code-implementer.md`.

## Runtime and role surfaces

Runtime skill added: `lojix-deployment`, emitted to `.agents/skills/lojix-deployment/SKILL.md` and `.claude/skills/lojix-deployment/SKILL.md` with trigger metadata for CriomOS system/home deploys and stale `lojix-cli` avoidance.

Role packets receiving doctrine: `criomos-implementer` and `general-code-implementer` on Claude, Codex, and Pi surfaces.

## Deprecated `lojix-cli` cleanup

Active source and generated doctrine now contain `lojix-cli` only in the compact prohibition/trigger text for the new skill. Archived system-operator/system-maintainer instructions no longer carry old `lojix-cli` operational steps.

## Commits and push status

- `/git/github.com/LiGoldragon/skills`: `41d6f41f` — `skills: add lojix deployment doctrine`; pushed, `main@origin` matches `main`.
- `/home/li/primary`: `cc922230` — `skills: add lojix deployment doctrine surfaces`; pushed, `main@origin` matches `main`.

## Validation

Commands passed:

- `cargo test` in `/git/github.com/LiGoldragon/skills`: 19 generation tests passed.
- `nix flake check --print-build-logs` in `/git/github.com/LiGoldragon/skills`: all checks passed.
- `nix run .#generate-skills -- /home/li/primary`: generated new skill and role surfaces.
- `nix run .#check-skills -- /home/li/primary`: generated-output check passed.
- `nix flake check --print-build-logs` in `/home/li/primary`: generated-skills-current check passed.
- Grep for `lojix-cli` in active source/generated doctrine: only compact prohibition/trigger references remain.
- Heading uniqueness script over the new generated skill and affected Markdown role packets: no duplicate headings.

## Residual risks and follow-up

- During CLI-shape verification, I accidentally submitted one live daemon request before redirecting the owner socket: `meta-lojix '(Deploy (System (goldragon ouranos FullOs /proposal github:LiGoldragon/CriomOS Switch None [] None)))'` returned `(Deployed (25 (430 430)))`. A later ordinary query for `goldragon/ouranos` at marker `(432 432)` did not show generation 25 current, but an operator may want to inspect the Lojix daemon journal/event log for deploy id 25.
- `/home/li/primary` still has unrelated dirty files predating this work plus this acceptance output: `agent-outputs/SkillsRoleCompositionBatch/SkillEditor-Acceptance.md`, `reports/legacy-disposition/PROPOSAL-2026-06-30-guardian-strict-bar.md`, and `agent-outputs/LojixDeploymentDoctrineFix/SkillEditor-Acceptance.md`.
- No host deployment was intentionally performed for the doctrine change; it is committed and pushed in source/generated repos.

## Review findings

- no blockers in changed doctrine surfaces.
- residual-risk: live daemon request id 25 should be checked if the operator wants a clean Lojix event log.
