Presentation.{ «CriomOS knowledge» }

# CriomOS knowledge

### Proposal 1: Everything is declared · mind-belief › knowledge/criomos.md

**Comment** *Opus 5.5, flow b2e257, ordered by Psyche core Primary; checked at origin/main of CriomOS 88dc887, CriomOS-home 6f6eec6, the cluster data dc57e80, horizon-rs ce2ccf6, criomos-horizon-config 74a4ad3, and at lojix 3fc95f0, the revision CriomOS locks.* The module opens on what you made clear today. The old opening said no node name decides what is enabled; userHomes.nix does, so rule and breach are stated apart. knowledge:nix-builds does not exist; criomos-core is a vision:criomos line, left to a vision proposal.

- dependencies: [knowledge-lojix]
+ dependencies: [knowledge:lojix]

- CriomOS is a flake that builds a whole host from a declaration. It holds no cluster or node name; a node name never decides whether a module is enabled, a Horizon role or capability field does. (`CriomOS/AGENTS.md:13-14`; the metal module reads `horizon.node.behavesAs` and `model`, `modules/nixos/metal/default.nix:33`.)
+ ```mermaid
+ flowchart TB
+   c["CriomOS"]
+   h["a host"]
+   ch["CriomOS-home"]
+   u["a user environment"]
+   n["each running Nexus"]
+   g["a generation switch"]
+   c -- "declares" --> h
+   ch -- "declares" --> u
+   ch -- "declares, one unit per version" --> n
+   h -- "reaches the machine by" --> g
+   u -- "reaches the machine by" --> g
+   n -- "reaches the machine by" --> g
+ ```
+
+ Everything that runs is declared, always: packages, units, drop-ins, timers, links. Several versions of a Nexus run side by side, each its own declared unit. A thing placed by hand is a defect, replaced by its declaration.
+
+ A Horizon role or capability field decides what is enabled; CriomOS holds no cluster or node name (`CriomOS/AGENTS.md`). `modules/nixos/userHomes.nix` still decides by node and user names; that awaits a ruling.

### Proposal 2: The cluster data, as it is typed now · mind-belief › knowledge/criomos.md

**Comment** horizon-rs now types the cluster in Ethos; `proposal.rs`, `machine.rs` and `species.rs` are gone, `Pod` is `VirtualMachine`. The Home input is bare, its revision in the lock.

  ## From declaration to host

- A cluster is declared as cluster data: nodes, users, domains and trust (`ClusterProposal`, `horizon-rs/lib/src/proposal.rs:30`). A node's `machine` has species `Metal` or `Pod` and, among other fields, an optional `model`, `chip_gen` and RAM (`horizon-rs/lib/src/machine.rs:15-40`, `species.rs:54-56`).
+ ```ethos
+ ; horizon-rs lib/ethos/horizon.ethos
+ HorizonDefinition.{ HorizonConfiguration
+                     ClusterDefinition }
+ ClusterDefinition.{ ClusterName   ; example-cluster
+                     ClusterNodes
+                     GenericNodeNames
+                     Users
+                     Domains
+                     ClusterTrust }
+ NodeDefinition.{ NodeName
+                  NodeVariant
+                  Magnitude
+                  Magnitude
+                  MachineDefinition
+                  NodeEnvironment
+                  NodeNetwork
+                  NodeKeys
+                  Option<Boolean>
+                  Capabilities   ; decides a module
+                  Option<FixedLocation> }
+ MachineDefinition.[
+    Metal.{ Architecture Hardware }
+    VirtualMachine.{ VirtualMachineHost
+                     Hardware
+                     Option<Integer> } ]
+ Capabilities.Vector<NodeCapability>
+ ; abridged: 22 variants
+ NodeCapability.[ Center Edge LargeAi Router
+                  NixBuilder.Option<Integer>
+                  NixCache TailnetController
+                  VmHost … ]
+ ```
+
+ ```datom
+ ; example-node, in a cluster definition, abridged
+ { example-node … Large Max
+   Metal.{ X86_64
+           { 12 Some.ExampleModel
+             None Some.12 Some.32 None } }
+   …
+   [ Edge.{} LowPower.{} NextGeneration.{}
+     HardwareVideo.{} … ]
+   … }
+ ```

