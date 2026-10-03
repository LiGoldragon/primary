# orchestrate-test: the Orchestrate test twin

`orchestrate-test` lives at `/git/github.com/LiGoldragon/orchestrate-test`, with its remote at `github.com/LiGoldragon/orchestrate-test` (public). It was created with `gh repo create`, and `main` was pushed at `97ed7804d29affafb56407f94c5f4b55aec38438`. Its first scenario is a pure Nix check that needs no credentials and no model. A second scenario, a light-model Claude run, is gated off and has not been run.

## Layout

The repository follows the numtide blueprint layout that compensation-nix prescribes, with persona-test as its sibling.

| Path | Role |
|---|---|
| `flake.nix` | Holds the inputs and `inputs.blueprint { inherit inputs; }`. `orchestrate` is pinned to `github:LiGoldragon/orchestrate/d80a617f7e03ebade846c41ac540b7d173d3d056` (0.35.0, main at the time), and its `nixpkgs` follows this flake's (`github:LiGoldragon/nixpkgs?ref=main`). |
| `lib/default.nix` | `flake.lib.components.orchestrate` and `flake.lib.cheapestModel`. |
| `lib/components/orchestrate.nix` | The Nexus and both clients from the pinned package. It also gives the socket and store paths relative to the XDG roots. `start` exports `ORCHESTRATE_SOCKET` and `ORCHESTRATE_META_SOCKET` and waits, bounded, until **both** sockets are bound. `stop` sends TERM and requires the Nexus to exit within 10 s. |
| `checks/orchestrate.nix` | The pure scenario `orchestrate`. |
| `packages/orchestrate-claude.nix` | The semi-sandbox runner `orchestrate-claude`, gated. |
| `checks/lint.nix`, `formatter.nix` | nixfmt --check, deadnix and statix; `pkgs.nixfmt`. |
| `README.md`, `AGENTS.md` (`CLAUDE.md` is a symlink to it) | How to run each scenario, and the house rules. |

## Scenario 1: `orchestrate` (pure check)

`orchestrate-nexus` is started with no arguments, with `XDG_RUNTIME_DIR` and `XDG_STATE_HOME` set under a `mktemp -d` root inside the build sandbox. It therefore opens a fresh store at `state/orchestrate-nexus/orchestrate-nexus.sema` and binds `orchestrate.sock` and `orchestrate-meta.sock`.

The stock `orchestrate` and `orchestrate-meta` binaries are then driven, each call under `timeout 10`. For each call the check compares the **whole** stdout and the exit code against literal text written in the check. That text comes from the documented contract and the earlier witnesses, not from the clients.

Output of `nix flake check github:LiGoldragon/orchestrate-test` after the push (rc 0, 112 s wall, on prometheus; 3 checks: `lint`, `orchestrate`, `pkgs-orchestrate-claude`):

```
orchestrate> orchestrate-nexus ready
orchestrate> observe-empty: Observed.Locks.[] (exit 0)
orchestrate> lock: Locked.{ 1 OrchestrateTestProbe 3ec648 [ /build/tmp.IvC7goUmL5/work/probe ] «two words» } (exit 0)
orchestrate> release: Released.{ 1 OrchestrateTestProbe 3ec648 [ /build/tmp.IvC7goUmL5/work/probe ] «two words» } (exit 0)
orchestrate> observe-released: Observed.Locks.[] (exit 0)
orchestrate> configure: Configured.{ { /build/tmp.IvC7goUmL5/runtime/orchestrate-nexus/orchestrate.sock /build/tmp.IvC7goUmL5/runtime/orchestrate-nexus/orchestrate-meta.sock } True } (exit 0)
orchestrate> orchestrate: torn down
all checks passed!
```

The first local `nix flake check` took 345 s wall (rc 0). Most of that was the remote builder compiling orchestrate against the followed nixpkgs. That run was of the tree before the exit trap described below was added.

**Seen failing.** A scratch copy expected `Locked.{ 2 …` and failed exactly there (rc 1):

