# 6 · Synthesis — the create→observe→DNS→deploy handoff: implementation-ready spec + fix ledger

cloud-designer, session 72, 2026-06-19. Synthesizes lanes A–D
(`1-lojix-deploy-contract.md`, `2-cloud-socket-contract.md`,
`3-criomos-cloudnode-build.md`, `4-hanging-bugs-ledger.md`) with the
adversarial verdicts on the bug findings and the completeness critiques of
each lane. Live Spirit was down this session; intent grounded in manifested
`INTENT.md` / `ARCHITECTURE.md` and schema sources. Every load-bearing claim
cites `file:line`; NOTA is ground-truth (encoder-verified, lanes A/B). Two
cloud trees were checked: main HEAD `3b38cdd` and the `cloud-designer-intent-refresh`
worktree `88b852d` (two designer commits ahead — INTENT/README/flake docs
only; no code or schema change vs main).

## TL;DR — what changed vs lanes A/B from the verdicts

- **The 10-leg cloud table is missing a mandatory 11th leg: `SetPolicy`
  between DNS RegisterAccount and PreparePlan.** Without it, DNS ApplyPlan
  returns `ProviderNotConfigured` regardless of a correct account + approved
  plan, because `account_binding_for_zone` (`cloud/src/lib.rs:1097-1113`)
  resolves the account **only through a zone policy** whose `provider ==
  Cloudflare` and `allowed_zones` contains the exact zone. Confirmed in
  source this session. The host path does NOT need this asymmetry.
- **The DNS plan id is deterministic and constructible — not an open
  unknown.** `format!("{}-{:?}-plan", zone.as_str(), provider)`
  (`cloud/src/lib.rs:1236`) ⇒ for zone `criome`, provider Cloudflare the id
  is the literal `criome-Cloudflare-plan`. Lane B left it blank; it is now
  pinned, so legs 8–9 need no reply round-trip.
- **The Cloudflare RegisterAccount precondition is register-time, not
  apply-time, and is load-bearing — not "severity low."** `register_account`
  calls `verify_credential` → `EnvironmentCredentialSource::token` →
  `std::env::var(handle)` (`cloud/src/cloudflare.rs:51-56`) at register, so
  leg 6 fails immediately with a `CredentialHandleUnknown`-mapped rejection
  unless the handle's env var is present in the **daemon process**. The host
  providers do NOT verify at register, so this is a Cloudflare-only surprise.
- **lojix is build-on-target, not `nix copy`.** Report 71's `nix copy --to
  ssh-ng://` leg is now the no-op path (verdict D8 CONFIRMED); the real
  contact is `nix build --eval-store auto --store ssh-ng://root@<node>.<cluster>.criome
  <drv>^*` realizing in the node's own store, then a BootOnce activation.
- **The single load-bearing join is name-equality, not a wire contract.**
  The cloud `DesiredHostState.host_name` and the lojix `(cluster node)` pair
  must produce the **same** `<node>.<cluster>.criome` — that is the domain
  the A record publishes and the one `SshTarget::root_at_node` derives. The
  two daemons never talk; the operator hand-threads one node identity.
- **Both `goldragon`/`prometheus` worked examples in lanes A/1 are the WRONG
  node for the handoff.** `goldragon/datom.nota:59` declares `prometheus
  (LargeAiRouter …)` — an existing on-prem node — and `CloudNode` does not
  exist in the proposal at all. The first slice needs a fresh CloudNode node
  declared in the source proposal with `species CloudNode`, or the deploy
  materializes an on-prem profile.

## The corrected handoff, end to end

