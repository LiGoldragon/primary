# 221 — Lojix + Arca + horizon-leaner-shape state (2026-05-18)

*Topic compendium for the biggest and most-active arc in the workspace:
the lean rewrite of the deploy stack. Part of the 2026-05-18 workspace
state-of-art series. Master index lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

**Production stack on `main` (Stack A)** still runs the old monolithic
`lojix-cli` across every cluster node. Six repos pinned: `horizon-rs`,
`lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, `goldragon` —
all canonical `/git/...` checkouts. `CriomOS/flake.lock` pins
`lojix-cli` at `42529ebd2114`. No daemon. **All production fixes go here.**

**Lean rewrite on `horizon-leaner-shape` (Stack B)** has reached an
end-to-end smoke milestone but is **not deployed to any node**.
SS/134 records: `zeus` FullOS built end-to-end through builder
`prometheus`; `lojix` recorded `Generation generation_12 goldragon
zeus FullOs ... Built`. Six existing repos on `horizon-leaner-shape`
plus two new repos: `lojix` (daemon + thin CLI, single crate, two
binaries) and `criomos-horizon-config` (pan-horizon constants on
`main`). `signal-lojix` is also on `horizon-leaner-shape` and is no
longer a skeleton — its worktree has a real `Cargo.toml`/`src/lib.rs`
with `DeploymentRequestDigest`, channel macro, and
`LojixDaemonConfiguration` carrying `horizon_configuration_source`.

**Cutover is not done.** Per `protocols/active-repositories.md`
§"Two deploy stacks coexist", cutover must be coordinated across all
repos after feature parity. The biggest landed piece since smoke is
the **CriomeAuthorizationActor gate** (OA/151): build effects are now
blocked until a typed authorization grant lands. Production
`real-build-smoke` is parked because the daemon path fails closed
(intentional) until the real `signal-criome` socket client lands.

**Notable doc drift.** The canonical `/git/.../signal-lojix/ARCHITECTURE.md`
on `main` claims "Skeleton. Documentation only. No Cargo.toml, no src/,
no flake.nix." — this is **stale**; the worktree on
`horizon-leaner-shape` has all three. Either update the status note or
accept the main-branch ARCH as a frozen snapshot until cutover.

---

## 2 · Load-bearing reports

### System-specialist lane

| Path | Carries |
|---|---|
| `reports/system-specialist/141-lojix-criome-arca-implementation-synthesis-2026-05-17.md` | **Canonical synthesis.** Four-daemon shape, request lifecycle, `DeploymentArtifactSet` enumeration, best-implementation sequence. |
| `reports/system-specialist/142-criome-public-socket-and-deploy-approval-clarification-2026-05-17.md` | Corrections to SS/141 from user answers: regular `signal-criome` is public+unencrypted; signature is in Criome; "signed object" reframed as Criome permission artifact. |
| `reports/system-specialist/140-lojix-criome-mediated-authorization-decision-2026-05-17.md` | Original user authorization decision; SS/141 supersedes for synthesis, but this is the decision source. |
| `reports/system-specialist/139-arca-daemon-content-addressed-store-architecture-2026-05-17.md` | Standalone Arca architecture: full BLAKE3 identity; daemon-allocated stable locators; base32 prefix floor of 10-12 chars; `/arca` system root; existing-repo gap analysis (todo!() bodies, `~/.arca` → `/arca`). |
| `reports/system-specialist/138-lojix-arca-distributed-deploy-architecture-2026-05-17.md` | Three planes (control / artifact / realized-output); `NixDaemonConfigurationActor` shape. |
| `reports/system-specialist/137-lojix-self-deploy-cache-coordination-architecture-2026-05-17.md` | Four-role daemon mesh; local-execution-per-concern. |
| `reports/system-specialist/136-horizon-rs-lojix-state-audit-2026-05-17.md` | `lojix/src/deploy.rs` 2,083 lines (45% of repo); witnessed configuration-boundary tests; split needed. |
| `reports/system-specialist/135-lean-horizon-follow-up-after-user-decisions-2026-05-17.md`, `/134-lean-horizon-pan-config-and-lojix-build-2026-05-17.md` | `criomos-horizon-config`/transitional-IPv4-LAN landing + smoke evidence. |

### System-assistant lane

| Path | Carries |
|---|---|
| `reports/system-assistant/23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md` | Current open-question catalog after D/214 + OA/149/150. |
| `reports/system-assistant/22-audit-criome-routed-authorization-arc-2026-05-17.md` | Cross-lane critique; explicitly retires SS/21's framings. |

### Designer lane

| Path | Carries |
|---|---|
| `reports/designer/207-horizon-boundary-audit-and-lean-down-plan-2026-05-17.md` | **Canonical four-bucket sorter** + 26% schema reduction plan. |
| `reports/designer/208-pan-horizon-configuration-brainstorm-2026-05-17.md` | Pan-horizon NOTA shape rationale. |

### Designer-assistant lane

| Path | Carries |
|---|---|
| `reports/designer-assistant/113-lojix-daemon-boundary-and-open-context-2026-05-17.md` | **Canonical thin-CLI-daemon-boundary statement**; architecture edits log (CLI/daemon boundary loud in four ARCH files). |
| `reports/designer-assistant/111-horizon-lojix-context-maintenance-2026-05-17.md` | Post-context-maintenance condensation; supersedes five intermediate reports. |
| `reports/designer-assistant/112-horizon-lojix-criomos-direction-research-2026-05-17.md` | Three-projection-inputs reconstruction. |

### Operator-assistant lane

| Path | Carries |
|---|---|
| `reports/operator-assistant/151-lojix-criome-authorization-gate-2026-05-17.md` | **Only landed lojix-side code report this date.** `signal-lojix df49dae1` (DeploymentRequestDigest) and `lojix 6a799dac` (CriomeAuthorization actor, deployment gate). Both bookmarks pushed. |

---

## 3 · Stale / superseded / partially-stale reports

| Path | Status | Reason |
|---|---|---|
| `reports/system-assistant/16-two-deploy-stacks-coexist-survey-and-doc-proposal-2026-05-17.md` | **Retire** | Landed verbatim in `protocols/active-repositories.md` §"Two deploy stacks coexist"; surviving as a draft of doc that already exists. |
| `reports/system-assistant/17-review-of-sys-136-horizon-rs-lojix-audit-2026-05-17.md` | **Retire** | Findings folded into SS/136 narrative; safe with a follow-up note about `primary-766g` cross-link. |
| `reports/system-assistant/18-daemon-mesh-deploy-architecture-exploration-2026-05-17.md` | **Partial retire** | G1-G19 gap audit; many gaps closed (G1/G4/G7/G11/G15/G19). Useful as checklist witness; residuals live in SS/23. Retire after cross-walking residuals. |
| `reports/system-assistant/19-deploy-mesh-with-arca-substrate-2026-05-17.md` | **Retire** | Subsumed by SS/138 and SS/141; SYS/22 explicitly identifies it as subsumed. |
| `reports/system-assistant/20-arca-content-addressed-substrate-design-2026-05-17.md` | **Partial retire** | Five-axes framing useful as historical context for the user's verbal debate; SS/139 has the canonical decisions (base32 production floor, not 16-hex prefix). |
| `reports/system-assistant/21-criome-routed-authorization-and-thin-cli-shape-2026-05-17.md` | **Retire** | SYS/22 explicitly retires the "criome holds permission data → ACL" framing and the single-criome-per-node framing. Three-mesh diagram value preserved in SS/141. |

---

## 4 · Architecture key decisions (consolidated)

From SS/141 + SS/142 + D/207/208 + DA/113:

1. **Four daemons per node**: `criome-daemon` (authorization, signatures, quorum, identity), `lojix-daemon` (deploy job state, planning, actor orchestration), `arca-daemon` (content-addressed artifacts), `nix-daemon` (Nix store / builds / closure import). `lojix-daemon` coordinates the other three but does not own their state.
2. **Three meshes per cluster** (refined post-SS/22): `signal-criome` (per-(host, user) — not per-node), `signal-lojix` (deploy coordination), `signal-arca` (content-addressed substrate).
3. **CLI/daemon boundary is hard** (DA/113): CLI does not read `horizon.nota`, does not read `datom.nota`, does not call `ClusterProposal::project`, does not invoke Nix, does not stage flakes, does not create GC roots, does not write `sema-engine`. CLI only decodes NOTA → Signal request and renders Signal reply → NOTA.
4. **Three projection inputs**: `HorizonProposal` (operator-wide) + `ClusterProposal` (per-cluster) + `Viewpoint` (request-time `(cluster, node)` lens). Code implements; some ARCH prose still drifts to one-input framing.
5. **Authorization model** (corrected by SS/142): regular `signal-criome` socket is public + unencrypted; security comes from Criome signatures + receiving daemon policy, not from socket access. Source-Criome signs permission; target-Criome authorizes effects in its environment. `lojix` does not own permission; `lojix` does not sign.
6. **Owner approval is an Assert**: owner emits `AssertSigningDecision` as durable fact; `criome-daemon` then mutates pending → signed/denied.
7. **`/arca` system root**, not `~/.arca` — full BLAKE3 identity, daemon-allocated stable locators with base32 prefix floor of 10-12 chars (not 3 hex), exposed locators never renamed.
8. **NixDaemonConfigurationActor pattern**: CriomOS installs `!include /var/lib/lojix/nix/nix.conf` in `/etc/nix/nix.conf`; lojix owns only the include file + restart lock + last-applied-config-hash + health observations + lease/expiry cleanup.
9. **Four-bucket sorter** (D/207): cluster fact / horizon constant / horizon derivation / CriomOS-side. The doc-comment smell "*Replaces the literals scattered across CriomOS*" is almost always wrong — move the projection to horizon, leave literals as CriomOS defaults.
10. **Transitional IPv4 LAN**: keep one explicit constant in `HorizonProposal`; do not build a multi-cluster IPv4 allocator. IPv6-first is the long-term direction.

---

## 5 · Four-daemon shape (per node)

| Daemon | Owns |
|---|---|
| `criome-daemon` | authorization, signatures, quorum, identity, owner/peer routing. One per (host, user) per SS/22 refinement. |
| `lojix-daemon` | deploy job state, planning, actor orchestration, observations |
| `arca-daemon` | content-addressed artifact storage and replication |
| `nix-daemon` | Nix store, builds, closure import, substituter trust enforcement |

The cluster control plane is three meshes: signal-criome, signal-lojix, signal-arca. The operator's laptop runs only the CLIs (plus optionally criome if it holds a signing key; plus optionally arca if it stages artifacts).

---

## 6 · DeploymentArtifactSet shape

Per SS/141 §"Artifact set" (refined by SS/142 with `criome_permission_grant_digest` as the preferred name for the authorization field):

```
DeploymentArtifactSet {
  signal_lojix_request_digest,
  criome_authorization_digest,       // or criome_permission_grant_digest
  horizon_proposal_digest,
  cluster_proposal_digest,
  viewpoint_digest,
  projected_horizon_digest,
  generated_nix_inputs_digest,
  topology_snapshot_digest,
  deployment_plan_digest,
}
```

Nine digests. The plan should name the authorized request digest;
coordinator may sign plan for integrity, but permission comes from the
Criome authorization object.

---

## 7 · Open questions (prioritized)

### Tier 1 — block multi-node progress

- **Q1** (SS/23 Q1, SS/22 Q4) — Unattended-system-daemon bootstrap. Lean: v1 unencrypted master key + filesystem permissions; v2 TPM-sealed.
- **Q2** (SS/23 Q2, SS/22 Q1) — Cross-user-same-host criome routing. Lean: persistent system-level routing socket owned by privileged-but-isolated routing daemon.
- **Q3** (SS/23 Q3, SS/22 Q2) — System criome's role. Lean: full participant under operator-set policy.

### Tier 2 — wire contract decisions

- **Q4** (SS/23 Q4, SS/22 Q5, SS/141 Q3) — `SignedObject` canonical bytes. Lean: all security-relevant scope inside the signed digest.
- **Q5** (SS/23 Q5, SS/22 Q10) — Verifier policy vs originator policy.
- **Q6** (SS/23 Q6) — `owner-signal-criome` contract sketch + ECDH cipher choice.
- **Q7** (SS/142 Q2) — Noun for the signed permission object (`CriomePermissionGrant` vs `AuthorizationGrant`).
- **Q8** (SS/142 Q3) — Target environment definition.
- **Q9** (SS/142 Q5) — First owner approval action.

### Tier 3 — operability

- **Q10** (SS/141 Q4, SS/142) — Scope of one authorization for all local effects. Lean: authorize plan once with explicit scope.
- **Q11** (SS/141 Q5, SS/22 Q12) — First owner approval surface. Lean: simple self-signing first; then long-running owner client.
- **Q12** (SS/141 Q7) — ClaviFaber separate key classes. Lean: keep separate.
- **Q13** (SS/141 Q8) — `/arca` migration timing. Lean: now, as system default.

### Tier 4 — surfaced from recent reads

- **Q14** (SS/23 Q10) — Criome receives content + digest, not just digest.
- **Q15** (DA/113 Open Concept 3) — `owned_cluster` vs operator-wide daemon. Lean: one daemon per cluster in v1.
- **Q16** (DA/113 Open Concept 4) — AI model materialization in system closure vs separate unit. Lean: system closure for v1.
- **Q17** (DA/111 + DA/112) — `NodeSpecies` + `NodeRole` + `NodeOverride` schema (replace `LargeAiRouter` with primary species + additive roles).

---

## 8 · Implementation state

### horizon-leaner-shape branch repos

| Repo | Tip (worktree) | Status |
|---|---|---|
| `horizon-rs` | `45056dc4`+ | Three-input projection implemented |
| `lojix` | includes `6a799dac` (CriomeAuthorization) | 4,622+ lines Rust; `src/deploy.rs` 2,083 lines (split needed) |
| `signal-lojix` | `df49dae1`+ | Has Cargo.toml, src/lib.rs, tests. **/git ARCH "skeleton" note is stale** |
| `goldragon` | on horizon-leaner-shape | datom shed 482 → 294 lines |
| `CriomOS` | `5027d9ac`+ | Consumes lean projection |
| `CriomOS-home` | `e1206533` | |
| `CriomOS-lib` | `21de5ebc` | Owns AI/NordVPN catalogs |

### New repos on `main`

- `criomos-horizon-config/main` @ `08adcf11bd5e` — `horizon.nota` with transitional IPv4 LAN.
- `lojix/main` — only AGENTS.md + ARCH skeleton on canonical /git; implementation on `horizon-leaner-shape`.

### Coded vs stubbed vs not started

**Coded**: thin CLI, daemon socket, daemon configuration with pan-horizon path, Horizon projection, build job actor, deployment ledger, GC roots, generation pinning, fake-tool build pipeline tests, configuration-boundary tests (5 tests), real-build-smoke runner (parked), three-input projection, `DeploymentRequestDigest`, `CriomeAuthorization` actor with `GrantForTests` / `Unavailable` policies.

**Stubbed**: `CacheRetentionRequest` rejects with empty observations (wire-only); `peer_daemons` accepted but no routing plane; `operator_identity` stored but no verification; activation/current-generation switching; declarative supervision/restart policy; secrets are convention-based scan (not typed binding); remote generated inputs use fixed builder path with no first-class cleanup.

**Not started**: real Criome socket client (CriomeAuthorization fails closed in production); Arca daemon (`/git/.../arca` is skeleton with `todo!()`); `NixDaemonConfigurationActor`; daemon-to-daemon coordination; `AwaitingAuthorization` durable state; `deploy.rs` split into nouns.

**Cutover status: NOT DONE.** Production still on Stack A. Per `protocols/active-repositories.md`, do not fold one stack into the other piecemeal — schemas have diverged.

---

## 9 · Best implementation sequence (SS/141 + SS/22 §9)

1. Canonical request digest helper. **LANDED** (OA/151, `signal-lojix df49dae1`).
2. Fake Criome authorization in `lojix` tests; gate Nix effects. **LANDED** (OA/151, `lojix 6a799dac`).
3. Pending authorization state (`AwaitingAuthorization` + observation subscription). Not started.
4. Artifact set skeleton (Arca artifact-set types + fake Arca test adapter). Not started.
5. Nix configuration actor skeleton (mutable include + restart). Not started.
6. Split `deploy.rs` toward actor nouns. Cross-links to `primary-766g`.
7. Distributed fake-daemon integration. Not started.
8. Real Arca daemon path. Not started.
9. Real Criome path. Not started.
10. Real Nix first slice (build + SSH store source + verify + activate). Not started.

---

## 10 · Discipline rules

**"No Nix effect before CriomeAuthorizationActor grant"** (SS/141 §"Actors I expect in lojix"):

> No actor that mutates Nix, the store, a cache session, or a system profile runs before `CriomeAuthorizationActor` grants the exact request/scope.

Witness: OA/151 §"Test Witness" — `criome_authorization_denial_blocks_every_fake_nix_effect` in `lojix/horizon-leaner-shape/tests/build_pipeline.rs`.

ARCH text in:
- `lojix/horizon-leaner-shape/ARCHITECTURE.md` — "no local Nix, SSH, rsync, GC-root, cache, or activation effect starts until the authorization gate grants the canonical digest and scope."
- `lojix/horizon-leaner-shape/README.md` — warns daemon path fails closed until real Criome socket client lands.
- `signal-lojix/horizon-leaner-shape/ARCHITECTURE.md` — canonical deployment request digest belongs to contract layer.

**CLI/daemon boundary** (DA/113): `lojix/horizon-leaner-shape/ARCHITECTURE.md` + `tests/configuration_boundary.rs` (5 tests including `cli_has_exactly_one_runtime_peer_the_daemon_socket` and `daemon_deployment_path_owns_horizon_projection`).

**Two-deploy-stacks discipline**: `AGENTS.md` §"Two deploy stacks coexist" + `protocols/active-repositories.md` §"Two deploy stacks coexist".

---

## 11 · Recommendations for context maintenance

### Retire

- SS/16 (landed verbatim in `protocols/active-repositories.md`)
- SS/17 (folded into SS/136 narrative)
- SS/19 (subsumed by SS/138 + SS/141)
- SS/21 (superseded by SS/22 + SS/141 + D/213/214)

### Partial retire (residual narrative)

- SS/18 — retire after cross-walking residuals into SS/23
- SS/20 — five-axes framing useful as historical; SS/139 has canonical Arca decisions

### Forward to other roles

- CriomeAuthorizationActor witness needs cross-link from SS/141 to OA/151 so criome-side designers see what lojix-side already proves.
- D/207 four-bucket sorter discipline needs to be cited in any future SS report adding fields to `ClusterProposal` or `HorizonProposal`.
- DA/113 CLI/daemon boundary statement needs to be the citation when production cutover begins.

### Update directly (ARCH drift)

- **`/git/.../signal-lojix/ARCHITECTURE.md`** — replace "Skeleton. Documentation only. No Cargo.toml, no src/, no flake.nix" with "main holds the skeleton ARCH; current implementation on `horizon-leaner-shape`". Otherwise future agents will be misled.
- **`/git/.../arca/ARCHITECTURE.md`** — needs `/arca` (not `~/.arca`) decision and SS/139 collision/locator policy. Currently still describes `~/.arca`. Block before any implementation pass.

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master.
- `reports/designer/216-criome-routed-authorization-state-2026-05-18.md` — adjacent: criome side of the deploy authorization arc.
- `reports/designer/220-full-signal-executor-state-2026-05-18.md` — adjacent: `lojix-daemon` is the recommended second executor implementation after persona-terminal.
- `protocols/active-repositories.md` §"Two deploy stacks coexist" — the canonical discipline.
