<!-- to-the-living:start -->
Presentation.{ «Lojix, the broad vision» }

```
        CriomOS
           │
   ┌───────┴────────┐
 Criome-specific   the rest
                      │
                  Lojix OS
                      │
    Lojix, a Datom language
    spoken to the Lojix nexus
                      │
      Ethos shorthands for builds
```

In production a Lojix nexus deploys, pins and
tests through its two sockets. Lojix OS, the
language and the shorthands are vision only, for
later.

## 1. A new vision skill

`psyche-skills/skills/vision-lojix.md`, new file.

```diff
+ ---
+ description: Lojix — the Datom language spoken
+   to the Lojix nexus, Lojix OS, or Ethos build
+   shorthands — is designed or judged against
+   what the living wants.
+ dependencies: [vision-datom, vision-ethos]
+ ---
+
+ Lojix is the answer to Nix: a domain-specific
+ language specified in Datom, how one talks to
+ the Lojix nexus.
+
+ Lojix OS is the part of CriomOS that is not
+ Criome-specific, extracted.
+
+ Ethos gains shorthands for builds: one-off build
+ scripts, packages, and build options that can
+ be overridden.
+
+ Lojix eventually takes care of the deployment
+ operation: next, stable and last.
+
+ ## Sources
+
+ ebbe30 lojix
+ ebbe30 deployment
+ e1953c nexus
```

**Ruling 1.** (a) Land as shown. (b) Amend by line.
<!-- to-the-living:end -->
