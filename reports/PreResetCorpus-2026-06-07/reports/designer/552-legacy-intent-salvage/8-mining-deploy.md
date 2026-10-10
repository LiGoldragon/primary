---
title: 552 — Legacy intent salvage — mining deploy.nota
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, legacy-nota, deploy, lojix, deletion-readiness]
description: |
  Mining report for intent/deploy.nota (14 records). Finds the few core,
  durable, not-too-specific deploy-architecture ideas genuinely at risk on
  deletion — not already in Spirit and not already in the guidance layer.
---

# 552 — Mining deploy.nota

## Scope

Scanned `/tmp/intent-text/deploy.txt` — the date-stripped text extraction of
`intent/deploy.nota`, 14 records (all stored Maximum certainty in the legacy
file, which over-states; the legacy file recorded everything at Maximum). The
deploy domain is one of the best-covered in the deployed Spirit store (deploy
19, deployment 23, lojix 18, the full lojix rewrite charter present), so most
records dedup cleanly. Three genuine gaps survive; two more are borderline and
flagged for the synthesis pass.

## Salvage candidates

### 1. Node deploys itself locally — eliminating the remote-activation problem class

- **Kind:** Decision
- **Proposed topics:** `[lojix deploy daemon-mesh local-activation ssh-safety resilience]`
- **Proposed description:** The lean lojix deploy model is local execution per
  concern: the host being deployed runs its OWN activation. The deploy daemon
  mesh coordinates remote daemons (build, cache, target) but does not hold a
  remote SSH session for the activation effect itself — the node deploys
  itself. This is an ARCHITECTURAL elimination of the entire
  SSH-disconnect-survival problem class, not a work-around: where the
  production stack engineered detached/boot-mode activation so a dropped SSH
  would not kill a deploy, the new model removes remote activation entirely so
  there is nothing for a disconnect to kill.
- **Proposed certainty:** High (legacy says Maximum, but it is a design
  direction for an unfinished rewrite, so High is honest).
- **Supporting verbatim:** "the deployment could actually be done by using the
  lojix daemon of the host on which we're deploying, so that the deployment
  logic wouldn't need all of this remote command passing... we ended up
  implementing logic to make sure that a disconnect, an SSH disconnect, did not
  kill the deployment process."
- **Preservation evidence:** Spirit deploy/lojix queries return many records on
  the SSH-disconnect symptom (`kx32`, `65bo`, `1lex`, `ic7c`, `xv9v`) but all
  describe WORKING AROUND it on the production stack (boot-mode, detached
  systemd units, out-of-band access). The architectural elimination via
  node-local self-activation is absent. `2alg` covers the concurrent
  per-request worker model, not local-vs-remote activation locus. `rg` over
  ESSENCE/AGENTS/INTENT/skills for `self.deploy|node.*itself|local.*activation|
  ssh.disconnect` returns nothing.
- **At-risk rationale:** This is the founding "why" of the lojix lean rewrite's
  deploy model — the single sentence that explains why the new stack drops all
  the remote-command-passing machinery. The Spirit records describe the
  symptom and its production work-arounds but never the architectural cure, so
  deleting the legacy file loses the design rationale.

### 2. Daemon holds a believed cluster + network topology that routing consults

- **Kind:** Principle
- **Proposed topics:** `[lojix deploy topology routing cluster-data network cost]`
- **Proposed description:** The lojix daemon maintains a "possibly-true" /
  last-known-believed cluster AND network topology — node roles, reachability,
  latency, bandwidth, and cost — as part of its state, beyond just deploy job
  records. The believed topology informs deploy routing: which node serves as
  Nix cache, whether to fall back to builder-as-cache, whether a remote cache
  is too far / too narrow-bandwidth / too expensive on a metered network to use.
  State is more than job records; it is a cluster-and-network-and-cost model
  that routing decisions read.
- **Proposed certainty:** Medium (a stated direction for an unbuilt routing
  layer; the cost/metered-network variables are explicitly tentative wording).
- **Supporting verbatim:** "a very important part of the state is what the
  daemon believes the topology is. It's a possibly true topology... last known,
  believed to be true... network topology, so that if the Nix cache is really
  far or has very little bandwidth or is expensive, we could even have variables
  like cost."
- **Preservation evidence:** `i6ih` (Maximum) states the GENERAL Criome pattern
  — component state is last-known-acknowledgment forming a quorum-of-agreement
  — which is the upstream root of this idea, but it does NOT name the
  deploy-specific application: a network/cost topology model the deployer's
  cache-routing decisions consult. Spirit topology query returns routing and
  cluster-data records (`9p8v`, `a2t4`, horizon split) but none about a
  cost/latency/bandwidth-aware deploy-routing model. No guidance-file hit for
  `believed topology|cost.*cache|metered`.
- **At-risk rationale:** `i6ih` preserves the abstract pattern; the concrete
  deploy-routing consequence (believed network topology + cost model drives
  cache selection and fallback) is the load-bearing specific that survives
  generalization and is found nowhere else. Without it the deploy daemon's
  state scope collapses to job records.

### 3. Criome holds deploy authorization policy; the signal call is the signed object

- **Kind:** Decision
- **Proposed topics:** `[lojix signal-lojix criome authorization policy-contract signing]`
- **Proposed description:** Authorization for a deploy (a signal-lojix call) is
  propagated through the criome-daemon topology: criome holds the policy data
  (which key or quorum has which permission) and the signal-lojix call is the
  object signed. lojix does not own permission and does not itself sign — it
  submits intent and waits for criome to authorize; the signature lives in
  criome, not in lojix. Daemons talk to daemons and the CLI/client only
  initiates: the receiving lojix daemon forwards the request to the local
  criome daemon, which routes signature solicitations to the concerned clients
  (signing devices, persona-terminal surfaces, yubikeys). The operator's
  machine is a thin client needing only the CLI, plus optionally its own criome
  daemon if it holds a signing key.
