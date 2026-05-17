# 21 — Criome-routed authorization + thin-CLI caller shape

Date: 2026-05-17
Role: system-assistant
Scope: Capture the user's answers to SYS/19's two biggest open
decisions (authorization envelope model + caller shape), connect them
to the existing `criome` and `signal-criome` repos, and surface what
opens up next. Short follow-up to SYS/19 / SYS/20.

---

## 0. The two answers

**Answer 1 — Authorization envelopes.**
> *"we need the criome-daemon for this. authorization is propagated
> through the criome-daemon topology first, with the signal lojix call
> being the object signed, and the criome holds the permission data
> (which key/quorum has which permission)"*

**Answer 2 — Caller shape (G14).**
> *"daemons talk to each other, the cli (or any client) only initiates
> the deploy. the daemon then forwards the request to the
> criome-daemon, which might route the request signature(s) to the
> concerned clients."*

Both answers are highly compatible with what already exists in the
`criome` and `signal-criome` repos. **There is no new trust substrate
to design — there is an integration to specify.**

---

## 1. What the existing criome already gives us

`/git/github.com/LiGoldragon/criome` and
`/git/github.com/LiGoldragon/signal-criome` have substantial
architecture already in place:

- **BLS12-381 signatures from day one**, via `blst`. The architecture
  doc says verbatim:
  > *"Committing to BLS at milestone one keeps every Spartan
  > attestation a quorum candidate without a future scheme migration
  > when eventual-Criome's quorum-signature multi-sig lands."*
  This is the user's "quorum" — the cryptographic substrate for it
  has already been chosen specifically to make it natural.

- **Operative principle**: *"Criome verifies; Persona decides."*
  Sign/verify is criome's job; policy decisions live elsewhere
  (today in persona-mind for prompts; in the new lojix integration,
  the policy lives in criome's record store and is consulted by the
  criome-daemon during signature routing).

- **`signal-criome` wire already has the right vocabulary:**
  - `Sign` / `SignReceipt`
  - `VerifyAttestation` / `VerificationResult`
  - `SignatureEnvelope`, `SignedObject`
  - `DelegationGrant`
  - `AttestAuthorization` / `AttestationReceipt`
  - `SignedPersonaRequest` — already exemplifies the pattern of "an
    inner request wrapped with signatures for a principal"

- **Identity registry feeds**: ClaviFaber's per-host
  `PublicKeyPublication` already flows into criome's identity
  registry. The clavifaber-provisioned per-node signing keys the user
  mentioned earlier (for cache trust) are the same identity
  population. **One identity layer for both cache trust and request
  authorization** — clean.

- **Triad shape**: criome already has the `criome` CLI (one NOTA in,
  one NOTA out) and the `criome-daemon` design. signal-criome is the
  wire. Same shape as everything else.

The repo is **pre-rewrite** — the current code at commit `a3f4173`
is the prior sema-records-validator skeleton; the BLS-daemon target
is in operator's first track. So criome isn't built yet, but the
target shape is well-specified.

---

## 2. The cluster control plane is now three meshes

```
┌──────────────────────────────────────────────────────────┐
│  signal-criome mesh — authorization + identity           │
│  who can do what; signatures; quorum gathering;          │
│  identity registry; attestation audit log                │
│  Each node: criome-daemon                                │
└──────────────────────────────────────────────────────────┘
           ▲
           │ "is this signal-lojix call authorized?"
           │ "gather the signatures this action needs"
           │
┌──────────────────────────────────────────────────────────┐
│  signal-lojix mesh — deploy coordination                 │
│  who builds, who caches, who activates;                  │
│  role assignments; observation events                    │
│  Each node: lojix-daemon                                 │
└──────────────────────────────────────────────────────────┘
           │
           │ "fetch the bulky thing at this hash"
           ▼
┌──────────────────────────────────────────────────────────┐
│  signal-arca mesh — content-addressed substrate          │
│  bulk artifacts: plans, projections, configs;            │
│  peer-to-peer content fetch                              │
│  Each node: arca-daemon                                  │
└──────────────────────────────────────────────────────────┘
```

Each daemon owns one concern. Composition is clean:
- Criome answers "is this request authorized?" → returns SignedObject.
- Arca answers "give me the bytes at this hash" → returns content.
- Lojix uses both: it asks criome to authorize each
  signal-lojix call, and it uses arca hashes to reference bulky
  artifacts.

---

## 3. The deploy-authorization flow, concretely

Re-using SYS/19's Uranus/Tiger/Balboa/Zeus example with criome
folded in:

