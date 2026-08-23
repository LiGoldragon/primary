# Lojix timeout removal implementation

## Result sought

Remove the wall-clock timeout from Lojix effects entirely. The new startup
configuration has no timeout member; an active effect is governed by its own
completion, cancellation, or concrete failure rather than elapsed time.

## Integration order

1. Land the Lojix producer: typed configuration/archive, writer, executor,
   behavioral tests, public version, and its documentation.
2. Regenerate and validate any authored-skill consumer changed for the shorter
   writer input.
3. Update CriomOS's Nix module, persona projection, evaluation checks, public
   architecture wording, and flake pin to the pushed producer ref.
4. Run independent Nix evaluation and remote-builder realization checks on the
   complete pinned consumer closure. These are build evidence only; deployment
   remains outside this subflow.

## Coordination state

The documented Orchestrate lane and claim forms were tried before writing these
flow records. The current local clients both returned `transport IO error: No
such file or directory (os error 2)`, so no advisory lane could be registered.
The pre-existing shared CriomOS main workspace is dirty on unrelated paths and
will not be used for this integration.

## Sources

- [implementation boundary witness](../witnesses/lojixTimeoutRemovalImplementation.md)
- [timeout provenance report](lojixEffectTimeout.md)
- [active flow log](../log.md)