```mermaid
sequenceDiagram
  participant OP as operator (local on daemon hosts, li)
  participant CLOUD as cloud daemon (meta + ordinary sockets)
  participant CF as Cloudflare (cloud's own flarectl op)
  participant LJX as lojix daemon (owner + ordinary sockets)
  participant NODE as CloudNode (<node>.<cluster>.criome)

  Note over OP,CLOUD: PRECOND: daemon env carries DIGITALOCEAN_ACCESS_TOKEN<br/>AND the CF credential-handle env var (register-time getenv)

  rect rgb(235,245,255)
  Note over OP,CLOUD: CREATE (meta socket) — provision the node
  OP->>CLOUD: 1 RegisterAccount (DigitalOcean ...)
  OP->>CLOUD: 2 PrepareHostPlan ((DigitalOcean <node>.<cluster>.criome ... <CloudNode-snapshot-id> <ssh-key-name>))
  OP->>CLOUD: 3 ApprovePlan (<node>.<cluster>.criome-DigitalOcean-host-plan)
  OP->>CLOUD: 4 ApplyPlan  (<node>.<cluster>.criome-DigitalOcean-host-plan)
  CLOUD-->>OP: (PlanApplied (...host-plan))  — acceptance only, NO ip
  end

  rect rgb(235,255,235)
  Note over OP,CLOUD: OBSERVE (ordinary socket) — poll the create→observe seam
  loop until status==Running AND ipv4 != []
    OP->>CLOUD: 5 Observe (Servers (DigitalOcean None))
    CLOUD-->>OP: CloudHost (... ipv4 status)
  end
  end

  rect rgb(255,245,235)
  Note over OP,CF: DNS (meta socket) — publish A record via cloud's own CF op
  OP->>CLOUD: 6 RegisterAccount (Cloudflare criome-dns <cf-handle-env-var>)
  OP->>CLOUD: 7 SetPolicy (([(Cloudflare criome-dns [criome])]) [])  ← MANDATORY, was missing
  OP->>CLOUD: 8 PreparePlan ((Cloudflare criome [(<node>.<cluster>.criome AddressV4 [<ipv4>] Direct)] []))
  OP->>CLOUD: 9 ApprovePlan (criome-Cloudflare-plan)
  OP->>CLOUD: 10 ApplyPlan  (criome-Cloudflare-plan)
  CLOUD->>CF: flarectl create A <node>.<cluster>.criome -> <ipv4>
  OP->>CLOUD: 11 Observe (Records (Cloudflare criome))  — verify
  end

  rect rgb(245,235,255)
  Note over OP,LJX: DEPLOY (owner socket, local) — build-on-target, NOT nix copy
  OP->>LJX: 12 Deploy (System (<cluster> <node> FullOs <source> <flake> BootOnce None [] None))
  LJX-->>OP: (Deployed (<deployment-id> (<commit-seq> <state-digest>)))
  LJX->>NODE: nix build --eval-store auto --store ssh-ng://root@<node>.<cluster>.criome <drv>^*
  Note over LJX,NODE: realization in NODE's store; closure never transits daemon host;<br/>copy step = NO-OP for TargetStore
  LJX->>NODE: ssh systemd-run ... bootctl set-default OLD + set-oneshot NEW
  par terminal-state detection
    OP->>LJX: 13a Query (ByNode (<cluster> <node> (Some FullOs)))  — non-empty row = Activated
  and
    OP->>LJX: 13b WatchDeployments ((None (Some <cluster>) (Some <node>)))  — phase stream incl Failed
  end
  end
```

## 1 · The implementation-ready spec

### 1.1 Boot preconditions (both daemons, local)

The cloud and lojix daemons both run locally on the operator host; their
mutating sockets are uid/gid-gated (`0o600` meta / owner sockets), so every
mutating leg must originate on the host (lane A, `ARCHITECTURE.md:64-68`).

| Precond | Detail | Source |
|---|---|---|
| cloud daemon env carries `DIGITALOCEAN_ACCESS_TOKEN` | DO REST is in-process; the handle named in leg 1 must resolve in the daemon's env | lane B; `cloudflare.rs:51-56` (handle indirection); `flake.nix:96-99` wrapper |
| cloud daemon env carries the **CF credential-handle env var** | leg 6 `verify_credential` does `getenv(handle)` at **register** time, not apply | `cloud/src/lib.rs:1398-1402`; `cloudflare.rs:300-302,51-56` |
| cloud daemon built `--features digitalocean,cloudflare` | `apps.daemon` default is cloudflare-only (D6); use `apps.daemon-digitalocean` | `flake.nix:124,194-197`; `Cargo.toml:27` |
| `meta-lojix` built `--features nota-text` | default `[]` build rejects NOTA text, accepts only rkyv | `lojix/Cargo.toml:31`; `flake.nix:58` |
| the proposal `source` path is present + parseable **on the lojix daemon host** | `ProposalFile::load` / `ClusterProjection::from_source` are LOCAL reads; missing ⇒ `ProposalSourceUnreachable` | `lojix/src/schema_runtime.rs:2137-2138,3066-3068,460-466` |
| the `source` proposal **declares the target node with `species CloudNode`** | horizon materialization reads `source` on the daemon host and renders by species; absent ⇒ materialization fails before any build | `schema_runtime.rs:911,993-998,2825-2831` |
| the DNS A record `<node>.<cluster>.criome → <ipv4>` is published + propagated | lojix derives the IP through DNS at ssh time; never told it directly | lane A §3; `schema_runtime.rs:3350-3369` |

