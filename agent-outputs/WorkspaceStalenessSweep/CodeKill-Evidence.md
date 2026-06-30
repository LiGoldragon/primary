# Code Kill Evidence

Task: code cleanup for epic `primary-5rzf`, bead `primary-5rzf.7`.

Scope: acted only on verifier ledger section `CONFIRMED FOR CODE KILL (.7)` in `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`. No suspect, rejected, Spirit intent, or private-repo item was inspected or changed.

## Coordination

- Claimed `primary-5rzf.7` with `bd update primary-5rzf.7 --claim`.
- Claimed edited shared paths with `orchestrate`.
- `/git/github.com/LiGoldragon/lojix` was already claimed by `system-designer`, so it was not edited in place.
- Created isolated lojix workspace `/git/github.com/LiGoldragon/lojix-primary-5rzf-7` from `main` with `jj workspace add --revision main --message 'primary-5rzf-7-code-kill'`.
- Filed tracking bead `primary-pg6f` for that isolated lojix worktree and final disposition.

## Items

### C1. Persona runtime still exposes `persona-mind` for `mind`

Ledger reference: `Verifier-Ledger.md`, `CONFIRMED FOR CODE KILL (.7)`, C1.

Action taken:

- Replaced Mind component lookup and projection from `persona-mind` to `mind`.
- Renamed the persona flake input and exported package/check attr from `persona-mind` to `mind`.
- Renamed the prototype launcher from `persona-mind-prototype-launcher` to `mind-prototype-launcher`.
- Updated in-repo tests and the fixture binary so the manager, component fixture, and test expectations agree on `mind`.

Files changed:

- `/git/github.com/LiGoldragon/persona/src/engine.rs`
- `/git/github.com/LiGoldragon/persona/src/bin/persona_component_fixture.rs`
- `/git/github.com/LiGoldragon/persona/flake.nix`
- `/git/github.com/LiGoldragon/persona/flake.lock`
- `/git/github.com/LiGoldragon/persona/tests/daemon.rs`
- `/git/github.com/LiGoldragon/persona/tests/direct_process.rs`
- `/git/github.com/LiGoldragon/persona/tests/engine.rs`
- `/git/github.com/LiGoldragon/persona/tests/request.rs`
- `/git/github.com/LiGoldragon/persona/tests/state.rs`
- `/git/github.com/LiGoldragon/persona/tests/supervisor.rs`

### C2. Primary workspace points at dead `persona-mind` checkout path

Ledger reference: `Verifier-Ledger.md`, `CONFIRMED FOR CODE KILL (.7)`, C2.

Action taken:

- Replaced the VS Code workspace folder name/path with `mind` and `/git/github.com/LiGoldragon/mind`.

File changed:

- `/home/li/primary/primary.code-workspace`

### C3. `lojix` README still points new work to superseded `horizon-re-engineering`

Ledger reference: `Verifier-Ledger.md`, `CONFIRMED FOR CODE KILL (.7)`, C3.

Action taken:

- In isolated worktree `/git/github.com/LiGoldragon/lojix-primary-5rzf-7`, replaced the README status sentence so new work lands on `horizon-leaner-shape`.
- The occupied `/git/github.com/LiGoldragon/lojix` checkout was not modified.

File changed:

- `/git/github.com/LiGoldragon/lojix-primary-5rzf-7/README.md`

### C4. Workspace/code-repo docs still point at `signal-persona-mind`

Ledger reference: `Verifier-Ledger.md`, `CONFIRMED FOR CODE KILL (.7)`, C4.

Action taken:

- Replaced the VS Code workspace folder name/path with `signal-mind` and `/git/github.com/LiGoldragon/signal-mind`.
- Replaced `meta-signal-router` repo-local instruction reference from `../signal-persona-mind/ARCHITECTURE.md` to `../signal-mind/ARCHITECTURE.md`.

Files changed:

- `/home/li/primary/primary.code-workspace`
- `/git/github.com/LiGoldragon/meta-signal-router/skills.md`

## Checks

- `jq empty /home/li/primary/primary.code-workspace`: passed.
- `rg -n "persona-mind|signal-persona-mind" /git/github.com/LiGoldragon/persona/src /git/github.com/LiGoldragon/persona/tests /git/github.com/LiGoldragon/persona/flake.nix /git/github.com/LiGoldragon/persona/flake.lock /home/li/primary/primary.code-workspace /git/github.com/LiGoldragon/meta-signal-router/skills.md || true`: no hits.
- `rg -n "horizon-re-engineering" README.md || true` in `/git/github.com/LiGoldragon/lojix-primary-5rzf-7`: no hits.
- `cargo fmt --check` in `/git/github.com/LiGoldragon/persona`: passed.
- `cargo test` in `/git/github.com/LiGoldragon/persona`: passed; 76 tests passed, 1 existing ignored test.
- `cargo test --test daemon constraint_persona_daemon_launches_prototype_supervised_components_through_engine_supervisor` in `/git/github.com/LiGoldragon/persona`: passed after updating the fixture identity.
- `nix eval --no-write-lock-file .#packages.x86_64-linux.mind.pname` in `/git/github.com/LiGoldragon/persona`: passed, returned `mind`.
- `nix eval --no-write-lock-file .#checks.x86_64-linux.mind.name` in `/git/github.com/LiGoldragon/persona`: passed, returned `mind-test-0.3.0`.
- `nix flake check --no-write-lock-file` in `/git/github.com/LiGoldragon/persona`: failed outside the touched `mind` rename surface while checking `packages.x86_64-linux.persona-message`; the fixed-output Rust channel file hash from the binary cache did not match the hash declared by that dependency.

## Blockers And Follow-Up

- `primary-5rzf.7` was not closed because full Nix flake check evidence is not green. The failure appears unrelated to this cleanup, but it still blocks strict bead acceptance.
- The isolated lojix worktree change needs final disposition through `primary-pg6f`: partial merge of `/git/github.com/LiGoldragon/lojix-primary-5rzf-7/README.md` or discard after another integration path.
- No private scope was needed.
- No commit or push was performed.
