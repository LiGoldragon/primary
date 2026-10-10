# Audit: Field tool and field-clj vs vision — 38de5b subflow, 2026-09-25

Witnessed at field-clj 212cf38; D1 has since landed main 9026513c (path rule); lock 6326 was released by a676b3 after this audit's observation.

**What the Field tool is.** In the vision it is Hacky Field, the Clojure tool through which flows act on the system. The first thing the living named for it is making a change and committing it in one go: \"You could create the [Hacky] field, which is how you interact with the system. You were just doing 'make a change and then JJ commit' in one go … a simple EDN input. You're emulating datom with EDN\" (e51411 stack, 2026-09-25). It is to be the -clj prototype of a Field Nexus: Malli for the types, pseudo-traits for the kinds, compiled through Nix and later rewritten in Ethos and Rust (specialties-distillation, items 6–8). Older records give the nexus a wider job: \"call the field CLI … a signal with a traceback to its caller\" (b05237), and \"Functionality for the field means querying stuff about the system\" (b80e55).

**What exists.** No Rust Field tool exists. The Field tool is `field-clj`, at `/git/github.com/LiGoldragon/field-clj`, main 212cf38, identical to the remote. It is one operation, `commit`, in 96 lines (`src/field_clj/core.clj`). Its test suite ran once: 8 tests, 19 assertions, 0 failures. Its Nix flake check fails in the sandbox because it cannot reach Maven. CriomOS-home main 47b1d61 installs it in the Medium profile, pinned at 212cf38. It is not yet on PATH on ouranos; that activation is under lock 6326. A separate repo, `/git/github.com/LiGoldragon/field`, holds Field's read-only Node inventory scripts; its tests pass 3 of 3.

# audit-field.md

