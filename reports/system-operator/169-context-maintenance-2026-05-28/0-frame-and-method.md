# Frame and Method

System-operator context-maintenance pass requested from
`reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/6-overview.md`.

The current system-operator lane has two simultaneous obligations:

- finish the active production Spirit observation-surface deployment without
  losing the in-progress code state;
- apply the system-designer cross-lane handoff for stale system-operator
  reports using `skills/context-maintenance.md`.

## Scope

This pass covers `reports/system-operator/` only. Other lanes' drops are left
to their owners.

The cited handoff says:

- drop `162`, `163`, and `165` cleanly;
- forward-confirm then drop `164`;
- forward-confirm then drop `156` through `160` into the cloud lanes;
- drop `161` if `166` fully supersedes it;
- keep `166`, `167`, and `168` as current;
- decide whether `139` should migrate to Arca's permanent docs or remain as an
  active architecture report;
- review old `1` through `7` for STT, NOTA, and Spirit history.

## Subagent Slot

`1-system-operator-inventory.md` is reserved for a read-only subagent audit.
The subagent checks the report set against the handoff and recommends exact
forward / migrate / keep / drop actions. The dispatcher executes only after
reviewing that audit.

## Active Work State

Do not lose the current production Spirit implementation state:

- `signal-persona-spirit` is already committed at `b222fb98` with the cleaner
  observation surface.
- `persona-spirit` has local edits and passing Cargo tests; it still needs
  `nix flake check`, commit, and push.
- `CriomOS-home` still needs the `persona-spirit-v0-3-0` input repin,
  check, and `HomeOnly` activation.
- `skills/spirit-cli.md` has local documentation edits that should be split
  into a scoped primary commit.

