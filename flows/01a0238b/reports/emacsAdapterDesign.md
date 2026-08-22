# Emacs adapter design

## Outcome

Create a public `chroma-emacs` repository. It provides Emacs feature
`chroma-theme` and global `chroma-theme-mode`. Chroma remains the sole semantic
light/dark authority; the plugin is the sole Emacs projection; `criomos-home`
owns Ignis generation and declarative deployment.

## Ownership

| Owner | Contract |
|---|---|
| Chroma | Desired Light/Dark state, persisted monotonic revision, D-Bus publication, and per-consumer projection status |
| `chroma-emacs` | Subscribe, reconcile, apply, verify, and acknowledge Emacs theme projection |
| `criomos-home` | Pin and native-compile the plugin, supply theme symbols and load paths, enable the mode, and generate Ignis themes |

## D-Bus protocol

Registration returns the current desired theme and revision. Chroma signals
later desired-state revisions. The plugin reports an applied acknowledgement
or a typed bounded failure for that revision. Chroma exposes each consumer as
`Pending`, `Applied`, `Unavailable`, or `Failed` without allowing an absent
Emacs process to block other projections.

The revision persists across Chroma restart. The plugin subscribes before it
registers, reconciles the returned snapshot, re-registers after service-owner
change, ignores stale revisions, and treats duplicate current revisions
idempotently. A duplicate still checks the postcondition so drift can converge.

## Emacs behavior

The plugin maps semantic Light and Dark values to declaratively supplied Emacs
theme symbols. It resolves and loads the target, disables only the opposite
Chroma-owned theme, preserves unrelated overlay themes, verifies the resulting
theme state, and acknowledges only after the postcondition holds.

Full Lisp diagnostics remain local to Emacs. Chroma receives a typed failure
and bounded summary. A semantic loading failure remains visibly failed rather
than being hidden by an infinite retry loop; transport recovery and restart
reconciliation remain automatic.

The plugin does not schedule themes, generate palettes, embed setup-specific
paths, own Ignis assets, or disable unrelated themes.

## Repository and proof boundaries

The new repository exposes a Nix package and checks. Its ERT and isolated-daemon
tests use a fake D-Bus peer to prove Light-to-Dark and Dark-to-Light projection,
late startup, reconnect, duplicate and stale revisions, preservation of
overlays, rollback or preservation on load failure, and typed reporting.

Chroma owns protocol tests for snapshots, persisted revisions, registration,
status transitions, stale acknowledgements, and restart. `criomos-home` owns
the real end-to-end Nix witness with built Chroma, generated Ignis themes, and
an isolated Emacs daemon; it observes both `custom-enabled-themes` and a
representative rendered face.

## Implementation order

1. Create and prove the public `chroma-emacs` package against a fake D-Bus peer.
2. Implement and prove Chroma's D-Bus theme and consumer-status contract.
3. Pin both in `criomos-home`, remove Darkman and the one-shot `emacsclient`
   projection, and add the end-to-end check.
4. Pin, deploy, and separately witness evaluation, activation, live theme
   transitions, and restart reconciliation.

No parallel compatibility path is retained.

## Sources

- `flows/01a0238b/vision/emacsPlugin.md`
- `flows/01a0238b/witnesses/transcriptProvenance.md`
- `flows/01a0238b/witnesses/sourceBoundaries.md`
- Flow `01a020ff`
- Bead `primary-77d`
