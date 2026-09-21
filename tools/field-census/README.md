# Field census service

For a one-shot, lightweight overview for a living flow, run:

```sh
node tools/field-census.mjs --overview
node tools/field-census.mjs --overview --json
```

This mode reads one Herdr agent roster and the HM registry for the
`messaging-build` session (override with `FIELD_HERDR_SESSION` and `HM_REGISTRY`).
It counts Herdr agent records, exact HM routes, unmatched Herdr records, and
unmatched registrations separately. Exact means the session, pane, terminal,
name, and harness all agree. The snapshot is timestamped; an unmatched
registration only describes this observation, not a retired Flow. Lifecycle is
Herdr's observed status, and availability, task, blocker, role, and context
remain unknown where no explicit evidence was supplied. The JSON includes
route bindings for machine use; the Markdown view omits them. This command
does not read transcripts or terminal screens, contact peers, or schedule work.

`field-census.mjs` observes Herdr panes and agents, exact HM bindings, terminal
status, transcript availability, Orchestrate lock owners, host health, and the
Nix daemon. It never closes a pane, launches a seat, or wakes an agent.

`field-census-cycle.mjs` atomically writes the full JSON snapshot to
`~/.local/state/field-census/latest.json`. It sends a short pointer to the
configured Field Low and Ultra Low Flow IDs every `notify_seconds`, after HM
revalidates each exact live route. A failed or uncertain submission creates a
durable hold in `notification-state.json`; an operator must reconcile that
state before any retry. A preexisting `cycle.lock` also requires inspection
before removal.

The deployed timer samples every five minutes. The initial notification
interval is 30 minutes. `recipients.json` is operational state, updated at
each verified Field Low or Ultra Low transfer; stale routes fail closed.

Example `~/.config/field-census/recipients.json`:

```json
{"sender_flow_id":"9ddcbc","field_low_flow_id":"0347d0","field_ultra_flow_id":"c88918","notify_seconds":1800}
```

The snapshot reports observed bindings, including old crossovers. It does not
claim a binding is a ready main, or classify any pane as safe to reap. Wake
policy belongs to the Mind checkup controller and is disabled here.
