# Home and Chroma reconciliation

CriomOS-home `main` is landed at `b7ccb8756fc7c19255923a963f3d51c63e77f6c0`. Its parent `d75622900b33caad8dc0f6b9f997b63f7f2c7ac5` removes the retired Horizon-user reconstruction: Home indexes the current `horizon.users` vector by name while modules consume the current record fields directly (`size`, `hasPublicKey`, `publicKeys`, and `resolvedTextSize`). The final commit pins Chroma `a82bb5018cde02267869e880f2d8d962a6395e48`. Both revisions were verified against the public remotes with `git ls-remote` after push.

Chroma `a82bb5018cde02267869e880f2d8d962a6395e48` incorporates the preserved overnight 0.7 dependency/generated-code upgrade, documents its breaking generated API, retains the event-driven sandbox waits, and restores the current visual snapshot when the session resumes before requesting schedule reconciliation. It also repairs the `session-dbus` Nix check: the upgraded Rust build wrapper retained `cargoTestCommand` as an unused derivation variable, so the former check ran the ordinary test suite and silently skipped its ignored private-bus test. The explicit `checkPhase` now executes that test under a private D-Bus session.

The ordered regression witness resets fake Gamma brightness from the desired `0.85` to `1.0` and sends `ResumeFromSleep`. Before the repair it failed with `left: 1.0, right: 0.85` in remote derivation `fk01a1rwk96vmjbzvqzfkbcjqfri6x5r-chroma-test-0.7.0.drv`. After the repair the same session-bus check passed as `/nix/store/ysypvsr0lbpjfr7gdqsk507yz38n8qd9-chroma-test-0.7.0`.

All four Chroma durable gates built on the configured remote builder:

- default: `/nix/store/85v78h1lhsjd9gkplgbg4qd2ym5gi60h-chroma-test-0.7.0`
- session-dbus: `/nix/store/ysypvsr0lbpjfr7gdqsk507yz38n8qd9-chroma-test-0.7.0`
- sandbox-terminal: `/nix/store/7xmrp3zz69r5cz5lcjn5xsc929x982p4-chroma-sandbox-terminal-check`
- set-dark-theme-example: `/nix/store/wlh947ay147rwv3vwl0p76b6cpxa1w93-chroma-set-dark-theme-example-check`

Home's earlier Horizon repair had remote witnesses for `horizon-user-projection`, `bitwarden-availability`, `default-opener`, and `home-profile-absence`. The standalone Home Chroma check command stops at Home's intentional `no system input was provided` boundary. The system reconciliation worker owns the final composed evaluation/build against Home `b7ccb875`; this report does not claim that separate witness.

The live read-only observation before deployment was `chroma GetState -> State.{ Light 6500 85 }` while Gamma reported `d 1`. Chroma was still the deployed 0.5.0 store package. The host suspended after that daemon's last start, and the pre-repair resume path could suppress equal desired schedule values, so resume recovery is a supported explanation and the reproduced defect is fixed. The journal does not prove exactly which backend event reset the live Gamma value; the final deployment must witness the actual Gamma property at `0.85` after activation and after a suspend/resume cycle.

The Home and Chroma isolated working copies were clean after push. Orchestrate locks 1379 and 1383 returned typed `Released` receipts. Peer work and the original preserved Chroma checkout were not edited.

## Sources

- CriomOS-home public `main`: `b7ccb8756fc7c19255923a963f3d51c63e77f6c0`
- Chroma public `main`: `a82bb5018cde02267869e880f2d8d962a6395e48`
- Chroma red witness: `nix log /nix/store/fk01a1rwk96vmjbzvqzfkbcjqfri6x5r-chroma-test-0.7.0.drv`
- Chroma green witnesses: the four remote output paths above
- Live state: `chroma GetState`; `busctl --user get-property rs.wl-gammarelay / rs.wl.gammarelay Brightness`
- Live lifecycle: `systemctl --user show chroma-daemon.service wl-gammarelay-rs.service`; boot journal around 2026-09-11 13:39, 14:35, and 18:57–19:01 CST
- Coordination receipts: Orchestrate locks 1379, 1383, and report lock 1384
