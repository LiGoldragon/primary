# Mentci producer-chain repair item

Status: tracked; implementation unassigned pending producer-chain collision and compatibility review.

## Immutable failure chain

- Home pins Mentci `0.5.0` at `235b1b44ecd93857df60c36a2ca4fa16fab5984f`.
- That source pins Meta Signal Criome `1c3bd8784142c54856e031d74b897382204cec21` and Schema Rust `37b7d1035a472a15081f3e2e8a93b95bf733c3ee`.
- Meta Signal Criome's exact `build.rs` imports `schema_rust::bootstrap::BootstrapInterfaceGeneration`; Schema Rust had removed that symbol in `dbfc39c2a46a3c2ce9da254aa4479536390ab805`. The current API includes `BootstrapGeneration`.
- The retained Home terminal account identifies `mentci-deps-0.5.0.drv` exit 101 on this import; `agent-daemon-configuration.drv` exit 65 is separately owned by the Home fixture repair, and its service/mentci failures are consequences.

## Scope and history

The retained terminal-migration report identifies legacy build-script work in Meta Signal Criome, Signal Mentci, and Meta Signal Mentci. Signal Criome is the fourth contract in the shared producer chain. The report's historical repair references are Meta Signal Criome `5acfedafd63964da1a4d1082245f3943c6d371b5`, Signal Mentci `293ea752`, Meta Signal Mentci `b063a33d`, and Mentci migration branch `f6db8d-datom-migration` at `4edaf70d`.

No present producer owner or active lock is witnessed. The historical report states its originating flow held no lock after its work. A Mentci-only repair is unsafe: Mentci, Criome, and Mentci-lib share Meta Signal Criome's `links` constraint.

## Exception-matrix limit

The source mismatch predates the September 26 Messenger and Flow pins, but retained evidence does not show the same full Home check running on the pre-pin base and candidate with the same derivations/errors. It also does not establish whether implicated packages or units changed at activation. Therefore it supports chronology only, not Form 1 failure-identity equivalence.

## Repair brief

Assign one owner for an immutable producer-chain audit across Signal Criome, Meta Signal Criome, Signal Mentci, and Meta Signal Mentci. Establish each build script's intended Schema Rust API, then explicitly choose either a compatible legacy Schema Rust pin or a coordinated current-API port. Review generated-wire and consumer consequences before changing pins; do not repin Mentci alone.

## Sources

- `flows/f6db8d/reports/terminal-migration.md`, sections 11-13.
- `flows/8904b1/log.md`, entries 1487-1545 and 1507-1540, retained in `/home/li/wt/primary/56ae53`.
- Immutable source reads of the Mentci, Meta Signal Criome, and Schema Rust revisions listed above.
