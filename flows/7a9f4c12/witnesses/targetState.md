Subject: Zeus current system, boot, capacity, activation, and Home Manager state.

Method: read-only root SSH to `192.168.18.95` with strict host-key checking,
running `hostname`, `uname`, `nixos-version`, `readlink -f /run/current-system`,
`readlink -f /run/booted-system`, `readlink -f /nix/var/nix/profiles/system`,
`nix-env --list-generations --profile /nix/var/nix/profiles/system`,
`bootctl status --no-pager`, `bootctl list --no-pager`, `df -hT / /nix
/nix/store /boot`, `df -ih ...`, `systemctl is-system-running`,
`systemctl --failed --no-legend`, `journalctl -b ...`, and for each declared
user `bird` and `li`, `readlink -f /home/<user>/.local/state/nix/profiles/home-manager`,
`nix-env --list-generations --profile ...`, and read-only systemd status and
journal for `home-manager-<user>.service`.

Observed:

- Zeus reports NixOS `26.05.20260422.0726a0e (Yarara)`, x86_64, and Linux
  `7.0.1`.
- `/run/current-system`, `/run/booted-system`, and the system profile all
  resolve to the same NixOS system output ending
  `nixos-system-zeus-26.05.20260422.0726a0e`. System profile generation 63 is
  current (2026-08-09 16:21:29); generations 60, 61, and 62 remain available,
  making generation 62 the immediate observed rollback candidate.
- systemd-boot reports current and default entry
  `nixos-generation-63.conf`; entries for generations 60–63 are present.
  Secure Boot is disabled.
- `/nix` and `/nix/store` share the root ext4 filesystem: 468 GB total, 364 GB
  used, 81 GB available (82%); inode use is 10%. `/boot` has 392 MB free of
  500 MB (22% used).
- `systemctl is-system-running` reports `running` and the failed-unit list is
  empty at probe time.
- The boot journal records `Finished NixOS Activation` on 2026-08-21 at
  10:11:52 CEST. `home-manager-bird.service` and
  `home-manager-li.service` are enabled, `active (exited)`, and report
  `Result=success`; their last recorded activations completed on 2026-08-21.
- The activation-related journal is not warning-free: it records duplicate
  D-Bus service-name warnings, an `mpd.service` start failure, and expected
  user-session messages such as “User systemd daemon not running. Skipping
  reload.” These are journal observations, not a claim that a new activation
  failed.
- Independent Home Manager profiles are present at
  `/home/bird/.local/state/nix/profiles/home-manager` generation 30
  (2026-07-29 16:58:00, current) and
  `/home/li/.local/state/nix/profiles/home-manager` generation 28
  (2026-01-17 17:47:02, current). Each profile has only that one generation in
  the observed generation listing.
- The enabled NixOS-managed Home Manager services point to separate
  `current-home` generation outputs in their service/gcroots state. The
  service activations succeeded, but this is distinct evidence from the
  independent profile symlinks; the probe did not derive a generation number
  for each service output.

Inference: the host is live and has a usable rollback profile and enough free
space for a normal closure transfer only as a capacity observation, not as a
guarantee that a proposed closure fits. The system activation surface is
currently operational, but journal warnings and the independent-profile versus
managed-service distinction require review before declaring a deployment safe.

Unknown: the target's intended next source revision, evaluated closure size,
cache/signing-key policy, exact Home Manager synchronization intent, and which
activation action is authorized remain unresolved. No secret-bearing files were
read.
