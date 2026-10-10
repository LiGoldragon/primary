# Scout Snippet Restoration Findings

## Task and scope

Investigate the recent slash-down / power-wash cleanup of the skills corpus for useful code blocks or concrete examples that were removed and should be restored or replaced compactly. Scope was read-only except this required worker output file.

Consulted source repo surfaces and generated primary surfaces:

- `AGENTS.md` in primary and `AGENTS.md` / `skills.md` in the skills source repo.
- Recent skills source history around `f186170c` through `6b8cf0d6` via `jj log`, `jj diff --stat`, and `jj file show`.
- Generated primary runtime surfaces under `.agents/skills/*/SKILL.md` and `.claude/skills/*/SKILL.md` via `find`, `jj diff --stat`, and targeted reads.
- Current source modules under `modules/*/full.md`, with focused reads of Rust, Kameo, enum-contact, Mermaid, NOTA, Nix, testing, jj, Spirit, and repository-management skills.

No tests or generators were run.

## Observed facts

- Source repo cleanup chain inspected: `f186170c skill-editor: remove duplicated scope doctrine`, `b5c0ace6 skill-editor: prune worst-offender skill batch`, `2acbe6a skill-editor: prune response-boilerplate batch`, `9a89ec99 skill-editor: prune high-count skill batch`, `5ba32770 skill-editor: remove residual audit blockers`, `e1a40adb skills: remove retired skills from generation`, `6b8cf0d6 skills: power-wash doctrine corpus`.
- Source diff from `parents(f186170c)` to `@` reports `80 files changed, 1726 insertions(+), 15124 deletions(-)`.
- Primary generated reconcile commit `483c30ec skills: reconcile power-washed runtime surfaces` mirrors the same categories into `.agents/skills/*` and `.claude/skills/*`; its stat includes removal of generated `rust-parsers`, `subscription-lifecycle`, `workspace-vocabulary`, `autonomous-agent`, and others.
- Current active Rust-related source modules are `modules/rust-core/full.md`, `modules/rust-discipline/full.md`, `modules/rust-methods/full.md`, `modules/rust-errors/full.md`, `modules/rust-storage-and-wire/full.md`, and `modules/rust-crate-layout/full.md`. `modules/rust-parsers/full.md` is absent; generated `.agents/skills/rust-parsers/SKILL.md` is absent.
- Current `modules/rust-methods/full.md`, `modules/rust-storage-and-wire/full.md`, `modules/rust-discipline/full.md`, `modules/kameo/full.md`, `modules/enum-contact-points/full.md`, `modules/mermaid/full.md`, and `modules/testing/full.md` have no fenced code blocks.
- Current retained useful examples include `modules/rust-errors/full.md` with a compact `thiserror` enum, `modules/rust-crate-layout/full.md` with crate/test layout and doc-comment examples, `modules/typed-records-over-flags/full.md` with compact Rust examples, `modules/jj/full.md` with compact command blocks, `modules/spirit-cli/full.md` with one compact record example, `modules/nota-comments/full.md` with one compact rationale-comment example, and `modules/repository-management/full.md` with compact `ghq`/`gh` command examples.
- A script comparing fenced blocks at `parents(f186170c)` versus current found removed block counts including: `modules/rust-methods/full.md` 15 Rust blocks / 132 lines, `modules/kameo/full.md` 17 Rust blocks / 207 lines, `modules/rust-storage-and-wire/full.md` 5 blocks / 32 lines, `modules/rust-parsers/full.md` 1 Rust block / 28 lines, `modules/enum-contact-points/full.md` 9 Rust blocks / 108 lines, `modules/mermaid/full.md` 13 Mermaid blocks / 57 lines, `modules/testing/full.md` 5 blocks / 26 lines, `modules/nix-discipline/full.md` 12 command/Nix blocks / 27 lines, `modules/nota-design/full.md` 14 blocks / 66 lines, and `modules/structural-forms/full.md` 4 blocks / 14 lines.
- Deleted modules with fenced examples were `modules/autonomous-agent/full.md`, `modules/report-naming/full.md`, `modules/rust-parsers/full.md`, `modules/subscription-lifecycle/full.md`, and `modules/workspace-update-report/full.md`. Of these, `rust-parsers` had the clearest reusable compact code pattern; `subscription-lifecycle` had a useful typed-stream shape but was more domain-specific and not clearly needed as a restored skill.
- `manifests/module-dependencies.nota` currently lists `rust-core`, `rust-discipline`, `rust-methods`, `rust-errors`, `rust-storage-and-wire`, and `rust-crate-layout` with empty dependency vectors. Role packets such as generated `general-code-implementer` load `rust-core`; individual skill loads do not prove automatic loading of `rust-core`.

