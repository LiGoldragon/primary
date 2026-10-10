# Aspect-owned skills migration design

## Mandate and present boundary

The living has ordered a new main workspace repository in which all vision is
migrated into `psyche-skills`, `mind-skills`, and `field-skills`, merged with
the existing skills. This is a data migration and a new canonical source
layout. It does not delete `Vision/`, `vision-raw/`, any flow lane, or the
current Curriculum repository.

The current Curriculum architecture at
`/git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md` contains independent
Markdown skill sources under `skills/` and one `roles.datom` record. The
current Primary consumer calls `curriculum-deploy` with that single skills
directory, and its generated `.agents`, `.claude`, `.codex`, and `.pi`
surfaces are evidence rather than authored input. The
[context standard](../../edf227/books/curriculum-the-context-standard.md)
supplies the intended future module identity: `(ModuleType, Name)` identifies
a module, a manifest gives its location, and role configuration chooses ordered
placements.

The reported target is a new **consumer workspace repository**, here called
`psyche-workspace` as a placeholder, plus the three aspect-owned skill
repositories. The final consumer repository name, remote, and mount location
are real implementation-owner decisions; this report does not silently choose
them. Curriculum and the original vision corpus stay readable provenance roots.

## Repository topology and supported source interface

The existing aspect repositories already exist and are intentionally empty:
`psyche-skills`, `mind-skills`, and `field-skills`. Their READMEs say their
internal layout is undecided. They are the three authored-source repositories;
the new main workspace repository is their **consumer**, alongside the existing
Curriculum input. It must not nest or duplicate those repositories.

```text
psyche-skills/                 mind-skills/                  field-skills/
  <flat *.md source directory>   <flat *.md source directory>  <flat *.md source directory>
            \                         |                         /
             \                        |                        /
              Psyche.«dir»       Mind.«dir»       Field.«dir»
                           \       |       /
                            curriculum-deploy
                                  |
             Curriculum/roles.datom + new-main-workspace/
                                  |
       generated .agents/.claude/.codex/.pi evidence surfaces
```

This is already supported by `curriculum-deploy`: its `Generate`, `Check`, and
`Visualize` requests take `CurriculumRoot`, then a vector of
`Psyche.«directory»`, `Mind.«directory»`, and `Field.«directory»`, then the
consumer workspace. It reads `roles.datom` only from Curriculum. It reads only
`*.md` files directly in each declared directory, orders the united catalog by
skill name, and refuses duplicate basenames before it writes. The first
migration must therefore choose and pass concrete flat source directories,
rather than passing repository roots by assumption or introducing a recursive
layout the runtime does not read.

The layout choice is routine once made: use one flat `skills/` directory in
each aspect repository. The new workspace pins Curriculum and the three aspect
repositories, points both Generate and Check at all three `skills/`
directories, and treats generated trees as read-only evidence. Its repository
name, remote, and mount/input location remain a real implementation-owner
choice; `psyche-workspace` below is only a placeholder label.

The existing Curriculum architecture at
`/git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md` contains independent
Markdown skill sources under `skills/` and one `roles.datom` record. The current Primary consumer calls `curriculum-deploy`
with only `Psyche.«${curriculum}/skills»`; both its Generate and Check
declarations must change together at cutover. Current launchers consume
`.agents/skills` and Claude tooling consumes `.claude/skills`, so no launcher
or native-seat test may claim the new layout until generation and Check finish.

Module type and aspect remain distinct. The existing context standard supplies
the intended module identity: `(ModuleType, Name)` identifies a module, a
manifest gives its location, and role configuration chooses ordered placements.
The filesystem source aspect declares ownership; it is not another module type.

The present generator has an additional compatibility constraint: output skill
names are global basenames, so duplicate `*.md` stems across all three source
directories refuse before writes. The future Flow registry may distinguish
`(ModuleType, Name)`, but this migration must give colliding skill files
distinct catalog names or defer one of them. It must not rely on module type to
bypass the current generator refusal.

## Statement migration and provenance

