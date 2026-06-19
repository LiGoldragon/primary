# 148 — Durable production test VM on prometheus: how horizon supports it, the role shape, and the 7let/77ic reconciliation

*The psyche asked, mid-test-work: "also test it with a durable node which is a vm
node (how do we support that in horizon?) and lives on prometheus, but isn't booted
by default. that way we can test our OS in that vm for continual development on the
production side... maybe we have a production test vm role?" Captured as Spirit `77ic`
(the durable on-demand test-VM increment), extending `y1v5`/`cncj`/`qkvx`/`se72`. This
is the grounded design answer. Headline: horizon already ships both legs typed, so no
new node kind is needed; the "role" already exists as a typed pair; the only genuinely
open question is an intent reconciliation between `7let` (host-untouched) and `77ic`
(durable, defined in cluster data) that is the psyche's to settle. Source: three
grounded readers (horizon node-model, CriomOS module/boot/networking, role-shape/
cutover) + synthesis.*

## Direct answer

A durable VM test node is supported in horizon with **no new node kind** — it is the
pair horizon already ships typed: the host capability `NodeService::VmHost` (the host
advertises a VM substrate) plus the guest role `NodeSpecies::TestVm` (the guest *is*
the test node), joined by the `ex_nodes` fold on `super_node == host &&
behaves_as.test_vm`. Both legs already exist typed on `horizon-rs` main
(`lib/src/proposal.rs:128` for `VmHost`, `lib/src/species.rs:30` for `TestVm`), and
the not-booted-by-default CriomOS module already consumes them
(`test-vm-host.nix:216`, `autostart = false`). So yes, treat it as a "production
test-VM role," but recognize the role is **a durable `TestVm` node homed on a
`VmHost`-carrying prometheus** — authored in cluster data, not a third type. The only
remaining horizon work is authoring the fact in `goldragon/datom.nota` (a psyche-gated
production-cluster edit) and, to literally satisfy the typed-source ask of Spirit
`qkvx` (the typed-NodeService-not-string decision), optionally adding a guest-side
`NodeService::VmTesting` variant to carry the durable-vs-ephemeral distinction;
nothing else needs inventing.

## How horizon expresses a durable VM node

Horizon already separates the two orthogonal axes this node needs. **KIND** is the
node species — the whole-node role — and **SERVICES** is a `Vec<NodeService>` of
per-node opt-in capabilities (`proposal.rs:38-94`, `NodeProposal { pub species:
NodeSpecies, ... pub services: Vec<NodeService> }`). The durable test node lives on
both axes at once, across two nodes:

- **Host leg (a service on prometheus).** `NodeService::VmHost { guest_subnet:
  TapSubnet, kvm: KvmAvailability, maximum_guests: Option<MaximumGuests> }`
  (`proposal.rs:128-142`). Its doc is explicit that the substrate facts are
  "cluster-authored here rather than invented in the Nix layer," and that it is a
  "sibling to `NixBuilder` — both opt-in per-node capabilities, never inferred from
  the node name" — exactly the typed-source discipline `qkvx` demands. It carries
  hand-rolled positional `NotaEncode`/`NotaDecode` (`proposal.rs:271-376`) and a
  `NodeServiceKind` mirror.
- **Guest leg (a species on the durable node).** `NodeSpecies::TestVm`
  (`species.rs:30`) is "a first-class cluster role ... a virtual machine (substrate
  `MachineSpecies::Pod`) but NOT an edge, center, or router node. The host the VM
  runs on is `Machine::super_node`." Its substrate-`Pod` projects
  `behaves_as.virtual_machine`, and species `TestVm` independently fires
  `behaves_as.test_vm` (`node.rs:210-219`) — derived flags, never inferred from the
  node name.

The join needs **zero new wiring**: the durable node names `machine.super_node =
prometheus` and `machine.species = Pod`; prometheus independently declares
`(VmHost ...)`; guest discovery is the existing fold (`super_node == this_node &&
behaves_as.test_vm`), and a `Pod` naming a missing `super_node` fails
`validate_pod_super_node` → `Error::MissingSuperNode` (`node.rs:645-666`).

