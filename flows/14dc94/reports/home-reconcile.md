# Home and Chroma reconciliation

CriomOS-home `main` is landed at `f652ba9ae6b24b7e946e60e98acc270280beb774`. Its ancestor `d75622900b33caad8dc0f6b9f997b63f7f2c7ac5` removes the retired Horizon-user reconstruction: Home indexes the current `horizon.users` vector by name while modules consume the current record fields directly (`size`, `hasPublicKey`, `publicKeys`, and `resolvedTextSize`). `fc51010176cb7d6eb77e73f88bae7405840e7414` repairs the remaining registered-check fixtures against that current user contract. The final commit pins Chroma `fc3a74ac5a0b5c92fc8f65d38cb8d6ba32d2bb37`. The Home and Chroma revisions were verified against the public remotes with `git ls-remote` after push.

Chroma `a82bb5018cde02267869e880f2d8d962a6395e48` incorporates the preserved overnight 0.7 dependency/generated-code upgrade, documents its breaking generated API, retains the event-driven sandbox waits, and restores the current visual snapshot when the session resumes before requesting schedule reconciliation. It also repairs the `session-dbus` Nix check: the upgraded Rust build wrapper retained `cargoTestCommand` as an unused derivation variable, so the former check ran the ordinary test suite and silently skipped its ignored private-bus test. The explicit `checkPhase` now executes that test under a private D-Bus session.

The ordered regression witness resets fake Gamma brightness from the desired `0.85` to `1.0` and sends `ResumeFromSleep`. Before the repair it failed with `left: 1.0, right: 0.85` in remote derivation `fk01a1rwk96vmjbzvqzfkbcjqfri6x5r-chroma-test-0.7.0.drv`. After the repair the same session-bus check passed as `/nix/store/ysypvsr0lbpjfr7gdqsk507yz38n8qd9-chroma-test-0.7.0`.

All four Chroma durable gates built on the configured remote builder:

- default: `/nix/store/85v78h1lhsjd9gkplgbg4qd2ym5gi60h-chroma-test-0.7.0`
- session-dbus: `/nix/store/ysypvsr0lbpjfr7gdqsk507yz38n8qd9-chroma-test-0.7.0`
- sandbox-terminal: `/nix/store/7xmrp3zz69r5cz5lcjn5xsc929x982p4-chroma-sandbox-terminal-check`
- set-dark-theme-example: `/nix/store/wlh947ay147rwv3vwl0p76b6cpxa1w93-chroma-set-dark-theme-example-check`

Home's earlier Horizon repair had remote witnesses for `horizon-user-projection`, `bitwarden-availability`, `default-opener`, and `home-profile-absence`. The standalone Home Chroma check command stops at Home's intentional `no system input was provided` boundary. The system reconciliation worker owns the final materialized evaluation/build against Home `fc510101`; this report does not claim that separate witness.

The final fixture follow-up gives `ghostty-primary-selection` a current string-valued `user.size` and makes `horizon-user-projection` accept Blueprint's complete `callPackage` argument set while deriving `lib` from `pkgs`. Their actual flake outputs evaluated to `/nix/store/70hqdac3ygfzcy54mdka6c6biw30mkdr-ghostty-primary-selection.drv` and `/nix/store/57avci0lrszxpg9xd878f259wsdlf4k1-horizon-user-projection-check.drv`. The full composed `NIXPKGS_ALLOW_UNFREE=1 nix flake check --no-build --impure` passed package/check enumeration with these repairs and then stopped at a nested external `system.system` stub: the CriomOS checkout is a consumer whose own `system` input still requires Lojix materialization, rather than the tiny System tuple flake Home expects. This is the exact full-check limitation; the system reconciliation worker independently reproduced it and owns the final materialized system build against `fc510101`.

