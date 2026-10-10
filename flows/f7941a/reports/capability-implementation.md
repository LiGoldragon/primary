# Capability-authorized history implementation

The reusable producer landed on public Plannotator `main` at
`013912e008fff9aca24e2e8b4de13054d116aeeb`. The implementation is the new
`@plannotator/capability-history` package. It preserves the repository's actual
`GuideSnapshotV1` source contract and immutable public fixture bytes; it adds no
replacement guide or report format.

The broker issues random opaque `chv1.*` tokens and retains only their SHA-256
digests. Its server-side records bind each capability to issuer and subject
identity, audience, lineage anchor, scopes, artifact kinds or exact artifact
ids, past/future depth, expiry, revocation state, and parent capability. A child
capability can move only to a registered direct child flow. Its identity and
audience stay bound to the parent gateway, while scope, kind, resource, depth,
and expiry can only narrow. Revoking any ancestor invalidates every descendant.
Restarting the broker intentionally invalidates all tokens because capability
records are memory-only.

Source registration carries metadata only. `readArtifact` and `reconstruct`
finish capability, identity, audience, expiry, revocation, scope, resource, and
lineage authorization before calling the private `ArtifactSource`. Reads return
an observed source revision and digest. A read whose revision differs from the
registered expected revision is rejected as stale; an attested lineage map marks
freshness from the source observation rather than from the request timestamp.

For an authority anchored at `present` with one predecessor and one authorized
successor, reconstruction returns:

```text
past
`- present [current]
   `- future
```

An unrelated registered root and its artifact are absent from both the map and
source calls. The map therefore describes authorized nodes only; it does not
reveal that denied lineage exists.

The synthetic Unix HTTP server exposes two GET routes:

```text
GET /v1/artifacts/{opaqueArtifactId}
GET /v1/lineage/current?attest=1
Authorization: Capability chv1.<opaque-token>
```

It accepts no path or upload route, rejects request bodies, caps URI and header
sizes, caps artifact reads at 8 MiB by default, and sets header, request,
keep-alive, and per-socket request bounds. The public README contains a complete
synthetic producer example and the reproducible check command.

The private file authority proves a broker UID distinct from the worker UID and
requires broker-owned protected roots/state with no group or world access. Its
file source rejects path traversal, symlink components, non-regular files,
hardlinks, permission changes, oversize reads, and a file that changes while its
descriptor is open. Keys, capability records, artifact-id/path mappings, and
source bytes remain inside that authority API rather than in a worker-readable
namespace.

Private Unix serving is deliberately hard-disabled. Node/Bun does not expose
Linux `SO_PEERCRED` for this HTTP socket surface, so the static principal used by
the synthetic server cannot prove which same-UID flow connected. Enabling a
`private` flag would only declare isolation. Production serving needs an actual
peer-authenticated broker boundary, such as a small native acceptor that verifies
`SO_PEERCRED` and passes a witnessed gateway identity into the broker, with the
broker and its source/keys under an OS authority unavailable to workers. No
scoped private source or key was supplied in this flow, and no personal record,
parent transcript, cache, log, or prompt was read. Usable private history is
therefore not claimed.

The fail-first behavioral run reached five passing tests and failed the
path-shaped request contract (`403` observed where an absent route required
`404`). After the route witness and security cases were completed, the configured
remote builder passed 10 tests and 36 expectations. They cover authorization
before source access, exact guide-byte preservation, source-backed freshness and
stale rejection, authorized-only ASCII mapping, audience/time/depth/resource/kind
attenuation, inherited revocation, same-UID and permission rejection, symlink and
hardlink rejection, private-server fail-closed behavior, and real Unix-socket
artifact/map requests. The pushed revision was independently evaluated from its
GitHub URL and the same Nix check exited zero.

CriomOS-home commit `6fb30e0f1441` adds the desktop gateway, and integration
commit `9548d7d353dd` pins the pushed Plannotator producer. The configured remote check drove an HTTPS gateway
request through the actual pinned synthetic Unix broker and observed the returned
synthetic artifact. This proves the public end-to-end transport contract without
granting or reading private material.

## Sources

- Plannotator commits `c1f48dd30416` (fail-first contract), `9c2cefe4b970`
  (implementation), and `013912e008ff` (public usage and landed `main`).
- Plannotator `packages/core/guide-format.ts` and
  `packages/core/guide-format-fixtures.ts`.
- Plannotator `packages/capability-history/` and
  `checks/capability-history/default.nix`.
- Remote Nix check
  `github:LiGoldragon/plannotator/013912e008fff9aca24e2e8b4de13054d116aeeb#checks.x86_64-linux.capability-history`.
- CriomOS-home gateway commit `6fb30e0f1441`, integration commit
  `9548d7d353dd`, and their pinned synthetic broker gateway check.
- `flows/564f55/reports/codexLaunch.md`, `flows/219191/log.md`, and
  `flows/bc3530/log.md`, the three operational references explicitly authorized
  by the brief.