- `horizon-rs` projects the cluster data into one view of one node. Lojix writes that view, the system tuple, the deployment shape and the secrets as generated flake inputs `horizon`, `system`, `deployment` and `secrets` (`lojix/src/bootstrap.rs:2724-2756`, `1196`). CriomOS declares them as stubs (`CriomOS/flake.nix:120-141`) and builds the output `nixosConfigurations.target` from `nixosSystem` with `specialArgs` `horizon system deployment inputs`, the `readOnlyPkgs` module, home-manager when home is included, and `nixosModules.criomos` (`flake.nix:278-300`). The `system` stub is deliberately throwing (`flake.nix:160`).
+ ```mermaid
+ flowchart TB
+   d["the cluster data"]
+   v["one node's view"]
+   i["four flake inputs"]
+   c["CriomOS"]
+   t["the host target"]
+   u["each user's Home"]
+   d -- "is projected into" --> v
+   v -- "is written by Lojix as" --> i
+   i -- "replace the stubs of" --> c
+   c -- "builds" --> t
+   c -- "builds, inside it" --> u
+ ```
+
+ The four inputs are `horizon`, `system`, `deployment` and `secrets`. The host target is `nixosConfigurations.target`; a Home is `homeConfigurations.<user>.activationPackage`, built only through CriomOS.

- CriomOS-home builds the user environment, consumed as the input `criomos-home` pinned to a revision (`flake.nix:36`).
+ CriomOS-home is the input `criomos-home`, a bare URL; CriomOS's `flake.lock` holds its revision.

### Proposal 3: Where a fix lands, cited by name · mind-belief › knowledge/criomos.md

**Comment** The line numbers, off by one since 52e55e9, become the names they pointed at.

  ## Where a fix lands

  A fix lands in the repository that owns the thing, and is deployed.

- - A kernel parameter for one machine model or role: `boot.kernelParams = lib.concatLists [...]` in `modules/nixos/metal/default.nix:509`, with `optionals behavesAs.center [...]` blocks inside it (`:533`); the whole module applies under `mkIf behavesAs.bareMetal` (`:445`).
- - A new machine model: one row in `modelFactsIndex` (`:61`). An unset or unlisted model throws at evaluation (`:116-125`).
- - A system package: `environment.systemPackages` in the module that owns it (`metal/default.nix:640`; `criome.nix:180`). A new module is added to the `imports` of `modules/nixos/criomos.nix`.
- - A unit: `systemd.services.<name>` in a module, gated by `mkIf` on a Horizon field (`metal/default.nix:551`, `569`, `582`).
+ - A kernel parameter for one machine model or role: `boot.kernelParams = lib.concatLists [...]` in `modules/nixos/metal/default.nix`, with `optionals behavesAs.center [...]` blocks inside it; the whole module applies under `mkIf behavesAs.bareMetal`.
+ - A new machine model: one row in `modelFactsIndex` in the same file. An unset or unlisted model throws at evaluation.
+ - A system package: `environment.systemPackages` in the module that owns it. A new module is added to the `imports` of `modules/nixos/criomos.nix`.
+ - A unit: `systemd.services.<name>` in a module, gated by `mkIf` on a Horizon field; a user unit: `systemd.user.services.<name>` in CriomOS-home.
- - A fact that differs per cluster: the authored cluster declaration that `horizon-rs` consumes, not necessarily the `horizon-rs` implementation repository.
- - A user program: CriomOS-home (`flake.nix:36`).
+ - A fact that differs per cluster: the cluster's own data repository, not the `horizon-rs` implementation.
+ - A user program or a Nexus version: CriomOS-home.

