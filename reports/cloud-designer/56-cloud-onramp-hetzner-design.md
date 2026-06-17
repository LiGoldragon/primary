# 56 · Cloud on-ramp — on-demand compute nodes, Hetzner first (2026-06-17)

Psyche directive: *"we need to get cloud nodes up. we need the cloud
component to connect to providers so we can spinup on demand. target
easiest spinup targets."* Captured as Spirit `150a` (Decision, High):
[The cloud component next active capability is on-demand compute-node
provisioning: connecting to cloud-hoster provider APIs to spin up server
nodes on demand. Provider growth targets the easiest-to-spin-up providers
first.]

This report mines the existing cloud intent + the shipped daemon + the
deploy stack (a five-agent understand sweep, `wf_41161f23`), recommends a
provider, and decomposes the work into a clearly-unblocked **Phase 1**
(bare node up on demand) and a fork-bearing **Phase 2** (bare node →
CriomOS cluster member). The forks in §7 are the psyche's to call; Phase 1
is mine to build.

## 1 · The reframe — this is one provider, not a greenfield

The cloud component is not documentation-only. Bead `primary-kbmi` (the
cloud/domain-criome runtime build) is CLOSED: the daemon ships with a thin
CLI, two sockets (public `signal-cloud` for Observe/Validate, owner-only
`meta-signal-cloud` for Mutate), sema-engine state, and **Cloudflare DNS
read-only** as the proven first provider. "Spinup on demand" = a second
provider — a **compute** provider — added along the exact pattern
Cloudflare established.

Settled intent already fixes the surface:

- [Cloud is the home for provider API machinery including Cloudflare,
  Google, and cloud hosters such as Hetzner] (`mcwa`) — the compute-hoster
  direction was already named; `150a` turns it active.
- [Cloud component surface splits Mutate verbs onto meta-signal-cloud
  (privileged) and Query verbs onto signal-cloud (public)] (`6sxn`); Plan
  renamed Mutate, reply Mutated (`p6j5`); last-known-acknowledgment state,
  Mutate-sent vs Mutated (`8fe9`).
- [Provider support should be build-selectable; unsupported provider
  requests return a typed unsupported-capability reply] (`jvpe`);
  capability observation distinguishes built-but-unconfigured from
  not-built (`zm8n`).
- Contracts carry ONLY wire vocabulary; Nexus + SEMA planes live in the
  daemon (`l6zw`, `yjik`, `26e7`).
- The gopass-shim auth pattern is proven on Cloudflare: a provider-scoped
  gopass path injected as an env var by a `wrapProgram` clause inside the
  nix closure, never in the rkyv config, never echoed (`nsi2`, `16l0`,
  `ravc`).

The sweep also found the scaffolding is half-built **for Hetzner
specifically**: the `Provider::Hetzner` variant exists in both contracts,
`provider_supports_capability` already maps `(Hetzner, CloudHosts)`
(`cloud/src/lib.rs:1354-1364`), `provider_is_built` already gates on a
`hetzner` cargo feature (`cloud/Cargo.toml:30`, currently an empty
placeholder). The directive lands on a path the architecture already
anticipated.

## 2 · Recommendation — Hetzner Cloud

Ranked easiest-first for programmatic on-demand NixOS spinup (current
2026 facts, verify live pricing at create time):