### 1.2 The ordered legs (copy-pasteable NOTA)

`<provider-account>`, `<ssh-key-name>`, `<CloudNode-snapshot-id>`,
`<server-type>`, `<ipv4>`, `<cluster>`, `<node>`, `<source>`, `<flake>` are
the deploy-time fillers. The example pins `<cluster>=goldragon`, a fresh
`<node>=<cloud-node-name>` (NOT `prometheus`), zone `criome`.

| # | Leg | Socket | NOTA (drive the hand-written tree, not `.schema`) |
|---|---|---|---|
| 1 | Register host account | meta | `meta-cloud "(RegisterAccount (DigitalOcean criome-test DIGITALOCEAN_ACCESS_TOKEN))"` |
| 2 | Prepare create plan | meta | `meta-cloud "(PrepareHostPlan ((DigitalOcean <node>.<cluster>.criome <server-type> <CloudNode-snapshot-id> <ssh-key-name>)))"` |
| 3 | Approve plan | meta | `meta-cloud "(ApprovePlan (<node>.<cluster>.criome-DigitalOcean-host-plan))"` |
| 4 | Apply plan [Create] | meta | `meta-cloud "(ApplyPlan (<node>.<cluster>.criome-DigitalOcean-host-plan))"` |
| 5 | Observe servers (poll) | ordinary | `cloud "(Observe (Servers (DigitalOcean None)))"` |
| 6 | Register DNS account | meta | `meta-cloud "(RegisterAccount (Cloudflare criome-dns <cf-handle-env-var>))"` |
| **7** | **Set zone policy (MANDATORY)** | meta | `meta-cloud "(SetPolicy (([(Cloudflare criome-dns [criome])]) []))"` |
| 8 | Prepare DNS A-record plan | meta | `meta-cloud "(PreparePlan ((Cloudflare criome [(<node>.<cluster>.criome AddressV4 [<ipv4>] Direct)] [])))"` |
| 9 | Approve DNS plan | meta | `meta-cloud "(ApprovePlan (criome-Cloudflare-plan))"` |
| 10 | Apply DNS plan | meta | `meta-cloud "(ApplyPlan (criome-Cloudflare-plan))"` |
| 11 | Observe records (verify) | ordinary | `cloud "(Observe (Records (Cloudflare criome)))"` |
| 12 | Deploy the node | owner (lojix) | `meta-lojix "(Deploy (System (<cluster> <node> FullOs <source> <flake> BootOnce None [] None)))"` |
| 13a | Confirm Activated | ordinary (lojix) | `lojix "(Query (ByNode (<cluster> <node> (Some FullOs))))"` |
| 13b | Watch phase stream | ordinary (lojix) | `lojix "(WatchDeployments ((None (Some <cluster>) (Some <node>))))"` |

Leg-7 field shape (confirmed this session): `SetPolicy(Policy)`, `Policy`
is the inline 2-field struct `(zones capabilities)`
(`meta-signal-cloud/src/lib.rs:99-104`); `zones` is a vector of `ZonePolicy`,
the inline 3-field `(provider account allowed_zones)`
(`meta-signal-cloud/src/lib.rs:91-96`); `allowed_zones` must contain the
**same** `DomainName` atom (`criome`) used as `zone` in leg 8. `capabilities`
stays `[]`.

### 1.3 The create→observe poll seam

`ApplyPlan[Create]` returns only `(PlanApplied (<plan-id>))` — no IP, no
status (`cloud/src/lib.rs:1613-1615,1672-1674`). Readiness lives in the
separately-observed 8-field `CloudHost` record (lane B):

- **poll predicate:** `status == Running` AND `ipv4 != []`.
- `status: HostStatus ∈ {Initializing, Running, Stopped, Deleting, Unknown}`
  (`signal-cloud/src/lib.rs:215-221`); fresh node reads `Initializing`.
