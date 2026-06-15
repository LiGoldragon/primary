# Design proposal: a general, cluster-data-generated VM-testing interface + a readable OS/home-profile test suite

For psyche review. This is an architecture change — it specifies the model
change, the generator, the driving model, the test suite, and the
implementation order. It does **not** implement.

Grounding: `0-frame.md` (this directory); reports 47 (TestVm role design), 48
(microvm live e2e), 49 (UEFI activation e2e). Branch `horizon-test-vm` carries
Units A/B; the live mains carry the bespoke `/tmp` apparatus this generalizes.

## 0. The one-paragraph shape

A test is `mkVmTest { hostNode; vmNode; testScript; }`. The host and guest are
**named cluster nodes**, each with a horizon role; the generator projects both
through `horizon-cli`, builds the guest as a real CriomOS `nixosSystem` from its
projection, applies a **named test-substrate override profile**, boots it on the
**microvm machine type** under `runNixOSTest`, and runs the `testScript`. The
host's VM-hosting facts (tap subnet, KVM, capacity) come from a new
**`NodeService::VmHost`** datum on the host's projection, replacing the
`169.254.100+i.1` addressing currently invented in Nix. Nothing about a test is
cluster-specific: the author writes only `(hostNode, vmNode, assertions)`; every
substrate constraint is baked into the generator. A separate, single
`meta-lojix Deploy` smoke test keeps the real production deploy path under test
exactly once.

## 1. The horizon test-VM-HOST role — model change

### 1.1 The host role is a DERIVED CAPABILITY, not a species or facet

**Decision: do not add a host `NodeSpecies` and do not add a
`behavesAs.testVmHost` facet.** The host role is "I host >= 1 node whose
`machine.superNode == thisNode && behavesAs.testVm`" — a pure function of the
host's own projected `exNodes`. Unit B already implements exactly this
(`test-vm-host.nix:60-71`, fold over `exNodes`; `hasGuests` gate at `:173,175`).

Why not the alternatives:

- **A `NodeSpecies::TestVmHost`** is wrong because species is a node's *singular*
  cluster role (`species.rs:13-31`). The live host (`prometheus`/`atlas`) is a
  `Center`/router and must stay so; a node cannot be both `Center` and
  `TestVmHost`. Forcing a host to change species to host VMs breaks the
  "predictable role" intent into an either/or.
- **A `behavesAs.testVmHost` facet** is wrong because `BehavesAs::derive` takes
  only `(type_is, machine, io_disks_empty)` (`node.rs:190`) — it sees one node in
  isolation, never the cluster graph. "Do I host a guest?" is a cross-node
  question answerable only after every node is projected. `derive` runs per-node
  inside the projection loop *before* `exNodes` exists, so it structurally cannot
  compute it.
- **A derived capability** (recommended) is what Unit B shipped: the host's role
  *is* the set of guests it hosts, computed from data, with zero host-side
  authored state. This is the "predictable / generated-config" interface — the
  host config is a deterministic function of the projected horizon.

### 1.2 The gap: host-side VM-hosting data is invented in Nix, not projected

The capability is data-driven on the *guest* side but the *host* side is
fabricated:

| Host fact | Today | Problem |
|---|---|---|
| KVM availability | `haveMicrovm = inputs ? microvm` flake-input probe (`test-vm-host.nix:54`) | not a projected host fact; "can this host run accelerated guests" is unmodeled |
| guest tap subnet | hardcoded `169.254.${100+index}.1` (`:71`), `vmt${index}` (`:75`), `02:00:00:00:00:NN` MAC (`:82-88`) | pure Nix convention; not cluster-authored, not predictable across hosts |
| capacity ceiling | absent | the `exNodes` fold will happily over-subscribe host RAM/cores |

### 1.3 The model change: a `NodeService::VmHost` payload variant

Model the host's VM-hosting capability as a **`NodeService` payload variant** in
`horizon-rs/lib/src/proposal.rs`, sibling to the existing `NixBuilder { maximum_jobs }`
(`proposal.rs:107-110`). Services are exactly "extra capabilities a node opts
into, carried as per-node data, never inferred from name" — the right taxonomy.
Precedent: the *old* `vm-testing/default.nix` already carried host VM capability
as a `VmTesting` service payload, resolved "exactly like TailnetClient." Unit B
dropped that in favor of pure `exNodes`-derivation (correct for the guest fold)
but left the host's tap/KVM data unmodeled. **Restore a slim host capability
service for the tap subnet + KVM, keep Unit B's data-driven guest fold.**

