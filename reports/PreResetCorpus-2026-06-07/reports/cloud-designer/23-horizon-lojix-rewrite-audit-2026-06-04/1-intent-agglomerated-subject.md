# A4 — Horizon / Logix rewrite: the agglomerated intent narrative

Cloud-designer lane, 2026-06-04. Read-only design audit. This is the
file a future agent reads INSTEAD of the ~40 scattered Spirit records
and the legacy `intent/*.nota` substrate behind the Horizon + Logix
(`lojix`) rewrite. It synthesizes the three intent sweeps (A1
Horizon-side Spirit, A2 Logix-side Spirit, A3 legacy substrate) into one
narrative organized by theme. Every claim cites the record id or
`file:line` it rests on. Nothing here is invented intent; where the
corpus is silent, that silence is named as an open question.

## The one-sentence vision

Two components replace the production deploy monolith: **Horizon** is a
deliberately minimal projection surface that turns authored cluster
*facts* into Nix-consumable typed values, and **Logix** (the `lojix`
component) is a traditional triad-engine daemon that orchestrates the
deploy. Finish both to parity, cut over, and retire the dual
production/next deploy stacks (`75auhtr308tgt4kaa9a`, Decision, High).

## Theme 1 — Horizon is minimal: WHAT, never HOW (DECIDED)

The apex principle for Horizon, and the most universal intent in the
arc. Horizon expresses only **what** the psyche (as cluster user) wants
the cluster to do — typed facts — and never **how**, and never
decision-making. Horizon emits simple typed facts; **Nix consumes them
and composes the complex decisions downstream**, so complexity stays out
of Horizon (`7ggswqdxqqz97za6o7w`, Principle, High). Everything else
about Horizon serves this.

This is not new direction. It is the faithful restatement of a
2026-05-20 Maximum-certainty legacy Principle: cluster data must not
embed operational constants — ports, derived addresses, well-known
constants live in the *consumer*, not Horizon (`intent/horizon.nota:15-20`,
synthesized into the lean `horizon-rs/horizon-leaner-shape/INTENT.md`
§Beautiful horizon over beautiful Nix at `INTENT.md:73-94`). The legacy
substrate states the rule sharply: **prefer beautiful Horizon over
beautiful Nix — ugliness goes in Nix** (`intent/horizon.nota:57-62`,
`INTENT.md:21-23`). The session record `7ggswqdxqqz97za6o7w` is the
refreshed High-certainty head of that lineage; no legacy intent is
orphaned by it.

Two corollaries carry the principle into the type system:

- **Variants over booleans.** Express a fact as a data-carrying variant
  where inline tuning is part of the dial, not a boolean flag
  (`intent/horizon.nota:1-13`, `INTENT.md:29-39`).
- **No input/output type duplication.** Where the input type can also
  serve as the output type for a passthrough value, reuse it rather than
  defining parallel in/out type families; fewer reused types keep the
  model small (`10v4744869xt5spwnam`, Principle, High). This too is a
  faithful refresh of a 2026-05-20 Maximum Principle
  (`intent/horizon.nota:64-69`, `INTENT.md:97-106`), not new intent.

Minimalism is thus enforced at two levels at once: the *semantic*
boundary (facts, never decisions) and the *type-count* level (reuse,
never duplicate).

## Theme 2 — the split: Horizon stays a hack, Logix carries the triad (DECIDED)

The defining structural decision of the arc, and the resolution of a
long-open question. Horizon stays the simple projection surface — "a
hack for now," and that is acceptable — and is explicitly **NOT** a full
triad component (no actor engine, no Signal/Nexus/SEMA runtime).
**Logix (`lojix`) is the more traditional component that receives the
full triad-engine + schema-based-component port** (`1bok2bxvu3beswif9mv`,
Clarification, High).

This closes a trichotomy that sat open across the whole legacy
substrate. The earlier record `1vymk533gmb43v78e46` (Medium) left
Horizon's runtime shape open — maybe signal-only, maybe full triad,
maybe pure-projection library — and named datatype-generation as the
thing that would illuminate the choice. `1bok2bxvu3beswif9mv` resolves
it: Horizon = projection surface, Logix = triad. The same open question
appears in two GC-context reports — cloud-operator report 11 finding #7,
and system-operator report 167's "Next Best Step #2" both asked "is
Horizon a library or a component?" — and is now answered. Treat the
Horizon-as-triad-component framing in those older reports (and in the
system-operator/167 pure-schema prototype, which gave Horizon
`Input`/`Output` planes) as **superseded**: its value survives only as
proof that the schema pipeline works, which is evidence for Logix, not a
shape for Horizon.

