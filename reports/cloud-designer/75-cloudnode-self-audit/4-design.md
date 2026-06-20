# Critic 4 — cross-cutting design coherence + cluster data (the doris CloudNode)

Adversarial read of the whole CloudNode feature as a *design*, not as code.
Scope deliberately avoids Critic 1's territory (the Rust harness internals —
the all-digit mode sniff, the hardcoded `monitoring`/`ipv6`, the copy-not-
generalize `DeployCleanup`; all already filed in `1-rust.md`). This report
attacks the SHAPE: a test node named doris injected into production cluster
data, a committed real-looking ssh key with no known private half, placeholder
sizing frozen as fact, the four-repo spread, and the harness's two-mode design.

Files under judgment:
- `goldragon/cloud-node-data/datom.nota` (the committed doris entry, `b10df73`)
- `horizon-rs/.../species.rs`, `node.rs` (`NodeSpecies::CloudNode`, `a94e2b9`)
- `CriomOS/.../disks/cloud-node.nix` (`621a89a`, `d58f95d`)
- `cloud/.../digitalocean_deploy_live.rs`, `scripts/...mint...sh`, `flake.nix`

## Findings

### HIGH-1 — doris is a throwaway TEST node committed into PRODUCTION cluster data

`goldragon/cloud-node-data/datom.nota:28-49` adds `doris` to the goldragon
cluster proposal — the file whose own header (`:1`) and README (`README.md:3`)
call it "production cluster proposal" / "Production data for every node." The
commit message (`b10df73`) admits the node is sized with "placeholder sizing"
and carries a "throwaway placeholder" key. So a node that does not exist, whose
private key nobody holds, whose CPU/RAM/disk numbers are admittedly invented,
is now a first-class production cluster fact.

Why this is bad: cluster data is the source of truth consumed by *every other
node's* projection. `horizon-rs/lib/src/horizon.rs:148-157` builds `ex_nodes`
as the full node map minus the viewpoint, so the doris entry materializes into
`prometheus`'s horizon, `tiger`'s horizon, `ouranos`'s horizon — every node now
sees a peer named doris with trust `Max` (`datom.nota:245`, the trust block also
lists it `Max`). A `Max`-trust node is admin-reachable and mesh-projected; the
generated CriomOS config for real machines now references a phantom that has no
droplet behind it. That is exactly the failure mode the workspace's two-deploy-
stack discipline exists to prevent: an unproven thing leaking into the stack
that protects real hosts. "It only projects, nobody deploys it yet" is not a
defense — the data IS the contract, and it's already merged onto the branch
feeding the real cluster.

The honest precedent is right there and was ignored: `vm-testing`
(`datom.nota:178`) is a test node, but it is a `TestVm` species whose doc
(`species.rs` TestVm) marks it throwaway, it is pinned to a real host
(`super_node (Some prometheus)`), and it is a guest that gets launched and
stopped. doris is none of that — it is a permanent-looking `CloudNode` with no
host and no instance.

Fix: a test droplet does not belong in production cluster data. Either (a) put
doris in `CriomOS-test-cluster/clusters/*.nota` (the existing test-cluster
fixture repo the harness comments already reference — `horizon.rs` test comment
at the top of the new test cites `CriomOS-test-cluster/clusters/fieldlab.nota`),
or (b) if a DigitalOcean node is genuinely intended for the *real* cluster, then
provision it for real and commit real values — not a placeholder. The one thing
that should not happen is the current middle state: a fake node wearing
production clothes.

### HIGH-2 — the committed ssh blob is a REAL-LOOKING key whose private half nobody holds — worse than the obvious placeholder it replaced

`datom.nota:38`:
`(AAAAC3NzaC1lZDI1NTE5AAAAIDqIzfIew2Kt74D1axqbitgG/KP6WtT4bFl0zX7S+/4L None None)`

