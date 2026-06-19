# 65 · Where the cloud-node image lives (2026-06-19)

The psyche asked: *"we should have an updated image to get our cloud nodes
up quickly. where is the right place to keep that code?"*

Short answer: the image **definition** is an OS artifact and belongs in
**CriomOS**, as a minimal cloud-node system profile gated by a new
`NodeSpecies::CloudNode` (mirroring the existing `TestVm` model). The
**cloud daemon stays the control plane** and only references the built
snapshot id — and it does so through the `image_name` field that
*already exists* on the wire, so **no new wire field is required**. The
build pipeline is `nixos-generators`/`nixos-rebuild build-image` ->
provider snapshot/custom-image -> boot-from-snapshot.

The thesis in the directive survives contact with the real code, with one
honest correction (CriomOS *does* have a `modules/nixos/disks/` dir; what
it lacks is any image-*format* output) and one sharpening (the wire field
is already present, not a new optional add). Details below.

## 1 · The answer: CriomOS, as a `CloudNode` species profile

### What CriomOS actually looks like today

CriomOS exposes exactly one deploy surface —
`nixosConfigurations.target` (`flake.nix`) — network-neutral, with no
`hosts/` directory and no per-host configs; the per-`(cluster, node)`
facts arrive through the projected `horizon` input and CriomOS modules
*render* them. There is no `nixos-generators` import and no image-format
output anywhere in `flake.nix`, `modules/`, or `packages/` (grep for
`generator`/`qcow`/`build-image`/`digital-ocean` finds only unrelated
hits). The single existing "image" path is the live ISO at
`modules/nixos/disks/liveiso.nix`.

Correction to one input: there **is** a `modules/nixos/disks/` directory
(`default.nix`, `preinstalled.nix`, `pod.nix`, `liveiso.nix`). It is the
right neighbourhood for an image module. `preinstalled.nix` is the
standard installed-disk renderer (reads `horizon.node.io.disks`,
`bootloader`, swap); `pod.nix` is the container substrate; `liveiso.nix`
is the bootable-ISO variant. A cloud-node image is the fourth member of
exactly this family.

### How a node role is added — the `TestVm` model to mirror

A node class in this stack is **a species, a derived facet, and a gated
module** — three coordinated edits, no daemon code:

1. **horizon-rs `lib/src/species.rs`** — add a `NodeSpecies` variant.
   `TestVm` is already there as the precedent: a first-class, deliberately
   minimal cluster role whose substrate is `MachineSpecies::Pod`.
2. **horizon-rs `lib/src/node.rs`** — `TypeIs::from_species` maps the
   variant to a flag and `BehavesAs::derive` projects the node's
   `behaves_as` facets. `TestVm` sets `test_vm: true` and, by setting none
   of the heavy `type_is` flags, leaves edge/center/router/large_ai all
   false — that is the whole leanness mechanism.
3. **CriomOS `modules/nixos/criomos.nix`** — import a gate module wrapped
   in `mkIf (behavesAs.<facet> or false)`. `test-vm-guest.nix` is the
   model: `mkIf (behavesAs.testVm or false) { … }` suppresses doc/home
   weight while leaving the node a real, deployable target (sshd, root
   keys, real disk all untouched).

A `CloudNode` species slots into exactly these three seams. The image
module is the CriomOS leg — call it `modules/nixos/disks/cloud-image.nix`
(or `cloud-node.nix` alongside it), gated on a new `behavesAs.cloudNode`,
carrying: `services.openssh.enable = true`; the provider-appropriate
bootloader and serial console; cloud-init / metadata fetch + SSH-key
injection; growpart/online root-FS resize; and *no* GUI. It is the
boot-time-minimal counterpart to `liveiso.nix`. The **image-format
output** (qcow2 for DO, raw for Hetzner) is a *new* flake attribute — see
§3 — but the system *definition* it builds from is this CriomOS module.

### Alternatives, decided explicitly

- **(a) Profile inside CriomOS — CHOSEN.** The image is a NixOS system
  configuration: bootloader, filesystems, sshd, cloud-init, console. Every
  one of those already lives in CriomOS modules and is projected from
  horizon. Putting it anywhere else would duplicate the platform's module
  tree. It reuses the species/`behavesAs`/gated-module machinery the
  platform is built on, so it costs ~one module plus three small horizon
  edits, not a new repo.

- **(b) A small dedicated repo — REJECTED for now.** A separate
  `criomos-cloud-image` flake would have to consume CriomOS as an input,
  re-thread `system`/`pkgs`/`horizon`, and duplicate the disko/console/
  cloud-init choices that are CriomOS's job. The only thing genuinely
  *not* a system config is the image-*format* wrapper (the
  `nixos-generators`/`build-image` invocation), and that is one flake
  attribute, not a repo's worth of surface. Revisit only if the build
  pipeline grows provider-specific tooling heavy enough to warrant its own
  CI lane; today it does not.

