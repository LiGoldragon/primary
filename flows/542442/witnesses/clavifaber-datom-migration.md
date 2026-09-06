# ClaviFaber migration witness

## Published ancestry

- Baseline main: `d0488014bf931a4690cc2f64a0b41c1df3435cab`
- First migrated producer: `3ede427858d9734488be7a3e51bb24f318700f35`
- Final published main: `2203f677d3448d99269d66386d35683cd10a05ef`

The published history is forward-only:
`3ede4278 → a651c75e → 8449c36d → a45f1d23 → 8ed3aaea → 2203f677`.

## Public contract

The active no-optional request decodes as:

```text
PublicKeyPublicationWriting.{ ouranos { /etc/ssh/ssh_host_ed25519_key.pub } None None /etc/criomOS/complex/publication.datom }
```

Its reply is:

```text
PublicKeyPublicationWritten.{ /etc/criomOS/complex/publication.datom }
```

Optional locations use `Some.{ <path> }`. The public file is a direct product
`{ <node> <ssh-public-key> <optional-yggdrasil> <optional-wifi-certificate> }`;
it is not a request/reply envelope or a nominal compatibility wrapper.

`tests/request_surface.rs::documented_operator_examples_decode_without_execution`
decodes all six literal operator examples, including `Some.{ ... }`, without
executing a request.

## Gates

The final `2203…` test-only successor has the first four terminal receipts
below. Its local suite contained 28 tests, including the six-literal
decoder-only witness. The two packaged app receipts are for `8ed3…`, the
immediately preceding writer/package source; `2203…` changes only
`tests/request_surface.rs`. No packaged-derivation identity is claimed from
that source fact.

```text
cargo fmt --check
cargo test --all-targets
cargo clippy --all-targets -- -D warnings
nix flake check --option max-jobs 0 --option builders '@/etc/nix/machines' --option fallback false
```

At `8ed3aaeaef594c8d61a60b59ac50af0d75093d7d`, these two packaged app
commands separately terminaled with exit 0:

```text
nix run --option max-jobs 0 --option builders '@/etc/nix/machines' --option fallback false .#test-pki-lifecycle
nix run --option max-jobs 0 --option builders '@/etc/nix/machines' --option fallback false .#test-deployment-sandbox
```

The attached Nix check covers build, test, formatting, clippy, and generated
Ethos freshness. At `8ed3…`, the packaged PKI fixture exercised real temporary
GPG, certificate issuance/verification, keypair idempotency, and a
`publication.datom` mode 0644 write. At that same revision, the rootless bwrap
fixture exercised the writer/reply boundary, host-visible public output, and
absence of a ClaviFaber-owned SSH private key.

The initial generated freshness check incorrectly assumed the output filename
survived Nix store source naming; `a651c75e` changed it to require exactly one
generated Rust file and compare that file. The temporary PKI and bwrap
fixtures then exposed and corrected stale legacy wrapper assertions in
`8449c36d`, `a45f1d23`, and `8ed3aaea`; the final gate above covers the
resulting contract.
