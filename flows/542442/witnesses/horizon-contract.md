# Horizon contract witness

Horizon main `05879e7c1e5f637f78fbe26234b95213c77c59bc` is release 0.6.0.
Remote Nix gates passed for its default test package, default package, and
`horizon-compose`. Its public contract composes separately authored
configuration and cluster inputs into `horizon-definition.datom`.

The generated contract witness covers graphical and minimal Live definitions,
Installation disks and persistent swap, keyboard and compressed swap, router
and backup Wi-Fi opaque references, KVM availability, users/domains/trust,
external and cluster-hosted VMs, and generic selection. It rejects missing local
VM hosts, collisions, unselected generic nodes, and chained VM architecture
inheritance beyond the approved single hop. `VmTesting` retains its independent
host payload from `TestVm` guest identity.

Goldragon `1f49f8dea50932cacc781d531c48b6d20805b439` owns the canonical public
artifact and rendered Synchronizer builder source:

```text
ClusterRole.{ NixBuilder HorizonDefinition./absolute/horizon-definition.datom }
```

The cluster-neutral composer is
`7050afef14bcfe649c0d05bdaa681d1577cafc46`.

CriomOS candidate `de02ef17a47fd92ae7f38b1c32330a42b6066330` consumes current
Clavifaber `2203f677d3448d99269d66386d35683cd10a05ef`. Its remote publication
consumer derivation
`frx1mijxcaj78v7nm7vkiz043ahfypah-clavifaber-publication-request.drv` exited
0. The gate runs the module-generated `PublicKeyPublicationWriting` request,
checks its typed reply and direct `publication.datom`, preserves 0644 atomic
publication, proves idempotency, and rejects the retired `.dotos` basename.

Fresh normal BuildOnly witnesses use immutable Lojix
`7e29c37f51092e5a20abf88c670aabd2acee6e52#lojix-bootstrap`, BuildOnly,
NoSecrets, and no activation.

| Target | Definition SHA-256 | Derivation | Output | Journal SHA-256 | Terminal SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `(fieldlab, mercury)` `BaseHost` | `ed4ff2d23b87cf4f07bf928a7c7734d478e8a38cd709be59db972a6e3ccacd22` | `/nix/store/bix0y5slnhh16ggc6gp9qlyb5xlln9gp-nixos-system-mercury-26.11.20260813.0e251e2.drv` | `/nix/store/yjbywpb126djjpq8h56hbax58f3gi55l-nixos-system-mercury-26.11.20260813.0e251e2` | `37d87cd51a62c4794e7d0bec1ba17b65554669f9eee524103240764ecf729d54` | `57a54338cbe8b5f8d384111138d1ccc0d0b2ba35b7021e9841464f055004e2e9` |
| `(goldragon, ouranos)` `CompleteHost` | `eac13fa803fa8db358dfd03fc9a7c1a74bca27970b37008be4eccc9873322947` | `/nix/store/9fdvm7zkyqkqmawas11lxyksyz6fnjg0-nixos-system-ouranos-26.11.20260813.0e251e2.drv` | `/nix/store/z5hhwav5zw1ia8k9ajhpmqmqbdzd9ly3-nixos-system-ouranos-26.11.20260813.0e251e2` | `c1a53a76c1985850082b7a3fc3df10b6e7714790995eb05223bb1f791847072b` | `8c87499d4e79bf8df8cc74a3c7560d43d6fb731e35c97397c45a06d1e6c6cdaf` |

Each terminal reported `BootstrapTerminal.Succeeded` with exit code 0. Every
generated input directory is mode 0700 and each terminal evidence file is mode
0600. The final Ouranos generated `nix-daemon` unit includes `gitMinimal` in
its effective PATH, proving the scoped cold-Git dependency reached the actual
NixOS output.

The exact de02 ownership graph evaluates to the prior remote-passed
`hbh54ji2adw2r6dfkjs77mhawsbs4kh2-lojix-ownership.drv`; derivation equality
carries its exit-0 output `z7wd79vknmdmyjk2ybrik78lq21i54j4-lojix-ownership`.

The aggregate CriomOS check remains blocked by unrelated MS2130 kernel review
`primary-5pq`; it is not represented as passed. C6 remains the external-owned
combined final gate and is pending at this revision.
