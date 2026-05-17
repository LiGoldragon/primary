# 132 — Horizon Domain Suffixes Are Constants, Not Cluster Data

*Audit correction for `reports/designer-assistant/102-horizon-leaner-shape-downstream-pickup-2026-05-17.md`. The earlier review found `goldragon/datom.nota` already carries `"criome"` and `"criome.net"`. The user corrected the premise: those literals should not be in cluster-authored data at all. This report records the corrected architecture and the downstream pickup shape.*

## Finding

`"criome"` and `"criome.net"` are implementation constants of the Horizon/CriomOS ecosystem. They are not facts about the `goldragon` cluster and should not be authored in `goldragon/datom.nota`.

The current `horizon-rs` shape violates that boundary:

- `ClusterProposal` has `domain: ClusterDomain` and `public_domain: PublicDomain`.
- `ClusterProposal::project` threads `self.domain` into node domain derivation.
- `ClusterProposal::project` threads `self.public_domain` into user email and Matrix identifier derivation.
- `goldragon/datom.nota` currently ends with `"criome"` and `"criome.net"` to satisfy those fields.

That makes the cluster repository carry constants that belong to the projection engine. Another cluster using CriomOS should not be able to choose a different internal suffix by editing cluster data unless the platform has explicitly grown a supported domain-policy axis.

## Correction To Report 102

Report 102's section 2.4 says the `publicDomain` value is "missing" from `goldragon/datom.nota` and must be added before end-to-end projection can smoke.

Corrected reading:

- The old report was right that the current schema expects the value.
- The old report was wrong to treat adding `"criome.net"` as the architectural fix.
- The present `goldragon/datom.nota` tail containing `"criome"` and `"criome.net"` is a workaround for a misplaced schema field.
- The real fix is to remove those fields from the cluster proposal input and make Horizon supply typed constants during projection.

## Desired Shape

Horizon owns the fixed suffix policy:

- internal cluster domain suffix: `criome`
- public user-facing domain suffix: `criome.net`

The exact Rust shape can be either:

- a small constants module that exposes typed constructor helpers, or
- associated constructors on `ClusterDomain` and `PublicDomain`.

Because the newtypes currently wrap `String`, typed `const` values are not directly ergonomic. A clean implementation is:

```rust
impl ClusterDomain {
    pub fn criome() -> Self {
        Self("criome".to_owned())
    }
}

impl PublicDomain {
    pub fn criome_net() -> Self {
        Self("criome.net".to_owned())
    }
}
```

If the constants are likely to grow into a named policy, introduce a `HorizonDomainPolicy` value instead. For the current system, plain typed constructors are enough and keep the projection boundary simple.

## Required Code Changes

### `horizon-rs`

Remove these fields from the proposal/input boundary:

- `ClusterProposal::domain`
- `ClusterProposal::public_domain`

Replace their uses in projection:

- `NodeProjection.cluster_domain` should receive `ClusterDomain::criome()`.
- `UserProjection.cluster_public_domain` should receive `PublicDomain::criome_net()`.
- `view::Cluster.domain` should be populated from `ClusterDomain::criome()`.

Add tests that make the boundary explicit:

- a `ClusterProposal` fixture without trailing domain literals decodes and projects;
- projected node domain remains `<node>.<cluster>.criome`;
- projected user email/Matrix identifiers remain `<user>@<cluster>.criome.net` and `@<user>:<cluster>.criome.net`;
- projection tests fail if the proposal schema starts requiring a domain suffix again.

Update stale docs/skills that still present these as cluster-authored fields.

### `goldragon`

Remove the two tail literals from `datom.nota`:

- `"criome"`
- `"criome.net"`

After the `horizon-rs` schema fix, their presence should be unnecessary and preferably invalid.

### `lojix`

Lojix should only need the `horizon-lib` input bump and lock refresh after the `horizon-rs` change. It should not author, pass, or patch domain suffixes.

### `CriomOS` / `CriomOS-home`

Downstream Nix should continue reading projected fields such as `node.criomeDomainName` and `cluster.domain`. The change is upstream of those projected values. Nix should not introduce local `"criome"` or `"criome.net"` fallbacks.

## Related Smell

`tailnet.baseDomain` currently appears in test fixtures as values like `tailnet.goldragon.criome`. If this is always derived from the cluster name plus the internal Horizon suffix, it has the same smell and should become a derived field. If tailnet needs a configurable DNS suffix independent of CriomOS' internal domain, that must be named as a real policy axis rather than smuggling the internal constant back into cluster data.

This is not required to fix the immediate `domain` / `public_domain` leak, but it should be checked during the same cleanup.

## Verification

The cleanup is green only when these witnesses exist:

1. `goldragon/datom.nota` no longer contains the two tail suffix literals.
2. `horizon-cli --cluster goldragon --node prometheus < datom.nota` still emits JSON.
3. The emitted JSON still contains node names under `.goldragon.criome`.
4. A projected user still receives the `.goldragon.criome.net` email/Matrix domain.
5. `rg -n '"criome"|"criome.net"' goldragon/datom.nota` returns no matches except unrelated prose comments if any remain.
6. `cargo test --jobs 1 --workspace -- --test-threads=1` passes in `horizon-rs`.
7. The downstream `horizon-leaner-shape` pickup report is amended or superseded so no agent adds the literals back as a "missing publicDomain" fix.

## Recommendation

Treat this as part of the `horizon-leaner-shape` wire break rather than as a follow-up compatibility patch. The branch is already breaking downstream JSON shape intentionally, and this is the same category of correction: move a derived platform fact out of cluster data and into the projector that owns it.

