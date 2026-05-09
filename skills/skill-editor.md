# Skill — skill editor

*How skill files are named, located, and cross-referenced.*

---

## What a skill file is

A skill file is "what an agent needs to know to be effective in
this scope." Two scales:

- **Repo skill** — what an agent needs to be effective in *this
  repo*. Project-specific intent, the repo's role, the
  invariants that don't fit in `ARCHITECTURE.md` because they're
  about *how to work* rather than *what the system is*.
- **Workspace skill** — a cross-cutting capability that applies
  across many repos in the workspace (e.g. `autonomous-agent`,
  `skill-editor`).

Skill files complement, but do not replace, `AGENTS.md` and
`ARCHITECTURE.md`. AGENTS.md is the canonical workspace contract
(what every agent must do); ARCHITECTURE.md is the repo's shape
(what the system IS); skills.md is what an agent needs to know
to be *good at* a particular scope.

---

## Naming and location

| Scale | Path | Example |
|---|---|---|
| Workspace skill | `<workspace>/skills/<name>.md` | `~/primary/skills/autonomous-agent.md` |
| Repo skill | `<repo-root>/skills.md` | `criome/skills.md` |

One file per repo. Workspace skills are lowercase-with-hyphens.

---

## Cross-references

When one skill refers to another, **use the repo name plus the
filename**. Never use a full HTTPS URL.

Right:

- "see criome's `skills.md`"
- "see this workspace's `skills/abstractions.md`"
- "see this workspace's `skills/autonomous-agent.md`"
- "see lore's `rust/ractor.md`" (when the target is a tool
  reference, not a skill)

Wrong:

- `https://github.com/<org>/criome/blob/main/skills.md`
- `https://github.com/<org>/primary/blob/main/skills/abstractions.md`

**Why:** deep file URLs silently break when files move, get
renamed, or are deleted. A repo-name reference stays valid
because the reader knows the convention — the skill file is at
the repo root, named `skills.md`.

For repo-level pointers (when you mean "this repo exists,"
without naming a specific file), use the nix-flake form:
`github:<org>/<repo>`.

---

## Format

Skill files are markdown. No required schema. **One capability
per skill** — when a file straddles two distinct capabilities,
split it. Length is not the criterion; the cohesion of what's
inside is. A 1000-line skill that covers a single coherent
discipline (e.g. Rust craft) is fine; a 200-line skill that
mixes notation design with deploy hygiene is not.

The capability test: *would an agent reaching for one of the
sections be helped or hindered by also having the other in
view?* If helped (one cross-cuts the other; the rules cite each
other), it's one capability. If hindered (the agent has to skim
past unrelated rules to find what they came for), it's two.

The structure that has worked across this workspace:

```markdown
# Skill — <name>

*<one-line purpose>*

---

## What this skill is for

<two or three paragraphs setting the scope>

---

## <load-bearing sections>

<the actual rules / patterns / how-to>

---

## See also

<repo-name + filename references to neighboring skills>
```

The `# Skill — <name>` heading is recognisable, separates
skills from regular docs, and matches the file naming.

---

## What goes in a repo skill

A repo's `skills.md` typically holds:

- **The repo's intent** — what it's for and what's
  non-negotiable about it. This is where project-specific
  versions of "this is meant to be eventually impossible to
  improve" live.
- **The thing this repo is the canonical owner of** — naming
  the things only this repo decides.
- **Invariants about how to work in this repo** — what an
  agent must not do, what conventions are load-bearing.
- **Pointers** to the repo's `ARCHITECTURE.md`, `AGENTS.md`,
  and any neighboring skills the agent should also read.

A repo skill does **not** duplicate the workspace contract or
language-agnostic discipline (those live in `lore/`). It
captures only what is specific to this repo.

## What goes in a workspace skill (and what doesn't)

A workspace skill (`~/primary/skills/<name>.md`) captures
**patterns that apply across multiple repos**: cross-cutting
disciplines, agent-behavior rules, language-design
principles, contract-repo conventions. The test is *audience*:
if a fresh agent in a totally unrelated future repo would
benefit from the rule, the rule belongs in primary.

