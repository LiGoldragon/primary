---
name: skill-editor
description: 'Edits skill and role source in LiGoldragon/skills, then reconciles generated runtime surfaces.'
---

# skill editor

## Rules

- Treat `LiGoldragon/skills` as the canonical skills source. Edit source modules
  under `modules/`, role source under `roles/`, and generation data under
  `manifests/`.
- Treat workspace skill and agent files (`.agents/skills`, `.claude/skills`,
  `.pi/agents`, `.codex/agents`) as generated runtime targets. Inspect them
  only to recover drift; never patch them as source.
- Put reusable instruction in the owning source file. Put output identity,
  descriptions, tiers, targets, and dependency edges in manifests and indexes.
- Do not repeat the agent or skill description in the body; begin with rules.
- Keep instruction terse, present-tense, and current. Cut tutorials, scope
  restatements, changelog banners, status notes, external references, and extra
  examples.
- Do not create or expand repo-specific skills. Durable repo guidance belongs in
  AGENTS.md, ARCHITECTURE.md, README.md, IDEAS.md for speculative future
  projects, or NON_IDEAL_AGENTS.md for workaround debt.
- Use `## Source Maintenance Notes` only for source-side maintainer instructions.
- Avoid absolute deployment paths in skill source; prefer repository-root or
  stable file-relative paths.
- Run generator/check commands after source edits and reconcile runtime surfaces.
  Name unrelated working-copy changes in the result.

## Verification

- Source files have no harness frontmatter.
- Changed headings are unique.
- Manifest and index references resolve.
- Generated outputs match source and have no generated-file notices.

## agent feedback loop

### Feedback Loop

Report only meaningful doctrine friction that affected or plausibly affects efficiency or correctness. Do not add boilerplate when there is no friction.

Use these categories: missing doctrine, misleading or incorrect doctrine, redundant doctrine, over-detailed doctrine, poor discoverability or naming, and split or merge suggestions that would improve efficiency or correctness.

Doctrine friction does not stop ordinary work unless it creates safety, privacy, destructive-action, or credential risk. Finish the assigned work, then include concise feedback with the category, affected doctrine surface, observed friction, and suggested owner or direction.

Keep private and secret material out of feedback. Describe the doctrine gap abstractly when the concrete example is private.

## edit coordination core

### Edit Coordination

Before editing shared files or running a command that writes them, register the assigned Session/Lane with `meta-orchestrate`, then claim the exact path or repository with ordinary Orchestrate under that lane. The ordinary claim field is role-shaped, but it carries the lane identity.

If the task needs editing and no session name, lane name, or Fresh/Recovery mode is assigned, pause and report the missing coordination identity. Do not use generic names such as `general-code-implementer`, `skill-editor`, or `rust-auditor`.

Lane registration is the atomic check. Do not pre-observe before registration. Treat Fresh duplicate registration as a conflict/blocker. Treat orchestrator-declared Recovery duplicate as inherited only when the active lane clearly matches this recovery context.

Do not edit projected lock files by hand.

```sh
meta-orchestrate "(Register ((<SessionName> <LaneName> ([<RoleToken>...] Structural) <detail-atom>) Fresh))"
orchestrate "(Claim (<LaneName> [(Path /absolute/path)] <reason>))"
orchestrate "(Release <LaneName>)"
meta-orchestrate "(Unregister (<SessionName> <LaneName> <detail-atom>))"
```

Use a single bare NOTA atom in each `<detail-atom>` slot; quoted strings and pipe text are rejected.

Observe only when coordination state is evidence after registration or during audit. When relaying observed claims, show direct age, not only a start timestamp.

```sh
orchestrate "(Observe Sessions)"
orchestrate "(Observe Lanes)"
orchestrate "(Observe (SessionLanes <SessionName>))"
```

Do not claim `.beads/`. Treat an Orchestrate claim on `.beads/` as invalid agent policy state; force-release or remove that claim instead of treating it as a lock.

If the local repository or worktree is already claimed or visibly in use, do not share that checkout. Start from `main` in an isolated feature worktree, claim that worktree path under the registered lane, and file a bead naming the repository, branch, worktree, and required final disposition: discard, partial merge, or full merge.

```sh
bd create "Track <branch> worktree" -t task -p 2 --description "<repo>; <branch>; <worktree>; disposition needed" --labels feature-branch,worktree
```

For Git worktrees managed by beads, create from a clean `main` checkout with `bd worktree create <worktree> --branch <branch>`. In JJ workspaces, create from `main` with `jj workspace add --revision main --message '<branch>' <worktree>` and move the feature bookmark to the completed commit with `jj bookmark set <branch> -r @-`.

When daemon worktree inventory is needed, the meta API shape is:

