# 47 · Horizon test-VM infrastructure — design proposal (psyche review)

Synthesis of the grounding fan-out (`1-horizon-model.md`,
`2-criomos-derivation.md`, `3-host-lifecycle-lojix.md`) into one concrete,
reviewable proposal. This proposes an architecture change to the horizon
model; nothing here is implemented. Captured intent in `0-frame-and-intent.md`:
integrated, not always running, a proper horizon role, a node declared AS a
test VM naming its host/location/resources.

## 0. Design stance

The grounding established that the model already carries most of the machinery:
a Pod-on-host relation (`Machine.super_node`), a derived `behavesAs.virtualMachine`
facet, per-node routed Criome domains, and an on-demand host primitive
(`criomos-nspawn start/stop`). The genuinely-new pieces are small and bounded:

1. one `NodeSpecies` variant (`TestVm`),
2. one optional `Machine` field (`location`),
3. one optional `Machine` field (`disk_gb`) for VM disk sizing,
4. one derived `behavesAs` facet (`testVm`),
5. a host-side guest-config upgrade in CriomOS (turn the inline stub into a
   real deployable CriomOS guest),
6. on-demand wiring (manual `criomos-nspawn` trigger now; an optional lojix
   meta op later).

The whole design is "fill the three gaps the grounding named, reuse the rest."
We do NOT invent a new node-on-host relation, a new address scheme, or a new
deploy path — all three already work for the live `dune` Pod.

## 1. Test-VM role/species in horizon

### Where it goes in the taxonomy

"Role/species" splits across two enums (`horizon-rs/lib/src/species.rs`):
`NodeSpecies` (cluster role) and `MachineSpecies` (`Metal | Pod` substrate).
The psyche's "proper role created in horizon" is a **new `NodeSpecies`
variant** — the cluster-role axis — while the substrate stays
`MachineSpecies::Pod` so `behavesAs.virtualMachine` keeps deriving true.

```
pub enum NodeSpecies {
    Center, LargeAi, LargeAiRouter, Hybrid, Edge, EdgeTesting,
    MediaBroadcast, Router, RouterTesting,
    TestVm,   // NEW — on-demand test virtual machine
}
```

`TestVm` is a distinct role, not a reuse of `EdgeTesting`. `EdgeTesting` means
"a next-gen edge node" (it derives `edge`, `next_gen`, `low_power`); it is a
class of real hardware, orthogonal to "this is an ephemeral VM." Conflating
them would make every test VM also derive the full edge desktop stack.

### Threading it through the projection

The variant must be added in three coupled places in `horizon-rs/lib/src/node.rs`
(all closed `match`/struct so the compiler enforces completeness):

- `TypeIs` struct + `TypeIs::from_species` (`node.rs:152-180`): add a
  `test_vm: bool` field and `test_vm: matches!(s, NodeSpecies::TestVm)`.
- `BehavesAs` struct + `BehavesAs::derive` (`node.rs:140-204`): add a
  `test_vm: bool` facet. Derivation:
  `let test_vm = type_is.test_vm;` and importantly
  `let iso = !virtual_machine && io_disks_empty;` stays as-is (a TestVm is a
  Pod, so `iso` is already false for it — good, it is NOT an installer image).
  A TestVm should derive a **minimal** profile: it is NOT `edge`, NOT `center`,
  NOT `router`. It carries only `virtual_machine = true` (from Pod) and the new
  `test_vm = true`. This keeps the guest config lean.

### What it means semantically

`behavesAs.testVm` is the facet CriomOS gates the **guest's own** lean config
on. `behavesAs.virtualMachine` (already derived from Pod) is what the **host**
gates the `microvm`/`nspawn` substrate on. The two facets do different jobs:
`testVm` shapes the guest; `virtualMachine` flags "this node runs on a host."

## 2. A node declared AS a test VM (the datom shape)

