# Synchronizer universality refactor — implementation evidence

## Task and scope

Make the `synchronizer` tool genuinely universal: only deterministic behavior
in code, everything project-varying behind typed NOTA config; the tool carries
zero project data. Externalize the criome config to a dedicated home. Build +
full tests green; extend tests for the new config surface; update
ARCHITECTURE.md with the design law and full schema.

Repos touched:
- `/git/github.com/LiGoldragon/synchronizer` (main `a8c95728` → `85bbd3d0`,
  local-only, no remote — not pushed, per the gated go-live plan).
- `/git/github.com/LiGoldragon/goldragon` (main `824ffe64` → `c1355866`,
  pushed to origin) — new `synchronizer.nota` (the criome config home).

## Hard-coded project logic found, and how it was generalized

Observed facts (grep + read of every `src/` module), each with its fix:

1. **Commit author** — `git_repository.rs` hard-coded
   `name: "synchronizer", email: "synchronizer@criome.net"` on every bump
   commit. → New `CommitAuthor { name, email }` config record (typed
   `AuthorName`/`AuthorEmail` newtypes); `GitRepository` holds it and stamps
   author + committer from it.

2. **Mainline branch** — `git_repository.rs` queried `refs/heads/main`
   literally; `BranchName::main()`/`BranchName::synchronizer()` were
   constants; the cascade redirect, resolver, and push all assumed them. →
   New `BranchScheme { mainline, staging }` config record. `remote_main_tip`
   queries the configured mainline; `push_synchronizer_branch` pushes the
   configured staging; `ResolvedTarget::reachable_branch(scheme)` and
   `VersionResolver` carry the scheme; `component_manifests::pinned_value`
   takes the mainline for the default-branch case. Removed
   `BranchName::main()`/`::synchronizer()` constructors entirely.

3. **Builder-host resolution** — `driver.rs::new` hard-wired
   `CriomosClusterDirectory` as the only builder-host path. → New
   `BuilderResolution` enum config (`DirectHost(BuilderHost)` |
   `ClusterRole(BuilderRole, ClusterSource)`). `driver.rs` adds a
   `BuilderHostResolver` trait + `ConfiguredBuilderHost` that dispatches on
   the strategy: a direct host is returned as-is; a cluster role resolves
   through `CriomosClusterDirectory` — now one optional plugin, never the only
   path, never hard-coded. `ClusterConfiguration` renamed to `ClusterSource`.

4. **Verify-gate words** — `build_verify.rs::WireCheckClassifier::workspace()`
   hard-coded `["daemon","daemons","socket","sockets","wire"]`. → New
   `VerifyPolicy` enum config (`WireExercising(Vec<WireCheckWord>)` |
   `DefaultBuild`). `WireCheckClassifier::new(words)`; `BuildVerifier` holds
   the policy and, for `DefaultBuild`, skips check enumeration entirely.

5. **Hard-coded role name in the cluster plugin** —
   `role_resolution.rs::ServiceRoleView` decode branched on the literal
   `"NixBuilder"` to read the capacity payload. → Capacity now read
   generically from the service's trailing payload wherever it decodes as an
   `Option<u32>`; no service-kind name in code.

6. **Run-scope failure label** — `driver.rs` used the literal
   `ComponentName::new("synchronizer")`. → Derives from
   `env!("CARGO_PKG_NAME")` (tool identity, deterministic).

7. **Doc comments** describing now-configurable behavior generalized
   (`cargo_manifest.rs`, `version_resolver.rs`) so they no longer imply fixed
   `main`/`synchronizer` names.

Interpretation (kept in code, with justification):
- **Forge** is a closed `enum` with a method surface (`repository_url`,
  `owner`, `flake_reference`). This IS the abstraction: all forge-shaped URL
  construction is centralized; nothing branches on GitHub outside it. A closed
  enum is the workspace-correct interface form (variant set in the type system,
  decodable from NOTA — a trait object is not). GitHub is the sole impl.
