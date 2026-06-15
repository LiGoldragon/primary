# 650 — Cross-check of system-designer 111: the message direct-delivery fast path

Designer review of `reports/system-designer/111-message-direct-delivery-fastpath-2026-06-15.md`
(SD leans *for* the psyche's proposed fast path) against `76.1`
(`reports/system-designer/76-message-router-overlap-2026-06-05/1-overview-verdict.md`,
"keep separate, message is under-built") and the current `message/INTENT.md`
(message is a stateless boundary; SEMA "honestly empty"). The psyche asked for my
take. Nothing here is intent — the decision and SD's three pinned questions are
the psyche's.

## Intent check (Spirit, read directly — not from SD's paraphrase)

Queried the deployed Spirit store for the records SD cites. The actual text
changes the picture on one load-bearing point.

- **`l3k4`** (Decision, Medium): [message creates a log event for the existence of
  the message, but DELIVERY is established only when the router gets the
  harness-side acknowledgement; the router is the authoritative source for delivery
  facts]. **Two clauses.**
- **`17ss`** (Principle, Medium): [Router-acknowledgement = delivery durable on
  harness-side ack].
- **`n775`** (Decision, Medium, referent `message`): [the message component gains a
  meta-signal owner-policy plane … owner identity for SO_PEERCRED origin attribution
  arrives as authenticated owner policy over the meta-signal plane]. Confirmed real
  and load-bearing for the registry mechanism. ✓
- The fast path itself — "direct delivery," "publicly reachable" — returns **no
  record.** Y is unrecorded intent, still in dialogue (as SD says).

**The correction this forces:** SD says the fast path "finally realizes `l3k4`."
That is true of `l3k4`'s *first* clause (existence → message) and **the opposite of
its second** ([the router is the authoritative source for delivery facts]). On the
direct path message owns delivery with no router/harness ack — which contradicts
both `l3k4`'s delivery clause and `17ss` outright. So **Y does not realize `l3k4`;
it supersedes part of it.** Per the workspace rule that intent is primordial and
superseding it is always explicit, this matters: an agent told "Y realizes `l3k4`"
would contradict recorded intent believing it was honoring it. If the psyche wants
Y, `l3k4`'s delivery clause and `17ss` must be **explicitly superseded**, not
quietly overwritten — that is a higher bar than 111 frames, and it is the strongest
reason to treat Y as its own decision (below).

(Minor hygiene note: `l3k4` and `17ss` carry empty referent vectors — they're about
message/router delivery but tagged by domain only, so a referent query misses them.
Worth tagging `message` when they're next touched.)

## Where I agree with SD

- **Don't merge; keep the 0660/0600 split.** The SO_PEERCRED physics in `76.1` is
  irreducible — message is the only process that can mint origin. Unchanged.
- **`message` should stop being empty.** `l3k4` assigns it the existence-fact and
  it owns nothing durable today. Realizing that is correct and overdue.
- **The meta-signal plane (`n775`) is the right carrier** for owner policy (the
  "publicly reachable" mark + uid→endpoint registry). This is consistent with the
  daemon discipline (binary meta-signal config, owner-only 0600 tier).
- **Q-answers #1 and #2 are forced, not chosen:** "public" ≡ ungated (no channel
  grant), and `direct ⇔ public ∧ local ∧ uid-known` — a remote agent always needs
  router because message has no transport. These follow from the physics; SD has
  them right.

## Where I'd push back — the one thing SD's framing obscures

**SD couples two separable decisions. They should be decided apart.**

- **Decision X — message owns the existence-fact durably** (76.1 Option A).
  Standalone good; fixes the under-built gap and the fragility. Existence is
  *path-independent* — message is the ingress for everything — so X needs no fast
  path to justify it.
- **Decision Y — message direct-delivers to public+local agents** (the new fast
  path). Heavier: a registry, a second decision branch, a delivery record, and a
  delivery path *inside the 0660 door*.

SD's load-bearing sentence — "direct delivery means message must own durable
state, so Q1 → build it" — runs the implication backward. X already forces
durable state; Y is not needed to justify building message. So **Y must stand on
its own cost/benefit**, not borrow X's. Recommend the psyche capture X now and
weigh Y separately.

## Three costs of Y that 111 underweights

1. **Y moves state *into* the untrusted door — the exact thing 76.1's isolation
   argument protects against.** 76.1's load-bearing point was: don't put durable
   state + a registry in the same address space as the 0660 external door. Y does
   precisely that (attenuated: no channel-grant adjudication, but a registry +
   a direct-path ledger now live behind 0660). SD frames Y as *resolving* the
   fragility; it actually *trades some isolation for latency*. That's a legitimate
   judgment call — but it is a trade, not a clean win, and the report should say so.

2. **Y fragments the delivery ledger.** 76.1's model is clean: existence→message,
   delivery→router, one place each. Y splits *delivery* ownership by path, so **no
   single component holds the complete delivery ledger.** SD's open #6 ("where does
   the complete ledger live") is the sharpest unresolved issue, and both
   resolutions cost: mirroring direct-path facts to router gives back part of the
   hop Y saved; making message's log the union puts the *complete* delivery ledger
   behind 0660 — maximal scope and maximal erosion of (1).

3. **Y decentralizes origin-policy enforcement.** "The fast path has no authority
   to leak" is true only of *channel-grant* authority. The fast path still carries
   the `MessageOrigin` stamp, and on the direct path **every public agent** — not
   just router — must enforce origin policy (accept/reject `External(Owner)` vs
   `NonOwnerUser`). Router centralizes that today; Y distributes it to N agents.
   Safe *iff* "public" agents are genuinely low-authority and don't gate on origin;
   risky if any public agent takes owner-only actions off a direct-delivered stamp.
   This is the real content of SD's #3, sharpened: message becomes the trust anchor
   for the mesh, and the *enforcement* obligation fragments outward.

## Two correctness questions to add to SD's list

- **TOCTOU on the registry.** Path selection reads owner policy that the
  meta-signal plane updates asynchronously. A public→private revocation racing an
  in-flight message means a message direct-delivers to a no-longer-public agent.
  Probably benign (it *was* public), but the registry's consistency model vs SD's
  "atomic path selection" (#5) needs pinning.
- **Recovery-guarantee asymmetry.** Router's durable ledger gives crash-recovery /
  redelivery. If message crashes mid-direct-delivery, either message grows its own
  durable delivery state + redelivery (more scope, more state behind 0660) or the
  direct path is **best-effort** — a *weaker* guarantee than the routed path. Two
  delivery paths with two different durability guarantees is a real semantic split
  the design must state, not just "delivery splits by path."

## My recommendation

**Capture X now; gate Y.** Realizing `l3k4` (message owns existence durably) is an
unambiguous win — do it, and it dissolves 76.1's fragility on its own. Treat the
fast path Y as a *separate, later* decision, gated on: (a) evidence the local-public
traffic is actually high-volume enough to be worth a hop (the latency case is
asserted, not measured), and (b) a resolved answer to the ledger-completeness (#6)
and recovery-guarantee questions. If the psyche wants Y, the cleanest containment
is: message's direct-path record is **existence + a best-effort delivery ack**, the
**complete** delivery ledger stays mirrored in router (so audit has one home), and
"public" is contractually constrained to origin-agnostic, low-authority agents — so
the per-agent enforcement burden (cost 3) is real-but-bounded.

Net: SD's instinct is sound and the design is coherent; my one structural
disagreement is the bundling. Decoupling X from Y lets the psyche bank the certain
win without committing to the scope, the in-door state, and the split ledger that Y
brings — which are exactly the properties 76.1 spent its argument protecting.
