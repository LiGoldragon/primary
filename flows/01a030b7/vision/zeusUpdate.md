# Zeus update

## 2026-08-24T00:26:58+02:00 — use Ethernet for heavy Nix-path transfer

Context: transport boundary for resuming the Zeus update. The direct Ethernet address carries heavy Nix-store-path transfer; the existing Yggdrasil route remains suitable for activation and other light traffic.

> Then resume the zeus update. use its ethernet LAN ip address 192.168.18.95 if you need to move nix paths to it (yggdrassil is over wifi and will be very slow and heavy, but it's fine for activation and other non-heavy transfers usage)

— psyche, typed in current flow `01a030b7`.