Shape (matching the existing struct-variant + `kind()` + Nota codec discipline
in `proposal.rs:96-233` — every identifier a full English word per AGENTS.md):

```rust
/// Run cluster test VMs. The host's VM substrate (tap subnet, KVM,
/// capacity ceiling) is cluster-authored here rather than invented in
/// the Nix layer. Guests are still discovered by the exNodes fold
/// (superNode == thisNode && behavesAs.testVm); this carries only the
/// host's own capability data.
VmHost {
    /// CIDR the per-guest taps live in. Replaces the hardcoded
    /// 169.254.100+index.1 host-endpoint scheme. The generator derives
    /// each guest's host endpoint and route from this subnet + index.
    guest_subnet: TapSubnet,
    /// Hardware acceleration available (/dev/kvm). When false the
    /// generator emits a TCG (software) substrate.
    kvm: bool,
    /// Maximum concurrent guests this host advertises. Absent means no
    /// declared ceiling. The generator asserts the hosted set fits.
    maximum_guests: Option<u32>,
},
```

`TapSubnet` is a typed-domain-value (no bare `String`/CIDR) per the
typed-domain-values rule, parsed once at the proposal boundary. The host then
reads its subnet and KVM facts from `horizon.node.services` exactly as the guest
fold reads guest facts from `horizon.exNodes`.

### 1.4 Two supporting changes

- **Projection invariant**: any `Pod`/`TestVm` node's `super_node` must name an
  existing proposal node, even when `machine.arch` is explicit (today the
  existence check at `node.rs:582-584` is skipped when arch is `Some`). Reuse
  `Error::MissingSuperNode`. Makes the host→guest graph total — no guest can name
  a non-existent host.
- **Host-viewpoint golden test**: the current golden test
  (`lib/tests/horizon.rs:468-540`) asserts the *guest* projection but never
  projects from the host's viewpoint to assert the guest appears in
  `prometheus.exNodes` with `superNode == prometheus && behavesAs.testVm`. Add
  that assertion; it locks the predictable host interface.

### 1.5 The exact host-side data the generator reads (the "predictable interface")

| Source | Field | Status |
|---|---|---|
| host `horizon.node` | `name` (match `superNode`), `nodeIp` (host routing) | projected today |
| host `horizon.node.services` | `VmHost { guest_subnet, kvm, maximum_guests }` | **new** |
| host `horizon.exNodes.<guest>` | `machine.superNode`, `behavesAs.testVm`, `machine.{cores,ramGb,diskGb}`, `nodeIp`, `criomeDomainName` | projected today (no change) |

Net horizon change: **one `NodeService::VmHost` variant + one projection
invariant + one golden test.** Everything else already exists on the branch.

## 2. The predictable, nix-GENERATED VM-test interface — the heart

### 2.1 The generator signature

A flake-check generator living in CriomOS-test-cluster (`lib/mkVmTest.nix`),
extending the existing `fixtureSystem`/`configurationFor` builders
(`flake.nix:114-133`, `cluster-contracts.nix:43-58`) from static-attribute
assertions to a booted `testScript`:

```nix
mkVmTest = {
  cluster,                  # cluster name, e.g. "fieldlab"
  hostNode,                 # physical host node, e.g. "atlas" — provides VmHost data
  vmNode,                   # the TestVm guest node, e.g. "mercury"
  testScript,               # runNixOSTest python, reads like prose
  substrate ? "microvm",   # "microvm" (booting, default) | "uefi" (BootOnce, gated)
  extraGuestModules ? [ ],
} -> <a flake check derivation>
```

It internally:

1. **Projects both nodes** from the same cluster data — `horizon-cli --cluster
   ${cluster} --node ${vmNode}` (and `${hostNode}`), or reads the committed
   `fixtures/horizon/<node>.json`. This is the deterministic cluster-data →
   config-data step the psyche named.
