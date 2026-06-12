# 217 - Criome meta-contract modernization gap

## Context

The `criome` upkeep slice refreshed the current triad without taking over
work that should be designed as a reusable pattern:

- `signal-criome` is on the current generated schema stack and now has
  `nota-text` checks in Cargo and Nix.
- `criome` is on the current runtime dependency stack, including current
  `sema-engine`, `triad-runtime`, and `signal-criome`.
- `meta-signal-criome` now has workspace docs, a flake, a committed lockfile,
  current toolchain/dependency pins, and NOTA-free default checks.

The slice is pushed:

- `signal-criome` commit `6c77bea0`: generated contract stack refresh.
- `criome` commit `4d29e2be`: runtime dependency stack refresh.
- `meta-signal-criome` commit `34a0c092`: flake/docs/dependency refresh.

## Remaining Gap

`criome` is not yet at the same real dual-CLI / generated-meta-contract shape
as the newest Spirit-derived pattern.

The blocking facts are:

- `meta-signal-criome` is still hand-written with `signal_frame::signal_channel!`,
  not a schema-derived contract with `schema/lib.schema`, generated artifacts,
  and schema freshness tests.
- `criome` does not yet expose a real `meta-criome` client binary over a
  separate meta socket.
- The daemon path is still a hand-written skeleton rather than a generated
  Signal/Nexus/SEMA runtime split.
- `meta-signal-criome` currently has zero behavioral tests; it only proves that
  the crate builds in default and `nota-text` modes.
- The next client extraction candidate from report 216 should probably land
  before duplicating more ordinary/meta thin-client code in `criome`.

## Recommendation

Do not paper over this by adding a one-off `meta-criome` binary against the
current hand-written meta contract.

The next real slice should be:

1. Move `meta-signal-criome` to a schema-derived `WireContract` shape.
2. Add canonical NOTA examples and generated round-trip/freshness checks.
3. Extract the repeated thin-client request/reply kernel into `triad-runtime`
   if the client shape has stabilized enough after `message`, `router`, and
   `criome`.
4. Then wire `criome` to expose ordinary and meta clients over separate sockets
   using the shared client kernel.

That sequence keeps the component-specific code small and avoids hardening the
current hand-written meta path into another pattern every later component must
unwind.
