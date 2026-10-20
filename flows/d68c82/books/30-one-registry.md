<!-- to-the-living:start -->
Presentation.{ «One registry of builds» }

# One registry of builds

```
 any machine
 +------------------------+
 | only the profiles in   |
 | use here; no other     |
 | links to builds        |
 +------------------------+
     |  builds and fetches
     v
 +------------------------+
 | the remote builder's   |
 | store                  |
 | roots: its own system  |
 | + one registry profile |
 +------------------------+
     |  daily
     v
 +------------------------+
 | least recently used    |
 | builds removed until   |
 | the store fits         |
 +------------------------+
```

## The builder's store today

| | value |
|---|---|
| disk | 1.9 TB, 787 GB used |
| builds in the store | 98,200 |
| leftover links holding builds | 84 in home and evidence folders, 10 from source checks |
| daily cleanup, last night | 6.7 GB freed |

Nix keeps no record of when or how often a build is used. The one trace is the last time a file was read, updated about once a day. One existing tool, nix-heuristic-gc, removes builds in that order, through Nix's own cleanup. How often a build is used needs a counter of our own: the cache server's request log can be it.

## Proposal 1: where builds live

File: psyche-context/skills/vision-builds.md, new

+ ---
+ description: Builds are made, kept or collected.
+ dependencies: []
+ ---
+
+ ## Builds
+
+ Builds live in the remote builder's store. A machine keeps links only to the profiles in use on it. A build worth keeping is listed in one registry profile; every other build is collected by how recently and how often it was used.

Ruling: land, amend, or reject.

## Proposal 2: no leftover links

File: field-context/skills/compensation-nix-workflow.md, at the end

+ No build or check leaves a link to its result; a link exists only for a profile in use on its machine.

Ruling: land, amend, or reject.

## Proposal 3: the builder collects by recency

File: CriomOS modules/nixos/nix/builder.nix

On the node whose cluster data makes it the dedicated builder (remote builder and center; today Prometheus alone): one registry profile; the leftover links removed; nix-heuristic-gc runs daily after the existing cleanup and removes the least recently used builds until 1 TB of the disk is free.

Ruling: land, amend, or reject.

## Proposal 4: counting use

File: CriomOS modules/nixos/nix/cache.nix

On the node whose cluster data makes it the Nix cache (today Prometheus): Harmonia replaces nix-serve, and its request log is counted per build each day, so frequency of use joins recency in the order of removal.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
