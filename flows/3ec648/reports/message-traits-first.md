# Message traits first

Subflow of 3ec648, 2026-10-02. Repository `message`
(/git/github.com/LiGoldragon/message), main 481b579f (0.17.0) to main
7ffd4a27 (0.17.1), five commits, pushed. Work done in a scratch jj workspace
(forgotten afterwards); the default working copy was left empty on main.
Nothing deployed; no running message-nexus or message-daemon touched (every
cargo run had `/run/user/1001` masked by a bwrap tmpfs).

## The survey described the 0.14.0 daemon, not main

The brief's findings — configuration file as argv, meta Configure
unimplemented, `relay.rs` with 33 free functions — are true of the running
`message-daemon` 0.14.0 (`message-daemon ~/.local/state/message/message-daemon.signal`,
from CriomOS-home `modules/home/profiles/min/message.nix`). On main they had
already been settled by 0.15.0 (f0cf9b50, which deleted `relay.rs`):
`message-nexus` refuses arguments, seeds a new store from defaults derived
from `HOME`/`XDG_RUNTIME_DIR`, resumes a populated one, and implements
`Configure` (stored; `NexusRestartRequired` when its own sockets move). On
main there were 0 production free functions besides `fn main()`, 12 inherent
impl blocks, and no zero-sized namespaces.

## What changed

- `d9fa1f44` tests: new `tests/configuration_lives_in_the_store.rs`, four
  process-level tests: an argv configuration file stops the Nexus before any
  store or socket; a Configured Flow edge survives a restart; a restarted
  Nexus binds where Configure moved its sockets; `MESSAGE_SOCKET`,
  `MESSAGE_META_SOCKET`, `FLOW_SOCKET`, `FLOW_META_SOCKET` do not reach it.
- `7415dc26` new crate `message-defaults` (flow-defaults' shape: anchors,
  `ReadsAnchors`, `LaysOutDefaults`), used by the Nexus and both clients. The
  clients' fallback was a hard-coded `/run/user/1001`; it is now
  `/run/user/<uid>`. The Nexus's `HOME` fallback is the password database
  (was `/`).
- `bf8ef872` the 12 inherent blocks became traits: `OpensNexus`,
  `StampsLedger` on `SystemTime` (the clock had no owner), `OpensStore` +
  `ReadsRows`, `RequestsFlowDelivery` on `MessageRecord`, `AddressesAttempts`
  on `Addressee`, `NamesAttempt` on `str` (was `Addressee::attempt_of`),
  `ExchangesWithFlowMeta`, `StreamsAgentStates` on `AgentWatch`,
  `ReportsReceipt` on `ReceiptRecord`, `ServesSocket` on `Socket`,
  `FindsNexusSocket` on each client. `ReceiptRecord::key_of` folded into its
  `EngineRecord` impl.
- `0f345c29` `checks/no-free-functions.sh`, `no-inherent-methods.sh`,
  `production-rust.sh` copied from flow (lojix's), scoped to the four crates,
  wired as `checks.no-free-functions` / `checks.no-inherent-methods`.
- `7ffd4a27` 0.17.1 (Cargo.toml, flake.nix), UPGRADES entry, ARCHITECTURE.
  No wire or store change, so a patch bump. The UPGRADES entry says a 0.15+
  unit changes nothing, and spells out what a unit on the 0.14.0 shape must
  change: `ExecStart` to `message-nexus` with no argument, drop the
  `message-write-configuration` ExecStartPre, environment `HOME` +
  `XDG_RUNTIME_DIR` only, other paths via `message-meta 'Configure.{ … }'`,
  `meta-message` renamed `message-meta`.

## Tests

Before: 16 tests, all green. After: 21 (4 integration + 1 defaults unit),
all green; `cargo clippy --workspace --all-targets --all-features -D warnings`
clean.

Seen failing: since main already behaved as wanted, the four new tests
passed on arrival and were seen failing by mutation of the Nexus (store
re-seeded from defaults on every open; `FLOW_SOCKET`/`FLOW_META_SOCKET` read;
one argument accepted): three FAILED, and the argv test hung and was killed
by the 300 s bound (the mutant serves forever; a regression there shows as a
timeout, not an assertion). `no-inherent-methods` was seen failing on main's
tree (12 blocks); `no-free-functions` passed on main and was seen failing on a
copy with one stray `pub(crate) fn`. The defaults unit test was not seen
failing.

`nix flake check --keep-going -L path:<workspace>` on 7ffd4a27, user unit
`message-flake-check-3ec648` (RuntimeMaxSec=7200, MemoryMax=12G): "all
checks passed!", exit 0, x86_64-linux — default (tests), clippy, fmt, the
three existing source-constraint checks and both new law checks.

## Not settled (returned)

- CriomOS-home `message.nix` still runs `message-daemon` 0.14.0 with an argv
  signal file; `daemonBinary` defaults to `message-daemon`. Moving the stable
  slot to `message-nexus` is a deployment, out of scope.
- `delivery.rs`, `service.rs`, `store.rs` and the old test file stay under
  ~400 lines; trait names were chosen per block, not designed as one ontology
  first.
- The edit was not claimed through Orchestrate; an isolated jj workspace was
  used instead.

## Sources

- Brief from main flow 3ec648; skills subflow, vision-nexus, knowledge-nexus, versioning, testing, nix-workflow, file-editing, flow-evidence.
- /home/li/primary/flows/3ec648/reports/flow-traits-first.md; flow `checks/*.sh`, `crates/flow-defaults/src/lib.rs`.
- message history: f0cf9b50 (0.15.0, relay.rs removed), 481b579f.
- CriomOS-home `modules/home/profiles/min/message.nix`, `flow-message-next.nix` (read only).
- `ps` of the running message-daemon 0.14.0 and message-nexus 0.17.0.
- message commits d9fa1f44, 7415dc26, bf8ef872, 0f345c29, 7ffd4a27; unit message-flake-check-3ec648 log.