```
orchestrate> lock: Locked.{ 1 OrchestrateTestProbe 3ec648 [ … ] «two words» } (exit 0)
orchestrate> lock: expected Locked.{ 2 OrchestrateTestProbe 3ec648 [ … ] «two words» } (exit 0)
```

The first two failing attempts never reached an outcome. One was an unrelated input fetch; both then waited on the builder's upload lock, which other flows' builds held, and hit the timeout. While working through this I found a real defect: without an exit trap, a failing assertion leaves the backgrounded Nexus holding the build log open, so a red check would hang instead of failing. The check now kills the Nexus in an `EXIT` trap, and the failing run above ended with rc 1 rather than hanging. Its 778 s was mostly the wait for the upload lock.

**What it proves:**
- The pinned 0.35.0 Nexus starts with no arguments on redirected XDG roots, opens a fresh store, and binds both designed socket names.
- The ordinary client turns a Lock whose reason is in guillemets into Signal, and the Nexus answers `Locked` with id 1.
- `Release.1` answers `Released` with the same record.
- Observe shows an empty lock set before the Lock and again after the Release.
- The meta client reaches `orchestrate-meta.sock`, and Configure with the same paths answers `Configured.{ { … } True }`.
- The Nexus exits on TERM.
- All of this runs with no network, no credentials and no model, inside the Nix sandbox.

**What it does not prove:**
- The restart and resume behaviour of a populated store, including the legacy `meta-orchestrate.sock` case in `witnesses/orchestrate-meta-socket.md`.
- Any refusal path, such as a duplicate name, a curly-quote reason, or an unknown id.
- That Configure to *different* paths takes effect.
- Peer-credential authority across users, because the build sandbox has a single uid.
- The CriomOS-home client wrappers. The check uses the direct binaries, not `~/.nix-profile/bin/orchestrate*`.
- The deployed live Nexus. The check runs the pinned rev rebuilt against `LiGoldragon/nixpkgs`, not the store path the live unit runs.
- Systems other than x86_64-linux.

## Scenario 2: `orchestrate-claude` (semi-sandbox, gated, not run)

`packages/orchestrate-claude.nix` is a `writeShellApplication` runner adapted from `witnesses/semi-sandbox-capsule.sh`.

Gate:
- The runner exits 2 unless `ORCHESTRATE_TEST_LIVE=1`. Running `nix run github:LiGoldragon/orchestrate-test#orchestrate-claude` without the flag printed the refusal and returned rc 2.
- In CI, `nix flake check` only builds the script (`pkgs-orchestrate-claude`) and never runs it.

How it runs: `ORCHESTRATE_TEST_LIVE=1 nix run github:LiGoldragon/orchestrate-test#orchestrate-claude`. The optional variables are `ORCHESTRATE_TEST_MODEL` (default `haiku`), `ORCHESTRATE_TEST_CLAUDE`, `ORCHESTRATE_TEST_CREDENTIAL`, `ORCHESTRATE_TEST_SKILL` and `ORCHESTRATE_TEST_KEEP`. The README has the table.

Kept from the capsule:
- The **unwrapped** `.claude-wrapped` binary. By default the runner finds it beside the real store path of the installed `claude`, because that wrapper prepends `--dangerously-skip-permissions`.
- `--permission-mode default` with the print-mode allow rule `--allowedTools Skill 'Bash(orchestrate:*)'`.
- `--strict-mcp-config`, `ENABLE_CLAUDEAI_MCP_SERVERS=false`, and the three `DISABLE_*` variables.
- `env -i`, with HOME and every XDG root under the run's own root.
- Only `.credentials.json` and the orchestrate skill are copied in.
- The bounds: `MemoryMax=2G` through `systemd-run --user --scope`, 600 s, and 12 turns.

Changed from the capsule:
- The root comes from `mktemp -d /tmp/ot-XXXXXXXX` (short enough for the 108-byte `sun_path` limit) and is removed in an exit trap, so no symlink alias is needed.
- The Nexus is the pinned flake build, not a hardcoded store path.
- Only the ordinary client is on the flow's PATH, not the meta client.
- The runner refuses to start when the access token expires within 15 minutes (it reads only `expiresAt`), and warns if the sandbox copy of the credential changed. This covers capsule gap 9.
- The Lock reason is bare (`RoundTrip`), as in capsule runs 2 and 3, because Haiku rewrote quote delimiters.

