# External Horizon composition witness

## Ownership and dataflow

`criomos-horizon-config@7050afef14bcfe649c0d05bdaa681d1577cafc46` contains a
cluster-neutral public `HorizonConfiguration`; tested ancestor `1f58fc5` has
the identical tree and NAR hash. Goldragon
`1f49f8dea50932cacc781d531c48b6d20805b439` owns the independently authored
`ClusterDefinition`, including explicit generic-node selection. It is the
assembly owner; the generic configuration producer does not pin Goldragon.

```text
HorizonConfiguration + ClusterDefinition
       explicit immutable inputs
                 |
       Horizon typed compose/encode
                 |
  derivation directory/horizon-definition.datom
                 |
       Lojix ProposalSource (one regular file)
```

The composer is Horizon `05879e7c1e5f637f78fbe26234b95213c77c59bc`; it parses
both roots and produces `HorizonDefinition`, never a textual concatenation or
ambient lookup. Lojix `7e29c37f51092e5a20abf88c670aabd2acee6e52` decodes that
root, resolves `(cluster, node)`, and projects only after selected generic
names have been applied.

## Canonical public artifact

Goldragon’s final artifact is the immutable canonical child:

`/nix/store/0in67wflv4rxnylf4hbpdmni3m5as4sl-horizon-definition/horizon-definition.datom`

Its public bytes are 5,987 bytes and SHA-256
`eac13fa803fa8db358dfd03fc9a7c1a74bca27970b37008be4eccc9873322947`.
The directory shape supplies Lojix’s required exact basename without copying
or a sibling search.

Catalogue availability does not imply cluster membership. Composition/resolution
rejects unknown selected names and local/generic name collisions. The document
contains public fields and opaque secret references only; privileged private
material is supplied separately as `SecretsInput` and is not part of this
artifact.

Goldragon renders the current Synchronizer `ClusterRole` configuration with
the canonical child supplied as its `HorizonDefinition` source. Synchronizer
`b42c9df295adccdd65381f8bd444147099036183` decoded that rendered configuration
and resolved the composed data dynamically, selecting Prometheus from the
published candidates.
