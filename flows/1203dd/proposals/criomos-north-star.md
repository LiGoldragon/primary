Presentation.{ «CriomOS, the north star» Proposal }
# CriomOS, the north star

Created by Fable 5.1, who wrote this; a Sonnet gathered the repository history and his words from the transcripts.

### Proposal 1: What CriomOS is · psyche-belief › vision/criomos.md

**Comment** Replaces the opening of "CriomOS". The first line stays; the lineage and the division between interpreter and data are added.

  CriomOS is a declarative operating system: every host is built from its declaration.
+ CriomOS is the host system of the Criome, an evolved NixOS that is its bootstrap: it is to be written in Memory and Lojix in time, and NixOS carries it until then.
+
+ The CriomOS repository is the interpreter, never the configuration: it holds what is universal to every host, and the cluster data holds everything specific, a host's name, a feature on or off, which hardware it is. The same CriomOS source builds any node of any cluster.
+
+ ```mermaid
+ flowchart TB
+   d["cluster data: hosts, users,
+     hardware, features"]
+   h["Horizon: the typed cluster,
+     one contract in Ethos"]
+   c["CriomOS: the interpreter,
+     universal to every host"]
+   n["a host"]
+   l["Lojix: the only interface"]
+   d -- "is read into" --> h
+   h -- "is the only input of" --> c
+   c -- "builds" --> n
+   l -- "projects the data and drives" --> h
+   l -- "deploys" --> n
+ ```
+
+ Nobody edits a file on a host. A thing placed by hand is a defect, replaced by its declaration and a deploy.
  A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.
  Every hotfix in place is removed and replaced by that fix.

### Proposal 2: Lojix and Horizon · psyche-belief › vision/criomos.md

**Comment** A new section after "What Nix declares".

+ ## Lojix and Horizon
+
+ Lojix is the only interface to a deployment, and its CLI takes one typed object and nothing else. Lojix is a Nexus.
+
+ The cluster data is a signal contract written in Ethos, so that any logic reads it as types. Horizon is a Nexus: the current state of the cluster is asked of it, which node is the workhorse among the answers.
+
+ The nodes every cluster can call on, a live installation image among them, are a general definition given to Lojix as an input, outside any cluster.

### Proposal 3: Versions · psyche-belief › vision/criomos.md

**Comment** A new section after "Hardware".

+ ## Versions
+
+ CriomOS pins one nixpkgs commit, and every package on every host follows from it. Moving the pin is a new major version of CriomOS, named by a tag on CriomOS itself.
+
+ Every Nexus runs as stable and next, each a declared unit; the next is tested before it is the stable. A module is tested in a virtual machine, or a sandbox written in Nix, before it is deployed through CriomOS.
+
+ Heavy builds run on the workhorse; a laptop evaluates only.

### Proposal 4: The environment · psyche-belief › vision/criomos.md

**Comment** A new section at the end.

+ ## The environment
+
+ The default environment holds the tools a host needs and nothing accumulated; what is not needed is removed.
+
+ A flow is briefed about CriomOS by belief modules; no AGENTS.md stands in a CriomOS repository.

### Proposal 5: The long horizon · psyche-belief › vision/long/criomos.md

**Comment** A new module.

+ ---
+ description: CriomOS as it is ideally to be, past NixOS.
+ dependencies: [vision-criomos]
+ ---
+
+ The parts of CriomOS that are not the Criome's are extracted into LojixOS, and CriomOS becomes a configuration on it: a thin data tree per deployment. Lojix is the answer to Nix: the Datom language in which a system is declared.
+
+ The Criome holds the authentication of a deploy: the root call that activates a host's system is the Criome's.
