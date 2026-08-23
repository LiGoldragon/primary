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

## Completed source closure

Lojix `main` now points to immutable commit
`edbb53aab003a071ffbb0f6643e8d29c0bf9b691`, package version `0.18.0`.
That producer removes the timeout member from the startup archive and
configuration writer, removes elapsed-time enforcement from effect execution,
and uses the nine-field writer request. Its new writer test was first observed
failing against the old ten-field implementation. Formatting, the Dotos-text
all-target test suite, Clippy, Nix evaluation, and the remote-builder Nix
`fmt`, `test`, `clippy`, and `fresh-daemon-startup` checks passed.

The sole authored instruction change was pushed in Curriculum `main` commit
`6b5e67b8`, then regenerated in the consumer workspace in commit `d06bd6fa`.
The resulting instruction documents the nine-field request. Generation,
`check-skills`, and the Curriculum remote-builder Nix flake check passed.

CriomOS `main` now points to immutable commit
`a4322cd144821119936283339b1bc5926b97a738`, directly after
`93049a6e3eb7f66a23484402c96d835caa233b99`. It pins the same pushed Lojix
`main` commit and removes the Nix option, persona value, writer serialization,
check fixtures and assertions, and public timeout wording. Formatting and
parsing of every changed consumer path, lock revision/hash assertions, and
candidate-to-producer-main alignment passed. The producer startup check was
realized remotely with local jobs disabled.

Whole-CriomOS evaluation and realization are deliberately deferred, not passed:
they require four exact Lojix-materialized inputs (`system`, `horizon`,
`deployment`, and `secrets`). None was supplied, and repository instructions
forbid deriving, fabricating, or reusing an unspecified input tree. A future
authorized Lojix Evaluate for the selected controller node is the deployment
stage that materializes those exact inputs. No deployment, activation, daemon
restart, closure copy, state mutation, reboot, or garbage collection was
performed.

## Sources

- [implementation boundary witness](../witnesses/lojixTimeoutRemovalImplementation.md)
- [timeout provenance report](lojixEffectTimeout.md)
- [active flow log](../log.md)
- [completed source closure witness](../witnesses/lojixTimeoutRemovalImplementation.md)
