# 110 — Cluster-trust runtime within Criome

*Designer report. Resolves `primary-rab` (cluster-registry component
identity). Records the user's correction (2026-05-10): the cluster-trust
runtime is not persona-shaped — it lives within **Criome**, the universal
validator/coordinator daemon at the center of the sema-ecosystem.
ClaviFaber's per-host publications feed into Criome; Criome distributes
host-identity/cluster-trust to subscribers as a new responsibility
alongside its existing record-validation role.*

*Supersedes: an earlier draft of this report numbered the cluster-trust
runtime as `persona-trust`, a new persona-* component. That framing was
wrong on the ecosystem boundary — auth/security/identity is Criome's
domain, not Persona's. The persona/ARCHITECTURE.md additions associated
with that draft were rolled back in commit `c385ee63`.*

---

## 0 · TL;DR

| Question | Answer |
|---|---|
| Where does the cluster-trust runtime live? | **Within Criome** — the existing `Criome` repo at `/git/github.com/LiGoldragon/criome`. Same daemon that already owns sema-ecosystem record validation; cluster-trust extends its scope. |
| Who consumes ClaviFaber's per-host `PublicKeyPublication` records? | Criome (one canonical consumer; the central cluster node runs it). |
| Who pushes trust observations to host subscribers? | Criome (via a new responsibility added to its existing daemon). |
| Does the existing `criome/ARCHITECTURE.md` need rewriting? | The document stays correct as-is for sema-ecosystem record validation. Cluster-trust is a follow-up addition to its scope; either Criome's ARCH widens incrementally or a sibling section names the auth/security plane. That is system-specialist's call when implementation lands. |

---

## 1 · The mistake the earlier draft made

The earlier draft of this report (commit `81125fa3`, content now retired)
proposed a *new* persona-* component named `persona-trust` to own the
cluster-trust runtime. The reasoning chain was:

> *"Persona is the durable agent (workspace's answer to OpenClaw and
> Gas City). Cluster-trust is durable-agent work. Therefore cluster-trust
> is persona-shaped."*

That chain looked plausible but was wrong on the ecosystem boundary.
Persona owns **workspace-scope durable-agent runtime** (mind, router,
harness, work graph). It does *not* own machine-scope or cluster-scope
identity infrastructure. Auth/security/identity belongs to **Criome** —
the workspace's universal validator/coordinator daemon, which already
signs capability tokens and validates incoming signal requests
(`/git/github.com/LiGoldragon/criome/ARCHITECTURE.md` §0 TL;DR).

The contradiction surfaced when I read Criome's existing ARCH and saw
its self-description as *"the daemon at the center of the sema-ecosystem
… owns the records database … validates incoming signal requests …
forwards effect-bearing verbs … signs capability tokens."* I read this
as orthogonal to auth/security. The user clarified: it's not orthogonal
— Criome is bigger than just record validation. **Criome is the
universal validator/coordinator daemon.** Auth/security is one of its
roles already (capability-token signing); cluster-trust is the next
concrete addition.

---

## 2 · Criome's scope, broader than I read it

The user named Criome's eventual scope explicitly: *"eventually
everything will go through Criome. We're going to program through the
Criome, the Criome will validate everything, it'll replace Git, it'll
replace our code editor, it'll replace SSH, it'll replace the web
server."*

That's a vision, not the current implementation. Today's Criome owns:

- the typed records database (Graph/Node/Edge/Derivation/CompiledBinary)
- signal request validation
- effect-bearing verb dispatch
- capability-token signing

The vision adds — over time — programming surfaces, version-control
history, network identity, web request handling, and other concerns
that today live in Git, code editors, SSH, web servers. Criome IS the
universal computing paradigm component (per its `README.md` heading
*"A Universal Computing Paradigm"*).

Cluster-trust runtime fits naturally inside that scope:

