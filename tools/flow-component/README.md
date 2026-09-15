# Flow component prototype

This is a placeholder component inside primary, not a new Flow repository.
It accepts exactly one canonical inline Datom command. `Launch` uses a
per-flow transient user scope around Ghostty and its Claude child. `Attach` is
intentionally ordinary-socket-shaped but cannot attach until a Flow-owned
durable registry exists.

The CLI turns `Launch` into a real portable `MetaSignal` frame and `Attach`
into an `OrdinarySignal` frame before it takes the corresponding action. The
test fixture binds the two actual binary transports separately, using the
actual Nexus authority modes: ordinary `0660`, meta `0600`. It proves
Datom-to-Signal framing and typed round trips for privileged Launch versus
ordinary Attach. The fixture has no installed daemon, durable store, or peer
credential check; those Flow Nexus concerns remain unfinished.

The convenience words `flow launch primary claude /flow attach name` are a
proposal only. The implemented surface is the named Datom object:

```text
Launch.{ primary claude haiku /flow attach name UUID /system-prompt /user-prompt { HOME PATH Some.DISPLAY None None None Some.RUNTIME } }
```

`env -i` runs inside the scope, so only the supplied HOME/PATH/display/XDG
values enter Ghostty or Claude. It removes `NO_COLOR`, `CODEX_CI`, and all
`CODEX_*` values. Launch success still requires an external postflight record
showing exact UUID, nonempty bridgeSessionId, and matching remote name.

## terminal-cell comparison

terminal-cell 3.0.1 is the existing low-level durable PTY owner. It launches a
daemon-owned command and attaches a viewer over its data socket, with local
runtime metadata and no higher-level durable registry. This prototype does not
reimplement its PTY, transcript, input, or viewer protocol. It directly scopes
the requested Ghostty/Claude launch because terminal-cell's daemon/viewer
topology does not yet expose this component's per-flow systemd scope and Claude
remote bridge postflight as one owned contract. A durable implementation must
choose terminal-cell as its PTY backend or replace it explicitly; it must not
add a second durable PTY.
