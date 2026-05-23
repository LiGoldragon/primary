# Component usage and tests

*Kind: Research - Topic: component NOTA usage - 2026-05-23*

## Claim

For a normal component author, NOTA appears at authored human edges:
CLI argv, startup/config files, examples, tests, and debug/audit
projection. It is not the daemon-to-daemon wire. Component daemons
compose through typed Signal frames and rkyv archives; NOTA is the
human-typed or human-readable projection of those same typed records.

The practical authoring rule is: write one typed positional NOTA
record, let `nota-codec` decode it into the contract type, then cross
the runtime boundary in the component's normal binary format.

## What components show today

`nota-config` is the clearest one-argument startup helper. A binary
calls `ConfigurationSource::from_argv()?.decode()?`; argv must contain
exactly one source: inline NOTA beginning with `(`, a `.nota` path, or
a `.rkyv` path. The crate rejects missing args, multiple args, unknown
extensions, and rkyv input for NOTA-only records. Its examples and
tests now use bracket strings such as `([we're ready] High)`.

`chronos` and `chroma` show the small daemon-client pattern:
`Request` and `Response` are `NotaEnum` plus rkyv archive types. The
CLI parses a NOTA request from argv, archives it, sends length-prefixed
rkyv bytes over the daemon socket, receives a response frame, and
prints one NOTA response. Their integration tests round-trip both NOTA
and rkyv for each request/reply family.

`signal-lojix` shows the contract-crate pattern. The crate owns
operation, reply, event, stream, newtype, and configuration records;
it has no runtime actors or storage. Configuration records live in the
contract surface too: `LojixDaemonConfiguration` supports NOTA and
rkyv through `impl_rkyv_configuration!`, while
`LojixCliConfiguration` is NOTA-only through
`impl_nota_only_configuration!`. Round-trip tests cover operation
records, subscription replies, daemon config, CLI config, rkyv config
decode, and the pure-contract no-runtime-dependency witness.

`clavifaber` is useful as a NOTA-only tool surface. It takes an
inline request, decodes a `ClaviFaberRequest`, executes, and prints a
`ClaviFaberResponse` as NOTA. Its current parser joins all argv tokens
before decoding, so it is not the strict model for new component
binaries, but its request/response and apostrophe witnesses are good.

`lojix-cli` is transitional production tooling, not the canonical
component shape. Its current README supports inline requests, request
files, and a no-argument default config file; it also joins split shell
tokens for inline records. Its `docs/basic-usage.md` still contains
old flag-shaped examples. Do not copy those behaviors into a new
component guide. The useful parts are its typed positional request
schema and its tests for bracket-string paths, extra path rejection,
and trailing-token rejection.

## The CLI pattern to teach

Teach component CLIs as one request source, not flag sets:

```sh
chroma "(SetWarmth Warm)"
chronos "(Subscribe [CivilDawn CivilDusk])"
clavifaber "(CertificateAuthorityIssuance ([ABC123] [Cluster CA] [/var/lib/clavifaber/ca.pem]))"
lojix-cli "(CheckHostKeyMaterial goldragon tiger [/tmp/operator's datom.nota])"
```

The important part is not the command names above; it is the shape:
one shell argument containing one NOTA request record. A new component
should reject extra argv tokens and reject trailing NOTA tokens after
the decoded record. If the binary needs discovery, use ordinary NOTA
help operations such as `(Help Main)` and `(Help (Verb Deploy))`, not
`--help`.

Bracket strings solve the apostrophe friction that made quote strings
awkward in shell examples:

```sh
# Legacy authored NOTA forced either shell escaping or nested quotes.
component "(Say \"we're ready\")"

# Bracket string: one shell double-quoted argument; apostrophe is ordinary text.
component "(Say [we're ready])"
```

This solves the normal apostrophe case, not every shell metacharacter.
If the NOTA text contains shell-sensitive content for the chosen outer
quote style, use a `.nota` file or choose the outer quoting
deliberately.

## Configuration guidance

