# 108 — Clavifaber actor + async-isolation audit (primary-jg1)

Closing report for the clavifaber half of `primary-jg1`. Chroma half
was already closed in commits 8a405492 + 4d5c3802 per the bead notes.

## What the audit was

Five constraints from the bead, scanned across `src/` and `tests/`:

1. **No production TODO/stub/unimplemented paths.**
2. **No raw hand-rolled async actor runtime.** Kameo is the runtime;
   no parallel actor abstraction.
3. **No shared `Arc<Mutex<…>>` / `Arc<RwLock<…>>` coordination
   between actors.**
4. **Blocking I/O isolated behind owned actors or bounded native
   calls.** Each blocking subprocess and syscall is owned by a
   named actor that wraps it in `tokio::task::spawn_blocking` +
   `DelegatedReply`.
5. **Tests guard the constraints.** Forbidden-edge witnesses,
   topology witnesses, trace witnesses.

## Findings

| Dimension | Finding |
|---|---|
| TODO / FIXME / XXX in production source | **None.** Clean grep across `src/` and `tests/`. |
| `unimplemented!()` / `todo!()` / `panic!()` / `unreachable!()` in production source | **None.** Clean grep across `src/`. |
| `Arc<Mutex<…>>` / `Arc<RwLock<…>>` / `Arc<tokio::sync::*>` between actors | **None.** Clean grep across `src/`. |
| Raw `tokio::spawn` outside known DelegatedReply patterns | **4 occurrences, all canonical.** All in `src/actors/gpg_agent_session.rs` (2) and `src/actors/yggdrasil_key.rs` (2) — wrapping the `(delegated, sender)` future after `spawn_blocking` returns. This is the documented Kameo pattern from `~/primary/skills/kameo.md` §"DelegatedReply<R>". |
| `std::process::Command` invocation sites | **3 owners, all correct.** `src/yggdrasil.rs` (yggdrasil binary; called only by `YggdrasilKey`), `src/gpg_agent.rs` (`gpgconf`; called only by `GpgAgentSession` via `GpgAgent::connect`), `src/actors/gpg_agent_session.rs` (gpg binary, inside `spawn_blocking`). |
| `fs::write` / `File::create` outside `util.rs` | **None.** `tests/forbidden_edges.rs::all_file_writes_go_through_atomic_file` enforces. |

## Tightening landed

The audit found one missing forbidden-edge witness: nothing
prevented a future agent from invoking the `yggdrasil` binary
outside the `YggdrasilKey` actor's plane. The `gpg_agent` module had
the same shape and is already locked by
`only_gpg_agent_session_owns_the_gpg_agent_connection`. Brought
yggdrasil to parity:

- `tests/forbidden_edges.rs::only_yggdrasil_key_owns_the_yggdrasil_binary`
  — static source scan for the `"yggdrasil"` literal and the
  `yggdrasil_binary` variable name; only `src/yggdrasil.rs` (data)
  and `src/actors/yggdrasil_key.rs` (actor) may match.
- `ARCHITECTURE.md` Constraints table gains a same-named row.

Landed as commit `f251188` (clavifaber).

## What's already guarded by witnesses (pre-audit)

