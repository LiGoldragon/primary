# 106 — Clavifaber YggdrasilKey actor (primary-3t9 v1)

Closing report for `primary-3t9`. Two open follow-ups named at the
end.

## What landed

Five clavifaber commits and one CriomOS commit add a first-class
`YggdrasilKey` actor that owns the per-host Yggdrasil keypair file
and projects it (statically, no daemon) to the public hex key + IPv6
address consumed by `publication.nota`.

| Repo | Commit | Subject |
|---|---|---|
| clavifaber | `73b7a82` | Add actor — YggdrasilKey + typed YggdrasilPlan/Projection |
| clavifaber | `d473f7c` | Add tests — topology + ensure-then-read trace + idempotent keypair + publication populated |
| clavifaber | `36450d4` | Wire flake — yggdrasil in commonArgs + dev shell + state-write field shape |
| clavifaber | `260c01d` | Extend test-pki-lifecycle Phase 8 — Converge with YggdrasilPlan against real yggdrasil binary |
| clavifaber | `8cdaa8a` | Document Yggdrasil identity plane in ARCHITECTURE.md + skills.md |
| CriomOS | `b041b42` | complex-init Path = [pkgs.yggdrasil] + new Converge field shape |

## Plane shape

```
RuntimeRoot
  ├── HostIdentity
  ├── SshHostKey
  ├── GpgAgentSession        (DelegatedReply over spawn_blocking — gpg-agent IO)
  ├── CertificateIssuer
  ├── PublicationCollector
  ├── YggdrasilKey           (DelegatedReply over spawn_blocking — yggdrasil binary)
  └── TraceRecorder (test-only)
```

`YggdrasilKey` accepts two messages:

- `EnsureYggdrasilIdentity { keypair_path }` — idempotent; if the
  keypair file is missing, runs `yggdrasil -genconf -json`, extracts
  the `PrivateKey` field, and writes
  `{"PrivateKey":"<128 hex>"}` atomically with mode 0600. Returns
  `Result<(), Error>`.
- `ReadYggdrasilProjection { keypair_path }` — runs
  `yggdrasil -useconffile <path> -publickey` and
  `-address` against the persisted keypair file (no daemon),
  returning `YggdrasilProjection { public_key, address }`.

Both handlers use `tokio::task::spawn_blocking` + `DelegatedReply`
so the mailbox stays responsive while the yggdrasil subprocess runs
— the same shape `GpgAgentSession` uses for gpg-agent IO.

The yggdrasil binary is resolved from the process PATH (override:
`CLAVIFABER_YGGDRASIL_BIN`). CriomOS's `complex-init` systemd
service supplies it via `path = [ pkgs.yggdrasil ]`.

## Converge field-shape change

The opaque caller-supplied `yggdrasil_address` + `yggdrasil_public_key`
fields on `Converge` and `PublicKeyPublicationRequest` are gone.
Replaced by one typed field:

```nota
yggdrasil: Option<YggdrasilPlan>
  where YggdrasilPlan { keypair_path: String }
```

When `Some`, the runner asks `YggdrasilKey` to ensure the keypair,
reads the projection, and `PublicationCollector` writes the typed
strings into `PublicKeyPublication`. When `None`, the publication's
`yggdrasil_address` and `yggdrasil_public_key` stay `None`.

The published record `PublicKeyPublication` keeps both fields as
separate `Option<String>` values — that's the human-facing wire
shape per `clavifaber/skills.md`.

## Witnesses

Each load-bearing claim has a same-named test:

| Claim | Witness |
|---|---|
| Actor type carries data | `tests/actor_topology.rs::actor_types_carry_data_not_zero_size` (asserts on `YggdrasilKey`) |
| Runtime root spawns the actor | `tests/actor_topology.rs::runtime_root_spawns_every_named_actor` (destructure includes `yggdrasil_key`) |
| Projection runs ensure-then-read | `tests/actor_trace.rs::yggdrasil_projection_runs_ensure_then_read` |
| Converge populates publication via the actor | `tests/converge.rs::converge_with_yggdrasil_plan_populates_publication_and_keypair_file` (asserts mode 0600 + 64-hex public key + IPv6 address) |
| Keypair stable across re-converge | `tests/converge.rs::converge_with_yggdrasil_plan_is_idempotent_on_keypair` |
| Mailbox stays responsive during yggdrasil IO | Code-shape: `Reply = DelegatedReply<R>` + `spawn_blocking` per handler |
| Phase 8 against real yggdrasil binary | `nix run .#test-pki-lifecycle` (10 phases including yggdrasil keypair mode + 64-hex public key + stable across re-converge) |

`nix flake check` passes all 8 derivations including the chained
`state-write`/`state-read` durability witnesses.

## Why CriomOS sets `yggdrasil = None` today

The CriomOS systemd unit has `pkgs.yggdrasil` on PATH but the
`Converge` request still passes `None` for the yggdrasil field.
Reason: the existing `modules/nixos/network/yggdrasil.nix` module
still owns the runtime keypair via its own preStart seed step
(writing `preCriadJson` in the yggdrasild dynamic-user state dir).
If clavifaber also minted a keypair, the host would have two
separate Yggdrasil identities — the publication would carry one,
the running daemon would use the other.

The consolidation — clavifaber as the sole owner of the per-host
keypair, with `network/yggdrasil.nix` reading from clavifaber's
file instead of seeding its own — is named as follow-up below.

## Out of scope for v1 (parked)

- **Rotation.** No timer-driven renewal. The keypair is stable
  across re-converge by design (witness:
  `converge_with_yggdrasil_plan_is_idempotent_on_keypair`).
  The bead notes name the renewal scheduler shape (one shared
  `RenewalScheduler` actor over `timerfd` per
  `skills/push-not-pull.md` §"Named carve-outs", or per-domain) as
  an architecture review note for after the convergence runner is
  shipped.
- **End-to-end sandbox witness.** Acceptance criterion mentions
  `nix run .#test-host-lifecycle` showing a generated address.
  That sandbox is `primary-mm0` (system-assistant lane, currently
  someone else's). When it lands, it can call clavifaber with a
  `YggdrasilPlan` and inspect `publication.nota` — no clavifaber
  changes needed.

## Follow-ups to file

- **Clavifaber-as-sole-owner of the per-host yggdrasil keypair.**
  CriomOS bead. Move the `preCriadJson` seed step out of
  `modules/nixos/network/yggdrasil.nix` into clavifaber's plane;
  point both consumers (network module + clavifaber's
  `YggdrasilPlan`) at the same path; switch the `Converge` call in
  `complex.nix` from `yggdrasil = None` to a real
  `(YggdrasilPlan "...")`. Needs care around the dynamic-user
  state dir and ownership.
- **Rotation / renewal scheduler shape.** Architecture review
  note: shared `RenewalScheduler` actor (one `timerfd` per
  rotation-bearing concern, durable deadlines in
  `clavifaber.redb`) vs per-domain timers. Same question affects
  `primary-ari` (WifiCertificate) and any future SSH-key rotation.

## Test commands

```sh
cd /git/github.com/LiGoldragon/clavifaber
nix flake check                  # 8 checks; pure tests + chained state durability
nix run .#test-pki-lifecycle     # impure; 8 phases including Phase 8 yggdrasil
```