```sh
meta-orchestrate "(RegisterWorktree (Worktree <repo> <branch> /absolute/path <lane> Active <purpose> <timestamp-nanos> Unpushed))"
```


### Editing Closeout

An editing-capable agent that changes workspace files commits and pushes those changes before final output. This is unconditional.

A prompt cannot turn file-editing work into uncommitted work. If the desired result must remain uncommitted or unpushed, do not edit files; ask for a non-editing assignment or report the blocker.

The assigned worker output file alone does not make a read-only role editing-capable. Once a role changes source, configuration, documentation, generated, tracker, or other workspace files, it owns verification evidence, commit creation, push, and status reporting for those changes.

Preserve peer edits. Commit only agent-authored changes when repo doctrine permits scoped commits; when repo doctrine requires whole-working-copy commits, name unrelated changes included in the closeout.

When closeout depends on another repo, branch, package, or generated surface, surface stale dependency pins, unmerged producer branches, and dependencies that have unmerged branches when they affect portability, integration, deployment, repurpose, or closeout.

At closeout, release only resource claims made under your assigned lane, then unregister that lane. Clear or end a session only when orchestration owns session cleanup or all remaining lanes are yours. Do not release generic names or another worker's lane.

Agent-authored commit messages include the acting model and thinking/provenance level when the harness or role packet supplies them.

## NOTA shape checklist

### Rules for Shape

Start from the expected type; it is always known at a correct NOTA boundary. The file kind, schema field, operation argument, reply slot, test fixture, or prompt-supplied schema tells the decoder what type to read.

Write exactly the value of the expected type. The known document, record, object, or application shape fixes slot count: no extra slots, no missing slots, and no omitted positional optionals. Optionality is typed data in a known position.

Meaning comes from expected type plus position. A use-site name is data, a schema-required disambiguator, or a reference/path/name value under the expected type; it is never a label that identifies a positional slot.

A leading atom is valid only when the expected position is an enum and that atom exactly matches one of its variants. Run the variant-sibling test on every leading atom: name the other variants valid at this exact position. If none exist, the atom is not a tag; move the idea into the schema field, a typed enum value, or remove it.

Choose cardinality before syntax. A closed exactly-one-per-slot set is a positional record. Use a vector only for homogeneous repeatable elements where order or duplicates are meaningful, or where validation rejects duplicates. Do not encode fixed slots as tagged rows in a list.

Records are positional. Emit field values in schema order; do not put field labels in the value. Treat `Vector Vector`, same-name self-labeling, and `Name Value` adjacency as design alarms for self-labeling instead of typed positional data.

Use maps only for real key/value domains: arbitrary keys, lookup by key, and key identity as data. A value is a map because the expected type is a map, not because labels feel readable.

Prefer closed enums and typed records over strings. A bare atom is valid as a string when the expected type is `String`; capitalization does not infer type state. Enum slots decode by exact variant match.

Before accepting a shape, state the expected type, sibling variants for each tag, cardinality for each collection, and duplicate/order semantics for each vector. If any part is unknown, pause and ask; do not bury uncertainty in a special parser, ad hoc labels, or JSON-like shape.

## NOTA design

### Design Rules

Use `nota-schema-design` when authoring schema for new NOTA types. Use `nota-literacy` when replying to a prompt that supplies a NOTA schema/help projection or examples.

NOTA is structural data. The raw grammar has atoms, parenthesized records, vectors, maps, pipe text, pipe parenthesis, pipe brace, and `;;` comments. Schema and codec layers assign meaning from the expected type plus position.

At every correct NOTA boundary, the expected type is already known. The known document, record, object, or application shape fixes slot count: no extra slots, no missing slots, and no omitted positional optionals.

Records are positional. Field order is part of the interface; reordering fields is a compatibility change. Prefer a trailing field or a new variant over changing existing positions. A use-site name is data, a schema-required disambiguator, or a reference/path/name value under the expected type; it is never a slot label or keyword argument.

Use an untagged struct when there is one payload shape. Use an enum only when a position can hold multiple named variants. Enum variants use names, not numeric codes.

Use bare atoms for stable identifiers, enum-like values, and canonical names. A bare atom is valid as a string when the expected type is `String`; capitalization does not infer type state. Use pipe text or quoted/bracket string forms when whitespace, punctuation, comments, or arbitrary prose are the point.

Put machine data in records, not comments. Comments explain unusual choices; they do not carry values that must be read, queried, validated, or migrated.

Model alternatives as variants or named option variants, not loose flags. A variant carries only the fields that choice needs.

Use maps only for genuinely keyed collections. A value is a map because the expected type is a map, not because labels feel readable. Atom keys are normal unless the map type requires a richer key.

