# Perspective 2 — The Component Constellation

Grounded read of the live Persona/Sema/Signal component set: the triad
pattern that every stateful capability follows, what each component owns,
and the who-does-what relationships. Sources are cited inline; every claim
traces to a real file under `/home/li/primary/` or `/git/github.com/LiGoldragon/`.

Primary sources read:
- `protocols/active-repositories.md` (the live repo map)
- `skills/component-triad.md` (the universal shape)
- Per-repo `INTENT.md`: spirit, criome, router, mirror, message, mind, persona, harness
- `mirror/ARCHITECTURE.md` (object-move / version-control detail)

## 1. The repo-triad pattern — packaging

Every stateful capability is THREE repos, not one (`skills/component-triad.md`
§"The shape", lines 83-112):

```
<component>/              runtime: lib + <name>-daemon + thin <name> CLI
                          + daemon-local schema/{signal,nexus,sema}.schema
signal-<component>/       ordinary working wire vocabulary (WireContract → zero engines)
meta-signal-<component>/  meta policy authority/configuration vocabulary (WireContract → zero engines)
```

Load-bearing distinctions:

- **The CLI is NOT a triad leg.** It is the daemon's thin first client,
  bundled in the runtime repo (`component-triad.md` lines 110-111, and the
  AGENTS.md triad override). A component is daemon + two wire contracts.
- **Two "Signal" schema files, kept distinct** (`component-triad.md`
  lines 20-81). The *public signal contract* lives in `signal-<component>`
  (emission target `WireContract`, wire types + codecs only, the single
  source of wire types for every linker per intent `tb9h`). The
  *daemon-local signal runtime* lives in `<component>/schema/signal.schema`
  (emission target `SignalRuntime`, emits the `SignalEngine` trait OVER the
  imported contract types, never a second copy).
- **Single-source rule governs the meta contract too**: the daemon imports
  its meta vocabulary from `meta-signal-<component>`; it never declares a
  local meta-signal wire contract in-tree (`component-triad.md` lines 44-59).
  spirit currently violates this (local `schema/meta-signal.schema`, no dep
  on `meta-signal-spirit`) — a named gap, not the target.
- **Three concrete properties bought by the split** (lines 114-139):
  rebuild-churn isolation (peers depend on the small stable contract, not
  the churning daemon), security-sensitivity visibility (owner-only ops in a
  distinct repo = repo-boundary authority), and meta-signal optionality (a
  component with no owner ships two repos).

### Binary naming (lines 142-209)

A component is TWO binaries: CLI `<component>` (the role-name humans type)
and daemon `<component>-daemon`. The repo may carry a system prefix
(`persona-spirit` ships CLI `spirit` + daemon `persona-spirit-daemon`).
No `-cli`/`-server`/`-service` suffixes; `lojix-cli` is a transitional
carry-over, not the convention.

## 2. The runtime triad — three engines INSIDE the daemon

Distinct from the repo triad. Inside the `<component>` daemon, three
schema-driven planes organize logic (`component-triad.md` §"Runtime triad",
lines 733-1160), matching the three schema types:

| Engine | Schema type | Role | Trait shape |
|---|---|---|---|
| **Signal** | `Signal` | wire + communication: admission, dispatch, identity-stamp, frame triage. No heavy logic. | `triage(Signal<Input>) → Nexus<Input>` + `reply(Nexus<Output>) → Signal<Output>` |
| **Nexus** | `Nexus` | the in-between: heavy logic, mail keeper, Signal↔SEMA translator. Most work here. ALSO the engine's feature catalog (every internal feature MUST be a Nexus verb/object — visibility, not hidden code). | `execute(&mut self, Nexus<Input>) → Nexus<Output>` / `decide(NexusWork) → NexusAction` |
| **SEMA** | `Sema` | durable single-writer state over redb/`sema-engine`. Writes serialize; reads concurrent. | `apply(&mut self, Sema<WriteInput>) → Sema<WriteOutput>` + `observe(&self, …) → …` |

