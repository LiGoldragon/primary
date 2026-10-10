# Spirit Nexus invariant audit — 2026-09-10

Read current `src/bin/spirit-daemon.rs`, `src/daemon.rs`, `src/component_daemon.rs`, and authored operational modules against the supplied Nexus authority.

* **Bootstrap gap:** `spirit-daemon` still requires exactly one configuration-archive argument and has no zero-argument component default. `Configuration::new` seeds paths only in callers; it does not provide a persisted initial Configure/marker state.
* **Meta persistence gap:** current meta `Configure` writes owner runtime state but the audit has not yet found a persisted Configure marker carried by Sema/reopen logic.
* **Ordinary reversal gap:** ordinary `Query` has no initial Configure operation; ordinary/meta separation currently rejects meta bytes at the working socket rather than supporting a defined bootstrap/reversal flow.
* **Actor substrate:** component daemon imports Kameo `Message`/`Context`; exact end-to-end actor boundary needs validation after bootstrap work.
* **Packaging gap:** current package retains client and Nexus in one crate; `datom-cli` gates client textualization but crate split/no-Datom Nexus proof is outstanding.

This is an audit record, not a completion claim. Existing archive migrations remain untouched.

## Lifecycle correction — 2026-09-10

A new reusable `nexus` crate is the agreed home for the standard surface `ConfigurationState<C>` and the qualifier-named `Configurable<C>` capability; it is an unpushed draft while its owner completes gates, so this report does not treat it as published evidence. The authoritative transition is precise: ordinary Configure may replace the current configuration while `meta_configure_occurred` remains false; only a successful meta Configure sets it; only meta reversal clears it. Spirit must persist this state inside its Sema record family rather than treating its current in-memory archive target as lifecycle evidence. Current `Engine::configure` is deliberately infallible, so a rejection/no-mutation witness follows the corrected effect's real validation policy instead of fabricating a rejection for the old archive-target setter.

## Stable store identity evidence

The active user profile defines Spirit state as `$HOME/.local/state/spirit`, with its live Sema at `$HOME/.local/state/spirit/spirit.sema`; direct filesystem inspection found that exact file present on 2026-09-10. The current service bundle also derives `spirit.sema` beneath its injected `stateDirectory`. The new zero-argument startup must retain this established state identity while it removes the generated bootstrap-configuration argument. It must never interpret a Configure database field as a request to start an empty store elsewhere. Mutable configuration is therefore `SpiritNexusConfiguration` without a database path; its desired socket/trace/authorization/guardian settings apply after restart from the established store.