### Proposal 4: Lojix on a host, without its source lines · mind-belief › knowledge/criomos.md

**Comment** The source lines were lojix main's, not the deployed 8.1.0. The rollback paragraph cited a gaps file that does not exist. The query paragraph repeated knowledge:lojix.

  ## Lojix: build, deploy, ask

- Lojix evaluates the target's derivation with `nix eval --raw <flake>#<output>.drvPath` (`lojix/src/schema_runtime.rs:7742-7749`; bootstrap path `bootstrap.rs:2653-2662`) and builds it with `nix build --print-out-paths <drv>^*`, on an explicit builder when one is named (`bootstrap.rs:2666-2681`; daemon builds `schema_runtime.rs:6516`). A closure is copied to the target with `nix copy --to <store-uri>` (`schema_runtime.rs:6331-6336`).
-
- Host activation on the target, by action (`schema_runtime.rs:6807-6825`):
+ ```mermaid
+ flowchart TB
+   l["Lojix"]
+   d["the derivation"]
+   c["the closure"]
+   t["the target"]
+   a["the action"]
+   l -- "evaluates" --> d
+   d -- "is built into" --> c
+   c -- "is copied to" --> t
+   t -- "is switched by" --> a
+ ```
+
+ `nix eval`, then `nix build` on the named builder, then `nix copy --to <store-uri>`.
+
+ ```ethos
+ ; signal-lojix
+ HostDeployAction.[
+    Evaluate          ; activates nothing
+    Realize           ; builds; activates nothing
+    SetBootProfile    ; profile set; boot
+    ActivateNow       ; profile set; switch
+    TestActivation    ; test alone
+    ScheduleBootOnce ] ; boots it once
+ ```

- - `SetBootProfile`: `nix-env -p /nix/var/nix/profiles/system --set <closure>`, then `<closure>/bin/switch-to-configuration boot`.
- - `ActivateNow`: the same with `switch`.
- - `TestActivation`: `switch-to-configuration test` alone.
- - `ScheduleBootOnce`: a detached unit runs `nix-env --set`, `switch-to-configuration boot`, then `bootctl set-default <old entry>` and `bootctl set-oneshot <new entry>` (`schema_runtime.rs:6836-6852`; `bootstrap.rs:478-503`).
- - `Evaluate` and `Realize` do not activate (`schema_runtime.rs:1236-1275`).
-
- What is deployed is read with `lojix 'Query.ByNode.{ cluster node None }'`. The selector variants are `ByNode ByGeneration ByDeployment ByEventLog ByTestRun` (`signal-lojix/ethos/signal.ethos:115-117`); the answer lists the generations Lojix has recorded as live for the node, each with its slot, and the deployment records, with a state marker (`schema_runtime.rs:5096-5128`, `2592-2640`). These are Lojix's recorded deployment and generation state: they report what Lojix recorded, not a fresh attestation of what the host is running now. A flow needing a fact about a host asks Lojix this way and, where the current running system matters, checks the host itself. Deploy is `lojix-meta` `Deploy.Host`, a `HostDeployment` record (`meta-signal-lojix/ethos/signal.ethos:31`).
-
- Rollback: `GenerationSlot::Rollback` exists as a slot name (`runtime_model.rs:146`, `adapters.rs:247`); in the inspected lojix revision (`src/`, see Inspected revisions in the gaps file) no code assigns it or acts on it, and no Lojix path found there rolls a host back. The one-shot boot sets the previous boot entry as the persistent default (`schema_runtime.rs:6708-6714`, script above): the previous entry remains the persistent default for a subsequent boot; this does not prove automatic recovery or reboot after failure. The Lojix store reset (`lojix/src/reconstruction.rs:92-163`) recreates a pre-v5 Lojix store and is not a rollback. Going back to an earlier system is a new deploy of an earlier closure (unverified as a tested path).
+ Lojix has no rollback. Going back is a new deployment of an earlier CriomOS revision.

