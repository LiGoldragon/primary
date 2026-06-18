# 680 · Telos integrated PoC — the differentiator subscription/fan-out (Fork A)

The integrated agreement-machine PoC: admit a contract, evaluate it under a
membership-scoped quorum, stamp it with a crystallized-past moment, pulse the
*reference* (not the payload), and fan that reference out to subscribed
components by a single shared **component-differentiator** vocabulary. Plus the
contract-scheduled heartbeat. Grounded in the deployed shapes, not invented from
scratch.

Spirit grounding: `p3td` (quorum is the universal primitive, scoped by
membership), `m0p2` (object-update pulse pushes references; heartbeat = accept a
contract with an after-time condition, schedule a later check, fire a
quorum-signed acceptance if no intervening events), `ay3y` (every quorum-signed
object carries an `AttestedMoment` — crystallized past), `z9d6`
(content-addressed composable objects), `gc0n` (adjudicator ladder), `wckt`
(criome auth-only; router transports).

## 0 · The key finding: the differentiator already half-exists

The psyche asked for "a more universal contract which is mostly an enum with all
the components ... a differentiator for all the different components." That enum
is **already in the deployed schema** — it just hasn't been *named* as the
fan-out key or wired through the router. The pieces in
`signal-criome/schema/lib.schema`:

- `ComponentKind [Spirit Criome Router Mirror Lojix Persona Agent]` (line 86) —
  the "enum with all the components."
- `AuthorizedObjectKind [Operation Contract Agreement Time]` (line 214) — the
  per-object-function axis.
- `AuthorizedObjectInterest` (lines 221–226) — the subscription's interest set,
  already four variants: `AnyAuthorizedObject`, `(Component ComponentKind)`,
  `(ObjectKind AuthorizedObjectKind)`, `(ComponentObject ComponentObjectInterest)`.
- `AuthorizedObjectReference { component kind digest }` (228–232) — every
  pushed update *already* carries its `(component, kind)` differentiator class.
- `AuthorizedObjectUpdate { object contract decision stamp }` (270–275) — the
  pulse body. `object.component` and `object.kind` ARE the differentiator;
  `object.digest` is the reference; `stamp` is the `AttestedMoment` (`ay3y`).

So the design is not "add an enum" — it is: **name `(ComponentKind,
AuthorizedObjectKind)` the Differentiator, make it the router's match key, and
move the match from criome into the router** (criome stamps+authorizes; router
matches+delivers — `wckt`).

## 1 · The component-differentiator and the match rule

### The differentiator class (the elegant core)

A `Differentiator` is the cross-product coordinate every authorized object
lives at — the one shared vocabulary criome stamps onto an object and the router
matches subscriptions against:

```
Differentiator { component ComponentKind  kind AuthorizedObjectKind }
```

This is exactly the existing `ComponentObjectInterest` struct (lines 216–219)
under its true name. `AuthorizedObjectReference.{component,kind}` already
projects to it for free — `impl From<&AuthorizedObjectReference> for
Differentiator`, no new field on the wire.

Three concrete coordinates, to make it vivid:

- `(Spirit, Operation)` — Spirit accepted a new intent-log object. Mirror (which
  version-controls objects, `wckt`) subscribes; persona agents watching intent
  do too.
- `(Criome, Contract)` — a new authorization contract was admitted (`z9d6`).
  Router and criome-peer nodes subscribe (self-quorum members need it).
- `(Criome, Time)` — a heartbeat fired a quorum-signed `AttestedMoment` (§3).
  Any component holding a time-locked contract subscribes.

### Subscription = (subscriber, interest-set)

A subscription is `(Identity, AuthorizedObjectInterest)` — exactly today's
`AuthorizedObjectObservation { subscriber interest }` (261–264). The interest is
the *closed lattice over the differentiator*, which is why the four-variant enum
is elegant rather than a flat set: one variant covers a whole row, column, cell,
or the universe.

### The match rule (one function, total over the lattice)

`Differentiator::matches(&self, interest: &AuthorizedObjectInterest) -> bool`:

```
AnyAuthorizedObject              => true                          // the universe
(Component c)                    => self.component == c           // a row
(ObjectKind k)                   => self.kind == k                // a column
(ComponentObject { component k })=> self.component==component
                                    && self.kind==k               // one cell
```

Fan-out: on each `AuthorizedObjectUpdate`, the router computes the update's
`Differentiator` once, then iterates open subscriptions and ships the
*reference* (`object.digest` + class + `stamp`) to every subscriber whose
interest matches. criome never computes per-object impact; the router owns the
match-and-deliver step. The differentiator enum is the single shared word both
speak.

### Extending the existing token

`AuthorizedObjectUpdateToken { subscriber Identity }` (266–268) is today's only
subscription key — it cannot distinguish two interests from one identity, and
the router can't match on it. The extension carries the interest into the token:

```
AuthorizedObjectUpdateToken { subscriber Identity  interest AuthorizedObjectInterest }
```

