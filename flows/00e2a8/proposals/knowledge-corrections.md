Presentation.{ «Knowledge modules brought to practice» }

# Knowledge modules brought to practice

Created by Opus, from an audit by Opus.

### Proposal 1: the repositories worked on now · psyche-belief › knowledge/active-projects/0.md

::: comment
No book-nexus repository or contract exists; the book builder and checker live in makeshift-tools. Only the Flow, herdr, Curriculum and Energy Nexuses have a test repository. Build-base, rust-nix-example, goldragon and the repositories CriomOS is built from, lojix, orchestrate and CriomOS-home among them, are worked on this week and run now.
:::

  - ethos-zero: the ethos generator
+ - build-base, with rust-nix-example: the Rust build base and its working instance
  - nexus: the library that defines the core of a Nexus, its shared traits among it
  - flow, with signal-flow and meta-signal-flow: the Flow Nexus, its clients and its contracts
  - herdr-nexus, belief-nexus, each with its signal- and meta-signal- contract repositories: the Nexuses of the complex, version 1
  - Curriculum, with signal-curriculum-nexus and meta-signal-curriculum-nexus: Curriculum, version 1
  - energy-nexus, with signal-energy-nexus and meta-signal-energy-nexus: the Energy Nexus
- - book-nexus, with signal-book-nexus and meta-signal-book-nexus: the book tools
- - the test repository of each Nexus above, named <nexus>-tests: its tests
+ - makeshift-tools: the book tools and the Codex usage tools
+ - flow-nexus-tests, herdr-nexus-tests, curriculum-nexus-tests, energy-nexus-tests: the tests of the Nexuses they name
  - translator: the translator herdr-nexus and belief-nexus run
  - sema: version 0
- - criomos: the hosts
+ - criomos, with the repositories it is built from: the hosts
+ - goldragon: the cluster definition
  - psyche-belief, mind-belief, field-belief: the belief modules

### Proposal 2: the Flow version · psyche-belief › knowledge/flow-messaging/0.md

::: comment
The client on PATH and the running Flow Nexus are both 0.54.7, as the module's own Cancel paragraph already says.
:::

- The `flow-nexus` on PATH is Flow 0.54.3's ordinary client and `flow-nexus-meta` its meta client. Each takes one datom argument and nothing else, and reaches the Flow Nexus at the place its configuration names: `~/.config/nexus/flow-nexus.datom` (`$XDG_CONFIG_HOME/nexus/flow-nexus.datom` when set), `{ main }`. A missing or unreadable configuration, or one naming no place, is refused naming the file (`Missing.<path>`, `Unreadable.{ <path> <reason> }`, `Invalid.{ <path> <reason> }`, exit 2), and nothing is sent.
+ The `flow-nexus` on PATH is Flow 0.54.7's ordinary client and `flow-nexus-meta` its meta client. Each takes one datom argument and nothing else, and reaches the Flow Nexus at the place its configuration names: `~/.config/nexus/flow-nexus.datom` (`$XDG_CONFIG_HOME/nexus/flow-nexus.datom` when set), `{ main }`. A missing or unreadable configuration, or one naming no place, is refused naming the file (`Missing.<path>`, `Unreadable.{ <path> <reason> }`, `Invalid.{ <path> <reason> }`, exit 2), and nothing is sent.

### Proposal 3: an excerpt the checker accepts · mind-belief › knowledge/book/0.md

::: comment
The example's excerpt is not in the book vision module, so the checker the module describes refuses it; the new excerpt is that module's own line.
:::

```text
  ::: shown
  psyche-belief › vision/book/0.md
- A book carries belief modules, as they stand and as they are proposed to change; its sources live in its reference file.
+ The publisher builds the source as it was handed and publishes the page; it authors nothing and enforces nothing, and the book is as correct as its author made it.
  :::
```

### Proposal 4: the wrapper that adds the remote flag · mind-belief › knowledge/codex-reset/0.md

::: comment
The codex on PATH is the codex-cli 0.169.0 binary itself; the wrapper that adds the remote flag is codex-remote.
:::

  `~/.codex` login. The binary must be a real codex-cli 0.161 or later run directly, since
- the `codex` wrapper on PATH adds `--remote`, which `app-server` rejects.
+ the `codex-remote` wrapper adds `--remote`, which `app-server` rejects.
  The tools try `codex` on PATH, then the newest

### Proposal 5: user homes and the capability count · mind-belief › knowledge/criomos/0.md

::: comment
The user homes module now decides by the user's key on the node and the user's capabilities, so the first sentence holds for it too. The NodeCapability enumeration in horizon-rs has 24 variants.
:::

