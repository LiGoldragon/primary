# Nix Remote Ref Sweep - Frame and Method

## Trigger

The psyche rejected local Nix flake source references as a workspace pattern:
`--override-input ... path:/git/...` and local `path:` / `git+file://` refs in
flake inputs copy local checkout state, consume disk, and are not reproducible by
another agent.

The durable rule was recorded in Spirit as `ttbt` (remote-only Nix override
constraint) and reflected into `skills/nix-discipline.md`,
`skills/testing.md`, and `tools/nix-local-stack` in report 404.

## Method

I dispatched a background worker for the broad script/docs sweep and continued
locally on the behavior-bearing Nix code in `CriomOS-test-cluster`.

The sweep target was narrow:

- remove sibling-checkout `path:` overrides and examples;
- remove stale local-path advice in docs/scripts;
- keep behavior-bearing generated store paths visible rather than hiding them;
- test with Nix where possible;
- report unresolved cases that require a design decision rather than a
  mechanical rewrite.

## Local Work

The local implementation target was `CriomOS-test-cluster`'s generated deploy
flake. Before the fix, `lib/deploy-flake.nix` generated a synthetic flake whose
inputs were local `path:${...}` source trees. That shape no longer matches the
remote-only rule.

The new shape:

- generated deploy flake input URLs are `github:<owner>/<repo>/<rev>` from the
  parent `flake.lock` locked nodes;
- the generated deploy flake receives a copied `flake.lock` cut from the parent
  lock, so the offline VM test resolves by narHash;
- source trees remain explicit store dependencies for the hermetic deployer VM;
- `nix flake lock` no longer runs inside the offline builder.

Landed in `CriomOS-test-cluster` main as commit `34659ba1` (remove path refs
from deploy flake inputs).