- **(c) Inside the cloud daemon repo — REJECTED, on principle.** This
  violates the component-triad boundary. `cloud` is a daemon + its bundled
  CLI; `signal-cloud` / `meta-signal-cloud` are its working and meta
  signals. **A NixOS image is not a signal** — it is neither wire vocab
  nor runtime behaviour — so it is not triad-leg material and cannot live
  in any of the three. cloud's own INTENT.md says signal repos "carry only
  Signal wire vocabulary" and the runtime owns "provider execution" — an
  OS closure is neither. The daemon must *reference* the image, never
  *define* it. Mixing the OS artifact into the control plane is the same
  category error as baking nixpkgs into a REST client.

The triad boundary is the load-bearing reason (a) beats (c): the control
plane selects an id; the platform owns the bytes.

## 2 · The ownership split

**CriomOS owns the image DEFINITION. cloud owns snapshot-id SELECTION and
provisioning.** Concretely:

- **CriomOS** owns the `CloudNode` system profile and the build that turns
  it into a provider-uploadable artifact (qcow2 / raw). It owns the
  bootloader, console, cloud-init, growpart, disko device, and
  architecture *binding* per the projected `system`.
- **cloud** owns: which snapshot id to boot, the per-second/billing
  lifecycle, the provider API calls (create/observe/destroy), and the
  reuse pool. It treats the image as an opaque `ImageName` string.

### The wire: no new field is needed (verified)

The cloud-image-selection investigation's lean — *reuse the existing
`image_name`; no wire growth* — is **confirmed against the actual
source**. In `meta-signal-cloud/src/lib.rs`:

- `ImageName(String)` is an unvalidated newtype.
- `DesiredHostState` already carries `image_name: ImageName` (alongside
  `provider`, `host_name`, `server_type`, `ssh_key_name`).
- `HostPlan` already carries `image_name: ImageName` too.

The daemon already copies `DesiredHostState.image_name` into
`HostPlan.image_name` and the providers already set their payload's
`image` from it (DO `DropletPayload.image`, Hetzner `ServerPayload.image`,
in `signal-cloud`). Both DigitalOcean and Hetzner accept a **private image
referenced by numeric id** in exactly that string position. The live-test
runbook (report 64) already passes a real value there —
`ubuntu-24-04-x64` — in:

```
meta-cloud "(PrepareHostPlan ((DigitalOcean edge-test s-1vcpu-512mb-10gb ubuntu-24-04-x64 criome-test)))"
```

A pre-baked snapshot is a **drop-in replacement of that one string** with
the snapshot's numeric id. So:

- **No wire change.** No new field on `HostPlanPreparation`,
  `DesiredHostState`, or `HostPlan`; no schema-bridge edit; no signal-tree
  growth.
- **No daemon code change** to *carry* a snapshot id — the field is
  already plumbed end to end.
- The **only** code touched on the control-plane side is *where the id
  comes from*: today tests/CLI hand-author the `image_name`; the durable
  end-state is that the cluster spec authors it (the snapshot id is
  cluster-authored SPEC — see §4). A default/override convenience (a
  fallback when the caller omits it) is the *one* optional addition you
  could choose to make, and it is purely additive in `meta-signal-cloud`
  + `schema/lib.rs`; it is not required for the image-home decision.

Mark for the operator: **no wire/code change is required to start booting
from a snapshot.** The only *new* code is in CriomOS (the image module +
the build attribute, §3). Everything on the cloud side is value-level.

## 3 · The build -> upload -> boot pipeline, per provider

The two target providers diverge sharply because **DigitalOcean has a true
custom-image upload API and Hetzner does not.** This is the single most
important provider asymmetry for "up quickly."

### DigitalOcean — direct custom-image upload

DO accepts a custom image uploaded **by URL** (`POST /v2/images` with
`{name, url, distribution, region}`), formats raw/qcow2/vhdx/vdi/vmdk,
optionally gzip/bzip2, <=100 GB uncompressed; requires cloud-init >=0.7.7,
sshd at boot, ext3/ext4. No throwaway server needed.

Recipe sketch:

1. Author the CriomOS `CloudNode` profile (openssh, grub on BIOS x86,
   cloud-init, growpart, `console=ttyS0`, no GUI).
2. Add a flake attribute that builds the DO format —
   `nixos-generators.nixosGenerate { format = "do"; modules = [ <profile> ]; }`
   (the `do` format bundles DO cloud-init + growpart), or the 25.05+
   `nixos-rebuild build-image` / `digital-ocean-image.nix` path -> a
   `nixos.qcow2.gz`.
