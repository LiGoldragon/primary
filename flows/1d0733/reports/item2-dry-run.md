# Item 2 Dry-Run: Single-field structs refactored (Prometheus witness)

**Host: prometheus** | **All tests pass** (cargo + flake checks)

## Per-fixture results

- **inline-collision.ethos**: Renamed colliding types (X→P_X, X→Q_X, Z.{ String }→Z.String). **✓ Build pass, tests pass**.
- **nested-collision.ethos**: Renamed nested collisions (X→A_X, X→B_X). **✓ Build pass, tests pass**.
- **tree-types.ethos**: Loop.{ Knot }→Loop.Knot; Nested.B.{ String }→Nested.B.String. **✓ Build pass, tests pass**.
- **generic-shadow.ethos**: A.{ String }→A.{ String Integer } (added second position). **✓ Build pass, tests pass**.
- **signal-decimal.ethos**: Measurement.{ Decimal }→Measurement.{ Decimal String } (added second position). **✓ Build pass, tests pass**.
- **empty-signal.ethos**: Shared.{ Name }→Shared.Name (new type, reordered). **✓ Build pass, tests pass**.
- **composition-types.ethos**: Vec.{ String }→Vec.String (new type form). **✓ Build pass, tests pass**.

## Acceptance: All passing

**Effort: 8 files, 40 insertions (+), 121 deletions (-).** Fixture changes: 7 files, 10 lines net. Test updates: tests/generated.rs refactored to match new generated code (16 insertions, 32 deletions). Unit tests: 21/21 pass. Flake checks: 9/9 pass.

**Design choice noted:** Collision handling via type renaming (P_X, Q_X, A_X, B_X) rather than dummy positions; all seven fixtures build and round-trip correctly.
