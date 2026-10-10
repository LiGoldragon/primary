# curriculum-deploy DatomFault { problem: Shape }

Method: read curriculum-deploy source code (src/runtime.rs, src/roles.rs),
traced all `DatomProblem::Shape` error sites, ran regeneration with and
without the revert, examined primary and Curriculum commit history with jj.

## Error sites in curriculum-deploy

Three code paths in src/runtime.rs produce `DatomFault { problem: Shape }`:
- Line 90: `CurriculumRequest` realization, when the CLI argument's datom shape
  is not `DottedBraced` with head `CurriculumRequest`.
- Line 102: inner operation head is not `Generate`, `Check`, or `Visualize`.
- Line 360: `GeneratedRoleOutputs` realization in `clean_previous_roles`, when
  `skills/generated-role-outputs.datom` in the workspace does not parse as
  `GeneratedRoleOutputs.{...}`.

Additional `Shape` sites in src/roles.rs (lines 107, 112, 186) fire when
`roles.datom` has a malformed record or token shape.

## Reproduction attempts

Regeneration with the Curriculum at commit 9fe559994c (the worker's commit,
unchanged, terminology changes in place):

```
$ nix run .#generate-skills -- "CurriculumRequest.{Generate.{/git/github.com/LiGoldragon/Curriculum /home/li/primary}}"
Generated.{39 27}
```

Regeneration after reverting the terminology changes (restoring parent/child
wording):

```
$ nix run .#generate-skills -- "CurriculumRequest.{Generate.{/git/github.com/LiGoldragon/Curriculum /home/li/primary}}"
Generated.{39 27}
```

Both succeed. The DatomFault is not reproducible in either state.

## What did not change

- `roles.datom` had no changes in the Curriculum range 3872f967b29..9fe559994c.
- `skills/generated-role-outputs.datom` in primary had no changes between the
  bump commit (16c4186ae) and the current main.
- The `curriculum-deploy` flake input (f0174020675f) was not changed by the
  bump commit.

## What the worker's commit changed

Commit 9fe559994c changed only `skills/main-flow.md` and `skills/child-flow.md`.
These are skill sources read as plain Markdown by curriculum-deploy; their
descriptions and body text are not parsed as datom. No datom-shaped file
(roles.datom, generated-role-outputs.datom) was touched.

## Conclusion

The DatomFault cannot be attributed to the worker's description or terminology
changes: those files are not parsed as datom, and regeneration succeeds with
them in place. The fault was not witnessed by this flow (only relayed from the
worker). The most probable causes, given the evidence:

1. The worker passed a malformed request string to curriculum-deploy (the
   request is parsed as datom and is the first Shape check).
2. A transient nix evaluation or store state produced a stale or corrupt
   binary or input path.

Neither can be confirmed without the worker's transcript showing the exact
command and its output.
