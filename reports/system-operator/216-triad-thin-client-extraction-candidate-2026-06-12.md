# 216 - Triad thin-client extraction candidate

## Context

During the component upkeep pass, `message` and `router` both needed the
same thin-client shape that Spirit already established:

- exactly one component argument through `triad_runtime::ComponentCommand`;
- NOTA text is accepted only at the CLI edge;
- the CLI decodes one contract-local input record;
- the client writes one length-prefixed Signal frame to the component socket;
- the client reads one typed reply;
- the CLI prints one NOTA output record.

The repeated implementation is now visible in:

- `message/src/command.rs` and `message/src/meta.rs`;
- `router/src/client.rs`, `router/src/meta.rs`, and `router/src/cli_argument.rs`;
- the generated daemon side in `triad-runtime` and `schema-rust-next`, which already centralizes the listener/startup half of the pattern.

## Why This Matters

The daemon side is becoming reusable through generated `ComponentDaemon`
and shared runtime listener code. The client side is still being hand-built
per component. That creates three risks:

- environment variable names, default sockets, and argument behavior can drift;
- each component repeats reply-frame decoding and rejected-reply mapping;
- adding the dual CLI pair to every component will copy the same small but
easy-to-get-wrong process-boundary code.

This is not blocking the current upkeep pass. The local implementations are
small and tested. It is still a clear extraction candidate once one or two
more components confirm the same shape.

## Candidate Shared Shape

The reusable home should likely be `triad-runtime`, because it already owns
`ComponentCommand`, `BindingSurface`, `LengthPrefixedCodec`, and daemon
listener mechanics.

The library should own:

- one-argument NOTA text/file loading;
- synthetic exchange identifier creation for one-shot connector calls;
- request frame construction for `signal_frame::ExchangeFrame<Input, Output>`;
- committed single-reply extraction;
- rejected-reply conversion into a typed runtime error;
- optional raw generated-frame mode for meta contracts that currently use
  `Input::encode_signal_frame` / `Output::decode_signal_frame` directly.

Each component should still own:

- the binary names (`router`, `meta-router`, etc.);
- the environment variable names (`ROUTER_SOCKET`, `ROUTER_META_SOCKET`);
- default socket paths;
- contract input and output types;
- component-specific user-facing error prefix.

## Recommendation

Do not pause component upkeep for this yet. Let the next component pass
confirm whether its ordinary and meta clients fit the same two modes:

- exchange-framed ordinary `signal-<component>` request/reply;
- raw generated meta `meta-signal-<component>` request/reply, unless schema
  emission standardizes meta onto the same exchange frame.

If the next component repeats the same client code, extract the client command
kernel into `triad-runtime` before modernizing the rest of the fleet. That
will keep the per-component code down to environment configuration plus type
aliases, which matches the psyche's reusable-component intent without forcing
the extraction prematurely.
