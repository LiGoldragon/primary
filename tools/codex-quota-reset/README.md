# codex-quota-reset

One run is one decision. The program reads the Codex account's rate limits over the
app-server control socket, says what it saw, and — only when a policy file on disk says so
— spends exactly one earned reset credit. It never loops, never watches, and prints neither
the account id nor any token.

## Invocation

A datom-speaking CLI: one inline datom value, no flags.

```sh
node tools/codex-quota-reset/codex-quota-reset \
  'Check.{ <absolute policy path> <DefaultSocket|Socket.«path»> <SystemClock|At.<unixSeconds>> }'
```

`DefaultSocket` is `$HOME/.codex/app-server-control/app-server-control.sock`, the same
socket `tools/prompt-relay` and `tools/fan-out.mjs` speak to. The session initializes with
`capabilities.experimentalApi = true`; without it the account methods are not served.

Output is two lines (one, when the request itself is refused):

```
QuotaObserved.{ <remainingPercent> <resetsAt> <creditCount> }
ResetConsumed.{ <creditId> <outcome> } | ResetHeld.{ <reason> } | ResetRefused.{ <reason> }
```

`<resetsAt>` is the binding window's reset instant in UTC, or `Unknown`. The binding window
is whichever of the primary and secondary windows has the least left; that is the one a
reset would relieve. `<outcome>` is the backend's own word: `reset`, `nothingToReset`,
`noCredit` or `alreadyRedeemed`. A refusal exits 2. Refusals about the app-server are typed
and carry no backend prose: `appServerTimeout`, `appServerError: <JSON-RPC code>`,
`appServerUnavailable[: <errno>]`.

Hold reasons: `modeHold`, `aboveThreshold`, `windowEndsSooner`, `windowEndUnknown`,
`noCredit`, `creditDetailUnknown`, `alreadySpentThisWindow`.

## The policy file

Datom text, positional — mode, threshold percent remaining, minimum days of the window
still to run:

```
{ UseReset 15 2 }
```

`Hold` spends nothing whatever the reading. `UseReset` spends one credit when the binding
window is at or under the threshold **and** **at least** the minimum days of that window
remain — exactly two days left spends; a hair under does not, because a credit spent on a
window that is about to roll over anyway is wasted. Two days is the living's number.

A consequence worth saying plainly: the primary window runs five hours, so whenever it is
the binding one it has well under two days left and the tool holds. Under a two-day floor
only a binding **weekly** window is ever reset — a primary-window exhaustion is never
relieved by this program, whatever the policy says.

`policy.datom` in this directory is `Hold`; `policy.useReset.datom` is the spending policy.
Which one is installed is a deployment decision, not this program's.

## Which credit

The credit spent is an `available` one with the soonest non-null `expiresAt` — credits that
expire first are spent first — and its `creditId` is always named in the call. The consume
method also accepts an omitted `creditId`, in which case the backend picks by an unstated
rule; this program never does that.

## Not spending twice

The idempotency key is derived from the binding window's own `resetsAt`
(a UUID-shaped digest of `codex-quota-reset/window/<resetsAt>`), so every run against the
same window carries the same key: the backend treats a repeat as `alreadyRedeemed` rather
than a second spend. Before the call the program writes a `ResetAttempted` record to its own
log, so a run that dies or times out mid-call leaves the attempt on record.

The retry rule, in plain words: an attempt with no outcome recorded is not finished, and the
next run finishes it. When the log holds a `ResetAttempted` for the window and no
`ResetConsumed` after it, the next run **sends the consume again** — the same credit, the
same idempotency key, never a new one — and records whatever the backend answers. If the
earlier call had in fact gone through, the answer is `alreadyRedeemed`: the reset happened
once, and the record says so (`consumedEarlier`). Only once a `ResetConsumed` exists for the
window does the tool hold with `ResetHeld.{ alreadySpentThisWindow }`. So a slow backend on
one tick costs nothing but that tick, and no path spends twice.

## The log

Every observation and every decision is appended to
`$XDG_STATE_HOME/codex-quota-reset/log.ndjson`, else
`~/.local/state/codex-quota-reset/log.ndjson`. Append-only; nothing is rewritten. Records
carry `kind`, the observed percentages and instants, the credit id and the idempotency key.
The account id from the payload is not among them.

## How the core-checkup timer would call it

Not installed here. No unit and no timer are written by this proposal; **activation is the
secondary's**, as is the choice of which policy file to install.

The shape it would take: the existing core-checkup timer runs a oneshot user service whose
`ExecStart` is the invocation above with an absolute policy path and `DefaultSocket`, as the
same user that owns `~/.codex` (the socket is that user's), with `StandardOutput=journal` so
the two datom lines land in the journal beside the ndjson log. No `Restart=`: one run is one
decision, and a failed run is simply the next tick's work. The timer's period is the
checkup's own; the program is cheap and holds nothing between runs.

Nothing in the unit needs a secret: the app-server holds the account's credentials, and this
client never sees them.

## Tests

`tools/codex-quota-reset/tests/codex-quota-reset.test.mjs` runs the whole program against a
fake app-server over a Unix socket in a scratch directory, serving the real JSON payload
files under `tests/fixtures/`. Among the cases: a consume the fake never answers (the client
timeout fires, the attempt is logged, no outcome is), the rerun that resends it with the same
key, a rerun answered `alreadyRedeemed`, and a window with exactly two days left. No live
socket, no real account, and no credit is ever spent by the tests. Exposed as the `codex-quota-reset-fixtures` flake check.
