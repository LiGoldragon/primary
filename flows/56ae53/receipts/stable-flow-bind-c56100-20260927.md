# Stable Flow 0.12.2 bind of Mind Sol `c56100`

Witnessed 2026-09-27T00:58:07-06:00 from Field flow `56ae53`.

## Outcome

One authorized `MetaBindExisting` was submitted through the installed stable
Flow 0.12.2 client. It was not retried. The terminal response was
`RegisteredUnconfirmed`, and a read-only `List` through the same 0.12.2 client
showed `c56100` as `Pending`.

No Flow message was sent. No seat was restarted or retired, and no marker was
created.

## Fresh preflight

Immediately before the mutation:

- `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow 'List.{}'`
  had no `c56100` row.
- Native thread `01a0e0a1-7075-7cc2-928d-13fc56100504` had exact native title
  `MindV2.{ Sol c56100 }`; its latest applied settings were model `gpt-6-sol`
  and reasoning effort `medium`.
- Herdr session `recovery-56ae53` resolved agent `mind_sol_c56100`, idle and
  interactive ready, in workspace `w1`, tab `w1:t1`, pane `w1:p3`, terminal
  `term_65c6d6c5c3aac3`.
- Herdr server PID 301649 had UID 1001 and Linux process start token 1321351,
  and owned `/home/li/.config/herdr/sessions/recovery-56ae53/herdr.sock`.
- The foreground Codex process PID 318363 had UID 1001 and Linux process start
  token 1439670. Its cwd was
  `/home/li/wt/primary/mind-sol-successor-56ae53-target`, and its argv resumed
  the exact native thread above.

## Exact request

The request was passed as the sole positional argument to
`/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-meta`:

```text
MetaBindExisting.{ { recovery-56ae53 /home/li/.config/herdr/sessions/recovery-56ae53/herdr.sock { 301649 1001 1321351 } 56ae53 } [ { c56100 Mind Medium gpt-6-sol Codex 01a0e0a1-7075-7cc2-928d-13fc56100504 w1 w1:p3 w1:t1 term_65c6d6c5c3aac3 mind_sol_c56100 { 318363 1001 1439670 } /home/li/wt/primary/mind-sol-successor-56ae53-target } ] }
```

Exit status was 0. Terminal response, verbatim:

```text
BoundExisting.{ { recovery-56ae53 /home/li/.config/herdr/sessions/recovery-56ae53/herdr.sock { 301649 1001 1321351 } 56ae53 } [ Bound.{ c56100 RegisteredUnconfirmed } ] }
```

## Same-client readback

The stable 0.12.2 `flow 'List.{}'` readback contained this exact row:

```text
{ c56100 01a0e0a1-7075-7cc2-928d-13fc56100504 Codex Unavailable Available.{ recovery-56ae53 mind_sol_c56100 w1:p3 term_65c6d6c5c3aac3 } { 56ae53 recovery-56ae53 meta-bind-existing } Pending }
```

The bind therefore has a terminal typed response plus independent registry
readback. No message transport grade applies because this operation did not
send a Flow message.