One tension to carry forward. The earlier Decision `6wzz3up583b428kh3ok`
(High) bundles "lojix-horizon" together as a schema-deep rewrite with a
deep actor system, schema-defined interfaces AND data shapes, method-only
Rust. Read against the later split (`1bok2bxvu3beswif9mv`) and the
High-certainty minimalism principles, the resolved reading is: **the
deep actor system is Logix's; Horizon's share of `6wzz3` is only the
schema-emitted typed data model** (the datatypes generate regardless of
runtime shape), NOT a runtime engine. `1bok2bxvu3beswif9mv` governs the
split; `6wzz3`'s actor-system depth applies to Logix.

## Theme 3 — cluster-data is typed end-to-end, source-first (DECIDED)

The canonical pipeline and its anti-pattern correction. Cluster-data
features must be **typed end-to-end**, and the correct order is
**typed-source-first** (`431pfi7l1akuu22b01b`, Correction, High):

1. Extend the `horizon-rs` model with a real typed `NodeService` enum
   variant carrying `NotaEncode`/`NotaDecode`, modeled on the existing
   `NixBuilder` variant.
2. Author the fact in `goldragon`'s `datom.nota`.
3. Project it typed through `horizon-rs`.
4. Consume the typed value in CriomOS.

Explicitly forbidden as garbage: string keys at schema positions,
defensive or-empty-list defaults, and synthetic-fixture-fed checks. The
record arose from a concrete failure (VmTesting modeled as a string).
The taxonomy names **roles, not hosts**: the canonical reference is
`NodeService::LargeAi` (the large-ai-node role), not "Prometheus" —
Prometheus merely fills that role today (`1n6ew7o2lx9coz3wfqg`,
Correction, High).

The live driver behind the correction is the VM-testing CriomOS feature:
a real display/GPU/DRM VM, Nix-native, CI + interactive
(`7d326jk90fwf0olwfwr`, High), with a per-node gpu-passthrough option
disabled on the large-ai-node (`76qdqown4iuutjmloiq`, High), deployable
to the router node only if networking is proven non-breaking
(`5hir5bnz9af64zjg53d`, High), reachable via a Criome domain
(`7hckmg8fateik7xlm25`, High). These are CriomOS-feature intent, not
Horizon-architecture intent — they bound the data Horizon's
`NodeService` taxonomy must eventually carry as typed variants, and they
are the concrete first case the typed-source-first discipline must
absorb.

## Theme 4 — Logix is the deploy orchestrator (DECIDED direction, model under-captured)

Logix's domain is the cluster deploy itself. The legacy `intent/deploy.nota`
arc is the architecture the lean rewrite builds toward, and it is still
live (not superseded):

- **Deploys are local execution per concern; the node deploys itself.**
  The daemon coordinates remote build/cache daemons but holds no remote
  SSH activation session — this eliminates the SSH-disconnect-survival
  engineering that the production Stack A was built around
  (`intent/deploy.nota:1-13`). This is the core rationale for the whole
  Logix rewrite.
- **Three deploy variables:** where the build happens, where the Nix
  cache is, and where the target is (always the node itself)
  (`intent/deploy.nota:8-13`).
- **Logix maintains believed cluster + network topology state** —
  reachability, latency, bandwidth, cost — informing routing decisions
  (`intent/deploy.nota:15-20`). This is the direction for Logix's SEMA
  (durable-state) plane.
- **Logix owns `nix.conf`**, restarting `nix-daemon` for transient
  per-deploy substituter trust keys; every node has a Nix signing key
  (`intent/deploy.nota:22-34`).
- **Daemons talk to daemons; the CLI only initiates;** the operator
  machine is a thin client (`intent/deploy.nota:43-48`) — matching
  `1bok2bxvu3beswif9mv`'s framing of Logix as the traditional triad
  component whose CLI is its first thin client.