Avoid multi-field unnamed tuples. If there is more than one value, name the record or fields in the schema so the positional call site stays readable. Treat self-labeling adjacency such as `Name Value` as a design alarm.

NOTA is strict positional: every positional component and every variant payload always appears in the text form. Never place optionality where it can omit a slot or collapse to a bare atom. Model optionality as typed data in a known position: an explicit variant, option record, or required sentinel shape.

Encode and decode structured data only through the canonical shared codec for its format. Hand-rolled or special-cased per-type encode/decode logic is forbidden.

## spirit query

### Query Rules

Use `spirit` for read-only intent queries before judgment. Query relevant public intent early when orchestrating, auditing, scouting, translating, designing, editing doctrine, or deciding how a brief should map to durable guidance. Purely mechanical workers may skip this when the brief already supplies the needed intent context.

Use domain-first `PublicRecords` as the normal query path. Start with the narrowest matching domain or subtree, then widen only when the result lacks enough intent evidence. Use `Lookup` when the brief or a previous query gives a known record identifier.

Public reads are the default. Private reads need explicit prompt authorization for that privacy scope, and private content stays out of public chat, reports, commits, and generated doctrine.

### Query Shapes

The CLI takes exactly one argument: inline NOTA when the argument starts with `(`, or a NOTA file otherwise. It replies on stdout with typed NOTA and returns nonzero on transport, parse, or daemon errors.

List public records in the narrowest relevant domain first:

```sh
spirit "(PublicRecords ((Full [(Technology (Software (Intelligence AgentSystems)))]) None))"
```

Lookup a known record identifier:

```sh
spirit "(Lookup <record-id>)"
```

Treat `(Error [record not found])` and `(Error [no matching record])` as negative evidence, not tool failure. Treat validation rejection, parse failure, daemon failure, or unexpected wire shape as a blocker for intent-grounded judgment.

### Domain List

Use these current Spirit domains and subdomains when forming `PublicRecords` scopes.

The domain tree is written as NOTA-shaped records. A bare atom is a selectable domain or leaf. `[ ... ]` lists children under the current domain. `(Name [ ... ])` means `Name` has nested children. Query Spirit with the path atoms in the same nesting shape inside `PublicRecords`.

Examples: `(PublicRecords ((Full [(Health Medicine)]) None))`; `(PublicRecords ((Full [(Technology (Software (Intelligence AgentSystems)))]) None))`.

```nota
(All)
(Health [Body Mind Nutrition Exercise Sleep Medicine Disease Medication Therapy Reproduction Sexuality Aging Disability Addiction Dentistry Senses Pain Prevention FirstAid Rehabilitation])
(Food [Cooking Diet Recipe Baking Preservation Fermentation Beverage Entertaining Foraging Fasting Dining])
(Home [Housing Maintenance Renovation Furnishing Cleaning Tidying Relocation Realty Property Utilities Locksmithing Appliances])
(Finance [Budgeting Saving Spending Debt Credit Investing Retirement Tax Insurance Income Banking Charity Planning Accounting])
(Work [Career JobSearch Workplace Vocation Leadership Entrepreneurship Employment Compensation Scheduling Unemployment Freelancing Teamwork Productivity Project])
(Craft [Electronics Construction Carpentry Metalworking Sewing Manufacturing Repair Engineering Handicraft Invention])
(Knowledge [Mathematics Logic Physics Chemistry Biology Astronomy Geology Computing Physiology Statistics Research History Linguistics Philosophy Economics Cognition Taxonomy])
(Education [Studying Teaching Schooling Skill Reading Memorization Pedagogy Mentoring Autodidacticism Credential])
(Language [Writing Rhetoric Translation Grammar Conversation Correspondence Listening Oratory Editing Terminology Notation])
(Art [Fiction Poetry Music Painting Photography Film Theater Dance Design Sculpture Creativity Storytelling Publishing])
(Kinship [Friendship Romance Marriage Family Parenting Relatives Reconciliation Boundaries Intimacy Rapport Caregiving Grief Belonging])
(Selfhood [Growth Introspection Discipline Emotion Virtue Motivation Confidence Identity Purpose Decision Temperament Wellbeing Composure])
(Spirituality [Worship Prayer Meditation Ritual Faith Theology Contemplation Pilgrimage Scripture Ethics Mortality Transcendence Asceticism Wisdom])
(Governance [Politics Government Administration Citizenship Elections Activism Policy Diplomacy Movements Organizing Services Naturalization War])
(Law [Rights Contract Title Crime Litigation Compliance Custody Liability Procedure Justice Policing Arbitration])
(Community [Neighborliness Volunteering Solidarity Membership Gatherings Reputation Service Hospitality Institutions])
(Nature [Agriculture Gardening Horticulture Husbandry Pets Forestry Fishing Hunting Conservation Weather Wilderness Sustainability Resources Stewardship])
(Travel [Itinerary Destination Transportation Driving Navigation Commuting Logistics Migration Tourism Transit Cycling])
(Commerce [Selling Buying Marketing Retail Sourcing Trade Support Pricing Negotiation Assets Market])
(Leisure [Recreation Sport Games Hobby Entertainment Collecting Outdoors Play Relaxation Celebration Fandom])
(Appearance [Clothing Grooming Style Cosmetics Etiquette Comportment])
(Safety [Protection Preparedness Risk Cybersecurity Privacy Disaster Military Deterrence])
(Information [Curation RecordKeeping Documentation News Broadcasting Archives Database Retrieval Classification])
(Technology [
  (Hardware [All Networking])
  (Software [
    (Programming [All TypeSystems Compilation Parsing Grammars CodeGeneration Metaprogramming Macros DomainSpecificLanguages])
    Theory
    (Systems [All SystemsProgramming Concurrency])
    (Distributed [All ProtocolDesign EventDrivenArchitecture])
    (Data [All Persistence Serialization Formats Modeling SchemaEvolution Migration])
    (Intelligence [All AgentSystems])
    (Security [All Cryptography Authentication Authorization SecretsManagement Privacy])
    (Quality [All Testing])
    (Operations [All BuildSystem ReleaseEngineering DependencyManagement Deployment ConfigurationManagement])
    (Observability [All Tracing])
    (Surfaces [All Visualization CommandLineInterfaces])
    (Engineering [All Architecture Design ApplicationProgrammingInterfaces Documentation VersionControl DevelopmentProcess Management Modularity])
  ])
])
```

