# 116 — lojix-cli `CheckHostKeyMaterial`: orchestrator-side host-vs-cluster diff

Closes `primary-da7` (option 1 — report-only diff). Implements
the orchestrator-side check that report 113 deferred as "designer
decision pending."

## What landed

| Change | Location | Commit |
|---|---|---|
| New NOTA verb `CheckHostKeyMaterial`: SSH the host, cat its `publication.nota`, decode via `clavifaber::publication::PublicKeyPublication`, diff against horizon-projected per-host `Node` fields, print per-mismatch report | `lojix-cli` `src/check.rs` (new, ~250 lines) | `128ca667` |
| `LojixRequest` enum gains `CheckHostKeyMaterial(...)` variant; `LojixRequest::into_deploy_request()` (LojixRequest-level) removed (not every variant deploys); per-variant `into_deploy_request` retained on `FullOs`/`OsOnly`/`HomeOnly` | `lojix-cli` `src/request.rs`, `src/main.rs` | `128ca667` |
| Exit-code shape: 0 clean / 3 mismatches / 1 error (so `if lojix … ; then` is a meaningful operator gate) | `lojix-cli` `src/main.rs` | `128ca667` |
| `clavifaber` drops `branch = "main"` URL parameter on its `nota-codec` git dep so the parametrised and unparametrised URLs collapse to a single source-of-truth in downstream lock files | `clavifaber/Cargo.toml` | clavifaber `4e666c8a` |
| Refresh stale `Decoder::nota(...)` -> `Decoder::new(...)` (nota-codec retired the dialect wording) in `src/cluster.rs`, `src/request.rs` | `lojix-cli` | `128ca667` |
| Document the new verb + the non-deploy-verb category | `skills.md`, `ARCHITECTURE.md` | `bda23d23` |

Test surface: 45 cargo tests across 8 binaries + 4 nix flake check
derivations all green. Three unit tests for `base64_from_ssh_line`
in `src/check.rs`; one new NOTA round-trip test for the verb in
`tests/request.rs`.

## Shape rationale

Why orchestrator-side rather than host-side (per `primary-da7`
option A): the host's clavifaber stays cluster-unaware. It only
knows its own keys, not what the cluster DB expects. Asking
"does the host's material match the cluster?" is a question only
the orchestrator can answer. Putting the check in clavifaber
would have required threading the cluster DB through to every
host — exactly the coupling the system was shaped to avoid.

Why report-only (per `primary-da7` option 1): no mutation. The
operator hint per mismatch points at the `rm` + clavifaber-verb
sequence to converge (which exists because of the loud-fail
policy from report 113). The verb is a diagnostic, not a
remediation. Operators decide what to converge.

Why exit code 3 on mismatches: CI gates and operator scripts
need a meaningful non-zero. 1 stays reserved for "the check
itself failed" (SSH down, publication missing, decode error).

## Verb shape

```nota
(CheckHostKeyMaterial <cluster> <node> <source>)
```

- `cluster: ClusterName` — viewpoint cluster.
- `node: NodeName` — host being checked.
- `source: ProposalSource` — path to the goldragon datom that
  serves as the haywire-stage cluster DB.

The verb projects horizon, SSHes the host, reads
`/etc/criomOS/complex/publication.nota`, parses it, then diffs:

- SSH base64: `horizon.node.ssh_pub_key.as_str()` vs the
  base64 stripped from `publication.open_ssh_public_key`'s
  `ssh-ed25519 <base64> [<comment>]` line.
- Yggdrasil pubkey + address: `horizon.node.ygg_pub_key` /
  `ygg_address` vs `publication.yggdrasil` (both `Option`,
  three-case match).

Each mismatch carries a `concern` tag, `expected` (horizon),
`actual` (host), and an `operator_hint` naming the rm + clavifaber
verb pair that converges.

## Dep-graph fix worth its own note

The first `cargo check` after wiring the dep failed with "multiple
different versions of crate `nota_codec` in the dependency graph"
even though every entry resolved to the same revision. Cargo treats
`git = "<url>"` and `git = "<url>", branch = "main"` as distinct
sources because the parametrised query string differs. clavifaber
was the only repo using the parametrised form; `lojix-cli` and
`horizon-rs` were already on the unparametrised form. Aligning
clavifaber to the unparametrised form collapses the graph. Worth
remembering for any other crate that pulls clavifaber transitively.

## Skill discipline

`skills.md` now has a "Non-deploy verbs" section that names the
shape rules for non-deploy verbs:

- `NotaRecord`-derived struct, variant on `LojixRequest`.
- `main.rs` branches on the variant; exit codes 0/3/1.
- No host mutation through this path — route mutation through
  clavifaber's NOTA surface; don't grow a second.

If a future verb wants to mutate, it goes through clavifaber.
This keeps the orchestrator a read-side party and preserves the
property that the host's mutation paths are auditable from one
binary.

## Crates touched

- `lojix-cli`: `128ca667` (verb), `bda23d23` (docs).
- `clavifaber`: `4e666c8a` (dep alignment).

## Follow-ups

- The shared cluster cache notarinfo timeout during
  `nix flake check` is unrelated. The flake check passed; cargo
  resolved against the public fetcher.
- Operator usage example for the verb belongs in `README.md`
  next time someone touches the README. Not added in this pass
  because no other verbs are documented at that level there yet
  and a single-verb example would set an inconsistent precedent.
