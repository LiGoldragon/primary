# Skill template engine — design

Design for putting target conditionals inside skill markdown with minijinja,
replacing composed-in target modules.

Studied: `/git/github.com/LiGoldragon/skills` at 78 sources, 68 indexed modules,
50 active skills, 16 `RoleComposition` modules, 2 target insertions.
Nothing was edited.

## Read this first

The mechanism below is sound and every existing per-target insertion migrates
byte-identically through it. **The motivating case does not fit today's output
surfaces.** `management` is a skill; skills emit to exactly two files,
`.agents/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md`, and the
first is read by Pi *and* Codex (`ARCHITECTURE.md` line 40, `OutputSurface::skill_path`).
There is no Codex-only skill file, so `{% if codex %}` in `skills/management.md`
has no destination that is Codex and not Pi. See item 9. Items 1–8 are the
mechanism and hold either way.

## 1. Variable surface

**Recommendation.** Three booleans and nothing else: `claude`, `codex`, `pi`.
Spelling is boolean-per-target — `{% if codex %}`. Exactly one is true in every
render, asserted by the generator. Role packet modules are templated on the same
axis through the same code path. Permission and depth are **not** exposed.

Justification, spelling: with strict undefined (item 2) a typo'd boolean is a
hard error, while a typo'd *string* in `{% if target == "codex" %}` leaves
`target` defined and silently evaluates false — the English spelling is also the
safer one, which is the reverse of the usual trade.

Justification, no permission/depth: the permission-by-depth cross product is
already total, validated, and fails generation on a missing or duplicated cell,
so conditionals would create a second authority for a fact that already has a
non-decaying home. If a case ever arrives, add booleans (`critical`, `read`),
never string compares. Adding a variable later never breaks an existing template.

Context per output surface:

| surface | file | `claude` | `codex` | `pi` |
| --- | --- | --- | --- | --- |
| `ClaudeSkill` | `.claude/skills/<n>/SKILL.md` | true | false | false |
| `ClaudeAgent` | `.claude/agents/<role>.md` | true | false | false |
| `CodexAgent` | `.codex/agents/<role>.toml` | false | true | false |
| `PiAgent` | `.pi/agents/<role>.md` | false | false | true |
| `AgentsSkill` | `.agents/skills/<n>/SKILL.md` | false | **?** | **?** |

The last row is the whole problem. Two true, or two false; neither is honest.
Encode the invariant in code — the generator asserts exactly one true — so
`AgentsSkill` becomes unrepresentable and the gap cannot be papered over.

**Restrict the grammar.** Permit only `{% if <name> %}`, `{% else %}`,
`{% endif %}`, where `<name>` is one of the three. No expressions, no filters,
no loops, no `{{ }}`, no `{% include %}`, no `{% raw %}`. Reject anything else
before rendering. A closed grammar is what makes the checks in items 2, 4 and 10
cheap and total; an open one is how this decays.

## 2. Strictness

**Recommendation.** `env.set_undefined_behavior(UndefinedBehavior::Strict)`,
plus a closed-set pre-check on the template source.

minijinja 2.21's documented table:

| variant | printing | boolean test | attribute access |
| --- | --- | --- | --- |
| `Lenient` (default) | empty string | **false** | fails |
| `Chainable` | empty string | **false** | undefined |
| `SemiStrict` | fails | **false** | fails |
| `Strict` | fails | **fails** | fails |

`Strict` is the only variant where `{% if kodex %}` errors. The default is
`Lenient`, which is exactly the silently-empty-block failure mode.

Do not rely on `Strict` alone. The closed grammar (item 1) means every
conditional name is extractable by a line scanner, so validate names against
`{claude, codex, pi}` *before* handing the source to minijinja. That gives
"unknown target `kodex` at skills/management.md:7, known: claude, codex, pi"
instead of a generic render error, and it does not depend on subtleties of how
`not`, `and`, or `or` interact with undefined.

Config:

```
minijinja = "2"          # default features; this is a build tool, size is irrelevant

let mut env = Environment::new();
env.set_undefined_behavior(UndefinedBehavior::Strict);
env.set_trim_blocks(true);
env.set_lstrip_blocks(true);
env.set_keep_trailing_newline(true);
```

Render with `render_named_str(<source relative path>, text, ctx)` so
`minijinja::Error` carries the file name and `Error::line()` the line.

## 3. Whitespace

**Recommendation.** `trim_blocks = true`, `lstrip_blocks = true`,
`keep_trailing_newline = true`, plus a post-render normalization of the rendered
fragment: collapse any run of two or more blank lines to one, and end with
exactly one newline.

