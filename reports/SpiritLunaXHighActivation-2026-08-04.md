# Spirit Luna XHigh immutable activation — 2026-08-04

## Target and source chain

The authorized immutable user-environment target is CriomOS
`9b3d344631628cb19dda1a22af4d7ef25c5f8def`. Its locked release chain is
CriomOS-home `3dc0bada3f636065e7fd093711305a153dd5925a` and Spirit
`7405eee89e3b1b5b6764eb1a50cbdf467b93c9a7`.

The Lojix `UserEnvironment` activation request used that exact CriomOS revision
with `RequireImmutable`. Its reply text contained the requested revision, but
that was only an admission/request acknowledgement: Lojix later failed to show
the revision in its current-node record. It must not be treated as proof of an
active profile or generation. No store path, credentials, session material,
provider prompt/output, record body, Count value, or Marker value is recorded
here.

## Pre-activation and source gates

Before activation, bounded `Version`, `Count`, and `Marker` reads succeeded;
the judge and daemon user units were active and the three Spirit sockets were
present. The pre-read values were intentionally not emitted. A local witness
did not persist their hashes across its process boundary, so literal pre/post
equality is pending the independent verifier's retained pre-state witness.

The following source gates passed before activation:

- Spirit Rust suite with `nota-text`, including public-CLI negative grammar.
- Spirit release-input, service-bundle, and Nix test checks.
- CriomOS-home full flake check and `spirit-deployment` build.
- Lojix-materialized CriomOS flake check from both the local path and exact
  published origin, plus the exact-origin top-level system build.

An empty untracked local `checks/home-activation-equivalence` directory was
the sole initial full-check obstruction. It was claimed, verified empty, and
removed with non-recursive `rmdir`; no tracked source changed.

## Post-request local runtime observations

The following passed in the caller's local runtime context immediately after
the request, without emitting payloads. They are not attributed to the Lojix
target because the required Lojix current-node proof was absent:

- `spirit` reports version `0.27.0`.
- Judge and daemon user units are active; exactly three Spirit Unix sockets are
  present.
- The live judge argv contains `OpenAiCodex`, `gpt-5.6-luna`, and
  `(Some XHigh)`, and contains neither `gpt-5.6-terra` nor `(Some Medium)`.
- `spirit Version` and `meta-spirit ObserveHead` succeed.
- Both public CLIs reject zero operands, extra operands, `--pretty`, `--help`,
  and an existing raw file path.

The post-state hashes, over the raw typed replies and retained only as
non-content witnesses, are:

```text
Version 4dec7c56776bf522c41f3a6bcecd571476cecd4e7cfa6eb9574ea63292a24042
Count   369ec54a3bfd318438c31c53ed90007e389fb495780acca7e12259135188ed03
Marker  10cd7a826d754083fa6b8cc0088295afa6ffc9497a9d95ea46d8f501b98c46cf
```

No provider request was sent: no supported non-content provider-acceptance
interface was identified without constructing a judge request or exposing its
prompt/output. Service health and the configured live argv were verified
instead.

## Decision state

The independent verifier then found that Lojix did not retain the target
CriomOS revision in its current-node record. This fails the required active
profile/current-generation witness, so the target was rolled back immediately.
The raw activation and rollback replies were held only in transient shell
variables; they were not saved. No admission handle was issued or retained, and
one immediate `ByNode` query was made for each request; no poll series exists.
User-journal searches for either revision found no Lojix entry. No direct Home
Manager, NixOS rebuild, or other profile activation was performed.

The exact non-secret rollback request was a `Deploy(UserEnvironment(...))`
request for CriomOS `b46390940cf641e19bc9bbd243726308286a8bd2`, with
`ActivateNow`, `RequireImmutable`, `None`, and `[]`; it used the same approved
account/node/configuration reference as activation. The typed deployment reply
and subsequent node query both matched that immutable rollback revision. No
source commit was reverted.

Post-rollback gates passed without emitting record content: judge and daemon
are active, exactly three Spirit sockets are present, `Version` is `0.26.0`,
and `Marker` is `(25, 5374348791551424496)`. The live judge argv contains
`OpenAiCodex`, `gpt-5.6-terra`, and `(Some Medium)`, and contains neither
`gpt-5.6-luna` nor `(Some XHigh)`.

The published 0.27 source chain remains available, but a new activation may
proceed only after Lojix can retain and demonstrate its target current-profile
record alongside the bounded pre/post state witness.
