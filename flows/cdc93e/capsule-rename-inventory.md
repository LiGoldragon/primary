# Capsule Nexus: repository rename confirmation list

Request: Psyche core Opus, tsk5. Approval source: psyche-belief e66f43e6a12b8d64411c25cb1f1eed21a2716c16. Inventory only; no repository rename, source edit, build, or live switch performed.

## GitHub repositories awaiting confirmation

All are under `LiGoldragon`. All four exist as local repositories with matching GitHub origin URLs; authenticated GitHub existence/target-name checks remain for the authorized rename step.

| Current | Requested |
| --- | --- |
| herdr-nexus | capsule-nexus |
| signal-herdr-nexus | signal-capsule-nexus |
| meta-signal-herdr-nexus | meta-signal-capsule-nexus |
| herdr-nexus-tests | capsule-nexus-tests |

## Places that pin or carry the current identity

- `herdr-nexus/Cargo.toml`: workspace git dependencies on both contract repositories. `Cargo.lock`, generated `Cargo.nix`, and `crate-hashes.json` where present carry their URLs/revisions. `crates/translator/Cargo.toml` and its separate `Cargo.lock` also carry contract URLs; these require explicit treatment, not only the workspace manifest.
- `herdr-nexus-tests/flake.nix:11-12` and `flake.lock:76-89,112`: component input and locked repository name. The input currently embeds `82c2cab` in its URL; the rename must also place that revision in the lock alone. `tests/daemon.rs` imports the old component and contract crate identities.
- `build-base/crate-versions.json` and `crate-features.json`: contract package identity/revision and feature registries. Coordinate these with Core Sol; do not independently replace the shared base.
- The four repositories' `origin` remotes name the old GitHub repositories. The component and both contracts also have old-name `cluster` remotes. Local checkout/worktree paths carry the old names; preserve foreign worktrees and history.
- `metaflow/deployment.nix:48-53` pins old-name store outputs, pair launcher, daemon and meta CLI. This repository is not on the furnished active-project list; report to its owner before maintenance. It is evidence of a deployment reference, not authorization to switch it.
- `CriomOS-home/modules/home/profiles/min/flow-nexus-config/metaflows.datom` carries the old vision module selector in historical worktrees. The canonical current working tree has no old-name match. The home consumer owner must keep authored configuration aligned without hand-editing generated skill trees.
- `psyche-belief/knowledge/active-projects/0.md` still names the old repositories; the approved vision move itself is already landed. `mind-belief/knowledge/nix-rust-builds/0.md` contains the old translator package example. These are authored-module owner updates, not generated-skill edits.

## Component identity changes accompanying the URLs

The component workspace has old names in package manifests, Rust imports, Ethos import namespaces, generated modules, executable declarations, CLI configuration/socket names, checks, proof scripts and documentation. Its `crates/translator` is distinct from the separate `translator` repository. The requested public clients are `capsule` and `capsule-meta`; the library namespace is `capsule`; the backend emission type remains `Herdr`. Raw backend executable/verbs must retain herdr identity where they denote the backend.

The separate `translator` and `flow` repositories have no literal `herdr-nexus`/`herdr_nexus` matches in the inspected working trees. Their backend integrations still require owner review for semantic consumer changes; absence of that literal is not integration proof. `CriomOS` likewise has no literal old component name in inspected worktrees.

## Candidate custody and baseline

Canonical component working tree is dirty and diverged: local `main` 0e030834a7d0755a5c5a0b57c01d352bf1273ee8. Contract local mains are 8d78cd8dcdab228c67b6d471969eecb43c6fd68b and 4d0508b1699e356ac03d44cd05e490401f5fdcf7; they lag their local origin tracking refs. Test main is 07df7cf2bf9cb6e0795ca624a7fc33ec5c77a169. None of these is asserted as a fresh GitHub head.

Preserve `candidate/events-9b2f6c` (component 12c459ba9158, ordinary contract da517ff18ca3), `candidate/backend-pair-fab3af` (component 4f6493617153), and the foreign one-revision worktrees. Event work remains unaccepted; pinned22 remains unchanged. Namespace migration must not silently adopt event implementation or relax gates.

## Scope and evidence

Indexed repository search was followed by direct tracked/current-working-tree searches across the named consumers and existing linked worktrees. Index-only stale matches are not treated as current pins. Historical flow reports and generated skill trees are evidence, not rewrite targets. No claim is made about unseen clones, GitHub-only branches, external CI settings or remote-host deployment configuration; owners and authenticated GitHub metadata checks must close those gaps before rename execution.

Raw search results and per-worktree heads are scratch at `/tmp/capsule-inventory.yvD6BS/`; the exact URL pin appendix below persists the relevant positive findings.