## Sources
- The psyche and flow-aspect skills; file-editing skill.
- e51411 vision: `stack.md` (Hacky Field; the -clj tools), `messaging.md` (\"a cool [Clojure] tool called Field\"), `flowAspect.md`, `nexus.md`.
- b05237 `operational-theField.md`; b80e55 `fieldNexusSystemQuery.md`; 6fb948 `fieldScriptsAndAspectRepositories.md`; c7128c `commitSubflowScript.md`; 9993b5 `orchestrateCommitBinding.md` and `autoCommitOnWrite.md`; `Vision/committing.md`.
- 38de5b reports: `specialties-distillation.md` (items 6–8 and the clj-build shape), `vocabulary-acquisition.md` (0625c3: \"Datom has named fields, but it doesn't\").
- The field-clj brief and receipt in `flows/00f95a/launches/`, and the a676b3 transcript.

## Witnessed state
- **field-clj code.**
  - `core.clj:8-12`: Malli `:catn` schema for `commit`, message and non-empty paths.
  - `core.clj:17-22`: path rules. Relative, no `..`, no duplicates.
  - `core.clj:56-63`: every listed path must appear in `jj diff --name-only`. Other dirty paths are allowed (commit 212cf38, done on e51411's order for the rule \"commit exactly the named paths, refuse only swept-in or unchanged\").
  - `core.clj:64`: runs `jj commit -m msg paths…` with the paths passed bare.
  - `core.clj:67-73`: after committing, checks `jj diff -r @- --name-only` against the listed paths.
  - `core.clj:74-89`: moves the `main` bookmark, pushes it, then compares `git ls-remote --heads origin` with the local commit.
  - Output is an EDN map with named keys.
- **Nix packaging.** `flake.nix` is a `writeShellApplication` that runs `clojure -Sdeps`, which fetches Malli from Maven at run time. Every run prints \"Use of :paths external to the project has been deprecated\".
- **Scratch run** (my scratchpad; a jj repo with a local bare remote):
  - T1 (plain path) and T2 (`sp ace.txt`) succeeded.
  - T3, run from `sub/` with the repository-relative path `sub/c.txt`, was refused as missing-paths.
  - T4, run from `sub/` with the cwd-relative path `c.txt`, succeeded. Paths are therefore relative to the working directory, not the repository.
  - `p(1).txt` was refused as commit-failed, with no stderr in the output.
  - **`all()` was read by jj as a fileset expression.** It swept `other.txt` and `p(1).txt` into a local described commit, \"all\". The after-commit check refused before the bookmark move and push, but the commit stays in local history. It is not rolled back, and the refusal does not name it.
- **clj-build** is at `/git/github.com/LiGoldragon/clj-build`. It has no commits yet: the working copy was authored 14:51–14:53 today, and `git ls-remote origin` returned nothing. Its `lib/` defines `fetchCljDeps` (a fixed-output derivation), `mkCljCli`, `mkCljUberjar` and `mkCljChecks`.
- **field repo:** README plus `bin/field-readiness.mjs`, `bin/field-aspect-status.mjs` and `bin/field-luna-research.mjs`. Its working copy holds an uncommitted `.9e735b.flow-id.lock`.

## Gaps
Each gap is one task for one Opus subagent.

1. **Commit paths are read as jj filesets, can sweep in other files, and a refused commit is left in history.**
   - *Reference:* the field-clj brief (\"commit exactly those paths … Refuse if … an exact listed path cannot be resolved as intended\"); `Vision/committing.md` (\"A commit names its files\").
   - *Now:* `core.clj:64` passes paths bare. `all()` swept every dirty file into a commit. A mismatch after committing leaves that commit behind, local and unreported.
   - *Change:* quote every path as an exact fileset, `root-file:\"<escaped>\"`. Record `jj op log -n1` before committing, and on any refusal after the commit run `jj op restore <op>`. Report the restore in the refusal.
   - *Files:* `src/field_clj/core.clj`, `test/field_clj/core_test.clj`.
   - *Acceptance:* in a real temporary jj repo, `all()` and `p(1).txt` commit only themselves. A forced after-commit mismatch leaves `jj log` unchanged from before.
2. **Paths are relative to the working directory, not the repository.**
   - *Reference:* the brief (\"repository relative paths\").
   - *Now:* scratch runs T3 and T4.
   - *Change:* resolve `jj root` and run every jj and git command with `:dir` set to it.
   - *Files:* `core.clj`, tests.
   - *Acceptance:* running from a subdirectory with `sub/c.txt` succeeds; with `c.txt` it is refused.
3. **Refusals lack the evidence the brief asks for.**
   - *Reference:* brief item 6 (\"evidence needed to distinguish path scope, local commit, bookmark, push, and remote presence\").
   - *Now:* refusals carry no commit id, jj or git stderr, or remote id. A failed push leaves local `main` already moved.
   - *Change:* every refusal carries the stage, the stderr, the local commit id if one exists, the old and new local `main`, and the remote id. On push failure, restore `main` or report the divergence.
   - *Files:* `core.clj`, tests.
   - *Acceptance:* a unit test per stage checks these keys; a push rejected in a real temporary repo reports both ids.
4. **The push is verified against `origin`, not the real remote.**
   - *Reference:* file-editing skill (\"confirm … against the real remote directly … not merely against the checkout's configured `origin`\").
   - *Now:* `core.clj:84`.
   - *Change:* read the push URL of the remote jj pushed to and run `git ls-remote <url> refs/heads/main`. Refuse if the URL is a local path or a mirror, unless `--remote-url` is given.
   - *Files:* `core.clj`, tests.
   - *Acceptance:* a test where `origin` is a local clone of the real remote is refused.
5. **Not built hermetically, check broken, no compiled deployable; clj-build unused.**
   - *Reference:* \"you can compile it for deployment … use the power of Nix … reuse your libraries for how you package your nexuses. Create some Nix libraries\" (e51411 stack); specialties-distillation §The Nix library.
   - *Now:* Malli is fetched from Maven at run time; `checks.test` fails in the sandbox (witnessed); JVM launcher; the deprecated-paths warning prints on every run.
   - *Change:* once clj-build is published, use `fetchCljDeps`, `mkCljUberjar` or `mkCljCli` (bb runtime), and `mkCljChecks`.
   - *Files:* `flake.nix`, `flake.lock`, `deps.edn`.
   - *Acceptance:* `nix flake check` passes offline, and `nix run . -- 'commit […]'` works with network off and an empty `~/.m2`.
   - *Blocked:* on clj-build being committed and pushed by whoever is authoring it.
6. **The EDN does not emulate datom.**
   - *Reference:* \"You're emulating datom with EDN, right? Your spec in [Malli]\" (e51411 stack); \"there are no named fields\" (0625c3); the tag-chain rule in specialties-distillation (38de5b's proposal, not ruled by the living).
   - *Now:* input is a bare symbol plus a vector; output is a map with named keys.
   - *Change:* input `#commit [\"msg\" [\"p\"]]`; output positional tagged variants, e.g. `#success [commit-id [paths] :main :pushed :present]` and `#refused #push […]`. Add a Malli schema for the output and validate it before printing.
   - *Files:* `core.clj`, tests, README.
   - *Acceptance:* every output passes `m/validate` against the output schema, and the old input form is rejected (or accepted for one release, if Psyche rules so).
7. **No Malli-typed pseudo-traits to rewrite from.**
   - *Reference:* \"emulate the traits … rewrite them in Ethos and in Rust from the [Malli] and the pseudo traits\" (e51411 stack); specialties-distillation item 7.
   - *Now:* one nested function, `core.clj:52-89`, with 12 levels of `if`.
   - *Change:* define protocols `Scope`, `Committer`, `Publisher` and `Verifier`, each with Malli-typed inputs and outputs; the protocol functions return `[:ok x]` or `[:refused …]`, threaded through a short-circuit pipeline; keep the injectable runner.
   - *Files:* split `src/field_clj/` into `commit.clj`, `jj.clj` and `schema.clj`.
   - *Acceptance:* the existing 8 tests pass unchanged in meaning, and each protocol has a fake-backed test.
8. **The caller is not recorded.**
   - *Reference:* \"call the field CLI, which will create a signal with a traceback to its caller\" (b05237); \"depending on who's calling it, they would know\" (c7128c).
   - *Now:* no caller identity appears in the output or the commit.
   - *Change:* read `FLOW_ID` from the environment, add a `Flow: <id>` trailer to the commit description, and put the id in the output.
   - *Files:* `core.clj`, tests.
   - *Acceptance:* in a real temporary repo, the commit description ends with the trailer.
9. **Field tool scope beyond commit (needs a Psyche ruling before work starts).**
   - *Reference:* \"Functionality for the field means querying stuff about the system\" (b80e55); b05237.
   - *Now:* commit is the only operation. Read-only inventory lives in the field repo's Node scripts.
   - *Change:* if ruled, add a read-only `observe` operation to field-clj covering Herdr panes, harness liveness and Orchestrate locks, porting `field-readiness.mjs`.
   - *Files:* new `src/field_clj/observe.clj`.
   - *Acceptance:* a fixture-backed test, with output that validates against Malli.

## Improvements
- A missing `jj` or `git`, or a shell exception, escapes as a stack trace instead of an EDN refusal.
- `parse-command` accepts two input syntaxes: `commit [\"m\" [\"p\"]]` and `commit \"m\" [\"p\"]`.
- No tests cover fileset-syntax paths, a subdirectory working directory, exceptions, or a real jj repo (all tests use a fake runner).
- JVM start-up cost on every commit; a Babashka runtime would suit it.
- field repo: the uncommitted `.9e735b.flow-id.lock` sits in a tools repo that also holds flow directories (0ad137, 9e735b).

## Repo holders
- **field-clj:** Orchestrate lock 6326 FieldCljActivationFollowup, held by a676b3 on `/git/github.com/LiGoldragon/field-clj` («Complete verified Ouranos activation for corrected field-clj»). a676b3 also told 38de5b to treat the repo as held.
- **field:** no Orchestrate lock. The working copy has Field High 9e735b's uncommitted flow-id lock file.
- **clj-build:** no Orchestrate lock. Uncommitted work by an unidentified flow, 14:51–14:53 today.
- **CriomOS-home:** locks 1019 (f7941a, codex-artifact-gateway files) and 4964 (eb7bae, a worktree). Neither covers the field-clj lines.

## Unknowns
- Whether the living's ruling on the Orchestrate commit binding (9993b5: the lock description becomes the commit message and release commits) now belongs in field-clj.
- Whether the tag-chain EDN form is ruled.
- Who is authoring clj-build.
- Whether gap 9 is wanted now.
- Whether the Field Nexus ethos is to be designed first (distillation item 6); no field ethos exists.

