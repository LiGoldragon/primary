# CriomOS-home Flow 0.16.0 / Message 0.16.0 — state at wind-down

FLOW_ID e167d8, 2026-09-26. Written at a wind-down instruction; the bookmark is
complete and pushed, the aggregate check is unfinished.

## Bookmark and base

- Bookmark: `flow-message-016-e167d8` in CriomOS-home.
- Revision on the real remote (`git ls-remote ssh://git@github.com/LiGoldragon/CriomOS-home`):
  `648ae6cfe43b6196ac758039fb607a0ad275bb99`.
- Base: `integration-2-b860be` `5ed097a167e6103facbbc19566833a85dd9c5f83`
  (2026-09-26 00:54), the newest Home integration head; `main`
  `4a9d85d72b0c4057cf82293175a882cbde199b87` is its ancestor, and
  `integration-2-da88cf` `8a60835c` is an ancestor too. Nothing was asked of
  another flow.
- Worked in jj workspace `/home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-message-016-e167d8`
  under Orchestrate lock 7115 (released at wind-down). Locks 7031/7032 were
  already absent from `Observe.Locks`; nothing of da88cf's was touched, and main
  was never written.

## What the commit does

- `flake.nix`: `flow` → `github:LiGoldragon/flow/9aa9bf88e3ff6f3b68864eb300ee009897162ef4`,
  `message` → `github:LiGoldragon/message/f1843dbaa63f38634dc10d3b28df2f4a482d6d35`.
  `flake.lock` updated for those two inputs only. They share signal-flow
  `1c9e4b30` and meta-signal-flow `cbea31ef`, so they must move together.
- `modules/home/profiles/min/message.nix` rewritten. `message-nexus` with no
  arguments (0.16 refuses any argument vector but `--version`); unit renamed
  `message-nexus.service`; the profile wrapper, `message-write-configuration`,
  the `meta-message` wrapper and the pre-open preserver are gone, because
  `message` and `message-meta` already default to
  `$XDG_RUNTIME_DIR/message/{message,message-owner}.sock`, the sockets the
  Nexus serves. It sets `criomosHome.flow.messageNexusPath`.
- New declared, idempotent activation step `retireMessengerStore`: moves
  `messenger.sema`, its `.preopen` sidecars and `message-daemon.signal` into
  `~/.local/state/message/retired-0.14/`. It refuses rather than overwrite
  anything already retired, so no ledger can be lost to a second activation.
  The new store `~/.local/state/message/message.sema` is created by the Nexus
  itself.
- `modules/home/profiles/min/flow.nix`: new `criomosHome.flow.messageNexusPath`
  option and a new `flow-configuration.service` (oneshot, RemainAfterExit,
  After/Requires/PartOf `flow-nexus.service`). **How Flow 0.16 takes this
  configuration**: `MessageNexusPath` and `MetaAspects` exist only in the meta
  `Configuration` record — `DeploymentOverrides` reads `FLOW_SOURCE_ROOT` and
  `FLOW_CODEX_*` and nothing else — so the only route is one
  `flow-meta 'Configure.{ … }'` over the meta socket. The unit waits for the
  meta socket to appear (bounded, 30 s) and fails unless the reply is
  `Configured.…`. Admission works because a systemd user unit runs in no pane,
  which Flow resolves as the owner (`crates/flow-nexus/src/peer.rs`).
  `MessageNexusPath` is the store path `${message}/bin/message-nexus`: Flow
  compares `fs::canonicalize(/proc/<pid>/exe)` against
  `fs::canonicalize(MessageNexusPath)`, so the store path is exact and ties
  admission to the pinned closure.
- Removed: `modules/home/deployments/cf7879-cluster-relay.nix`,
  `checks/cluster-relay-package`, its flake registration and
  `docs/cf7879-cluster-relay-activation.md` — it ran Message's retired `relay`.
- `checks/flow-service-path`: `expectedFlowRevision` = `9aa9bf88…`, plus
  assertions that `flow-configuration` is declared, ordered behind the Nexus,
  oneshot, and that its `Configure` datom ends
  `… [ Psyche ] <messageNexusPath> }`.
- `checks/message-service-path` rewritten: argument-less ExecStart, no
  `message-daemon` unit, `messageNexusPath` agreement, the three 0.16
  executables present and the six retired ones absent, `--version` = 0.16.0,
  an argument refused, and the retirement step exercised for the move, for
  idempotence, and for its refusal to overwrite.
- `UPGRADES.md`: one entry covering every break, the activation sequence and
  the rollback.

## Checks

Run on Prometheus with `--max-jobs 0` and
`--override-input system path:<stub exposing system = "x86_64-linux">`, which
standalone CriomOS-home needs (`stubs/no-system` throws by design; the repo
exposes no `homeConfigurations` without a horizon, so a standalone home build
is not available here — it belongs to the CriomOS consumer that pins this
bookmark).

- `checks.x86_64-linux.flow-service-path` → built,
  `/nix/store/wlc1g03l3mzwhssi3kjgx6vj9vliyq4z-flow-service-path`.
- `checks.x86_64-linux.message-service-path` → built,
  `/nix/store/nq9s9bxxq3i47i73zxjhd5i3f0r8mkhs-message-service-path`.
  Message 0.16.0 itself built on the remote builder in the same run
  (`building … on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`).
- Both new checks were seen failing once before being trusted: `[ Psyche ]` →
  `[ Psyche Field ]` fails the flow assertion; adding a signal-path argument to
  ExecStart fails the message assertion.
