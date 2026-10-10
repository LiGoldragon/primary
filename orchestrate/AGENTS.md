# Orchestration Protocol

The coordination protocol for flows sharing the same workspace. The
live implementation is the `orchestrate` CLI: it takes one inline datom
value and no flags, submits a typed `signal-orchestrate` frame to
`orchestrate-nexus` over a Unix socket, and prints one datom reply.

## Current shape

Orchestrate is a Lock Nexus. It owns durable Locks in a Sema store
and serves two sockets:

- **Ordinary** (`orchestrate.sock`) -- Lock, Release, Observe.
- **Meta** (`meta-orchestrate.sock`) -- Configure (privileged).

The CLIs are datom-converting edges. Each takes exactly one inline
datom value and no flags. Flag-style arguments are rejected.

## Datom conventions

A string containing a space or a delimiter character is written in
curly quotes \u{201C} \u{201D}. A word without them is bare. Canonical
output uses spaced delimiters: `{ a b }`, `[ { ... } ]`. Empty
enclosures are tight: `[]`.

## Ordinary operations

```
orchestrate 'Lock.{ MyLock 6329f1 [ /absolute/path ] "why I hold it" }'
orchestrate 'Observe.Locks'
orchestrate 'Release.442'
```

`Locked` returns the complete Lock with its integer ID, name, flow,
paths, and reason. `Released` returns the complete Lock.
`LockRejected.DuplicateName` and `LockRejected.PathOverlap` are typed
refusals. `ReleaseRejected.UnknownLockId` is the release refusal.
`Observed.Locks.[]` is the empty snapshot; `Observed.Locks.[ { ... } ]`
carries locks ordered by name then ID.

## Meta operations

```
meta-orchestrate 'Configure.{ /o.sock /m.sock }'
```

## Faults

A client fault prints one datom value on stderr and exits 1:

- `Unreadable.{ ... }` -- the argument failed actualization.
- `Unreachable.{ ... }` -- the socket is unreachable.
- `Refused.{ ... }` -- wire-level refusal.

## No-argument self-description

With no argument, each CLI prints its signal contract ethos source and
its client failure vocabulary, then exits 0.

## Repositories

| Repository | Role |
|---|---|
| `orchestrate` | The Nexus, store, transport, and CLIs. |
| `signal-orchestrate` | Ordinary wire contract. |
| `meta-signal-orchestrate` | Meta wire contract. |

Contract changes flow: edit the ethos, regenerate through ethos-zero,
run the freshness test, pin the new signal crate rev.

## Deployment

Bump the `orchestrate` flake input in CriomOS-home, rebuild, restart
with `systemctl --user restart orchestrate-nexus`.
