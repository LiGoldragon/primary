# 704-1 — Research evidence digest (6 dimensions)

Condensed from the `criome-test-cluster-research` workflow (`wf_fbc72a4d-ab4`,
6 parallel readers). Each finding carries its `file:line` so the synthesis in
`2-design-and-plan.md` rests on verifiable ground, not assertion.

## Dimension 1 — criome, the propagation loop, the spirit gate

- **The spirit 1-of-1 gate is landed on `main` and fail-closed by
  construction.** Only `GateDecision::Authorized` releases fan-out;
  Unconfigured / Denied / Unreachable all hold the head back.
  `spirit/src/criome_gate.rs:141` (`ships()` matches only `Authorized`),
  `daemon.rs:163-169` (gate between commit and ship), `engine.rs:607`
  (`gate_and_ship_head`); landed `90875f2`, main HEAD `9ac01ae`. Behind the
  `mirror-shipper` cargo feature.
- **The gate mechanism.** On each working write spirit captures the post-commit
  head D from the versioned log (`engine.rs:610`, never `ShipOutcome.head`),
  projects `impl From<&LocalHeadCapture> for AuthorizedObjectReference`
  (`criome_gate.rs:71`), and calls the **local** criome over its per-user Unix
  socket; the synchronous `UnixStream` send is wrapped in `spawn_blocking`
  (`criome_gate.rs:210`) so the actor mailbox never blocks.
- **"criome cluster" = N criome daemons (one per Unix user / trust boundary)
  authorizing via BLS12-381 quorum** over the exact canonical request digest.
  `criome/ARCHITECTURE.md:84-149,412-442`.
- **1-of-1 (xhwa) needs NO criome quorum-code change** — criome's majority rule
  `required != 0 && required <= authorities && required > authorities/2`
  (`criome/src/language.rs:623`) already admits n=1,k=1; a 1-member root
  contract at deploy time is all that differs.
- **Cross-criome PEER transport does not exist in code.** The request/reply
  *shapes* exist (`CriomeRequest::RouteSignatureRequest` / `SubmitSignature` in
  signal-criome) and local actor routing exists; the missing piece is the
  daemon-to-daemon **network lane** — `criome/src/transport.rs` is
  `UnixStream`-only. (701 enabler E1.) **This narrowing matters: E1 is a
  transport lane, not a greenfield protocol.**
- **criome has ZERO networked tests** — no nixosTest, no microvm; flake checks
  are crane `cargoTest` + grep witnesses (`criome/flake.nix:80-164`). The
  daemon socket loop is serial-synchronous (`daemon.rs:159-160`).
- **The flagship test calls the engine directly.** `criome_gate_1of1.rs` spawns
  a real criome daemon over a real Unix socket and proves
  authorized-ships/denied-holds/unconfigured-holds — but **single-host,
  cross-thread**, and via `engine.gate_and_ship_head()` directly, not the
  spirit-daemon process. The mirror is in-process loopback TCP.
- **What a networked multi-node test must PROVE:** criome A aggregates real BLS
  signatures from criome B/C **over the wire** (true 2-of-3, not co-resident
  self-quorum p3td); the `AuthorizedObjectReference` is delivered across
  machines (E4); spirit B/C acquire **exactly head D** (fetch-by-digest E5, the
  live-loop race is structural across the net) or fail
  `MirrorRestoreHeadMismatch`; a denied/unreachable criome holds propagation
  end-to-end through real **processes**.

## Dimension 2 — CriomOS-test-cluster (the existing scaffold)

- **It is a Horizon→CriomOS regression fixture, not a criome+spirit harness.**
  Purpose: prove CriomOS consumes projected Horizon data without production
  facts leaking (synthetic `fieldlab`). `INTENT.md:5-11`.
- **criome is absent.** "criome" appears only as a DNS suffix
  (`fixtures/horizon/*.json:5`, `clusters/fieldlab.nota:210`,
  `mkDeployTest.nix:143`). **flake.lock inputs = criomos / horizon / lojix /
  persona-spirit / upgrade — NO `criome`, NO `signal-criome`, and the
  gate-bearing repo is `persona-spirit` (the OLD name), not the current
  `spirit`.** This input staleness is load-bearing for any gate test.
