# 119 — Handover: criome auth, CriomOS comms architecture, spirit intent

*A fully detailed handover of a long system-designer session spanning the
criome↔spirit authentication pilot, the CriomOS cross-node communication
architecture, spirit intent capture + maintenance, and a production outage. For
the operator (main integration), the cloud-designer (networking), and any agent
picking this up. Branch heads and record ids are current as of writing.*

## 1 — criome authentication (the headline deliverable)

A complete, tested working implementation across two repos. The operator bases
main on this.

**signal-criome** — branch `criome-admission-gate`, **pushed to origin** (commit
`783cc2fa`). Three contract additions for the admission gate:
`IdentityRegistration.admission (Optional SignatureEnvelope)`,
`CriomeDaemonConfiguration.cluster_root (Optional BlsPublicKey)` (+ a
`with_cluster_root` builder), `RejectionReason::UnauthorizedRegistration`.
Artifacts regenerated (`SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS=1`); builds clean.

**criome** — branch `criome-auth-pilot`, **local** (worktree
`~/wt/github.com/LiGoldragon/criome/criome-auth-pilot`), 6 commits on main
`2a02cf4d`, head `47b1dd0d`, repinned to the signal-criome branch:
1. real BLS12-381 master key + `verify_bls` (placeholder retired)
2. real BLS wired through the daemon actors (self-owned signing: criome signs as
   `Host("criome")`, caller in audit context; real `VerifyAttestation`)
3. the seven SO audit P1/P2/P3 fixes
4. the cluster-root admission gate core (`src/admission.rs`)
5. the full admission wire (gate threaded `config → CriomeDaemon → RootArguments
   → IdentityRegistry`; `register()` rejects `UnauthorizedRegistration`)
6. the admission scheme check (SO 227 P2)

**State: 33 tests green; `clippy -D warnings`, `cargo fmt --check`, and
`nix flake check` all pass** (the operator ran `nix flake check` in audit 227).

**The model:** criome verifies; Persona decides. criome stays auth-only (no network
transport — its cross-host-transport slot is superseded; router owns the wire). It
signs an out-of-band attestation binding the SO_PEERCRED caller to the exact
per-operation digest; the preimage covers the full attestation statement (content,
signer, audit context, validity interval, scheme). A key is admitted to the registry
only with a valid cluster-root signature over its `RegistrationStatement` (the trust
root). Key custody: generate-on-first-run, persist `0600` (transitional, `psc6`).

**Audits — all addressed:** `225` (7 P1/P2/P3 fixes), `226` (test-cluster status,
P1-before-meta-config sequencing, mirror=sema-VC daemon, substrate-before-ownership),
`227` (the admission scheme-check P2; confirmed the P1 fixes + nix flake check). `227`
audited the pre-wire commit `d09be336`, so its "registry still self-asserted" caveat
is superseded by commit 5 (the full wire).

**What remains for production (bead `kr40`):**
- **Production key custody:** `mlock`/`zeroize`/passphrase; verify the key-file
  owner and use an `openat`/no-follow handle to close the check-then-open race
  (`227` residual); eventually the authenticated `meta-signal-criome` key config,
  superseding `psc6`.
- **The cluster-root provisioning ceremony:** deploy-time, the cluster-root signs
  each node's criome master key → the criome self-admission. This makes the mesh
  trust non-circular and is the first-cross-system-trust edge.
- **Operator main integration:** merge the `signal-criome` branch to main, repin
  criome to main, `nix flake check`. Integration order is spelled out in SO `227`
  §Recommendation and SD report `118`.

## 2 — CriomOS cross-node communication architecture

Decided in a design dialogue; grounded against the repos in report `116`; the
psyche's decisions are in Spirit (below). **Shape:** CriomOS is a mesh of per-agent
smart microVM sandboxes; **one router per system** is the communication fabric
(cross-sandbox locally + cross-network router↔router); **criome signs, router
transports, mirror version-controls/moves objects, the tailnet encrypts, BLS
authenticates.** Intra-host sandbox↔router is **tap/L3** (vsock deferred — it loses
SO_PEERCRED). The message/router separation (`alom`) is kept; the per-system network
fabric realizes `i99x` and narrows `l3k4`'s harness-ack delivery clause to the local
path.

**Load-bearing gaps (nothing cross-node works yet):**
- **No component has a networked, encrypted transport.** router/message/mirror/criome
  all speak local Unix-socket `signal-frame`. The inter-host pattern is proven only in
  mirror's green tailnet-TCP e2e; the router has zero network surface in code.
- **The spirit→mirror shipper does not exist** (no mirror dep in spirit) — the e2e's
  first leg is unbuilt from scratch.
- criome registry admission gate now exists (§1); the cross-router trust still needs
  the provisioning ceremony.

**Staged plan (report 116/118):** criome security core (done on the branch) →
spirit→mirror shipper + authenticated ingest → router network transport (lift
`triad_runtime::TcpListenerDaemon`, add signal-router network roots + replay window +
`domain-criome` discovery) → intra-host tap/L3 + a cross-VM-boundary origin proof →
two-node e2e on the **live ouranos↔prometheus tailnet** (or a `mkVmTest`). The
cloud-designer already has live-microVM e2e capability (reports 45–51).

## 3 — Intent ledger (Spirit records this session)

