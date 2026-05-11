# 107 — Clavifaber WifiCertificate actor (primary-ari v1)

Closing report for `primary-ari`. Same shape as `primary-3t9`: name
the plane today as an actor; the future renewal driver attaches to
the same noun.

## What landed

Three clavifaber commits add a `WifiCertificate` actor that owns the
wifi-PKI cert lifecycle plane (server + client cert issuance) and
sits above the generic `CertificateIssuer` X.509 machinery.

| Commit | Subject |
|---|---|
| `7b27894` | Add actor — WifiCertificate routes Converge cert plans through the actor; idempotent skip on disk existence |
| `e43f25a` | Add tests — topology + skip-path trace witnesses + Converge succeeds with bogus keygrip when files exist |
| `10b7bed` | Document WiFi PKI plane in ARCHITECTURE.md + skills.md |

No CriomOS-side change needed: the wifi cert paths in `Converge` were
already routed through CriomOS today (zero config drift; just an
actor-routing change beneath the same NOTA surface).

## Plane shape

```
RuntimeRoot
  ├── HostIdentity
  ├── SshHostKey
  ├── GpgAgentSession        (DelegatedReply over spawn_blocking)
  ├── CertificateIssuer      (generic X.509 machinery)
  ├── WifiCertificate        (wifi-PKI domain plane; routes to CertificateIssuer; idempotent skip)
  ├── PublicationCollector
  ├── YggdrasilKey           (DelegatedReply over spawn_blocking)
  └── TraceRecorder (test-only)
```

`WifiCertificate` accepts:

- `EnsureWifiServerCertificate { plan: WifiServerCertificatePlan }`
  — if `output_certificate` and `output_private_key` both exist, skip;
  else load CA, ask `CertificateIssuer.IssueServerCertificate`, write
  cert (mode 0644) + private key (mode 0600) atomically.
- `EnsureWifiClientCertificate { plan: WifiClientCertificatePlan }`
  — if `output` exists, skip; else load CA, parse SSH public key, ask
  `CertificateIssuer.IssueNodeCertificate`, write cert (mode 0644)
  atomically.

Both `Reply = Result<(), Error>`. Not `DelegatedReply`: the `ask` to
`CertificateIssuer` doesn't block the runtime — `CertificateIssuer`
itself defers the gpg-agent IO to `GpgAgentSession`, which uses
`spawn_blocking`. The chain stays responsive.

The CA issuance plane (signing the cluster CA itself) is *not*
wifi-shaped — a CA can sign anything. So `Converge::run_actors`
keeps `converge_certificate_authority` as a free helper that calls
`CertificateIssuer.IssueCertificateAuthority` directly. Only the
server + client cert paths route through `WifiCertificate`.

## Witnesses

| Claim | Witness |
|---|---|
| Actor type carries data | `tests/actor_topology.rs::actor_types_carry_data_not_zero_size` (asserts on `WifiCertificate`) |
| Runtime root spawns the actor | `tests/actor_topology.rs::runtime_root_spawns_every_named_actor` (destructure includes `wifi_certificate`) |
| Actor sees server-cert request | `tests/actor_trace.rs::wifi_certificate_records_server_certificate_request` (skip-path; no gpg) |
| Actor sees client-cert request | `tests/actor_trace.rs::wifi_certificate_records_client_certificate_request` (skip-path; no gpg) |
| Skip on disk existence | `tests/converge.rs::converge_skips_wifi_certificate_issuance_when_files_already_exist` — Converge with bogus keygrip + nonexistent CA succeeds because pre-existing output files short-circuit the actor before any read or gpg-agent ask; markers in those files survive the run |
| End-to-end against real gpg-agent | `nix run .#test-pki-lifecycle` Phase 8 still passes — server + client cert issuance now flow through `WifiCertificate` and the resulting certs verify against the converged CA |

## Why no `DelegatedReply`

`actor-systems.md` forbids blocking inside a handler but allows
synchronous waits for another actor that doesn't call back upward.
`WifiCertificate.handle` awaits `CertificateIssuer.ask(...)`;
`CertificateIssuer.handle` awaits `GpgAgentSession.ask(...)`;
`GpgAgentSession.handle` is the one that wraps blocking gpg-agent IO
in `spawn_blocking` + `DelegatedReply`. Each link in the chain yields
to the runtime; no mailbox is held while the actual subprocess runs.

So `WifiCertificate` doesn't need its own `spawn_blocking`. The
`Reply = Result<(), Error>` shape is correct.

## Out of scope for v1 (parked)

- **Rotation.** No `RenewBeforeExpiry` message, no `not_after`
  ledger in redb, no timer-driven renewal scheduler. Bead notes
  name the design question: shared `RenewalScheduler` actor (one
  `timerfd` per rotation-bearing concern, deadlines durable in
  `clavifaber.redb`) vs per-domain timers. Same question affects
  `YggdrasilKey` (`primary-3t9`) and any future SSH-key rotation;
  the consolidation is downstream of `primary-mm0` (sandbox) so
  the renewal driver has somewhere to be tested.
- **redb cert ledger.** Will land alongside rotation. v1's
  idempotency is by file-existence-check, not by tracked deadlines.

## Test commands

```sh
cd /git/github.com/LiGoldragon/clavifaber
nix flake check                  # 8 checks; 30 cargo tests + chained state durability
nix run .#test-pki-lifecycle     # 8 phases; cert chain through WifiCertificate
```
