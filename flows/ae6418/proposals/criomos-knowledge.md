Presentation.{ «CriomOS knowledge» }

# CriomOS knowledge

Created by Opus, for audit findings 11 and 12; every fact read at CriomOS main ef60e92, CriomOS-home main 2d8d6041, horizon-rs 0.15.0 and goldragon main.

### Proposal 1: What a user runs is the capability vector of its key · mind-belief › knowledge/criomos.md

**Comment** The sentence saying `userHomes.nix` decides by node and user names is false since finding 3; it goes, and the mechanism that replaced it stands in its place. The citation to `CriomOS/AGENTS.md` stays: its "no node-name logic" rule now holds in the modules.

  A Horizon role or capability field decides what is enabled; CriomOS holds no cluster or node name (`CriomOS/AGENTS.md`).
- `modules/nixos/userHomes.nix` still decides by node and user names; that awaits a ruling.
+ What a user runs on a node is the capability vector of that user's key for the node:
+
+ ```ethos
+ ; horizon-rs lib/ethos/horizon.ethos
+ ; AgentStack: Curriculum, Flow, the Codex servers
+ ; CodexCandidate: the codex-next candidate
+ UserCapability.[ AgentStack CodexCandidate ]
+ ; one entry per node the user is present on
+ UserPubKey.{ NodeName
+              SshPubKey
+              Keygrip
+              Vector<UserCapability> }
+ ```
+
+ ```datom
+ ; a user's keys in the cluster data, abridged
+ [ { example-node …
+     [ AgentStack CodexCandidate ] }
+   { other-node … [] } ]
+ ```
+
+ Horizon projects, for the viewpoint node, `hasPublicKey` and `capabilities` onto each entry of `horizon.users`. `modules/nixos/userHomes.nix` builds a Home only for a user with `hasPublicKey`, and turns each capability into a CriomOS-home option:
+
+ ```nix
+ # modules/nixos/userHomes.nix: each capability
+ # enables the Home part that runs it
+ criomosHome.curriculum.enable =
+   builtins.elem "AgentStack" user.capabilities;
+ criomosHome.codexNextCandidate.enable =
+   builtins.elem "CodexCandidate"
+     user.capabilities;
+ ```
+
+ A new thing a user runs on some nodes is a new `UserCapability` variant, set on the keys in the cluster data and read in `userHomes.nix` or in the Home module that runs it.
+
+ ```mermaid
+ flowchart TB
+   k["a user's key for one node"]
+   v["its capability vector"]
+   p["hasPublicKey and capabilities"]
+   h["whether the user has a Home here"]
+   o["the criomosHome options"]
+   k -- "carries" --> v
+   v -- "is projected by Horizon as" --> p
+   p -- "decide, in userHomes.nix" --> h
+   p -- "enable, in userHomes.nix" --> o
+ ```

### Proposal 2: The user environment · mind-belief › knowledge/criomos-home.md, a new file

**Comment** No module covered CriomOS-home: how its modules gate, how a Nexus version is declared, herdr, the hooks, the skills projection, the index. Citations name files and symbols, since line numbers drift. The module depends on knowledge:criomos.