## Exact observed URL pins

### /git/github.com/LiGoldragon/herdr-nexus

Observed HEAD `0e030834a7d0755a5c5a0b57c01d352bf1273ee8`.

```text
/git/github.com/LiGoldragon/herdr-nexus/Cargo.lock:308:source = "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=4d0508b1699e356ac03d44cd05e490401f5fdcf7#4d0508b1699e356ac03d44cd05e490401f5fdcf7"
/git/github.com/LiGoldragon/herdr-nexus/Cargo.lock:536:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=8d78cd8dcdab228c67b6d471969eecb43c6fd68b#8d78cd8dcdab228c67b6d471969eecb43c6fd68b"
/git/github.com/LiGoldragon/herdr-nexus/Cargo.toml:10:signal-herdr-nexus = { git = "https://github.com/LiGoldragon/signal-herdr-nexus", rev = "8d78cd8dcdab228c67b6d471969eecb43c6fd68b", default-features = false }
/git/github.com/LiGoldragon/herdr-nexus/Cargo.toml:11:meta-signal-herdr-nexus = { git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus", rev = "4d0508b1699e356ac03d44cd05e490401f5fdcf7", default-features = false }
/git/github.com/LiGoldragon/herdr-nexus/crates/translator/Cargo.toml:21:git = "https://github.com/LiGoldragon/signal-herdr-nexus"
/git/github.com/LiGoldragon/herdr-nexus/crates/translator/Cargo.toml:42:git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus"
/git/github.com/LiGoldragon/herdr-nexus/crates/translator/Cargo.lock:372:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=2a6c8883bb9ce1ac9467c359bd323c3aa895d580#2a6c8883bb9ce1ac9467c359bd323c3aa895d580"
```

### /git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af

Observed HEAD `4f6493617153da1b8943d829d5ef4b72d3d3cbbb`.

```text
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/Cargo.toml:10:signal-herdr-nexus = { git = "https://github.com/LiGoldragon/signal-herdr-nexus", rev = "8d78cd8dcdab228c67b6d471969eecb43c6fd68b", default-features = false }
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/Cargo.toml:11:meta-signal-herdr-nexus = { git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus", rev = "1c85502", default-features = false }
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/Cargo.lock:305:source = "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=1c85502#1c855028eb1a6c66ee7977b82ed4dbaa76a92da4"
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/Cargo.lock:533:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=8d78cd8dcdab228c67b6d471969eecb43c6fd68b#8d78cd8dcdab228c67b6d471969eecb43c6fd68b"
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/crates/translator/Cargo.toml:21:git = "https://github.com/LiGoldragon/signal-herdr-nexus"
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/crates/translator/Cargo.toml:42:git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus"
/git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af/crates/translator/Cargo.lock:372:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=2a6c8883bb9ce1ac9467c359bd323c3aa895d580#2a6c8883bb9ce1ac9467c359bd323c3aa895d580"
```

### /git/worktrees/herdr-events-9b2f6c

Observed HEAD `12c459ba9158631ec7e766d99304e0edd42bb09f`.

```text
/git/worktrees/herdr-events-9b2f6c/Cargo.toml:10:signal-herdr-nexus = { git = "https://github.com/LiGoldragon/signal-herdr-nexus", rev = "da517ff18ca36008730f69102361184559ced343", default-features = false }
/git/worktrees/herdr-events-9b2f6c/Cargo.toml:11:meta-signal-herdr-nexus = { git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus", rev = "bf27dc2", default-features = false }
/git/worktrees/herdr-events-9b2f6c/crate-hashes.json:5:  "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=bf27dc2#0.4.1": "007jmhniy2gkh29q4m60ll9xj0rq6m5s3p0cl1nga5dsgalzix4x",
/git/worktrees/herdr-events-9b2f6c/crate-hashes.json:7:  "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=da517ff18ca36008730f69102361184559ced343#0.5.0": "04jjad8i54v040fwmpbz1rpgbcchih1r0s3dylbwwqqri3mpn1ih",
/git/worktrees/herdr-events-9b2f6c/Cargo.lock:290:source = "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=bf27dc2#bf27dc28a781b53aad553398faa27db1524651e6"
/git/worktrees/herdr-events-9b2f6c/Cargo.lock:525:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=da517ff18ca36008730f69102361184559ced343#da517ff18ca36008730f69102361184559ced343"
/git/worktrees/herdr-events-9b2f6c/Cargo.nix:1061:          url = "https://github.com/LiGoldragon/meta-signal-herdr-nexus";
/git/worktrees/herdr-events-9b2f6c/Cargo.nix:1869:          url = "https://github.com/LiGoldragon/signal-herdr-nexus";
/git/worktrees/herdr-events-9b2f6c/crates/translator/Cargo.lock:372:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=2a6c8883bb9ce1ac9467c359bd323c3aa895d580#2a6c8883bb9ce1ac9467c359bd323c3aa895d580"
/git/worktrees/herdr-events-9b2f6c/crates/translator/Cargo.toml:21:git = "https://github.com/LiGoldragon/signal-herdr-nexus"
/git/worktrees/herdr-events-9b2f6c/crates/translator/Cargo.toml:42:git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus"
```

