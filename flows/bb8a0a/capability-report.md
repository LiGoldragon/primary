# Curriculum version 1: custody and generator capability

Mind curriculum Sol, flow bb8a0a, model gpt-6.1-sol. No subagents started. First stage of lgj9 only; no domain implementation or deployment.

## Custody established

The version-0 checkout `/git/github.com/LiGoldragon/Curriculum` remains clean on `main`, at `5de349e` (tracking origin/main). An isolated worktree is `/git/worktrees/curriculum-v1-bb8a0a`, on unborn branch `version-1`, containing no inherited files. Command: `git worktree add --orphan -b version-1 /git/worktrees/curriculum-v1-bb8a0a`. Git 2.56.0 supports this directly. There is no new implementation revision yet.

Every existing ref is preserved: `git for-each-ref --format='%(refname) %(objectname)' | sha256sum` returned `b5bcfc2614941525be063088ea57e67fa1a41a68cfa1ad8049149a5e90370ac0` both before and after creation. No removal, main checkout switch, commit, push or live state change occurred. Orchestrate lock 52 covered the common `.git` plus the isolated worktree during creation; report path lock 53 covers this flow directory. Existing worktrees were listed and preserved.

The approved new repositories do not yet exist locally. Proposed canonical paths: `/git/github.com/LiGoldragon/signal-curriculum-nexus`, `/git/github.com/LiGoldragon/meta-signal-curriculum-nexus`, `/git/github.com/LiGoldragon/curriculum-nexus-tests`. They need creation/clone and exact custody before writes. A separate repository approval is not yet an active-project-list amendment; please obtain the amendment for these three before maintaining them.

## Build example read

Read every tracked file of `/git/github.com/LiGoldragon/rust-nix-example`, including all 1,324 lines of generated Cargo.nix. Its root flake takes only build-base and calls `base.lib.workspaceOutputs { cargoNix = ./Cargo.nix; }`. Cargo.nix and crate-hashes.json are committed. Its separate signal workspace demonstrates the git-to-workspace patch edge. No build or evaluation was run locally.

Its flake.lock pins base `2ff4cbaa6ffcbd89d27b2f4ef5afe0bf88d1786c`, while local build-base HEAD is `d9fbbb2057f16ae2cb9c9100ee4e4cdff70d708e`. This is an observed pin difference, not proof of divergent behavior. Follow the shared current version/feature tables rather than introducing private crate versions. The new contracts also need deliberate plain/datom feature-set entries and the active repository inputs in build-base before the full checks can pass. Builder from `/etc/nix/machines`: `prometheus.goldragon.criome`.

## Generator capabilities and gaps

The ethos-zero checkout is on an older clean `kind-to-trait` branch at `f0c8bf24792f1c30626ea2571312dc10cf5d2d8c` (19.0.1). It is not the candidate generator to reuse. Inspection of committed current origin/main `3ba71350c6827dfa79d200e20057ba0f8cdbb750` and build-base-pinned `1976e45fe1edfd5676cb33919dba1ec20c785a02` (22.0.0) confirms the following. Source evidence uses `git show <rev>:<path>`; no checkout was switched.

| Capability | Observed support and consequence |
| --- | --- |
| Roots | `src/lib.rs`, File/Root: Library, Signal, Operation, Memory only. Emission is absent. An explicit reviewed compromise or generator addition is required before claiming four-part generated Ethos. |
| Signal names | `src/sectioning.rs`: generated Query and Response at the file root, rather than implied signal::Input/Output. Use explicit module exports/aliases at the boundary only if reviewed; do not invent a second schema. |
| Operation/Memory | Operation has operations/outcomes/types sections and emits Operation/Outcome; Memory has imports and stored type declarations. |
| Traits | Only Library carries trait declarations and associations. A separate runtime Library ontology can own capabilities; root modules import their names. Standard root-implied Answerable/Deliverable/Operable/Memorizable/Emittable implementations are not generated. |
| Signatures | Trait heads, bounds, supertraits, associated types/constants and receiver separators exist. Associated types or trait bounds should express inputs rather than concrete imported data disguised as a trait. Read current signature checker before settling each concrete capability. |
| Types | Scalar newtypes, named structs, enums, inline payloads and containers are supported. Do not author `Composed.Composed` in the type section: use the already-declared payload bare in a variant, and place Request references in the Signal sections. |
| Derives | `src/generation.rs`: rkyv Archive/Serialize/Deserialize, Clone/Debug/Eq/Hash; conditional Datomizable and Composing under feature datom. The generator spells Composing, not Compositional. This supports text-free runtime contracts. |
| Imports | Resolution recognizes imports declared by the current file and emits fully-qualified Rust paths; this is not evidence that external dependency Ethos namespaces are exhaustively checked on disk. Rust compilation remains necessary. |
| Generated output | `File::generate()` returns Rust source. Use OUT_DIR build generation from each crate-local ethos/ directory and include the output, preserving one authored schema. No copied hand-maintained generated Rust. |