+ ---
+ description: The user environment must be maintained: a user program, a Nexus version, herdr, a harness hook, the skills projection or the code index is declared, changed or asked about.
+ dependencies: [knowledge:criomos]
+ ---
+
+ The user environment is CriomOS-home, the repository named by the skill variable The user environment. CriomOS consumes it as the input `criomos-home`: its package set (`legacyPackages`, the set CriomOS builds with), `homeModules.default`, shared by every Home, and `horizonUsersByName`, which turns `horizon.users` into the `user` each module reads.
+
+ ```mermaid
+ flowchart TB
+   c["CriomOS userHomes.nix"]
+   m["homeModules.default"]
+   d["modules/home/default.nix"]
+   g["size, capabilities, behavesAs"]
+   c -- "imports, for a user keyed here" --> m
+   m -- "imports every module in" --> d
+   d -- "each module gates itself on" --> g
+ ```
+
+ Every module is imported for every user; each gates itself. The user's size gates with `sizeAtLeast user.size "<tier>"` (`lib/horizon-user.nix`, tiers Zero, Min, Medium, Large, Max): `profiles/min` modules gate on Min, `profiles/med` on Medium, `profiles/max` on Large or Max. A capability gates through an option `userHomes.nix` sets, or a default reading `user.capabilities`. A node role gates through `horizon.node.behavesAs`, `edge` for the desktop modules among them. A module's switch is an option under `criomosHome.*`, declared in the module it gates.
+
+ ## A Nexus version
+
+ A Nexus version is one module of `profiles/min`, one user unit. `flow-nexus-version.nix` is a function of `{ version, slug }` returning that module: the option `criomosHome.flow<slug>` and, when it is enabled, the unit `flow-nexus-<slug>`, its state and runtime directories `flow-<slug>`, and the clients `flow-<version>` and `flow-meta-<version>` bound to its sockets.
+
+ ```nix
+ # profiles/min/flow-0531.nix, abridged:
+ # one declared version
+ imports = [
+   (import ./flow-nexus-version.nix {
+     version = "0.53.1";
+     slug = "0531";
+   })
+ ];
+ criomosHome.flow0531.configurationDirectory =
+   ./flow-nexus-config-0531;
+ # the bare names point at one version's clients
+ home.file.".local/bin/flow".source =
+   "${cfg.clients}/bin/flow-0.53.1";
+ home.file.".local/bin/flow-meta".source =
+   "${cfg.clients}/bin/flow-meta-0.53.1";
+ ```
+
+ The package comes from the flake input `flow-<slug>`, through its `mkFlowPackage`. The unit's `ExecStartPre` runs `configure-flow-<slug>`: it sends, in order, the generated `Configure.Nexus`, `models.datom`, `thresholds.datom`, `leave-outs.datom`, the generated `Configure.SendServers`, the metaflow declaration at `declarationPath`, then the version's trailing files, each answered `Configured.Replaced` or `Configured.Unchanged`. A version's datom files are in its `configurationDirectory`. A version retired keeps its module with `enable = false`, its clients still installed. The other Nexus units are `curriculum-nexus` (`curriculum.nix`), `orchestrate-nexus` (`orchestrate.nix`) and `harness-daemon` (`harness.nix`).
+
+ ## herdr
+
+ herdr is declared in `profiles/min/herdr.nix`: the package `packages/herdr` with its patch, pinned by an assertion on its version, and `herdr/config.toml`, whose `codex_executables` lists the Flow client wrappers. The unit `herdr-server` exists when `criomosHome.herdr.server.enable` is set; an activation guard refuses while another herdr server runs.
+
+ ## The harness hooks
+
+ ```mermaid
+ flowchart TB
+   cr["codex-remote-control.nix"]
+   pr["the PermissionRequest hook on Bash"]
+   t["the workspace trust of ~/primary"]
+   h["herdr.nix"]
+   s["the SessionStart hook"]
+   cr -- "~/.claude/settings.json" --> pr
+   cr -- "~/.claude.json" --> t
+   h -- "~/.codex-next/hooks.json" --> s
+ ```
+
+ The permission hook is `owned-agents/claude-code/permission-request-hook.nix`; it logs each request to `~/.local/state/claude/permission-requests.jsonl`. The herdr merge keeps the hooks it does not own. A hook the Flow Nexus writes into a pane it launches is the Flow package's, not Home's.
+
+ ## The skills projection
+
+ ```mermaid
+ flowchart TB
+   b["the three belief repositories' main"]
+   r["context-skills-regenerate"]
+   s["one skill tree per harness"]
+   p["~/primary/.claude, .agents, .codex …"]
+   b -- "are fetched and read by" --> r
+   r -- "renders, with generate.clj" --> s
+   s -- "is synced into" --> p
+ ```
+
+ `context-skills.nix` declares it, enabled by `criomosHome.contextSkills.enable`, which follows `criomosHome.curriculum.enable`. The service runs on a path unit watching each belief repository's main and remote main refs under `~/primary/repos`, and on a two-minute timer as a fetch backstop. The script is `packages/context-skills/regenerate.sh`; it syncs with `--delete`, so a skill tree holds only what the belief repositories hold. `curriculum-nexus` resolves roles; it writes no skill tree.
+
+ ## The code index
+
+ `profiles/min/zoekt-index.nix` declares `zoekt-index.service` and its timer, every `criomosHome.zoektIndex.interval`. It walks `criomosHome.zoektIndex.root` to `depth` for repositories, fetches each one's origin, and indexes `origin/HEAD`, the published default branch; worktrees are skipped.

### Proposal 3: The cluster data, located · mind-belief › knowledge/criomos-deploy.md

**Comment** The cluster data check named `horizon-compose` and the two files but not where they live, nor where Lojix writes the four inputs. The places are setup values, so they are skill variables (Proposal 4) and the module names them.

  `horizon-compose` in the cluster's repository composes its `cluster-definition.datom` with `criomos-horizon-config/horizon-configuration.datom`; a definition that does not compose fails the build. `nix flake check` projects each node through `horizon-cli` and asserts its builder, network and capability facts. A passing check yields the proposal `P` above.
+
+ The cluster's repository is the skill variable The cluster data, and `criomos-horizon-config` is The cluster configuration. The definition is built as the cluster data's `horizon-definition` package, and `P` is its `horizon-definition.datom`:
+
+ ```sh
+ # P is <out>/horizon-definition.datom
+ nix build --no-link --print-out-paths \
+   "<The cluster data>#horizon-definition"
+ ```
+
+ A deployment writes the four inputs under `/var/lib/lojix/generated-inputs/<cluster>/<node>/<shape>/`, the shape `complete-host`, `base-host` or `user-environment`, each input in its own directory: `horizon`, `system`, `deployment`, `secrets`. A build outside Lojix of what a deployment built overrides the stub inputs with these paths, `--override-input horizon path:<dir>/horizon` and the like.

### Proposal 4: Two skill variables · primary › SKILL_VARIABLES.md

  The user environment: /git/github.com/LiGoldragon/CriomOS-home
+ The cluster data: /git/github.com/LiGoldragon/goldragon
+ The cluster configuration: /git/github.com/LiGoldragon/criomos-horizon-config