- `ipv4: IpAddress(String)`; report 70 witnessed the empty value rendering
  as the bare empty atom `[]`. **One unconfirmed seam:** whether an empty
  `IpAddress` always emits exactly `[]` was taken from report 70's witness,
  not re-derived from the encoder this session — the poll comparison `ipv4 !=
  []` depends on it. Re-confirm by encoding an empty `IpAddress` and observing
  a fresh host once, before trusting the predicate for automation.
- post-destroy eventual-consistency can still list a node `Initializing`
  during the provider's read-lag window — a provider lag, not a daemon defect.

### 1.4 The deploy + terminal-state seam

`Deploy` reply `(Deployed (<deployment-id> (<commit-seq> <state-digest>)))`
is **acceptance only** (`meta-signal-lojix/schema/lib.schema:134`); the build
runs asynchronously. Two observe legs, with a real ambiguity to handle:

- **13a `Query (ByNode …)`** reads the live generation set, written only on
  activation success (`record_generation_activated`,
  `schema_runtime.rs:2222-2226`). A non-empty row for `(<cluster>, <node>,
  FullOs)` = reached Activated; for BootOnce the slot is `BootPending`, not
  `Current` (`schema_runtime.rs:2930`). The event log is NOT a phase probe —
  `ByEventLog` falls through to the live-set query (`schema_runtime.rs:2736`).
- **13b `WatchDeployments ((None (Some <cluster>) (Some <node>)))`** is the
  only reliable terminal-**failure** detector. The phase enum is `[Submitted
  Building Built Copying Activating Activated Failed]`
  (`signal-lojix/schema/lib.schema:140`); the watch payload is
  `DeploymentWatch { deployment (Optional DeploymentIdentifier) cluster
  (Optional ClusterName) node (Optional NodeName) }` — three optionals in
  declared order (`signal-lojix/schema/lib.schema:127`). **Why 13a alone is
  insufficient:** a `Failed` deploy never writes a Generation row, so an
  absent row is ambiguous between *still building a multi-tens-of-GB model
  closure on the target* and *Failed*. Only the `WatchDeployments` `Failed`
  phase event disambiguates. To watch by id instead, use `((Some <id>) None
  None)`. (NOTA shape reverse-engineered from the schema this session, not
  encoder-verified — confirm the Optional rendering before automating 13b.)

### 1.5 CloudNode snapshot preconditions (what the baked image must satisfy)

The `<CloudNode-snapshot-id>` in leg 2 is a numeric provider image id; the
image that mints it must satisfy ALL of (lane C + lane A §2 + critiques):

1. **systemd-boot UEFI NixOS** with `bootctl`, `/boot/loader/entries`, and a
   **mutable vfat ESP** — lojix activation runs `bootctl set-default/set-oneshot`
   and asserts the entry exists; lojix has no install path
   (`schema_runtime.rs:3616-3635,3674-3689`).
2. **root SSH login as a remote Nix store/builder over `ssh-ng` at BUILD
   time** — build-on-target realizes IN the node's store as root with
   `BatchMode=yes` (no interactive fallback) (`schema_runtime.rs:3386-3397,
   3991-4008`). This is strictly stronger than "copy destination."
3. **nix-daemon configured to accept the operator as a trusted-user /
   trusted-substituter** so `ssh-ng` store writes + signatures pass — the
   single hardest first-contact precondition, and it fails at the **build**
   step (opaque nix store error), not activation, if unmet.
4. **the operator's key in root's `authorized_keys`** so the very first
   lojix contact authenticates (lane C §2: deploy key via `mkAfter`;
   `test-substrate.nix:151-152` pattern), plus NSS + real root shell prebakes
   (`test-substrate.nix:130-141`) or sshd rejects root as "invalid user."
5. **serial console + growpart + cloud-init** (additive, gate-only) for
   headless boot observability, disk-fit, and first-boot SSH-key/hostname
   injection (lane C §2).
6. **the `<ssh-key-name>` in leg 2 already registered at the provider
   account** — DO resolves name→fingerprint at create (`digitalocean.rs:274`)
   and **silently drops unknown names** (keyless droplet); Hetzner 422-rejects
   an unknown name. Opposite failure modes on one precondition (verdict D14).
   **The two SSH surfaces must be reconciled:** the provider-injected
   `ssh_key_name` (cloud-init, first boot) and the baked root `deployKey`
   (image) should be the **same** key the operator's agent holds, or lojix's
   root ssh first-contact fails. Lane C leaves this unresolved; the image
   build must pin one key for both.

