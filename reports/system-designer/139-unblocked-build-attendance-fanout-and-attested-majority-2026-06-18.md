# 139 — Unblocked: building the router fan-out surface + the scoped attested-moment majority guard

*The designer handed off (`reports/designer/688`): the two decisions I was holding
on are already resolved this session. I grounded that against Spirit directly
(the forwarded-handoff gap-check), reconciled the one place 688 and my own reports
diverged, and launched the build of the now-unblocked work. Build workflow
`wgpa80oej` is running.*

## The handoff, grounded against Spirit (all confirmed)

| Record | Kind | What it settles |
|---|---|---|
| `m0p2` | Decision | **Router-sole.** "the router, as the sole operational matcher for all non-direct message passing, matches component subscriptions and fans the reference out … Criome keeps no operational delivery registry; any criome-local subscription surface is observation and audit only." Resolves the `m0p2`/`l2ha` fork I was holding on — and makes the attendance table **router-local and light**, not a governed criome contract. |
| `lt44` | Decision | **Two transport lanes**, refining my 138/2: router as general payload-blind fabric **+** a direct criome-to-criome peer lane for time-sensitive agreement (quorum signing, crystallized-time windows); the direct lane carries only agreement/auth, so criome stays auth/agreement-only. BLS aggregate verify is a v1 requirement on that lane. |
| `9s52` | Constraint | criome is **per-Unix-user**; the self-quorum is the psyche's own per-machine criomes (`n=1` is the single-machine degenerate case). |
| `gc0n` | Decision | The verdict/answer model is **closed**: criome only authorizes submitted objects; a different answer is a new typed proposal, not free-form. |
| `ay3y` | Decision | The clock is a **quorum-attested, crystallized-past** coarse time; `AttestedMoment` carries its own time proof. |

The psyche's settling words, per 688: [fine then, lets use the router for all
non-direct message passing.] That single principle resolves **both** of my held
decisions — it is router-sole fan-out (#2) *and* the affirmation of my Track B
"ride the router" recommendation (#1), now scoped by `lt44` to the non-time-
sensitive lane.

## The one divergence, reconciled — there are two quorum sites, not one

688 said the `k > n/2` guard (the designer's Woe-3) is needed and operator-
endorsed; my 138/4 said the quorum guard is a non-bug. **Both are right because
they name different code sites** (verified against `criome` `068f9db`):

- **`language.rs:414` `Threshold::validate_shape`** — the general caller-declared
  m-of-n evaluator. Stays as-is; a `>n/2` rewrite here regresses legitimate
  `required=1` and unanimity policies. (My 138/4 holds for this site.)
- **`language.rs:578` `AttestedMoment::rejection_reason`** — the time-attestation /
  head-quorum path. *This* needs `required > authorities.len()/2`: a decentralized
  quorum clock (`ay3y`) and quorum-backed objects (`m0p2`) must not be single-node-
  attestable, and fork-safety needs strict majority so two disjoint quorums can't
  attest conflicting moments/heads. (The designer's Woe-3 holds for this site.)

My 138/4 erred only in lumping `:578` with `:414`. The real hazard is applying the
majority clause to `:414` by mistake — so the fix is built **scoped to `:578`**,
with a code comment stating `:414` deliberately stays caller-declared.

## What's building now (workflow `wgpa80oej`)

- **Track G — the router `Attend`/`Withdraw` fan-out surface** (my #2, spec →
  build → adversarial-verify). On `signal-router` + `router` branch
  `attendance-fanout-139`: the `Attend`/`Withdraw` working-signal operations
  (`Withdraw`, not the forbidden SEMA word `Retract`), a router-local SEMA-durable
  attendance table keyed by `signal-standard`'s `AuthorizedObjectInterest` lattice,
  the match-by-`Differentiator` step, and the reference-push (m0p2: a reference,
  never the payload) over the existing `ComponentSocket` delivery. criome untouched.
- **Track H — the scoped `:578` majority guard** (build → verify). On `criome`
  branch `attested-moment-majority-guard-139`: the one-clause `required >
  authorities.len()/2` addition with boundary tests (`n=1/req=1` accepted,
  `n=2/req=1` rejected, `n=3/req=2` accepted, `n=4/req=2` rejected) and the comment
  fencing `:414`.

Both land on feature branches for operator to integrate to code-repo main.

## Still operator/system, not mine (from 688)

- **`signal-criome` positional migration (Woe 4)** — won't lower on current
  schema-next main; blocks regenerating the criome contracts, the mentci cross-
  import, and `signal-mentci` landing. The designer proved the pattern by migrating
  `signal-mentci`. This is the one critical path for the whole cross-import story.
- **`q1le` criome key custody** — gates *real* cryptographic verdict signing.
- Operator creating the `signal-standard` GitHub remote (Track C follow-up) so the
  router's `attendance-fanout-139` path-dependency can become a clean flake input.