- **The reusable-generator pattern already exists and is proven.**
  `lib/mkVmTest.nix:14-20` — author writes only `{cluster, hostNode, vmNode,
  testScript}` → a `runNixOSTest` check; size/accel/address flow from the
  Horizon projection kept honest by `projections-match-fieldlab`. Auto-pickup:
  declaring a Pod-on-a-VmHost node yields a `vm-<node>` check with zero flake
  edits (`flake.nix:53-68,201-203`).
- **The only existing multi-node networked test** is `lojix-deploy-smoke`
  (`lib/mkDeployTest.nix:1-574`): a real lojix daemon on node A deploys node B
  over the runner's vlan, fully offline, with `<node>.<cluster>.criome` DNS via
  `networking.hosts`, ssh-ng host-key trust, silent-daemon-by-polling. **It
  solves every hard networked-VM problem a criome test hits** — but tests lojix
  deploy, not authorization.
- **spirit appears only as a single-node redb upgrade test** in an nspawn
  container with sshd disabled (`flake.nix:390`; `scripts/spirit-upgrade-test-runner`).

## Dimension 3 — CriomOS VM-test infra + prometheus

- **prometheus IS the designated VM-test host in production cluster data.**
  `goldragon/datom.nota:59-79` (GMKtec EVO-X2, 8 cores, 128 GB RAM, X86_64),
  `:97` carries `VmHost 169.254.100.0/22 Available (Some 4)`, `:156-159`
  declares the `vm-testing TestVm` Pod with `super_node prometheus`.
