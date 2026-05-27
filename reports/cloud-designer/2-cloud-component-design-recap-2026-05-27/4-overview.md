# 4 · Overview — cloud component design recap (synthesis)

Synthesises the three preceding sub-agent reports
([1-spirit-substance.md](1-spirit-substance.md),
[2-existing-reports.md](2-existing-reports.md),
[3-repos-and-architecture.md](3-repos-and-architecture.md)) into
answers to the four framing questions
([0-frame-and-method.md](0-frame-and-method.md)).

## Prior-art note

`reports/cloud-operator/8-cloud-component-design-recap-2026-05-26/`
is a frame-only attempt at this same recap, filed yesterday under
the (then-misnamed) cloud-operator lane. Its method is
substantially identical to this one — three read-only scouts +
overview synthesis. Only the frame landed; no scout reports, no
synthesis. The current pass effectively completes it; the
landing changes lane to cloud-designer where it belongs.

## 1 · What IS cloud?

The cloud component is a **triad** (daemon + `signal-cloud`
working contract + `owner-signal-cloud` policy contract) that
**owns cloud-provider API management** [spirit 281, 294]. It is
the home for the machinery that talks to Cloudflare, Google
Cloud, Hetzner Cloud, and similar HTTP-API external systems. The
component sits on the **execution** side of the Criome
ecosystem; its peer `domain-criome` owns **domain meaning** and
provider-neutral projection. Cloud applies plans from authorised
sources to provider APIs; it does not decide what domains exist
or which records are correct.

The triad inherits every universal invariant from
`skills/component-triad.md`: the thin-CLI rule (one Signal peer,
no DB, no peer sockets), the wire-only-`signal-frame` rule, the
three-layer verb stack (Contract Operation → Component Command
→ Sema Operation), two authority tiers ordinary + owner, one
`cloud.redb` opened through `sema-engine`, single-NOTA-argument
binaries, no flags.

## 2 · What is its scope?

**Current ground (in code and contract):** Cloudflare DNS, with
Cloudflare settings and redirect rules slated as the
first-generation triad targets [spirit 282, 294, 680, 685].
First daemon runs almost-stateless — volatile in-memory cache
of last-known Cloudflare state, Cloudflare itself as source of
truth [spirit 681, 687]. Authentication is environment-variable
population via the FEMOS password-manager utility pattern
[spirit 682]; cloudflare-rs v0.14.1 is the substrate, with
`reqwest` filling the crate's coverage gaps (Rulesets, Pages,
Batch endpoint, CAA records) [system-operator/156].

**Projected expansion:** Google Cloud + Hetzner Cloud as
provider plugins [spirit 296]. Build-time opt-in via per-provider
Cargo features [spirit 283, 342;
third-designer/22-cloud-criome-design-research/4-opt-in-feature-compilation-design.md]
— `default = []`; published binary carries no provider; the
daemon's `(Help Main)` reply lists exactly what was compiled in.
Capability discovery distinguishes
*built-but-unconfigured* from *not-compiled-in*, so silent
failures don't hide a missing provider.

The cloud daemon may eventually **self-upgrade** when a
capability is requested that isn't built in [spirit 284, 295] —
conditions and mechanism undefined. Open question.

## 3 · What's settled vs. what's open?

### Settled (Medium+ magnitude)

- **Triad shape and naming.** Three repos (cloud + signal-cloud
  + owner-signal-cloud) created and building with cited commits
  [system-operator/160]. Repository names are unprefixed
  (`cloud`, not `persona-cloud` or `signal-cloud-daemon`); CLI
  binary is `cloud`; daemon binary is `cloud-daemon`; sockets
  are ordinary + owner Unix domain sockets at distinct modes.
- **Cloud plan preparation belongs on the owner signal surface**
  [spirit 325]. `Plan` materialises daemon state, so it lives
  on the policy contract even though its typed reply looks
  read-like. `Observe` + `Validate` stay on the ordinary
  contract.
- **State-machine model:** `Plan` renamed to `Mutate` with a
  two-state lifecycle — **Mutate-sent** (provider request not yet
  acknowledged) → **Mutated** (acknowledged) [spirit 338;
  third-designer/25-most-important-questions-2026-05-24/2-cloud-mutate-quorum-multi-zone.md].
- **State across Criome is last-known-acknowledgment, never
  live-query** [spirit 339], with quorum-of-agreement by
  acknowledging changes. Domain-criome may resolve unowned
  domains via cached last-known content-addressed records
  [spirit 340].
- **Provider-set is build-time opt-in.** Cargo features per
  provider gate dependencies and dispatcher modules; discovery
  via `(Help Main)`.
