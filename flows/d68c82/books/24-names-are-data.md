<!-- to-the-living:start -->
Presentation.{ «A module names the role, not the host» }

# A module names the role, not the host

```
 cluster data (each setup's own)
     |
     v
 +------------------------+
 | node Prometheus        |
 | services: Center,      |
 | LargeAi, NixBuilder 8, |
 | NixCache, VmHost       |
 +------------------------+
     |  Horizon projects
     v
 +------------------------+
 | behavesAs.center       |
 | behavesAs.largeAi      |
 | isRemoteNixBuilder     |
 | isNixCache             |
 +------------------------+
     |  CriomOS selects on
     |  these, never a name
     v
 +------------------------+
 | a context module names |
 | the same role          |
 +------------------------+
```

## What selects Prometheus today

| role in cluster data | nodes that have it |
|---|---|
| behavesAs.largeAi | Prometheus |
| isNixCache | Prometheus |
| center and remote builder (CriomOS calls it dedicatedNixBuilder) | Prometheus |
| behavesAs.center | Prometheus, balboa |
| isRemoteNixBuilder | Prometheus, tiger |

CriomOS already chooses the build machine this way:

```nix
dedicatedNixBuilder =
  (node.isRemoteNixBuilder or false)
  && (node.behavesAs.center or false);
```

## Proposal 1: a variable is named by its role

File: psyche-context/skills/vision-context-modules.md, at the end

+ A context module names a host, a user, a path or any other value that differs between setups by the role or feature that selects it in the system's data, never by the value one setup gives it.

Wrong, then right:

```
- One store on Prometheus keeps the measures.
+ One store on the dedicated Nix builder
+ keeps the measures.
```

Ruling: land, amend, or reject.

## Proposal 2: the monitoring store gets its own role

The monitoring store has no role of its own in the cluster data yet.

File: goldragon/cluster-definition.datom, Prometheus's services

```
- NixCache.{} VmHost.{ ... } ]
+ NixCache.{} MetricsStore.{} VmHost.{ ... } ]
```

Horizon projects it as `isMetricsStore`; the monitoring module enables its store on that node, and every node's collector sends to it.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
