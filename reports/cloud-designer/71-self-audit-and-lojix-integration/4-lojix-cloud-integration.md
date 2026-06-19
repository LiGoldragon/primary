# 4 · The lojix ↔ cloud deployment handoff

cloud-designer, 2026-06-19. Read-only design lane of session 71. Every
claim cites `file:line` or a Spirit record; production behaviour is
distinguished from what a report asserts.

## The shape, in one paragraph

cloud and lojix are **two operator-driven daemons that never call each
other** — they are joined by the operator (or a thin handoff tool) and by
two pieces of shared truth: a **node IP/domain** and a **CriomOS closure**.
cloud provisions a node booted from a **pre-baked CriomOS `CloudNode`
image** (`ad53`) so it comes up as a real, SSH-reachable NixOS, then hands
its `CloudHost { ipv4_address, host_name, host_identifier }` out via
`Observe Servers`. The operator publishes a `<node>.<cluster>.criome` DNS A
record (cloud's *own* Cloudflare capability — same daemon, separate
operation) pointing at that IP, and points lojix at exactly that domain.
lojix then runs its existing `nix copy --to ssh-ng://root@<domain>` +
remote-activate pipeline to switch the node onto the cluster generation.
There is **no wire contract between the two daemons today and none is
required** — the handoff is externally orchestrated through the domain
name, which is the one identifier both daemons already speak.

## (a) Bare node or pre-baked image? — PRE-BAKED CriomOS `CloudNode`

Decided, and now captured in Spirit `ad53` (Decision):

> *"Cloud-node OS images live in CriomOS as a minimal CloudNode-species
> profile built to provider snapshots so nodes boot fast. The cloud daemon
> references the image by id through the existing HostPlan image_name field
> and never holds the image definition."* — Spirit `ad53`

This resolves the prompt's fork in favour of pre-baked. The reasoning chain
(report 65 §3, §4):

- **A bare stock-Ubuntu node would force lojix to do a full
  install-and-convert hop** (`nixos-anywhere`/`nixos-infect`: kexec + disko
  + install + reboot, minutes) before its copy/activate pipeline means
  anything. lojix's activation pipeline assumes the target is *already a
  systemd-boot UEFI NixOS with `bootctl` and a mutable `/boot`* (report
  46-1 §3, citing `schema_runtime.rs:2390-2515`) — it has **no install
  path**. A bare node does not satisfy that precondition.
