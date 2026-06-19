# Kameo fork convergence and lifecycle audit

## Result

The production-facing Kameo split is converged everywhere I could safely touch
without colliding with active locks. Twenty-four repos now resolve `kameo` and
`kameo_macros` from `github:LiGoldragon/kameo`, branch `main`, commit
`f491b45d`. The prior persona POC no longer carries two Kameo packages in its
lockfile.

The remaining registry-sourced Kameo lock entries are:

| Repo | Why not changed in this slice |
|---|---|
| `spirit` | Already claimed/dirty under the active operator schema-propagation work. |
| `mirror` | Already claimed under the active operator schema-propagation work. |
| `lojix` | Claimed by system-designer for the live VM deploy-test chain. |
| `kameo` | The runtime repo itself; not a production consumer closure. |

`hexis` looked like a Kameo user only because the checkout was on an old
detached migration commit. Its current `main` has no Kameo dependency, so I
left it unchanged.

## What changed

Direct Kameo users now point at the fork in `Cargo.toml`, and every affected
root repo has a `[patch.crates-io]` entry so any transitive `kameo = "0.20"`
also resolves to the fork during that repo's build.

Direct dependency changes landed in:

| Repo | Main commit |
|---|---|
| `terminal` | `6d1f3703` |
| `kameo-testing` | `0256a08f` |
| `harness` | `81bcd004` |
| `triad-runtime` | `60e0ed7c` |
| `persona` | `6b6bc606` |
| `clavifaber` | `1397a6bd` |
| `introspect` | `7a6ecae7` |
| `repository-ledger` | `aca1a392` |
| `criome` | `454daf85` |
| `nexus` | `401dd326` |
| `terminal-cell` | `599a6fe6` |
| `chroma` | `19528b8d` |
| `system` | `334414c6` |
| `mentci` | `577d64b8` |
| `mind` | `57bb4daa` |
| `router` | `fb403c4c` |

Root-patch-only changes landed in:

| Repo | Main commit |
|---|---|
| `cloud` | `07683261` |
| `message` | `19845754` |
| `domain-criome` | `271bddc3` |
| `upgrade` | `5c653e34` |
| `schema-rust-next` | `e116cc46` |
| `agent` | `6a2d4fb4` |
| `orchestrate` | `4976a7e7` |
| `lojix-cli` | `a2c31daa` |

## Behavior audit

The fork is valuable in two distinct ways.

First, the `wait_for_shutdown()` terminal outcome is a better production and
test contract for resource-owning actors than a bare wait. The persona POC
proved this on `ManagerStore`: the test now waits for
`ActorStateAbsence::Dropped` plus `ActorTerminalReason::Stopped` before
reopening the same SEMA/redb path.

Second, the fork also changes `on_link_died`: the hook receives the peer's
final `ActorTerminalOutcome` as well as the older recursive
`ActorStopReason`. I updated `kameo-testing/tests/links.rs` to assert that a
killed linked peer reports `Dropped` / `Killed`, and documented the finding in
`kameo-testing/notes/findings.md`.

## Best next lifecycle uses

| Candidate | Benefit | Code that should change next |
|---|---|---|
| `router` | Highest next value. It supervises many internal actors and has ordered shutdown in `src/router.rs`. | Add tests that assert each stopped child reaches the expected terminal outcome before the router reports closed. |
| `criome` | High value. It owns store, registry, signer, verifier, authorization, and subscription actors. | Add teardown tests around `CriomeRoot` that assert store/registry actors terminate with normal outcomes and do not silently panic/cleanup-fail. |
| `triad-runtime` | High value because it underpins generated daemons. | Strengthen listener/request-gate shutdown tests to assert the terminal outcome, not just that `wait_for_shutdown()` returned. |
| `mind` | Medium/high value as the central state component. | Add store/engine actor shutdown witnesses once the current generated runtime shape stabilizes. |
| `terminal` / `terminal-cell` | Medium/high value for PTY/session lifecycle. | Use outcomes to distinguish clean session retirement from killed child/session cleanup failure. |
| `repository-ledger` | Medium value. Store and spool ingest actor can prove graceful close before restart/import tests. | Add terminal-outcome assertions around `RepositoryLedgerStoreActor` and `SpoolIngestActor`. |

No broad actor-code rewrite is needed just to adopt the fork. Most components
compile unchanged. The lifecycle API should be used where an actor owns a real
resource or where a supervisor's correctness depends on why a child died.

## Verification

- Lock/source scan across `/git/github.com/LiGoldragon/*/Cargo.lock`: after the
  changes, registry Kameo remains only in `spirit`, `mirror`, `lojix`, and
  `kameo` itself.
- `cargo metadata --locked` and `cargo tree -i kameo@0.20.0 --locked` through
  Nix-provided Cargo for every touched repo.
- `cargo check --locked` through Nix for `triad-runtime`, `persona`, `router`,
  `criome`, `mind`, `lojix-cli`, and `kameo-testing`.
- Persona lifecycle witness through Nix:
  `cargo test --locked --test manager_store constraint_manager_store_close_protocol_releases_storage_lock_before_shutdown -- --exact`.
- `kameo-testing` full test suite through Nix: `cargo test --locked`.
- `rustfmt --check` through Nix for the touched Kameo test files.

The host still prints the known flake-registry warning:
`input attribute 'owner' is missing`. It did not block Cargo resolution,
checks, tests, or pushes.
