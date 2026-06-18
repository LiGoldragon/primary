# 134 — The universal component-differentiator contract: design for Fork-A fan-out

*Fork A is resolved — per `l2ha` (Decision): [object-update fan-out is owned by
subscribing components and the router, not by criome computing per-object
impact … criome stamps and authorizes the object, and the router matches
subscriptions and fans the references out]. The psyche (relaying operator)
asked for elegant ideas to implement "a universal contract, mostly an enum of
all the components, used heavily by router and criome — a differentiator for all
the different components" so components subscribe to events related to their
function. This is the design. Method: a four-approach design panel → ranked
synthesis → an adversarial critic that caught real errors → my own verification
of every crux fact against the live schemas. Companion: report 133.*

> **Status (updated 2026-06-18, see report 135):** PARTLY SUPERSEDED but still
> the authoritative router-lane design. The core thesis (criome already stamps
> the `(component, kind)` coordinate; no new wire field) is CONFIRMED and BUILT
> (operator 414/415, PoC 680). Fork "home" is RESOLVED → the new shared library
> `signal-standard` (Spirit `eeeo`, designed in 681). Forks closed/coarse held;
> the principal-line fork was decided *against* my lean (Lojix/Agent/Persona stay
> in one closed enum, zoned, not moved off-axis). **Correction applied below:**
> the verb pair is `Attend`/`Withdraw`, not `Attend`/`Retract` — `Retract` is one
> of the six Sema words `7l7l` forbids on the wire (my original draft cited 7l7l
> yet violated it). The router half remains entirely unbuilt — it is this lane's
> work; see report 135 for the registry-owner tension that gates it.

## 1 — What already exists (don't reinvent)

- **criome already stamps the differentiator coordinate.** `signal-criome`
  emits `AuthorizedObjectReference { component ComponentKind · digest
  ObjectDigest · kind AuthorizedObjectKind }` inside `AuthorizedObjectUpdate`,
  where `AuthorizedObjectKind [Operation Contract Agreement Time]`. That
  `(component, kind)` pair **is** a functional differentiator, already produced
  at admission, reference-only (no payload).
- **The router already delivers to components** (`EndpointKind … ComponentSocket`;
  operator `37f9387`/`629ca92` deliver routed objects to component sockets) and
  already carries a registration mechanism (`RegisterActor` in
  `RouterBootstrapOperation`).
- **The router has no subscribe/interest surface yet** — only router-to-router
  forwarding (`RouterForwardRequest`). So the attendance registry is genuinely
  net-new, and lands on the *working* signal (not the meta policy wire).

## 2 — Four approaches, ranked

| # | Approach | Score | One-line |
|---|---|---|---|
| C | typed facet stamped at admission, matched on the envelope | 9 | smallest delta that gives a real differentiator distinct from the address label |
| A | enriched `ComponentName` as the facet key + a router `Attend` registry | 7 | closest to your literal words; but one component-level enum is too coarse for "events related to function" |
| B | interest **is** an admitted criome contract | 6 | most unified, but edges criome toward transport and adds ceremony to routine wiring |
| D | capability-grant via meta-signal `ChannelEndpoint`/`ChannelGrant` | 6 | reuses the most machinery, but mixes delivery with policy and routes subscribe through the meta socket |

## 3 — Recommended shape (lightest, after critique)

**"criome stamps the coordinate it already ships; the router owns the match;
the universal contract is the shared differentiator both cross-import."**

The elegance comes from *not inventing a new stamp*. criome already emits
`(component, kind)` on every authorized object. So:

1. **The "universal contract" = one shared module defining the reconciled
   `ComponentName`/`ComponentKind` enum + `AuthorizedObjectKind`**, cross-imported
   by both `signal-criome` (which stamps) and `signal-router` (which matches).
   This is precisely the psyche's "a special contract router and criome use
   heavily — a differentiator for all the different components." Today these
   types are component-local and mutually inconsistent (§4); promoting them to
   one shared, cross-imported contract *is* the change.