## Interpretations

- The cleanup correctly removed many generic manuals, local operational snippets, and large domain-specific examples, but it over-removed load-bearing examples from several programming skills where the rule is difficult to apply from prose alone.
- The highest-value restoration is not to bring back entire old sections. Use replacement examples: one or two small wrong/right or minimal-shape snippets per affected skill, especially in Rust and Kameo.
- Rust has duplicate abstract rule surfaces now: `rust-core` summarizes the same rules repeated in `rust-discipline`, while `rust-methods` / `rust-storage-and-wire` / `rust-errors` / `rust-crate-layout` split examples and detail. A compact `rust-core` plus one dependent Rust implementation-pattern skill would likely be safer than six active Rust skills, provided loading is explicit.
- Relying on dependency/core loading is only safe for role packets that already include `rust-core`. It is not safe for a user or model manually loading `rust-methods` unless the generator starts composing skill dependencies or the active output manifest changes.

## Findings and recommendations

| Severity | Skill / source path | Removed useful snippet category | Judgment | Proposed compact example shape |
|---|---|---|---|---|
| high | `modules/rust-methods/full.md` | Method-on-type examples: free parser to associated constructor, zero-sized method holder, domain newtype, string-prefix routing replaced by enum, one request object in / typed object out. Evidence: old blocks at lines 20-28, 106-122, 232-239, 313-338, 411-430; current has no fences. | Replace, do not restore the 15-block section. Current prose is too abstract for this central rule. | Add 1-2 tiny Rust snippets: (1) wrong free `parse_cert` vs `impl Cert { from_pem(...) }`; (2) wrong string-prefix route vs `enum Id { Message(MessageId), Delivery(DeliveryId) }` and a `match`. |
| high | `modules/rust-parsers/full.md` deleted | Hand-rolled JSON slicing vs real parser. Evidence: old deleted block lines 13-42; current `rust-core` and `rust-discipline` only say use a real parser. | Keep deleted as separate skill; replace with one compact example in a Rust dependent skill or `rust-core` if that is the only always-loaded Rust surface. | A 6-10 line wrong/right: wrong `text.find("PrivateKey")`; right `serde_json::from_slice::<ExternalKey>(bytes)?` then convert into `KeyMaterial`. Avoid the old long extraction example. |
| high | `modules/rust-storage-and-wire/full.md` | `rkyv::to_bytes`, length-prefix frame, and validate-on-read examples; also redb table example. Evidence: old blocks lines 30-60; current has no fences. | Replace with one compact encode/decode frame example. Do not restore old sema-engine/component-specific dependency example. | One 8-12 line snippet: archive request, write length + bytes, read buffer, `rkyv::access::<ArchivedRequest, _>(&buffer)?`, then use archived typed fields. |
| medium-high | `modules/kameo/full.md` | Minimal `Self`-is-actor implementation and typed `Message` handler; delegated reply and supervision examples. Evidence: old core block lines 27-68; current has no fences. | Replace with one minimal actor/message block. Do not restore module map, feature notes, or full supervision manual. | A compact `struct Worker { state }`, `impl Actor for Worker { type Args = Self; ... }`, `struct DoWork`, `impl Message<DoWork> for Worker { type Reply = Result<..., Error>; ... }`. |
| medium | `modules/enum-contact-points/full.md` | Cross-product match examples and trait shapes. Evidence: old `Reaches` block lines 54-74 and tuple-match examples around lines 202-216; current is all prose. | Replace with one small nested/tuple match. Trait templates are optional and probably too much. | A 6-10 line `match (state, operation)` showing valid/rejected variant pairs, preferably with no wildcard that hides new variants. |
| medium | `modules/mermaid/full.md` | Strict-renderer-safe diagram examples. Evidence: old had 13 Mermaid blocks; current has detailed syntax prose but no diagram block. | Replace with one tiny canonical diagram. Syntax skills benefit from a concrete valid block. | One 4-node `flowchart LR` using ASCII ids, quoted labels, and pipe edge labels. No local identifiers or citations. |
| medium-low | `modules/nota-design/full.md` and `modules/structural-forms/full.md` | Positional record / variant / structural-form examples. Evidence: old `nota-design` had 14 small syntax blocks; `structural-forms` had 4. Current `nota-schema-docs` retains one NOTA schema-doc example, but design/form rules are mostly abstract. | Consider one compact example only if editors are misapplying positional records. Do not duplicate `nota-schema-docs` or restore grammar manual blocks. | Tiny NOTA pair: one positional record and one variant-carrying record, with prose saying field order is interface. |
| medium-low | `modules/testing/full.md` | Typed observer and per-plane chain examples. Evidence: old had Rust and text blocks around schema-derived tests; current has no fences. | Do not restore old domain-heavy schema triad examples wholesale. Add a compact example only if test reviews keep accepting stringly observers or shortcut witnesses. | A short pseudo-flow block or 6-line typed assertion showing `Vec<Event>` instead of `Vec<String>`, without local project type names. |
| low | `modules/abstractions/full.md` | QueryParser and schema-emitted noun examples. Evidence: old had two Rust blocks; current no fences. | Do not add separately if `rust-methods` gets compact examples; otherwise one method-on-parser example would help. | Reuse the Rust-methods constructor/parser shape, not a second divergent example. |
| low | `modules/naming/full.md` | Namespace/redundant-prefix Rust examples. Evidence: old had five Rust blocks; current retains offender table and rules. | No immediate restoration. The table is compact and enough; add code only if agents keep prefixing crate/domain names. | If needed, one 4-line wrong/right showing `crate::Request` not `CrateRequest`. |
| low | `modules/nix-discipline/full.md` | Override-input and build command blocks. Evidence: old had 12 command/Nix blocks; current no fences. | No immediate restoration. Many old examples were too environment-specific. If adding, keep generic and avoid host/config details. | A generic `nix flake check` / `--override-input <input> <remote-ref>` shape only if reviewers need exact command form. |
| low / no restore | `modules/repository-management/full.md`, `modules/library/full.md`, `modules/reporting/full.md`, `modules/workspace-update-report/full.md`, `modules/report-naming/full.md`, `modules/autonomous-agent/full.md`, `modules/spirit-cli/full.md` | Local paths, report templates, workflow boilerplate, long CLI examples, or host-specific commands. | Do not restore. Current compact command examples in `jj`, `spirit-cli`, and `repository-management` are sufficient where needed. | None. |
| low / maybe delete or fold | `modules/rust-discipline/full.md` | Old only lost a naming example and cargo-sweep commands; current duplicates `rust-core` heavily. | Strong candidate to remove/fold during Rust agglomeration rather than add examples. | If retained, no code block; let `rust-core` summarize and the dependent Rust patterns skill carry examples. |
| no issue | `modules/rust-errors/full.md` | The compact `thiserror` enum survived. | Keep the example. If Rust skills are agglomerated, move this exact compact shape into the dependent Rust skill and delete the standalone skill. | No replacement needed. |
| no issue | `modules/rust-crate-layout/full.md` | Layout and doc-comment examples survived. | Keep or fold during Rust agglomeration. It is not a slash-down casualty. | If folding, retain one tree block for tests/layout and one doc-comment example only if length budget permits. |
| no issue | `modules/typed-records-over-flags/full.md`, `modules/nota-comments/full.md`, `modules/jj/full.md`, `modules/spirit-cli/full.md` | Compact examples remain. | No restoration needed. | None. |