- **A pre-baked CriomOS `CloudNode` snapshot boots straight into NixOS**
  with sshd + the operator/deploy key already present, so lojix's *first*
  contact is its normal `nix copy` + `switch-to-configuration` — no special
  first-boot path (report 65 §3 "Verdict — pre-baking wins for up
  quickly").
- The split is clean against the component triad: **CriomOS owns the image
  bytes; cloud selects a snapshot id; lojix activates generations.** A
  NixOS image is not a Signal, so it cannot live in any cloud triad leg
  (report 65 §1 alternative (c), rejected on principle).

One honest scoping note carried from report 65 §1: the `CloudNode` species,
its CriomOS gate module, and the provider-format build attribute are **all
unbuilt today** — the decision is captured, the artifact is not. Until the
snapshot exists, a live integration test boots stock `ubuntu-24-04-x64`
(report 70's witness used exactly that) and lojix must do a one-time
install hop, OR the test reuses the proven Prometheus-hosted local VM path
(report 46) which sidesteps cloud entirely.

The "mint the first snapshot" step is itself the one-time install hop and
diverges by provider (report 65 §3): **DigitalOcean** has a true custom-image
upload API (`POST /v2/images` by URL), so the snapshot is minted off-cluster
with no throwaway server; **Hetzner** has *no* upload API, so the first
snapshot must be cut from a running bootstrapped server
(`hcloud-upload-image` `dd`-into-rescue, or `nixos-anywhere` then
`create_image type=snapshot`). After first mint, both providers boot the
snapshot by numeric id in seconds.

## (b) What cloud hands lojix as a deploy target — domain + ssh, observed not returned

The deploy target lojix needs is fully determined by **one string**: the
domain `<node>.<cluster>.criome`. lojix computes copy/activate addresses
from the cursor's cluster+node, *not* from a per-deploy IP override —
`SshTarget::root_at_node → root@<node>.<cluster>.criome`
(`schema_runtime.rs:2154-2192`; report 46-1 §3, report 46-3 §3). So the
integration's whole job is: **make `<node>.<cluster>.criome` resolve to the
new node's IP and accept `root` over ssh with lojix's key.**

What cloud actually produces, and the three sub-handoffs:

1. **The node record.** cloud's observed wire struct is `CloudHost`
   (`signal-cloud/src/lib.rs:283-292`,
   `signal-cloud/schema/lib.schema:43`):
   ```
   CloudHost { provider, account, host_identifier, host_name(DomainName),
               server_type, image_name, ipv4_address(IpAddress), host_status }
   ```
   This is the `(provider, host_identifier, ipv4_address, ssh_key)` the
   prompt names, plus the domain `host_name` and `host_status`. **The IP is
   NOT returned by create.** `ApplyPlan [Create]` replies only
   `PlanApplied { plan: <identifier> }` (`cloud/src/lib.rs:1672-1674`) — the
   node's IP/identity surface *later* via `Observe Servers → CloudHost`
   (report 70's witness: `ApplyPlan` created droplet 578873541; a separate
   `ObserveServers` then listed its IP/status). So the handoff is
   **create-then-observe**, not create-returns-target. This is the single
   most load-bearing seam: a poller/orchestrator must observe until
   `host_status` leaves `Initializing` and an `ipv4_address` is present.

2. **The domain (via cloud's own DNS capability — the same daemon).** cloud
   already carries the `DomainNameSystemRecords` capability over Cloudflare:
   `RecordKind::AddressV4 → "A"` (`cloud/src/cloudflare_cli.rs:324`),
   `DomainNameSystemRecord { name, kind, value, proxy_mode }`
   (`signal-cloud/src/lib.rs:304-308`). So cloud *can* publish
   `dune.goldragon.criome → <ipv4>`. But **host-create and DNS-create are
   separate operations — the daemon does NOT auto-create an A record when it
   creates a host** (no DNS call in the `apply_*_host_plan` path,
   `cloud/src/lib.rs:1547-1677`; the runtime grep shows DNS and host create
   are disjoint code). The orchestrator issues the A-record creation as a
   second meta operation after observing the IP.

3. **The ssh key.** cloud injects an ssh key *by provider-registered name*
   at create: `ServerSpec { ssh_keys: vec![plan.ssh_key_name...] }`
   (`cloud/src/lib.rs:1658-1664`, DigitalOcean; Hetzner identical at
   `:1578-1612`). The key is **provider-side**: pre-registered with the
   provider account under a name, and cloud-init injects it into the node's
   `root` `authorized_keys` at first boot. For lojix to reach the node, the
   key registered under `ssh_key_name` must be the **public key of the
   identity lojix's `ssh`/`nix copy` use** (report 46-1 §6 — the daemon
   shells out to `ssh -o BatchMode=yes` and `nix copy --to ssh-ng://`,
   inheriting the runner's ssh identity, `schema_runtime.rs:2194-2205`).

**Is there a wire contract between cloud and lojix? No — and none is
needed.** Neither daemon imports the other; neither speaks the other's
signal. The coupling is the *domain name* plus the *ssh key identity*, both
external orchestration. This is the right shape: each daemon stays a pure
single-responsibility Signal endpoint (cloud INTENT.md "carry only Signal
wire vocabulary"; lojix INTENT.md "the daemon never initiates deploys on
its own"). The orchestration that joins them is operator-issued NOTA today,
and a thin handoff *tool* tomorrow (not a daemon-to-daemon link).

## (c) Secrets / identity — sops-nix at activation + criome-custodied machine identity

Two Spirit records pin this, and they answer the prompt's two halves:

- **Cluster/node secrets: sops-nix, decrypted on the target at activation
  (`cjrl`).** *"For cluster deployment [the most secure place] is SOPS-nix,
  encrypted at rest in the repository and decrypted only on the target host
  at activation."* — Spirit `cjrl` (Principle, VeryHigh). The secret bytes
  are **never on the wire and never in cloud's hands**: they ride inside the
  CriomOS closure as sops-encrypted files and are decrypted by the node's
  own age/host key at `switch-to-configuration` time. Report 40-2 confirms
  this is live: a router node (prometheus) *hard-fails eval* without the
  secrets override (the sops `sopsFiles` assertion at
  `router/default.nix:89-97`), while the three secret-free nodes (zeus,
  tiger, ouranos) evaluate and deploy with the empty `{ sopsFiles = {}; }`
  stub. **First cloud-node cutover targets a secret-free profile** (the
  `CloudNode` species is deliberately minimal, like `TestVm` — report 65
  §1) so the sops materialization is not on the critical path.

- **The node's machine identity that decrypts those secrets: criome-custodied
  (`h03z`).** *"the lojix deploy daemon's own operational credentials and
  unattended machine identity are custodied and authenticated through criome
  rather than borrowing the operator's personal logged-in session such as
  the GPG SSH agent."* — Spirit `h03z` (Decision; tags `lojix`, `criome`).
  Today lojix borrows the operator's ssh identity (report 46-1 §6); the
  intended end-state is a criome-custodied deploy identity. This connects to
  cloud's own credential arc: `iprx` (Decision) accepts the current
  wire-handle→env-var model as transitional and points custody at
  *"system-custodied machine credentials following the criome-custodied and
  sops-nix machine-identity pattern of h03z."*

So three identities, three custodians, no overlap:
| Identity | Used for | Custodian | State |
|---|---|---|---|
| cloud provider API token | create/destroy nodes | gopass handle → env var, behind 0o600 owner socket (`iprx`); → criome eventually | built (`iprx`) |
| node ssh / deploy key | lojix reaches the node | operator ssh identity today; criome-custodied per `h03z` | built (operator), intended (criome) |
| node host/age key | decrypts sops secrets at activation | the node's own machine identity (`cjrl`); criome-custodied (`h03z`) | per-node, sops path live (`cjrl`); criome integration unbuilt |

## (d) Built today vs unbuilt

**Built and proven live:**
- cloud create→observe→destroy through the daemon socket spine, against
  live DigitalOcean (report 70 — droplet 578873541, every leg over the
  socket). `ApplyPlan [Create]` → real node; `Observe Servers` → `CloudHost`
  with ipv4 + status.
- cloud DNS A-record capability over Cloudflare (`cloudflare_cli.rs`,
  capability `DomainNameSystemRecords`).
- ssh-key injection by provider-registered name at create
  (`cloud/src/lib.rs:1658-1664`).
- lojix's full copy + UEFI activation pipeline, target-store build, and
  disconnect-surviving `BootOnce` (ARCHITECTURE.md report-150 note;
  report 46-3) — validated against a local VM, not a cloud node.
- sops-nix-at-activation secrets gate, with the secret-free escape proven
  for zeus/tiger/ouranos (report 40-2).

**Unbuilt / open:**
- The CriomOS `CloudNode` species + gate module + provider-format build
  attribute — the snapshot itself (report 65 §1; `ad53` is captured, the
  artifact is not).
- The first-snapshot mint per provider (DO upload vs Hetzner bootstrap —
  report 65 §3).
- **The create→observe→DNS→deploy orchestration glue.** No tool sequences
  cloud-apply → poll-observe-for-ip → cloud-DNS-A → lojix-deploy today;
  report 70 ran the cloud legs by hand and never crossed into lojix.
- criome-custodied deploy/machine identity (`h03z`, `iprx` end-state) —
  intended, unbuilt.
- cloud has no SEMA-persisted provisioning ledger of "which node is which
  cluster member" yet (cloud INTENT.md names SEMA persistence as future);
  the (cluster, node) ↔ (provider, host_identifier, ipv4) binding lives
  only in the orchestrator's head today.

## Recommended concrete shape

**A thin, operator-authorized handoff tool (not a daemon-to-daemon wire)**
that runs the create→observe→DNS→deploy sequence, each step an existing
NOTA operation on an existing socket. cloud stays the compute/DNS control
plane; lojix stays the generation activator; CriomOS owns the image. The
tool is the orchestration the prompt asks for, and it needs **zero new wire
field** on either contract (report 65 §2: `image_name` already carries the
snapshot id end-to-end).

```mermaid
sequenceDiagram
    actor Op as Operator / handoff tool
    participant CriomOS as CriomOS<br/>(image bytes)
    participant Cloud as cloud-daemon<br/>(compute + DNS)
    participant Prov as Provider<br/>(DO / Hetzner)
    participant Node as New node<br/>(CloudNode snapshot)
    participant Lojix as lojix-daemon<br/>(generation activator)

    Note over CriomOS,Prov: ONE-TIME (per provider): mint the CloudNode snapshot
    CriomOS->>Prov: build CloudNode image → upload/snapshot → numeric image id (ad53)

    Note over Op,Node: PER NODE: create → observe → DNS → deploy
    Op->>Cloud: meta-cloud PrepareHostPlan<br/>(provider, host, type, IMAGE=snapshot-id, ssh_key_name)
    Op->>Cloud: meta-cloud ApprovePlan / ApplyPlan [Create]
    Cloud->>Prov: create_host(ServerSpec{ image=snapshot, ssh_keys=[key] })
    Prov->>Node: boot CloudNode snapshot; cloud-init injects ssh key
    Cloud-->>Op: PlanApplied(plan-id)  %% NO ip returned

    loop until status≠Initializing & ipv4 present
        Op->>Cloud: cloud Observe Servers
        Cloud-->>Op: CloudHost{ host_identifier, ipv4_address, status }
    end

    Op->>Cloud: meta-cloud apply DNS plan:<br/>A  <node>.<cluster>.criome → ipv4
    Cloud->>Prov: Cloudflare create A record

    Note over Lojix,Node: lojix's existing pipeline — domain is the only coupling
    Op->>Lojix: meta-lojix Deploy<br/>(cluster, node, FullOs, BootOnce)
    Lojix->>Node: nix copy --to ssh-ng://root@<node>.<cluster>.criome  (sops files inside closure)
    Lojix->>Node: ssh root@<domain> switch-to-configuration boot<br/>(node decrypts sops at activation — cjrl)
    Lojix-->>Op: AcceptedDeploy(generation-id)
    Op->>Lojix: lojix Query (ByEventLog) → Activated
```

The four guarantees this shape preserves:

1. **No daemon-to-daemon coupling.** cloud and lojix never import or call
   each other; the join is the domain name + ssh identity. Each stays a
   single-responsibility Signal endpoint.
2. **No new wire field.** The snapshot id rides the existing
   `image_name`; the IP rides the existing `CloudHost.ipv4_address`; the
   domain rides the existing `DomainNameSystemRecord`. Confirmed against
   source in report 65 §2.
3. **Secrets never touch cloud.** sops files are inside the lojix-copied
   closure and decrypt on the node at activation (`cjrl`); cloud only ever
   sees an IP and a domain.
4. **The create→observe seam is explicit.** Because create returns only a
   plan id, the orchestrator *must* poll `Observe Servers` for the IP — the
   one piece of glue that does not exist today and is the first thing to
   build.

The migration end-state (per `h03z`/`iprx`): the operator's ssh identity in
step "Deploy" and the provider token in step "create" both move to
criome-custodied machine credentials, and the node's sops host key becomes
criome-custodied too — at which point the handoff tool authenticates to
both daemons as a criome principal rather than borrowing a human session.
That is a custody upgrade to the *same* sequence, not a reshape of it.