### 1.6 Genuinely blocked vs ready

**Ready now (code + NOTA exist, proven or source-confirmed):**

- The full cloud create→observe→DNS path over sockets — every leg's NOTA is
  encoder-verified (lanes A/B) or source-pinned here (legs 7, 9–10). Report
  70 proved register→prepare→approve→apply→observe→destroy live against DO
  droplet 578873541 over the real sockets (verdict D9).
- `image_name` plumbs end-to-end to `ServerSpec.image` unchanged — booting
  from a snapshot needs **no wire or daemon code change** (lane B/C).
- The lojix `Deploy` build-on-target path is the production default and works
  for any node that is SSH-reachable as a trusted `ssh-ng` store (lane A).

**Blocked (no code to start from):**

- **The CloudNode image itself (Spirit ad53 platform half).** `NodeSpecies`
  ends at `TestVm` (`horizon-rs/lib/src/species.rs:30`); no `CloudNode`
  variant, no CriomOS gate module, no image-format flake attribute anywhere
  (grep: 0 hits for `nixos-generators|image-format|CloudNode|qcow2` across
  horizon-rs + CriomOS) (verdict D7). Until this ships there is no
  `<CloudNode-snapshot-id>` to provision and the whole handoff cannot run
  end-to-end. This is the critical-path blocker.
- **First-contact node trust (precond 3 above).** Not a code gap in any repo
  — an image-build acceptance criterion that does not yet exist.

## 2 · The consolidated fix ledger

Folds the still-open verdicts (D1–D20; D21 dropped — verdict FIXED in
`d9df93f5`) and the blocking completeness gaps. Severities/lanes use the
adversarial **corrected** values where they differ from lane D's matrix.

### 2.1 `designer_now` — apply on `cloud-designer-intent-refresh` or in reports

