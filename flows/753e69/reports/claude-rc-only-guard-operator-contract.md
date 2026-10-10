# Claude RC-only guard: operator contract

This contract limits one supported Herdr prompt to one currently supplied
Claude identity. It is not a continuation, bootstrap, lifecycle, or account
control procedure.

## Pinned target

The guard accepts only this complete identity tuple:

| Field | Required value |
| --- | --- |
| Session | `836818cc-83ab-4657-8b8f-1414f887559c` |
| Pane | `wD:p9` |
| Terminal | `term_65c138019438357` |
| Process ID | `3784555` |
| Process start ticks | `102010340` |
| Working directory | `/home/li/primary` |
| Model argv value | `claude-fable-5-1[1m]` |
| Effort | `medium` |

It must obtain those fields through Herdr pane and agent inspection and the
foreground-process record before sending input, then repeat the same checks at
the send boundary. A missing field, conflicting field, nonzero command result,
busy process, or ambiguous target is a refusal. A matching pane name alone is
insufficient.

## Operations

`inspect` is read-only. It emits a redacted record of the pinned identity,
Herdr inspection result, process check, and footer state. It never sends keys
or text.

`dry-run` performs every identity and footer check and records the would-send
action, but sends no prompt.

`execute-once` is available only after a successful inspection in the same
guard invocation. It uses the supported exact-pane transport:

```sh
herdr agent prompt wD:p9 /remote-control
```

The guard invokes it once only. It does not retry after an accepted send,
timeout, busy result, or transport error.

After a successful prompt result, the guard reads the same pinned pane again,
redacts the before/after footer records, and requires an actual `/rc` footer
indicator. The indicator proves only that Claude displays Remote Control as
enabled. Authentication, a remote address, and a remote-client attachment stay
unknown unless separately witnessed.

`stop` means terminate the guard's own pending operation before any send, or
return a refusal after a failed check. It never stops Claude, closes the pane,
sends an interrupt, or changes session state.

## Refusal and redaction

The receipt may include stable identifiers, check names, command exit status,
and the boolean `/rc` result. It must not include pane body text, prompts,
OAuth URLs, pairing codes, tokens, cookies, account identifiers, or secrets.
The footer capture is a minimized, redacted observation rather than a terminal
transcript.

The guard refuses if the postcondition is absent or ambiguous. Such a refusal
does not establish that Remote Control is disabled; it establishes only that
the requested proof was not obtained.

## Explicit exclusions

This operation must never bootstrap a session, replay a bootstrap, submit a
payload other than `/remote-control`, claim a Flow identity, set a title,
restart or reap a process, alter routing, or disclose an authentication URL or
code. It does not attest any earlier session history or original process
continuity beyond the supplied live identity tuple.

## Evidence boundary

One successful guarded execution proves a single exact-pane input and a later
displayed `/rc` footer under the rechecked identity. It does not prove external
reachability or authorize any broader remote-control workflow.
