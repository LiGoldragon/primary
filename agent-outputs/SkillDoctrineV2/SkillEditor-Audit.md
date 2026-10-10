# SkillDoctrineV2 Audit

## Task And Scope

Task: audit doctrine and role packet changes for SkillDoctrineV2, focused on
active `skills.nota` runtime-discovery references, role-bundle correctness and
bloat, composite-module shape, Pi generated packet consistency, generated-output
drift, and stale ungenerated source.

No source, generated output, commits, or pushes were changed. Historical
`agent-outputs/**` references were consulted as audit context, not treated as
active doctrine.

## Findings

### Medium: role packets still contain stale `skills/*.md` cross-references

Generated role packets include cross-references to `skills/beads.md`,
`skills/reporting.md`, `skills/intent-log.md`, `skills/spirit-cli.md`,
`skills/architecture-editor.md`, `skills/nota-design.md`,
`skills/actor-systems.md`, `skills/push-not-pull.md`, and
`skills/nix-discipline.md`. The current primary `skills/` directory contains
only `generated-role-outputs.nota`; the generated skill packets live under
`.agents/skills/` and `.claude/skills/`. These are not `skills.nota` references,
but they are stale runtime-path guidance inside active role packets.

Evidence:

- `/home/li/primary/.pi/agents/intent-translator.md:177` starts a required local
  skill loading list; lines `180-187` name `skills/*.md` paths.
- `/home/li/primary/.pi/agents/intent-translator.md:275` has a `See also`
  section with `skills/beads.md`, `skills/reporting.md`, and
  `skills/nota-design.md` on lines `277-279`.
- `/home/li/primary/.pi/agents/rust-auditor.md:727` has a `See also` section;
  lines `729-733` name `skills/actor-systems.md`,
  `skills/push-not-pull.md`, and `skills/nix-discipline.md`.
- Source owners are `/git/github.com/LiGoldragon/skills/modules/bead-weaver/full.md:9-19`
  and `/git/github.com/LiGoldragon/skills/modules/architectural-truth-tests/full.md:486-491`.
- `/home/li/primary/skills/` contains only `generated-role-outputs.nota`.

Suggested correction: update source modules to reference module/skill names or
generated harness skill surfaces, not primary `skills/*.md` paths; then
regenerate.

### Medium: auditor and repo-operator packets include implementation authority text

`rust-auditor`, `nix-auditor`, and `repo-operator` each include
`code-implementation-core`. Their role contracts say they do not implement the
original task or substitute for implementation, but the included module says the
worker owns “code edits” and instructs reading paths “before editing.” This is
authority bleed inside non-implementer packets.

Evidence:

- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:80-84`
  includes `code-implementation-core` in `rust-auditor`, `nix-auditor`, and
  `repo-operator`.
- `/git/github.com/LiGoldragon/skills/roles/rust-auditor/full.md:5-7` says the
  Rust Auditor does not implement the original task; lines `24-25` forbid
  rewriting unless authorized.
- `/git/github.com/LiGoldragon/skills/roles/nix-auditor/full.md:5-7` says the
  Nix Auditor does not implement the original task; lines `22-24` forbid
  rewriting unless authorized.
- `/git/github.com/LiGoldragon/skills/roles/repo-operator/full.md:5-7` says the
  Repo Operator does not substitute for implementation or audit; lines `27-28`
  route implementation fixes back unless authorized.
- `/home/li/primary/.pi/agents/rust-auditor.md:204-216`,
  `/home/li/primary/.pi/agents/nix-auditor.md:199-212`, and
  `/home/li/primary/.pi/agents/repo-operator.md:192-204` include
  implementation-module wording that assigns code edits and editing workflow to
  those roles.

Suggested correction: split the verification/versioning/review-useful parts
from `code-implementation-core` into a neutral code-review or code-evidence
core for auditors and repo operator, or omit that module from non-implementer
role bundles.

### Low: stale V1 wording remains in active V2 role source and generated packets

The active manifest has V2-style included modules, and generated packets are
V2 role doctrine bundles, but `role-intent-translator` still says “this V1
packet set.” This is not a runtime behavior blocker, but it is stale doctrine
wording in an active generated packet.

Evidence:

- `/git/github.com/LiGoldragon/skills/roles/intent-translator/full.md:35-37`
  says the lead/orchestrator is not a spawned worker role in “this V1 packet
  set.”
- The same wording appears in `/home/li/primary/.pi/agents/intent-translator.md:40`
  and `/home/li/primary/.claude/agents/intent-translator.md:40`.

Suggested correction: replace “this V1 packet set” with “the generated worker
packet set” or equivalent source wording, then regenerate.

### Low: manifest/index comments still label the system V1

The active records are V2-style, but source comments still say V1. Because the
data records are correct and generated checks pass, this is a stale-comment
cleanup, not a generated-output blocker.

Evidence:

- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:1` says
  “Active generated output manifest for V1 skill and role packet generation.”