2. **The differentiator = the `(component, kind)` coordinate criome already
   stamps.** criome gains nothing — it keeps emitting `AuthorizedObjectReference`.
   This is the cleanest read of `l2ha` ("criome stamps … the router matches and
   fans out") and keeps `wckt` exact (criome auth-only, moves nothing).
3. **The router gains the new surface** — a Sema-free `Attend`/`Withdraw` verb
   pair (NOT `Subscribe` *or* `Retract` — both are among the six Sema words
   `7l7l` forbids on the wire) and a SEMA-durable attendance table keyed
   by the coordinate. On an admitted object it matches attenders and pushes a
   *reference* (`m0p2`: digest, never payload); the component fetches the rkyv
   object by digest through the object-distribution layer.

```nota
;; component attends the function-events it cares about (working signal, router)
(AttendObjects ((Internal Terminal) [(Terminal Operation) (Spirit Contract)]))
(AttendanceOpened (AttendanceToken at-7f3a))
;; router pushes a REFERENCE when a matching (component, kind) object is admitted
(ObjectAvailable ((Spirit Contract) (AuthorizedObjectReference Spirit z9d6abc Contract)))
(RetractAttendance (AttendanceToken at-7f3a))
```

**Heartbeat:** not ambient. A component wanting periodic wakeups submits
criome's existing `ScheduleContractTimeCheck` (after-time condition); when it
fires, criome emits an update the router fans out — `m0p2`'s "programmed
after-time, no global heartbeat," zero new mechanism.

## 4 — The hard prerequisite (the real decision)

This cannot be a "pure projection," because **the component enum is three-way
conflicted** and a universal shared contract forces resolving it:

| Repo | Type | Shape | Members |
|---|---|---|---|
| `signal-persona` | `ComponentName` | **open String** | (any) |
| `signal-persona` | `ComponentKind` | closed [9] | Mind Router Message System Harness Terminal Introspect Orchestrate Spirit |
| `signal-message` | `ComponentName` | closed [9] | Mind Message Router Terminal Harness System Introspect Orchestrate Spirit |
| `signal-criome` | `ComponentKind` | closed [7] | Spirit Criome Router Mirror Lojix Persona Agent |

They disagree on **membership** (only criome has `Criome`/`Mirror`; only the
others have `Mind`/`Terminal`/`Harness`/`Introspect`/`Orchestrate`), on **shape**
(one is an open String), and on the **component-vs-principal line** (criome's
`Lojix`/`Persona`/`Agent` are arguably principals/runtimes, not component
daemons). Promoting to one universal differentiator requires ruling on all
three. This is the prerequisite, not a downstream confirm.

## 5 — Forks to steer

1. **Which membership wins, and the component-vs-principal line.** Are
   `Lojix`/`Persona`/`Agent` components or principals? That decides the
   superset. (Lean: the canonical set is the *component daemons*; principals
   stay on the `ConnectionClass`/identity axis.)
2. **Closed enum vs open identifier.** Lean **closed** for the component/function
   axis (components are a deploy-bound set; adding one is already an
   all-consumers-rebuild event, so a contract bump costs nothing and buys
   exhaustive `match`). Note the tension: `signal-persona` *already* types
   `ComponentName` as an open String, and `udgu`/`irmw` say *principals/roles*
   should be open — so the clean line is **closed for what-component, open for
   who-connects**. Your call.
3. **Facet granularity.** Start with the existing `AuthorizedObjectKind`
   `[Operation Contract Agreement Time]` keyed by component — *no new enum, no
   mapping-bug surface*. Only enrich to a wider `ComponentFacet` (e.g. a
   ~12-variant functional vocabulary) if 4-way × component proves too coarse for
   "events related to function." (Lean: start with the 4-way; enrich on demand.)
4. **Home of the universal contract.** `signal-persona` or `signal-message`, or
   a new shared repo you authorize — **not** `signal-persona-origin` (it doesn't
   exist; the panel invented it).
5. **Is subscription itself a governed/audited act?** Router-held registry
   (recommended; light) vs interest-as-criome-contract (approach B; every
   subscription signed/revocable/audited). Pick B only if attendance must be
   governed.

## 6 — Intent notes

- **No capture owed.** Fork A is captured as `l2ha`; the universal-contract idea
  was stated exploratorily ("maybe … maybe … I need ideas") — not a durable
  decision until the psyche picks. This is a designer synthesis; the resolution,
  once chosen, is captured by the lane in live exchange (operator/psyche), not
  pre-recorded here.
- **Flag for a Clarify (operator/psyche's call):** `m0p2` still reads [criome
  pushes an update to affected components], which `l2ha` supersedes ([the router
  matches subscriptions and fans the references out]). The two phrasings name
  *different fan-out owners*; `l2ha` is the later narrowing. `m0p2` is a
  candidate for a `Clarify` so the intent layer doesn't carry both.

## 7 — Sequencing

This is offline contract + router design (the shared differentiator, the router
`Attend`/`Retract` surface, the attendance SEMA table). It is **not blocked on
the key track** — the lighter design has criome stamp the coordinate it already
ships, so nothing rides inside the criome-signed envelope and the admission-
signing ceremony is not a prerequisite. (Only the heavier "facet inside the
signed region to stop relay re-stamping" variant would couple to that ceremony —
avoided here.)