The node-on-host relation is the existing `Pod` machine shape — `super_node`
names the host, `super_user` names the owning user. We add `location` and an
optional `disk_gb`. Using the live `dune` declaration
(`CriomOS-test-cluster/clusters/fieldlab.nota:80-104`) as the template, a test
VM `mercury` hosted on physical node `atlas` in datacenter `home-lab`:

```nota
mercury (TestVm
  Min                         ;; size: Magnitude (lean)
  Max                         ;; trust
  (Pod                        ;; MachineSpecies::Pod — substrate = VM
    (Some X86_64)             ;; arch (could be None → inherit from atlas)
    4                         ;; cores
    None                      ;; model
    None                      ;; mother_board
    (Some atlas)              ;; super_node — THE HOST (physical node)
    (Some aria)               ;; super_user — owner on the host
    None                      ;; chip_gen
    (Some 8)                  ;; ram_gb — 8 GiB
    (Some 40)                 ;; disk_gb — 40 GiB  [NEW FIELD]
    (Some [home-lab]))        ;; location          [NEW FIELD]
  (Qwerty
    Uefi
    {
      [/] ([/dev/vda] Ext4 [])   ;; a real rooted disk, not tmpfs
    }
    [])
  ([AAAAC3NzaC1lZDI1NTE5...MercurySshPublicKey])  ;; pub_keys (ssh required)
  []                          ;; link_local_ips
  (Some [10.77.0.7/24])       ;; node_ip — the GUEST's own routed CIDR
  None False False []         ;; wireguard / nordvpn / wifi_cert / proxies
  False False None            ;; wants_printing / hw_video / router_interfaces
  (Some True)                 ;; online
  [(TailnetClient)])          ;; services
```

Reading it: `mercury` is a `TestVm`-role node, substrate `Pod`, 4 cores / 8 GiB
/ 40 GiB, hosted on `atlas`, owned by `aria`, located in `home-lab`, with its
own routed address `10.77.0.7/24` and domain `mercury.fieldlab.criome`.

Key points:
- **Host** = `Machine.super_node = atlas` (existing field, existing
  projection-walk in `resolve_arch`, `node.rs:549-575`).
- **Resources** = `Machine.cores` (existing), `Machine.ram_gb` (existing),
  `Machine.disk_gb` (NEW — VMs need a declared virtual-disk size; physical
  nodes get disk from partition layout, but a VM's disk is allocated at
  create time, so its size is genuinely cluster-authored and non-derivable).
- **Location** = `Machine.location` (NEW — see §3).
- The guest declares a **real `/` on a real disk** (`Ext4` on `/dev/vda`), not
  the `tmpfs` the `dune` fixture uses — because `mercury` must be a bootable,
  persistent, deployable target, not a throwaway fixture.

## 3. horizon-rs model + projection changes

### `Machine` gains two optional fields (positional-safe, at struct end)

`horizon-rs/lib/src/machine.rs`, appended after `ram_gb` per the
existing positional-NOTA convention (`machine.rs:29-30,36-37`):

```rust
/// Virtual disk size in gibibytes for a Pod (VM) node. None for a
/// Metal node (disk comes from the partition layout in `Io`) or a Pod
/// whose host pre-provisions the disk. Cluster-authored because a VM's
/// root disk is allocated at create time and is not derivable from
/// anything else. MUST stay near the end for positional nota parsing.
#[serde(default)]
pub disk_gb: Option<u32>,

/// Physical placement of this machine — a free site/datacenter/rack
/// label (e.g. `home-lab`, `hetzner-fsn1`). Cluster-authored,
/// variable, and non-derivable, so it passes the proposal-boundary
/// test (`horizon-rs/INTENT.md:20-27`). Optional; None means
/// unspecified. For a Pod, None MAY be resolved to the host's location
/// at projection time (open question §7). MUST stay near the end.
#[serde(default)]
pub location: Option<Location>,
```