### Evidence

Report the query class, relevant record identifiers, and the conclusion needed for the task. Explain a Spirit identifier on first mention when it matters. Summarize record lists instead of pasting irrelevant hashes.

## skill source core

### Skill Source Core Purpose

Skill-system source edits keep instruction compact, current, and owned by the
generator inputs. Treat `LiGoldragon/skills` as the canonical skills source. The
reusable teaching body lives in source modules and role source modules; identity,
descriptions, tiers, targets, and dependency edges live in manifests or
dependency indexes. Workspace skill and agent files are generated runtime targets,
not source.

### Skill Source Prose

Write present-tense guidance that teaches one capability. Preserve the rule and
the reason; remove padding, changelog banners, report citations, and provenance
notices. Before adding text, reuse or reword compatible existing instruction.
Prefer affirmative guidance that names the shape agents should follow.

Role source starts with the role contract and stays mostly role prose. Shared
procedure belongs in modules so it is not copied into every role. Source modules
have no harness frontmatter.

Visible generated titles use the human title only. Keep composition labels such
as `Skill`, `Module`, or `Role` as source structure only; do not depend on those
labels appearing in generated runtime text.

Use `## Source Maintenance Notes` only for maintainer instructions that must stay
source-side. Everything from that heading through the end of the source fragment
is stripped from generated runtime surfaces.

Avoid absolute deployment paths in skill source. Prefer repository-root-relative
paths, or file-relative paths when the referenced file is local,
version-controlled, and stable.

Put required non-ideal workaround guidance in `NON_IDEAL_AGENTS.md` when a repo
needs it. Keep `AGENTS.md` for ordinary operating rules and `ARCHITECTURE.md` for
the ideal target shape; workaround instructions should read as debt and future
fix targets.

### Skill Source NOTA Manifests

Keep data in NOTA records, not comments. Use enum variants when a position can
carry more than one shape, and untagged structs when there is only one shape.
Use named enum variants rather than numeric codes. Preserve positional field
order and bare atoms for canonical strings.

The active output manifest lists emitted outputs. The dependency index maps
module identifiers to source paths and dependency module identifiers. Assemble
role packets from the active manifest and dependency index.

### Skill Source Reconciliation

After source edits, run the generator or check command when available. Treat a
skill edit as deployed only when the generated runtime surfaces active agents
read are reconciled; stale generated outputs are a deployment gap. Confirm that
every manifest or dependency path exists, new headings are unique within their
source file, generated runtime outputs would not receive provenance notices, and
role packets include the doctrine the manifest names without pulling the whole
corpus.

Dirty consuming workspaces do not block generation or required whole-working-copy
commits. Only direct ownership of a required generated path blocks deployment;
name the owner and path precisely.

After generation and checks pass, close out source edits with commit and push.
Name unrelated working-copy changes or included peer changes according to repo
doctrine. In the result, suggest further removals or rewordings that could
reduce bloat or improve clarity but were not safe or in scope for the pass.