Now `subscription.rs`'s `authorized_object_subscriptions:
Vec<AuthorizedObjectUpdateToken>` (line 23) becomes a matchable table: open
stores `(subscriber, interest)`; `publish` filters by
`update.differentiator().matches(token.interest)` instead of today's
fan-to-everyone `subscriber_count = subscriptions.len()` (line 128). No
pre-production compat owed — break the token, regenerate consumers.

## 2 · Quorum scoped by membership (`p3td`)

One object expresses both quorum modes — the deployed `Threshold { required_signatures
members (Vector PolicyMember) }` (137–140), reached through `Rule::Threshold`
(line 124). The members carry the scope:

- **Self-quorum** (reliability + credible time): `members` are k-of-n
  `KeyMember(Host name)` / `KeyMember(Cluster name)` identities that are *all the
  same principal's own nodes*. Forging needs a threshold of one's own nodes —
  the reliability mechanism of `p3td`, used for `(Criome, Time)` heartbeats.
- **Multi-party** (cross-party trust): `members` span distinct principals
  (`Persona`, `Agent`, peer `Cluster`). k-of-n across principals.

No new type: the *membership composition* is the scope. The PoC's evaluator
checks `evidence.signatures` against `threshold.members` and counts satisfied
distinct members ≥ `required_signatures`, yielding `EvaluationDecision`
(`Authorized` / `(Rejected (QuorumShort ...))` / `EscalateToPsyche` per `gc0n`).

## 3 · The contract-scheduled heartbeat (`m0p2`)

The ops already exist: `ScheduleContractTimeCheck ContractTimeCheck`,
`RunDueContractChecks AttestedMoment`, reply `DueContractChecksEvaluated`. Flow:

1. Admit a `Contract` whose `Rule` is `(ActiveAfter (TimedRule { boundary
   signed_by }))` or `(TimeSwitch { boundary before after })` (142–151).
   Acceptance schedules a `ContractTimeCheck { contract due_at result absent }`
   (285–290) — `result` is the reference to fire, `absent` the differentiator
   interest whose *absence* (no intervening matching update) is the trigger.
2. `RunDueContractChecks(now_moment)`: for each check with `due_at` past the
   supplied `AttestedMoment` window (crystallized-past — `ay3y`, never ambient
   wall-clock), scan the object log for any `AuthorizedObjectUpdate` matching
   `absent` since scheduling.
3. If none intervened, criome fires a fresh `AuthorizedObjectUpdate` for
   `result`, quorum-signed (self-quorum, §2) and stamped with `now_moment` —
   then §1's fan-out delivers it. A `(Criome, Time)` differentiator pulse.

This is "a heartbeat is programmed, not ambient" made concrete: a time pulse is
just a contract whose after-condition matured with no contradicting event.

## 4 · The integrated PoC crate — `/tmp/telos-poc`

A self-contained Rust crate (no daemon, no sockets, no real BLS — a fixed test
signer like router's `AcceptFixedTestIdentity`), proving the whole loop in
in-process actor calls and one integration test. Obeys Rust discipline:
data-bearing `impl`s only, typed per-crate `Error`, no free functions.

```
/tmp/telos-poc/
  Cargo.toml                      kameo + signal-criome (path dep on the deployed contract types)
  src/
    differentiator.rs            Differentiator + From<&AuthorizedObjectReference>
                                 + matches(&AuthorizedObjectInterest) -> bool   [§1]
    quorum.rs                    Threshold eval: count distinct satisfied members
                                 vs required_signatures; self- vs multi by membership [§2]
    moment.rs                    AttestedMoment construction (fixed test quorum over a
                                 TimeWindow) — the crystallized-past stamp [ay3y]
    criome.rs                    CriomeCore actor: AdmitContract -> store;
                                 EvaluateAuthorization -> quorum.rs + moment.rs ->
                                 EvaluationDecision; emits AuthorizedObjectUpdate (reference) [z9d6]
    router.rs                    SubscriptionTable actor (extends subscription.rs shape):
                                 Open(token w/ interest) / Close / Publish ->
                                 fan reference to matched subscribers only [§1, wckt]
    component.rs                 Subscriber actor: receives a reference, then FETCHES
                                 the object by digest from the store (pull, not push) [m0p2]
    heartbeat.rs                 ScheduleContractTimeCheck + RunDueContractChecks:
                                 fire quorum-signed (Criome,Time) update if no intervening
                                 matching update [§3, m0p2]
    store.rs                     content-addressed object store (digest -> rkyv bytes) [z9d6]
    error.rs                     one typed PocError enum
    lib.rs                       wiring: CriomeCore -> SubscriptionTable -> components
  tests/
    end_to_end.rs                admit -> evaluate(quorum+stamp) -> pulse(ref) ->
                                 router fans by differentiator -> only matched component
                                 fetches; non-matching subscriber gets nothing
    heartbeat.rs                 schedule after-time check; no intervening event ->
                                 RunDueContractChecks fires (Criome,Time) pulse, fanned to
                                 the time-interested subscriber; intervening event suppresses it
```

End-to-end assertion: a `(Spirit, Operation)` update reaches a subscriber whose
interest is `(Component Spirit)` or `(ObjectKind Operation)` or
`AnyAuthorizedObject`, and is withheld from `(Component Mirror)`-only and
`(ComponentObject (Criome, Contract))` subscribers — proving the match rule is
the differentiator. The subscriber holds only the reference until it fetches
from `store.rs` (`m0p2`'s push-references/components-fetch). criome computed no
per-object impact; the router did the matching (`wckt`).

## 5 · Open questions for the psyche

1. **Differentiator granularity.** Is `(ComponentKind, AuthorizedObjectKind)`
   the whole differentiator, or do we also need a *named-function* sub-axis
   within a component (e.g. Spirit `intent-log` vs Spirit `marker`)? The current
   four `AuthorizedObjectKind` variants are coarse; a third axis would make
   `Differentiator` a triple. I lean coarse for the PoC.
2. **Token identity.** Adding `interest` to `AuthorizedObjectUpdateToken` makes
   one identity hold many tokens. Confirm retraction is per-(identity,interest),
   not per-identity (today's `close` removes by whole token — fine once interest
   is in the token).
3. **Heartbeat "intervening event" scope.** `ContractTimeCheck.absent` is an
   `AuthorizedObjectInterest` — so "no intervening event" means "no update
   matching that interest." Confirm that's the intended semantics vs. a narrower
   per-contract event match.
