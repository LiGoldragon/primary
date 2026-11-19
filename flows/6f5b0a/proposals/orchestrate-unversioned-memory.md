# Zeus Orchestrate: explicit migration boundary

Read-only assessment answering iyn4, 2026-11-18. No state file was opened, copied, stamped, deleted or migrated; no service operation or build was performed. The observations of Zeus are inherited from the November 14 triage, not fresh live verification.

## Finding

The deployed source provides no demonstrated record-preserving path from Zeus's unidentified unversioned store into Orchestrate 0.38.0. The immediate refusal originates in the memory kernel, before Orchestrate's family-level cutover can run. The words “migrate explicitly” in the error are a requirement, not evidence of an available migration command.

## Pinned source evidence

- Orchestrate `0f9961460f84b752fa9605ebf0e2b6e1c685aa91`, `Cargo.lock`: memory `69d91c486b335575ee5e4b0eb79da27094e700b6`, version 0.1.1; memory-engine `abf9d85166e22440440baba03358913458905b8d` per inherited triage.
- memory `69d91c4`, `src/lib.rs:480–503,527–550`: `Memory::open_with_schema` creates a write transaction; `ensure_schema_version` returns `LegacyFileLacksSchema` for an existing file without a version. Commit follows successful validation only. `tests/kernel.rs:192–196` checks that refusal.
- Orchestrate `crates/orchestrate-nexus/src/store/mod.rs:102–104`: `OrchestrateStore::open` first calls `Engine::open`; legacy-lock inspection and metadata seeding follow it. Therefore those later operations cannot solve this refusal.
- `store/legacy.rs`, `PreflightsLegacyStore::inspect`: the shipped upgrade preflight also calls `Engine::open` with the current schema. It is a legacy PathLock counter, not an unversioned-store decoder, and is not a suitable raw forensic reader.
- `UPGRADES.md:466–493`: `orchestrate-store-migrate` was deleted in 0.32 because it targeted the wrong generation. Its older documented invocation is explicitly corrected as historical. Remaining configuration cutover carries Locks and allocator unchanged for recognized stores; it is not a migration from arbitrary unstamped bytes.
- `store/mod.rs:118–123` also refuses the superseded situation family. Passing the kernel guard would not prove the remaining store admissible.

## Unknowns that select the design

The creator release, redb/rkyv layout, table catalog, complete record population and any active reservation ownership in Zeus's actual file remain unknown. Missing schema metadata alone identifies none of them. Empty state and compatibility with current archived types must not be assumed.

## Proposed next authorized unit

Core assigns an Orchestrate/memory owner and Field supplies a reviewed, consistent, immutable evidence copy plus deployment provenance. A genuinely read-only inventory establishes the file format and table identities without invoking current engine startup. The owner selects an exact historical decoder only when its schema matches evidence; ambiguity returns a typed refusal with the missing identity evidence.

The migration is then designed for that identified source and an explicit target revision. It reads the preserved source and writes a separate destination; its report accounts for every table and record, configuration and privilege state, reservation fields and ownership, allocator monotonicity, and situation/relocation identity. A missing old Flow attribution remains unresolved rather than invented. Unknown families and malformed records stop conversion. Source bytes remain unchanged.

Acceptance requires independently checked record conservation and negative fixtures, source hashes before and after, repeat/crash behavior, and a disposable destination restart with both target clients. Socket claims and file-identity relocation need an explicit isolated validation plan: copying a situation-bearing store is not permission to bind its recorded sockets. Field promotion and recovery are separately reviewed after these proofs. This proposal authorizes neither implementation nor operational migration.

Sources: inherited `/home/li/primary/flows/374411/ethos-followup/triage.md` and its private `raw/zeus-orchestrate.txt`; pinned repositories under `/git/github.com/LiGoldragon/{orchestrate,memory,memory-engine}`. Unrelated paused work remains paused.
