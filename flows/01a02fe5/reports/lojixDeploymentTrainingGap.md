# Lojix deployment training gap

## Why deployment 49 used Zeus on Ouranos

The visible user requests authorized installing Herdr and Orca in Home and
deploying the update. They did not name Zeus. The submitting subflow inherited
a deployment setup whose shared variables combined:

- logical deployment node `zeus`;
- controller node `ouranos`;
- Nix store transport `ssh-ng://li@ouranos`;
- SSH activation destination `li@ouranos`.

The parent flow described the resulting mixed Home request as an existing
template. The child reused it for deployment 49. Lojix then did exactly what
the request said: it evaluated Zeus and activated the result on Ouranos.

The exact root-to-child assignment and follow-up payloads are encrypted, so it
is unknown whether they explicitly repeated Zeus. The visible parent request
and approvals did not.

## Training deficiency

The authored Lojix training says that node identity and supplied transports are
independent and that Lojix does not derive routes from node names. It contains
no operation-specific rule requiring a profile-changing activation target to
be reconciled with the logical node. The submitting agent therefore violated
no explicit training prohibition.

The global variable names also made composition unsafe: `DeploymentNode` was a
Zeus value while the generic deployment transport variables named Ouranos.
They did not say which operation each value was valid for or require proof that
the transported activation still reached the logical node.

## Invariant anatomy

- The logical node selects Horizon projection, node-specific outputs,
  identities, and keygrips.
- A daemon/controller and a Nix builder may be different physical hosts from
  the logical node for query, evaluation, realization, or build-only work.
- Copy and activation routes may use different DNS names or direct IPs only
  when evidence establishes that they reach the same physical logical node.
- `UserEnvironment SetProfile`, `UserEnvironment ActivateNow`, and host
  activation actions cross the physical-state boundary. Before submission,
  training must require reconciliation of the logical node with the physical
  endpoint whose profile or system will change.
- A mismatch at that boundary must stop for correction or explicit design
  authority; it must not be inherited from a generic template.

## Code boundary

Current Lojix validates route shape and login authority but does not validate
logical-node/endpoint identity. Better training can prevent request
construction errors immediately. A typed engine guardrail is a separate design
decision because cross-node controllers, builders, and staging operations are
legitimate.

## Sources

- `/home/li/primary/SKILL_VARIABLES.md`, deployment variables.
- `/home/li/.codex/sessions/2026/08/23/rollout-2026-08-23T17-00-36-01a02f23-46a6-7573-94cb-54420597526d.jsonl`, ordinals 2019, 2056, and 2081.
- `/home/li/.codex/sessions/2026/08/23/rollout-2026-08-23T21-12-06-01a03009-87e6-7231-8d15-58a80bcbc94f.jsonl`, ordinals 91, 175, 789, and 790.
- `flows/01a02fe5/reports/wrongHomeDeployment.md`.
- `flows/7a9f4c12/witnesses/reachability.md`.
- `flows/01a02b46/vision/zeusUpdate.md`.
- Authored Lojix skill and `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`.
- Flow `01a02fe5`.