### /tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus

Observed HEAD `30e674c2ac75da475b8ab8ee06b4a475d22db2ee`.

```text
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/Cargo.toml:10:signal-herdr-nexus = { git = "https://github.com/LiGoldragon/signal-herdr-nexus", rev = "10b9d21", default-features = false }
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/Cargo.toml:11:meta-signal-herdr-nexus = { git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus", rev = "bf27dc2", default-features = false }
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/crate-hashes.json:5:  "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=bf27dc2#0.4.1": "007jmhniy2gkh29q4m60ll9xj0rq6m5s3p0cl1nga5dsgalzix4x",
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/crate-hashes.json:7:  "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=10b9d21#0.4.0": "12fvhvyh0zaaf135pr7vm71alcyvv7fbdxp1ig5cr0r3c3nap8ck",
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/Cargo.lock:290:source = "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=bf27dc2#bf27dc28a781b53aad553398faa27db1524651e6"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/Cargo.lock:525:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=10b9d21#10b9d215097504d5c911bb491ef8a5f276a3c683"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/Cargo.nix:1061:          url = "https://github.com/LiGoldragon/meta-signal-herdr-nexus";
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/Cargo.nix:1869:          url = "https://github.com/LiGoldragon/signal-herdr-nexus";
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/crates/translator/Cargo.toml:21:git = "https://github.com/LiGoldragon/signal-herdr-nexus"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/crates/translator/Cargo.toml:42:git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/land/ws/herdr-nexus/crates/translator/Cargo.lock:372:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=2a6c8883bb9ce1ac9467c359bd323c3aa895d580#2a6c8883bb9ce1ac9467c359bd323c3aa895d580"
```

### /tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus

Observed HEAD `9b1851d08edd5e5d51eb8d272c5773fea3c294e7`.

```text
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/Cargo.toml:10:signal-herdr-nexus = { git = "https://github.com/LiGoldragon/signal-herdr-nexus", rev = "10b9d21", default-features = false }
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/Cargo.toml:11:meta-signal-herdr-nexus = { git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus", rev = "bf27dc2", default-features = false }
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/crate-hashes.json:5:  "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=bf27dc2#0.4.1": "007jmhniy2gkh29q4m60ll9xj0rq6m5s3p0cl1nga5dsgalzix4x",
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/crate-hashes.json:7:  "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=10b9d21#0.4.0": "12fvhvyh0zaaf135pr7vm71alcyvv7fbdxp1ig5cr0r3c3nap8ck",
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/Cargo.nix:1061:          url = "https://github.com/LiGoldragon/meta-signal-herdr-nexus";
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/Cargo.nix:1869:          url = "https://github.com/LiGoldragon/signal-herdr-nexus";
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/Cargo.lock:290:source = "git+https://github.com/LiGoldragon/meta-signal-herdr-nexus?rev=bf27dc2#bf27dc28a781b53aad553398faa27db1524651e6"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/Cargo.lock:525:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=10b9d21#10b9d215097504d5c911bb491ef8a5f276a3c683"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/crates/translator/Cargo.lock:372:source = "git+https://github.com/LiGoldragon/signal-herdr-nexus?rev=2a6c8883bb9ce1ac9467c359bd323c3aa895d580#2a6c8883bb9ce1ac9467c359bd323c3aa895d580"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/crates/translator/Cargo.toml:21:git = "https://github.com/LiGoldragon/signal-herdr-nexus"
/tmp/claude-1001/-home-li-primary/01493920-0d9e-5777-bcac-07b744545bcb/scratchpad/ws/herdr-nexus/crates/translator/Cargo.toml:42:git = "https://github.com/LiGoldragon/meta-signal-herdr-nexus"
```

### /git/github.com/LiGoldragon/herdr-nexus-tests

Observed HEAD `07df7cf2bf9cb6e0795ca624a7fc33ec5c77a169`.

```text
/git/github.com/LiGoldragon/herdr-nexus-tests/flake.lock:82:        "repo": "herdr-nexus",
/git/github.com/LiGoldragon/herdr-nexus-tests/flake.lock:89:        "repo": "herdr-nexus",
/git/github.com/LiGoldragon/herdr-nexus-tests/flake.nix:12:      url = "github:LiGoldragon/herdr-nexus/82c2cab";
```