- A Horizon role or capability field decides what is enabled; CriomOS holds no cluster or node name (`CriomOS/AGENTS.md`). `modules/nixos/userHomes.nix` still decides by node and user names; that awaits a ruling.
+ A Horizon role or capability field decides what is enabled; CriomOS holds no cluster or node name (`CriomOS/AGENTS.md`).

```ethos
  Capabilities.Vector<NodeCapability>
- ; abridged: 22 variants
+ ; abridged: 24 variants
  NodeCapability.[ Center Edge LargeAi Router
```

### Proposal 6: the nodes the cluster check projects · mind-belief › knowledge/criomos-deploy/0.md

::: comment
The cluster's flake check projects the nodes it names, two of the cluster's nodes, and asserts facts of each.
:::

- `horizon-compose` in the cluster's repository composes its `cluster-definition.datom` with `criomos-horizon-config/horizon-configuration.datom`; a definition that does not compose fails the build. `nix flake check` projects each node through `horizon-cli` and asserts its builder, network and capability facts. A passing check yields the proposal `P` above.
+ `horizon-compose` in the cluster's repository composes its `cluster-definition.datom` with `criomos-horizon-config/horizon-configuration.datom`; a definition that does not compose fails the build. `nix flake check` projects the nodes it names through `horizon-cli` and asserts their builder, network and capability facts. A passing check yields the proposal `P` above.

### Proposal 7: the repositories on build-base · mind-belief › knowledge/nix-rust-builds/0.md

::: comment
Nexus, energy-nexus and its contracts, and the Nexus test repositories pin their own nixpkgs and build with crane; Curriculum has no flake. The repositories on build-base take everything from it.
:::

- Every active repository takes nixpkgs, the Rust toolchain and the crate overrides from build-base and pins none of its own. A crate at one version and one feature set then has one store path in every repository, built once on the remote builder and served to all. A native input a crate needs is added to build-base's overrides, never in a repository.
+ Every repository built on build-base takes nixpkgs, the Rust toolchain and the crate overrides from it and pins none of its own. A crate at one version and one feature set then has one store path in every repository, built once on the remote builder and served to all. A native input a crate needs is added to build-base's overrides, never in a repository.

### Proposal 8: a module per subject and version · mind-belief › knowledge/psyche/0.md

::: comment
Several vision subjects hold a version 1 module, some beside a version 0.
:::

- Crystallized psyche is in the psyche-belief repository, in `spirit/`, `intent/` and `vision/`, one module per subject: `vision/ethos/0.md` is the skill `vision:ethos:0`.
+ Crystallized psyche is in the psyche-belief repository, in `spirit/`, `intent/` and `vision/`, one module per subject and version: `vision/ethos/0.md` is the skill `vision:ethos:0`.

### Proposal 9: when a checkout is indexed · mind-belief › knowledge/repositories/0.md

::: comment
A git hook indexes a repository when a commit or a merge lands in it; sixty checkouts under the checkout root have no index shard.
:::

- A checkout lives at `/git/<host>/<owner>/<name>`. zoekt indexes every checkout's HEAD there (knowledge:search:0).
+ A checkout lives at `/git/<host>/<owner>/<name>`. zoekt indexes a checkout's HEAD there after each commit and merge in it (knowledge:search:0).

### Proposal 10: what re-indexes a repository · mind-belief › knowledge/search/0.md

::: comment
No timer exists. The post-commit and post-merge git hook queues the repository, and a path unit starts the drain that builds and installs its index.
:::

- Code and text under /git are searched with zoekt, an indexed search whose repeated queries answer in about 0.1 s where `rg` over the same tree takes seconds: `zoekt -index_dir ~/.local/share/zoekt/index 'text'`. A query is a regular expression by default; `f:name` restricts to file names, `r:repo` to a repository, `lang:rust` to a language, `sym:name` to a symbol, `case:yes` makes it case-sensitive, and terms combine with spaces (and), `or` and `-` (not). A timer re-indexes the HEAD of every repository under /git every 15 minutes.
+ Code and text under /git are searched with zoekt, an indexed search whose repeated queries answer in about 0.1 s where `rg` over the same tree takes seconds: `zoekt -index_dir ~/.local/share/zoekt/index 'text'`. A query is a regular expression by default; `f:name` restricts to file names, `r:repo` to a repository, `lang:rust` to a language, `sym:name` to a symbol, `case:yes` makes it case-sensitive, and terms combine with spaces (and), `or` and `-` (not). A git hook re-indexes the HEAD of a repository after each commit and merge in it.