The one fresh, concrete scope decision in Spirit: **`lojix-daemon` owns
GitHub-authenticated Nix flake-input resolution** — it pulls the GitHub
key from gopass and injects it via `NIX_CONFIG` access-tokens through a
small Rust library the daemon calls. GitHub rate-limit
stale-activation is a deploy-path problem owned by Logix, not the
Pi-package (`1orezxnzgedct1grkn4`, Decision High; implementation form
only Medium). This is the clearest signal that Logix's **Nexus** plane
is the deploy/build orchestration brain.

OPEN / under-captured (flagged in Theme 8): the deploy-orchestrator
*domain model* — generations, GC-roots, build cache, the Nexus
deploy-decision vocabulary, and the Logix wire contract — is essentially
**un-captured in Spirit**. Those concepts live in code and reports, not
intent.

## Theme 5 — the triad shape Logix must adopt (DECIDED, fully specified)

The triad architecture Logix ports onto is the most thoroughly captured
part of the corpus (these are workspace-wide component-shape records, not
Logix-specific, but they govern the port):

- **Three schema TYPES map to three runtime planes**
  (`35rca20ls4n2v0hwi6f`, High; `7df3iwgjympmx09xb4u`, Principle, High):
  **Signal** (comms/wire), **Nexus** (execution, heavy compute and
  decisions — the former "Executor", now renamed), **SEMA** (durable
  state). The flow is Signal → Nexus → SEMA → Nexus → Signal → client
  (`xj4c6f51lin3uix5`, Principle, High; `60h680s4gg5ziy81vaa`,
  Clarification, High): SignalEngine triages the wire and preserves reply
  correlation; NexusEngine owns the heavy decisions over the Signal
  message + SEMA replies; SemaEngine owns durable state.
- **The contract repos carry wire vocabulary ONLY.** `signal-lojix`
  (ordinary working wire) and `meta-signal-lojix` (policy wire) hold
  Signal Input/Output roots, record types, and the codec — and emit NO
  engine traits; Nexus/SEMA are daemon-internal
  (`4b5gisizo80a9c5de1g`, Correction High; `394s6ikhccnt4mxnott`,
  Maximum). The Sema classification words
  (Assert/Mutate/Retract/Match/Subscribe/Validate) must never leak onto
  the wire as request-root tags — domain verbs only, Sema class derived
  internally (`5vy3adk1bn8t30ig7w2`, Decision, High).
- **The Nexus and SEMA plane schemas are separate `.schema` files inside
  the lojix daemon crate** (e.g. `lojix/schema/nexus.schema`,
  `lojix/schema/sema.schema`), each importing the wire-contract Signal
  IO — NOT separate crates or repos (`1up1ufia24c2opn3mqn`, Decision High;
  `7joz3dmegqiptqgra5p`, Correction VeryHigh; `2auv4uvj4cr71iy2emj`,
  Correction High). A component is three schemas minimum. (One record,
  `2bgatqufm9m0dktxkv5`, prints at Certainty Zero — a likely unset
  default — but is corroborated by three higher-certainty records; treat
  the shape as settled.)
- **Runtime is terse and generated.** Every component conducts core logic
  through schema-emitted traits whose methods take/return root types;
  runtime = composition of trait impls (`r59l2td3o6pvq9vhl3`, Principle
  VeryHigh). Logix plugs into the generic triad runtime runner being
  extracted (`5pcw3e6jsldovqho5nq`, High), gets engine mechanism / runner
  shape / trace plumbing from generation
  (`75ccxoajlbvlwds7lmz`, `1mttcjcny0w2737btig`), with `on_start`/`on_stop`
  lifecycle hooks (`4ffjo8wto0uymelwzel`) and tracing built into the
  generated engine traits as default impls (`6cm8ptey04dka3t9uem`).
  Handwritten Logix Rust fills only domain decisions
  (`6i4xbkbubwpoz5evzcs`, `34fk3wdhzfzwr3u0nuf`). It reuses the NOTA codec
  rather than emitting a parallel one (`1d7c1tpiaia2dhxa781`, Maximum) and
  obeys method-only-no-free-functions (`4y8jq32f2us1eld7anj`, Maximum).