**Identity / IP / domain (per Spirit `ggvg`, the projected-criome-domain ask) come
free.** The criome domain is projected, not authored: `CriomeDomainName::for_node`
yields `<node>.<cluster>.criome` (`name.rs:107-108`, called at `node.rs:367`), so a
node named `vm-testing` gets `vm-testing.<cluster>.criome` automatically. The IP is
cluster-authored as `node_ip: Option<NodeIp>` (a CIDR). The multi-host image-exchange
boundary is also already landed (`machine.rs:56-79`, `node.rs:548-564`).

**The one typed gap (`qkvx` / bead `primary-wvey`, the discard-the-string-hack
item).** Today the guest is marked only by its *species*; there is no guest-side
service variant. If we want the durable-vs-ephemeral distinction carried at the
service layer (the `TestVm` species doc at `species.rs:28-29` still describes the
*ephemeral* "launched to test, stopped after" model), add `NodeService::VmTesting {
persistence: Persistence }` strictly on the `VmHost`/`NixBuilder` template — enum arm,
`NodeServiceKind` arm, `kind()`/`is_kind`, a borrowed `VmTestingCapability<'a>` view,
`NodeProposal`/`Node` accessors, and both hand-written `NotaEncode`/`NotaDecode` arms.
Any field must be a typed closed-set domain value mirroring
`KvmAvailability`/`MaximumGuests`, never a bare bool/`String`. Optional for a first
cut; the node is fully definable from species + `VmHost` alone.

## Not booted by default

The mechanism is microvm.nix's per-VM `autostart`, already set in the canonical module
(`CriomOS/modules/nixos/test-vm-host.nix:216`, `autostart = false`). microvm.nix
builds a `microvm@<guest>.service` unit for every `microvm.vms` entry, but the
boot-time pull is filtered: `config.microvm.autostart` is `builtins.filter (vmName:
... .autostart) ...` (microvm host `default.nix:287-289`), and the only boot target,
`microvms.target` (`wantedBy = [ "multi-user.target" ]`), wants only the autostart
units (`default.nix:291-293`). So the guest's unit exists in the generation but
nothing pulls it at boot. You start it on demand with `systemctl start
microvm@<guest>.service` and stop it with `systemctl stop`, leaving it defined.

**Proof an idle guest is inert.** The guest's tap device and the host's `/32` route
exist *only while the unit runs*: `microvm-tap-interfaces@<guest>` is `partOf`
`microvm@<guest>.service`, running `tap-up` on `ExecStart` and `tap-down` on
`ExecStop` (microvm host `default.nix:152-165`), and `microvm@` requires it
(`default.nix:242-243`). With `autostart = false` the parent never starts at boot, so
`tap-up` never runs and the tap never appears. An idle guest consumes no CPU/RAM and
creates no tap — precisely Spirit `77ic`'s reasoning that the not-booted-by-default
mode keeps the guest and its routed networking inactive until a test is started.

## Keeping prometheus safe (Spirit `5hir5bnz`, do-not-break-prometheus-networking)

**What touches the host at all.** `test-vm-host.nix` scopes its host-side networking
as additive and link-local: each guest tap gets a dedicated `systemd.network` matching
**only by tap device name** (`matchConfig.Name = tapId entry.index`), a `/32` endpoint
sliced from the cluster-authored `guest_subnet` (not the host node IP), a `/32` route
to the guest, `RequiredForOnline=no`, and never a default route
(`test-vm-host.nix:266-280`). The `05-` filename prefix sorts before any broad
`10-main-eth` matcher so the tap is claimed by-name. The module header states it "does
NOT touch, replace, or reorder the host's existing interfaces / routing / firewall."

**The residual exposure to confirm.** `test-vm-host.nix:302-309` still *writes*
host-generation networking unconditionally (`systemd.network.networks = tapNetworks`,
`networking.useNetworkd = true`, `systemd.network.enable = true`, `networking.hosts =
guestHostEntries`) regardless of whether a guest runs. The tap *device* only appears
on guest start, but the networkd reconciliation runs at **activation**. On a live
router, a switch that restarts `systemd-networkd` is exactly the failure (Spirit
`kx32`, the deploy-dropped-connectivity record) that took down connectivity during a
prior deploy. Mitigation per Spirit `xv9v`/`1lex` (the BootOnce / durable-transient
records): activate via BootOnce, never a live `switch-to-configuration`, and bring the
durable node up out-of-band/console first. The `networking.hosts` line is an inert
`/etc/hosts` entry and is safe.

