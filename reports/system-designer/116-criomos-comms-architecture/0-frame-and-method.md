# 116 — CriomOS communication architecture — frame and method

*The psyche opened a per-agent-microVM + per-system-router communication model in a
live design discussion ("the networking belongs in router … the router can be
per-system … it's how things talk across sandboxes and network … a sandbox is a
microvm, one per agent, since all spaces become smart in criomos"). This meta-report
grounds that model against the actual repos and brings back the decisions. It builds
on the criome auth pilot (reports 112–114) and the SO audit (225 / report 115).*

## Files

- `0-frame-and-method.md` — this file: the model, method, and the one research gap.
- `1-grounded-architecture.md` — the architecture grounded in code: components,
  transport tiers, the e2e flow, and the message/router relationship.
- `2-decisions-and-security-prerequisites.md` — **the deliverable**: the
  critique-corrected, psyche-facing decisions, the load-bearing security
  prerequisite, and the staged plan.

## The model (psyche, verbatim fragments)

CriomOS = a mesh of per-agent smart microVM sandboxes. ONE router per system. The
router is the communication fabric: cross-sandbox locally **and** cross-network
(router↔router). criome = auth/identity; router = transport; mirror = object
version-control; spirit = intent.

## Method

A seven-agent designer workflow (`wf_8622d8c2-d09`): five grounded readers
(router/message current state · microVM substrate + cloud-designer e2e · criome auth
for cross-router trust · mirror object flow · intent-fit/supersession) → one
architecture synthesis → one adversarial critic. All claims carry file/record
evidence; `2-…` reflects the **critic-corrected** decisions, not the raw synthesis.

## Research gap (one reader died)

The `mirror-object-flow` reader failed on an API socket error, so the object-fetch
half is grounded only through the synthesis + critic (who read mirror directly:
`mirror/src/service.rs`, INTENT `rj9y`, the green `end_to_end_arc.rs`). The mirror
findings below are real but thinner than the router/criome/substrate findings; a
follow-up mirror-specific pass is worth doing before the object-propagation leg is
built.

## The single most important correction

The critic found the load-bearing gap is **not** transport and **not** even BLS: it
is that **criome's identity registry has no admission control** (`IdentityRegistration`
carries no signer field; `register()` only dedups — `criome/src/actors/registry.rs:90`).
Any principal reaching criome's working socket can register an arbitrary identity↔key,
so the entire cross-router trust chain rests on an unauthenticated call, and the
first cross-system trust edge is circular/un-establishable today. This is the #1
prerequisite — ahead of networking, ahead of BLS — and the decision the synthesis
omitted. It is now decision **A** in `2-…`.