`Location` is a new transparent newtype in `machine.rs` (mirrors `ModelName`):

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, NotaDecode, NotaEncode)]
#[serde(transparent)]
pub struct Location(pub(crate) String);
```

Both fields flow through projection automatically: `Node` carries the full
`machine: Machine` (`node.rs:35`, set at `:404-405`), so `super_node`,
`location`, `disk_gb` all survive into the projected `Node` with no extra
plumbing — exactly as `super_node` already does for `dune`.

### Species threading (per §1)

`species.rs`: add `NodeSpecies::TestVm`. `node.rs`: add `test_vm` to `TypeIs`
+ `from_species`, and `test_vm` to `BehavesAs` + `derive`. These are the only
required edits; the projection entry point `ClusterProposal::project`
(`horizon.rs:31-145`) needs no change — a TestVm node validates, projects,
gets its domain, and lands in the per-node Horizon like any node.

### Projection self-consistency

Optionally add a projection validation: a `TestVm`/`Pod` node MUST name a
`super_node` that exists in the proposal map (reuse the existing
`Error::MissingSuperNode`, already raised by `resolve_arch` at `node.rs:564`).
This is a tightening, not new error machinery.

## 4. What CriomOS emits

Two horizon-projected facts produce two distinct emissions (the grounding's
"net shape," `2-criomos-derivation.md` §3).

### (a) On the HOST (`atlas` — the named `super_node`)

The host carries no special service flag in the cleanest design: it derives
"I host VMs" from the projected cluster. Concretely, extend the existing
`vm-testing` host module (`modules/nixos/vm-testing/default.nix`) so that for
each projected `ex_node` whose `machine.superNode == thisNode` and whose
`behavesAs.testVm` is true, the host emits:

1. A `microvm.vms.<guestName>` (or nspawn machine) declaration with
   `vcpu`/`mem`/disk from the guest's `machine.cores`/`ram_gb`/`disk_gb`.
2. A **fully set-up tap**: host tap device + the guest's own
   `node_ip`/route, so the guest is reachable on its own address (today the
   `dune`-style tap has only an `id`/`mac`, no host-side setup — the gap named
   at `vm-testing/default.nix:170-176`).
3. A `networking.hosts` entry resolving the **guest's** criome domain
   (`<guest>.<cluster>.criome`) to the **guest's** IP — not the host's IP as
   the current module does (`:140-142`).
4. **Non-autostart** guest unit — the VM is created/installed but does not
   start at boot, so "launched to test, stopped after" is the default.

The `nspawn` path is the simplest on-demand substrate (it is imperative and
does not auto-start; `nspawn.nix`), gated to `size.large && behavesAs.center`
hosts — i.e. `atlas`-class. The `microvm` path gives a truer routed VM but
needs the non-autostart wiring added. Both are viable; **proposal picks nspawn
for v1** (least new machinery, on-demand is the default behavior) with microvm
as a follow-up for full hardware fidelity. (Open question §7.)

### (b) On the GUEST (`mercury` — the initial deployable config)

The guest is itself a declared cluster node, so CriomOS derives its config from
its own projected horizon. With `behavesAs.testVm = true` and a real
`/` disk, the guest must emit a real, bootable, deployable CriomOS image — NOT
the 7-line inline stub. The grounding (`2`, §3) names exactly what it needs,
all of which the standard module tree already emits for any node:

- `services.openssh.enable = true`, keys-only (`normalize.nix:171-176`).
- `users.users.root.openssh.authorizedKeys.keys = adminSshPubKeys` (the
  operator key — `users.nix:45-49`), so lojix can SSH-deploy into it.
- `networking.hosts` / `ssh_known_hosts` from its own
  `nodeIp`/`criomeDomainName` (`network/default.nix`, `normalize.nix:36-43`).
- A `behavesAs.testVm` gate that suppresses the heavy desktop/edge stack so the
  guest stays minimal (it already derives NOT-edge/NOT-center per §1).

The key change is purely "make the guest a real node": because `mercury` is a
declared proposal node with its own pub_keys, node_ip, and a real root disk,
the existing CriomOS module tree builds it as a genuine deploy target. The
`behavesAs.testVm` facet only trims it down. **No new guest-config machinery —
the guest just stops being a special inline stub and becomes an ordinary node.**

## 5. On-demand lifecycle (up/down + who triggers)

The host primitive already exists: `criomos-nspawn` with verbs
`create`/`update`/`start`/`stop`/`terminate`/`remove` (`nspawn.nix:29-37`),
runnable NOPASSWD by the `nixdev` group on the host. A created machine does NOT
auto-start, so on-demand is the default.

**v1 (manual trigger, ships first):**
1. **UP:** a `nixdev` operator (or a test-cluster script — the precedent
   exists: `CriomOS-test-cluster/scripts/nspawn-dune-on-prometheus` et al.)
   runs on the host: `criomos-nspawn create mercury <system-path>` then
   `criomos-nspawn start mercury`. The guest boots on its own
   `10.77.0.7/24` / `mercury.fieldlab.criome`.
2. **DEPLOY:** lojix deploys to the now-reachable address (§6).
3. **DOWN:** after the test, the same trigger runs `criomos-nspawn stop mercury`
   (or `terminate`/`remove` to reclaim).

Who triggers: a person or test-runner script in the `nixdev` group on the
physical host (`atlas`). No daemon owns the lifecycle in v1.

**v2 (optional, lojix-driven — see §6 option B):** lojix gains `StartNode`/
`StopNode` meta ops that SSH the `super_node` host and run `criomos-nspawn
start/stop`, recording the already-built `ContainerLifecycleRecord`. This makes
the lifecycle daemon-owned and durable. Deferred — v1 ships without it.

## 6. lojix integration

### Addressing: zero new work

lojix targets `root@<node>.<cluster>.criome` via
`SshTarget::root_at_node` → `CriomeDomainName::for_node`
(`schema_runtime.rs:496-504,2155-2176`). Because `mercury` is an ordinary
projected node with its own domain, lojix deploys to
`root@mercury.fieldlab.criome` with NO special path. The horizon-derived
address is exactly the integration the psyche asked for. lojix does not know or
care that `mercury` is a VM — it assumes the address is UP (which §5 step 1
guarantees). This matches the lojix cutover charter
(`lojix/INTENT.md:94-97`): "a full OS on a routed microVM with its own Criome
domain and reachable IP."

### Two integration options (proposal picks A for v1)

- **A — lojix stays address-only (status quo, v1).** The test orchestrator /
  test-cluster script starts the VM via `criomos-nspawn`, waits for the
  address, calls lojix `Deploy`, then stops it. Least change; lojix unchanged.
  This is the proposal's v1.
- **B — lojix gains node-lifecycle (v2, deferred).** Add `StartNode`/`StopNode`
  to `meta-signal-lojix/schema/lib.schema` (today `[Deploy Pin Unpin Retire]`),
  a `StartNode`/`StopNode` `EffectCommand` that reads the guest's
  `machine.superNode` from horizon (already projected —
  `fixtures/horizon/dune.json:33`), SSHes that host, runs `criomos-nspawn
  start/stop`, and records the existing `ContainerTransition`
  (`lojix/src/schema/sema.rs:134-164`). The recording table is already built;
  only the driver (meta op + effect + host SSH) is missing. Auto-start-before-
  deploy could then key on `behavesAs.virtualMachine`.

## 7. Open questions for psyche review

1. **Variant name** — `TestVm` vs `EdgeTestVm` vs `Sandbox`? Proposal uses
   `TestVm` (substrate-neutral cluster role). Confirm.
2. **`location` derivation** — should a Pod's `None` location resolve to its
   host's location at projection (one-hop walk like `resolve_arch`), or stay
   literally None? Proposal leans toward derive-from-host (a VM is physically
   where its host is) but allow explicit override.
3. **`location` shape** — free `Location` string now, or a closed enum of known
   sites? Proposal: free newtype now (sites churn); tighten later if needed.
4. **Substrate: nspawn vs microvm for v1** — nspawn is on-demand-by-default and
   needs no new machinery; microvm gives truer hardware (own kernel, VFIO) but
   needs non-autostart wiring. Proposal: nspawn v1, microvm follow-up. Confirm
   which the psyche wants the test VM to actually be.
5. **Lifecycle ownership** — manual `nixdev` trigger (v1) vs lojix meta op
   (v2)? Proposal ships v1 manual; is v2 in-scope for this change or a separate
   later proposal?
6. **`disk_gb` placement** — on `Machine` (proposal) vs as a `size: Magnitude`
   bump vs structural in `Io`? Proposal puts it on `Machine` beside `ram_gb`
   because a VM disk is a single allocated number, not a partition layout.
7. **Resource model** — raw `cores`/`ram_gb`/`disk_gb` (proposal, since a VM
   author wants exact knobs) vs the abstract `size: Magnitude` ladder used
   elsewhere? Proposal: raw for VMs (they are explicitly hand-sized).

## 8. Implementation order

1. **horizon-rs model** — `species.rs`: add `NodeSpecies::TestVm`. `machine.rs`:
   add `disk_gb`, `location`, and the `Location` newtype. `node.rs`: add
   `test_vm` to `TypeIs` + `from_species`, and to `BehavesAs` + `derive`. Update
   any exhaustive `match`/struct-literal the compiler flags. (`horizon-rs/lib/src/`)
2. **horizon-rs tests/fixtures** — add a `TestVm` Pod node to a test cluster and
   a golden-projection fixture mirroring `fixtures/horizon/dune.json` (assert
   `behavesAs.testVm`, `machine.superNode`, `machine.location`, `disk_gb`,
   and `criomeDomainName`). (`horizon-rs/lib/tests/`, `horizon-rs/fixtures/`)
3. **Declare the test VM** — add `mercury` (or chosen name) to
   `CriomOS-test-cluster/clusters/fieldlab.nota` as the §2 datom, hosted on a
   real `Large`+`Center` host (`atlas`).
   (`CriomOS-test-cluster/clusters/fieldlab.nota`)
4. **CriomOS guest config** — gate the lean guest profile on
   `behavesAs.testVm`; ensure the guest emits sshd + operator key (it already
   does as a normal node — the work is suppressing the heavy stack, not adding
   deploy plumbing). (`CriomOS/modules/nixos/` — new `test-vm/` gate or
   `normalize.nix` branch)
5. **CriomOS host emission** — extend `vm-testing/default.nix` (or a new
   `test-vm-host` module) to, per projected `ex_node` with
   `superNode == thisNode && behavesAs.testVm`, emit the nspawn/microvm guest +
   set-up tap + guest-IP `networking.hosts` entry + non-autostart unit.
   (`CriomOS/modules/nixos/vm-testing/default.nix`)
6. **Wire the trigger** — a test-cluster host-side runner script
   (`criomos-nspawn create/start … ; lojix Deploy … ; criomos-nspawn stop`)
   modeled on `nspawn-dune-on-prometheus`.
   (`CriomOS-test-cluster/scripts/`)
7. **(v2, optional, separate proposal)** lojix `StartNode`/`StopNode` meta op +
   effect + `ContainerTransition` recording, reading `machine.superNode` for
   the host SSH target. (`meta-signal-lojix/schema/`, `lojix/src/`)

Steps 1-6 deliver the full intent: a horizon-declared, on-demand, integrated
test VM that lojix deploys to via its derived address. Step 7 is the
daemon-owned-lifecycle upgrade and can land later without reshaping 1-6.
