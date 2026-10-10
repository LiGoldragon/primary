# Codex rotation completion receipt

Source revision: CriomOS-home `0025894f6238` on `main` (following rotation source `0eda1be1`, Herdr predecessor admission `a07be7d7`).

Activation completed successfully from `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation`; its NarHash is `sha256-6/25jVmEMXkkxagzV5jhBDUiRWz2OhTaIZefgkkFnqc=`. The Home Manager profile resolves to that artifact.

`sd-switch` planned and performed only these rotation unit effects: stop `flow-configuration-next.service`, `flow-nexus-next.service`, and `flow-nexus.service`; start `codex-remote-control-next-8mkkxq293hk2.service` plus those three Flow units. The plan also started `criomos-ui-priority.service` and `set-SSH_AUTH_SOCK.service`; neither is a Codex or Flow server. No occupied Codex unit was stopped or restarted.

Active rotation units are `codex-remote-control.service`, `codex-remote-control-next.service`, `codex-remote-control-next-8mkkxq293hk2.service`, `flow-nexus.service`, `flow-nexus-next.service`, and `flow-configuration-next.service` (active/exited after successful configuration).

The preserved servers remain PID 1936 (0.153.4) and PID 1960 (0.158.0-alpha.9). Their socket inodes remain respectively 53217316 at `.codex` and 33431380 at `.codex-next`. The new candidate socket is `.codex-next-8mkkxq293hk2`, inode 33454845. Plain `codex` reports 0.158.0-alpha.9 and routes to the preserved `.codex-next` role; `codex-next` reports 0.161.0-alpha.2 and has isolated candidate state.

The unregistered foreground CLI PID 1824790 remains alive, and its FD 37 remains connected to PID 1936's old-stable socket. The six registered Codex native bindings remain the same UUID/pane pairs: `01a0e8d3-aace-7712-aae2-3ce6f51adad5`/w1:pG, `01a0e9d1-d20f-7b43-98b0-15bb666e70e1`/w1:pJ, `01a0ee2e-a52e-7c92-98c7-9a5d5b96b3f3`/w1:pQ, `01a0ee49-43e2-7b02-8a24-b81025548ba8`/w1:pV, `01a0ee54-3ef1-73b1-a09f-06f6cbb53630`/w1:pW, and `01a0ee71-5824-7c40-b65c-7841bc2558eb`/w1:pX. Their preflight foreground PIDs were 3909351, 4094177, 643951, 684085, 698231, and 736948; the post-activation Herdr roster retains the same identities and panes.

Both Flow Nexuses were deliberately restarted after the successful Flow configuration unit, so their future role table is applied: stable uses the preserved `.codex-next` endpoint and candidate uses the hash-identified candidate endpoint. Existing native sessions were outside the Flow service cgroups and were not migrated or terminated.