**Reconciling the two CriomOS modules and bead `primary-wvey`.** Two modules compete,
both imported in `criomos.nix`:

- `test-vm-host.nix` (**keep**) reads the real typed `VmHost` payload off
  `horizon.node.services` (`:85`), emits `autostart = false` guests, a real disk, the
  additive by-name tap, and `networking.hosts` resolving the **guest** IP (`:285-291`).
- `vm-testing/default.nix` (**delete**, with its `criomos.nix:40` import) is the
  obsolete string-keyed hack: it gates on a string `VmTesting` not in the schema
  (`:48`, can never fire on a real node), inherits `autostart=true`, sets
  `virtualisation.libvirtd.enable`, projects `networking.hosts` at the **host** IP, and
  uses a hardcoded persistent tap — the exact host-touching over-engineering Spirit
  `7let` and `5hir5bnz` forbid.

This is the work bead `primary-wvey` called for; Spirit `77ic` supersedes its garbage
and resolves it as the `VmHost` + `TestVm` pair. Update/close that bead to point at
`VmHost` + `TestVm`, noting `cncj` (gpu-passthrough disabled on prometheus) resolved
the passthrough split — so `VmHost` correctly carries no `gpuPassthrough` field.

## The production-test-vm role — the recommended shape

**Decision: host service plus guest node-kind — and they are the same shape, already
~80% built.** Add no new node KIND beyond what exists.

- **Option A (host `VmHost` service + guest `TestVm` node): recommended.** Fits
  horizon's model exactly — services attach to hosts, nodes have a species. Both types
  exist typed; the typed `test-vm-host.nix` already consumes them not-booted-by-default;
  the multi-host/image-exchange projection is landed; honours `qkvx` and `77ic`
  verbatim. The durable node is just cluster-data authoring plus a not-booted-at-boot
  unit.
- **Option B (a dedicated node KIND only, host unmarked): rejected.** Without
  `VmHost` the module has nowhere typed to read `kvm`/`guest_subnet`/`maximum_guests`
  and must infer them from the node name — the exact anti-pattern `qkvx`/`cncj`
  condemn.
- **Option C ("both"): not a third option — it is what A already is.** The service
  marks the host capability, the species marks the guest role, the `ex_nodes` fold
  joins them. Framing it as "both" risks a redundant third type — do not add one.

**The typed shape, concretely.** The production test-VM role = a durable
`NodeSpecies::TestVm` node in `datom.nota` homed on a `VmHost`-carrying prometheus.
Production edit: append `(VmHost <tap-subnet> Available (Some <ceiling>))` to
prometheus's service vector `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`
(`goldragon/datom.nota:97`) — `Available` because prometheus is x86-64 with real KVM —
and add a new top-level `TestVm` node (e.g. `vm-testing`) with `machine = (Pod ...
super_node=prometheus ...)`, an authored `node_ip`, and ygg keys. prometheus's species
stays `LargeAiRouter`; host capability is always a service, never a species.

## How the lojix live Test-op drives it

Yes — the live Test-op should **start → deploy → assert → stop** the durable node,
leaving it defined. The scaffolding already has the right bracket but stubbed effects
(per report 147: `run_bring_up_test_vm`/`run_tear_down_test_vm` build a real `ssh` +
`systemd-run --user` + `unshare -rn` + `nsenter` invocation then discard it with
`let _invocation =`, `schema_runtime.rs:2894-2926`; no `DeployIntoTestVm`/
`AssertTestVm` effect between bring-up and tear-down, `:1755-1782`; `Live` honestly
rejected at submit, `:1595-1600`). The realization of `77ic`'s "not booted by default
but started on demand":

1. **Start** — `BringUpTestVm` starts the already-built non-autostart
   `microvm@<guest>.service` (or, on a live router, the host-untouched `unshare -rn` +
   `nsenter` transient path).