This base64 blob decodes to a *structurally valid ed25519 public key*: the
ssh wire framing parses (`ssh-ed25519`, a 32-byte key body, nothing left over).
It is indistinguishable from a real host key by inspection. Compare what the
DESIGN report 74 actually specified (`74-criomos-cloudnode-image/2-cluster-
data.md:162`):
`AAAAC3NzaC1lZDI1NTE5AAAAIArEPLACEHOLDERdorisCloudNodeSshKeyReplaceMe00000000`
— a blob with the literal word `PLACEHOLDER...ReplaceMe` baked in. The
implementation SILENTLY DOWNGRADED an obvious placeholder into a covert one.

Why this is bad — and it's the dangerous reading, not just the ugly one:
1. A `grep -i placeholder datom.nota` finds nothing. The single mechanical
   safeguard against shipping the fake key — its own self-identifying text —
   was removed. The only record that `:38` is fake now lives in a git commit
   message (`b10df73`), which no tool consults at deploy time.
2. It is a dangling credential. Someone minted a real keypair (the blob is a
   real curve point), put the public half in production cluster data, and threw
   the private half away (or didn't — nobody can tell). A "host key" in a
   cluster proposal is a trust anchor; committing one whose provenance is
   "throwaway, discard me" and whose private half is unaccounted for is a
   security smell in a file the README labels production trust data.
3. `SshPubKey` validation (`pub_key.rs`, per report 74/2:64-69) has no length
   or realness check — it accepts any base64 token. So the type system will
   never catch this. The self-identifying placeholder text was the *only* gate,
   and it was discarded.

Fix: if a placeholder must exist at all (see HIGH-1 — it shouldn't, in
production data), it MUST be self-identifying and MUST NOT decode to a valid
key — e.g. `AAAA...PLACEHOLDER-doris-REPLACE-BEFORE-DEPLOY-...` exactly as the
design report wrote it. Better: a real CloudNode's host key is generated by the
node at first boot and read back by the deploy step, so the cluster entry
should carry no key until the droplet exists — make `pub_keys.ssh` express
"pending first-boot" rather than a fabricated value.

### HIGH-3 — "CloudNode-image" is one abstraction smeared across four repos with three different spellings of the same boolean

The feature is a single concept — "a lean cloud node and the image you boot it
from" — but its definition is scattered, and the *same* gate is re-spelled at
every hop:
- `horizon-rs/lib/src/species.rs`: `NodeSpecies::CloudNode` (the species)
- `horizon-rs/lib/src/node.rs`: `TypeIs.cloud_node` and `BehavesAs.cloud_node`
  (two more booleans deriving from it)
- `goldragon/.../datom.nota:28`: the literal `CloudNode` record + a hand-
  authored `(Metal ... Mbr ... /dev/vda ...)` that the *human* must keep
  consistent with what CriomOS expects
- `CriomOS/.../disks/cloud-node.nix:16`: `horizon.node.behavesAs.cloudNode`
  (the same bit, now camelCase via serde) gating the image module
- `cloud/.../digitalocean_deploy_live.rs`: a deploy harness that knows none of
  the above and re-derives "is this a CriomOS node" from an `/etc/os-release`
  string match (`:260`).

Why this is bad: there is no single owner of "what a CloudNode is." The species
says "lean, Metal, Mbr." The datom must *manually* restate Metal+Mbr+/dev/vda
(`datom.nota:31-37`) — nothing enforces that a `CloudNode` species node carries
`Mbr`; a human could write `CloudNode ... Uefi` and projection would accept it,
then the CriomOS module's `boot.loader.grub.devices = mkForce [/dev/vda]`
(`cloud-node.nix:68`) would fight a UEFI config. The invariant the species
*claims* in its doc comment ("`Bootloader::Mbr` for DigitalOcean BIOS/GRUB") is
documentation, not a constraint. So the "coherent abstraction" is actually a
hand-maintained agreement across four repos with no type tying them together —
the Frankenstein the prompt suspected. Beauty (the special case dissolving into
the normal case) is the opposite of what shipped: CloudNode adds a brand-new
special case at *every* layer (a new species variant, two new derived bools, a
new image module, a new deploy mode) and dissolves nothing.

Fix: if CloudNode is real, the species must *own* its substrate invariants —
projection should reject a `CloudNode` whose `io.bootloader != Mbr` or whose
disk isn't `/dev/vda`, so the datom can't drift from what the image module
needs. Then the CriomOS module reads a *guaranteed* shape, not a hopeful one.
And collapse the boolean trio: `TypeIs.cloud_node` + `BehavesAs.cloud_node` are
the same fact as `species == CloudNode` (`node.rs:204,227`); see MEDIUM-1.

### HIGH-4 — placeholder sizing (1 core / 2 GiB / 25 GiB / nyc3) is committed as if it were measured fact, and it already disagrees with the harness defaults

`datom.nota:31`:
`(Metal (Some X86_64) 1 ... (Some 2) (Some 25) (Some digitalocean-nyc3) [])`
The commit message calls all of this "placeholder sizing." But in the datom it
is indistinguishable from balboa's real `4` cores or prometheus's real `128`
GiB — there is no marker, no `None`, nothing saying "unknown." `cores`,
`ram_gb`, `disk_gb` are all *required-ish* facts other nodes fill honestly;
freezing invented numbers there means the next reader treats them as the chosen
plan.

Worse, the placeholder is already internally inconsistent with the harness that
is supposed to provision it:
- datom location: `digitalocean-nyc3` (`datom.nota:31`)
- harness default region: `DEFAULT_REGION = "nyc1"`
  (`cloud/src/digitalocean.rs:30`)
- harness default size: `DEFAULT_SIZE = "s-1vcpu-512mb-10gb"`
  (`:28`) — that's 512 MiB / 10 GiB, NOT the datom's 2 GiB / 25 GiB.
- the mint script default: `SIZE=s-2vcpu-2gb` (`scripts/...:31`), `REGION=nyc3`
  (`:30`) — a THIRD size and it disagrees with the harness on cores.

So three artifacts that describe the same droplet disagree on its region (nyc1
vs nyc3), its RAM (512 MiB vs 2 GiB), its disk (10 vs 25 GiB), and its cores
(1 vs 2). Nothing reconciles them because the sizing was never real. This is
precisely why placeholders must not be committed as values: they immediately
fork into mutually-inconsistent copies and the reader can't tell which is
authoritative.

Fix: don't commit invented numbers as facts. If the droplet plan isn't chosen,
the fields that can be `None` (`ram_gb`, `disk_gb`, `location` are all
`Option`) should be `None` — the schema already models "operator hasn't filled
it in yet" (`machine.rs:38` doc says exactly that). When the plan IS chosen,
ONE place must own it and the datom/harness/mint-script derive from it, not
re-type it. Today they each guess.

### MEDIUM-1 — `TypeIs.cloud_node` and `BehavesAs.cloud_node` are dead-weight duplicates of `species == CloudNode`

`horizon-rs/lib/src/node.rs:204` sets `cloud_node: matches!(s,
NodeSpecies::CloudNode)`, then `:227` copies it through `let cloud_node =
type_is.cloud_node;`, then stores it in `BehavesAs`. The author's own commit
message and the new test assert `behaves_as.cloud_node` alongside
`type_is.cloud_node` AND `species == CloudNode` (`horizon.rs` test:
`assert!(matches!(doris.species, NodeSpecies::CloudNode))` *and*
`assert!(doris.behaves_as.cloud_node)` *and* `assert!(doris.type_is.
cloud_node)`) — three assertions for one fact.

Why this is bad: `cloud_node` is a pure function of `species` with no extra
information — unlike, say, `virtual_machine` (which also keys off `Machine`
substrate). It adds a third synonym for `species == CloudNode` and a reader now
has to wonder whether the three can ever disagree (they can't, by construction).
That is bool-flag accretion the typed-records discipline warns against: when a
flag is `matches!(species, X)` verbatim and adds nothing, it shouldn't be a
stored field — it's a method. The comment at `node.rs:227-232` spends six lines
explaining that `cloud_node` "is NOT a Pod, so `virtual_machine` stays false"
— but `virtual_machine` already derives that independently; the explanation is
defending a redundancy.

Fix: if downstream truly needs a quick "is this lean" predicate, make it a
method on the species/horizon node (`fn is_cloud_node(&self) -> bool { matches!
(self.species, CloudNode) }`), not two stored booleans copied through the
projection. The CriomOS module already reads `behavesAs.cloudNode` — but it
could read `species == CloudNode` from the same projection with no new field.

### MEDIUM-2 — the harness's "two modes" are a string-typed fork the deploy step can't see, coupling image-provenance to a `println!`

The harness advertises "mode 1 (pre-made CriomOS image) vs mode 2 (stock
distribution slug)" (`digitalocean_deploy_live.rs:16-22, 57-64`). Critic 1
already nailed the *implementation* (the all-digit sniff at `:163`). The
*design* problem is deeper and worth stating separately: the mode is never a
real input to the deploy. It only changes a log label (`:57-64`) and, for
mode 2, you still need `DEPLOY_FLAKE` set or the node never becomes CriomOS at
all (`:251-257`). So "mode 2 deploys CriomOS" is only true if a *second*,
independent env var is also set — the mode and the actual-CriomOS-ness are
decoupled. A reader picks "mode 2, ssh-reachable confirm" from the doc header
(`:16`) and gets a stock Ubuntu droplet that reports `ID=ubuntu`, never matches
the `ID=nixos` marker (`:139,260`), and the witness says `ssh-reachable`, not
`criomos-confirmed` — a silent non-result the harness presents as a successful
run path.

Why this is bad: the two-mode framing promises "either way you get a CriomOS
node," but mode 2 only gets you there via an orthogonal flake-deploy step that
the mode abstraction doesn't mention. The coupling is implicit and load-bearing
and lives only in prose. The honest model is: provenance is one typed input
(`ImageSource::{Snapshot, Slug}`), and "make it CriomOS" is a separate typed
step (`deploy: None | Flake(ref)`); the witness reflects the cross-product
honestly. Today a `Slug` image with no `DEPLOY_FLAKE` is a legal, green,
useless run.

Fix: model the two axes as two typed fields (image provenance × deploy action),
not one stringly "mode." Reject or loudly warn on the useless combination
(`Slug` + no flake + expecting CriomOS). Let the witness say "stock ubuntu,
no deploy" instead of dressing it as a deploy harness outcome.

### MEDIUM-3 — the four-repo spread is real, but the seams aren't typed, so the spread buys coupling without buying safety

The feature touches four repos (horizon-rs species, CriomOS image module,
goldragon datom, cloud harness). Some of that split is legitimate and matches
the workspace's repo boundaries (schema in horizon-rs, OS modules in CriomOS,
data in goldragon, deploy tooling in cloud). The problem is not the *number* of
repos — it's that the cross-repo contract is entirely by-convention:
- horizon-rs emits `behavesAs.cloudNode` as JSON; CriomOS reads it as a Nix
  attr with `or false` (`cloud-node.nix:16`) — a *silent* default, so a typo or
  a schema rename makes every node "not a cloud node" and the module goes inert
  with no error.