No installed ethos-zero command was found on this seat. The above is source inspection, not an executed generator proof. A remote committed-revision generation/compile gate will be the implementation-stage proof. No generator changes are authorized by this report.

## Consumer evidence and minimal Role shape

Authored Role Markdown in mind-belief/role and field-belief/role currently shows description/dependencies/placement; the inspected descriptions carry no model/tools/caller-policy metadata. New RoleSettings therefore require an explicit authored schema and test fixtures; these fields cannot be inferred from existing descriptions.

Generated consumer evidence, read only: `.claude/agents/read-ordinary.md` lines 1–7 has name, description, model sonnet, effort high and an explicit tools sequence. `.claude/agents/general-purpose.md` lines 1–6 omits tools. `.codex/agents/explorer.toml` lines 1–4 has name, description, native model gpt-5.6-luna and model_reasoning_effort medium; developer_instructions is its composed body. These are current observations, not version-1 policy. Distinguish an absent tools constraint from an explicitly empty list. Caller policy was not found in those front matters; its vocabulary remains a design question.

Recommend RoleSetting hold a native model identifier, optional tool constraint (distinguishing unrestricted from listed tools), and an explicitly typed caller policy; effort needs an explicit decision rather than silently inheriting an old renderer default. A Subagent composition returns this setting separately from composed text, as Opus ruled.

Minimal furnishing artifact plan: relative path plus text for each generated artifact, separated from composed registry data. Flow artifacts need system and startup bundles plus harness skill trees; Subagent needs one Claude Markdown or Codex TOML role file. The exact output paths and HiddenSkill listing semantics must be chosen explicitly: current generated files alone do not define them. All writes stay under the sandbox workspace.

## Flow rehearsal boundary

Current Flow at `53782fba5e1f5b761b87f09809c0b319bcc27ad0`, `crates/flow-nexus/src/context.rs` lines 14–31 and 42–46, embeds an old Curriculum contract, sends ComposeStartup over one socket and verifies per-rendered SHA-256 provenance; it also carries predecessor records. This is a consumer contract to replace in an isolated adapter/rehearsal, not a version-1 feature to retain. Curriculum version 1 returns belief and typed Module fingerprint provenance only; Flow retains predecessor records and any rendered-envelope integrity it itself requires.

## Smallest proposed crate boundaries

Ordinary contract repository: curriculum vocabulary Library crate plus signal-curriculum-nexus Signal crate, with independent datom features. Owner repository: meta-signal-curriculum-nexus, depending on that vocabulary. Implementation repository: curriculum-nexus (resident actor, composer, Operation, Memory, source readers) and curriculum-nexus-translator (text boundary and typed furnishing execution, ordinary/meta CLI binaries). A runtime ontology Library names traits for the concrete data-bearing owners; no extra pure-composer crate is needed initially. Shared translator binary transport can be reused after revision/trait inspection, not copied wholesale.

Separate `/git/github.com/LiGoldragon/curriculum-nexus-tests` holds scenario fixtures and every acceptance test. It consumes exact published revisions, runs per-scenario sandboxes and checks the candidate binaries. The Nix gate must compile each input once through base and execute prebuilt tests.

## Current policy carried into schema review

Use the updated notion and q6jx: stable dependency-first composition, repeated module once, explicit placement wins, configured source order first-wins. Break cycles at first encounter and observe typed source-read cycle information; unread reread retains last good source and publishes unread observation. Module identity is Kind/Subject/Option<Version>; file paths are literal `<kind>/<subject>.md` or `<kind>/<subject>/<version>.md`, with no suffix inference. Fingerprint one typed Module value containing name, description, dependencies, optional RoleSetting and body, before rendering; use that same hash for provenance and change comparison.

Next event: Astra reviews these boundaries and resolves Emission support, RoleSetting/caller policy and furnishing path contracts, then supplies generated schema/trait handoff. No domain body work has begun.
