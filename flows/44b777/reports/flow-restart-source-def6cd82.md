# Source for the next Flow restart: the audit-fix line plus e6b56575

Psyche criomos Secondary 44b777, 2026-11-06. This is source only: nothing is built or activated.

## Heads (pushed, new branches)

- CriomOS-home criomos-0513-base-44b777: def6cd82bb9c15af7ea3945af53bb0edeb1000f9. Its parents are 02a775ee (the live 256 Home: the audit-fix line plus d68b2865) and e6b56575eee782c2a19179074d6bb4e34a49432f.
- CriomOS criomos-0513-base-44b777: 8f8ead9da1b674fcf704730f3d3c27f33be4010a. Its parent is 994c107 (the live 256), and it changes only flake.lock, criomos-home 02a775ee to def6cd82. The lock's original URL stays bare.

## Full parent to target diff, Home 02a775ee to def6cd82

```diff
diff --git a/modules/home/profiles/min/flow-nexus-config/models.datom b/modules/home/profiles/min/flow-nexus-config/models.datom
index 0079d1a4..00f4f772 100644
--- a/modules/home/profiles/min/flow-nexus-config/models.datom
+++ b/modules/home/profiles/min/flow-nexus-config/models.datom
@@ -8,7 +8,7 @@ Configure.Models.[
   { Secondary Field gpt-6.1-sol }
   { Secondary Mind gpt-6.1-sol }
   { Secondary Psyche claude-opus-5-5 }
-  { Tertiary Field gpt-6-luna }
+  { Tertiary Field claude-sonnet-5-5 }
   { Tertiary Mind gpt-6-luna }
   { Tertiary Psyche claude-sonnet-5-5 }
 ]
```

Nothing else of main enters, because e6b56575's own parents, d68b2865 and 6f6eec61, are already on the line. Main holds nothing beyond e6b56575: `git log 02a775ee..origin/main` lists e6b56575 alone.

## Preserved, by construction, since the diff is that one line

- The 0.39 unit and its Message Nexus partner stay removed (77711f2b, 97099745).
- Curriculum and zoekt stay declared (12255918, 9e2d259c).
- The Wispr fix of 256 stays (d68b2865).
- Metaflows: the unit passes the mutable state file `~/.local/state/flow-declarations/metaflows.datom`, the same path as the live unit. No metaflow snapshot is in Home.

## Evaluated flow-nexus-0511 unit against the live unit

This was read from the evaluated derivation /nix/store/jrd33vinj1rw0ls1wcrg5289viiqvkc5-flow-nexus-0511.service.drv, without building. The generation derivation is /nix/store/6skn916g1f42wd2irsv8s2w9v4gkc9fk-home-manager-generation.drv.

```diff
10c10
< /nix/store/fm84vwp2k8hfzacm0lw04g61p6h437rb-models.datom
---
> /nix/store/wrfsfs3lx2vlg0hgimfpjklr002s1vsi-models.datom
11c11
<   { Tertiary Field gpt-6-luna }
---
>   { Tertiary Field claude-sonnet-5-5 }
```

Every other line of the unit is byte-identical; the evaluated text ends in one extra trailing newline. Switching to this generation changes the unit, so Home restarts flow-nexus-0511 at activation. It is therefore switched only at a Flow restart that Mind versionZero Primary approves.