- **Daemon config is binary (rkyv), not a NOTA CLI arg.** The daemon
  reads an rkyv state file at a known path or enters STANDBY awaiting a
  config-signal, and can carry MULTIPLE signal interfaces (working +
  meta + config) enumerated by a top-level numerator enum
  (`cebbheusoakkpevjgs`, Decision, High) — directly relevant since Logix
  needs a config-signal alongside its working and meta signals.
- **Policy contract is born `meta-signal-lojix`, never `owner-signal-lojix`.**
  The fleet rename owner-signal → meta-signal is active work, not
  tentative (`3lchri1gcxm3mc7ltm3`, `2hstvjvbxb8z0tp0xsp`,
  `1n5b0k32jjw75rhgkb6`, all High), superseding the stale
  `3i3hed0a6790r2clvo3` (Medium). The split into `signal-<c>` +
  `meta-signal-<c>` is about rebuild-churn isolation and authority
  visibility, not state/logic location (`7f5nk0cnkv8xov3qtrc`, High).

The legacy `intent/deploy.nota` already anticipated the contract split:
`signal-lojix` splits Deploy into Build/Activate/Deploy/Rollback (verbs
are cheap; Activate-vs-Deploy collapse left open,
`intent/deploy.nota:71-76`), and the policy contract is no longer
deferred — build it now (`intent/deploy.nota:57-62`, with the
owner→meta rename applied).

## Theme 6 — the cutover goal and its gating (DECIDED)

The apex Decision: **finish the rewrite to cutover and retire the dual
stack** — the production Stack A monolith (`lojix-cli`) and the lean
Stack B rewrite (`horizon-leaner-shape`) — ending the parallel
maintenance burden (`75auhtr308tgt4kaa9a`, Decision, High). The lean
lojix/horizon stack becomes the main deployment after MVP
(`a5anew11ndgk5cq40z`, Decision, High).

The posture is **reach parity, then switch — no heavy formal cutover
plan**. The cutover is per-node, not flag-day: the production `lojix-cli`
IS the bootstrap path, so bootstrap is not a gap
(`intent/deploy.nota:50-55`, codified in
`protocols/active-repositories.md`). The closest precedent for the
posture is the Spirit cutover: move to the new schema-derived target
when close enough, no heavy plan (`30i1vnjilr9wuj8m9zm`, Decision, High;
Spirit-specific, cited as precedent not as a Logix decision).

The gating constraints:

- **Sandbox testing is a precondition** for cutover to main deployment
  (`29o9zjczlfvp2n7o28d`, Constraint, High); Prometheus has an existing
  nspawn-based sandbox as the audit-start pointer
  (`4xb0llpz53s1kst0n6e`, Minimum).
- **Prototypes must use the designed components FULLY** — develop an
  incomplete component rather than bypass it (`5wo8xmt0qpl6u6t10md`,
  Constraint, High).
- **Horizon's pure-schema work is proven by a working end-to-end
  prototype** — imports → assembled schema → generated data types — not
  design prose (`3zue95xkt8gzui12cao`, Constraint, High).
- **High-confidence production CriomOS changes are ported into the
  rewrite stack immediately** where the correct change is clear, then
  builds are tested (`6pmeinb6tqtdotsgi4u`, Decision, High).
- **Every code/logic change bumps the component version** (≥ patch),
  carried by a versioning skill (`6lyf1a5nuoew2qr6zt7`, Decision, High).
- Router-node deploys are bounded by router-safety: boot-mode / BootOnce,
  never a live switch (`3bwb44y2z`, `1khq45xxg`, `5er7r9fj9whba2ewgit`).

## Theme 7 — the biggest STALE-vs-CODE gap the cutover must absorb

The single most consequential finding for an implementer. The
**role-merge** is settled intent but NOT landed in code.

The legacy arc settled (Maximum/Medium, 2026-05-21) a sweeping redesign:
merge `NodeSpecies` + `NodeService` into ONE `roles: Vec<Role>` field
in first position; drop the derived booleans down to CriomOS-lib; retire
`view::BuilderConfig`, `online`, `node_ip`, `transitional_ipv4_lan`;
rename `Contained` → `Pod`; fold bare bools into role variants; species
collapses to Center/Edge/CloudHost (`intent/horizon.nota:190-202`,
captured in `INTENT.md:41-71`).

