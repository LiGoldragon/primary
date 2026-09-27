# Ouranos Herdr remote access receipt

## Verified

- Ouranos runs Herdr default (`0.8.2`, protocol `20`) on its local Unix socket.
- Tailscale advertises `ouranos.tailnet.goldragon.criome` at `100.64.0.2`.
- SSH listens on port 22.
- A read-only SSH probe to `li@100.64.0.2` reached Ouranos and read Herdr server status and the default-session agent list.

## Laptop attach

With the laptop connected to this Tailscale tailnet and an SSH identity for `li`, run:

```sh
herdr --remote li@ouranos.tailnet.goldragon.criome --session default
```

## Unverified boundary

No independent laptop or peer-host attach was witnessed. Prometheus was offline and Zeus did not resolve during this check. The command above is the supported attach path, not evidence that a particular laptop has joined successfully.