- the datom hand-restates the Metal/Mbr/`/dev/vda` shape (HIGH-3) that the
  image module hard-assumes (`cloud-node.nix:68`).
- the harness in the `cloud` repo knows nothing about horizon at all — it
  re-confirms "is this CriomOS" by SSHing in and grepping os-release
  (`:259-266`), re-deriving downstream what the schema already knew upstream.

Why this is bad: four repos that must agree, with zero compile-time or
projection-time enforcement of the agreement, is more surface than one feature
should carry. The `or false` fallback (`cloud-node.nix:16`) is the tell: it
turns a contract violation (horizon didn't emit the expected field) into a
silent no-op instead of a loud failure. DRY across repos is fine when a type
crosses the boundary; here only untyped strings/attrs cross.

Fix: the seam that matters is horizon→CriomOS. Make the CriomOS module assert
the field exists rather than `or false`-defaulting it (a missing
`behavesAs.cloudNode` is a projection bug, not "false"). Push the
Metal/Mbr/vda invariant into horizon-rs projection (HIGH-3) so the datom can't
drift. The harness's os-release re-confirmation is acceptable as an
*independent* end-to-end check, but it should be labeled as belt-and-suspenders,
not as the system's notion of "is this a cloud node."

### MEDIUM-4 — the node name `doris` is arbitrary and undermines the cluster's own naming scheme

`datom.nota:28`. The design report justifies the name as "DigitalOcean + a real
name; fresh, unused" (`74/2:145,178`) — i.e. it starts with D, like
DigitalOcean. But the cluster's actual names are a mix
(`balboa`/`ouranos`/`prometheus`/`tiger`/`zeus` — myth/proper-nouns —
plus the descriptive `vm-testing`). `doris` is neither a clear mythic peer nor
descriptive of role. For a node the author *admits* is a placeholder test
droplet, a cute proper noun is the wrong call: it reads as a permanent cluster
member (like zeus/tiger), hiding its throwaway nature exactly the way the
covert ssh key does (HIGH-2). The cluster already has the right convention for
test nodes — `vm-testing` says what it is.

Why this is bad: naming is the cheapest documentation. A test droplet named
`doris` looks production; a test droplet named `do-test` / `cloud-test` /
`digitalocean-test` is self-describing and would have made HIGH-1 obvious at a
glance in the trust block (`:245`).

Fix: if a test node stays (it shouldn't be in production data — HIGH-1), name
it for what it is (`do-test`). If a *real* DigitalOcean node is intended, a
proper noun is fine — but then it must carry real values, not placeholders.

### MEDIUM-5 — the CriomOS module fights nixpkgs defaults with `mkForce` in three places instead of owning the network story once

`cloud-node.nix:47-49,68`: `networking.useNetworkd = lib.mkForce true`,
`networking.networkmanager.enable = lib.mkForce false`,
`boot.loader.grub.devices = lib.mkForce [ "/dev/vda" ]`. The long comment at
`:40-46` explains *why* each force is needed — center-node DHCP is gated on
`behaves_as.center`, NetworkManager is on for lean nodes, etc. That comment is
an admission that the module is reaching across CriomOS's *other* modules to
override decisions they made, rather than the node profile composing cleanly.

Why this is bad: `mkForce` is the override-fighting the Nix discipline warns
against — it wins the priority war but it means two modules disagree about the
same option and the cloud module is bulldozing. If a CloudNode is genuinely a
distinct profile, the base modules should be *gated* so they don't set
networkmanager/networkd for a cloud node in the first place, leaving the cloud
module to set them at normal priority. Three `mkForce`es in one 80-line module,
each with a paragraph of justification, is a sign the profile boundaries are
wrong, not that the forces are clever.

Fix: gate the conflicting base config (NetworkManager-on, center-DHCP) so it
excludes `behavesAs.cloudNode`, then set networkd/grub at default priority here.
Reserve `mkForce` for genuine last-resort conflicts, not for routine
profile composition.

### LOW-1 — `diskSize = mkDefault "auto"` and the firmware/docs trims use `mkDefault`, inviting silent override of the one lever that keeps the image small

`cloud-node.nix:35` sets the closure-sizing lever `virtualisation.diskSize =
mkDefault "auto"` — the comment (`:31-34`) calls this "the lever that keeps the
image at ~1 GB, not 60." But `mkDefault` is the *lowest* priority; any other
module setting `diskSize` wins. For the single most load-bearing minimality
control, `mkDefault` is the wrong altitude — it should be a normal assignment
(or `mkForce` if something upstream sets it) so the 1-GB guarantee can't be
silently lost. Same for the `documentation.*`/`firmware`/`fontconfig`
`mkDefault false` (`:73-79`): if minimality is the contract, these are the
profile's decision, not a suggestion.

Fix: make the minimality levers normal assignments; reserve `mkDefault` for
things a node legitimately overrides.

### LOW-2 — the mint script is the only producer of a mode-1 image and it is unpinned `curl | bash` of an external master branch

`scripts/digitalocean-mint-criomos-image.sh:82` pipes
`elitak/nixos-infect`'s `master` through `bash -x` with `|| true`. (Critic 1
flagged the orphaned-from-flake and infect-default angles; the design point I
add: the *entire mode-1 image supply chain* for this feature terminates in an
unpinned third-party script fetched at runtime from a moving branch, inside a
repo whose stated reason to exist is reproducibility.) The feature's headline
claim is "declarative, reproducible, content-sized image" (report 74/6) — but
that 1.1-GB declarative image is built by the *CriomOS* path (`nix build
digitalOceanImage`), while the harness's mode-1 still depends on this
non-reproducible mint. Two image-production paths, one reproducible and one
not, and the non-reproducible one is what the live harness actually boots.

Fix: if the declarative `digitalOceanImage` is the real artifact (it is, per
74/6), the harness should consume *that* (upload it, boot its id), and the
nixos-infect mint script should be deleted, not shipped as a parallel path.
One image producer, the reproducible one.

### NIT-1 — doris's `online` is `None` while its sibling test node `vm-testing` is `(Some True)`

`datom.nota:48` (doris `online None`) vs `:200` (`vm-testing` `(Some True)`).
`None` defaults to online (`node.rs:413`), so the behavior matches, but two
test-ish nodes spell the same intent two different ways. Minor inconsistency in
a file that otherwise prizes explicitness (every node writes its full positional
tail). Pick one spelling for "online."

### NIT-2 — the new test re-asserts what three other assertions already cover

`horizon-rs` test `project_cloud_node_metal_derives_lean_profile` asserts
`species == CloudNode`, `behaves_as.cloud_node`, `type_is.cloud_node`,
`!virtual_machine`, `bare_metal`, `!iso`, and five `!role` facets. Given
MEDIUM-1 (the three cloud_node spellings are one fact), and that `bare_metal`/
`virtual_machine` are already covered by the existing TestVm/Metal tests, a
chunk of this test is re-verifying the projection's bookkeeping rather than the
new behavior. The one assertion that earns its keep is "no role facet derives
onto a lean cloud node." Tighten to that.

## Severity roll-up

- HIGH: test node doris in production data (1); covert real-looking ssh key
  replacing the self-identifying placeholder (2); CloudNode-image is a four-repo
  hand-maintained agreement with no type tying it, invariants only in doc-
  comments (3); placeholder sizing committed as fact and already forked three
  ways across datom/harness/mint (4).
- MEDIUM: `type_is`/`behaves_as` cloud_node duplicate `species == CloudNode`
  (1); two-mode harness couples provenance to a log label, mode-2-as-CriomOS
  silently depends on a second env var (2); four-repo seams untyped, `or false`
  turns contract violation into silent no-op (3); arbitrary cute name on a
  throwaway node (4); three `mkForce`es papering over wrong profile boundaries
  (5).
- LOW: minimality levers at `mkDefault` (lowest) priority (1); mode-1 image
  supply chain is unpinned `curl|bash` while the headline image is the
  declarative one (2).
- NIT: `online` spelled two ways across the two test nodes (1); the new test
  re-asserts redundant bookkeeping (2).

## The one-sentence verdict

The CloudNode feature works mechanically (the 1.1-GB image is a genuine win),
but as a *design* it injected a fake node into production trust data behind a
real-looking key and an invented size, and it expresses one abstraction as a
hand-maintained treaty across four repos whose only enforcement is prose — the
opposite of the special-case-dissolves-into-the-normal-case beauty the workspace
asks for.
