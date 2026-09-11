# Periphery audit — method

Read-only. Every repository inspected through `git` object reads at named
revisions in the shared checkouts under `/git/github.com/LiGoldragon/`; no
fetch, no checkout, no write to any repository.

One build was run: `cargo check --no-default-features` on mirror
`783be4b84c04d6b2ebb65c8f93fe140ba7d2646f`, in a fresh clone at
`<scratchpad>/mirror-wip` made with `git clone --no-local --shared` from the
shared checkout. Captured as `mirror-wip-cargo-check.log` / `.exit`.

Nix store provenance established with `nix-store -q --deriver` on the targets
of the `result-*` symlinks committed in signal-standard `2c90fc99`, compared
against the `.drv` paths printed in flow 857335's
`witnesses/signal-standard-nix-6688f8ca.log`.

Runtime-dependency sweep (systemd user units, running processes, flake inputs,
Cargo manifests across the estate) delegated to a read-only subagent; its
findings are marked relayed in the report and the ones this flow re-checked are
marked witnessed.
