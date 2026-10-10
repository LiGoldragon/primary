# Listener Wispr credential consumer

The portable Listener realization is pushed on bookmark
`listener-wispr-credential-consumer-4647d2` at `c613432be602`.

It replaces the two legacy Wispr GoPass lookups with one request-time
`wispr-flow/credentials` document read. Listener starts `gopass show -o`
with a piped stdout descriptor, null stdin and stderr, bounds the bytes, and
parses them inside the Listener process. The document is never placed in an
argument, ordinary environment variable, file, error, log, persistent job,
fixture, snapshot, or command output.

The parsed in-process session supplies the bearer, provider user identity, and
persisted UUID-shaped desktop session ID together. Supabase documents derive
the user from nested `user.id`; WorkOS documents derive it from the JWT
`urn:wispr:user_external_id` claim. Request IDs are generated in UUID shape.
`openai/api-key` was not changed.

The behavioral test was first run red when the provider session identifier did
not exist in the parsed state. The green test set covers both supported
session variants, a single request-time document shared by bearer and wire
identity, and rejection of a document missing the session identifier. The
full Nix `test` check passed from the configured remote builder. No Wispr
contact, deployment, or real credential read was performed.

The Nix Clippy check remains non-green on nine existing warnings: five are in
unchanged non-Wispr files and four are in unchanged Wispr parsing/backend
sections. That gate is not evidence against the committed consumer contract.

Integration constraints: this is a feature bookmark, not `main`; it must be
reconciled with the continuing sandbox and the two currently locked Wispr
workspaces before integration. Credential provisioning and any live provider
verification remain separate authorized work.

## Sources

- `/home/li/primary/flows/4647d2/vision/listenerWisprFlow.md`: the living's GoPass credential-store and Listener-loading direction.
- `/home/li/primary/flows/4647d2/reports/prior-flow-state.md`: established Listener isolation, prior credential names, current workspaces, and identity evidence.
- `/tmp/listener-wispr-auth-01a0539e.lBulYC/src/wispr.rs` at commit `c613432be602`: request-time descriptor reader, in-process parsing, and behavioral tests.
- `cargo test --lib credential_document_derives_the_provider_identity_for_supported_sessions`: red witness before the session-ID implementation.
- `cargo test --lib credential_document_`: green focused behavioral tests.
- `nix build --no-link --print-out-paths 'path:.#checks.x86_64-linux.test'`: remote Nix test check, producing `/nix/store/hy3pliwn8j0fb0mbslnhirlbmr492i63-listener-test-0.17.0`.
