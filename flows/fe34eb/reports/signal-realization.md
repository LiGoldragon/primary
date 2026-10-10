# Signal repository realization

Delegated by the main flow of fe34eb on 2026-09-12, on the living's
"implement what is ruled", against the 2026-09-10 ruling in
`flows/fe34eb/vision/signal.md`: merge the shared signal code into one
repository named `signal`, starting with the recently written code, with
no unused code in it; archive the old `signal` repository and rename
`signal-standard` to it; the old git history is not needed.

## What was done, per repository

### `signal-legacy` (was `signal`) — archived

The uncommitted Nota-to-Dotos rename found in the checkout was committed
first, as its own change (`e64aef5986d2`), so nothing was lost. The
repository was then renamed on GitHub to `signal-legacy` and marked
archived. The local checkout moved to
`/git/github.com/LiGoldragon/signal-legacy` and its remote was repointed.
Nothing was deleted. Its one dependent, `signal-forge`, was not touched;
GitHub's rename redirect keeps its pin resolving.

### `signal-derive-legacy` (was `signal-derive`) — archived

Same treatment. The uncommitted Nota-to-Dotos rename of its architecture
document was committed as `94672754ad3a`, then the repository was renamed
and archived. Its only dependent was the legacy `signal`.

### `signal` (was `signal-standard`) — 1.0.0 to 2.0.0, `626e407be520`

Renamed on GitHub and locally. The crate, the library, and the Cargo
`links` key are all `signal` now.

Removed, as orphaned: `src/bootstrap_manifest.rs` (122 lines) and
`src/schema/` (432 lines across four files). Nothing imported them and
nothing compiled them — `build.rs` only ever checked
`ethos/signal.ethos` against `src/generated/signal.rs`. Also removed
eleven Nix `result-N` symlinks that had been committed into the
repository; they pointed into the store and were not source. The
`ethos/` directory and the generated taxonomy were kept, as ruled.

Added `src/portable.rs`: the `Signal<T>` frame and the three kinds
`Signalizable`, `ByteViewable`, `Restorable<T>`, moved from the contract
crates and made generic. `Signalizable` and `Restorable<T>` are blanket
implementations over the rkyv bounds, so a contract crate now inherits
all three without writing a line.

Added `src/frame.rs` and `src/transport.rs`: one implementation of the
length-prefix framing — `FrameCapacity`, `FrameBody`, `FramePrefix`, and
the traits `Capacious`, `LengthDeclaring`, `Framable`, `FrameReading`,
`FrameWriting`, and, behind the new `transport` feature,
`AsyncFrameReading` and `AsyncFrameWriting`.

Added `DESIGN.md`: the four sections of the legacy repository's
`ARCHITECTURE.md` worth carrying, reproduced verbatim and attributed to
`signal-legacy` at `e64aef5986d2` — one record one form; the reply
protocol (position pairing, no correlation ids); the origin route as
implicit return address; authorization at the wire. Marked there as
inherited reasoning, not specification, because the protocol on top of
portable rkyv is still to be decided.