The deployed code has NOT done this. Verified this session against the
lean stack: `NodeProposal` at
`horizon-rs/horizon-leaner-shape/lib/src/proposal/node.rs:32` still
carries `pub species: NodeSpecies`, and the same struct at
`proposal/node.rs:86` still carries a separate `pub services:
Vec<NodeService>`. The struct also still holds the very fields the merge
intends to retire/fold — `online: Option<bool>` (`node.rs:79`), `node_ip:
Option<NodeIp>` (`node.rs:43`), and bare bools `nordvpn`, `wifi_cert`,
`wants_printing`, `wants_hw_video_accel` (`node.rs:47-63`). So
`INTENT.md` describes the **destination** schema; the code is at the
**origin** schema. The session records do not re-touch the merge, so it
remains open implementation debt the cutover must either land or the
psyche must confirm as deferred.

## Theme 8 — what is OPEN (flagged for psyche or design)

- **The Logix deploy-orchestrator domain model is un-captured.** Spirit
  returned NO records for `logix`/`signal-lojix`/`stack`/`flake`/`datom`/
  `generation`/`gc-roots`/`cache` as topics. Generations, GC-roots, build
  cache, and the Nexus deploy-decision vocabulary are design-space in
  code/reports, not intent. `meta-signal-lojix` is not captured at all,
  and the `signal-lojix` repo is a skeleton (the orchestrator frame notes
  `signal-lojix/ARCHITECTURE.md` still documents the OLD three-layer
  signal-frame/signal-core/signal-sema migration, not the new
  schema-derived triad).
- **The `lojix-daemon` flake-auth library's implementation form is only
  Medium** (`1orezxnzgedct1grkn4`).
- **The role-merge implementation status** (Theme 7) needs an explicit
  land-or-defer call.
- **Activate-vs-Deploy verb collapse** on the `signal-lojix` contract was
  left open in the legacy substrate (`intent/deploy.nota:71-76`).
- **Criome-mediated authorization for Logix** is live-as-destination but
  explicitly deferred from the current migration arc
  (`intent/deploy.nota:36-48` vs `intent/deploy.nota:64-69`) — the
  cutover should NOT block on it.

## Provenance and supersession ledger

- Faithful refreshes (session records restate prior Maximum Principles,
  not new intent): `7ggswqdxqqz97za6o7w` ← `intent/horizon.nota:15-20`;
  `10v4744869xt5spwnam` ← `intent/horizon.nota:64-69`.
- Resolved-open: `1vymk533gmb43v78e46` (Medium, Horizon runtime-shape
  open) is superseded by `1bok2bxvu3beswif9mv` (High). The only surviving
  nugget of `1vymk533` is the mechanical finding that a pure-projection
  Horizon needs a types-only-module schema shape — carry that into the
  design, drop the trichotomy framing.
- Stale naming: `3i3hed0a6790r2clvo3` (Medium, owner-signal stays active)
  superseded by the active meta-signal rename records.
- Stale-vs-code: the role-merge (Theme 7) — intent settled, code at
  origin.
- One-shot working orders that predate the working-orders-are-not-intent
  discipline and should be treated as stale/completed: the three
  persona-spirit deployment records at `intent/deploy.nota:78-97`; the
  execution-sequence tail of `6wzz3up583b428kh3ok` (reload → self-train →
  vision report → dispatch subagent); the handoff order
  `ifcmomoobjs4f3vaw7` (operator inspects the schema-pipeline frame).
- GC'd, not a gap: designer reports 207/208/246/248 were collected after
  their substance was lifted into Spirit and the per-repo `INTENT.md`;
  the designer-report layer is no longer a source for this arc.

## Internal consistency

The High-certainty corpus is internally consistent. The only resolved
contradiction is the `6wzz3` (lojix-horizon deep actor system) vs
`1bok2` (Horizon NOT a triad) tension, settled in Theme 2 in favor of
`1bok2` governing the split and `6wzz3`'s depth applying to Logix. The
only certainty gaps are `1vymk533` (Medium, already resolved) and the
under-captured Logix domain model (Theme 8).
