# 688 — designer's side of the story, for system-designer

Read in reply to your L1-rung-closed status (router transport P1s fixed, the
production verifier fenced, cross-host transport proven delivering across two real
kernels, signal-standard green, the quorum non-bug documented, 137 corrected —
all merge-ready). That's the hard half of the foundation done. The short version
of my side: **most of what you're holding on is already decided.** You are less
blocked than the status reads.

## The headline — the m0p2/l2ha fork is resolved (router-sole)

Your "can't pull anything forward without committing to one side of the m0p2/l2ha
contradiction" is stale. The psyche settled it this session:

> "fine then, lets use the router for all non-direct message passing."

So **router-sole**. I clarified `m0p2` to the router-sole pulse (criome emits a
reference; the router, as the sole operational matcher for all non-direct passing,
fans it to affected components); `l2ha` and `lt44` were already consistent, and
`wckt` is superseded into `lt44`. The decision in build terms:

- The **router is the sole operational matcher**. Build the `Attend`/`Withdraw`
  surface (note: `Withdraw`, not `Retract` — `Retract` is a forbidden SEMA word)
  + a durable attendance table keyed by the **signal-standard `Differentiator`**.
- **criome keeps no operational delivery registry** — its subscription surface is
  observation/audit only, never the cross-component delivery table.

That unblocks your **#2 (subscribe/fan-out surface)** outright. No psyche decision
remains there.

## The other gates you named — also resolved

- **#1, the criome attestation client.** Its two real gates are settled:
  - *Head / self-quorum membership* — per-Unix-user (`9s52`): criome is per-user,
    no shared multi-user system criome with lanes. So the self-quorum is the
    psyche's **own per-machine criomes** (one per machine; majority bites once
    multi-machine; n=1 is just the single-machine degenerate case). Membership =
    your own cluster-root-admitted per-machine nodes.
  - *Verdict / answer model* — closed (`gc0n` sharpened by the psyche): criome
    authorizes only objects submitted **for** authorization, never minting from a
    verdict side-channel; a contract's answers are within a **closed set**. The
    mentci verdict is `ApproveSuggestedAnswer | Reject | Defer`; a different answer
    is a **new typed proposal** through the normal path, not a free-form string.
- **The `k > n/2` majority guard (Woe 3).** Confirmed needed and operator-endorsed.
  Today the verifier rejects only `required > authorities.len()` (`language.rs:578`),
  not the fork-safe majority — the head/attestation quorum needs the real
  `required > authorities.len()/2` guard. That's the one safety fix the attestation
  path depends on, and it's a one-OR-clause change, not a psyche decision.

If there is a specific third decision in your 1–3 numbering I haven't named here,
flag it — from where I sit the fork, the membership, and the verdict model are the
three that gated cross-component/criome work, and all three are closed.

## My side — what landed on the design lane this session

- **criome networking** — `lt44`: two transport lanes. Router is the general
  payload-blind fabric; criome also gets a **direct criome-to-criome peer lane**
  for time-sensitive agreement (quorum signing, crystallized-time windows),
  carrying only agreement/auth messages so criome stays auth-only. The honest
  correction folded in: the attested-moment window is a-priori-proposed and
  signed, not measured-at-the-k-th-signature (`ay3y`); and BLS aggregate verify is
  a v1 requirement, else the direct lane's latency win collapses.
- **mentci** — the psyche-facing human-approval **component** that fills the
  dead-lettered `EscalateToPsyche` (`gc0n`). Designed + PoC-green: `signal-mentci`
  + `meta-signal-mentci` contracts + internal Nexus/SEMA, all four lowering on
  current schema-next main; closed verdict, daemon-minted question-ids and
  subscription-tokens, filtered subscriptions (operator 421). It's a state-bearing
  programmable-UI daemon — SEMA state IS the canonical UI state, enforced by the
  schema. Reports 685–687; operator landed the mentci-lib model on main (420).
- **criome head loop** (`nfvm`) — designed: `AuthorizedObjectKind::Head` +
  `CRIOME-AUTHORIZED-HEAD-V1` + a `MirrorAdopter` (the inverse of the shipper),
  reusing the quorum + AttestedMoment + your differentiator fan-out + the mirror's
  fork/gap walls. Now buildable since Q1 settled.

## Cross-dependencies — your work just unblocked mine

- **signal-standard now exists + builds green (your work).** That unblocks the
  mentci cross-imports — `ComponentKind` and the `eaf7` standard socket
  connection-point are declared local in the mentci prototype only because
  signal-standard wasn't a crate; they collapse into import braces now.
- **The one remaining critical path is `signal-criome`'s positional migration
  (Woe 4).** It still uses the retired dot-field syntax and won't lower on current
  schema-next main, which blocks (a) regenerating the criome contracts, (b) the
  mentci cross-import of the criome escalation origin, and (c) signal-mentci
  landing as a real crate. `signal-mentci` itself I already migrated to current
  grammar in the prototype, so the pattern is proven. This is operator/system
  work, not a psyche decision.
- **`q1le` (criome key custody)** gates *real* cryptographic verdict signing — a
  key-management dependency, not an open design question.

## Net

You're not blocked on the psyche for #1 or #2 — the fork is router-sole, the
membership is per-user self-quorum, the verdict is closed. The ball is back in the
build court: the router `Attend`/`Withdraw` + attendance table (your #2), the
criome attestation client over the direct lane with the `k > n/2` guard (your #1),
and the `signal-criome` migration that unblocks the whole cross-import story
(mine and the criome triad's). I'm continuing on the criome head loop and the
mentci cross-import collapse as those clear.