3. Host it at a public URL.
4. `doctl compute image create nixos-node --image-url https://host/nixos.qcow2.gz --region nyc1`
   (or `POST /v2/images` with `distribution=Unknown` — DO has no NixOS
   distribution option; `Unknown` is community practice).
5. Wait for status `active` (5-30 min); read the **numeric image id**.
6. Boot fast nodes by passing that numeric id as the `image_name`.

DO custom images and droplet snapshots are distinct API objects but both
end up as **private images referenced by numeric id**. Snapshot storage is
$0.06/GB-mo on final compressed size; the image uploads to one datacenter
and is transferable to others with no multi-region surcharge.

### Hetzner — snapshot-from-bootstrap (the chicken-and-egg)

**Hetzner Cloud has NO disk-image upload API** (confirmed across sources).
The *only* way to get a custom OS image in is to **snapshot a running
server** (`POST /servers/{id}/actions/create_image` with `type=snapshot`).
That snapshot survives server deletion and is referenced by numeric id at
server create. So you must **bootstrap once** to mint the first snapshot —
the chicken-and-egg.

Two ways to mint that first snapshot:

- **Option A — no NixOS install hop (`apricote/hcloud-upload-image`).**
  Build a raw image (`nixos-generate -f raw` / `build-image raw` ->
  `nixos.raw.bz2`), host it, then
  `hcloud-upload-image upload --image-url https://host/nixos.raw.bz2 --architecture x86 --compression bz2 --location nbg1`.
  The tool boots a temp server into rescue mode, `dd`s the raw image onto
  the root disk, snapshots, and deletes the temp server — leaving a
  reusable snapshot id. This is the cleanest "image-home" -> snapshot path
  for Hetzner.
- **Option B — install hop.** Create a stock-Ubuntu server, run
  `nixos-anywhere --flake .#<host>` (kexec + disko partition + install),
  then `hcloud server create-image <id> --type snapshot`. Slower, but
  reuses the disko/`nixos-anywhere` path that Phase-2 fork 1 already
  leans toward for *first* install.

Then spin up fast:
`hcloud server create --image <snapshot-id> --type cx22 --location nbg1`.
Hetzner snapshot storage is ~EUR 0.014/GB-mo (post 2026-04-01; confirm on
the official page before quoting).

### nixos-generators formats and the "up quickly" verdict

Formats: `do`/`digitalocean` (qcow2.gz + cloud-init), `qcow`/`qcow2`,
`raw`/`raw-efi`, plus `amazon`/`gce`/`azure`. Build via `nixos-generate -f
<fmt>` or the flake `nixosGenerate{format=…}`; 25.05+ supersedes the CLI
with `nixos-rebuild build-image --image-variant <variant>` /
`config.system.build.images`. **Pin which path** you standardize on — the
exact attribute names shift across nixpkgs releases (caveat below).

**Verdict — pre-baking wins for "up quickly."** A pre-baked snapshot/custom
image is boot-and-go in seconds: the disk already contains a booting
NixOS, no install step. `nixos-anywhere`/`nixos-infect` *install* NixOS at
provision time (minutes + reboot/kexec) — they are how you *mint* the
first image (mandatory on Hetzner) and how you do declarative disko
partitioning, **not** how you spin up routinely. This is precisely why the
psyche's "up quickly" instinct points at a pre-baked image, and why the
image belongs in CriomOS as a buildable artifact rather than as a
per-provision install script in the daemon.

### Caveats to carry into implementation

- Hetzner's raw OpenAPI page is a JS app that didn't render via fetch; the
  `create_image type=snapshot` and image-by-id semantics are confirmed
  from the official hcloud Python client docs + secondary sources. Verify
  exact JSON field shapes against `docs.hetzner.cloud` if scripting.
- Hetzner snapshot price (EUR 0.014/GB-mo) is dated 2026-04-01 per
  secondary sources; confirm on the official pricing page.
- DO has no NixOS `distribution`; `Unknown` is community practice and DO
  does not QA NixOS images (the qcow2 + cloud-init path is well-trodden in
  the community).
- `nixos-generators` is in flux (25.05+ pushes `build-image`); pin the
  path and the attribute names.
- Re-verify `hcloud`/`doctl`/`hcloud-upload-image` flag names and defaults
  (e.g. Hetzner location `fsn1`) against the installed tool versions.
- Validate serial-console `kernelParams` per instance type before baking
  (`console=ttyS0` x86; ARM/Ampere needs `virtio_gpu` in initrd per the
  NixOS wiki).

## 4 · How this settles the deferred Phase-2 forks

Reports 56-60 left three Phase-2 forks open with designer *leans* (no
captured Spirit). The image MECHANISM was already settled
(`nixos-anywhere` over kexec for first install; native pre-built images a
deferred optimization). "Where the cloud-node image lives" is **not itself
a new fork** — it is a sub-question of forks 1 and 2. Deciding it as above
**resolves or constrains** each, consistent with the recorded leans:

