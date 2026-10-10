# Stale GC root removal — secondary-348e7b/realize-18/candidate-root

Host: ouranos. Date: 2026-09-25.

## Checks

1. `readlink -f ~/.local/state/secondary-348e7b/realize-18/candidate-root`
   -> `/nix/store/71wfmszzhg2lw8ggafky1q3aa7cak4bf-nixos-system-prometheus-26.11.20260813.0e251e2`

2. `nix-store --query --roots <target>`
   -> only one root listed:
   `/home/li/.local/state/secondary-348e7b/realize-18/candidate-root -> /nix/store/71wfmszzhg2lw8ggafky1q3aa7cak4bf-nixos-system-prometheus-26.11.20260813.0e251e2`
   (plus unrelated stale-temproots-file cleanup noise from nix-store itself)

3. `nix path-info -S <target>`
   -> closure size 85483390376 bytes (~79.6 GiB)

4. `hm-list` — flow `348e7b` does not appear in the listing at all (not even
   as STALE), confirming it is not a live/tracked flow.

5. `readlink /run/current-system` on ouranos
   -> `/nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-26.11.20260813.0e251e2`
   (different host, different hash — not this target)

6. `ssh -o BatchMode=yes prometheus.goldragon.criome 'readlink /run/current-system'`
   -> `/nix/store/7f8kpzcnj3x03p5057fvs91k6wjvjwqz-nixos-system-prometheus-26.11.20260813.0e251e2`
   (different store hash from the candidate target — not the booted system)

7. `/nix/var/nix/profiles/system*` on ouranos:
   `system -> system-188-link -> /nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-...`
   (does not reference the candidate target)

## Action taken

All checks passed: single root, flow not live, not the current/booted system
of either host, not referenced by any system profile generation. Removed
only the symlink:

```
rm ~/.local/state/secondary-348e7b/realize-18/candidate-root
```

The directory and the underlying `/nix/store` path were left untouched; no
GC run was triggered here.

## Reclaimable

Closure size of the now-unrooted path: ~79.6 GiB (85483390376 bytes),
available to the nightly GC once it next runs.
