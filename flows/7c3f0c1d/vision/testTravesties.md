## 2026-08-19 — a test cannot bring in its own data and test it against production; remove the crap

Design session `7c3f0c1d`, typed (captured 2026-08-19T14:45+02:00), on the
report that Curriculum's `nix flake check` fails on `role-cross-product-manifests`
because the check hardcodes model names that `role-depths.dotos` no longer has:

> most of those tests are complete garbage. we should remove the crap. a test
> cannot bring in its own data and then test it against production. and the
> notion of testing if the production code conforms to itself is so stupid it
> can hardly be expressed in words. Im stunned at the stupidity of many tests
> that agents seem to conceive. I havent tackled this problem, but I will once
> we have a hold of the top stratum and more properly trained flows.

