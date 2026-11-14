# Actual record integration: unexercised, not incompatible

Completed checker report supplies no evidence that actual record imports were unavailable. It selected reproduced rkyv record shapes and qualified that choice. No actual-record import attempt, visibility error, dependency failure, or compiler incompatibility is recorded. The reason for omitting actual imports beyond that fixture scope is unknown; do not turn an unrun test into a diagnosed blocker.

Held context identifies public sema::DatabaseHeader and Engine's crate-root TableRegistration/VersioningPolicy names (external candidate paths sema_engine::TableRegistration and sema_engine::VersioningPolicy). Their exact external export availability was not checked by the completed fixture. The actual held Sema Cargo.toml uses redb="4" while its source imports new inspection capabilities; real crate integration is separately held at unpublished dependency materialization. That known barrier does not prove these record imports fail, nor did the fixture exercise it.

Smallest proposed follow-on, only after separate approval: retain this exact isolated fixture and import actual types from supported immutable read-only pinned Sema/Engine crate materialization; add owned DatabaseHeader decode, finite catalog Vec<(String,TableRegistration)> and VersioningPolicy decode positives in normal/experimental-api-5. Verify exact type exports/dependencies first; record precise materialization GAP if unavailable. No implementation-root dependency override, copied stand-in substitution, source patch, new launch or continuation authorized here.

Completed artifacts/fixture lock25643 retained. No extension/new work performed for this explanation; only completed report and held context used.