### Proposal 5: Criome and the guests, kept · mind-belief › knowledge/criomos.md

**Comment** Kept; line citations dropped.

  ## Criome

- Criome is a BLS12-381 signature authentication and attestation daemon: it holds a master key, an identity registry and delegation grants; verifies signatures; and signs attestations (`criome/ARCHITECTURE.md` TL;DR; `criome/src/master_key.rs:8`, `admission.rs:101`). It serves a working socket for clients and an owner-only meta socket (`criome/src/daemon.rs:214-270`, `CriomOS/modules/nixos/criome.nix` header). CriomOS runs it as a systemd service when `services.criome.enable` is set; the option is off by default and the module is imported for every node (`criome.nix:108`, `criomos.nix:28`). Its master key is generated on first start and kept in the daemon's state directory (`criome.nix` header).
+ Criome is a BLS12-381 signature authentication and attestation daemon: it holds a master key, an identity registry and delegation grants; verifies signatures; and signs attestations (`criome/ARCHITECTURE.md`). It serves a working socket for clients and an owner-only meta socket. CriomOS runs it as a systemd service when `services.criome.enable` is set; the option is off by default and the module is imported for every node (`modules/nixos/criome.nix`). Its master key is generated on first start and kept in the daemon's state directory.

  `criome/ARCHITECTURE.md` states that `lojix-daemon` submits a request digest to the local criome and acts after a grant. Lojix source contains no reference to criome, so this participation is a documented design, unverified in code.

  ## What CriomOS does not use

  The CriomOS guide records that hosts carry no `/etc/nixos` flake, so `microvm -l` reports empty; guests are read with `systemctl list-units 'microvm@*'` (`CriomOS/AGENTS.md:42`).

### Proposal 6: A change, from commit to generation switch · mind-belief › knowledge/criomos-deploy.md

**Comment** The module was a record of three deployments. It becomes three charts, their types, and one example whose names are plainly examples. The old module's lines are removed whole and not reproduced here, since they recorded this installation.

