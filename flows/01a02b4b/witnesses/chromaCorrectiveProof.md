# Chroma corrective proof

Method: probe commands run in `/git/github.com/LiGoldragon/chroma` on 2026-08-23.

`cargo test --test theme_dbus stale_failure_reports_must_still_use_the_bounded_public_vocabulary -- --exact`
failed before the correction: an invalid stale failure code returned `Ok(())`.

After the correction, `cargo test`, the explicit private-bus command
`dbus-run-session -- cargo test --lib actual_theme_dbus_service_binds_the_real_protocol_to_unique_bus_owners -- --ignored`, and the state-store reopen tests passed.

`nix eval .#checks.x86_64-linux.session-dbus.drvPath --raw` resolved the
session-bus check. Both `nix build --no-link .#checks.x86_64-linux.session-dbus`
and `nix build --no-link .#checks.x86_64-linux.default` completed through the
configured remote builder `prometheus.goldragon.criome`.
