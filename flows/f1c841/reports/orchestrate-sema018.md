# orchestrate 0.37.1 on sema-engine 0.18.0

Landed. orchestrate main is `96e08e01` (orchestrate 0.37.1), one commit on
`c7c44cb3` (0.37.0). It repins sema-engine from 0.17.0 `489d290d` to 0.18.0
`9884905f` and changes nothing else: `Cargo.toml` (rev and workspace version),
`Cargo.lock` (sema-engine and the three workspace crates; sema-engine's own
dependency list is unchanged), and an `UPGRADES.md` entry.

No code change was needed. orchestrate never called `with_prior` or
`EvolutionStep`, which 0.18.0 removes, and never matches `sema_engine::Error`
exhaustively (it wraps it with `#[from]`), so the new error arms compile through.

## Store

Opens unchanged. sema-engine 0.18.0 keeps the engine storage layout number;
its new `__sema_engine_change_receipts` table appears only on a store's first
Memorable change, which orchestrate never makes. UPGRADES.md says so under
"0.37.0 to 0.37.1": no wire change, no store change.

Witnessed at process level with the two Nix-built packages
(`/nix/store/vxxc2x08...-orchestrate-0.37.0`, `/nix/store/d5b1yjk4...-orchestrate-0.37.1`)
on a fresh `XDG_RUNTIME_DIR` and `XDG_STATE_HOME`: 0.37.0 took Lock 1 and
stopped (exit 0); 0.37.1 resumed the same store, observed Lock 1, took Lock 2
and stopped (exit 0); 0.37.0 resumed it again and observed both Locks (exit 0).
Each start printed `orchestrate-nexus ready`.

## Gates

- `cargo test --workspace` in the worktree, under a 12G memory cap and a 1200s timeout:
  every suite passed, `live_nexus` 16 of 16 included.
- `nix flake check` on `git+file:///git/github.com/LiGoldragon/orchestrate?rev=96e08e01...`:
  all checks passed (build, carried-store, clippy, configuration-authority,
  datom-free-nexus, doc, fmt, live-nexus, meta-client, ordinary-client,
  ordinary-lock-contract, peer-authority, relocation, socket-claim, stopping,
  store-generations, test, test-doc).
- orchestrate-test at main `b8e2b971`, run with a transient
  `--override-input orchestrate github:LiGoldragon/orchestrate/96e08e01...`
  and `--no-write-lock-file`: all checks passed, among them
  orchestrate-previous-orchestrate (0.36.1 to this), orchestrate-rollback,
  orchestrate-live-orchestrate (live 0.35.0) and orchestrate-populated-store.
  Nothing in orchestrate-test changed: its main still pins orchestrate
  `c7c44cb3` (0.37.0), as the morning's Home candidate needs.

## Not done

- CriomOS-home is untouched. Its branch `f1c841-orchestrate-0.37` still carries
  0.37.0. Moving Home to 0.37.1 means repinning that input. Nothing requires it.
- orchestrate-test does not pin 0.37.1. Repinning it, and making 0.37.0 its
  previous release, is left until the Home candidate is settled.

## Sources

- sema-engine `UPGRADES.md` at `9884905f`, section 0.18.0.
- orchestrate worktree `/home/li/wt/github.com/LiGoldragon/orchestrate/sema018-f1c841`,
  commit `96e08e01401db7a703f2b59ce045b97df502cc07`; Lock 11714, released.
- Logs in this subflow's scratchpad: `cargo-test.log`, `flake-check.log`, `otest.log`.
