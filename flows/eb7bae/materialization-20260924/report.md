# Fresh Horizon/Lojix materialization report

## Outcome

The current published graph cannot produce one Lojix materialization carrying
both requested facts.

Goldragon `8c4d03de76907f590072c0998b00037330ebcd82` materialized successfully,
using local jobs disabled and fallback disabled, to the immutable output:

`/nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom`

The output was copied from the Prometheus cache and its path-info carries a
`prometheus.goldragon.criome` signature. The canonical child is a mode-0444,
6079-byte regular file with SHA-256
`d280c719030bd066e23d1f003e804d73d699756dae18776114551cac201040e8`.

Fresh Goldragon/Horizon projections for both nodes exited 0. Prometheus has
`node.network.routerInterfaces`, with WAN `eno1`; it has no legacy top-level
`node.routerInterfaces`. Ouranos has `node.network.routerInterfaces: null` and
no `UsbIpv4Gateway` capability or string anywhere in its generated viewpoint.
The exact immutable Goldragon cluster source likewise contains zero
`UsbIpv4Gateway` literals. The missing Ouranos value is therefore an authored
producer-graph absence, not a projection or assertion failure.

## Lojix interface blocker

The supported installed Lojix client is Lojix 6.0.0 from the requested current
main `c4bba4fa12408c39ff745b0773468cd32a74403f`. It pins Horizon
`40d04d2504fee619e9b2b2564b8a769a3a9d6049`, horizon-lib 0.10.1.

The Goldragon producer instead pins Horizon
`ee8d6f8d27eb6e200504807971ffdd26aaca7ed1`, horizon-lib 0.12.0. Compared with
the Lojix pin, that producer adds the `OpenCodeTesting` node-capability variant
and changes fixed-location fields from `f64` to `datom_codec::Decimal`. The
materialized Ouranos definition actually contains `OpenCodeTesting` and fixed
location values.

A disconnected, exact `Deploy.Host` Horizon request against the generated
child exited 2 before socket exchange:

`(CliRejected [Datom request did not decode: proposal source is not a Horizon definition])`

Thus Lojix cannot enter its `MaterializeHorizon` effect for this producer
artifact. There is no supported materialize-only Lojix CLI: the daemon path
materializes after accepted deployment admission, while the maintained
`lojix-bootstrap` `BuildOnly` path proceeds from materialization into a system
build and GC-root creation. Both are outside this lane's no-deployment/no-build
boundary, and the decoder mismatch precedes either one in this graph.

## Pin verification

At the first remote-main check, the requested CriomOS, CriomOS-home, Lojix,
and Goldragon revisions all matched GitHub `main`. During this run,
CriomOS-home advanced by one descendant commit to
`50757d395b5a501f2bd97d39daae717ee6f556a3`; the requested
`09cace84f11d56e1d4299e4921942c5fbfb0211e` remains its merge base and an
immutable valid pin. CriomOS, Lojix, and Goldragon remained at the requested
remote-main revisions when captured in `generated/pins.json`.

The reported Horizon `40d04d2504fee619e9b2b2564b8a769a3a9d6049` is verified
as Lojix's exact pin, not Horizon's current remote main. Horizon remote main was
`b45d6ad48b5ee5d28eb0127f17c6e0084b696e60` at capture time.

## Evidence boundary

This is composition, projection, schema, and disconnected decoder evidence.
It is not a Lojix materialized input set, OS evaluation/build, deployment,
activation, service action, VM test, or live-host proof. No repository,
foreign lock, service, socket, host configuration, or secret was modified or
read. The retained Lojix worktree and locks were not touched.

The bounded next producer requirement is a published Goldragon revision that
actually assigns `UsbIpv4Gateway` to Ouranos and pins a Horizon schema accepted
by the intended Lojix revision, followed by a correspondingly published Lojix
decoder pin. Only then can supported Lojix materialization produce the combined
shape.