+ ---
+ description: A change to a host or to the user environment is made, checked and switched in through Lojix.
+ dependencies: [knowledge:lojix, knowledge:criomos, knowledge:secrets]
+ ---
+
+ ## From commit to generation switch
+
+ ```mermaid
+ flowchart TB
+   a["a commit"]
+   b["a revision"]
+   c["a CriomOS commit"]
+   d["a CriomOS revision"]
+   e["a Lojix deployment"]
+   f["a generation"]
+   a -- "is checked and pushed as" --> b
+   b -- "is pinned by the lock of" --> c
+   c -- "is pushed as" --> d
+   d -- "is named by" --> e
+   e -- "switches in" --> f
+ ```
+
+ The owning repository is CriomOS for a host, CriomOS-home for the user environment, the cluster's own repository for the cluster data. The consumer pins a producer with `nix flake update <input>`; the URL stays bare. Nothing is installed, linked, started or edited on a machine by hand.
+
+ ```datom
+ ; a Realize of the CriomOS revision R
+ ; P: the proposal, S: the secrets, R: the revision
+ ; U: example-user@example-node.example-cluster.example
+ Deploy.UserEnvironment.{
+    example-cluster example-node example-user
+    P
+    SecretsDirectory.S
+    github:example-owner/CriomOS?rev=R
+    { ssh-ng://U U }
+    Horizon
+    { homeConfigurations.example-user.activationPackage }
+    HomeManagerNixProfileV1
+    Realize            ; then ActivateNow
+    RequireImmutable
+    Some.@/etc/nix/machines
+    [] }
+ ```
+
+ `P` is the absolute `horizon-definition.datom` the cluster data check yields, `S` the cluster's secrets directory, `R` a pushed 40-hex CriomOS revision.
+
+ ## A Lojix deployment
+
+ ```mermaid
+ flowchart TB
+   r["Deploy, Realize"]
+   h["DeployAccepted"]
+   t["a terminal"]
+   a["Deploy, ActivateNow"]
+   g["a Current generation"]
+   l["the live target"]
+   r -- "is answered by" --> h
+   h -- "is queried until" --> t
+   t -- "Succeeded, permits" --> a
+   a -- "ends in" --> g
+   g -- "is checked against" --> l
+ ```
+
+ ```ethos
+ ; meta-signal-lojix: the owner's request
+ DeploySubmission.[
+    UserEnvironment.UserEnvironmentDeployment
+    Host.HostDeployment ]
+ UserEnvironmentDeployment.{
+    ClusterName
+    NodeName
+    UserName
+    ProposalSource      ; horizon-definition
+    SecretsInput
+    FlakeReference      ; CriomOS?rev=<hex>
+    DeploymentTransport ; user-scoped
+    DeploymentInputMode
+    DeploymentOutputSelector
+    ActivationBackend
+    UserEnvironmentAction
+    SourceRevisionPolicy
+    Option<NixBuilderSpec>
+    Vector<ExtraSubstituter> }
+ HostDeployment.{
+    ClusterName
+    NodeName
+    HostComposition     ; in place of the user
+    ProposalSource
+    SecretsInput
+    FlakeReference
+    DeploymentTransport ; root-scoped
+    DeploymentInputMode
+    DeploymentOutputSelector
+    ActivationBackend
+    HostDeployAction
+    SourceRevisionPolicy
+    Option<NixBuilderSpec>
+    Vector<ExtraSubstituter> }
+ ; signal-lojix: the parts
+ SecretsInput.[ NoSecrets
+                SecretsDirectory.String ]
+ DeploymentTransport.{ NixStoreUri
+                       SshDestination }
+ DeploymentInputMode.[ Horizon Direct ]
+ DeploymentOutputSelector.{ FlakeAttribute }
+ ActivationBackend.[ HomeManagerNixProfileV1
+                     NixosSystemdBootV1 ]
+ UserEnvironmentAction.[ Realize
+                         SetProfile
+                         ActivateNow ]
+ HostComposition.[ CompleteHost BaseHost ]
+ SourceRevisionPolicy.[ RequireImmutable
+                        ResolveAndRecord ]
+ ; signal-lojix: the answers
+ DeployHandle.{ DeploymentIdentifier
+                DatabaseMarker } ; admission only
+ DeploymentRecord.{
+    DeploymentIdentifier
+    GenerationIdentifier
+    DeploymentRequestIdentity
+    Option<AdmissionMarker>
+    DeploymentLifecycle
+    Option<TerminalMarker>
+    Option<DeploymentTerminal> } ; done when Some
+ DeploymentTerminal.[
+    Succeeded
+    Failed.DeploymentFailure  ; stderr only
+    Rejected.DeploymentTerminalReason ]
+ ActivationEffect.[ ProfileOnly LiveActivation
+                    BootProfile BootOnceProfile
+                    TestActivation ]
+ GenerationSlot.[ Current BootPending Recent
+                  Pinned Rollback ]
+ ```
+
+ ```datom
+ ; a Realize, then an ActivateNow, as Lojix answers
+ DeployAccepted.{ 13 { 500 500 } }
+ Queried.{ [] [ { 13 13
+    { UserEnvironment.example-user example-cluster example-node
+      UserEnvironment
+      UserEnvironment.Realize ProfileOnly
+      RequireImmutable Some.R }
+    Some.{ 500 500 } Completed
+    Some.{ 516 516 } Some.Succeeded } ] … }
+ DeployAccepted.{ 14 { 521 521 } }
+ Queried.{ [ { 14 14 example-cluster example-node
+      UserEnvironment LiveActivation Current
+      Some.G Some.R } ]
+    [ { 14 14 … UserEnvironment.ActivateNow
+      LiveActivation … Completed
+      Some.{ 554 554 } Some.Succeeded } ] … }
+ ```
+
+ `G` is the Home Manager generation's store path. `Current` is what Lojix recorded, not what runs. After an `ActivateNow` the target is read: the Home Manager profile resolving to `G`, `~/.nix-profile` holding `G`'s home-path alone, every Home file linking into `G`'s home-files, and each unit the change touched in the state it was meant to reach. `ActivateNow` sets the profile before it activates, so the profile, the links and the units are each read apart. A file or a profile package placed by hand fails the activation: a file in a declared file's place stops it at the link check, and a hand-installed package that collides with the declared home-path stops it after the old home-path has left the profile. Past the record, a diagnosis is a separately authorized command as the user; never a root shell, a hand move, a forced overwrite or an unapproved retry.
+
+ A host takes the same chart with `Deploy.Host`, the root pair `{ ssh-ng://root@<host> root@<host> }` and the output `nixosConfigurations.target.config.system.build.toplevel`; `SetBootProfile` leaves the generation `BootPending`, and the living reboots.
+
+ ## A cluster data check
+
+ ```mermaid
+ flowchart TB
+   c1["cluster-definition.datom"]
+   d["horizon-definition"]
+   c2["horizon-configuration.datom"]
+   f["nix flake check"]
+   p["the proposal path"]
+   c1 -- "is composed into" --> d
+   c2 -- "is composed into" --> d
+   d -- "is projected per node by" --> f
+   f -- "passing, yields" --> p
+ ```
+
+ `horizon-compose` in the cluster's repository composes its `cluster-definition.datom` with `criomos-horizon-config/horizon-configuration.datom`; a definition that does not compose fails the build. `nix flake check` projects each node through `horizon-cli` and asserts its builder, network and capability facts. A passing check yields the proposal `P` above.

