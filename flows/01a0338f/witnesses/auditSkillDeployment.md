# Package audit skill deployment

Method: probe immutable Curriculum and Primary commits, generated consumer equality, runtime discovery, and the consumer flake check through the independent `current_node_gates` verification subflow on 2026-08-25.

Curriculum `origin/main` contains commit `ccd1e9f00a9a3fcb8e03dd0f29c6eca2864a035b`, changing only authored `skills/nix-input-upgrade.md`. The living-approved sentence appears exactly once at line 8:

> Before advancing an external package input, verify its final provider, immutable upstream payload and hash, embedded runtimes, contract-pinned consumers, built launchers, and resident versions.

Primary `origin/main` contains consumer deployment commit `d1056645c586dd4af18b5c977739a3da69f0a99f`, changing only the Curriculum pin/lock and generated `.agents` and `.claude` copies of this skill. Both generated files byte-match the authored file at the pinned Curriculum revision. The lock records revision `ccd1e9f…` and narHash `sha256-J2z6R3Ntf3wjKMCYVbG1dK0bqXtXz/m16o7lE61w2AE=`.

Independent `nix flake check --no-build --no-write-lock-file --accept-flake-config` exited 0 and included `checks.x86_64-linux.generated-skills-current`. Runtime discovery exposes `nix-input-upgrade`. The implementation's full `nix flake check` also passed on the configured remote builder.

No version was bumped because the change is guidance/generated deployment rather than a public package, wire, or storage contract. No Codex/Claude package or node gate changed. The isolated clean Curriculum worktree was forgotten and moved recoverably to freedesktop Trash.