Assertions:
- A `success` result.
- `permissionMode` is `default`, and there are no permission denials.
- The exact `Locked.{ 1 … }` and `Released.{ 1 … }` lines appear in the transcript's tool results.
- Checked against the Nexus itself after the run: `Observe.Locks` is empty, and a fresh Lock gets id 2.

Not isolated, as in the capsule: the filesystem, and the account (the claude.ai skills still sync into the sandbox home).

## Open points

- The `orchestrate-claude` runner has never been run. Its first live run is the living's call.
- The `pkgs-orchestrate-claude` check builds the script but does not run it.
- `persona-test`'s working tree contains two stray directories, literally named `1625330{name}Home` and `1625330{name}Runtime`. They are leftovers from its `isolatedComponentEnv` (the Nix string `$${name}` renders as shell `$$` plus `{name}`). I did not touch them.
- The remote builder's upload lock is shared across flows, and long builds from other flows held it for tens of minutes. A bounded check can time out on that wait rather than on its own work.

## Update: orchestrate 0.36.1 and two restart scenarios

`main` is now `5f0d568ec0bafd3ebc3b6ee6eec1937b4ee892e0`. It pins `orchestrate` at `bc5cd36e81df395ed1f84e2e3e98d5a6ee90bf8c` (0.36.1). The brief named b56f2644 (0.36.0), and the coordinator then redirected the pin to bc5cd36e. The work was first proven at b56f2644 and then again at bc5cd36e.

### Pin

The `orchestrate` scenario passes unchanged in meaning at both revisions, and **no reply text changed**. Its five replies are byte-identical to the 0.35.0 run above, so no expected text was edited. The check file changed only in form: its root, its `expect` and its exit trap moved into the shared frame `lib/scenario.nix` (`flake.lib.scenario`).

### Component change

`start` used to wait for both socket files to exist. On a restart, the previous run's files are still on disk, so that wait proved nothing; this was the side observation in `witnesses/orchestrate-meta-socket.md`. `start` now writes the Nexus's stdout to `$XDG_RUNTIME_DIR/orchestrate-nexus.stdout` and waits, bounded, for the Nexus's own `orchestrate-nexus ready` line. `main.rs` prints that line only after `TransportRuntime::bind` has bound both sockets the store names.

`start` exports the default client socket paths only when the caller has not set them. Because of that, the `orchestrate-claude` runner now unsets both variables before `start`. Otherwise a value exported in the living's own shell could aim its after-run assertions at the live Nexus.

### Scenario `orchestrate-populated-store` (pure check)

The brief called it `populated-store`. It is named `orchestrate-populated-store` under compensation-nix's naming rule: components first, then a suffix to separate scenarios with the same components.

Steps:
1. Fresh store: `Lock` returns `Locked.{ 1 … }`.
2. TERM. The Nexus is required to exit within 10 s.
3. `start` again on the same directories.
4. `Observe.Locks` returns `Observed.Locks.[ { 1 OrchestrateTestProbe 3ec648 [ … ] «two words» } ]`. The vector form comes from orchestrate AGENTS.md.
5. A second Lock returns `Locked.{ 2 SecondProbe … }`, so the allocator persisted.
6. Meta `Configure` with the same paths returns `Configured.{ { … } True }`.

The previous run's socket files were still on disk, and a stale socket file refuses connections. A reply on each socket after the restart therefore proves that each one was bound again.

### Scenario `orchestrate-old-meta-name` (pure check)

The brief called it `old-meta-name`; it is renamed by the same rule. It reproduces the live store.