- **flake-input `original`-preservation** and the **cascade rule** stay in
  code: both are deterministic (Nix lock/declaration reconciliation; the
  ascent algorithm), not project-varying. Making them config would only let a
  consumer choose a broken behavior. Documented in ARCHITECTURE §0a.

## Full config schema (what a consumer supplies)

Root `SynchronizerConfig` (strict positional, untagged), 7 fields:

```nota
(<forge>              ; (GitHub <owner>)
 <checkout-root>      ; absolute path holding <checkout-root>/<name> clones
 [<component>]        ; (<name> AtRoot | (AtPath <abs>))
 <branch-scheme>      ; (<mainline> <staging>)  e.g. (main synchronizer)
 <builder-resolution> ; (DirectHost <host>) | (ClusterRole (<role> <cluster-source>))
 <verify-policy>      ; (WireExercising [<word>...]) | DefaultBuild
 <commit-author>)     ; (<name> <email>)
;; cluster-source: (ClusterProposal <absolute-path>)  ; horizon-rs ClusterProposal datom
```

A multi-field enum variant is a tag + one grouped payload record, e.g.
`(ClusterRole (NixBuilder (ClusterProposal /path/datom.nota)))`.

Validate a config without a live run:
`cargo run --example validate -- <config.nota>` (decode only; no git/nix/net).

## Where the criome config lives, and why

`LiGoldragon/goldragon/synchronizer.nota` (pushed). goldragon is the existing
public criome infra-DATA repo (data-only, no code/flake, jj-managed, pushed).
Justification: its `ClusterRole` strategy reads `goldragon/datom.nota`, so the
config and the cluster surface it depends on version together in one repo; a
data-only repo is the right home for a typed-NOTA config; primary `reports/`
and `beads/` deliberately avoided. Recommendation/follow-up: if the psyche
prefers a dedicated `synchronizer-config` repo later, the file moves verbatim
and only the ARCHITECTURE §3a pointer changes.

## Changed files

synchronizer/src: configuration.rs, types.rs, build_verify.rs, driver.rs,
role_resolution.rs, version_resolver.rs, component_manifests.rs,
git_repository.rs, cargo_manifest.rs. New: examples/validate.rs.
synchronizer/tests: configuration.rs, driver.rs, fixtures/mod.rs,
build_verify.rs, role_resolution.rs, git_repository.rs, topology.rs,
version_resolver.rs, nix_resolution.rs. Docs: ARCHITECTURE.md, README.md.
goldragon: synchronizer.nota (new).

## Checks run and results

- `cargo build` — ok.
- `cargo test` — 43 passed, 0 failed, 1 ignored (stateful nix probe, unchanged).
- `cargo clippy --all-targets` — 0 warnings, 0 errors.
- `cargo fmt --check` — clean.
- `cargo run --example validate -- goldragon/synchronizer.nota` —
  `ok: 4 components configured` (decode-only, no live run).
- `src/` literal sweep — remaining `main`/`synchronizer`/`LiGoldragon`/
  `NixBuilder` occurrences are all `e.g.`-style doc examples; no project
  literal drives behavior.

New witnesses added: non-criome config round-trip; generic (octocat / trunk /
bump-train / DirectHost / DefaultBuild) end-to-end ascent proving the staging
redirect uses the configured branch; `ConfiguredBuilderHost` DirectHost +
ClusterRole (real resolver via tempfile); VerifyPolicy-selects-classifier;
configurable-commit-author (git_repository witness reads the committed author).

## Blockers / unknowns / follow-up

- Go-live (create the GitHub remote, run the tool live) is a separate gated
  stage after audit — deliberately not done. synchronizer has no remote, so
  its commit is local-only (not pushed).
- Bounded extension point (not a blocker): flake.lock `is_github` /
  `github_inputs` key on the Nix source-type tag `"github"` — correct for the
  sole GitHub forge; a future non-GitHub `Forge` variant would pair with a
  sibling source-type check.
- Dual-pin limitation ([dependencies]+[dev-dependencies] same package refused
  loud) preserved unchanged, as instructed.