2. **Builds the guest** as a real CriomOS `nixosSystem` with `specialArgs.horizon
   = <vmNode projection>` + `modules = [criomos] ++ extraGuestModules` — 100%
   horizon-data-generated, never a hand-stubbed `horizon` (the key improvement
   over `nspawn-role-policy`'s inline literal stub).
3. **Sizes the VM from cluster data** — `virtualisation.{cores,memorySize,diskSize}`
   from the guest's `machine.{cores,ramGb,diskGb}`; the host endpoint/route from
   the host's `VmHost.guest_subnet` + guest index. This is "cluster data from the
   vm host and the vm-node config" verbatim.
4. **Applies the test-substrate override profile** (§2.3) — the named writable
   store / require-sigs / NSS / shell / serial / label set, parameterized by
   `substrate`.
5. **Forces the microvm machine type** on `nodes.${vmNode}` so the lean profile
   boots (stock `runNixOSTest` defaults to q35, which hangs).
6. **Runs `testScript`** under `runNixOSTest`.

The author writes only `{ cluster, hostNode, vmNode, testScript }`. The role
(`TestVm` → `behavesAs.testVm`), the host edge (`super_node`), the tap subnet,
the substrate fixes — all flow from cluster data. **This is "cluster-data-generated,
not cluster-specific": the test is a function of the cluster model.**

### 2.2 Substrate constraints baked into the generator (not authored per-test)

All five learned-live constraints live in the generator, invisible to the test
author:

1. **microvm machine type** — `virtualisation.qemu` overridden to `-M microvm` /
   kernel direct-boot for the booting suite (reports 48/49: q35 hangs the lean
   userspace).
2. **Writable disk + writable store** — `boot.nixStoreMountOpts = ["rw"]` (the
   26.05 successor to `boot.readOnlyNixStore = false`) + a real writable ext4
   root; `runNixOSTest` gives writability for free, so this matters for the live
   path. Without it `nix copy` into the target fails (the S5 mode).
3. **Additive tap, host untouched** (`5hir5bnz`) — the host-emission path uses a
   `.network` matching ONLY `vmt<i>` by name with a `/32` link-local endpoint,
   `RequiredForOnline = no`, `autostart = false`; the *live* path uses a user
   network namespace (`unshare -rn`, no sudo). The hermetic `runNixOSTest` path
   sidesteps host networking entirely (its own test network). **Latent bug to
   bake around**: the `70-test-vm-vmt0` `.network` sorts *after* a center-non-router
   host's broad `10-main-eth` and gets DHCP-claimed — generator emits a `05-`
   prefix when the host is a plain center; inert on a router host like atlas.
4. **Horizon-derived address** — `networking.hosts` resolves the guest's
   `criomeDomainName` to the *guest's* `nodeIp` (not the host's); lojix targets
   `root@<vmNode>.<cluster>.criome` with zero VM special-casing.
5. **Lean-guest pre-bakes** — nscd re-enabled + `passwd/group/shadow` pinned to
   `files` (else sshd rejects root as "invalid user"); an absolute
   `${bashInteractive}/bin/bash` root shell; `nix.settings.require-sigs = false`
   as a *substrate* property (the daemon's `nix copy` stays production-identical);
   serial `console=ttyS0`; ESP/root labels (`nixos`/`ESP`) aligned to what
   `switch-to-configuration` expects.

### 2.3 The named test-substrate override profile (highest-leverage generalization)

Promote the per-run `/tmp` override sets — independently re-derived in *both*
live runs (reports 48 §fixes 1-5, 49 §step 2) — into a single generated module
`modules/nixos/test-substrate.nix` (or a CriomOS-test-cluster `lib` module),
parameterized by `substrate ∈ {microvm, uefi}`:

| Override | microvm | uefi | Source |
|---|---|---|---|
| `boot.nixStoreMountOpts = ["rw"]` | yes | yes | writable store, S5 fix |
| `nix.settings.require-sigs = false` | yes | yes | unsigned local closure |
| nscd on + NSS `files` pin | yes | yes | sshd "invalid user" fix |
| absolute root shell | yes | yes | login-shell-exists fix |
| `console=ttyS0` serial | yes | yes | observability |
| ESP/root label alignment | n/a | yes | `switch-to-configuration` |
| `-M microvm` direct boot | yes | no | userspace comes up |
| q35 + OVMF + ESP | no | yes | BootOnce possible |

The difference between "a lean CriomOS guest" and "a lean CriomOS guest that
boots and accepts a deploy" *is* this profile. It must be generated, named, and
substrate-parameterized — never re-typed into `/tmp`.

### 2.4 Why the generator extends, not replaces, Unit B

`test-vm-host.nix:60-185` already computes tap/MAC/endpoint/disk/domain from
cluster data correctly. The gap is that it emits a *networkd host tap* + a
*microvm.vms declaration* — the host-deploy path. The generator adds the
**runner + base-image + user-namespace network + credentials + bring-up/teardown**
as buildable/runnable attributes for the hermetic and live test paths. Both
consume the same projected horizon JSON; the difference is only whether the
microvm boots inside the `runNixOSTest` sandbox (hermetic) or on the real host
(fidelity).

## 3. The driving model — recommendation

**Recommend: split by what each model proves.**

### 3.1 Pure-nix microvm VM tests for the OS/home-profile suite (the bulk)

"Does role R + profile P produce a correct, working OS?" is a statement about the
*built config*, fully determined by cluster data. It needs no daemon, no SSH, no
tap, no live host — it runs hermetically as a flake `check` under QEMU
(microvm machine type). This is the natural *runtime* extension of every existing
CriomOS check (all of which are static-eval policy assertions today; **zero**
`nixosTest`/`runNixOSTest` exists in the stack yet). Same `configurationFor
horizon modules` builder, but boot it and assert behavior. This is where the
psyche's "bunch of easy-to-read tests for complex OS and home-profile testing"
lives.

### 3.2 One thin lojix-deploy smoke test for the production path (exactly once)

"Does the real deploy path work — build → copy → activate → BootOnce → survive
disconnect against a real writable-disk node?" is fundamentally heavier (running
daemon, additive tap, SSH-reachable address, writable disk, UEFI substrate). It
proves the *machinery*, not the *content* of any role/profile — re-proving it per
role is wasteful and brittle. It is also where the highest-value bug was caught
(the `.drv^*` fix). So: **one** representative node, run end-to-end via
`meta-lojix Deploy … build_attribute=<fixture-toplevel-attr>` against
`root@<node>.<cluster>.criome`, asserting the durable terminal job record via the
ordinary `lojix Query` (`Selection::ByNode`). `SystemAction` selects depth — a CI
smoke can stop at `Build`/`Boot`; full fidelity uses `BootOnce`.