Rewrote `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, and
`NON_IDEAL_AGENTS.md`, which described the removed files as if live.
Added `UPGRADES.md`. The flake's `contract-crate-carries-no-runtime`
check became `carries-no-engine` (kameo, redb, sema, ractor) plus a
`default-features-carry-no-runtime` build, since tokio is now an optional
framing dependency; `test-transport` and `clippy-transport` checks were
added.

### The six contract crates

Each carried a byte-identical 72-line `src/lib.rs`. Confirmed identical
by md5 before the move. **Ethos Zero does not emit that file** — its
generator contains no reference to `Signalizable`, `ByteViewable`,
`Restorable`, or a `PhantomData`-carrying `Signal` type; the only
`PhantomData` in `ethos-zero/src/lib.rs` belongs to its own `Potential<T>`.
The file was hand-written and hand-copied, so it was moved, not
regenerated.

Each crate's `src/lib.rs` is now four lines — the generated module, its
re-export, and the `ETHOS` constant — and each depends on `signal`.
Each got an `UPGRADES.md` entry.

| repository | before | after | revision |
| --- | --- | --- | --- |
| `signal-lojix` | 1.2.0 | 2.0.0 | `662cedb7d92b` |
| `meta-signal-lojix` | 2.3.0 | 3.0.1 | `f7f11d410d68` |
| `signal-spirit` | 1.2.0 | 2.0.0 | `e4ab10624a0a` |
| `meta-signal-spirit` | 1.0.1 | 2.0.1 | `a4b8cddedd05` |
| `signal-orchestrate` | 1.0.4 | 2.0.0 | `7408fb6f5f2b` |
| `meta-signal-orchestrate` | 1.1.0 | 2.0.2 | `d8e035014a26` |

Four of the six held uncommitted peer work — a contract regeneration
against current Datom, Protos, and Ethos Zero, complete and passing its
own tests. It was committed first, as its own change, before anything of
this flow's was written. `signal-orchestrate` and `meta-signal-orchestrate`
also carried a local `flow857335-orchestrate-lifecycle-wip` bookmark; it
was restored to its origin position afterwards, and only `main` was
pushed.

Three of the meta crates pinned their ordinary contract by absolute
local path (`path = "/git/github.com/LiGoldragon/..."`), which no other
checkout and no Nix build can resolve — `meta-signal-orchestrate`'s Nix
check failed on exactly that. All three were repointed to pushed
revisions, which is the patch bump in the table above.

### `lojix` — 1.0.1 to 2.0.0, `fab60e584daf`

Takes the framing from `signal` on both daemon sockets (`src/daemon.rs`)
and the client exchange (`src/client.rs`), and the Signal kinds from
`signal` rather than from the two contract crates. `lojix::Error::SignalFrame`
now wraps `signal::FrameError`. `triad-runtime` remains the actor
listener runtime and keeps its streaming path untouched; only its frame
codec is no longer used here. All five workspace crates bumped together.

### `orchestrate` — not touched. See "What was left".

## The byte order — a decision this flow made

The brief's witnessed state said both nexuses hand-roll *a 4-byte
little-endian prefix*. That is not what the code says.
`orchestrate/crates/orchestrate-nexus/src/transport.rs` used
`u32::from_le_bytes` / `to_le_bytes`; `triad-runtime/src/frame.rs`, which
Lojix uses, used `from_be_bytes` / `to_be_bytes`. The two nexuses were
silently incompatible.

One implementation therefore required picking one. `signal` is
big-endian, following `triad-runtime`, the legacy `signal` architecture
document ("4-byte big-endian length prefix"), and network byte order.
This is the flow's own decision, not a ruling, and it is recorded in
`signal/ARCHITECTURE.md`, `signal/AGENTS.md`, and `signal/UPGRADES.md`
so the next flow inherits it rather than rediscovering it. Lojix's wire
is unchanged by it; Orchestrate's would flip, which is part of why
Orchestrate was left (below).

## What was verified, and how

Every repository was tested locally with `cargo test` and gated with
`cargo clippy -- -D warnings`, then built and tested again through its
Nix flake check on the remote builder `prometheus.goldragon.criome` with
`nix flake check --max-jobs 0`, so nothing was built locally. Outputs are
in `flows/fe34eb/witnesses/<repository>-flake-check.txt`; the per-run
verdicts are in `flows/fe34eb/witnesses/flake-checks.md`.

The framing has seven new behavioral tests in `signal/tests/framing.rs`
and two in `signal/tests/async_framing.rs`. The prefix test compares
against a hand-written expected byte vector (`00 00 00 03 AA BB CC`),
not against anything the code computes. All nine were seen failing once:
flipping `to_be_bytes` to `to_le_bytes` in `src/frame.rs` failed three of
them, including the round-trip and the signalize-frame-restore end to
end; the change was reverted and they passed again.

The real witness for Lojix is `lojix-nexus`'s `daemon_configuration` test,
which starts the Nexus and exchanges typed signals over both real Unix
sockets, with client and daemon both on `signal`'s frame. The whole
workspace passes: 96 library tests plus every integration test.

The GitHub rename redirect was witnessed directly, not assumed:
`git ls-remote https://github.com/LiGoldragon/signal-standard` resolves
and returns the new `signal` HEAD, and `cargo fetch` in `signal-agent` —
one of the fourteen legacy-wired dependents, pinned at
`f12d0cb9e480` — succeeds through the old URL. None of the fourteen
needed a change, so none was made.

