# Build Readiness (Partial)

Two more results in:
- **CriomOS**: default `nix flake show` throws by design — `error: CriomOS: no system input was provided` (the `system` input is a `path:./stubs/no-system` stub that `throw`s until lojix overrides it at deploy time). So CriomOS is not independently evaluable without a materialized `system` override; the throw is intentional and self-documented.
- **forge**: no `packages.x86_64-linux.default` and no `checks.x86_64-linux` attributes — so my earlier "EVAL_OK" for forge was a vacuous "all checks passed" (no checks wired). Let me confirm forge's actual flake outputs, then finalize.