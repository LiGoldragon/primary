# Hacky Messenger shipped

Built by messaging-builder-1, Flow 6034cc, for primary Psyche opus 108ab0.

Four commands live in primary `tools/` and are exposed on this machine's PATH
through symlinks in `~/.local/bin`:

```sh
export FLOW_ID=YOUR_FLOW_ID
hm-register YOUR_FLOW_ID YOUR_HERDR_AGENT --session YOUR_HERDR_SESSION
hm-list
hm-send TARGET_FLOW_ID 'Your message'
hm-send-abrupt TARGET_CODEX_FLOW_ID 'Interrupt and read this'
```

Implementation: `tools/hacky-messenger/hm.py`. Usage and operational limits:
`tools/hacky-messenger/README.md`. No extra Python packages or daemon required.
The registry is `~/.local/state/hacky-messenger`, overrideable with HM_REGISTRY.
Every registry mutation and send reserves that directory through Orchestrate.

## Production witness

- Registered this actual running Codex agent as Flow 6034cc in messaging-build.
- `hm-list` showed its live working state and flow ID.
- Ran hm-send with the marker `HM_PRODUCTION_PROBE_6034cc` addressed to 6034cc.
- Herdr accepted submission.
- The complete message then arrived as a user message in this active Codex
  conversation, mid-task. This flow acknowledged that exact marker in commentary.

This proves live plain-string prompt delivery to a running Codex recipient. It
is a loopback witness, not a separate-flow or Claude delivery witness. Hard-abrupt
ordering was tested with a fake Herdr; no live Escape interruption was performed.
Only this agent was listed in the one running Herdr session when checked.
Other existing primary flows must be placed in Herdr and registered before
Hacky Messenger can address them. No primary was moved or restarted.

## Automated validation

Ten unittest cases pass: literal Unicode/multiline payload; Escape-before-prompt;
stale terminal refusal; conflicting registration; terminal control character
rejection before input; unknown/traversal IDs; Escape failure suppressing prompt;
partial hard-abrupt failure; blocked agent refusal; Herdr error JSON despite a
successful process exit. The control-character test was observed failing on DEL,
then passed after fixing rejection of DEL and C1 control characters.

`check.nix` exposes the same test gate to Nix consumers. Nix syntax parsing
passed; the Nix derivation itself was not built. The Python suite ran locally.

Live probes found that Herdr's terminal ID is not accepted as an agent target;
pane ID is. The scripts compare the registered terminal identity/name/harness
against live state, then address the pane. Herdr's state check and send are
separate calls, so an occupant replacement race remains. Submission is not a
read receipt, and uncertain sends are not automatically retried.

## Proper triangle follow-on

The later design mosaic changes the proper soft tier to an end-of-turn queue;
Hacky Messenger exposes ordinary prompt and Codex hard-abrupt only. The proper
Flow/Message implementation must retain a distinct soft mechanism rather than
claim prompt provides end-of-turn semantics.

The prior Rust implementation blockers remain: fac697 owns Flow/Message and
Signal repository locks, Message's checkout is not main, RequestWorktree is
unavailable on the installed Orchestrate, and the applicable Rust doctrine has
not been named in the role packet or follow-up. Ownership transfer/workspace
coordination was requested. No claimed component checkout was edited. No legacy
decoder or generated skill tree was changed.
