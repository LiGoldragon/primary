# 54 · psyche decisions (2026-06-16)

The lojix test op + multi-host model — open decisions resolved:

- **A — additive `super_nodes`** (not widening `super_node` to a `Vec`): single-host
  nodes project byte-identically; the host-set is `{super_node} ∪ super_nodes`.
- **B — image-exchange SCOPED to the declared hosts** (NOT cluster-wide): the
  per-node scoped signing-key emission is load-bearing — a host trusts another's
  signing key only where they co-host a node, a tighter boundary than the
  cluster-wide pool. "Declaring it on these hosts gives THEM permission."
- **C — `TestMode [Hermetic Live]`** (no `Both` for now; run separately).
- **D — the shorthand `Check` defaults the cluster too** (from `TestDefaults`),
  so `(Check mercury)` is the routine form.
- **E — async `AcceptedTest` handle + a queryable durable result** as the base;
  the quick `Check` shorthand returns a blocking verdict for routine use.

## Implementation order

1. **Unit 1 — horizon** multi-host (`super_nodes` + `host_set`) + the SCOPED
   image-exchange projection + the host-set/single-arch invariants
   (horizon-test-vm branch). *(building)*
2. **Unit 2 — the lojix op**: the `Test` meta-op + `Check` shorthand + the
   `TestDefaults` config in the signal/meta-signal schema; the daemon handler +
   the hermetic dispatch (`NixBuild` the `vm-<node>` check) + the `TestRunTable`
   and `(ByTestRun …)` query (closing observability); the live
   `BringUpTestVm`/`TearDownTestVm` effects built but NOT run live. → lojix main
   (the triad rule, o5rz). The hermetic path is proven end-to-end; the live run
   is gated.
3. **Unit 3 — CriomOS**: emit the scoped image-exchange keys as
   `extra-trusted-public-keys` from the node's host-set.
4. **(gated)** the Prometheus goldragon `VmHost` edit + the first live run —
   psyche-gated.

## Related

Report 53 §1 (the auto-pickup suite) is DONE — `dune` (an Edge Pod with no test
before) auto-gains a full Edge check, review PASS (CriomOS-test-cluster
horizon-test-vm `46febf36`). The auto-pickup checks are the hermetic engine the
lojix `Test` op dispatches to.
