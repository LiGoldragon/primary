Presentation.{ «A test repository per repository» Proposal }

# A test repository per repository

Created by Fable 5.1, on the living's words of 2026-11-09.

### Proposal 1: One test repository per repository · psyche-belief › vision/testing.md

::: comment
The living's design today: tests apart from the source, so a test edit recompiles no source; one test repository per repository, not one for all, so a change in one repository rebuilds its own tests and no other's. The tested code enters the test repository as built store paths, so a test build compiles the tests alone.
:::

  A repository's tests live in a test repository of their own, apart from the code they test, so a test changes on its own.

+ There is one test repository per repository, never one for all: a test repository takes the repository it tests as its one source input, so a change in one repository rebuilds its own tests and no other's. The tested repository enters as its built derivations, and a test build compiles the tests alone; a test that must see a crate's private items stays in that crate and compiles with it. The test repository is named for the repository it tests, `<repository>-tests`.

+ ```nix
+ # protos-tests/flake.nix: the tested repository is the one source input, taken built
+ inputs.protos.url = "github:LiGoldragon/protos";
+ outputs = { self, base, protos }: base.lib.testOutputs { tested = protos; cargoNix = ./Cargo.nix; };
+ ```

+ ```mermaid
+ flowchart TB
+     s["protos: the source"] -- "built once, enters as store paths" --> t["protos-tests"]
+     e["an edit to a test"] -- "rebuilds" --> t
+     e -- "rebuilds nothing of" --> s
+     o["an edit to another repository"] -- "touches" --> n["its own tests, no other's"]
+ ```