## Rust agglomeration notes

Recommended shape if the Rust cleanup is implemented later:

1. Keep `rust-core` as the small always-loaded role dependency. It should state the rules, not carry every example.
2. Create or designate one dependent Rust implementation-pattern skill that carries the load-bearing examples from `rust-methods`, parser discipline, `rust-errors`, storage/wire, and Kameo. Keep it short: method-on-type, real parser, typed error enum, typed wire encode/decode, and Kameo actor/message shape.
3. Retire or fold `rust-discipline` because it duplicates `rust-core` and currently adds little concrete value.
4. Keep `rust-parsers` deleted as an independent skill; its useful content is one example, not a whole skill.
5. Decide whether `rust-crate-layout` remains task-specific or folds into the dependent skill. It still has useful compact examples, so do not delete its content without migrating the layout examples.
6. Do not repeat all `rust-core` rules in the dependent skill. Rely on `rust-core` for broad rules and use examples to disambiguate non-obvious cases.
7. Make loading explicit. Current manifest dependency vectors for Rust skills are empty, so a practical assumption is: role packets load `rust-core`; on-demand Rust examples require explicitly loading the dependent Rust skill, or the generator/manifest must be changed to compose that dependency.

## Checks run

- `pwd && ls && find .. -maxdepth 2 -name AGENTS.md -print` — identified primary workspace surfaces.
- `jj status --no-pager` in primary — observed pre-existing working-copy additions under `agent-outputs/*` before this scout output.
- `find skills -maxdepth 3 -type f`, `rg` over primary excluding private scopes — located generated skill context and source repo pointer.
- In skills source repo: `jj status --no-pager`, `jj log`, `jj diff --stat`, `jj file list`, `jj file show`, `rg`, `wc -l`, and targeted `read` calls.
- In primary: `find .agents .claude .codex .pi -maxdepth 3 -type f`, `jj log`, and `jj diff --stat -r 483c30ec`.