| ID | Item | Sev | Where |
|---|---|---|---|
| D1 | `cloud-daemon` flake wrapper never injects the CF credential the daemon reads — add a third `--run` line sourcing `CLOUDFLARE_DNS_TOKEN` from `gopass cloudflare.com/token`, mirroring HCLOUD/DIGITALOCEAN | P1 | `cloud/flake.nix:96-99` (branch) |
| D3 | Wire two-tree drift + 3141-line `schema_bridge` straddle — replace hand-written `signal-cloud/src/lib.rs` types with `pub use crate::schema` re-exports, collapse the bridge | P1 | signal-cloud + cloud branch |
| D4 | meta schema redeclares signal-cloud types — adopt the `cloud/schema/sema.schema:7-32` cross-crate import block (`Provider signal-cloud:lib:Provider`), delete redeclarations | P2 | `meta-signal-cloud/schema/lib.schema:1,101-105` |
| D5 | Hetzner ships in no binary — decide add `packages.hetzner` now vs accept DO-lead deferral (hcp8 resolved intent; build gap is the residue) | P2 | `cloud/flake.nix:123-130` (+ psyche) |
| D6 | `apps.daemon`/`apps.default` are cloudflare-only — repoint at the compute-capable build, or confirm DNS-only-by-default is deliberate; default build returns `RequestUnsupported{CapabilityNotCompiled}` for host requests | P1 | `cloud/flake.nix:124,184-197` (+ psyche) |
| D7b | Write the CloudNode stance into `CriomOS/INTENT.md` + `horizon-rs/INTENT.md` (cloud-side already done in worktree INTENT.md:61-71); cross-repo discoverability is 1/3 done | P1 | CriomOS + horizon-rs INTENT |
| D8 | Report 71 §4 + 5-synthesis mermaids show `nix copy --to ssh-ng://` — replace with `nix build --eval-store auto --store ssh-ng://… ^*` realize-on-target + note copy is now a no-op | P2 | reports/cloud-designer/71 |
| D9 | `protocols/active-repositories.md:91` describes the daemon as "single EngineActor over a synchronous sema-engine Store" — rewrite to emitted `ActorMultiListenerDaemon` over `Arc<Store>` (still kameo but emitted/generic), cite report 70's live run | P2 | `/home/li/primary/protocols/active-repositories.md:91` |
| D10 | `cloud/ARCHITECTURE.md` "Actor Shape" (5 named actors none of which exist) + "must not block the ordinary listener" contradict the shipped single-engine blocking-IO daemon — reconcile or mark aspirational, tie to D2 | P2 | `cloud/ARCHITECTURE.md:3-5,32-41` |
| D11 | Config encoder is an `examples/` target with 3 hardcoded args, parses no NOTA — re-home to a deploy-stack bin consuming a NOTA `DaemonConfiguration` | P2 | `cloud/examples/write_config.rs:30,39-45` |
| D12 | sema-engine `SchemaRuntime`/`SchemaStore` pilot is unreachable from the daemon path (`build_runtime` builds `Arc<Store>`, not `SchemaStore`); decide cut-vs-promote, then reconcile ARCHITECTURE (D10) | P2 | `cloud/src/schema_daemon.rs:54,67`; `lib.rs:43-44` (+ psyche) |
| D13 | DO/Hetzner adapters are near-byte mirrors (own `trait Api`/`HttpApi`/`get`/`post`/`delete`/`decode_call`); invent a shared compute-provider REST client noun before `google-cloud = []` triples it; fold in D18 | P2 | `digitalocean.rs` + `hetzner.rs` |
| D15 | `CredentialHandle(String)` is an unvalidated wire-string used verbatim as a getenv name (now in BOTH cloudflare.rs:53 AND hetzner.rs:69-77); validate vs seal — a custody decision | P2 | `meta-signal-cloud/src/lib.rs:30-40` (+ psyche) |
| D16 | `ImageName(String)` accepts empty — but minting `ImageName::new("")` for Destroy plans is **deliberate** (`cloud/src/lib.rs:1313-1316`); a naive empty-reject `TryFrom` would BREAK it. Downgraded to P3 designer-polish (the real residue: garbage fails at the provider, not the wire edge) | P3 | `meta-signal-cloud/src/lib.rs:148-158` |
| D18 | Three near-identical `meta_reply_for_*_error` matchers, no `impl From<…Error> for RejectionReason` — orphan-rule-legal (provider Error types are local). Folds into D13 | P3 | `cloud/src/lib.rs:1530,1621,1680` |
| D19 | Cloudflare collapses every ureq class into `Error::RequestFailed` — split by Status (404→ZoneNotFound, 401/403→credential, 429→rate-limit) | P3 | `cloud/src/cloudflare.rs:147,168,189,203,213` |
| D20 | Three distinct `RejectionReason` enums share one name across the triad's schemas — distinct names or documented overload (no runtime collision) | P3 | signal/meta/sema schemas |
| C-1 | **(completeness gap, blocks impl)** Document the mandatory `SetPolicy` DNS leg (leg 7) in the spec/report — without it DNS ApplyPlan returns `ProviderNotConfigured` | P1 | this report (done) + any spec |
| C-2 | **(completeness gap)** Pin the DNS plan id `criome-Cloudflare-plan` (was "open"); pin register-time CF getenv as the leg-6 precond | P2 | this report (done) |

### 2.2 `operator_beads` — operator code

| ID | Item | Sev | Where |
|---|---|---|---|
| D2 | Blocking provider IO (`ureq`/`flarectl`, bare `.call()`, no per-call timeout) inside the async handler — move onto `spawn_blocking` + permit pool + bounded timeout + `DelegatedReply`, per `actor-systems.md:224-258` | P1 | `cloud/src/schema_daemon.rs:74-109`→`lib.rs:685-699`→providers |
| D7a | Build the CloudNode platform half: 3 horizon-rs edits (`NodeSpecies::CloudNode` + `TypeIs.cloud_node` arm + `BehavesAs.cloud_node` passthrough), 1 CriomOS gate module (`disks/cloud-node.nix`, additive: systemd-boot UEFI + mutable /boot + serial + growpart + cloud-init + root deploy key), 1 net-new image-format flake attr (qcow2 DO / raw Hetzner) — exercised in `CriomOS-test-cluster`, not the cloud repo | P1 | horizon-rs + CriomOS + CriomOS-test-cluster |
| D14 | Call `ensure_ssh_key` on the create path (or validate-and-reject loudly + uniformly across DO/Hetzner); today an unregistered `ssh_key_name` makes DO a silent keyless droplet and Hetzner a 422 | P2 | `cloud/src/lib.rs:1593-1607,1652-1666` |
| D17 | No committed test drives `ApplyPlan` / the full lifecycle **over the daemon sockets** (committed ApplyPlan tests are all in-process with mocked Api; `schema_daemon.rs` socket tests stop at meta registration → `CredentialHandleUnknown`). Add a committed socket-apply lifecycle test (CI-mocked + `#[ignore]` live variant) | P2 | `cloud/tests/` |