The first deployed 0.7 integration exposed a separate GeoClue client defect. The exact Horizon static location remained configured with 1000 m accuracy, while Chroma requested GeoClue accuracy level 1 (`Country`). GeoClue mapped that request through its privacy behavior and emitted a 4000 m fix, which Chroma correctly refused under its ruled 1000 m ceiling. Chroma 0.7.1 requests the public `Exact` enum value 8 while preserving the ceiling and last-good-location lease behavior.

A private-bus fake GeoClue client captures the actual `RequestedAccuracyLevel` property write. Before the fix, remote derivation `q6lrcv501vvkhpc6gzcdw88da7yh473x-chroma-test-0.7.0.drv` failed with captured value 1 versus required 8. After the fix, the session check passed as `/nix/store/31yzb7p3w2a6b7ar1gsqh3sw06zw0lsd-chroma-test-0.7.1`; the default suite, including rejection above 1000 m and retention of a valid held fix, passed as `/nix/store/8yvnk862530ispyip6zmd9hgha4v26xn-chroma-test-0.7.1`. Sandbox terminal passed as `/nix/store/2y4gim2ckfijmxnq4nvsj96zqixbmdxv-chroma-sandbox-terminal-check`. The set-dark check first timed out waiting 90 seconds for Ghostty configuration during a concurrent run; a sequential rerun of the same derivation passed as `/nix/store/v2q4x3dr4gj3x2526kdy8b1x6r9vdbzq-chroma-set-dark-theme-example-check`. These observations establish the rerun result without assigning a cause to the initial timeout.

Home's direct consumers of the final Chroma pin evaluated to `/nix/store/zdf6f33b2sp153ip834c6dlj24fazb1j-chroma-datom-config-check.drv` and `/nix/store/5acahkpx6rpajglcfwcj69b4qxdcp66n-chroma-emacs-resident-check.drv`. The system reconciliation worker owns the composed build and live witness that GeoClue now reports an accepted accuracy and `GetSolarClock` becomes available.

The live read-only observation before deployment was `chroma GetState -> State.{ Light 6500 85 }` while Gamma reported `d 1`. Chroma was still the deployed 0.5.0 store package. The host suspended after that daemon's last start, and the pre-repair resume path could suppress equal desired schedule values, so resume recovery is a supported explanation and the reproduced defect is fixed. The journal does not prove exactly which backend event reset the live Gamma value; the final deployment must witness the actual Gamma property at `0.85` after activation and after a suspend/resume cycle.

The Home and Chroma isolated working copies were clean after push. Orchestrate locks 1379 and 1383 returned typed `Released` receipts. Peer work and the original preserved Chroma checkout were not edited.

## Sources

- CriomOS-home public `main`: `f652ba9ae6b24b7e946e60e98acc270280beb774`
- Chroma public `main`: `fc3a74ac5a0b5c92fc8f65d38cb8d6ba32d2bb37`
- Chroma red witness: `nix log /nix/store/fk01a1rwk96vmjbzvqzfkbcjqfri6x5r-chroma-test-0.7.0.drv`
- Chroma green witnesses: the four remote output paths above
- Live state: `chroma GetState`; `busctl --user get-property rs.wl-gammarelay / rs.wl.gammarelay Brightness`
- Live lifecycle: `systemctl --user show chroma-daemon.service wl-gammarelay-rs.service`; boot journal around 2026-09-11 13:39, 14:35, and 18:57–19:01 CST
- Follow-up direct evaluation: `/nix/store/70hqdac3ygfzcy54mdka6c6biw30mkdr-ghostty-primary-selection.drv`; `/nix/store/57avci0lrszxpg9xd878f259wsdlf4k1-horizon-user-projection-check.drv`
- GeoClue exact-request red witness: `nix log /nix/store/q6lrcv501vvkhpc6gzcdw88da7yh473x-chroma-test-0.7.0.drv`
- GeoClue exact-request and Home consumer green witnesses: the 0.7.1 and direct-evaluation store paths above
- Coordination receipts: Orchestrate locks 1379, 1383, report lock 1384, fixture-repair lock 1385, and accuracy-repair lock 1386; all returned typed `Released` receipts
