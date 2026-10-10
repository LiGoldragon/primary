# ClaviFaber authored-skill review

This is a review-only patch. It has **not** been applied to
`/home/li/wt/github.com/LiGoldragon/clavifaber-datom-542442/skills.md`.
That file is an authored repository skill and requires the separate
psyche-interraction approval described by the flow before any edit.

## Source and basis

- Source: `/home/li/wt/github.com/LiGoldragon/clavifaber-datom-542442/skills.md`
- Read-only source SHA-256: `4f4fddfd92e55f507b5882e9bd744edb527d4ad4ef53ee1bd11f2b1bd706b295`
- Producer main: `2203f677d3448d99269d66386d35683cd10a05ef`
- Proposed patch: [clavifaber-skill-review.patch](clavifaber-skill-review.patch)

## Proposed changes

The patch changes only the stale current-codec instruction: Dotos request and
response terminology, the six operator examples, generated-source ownership,
the public filename, and the fifth Nix check. It preserves the skill's scope,
private-material rules, actor topology, idempotency, operator override, and
force-rotation guidance.

The examples are decoder-valid literal Datom values. They are not executable
production requests: their authority identifiers and file paths are fixtures.
The public publication is a direct generated `PublicKeyPublication` product,
not a request/reply envelope or a nominal text wrapper. Its active filename is
`publication.datom`; retained `publication.dotos` is not interpreted or
rewritten by this release.

## Validation

The exact public writer request with no optional planes is:

```text
PublicKeyPublicationWriting.{ ouranos { /etc/ssh/ssh_host_ed25519_key.pub } None None /etc/criomOS/complex/publication.datom }
```

It replies:

```text
PublicKeyPublicationWritten.{ /etc/criomOS/complex/publication.datom }
```

The current optional location form is `Some.{ <path> }`, as the proposed sixth
example shows. `tests/request_surface.rs::documented_operator_examples_decode_without_execution`
decodes all six literal examples without touching their fixture paths.
`cargo test --all-targets` also exercises generated request/reply round trips
and direct publication decode; attached remote `nix flake check` passed with
its generated-source freshness check. The packaged temporary PKI and rootless
bwrap fixtures passed against the preceding equivalent writer/package source;
the final main adds only this decoder-only documentation witness.

## Decoder dry-run receipt

At producer main `2203f677d3448d99269d66386d35683cd10a05ef`,
`cargo test --all-targets` terminaled with exit 0 and included
`documented_operator_examples_decode_without_execution`. That test calls only
`ClaviFaberRequest::decode` on each of the six literal examples; it does not
call `execute`, open their fixture paths, issue certificates, or write files.

## Patch applicability dry run

The unchanged source `skills.md` was copied to a fresh disposable directory,
then `patch --dry-run -p1 -i clavifaber-skill-review.patch` ran from that
directory. It printed `checking file skills.md` and exited 0. The copy was
removed with its disposable directory; no authored skill file was modified.
