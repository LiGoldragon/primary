Presentation.{ «What CriomOS is» Proposal }

# What CriomOS is

Created by Fable 5.1, from two readings by Sonnet: the CriomOS, CriomOS-home, Lojix, Horizon and cluster repositories at the level of concept, and the current principles and libraries of Nix.

### Proposal 1: What CriomOS is · psyche-belief › vision/criomos.md

::: comment
The module reviewed whole: the first line replaced by a definition from first principles, three sections added, the rest standing. The code is evidence, not authority.
:::

- CriomOS is a declarative operating system: every host is built from its declaration.
+ CriomOS is a NixOS derivative: NixOS modules, evaluated by NixOS's own module system into one system, the target. NixOS has a configuration per machine, named for it, and rebuilds the machine from a file on it; CriomOS has none of that, and holds no host: a host is the target with its facts, its view of the horizon, its system, its deployment and its secrets, which enter as flake inputs and nowhere else. CriomOS knows no cluster, node or user by name; a name is data flowing through, and what a module does is decided by a capability the node declares. CriomOS-home is the same for a user's environment, in Home Manager modules; it declares and deploys nothing of the host.

```nix
+ # the one system; a host is its inputs
+ nixosConfigurations.target =
+   nixpkgs.lib.nixosSystem {
+     specialArgs = {
+       inherit horizon system deployment secrets;
+     };
+     modules = [ self.nixosModules.criomos ];
+   };
```

+ ## The cluster data, Horizon and Lojix

+ The cluster data is the owner's declaration of his cluster, in datom, in a repository of his own: its nodes, each with its machine, capabilities, network and keys, its users, domains and trust. Horizon composes it with the catalogue of generic nodes into one definition and projects it per node; CriomOS reads a node's projection and never the files, so every fact of a node or of the network lives in the cluster data and the schema it fills. Lojix is the deployment authority: the Nexus that takes a deployment request, projects the horizon for the node, evaluates the target with that node's inputs, builds it in the target's store and activates it, a host or a user's Home, keeping the generations, the roots and the record. The request names the transport, the store and the account; CriomOS names none of them.

```mermaid
+ flowchart TB
+     c["the cluster data: the owner's cluster, in datom"] --> h["Horizon: composes with the generic nodes, projects per node"]
+     h -- "the node's view, one input" --> t["CriomOS: the target"]
+     s["system, deployment, secrets: the other inputs"] --> t
+     l["Lojix: a deployment request"] -- "evaluates, builds in the target's store, activates" --> t
+     t -- "a generation of" --> n["the host, and each user's Home"]
```

+ ## How the code is written

+ A module reads a capability and names no node, user or cluster. A value a program takes is a typed option: a program's configuration is a settings option in the program's own format, rendered by Nix, and a secret is a path the program reads at run time. A fact lives once: in the cluster data when it is the cluster's, in Horizon's schema when it is a kind of node, in a module when it is how a program is set up. Evaluation is pure and complete before anything builds: nothing is imported from a derivation, read from the environment or found on a lookup path. Nix declares and does not run: activation places files and starts units, and a job is a unit's. Nix code is tested where it is written, a function by its expected value, a module by the options it yields and the errors it refuses, a system in a virtual machine, every test a check of its flake. A Rust crate lives in its own repository and enters as a derivation, its dependencies built apart from it. A library shared by CriomOS and CriomOS-home holds no cluster policy. The repositories carry no instructions to agents: what a flow needs to maintain CriomOS is a knowledge module, and what it is to believe of CriomOS is this vision.

```nix
+ # a program's configuration: typed, in its format
+ options.programs.example.settings =
+   lib.mkOption {
+     type = (pkgs.formats.toml { }).type;
+     default = { };
+   };
```

### Proposal 2: What starts a Nexus · psyche-belief › vision/nexus-v1.md

::: comment
The Nexus's architecture is independent of its starter.
:::

+ What starts a Nexus, a service manager or a hand at a shell, is the host's; the Nexus knows its place and nothing of its starter.