### Proposal 7: Which Lojix answers · mind-belief › knowledge/lojix.md

**Comment** The hosts run the lojix CriomOS locks, 8.1.0, behind lojix main. The sockets are set by CriomOS.

  `lojix-nexus` owns Lojix's state and two sockets. `lojix` speaks the ordinary contract, `signal-lojix`, on `LOJIX_ORDINARY_SOCKET`, to query and watch; `lojix-meta` speaks the owner contract, `meta-signal-lojix`, on `LOJIX_OWNER_SOCKET`, to configure, deploy, pin, unpin, retire and test. Neither socket has a default path.
+ `lojix-nexus` and both clients are the lojix revision CriomOS's `flake.lock` pins; its source is read there, not at lojix main. CriomOS sets both variables for every user (`modules/nixos/lojix.nix`): `/run/lojix/ordinary.sock` and `/run/lojix/meta.sock`.

- Use `RequireImmutable` when production deployment must identify one exact source revision. Push producer revisions before pushing the consumer revision that pins them.
+ A production deployment is `RequireImmutable`, at a pushed CriomOS revision; producers are pushed before the consumer that pins them.

### Proposal 8: A topic opened, not a rule: Lojix as a Nexus · mind-belief › knowledge/lojix.md

**Comment** A topic opened, not a rule: shown in a proposal's form so it can be judged. Lojix is already `lojix-nexus` with two sockets; as a Nexus v1, its four parts in Ethos, it would gain phases pushed in place of re-queries, every nix call a typed emission keeping stdout and stderr whole, a declared unit per version with a number for every change (six lojix commits since 9.0.2 carry none), configuration through its meta socket in place of environment variables, and Criome's grant before it acts, which Criome documents and Lojix does not yet do.

+ ```mermaid
+ flowchart TB
+   l["Lojix as a Nexus v1"]
+   s["a subscriber"]
+   e["a typed Emission"]
+   v["a declared unit per version"]
+   m["its meta socket"]
+   c["Criome, an edge"]
+   l -- "pushes each phase to" --> s
+   l -- "makes each nix call" --> e
+   l -- "runs as" --> v
+   m -- "configures" --> l
+   l -- "asks a grant of" --> c
+ ```