- It validates incoming submissions from per-host ClaviFaber convergence
  runs (validation is Criome's existing strength).
- It persists host-identity material into a typed records table
  (records-database is Criome's existing strength).
- It signs trust observations distributed to subscribers (capability
  signing is Criome's existing strength).
- It pushes typed events to subscribers (signal-based push is the
  natural extension of validate-and-persist).

So adding cluster-trust to Criome doesn't require a new daemon, a new
repo, or a new architectural pattern — it extends the existing one.

---

## 3 · CriomOS is named after Criome

The OS-distribution naming reflects the ecosystem's center:

- **Criome** — the universal validator/coordinator daemon.
- **CriomOS** — the NixOS distribution that's *intended to rely on*
  Criome for its core functions (auth, identity, validation, eventually
  more). Currently in a "pre-duct-tape" stage — CriomOS uses Criome's
  name as an intent-holder while the integration is still ad-hoc.

Two things follow:

- ClaviFaber's per-host runs (`primary-7a7`) are CriomOS systemd
  services. Their outputs feed Criome on the cluster's central node.
- Persona consumers may eventually route through Criome too (signing,
  validation), but for now Persona components have their own
  daemons (mind, router, etc.). The vision converges; the
  implementation is incremental.

---

## 4 · ClaviFaber → Criome contract

The `signal-clavifaber` contract (designer/111) names the wire shape.
Two relations:

| Relation | Endpoints | Direction | Cardinality |
|---|---|---|---|
| Publication push | per-host ClaviFaber → Criome | host → cluster | many → one; one-shot per host convergence |
| Trust subscription | Criome → host subscriber | cluster → host | one → many; long-lived stream |

Both relations terminate at Criome on the cluster side. ClaviFaber's
existing `PublicKeyPublication` shape
(`/git/github.com/LiGoldragon/clavifaber/src/publication.rs:7-13`) is
the input record; Criome's distributed `TrustObservation` is the
output record (carried in a `TrustUpdate` event per designer/111 §3).

The transport carve-out in designer/111 §5 (file+inotify as fallback to
direct socket push) still applies; it's a system-specialist deployment
call independent of which daemon owns the cluster-side runtime.

---

## 5 · What this report does and doesn't decide

**Decides**:

- Cluster-trust runtime lives in Criome (the existing repo), not in a
  new persona-* component.
- ClaviFaber's per-host publications feed Criome.
- Criome's scope expands to include cluster-host-identity state
  alongside its existing sema-ecosystem record validation.
- The retired persona-trust framing is supplanted; persona/ARCH is
  rolled back accordingly (commit `c385ee63`).

**Does not decide** (deferred to system-specialist or later beads):

- Whether Criome's `ARCHITECTURE.md` widens its existing scope in place
  or adds a sibling §"Auth/security/identity plane" — implementation
  detail; either works.
- Concrete actor topology inside Criome for the cluster-trust plane:
  `ClusterRegistryActor` + `TrustDistributionActor` per `primary-e3c`
  is the system-specialist's design call. They were named in
  `primary-3m0` and stay valid as actor nouns.
- Concrete redb table layout for cluster-trust state — Criome's
  existing sema layer absorbs it via a new typed table; system-specialist
  picks the table key shape when implementing.
- The persona-vs-Criome convergence path long-term — whether Persona's
  daemons eventually route through Criome for validation is a separate
  architectural question.

---

## 6 · Follow-up beads

`primary-rab` closes with this report. Updates to other beads:

- `primary-e3c` (the cluster-trust implementation bead): currently
  scoped to `clavifaber` repo + `system-specialist` role. The work
  actually lands in `Criome` — needs label update from
  `repo:clavifaber` to `repo:criome`. The two actor nouns
  (`ClusterRegistryActor`, `TrustDistributionActor`) are still correct.
  System-specialist's lane.
- The earlier draft's two follow-up beads (persona-trust repo creation,
  persona/ARCH cluster-trust integration tests) are dropped — they
  presumed the wrong ecosystem.
- A possible new bead (file later if useful): *"Criome ARCH update —
  add cluster-trust plane alongside sema-ecosystem record validation."*
  System-specialist or operator lane, depending on who picks up the
  Criome implementation surface. Not filing today; can wait until
  someone is actively touching Criome's source.

---

## See also

- `~/primary/reports/designer/111-signal-clavifaber-contract-shape.md`
  — sibling report; defines the ClaviFaber↔Criome wire contract. Refers
  to `Criome` as the cluster-side consumer.
- `~/primary/reports/1-gas-city-fiasco.md` — the failure-mode framing
  that grounds Persona's positioning (still useful as a reference for
  durable-agent design, separate from Criome's ecosystem boundary).
- `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md` — Criome's
  current self-description as the sema-ecosystem validator daemon. The
  cluster-trust work extends its scope; it doesn't replace this
  framing.
- `/git/github.com/LiGoldragon/criome/README.md` — *"The Criome / A
  Universal Computing Paradigm"*; the upstream vision statement.
- `/git/github.com/LiGoldragon/clavifaber/ARCHITECTURE.md` — ClaviFaber's
  current scope (per-host identity material producer). Its disclaimer
  about the cluster-database writer still stands; the writer is Criome,
  per this report.
- `/git/github.com/LiGoldragon/clavifaber/src/publication.rs:7-13` —
  the `PublicKeyPublication` shape that crosses the per-host →
  Criome boundary.
- `~/primary/protocols/active-repositories.md` — the active repo map;
  Criome's role description there is currently *"Sema ecosystem
  consumer and architecture reference"* and benefits from being
  widened to *"Universal validator/coordinator daemon; sema-ecosystem
  records + cluster-host trust"* once this lands. Not done in this
  report (active-repositories.md is a small attention map, not the
  primary architecture surface).
