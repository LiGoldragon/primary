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
Herdr's observed status, and availability, task, blocker, and role remain
unknown where no explicit evidence was supplied. The JSON includes route
bindings for machine use; the Markdown view omits them.

For exact routes with a native thread ID, overview adds a `context` observation
with native usage, context window evidence, quota scope, timestamps, freshness,
and errors. Codex uses a read-only app-server `thread/read` for the exact path,
then reads at most 1 MiB of recent usage records from that rollout. Claude
reads at most 512 KiB of its exact-session transcript tail; a recent metadata
snapshot under `~/.local/state/field-census/claude-statusline/<session-id>.json`
takes precedence if one has been installed and published. Override that
directory with `FIELD_CLAUDE_STATUSLINE_DIR`. The supplied publisher is not
installed by this census command. No message content is returned. `context_tokens`
and `context_pct` are convenience fields; `context_quality` states whether a
number is exact or a proxy. Cumulative Codex tokens and account quota are
distinct from current context occupancy. Overview makes one read-only Codex
`account/rateLimits/read` request per snapshot, in parallel with per-thread
reads, and returns it as `account_quota`; a thread's older event quota is labeled
as such. Missing native evidence remains null.
This command does not contact peers or schedule work.

`field-census.mjs` observes Herdr panes and agents, exact HM bindings, terminal
status, transcript availability, Orchestrate lock owners, host health, and the
Nix daemon. It never closes a pane, launches a seat, or wakes an agent.

`field-census-cycle.mjs --observe-only` atomically writes the full JSON
snapshot to `~/.local/state/field-census/latest.json`. The installed service
uses this mode; its five-minute timer makes **no HM submission** and never
reads or changes `notification-state.json`. The thirty-minute shadow checkup
uses that snapshot passively. A preexisting `cycle.lock` requires inspection
before removal.

Invoking `field-census-cycle.mjs` without `--observe-only` retains the earlier
manual bounded-summary behavior: it sends a short pointer to configured Field
Low and Ultra Low Flow IDs every `notify_seconds`, after HM revalidates each
exact live route. A failed or uncertain submission creates a durable hold in
`notification-state.json`; an operator must reconcile that state before any
retry. `recipients.json` is preserved operational state, not timer input.

Example `~/.config/field-census/recipients.json`:

```json
{"sender_flow_id":"9ddcbc","field_low_flow_id":"0347d0","field_ultra_flow_id":"c88918","notify_seconds":1800}
```

The snapshot reports observed bindings, including old crossovers. It does not
claim a binding is a ready main, or classify any pane as safe to reap. Wake
policy belongs to the Mind checkup controller and is disabled here.