| Constraint | Witness |
|---|---|
| Public actor types carry data (no public ZST) | `tests/actor_topology.rs::actor_types_carry_data_not_zero_size` |
| Runtime root spawns every named actor | `tests/actor_topology.rs::runtime_root_spawns_every_named_actor` |
| `HostIdentity` mailbox path on `EnsureIdentity` | `tests/actor_trace.rs::ensure_identity_witness_records_host_identity_receive_and_reply` |
| `LoadIdentity` precedes `WritePublicKeyProjection` | `tests/actor_trace.rs::public_key_derivation_runs_host_identity_then_ssh_host_key` |
| `EnsureYggdrasilIdentity` precedes `ReadYggdrasilProjection` | `tests/actor_trace.rs::yggdrasil_projection_runs_ensure_then_read` |
| `WifiCertificate` receives server + client cert messages | `tests/actor_trace.rs::wifi_certificate_records_server_certificate_request` + `…_client_certificate_request` |
| GpgAgent crate-private + only `GpgAgentSession` reaches it | `tests/forbidden_edges.rs::only_gpg_agent_session_owns_the_gpg_agent_connection` (+ `mod gpg_agent` in `src/lib.rs`) |
| All file writes through `AtomicFile` | `tests/forbidden_edges.rs::all_file_writes_go_through_atomic_file` |
| Yggdrasil binary ownership (NEW this audit) | `tests/forbidden_edges.rs::only_yggdrasil_key_owns_the_yggdrasil_binary` |
| Sema schema-version guard | `tests/state_schema.rs::sema_open_with_wrong_schema_version_hard_fails` |
| Convergence gate skips on identical input | `tests/converge.rs::converge_skips_when_input_hash_matches_last_converged` |
| Convergence re-runs on input change | `tests/converge.rs::converge_re_runs_when_input_changes` |
| Idempotent re-converge produces byte-identical publication | `tests/converge.rs::converge_is_idempotent_against_existing_identity` |
| publication.nota mode 0644 | `tests/converge.rs::converge_writes_publication_with_644_mode` |
| clavifaber.redb mode 0600 | `tests/converge.rs::converge_creates_state_database_with_600_mode` |
| Yggdrasil keypair file mode 0600 + 64-hex pubkey + IPv6 address | `tests/converge.rs::converge_with_yggdrasil_plan_populates_publication_and_keypair_file` |
| Yggdrasil keypair stable across re-converge | `tests/converge.rs::converge_with_yggdrasil_plan_is_idempotent_on_keypair` |
| WifiCertificate skips on disk existence | `tests/converge.rs::converge_skips_wifi_certificate_issuance_when_files_already_exist` |
| Private key bytes never on stdout/stderr | `tests/converge.rs::converge_does_not_emit_private_key_bytes_on_stdout` |
| Identity directory mode 0700; key.pem 0600; ssh.pub 0644 | `tests/identity_directory_lifecycle.rs::*` |
| Corrupt key quarantine | `tests/identity_directory_lifecycle.rs::complex_init_quarantines_corrupt_private_key_before_replacement` |
| State durable across processes (chained Nix) | `flake.nix` `checks.state-write` + `checks.state-read` |
| End-to-end against real gpg-agent + yggdrasil | `nix run .#test-pki-lifecycle` (8 phases) |

Total: **23 constraint witnesses guarded by tests**.

## Async-isolation surface

The blocking-IO isolation chain reads cleanly:

```
WifiCertificate          (Reply = Result<(), Error>; awaits ↓)
   ↓
CertificateIssuer        (Reply = Result<…, Error>; awaits ↓ via signer closure)
   ↓
GpgAgentSession          (Reply = DelegatedReply<…>; spawn_blocking around gpg + assuan)

YggdrasilKey             (Reply = DelegatedReply<…>; spawn_blocking around yggdrasil binary)

HostIdentity / SshHostKey / PublicationCollector
                         (Reply = Result<…, Error>; small synchronous file work; no
                          subprocesses; no mailbox hold during anything material)
```

Two actors anchor the spawn_blocking pattern (`GpgAgentSession`,
`YggdrasilKey`); upstream actors await them via `ask` without
re-introducing blocking. The runtime stays responsive.

## Acceptance status

| Bead criterion | Status |
|---|---|
| No production TODO/stub/unimplemented paths | ✓ |
| No raw hand-rolled async actor runtime | ✓ (Kameo only) |
| No `Arc<Mutex>` coordination | ✓ |
| Blocking I/O isolated behind owned actors or bounded native calls | ✓ (gpg-agent + yggdrasil are the only blocking IO; both wrapped) |
| Chroma + Clavifaber have tests guarding these constraints | ✓ (Chroma: per bead notes; Clavifaber: 23 witnesses including the new yggdrasil-ownership row) |

Audit closes. No further follow-up beads filed — the system is in
the shape the bead asked for.

## Test commands

```sh
cd /git/github.com/LiGoldragon/clavifaber
nix flake check                  # 8 derivations
nix run .#test-pki-lifecycle     # 8 phases
```
