# 111 — message direct-delivery fast path: a proposal assessment

*Mid-dialogue, the psyche proposed a new division of labor between `message` and
`router`: [message would pass some messages directly without router, if the agent
knows about another agent by its uid, and that agent is marked as publicly
reachable … then router routes to gated agents, and to agents across network]. This
is a materially different architecture from reports 75/76 (where `message` is a pure
trust membrane and `router` does all routing). This report assesses it — strengths,
open questions, and how it resolves the still-open existence-log question (110 §4 /
report 109) and rides on the just-decided meta-signal policy plane (Spirit Decision
`n775`). The
proposal is under discussion; nothing is recorded as intent yet.*

## The proposed model

A **two-path** delivery split, by *authority and locality*:

- **Fast path — `message` direct-delivers (no `router`)** when **both**: the sender
  addresses the target agent by its **uid**, and the target is **marked publicly
  reachable** (ungated). `message` already authenticates the sender via
  `SO_PEERCRED`; it would resolve the target uid to its endpoint and deliver
  peer-to-peer.
- **Slow path — `router` routes** for: **gated agents** (delivery that needs
  authority adjudication / a channel grant) and **agents across the network**
  (remote / federated transport).

In one line: `message` handles the *zero-authority, local, public* case; `router`
handles everything that needs **a gate or the network**.

## Why this is a strong model (what I think)

**1. It is a principled trust gradient, not a shortcut.** The untrusted `0660`
ingress door (`message`) only ever direct-delivers where there is **no authority to
abuse** — public agents that anyone could reach anyway. Every case carrying real
authority (gated agents) or crossing a trust-domain (network) goes through the
`0600` authoritative `router` with its durable ledger. So the blast-radius worry
that made 76.1 say "keep separate but it's fragile" is *contained by construction*:
direct delivery cannot leak authority because the fast path has none.

**2. It resolves the "message is under-built" tension decisively.** 76.1's sharpest
finding was that `message` owns no durable fact while intent `l3k4` says it should.
This proposal gives `message` a real job — fast-path delivery — and therefore a
reason for durable state: a delivery/existence record for the messages it delivers
directly. It answers the open Q1 (build the existence-log vs trust-membrane)
**toward build**: `message` becomes feature-bearing.

**3. It makes the two-facts model cleaner, not messier.** With direct delivery, the
fact ownership becomes:

| Fact | Direct (fast) path | Routed (slow) path |
|---|---|---|
| **Existence** (bytes arrived at ingress) | `message` | `message` |
| **Delivery** (target acknowledged) | `message` (it delivers + gets the ack) | `router` (harness/target ack) |

`message` **always** owns existence (it is the ingress for everything) — which is
exactly `l3k4`, finally realized — and delivery-ownership splits by path. That is a
sharper, more honest model than today's (where `router` writes even the existence
record).

**4. It rides on the meta-signal policy plane just decided (Q2).** The "publicly
reachable" mark and the uid→endpoint registry are **owner policy** — declared by the
owner over the meta-signal plane. The two answers compose into one design: the owner
declares, via meta-signal, who is public and reachable; `message` uses that registry
to choose the fast path. No new mechanism — the Q2 plane carries it.

**5. Latency.** It removes a hop (`sender→message→router→target` becomes
`sender→message→target`) for the high-volume local-public case.

## Open questions the psyche needs to settle

These are the load-bearing details before this becomes buildable intent:

1. **What does "publicly reachable" mean, precisely?** Most likely: *ungated* —
   accepts unsolicited messages without a channel grant (gated = `router` must
   adjudicate a grant first). Confirm that "public" ≡ "no channel grant required,"
   and that it is set per-agent by the owner over the meta-signal plane.
2. **Public AND local, or can a public agent be remote?** A publicly-reachable agent
   that lives *across the network* still needs `router` for transport. So the fast
   path is **public AND local**; "remote" (any gating) always routes. Confirm the
   path-selection rule is: `direct ⇔ (public ∧ local ∧ uid-known)`, else `router`.
3. **Discovery / addressing.** How does a sender "know about another agent by its
   uid"? Does it query `message`'s registry, or is there a directory? `message` (via
   its policy plane) holds the public registry and resolves uid→endpoint — but the
   *discovery* surface (how a sender learns who is public) needs definition.
4. **The stamp-trust surface widens.** On the direct path, the *target* agent must
   trust `message`'s `MessageOrigin` stamp (just as `router` trusts it today). So
   every agent that can receive a direct-delivered message must trust `message` as a
   stamper — a wider trust relationship than today (where only `router` consumes the
   stamp). Acceptable, but it makes `message` a trust anchor for the whole local
   public mesh, not just the ingress.
5. **Exactly-once path selection.** Two delivery paths means the direct-vs-router
   decision must be **total and atomic** at `message` so no message is double-sent or
   dropped between paths.
6. **Does `router` still see direct-path existence?** If audit/replay needs a single
   place to see all messages, either `message`'s existence-log is the union surface,
   or direct-path existence is mirrored to `router`. Decide where the *complete*
   ledger lives.

## What it resolves and what it implies

- **Q1 (existence-log): → build it.** Under this model `message` must own durable
  state (existence always; delivery on the direct path), so the "thin trust
  membrane" option (110 §4 Option B) is off the table — `message` becomes a real
  feature-bearing triad component.
- **Q2 (meta-signal plane, Spirit `n775`): confirmed and load-bearing.** The plane
  carries both the owner identity and the public-reachability registry.
- **`message` becomes a 3-plane triad** (Signal + Nexus + SEMA) with a meta tier —
  no longer the 2-plane carve-out report 75 §3.1 recommended. The 75/76 "stateless
  carve-out" framing is superseded by this dialogue.

## Verdict

I'd lean **for** it. It is a coherent, security-sound split that turns `message`'s
under-built gap into a clear role, realizes `l3k4`, and composes cleanly with the
meta-signal plane. The risk is purely *scope* — `message` grows from a membrane into
a real component with a registry, a delivery path, and a ledger — but the trust
property (the untrusted door only fast-paths the no-authority case) holds, which is
the part that actually matters. The six open questions above are what turn it from a
good instinct into buildable intent; once the psyche settles them (especially #1, #2,
#4) it should be captured as the governing message/router architecture decision and
the 75/76 carve-out framing formally superseded.
