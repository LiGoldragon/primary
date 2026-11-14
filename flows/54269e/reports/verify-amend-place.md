# Verification on ouranos: Configure.Amend, and the Nexus place file

Tested 2026-11-14 against live Flow 0.56.2 (`/nix/store/nwwm7mri...-flow-configured-0.56.2`, PID 654687, flow eabddc8d). Scratch is `/tmp/tmp.Ldh7XpNUmU` (made with mktemp -d). It holds every read, the diffs and the throwaway runner `run-throwaway.sh`.

## 1. Single-value configuration: passes

**The input form.** Flow eabddc8d pins meta-signal-flow at `cdb4e7df` (Cargo.toml `rev = "cdb4e7df3e52065c8c28c6f936e2f6f6fa285c9b"`, version 79.0.0). Its `ethos/signal.ethos` declares `Configure.Amend.{ Address Change }` and `Change.[ Workspace.Option<Root> Purpose Kind.FlowKind Continuity Add.Element Remove.Element ]`. The contract's own test writes the input as `Configure.Amend.{ { Mind atomicTrialAlpha Luna } Purpose.«Alpha after» }`.

**The target.** `{ Mind survey Sol }`, OnDemand. Its original Purpose occurs once in the configuration:
`«Surveys the active repositories one at a time: what the code is, the tests that test nothing, the convoluted code; one page each to Psyche core Opus.»`

**The sequence**, one Amend and its reverse, each between full reads:

```sh
flow-nexus-meta 'Configuration' > c0.datom                                   # exit 0
flow-nexus-meta 'Configure.Amend.{ { Mind survey Sol } Purpose.«Verification probe 54269e: temporary purpose, restored at once.» }'
# Configured.Amend.{ { Mind survey Sol } Purpose.«Verification probe 54269e: temporary purpose, restored at once.» }
flow-nexus-meta 'Configuration' > c1.datom                                   # exit 0
flow-nexus-meta "Configure.Amend.{ { Mind survey Sol } Purpose.«$ORIG» }"
# Configured.Amend.{ { Mind survey Sol } Purpose.«Surveys the active repositories ... to Psyche core Opus.» }
flow-nexus-meta 'Configuration' > c2.datom                                   # exit 0
```

**What the diffs show:**

- sha256 of the three reads:
  - c0 `5a833253...`
  - c1 `7f9fae10...`
  - c2 `5a833253...`
- c0 and c2 are byte-identical, so the undo left nothing behind.
- c0 to c1, split one permaflow per line: `diff` shows one changed line, line 27, which is `{ Mind survey Sol }`. The word diff shows only the Purpose text.
- Exact check: replacing that one Purpose string in c0 with the new text gives exactly c1 (`c0.replace(o, n) == c1: True`). No other byte of any other permaflow or family differs.
- The Counters `{ 17323 4513 4236 }` were the same in all three reads, so live traffic added no noise to the comparison.
- The Flow journal for those minutes holds no refusal or error.

## 2. A Nexus starting from a place file: not built in the live Flow

**What is live (flow eabddc8d, CriomOS-home 39c86609):**

- The daemon is started with one place datom as its argument. Home's unit runs `flow-nexus-daemon "{ «main» «/run/user/1001/nexus/main» «/home/li/.local/state/nexus/main» }"`.
- A fresh memory is seeded with the Nexus row that is compiled into the executable. The mechanism is the `executable-default-configuration` feature with `SeedsExecutableDefault`, built by `nix/mk-flow-package.nix`, `mkFlowPackage { defaultConfiguration }`.
- The other families are declared after the start. The oneshot `flow-configure-0550.service` (`configure-flow-0550` plus ten datom files) sends them over the meta socket.
- No `.signal` place file is read. `strings` on the live `flow-nexus-daemon` finds no `flow-nexus.signal`. No `nexus-configure` exists in the Nix store, and CriomOS-home main has no `.signal` and no `-configure` tool for it.

**What exists unmerged:** branch `pko0-e3a7d1` in flow (8f78c733, e33eb116) and in translator (130c27a, ba3794e, translator 0.6.0 with `nexus-configure`), plus a build-base branch. Neither flow nor translator is merged to main. The report is `/home/li/primary/flows/e3a7d1/pko0-report.md`, gate green at 8f78c73.

That branch differs from the design in the brief:

- Its file `$XDG_CONFIG_HOME/nexus/<place-name>/flow-nexus.signal` holds only the Place: Runtime and State.
- The tool is the shared `nexus-configure 'Compile.{ <datom file> <signal file> }'`, not `flow-nexus-configure`.
- A new memory always starts unconfigured, and configuration still arrives over meta after the start.
- With no file, the Nexus starts at the default directories.
- A file that does not decode stops the start, naming the file.

The configurator proposal `/home/li/primary/flows/011913/proposals/configurator.md`, where the file carries the Nexus's Configuration, is not built anywhere I found.

**Throwaway test of the live binary.** `run-throwaway.sh` runs the live `flow-nexus-daemon` under `env -i` with HOME and every XDG directory inside the scratch directory. It uses its own place directories, its own sockets and a fresh memory, and queries the throwaway Nexus with the live `flow-nexus-meta`, configured by `{ main }` in the scratch config home.

```sh
env -i PATH=$PATH HOME=$R/home XDG_CONFIG_HOME=$R/config XDG_RUNTIME_DIR=$R/run XDG_STATE_HOME=$R/state ... \
  flow-nexus-daemon "{ «main» «$R/run/nexus/main» «$R/state/nexus/main» }" &
flow-nexus-meta 'Configuration'
```

| run | file at `config/nexus/main/flow-nexus.signal` | memory before | Configuration answer |
|---|---|---|---|
| A | none | empty | `Configuration.{ { /home/li/primary { …codex-stable… } { …codex-next… } … default } [] [] Unconfigured … { 1 3 1 } 64 3 Unconfigured }` |
| B | `not a signal frame` (garbage) | empty | byte-identical to A |

What the runs show:

- With no file, the live binary does not start unconfigured. It comes up with the compiled-in Nexus row, and every other family is empty.
- A file at the designed path is not read at all. The pko0 branch would refuse a garbage file, naming it.
- I could not test a compiled place file, because no `nexus-configure` is built.
- Both daemons stopped on SIGTERM with exit 0 and printed nothing. Neither spawned a child process.
- The live `flow*.sock` inodes and mtimes are unchanged, and `flow-nexus-0550.service` is still active.

## Found along the way, not fixed

- The live configuration's Curriculum path is `/run/user/1001/curriculum/curriculum.sock`, set by the configure oneshot. A fresh memory's compiled seed carries the placeholder `/run/flow-0550-undeclared-runtime/curriculum/curriculum.sock`. A new memory therefore depends on the oneshot to correct it.