Use `nota-config` for process startup configuration. The daemon config
record should name identity, socket paths, state paths, and bootstrap
policy path in one typed record. The CLI config record should contain
only client rendering/connection policy. Deploy plans, user commands,
and ordinary operations belong in request records, not startup config.

For component policy, follow the triad rule: `bootstrap-policy.nota`
is a first-start seed, not a lasting source of truth. After bootstrap,
policy changes flow through the owner-signal contract. For ordinary
user-authored data config, prefer deriving `NotaRecord`/`NotaEnum` and
parsing with `nota-codec`; `chroma`'s current config parser is an
implementation bridge that normalizes bracket strings before an older
custom AST path.

## Tests and examples

Name tests after the user-facing or architectural constraint, not the
syntax feature alone. Good current examples:

- `nota_argument_accepts_apostrophe_text_without_quote_delimiters`
- `source_path_with_apostrophe_must_not_require_quote_delimiters`
- `error_messages_with_apostrophes_do_not_require_quote_delimiters`
- `config_paths_with_apostrophes_do_not_require_quote_delimiters`
- `daemon_configuration_round_trips_through_nota_text`
- `cli_configuration_rejects_rkyv_bytes`
- `contract_crate_has_no_runtime_dependencies`

Keep tests Nix-owned. Pure Rust tests are acceptable when the flake
exposes them through `checks.<system>.default` or a named
`checks.<system>.<constraint>` output. `signal-lojix` is the best
named-check example: it exposes `test-round-trip`,
`test-contract-crate-has-no-runtime-dependencies`, doc, fmt, clippy,
and build checks. Stateful witnesses should also be flake outputs:
`chroma` exposes a sandbox terminal check/app, and `clavifaber`
exposes `test-pki-lifecycle` and `test-deployment-sandbox` apps.
Manual `cargo test` is only an inner-loop convenience.

For signal contracts, tests should prove both projections when both
matter: NOTA for CLI/debug examples and rkyv or Signal frame bytes for
the daemon path. A single round-trip through one text codec is not a
wire witness.

## Migration notes

For authored NOTA examples and expected output, migrate legacy quote
strings to bracket strings wherever practical:

- `"we're ready"` becomes `[we're ready]`.
- `"theme's palette is missing"` becomes `[theme's palette is missing]`.
- `"/tmp/operator's datom.nota"` becomes `[/tmp/operator's datom.nota]`.
- Multiline content uses `[|...|]` when that preserves the value.
- `]` and `\` inside inline bracket strings are escaped as `\]` and
  `\\`.

Do not confuse host-language string literals with authored NOTA quote
delimiters. Rust tests still need Rust quotes around the test string;
the migration target is the NOTA text inside those Rust strings.

For codec derives, migrate old `NotaSum` and `NotaUnitEnum` usage to
`NotaEnum`. `NotaEnum` now covers unit variants, data-carrying
variants, and mixed enums. Unit variants encode bare (`TailnetClient`);
data variants encode record-shaped (`(NixBuilder (Some 8))`);
single-field tuple variants encode the inner value after the variant
tag (`(PersonaDevelopment [agent runtime])`). Empty struct variants
should become unit variants, and multi-field tuple variants should
become named-field struct variants.

One stale-doc edge affects the guide: `signal-lojix` source has moved
to `NotaEnum`, but its `ARCHITECTURE.md` and `skills.md` still mention
`NotaSum`. A user guide should teach `NotaEnum` only, and treat old
`NotaSum`/`NotaUnitEnum` references as migration residue.

## Normal author checklist

1. Define the operation/configuration type in Rust with
   `NotaRecord`, `NotaEnum`, `NotaTransparent`, `NotaTryTransparent`,
   and `NotaMapKey` as appropriate.
2. Make the CLI consume exactly one request source and produce one
   NOTA reply or typed error.
3. Reject extra argv and trailing decoded tokens.
4. Use bracket strings in examples for prose, paths with apostrophes,
   paths with spaces, PascalCase string content, `None` as literal
   string content, and any content outside the bare alphabets.
5. Put every recurring example or constraint in a Nix-owned check or
   app.
6. Use constraint-style test names that explain why the behavior
   matters to users or architecture.