| Provider | Ease | NixOS bring-up | Cheapest | Auth |
|---|---|---|---|---|
| **Hetzner Cloud** | **easiest** | nixos-anywhere/kexec (its canonical example); native images exist | CAX11 ARM ~€3.79/mo, CX22 x86 ~€4.59/mo | single project Bearer token; `ssh_keys` is a first-class create field |
| DigitalOcean | easy | no native image; kexec/nixos-anywhere | $4/mo | Bearer token; account-level SSH keys |
| Vultr | easy | kexec or custom ISO upload | $2.50/mo IPv6-only | Bearer key; SSH-key resources |
| Linode/Akamai | moderate | kexec, but reported post-install non-boot (#412) | $5/mo | Bearer token |
| Scaleway | moderate | kexec; less community tread | ~€4.99/mo | access-key + secret + org-id |
| AWS EC2 | hard | **official NixOS AMIs** + first-party Rust SDK, but IAM/VPC/SigV4 | t4g.nano ~$3.07/mo + surcharges | IAM SigV4 |

**Hetzner wins every friction axis for a Rust-daemon flow:** one
project-scoped Bearer token (no SigV4/IAM, no access-key+secret+org-id
dance — the daemon's REST client is a thin authenticated POST); `ssh_keys`
is a first-class array on `POST /v1/servers` so the create-time key is
declarative, no cloud-init templating; it is the canonical documented
nixos-anywhere target (best-trodden install path); and it is the cheapest
of the six.

**Call the flat REST directly with `reqwest`, not an SDK.** The only
first-party Rust SDK in the field is AWS's; Hetzner's two crates (`hcloud`
0.23, `hetzner` 1.0) are community-maintained. For a daemon we control the
REST surface is simple enough that a thin `reqwest` client keeps the
dependency surface owned — preferred over an unvetted SDK dependency.

AWS is worth a footnote: it is the *only* provider with native NixOS AMIs
(launch directly, no kexec) **and** a first-party Rust SDK. If
attestation/native-image guarantees later become a hard requirement, the
easiest-first Hetzner pick may warrant revisiting — noted, not blocking.

## 3 · Two phases — what's unblocked vs what forks

**Phase 1 — a bare cloud node, up on demand (UNBLOCKED, designer-owned).**
The cloud daemon gains a Hetzner compute provider: `CreateServer` /
`DestroyServer` Mutate ops on the owner socket, `Observe` for server
state on the public socket, a `reqwest` client, the `hetzner/api-token`
gopass shim, the cargo feature. This alone satisfies "connect to providers
so we can spinup on demand" — a real VM, created and destroyed on command,
following the Cloudflare pattern with zero architectural forks. **I can
build this now.**

**Phase 2 — bare node → CriomOS cluster member (FORKED, §7).** Turning
the bare VM into a deployed, tailnet-joined CriomOS node crosses into the
deploy stack and surfaces two genuine architecture decisions (the install
hop's owner; the chicken-and-egg of naming a node before it exists). These
are the psyche's calls and should be settled before Phase 2 — but they do
**not** block Phase 1.

## 4 · The minimal path to one node up

1. **PROVISION** — owner submits a compute Mutate on the meta socket. The
   daemon resolves `HCLOUD_TOKEN` fresh from gopass `hetzner/api-token`
   (wrapProgram shim, mirroring `cloud/flake.nix:49-57`), registers the
   durable CriomOS root pubkey once as a Hetzner project resource
   (`POST /v1/ssh_keys`, reuse by name), then `POST /v1/servers` with
   `server_type` (cax11/cx22), a base image (Ubuntu for the kexec route),
   and `ssh_keys:[<name>]`. Store the returned server id + public IPv4 in
   SEMA.
2. **WAIT-READY** — poll `GET /v1/servers/{id}` until `status=running` and
   TCP:22 answers (key-auth works on first boot — the pubkey was in the
   create call).
3. **INSTALL** — run nixos-anywhere non-interactively from the daemon's
   Nix-capable environment: `nix run github:nix-community/nixos-anywhere --
   --flake <criomos-flake>#<host> --generate-hardware-config
   nixos-generate-config ./hardware-configuration.nix --target-host
   root@<ip>`. kexec boots the installer, disko partitions, the CriomOS
   config installs. The **durable** root key lives in the CriomOS flake
   (`adminSshPubKeys` → `users.nix:46-48`), independent of the Hetzner
   create-time key (which only authenticates the kexec session).
4. **REGISTER-DNS** — the cloud daemon's existing Cloudflare path writes
   `node-N.cluster.criome → public IPv4` so the hostname resolves for
   lojix.
5. **JOIN/DEPLOY** — operator submits `meta-lojix (Deploy FullOs cluster
   node-N github:LiGoldragon/CriomOS Boot none)`; lojix materializes the
   horizon, builds the closure, `nix copy --to ssh-ng://root@…`, activates
   via `switch-to-configuration boot`; the host reboots into the
   generation, joins the Tailnet, becomes an operational member.

## 5 · Architecture — three daemons, one spine

Three independent daemons compose along provision→install→deploy; none
spans the whole chain today, and the **install hop is the load-bearing
gap**.

- **cloud (PROVISION).** Owns the Nexus effect plane + SEMA state. Owner
  `meta-signal-cloud` carries Mutate; public `signal-cloud` carries
  Observe/Validate. Secrets enter via the gopass wrapProgram shim — the
  daemon takes exactly one rkyv startup arg and never sees the secret
  value. For compute, this same machinery reaches the Hetzner REST API and
  (Phase 2) shells out to nixos-anywhere.
- **horizon-rs (MODEL, not a daemon).** Projects a cluster proposal into
  per-(cluster,node) horizons CriomOS consumes — `adminSshPubKeys`, roles,
  host-set image-exchange keys. The provider↔CriomOS SSH handoff closes
  because the *same* pubkey is declared in `goldragon/datom.nota`, injected
  by the provider at create, and baked into root's authorizedKeys by
  CriomOS (`users.nix:46-48`). horizon-rs has a Machine/Node model
  (`super_node`/`host_set`) but carries **no provider identity or
  bootstrap-flake reference** yet — its own `INTENT.md` flags this.
- **lojix (DEPLOY).** Takes `meta-lojix Deploy`, materializes the horizon,
  builds + `nix copy` + `switch-to-configuration` over ssh-ng to a host
  **that already runs NixOS**. lojix explicitly does **not** bootstrap
  (ARCHITECTURE scope S4a: copy/activate are target-safe).

The missing seam: after cloud creates the bare VM, *something* runs
nixos-anywhere to land an initial NixOS so lojix can take over — plus a
SEMA-tracked handoff of the node's IP and readiness between the cloud and
lojix planes.

**The single biggest implementation risk** (§8): server provision and the
nixos-anywhere shell-out are long, blocking operations. The current
Cloudflare path is synchronous and an audit already flags that long
provider calls block the listener socket. The compute effect **must** be
deferred/actor-based, not inline — or the daemon freezes for the whole
install.

## 6 · Component change list

- **cloud (daemon + adapter).** New `src/hetzner.rs` — a `reqwest`-based
  `HetznerApi` trait + `ProviderClient { api, credentials }` with
  create/get/delete/ensure-ssh-key, credentials via the existing
  `EnvironmentCredentialSource` (`cloudflare.rs:48-57`). Enable the
  `hetzner` feature deps (`Cargo.toml:30`). Extend `Store`
  (`lib.rs:523-594`) with a `#[cfg(feature="hetzner")]` field + observe/
  apply handlers (`lib.rs:1137-1269`). Add a `CommandEffect` variant in
  `cloud/schema/nexus.schema` and the `default_capabilities` entry
  (`schema_runtime.rs:104-127`) — note the capability matrix is half-done.
  **Compute effects run off the listener (deferred/actor), not inline.**
- **signal-cloud (contract).** Wire vocab is DNS+redirect only today. Add
  a read-only `CloudHostsQuery`/`CloudHostListing` Observation arm and a
  `CloudHost { name … identifier … provider … host_state … public_address
  … }` record. Wire-only; no runtime logic (`l6zw`/`yjik`/`26e7`).
- **meta-signal-cloud (contract).** Add compute Mutate ops:
  `DesiredHostState`, a `HostPlan` (create/delete/resize), Prepare/Approve/
  Apply variants (or union into the existing Plan), and rejection reasons
  (e.g. InsufficientQuota). RegisterAccount/RotateCredential/SetPolicy stay
  provider-agnostic — the Hetzner credential just registers against
  `hetzner/api-token`.
- **lojix (daemon).** No schema change for the deploy itself. The gap is
  the install hop (Phase 2 fork): either a new bootstrap effect/tool that
  runs nixos-anywhere before Deploy, or cloud owns the shell-out and lojix
  only deploys post-install. S4a does **not** cover bootstrap — adding it
  is a deliberate scope expansion with its own intent capture.
- **CriomOS (OS image).** Minimal for the SSH handoff (root authorizedKeys
  already flow from `adminSshPubKeys`, `users.nix:46-48`). Needs a per-host
  disko disk-config matching the Hetzner device (`/dev/sda` for cx22;
  verify the cax11/ARM device once) and a hardware-config consumable by
  `nixos-anywhere --generate-hardware-config`. One architecture per host.
- **horizon-rs (model, Phase 2).** No provider/bootstrap notion today
  (`INTENT.md` open question). If provisioning is cluster-authored, add a
  provider/bootstrap dimension to the Machine/Node model (provider,
  server_type/architecture, bootstrap-flake ref) — this resolves the
  chicken-and-egg.
- **goldragon/datom.nota.** Declare node-N with its `adminSshPubKey` (the
  durable CriomOS key, == the key registered at Hetzner) and, if horizon
  gains the dimension, provider/server_type/architecture/bootstrap-flake.
- **secrets.** Add gopass `hetzner/api-token` → `HCLOUD_TOKEN`, a
  wrapProgram clause injecting it into the cloud-daemon env at launch
  (mirror `cloudflareCli`, `flake.nix:49-58`, exit 78 on fetch failure).
  Never echoed; stays out of the rkyv DaemonConfiguration.

## 7 · Open decisions for the psyche

Each changes what gets built; my recommended disposition follows each.

1. **Install-hop ownership.** Does the cloud daemon shell out to
   nixos-anywhere itself (cloud owns provision→installed-NixOS, lojix takes
   over), or does lojix gain a new bootstrap effect (cloud only creates the
   bare VM)? This decides which daemon's blast radius and contract grows,
   and whether lojix expands beyond its declared S4a scope. The install
   *mechanism* is settled (nixos-anywhere over kexec); only the *owner* is
   open. **Recommend: cloud owns it** — provisioning and first-install are
   one provider concern; keep lojix purely the steady-state cluster
   deployer. (Phase 2; does not block Phase 1.)
2. **Chicken-and-egg / horizon provider dimension.** A node must be named
   in the cluster proposal to be projected, but it doesn't exist until
   provisioned. Two resolutions: (a) horizon-rs gains a provider/bootstrap
   dimension so provisioning is cluster-authored from `datom.nota`; or (b)
   provisioning stays outside horizon and registers the node into the
   proposal *after* the VM exists (two-phase: provision → amend proposal →
   project → deploy). **Recommend (b) first** (less model churn, matches
   "create on demand"), with (a) as the durable end-state once the pattern
   proves out.
3. **Default architecture.** ARM (CAX11, ~€3.79/mo, aarch64) or x86 (CX22,
   ~€4.59/mo, x86_64) as the default CriomOS cloud node? Fixes the flake
   system attribute, disko device, and image architecture per host.
   **Recommend ARM/CAX11** (cheapest; our stack already builds aarch64) —
   trivially overridable per node.

Two follow-on optimizations carry clear defaults and need no decision now:
contract shape (recommend a **new compute Observation/Plan family** rather
than overloading the DNS-shaped Plan — designer's call per the parallel-
lane model); and native-image vs kexec (recommend **kexec/nixos-anywhere
first**, a pre-built Hetzner snapshot via nixos-generators+hcloud-upload-
image as a later lock-step optimization).

## 8 · Risks

- **Blocking listener** (highest) — compute effects must be deferred/actor,
  not inline like the sync Cloudflare path, or the daemon freezes for the
  whole provision+install.
- **Two-key conflation lockout** — the Hetzner create-time key authenticates
  only the kexec session; a full-disk install wipes it. The durable root
  key MUST live in the CriomOS flake and equal the `datom.nota` key.
- **disko device mismatch** — the most common nixos-anywhere failure; use
  `--generate-hardware-config`, pin the device per server_type, verify the
  ARM device once.
- **Nix-capable install host** — nixos-anywhere needs nix where it runs;
  the cloud daemon already lives in a Nix closure, but confirm nix is on
  PATH or shell out to a build host.
- **Price/region drift** — read live Hetzner pricing at create time (15 Jun
  2026 adjustment); don't hardcode.
- **Cross-provider disko non-portability** — the Hetzner disk-config does
  not transfer unchanged (Linode #412 non-boot); verify each provider once.
- **Contract churn** — both contracts are DNS+redirect-shaped today; design
  the compute family once rather than bolting it onto DNS records.
- **lojix scope creep** — if the install hop lands on lojix, treat it as an
  explicit architecture decision with its own intent capture.

## 9 · Next step

Build **Phase 1** on cloud-component feature branches in `~/wt` (cloud +
signal-cloud + meta-signal-cloud), per the cloud-designer prototype method
(`iplo`): a working Hetzner compute provider that creates, observes, and
destroys a real bare VM on demand through the meta + ordinary sockets,
gopass-tokened, feature-gated, with the compute effect deferred off the
listener. Audit it against the full designed surface; the gaps drive the
next growth pass. Phase 2 waits on the §7 forks.
