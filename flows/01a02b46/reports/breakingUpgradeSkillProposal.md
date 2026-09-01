# Breaking-upgrade deployment documentation skill proposal

## Result

Proposal only. No Curriculum source, manifest, generated tree, repository
source, deployment, or runtime state was changed.

The terminal-best shape is one generic Workflow/Mechanism skill whose active
procedure belongs to the repository that owns the deployment boundary. Lojix
syntax and Nix mechanics remain in their existing skills; this skill joins
their repository facts into one transition-specific procedure and requires
that procedure to be corrected before a failed or partial retry.

## Exact proposed source

Proposed file: `Curriculum/skills/breaking-upgrade-deployment.md`

```markdown
---
description: A producer or consumer change breaks the live deployment contract and the target must cross incompatible revisions.
dependencies: [documentation-placement, flows, repository-lifecycle, testing, versioning]
---

Identify the incompatible producer and consumer contracts, the repositories that own them, the last live revision, candidate immutable revisions, the deployment boundary, and rollback authority before changing code.

Keep one active procedure in the deployment-owning repository at `docs/deployment/breaking/<upgrade-id>.md`.

The procedure takes the contract delta, immutable producer and consumer revisions, deployment proposal, transport, backend, action, preflight baseline, independent postconditions, stop conditions, and retry authority as inputs.

It outputs an ordered producer-to-consumer-to-live procedure with links to each repository fact, exact gates, and a record format for attempts.

Create and land the procedure before changing the consumer. Push and verify the producer before the consumer updates its lock or package, and push the consumer with the complete procedure before live deployment.

Use the owning deployment interface and its typed contract; do not add a parallel script, flag, hot fix, or compatibility path.

Keep deployment facts in the owning repository's source, manifests, variables, and checks; point to them with stable relative links and state only this transition's order and gates.

Capture a read-only baseline before an effectful stage and observe each stage to a terminal result. Report durable deployment state, realized closure, live state, and persistent boot or profile state separately.

If an attempt fails or partially changes the target, stop and record the exact request, source revision, stage, terminal result, live observations, durable observations, and unknowns in the repository's established evidence or report surface. Mark the record evidence-only.

Correct the active procedure from that evidence before retrying. A retry uses the corrected procedure and new immutable source or procedure revisions; if no correction is needed, state why and retain the failed-attempt link. Do not infer rollback, retry, or recovery authority.

Keep historical attempt records immutable and linked from the active procedure. Replace obsolete active instructions in the one canonical procedure; never leave competing procedures or turn an attempt report into an instruction.

Do not duplicate `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, or flow reports. Link to their facts and to flow witnesses; the procedure is only the deployment-specific ordering and gates.
```

The frontmatter dependencies are deliberately generic. A Lojix deployment
also loads `lojix` and `nix-workflow` when those triggers apply; coupling this
new skill to Lojix would make unrelated breaking deployments load a daemon
contract they do not use.

## Boundary and placement

The trigger is an incompatible producer/consumer contract that must cross a
live deployment boundary. This is distinct from `nix-input-upgrade`, which
maps and pins ordinary Nix input changes, and from `lojix`, which defines the
typed deployment mechanism. It is not a general deployment guide, a release
note, a migration narrative, or a replacement for repository instructions.

The recommended canonical active location is one file in the deployment-owning
repository:

`docs/deployment/breaking/<upgrade-id>.md`

`<upgrade-id>` names the contract transition, not a host or an attempt. The
repository's documented evidence/report surface holds immutable attempt
records, marked evidence-only and linked from the active procedure. For
CriomOS this means the existing `reports/` surface, not a second `docs/`
runbook. The active procedure remains the only operational instruction.

The procedure is created before the consumer changes, after the producer
contract is understood, and is complete with pushed immutable references
before live deployment. Producer, consumer, and live deployment evidence are
separate gates. The procedure may be corrected after each source or live
observation, but no retry uses stale active text.

## Manifest placement

Add this source identity to `manifests/module-dependencies.dotos`:

```text
{breaking-upgrade-deployment skills/breaking-upgrade-deployment.md RuntimeSkill}
```

Place it beside the existing `documentation-placement` and other Workflow
mechanism rows.

Add this active output to `manifests/active-outputs.dotos`:

```text
Skill.{breaking-upgrade-deployment breaking-upgrade-deployment Workflow Mechanism [AgentsSkill ClaudeSkill]}
```

Place it beside the existing `documentation-placement` active output.

Do not add a target insertion, universal role module, or skill composition.
The source frontmatter owns description and dependencies; the manifests own
source identity, output identity, category, tier, and target surfaces.

## Lojix 0.18→0.19 instantiation

The transition identifier would be
`lojix-0.18-to-0.19-boot-contract`.

The deployment-owning procedure would be proposed at:

`/git/github.com/LiGoldragon/CriomOS/docs/deployment/breaking/lojix-0.18-to-0.19-boot-contract.md`

The procedure would point rather than copy:

The producer's pushed immutable `lojix` 0.19.0 commit is
`0105f8d8f18dd91291e0a0fbe828e84ceda65714`; the producer package version and
boot contract are facts in that repository's `Cargo.toml` and source.

The consumer's pushed CriomOS commit is
`02ac43b193efd7ee542ab1a4d0594c76292edc53`, with the exact producer pin in
`flake.lock`. The test-cluster consumer pin is
`6e34f9e5db7dfa3c13209812b5a4270268a45ff3`; its checks are evidence for the
test surface, not proof of a live host deployment.

The procedure would link to CriomOS `AGENTS.md` for the four Lojix-materialized
inputs and lock-before-deploy rule, CriomOS `ARCHITECTURE.md` for the
deployment convergence surfaces, and the `lojix` skill for the typed
`Deploy.Host` request and terminal query. It would name the exact target,
proposal, transport, backend, action, and source revision from deployment
variables and the caller's approved request, never copy those values into a
generic skill.

Its order would be: prove the producer contract and suite; push it; pin and
verify it in CriomOS and its required consumers; push the complete procedure
with the consumer; then run Lojix Evaluate, Realize, and the explicitly chosen
host action, observing each to terminal state and checking live and persistent
boot projections independently.

The current flow annotation claims that Lojix 0.19.0 and the two consumer
pins landed, while no deployment, activation, reboot, EFI mutation, or garbage
collection occurred. That is a claim preserved in the flow record, not a live
deployment witness. The procedure therefore remains required before any
0.18→0.19 live request.

If the crossing fails or partially changes a host, the attempt record would
link the relevant flow witness and preserve the Lojix terminal state beside
live profile, daemon, and boot observations. The active procedure would then
be corrected before retry. The existing Ouranos 0.17.5→0.18.0 witnesses show
why this matters: a terminal `ActivateFailed` can coexist with a new live and
persistent system, and a healthy successor daemon does not establish durable
`Current`.

## Preserved and excluded material

The active procedure preserves only the transition-specific sequence, gates,
exact immutable references, postconditions, and correction links. Source
contracts remain in producer and consumer code, schemas, checks, manifests,
and variables. Repository operating rules remain in `AGENTS.md`; system shape
and invariants remain in `ARCHITECTURE.md`; user-facing use remains in
`README.md`; flow reports and witnesses remain historical evidence.

An attempt record is evidence-only. It may say what happened, link the exact
request and witnesses, and identify unknowns; it must not contain a second
copy of the procedure. Superseded procedures are not kept as active aliases;
the current file is corrected in place, while old attempt records remain
immutable and linked.

## Unresolved choices for the living

1. Confirm that the deployment-owning repository is the sole canonical home
   for a cross-repository breaking procedure (recommended), rather than
   requiring copies or links in every producer and consumer repository.
2. Confirm whether historical attempt records should use each repository's
   established `reports/`/witness surface (recommended) or a fixed adjacent
   `docs/deployment/breaking/.../attempts/` tree.
3. Confirm whether retry or recovery authority is inherited from the owning
   deployment skill or must be explicitly re-approved for every partial live
   attempt. This proposal leaves it unresolved and never infers it.
4. Confirm that the new skill remains Lojix-agnostic and composes with
   `lojix`/`nix-workflow` only for the current instantiation (recommended).

## Sources

`/home/li/primary/flows/01a02b46/vision/zeusUpdate.md` — exact 2026-08-23
12:46:07 ruling requesting this proposal and requiring correction after failed
or partial practice.

`/home/li/primary/flows/01a02b46/annotations.md` — current flow annotation
claiming Lojix 0.19.0 and consumer pins landed without runtime deployment.

`/home/li/primary/flows/01a02b46/reports/lojixSelfUpgrade.md` — staged
0.17.5→0.18.0 crossing order and independent terminal/live checks.

`/home/li/primary/flows/01a02b46/reports/ouranosLojixSelfUpgradeFinal.md`
and `ouranosClaviFaberRecovery.md` — partial activation witnesses where live
state and durable Lojix state diverged.

`/home/li/primary/flows/01a02b46/witnesses/ouranosLojixSelfUpgradeExecution.md`
and `ouranosClaviFaberRecovery.md` — method-bearing live observations.

`/git/github.com/LiGoldragon/Curriculum/skills/{documentation-placement,flows,lojix,nix-workflow,repository-lifecycle,skill-designing,testing,versioning}.md`
— authored placement, flow, deployment, Nix, lifecycle, design, proof, and
versioning guidance.

`/git/github.com/LiGoldragon/Curriculum/manifests/{module-dependencies,active-outputs}.dotos`
and `Curriculum/ARCHITECTURE.md` — manifest ownership and active output shape.

`/git/github.com/obra/superpowers/skills/{writing-skills,systematic-debugging,verification-before-completion}.md`
and `/git/github.com/anthropics/skills/skills/skill-creator/SKILL.md` — prior
art for minimal trigger descriptions, evidence-led correction, and
skill-authoring boundaries.

`/git/github.com/LiGoldragon/CriomOS/{AGENTS.md,ARCHITECTURE.md,README.md}` —
deployment ownership, documentation layers, and deployment convergence facts.

`/git/github.com/LiGoldragon/lojix/{Cargo.toml,src/schema_runtime.rs}` at
`0105f8d8f18dd91291e0a0fbe828e84ceda65714` — producer version and current boot
contract source witness.
