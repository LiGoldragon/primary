# orchestrate -- architecture

Orchestrate is a Lock Nexus: one durable state owner, two sockets,
two CLIs.

## Shape

`orchestrate-nexus` is the long-running Nexus. It opens two
Unix-domain sockets:

- Ordinary (`orchestrate.sock`) -- Lock, Release, Observe.
- Meta (`meta-orchestrate.sock`) -- Configure.

`orchestrate` and `meta-orchestrate` are datom-converting edge CLIs.
Each takes exactly one inline datom value and no flags. With no
argument, each prints its signal ethos and client failure vocabulary.

The wire is binary rkyv: `Frame.{ Version Body }`. Version is the
signal contract's semver. The Signal's version is the wire version.

## Repositories

| Repository | Role |
|---|---|
| `orchestrate` | Nexus, store, transport, CLIs. |
| `signal-orchestrate` | Ordinary wire contract (ethos + generated Rust). |
| `meta-signal-orchestrate` | Meta wire contract. |

## Code shape

Every method lives under a trait. The ordinary ontology is three
traits on `OrchestrateStore`: `Locks`, `Releases`, `Observes`.
`fn main()` is the only free function.

## State

The Sema store persists:

- The `Configure` value (two socket paths).
- Every active `Lock` (five positional fields: LockId, LockName,
  FlowId, Vector\<LockPath\>, LockReason).
- The next LockId (monotonic, never reused).

Lock paths are absolute. FlowId is attribution, not authorization.
Release is cooperative; there is no force release.

## Datom conventions

Spaced delimiters: `{ a b }`, `[ { ... } ]`. Empty enclosures tight:
`[]`. Strings with spaces or delimiters in curly quotes
\u{201C} \u{201D}; bare words without.

## Faults

Client faults (`Unreadable`, `Unreachable`, `Refused`) are datom on
stderr with exit 1.

## Contract changes

Edit the ethos in the signal crate, regenerate through ethos-zero, run
the freshness test (`tests/regeneration.rs`), pin the new rev in
orchestrate.

## Deployment

Bump the `orchestrate` flake input in CriomOS-home, rebuild, restart
`orchestrate-nexus`.