```
Operator                          Operator's CLI device
  │                                       │
  │ runs `lojix deploy ...`               │
  └──────────────────────────────────────▶│
                                          │
                                          ├─ submits intent to one
                                          │  chosen cluster's lojix-daemon
                                          │  (Uranus, in this example)
                                          ▼
                                  Uranus lojix-daemon
                                  receives DeploymentSubmission
                                  (unsigned intent)
                                          │
                                          ▼
                                  Uranus criome-daemon
                                  "authorize this signal-lojix request
                                   for this deploy plan against my
                                   permission records"
                                          │
                                          ├─ check policy: which keys/
                                          │  quorum needed for this
                                          │  action (deploy to Zeus,
                                          │  this build, this caller)?
                                          │
                                          ├─ if more sigs needed:
                                          │  route signature solicitation
                                          │  to peer criome-daemons
                                          │  (whichever ones hold the
                                          │  keys / contact the clients)
                                          │
                                          ├─ peer criome-daemons solicit
                                          │  signatures from "concerned
                                          │  clients" (operator's
                                          │  yubikey, phone agent,
                                          │  persona-terminal, etc.)
                                          │
                                          ├─ assemble SignedObject:
                                          │  the original signal-lojix
                                          │  request, with the
                                          │  required sigs attached
                                          │
                                          └─ return SignedObject to
                                             Uranus lojix-daemon
                                          │
                                          ▼
                                  Uranus lojix-daemon
                                  now has an authorized envelope;
                                  fans out signal-lojix requests
                                  (containing the SignedObject) to
                                  Tiger, Balboa, Zeus
                                          │
                                          ▼
                                  Each receiving daemon
                                  asks its local criome-daemon
                                  "verify this SignedObject" →
                                  proceeds if verified
```

**Important properties:**
- The CLI device only initiates intent. It doesn't sign and doesn't
  decide policy. (Whoever holds keys might be on a different device.)
- Signature solicitation is a **post-submission** flow. This means
  quorum gathering can take time — minutes, hours, possibly days for
  multi-party sign-offs. The wire needs to support pending /
  in-flight authorization states.
- "Concerned clients" — the devices/agents that hold the keys
  criome needs — are likely persona-terminal-mediated UX surfaces,
  yubikeys, or other operator devices.
- Every receiving daemon verifies independently against its own
  criome-daemon's identity registry. No daemon trusts the sender
  to vouch for authorization.

---

## 4. Caller shape (G14) — closed

Operator's laptop runs:
- `lojix` CLI (thin; submits intent to a chosen cluster's
  lojix-daemon)
- Optionally a local `criome-daemon` **if** the laptop holds a
  signing key — i.e., if the operator's key lives on this device.
  Without a local criome-daemon, the laptop can't sign; signatures
  come from other devices/agents.
- Optionally a local `arca-daemon` if the operator wants
  artifact-flow to/from operator-local storage (not required for the
  deploy itself).

Operator's laptop does **not** run `lojix-daemon`. Cluster nodes do.
The mesh is between cluster nodes; the laptop is a thin client of
that mesh.

This also means: **deploys can be initiated from any device that has
the CLI and a route to any cluster lojix-daemon.** No setup on the
device beyond the CLI. The signing devices are independent.

---

## 5. What's still open after these two answers

Most architectural shape is now settled. What remains is integration
work and a few specific decisions:

### 5.1 Policy schema (medium — needs designer/operator pass)

