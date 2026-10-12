# The caller is witnessed

```
 CLI process          Nexus
 ┌──────────────┐     ┌────────────────────┐
 │ reads its    │     │ peer credentials   │
 │ own ancestry │ ──▶ │ = first element?   │
 │ from /proc   │ msg │ re-read chain      │
 │ [cli sh wrap │     │ from /proc, equal? │
 │  harness…]   │     │ else Unidentified  │
 └──────────────┘     └─────────┬──────────┘
                                │ witnessed
                                ▼ Ancestry
                      ┌────────────────────┐
                      │ Flow: find a bound │
                      │ address in chain   │
                      └────────────────────┘
```

Every Nexus CLI carries the ancestry it read; the Nexus trusts only what it re-witnesses at the socket and in /proc, at the moment of receipt. The library is generated, built and passing its fixtures on Prometheus, on a branch; it is not on nexus main and Flow does not import it yet.

## Distillation

### Proposal 1 — the shared library, in ethos

File: nexus repository, `ethos/library.ethos`, new, shown whole.

```
Library                    ; shared by every Nexus
[]                         ; imports: intrinsic only
[  Pid.Integer             ; types
   Started.Integer         ; stat field 22: ticks
                           ; since boot, not time
   Process.{               ; one process identity
      Pid
      Started }
   Ancestry.Vector<Process> ; the CLI first, its
                           ; parents, init last
   Unidentified.[          ; why a chain is not
      PeerMismatch         ; trusted
      Vanished
      Reused
      Malformed ] ]
[  Identifiable.[          ; traits: re-observe a
      identify.[           ; process and its chain
         Result<Ancestry Unidentified> ] ] ]
[  Process.[ Identifiable ] ] ; associations
```

Ruling 1: (a) land it on nexus main and have Flow import it, dropping its own Process; (b) change it first: name what.

Ruling 2: a process identity is a pid and its start ticks, which do not tell one boot from another; a stored binding lapses with the boot it was observed in. (a) boot identity stays outside Process, as now; (b) Process gains a Boot field; (c) yours.

### Proposal 2 — what a Nexus promises about its caller

File: psyche-skills `skills/vision-nexus.md`, «Default clients», after the shared-library line proposed in the fourth edition.

Added: A Nexus witnesses its caller at the moment it receives: the CLI carries the ancestry it read, the first element must be the socket's peer, and the Nexus re-reads the whole chain and refuses any difference. Shells and wrappers stay in the chain. A Nexus promises nothing about a process's later life, and a stored binding to a process lapses with the boot it was observed in.

Ruling 3: (a) land; (b) reword: say how.

### What passes

| fixture | result |
|---|---|
| real socket CLI through a wrapper, wrapper and parent edges kept | passes |
| parent named as peer; unrelated live process inserted as ancestor | refused |
| vanished process; reused pid or ancestor; reparent or reuse between the two observations | refused |
| missing init, cycles, empty claim | refused |
| stat names with spaces, parentheses, newlines, non-UTF-8 | parsed |
| generated association compiles; Ancestry rkyv roundtrip | passes |
| package build, tests, datom tests on Prometheus | pass |
