# Final published-source inventory

This is a read-only audit of the named, published Git objects. I queried each
repository with `jj log -r <object>` and `jj log -r main@origin`, then read the
object's `Cargo.toml` and `Cargo.lock` with `jj file show`. It does not treat a
worktree's `@` as a release source. Audit lock: `899 FinalSourceInventory`.

## Published objects and effective direct pins

All named producer revisions below equal their repository's `main@origin`,
except where the table explicitly says otherwise. The codec and Protos source
objects themselves also equal `main@origin`:
`datom-codec` `41a3c073d5c5cdcb3ebb1a5c842e8c068145fdb2` (0.21.0) and
`protos` `2d999f1733347b7e64e24b2f75ba889ad7182bc0` (0.26.0).

| Published repository/object | Effective current-codec inputs at that object |
| --- | --- |
| `horizon-rs` `05879e7c1e5f637f78fbe26234b95213c77c59bc` | Direct Cargo and lock pins: Datom `41a3c073…`, Protos `2d999f173334`, Ethos-zero `341c5c57e45d98ee7d8a88d9b5746d3f50b16683`. |
| `lojix` `7e29c37f51092e5a20abf88c670aabd2acee6e52` | Direct Horizon `05879…`, Datom `41a3c073…`, Protos `2d999f173334`, ordinary Signal `5ce3…`, owner Signal `55c1…`, and signal-frame `80f70d…`. Its resolved lock has Ethos-zero `341c5…` through Horizon and `bcf728…` through the two Signals. |
| `signal-lojix` `5ce3f11feac22a0ddbed028dec2a60385f77fa55` and `meta-signal-lojix` `55c1df20ddfa6ae99e0f4bca57b803bf366b781f` | Both directly pin Datom `41a3c073…`, Protos `2d999f173334`, and build with Ethos-zero `bcf728bbe4521e663f4773d3c1fd4ebb643df32e`. |
| `orchestrate` `ac8a92666f4abd8356522c4d52ab23ddcdff4c15` | Direct Datom `41a3c073…`, Protos `2d999f173334`, Ethos-zero `a0c0548a73f1b6350d4267416b4109304888d67e`, ordinary Signal `5c28…`, owner Signal `8ccb…`, and signal-frame `80f70d…`. |
| `signal-orchestrate` `5c28bbf7ec4cb4d58c26a24e82948a7a9218794b` and `meta-signal-orchestrate` `8ccb5c2d07628f3fed0158eae12b5834786f0791` | Both directly pin Datom `41a3c073…` and Protos `2d999f173334`; their checked generator dev pin is Ethos-zero `a0c054…`. |
| `synchronizer` `b42c9df295adccdd65381f8bd444147099036183` | Direct Datom `41a3c073…`, Protos `2d999f173334`, Ethos-zero `341c5…`, and Horizon `05879…`. |
| `relative-age-display` `99d184541ed8b71daeafd44f025cdaafe7ecef82`, `chroma` `c9c11a5b5724bc28e402a48615c2f0d1a7b40813`, `chronos` `a5cf51f440a722c60963a5f1a0ea95bb3251ddb0` | Each Cargo lock resolves Datom `41a3c073…` and Protos `2d999f173334`; each has the checked generator/test pin Ethos-zero `bcf728…`. |
| `clavifaber` `2203f677d3448d99269d66386d35683cd10a05ef` | Direct Cargo and lock pins: Datom `41a3c073…`, Protos `2d999f173334`, and generated Ethos-zero `bcf728…`. This is current `main@origin`, not the earlier feature parent `8ed3…`; it removes the direct legacy Dotos dependency from the active package and public-file writer. Kameo `f491…` remains a separate actor-runtime input. |
| `claude-answers` `3a14cb12f885932de35a7ef7793e8a99a796c67f` and `curriculum-deploy` `7cc3cb53a10ab6ada383ea647c1ac87d1409266d` | Each directly resolves Datom `41a3c073…`, Protos `2d999f173334`, and test-generation Ethos-zero `341c5…`. |
| `criomos-horizon-config` `7050afef14bcfe649c0d05bdaa681d1577cafc46` | Declarative composition library only: no Cargo codec dependency. It invokes its explicitly supplied `horizon-compose` on separate configuration and cluster artifacts and writes `horizon-definition.datom`. |
| `goldragon` `1f49f8dea50932cacc781d531c48b6d20805b439` | Its published flake pins Horizon `05879…`, external configuration `7050…`, and Synchronizer `b42…`; its cluster input is data, not a Rust codec dependency. |
| `signal-ethos-zero` `42df8e3c648951f66fb754844369a8646b21bbdd` and `meta-signal-ethos-zero` `6b32b72dbfcfd236261399035e4827aad77b79fe` | Both directly resolve Datom `41a3c073…`, Protos `2d999f173334`, and build/test with Ethos-zero `bcf728…`. They publish distinct shared-frame identities 7/4 and 8/4, respectively. |

