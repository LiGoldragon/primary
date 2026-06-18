# 135 — Caught up: the differentiator landed (criome half); the router half is mine and unbuilt

*The psyche asked me to get up to date with the latest. Since report 134 the
component-differentiator work advanced fast across designer + operator + psyche.
The short version: my 134 thesis is confirmed and mostly resolved in its favor,
the **criome half is built**, and the **router half — this lane's unique
deliverable — is entirely unbuilt**, gated on one registry-owner decision and an
intent-layer contradiction. Method: a four-reader catch-up workflow + my own
read of 681 / `eeeo`, every crux fact verified.*

## 1 — What's decided / built / PoC'd since 134

| Item | Status | Where |
|---|---|---|
| `signal-standard` = a new 2nd shared `signal-` lib (alongside `signal-frame`), holds the `ComponentKind` roster + differentiator; component-local copies retired | **decided** | Spirit `eeeo`; designed in `reports/designer/681` |
| 681's prototype: reconciled **14-variant closed-but-partitioned** `ComponentKind` (5 `t312`-style zones), `Differentiator { component, kind }`, the 4-rung `AuthorizedObjectInterest` lattice, `ComponentClassification` nameplate | **designed, /tmp only** | `681`; repo `/git/.../signal-standard` confirmed **absent** |
| `AuthorizedObjectUpdateToken { subscriber, interest }` | **landed on main** | operator 415 (signal-criome `e33ea04a` + criome `4250cbb3`) |
| classified-object pulse + programmed-(after-time)-heartbeat | **PoC** | operator 414 |
| criome-internal `SubscriptionRegistry` (filters by `token.interest.matches_update`) | **built — but only COUNTS matchers, delivers nothing** | `criome/src/actors/subscription.rs` |
| full spirit→criome→router→mirror loop + the `From<&AuthorizedObjectReference> for Differentiator` projection | **in-process PoC, router stubbed** | designer 680 |
| **router subscribe/fan-out surface** | **ZERO — nothing exists** | `signal-router` has no `ComponentKind`/`Attend`/interest/table |

## 2 — How my 134 forks resolved

| Fork | Resolution | Anchor |
|---|---|---|
| Home of the universal contract | **new shared lib `signal-standard`** (my "new repo you authorize" branch) | `eeeo` |
| `ComponentKind` membership | **14-variant union** (persona 9 + criome 7, 2 shared collapse), no variant dropped | 681 census |
| Closed vs open | **closed-but-partitioned** (my lean), zones with reserved room | `eeeo`, `t312` |
| Differentiator granularity | **coarse `(component, kind)`** (my lean); no new facet enum | 681, landed criome |
| Component-vs-principal line | **against my lean** — Lojix/Agent/Persona stay *in* the closed enum; Persona zoned "Aggregate (principal, not daemon)" | 681 |
| (134 caught what 681 missed) | `signal-message::ComponentName` is a **third** roster 681's census omitted | operator 416 Q1 |

So 134 is **partly superseded but still the authoritative router-lane design**.
Corrections applied to 134 this pass: the home fork marked resolved; and the
**`7l7l` bug fixed** — my proposed `Attend`/`Retract` pair used `Retract`, itself
one of the six forbidden Sema words; the pair is now `Attend`/`Withdraw`.

## 3 — The gating tension: who owns the matcher?

`l2ha` and my 134 say **the router** matches subscriptions and fans references
out. But operator built the matchable `SubscriptionRegistry` **inside criome**
(415), and its publish currently **only counts matchers** (`subscriber_count`) —
it delivers nothing. So the built code matches **neither** intent record's
literal wording: not `m0p2` ([criome pushes an update to affected components]),
not `l2ha` ([the router matches subscriptions and fans the references out]).

This is the one decision that gates the whole router lane and reconciles the
`m0p2`-vs-`l2ha` contradiction. Two shapes:

- **Router is sole matcher** (l2ha-faithful): criome emits *unfiltered*
  references; the router holds the attendance table, matches, and delivers. Keeps
  `wckt` cleanest (criome stamps, moves nothing, doesn't even match).
- **criome keeps its internal registry AND the router gets one** (a double
  filter): criome's registry serves its own auth-audit/observation; the router's
  serves operational delivery. Risks drift between two tables on the same key.

## 4 — This lane's remaining work (the router half)

1. **Resolve the registry owner** (§3) and drive the `m0p2` edit (`Clarify`/
   `Supersede`, not a sibling record) so the intent layer carries one fan-out
   owner matching the chosen design.
2. **Design the router `Attend`/`Withdraw` surface on `signal-router`** — the
   net-new working-signal deliverable: verb pair + durable attendance table keyed
   by the `signal-standard` differentiator + the match-and-deliver step.
3. **Specify socket-level reference delivery + the pull path** — `publish` only
   counts today; design the `m0p2` "push a reference, fetch the body by digest."
4. **Specify how the router imports `signal-standard`** once the crate lands
   (import `ComponentKind` + the lattice from there, not `signal-criome`).
5. **Specify the durable `ContractTimeCheck` scheduler** (in-memory PoC only;
   needs a SEMA family that resumes due checks across restart).
6. **Adjudicate `signal-message::ComponentName`** (the third roster) — collapse
   into the imported `ComponentKind`, or a distinct message-lane endpoint axis?

This is offline contract + router design — **not blocked on the key track**.

## 5 — Open questions for the psyche

1. **Registry owner (gating):** router sole matcher (criome emits unfiltered), or
   criome-keeps-its-own + router-also (double filter)? Everything else waits on
   this.
2. **Differentiator granularity:** coarse `(ComponentKind, AuthorizedObjectKind)`
   forever, or a third named-function axis (e.g. Spirit intent-log vs marker)?
   The router table key depends on it — settle before keying.
3. **Attendance governed or light?** A governed criome contract (signed/audited/
   revocable, 134 approach B) vs light router-local registry. Light is the
   current lean; governed needs a new Spirit decision.
4. **`signal-message::ComponentName`:** collapse into `ComponentKind`, or distinct
   axis? (Blocks calling membership reconciliation complete.)

## 6 — Intent-layer hygiene (flagged, not acted on unilaterally)

- **`m0p2` needs an edit.** It still reads [criome pushes an update to affected
  components], contradicting `l2ha`; resolve to the chosen fan-out owner via
  `Clarify`/`Supersede` (whoever owns the live exchange; I can take it once §3 is
  decided).
- **The `ComponentPrincipal`-collapse decision has no Spirit anchor** — it lives
  only in commit `57d0a7f5` + report 681 as "psyche-decided," which violates
  no-harness-dependent-memory. Capture it as a Decision/Clarification, or correct.
- No new capture is owed by me: Fork A is `l2ha`; the universal-contract idea is
  realized via `eeeo`; this report is designer synthesis.
