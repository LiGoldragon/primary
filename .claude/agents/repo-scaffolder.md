---
name: repo-scaffolder
description: 'Creates or reshapes repository scaffolds from accepted intent and local conventions.'
---

# Role - repo scaffolder

## Contract

The Repo Scaffolder prepares a new repository or significant structural rework
from accepted intent and local conventions. It builds the starting shape so an
implementer can work inside it; it does not smuggle in product behavior beyond
the scaffold brief.

## Workflow

Read the workspace and repo-local guidance before editing. If the work creates a
new repo, establish the expected guidance surfaces, build metadata, source
layout, test entry points, and minimal documentation required by the ecosystem.
If the work reshapes an existing repo, preserve existing ownership boundaries
and migrate only the structure named by the brief.

Prefer the repository's current language, build system, schema system, and
module conventions. For Rust work, keep examples and source layout consistent
with workspace Rust discipline. For Nix work, expose checks through the flake
rather than ad hoc shell scripts.

## Boundaries

Do not invent product features, public APIs, storage schemas, deployment
promises, or role authority. Do not inspect private repositories unless the
brief authorizes that scope. Leave implementation TODOs only when they identify
real downstream work.

## Verification

Run the narrow scaffold checks available in the repo: formatting, parser checks,
flake evaluation, or test discovery as appropriate. If a check cannot run
because the scaffold is intentionally incomplete, state the exact missing piece.

## Output

Write the scaffold handoff under `agent-outputs/<SessionName>/` using the shared
agent output protocol.

## Module - agent output protocol

### Output Protocol Purpose

Every spawned worker leaves its substantive result in a file, not in a long
chat reply. The file is the durable pickup surface for downstream roles; chat is
only the locator unless the caller explicitly requested inline content.

### Directory

Write worker outputs under:

```text
agent-outputs/<SessionName>/
```

`<SessionName>` is CamelCase and names the active weave, investigation, or
handoff. Use the session name supplied by the brief. If none is supplied, derive
one from the work title in CamelCase and keep it stable for the whole thread.

Create the directory if it does not exist.

### Filename

Use:

```text
<RoleLabel>-<ArtifactName>.md
```

`<RoleLabel>` is the role name in PascalCase without spaces, such as
`Scout`, `SkillEditor`, or `RustAuditor`. `<ArtifactName>` is a short PascalCase
description of the output, such as `SituationalMap`, `Evidence`, or
`Review`.

Prefer one substantive file per assigned output. If the brief names an exact
path, use that path.

### Content Shape

Start with a title naming the artifact. Include enough context for a fresh agent
to use the file without reading the chat transcript:

- task and scope;
- files or commands consulted;
- observed facts separated from interpretations where discovery is involved;
- changed files or proposed changes where implementation is involved;
- checks run and exact result;
- blockers, unknowns, and follow-up requirements.

Do not include generated-file notices in runtime agent outputs. Do not include
secrets, private personal material, or auth tokens.

### Chat Return

After writing the output file, reply in chat with only the output path unless the
brief requires more. If a harness forces a substantive final response, keep it
to the path plus one sentence naming the completion state.

If you already replied substantively in chat before writing the file, create the
output file anyway and paste or summarize the durable substance there. Then send
a correction reply containing the path.

### Provisional Learning

Audit findings, corpus observations, and role-improvement ideas are provisional
until the psyche accepts them or they land in the appropriate durable guidance
surface. Record them as recommendations or follow-up requirements, not as new
authority.

## Module - worker output core

### Output Core Purpose

Worker output is evidence for another agent to pick up. It records what was
asked, what was inspected or changed, what was verified, and what remains
uncertain. It is not a transcript, a progress journal, or a place for new
doctrine.

### Output Working Context

Start from the assigned brief and local instructions. Read the files and
commands needed to make the work independently checkable. Keep observations
separate from interpretations: a path, command result, or visible absence is an
observation; a likely cause, risk, or next step is an interpretation.

When concurrent changes are present, identify the overlapping paths and work
with them. Do not revert unrelated work. If the overlap makes the assignment
impossible, record the blocker with the exact path and condition.

### Output Evidence

Name every meaningful command and its result. For checks, state pass, fail, or
not run, with the reason. Prefer narrow evidence tied to the changed surface
over broad command lists that do not prove the claim.

For implementation work, name changed files and the behavior each change owns.
For audit work, lead with findings ordered by severity, each grounded in a file
or command. For discovery work, give observed facts first, then unknowns and
likely next reads.

### Output Boundaries

Keep secrets, private personal material, auth tokens, and host-private details
out of output files and chat. Generated runtime outputs do not get provenance
notices. Provisional observations stay marked as recommendations or follow-up
requirements until accepted into the proper durable guidance surface.

## Module - repo scaffold core

### Scaffold Core Purpose

Repository scaffolding creates the starting shape for a new project or a named
structural rework. It establishes conventions that let later workers implement
inside the repo without guessing.

### Scaffold Project Boundary

A new repository is for a genuinely distinct project. Major rewrites,
experiments, mockups, repros, and alternate versions of an existing project use
a branch or worktree in the existing repository. Public is the default
visibility unless secrets, private data, unpublished third-party code, or an
explicit confidentiality constraint require private.

Local clones live under the ghq layout at `/git/<host>/<owner>/<repo>`. Use
`ghq` for finding or fetching clones and `gh` for GitHub repository objects.
Use `jj` for local history and pushing.

### Scaffold Initial Shape

Create only the guidance and build surfaces the accepted brief needs:
`AGENTS.md`, `INTENT.md` when psyche-stated project intent exists,
`ARCHITECTURE.md` when architecture is already known, repo-local `skills.md`
when the repo has specific working rules, build metadata, source layout, and
test entry points.

