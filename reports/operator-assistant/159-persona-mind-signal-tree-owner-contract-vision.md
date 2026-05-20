# PersonaMind Signal Tree And Owner Contract Vision

## What Landed

I updated the shared vocabulary:

- `AGENTS.md` now says the component triad is daemon/runtime repo plus
  working signal plus policy signal. The CLI is the daemon's bundled
  thin first client, not a triad leg.
- `skills/component-triad.md` now carries the same vocabulary in
  fuller form: working signal, policy signal, signal types, signal
  tree, policy state, working state.

I created and pushed `owner-signal-persona-mind`:

- Local checkout:
  `/git/github.com/LiGoldragon/owner-signal-persona-mind`
- Primary symlink:
  `/home/li/primary/repos/owner-signal-persona-mind`
- Remote:
  `https://github.com/LiGoldragon/owner-signal-persona-mind`
- Commit:
  `d20d72cc owner-signal-persona-mind: scaffold policy contract`

The scaffold is intentionally narrow. It is a contract crate, not a
runtime. It declares:

- `Configure(Configuration)`
- `Inspect(Inspection)`
- replies `Configured`, `PolicySnapshot`, `ConfigurationRejected`,
  and `RequestUnimplemented`

Checks run:

- `cargo fmt --check`
- `cargo test`
- `nix flake check --max-jobs 0`

## Why The Owner Surface Starts Narrow

The clear intent is that PersonaSpirit owns PersonaMind and that every
stateful component has an owner-only policy/configuration contract.

The unclear part is the concrete Spirit-to-Mind verb set. The existing
intent gap analysis already names this as high severity: Spirit owns
Mind, but the workspace has not settled which owner verbs Spirit issues.

So I did not encode a large speculative authority surface. The new repo
only gives Mind a policy signal skeleton that can compile, round-trip,
and receive future verbs without starting from zero.

## Current PersonaMind Working Signal Problems

`signal-persona-mind` still carries the older mixed signal tree.

The current request enum mixes at least three relations:

- typed mind graph: thoughts and relations;
- work/memory graph: openings, notes, links, status, aliases, queries;
- channel choreography: adjudication, channel grants, extension,
  retraction, denial, listing.

That is already a naming smell. A single mega `MindRequest` enum makes
the crate boundary look simpler than the actual relation model.

The worst part is channel choreography. Names such as `ChannelGrant`,
`ChannelExtend`, `ChannelRetract`, and `AdjudicationDeny` hide
direction. If Mind is the authority, then:

- router-to-mind should submit an adjudication observation/request;
- mind-to-router should issue owner orders through
  `owner-signal-persona-router`, not through `signal-persona-mind`.

So the current tree likely conflates two different boundaries:

- ordinary inbound observation/query to Mind;
- outbound authority orders from Mind to Router.

The names exposed that flaw.

## Target Shape I Would Aim For

`owner-signal-persona-mind` should stay policy-shaped:

- `Configure(Configuration)`
- `Inspect(Inspection)`
- future Spirit-to-Mind verbs only after the owner discipline
  crystallizes.

It should not carry ordinary `Thought`, `Relation`, work item, or note
mutations. Those are working-signal concepts.

`signal-persona-mind` should be refactored toward relation-shaped
operation roots:

- typed mind graph: one `Submit(Submission)` operation whose payload
  is a closed sum of `Thought` or `Relation`; one `Query(Query)` whose
  payload names the read target.
- work/memory graph: `Open`, `Annotate` or `Note`, `Link`,
  `ChangeStatus`, `AssignAlias`, and `Query`.
- subscriptions: mandatory `Tap`/`Untap` for Persona introspection;
  domain-specific graph watches can stay only if they are truly
  working-domain subscriptions, not the universal observer hook.
- channel choreography: keep only the inbound router-to-mind shape
  here, likely `Adjudicate(Adjudication)` or `Submit(Adjudication)`.
  Move grant/extend/revoke/deny authority orders to the router owner
  signal.

The rule I would enforce during the refactor: an operation root must
tell who is acting at this boundary. If the name only says the noun
being affected, it probably hides direction and authority.

## Naming Notes

`SubmitThought` and `SubmitRelation` are not terrible, but they are
operation-plus-payload fused into variant names. The cleaner tree is:

- operation root: `Submit`
- payload: `Submission::Thought(Thought)` or
  `Submission::Relation(Relation)`

`QueryThoughts`, `QueryRelations`, and `ChannelList` should not remain
three unrelated root shapes. They are read operations with different
targets. Prefer:

- operation root: `Query`
- payload: `Query::Thoughts`, `Query::Relations`,
  `Query::Channels` if channels remain on Mind's ordinary surface

`SubscriptionRetraction` is a noun, not a boundary action. Under the
current three-layer direction, universal observation closes with
`Untap`. If Mind still needs graph-domain subscriptions, use a
domain verb such as `Watch` / `Unwatch`, and keep it distinct from
the mandatory introspection hook.

`RoleName` in `signal-persona-mind` is stale relative to the dynamic
role/lane direction. Future Mind graph records should not bake the old
closed role set into durable thought/work schema unless the role record
is historical. Active dynamic roles should use the orchestrate-owned
role identifier vocabulary.

## Questions

1. Should `owner-signal-persona-mind` eventually carry a concrete
   Spirit-to-Mind intent synchronization verb, or should Spirit's
   influence first enter as owner policy only? The scaffold currently
   models synchronization as policy configuration, not as a record
   ingestion operation.

2. Does Mind lifecycle control belong to PersonaSpirit's owner signal,
   or to the infrastructure supervisor only? I did not add `Start`,
   `Stop`, `Suspend`, or `Resume` because the supervisor-vs-Spirit
   authority line is still ambiguous.

3. Should the Mind-to-Router grant/extend/revoke/deny family move to
   `owner-signal-persona-router`? My answer is yes; keeping those
   operations in `signal-persona-mind` reads like the router is calling
   Mind to perform Mind-local state changes, when the actual authority
   direction is Mind ordering Router.

4. When refactoring `signal-persona-mind`, should we wait for the macro
   to support multiple relation families inside one contract crate, or
   should we encode relation separation now with sum payloads under
   unique operation roots such as `Submit`, `Query`, `Watch`, and
   `Unwatch`?