Result: inspection succeeded; no tests or generators were run.

## Unknowns and residual risks

- I did not inspect private repos or private generated package skill bodies.
- I did not run `check-skills` or regenerate outputs because the task is investigatory and read-only.
- I did not inspect every deleted prose section in full; focus was code blocks, concrete snippets, and current abstraction level.
- Some recommendations depend on future loading-design decisions: if generator dependency composition changes, the Rust agglomeration recommendation should be revisited.
- I wrote this required scout output file despite the user's preference to avoid reports; the role contract required an output under `agent-outputs/<SessionName>/`.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings list source paths such as modules/rust-methods/full.md, modules/rust-parsers/full.md, modules/rust-storage-and-wire/full.md, modules/kameo/full.md, modules/enum-contact-points/full.md, modules/mermaid/full.md, and generated primary surface evidence from jj diff -r 483c30ec. Each finding includes severity and restore/replace/delete judgment."
    }
  ],
  "changedFiles": [
    "agent-outputs/SkillsSlashDown/Scout-SnippetRestorationFindings.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "pwd && ls && find .. -maxdepth 2 -name AGENTS.md -print",
      "result": "passed",
      "summary": "Confirmed primary workspace and local instruction file."
    },
    {
      "command": "jj status --no-pager",
      "result": "passed",
      "summary": "Observed pre-existing primary working-copy additions under agent-outputs before writing this report."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/skills && jj log --no-pager -r 'ancestors(@, 15)'",
      "result": "passed",
      "summary": "Identified recent cleanup commits from f186170c through 6b8cf0d6."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/skills && jj diff --no-pager -r <cleanup-commit> --stat",
      "result": "passed",
      "summary": "Mapped changed files and deletion-heavy cleanup commits."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/skills && python3 fenced-block comparison using jj file list/show",
      "result": "passed",
      "summary": "Counted removed fenced blocks per module between parents(f186170c) and current."
    },
    {
      "command": "cd /home/li/primary && jj diff --no-pager -r 483c30ec --stat",
      "result": "passed",
      "summary": "Confirmed generated primary surfaces mirrored the power-washed removals."
    },
    {
      "command": "targeted read/rg of current modules and generated .agents skills",
      "result": "passed",
      "summary": "Verified current abstraction level and retained examples."
    }
  ],
  "validationOutput": [
    "Inspection-only pass completed; no tests or generators run.",
    "Source repo status was clean before this scout work; primary already had unrelated agent-output additions before this scout output."
  ],
  "residualRisks": [
    "No private scopes inspected.",
    "No regeneration/check-skills run.",
    "Findings focus on code blocks and concrete examples, not every removed prose paragraph."
  ],
  "noStagedFiles": false,
  "diffSummary": "Added one scout findings report under agent-outputs/SkillsSlashDown; no source, generated skill, commit, or push changes.",
  "reviewFindings": [
    "high: modules/rust-methods/full.md - central Rust method/type rule lost all 15 concrete Rust examples; replace with compact wrong/right snippets.",
    "high: modules/rust-parsers/full.md - deleted skill contained one useful parser-library example; keep skill deleted but fold a tiny example into Rust patterns/core.",
    "high: modules/rust-storage-and-wire/full.md - storage/wire rules lost rkyv framing examples; add one compact typed frame example.",
    "medium-high: modules/kameo/full.md - current Kameo rules are abstract without a minimal actor/message implementation; add one compact shape example.",
    "medium: modules/enum-contact-points/full.md - contact-point rule lost match-matrix examples; add one small tuple/nested match example.",
    "medium: modules/mermaid/full.md - syntax skill lacks a valid minimal diagram; add one strict-renderer-safe diagram block.",
    "low/no blockers: many deleted local-path/report/CLI examples should not be restored."
  ],
  "manualNotes": "Rust consolidation should assume rust-core is loaded by code role packets, but current Rust skill dependency vectors are empty; make any dependent Rust pattern skill explicit rather than relying on automatic dependency loading."
}
```