- `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota:1`
  says “Dependency-only module index for V1 generation.”

Suggested correction: update comments to describe current manifest-driven skill
and role packet generation.

### Low: `rust-auditor` remains substantially larger than other role packets

Most generated role packets are roughly 7.6k-13.4k bytes, while
`rust-auditor` is 33.6k bytes because it includes the full
`architectural-truth-tests` skill. This matches the handoff’s acknowledged
tradeoff and is audit-specific, so it is not blocking. It is still the obvious
remaining bloat target.

Evidence:

- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:80` includes
  full `architectural-truth-tests` in `rust-auditor`.
- `/home/li/primary/.pi/agents/rust-auditor.md:244` starts the embedded full
  skill; it runs through line `734`.
- `wc -c /home/li/primary/.claude/agents/*.md` showed `rust-auditor.md` at
  `33602` bytes; the next largest packet was `repo-scaffolder.md` at `13437`
  bytes.

Suggested correction: extract a slim audit witness core if this packet size is
judged too heavy; otherwise accept as a deliberate V2 exception.

## Non-Findings

No blocking issue found.

No active instruction to use `skills.nota` or runtime skill-index discovery was
found in primary boot docs, active skill source modules, role source modules, or
generated role/skill packets. The only active match was the boot-contract
prohibition at `/home/li/primary/AGENTS.md:14`: “Do not perform runtime
skill-index discovery.”

The new slim composite modules are self-contained teaching packets rather than
mere indexes. The focused scan found scoped module headings and no `See also`,
`skills/`, “index into,” or required-reading chains in the new core modules.

Pi generated role packets are consistent with Claude generated role packets for
the same generated role names. `cmp` reported no differences between each
`/home/li/primary/.claude/agents/<role>.md` and
`/home/li/primary/.pi/agents/<role>.md`. The project `scout` packet exists, so
the known bundled Pi `scout` name is shadowed in this workspace. The broader
Pi concern about unshadowed bundled builtins remains a policy issue from the
scout map, not a generated packet mismatch found here.

`skills-check.nota` passes for the current skills repo working copy against
`/home/li/primary`.

## Checks Run

- Read `/home/li/primary/.agents/skills/skill-editor/SKILL.md`.
- Read the supplied handoffs:
  `/home/li/primary/agent-outputs/ReplaceRuntimeDiscoveryDoctrine/SkillEditor-Handoff.md`,
  `/git/github.com/LiGoldragon/skills/agent-outputs/V2RoleDoctrineBundles/SkillEditor-Handoff.md`,
  and
  `/git/github.com/LiGoldragon/skills/agent-outputs/SkillDoctrineV2/SkillEditor-Handoff.md`.
- Read proposal/context files under `/home/li/primary/agent-outputs/SkillDoctrineV2/`.
- Read `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota` and
  `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota`.
- `rg -n "skills/skills\\.nota|skills\\.nota|Skill Index|skill index|runtime discovery|runtime-discovery|discovery index|discovery-index|perform runtime skill-index discovery|skill-index discovery" ...`
  over primary boot docs, generated skill packets, generated role packets,
  source modules, source roles, README/architecture, and manifests: only
  `/home/li/primary/AGENTS.md:14` matched, as a prohibition.
- `find /home/li/primary/.claude/agents /home/li/primary/.codex/agents /home/li/primary/.pi/agents -maxdepth 1 -type f -print0 | xargs -0 wc -l | sort -n`:
  role packet line counts inspected; `rust-auditor` is the outlier at 734 lines
  for Claude/Pi.
- `wc -c /home/li/primary/.claude/agents/*.md`: byte-size check; `rust-auditor`
  is `33602` bytes.
- `cmp -s` for each generated Claude/Pi role pair: no differences reported.
- `rg -n "V1|V2|runtime discovery|skills\\.nota|skills/" ...` over source
  roles, new core modules, Claude/Pi generated role packets: found stale V1
  wording and stale `skills/*.md` cross-references, but no `skills.nota`.
- `rg -n "generated from|DO NOT EDIT|Generated by|This file was generated" ...`
  over generated role packets: no generated-file provenance notices found; the
  generic word “provenance” only appears inside doctrine forbidding provenance
  notices.
- `rg -n "^# Skill —|^# Module|^# Role|See also|read .* below|links|index into|points at|load .*skills|skills/" ...`
  over the new slim core modules: no index-style or stale-path references found
  beyond module headings.
- `test ! -e /home/li/primary/skills/skills.nota`: passed; retired generated
  file is absent.
- `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run --
  skills-check.nota` from `/git/github.com/LiGoldragon/skills`: passed.