### 3.3 The unresolved blocker the proposal surfaces (does not hide)

The lean CriomOS profile boots userspace on `-M microvm` but **cannot do UEFI
BootOnce** (no ESP); it **does BootOnce on q35+OVMF** but **hangs userspace**. So
the full-fidelity lojix smoke test's substrate is **blocked on the open Unit-B
q35-userspace hardening**, OR scoped to assert through generation-activation
(proven on microvm in report 48) rather than a booted gen-2 userspace. The
hermetic OS/home suite (§3.1) is unaffected — it uses microvm, where userspace
works.

## 4. The readable test suite

### 4.1 The easy-to-read shape

The author writes a declarative spec; the substrate is baked in:

```
TestSpec:
  cluster   = fieldlab
  hostNode  = atlas              ;; carries VmHost { guest_subnet, kvm }
  vmNode    = mercury            ;; declared TestVm in clusters/fieldlab.nota
  substrate = microvm            ;; baked constraint, not authored
  testScript:
    mercury.wait_for_unit("sshd.service")
    mercury.succeed("test -e /etc/horizon.json")
    mercury.succeed("findmnt -no OPTIONS /nix/store | grep -qw rw")
```

The `testScript` reads like prose. The node is declared once in
`clusters/fieldlab.nota`; every test references it by name and cluster data flows
through `horizon-cli` → JSON → `nixosSystem` automatically. Static role/profile
*contract* properties (packages present, services enabled, a domain resolves)
stay in the cheaper eval-check layer; the booted suite proves *behavioral*
properties (sshd answers, the home profile activates, a service runs).

### 4.2 Candidate OS-config tests (from the profiles grounding)

Each is a `(role, size, model)` tuple a TestVm-style node requests; the booted
guest asserts live state against the cited ground-truth module.

