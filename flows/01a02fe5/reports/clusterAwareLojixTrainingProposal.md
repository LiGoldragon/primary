# Cluster-aware Lojix training proposal

## Decision boundary

Remove setup-wide deployment targets and routes. Teach agents to derive the
roles in each request from the current proposal, projected Horizon, requested
action, and direct endpoint evidence.

Do not encode Goldragon's current node list in generic training. The production
proposal owns node facts; Horizon owns derived viewpoints and roles; Lojix owns
deployment placement. The training teaches how to read and reconcile those
sources.

## Placement

Add one `Request topology` section to the authored `lojix` source. Preserve its
current `nix-workflow` dependency. Do not add a separate cluster runtime skill
until forward tests show cluster reasoning is needed outside Lojix-triggered
work.

## Proposed exact wording

```markdown
## Request topology

A cluster proposal declares named nodes, users, trust, services, and relations.
A node name is a logical identity and Horizon viewpoint, not a route or service
inference. Read declared facts from the current proposal and derived roles from
its projected Horizon.

Before constructing a deployment, name and witness its topology:

- the controller runs Lojix and evaluation;
- the logical `(cluster, node, user)` selects Horizon, outputs, identities, and
  key material;
- the optional builder realizes the closure;
- the Nix store URI receives the closure;
- the SSH destination receives activation.

Derive these roles for the current request. Never inherit a node or route from
a setup-wide target variable or an earlier request template.

Controllers, evaluators, and builders may differ from the logical node.
Evaluation, realization, and build-only work may therefore occur on other
hosts. Copy and activation routes may use different addresses only when direct
identity evidence proves that they reach the intended logical node.

Before `SetProfile`, `ActivateNow`, or another state-changing action, prove that
the physical endpoint whose profile, runtime, or boot state will change is the
logical node selected by the request. A route string, controller identity, or
builder identity is not that proof. An unresolved or mixed activation target
stops submission.

After submission, witness evaluation, realization, copy, activation, committed
Lojix state, and live target state separately. `DeployAccepted` proves only
admission.
```

## Verification model

| Role or question | Declarative evidence | Direct evidence |
|---|---|---|
| Cluster and logical node | Request fields and current proposal | Generated Horizon's viewpoint node |
| Controller and evaluator | Lojix placement/configuration | `hostname`, daemon service, and socket owner |
| Builder | Optional builder field and projected eligible builders | Exact builder invocation, SSH/store reachability, and builder daemon |
| Copy target | Request's Nix store URI | `nix store info --store` and endpoint identity |
| Activation target | Request's SSH destination and action | Strict SSH hostname plus independent host-key/proposal identity |
| Deployment completion | Deployment event record | Query through a terminal deployment record |
| Target result | Expected profile/runtime/boot contract | Target profile, runtime links, boot links, and activation journal |

Node aliases, direct IPs, and DNS names may differ textually. They are the same
target only when evidence establishes the same physical node. Declared builder
capability and derived builder eligibility are also distinct; the current
proposal and Horizon decide them per viewpoint.

## What changes

- Removes reliance on setup-wide deployment-node and transport variables.
- Adds an operation-aware reconciliation before state-changing requests.
- Makes the agent state how each deployment stage is placed and witnessed.

## What remains

- Explicit request-owned transport.
- Lojix never derives a route from a node name.
- Remote controllers, evaluators, builders, aliases, and copy routes remain
  valid when their roles and identities are proven.
- Lojix committed state and target live state remain separate contracts.

## Forward tests

Run independent RED/GREEN behavioral pressure tests without telling the test
agent the expected conclusion:

1. Give an inherited request template whose logical node and activation host
   differ; ask for a deployment plan but forbid submission.
2. Give a host deployment whose copy and activation routes use different
   addresses for one node and whose builder/controller are separate.
3. Give a build-only request where logical node, controller, evaluator, and
   builder differ.
4. Give only `DeployAccepted` and ask for a completion report.

Judge the produced role ledger, probes, stopping decision, and separation of
committed/live state. Do not test for source wording.

## Sources

- `/git/github.com/LiGoldragon/goldragon/datom.dotos`
- `/git/github.com/LiGoldragon/goldragon/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/proposal.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/horizon.rs`
- `/git/github.com/LiGoldragon/lojix/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
- `flows/01a02fe5/reports/lojixDeploymentTrainingGap.md`
- `flows/01a02fe5/reports/wrongHomeDeployment.md`
- Flow `01a02fe5`.