**Live:**
- `w2g3` (operator, Decision) — spirit is the criome-auth pilot consumer.
- `2st7` (Decision) — the settled pilot mechanism (caller / after-the-fact / per-op
  digest).
- `wckt` (Decision, Medium) — the CriomOS comms architecture.
- `ermr` (Decision, Medium) — cross-system trust root: cluster-root signs member keys.
- `5osd` (Correction of `0yx5`, Medium) — per-system mirror + authenticated ingest.
- `psc6` (Decision) — criome key custody (generate-on-first-run, 0600, transitional).
- `15df` (Correction High) — intent's single source becomes Spirit; ARCHITECTURE.md
  is the per-repo doc; INTENT.md migrates off gradually. Supersedes `cdd3`.
- pre-existing pilrs the work rests on: `a4i6`, `9v7h`, `q1cw`, `i9qv`, `jtmt`, `3fm6`.

**Zeroed (recoverable):** `kxdz` (my duplicate of `w2g3`+`a4i6`), `cdd3` (superseded
by `15df`). **Removed:** `6x6h` (a clarification I wrongly stacked instead of editing).

**Discipline notes for the next agent:** a Clarification is an *edit* of the record
it refines (`Clarify`/`Supersede`/`Retire`), not a new stacked record. An
AskUserQuestion pick of a "(Recommended)" option is a *lean* — it clears `Medium`,
not `High`; hedged testimony ("probably", "can be") likewise caps certainty. The
guardian correctly enforced both this session.

## 4 — Intent substrate: Spirit-as-source, spirit.nota, spiritbackup.nota

`15df` decided Spirit is the single intent source. **Open mechanism (bead `ebev`,
not yet settled intent):** the psyche's `spirit.nota` proposal — a per-repo,
versioned/timestamped **filtered NOTA printout** of the repo's intent (scoped by
referent, public-only), generated by a spirit client; replaces hand-authored
INTENT.md; ARCHITECTURE.md stays hand-maintained. The contract-doc rewrite (AGENTS.md
+ intent skills) is staged in `ebev` — gradual, not done yet. Primacy is unchanged:
intent stays first-read; only the substrate moves.

`spiritbackup.nota` (repo root) is a **new, working offline-capture mechanism**: when
spirit is down, log the whole intent request there; replay through the guardian on
recovery. Proven end-to-end this session (3 decisions queued during the outage, then
replayed → `wckt`/`ermr`/`5osd`).

## 5 — Production incidents

- **`4bw6` (RESOLVED):** spirit-daemon outage — a 13:06 deploy's `spirit-migrate-store`
  rejected the live schema 10 (`unrecognized spirit store schema version: 10`),
  restart-looped to `start-limit-hit`. Data intact; operator restored it (0.13.0).
- **`9cop` (OPEN):** the `Clarify`/`Supersede`/`Retire` edit path errors on the
  deployed daemon (`schema version mismatch — v9 vs v10`). **Intent can be Recorded,
  Removed, and re-graded, but NOT edited/superseded in production** until the v9
  lineage store is migrated. Same v9/v10 root as `4bw6`. This blocked the in-place
  edit of `15df` this session.

## 6 — Open beads

- `kr40` (P1) — criome crypto: admission-signing **closed** on the branch; key
  custody + provisioning ceremony remain; operator main integration.
- `5zur` (P2) — the spirit-side criome-auth pilot (CriomeAuthority client, thread
  `ConnectionContext` past `daemon.rs:142`, `EntryDigest` accessor, out-of-band
  attestation ledger). Unblocked on criome's side.
- `ebev` (P2) — intent-substrate rollout + the `spirit.nota` mechanism.
- `9cop` (P1) — the Clarify/edit-path v9→v10 store migration (operator).
- `4bw6` (P1, resolved) — the spirit outage.

## 7 — Open psyche decisions / next steps

1. **criome:** continue (production key custody / provisioning ceremony) **or** hand
   to the operator for main integration. The crypto + gate are done and tested.
2. **`spirit.nota`:** adopt as the substrate mechanism (then I capture + spec it) —
   proposed, not yet settled.
3. **The `ebev` contract rewrite** (AGENTS.md + intent skills to make Spirit
   canonical) — do now or stage with the gradual migration.
4. **VC-tower sequencing** (from report 109, never decided): ship the sema-engine
   0.6.x self-heal tower next / defer / re-scope against deployed 0.4.0+schema-10.
5. **Networking build sequence** (report 116 staged plan) — when to start the
   spirit→mirror shipper and the router network transport.

## 8 — Report + branch index

- SD reports this session: `109` (open points), `112/` (criome concept), `113`
  (session summary), `114` (BLS impl), `115` (networking audit response), `116/`
  (comms architecture), `117` (where-we-are, visual), `118` (auth reference), `119`
  (this handover).
- SO audits: `223` (criome/spirit position), `225` (BLS impl), `226` (networking
  response), `227` (auth reference).
- cloud-designer: `45–51` (live microVM e2e + the general VM-testing interface).
- Branches: `signal-criome/criome-admission-gate` (origin), `criome/criome-auth-pilot`
  (local, head `47b1dd0d`).
- Live infra: two tailnet nodes ouranos↔prometheus (~16ms, ygg-reachable).