- **`vm-testing-prometheus-policy` settles the policy** (Spirit 2632): on
  prometheus `gpuPassthrough=false`, no VFIO (it's an AI node), and it publishes
  `vm-testing.criome.criome` → node IP. Isolated `evalModules` check.
  `CriomOS/checks/vm-testing-prometheus-policy/default.nix:122-147`.
- **The test-substrate profile bakes every live-run guest fix** (writable store,
  `require-sigs=false`, NSS/nscd, root shell, sshd+deploy key, horizon-derived
  `<node>.<cluster>.criome`, serial). Function of substrate → `{guestModule,
  vmTypeModule}`. `CriomOS/modules/nixos/test-substrate.nix:44-213`.
- **runNixOSTest and `-M microvm` cannot compose** — the driver's PCI
  virtconsole backdoor vs microvm's no-PCI bus; mkVmTest keeps the qemu-vm.nix
  substrate and applies only OS prebakes. `mkVmTest.nix:63-86`. A criome
  generator must inherit this resolution.
- **Image-exchange trust is already scoped to co-hosts** — additive
  `extra-trusted-public-keys` for exactly the peers sharing a TestVm guest.
  `CriomOS/checks/image-exchange-keys-scoped-to-co-hosts/default.nix`. The
  multi-host distribution primitive a real cluster builds on.

## Dimension 4 — cloud triad + DigitalOcean

- **DO provisioning is a working Phase-1 sync adapter.** `cloud/src/digitalocean.rs`
  (565 lines): `trait Api` (mock/`HttpApi` swap), create/observe/destroy
  droplets, ssh-key-name→fingerprint, DO v2 REST via blocking `ureq`. Full host
  lifecycle through real Store handlers (`tests/digitalocean.rs`); a real-API
  `#[ignore]` end-to-end (`tests/digitalocean_live.rs:27-108`, Drop-guard
  cleanup `:215`). Defaults `s-1vcpu-512mb-10gb` ($4/mo) / `nyc1` /
  `ubuntu-24-04-x64`.
- **A droplet does NOT become a NixOS criome+spirit host today.** Stock Ubuntu
  only; **no nixos-infect / nixos-anywhere / cloud-init / user_data path**. The
  meta contract `DesiredHostState`/`HostPlan` carries provider + host_name +
  server_type + image_name + ssh_key_name + intent — **no bring-up field**
  (`meta-signal-cloud/schema/lib.schema:75-91`).
- **Prior art biases the bring-up choice: `cloud/src/hetzner.rs:10` already names
  nixos-anywhere as the Phase-2 direction.** So the DO bring-up mechanism is
  *not* an open greenfield choice — nixos-anywhere is the repo's own lean.
- **Secrets are by-handle** — meta carries a `CredentialHandle` (env-var name);
  the flake injects `DIGITALOCEAN_ACCESS_TOKEN` from gopass
  (`digitalocean.rs:82-88`, `flake.nix`).
- **Teardown is idempotent** (404 = success; `destroy_host_by_name` resolves
  name→id). The keep-warm/billing-hour reuse pool (Spirit 6ks1) is **described
  for Hetzner, not built for anyone** (`INTENT.md:35-46`).

## Dimension 5 — horizon-rs + lojix

- **horizon-rs is a pure one-shot projection LIBRARY** — no daemon, no
  networking, no I/O, no actors, no tokio/rkyv. `ARCHITECTURE.md:1-13`,
  `DESIGN.md:561-573`. It cannot *run* a test. Its role is the typed
  cluster/node/machine MODEL: `NodeSpecies::TestVm`, `MachineSpecies::Pod`,
  `NodeService::VmHost{guest_subnet,kvm,maximum_guests}`, `super_node`/
  `super_nodes`, scoped `image_exchange_pub_keys` (`node.rs:565-571,608-611`,
  `machine.rs:69-86`).
- **lojix (the daemon) already has a typed, durable, push-based test control
  plane.** A meta `Test` op: `(Check [node])` / `(Run cluster nodes host mode)`
  → durable `TestRun` rows surviving restart, host/node selection validated
  against the real projection. `schema_runtime.rs:199-200,521-555`;
  `tests/test_op.rs:390-516` drives real `nix build … vm-<node>`. **This is the
  ready-made control surface — a criome cluster test should EXTEND it, not
  invent a rival orchestrator.**
- **lojix's charter already targets the exact networked goal** — "validated
  end-to-end against the full routed microVM with its own Criome domain and
  reachable IP, surviving SSH disconnect" (`INTENT.md:93-97`, Spirit se72) —
  but the **Live path is gated off** (`test_op.rs:350-381`
  `live_run_is_rejected_at_submit_never_a_faked_pass`).
- **lojix names the missing cluster-trust runtime** — horizon carries policy +
  fingerprints, clavifaber emits local public material, but the runtime that
  *distributes* it across the cluster does not exist (`lojix/ARCHITECTURE.md:116-119`).
  This is exactly the kind of thing a criome cluster would govern.
- Prompt attribution note: `substituter.rs` / `check_host_key_material.rs` are
  in **lojix-cli** (the deploy CLI), not lojix; there is no standalone
  Nix-substituter tool.

## Dimension 6 — testing discipline + the interface design space

- **"All tests in Nix" is literal and enforced** — `nix flake check` (pure) or
  `nix run .#<name>` (stateful); constraint→named-witness→Nix; positive+negative
  witness pair per constraint; `-test` binary suffix; no positive-grep proofs;
  VM checks only on authorized hosts. `skills/testing.md:9-17,69-73`,
  `skills/architectural-truth-tests.md:30-33,221`.
- **The only genuine two-kernel networked check is router's**
  `router-two-kernel-cross-host-transport` (branch `transport-two-kernel-e2e-138`)
  — and it uses an **FNV fixed-identity stub, not real criome BLS**
  (report `138/6:87-93`). The "biggest hidden fake": router's loose-String
  attestation does not match criome's `Attestation`/`ContentReference` shape; a
  `CriomeForwardVerifier` reconciliation must land before "real BLS over a real
  hop" is honest.
- **Report 136 already laid the rung ladder:** L0 loopback (landed) → L1
  two-kernel runNixOSTest with REAL criome → L2 Yggdrasil-routed → L3 two real
  hosts. Each rung kills one masquerade (loopback-as-remote, FNV-as-BLS,
  in-RAM-as-durable-replay). `136:128-141,79-95`.
- **The three substrates are already differentiated by INTENT records, and two
  conflict:** hermetic runNixOSTest = every-commit host-untouched (Spirit
  `7let`, high certainty); durable microvm TestVm = production-side dev target
  that touches prometheus's generation (Spirit `77ic`, medium). **`7let` vs
  `77ic` is an unresolved psyche reconciliation** about whether the durable node
  may exist on prometheus at all. `148:190-198,218-248`.
- **The durable substrate is written but undeployed** — blocked cluster-wide by
  a clavifaber/`nota-derive` build breakage + a malformed /128 route bug
  (`149:82-104`). Only the hermetic substrate is runnable today.
- **First real-host cluster decided:** prometheus + ouranos + zeus as the first
  2-of-3, tiger first expansion, balboa excluded.
  `703-engine-fixes/7-system-operator-brief.md:305-349`.
