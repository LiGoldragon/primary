# Orchestrate on its Ethos, ethos-zero 27

Everything is on branches named `ethos27-2e404d`, each one a fast-forward of its main and pushed. Nothing is merged, deployed or switched, and the running orchestrate service was not touched. Evidence is in `/home/li/primary/flows/2e404d/orchestrate/`.

## Repositories and gates

Every gate ran `nix-fast-build --remote prometheus` on `checks.x86_64-linux`, against the committed revision named in the table.

| repository | head | on main | gate | log |
|---|---|---|---|---|
| signal-orchestrate | 8335cf9 (6.0.0) | df564c6 | exit 0, 13 checks | `gates/signal-orchestrate-8335cf9….log` |
| meta-signal-orchestrate | 055950b (6.0.0) | 5e4986d | exit 0, 13 checks | `gates/meta-signal-orchestrate-055950b….log` |
| nexus | 64a735d | c495f2a | exit 0, 3 checks | `gates/nexus-64a735d….log` |
| orchestrate | e78534f (0.39.0) | 0f99614 | exit 0: 18 checks, 181 tests passed, 0 failed | `gates/orchestrate-e78534f….log` |
| orchestrate-test | 6a6c812 | b8e2b97 | exit 0, 9 checks | `gates/orchestrate-test-6a6c812….log`, scenario transcripts in `orchestrate-test-scenarios-6a6c812….txt` |

- **nexus is touched; build-base is not.** ethos-zero derives `Hash` on every type it generates. The generated Memory records hold `nexus::ConfigurationState`, `Situation` and `Relocation`, which did not derive `Hash`, so 64a735d adds the derive to those types and to `StoreIdentity`. No crate edge forced a change to build-base.
- **No Cargo.nix.** None of these repositories uses crate2nix: they build with crane, so no Cargo.nix needed regenerating. Cargo.lock was updated in each repository.
- **Freshness negative test:** a commit with a deliberately stale `src/memory.rs` fails the build with "src/memory.rs is stale; regenerate it from memory.ethos" (`gates/negative-stale-memory-93d11d5….log`). That commit is local only and was not pushed.

## What is generated and used now

- **signal-orchestrate and meta-signal-orchestrate** are Signal roots under ethos-zero 27. Each generates `Input`, `Output`, `Answering` and `impl Answerable for Input`.
- **orchestrate-nexus** answers every input through that generated dispatch, `input.answer(&answerer)`, in `crates/orchestrate-nexus/src/core.rs`. Its own match is gone.
- **`crates/orchestrate-nexus/memory.ethos`** is a Memory root. It generates `src/memory.rs`:
  - StoredMetadata, StoredSituation, StoredRelocation, StoredLock, StoredAllocator and StoredConfiguration;
  - the pre-0.25 PathLock records.
- **The keys, family descriptors and the open stay hand-written** in `store/record.rs` and `store/legacy.rs`.
- **`build.rs`** fails the build on a stale `memory.rs`.
- **StoredLock holds the contract's `HeldLock` whole.** The metadata tree holds `ConfigurationState<OrchestrateNexusConfiguration>`.

## Removed

- **From `store/record.rs`:**
  - the hand structs StoredLock (the Lock shape repeated with bare scalars), StoredConfiguration, StoredMetadata, StoredSituation, StoredRelocation and StoredAllocator;
  - the `Storing` trait, with its from_public and into_public conversions.
- **From `store/legacy.rs`:** the six hand records LegacyName, LegacyPath, LegacyPaths, LegacyReason, LegacyLock and LegacyStoredLock.
- No hand rkyv derive remains outside generated files.
- **From `configuration.rs`:** ConfigurationOutcome, Configured and AnswersMeta, which duplicated the meta Output and its dispatch.
- **From `ordinary.rs`:** IdentifiesLock, which was unused.
- **From both clients:** the hand `enum TransportError`, which sat beside the generated `TransportError`. Every client failure is now the generated `ClientFailure`, with the same text as before.
- **Kept:** the Nexus's internal `transport::TransportError`. It is unrelated to any Ethos type.

## Store proof