Flow: Signal IN → Nexus accepts mail (BEING-PROCESSED) → Nexus translates
to SEMA query → SEMA runs + produces reply (carries the database marker) →
Nexus translates SEMA reply to Signal response → Signal OUT
(`component-triad.md` lines 855-868). The engines are **kameo actors** now
(lines 882-907); `_inner` methods stay sync-pure component logic; the actor
shell drives the `NexusWork`/`NexusAction` loop async (lines 986-1047).

Nexus's inner-world/outer-world framing: Signal owns the OUTER boundary
(cross-process wire), SEMA owns the INNER boundary (durable state), Nexus is
the center that decides (lines 1141-1160). The canonical worked example for
the whole runtime triad is **spirit**.

## 3. The live component set

From `protocols/active-repositories.md` §"Current Core Stack" and the
per-repo INTENT files. Each row: name — one-line role — its triad
(✓ = the contract repo exists in the repo map).

| Component | Role (grounded) | Triad |
|---|---|---|
| **spirit** | Production Spirit daemon; records psyche intent; current copyable schema-derived triad exemplar (the runtime-triad worked example). | `spirit` + `signal-spirit` ✓ + `meta-signal-spirit` ✓ |
| **criome** | Minimal Spartan BLS12-381 auth/attestation: verify/sign, identity registry, delegation grants, replay guard, audit log. *Criome verifies; Persona decides.* | `criome` + `signal-criome` ✓ + `meta-signal-criome` ✓ |
| **router** | Routing policy, delivery state, authorized-channel authority; one per system; router-to-router TCP forwarding over the tailnet. Binds `router.sock` (0600). | `router` + `signal-router` ✓ + `meta-signal-router` ✓ |
| **message** | Stateless stamp-and-forward ingress (engine-owner edge). Mints SO_PEERCRED provenance, forwards typed frames to router. No durable ledger. Binds `message.sock` (0660, engine-owner group). | `message` + `signal-message` ✓ + `meta-signal-message` ✓ |
| **mirror** | Payload-blind append-ingest version-control remote: validates blake3 digest chain (sequence continuity, expected head, idempotent dedup), fsync-before-ack, stores opaque payload/artifact bytes; serves every component store from one daemon. | `mirror` + `signal-mirror` + `meta-signal-mirror` (the three repos authorized by Spirit `0yx5`) |
| **mind** | Authority root of the Persona control plane: workspace state (work items, Thought/Relation graph, decisions, subscriptions, channel choreography policy). Observes up-tree, orders down-tree. Replaces lock files. | `mind` + `signal-mind` ✓ + `meta-signal-mind` ✓ |
| **persona** | Engine-manager / permissioned system daemon: supervises component daemons, owns upgrade orchestration, FD-handoff (SCM_RIGHTS) for lossless cutover, systemd template units, multi-engine supervision. | `persona` + `signal-persona` ✓ + `meta-signal-persona` ✓ |
| **harness** | Models interactive AI harnesses (Codex/Claude/Pi/Fixture) as addressable runtime objects: lifecycle, typed transcript observations, terminal/Pi-RPC delivery adaptation. | `harness` + `signal-harness` ✓ + `meta-signal-harness` ✓ |
| **orchestrate** | Orchestration component runtime; mind owns it, it owns router + harness (authority-chain example). | `orchestrate` + `signal-orchestrate` ✓ + `meta-signal-orchestrate` ✓ |
| **terminal** | Persona-facing terminal owner: named sessions, Signal adapter; control plane on Signal, raw-byte data plane carved out (`control.sock` vs `data.sock`). Consumes `terminal-cell` PTY primitive. | `terminal` + `signal-terminal` ✓ + `meta-signal-terminal` ✓ |
| **system** | Deferred OS/window observation (focus). | `system` + `signal-system` ✓ + `meta-signal-system` ✓ |
| **introspect** | Supervised inspection plane: queries live daemons over Signal, fans in typed observations, projects NOTA only at the human edge. NOT in the delivery path; opens no peer redb. | `introspect` + `signal-introspect` ✓ + `meta-signal-introspect` ✓ |
| **repository-ledger** | Records pushed repo changes from the local Gitolite server into a sema-engine DB. | `repository-ledger` + `signal-repository-ledger` ✓ + `meta-signal-repository-ledger` ✓ |
| **upgrade** | Schema/version migration orchestration + version-handover driver (triad scaffold). | `upgrade` + `signal-upgrade` ✓ + `meta-signal-upgrade` ✓ |

