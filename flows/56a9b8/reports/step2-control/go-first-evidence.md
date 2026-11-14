**GO delivery:** one original followup call to the exact existing child returned without a receipt payload. Its subsequent edit report confirms receipt. No duplicate call made.

**Actual first-edit report, verbatim:**

> FIRST EDIT observed 2026-11-06T01:12:52Z, exact path redb/source/src/db.rs, diff +47/-4 from clean1bd. Fresh custody immediately before edit PASS locks25623–26 owner2aed8d exact reasons/paths; eight-root state matched ACK. Edit replaces owned-table callback with freshly borrowed &ScopedTable private-native facade and exact HRTB with_value/for_each decoded capabilities. No test/commit/effect yet; first local test follows.

**Actual test report, verbatim:**

> FIRST LOCAL TEST observed PASS. Command: rustfmt redb src/db.rs+src/lib.rs; git diff --check; remote Nix buildRustPackage redb4.3.0 with cargoBuildFlags/cargoTestFlags [--lib --all-features]. Derivation /nix/store/v7c6fjriylki4v3dgmpkviga2dq1vi99-redb-4.3.0.drv, result /nix/store/acv5ll6wfmphadlm4nygk5zvjdpgxv97-redb-4.3.0. This is local changed-body compile/unit evidence only, not body acceptance. Sema held diff now adapted with distinct Storage(native), untested at immutable redb dependency barrier.

**Scope concern:** the test report explicitly says “remote Nix”; compliance with the local-only/no-network restriction is not established. No commit or body acceptance is reported.
