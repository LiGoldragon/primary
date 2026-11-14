Presentation.{ «A repository on a machine is a cache» Proposal }
# A repository on a machine is a cache

Created by Fable 5.1, who wrote this; nothing else helped.

### Proposal 1: A repository on a machine is a cache · psyche-belief › vision/repositories.md

**Comment** A new module:

+ ---
+ description: A repository is fetched to a machine, read, tagged, or cleaned from it.
+ dependencies: []
+ ---
+
+ ## A repository on a machine is a cache
+
+ The source of truth is the remote. A checkout on a machine is a cache of it: fetched when a machine needs to read or change the code, kept while it is read, and removed when it has not been read for a set time. Nothing points at a checkout by path; what is pinned is pinned by remote and commit.
+
+ ```mermaid
+ flowchart TB
+   r["the remote: the source of truth"]
+   c["the checkout: a cache under /git"]
+   z["zoekt"]
+   g["removed"]
+   r -- "fetched, shallow, when a machine
+     needs to read it" --> c
+   c -- "indexed while it stands" --> z
+   c -- "unread for the set time" --> g
+   r -- "tagged or committed to without
+     a checkout" --> r
+ ```
+
+ ## A tag needs no checkout
+
+ A tag names a commit at the remote; it is created there, by the forge's API or by a push from a bare clone, and no working tree is needed for it.
+
+ ## A repin is a version of CriomOS
+
+ CriomOS pins one nixpkgs commit; every package on every host follows from it. Moving the pin is a new major version of CriomOS, named by a tag on CriomOS itself; Nix fetches the pinned commit into the store by hash and reads no checkout.
+
+ ```nix
+ # the pin: a remote and a commit, never a path
+ inputs.nixpkgs.url =
+   "github:example-owner/nixpkgs/0e251e24";
+ ```
+
+ ## A flow may make a repository
+
+ A flow is welcome to make a repository with a name of its own for a use of its own, a handover archive or a makeshift tool among them, as long as the repository is named for what it holds.