Adjacent/forthcoming (documentation-or-scaffold, bead `primary-kbmi`): `cloud`
(provider API management) and `domain-criome` (Criome-domain registry/resolution),
each with its own `signal-*` + `meta-signal-*` pair.

Named carve-outs that look like violations but aren't (`component-triad.md`
lines 591-613): pure libraries need no daemon (`signal-frame`, `signal-sema`,
`sema`, `sema-engine`, `horizon-rs`); high-bandwidth data-plane bytes get a
separate socket outside the triad (terminal's `data.sock`); a daemon may be a
Signal client of many peers (introspect → router/terminal/manager).

## 4. Who-does-what — the relationships

The constellation's division of labor, each grounded:

- **criome authenticates — signs/verifies, never transports.**
  *"Criome verifies; Persona decides"* (`criome/INTENT.md` lines 39-42).
  It answers "is this signature valid for this principal under this grant
  for these bytes?" — BLS12-381 from day one, out-of-band attestations only,
  content records carry no embedded proof. The router *"itself never holds
  keys or verifies signatures; that is criome's job, reached through a
  verifier seam"* (`router/INTENT.md` lines 73-74).

- **router transports — one per system, router-to-router.**
  Router owns routing policy, delivery state, channel authority
  (`router/INTENT.md` lines 3-6). It transports authenticated propagation
  to peer sides over plain TCP on the tailnet; *"Router's place in the chain
  is transport-only and event-causal"* (lines 78-91). The tailnet encrypts
  bytes; a criome attestation inside the forwarded frame authenticates the
  sending router — two separate concerns (lines 70-74). Carries a
  `RoutedContractObject` envelope of opaque rkyv octets.

- **mirror version-controls and moves objects.**
  The payload-blind sema version-control remote (`mirror/INTENT.md` line 1).
  In the spirit-vcs chain: spirit accepts a log object → asks local criome
  to authenticate it → router carries the authenticated propagation → remote
  criome/mirror act on the event → *"mirror fetches/restores the announced
  object state"* (`router/INTENT.md` lines 86-90). Mirror validates the
  blake3 digest chain and stores opaque bytes; it never decodes a
  component's record types (`mirror/INTENT.md` lines 37-40).

- **spirit records intent.**
  Production Spirit daemon; the deployed `spirit` CLI talks to
  `spirit-daemon` over rkyv. It is also the **runtime-triad exemplar**
  (`spirit/INTENT.md` lines 1-13). Owns the versioned-log-as-source-of-truth
  kernel inversion (record `iir4`) and logged-fold migration (`t0tu`).

- **mind / persona the agent (control) layer.**
  *mind* is the authority root of the control plane — observes up-tree
  (Assert/Match/Subscribe), orders down-tree (Mutate/Retract:
  ChannelGrant/Extend/Retract, AdjudicationDeny); replaces lock files
  (`mind/INTENT.md` lines 1-13). *persona* is the engine-manager /
  permissioned system daemon — supervises component daemons, owns upgrade
  orchestration and FD-handoff, multi-engine supervision
  (`persona/INTENT.md`). Note the two distinct authority shapes: persona's
  is infrastructure-shaped (spawn/restart/observe); mind's (and spirit's) is
  the cognitive/control authority chain.