| ID | Role / size | Ground truth | Key assertions |
|---|---|---|---|
| **T1** Baseline smoke | TestVm / min | `normalize.nix` | sshd active + `PasswordAuthentication no`; `/bin/sh` → mksh; `/etc/horizon.json` mode 0600; `ssh_known_hosts` carries each exNode domain; writable `/nix/store` (S5 absent) |
| **T2** Edge desktop | Edge / min | `edge/default.nix` | greetd/regreet greeter + niri session package; `xdg.portal` running, gtk backend + gnome-keyring Secret portal; gnome-keyring/gvfs/polkit/dbus active; keyd alt/meta swap; pipewire+wireplumber with `10-criomos-desktop-audio` |
| **T3** Router | Router / min | `router/default.nix` | `hostapd` + `kea-dhcp4-server` active; nftables ruleset has input-drop + WAN masquerade; `br-lan` bridge with gateway `/24`; `ip_forward=1`; router net units `restartIfChanged=false` (recovery guarantee) |
| **T4** Large-AI | LargeAi / large | `llm.nix` | `${node}-llama-router.service` present + `wantedBy multi-user.target`; firewall opens serverPort; `llama` user/group with video+render; `/var/lib/llama` tmpfile; sops secret unit wired (assert *configured*, not a live inference call) |
| **T5** Center / nspawn host | Center / large | `nspawn.nix` (+ `metal` EPP) | `criomos-nspawn` on PATH; `boot.enableContainers`; `container@` template + `nixos-container`; `%nixdev` NOPASSWD; `systemd-machined` active |
| **T6** Metal model quirk | Edge / ThinkPadT14Gen2Intel | `metal/default.nix` | `disable-spurious-wakeups.service` present; `mhi*`/`intel_ipu6` modprobe blacklist; `i8042.nomux=1` kernelParam. Caveat: VM asserts *declarative emissions* only, not physical effect — weaker than T1-T5 |

### 4.3 Candidate home-profile tests (assert as the deployed test user)

The home-profile angle needs a sibling guest that **keeps** the home profile —
`test-vm-guest.nix` currently *suppresses* `home-manager.users` for leanness
(`:44-51`). A home-profile test VM gates on `deployment.includeHome = true` (the
existing toggle, `criomos.nix`/guest gate `:33`), so the desktop/home surface can
boot and be asserted.

| ID | Profile | Ground truth | Key assertions |
|---|---|---|---|
| **H1** Base home | size.min | `profiles/min/default.nix` | `git config` user email/name, `pull.rebase=true`, `beads.role=maintainer`; jujutsu `editor=false` (abort-not-block) + difft; zsh dotDir; direnv+nix-direnv; dev binaries on PATH (rust, nil, jj, lojix-cli); mimeApps browser=chromium |
| **H2** Spirit daemon (highest-value, INTENT-backed) | size.min | `profiles/min/spirit.nix` + `checks/spirit-deployment` | `spirit-daemon.service` + `agent-daemon.service` user units; `spirit-daemon` After/Wants `agent-daemon`; build-time rkyv config archive non-empty + ExecStart points at it; `spirit`/`meta-spirit`/`agent` wrappers on PATH; **runtime escalation**: start the user service, assert the socket appears |
| **H3** Niri + rescue terminal | size.min | `profiles/min/niri.nix`, `ui-priority.nix` | niri config has rescue-terminal keybind; `criomos-rescue-terminal` is a `systemd-run --scope` with `MemoryHigh=2G`/`CPUWeight=1000`; `criomos-lock-{session,listener}` user services; UI-priority units protect niri/portals/pipewire (component-scoped) |
| **H4** Dictation (INTENT-backed) | size.min | `profiles/min/dictation.nix` | `whisrs.service` user unit bound declaratively to the dji PipeWire source (no polling); noctalia level widget + niri dictation keybind configured |
| **H5** Medium delta | size.medium | `profiles/med/default.nix` | tokenized `gh`/`hub` wrappers (resolve via gopass); graphical apps (element, telegram, cameractrls); starship notify. **Ladder assertion**: an H5 guest must still satisfy every H1 assertion (monotone inclusion) |
| **H6** Max profile | size.max, isMultimediaDev | `profiles/max/default.nix` | obs-studio + plugin set; chromium wrapped via hexis with remote-debugging once-seed; gimp/krita/calibre present. Heaviest closure — occasional, not the fast suite |

### 4.4 Recommended coverage