- **Fork 1 — install-hop owner (cloud-owns-install lean).** Image-home
  *presupposes* this fork, it does not reopen it. The CriomOS image is the
  artifact the install-hop owner consumes; the daemon still owns when/how
  to boot it. Choosing pre-baked snapshots **promotes** the deferred
  "native image" optimization from "later lock-step" to "the fast path,"
  but it does NOT remove the install-hop: Hetzner's first snapshot still
  needs a one-time bootstrap (Option A `dd`, or Option B `nixos-anywhere`),
  and disko-based partitioning still rides the install hop. Net:
  **settles** that the image is a CriomOS-built artifact, **leaves open**
  whether first-mint uses `hcloud-upload-image` (no install hop) or
  `nixos-anywhere` (install hop). Flag this as the live sub-choice the
  psyche should weigh.

- **Fork 2 — horizon model + provisioning ledger.** Image-home
  **constrains** it. The image/snapshot id passes horizon-rs's three-part
  proposal-boundary test (variability: owners pick different images;
  authority: the cluster owner, not the provider; non-derivable: must be
  told) -> it is **cluster-authored SPEC** in `datom.nota`. The
  provider-authored identity (server id, public IP) stays in the
  **ledger**. This pins the image to the spec side. It does **not** pick
  fork-2 option (a) full provider dimension + ledger-join vs (b)
  register-after — that sub-choice stays open.

- **Fork 3 — default architecture (ARM/CAX11 lean).** Image-home
  **settles the arch-bound facet**: a guest image is one closure per
  architecture (`horizon-rs`: `Error::HostSetArchMismatch`; `Arch::Arm64
  -> System::Aarch64Linux`). Picking ARM fixes the image `system` attribute
  to `aarch64-linux` and the disko device per `server_type`. Verify the
  ARM device once (the standing report-56 §8 risk). Trivially overridable
  per node.

What it leaves genuinely open: (1) Hetzner first-mint tool, (2) fork-2
(a)-vs-(b), (3) the ARM/x86 default itself (still a lean, not captured).
None of these block adopting the placement.

## 5 · Intent: not captured yet — recommended capture on confirmation

**This is a question, not yet a Decision.** The psyche asked "where is the
right place to keep that code?"; nothing here is captured in Spirit. The
three Phase-2 leans (cloud-owns-install, register-after, ARM/CAX11) live
only in reports 56-58, not in Spirit. The only NEW intent since the
opening directive `150a` is `g7zd` (DigitalOcean per-second provider,
landed) and `6ks1` (billing-hour reuse pool); neither touches image-home.

On psyche confirmation, run the Spirit gate -> **Record a new Decision**
(this is a genuinely new durable structural choice, not a clarification of
an existing record). Proposed shape (positional NOTA, bare atoms, no
quotes):

```
spirit "(Record (Decision High cloud [The cloud-node OS image is defined in CriomOS as a minimal CloudNode-species profile (mirroring TestVm), built to a provider image via nixos-generators. The cloud daemon stays the control plane and references only the built snapshot id through the existing image_name field — no new wire field. DigitalOcean uses custom-image upload; Hetzner snapshots a one-time bootstrap.]))"
```

(Verify the exact `Record` arity and field order against
`skills/skills.nota` and a fresh `spirit Observe cloud` before emitting —
I report the IDs as quoted in prior reports, not from a live query.)

INTENT.md updates to land on confirmation:

- **cloud INTENT.md** — under "On-demand compute provisioning," add: the
  image is selected by id through the existing `image_name`; cloud does
  not define or build the OS image; that is CriomOS's `CloudNode` profile.
- **CriomOS INTENT.md** — add a `CloudNode`-species line to the platform's
  scope: CriomOS owns the cloud-node image definition and its
  provider-format build (qcow2 for DO, raw for Hetzner), one closure per
  architecture.
- **horizon-rs** — when the species lands, note `CloudNode` in its
  `NodeSpecies` set and that the image/snapshot id is cluster-authored
  spec (passes the proposal-boundary test).
- **Primary INTENT.md** carries no cloud-node stance today; no change
  needed unless the psyche wants the placement reflected at workspace
  level.

## 6 · Relation to the live test in flight

Non-blocking. Report 64's DigitalOcean live test runs Tier 1
(adapter-level) and Tier 2 (full daemon chain) against **stock
`ubuntu-24-04-x64`** — passed in the exact `image_name` string position a
custom snapshot id will later occupy. The custom image is the **next
layer**, not a dependency: prove create/observe/destroy with stock Ubuntu
first, then swap the `image_name` value for the baked snapshot id with
**zero wire or daemon change**. The image work and the live test proceed
in parallel; nothing here gates the runbook.