**Component-specific patterns don't belong in primary.**
"How `nota-codec`'s encoder emits eligible PascalCase strings
as bare identifiers" is a nota-codec-specific implementation
rule — it goes in `nota-codec/skills.md`, not in a primary
skill. "Sema's resilience plane uses typed proposal/approval
records because LLMs can't be trusted to mutate state
directly" is a design choice for sema-shaped systems — it
goes in `sema/skills.md` (or stays in the design report)
once that repo's skills emerge, not in a primary skill.

The trap: when you discover a pattern, the temptation is to
write it as a primary skill ("future agents will benefit").
Resist this. Ask: *is this pattern about how we work across
the workspace, or about how a specific component is built?*
Component-specific goes to the component. The workspace skills
stay general.

---

## When to create a new repo skill

The trigger lives in `autonomous-agent.md`: after substantive
work in a repo lacking a `skills.md`, the agent creates one
before finishing the task. The skill captures what the agent
just learned about the repo.

The roll-out across the workspace is **incremental, not batch.**
A skill written while the agent has fresh context — having just
followed the repo's invariants, found its load-bearing files,
respected its boundaries — is a real skill. A skill written by
template-stamping across many repos in one go is a smell of the
form the rule is meant to prevent.

If you find yourself tempted to create skills for many repos
quickly, you don't have enough context for any of them. Pick
one repo, do real work in it, then write the skill.

---

## Editing rules

- Edit a skill in place; don't fork or version it.
- Keep it in present tense. Describe what IS, not what was.
- When a skill's content turns out to be wrong, rewrite the
  skill. The path that led there lives in version-control
  history.
- Cross-reference, don't duplicate. If two skills want to say
  the same thing, one of them should reference the other.
- After a meaningful edit, commit and push immediately
  (per the workspace's autonomous-agent skill).

---

## Examples never show free functions (only `main`)

**The only free function any example shows is `main`.**
Every other `fn` in an example body is a method on a type
(`impl T { fn ... }`) or an associated function (also inside
an `impl`).

This is stricter than `skills/abstractions.md`'s rule (which
permits free functions for small private helpers and pure
relational operations). The reason: **examples teach by
imitation**. An example that shows `fn parse_query(...)` —
even labelled "Wrong:" — primes the next agent to write a
free function. The Wrong/Right comparison teaches the wrong
shape twice.

```rust
// Wrong (rule violation in the example itself):
//
//   fn parse_query(text: &str) -> Result<QueryOp, Error> { … }
//
// vs.
//
//   impl QueryParser<'_> {
//       pub fn into_query(self) -> Result<QueryOp, Error> { … }
//   }

// Right (the example never shows the bad shape):
//
// Anti-pattern (in prose): a free `parse_query(text: &str) -> ...`
// would be a verb-without-a-noun (per `skills/abstractions.md`).
// The right shape is a method:
//
//   impl QueryParser<'_> {
//       pub fn into_query(self) -> Result<QueryOp, Error> { … }
//   }
```

When a skill needs to discuss an anti-pattern that IS the
free function, name the anti-pattern in **prose**, with the
right-shape code in the example block. Don't write the
free-function shape as code.

### Test functions

Rust's `#[test]` attribute requires the function be free —
that's a `cargo` constraint, not an example choice.
Examples for tests:
- Show the test **name** as a list item or in prose, not as
  a `fn ...()` block: *Test name patterns:*
  `router_cannot_deliver_without_store_commit`,
  `message_cli_cannot_write_private_message_log`.
- Show the test **body** inside an `impl Fixture { fn ... }`
  block when the body teaches structure, with prose noting
  *"the `#[test]` wrapper calls
  `Fixture::router_cannot_deliver_without_store_commit`."*

### `main` is the named exception

`fn main() { … }` is the one free function any example may
show — it's the binary entry point and Rust requires it.

### Auditing existing skills

When editing a skill, sweep its examples for the violation
before commit. The grep:

```sh
grep -nE '^\s*(pub )?(async )?fn ' <file> | grep -vE 'fn main\b'
```

Every match in an example block needs to be either inside
`impl` or removed.

---

## See also

- `autonomous-agent.md` — how to act on routine obstacles
  without asking; cross-reference rules.
- this workspace's `skills/naming.md` — naming conventions used
  inside skill files.
- lore's `AGENTS.md` — workspace contract; skills are
  downstream of the contract.