Steps:
1. Fresh store, then meta `Configure.{ «ord» «…/meta-orchestrate.sock» }` returns `Configured.{ { ord …/meta-orchestrate.sock } True }`.
2. TERM, then `start`.
3. The meta client at the legacy name returns `Configured` (exit 0).
4. At the default name it fails with empty stdout. Stderr is exactly `Unreachable.{ …/orchestrate-meta.sock «Unix socket I/O failed: Connection refused (os error 111)» }`, with exit 1.
5. The ordinary client is unaffected: `Observed.Locks.[]`.
6. Meta `Configure` back to `orchestrate-meta.sock` returns `Configured`.
7. TERM, then `start`.
8. The meta client at the default name returns `Configured`, and at the legacy name it gets the same `Unreachable … Connection refused` (exit 1).

**Correction to the earlier witness's wording.** A client failure is printed on **stderr**, not stdout. My first draft compared stdout and failed with an empty stdout, so the frame gained `expectFailure`. It requires stdout to be empty, the whole stderr to equal the expected text, and the exit code to match. The Unreachable text itself comes from the 0.35.0 witness and is unchanged in 0.36.x.

### Seen failing (at b56f2644, from a scratch copy with one expected value made wrong)

- `orchestrate-populated-store`, expecting id 7 after restart. rc 1 at exactly that step: `observe-after-restart: expected Observed.Locks.[ { 7 … } ]`, against the actual `{ 1 … }`.
- `orchestrate-old-meta-name`, expecting exit 0 from the legacy-name refusal. rc 1 at the last step, `meta-at-legacy-unreached: expected stderr Unreachable.{ …/meta-orchestrate.sock «… (os error 111)» } (exit 0)`, after every earlier step had passed.

### Green

The `nix flake check -L` runs were each made in a detached user unit (`systemd-run --user`, `RuntimeMaxSec=5400`, `MemoryMax=4G`), with builds on prometheus.
- At b56f2644: rc 0.
- At bc5cd36e: rc 0, with all four checks (`lint`, `orchestrate`, `orchestrate-populated-store`, `orchestrate-old-meta-name`) plus `pkgs-orchestrate-claude`.
- A first run at bc5cd36e failed in evaluation with rc 102 (`store path … contents have changed`) because I edited the README during evaluation. It was rerun clean.

After the push, `nix flake check -L --refresh github:LiGoldragon/orchestrate-test/5f0d568e…` against the remote flake returned rc 0 (`all checks passed!`). The check derivations were identical to the local green run, so they were already built.

### Still not proven

- A store actually written by 0.35.0 or earlier. The legacy name here is set by a 0.36.x Configure, not inherited from an old store.
- The CriomOS-home wrappers.
- The deployed live Nexus. The live remediation in `witnesses/orchestrate-meta-socket.md` was not performed.
- The `orchestrate-claude` runner is still unrun.

## Sources

- `/home/li/primary/flows/3ec648/witnesses/semi-sandbox-capsule.sh`, `/home/li/primary/flows/3ec648/reports/semi-sandbox.md`, `/home/li/primary/flows/3ec648/witnesses/orchestrate-meta-socket.md`, `/home/li/primary/flows/3ec648/witnesses/orchestrate-delimiter.md`.
- `/git/github.com/LiGoldragon/orchestrate` at d80a617f: `flake.nix`, `crates/orchestrate-nexus/src/defaults.rs`, `crates/orchestrate/src/main.rs`, `crates/orchestrate-meta/src/main.rs`.
- `/git/github.com/LiGoldragon/persona-test` (sibling layout).
- Build logs, in the scratchpad: `check1.log` (local, 345 s), `fail.log` (seen failing), `remote.log` (remote flake, 112 s).
- The living's words (STT, 2026-09-26 and 2026-10-02), as quoted in the main flow's brief.
- Update: `/git/github.com/LiGoldragon/orchestrate` at b56f2644 and bc5cd36e (`crates/orchestrate-nexus/src/main.rs`, `crates/orchestrate-meta/src/main.rs`, README, AGENTS.md, UPGRADES.md); logs in the scratchpad `ot-populated/` (`check.log` green at b56f2644, `fail-meta.log`, `check3.log` green at bc5cd36e, `remote.log`) and `fail-pop.log`.