2. **Deploy + assert** — the **new** `DeployIntoTestVm` + `AssertTestVm` pair fills the
   empty middle: `nix copy --to ssh-ng` + activate + run the flake's guest assertion.
   (This is exactly the lojix code work Track A is implementing now.)
3. **Stop** — `TearDownTestVm` stops the unit so the host netns returns
   byte-identical; the node persists in cluster data, only its runtime is on-demand.

**Relation to Track A's throwaway nixosTest — they complement.** The throwaway
`runNixOSTest` (`TestMode::Hermetic`, already landed and proven per cloud-designer 54)
is the fast, sandboxed, every-commit, host-untouched CI proof (`7let`). The durable
`TestVm` node (`TestMode::Live`, against the real homed node) is the continual
production-side dev target `77ic` adds on top. The operator-nspawn e2e (`btc0`) stays
available. **The durable `TestVm` node becomes the canonical cutover-validation target
of `se72`**, with the hermetic test as the CI proof.

## What's gated / who owns what

- **Production-cluster change (psyche-gated; operator / cluster-operator).** Appending
  `(VmHost ...)` to prometheus and adding the durable `TestVm` node in
  `goldragon/datom.nota` is a production cluster-data edit, and the first live run on
  the router is psyche-gated (cloud-operator report 388's gate). cluster-operator owns
  the live-router activation, which must be BootOnce, never a live switch (`xv9v`/
  `kx32`/`1lex`).
- **Code work (designer authors on `next`/feature in `~/wt`; operator owns main +
  rebase).** The optional `NodeService::VmTesting` typed variant in `horizon-rs` (built
  strictly on the `VmHost`/`NixBuilder` template), the deletion of
  `vm-testing/default.nix` + its `criomos.nix:40` import, and the two new lojix effects
  (`DeployIntoTestVm` + `AssertTestVm`) plus turning `LiveNotYetEnabled` into the real
  start→deploy→assert→stop cycle (Track A is mid-flight on the lojix effects).
- **Sequencing.** Author/confirm the typed horizon shape **before** deleting the string
  module, so the durable node stays definable from real cluster data.
- **Bead.** Update/close `primary-wvey` to point at `VmHost` + `TestVm`.

## Risks + the simpler alternative — the reconciliation that is the psyche's call

The honest tension is **Spirit `7let` (high certainty) vs `77ic` (medium).** `7let`
clarified that "reconfiguring the host generation with microvm.nix plus tap plus
projected `networking.hosts` ... was designer over-engineering and not psyche intent —
use the host KVM infra, deploy into the VM, leave the host untouched." `77ic` then asks
for "a persistent VM node defined in cluster data and homed on prometheus." A durable
node defined in cluster data **necessarily declares the microVM (and its tap `.network`
file) into prometheus's generation** — the precise host-generation touch `7let`
flagged.

- **The simpler transient host-untouched path (`7let`):** a throwaway KVM VM via the
  user-namespace path (`unshare -rn` + `nsenter`) or `runNixOSTest`, never touching
  `switch-to-configuration`. Right for one-off runs and every-commit CI — cheap,
  sandboxed, zero host-generation risk, already proven.
- **The durable-routed path (`77ic`):** the node persists in cluster data with a stable
  `vm-testing.<cluster>.criome` domain and routed reachability, started on demand.
  Right for continual production-side development — a stable target you redeploy to
  repeatedly. Its cost is the residual host-generation touch and the `5hir5bnz`
  activation-ripple risk.

**To confirm with the psyche before any live activation:** is an `autostart = false`
host-declared microVM the intended reading of "defined in cluster data but leave the
host untouched"? The unit is built into the generation but never pulled at boot, and on
a live router the run can use only the namespace-scoped path — so the host stays inert
until a test starts. That is the most plausible bridge between `7let` and `77ic`, but
`7let`'s higher certainty means the durable node's reachability model (namespace-scoped
bring-up vs a persistent host route) is the `5hir5bnz` boundary and is psyche-gated.
**Recommendation:** land the typed shape and the hermetic CI path now (in flight); gate
the durable-node `datom.nota` edit and first live-router run on explicit psyche
confirmation of the `7let`/`77ic` reconciliation.
