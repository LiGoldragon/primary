# Review Mind Router Policy

Report kind: review
Topic: PersonaMind, Router authority, and observation policy shape
Date: 2026-05-22
Lane: second-operator

## What This Review Supersedes

This report supersedes:

- `reports/second-operator/138-persona-mind-gap-close-2026-05-16.md`
- `reports/second-operator/159-persona-mind-signal-tree-owner-contract-vision.md`
- `reports/second-operator/160-owner-signal-persona-router-channel-authority.md`

It also carries forward the Router/Mind policy parts of:

- `reports/second-operator/131-persona-router-gap-close-2026-05-16.md`
- `reports/second-operator/135-phase3-push-subscription-chains-2026-05-16.md`

## Current Direction

PersonaMind should not be a dumping ground for every work, channel,
role, and router action. Its working signal still needs a signal-tree
cleanup around relation boundaries.

The target split:

- Mind working signal: ordinary mind graph and memory/work graph
  operations.
- Mind owner signal: PersonaSpirit-owned policy and configuration.
- Router working signal: ordinary router observation/query surface.
- Router owner signal: router channel authority orders.
- Orchestrate owner signal: the authority bridge that receives Mind's
  decision and orders Router.

The settled authority chain for channel policy is:

```text
Mind -> owner-signal-persona-orchestrate -> owner-signal-persona-router
```

Mind does not call Router's owner signal directly.

## Current Repos

`owner-signal-persona-mind` exists and is intentionally narrow. It
currently has policy-shaped `Configure` and `Inspect` style surface, not
ordinary Thought or Relation mutations.

`owner-signal-persona-router` exists and carries channel authority
orders:

- `Grant`
- `Extend`
- `Revoke`
- `Deny`

`signal-persona-mind` has already shed the moved authority orders:

- `ChannelGrant`
- `ChannelExtend`
- `ChannelRetract`
- `AdjudicationDeny`
- their receipt types

Mind still carries the inbound Router-to-Mind adjudication shape and
some channel read-side vocabulary.

## Signal-Tree Shape To Aim For

Mind working operations should name the boundary action, not fuse the
payload into the operation root.

Better shape:

- `Submit(Submission)` where `Submission` is a closed sum such as
  `Thought`, `Relation`, or another mind-owned submission.
- `Query(Query)` where `Query` names the read target.
- `Watch` and `Unwatch` only for domain graph subscriptions, if those
  truly differ from generic `Tap` and `Untap`.
- `Adjudicate` or `Submit(Adjudication)` for inbound router-to-mind
  adjudication, if Mind remains the decision point.

Avoid:

- `SubmitThought` and `SubmitRelation` as separate roots when a single
  submit relation is clearer.
- noun-only operation roots that hide direction.
- putting Router authority writes back into the Mind working signal.
- baking old closed `RoleName` enums into future active Mind records
  after Orchestrate owns dynamic role and lane identity.

## Live Questions

The concrete Spirit-to-Mind owner verb set is still not settled. Do not
invent it while doing Orchestrate executor migration. Keep
`owner-signal-persona-mind` narrow until the policy relation is clear.

`ChannelList` needs a future decision. It can stay temporarily on the
Mind read side only if it is a Mind view. If it represents Router grant
state, move the read to Router's working or owner-adjacent surface.

`AdjudicationRequest` needs a future decision. It can remain
Router-calls-Mind if Mind is a service deciding adjudications. If the
mandatory observable surface makes it an event stream, it may become a
Router observation consumed by Mind instead.

The `primary-hj4.1.4` bead for persona-mind post-commit subscription
delta delivery is real, but it should wait for the policy and graph
subscription boundaries to be clear enough that push delivery does not
solidify the wrong signal tree.

## Relation To Orchestrate

This report matters to Orchestrate only when owner policy expands.
`primary-c620` can migrate the existing Orchestrate operations to the
executor substrate without solving every Mind/Router policy question.

When owner-signal-persona-orchestrate grows, it should model Mind's
channel decision as a first-class owner command or policy request,
then emit Router owner orders. It should not hide that chain in a
string field or direct Mind-to-Router shortcut.