- **Production push prioritised over schema-engine migration.**
  MVP deliberately skips the new schema-engine approach to ship
  faster [spirit 684]; the schema-engine integration is
  deferred until the spirit MVP cuts over. Hand-written
  `signal_channel!` macros are the production wire surface for
  this push [second-designer/196-cloud-component-production-design-2026-05-25.md].
- **Authentication starting point:** env-var + FEMOS
  password-manager pattern [spirit 682]. Explicitly flagged as a
  starting point pending detailed-design investigation of safer
  alternatives.

### Open (load-bearing, awaiting psyche resolution)

- **meta-signal rename** (`owner-signal-*` → `meta-signal-*`):
  ~169 code symbols, ~95 ARCH lines, ~105 workspace files
  affected. Anchored on spirit 290 + 299, both **Minimum
  certainty**. Survey at
  third-designer/22-cloud-criome-design-research/5-meta-signal-rename-impact.md.
  Held for explicit psyche affirmation at Maximum certainty
  before execution.
- **Persona socket-binding via `SCM_RIGHTS`:** Persona binds the
  stable public socket per component and hands accepted FDs to
  the active daemon version. Flagged in
  third-designer/23-architecture-update-2026-05-23/0-orchestrator-synthesis.md
  as load-bearing for version-handover atomicity.
- **Content-addressed domain authority + Sub-ID identity
  primitives:** landed contracts use string newtypes; new
  intent records (311–320) require stronger identity typing.
  Partial sketch in
  third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md.
- **Self-upgrade conditions:** when does the cloud daemon
  self-upgrade for a missing-capability request, and through
  what mechanism? [spirit 284, 295]

### Constraints

- **Old Rust signal macro path on the production slice** [spirit
  679] — acknowledged technical debt, blocking-magnitude for
  the production deployment.
- No provider credentials in source, logs, or ordinary Signal
  records; secret material crosses owner policy only by handle
  [cloud/ARCHITECTURE.md].
- No deprecated `signal-core` in new code [cloud/ARCHITECTURE.md];
  sema-engine persistence is deferred specifically because
  sema-engine still depends on `signal-core` and that swap-out
  must precede full persistence wiring.

## 4 · Does the code exist?

**Yes — skeleton state.** All three triad repos plus the three
domain-criome triad repos are created and building with commits
cited in system-operator/160. The runtime
(`/git/github.com/LiGoldragon/cloud/`) has:

- Cargo.toml with two binaries.
- ARCHITECTURE.md.
- schema/ directory (placeholder for future schema work).
- Daemon multi-module code: `client.rs`, `cloudflare.rs`,
  `daemon.rs`, `lib.rs`.
- Ordinary + owner Unix socket binding.
- `signal-frame` decoding.
- Read-only Cloudflare DNS observation via env-var credential
  handles.

**Intentionally deferred per cloud/ARCHITECTURE.md (43–66):**

- Cloudflare live mutation (provider actor exists; apply
  endpoint returns typed rejection until mutation actor is real).
- sema-engine persistence (waiting on `signal-core` removal).
- Redirect observation and mutation.
- Schema-engine integration (waiting for schema MVP via
  spirit-next cutover).

**Template peer:** the most mature triad to mirror is
`persona-spirit/` — full Kameo-actor topology in a 35 KB
ARCHITECTURE.md, complete operation path, all five invariants
followed. Cloud should adopt persona-spirit's directory
organisation and socket/database naming as the actor topology
fills in.

## Next move

The component is past birth and into the **production-first
fill-in** phase: the next cloud-designer work item is not a new
triad, it is closing the gaps between the skeleton and the
production-pushable shape per
second-designer/196-cloud-component-production-design-2026-05-25.md.
Concretely:

1. **Audit the four open positions** above against the spirit
   records made since each was filed. Confirm none have been
   superseded; if any have, retire the open-question entry.
2. **Decide whether to land the Mutate/Query channel split now
   or defer**: the design is settled per intent 325 + 338, but
   no implementation report yet records that the move happened
   in the landed contracts. Either fix the contracts to match
   the design or carry the misalignment as a known seam until a
   subsequent psyche refinement re-anchors it.
3. **Surface the schema-engine deferral as an explicit timing
   record** — when does cloud cut over from hand-written
   `signal_channel!` to schema-derived? Currently "after spirit
   MVP" but the timing isn't a Spirit record yet.
4. **Audit the `cloud-operator` lane's seven pi-harness
   reports** under the standard context-maintenance rule — they
   are clearly mis-laned (per sub-agent 2's verdict) and should
   either migrate to `pi-operator/` or retire. Out of scope for
   this recap pass; flagged for a follow-up.
