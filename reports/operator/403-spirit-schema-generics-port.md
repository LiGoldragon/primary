# Spirit Schema Generics Port

## What landed

Spirit is now using the implemented schema generics path for its Nexus reaction frame. This is the `(| |)` generic/container-frame work, not trait declarations and not implementations-as-data.

The generator support landed first:

- Repo: `/git/github.com/LiGoldragon/schema-rust-next`
- Commit: `733b76d3` (`schema-rust: expand named frame applications`)
- Change: a namespace newtype declaration whose payload is an application of a generic enum frame now lowers as the named concrete enum.
- Regression: `tests/spirit_frame_application.rs` now proves `NexusWork (Work ...)` and `NexusAction (Action ...)` generate concrete `pub enum NexusWork` / `pub enum NexusAction`, not wrapper newtypes.

Spirit then consumed it:

- Repo: `/git/github.com/LiGoldragon/spirit`
- Commit: `161f3a2c` (`spirit: port nexus frame to schema generics`)
- `schema/nexus.schema` now defines:
  - `(| Work Event WriteDone ReadDone EffectDone |)` as the shared work frame.
  - `(| Action Reply Write Read Effect Continuation |)` as the shared action frame.
  - root `Input` / `Output` as applications of those frames.
  - `NexusWork` / `NexusAction` as named applications of those frames.

The old duplicated per-leg root wrappers (`SignalArrived`, `SemaWriteCompleted`, `ReplyToSignal`, `CommandEffect`, `Continue`, etc.) were removed where the frame expansion makes them unnecessary. The generated Rust now carries direct payload variants:

- `NexusWork::SignalArrived(SignalInput)`
- `NexusWork::SemaWriteCompleted(SemaWriteOutput)`
- `NexusAction::ReplyToSignal(SignalOutput)`
- `NexusAction::CommandEffect(NexusEffectCommand)`
- `NexusAction::Continue(NexusWork)`

The handwritten Spirit runtime bridge was updated to consume those direct payloads instead of unwrapping generated wrapper nouns.

## Verification

Passed in `schema-rust-next`:

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

Passed in `spirit`:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

The full Spirit test suite passed after the port, including the runtime triad tests that drive signal -> nexus -> sema -> reply behavior.

## Nix Gate

The local-stack Nix build was attempted twice with local path overrides. Both attempts sat silent in Nix daemon/store I/O wait behind an unrelated long-running Nix smoke build:

- first attempt was manually terminated after several minutes of no output;
- second attempt used `timeout 180s` and exited with code `124`.

So the Nix gate is not green and not failed by the Spirit code; it is blocked by shared Nix daemon/store contention on this machine. Cargo-level build, tests, and clippy are green.

## Clarification

This did not implement trait declarations or implementation bodies. The thing now live on Spirit is generics: container/frame declarations that substitute payload types into enum slots and generate concrete enums. That is the piece needed to stop hand-repeating the Work/Action frame.