Migration works on individual statements, never on an entire source file by
assumption. Each extracted record has:

```text
statement id; owning aspect; module type; target module name; status;
source path and line range; source form (typed, STT, book comment, agent note);
verbatim source or exact excerpt location; successor or supporting references.
```

The source index is append-only. A generated skill contains compact active
instructions plus links to its statement records; it does not copy a whole
vision record merely to make a prompt. Original files remain unchanged, so a
reader can recover original wording and context.

Assign by the *fact's natural context*, not by where it was recorded:

| Aspect | Receives | Examples from current corpus |
|---|---|---|
| Psyche | purpose, intent, vision, values, and living rulings | `Vision/psyche.md`, `Vision/flowNexus.md`, `Vision/meaning.md`, typed design rulings in flow vision files |
| Mind | research conclusions, interpretation methods, design/review constraints, and test/evidence policy | distilled technical explanation, `knowledge-*`, `trial-*`, review practices |
| Field | executable operating policy, deployment, runtime, publisher, and tool instructions | deployment boundaries, `compensation-*`, `operation-*`, `operating-system` |

This table is a classifier, not permission to invent ownership. A source may
contain statements for all three aspects. For example, a Psyche ruling that
Flow is asynchronous is Psyche vision; a proposal for a registry is Mind until
implemented; the launch/deployment procedure is Field. A single sentence that
carries two independently actionable claims becomes two linked records.

Existing skills are merged the same way. A skill file is placed under the
aspect that owns its instruction, while its current name and frontmatter remain
stable when possible. `spirit`, `intent`, and `vision-*` normally belong to
Psyche; `knowledge-*` and `trial-*` normally belong to Mind; `operation-*` and
`compensation-*` normally belong to Field. Names alone are insufficient: the
ledger confirms the assignment before a module becomes active.

### Status handling

- **Active** records may feed an aspect skill and role placement.
- **Superseded** records remain in `statements/superseded/`, name their
  successor, and are excluded from generated prompts.
- **Unsettled** records remain in `statements/unsettled/` with their question
  and source; they are not rendered as instructions.
- **Archived** records retain provenance only and are excluded from all role
  composition.
- **Agent-authored context** is indexed as such and cannot be promoted to a
  living ruling merely by migration.

This follows the existing distillation rule: a statement carries what the
psyche said, while archives preserve prior words and provenance. It also avoids
turning present design alternatives into an instruction by accident.

## Cross-aspect references and generated projections

A statement can cite another aspect through a typed reference, for example
`Psyche/Vision.flow -> Mind/Knowledge.flow-nexus` or
`Mind/Trial.generated-projection -> Field/Operation.curriculum-deploy`. A
reference supplies provenance or a handoff boundary; it does **not** import the
referenced text into the caller's prompt. Cross-aspect prompt inclusion happens
only through an explicit role configuration and placement in `roles.datom`.

The provenance ledger should add a source location and a non-prompt reference
list for each module. `curriculum-deploy` already supports three declared
aspect directories, but it does not witness statement status or cross-aspect
reference semantics. Keep those in the provenance ledger and role configuration
until an explicit manifest extension is implemented. Do not fake the three
sources by manually merging generated directories.

The existing generator produces vendor skill trees and role packets from its
three-source catalog plus Curriculum `roles.datom`. The following source map
and module-selection representation are proposed additions, not current
generator behavior:

1. vendor-neutral resolved module selections and provenance receipts;
2. `.agents/skills`, `.claude/skills`, `.codex/skills`, and `.pi/skills`;
3. harness agent definitions from each role's explicit system and loadable
   selections; and
4. a generated source map from each output to module and statement records.

Generated trees remain read-only evidence. No source file is regenerated from
a harness projection.

## Bootstrap and cutover

1. **Inventory without mutation.** Enumerate current Curriculum skills,
   `Vision/`, `vision-raw/`, and `flows/*/vision/`; record every source path,
   statement boundary, form, status, and proposed aspect. Preserve input
   bytes and paths in the source index; do not delete or rewrite originals.
