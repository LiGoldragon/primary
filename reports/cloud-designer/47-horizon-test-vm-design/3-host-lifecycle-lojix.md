# Test VM: node-on-host modeling, on-demand lifecycle, lojix integration

Read-only grounding for the test-VM horizon concept. Every claim cites a
file read. Mutated nothing.

## 1. Modeling — "node X is a VM hosted on physical node Y, with resources R"

The node-on-host relation already exists in the proposal and projection;
it is the `Pod` machine shape, not a new field.

### The host/super relation lives on `Machine`, not `Node`

`horizon-rs/lib/src/machine.rs:14-39` — `Machine` is:

- `species: MachineSpecies` (`Metal` | `Pod` per
  `lib/src/species.rs:37-40`); `Pod` IS "this node is a VM".
- `super_node: Option<NodeName>` (`machine.rs:20-21`, doc "Pod-only:
  which node hosts this pod") — the HOST relation. This is the clean
  host pointer: a `NodeName` reference to the physical node in the same
  proposal map.
- `super_user: Option<UserName>` (`machine.rs:22-23`, "Pod-only: which
  user runs this pod") — who owns the guest on the host.
- `cores: u32` and `ram_gb: Option<u32>` (`machine.rs:16,37-38`) carry
  resources R; arch defers to the host.

Arch resolution proves the relation is wired: a `Pod` may omit `arch`
and `NodeProposal::resolve_arch` follows `machine.super_node` one hop to
the host's arch (`lib/src/node.rs:549-575`; `Error::MissingSuperNode`
when the named host is absent — `lib/tests/error.rs:38`,
`lib/tests/node.rs:269-274`).

### Projection already flags the VM

`BehavesAs::derive` sets `virtual_machine = matches!(machine.species,
MachineSpecies::Pod)` and `bare_metal = …Metal` (`lib/src/node.rs:190-191`).
So `node.behavesAs.virtualMachine` is already a projected boolean
CriomOS can gate on.

### Address: the guest gets its OWN routed address

A node's reachable identity is independent of host/guest:
`CriomeDomainName::for_node(node, cluster)` = `<node>.<cluster>.criome`
(`lib/src/name.rs:106-109`), set unconditionally in
`NodeProposal::project` (`lib/src/node.rs:339,425`). The guest's IP is
its own `node_ip: Option<NodeIp>` (CIDR; `lib/src/address.rs:89-122`,
`proposal.rs:50`) plus its own yggdrasil `address`/`subnet`
(`proposal.rs:396-402`, `node.rs:342-345`). Reachability is the guest's
OWN routed address — NOT derived from or proxied behind the host.

### Canonical existing example — the `dune` Pod

`CriomOS-test-cluster/clusters/fieldlab.nota:80-104`: node `dune` is
`Edge` with machine
`(Pod (Some X86_64) 2 (Some [fixture-pod]) None (Some atlas) (Some aria) None (Some 4))`
— Pod, 2 cores, hosted on `super_node=atlas`, run by `super_user=aria`,
4 GiB RAM, its own `node_ip (Some [10.77.0.4/24])` and ygg
`[200:db8:1::4]`. Projects (`fixtures/horizon/dune.json:27-93`) to
`machine.superNode "atlas"`, `superUser "aria"`,
`criomeDomainName "dune.fieldlab.criome"`,
`behavesAs.virtualMachine true`. So a VM-on-host with its own routed
domain is already a first-class projected node.

### The gaps a test-VM concept must fill

1. **No `location L` field anywhere.** `Machine` has no location; the
   only host pointer is `super_node`. A "location" (physical site /
   datacenter / rack) would be a new optional field — likely on
   `Machine` beside `super_node`, kept near the struct end so positional
   NOTA still parses (the convention `machine.rs:29-30,36-37` already
   follows for `chip_gen`/`ram_gb`).
2. **No test-VM SPECIES.** `NodeSpecies` (`species.rs:13-23`) has
   `EdgeTesting`/`RouterTesting`, but "testing" there means a
   next-gen/edge ROLE, not "ephemeral VM." `Pod` is a `MachineSpecies`
   (substrate), orthogonal to role. A proper test-VM species/role is a
   genuine new variant — the proposal-boundary test in
   `horizon-rs/INTENT.md:20-27` (variable + cluster-authored +
   non-derivable) is the gate it must pass.
3. **No declared lifecycle posture.** The closest existing field is
   `online: Option<bool>` (`proposal.rs:78-86`): default-true, and when
   `Some(false)` it only gates `is_remote_nix_builder` so dispatchers
   skip the node — it does NOT mean "not yet started." An on-demand VM
   needs an explicit posture (see §2), not a reuse of `online`.

## 2. On-demand lifecycle — bring a declarative VM UP / DOWN

### The host-side primitive exists today: `criomos-nspawn`

`CriomOS/modules/nixos/nspawn.nix` builds a host CLI `criomos-nspawn`
over `pkgs.nixos-container` (`nspawn.nix:18,169`). Verbs
(`nspawn.nix:30-41,123-161`):
`create <name> <system-path>` / `update <name> <system-path>` /
`start <name>` / `stop <name>` / `restart` / `terminate` / `remove`
(destroy) / `shell` / `status` / `ip` / `list`.

This is exactly the on-demand seam: `create`/`update` install the
guest's built system; `start`/`stop` bring it UP and DOWN imperatively.
A created machine does NOT auto-start (`nixos-container create` is
imperative; nothing sets `autoStart`), so "launched to test, stopped
after" is the default, not always-running.

Provisioning facts:
- Gated to large center hosts: `enable = size.large && behavesAs.center
  && !isContainer && !behavesAs.iso` (`nspawn.nix:13`). A host that runs
  test VMs must be sized `Large` + `Center` — i.e. `atlas` in fieldlab.
- Authority: the `nixdev` group runs `criomos-nspawn` NOPASSWD via sudo
  (`nspawn.nix:171-181`, `trustedGroup = "nixdev"` at `:11`). So a
  trusted developer/operator user on the host triggers it.
- State dirs are tmpfiles-managed (`nspawn.nix:185-190`); these are
  nspawn/`nixos-container` (systemd-machined) guests, not microVMs.

### Who triggers UP/DOWN

Today: a person (or a script) in the `nixdev` group on the HOST runs
`criomos-nspawn start <name>` before the test and `stop <name>` after.
`CriomOS-test-cluster/scripts/` already has host-side runners
(`nspawn-spirit-upgrade-on-prometheus`, `nspawn-dune-on-prometheus`,
`run-on-prometheus`) that drive nspawn guests on a real host — the
manual/triggered precedent.

### lojix does NOT drive this yet — but has the recording surface

`lojix/INTENT.md:46-50` names "container-lifecycle records" as a
daemon-owned durable table. Present in schema:
`ContainerTransition { cluster_name, node_name, container, state }` and
`ContainerState [Starting Started Stopping Stopped Failed]`
(`lojix/src/schema/sema.rs:134-164`), persisted as
`ContainerLifecycleRecord` (`sema.rs:322-328`, table at `:317`,
`LoggedEvent::Container` at `:311`), recordable via
`SemaWriteInput::RecordContainerTransition` (`sema.rs:109`) →
`record_container_transition` (`schema_runtime.rs:1539-1556`,
`lib.rs:436`).

BUT: nothing CONSTRUCTS a `ContainerTransition` in the decide path.
`decide_meta_input` (`schema_runtime.rs:801-842`) handles only
Deploy/Pin/Unpin/Retire; there is no Start/Stop meta op, no
`StartContainer`/`StopContainer` `EffectCommand`, and the meta contract
`meta-signal-lojix/schema/lib.schema:57,60-63` exposes only
`[Deploy Pin Unpin Retire]`. So the lifecycle table is recordable
scaffolding with no driver. Adding lojix-driven UP/DOWN means: a new
meta op (e.g. `StartNode`/`StopNode`), a new effect that SSHes the host
to run `criomos-nspawn start/stop`, and recording the transition.

## 3. lojix integration — does lojix start the VM, or just deploy?

### lojix deploys to the horizon-derived address; today it does NOT start anything

A deploy's SSH target is `SshTarget::root_at_node(cluster, node)` =
`root@<node>.<cluster>.criome`, built from
`CriomeDomainName::for_node` (`schema_runtime.rs:2154-2177,500-504`).
The pipeline resolve→eval→build→copy→activate (`schema_runtime.rs:1138-1207`)
SSHes that target for copy/activate. lojix does NOT know a node is a VM
and does NOT start it — it assumes the address is already UP. There is
no pre-deploy "is the host's guest running?" check and no Pod/super_node
awareness anywhere in `schema_runtime.rs` (the only `super_node` use in
the stack is horizon arch resolution, `node.rs:564`).

The cutover charter even bakes this assumption in: lojix's end-to-end
validation target is "a full OS on a routed microVM with its own Criome
domain and reachable IP" (`lojix/INTENT.md:94-97`) — the VM is expected
ALREADY reachable when lojix deploys.

### So the test flow, today's pieces

1. **Bring UP:** on the host (`atlas`-class, sized Large+Center), a
   `nixdev` trigger runs `criomos-nspawn create/update <guest>
   <system-path>` then `criomos-nspawn start <guest>`
   (`nspawn.nix:127-141`). The guest comes up on its own
   `node_ip`/ygg address with domain `<guest>.<cluster>.criome`.
2. **Deploy:** lojix (meta `Deploy`) targets `root@<guest>.<cluster>.criome`
   exactly like any node (`schema_runtime.rs:2158-2166`) — no VM
   special-casing; the address is reachable because step 1 started it.
3. **Bring DOWN:** the same host-side trigger runs `criomos-nspawn stop`
   (or `terminate`/`remove`) after the test.

Steps 1 and 3 are OUTSIDE lojix today (host-side `criomos-nspawn`,
person/script-triggered). lojix only owns step 2.

### Cleanest design options for closing the loop (for the synthesis to weigh)

- **A — keep lojix address-only (status quo).** A test orchestrator (or
  the test-cluster scripts) starts the VM via `criomos-nspawn`, waits
  for the address, calls lojix Deploy, then stops it. lojix stays
  deploy-only; least change; matches `INTENT.md` "VM already reachable."
- **B — lojix gains a node-lifecycle meta op.** Add `StartNode`/`StopNode`
  to `meta-signal-lojix`, an effect that SSHes the `super_node` host and
  runs `criomos-nspawn start/stop <guest>`, recording the existing
  `ContainerTransition` (`sema.rs:134`). lojix would need to read the
  guest's `super_node` from horizon to know WHICH host to SSH (the
  projection already carries `machine.superNode` —
  `dune.json:33`). Auto-start-before-deploy could then be a deploy
  option keyed on `behavesAs.virtualMachine`.

The recording table (`ContainerLifecycleRecord`) is already built for
option B; only the driver (meta op + effect + host SSH) is missing.
</content>
</invoke>