The verified source identities are therefore current codec and Protos throughout
this published set. Different Ethos-zero revisions are explicit dependency pins
with current Datom/Protos beneath them; they are not an old `datomic`/Dotos
fallback.

## Ethos source identity and the offline exception

There are three repositories here:

- Generator: `https://github.com/LiGoldragon/ethos-zero`.
- Ordinary Signal: `https://github.com/LiGoldragon/signal-ethos-zero`.
- Meta Signal: `https://github.com/LiGoldragon/meta-signal-ethos-zero`.

`bcf728…` is a published generator object and remains the intentional consumer
pin for the structural Signal generators. It is **not** the current
`ethos-zero` `main@origin`: that is
`87a30492a4a2abcb7658ceed1c5fa5c07d48b37c`; `7b016…` is its immediately
preceding published Nexus-runtime main, and `bcf728…` is an ancestor of the
current main. The older Nexus runtime is also not a separate repository. It is the
`nexus/` package history inside that same `ethos-zero` repository; current
main contains its `nexus/src/bin/ethos-zero-migrate-v1.rs`,
`nexus/UPGRADES.md`, and migration tests.

That legacy handling is deliberately scoped to the offline v1-to-current store
migration reader. It retains an old source and emits a separate current store;
it is not a serving compatibility fallback. The original source inventory did
not rerun the preexisting `7b016…` gate. The subsequent binding repair is
published at `ethos-zero` `87a30492a4a2abcb7658ceed1c5fa5c07d48b37c`; its
attached remote `nix flake check --option max-jobs 0 --option builders
'@/etc/nix/machines' --option fallback false` returned `all checks passed`.
It repins the Nexus and both CLI derivations to the published 7/8 Signal pair.

## Ancestry and pending integrations

The known history-preservation cases remain published: Lojix `7e29…` is the
history-preserving merge retaining former main `46585…`, and Synchronizer
`b42…` is the published merge retaining its tested feature tree and former
main ancestry. ClaviFaber `2203…` is a forward-only successor of the first
migrated producer, not a detached feature reference. Every other named
revision above was checked as the actual `main@origin` object, rather than
inferred from a detached checkout.

## CriomOS package-set and kernel provenance correction

The immutable pre-flow CriomOS object is
`59d12e6fc664c8be0f8dc8af2846c81abdf860cb`; the flow candidate is
`f59d12116a19e8a44325fc9d97d64cccd06357c7`; the C6 owner reference is
`add8a445052e9517a10eff7877ed7608aca871b2`. I compared their committed
`flake.nix` and `flake.lock` files with external's fully resolved add8 lock at
`/tmp/c6-add8-overridden-resolved.lock`.

All four graphs map `root.inputs.nixpkgs` to lock node `nixpkgs_3`, the
immutable object `LiGoldragon/nixpkgs@0e251e24a4f24e036a084b6b4b2d2491af4167f4`.
They also preserve the same follows edges:

- `criomos-home.inputs.nixpkgs = [ "nixpkgs" ]` and
  `criomos-home.inputs.pkgs = [ "pkgs" ]`;
- `pkgs.inputs.nixpkgs = [ "nixpkgs" ]`.

The target callsite is unchanged across the three CriomOS objects:
`inputs.nixpkgs.lib.nixosSystem { inherit pkgs; ... }`, with
`pkgs = inputs.criomos-home.legacyPackages.${system}`. The pre-flow Home
`9c8…` and current Home `e717…` both derive that exported value from
`inputs.pkgs.pkgs.extend (...)`; their own `nixpkgs` and `pkgs` inputs use
the same follows declarations. Thus the target's NixOS library and supplied
package set both resolve through the root `0e251…` input in the actual graph.