- Aggregate `nix flake check --max-jobs 0` was started and **did not complete**;
  it was stopped at wind-down. Before that it failed on one check unrelated to
  this work: `active-network-widget`, whose own helper test raised
  `BrokenPipeError: [Errno 32] Broken pipe` in
  `active_network_helper.py:437 client_connected` *after* printing "active-network
  helper contract tests passed" and "active-network status validation tests
  passed" — a pre-existing flake in that check's fixture, touching neither Flow
  nor Message. Every other check reached had built. Whoever resumes should run
  the aggregate to completion and read its result rather than take this
  bookmark's two checks as standing for it.

## Caller survey — ordinary `Send` and `flow-meta`

Surveyed primary (scripts, tools, skills trees), Curriculum authored skills and
the generated `.claude`/`.agents`/`.codex`/`.pi` trees, CriomOS-home, CriomOS,
messenger-clj, field-clj.

**No executable caller of ordinary `flow 'Send.{ … }'` exists anywhere, and no
caller invokes `flow-meta` programmatically.** Every `Send.{ … }` and
`flow-meta '…'` occurrence outside Flow's own repository is a receipt, report
or design document recording a hand-run request. The removal therefore breaks
no running code; the documents are history and are left as written.

The three real callers, all on the ordinary socket, all surviving 0.16:

| Caller | Request | Must change to |
| --- | --- | --- |
| `/git/github.com/LiGoldragon/field-clj/src/field_clj/core.clj:57` (`#observe`) | `flow List.{}`, after `systemctl --user is-active flow-nexus.service` | Nothing. `List` is unchanged and writes nothing. Its test at `test/field_clj/core_test.clj:103,109` stubs the same call. |
| `/home/li/primary/tools/field-flow-preflight.mjs:48,52` | `flow resolve <id>` first, then `flow 'ResolveRecipient.<id>'` | Nothing required, but the word-command attempt is now dead weight: the 0.16 `flow` client accepts exactly one inline datom and no words (`crates/flow/src/main.rs`), so the first call always fails to the fallback. Drop the legacy branch and keep the datom. |
| `/home/li/primary/flows/6db4fe/flow-message-vm/flake.nix:54` | `flow 'ResolveRecipient.vm-missing'` in a NixOS VM test | Nothing, and it pins its own Flow. Repin it if it is to exercise 0.16. |

Consequences for things that are not callers but are affected:

- **messenger-clj / the `hm-*` commands** never touch Flow: they resolve a
  target and write its pane through Herdr directly. They keep working, but
  Flow 0.16 declares itself the only pane writer, so a pane messenger-clj
  writes is a write Flow neither leases nor grades. That conflict is a design
  decision for the psyche, not a mechanical change, and it is the reason to
  move `hm-send` onto `flow-meta 'Deliver.…'` rather than leave two writers.
- **Curriculum skills** name no Flow request; `messaging.md` and
  `compensation-messenger-clj.md` route through `hm-*`, and `nexus.md` speaks
  of `<nexus>` / `<nexus>-meta` generically. `file-editing.md:25` describes
  field-clj's `#observe` reading "flow-nexus user-service state" — still true.
  No skill edit is owed by this change. The generated `.claude`/`.agents`/
  `.codex`/`.pi` trees hold no Flow request either.
- **Flow 0.16 Start continues into the brief itself** (0.14 onward): a caller
  that sends the brief as a second prompt after a launch receipt would now
  send it twice. No such caller was found among the three above; anything that
  launches seats outside Flow (`tools/native-seat-launch.mjs`) does not go
  through Start and is unaffected.
- **Field and Mind seats** that reach `flow-meta` by hand are now refused
  (`MetaAspects` is `[ Psyche ]`). That is the designed gate, not a fault.

## Activation steps and risks, for whoever activates

1. Pin this bookmark's revision `648ae6cf` from the CriomOS consumer and build
   there; standalone CriomOS-home cannot produce the home activation package.
2. Activate. `retireMessengerStore` runs after the write boundary and moves the
   0.14 state aside. **Risk**: it refuses, and fails activation, if
   `retired-0.14/` already holds a file of the same name — recover by naming
   the second copy by hand, never by deleting either.
3. `systemctl --user daemon-reload`, then
   `systemctl --user disable --now message-daemon.service`. **Risk**: a unit
   from the previous generation survives activation; two Nexuses would open
   different stores and both write panes' worth of confusion.
4. `systemctl --user status flow-nexus.service flow-configuration.service message-nexus.service`.
   `flow-configuration.service` must be `active (exited)` having printed
   `Configured.{ … }`. **Risk**: it fails if Flow's meta socket does not appear
   within 30 s, or if Flow answers anything but `Configured` — and until it
   succeeds Flow refuses Message on the meta socket and every delivery fails
   closed. `Configure` replaces the Configuration record whole, so a value
   changed by hand over the meta socket is reset at every activation and boot;
   that is intended and is where to look if a hand-set value disappears.
5. Witness admission before trusting the route: one `flow-meta 'Deliver.{ … }'`
   from the owner's shell, and one Message delivery end to end. Nothing here
   has been witnessed live — this bookmark is evaluation and build evidence
   only, with no deploy and no activation.
6. Rollback: the previous Home generation restores Flow 0.14.0, Message 0.14.0
   and `message-daemon.service`; then move `retired-0.14/messenger.sema` and
   its sidecars back beside it, because 0.14 opens no other store. No
   countdown rollback is armed: neither unit can take network or remote access
   away.
