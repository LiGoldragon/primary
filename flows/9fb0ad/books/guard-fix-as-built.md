<!-- to-the-living:start -->
Presentation.{ «The guard fix, as built» }

An addendum to «The deployment stopped at the first activation». The fix is ready on branches, built, activated nowhere; it differs from what that book proposed, so your numbers there need one line of reading.

## 1. What the guard was for

Its commits say it: the messenger links in `~/.local/bin` predate Home ownership; Home must not overwrite a binding it does not own, and the old hand-made shims were to be replaced during one migration only. That migration is finished. The bug is that "Home's own" was written as one pinned store path, so the guard stopped working at the next generation.

## 2. The fix as built

Not an admission rule for the generation being replaced, as proposed. The forced overwrite and the custom step are removed, and Home Manager's own link check guards the bindings: it replaces a link into any of its own generations and refuses a foreign file or a differing foreign link. That is the guard's purpose, keyed on generations rather than one path, with no compatibility branch. The package check was rewritten to assert it, with two passing and two refusing cases; green. A host still carrying the old shims would now refuse safely rather than be migrated.

The same patch sits on all four bases the plan needs: orchestrate 0.37, Flow and Message next, the regular slot, and main itself — because your current generation's own activation also refuses, the fixed main is the only rollback that will actually activate. All four generations are built; each new activation's link check was run read-only against your live home and passed.

## 3. How your numbers are read

Choices 1 and 2 of «The deployment stopped at the first activation» (fix, rebuild, activate all three / orchestrate first) are read as this fix. Choice 3 (remove the guard altogether) is in effect what this is, with Home Manager's own check kept. If you want the pinned-path admission shape instead, name 7.

One latent twin: the Herdr config is admitted by one pinned path the same way; it works today and will refuse when that config next changes. 8 = fix it the same way now, in the same branches; 9 = later.
<!-- to-the-living:end -->