The lock also contains a separate `NixOS/nixpkgs@f83fc3c307e74bc5fd5adb7eb6b8b13ffd2a36e1`
node. It is not the root input pointer or the Home/Pkgs follows target for this
target construction, so it cannot establish the target's package or kernel
baseline. The pre-flow-to-f59 lock changes Home and consumer revisions, but
neither `nixpkgs_3` nor these follows edges; add8's committed lock is bytewise
identical to f59's. No parent/follows or effective package-input change in
this flow explains a kernel movement.

The current actual ownership check selected kernel `7.1.8`. This source audit
does not reconstruct a pre-flow kernel derivation, and therefore does not
claim a `7.0.9` to `7.1.8` transition. With the same effective root input and
package-boundary source expressions, any such claim needs a separately
captured exact pre-flow derivation/control rather than the unselected `f83…`
lock node or a manually rewired harness.

CriomOS Home, CriomOS, and CriomOS test-cluster remain feature-integration
work, not evidence that their older published mains missed this migration. The
current Home feature is `e71729ec6ebccce9d853227aea549712344a743c`. The
current CriomOS feature is `de02ef17a47fd92ae7f38b1c32330a42b6066330`, with
`lastModified=1788675700` and
`narHash=sha256-H4TR3gal5vXxLy9vdmyuS580I8liV9uccTU570WRb1Q=`. It pins
ClaviFaber `2203f677d3448d99269d66386d35683cd10a05ef`; its focused remote
publication gate passed, including direct `publication.datom`, typed reply,
mode 0644, absent legacy basename, and idempotency. The exact resolved-graph
ownership check — not the rejected raw-f83 experiment — built remotely to exit
0 as `/nix/store/hbh54ji2adw2r6dfkjs77mhawsbs4kh2-lojix-ownership.drv`,
producing `/nix/store/z7wd79vknmdmyjk2ybrik78lq21i54j4-lojix-ownership`.

The root-alias correction remains material: these checks select the locked
`0e251…` package graph, not the separately present raw `f83…` node. Fresh
BuildOnly invocations use immutable Lojix
`7e29c37f51092e5a20abf88c670aabd2acee6e52#lojix-bootstrap`, `NoSecrets`,
fresh caller-owned journal/GC-root/terminal paths, and no activation. Mercury
`(fieldlab, mercury)` BaseHost returned exit 0 and
`BootstrapTerminal.Succeeded` for
`/nix/store/bix0y5slnhh16ggc6gp9qlyb5xlln9gp-nixos-system-mercury-26.11.20260813.0e251e2.drv`,
producing
`/nix/store/yjbywpb126djjpq8h56hbax58f3gi55l-nixos-system-mercury-26.11.20260813.0e251e2`.
Its journal and terminal SHA-256 values are
`37d87cd51a62c4794e7d0bec1ba17b65554669f9eee524103240764ecf729d54` and
`57a54338cbe8b5f8d384111138d1ccc0d0b2ba35b7021e9841464f055004e2e9`.
Ouranos `(goldragon, ouranos)` CompleteHost likewise returned exit 0 and
`BootstrapTerminal.Succeeded` for
`/nix/store/9fdvm7zkyqkqmawas11lxyksyz6fnjg0-nixos-system-ouranos-26.11.20260813.0e251e2.drv`,
producing
`/nix/store/z5hhwav5zw1ia8k9ajhpmqmqbdzd9ly3-nixos-system-ouranos-26.11.20260813.0e251e2`.
Its journal and terminal SHA-256 values are
`c1a53a76c1985850082b7a3fc3df10b6e7714790995eb05223bb1f791847072b` and
`8c87499d4e79bf8df8cc74a3c7560d43d6fb731e35c97397c45a06d1e6c6cdaf`.
All four generated input directories are mode 0700 and terminal evidence is
mode 0600.

External's current C6 candidate is
a76b76e5c18d4c71554933b8fd3ef003375d0610. Its five non-C6 exact outputs
(projections, both negative cases, cluster-contracts, and full-module-contracts)
are valid remote-signed paths. C6 itself has no valid output yet: its exact
`9kzf1…` derivation remained unbuilt after the preceding combined command
ended without a C6 terminal result, and a fresh attached remote-only C6 build
is running. Home, CriomOS, and test-cluster mains remain held for combined C6
acceptance. The aggregate CriomOS check is also not claimed passed while the
unrelated strict MS2130 kernel-review assertion remains tracked as
`primary-5pq`. Relative-age-display and Chronos have no Home/OS owner in this
stack. This source audit does not infer C6 terminal success or any activation.