The three minijinja settings remove the newline after a block tag and any
indentation before one. They do **not** remove the blank line an author writes
*before* a block that renders empty. That leftover is the stray blank line, and
it is load-bearing, not cosmetic: without the normalization the two existing
insertions do not migrate byte-identically. Both source-side rules ("put the
blank line inside the block") and this normalization work; the normalization is
the one that cannot be forgotten.

The normalization is a no-op on today's corpus — no source file in `skills/`
contains a double blank line or lacks a final newline.

### Rendered output, the `management` example

Source `skills/management.md`, exactly as written in the brief:

```
Reserve your context for managing subagents.
Use no tools except subagent coordination.
Delegate all task work.
Do other work while agents run.
Return a synthesis to the caller.

{% if codex %}
Keep a wait active while agents run; you are resumed only through it.
Wait with no timeout.
A psyche message interrupts the wait immediately, so waiting costs no responsiveness.
Say nothing when a wait returns with nothing finished.
{% endif %}
```

Fragment render, `codex = false`:

```
Reserve your context for managing subagents.
Use no tools except subagent coordination.
Delegate all task work.
Do other work while agents run.
Return a synthesis to the caller.
```

The `{% if %}` and `{% endif %}` lines vanish with their own newlines. The blank
line the author left before `{% if %}` survives the render and is removed by the
trailing-newline rule. The fragment ends with one newline after `caller.` and no
blank line.

Fragment render, `codex = true`:

```
Reserve your context for managing subagents.
Use no tools except subagent coordination.
Delegate all task work.
Do other work while agents run.
Return a synthesis to the caller.

Keep a wait active while agents run; you are resumed only through it.
Wait with no timeout.
A psyche message interrupts the wait immediately, so waiting costs no responsiveness.
Say nothing when a wait returns with nothing finished.
```

One blank line before the Codex block, none after `finished.`, one final newline.

### The whole file

`MarkdownAssembly` prepends the frontmatter block and one blank line. The
complete `.claude/skills/management/SKILL.md`:

```
---
name: management
description: 'Use when coordinating delegated work for a caller.'
---

Reserve your context for managing subagents.
Use no tools except subagent coordination.
Delegate all task work.
Do other work while agents run.
Return a synthesis to the caller.
```

File ends with one newline after `caller.` — byte-identical in shape to the file
deployed today, with `Never block on subagents.` replaced by
`Do other work while agents run.`

The `codex = true` counterpart is `.codex/skills/management/SKILL.md` and exists
only if item 9 is approved. Without it, the only non-Claude file is
`.agents/skills/management/SKILL.md`, which Pi also reads.

### Whitespace evidence from the two real migrations

`general-instructions.md` inlining `codex-skill-loading`:

```
- Do not make material authority, security, compatibility, schema, curriculum, or deployment changes without explicit psyche approval.

{% if codex %}
# skill loading

- Do not reload a complete pasted skill unless freshness or source verification is required.
{% endif %}
```

`# skill loading` and not `## skill loading`: `general-instructions` is fragment
index 1 in every role packet, and `HeadingNormalizer` demotes by one for any
fragment past the first. The Codex render reproduces today's
`.codex/agents/*.toml` byte for byte. The Claude and Pi renders end with
`...approval.` plus the trailing-newline rule, also byte-identical to today.

`psyche-interraction.md` inlining `psyche-interraction-claude-briefness`:

```
## Central
Be very brief unless writing a context handover.
Align with the psyche’s vision.
Ask the psyche *until the vision is clear.*

{% if claude %}
Use the fewest words that preserve the answer.
Do not repeat context the psyche already knows.
{% endif %}
```

Both renders reproduce the deployed files exactly. Without the trailing-newline
rule the `AgentsSkill` render gains a blank line and the migration is no longer
byte-identical.

## 4. Leak guard

**Recommendation.** Fail generation if any generated output contains `{` or `}`.
Not the six Jinja markers — any brace.

Reason: the six-marker scan misses the near-miss. `{ % if codex % }` is not a
tag, so minijinja passes it through as literal text, and it contains no `{%`.
A stray space in a conditional would ship the conditional to an agent as
doctrine. The brace scan catches it.

This is satisfiable today at zero cost: **there is not a single `{` or `}` in
any of the 78 source files, nor in any of the 76 deployed generated files.**
Verified.

Placement: on the final rendered string, inside `ManifestAssembler::render`,
after markdown assembly for `Markdown` and after the TOML wrapper for `Toml`.
That covers both Write and Check mode and the non-writing `visualize` path,
because all three go through `render`. Error carries the output path, line
number, and the offending line.

The cost is real and permanent: doctrine can never contain a brace. Concretely,
a future `skill-templating` skill cannot show `{% if codex %}` to an agent —
`{% raw %}` would render the literal and the guard would reject it, correctly.
Document the syntax in the skills repo's `ARCHITECTURE.md` and `AGENTS.md`,
which are not generated outputs. If the psyche ever wants brace-bearing
doctrine, the documented relaxation is: allow braces only inside fenced code
blocks, verified by a fence-aware scanner, and keep the absolute ban outside
fences. Do not relax it speculatively.

## 5. What the manifests lose

**`target-module-insertions.nota` — dies entirely.** Both records migrate to
conditionals (`general-instructions` → `{% if codex %}`, `psyche-interraction`
→ `{% if claude %}`). Delete the manifest, the `TargetModuleInsertions` and
`TargetModuleInsertion` schema types, `ModuleIndex::target_modules`, and the
insertion step in `ModuleExpansion::append`. The two overlay sources
`codex-skill-loading.md` and `psyche-interraction-claude-briefness.md` are
deleted with it. Justification: this manifest exists only to express per-target
variation, which is exactly what conditionals now express.

**`module-dependencies.nota` — survives, shrinks.** It carries three facts, only
one of which templating touches. Dependency edges (`nota-literacy` →
`nota-shape-checklist`, `release-train-development` → four modules) are shared
content, untouched. `ModuleKind` is the guard that stops a role-only module
being emitted as a runtime skill; keep it, while noting it becomes near-degenerate
once the orphans go — `general-instructions` would be the only `RoleComposition`
left. It shrinks by the 14 orphan records. Separately and optionally, the
`skills/<id>.md` path column is already forced by `require_flat_source_path` and
so is derivable; dropping it is a clean follow-on but is a schema change and
should not ride along with this one.

**`universal-role-modules.nota` — survives unchanged.** `[general-instructions
tenets]` is shared content injected into 24 generated packets, not per-target
variation. Templating cannot replace it and `{% include %}` cannot either,
because roles have no source file — they are generated, so there is no template
to host the include. This is the clearest instance of the trap named in the
brief: leave it alone.

**`skill-module-compositions.nota` — dies, but not because of templating.** Its
one record, `(psyche-interraction [psyche-interraction-continuation])`, is a
composition with exactly one consumer, always. That is a file split, not reuse.
Inline `psyche-interraction-continuation.md` into `psyche-interraction.md`,
delete both the module and the manifest, and delete the
`SkillModuleCompositions` schema types. Note this is *not* byte-identical: the
continuation content moves from fragment index 1/2 to fragment 0, so its
headings go from `### Conversation` to `## Conversation`. Arguably more correct,
since `## Central` is already at that level — but it is an output change and
needs approval on its own terms. Doing it is optional and separable from the
rest.

**Shared blocks stay a manifest concept. No `{% include %}`, no macros.**
An include reintroduces the exact failure the change is meant to remove: the
included file's only reference lives inside another file's body, and deleting
the including line silently orphans it with nothing able to detect it. The
manifest is at least machine-checkable. See item 10 for the check that makes
orphans impossible in either representation.

## 6. The 14 orphans

**Recommendation.** The mechanism deletes nothing and decides nothing. It adds
one rule — *an unreachable source file fails generation* — and reports the list.
The psyche then chooses delete-or-wire per file.

Scope is larger than 14. Three disjoint sets:

- **14 indexed `RoleComposition` orphans**: `spirit-submission`,
  `edit-coordination-core`, `editing-closeout`, `code-implementation-core`,
  `non-ideal-registry`, `rust-core`, `nix-core`, `intent-core`,
  `repo-scaffold-core`, `repo-operation-core`, `architectural-truth-tests`,
  `rust-discipline`, `bead-weaver`, `nixos-vm-testing`. (`rust-discipline` is
  reachable only from `rust-core`, itself an orphan.)
- **10 files not in the index at all**: `claude-manager-non-fable`,
  `manager-boundary`, `manager-communication`, `manager-decisions`,
  `manager-dispatch`, `manager-intent-classification`, `manager-liveness`,
  `manager-safeguards`, `manager-synthesis`, `psyche-facing-commitments`.
- **The sources freed by the in-flight 50 → 26 skill deletion**, whose count
  is not yet settled.

The 10 unindexed files are worse than orphans: `flake.nix`'s
`interaction-skill-composition-guardrails` check currently *requires* nine of
them to exist on disk while being absent from the index. A check enshrines the
decay it should have caught. That check must be rewritten regardless of this
design.

Sequencing matters: the reachability check must land in the same commit as the
disposition, or after it. Landing it first breaks generation for 24-plus files.

## 7. Migration

Each step is independently green — `check-skills` passes against the unchanged
deployed workspace, which is the byte-identity proof.

0. **Wait.** Do not start while the 50 → 26 deletion is editing
   `active-outputs.nota` and `module-dependencies.nota`.
1. **Add the engine, change nothing.** minijinja in `Cargo.toml` and
   `Cargo.lock`; `MarkdownFragment::read(path, target)` renders through the
   configured `Environment`, then applies the blank-line normalization; the
   generated role leading fragment (`from_text`) is not templated. Because no
   source contains a brace, this is a byte-identical no-op. `check-skills` must
   pass with no regeneration. This is the safe landing.
2. **Add the leak guard and the grammar/name pre-check.** Also a no-op today.
   `check-skills` still green.
3. **Migrate `general-instructions`.** Add the `{% if codex %}` block, delete
   the `target-module-insertions.nota` record, delete `codex-skill-loading.md`
   and its index record. Regenerate; diff must be empty.
4. **Migrate `psyche-interraction`.** Same shape with `{% if claude %}`. Then
   delete `target-module-insertions.nota`, its schema types, and the expansion
   code. Diff must be empty.
5. **The `management` change.** Blocked on item 9. If approved, the surface
   split lands as its own step *before* the content change, so the new
   `.codex/skills/` and `.pi/skills/` files appear as a pure duplication of
   `.agents/skills/` and can be reviewed as such.
6. **Reachability check plus orphan disposition,** in one commit (item 6).
7. **Optional:** collapse `skill-module-compositions.nota` (item 5); drop the
   derivable path column from `module-dependencies.nota`.

## 8. Tests

### Existing Rust tests that break

| test | line | why |
| --- | --- | --- |
| `target_module_insertions_apply_only_to_matching_generated_surfaces` | 473 | mechanism retired; replace with the per-target conditional test |
| `psyche_interraction_claude_briefness_is_typed_and_target_scoped` | 374 | `assert_eq!` on exact source text, and `include_str!` of a deleted file — **compile error** |
| `management_is_subagent_scoped_and_has_no_psyche_interaction_doctrine` | 253 | asserts `Never block on subagents.`, which the new text replaces |
| `harness_api_fields_do_not_leak_into_general_management_doctrine` | 282 | `include_str!` of nine `manager-*.md` files — **compile error** if they are deleted in step 6 |
| `host_reboot_requires_specific_psyche_approval` | 428 | `include_str!("manager-safeguards.md")` — same |
| `skill_module_compositions_reject_inactive_and_duplicate_skill_entries` | 199 | only if the optional step 7 lands |
| `generation_rejects_nested_legacy_module_source_paths` | 170 | only if the path column is dropped |

`general_instructions_compose_once_and_keep_authority_gates` (439) survives —
`universal-role-modules.nota` is kept.

### Existing nix checks that break

- `interaction-skill-composition-guardrails` — `cmp "$management"
  "$expected_management"` is a byte comparison of `skills/management.md` against
  five exact lines. It breaks the instant a conditional is added. It also greps
  for both retired manifest records and requires the nine unindexed
  `manager-*.md` files to exist. Full rewrite.
- `flat-active-source-layout` — survives; needs rework only if the path column
  is dropped.
- `role-cross-product-manifests` — **appears already stale**, independent of
  this design: it greps `(critical (claude-opus-5 (Some High)) (gpt-5.6-sol
  (Some Medium)))` while `role-depths.nota` now reads `(gpt-5.6-terra (Some
  Xhigh))`. Worth confirming before assuming this design broke it.

### New tests

1. **A conditional renders per target.** One fixture source with all three
   blocks; assert the Claude output carries only Claude lines, the Codex packet
   only Codex lines, the Pi packet only Pi lines, and each output carries the
   unconditional lines exactly once.
2. **Strict undefined fails the build.** `{% if kodex %}` errors, and the
   message names the file, the line, and the three known targets. Cover
   `{% if not kodex %}` too rather than assuming `not` inherits the behavior.
3. **No template syntax leaks.** A fixture that would emit `{%` fails with the
   leak error. Plus a corpus-wide test: generate from the repo and assert no
   generated file contains `{` or `}`.
4. **Whitespace golden.** Byte-exact assertion of both renders of the
   `management` example in item 3. This is the test that catches a regression in
   any of the four whitespace settings at once.
5. **Exactly one target is true.** Assert the invariant for every generated
   surface; this is what makes the item 9 gap a build failure rather than a
   silent wrong answer.
6. **Grammar is closed.** `{% for %}`, `{{ x }}`, `{% include %}`, `{% raw %}`
   each rejected with a grammar error.
7. **Reachability.** An unreferenced `skills/*.md` fails generation, naming it.
8. **Dead branch.** See item 10 — a `{% if pi %}` inside a module that never
   renders for Pi fails generation.

## 9. Blocking question for the psyche

`AgentsSkill` is one file read by both Pi and Codex. The motivating case needs
Codex-only skill lines. Three ways out; none can be chosen by an agent, because
each is a deployment change.

- **Split the skill surface.** Replace `AgentsSkill` with `CodexSkill`
  (`.codex/skills/<n>/SKILL.md`) and `PiSkill` (`.pi/skills/<n>/SKILL.md`).
  `{% if codex %}` becomes real, and the one-true invariant holds everywhere.
  Cost: skill file count goes from 2 per skill to 3. **Prerequisite I could not
  verify:** whether Codex and Pi each actually read their own skills directory.
  The workspace shows no path wiring — Codex's own doctrine
  (`codex-skill-loading`) describes skills as *pasted* blocks, so some external
  loader decides, and I could not find it. Do not approve this without
  confirming the loader reads the new paths, or the skills silently stop
  arriving.
- **Keep the shared file, put the lines in it.** Pi is then told to keep a wait
  active when its harness notifies on completion — the exact waste the doctrine
  exists to prevent. Not recommended.
- **Keep the shared file, drop the case.** Codex managers do not get the lines
  as a skill. The lines could instead live in a role-packet module, where
  `CodexAgent` is a distinct surface — but there is no manager role anymore, so
  they would reach all 8 Codex packets.

Recommendation: the split, gated on confirming the loader. Everything in items
1–8 lands and delivers value before this is answered.

## 10. What I think is wrong or risky

**The anti-decay claim is only half true, and the untrue half is worse than what
it replaces.** A conditional cannot orphan a *file*, but it can orphan a
*branch*. Write `{% if pi %}` inside a module that never renders for Pi and you
have dead doctrine that no grep, no manifest, and no reader will ever find —
today's 14 orphans are at least a `.md` file sitting visibly on disk with a
greppable name. Without a guard this trades 14 visible orphans for an unbounded
number of invisible ones.

The fix is cheap given the closed grammar: the generation plan already knows
which surfaces each module renders into, so for every `{% if X %}` in a module,
require `X` to be true in at least one surface that module actually reaches.
`{% if pi %}` in a role-only module is fine; `{% if pi %}` in a Claude-skill-only
module fails. **Treat this as part of the design, not an extra** — without it
the change does not deliver its stated purpose.

**A reachability check delivers the stated purpose more directly than
templating does.** "Every file in `skills/` must be reachable from
`active-outputs.nota`" would have caught all 24 dangling files years ago and
costs a day. Templating is still worth doing — it is the only way to express the
`management` case, and it removes a manifest that exists purely for target
variation — but the psyche should know that the decay he named is fixed by the
check, not by the engine, and that the check should land regardless of whether
the engine does.

**Every skill source becomes a template forever.** A brace in prose is now a
build error rather than text. Zero sources contain one today, so the cost is
zero now, but it is a permanent constraint on what doctrine can say — most
sharply for any future skill that documents this very syntax (item 4).

**Migration byte-identity is narrower than it looks.** The two target insertions
migrate exactly. Inlining `psyche-interraction-continuation` does not — its
headings shift from `###` to `##`. Verify every migration step by diffing
generated output; do not assume.

**Strict undefined does not catch a semantically wrong but defined target.**
`{% if claude %}` written where `{% if codex %}` was meant renders cleanly and
passes every check here. Nothing in this design, or any design, catches that.

**`ModuleKind` becomes near-degenerate.** After the orphans go,
`general-instructions` is the only `RoleComposition`. Keeping it is defensible —
it is a real guard — but a one-member category is worth revisiting later.

**Two existing checks are already broken or actively harmful and are not this
design's doing.** `role-cross-product-manifests` greps a model
(`gpt-5.6-sol`) that no longer appears in `role-depths.nota`.
`interaction-skill-composition-guardrails` requires nine unindexed files to
remain on disk. Both should be confirmed and fixed on their own, so the
migration is not blamed for them.
