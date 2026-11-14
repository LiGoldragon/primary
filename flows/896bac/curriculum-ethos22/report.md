# Task 34y2: Curriculum's contract under ethos-zero 22, with a freshness check

## Branch

- Curriculum branch `ethos22-896bac`, head `26e14b22c986537ead9b994e8044d8717167ccda`, is pushed. It is one commit on `notion-declarations` 3e38a65.
- The worktree is `/git/worktrees/Curriculum-ethos22-896bac`.
- Nothing is merged into main or deployed.
- The generator is ethos-zero 22.0.0 at rev `1976e45`, the same revision Flow pins.

## The ethos change

Only the syntax changed:

```diff
-  RolesDocument.[ Roles.Roles ]
+  RolesDocument.[ Roles ]
```

- ethos-zero 16 generated `pub enum RolesDocument { Roles(Roles) }` from the old line.
- ethos-zero 22 generates the identical enum from the new line.
- Flow's copy of the file already uses the new form.

No meaning had to change, so there is no question about the ethos itself.

## Regenerated Rust

- In the regenerated `src/generated.rs`, 35 type aliases became one-field tuple structs.
- The hand-written code and the tests now wrap and unwrap those types explicitly, as Flow's code does.

## The build check

- A new `build.rs`, modelled on flow-nexus's, regenerates the Rust from `curriculum.ethos` and fails when it differs from `src/generated.rs`.
- ethos-zero is added as a build-dependency.
- `Cargo.lock`, `Cargo.nix` and `crate-hashes.json` are regenerated.

## Gate

- nix-fast-build on prometheus, run against the committed head, exits 0. Every check passed: crate-versions, crate-features, cargo-nix, curriculum and default.
- Clippy ran with `-D warnings`.
- Two deliberately stale commits each failed with exit 1, "src/generated.rs is stale":
  - a newline appended to `src/generated.rs`;
  - a type added to the ethos without regenerating.
- Neither stale commit was pushed.

## Composition is unchanged

The full table is in `compose-compare.txt`. Every run composed 39 permaflows with 928 module positions, and every harness check passed.

| Comparison | Result |
|---|---|
| Branch binary vs base binary, same beliefs, raw replies | 39 compared, 0 differ |
| Live client asking the branch Nexus vs the live binary | 39 compared, 0 differ |
| The same, vs the release proof e3d6b3 | 38 compared, 0 differ |
| Branch client asking the live Nexus | 39 compared, 0 differ |
| rkyv Query frames, every client pairing | 39 compared, 0 differ |
| rkyv Outcome frames, every Nexus pairing | 39 compared, 0 differ |

The rkyv frames are byte-equal between the code from ethos-zero 16 and from ethos-zero 22.

### Which beliefs the runs used

- The branch could not run on the live belief revisions, and neither could its base `notion-declarations`.
  - Both refuse to start without `modules.datom`; the refusals are in `start-refusals.txt`.
  - So they ran on the belief repositories' `notion-declarations` heads. Each head is the live revision plus one commit adding only `modules.datom`.
  - The replies differ from live only in those three revision ids, and the comparisons above map them to the live ids first.
- `notion-declarations` already differed from live main in its command-line output, before this branch.
  - Its client writes a guillemet nested inside a string bare, where live escapes it as `\»`.
  - The decoded results and the wire frames are equal.
  - Flow reads the frames, not that text.
  - The cause is probably the protos and datom-codec upgrade on `notion-declarations`; I did not bisect it.

## Flow's second copy of the contract

- Flow main's `crates/flow-nexus/ethos/curriculum.ethos` differs from this branch's only in the five ModuleDeclaration types, none of which goes over the wire.
- The smallest shape is to move this branch's `curriculum.ethos` whole into the empty `signal-curriculum-nexus` repository.
  - That repository gets the ethos, the generated Rust, this `build.rs`, and a `datom` feature.
  - The new crate is added to build-base's `crate-versions.json`.
  - Curriculum and Flow both depend on it and delete their own copies.
  - In Flow, the paths change in `context.rs`, `values.rs` and two test files. The re-export at `lib.rs:14` is kept, so `starter.ethos` stays as it is.
- Flow's capsule also pins Curriculum's source, through the flake input `curriculum` and `nix/curriculum/Cargo.nix`. That is a fact held twice. A check in Flow that compares the two lock entries would make it one.

Wire effects:
- Moving the crate changes no bytes.
- If the shared crate adopts a contract-digest greeting, the wire changes. Flow and Curriculum would then have to be deployed together, and Flow 0.54.7 would no longer be served.

### Design question, for Fable

Should the shared contract hold only the types that Query and Outcome reach? Curriculum's own file formats (RolesDocument, ModuleDeclarations, CliRequest, ProjectionCandidate) would then import it. The whole-file move is the smaller step.

## Evidence

- In this directory: `compose-compare.txt`, `start-refusals.txt`, the gate log, the two `negative-stale-*.log` files, and `harness/`.
- The raw outputs are under `/tmp/896bac-*` on prometheus. `/tmp` there does not survive a reboot.