### 2.3 `sysop_beads` — deploy / OS / flake glue

| Item | Detail |
|---|---|
| First-snapshot mint, per provider | DO `POST /v2/images` by URL (off-cluster, no throwaway) ⇒ numeric id; Hetzner `hcloud-upload-image` (boot→rescue→dd→snapshot→delete) or `nixos-anywhere`+snapshot ⇒ numeric id. Both feed `image_name`. Re-confirm `hcloud`/`doctl` flag names + the DO custom-image cloud-init≥0.7.7 / ext3-4 constraints against live tool versions before scripting (lane C §3, UNVERIFIED). |
| Image-format mechanism | Pin `nixos-generators` input vs nixpkgs-native `system.build.images` against the live `github:LiGoldragon/nixpkgs?ref=main` fork (not checked out this session). |
| First-contact node trust | The baked CloudNode image must ship: operator key in root `authorized_keys`, nix-daemon `trusted-users` accepting the operator for `ssh-ng` store writes, systemd-boot UEFI + mutable `/boot`. These are image-build acceptance criteria, not code in any repo. `BatchMode=yes` means no interactive fallback — failures surface as opaque nix store errors at the **build** step. |
| Daemon env wiring (ties to D1) | Whatever launches the cloud daemon must export the registered credential-handle env vars (DO token + CF handle) into the daemon process before any RegisterAccount — the flake wrapper is the injection site. |
| Goldragon proposal | Add a CloudNode node entry to `goldragon/datom.nota` (or a dedicated source proposal) with `species CloudNode` + `MachineSpecies::Pod` + `Bootloader::Uefi`, present + parseable on the lojix daemon host at deploy time. |

## 3 · The depth-first FIRST SLICE to prove

**Slice: provision one DigitalOcean CloudNode, publish its A record, and
BootOnce-deploy a FullOs CriomOS generation onto it — end to end, on a branch,
one capability proven before generalizing.**

Per designer discipline (one capability proven on a branch at a time), the
ordering is forced by the critical-path blocker: the CloudNode image does not
exist, and nothing downstream can run without a `<CloudNode-snapshot-id>` and
a node that satisfies first-contact trust. So the slice is:

1. **Land the CloudNode species + image (operator-bead D7a + sysop mint).**
   The 3 horizon-rs edits + CriomOS gate + image-format attr, exercised in
   `CriomOS-test-cluster`. Mint one DO custom image ⇒ numeric id. This is the
   gate; everything else is already source-confirmed ready.
2. **Provision + observe (legs 1–5).** Proven shape from report 70; the only
   new fact is the snapshot id as `image_name`. Confirm the empty-`ipv4`
   renders `[]` for the poll predicate (§1.3).
3. **DNS publish (legs 6–11, with the mandatory SetPolicy leg 7).** First live
   CF-over-socket run — D1 (CF daemon env wiring) must be applied first or
   leg 6 fails at register-time getenv.
4. **Deploy (legs 12–13).** First build-on-target deploy onto a cloud node;
   prove 13b `WatchDeployments` surfaces `Activated` (and that 13a's row
   appears) before trusting the seam.

Prove on the `cloud-designer-intent-refresh` branch for the cloud-side doc
fixes (D1, D6, D8, D9, D10, INTENT stances) and operator/sysop beads for the
image. Do NOT widen to Hetzner (D5), the shared REST client (D13), or the
sema-pilot cut (D12) until this one node deploys.

## Open psyche questions

Restated in the structured return. The five that genuinely need the human:
provider-lead for the CloudNode image, whether to build the handoff tool now
vs hand-issue the legs, the first-proof path, whether to make the ledger
durable in Spirit now, and which SSH identity backs the first build-on-target
contact.
