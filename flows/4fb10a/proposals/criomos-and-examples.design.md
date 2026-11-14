# Design: CriomOS lines in CriomOS, and examples that name no machine of his

Author: Psyche beliefReview Fable (Fable 5.2). A worker assembles the presentation source from this file, in the in-place form, each touched module shown whole as it stands. Title: «CriomOS lines in CriomOS, and examples that name no machine of his». Kind: Proposal. Signature line: Created by Fable 5.2; Sonnet readers found the lines, and a worker assembled the page. Wording marked ADD, REMOVE, MOVE, REPLACE or COMMENT is final. Modules: /git/github.com/LiGoldragon/psyche-belief.

---

## Proposal 1: The builder's store · psyche-belief › vision/nix-builds.md, vision/criomos.md

COMMENT
His comment on the Nix book, 10 November, on the text of the builder's store: «This should probably go in Criomos.» The cache line went there; this sentence stayed behind.

MOVE, from psyche-belief › vision/nix-builds.md (the first sentence of its paragraph; the rest of the paragraph stays) to psyche-belief › vision/criomos.md, section «## Services», before the sentence «The remote builder serves its store as the cluster's binary cache», in the same paragraph:
Nix builds live in the remote builder's store.

---

## Proposal 2: X11 · psyche-belief › vision/x11.md, vision/criomos.md

COMMENT
A module of one line, on a choice of the CriomOS desktop, which the CriomOS vision names as its own subject. His words, 12 November: «I'm trying to keep the belief where it belongs as much as possible.»

MOVE, from psyche-belief › vision/x11.md to psyche-belief › vision/criomos.md, as a new last paragraph of the section «## Services»:
The CriomOS desktop runs without relying on X11. X11 stays installed as a fallback.

REMOVE, the module psyche-belief › vision/x11.md, whole, with a Destroy mark: its one line has moved.

---

## Proposal 3: A flake input names the cluster's server · psyche-belief › vision/nix-builds.md

COMMENT
The example names GitHub and his account. The Git server vision, landed after it, says every flake input names a repository on the cluster's own server, and writes the example so.

REPLACE, only the changed words marked:
was: inputs.flow.url = "github:LiGoldragon/flow";   # the repository, bare; flake.lock holds the commit
becomes: inputs.flow.url = "git+ssh://git.example.criom.net/li/flow";   # the repository, bare; flake.lock holds the commit

---

## Proposal 4: Examples with example names · psyche-belief › vision/aspects.md, vision/belief-nexus-v1.md, vision/flow-nexus.md, vision/flow-nexus-v1.md, vision/nexus-v1.md, vision/complex-v1.md

COMMENT
The vision on belief modules: «A belief module carries the mechanism, and nothing that is true of his own machines alone: no cluster name, host name, login, path or address of his.» Fifteen example lines carry his home directory or his account. One rule replaces them all; each line is shown as a REPLACE with only the changed words marked.

REPLACE, in every line of the six modules that holds it:
was: /home/li
becomes: /home/example
and:
was: LiGoldragon
becomes: example-owner

The lines, by module and line number of psyche-belief main: vision/aspects.md 14; vision/belief-nexus-v1.md 41, 43, 44, 50, 119, 122, 123; vision/flow-nexus-v1.md 76, 398; vision/flow-nexus.md 185, 336; vision/nexus-v1.md 140; vision/complex-v1.md 110, 130.