## What was left

**`orchestrate` is not migrated.** Its checkout holds substantial
uncommitted peer work (ten files, +164/-79) from flow 857335: the
first-configuration feature in `store.rs`, a trait-renaming pass in
`transport.rs`, and two absolute-path dependency pins. That work does not
compile — `meta_signal_orchestrate::Configure` no longer exists, and
`signal_orchestrate::Query::Configure` is a new unhandled variant — so it
could not be committed as found, and it was left exactly as found instead
of being overwritten.

Probing from a clean worktree at `main` confirmed the blocker is not
mechanical: repinning to the 2.0.0 contracts leaves eight compile errors
in `orchestrate-nexus`, of which the import fixes are trivial but
`Query::Configure` and the `MetaConfigureDone` marker are the ordinary-socket
first-configuration feature of the Nexus vision — new Nexus implementation,
not signal-repository realization, and the same work the uncommitted
changes are half-way through. Flow 857335 also declared Orchestrate
implementation held until its two skeptical audits are reconciled; those
audits were interrupted and never delivered reports.

A framing-only change to Orchestrate was considered and rejected: it
would flip a live Nexus's wire byte order on its own, and the very next
commit — the contract repin — would rewrite it. Both belong in one
breaking Orchestrate release. The remaining work is exactly:

1. Finish or discard the uncommitted first-configuration work in
   `crates/orchestrate-nexus/src/store.rs`.
2. Repin to `signal-orchestrate` `7408fb6f5f2b` and
   `meta-signal-orchestrate` `d8e035014a26`, and import the Signal kinds
   from `signal` `626e407be520`.
3. Replace `SignalPayload` in `crates/orchestrate-nexus/src/transport.rs`
   with `signal`'s `AsyncFrameReading` / `AsyncFrameWriting`, accepting
   the little-endian to big-endian flip, and rebuild the Nexus and both
   CLIs together.
4. Regenerate the stale `src/generated/client.rs` in `orchestrate` and
   `orchestrate-meta`; their build scripts already refuse them as stale
   against the current Ethos Zero.

**Two further findings, neither acted on.**

`lojix/tests/actor_native_runtime.rs` is a change-detector: it asserts
that `src/daemon.rs` contains and does not contain particular source
strings. The testing discipline forbids such a test. Two of its markers
were updated so it would pass; it was not rewritten, because a real test
of the same property would have to exercise listener concurrency. It
should be replaced or deleted.

Six more contract crates appear to carry the same copied Signal code —
`signal-introspect`, `signal-message`, `signal-persona`,
`signal-spirit-judge`, `meta-signal-terminal`, `meta-signal-upgrade`.
Only their test files were grepped, not their sources, so this is a lead,
not a finding. None is on the realized stack.

One thing was lost: an untracked `examples/` directory in the
`signal-standard` checkout was deleted while clearing orphaned files. It
had never been committed in the repository's history and nothing
referenced it beyond a filter in `flake.nix`, so nothing recoverable was
in git. It is reported rather than hidden.

## Sources

- Ruling: `flows/fe34eb/vision/signal.md`, 2026-09-10 entries; `Vision/signal.md`; `Vision/nexus.md` (Routing).
- Witnessed state carried in the brief: `flows/fe34eb/log.md`, 2026-09-11 and 2026-09-12.
- Peer work and its gate: `flows/857335/log.md` and `flows/857335/reports/shutdown-signals.md`, both read in `primary` at `d95f40754`.
- Everything under "What was done" and "What was verified" was witnessed directly in this flow by reading the checkouts, running the commands named, and reading their output.
- The byte-order finding was read in `orchestrate/crates/orchestrate-nexus/src/transport.rs` and `triad-runtime/src/frame.rs`; it contradicts the brief's witnessed state, and the contradiction is this flow's own.
