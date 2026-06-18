# Spirit Guardian Negative-Guideline Deploy

Date: 2026-06-18
Role: system-designer

## Result

Spirit now rejects intent proposals whose operative guidance is centered on negation rather than the affirmative rule to follow. The change is integrated on `main`, tested against the live guardian, deployed to `ouranos`, and verified through the deployed `spirit` CLI.

## Commits

| Repo | Main commit | Change |
|---|---:|---|
| `signal-spirit` | `e5f432b2` | Adds `GuardianRejectionReason::NegativeGuideline` to the working signal contract and generated round-trip coverage. |
| `meta-signal-spirit` | `d26bed81` | Locks to `signal-spirit/main` carrying the new rejection reason. |
| `spirit` | `6092b804` | Adds the guardian prompt gate, worked examples, Spirit docs, and live scenario coverage. |
| `spirit` | `e046b29e` | Locks Spirit's Nix vendored `signal-spirit` and `meta-signal-spirit` source inputs to the integrated commits. |
| `CriomOS-home` | `22820923` | Pins the deployed Home profile to Spirit `e046b29e`. |
| `CriomOS` | `8a07a588` | Pins FullOS to the updated CriomOS-home input. |

## Verification

Local Rust and contract checks:

- `signal-spirit`: schema regeneration check, `cargo test --features nota-text`, `cargo fmt --check`.
- `meta-signal-spirit`: `cargo check --features nota-text`, `cargo fmt --check`.
- `spirit`: `cargo check --features agent-guardian`, `cargo fmt --check`, `cargo test --features agent-guardian guardian_prompt`.

Live guardian check:

- `cargo test --features agent-guardian live_deepseek_guardian_accepts_and_rejects_realistic_scenarios -- --ignored --nocapture`
- The pass/fail live scenario list now uses separate human-like testimony and reasoning, and includes the `negative spelling guideline` scenario expecting `NegativeGuideline`.

Nix/package checks:

- `nix build .#default --print-out-paths --no-link` in `spirit` built the default package with updated vendored source locks.
- `lojix-run "(HomeOnly goldragon ouranos li [/git/github.com/LiGoldragon/goldragon/datom.nota] [github:LiGoldragon/CriomOS-home/main] Activate None None)"` completed successfully.

Deployed daemon check:

- `systemctl --user status spirit-daemon.service` shows the service restarted on 2026-06-18 at 10:29:26 CEST from the new Spirit package path.
- `spirit "(Version)"` returns `(VersionReported 0.14.0)`.
- A deployed `Propose` call for the old negative spelling shape returned `(GuardianRejected (NegativeGuideline ...))`, proving the running daemon and CLI understand the new typed reason.

## Notes

The direct `HomeOnly` request against `CriomOS/main` failed because that flake does not expose `homeConfigurations.li.activationPackage`. The successful deploy used `CriomOS-home/main` directly, which is the existing working HomeOnly path.

The `FullOs` deploy path against `CriomOS/main` is still blocked by an unrelated evaluation error in `modules/nixos/test-vm-guest.nix`: `attribute 'testVm' missing`. CriomOS has still been lock-bumped to the updated CriomOS-home input, but FullOS switch was not completed in this pass.
