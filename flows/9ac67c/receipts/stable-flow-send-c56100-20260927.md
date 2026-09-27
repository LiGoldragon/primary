# Stable Flow 0.12.2 Send to `c56100`

## Outcome

Exactly one ordinary Flow `Send` was submitted. It was not retried.

The installed stable client returned status 0 and exact stdout:

```text
Sent.Presented.{ c56100 w1:p3 1790492832474 }
```

Its stderr was empty.

The immediate same-client `List.{}` returned status 0. Its exact `c56100`
row was:

```text
{ c56100 01a0e0a1-7075-7cc2-928d-13fc56100504 Codex Unavailable Available.{ recovery-56ae53 mind_sol_c56100 w1:p3 term_65c6d6c5c3aac3 } { 56ae53 recovery-56ae53 meta-bind-existing } Active }
```

Thus the transport grade is explicitly `Presented`, and the durable stable
Flow row is explicitly `Active` after presentation. These facts do not prove
that the native harness read or answered the prompt.

## Exact request

The request was the sole positional argument to
`/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow` with
`XDG_RUNTIME_DIR=/run/user/1001`:

```text
Send.{ c56100 «Please advance the imported-seat recovery: review the durable Pending binding now visible in stable Flow, identify the source-backed confirmation lifecycle for imported rows in Flow-next, and report the smallest safe implementation and test plan to Field and Fable. Do not start, stop, replace, or activate any seat from this request.» }
```

## Fresh preflight

- Stable Flow daemon PID 1937 ran the 0.12.2 `flow-nexus` closure and exposed
  `FLOW_SOURCE_ROOT=/home/li/primary`, `XDG_RUNTIME_DIR=/run/user/1001`.
- The client resolved to the matching 0.12.2 closure and reported
  `flow 0.12.2`.
- `/home/li/primary/flows/.c56100.flow-id` was a regular 0600 file with SHA256
  `da9623abeacfcbc5e6eccea13801c160a2e1c6f6aa879560826e5921625666f9`,
  harness `codex`, identity `01a0e0a1-7075-7cc2-928d-13fc56100504`, and alias
  `c56100`.
- Primary revision `d4b74bf68e2d0032622c9be3ec3e65772d9280ca` had description
  `Record c56100 Flow identity marker`.
- Pre-send stable `List.{}` showed `c56100` `Pending`, endpoint `Unavailable`,
  and route `Available.{ recovery-56ae53 mind_sol_c56100 w1:p3 term_65c6d6c5c3aac3 }`.
- Herdr `agent list` showed the same Codex native session, pane, terminal, cwd,
  `agent_status=idle`, and `interactive_ready=true`. PID 318363 had UID 1001,
  start token 1439670, and resumed the exact native session.

## Retained raw evidence

The complete subsequent List and byte-exact command results were retained at
`/var/tmp/c56100-flow-send.x5mibp/` during publication:

- `send.stdout`: 46 bytes, SHA256
  `0417359c8e76451cd034e19de32aa1e955f209f998de7a167f79b385331e58a4`
- `send.stderr`: 0 bytes, SHA256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `send.status`: `0`
- `list.stdout`: 5653 bytes, SHA256
  `13173681d95a44400c574f07c2a948831a4ca110c8677297c87ba78f3651da7e`
- `list.stderr`: 0 bytes, SHA256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `list.status`: `0`

## Evidence grade

The Send has a typed terminal `Presented` result and an independent immediate
registry readback of `Active`. Native read or reply evidence is a separate
grade and is not inferred from either result.
