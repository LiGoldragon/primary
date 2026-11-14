Presentation.{ «Nothing is built twice» Proposal }

# Nothing is built twice

Created by Fable 5.1, on the living's words of 2026-11-09 and on the evidence of Psyche core Opus; edition 2, after his comments. The Nix intent of edition 1 is landed.

### Proposal 1: The crate registry · psyche-belief › vision/nix-builds.md

::: comment
Redone for clarity. The registry is two files in build-base, generated from the lockfiles of every active repository, and a check in every repository compares its own lock and its own resolved features against them. The same crate at the same version then has one set of inputs everywhere, so it builds once and every repository takes the same store path. The excerpts below are from build-base as it stands.
:::

+ ## The crate registry

+ The system builds a crate once when every repository asks for the same crate: the same version, the same revision for one of our own, and the same features. build-base holds that agreement as the crate registry, two files at its root, generated from the lockfiles and Cargo.nix of every active repository and never written by hand.

+ `crate-versions.json` names, for every crate taken from another repository, the one version the system uses, and for a git crate the one locked revision of that version. `crate-features.json` names, for that version or revision, the features it is built with and the optional dependencies those features attach.

+ ```json
+ // crate-versions.json: one version per crate; one revision per version of our own
+ { "registry": { "anyhow": ["1.0.104"], "serde": ["1.0.229"], "tokio": ["1.53.1"] },
+   "git":      { "protos": { "0.33.0": ["c93b598"] } } }
+ ```

+ ```json
+ // crate-features.json: the one feature set, and what it attaches
+ { "serde":  { "1.0.229": { "features": ["default", "derive", "std"], "attaches": ["serde_derive"] } },
+   "protos": { "0.33.0": { "c93b598": { "features": ["default", "rkyv"], "attaches": ["rkyv"] } } } }
+ ```

+ Every active repository carries two checks in its `checks.default`: `crate-versions` compares the repository's `Cargo.lock` with the version registry and refuses a version or revision outside it; `crate-features` compares what the repository's `Cargo.nix` resolves with the feature registry and refuses a feature outside it or an attached dependency the repository lacks. A repository that departs from the registry is red until it agrees.

+ ```sh
+ # a refusal: the lock asks for a syn the registry does not hold
+ crate-versions: syn 3.0.10 in Cargo.lock; registry holds 2.0.119
+ ```

+ A crate enters or moves in one way. The flow that needs a new crate, or a newer version, changes it in its repository, regenerates both files over every active repository, commits them in build-base, and moves every active repository to that build-base in the same change; a repository whose lock the union's attached dependency reaches carries that edge in its manifest. The registry thus changes once, and every repository follows at once.

+ ```sh
+ # regenerate the registry over every active repository; never edited by hand
+ nix run github:LiGoldragon/build-base#crate-version-set -- */Cargo.lock
+ nix run github:LiGoldragon/build-base#crate-feature-set -- */Cargo.nix
+ ```

+ ```mermaid
+ flowchart TB
+     l["every active repository's Cargo.lock and Cargo.nix"] -- "generate" --> r["build-base: crate-versions.json, crate-features.json"]
+     r -- "checked by each repository's gate" --> g["crate-versions, crate-features: red on any departure"]
+     r -- "one version, one feature set" --> d["one derivation, one store path, everywhere"]
+     n["a flow needing a new crate"] -- "regenerates, commits in build-base, moves every repository" --> r
+ ```

### Proposal 2: The builder's store is the cluster's cache · psyche-belief › vision/criomos.md

::: comment
Moved from vision:nix-builds at his comment: it is a service of a CriomOS node. Landed in CriomOS already as the NixCache capability.
:::

  ## Services

  A new service lives in CriomOS.
  A service is updated by bringing it up at its latest version.

+ The remote builder serves its store as the cluster's binary cache, a capability of that node declared in the cluster data; every other host substitutes from it first, and compiles nothing the builder holds.

+ ```datom
+ ; the builder node in the cluster data; the names are an example
+ { builder OnPremise [ GitServer RemoteBuilder NixCache ] }
+ ```
