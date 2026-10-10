<!-- to-the-living:start -->
Presentation.{ «Next, stable, last» }

```
  next ──promote──► stable ──retire──► last
  (test            (what runs)      (fallback)
   deployment)
```

In production, Flow's nexus runs as stable and
Next; there is no last. Everything below is
design.

## 1. The three generations

`psyche-skills/skills/vision-deployment.md`, new
section before Sources, and one Sources line.

```diff
+ ## Next, stable, last
+
+ Every repository has a next branch: the test
+ deployment. The next-suffixed package or server
+ is built from it. Stable is what runs. Last is
+ the stable before it, kept as the fallback when
+ stable turns unstable, and to make the atomic
+ move smooth. Upgrading the NixOS layer changes
+ next, stable and last, not all at a time.
@@ Sources @@
+ ebbe30 deployment
```

**Ruling 1.** (a) Land as shown. (b) Amend by line.
<!-- to-the-living:end -->