1. **Bytes.** Every generated record archives to the bytes the 0.38.0 hand record of its family wrote. `tests/memory_representation.rs` checks five records: the Lock, the allocator, the metadata tree (open and closed), the carried configuration and the PathLock.
2. **No upgrade is needed.** Table names and schema labels are unchanged, so no upgrade path was written.
3. **The real store copy.** I took the live store `~/.local/state/orchestrate-nexus/orchestrate-nexus.memory` read-only, at sha256 2cb3abcb…, with 12 Locks. Each run used a fresh copy in a bwrap mount namespace, with the copy at the live store's path and a fresh directory over the live socket directory. All runs are in `orchestrate/store-proof/`.
   - **A and B, the same 11 inputs.** Observe, Lock, duplicate name, path overlap, Release, unknown Release, ordinary and meta Configure, and malformed text, run through:
     - the live 0.38.0 (`/nix/store/zlyxh0bq…`) Nexus and clients (A);
     - the 0.39.0 Nexus and clients (B).
     The two transcripts are byte-identical.
   - **C, rollback:** 0.38.0 opens the store 0.39.0 served.
   - **D, forward:** 0.39.0 opens the store 0.38.0 served.
   - **The same Observe throughout.** Observe after C and D equals the copy's first Observe (md5 c197a67e…).
   - **E and F, crossed versions.** An ordinary client of one release is refused by the other release's Nexus at the greeting (`GreetingRefused.ContractMismatch`). The meta client of either release is answered by either Nexus.
4. **orchestrate-test.** It now pins 0.39.0 against previous 0.38.0 and live 0.38.0. The rollback, previous-store, live-store, populated-store and old-meta-name scenarios all pass.
   - The component named the store `orchestrate-nexus.sema`, a name stale since the Memory rename. It is now `.memory`.

## Wire

- **Unchanged:**
  - the Datom text both CLIs accept and print;
  - every scenario reply;
  - the meta contract: its digest, its layout, and its interworking across releases.
- **The ordinary digest changes:** 8912638139974146909 becomes 4020875787160854601.
  - The 27 Signal root pairs outputs with inputs by position, so `ConfigurationRefused` moves to after `Observed`. That changes the archived tag of Locked, Released, Observed and ConfigurationRefused.
  - The Nexus and the `orchestrate` client therefore move together.
  - mind and orchestrator-judge also depend on signal-orchestrate, at their own pins.
- **ethos-zero 19.2 is still in the graph.** It enters through `signal` 7afb68b's build-dependency, because signal itself was not moved.

## Questions for Fable

1. ethos-zero 27 refuses an input `Lock.LockRequest` next to a declared type `Lock` (`Payload.Lock`). The vision's own Signal example has exactly that, so to keep the CLI text `Lock.{ … }` I renamed the type to `HeldLock`. Is HeldLock the name, or does the generator change? (`signal-orchestrate/ethos/signal.ethos`, `psyche-belief/vision/signal/0.md`)
2. Positional pairing forced the ordinary outputs to be reordered, which changes their archived tags and the digest. Is that the intended cost of pairing, or should refusals be declared apart? (`signal-orchestrate/ethos/signal.ethos`)
3. `Answering` can refuse only with `Output`, so a store that fails to commit cannot be answered through it. The Answerer holds the failure and returns a never-sent `Unsent` output in its place. Should a capability carry a Nexus error type? (`orchestrate/crates/orchestrate-nexus/src/core.rs`)
4. The Memory root declares records only, so their keys, family names, schema labels and `EngineRecord` impls are hand-written. Which section of the Memory root is to hold them? (`orchestrate/crates/orchestrate-nexus/src/store/record.rs`)
5. Every generated type derives `Hash`, which made nexus add `Hash` to its stored kinds, and those kinds are hand-written Rust rather than Ethos. Should nexus's stored kinds get an Ethos Library, or should the derive set differ per root? (`nexus/src/situation.rs`)
6. Configure's output is `ConfigurationAccepted`, which does not follow the ruling "each input its own output, named its past tense". I left it, because renaming it changes printed text. Is it to be renamed `Configured`? (`signal-orchestrate/ethos/signal.ethos`)
7. A generic import becomes the field name `orchestrate_nexus_configuration_configuration_state`. Is there a form that names a position, or is that the name? (`orchestrate/crates/orchestrate-nexus/memory.ethos`)