- **harness runs agents.**
  Models interactive AI harnesses (Codex/Claude/Pi/Fixture) as addressable
  runtime objects: lifecycle, transcript observations, delivery adaptation
  (`harness/INTENT.md` lines 1-8). One `harness-daemon` may own multiple
  harness instances internally as actors/adapters. It does NOT own routing
  policy, focus observation, or PTY byte transport.

- **message is the front-door ingress** (the engine-owner edge that feeds
  the chain): stamp SO_PEERCRED provenance and forward to router; stateless,
  no ledger (`message/INTENT.md` lines 1-12, 49-61).

### The authority chain (control-plane shape)

From `component-triad.md` §"Authority chain" (lines 651-707) and the INTENTs:
**mind** (authority root) owns **orchestrate**; **orchestrate** owns
**router** and **harness**. Correctness is maintained top-down via Mutate
chains — issuer holds *possibly-mutated* state until ack, then advances;
partial failure is *commit-first-success-and-record-divergence*, not
two-phase rollback. Observation flows UP via push-Subscribe; authority flows
DOWN via Mutate.

### The spirit-vcs propagation chain (data-plane shape)

The cleanest worked relationship across the constellation
(`router/INTENT.md` lines 78-99, `mirror/ARCHITECTURE.md`):

```
spirit (accepts log object)
  → criome (authenticate the content-addressed object/event — sign/verify)
  → router (carry authenticated propagation, tailnet TCP, router-to-router)
  → remote criome (verify) + remote mirror (act on event)
  → mirror (fetch/restore announced object state; validate blake3 chain; fsync-then-ack)
```

One cryptographic basis spans the whole VCS/backup system: blake3 for
content addressing, criome BLS for signing/attesting (Spirit `x0ja`, quoted
in `mirror/INTENT.md` lines 30-34). This is the concrete realization of the
four-way separation: spirit produces, criome authenticates, router
transports, mirror version-controls/restores.

## 5. Two-tier authority surface (every triad)

Each stateful component exposes two typed authority surfaces on two
permission-separated sockets (`component-triad.md` Invariant 4, lines 331-362):

- **`signal-<component>`** — ordinary peer surface; any authenticated peer.
- **`meta-signal-<component>`** — meta policy authority; only the owner above
  it in the owner graph.

Contracts split by **who-can-call, not what-state-they-touch**: a
peer-callable Mutate (releasing one's own claim) lives in the ordinary
contract; an owner-only Mutate (mind ordering orchestrate to spawn) lives in
the meta contract. Both surfaces persist into ONE sema-engine DB per
component, split into **policy state** (changed only via meta-signal Mutate,
bootstrapped by authenticated binary meta-signal config) and **working
state** (produced by operation, starts empty) — Invariant 5, lines 364-416.

## 6. Daemon discipline (universal, from triad skill + INTENTs)

Confirmed live across spirit/criome/router/message/mind/harness INTENTs:
- One argument, no flags. CLI takes one NOTA request; daemon takes exactly
  one binary rkyv `<Component>DaemonConfiguration` and rejects inline NOTA
  and `.nota` paths (`component-triad.md` §"The one argument rule").
- A `<component>-write-configuration` bootstrap helper turns one NOTA
  request into the binary startup file (router/message/spirit INTENTs) — a
  text-edge helper, not a daemon surface.
- The wire between components is binary `signal-frame` only; NOTA lives at
  named text projection edges (CLI argv/stdout, authored deploy files),
  never inter-component (Invariant 2).
- `sema-engine` is the EXCLUSIVE database interface; no component makes
  direct redb calls (Spirit `fosp`, quoted in `mind/INTENT.md` lines 22-24).
- Virgin daemon starts `Unconfigured`, waits for authenticated binary
  meta-signal config; on restart self-resumes from persisted SEMA state.
