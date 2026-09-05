# Horizon implementation report

Horizon now exposes the approved generated Datom contract. Separate authored
`HorizonConfiguration` and `ClusterDefinition` inputs compose deterministically
through `horizon-compose` into one public `horizon-definition.datom`; consumers
decode `HorizonDefinition`, resolve the requested `(cluster, node)`, and project
only that selected node. A generic definition being present in the catalogue
does not establish membership.

The producer is released on Horizon main at
`05879e7c1e5f637f78fbe26234b95213c77c59bc`, version **0.6.0**. Remote Nix
checks for the default test package, default package, and `horizon-compose`
package passed at that revision.

The contract splits generic definitions from cluster selection without dropping
the previous domain facts. `Installation` carries persistent disk/layout data;
`Live` retains ordinary keyboard, compressed-swap, network, key, user, domain,
trust, machine, and capability facts. `MachineSpecies::Pod` was source-proven
to mean a VM guest and is migrated to `VirtualMachine`; no Container variant
was introduced. Virtual machines distinguish a cluster host from an authored
external host, and preserve the source-faithful single-hop architecture
inheritance rule. Typed `VmTesting` is distinct from `TestVm`.

Projection behavior retains the audited cluster-qualified empty-domain fallback,
GitHub-ID-to-username fallback, derived builders/caches/keys/user groups and
editor defaults, and opaque secret references rather than public secret values.

CriomOS source consumers are in
`8bbc75d3f2d1ed9a42a5063304083665b03b7c33` on
`horizon-module-consumer-fix-542442`. They read the actual projection directly:
scalar magnitude, lower-camel capability tags, `Wifi4`/`Wifi6`/`Wifi7`,
`fs_type`, `maximum_guests`, and `guest_subnet`; they do not reconstruct the
old proposal shape.

The composition artifact used for materialization is the immutable canonical
child `/nix/store/q8wmy9z7yr0igrbm8kvn3i8icvm4jsdh-horizon-definition/horizon-definition.datom`.
With `(goldragon, ouranos)`, `BaseHost`, and `NoSecrets`, Lojix materialized the
four caller-owned Nix inputs `system`, `horizon`, `deployment`, and `secrets`
and successfully evaluated the resulting CriomOS target. The final coherent
consumer BuildOnly gate is recorded in the Lojix report.

The final paired Lojix consumer is 0.21.0 at
`59293764e02e0fb0ec9251f382e627787420f30d`. Its behavior-complete Datom/Signal
and materialization revision is `d4404aad0d9418e29ebbbc8042c1684276bb3dcd`;
the final child corrects only retained-v4 inspector and public type
documentation. Horizon's producer release and composed artifact contract are
unchanged.