Criome holds "which key/quorum has which permission." Concretely:
- What's the shape of a policy record? `Permission { action_pattern,
  required_keys: KeySet | Quorum { threshold, eligible_keys } }`?
- What's the granularity of `action_pattern`? "Any deploy to Zeus"?
  "This specific deployment plan hash"? Per-cluster wildcard? Per-
  role?
- How do policy records get written? Bootstrap (clavifaber-provisioned
  initial policy on first boot)? Updated later by signed
  policy-amendment records?
- What's the default-deny vs default-allow semantics? Presumably
  default-deny.

This is where the user/designer's intent matters most. Probably the
right move: a designer report on the policy record shape and
defaults.

### 5.2 Signature solicitation UX flow (medium — persona integration)

When criome needs a signature from a client that isn't already
co-located with the criome-daemon, *how* does it solicit?
- Push notification to a persona-terminal? (Some persona surface
  shows "pending approval: deploy X to Zeus — sign?")
- Polling by the client device for pending requests?
- Long-poll signal-criome subscription?
- Yubikey-style: solicit-on-demand via a pre-shared communication
  channel?

This connects to the persona ecosystem (persona-terminal,
persona-mind) more than to lojix proper. Probably designer-lane.

### 5.3 Cross-criome-daemon routing for quorum gathering (small)

If Uranus's criome needs a signature from a key registered to a
device that talks to Balboa's criome-daemon, Uranus's criome routes
through Balboa's criome via signal-criome (criome-to-criome wire).
This is a new use of signal-criome (today's vocabulary is mostly
client-to-criome). Probably an extension to signal-criome adding
`ForwardSignatureSolicitation { object, target_key, ... }`.

### 5.4 Pending-authorization state in lojix (small)

If quorum gathering takes time (minutes-to-days for some actions),
lojix-daemon needs to represent an in-flight authorization. Probably:
`DeploymentPhase::AwaitingAuthorization` plus a subscription so the
CLI/operator can see "waiting on signatures from A and B."

### 5.5 Authorization on signal-criome itself (small but recursive)

Who can ask criome to sign? Presumably any registered identity may
request a `Sign` of any object, but criome's policy gates *which
sigs get applied*. This avoids a recursive trust problem (signing
the request to sign).

### 5.6 Replay protection (already handled in criome design)

The existing criome architecture mentions a `replay-guard`. Each
authorized signal-lojix request needs to include a nonce or
timestamp so the same signed envelope can't be re-played later.
Criome's existing design covers this; lojix integration just needs
to use it.

---

## 6. Revised what-to-build-first

Updates SYS/19 §9 with these answers folded in:

1. **Finish criome BLS-daemon rewrite** (already in operator's first
   track). Foundation everything else depends on. Includes:
   - Identity registry
   - Sign/verify primitives
   - Policy record store
   - signal-criome wire (largely already specified)
   - ClaviFaber identity feed
2. **Finish arca skeleton-as-design bodies** (SYS/20 §9 step 1).
   Independent of everything else; can land in parallel.
3. **Add cross-node signal-arca FetchHash** + signal-criome
   ForwardSignatureSolicitation. The two cross-node-mesh additions
   for arca and criome respectively. Static peer config v1.
4. **Add `NixConfigurationActor` to lojix-daemon** (SYS/19 §7).
   Independent of mesh deploy; valuable on its own.
5. **Add `idempotency_key` to `wire::DeploymentSubmission`**
   (SYS/18 G18). Tiny; do before any consumer ships.
6. **Land `deploy.rs` split toward new actor planes** (SYS/137
   §"Implementation consequences"). Sequenced with `primary-766g`
   (sema slot for `deployment_id`).
7. **Lojix-criome integration**: lojix-daemon hands signal-lojix
   requests to local criome-daemon for authorization; signal-lojix
   request types gain a `SignedObject` wrapper.
8. **Lojix-arca integration**: lojix-daemon writes plan artifacts
   to local arca-daemon; signal-lojix carries Arca hashes.
9. **Implement the deploy mesh proper** (per SYS/137 actor planes,
   SYS/19 deploy flow).

Steps 1+2 are foundation. Steps 3+4+5 are independent additions.
Steps 6+7+8+9 are the mesh integration itself, sequenced.

---

## 7. The two-stack picture, updated

From `protocols/active-repositories.md` §"Two deploy stacks coexist":

**Stack A** (production today) continues to be the bootstrap and the
operational stack until cutover. No architectural changes here.

**Stack B** (lean rewrite, on `horizon-leaner-shape`) now has a
clearer destination shape:

- `lojix` daemon owns deploy coordination
- `arca` daemon owns content substrate
- `criome` daemon owns authorization
- `nix-daemon` owns nix-store + builds (controlled by lojix-daemon's
  `NixConfigurationActor`)
- Each node runs all four
- Operator's laptop runs only the CLIs (+ optionally local criome /
  arca if the laptop participates as a signing key holder /
  artifact source)

Cutover (per `protocols/active-repositories.md`) goes node-by-node;
each node bootstraps via Stack A, then once on Stack B, joins the
three meshes.

---

## 8. What I want the user to see in chat

The architecture is now substantially settled. What's left is
**integration work and a small number of policy/UX decisions**, not
fundamental design questions.

The single highest-leverage point: **criome already specifies BLS
signatures from day one specifically so that quorum is natural** —
this matches your authorization-routing intent exactly. The trust
substrate isn't a new design; it's an existing design that just
needs the lojix integration spelled out.

The pending decisions worth pulling forward to designer-lane:
1. Policy record schema in criome (§5.1)
2. Signature solicitation UX through persona surfaces (§5.2)

Everything else is "implement the integration."