- **Proposed certainty:** Medium (the destination is clear but legacy records
  10 + 6 explicitly DEFER wiring criome authorization out of the current
  migration arc, so it is a stated future shape, not active).
- **Supporting verbatim:** "authorization is propagated through the
  criome-daemon topology first, with the signal lojix call being the object
  signed, and the criome holds the permission data (which key/quorum has which
  permission)" + "daemons talk to each other, the cli (or any client) only
  initiates the deploy."
- **Preservation evidence:** Spirit `vudl` / `9v7h` cover the lojix two-contract
  AUTHORITY SPLIT (owner-only Deploy/Pin/Unpin/Retire in meta-signal-lojix,
  peer-callable in signal-lojix) and SO_PEERCRED owner-socket auth — the LOCAL
  socket-tier authority — but NOT the criome-mediated, signature-as-signed-call,
  quorum-policy-in-criome model. The criome/domain-criome query returns
  authority-delegation constraints (`jq0q`, `3gki`) but nothing tying the
  signal-lojix call to criome as the signing/policy substrate. No guidance hit
  for `criome.*authoriz|signed object|quorum`.
- **At-risk rationale:** Spirit captured the deploy authority split as it lands
  now; the deferred destination — criome as the authorization substrate, the
  signal call as the signed object, lojix as a non-signing intent-submitter —
  is the design direction the split eventually converges to, and it lives ONLY
  in this file's deferred records. Deferred-but-durable destinations are
  exactly what gets lost when the source file is deleted.

## Borderline — flagged for synthesis, not strongly held

- **lojix-daemon takes control of nix config** (deploy.txt #4). The general
  idea — the deployer owns `/etc/nix/nix.conf` (or a daemon-owned include slot)
  and restarts nix-daemon to install a transient per-deploy substituter trust
  key then remove it on release — is NOT in Spirit. But it leans toward
  mechanism rather than durable principle, and `ur16`/`7x50` cover the broader
  daemon-owns-its-configuration shape. Synthesis may fold this into candidate 1
  as a consequence of node-local deploy rather than record it standalone.
- **Every node has a signing key; ClaviFaber populates on first boot**
  (deploy.txt #5). `skills/system-operator.md` carries the MANUAL per-node
  signing-key generation procedure (`nix-store --generate-binary-cache-key`)
  and flags it "partially landed." The DESIGN PRINCIPLE — that this is
  automatic on first boot via ClaviFaber, making cluster-wide signed-cache
  trust the default rather than a manual step — is not in Spirit and only
  partially in the skill. Worth a one-line principle if the synthesis judges
  the automatic-on-first-boot intent durable; dropped if the manual procedure
  in the skill is deemed sufficient.

## Already preserved / dropped (safe to delete)

Of 14 records, 9 fail the curation criteria and confirm the file is largely
safe to delete:

- **#7 daemons-talk-to-daemons / thin-client CLI** — folded into candidate 3
  above; the standalone CLI-only-initiates shape is also implied by `vudl` and
  the component-triad CLI-is-first-client rule in AGENTS.md.
- **#8 bootstrap is not an architectural gap** — a CORRECTION of an agent's
  invented problem ("the production lojix-cli IS the bootstrap path"); the
  two-stacks-coexist discipline is in `protocols/active-repositories.md` and
  the rewrite charter `tvbn`/`fe2j`. Transient correction, preserved upstream.
- **#9 owner-signal-lojix now vs CLI-dispatch-in-parallel** — a task-ordering
  decision ("do it now, adapt as code lands"); dies with the task. The durable
  outcome (meta-signal-lojix two-contract split) is in `vudl`, `hnpo`, `r9qy`.
- **#10 criome-mediated authorization deferred** — the deferral itself is
  transient; the destination is captured as candidate 3.
- **#11 split Build/Activate/Deploy/Rollback verbs** — the durable principle
  ("verbs are cheap, split beats collapse") is already in Spirit (the workspace
  verbs-are-cheap principle the record cites) and the concrete split is in
  `vudl`. Activate-vs-Deploy collapse was a one-off open question.
- **#12 use production CriomOS not the feature-branch checkout** — a one-off
  task scoping constraint for a specific deployment; too specific, dies with
  the task. The general production-target discipline is in `bc6f`, `dska`, and
  the two-stack discipline.
- **#13 update home-profile lock file before redeploy** — captured generally by
  `bc6f` (FullOS deploys carry latest home fixes via flake-lock update) and
  `bev5`; this instance is task-specific.
- **#14 redeploy only the necessary layer (home vs OS)** — a per-task decision
  rule for one Spirit rollout; the general home-vs-OS layering is operational
  and covered by `system-operator.md` deploy discipline.
- **#1/#2 SSH-disconnect work-arounds (the symptom side)** — the production
  work-around half is thoroughly in Spirit (`kx32`, `65bo`, `1lex`, `ic7c`,
  `xv9v`); only the architectural-elimination half (candidate 1) is at risk.

The file's deploy-safety reactions, the lojix rewrite charter, the concurrency
model, the authority split, and the verb split are all live in the deployed
Spirit store. The three surviving candidates are the design-direction "why"
statements — node-local self-deploy, believed-topology-drives-routing, and
criome-as-authorization-substrate — that the operational records never carry.