2. **Prepare the three aspect repositories and one consumer once.** Establish
   the new main workspace remote, default branch, and publisher authority; add
   one flat `skills/` directory to each aspect repository, then add copied
   existing skill modules and provenance-ledger records. Do not use a worktree
   or clone as a staging workaround.
3. **Classify and distill.** Populate the ledger. Mechanical source references
   may be prepared automatically, but an ambiguous active claim remains
   `Unsettled` until the owning aspect accepts its placement. Supersession
   links are explicit, never inferred only from filename or timestamp.
4. **Build the three-source deployment declaration.** Every active module has
   exactly one `(ModuleType, Name)`, one aspect-owned path, and a globally
   unique skill basename. Validate that every role selection resolves and that
   cross-aspect references resolve without changing prompt composition.
5. **Generate in the new consumer workspace.** Use the supported three-source
   declaration in both Generate and Check. Compare generated module selections,
   placement order, and source maps to the ledger; do not edit existing
   generated trees by hand.
6. **Cut over one consumer configuration.** Change the main workspace's
   Curriculum input or mount to the new repository, regenerate through the
   supported deployment command, and retain the previous Curriculum input as
   rollback. The cutover receipt reports artifact paths, source-map coverage,
   and match/mismatch, never raw identifiers.
7. **Observe then retire no source.** A successful generated-projection check
   and one configured-role launch witness prove the new input path. The old
   corpus remains available; a later explicit retention ruling is required for
   any archival or deletion operation.

## Validation

The implementation owner should demonstrate these acceptance cases before the
new repository becomes canonical:

- every inventoried source has a ledger outcome: active, superseded, unsettled,
  archived, or explicitly out of scope;
- each active statement has exactly one aspect assignment and source locator;
- a current catalog basename collision is refused before writes; any future
  `(ModuleType, Name)` registry distinction is tested separately from that
  generator constraint;
- an ambiguous statement cannot enter a generated prompt;
- every cross-aspect reference resolves but adds no prompt text unless a role
  placement explicitly selects it;
- generated skills and agent definitions come from the normalized manifest,
  retain declared selection order, and have source maps;
- an unchanged existing skill retains its instruction text after move, aside
  from path/provenance frontmatter required by the new schema;
- the cutover consumer can return a readable match/mismatch receipt and roll
  back to its prior input; and
- original `Vision/`, `vision-raw/`, and flow-lane sources remain present and
  unmodified.

## Publisher and workspace constraints

The earlier shared-Primary failure establishes a narrow rule for this work:
models do not operate JJ in a shared workspace. A single deterministic
publisher captures only authorized paths, detects changes during capture,
constructs a path-limited object commit without checkout/rebase/abandon, pushes
non-force, and reconciles a crash-after-push before advancing its private
baseline. It reports readable paths and outcomes; revisions and checksums stay
machine-held. Private paths, generated projections, and unrelated lanes are
explicit exclusions.

This rule applies to the new repository as well. It does not require a
worktree, clone, migration of the existing Primary tree, or a cross-repository
atomic publish. A cross-repository cutover is an ordered operation with a
recorded rollback boundary.

## Decisions still owed

1. The repository name, remote, and mount/input location for the new main
   workspace.
2. Whether the canonical manifest stores statement records directly or links
   to the separate provenance ledger. The proposed separation keeps prompt
   modules small and provenance durable.
3. Who accepts ambiguous aspect assignments. Routine classification can be
   prepared by deterministic inventory, but acceptance of an ambiguous living
   statement is a design judgment.
4. Whether and when to extend the ledger into a formal manifest for statement
   status and cross-aspect references. The three-aspect deployment interface is
   already supported; this is a separate data-model decision.
5. When, if ever, originals may be marked retained archive rather than merely
   preserved source. This order authorizes migration design, not deletion.

## Delivery

The requested messenger routes were previously unavailable. No repeated
message was attempted. This report is the handoff artifact for the Opus
successor.