- **Fast core (every run)**: T1, T2, T3, H1, H2 — the genuinely complex,
  service-bearing, INTENT-anchored surfaces, each reading cleanly ("router →
  hostapd+kea+nftables up; edge → greeter+portal+keyring up; spirit → both
  daemons up from the rkyv archive").
- **Second tier**: T4, T5, H3, H4.
- **Occasional / model-specific**: T6, H5, H6.

The size-ladder monotonicity (H1 ⊂ H5 ⊂ H6) gives a natural "compose, don't
duplicate" assertion structure.

## 5. Implementation surfaces + order

All designer work on `~/wt` feature branches; operator integrates main and
rebases. Code repos under `/git/github.com/LiGoldragon`. Build on
`horizon-test-vm` (Units A/B) — do not fork from main.

| Unit | Repo | Branch (from) | Deliverable |
|---|---|---|---|
| **C1** Host capability datum | horizon-rs | `horizon-test-vm` | `NodeService::VmHost { guest_subnet, kvm, maximum_guests }` (+ `kind()`, Nota codec, `TapSubnet` typed value) in `proposal.rs`; projection invariant (`Pod` superNode exists, reuse `Error::MissingSuperNode`); host-viewpoint golden test in `lib/tests/horizon.rs` |
| **C2** Host module reads projected data | CriomOS | `horizon-test-vm` | `test-vm-host.nix` reads `guest_subnet`/`kvm` from `horizon.node.services` instead of hardcoding `169.254.100+i.1`/input-probe; `05-` prefix on plain-center hosts |
| **C3** Test-substrate override profile | CriomOS | `horizon-test-vm` | `modules/nixos/test-substrate.nix` — the named writable-store/require-sigs/NSS/shell/serial/label set, parameterized by `substrate ∈ {microvm, uefi}` (§2.3); a home-keeping guest variant gated on `includeHome` |
| **C4** The `mkVmTest` generator | CriomOS-test-cluster | `vm-test-generator` (from main; consumes C1-C3 via flake inputs) | `lib/mkVmTest.nix` (§2.1); the first `runNixOSTest` in the stack, forced microvm; extends `fixtureSystem`/`configurationFor` from attr-asserts to booted `testScript` |
| **C5** The readable suite | CriomOS-test-cluster | `vm-test-generator` | T1-T3 + H1-H2 (fast core) wired as flake `checks`, each a `mkVmTest { … }` declarative spec; second/occasional tiers follow |
| **C6** lojix-deploy smoke test | CriomOS-test-cluster | `vm-test-generator` | one `meta-lojix Deploy … build_attribute=…` against `root@<node>.<cluster>.criome` + `lojix Query` assertion; substrate gated on the q35-userspace decision (§6) |

**Order rationale**: C1 is the model root (everything reads its data). C2/C3 are
CriomOS-side and independent of each other once C1 lands. C4 is the generator and
depends on C1-C3 through flake inputs. C5 is pure authoring on C4. C6 is the live
path and is the one unit blocked on an open decision. C1-C5 deliver the full
hermetic suite with no production dependency.

## 6. Open decisions needing psyche input

1. **Full-fidelity substrate (the central tension).** The lean profile boots
   userspace on microvm but can't do UEFI BootOnce; it does BootOnce on q35+OVMF
   but hangs userspace. Three options for the lojix smoke test (C6): (a) **harden
   the lean profile** to come up on q35+OVMF (a real Unit-B engineering effort,
   unblocks full BootOnce fidelity); (b) **scope the smoke test to
   generation-activation** on microvm (proven in report 48; no booted gen-2
   userspace assertion); (c) **defer C6** entirely and ship only the hermetic
   suite. Recommendation absent a directive: ship C1-C5 now, scope C6 to (b)
   until (a) is funded.

2. **`TapSubnet` granularity.** Should `VmHost.guest_subnet` be a single CIDR the
   generator slices per-guest-index, or an explicit per-guest endpoint map? A
   single CIDR is the more predictable, less-authored shape (recommended); an
   explicit map allows non-contiguous addressing if a host needs it.

3. **Where the generator and suite live.** Recommended: generator + suite in
   **CriomOS-test-cluster** (it already owns the projection→config pipeline and
   the fixtures), consuming CriomOS modules via flake input. Alternative: the
   generator in CriomOS itself (closer to the modules, but couples the OS repo to
   a test framework). Recommend CriomOS-test-cluster.

4. **Home-profile-keeping guest variant — facet or flag?** A home-profile test VM
   needs `home-manager.users` kept (the lean guest suppresses it). Option (a) a
   new `behavesAs` facet (e.g. a `homeTestVm` species variant); option (b) reuse
   the existing `deployment.includeHome = true` flag on an otherwise-TestVm node.
   Recommendation: (b) — `includeHome` already exists and toggles exactly this;
   no new species needed.

5. **`runNixOSTest` microvm override maintenance.** Forcing the microvm machine
   type onto a `runNixOSTest` node is a non-stock override of the python driver's
   default q35 boot. Acceptable risk, or should the suite instead drive
   microvm.nix's own runner with a thin assertion wrapper? Recommend the
   `runNixOSTest` override (its `wait_for_unit`/`succeed` orchestration is what
   makes tests "easy to read"); flag it as the one place the generator tracks
   upstream nixpkgs.
