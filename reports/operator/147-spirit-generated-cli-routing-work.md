# Spirit Generated CLI Routing Work

## Purpose

This report tracks the implementation slice for generated two-socket CLI
routing, using `persona-spirit` as the pilot.

## Requirements

- Implement the CLI macro shape from
  `reports/designer-assistant/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`.
- Use the macro in `persona-spirit` so `spirit` is a thin client only.
- Route working requests to the working socket and owner requests to the owner
  socket from a compile-time request-head table.
- Add enough relevant `owner-signal-persona-spirit` surface to prove owner
  routing without invented test-only semantics.
- Test ordinary and owner routing with Nix-backed constraints.
- Split `persona-spirit` flake packages so the `spirit` CLI and
  `persona-spirit-daemon` install separately.

## Current Plan

1. Inspect `signal-frame`, `signal-persona-spirit`,
   `owner-signal-persona-spirit`, and `persona-spirit` current macro and
   runtime surfaces.
2. Add the generated CLI runtime/macro in the correct signal crate.
3. Replace `spirit` hand-written routing with the macro.
4. Ensure owner request/reply types are NOTA-encodable and useful for routing
   tests.
5. Add source and integration witnesses that the CLI is thin, two-socket, and
   daemon-mediated.
6. Split Nix package outputs.
7. Run `nix flake check -L --max-jobs 0` on touched repos and push with `jj`.

## Live Notes

- The CLI must not open the Spirit database.
- The CLI must not stamp time or perform domain logic.
- Unknown request heads may fail outside a contract reply because no contract
  has been selected yet.
- Once a contract head is selected, decode/socket failures are ordinary process
  errors unless the daemon returns a typed reply.

## Progress

### Signal-frame

Implemented and pushed commit `0b5b3ef5` in `signal-frame`.

- `signal_channel!` emits `SignalOperationHeads` for generated operation enums.
- `signal_frame::signal_cli!` emits a data-bearing dispatch object from a
  working request enum and an owner request enum.
- `CommandLineRouteTable` routes a NOTA record head to `Working` or `Owner`
  and rejects unknown or ambiguous heads.
- Tests prove emitted heads and generated dispatch.

### Spirit contracts

Pinned both Spirit contract repos to the signal-frame commit above.

- `signal-persona-spirit`: commit `a9b3527a`.
- `owner-signal-persona-spirit`: commit `f4d268ef`.

No new owner-only operation was needed for this pilot: `Register` and `Start`
are already real owner-signal behavior and are enough to prove two-socket
routing without a test-only command.

### persona-spirit

Implemented, verified, and pushed commit `3ebc05af` in `persona-spirit`.

- `spirit` peeks the NOTA request head with `nota-codec`, routes through
  `SpiritCommandLineDispatch`, then decodes only the selected contract.
- Working requests use `PERSONA_SPIRIT_SOCKET` and
  `signal_persona_spirit::SpiritRequest`.
- Owner requests use `PERSONA_SPIRIT_OWNER_SOCKET` and
  `owner_signal_persona_spirit::OwnerSpiritRequest`.
- Owner replies encode back to NOTA through the same thin CLI boundary.
- CLI tests now prove generated dispatch, selected-socket missing errors, and
  an end-to-end owner request through the binary.
- Flake packages are split into `packages.spirit`,
  `packages.persona-spirit-daemon`, and `packages.full`; default is the CLI.

## Verification

- `CARGO_BUILD_JOBS=2 cargo test --locked` in `persona-spirit`: passed.
- `nix flake check -L --max-jobs 0` in `persona-spirit`: passed.

## Remaining Before Close

- Comment or update bead `primary-ojxq` (persona-spirit triad implementation).