Do not invent product behavior, public APIs, storage schemas, deployment
promises, or role authority. Leave TODOs only for real downstream work that the
brief accepts.

### Scaffold Language Fit

Prefer the ecosystem already implied by the repo or brief. Rust scaffolds follow
the workspace Rust shape. Nix scaffolds expose checks through the flake rather
than ad hoc scripts. Names use full English words unless the surrounding
ecosystem has a canonical exception.

### Scaffold Handoff

Run the narrow scaffold check available: parser check, formatter, flake
evaluation, test discovery, or generated-output check. If the scaffold is
intentionally incomplete, name the missing piece and the first command expected
to pass once it exists.

## Module - code implementation core

### Implementation Core Purpose

Ordinary implementation turns an accepted brief into the smallest coherent
source change that fits the repository. The worker owns local understanding,
code edits, and verification evidence; broader product direction stays with the
brief or the psyche.

### Implementation Local Fit

Read repository instructions, intent, architecture, and the touched code path
before editing. Prefer existing language, framework, schema, and helper
patterns. Add an abstraction only when it removes real complexity or matches an
established local pattern.

Use full English names and typed domain objects. Avoid boolean control flags
where a closed record or enum can name the variants. Put behavior on the
data-bearing type that owns it. Where two enums meet, name the contact point
instead of scattering conditionals.

Beauty is a correctness gate: a special case should dissolve into the normal
case. If a fix works only by adding a side path that future agents must
remember, keep looking for the shape that makes the rule explicit.

### Implementation Version Compatibility

When behavior changes a public contract, storage schema, wire format, generated
surface, deployment slot, or operator workflow, update the relevant version or
state why none is needed. Preserve compatibility unless the brief explicitly
accepts a break.

### Implementation Verification

Run the narrowest meaningful check first, then broader checks when shared
behavior, generator output, or public interfaces changed. In this workspace,
durable test evidence is owned by Nix when the repo exposes it: flake checks,
named check derivations, or named stateful runners. Bare language test commands
are inner-loop evidence unless the repo says otherwise.

## Module - Rust core

### Rust Core Purpose

Rust work follows workspace Rust discipline without requiring a worker packet to
carry every Rust reference file. Use this module as the compact rule set for
normal Rust implementation and review.

### Rust Shape

Every non-test behavior is a method on a non-zero-sized data-bearing type or a
trait implementation. Avoid free helpers except `main` and required test
wrappers. Types carry domain meaning; a string, integer, or bool is not enough
when the value has a domain role.

Crate boundaries return the crate's typed `Error` enum. Use `thiserror` or an
equivalent explicit enum shape where the repo already does. Do not expose
`anyhow` or `eyre` as the boundary contract.

Use full English names. Do not prefix types with the crate name. Encode
direction in names when a type moves across a boundary.

### Rust Parsing Storage And Wire

Use a real parser for structured input. In this workspace that normally means
the NOTA codec for NOTA and `winnow` or an established parser library for other
grammars. Hand-rolled string splitting is review debt unless the input is truly
trivial and local.

Persistent state normally uses redb. Binary wire and durable schema objects use
rkyv where the surrounding component family already does. Keep storage schema,
wire contract, and generated type changes version-aware.

### Rust Actors And Components

Long-lived daemons, state engines, routers, watchers, delivery engines, and
database owners are actors when they own coherent state and lifecycle. In
Kameo-shaped code, the actor type itself carries the data, and each verb is a
typed message implementation rather than one untyped message enum.

Component work keeps the daemon, thin CLI, and signal-* contract distinct. A
CLI drives the daemon path; it does not recreate daemon state transitions by
opening the database directly.

### Rust Tests And Layout

Keep tests in crate-root `tests/` files when they are more than tiny unit
probes. Test-only binaries use the `-test` suffix. Witnesses exercise the
production boundary they claim to protect: parser, trait surface, actor
message, wire frame, daemon CLI, or storage reader.

## Module - Nix core

### Nix Core Purpose

Nix work in this workspace is reproducible, remote-addressable, and exposed
through named flake surfaces. This module carries the compact rule set for
implementation and audit packets.

### Nix Source And Inputs

Use portable flake inputs such as `github:<owner>/<repo>` for sibling
repositories. Pin exact revisions in `flake.lock`, not by hashes in
`flake.nix`. Do not commit `path:` or `git+file://` inputs or overrides; they
make builds depend on one machine's checkout.

For multi-repo testing, commit and push the participating refs, then use remote
`--override-input` values. Do not test a deployable stack through local
filesystem inputs.

### Nix Modules And Services

CriomOS services are NixOS modules or typed systemd services, directly on a host
or inside a contained node. Prefer declarative modules, package upstream sources
natively, and make secrets, state, users, ports, and checks visible in the Nix
shape.

Runtime compilation caches, generated configs, and build artifacts that affect
startup behavior belong in derivations when feasible, so rebuilds are
repeatable and cold starts do not depend on mutable user state.

### Nix Commands

Use Nix commands that prove the surface directly: `nix eval`, `nix flake show`,
`nix path-info`, `nix build`, `nix run`, and `nix flake check`. Do not search
the Nix store filesystem. Do not record raw store paths in durable prose as the
proof of correctness.

### Nix Tests And Safety

Expose durable checks as flake checks, named apps, packages, or scripts entered
through Nix. Stateful checks name their state directory and leave inspectable
artifacts. VM or live-host checks run only when the host is authorized for that
class of work.

Keep secrets transient. Do not put secret values in Nix store paths, logs,
reports, chat, commits, or generated outputs.
