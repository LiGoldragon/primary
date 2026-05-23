# 166 — Sema-upgrade and schema-macro current state

*Kind: Current-state answer · Topic: sema-upgrade + sema schema macro · Date: 2026-05-24 · Lane: operator*

## Short answer

`sema-upgrade` is real as a library/prototype and sandbox host, but not yet a long-lived production daemon. The version-handover foundation around it is much stronger than the daemon story: `version-projection`, `signal-version-handover`, `owner-signal-version-handover`, `sema-engine` `CommitSequence`, Spirit migration modules, Spirit private upgrade sockets, and Persona owner handover authority all exist in code.

The schema macro destination is designed but not implemented. The old `signal-derive #[derive(Schema)]` macro exists, but it is legacy/under-review and is not the new content-addressed sema schema mechanism. The intended destination is now `signal-frame-macros` / `signal_channel!` as the converged schema source: it will emit NOTA codec, recursive Help docs, Tier 1 64-bit headers, golden-ratio section constants, and next-version `VersionProjection` using the next schema crate as a Cargo dependency.

## Sema-upgrade code state

Landed foundation:

- `version-projection` is the library home for `VersionProjection`, `ContractVersion`, migration index, and compatibility policy vocabulary.
- `signal-version-handover` carries the private daemon-to-daemon handover protocol: marker, readiness, completion, Mirror, Divergence, and recovery.
- `owner-signal-version-handover` exists and carries owner authority: `AttemptHandover`, `ForceFlip`, `Rollback`, and `Quarantine`.
- `sema-engine` has durable `CommitSequence` and replay APIs; every committed write advances the per-database high-water mark used by handover.
- `sema-upgrade` has the Spirit 0.1.0 to 0.1.1 migration module, the `handover.rs` protocol witness, temporary CLI/staging apps, and Nix sandbox witnesses.
- `persona-spirit` and `persona` have advanced enough that real private upgrade socket and Persona-driven owner handover paths exist in current source.

Still not landed:

- No `sema-upgrade-daemon` production triad exists on disk. `primary-l3h5` remains open.
- Designer `/315` explicitly keeps the daemon shape open: Persona may keep absorbing upgrade orchestration until a second component cutover proves `sema-upgrade-daemon` needs to emerge.
- The current `sema-upgrade` repo still describes itself as library-shaped plus Nix apps/sandboxes.
- The production Spirit cutover (`primary-x3ci`) remains blocked by the v0.1.0 protocol-aware maintenance build (`primary-wdl6`), remaining Persona upgrade orchestration work, and final deployed cutover flow.

Settled design constraints:

- Mirror payload stays raw bytes in a separate container, not a typed enum imported into every contract, per Spirit record 274.
- Persona is the current upgrade orchestrator path, per Spirit records 208–210.
- The first concrete cutover remains Spirit v0.1.0 to v0.1.1, not legacy file import.

## Schema macro state

There are three different things people may mean by “schema macro”; their states differ.

1. **Old `signal-derive #[derive(Schema)]`: exists, but not destination.** It emits an `impl signal::Kind for T` with a static descriptor. Its own source says the role is under review because sema-resident records are now the runtime authority for “what kinds exist”; the emitted descriptors no longer have an obvious consumer.
2. **NOTA schema language: designed, not implemented.** Designer `/263` and `/279` define a NOTA schema language, Blake3 content-addressed schema hashes, schema-header storage, and sema-upgrade dispatch through stored-vs-declared hash comparison. This is architecture, not currently a generator in code.
3. **New converged `signal_channel!` macro: partially implemented today, but missing schema-upgrade generation.** Current `signal-frame-macros` emits request/reply/event enums, kind enums, frame aliases, request-payload impls, stream witnesses, NOTA codec, and observable `Tap`/`Untap`. It does not yet emit recursive Help, Tier 1 `frame_micro`, `CONTRACT_SECTION`, or next-version `VersionProjection`.

Newest intent changes:

- Spirit record 366 says the upgrade path goes through next-version-as-Cargo-dependency: the current schema crate depends on the next schema crate, so the macro sees both and emits `VersionProjection` at current-version compile time.
- Spirit record 367 says the macro convergence is one epic: documentation via Help, Tier 1 64-bit headers, NOTA codec, and next-as-dependency upgrade projection all belong on the same macro extension surface.

Current related beads:

- `primary-ezqx` is the macro convergence epic.
- `primary-v5n2` is now ready for `contract_section` grammar after `primary-li0p` and `primary-avog` closed.
- `primary-2cjv` is ready for `Frame { micro, body }` reshape.
- `primary-8r1j` remains Help auto-injection, now expanded by `/312` to recursive Help-on-every-enum.
- The next-as-dependency / schema-projection macro design is framed by `/317/0-frame-and-method.md`, but the audit/design subreports promised there are not present yet; only the frame exists.

## Practical answer for next work

If the question is “can we use sema-upgrade today?”: yes for the Spirit migration sandbox/staging path and as a protocol witness; no as a production universal daemon.

If the question is “does the sema schema macro exist?”: the legacy descriptor derive exists but is not the new mechanism; the new content-addressed schema/generator/migration macro is still design plus beads, with the implementation target now consolidated into `signal_channel!` macro work.

If the question is “what should operator do next?”: either pick `primary-v5n2`/`primary-2cjv` for the macro foundation, or pick `primary-wdl6`/Persona cutover blockers for the Spirit production path. Do not start by building `sema-upgrade-daemon` unless psyche explicitly chooses the separate-daemon path over Persona absorbing orchestration.
