# Independent Spirit v14 live-cutover acceptance

Date: 2026-08-03, Europe/Madrid

Outcome: **accepted**. No rollback condition was observed.

This lane was read-only with respect to the live Spirit store and services. It
did not request or print record, archive, journal, or rollback bodies. A
separate validator read only a private copied snapshot and emitted bounded
counts, structural facts, equality results, and markers.

## Exact deployed provenance

- Lojix independently reported deployment `2`, generation `2`,
  `UserEnvironment`, `LiveActivation`, `Current`, at CriomOS
  `b46390940cf641e19bc9bbd243726308286a8bd2`.
- That exact CriomOS lock selects CriomOS-home
  `47f5494a4168a93ecfc5208032c778e909ca1313` and Spirit
  `44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8`; Home follows the root Spirit
  input.
- The live CLI reported Spirit `0.26.0`.

The executor's announcement that Lojix was Current was used only as a trigger.
The provenance and runtime observations above were collected independently.

## Independent migration and data witnesses

Both units were cleanly quiesced by the authorized executor during the copy
window. The verifier copied the active v14 live and lifecycle-archive files and
the retained v13 live and archive sources into a private `0700` directory with
`0600` copied files. Every copied file was byte-identical to its source at that
quiesced boundary.

A separately compiled, code-only validator then opened only that copy. It
proved:

| Invariant | Independent result |
|:--|:--|
| Frozen source inventory | 24 v13 records, 941 referents, one prior migration row |
| Current live count | 24 v14 records |
| Identity | every one of the 24 source identifiers exists unchanged in v14 |
| Retained substance | domains, kind, description, and importance match exactly for every record |
| Entry shape | exhaustive compiled destructuring has exactly those four fields, with no remainder |
| Live families | exactly `MigrationsFamily` and `RecordsFamily` |
| Removed surface | certainty, privacy, referents, scope, and `ReferentsFamily` are absent |
| Migration receipt | exactly one v13-to-v14 receipt, recording 24 migrated records |
| Fresh history | 25 log entries: 24 projected records plus the receipt |
| Marker | `(25, 5374348791551424496)` |
| Lifecycle archive | 1,498 v13 rows become 1,498 v14 rows with every identifier and retained field equal |
| Archive families | exactly `RecordsFamily` |
| Guardian journal | no live v7 file existed before first use; isolated first open created v7 and reported zero decisions |

The validator's exhaustive `Entry { domains, kind, description, importance }`
pattern is compile-time evidence against hidden retained fields. Runtime family
enumeration independently proves that the removed referent family was not
registered in either current store.

## Migrator evidence versus independent evidence

The released `spirit-migrate-store` internally stages a rollback copy before
any engine open, validates the frozen v13 catalog, projects the identifier and
four retained fields, rebuilds and reopens live and archive temporaries,
compares their projected rows, requires one v13-to-v14 receipt, sweeps stale
migration temporaries, and exposes archive then live by rename.

Those internal checks were not treated as sufficient for acceptance. The
separate validator additionally compared the retained source and final rows,
enumerated exact final families, compiled against the exact four-field Entry,
checked log length and marker, checked the full archive projection, and opened
a fresh v7 journal with zero decisions. Byte equality of the copied rollback
sources was also checked outside the migrator.

The validator was not part of the Spirit 0.26.0 release interface. Its source
was injected into a disposable private copy of exact Spirit `44ab8e97`, built
through that release's Nix-vendored dependency graph, and deleted with the
private candidate. Only a garbage-collectable, code-only Nix output remained
during verification. It was never run against the live state because its
engine opens can update storage bookkeeping.

## Restored runtime and cleanup

After cleanup and service restoration, independent reads observed:

- judge and daemon both `active/running`, result `success`, main status `0`;
- no unit drop-ins;
- daemon `Requires` and starts `After` the judge;
- three Spirit Unix listeners;
- version `0.26.0`;
- marker `(25, 5374348791551424496)`;
- count `24` through the five-axis v14 query.

The active state surface contains the v14 live and lifecycle archive and has:

- zero schema-14 migration temporaries;
- zero legacy guardian-journal files;
- zero legacy backup files or rollback directories;
- no live v7 journal yet, consistent with lazy first use and zero decisions.

The earlier disposable acceptance candidate was absent. This independent lane
then deleted its own 4,788,224-byte private copied candidate and verified that
no matching candidate directory remained. The final retained recovery material
is intentionally not named here.

## Bead reconciliation

Exactly two primary beads were eligible and are now closed:

- `primary-vq6.8.1`: the published Spirit 0.26.0 implementation, fixture and
  origin checks, removed-surface rejection, fresh v14 history/journal behavior,
  and real copied-corpus projection are all proven.
- `primary-whb`: the transfer envelope was read at Dolt revision
  `ausioluh925q7udo3fr49f9irdded94c`, its owning-store goal manifest was
  verified, and the additional v14 implementation/integration goals were
  included in the acquisition close reason. Its closure claims transfer only,
  not goal completion.

The following remain open because their exact acceptance is not proven:

- `primary-vq6.8`: accepted write-through-guardian and observer-stream e2e;
- `primary-7z3` and `primary-7z3.1`: queued private capture replay;
- `primary-7z3.2` and `skills-anu`: vocabulary completion;
- `primary-7z3.3`: psyche consultation decision;
- `CriomOS-dag`: restart/dependent recovery plus malformed, unavailable, and
  timeout fail-closed runtime witnesses;
- judge-independent reads and durable configuration persistence.

The Orchestrate `SpiritV14Implementation` entry remains an
`Active`/`AncestorOfMain` bookkeeping orphan. The release is already on main;
the orphan is not a runtime blocker and cannot be safely concluded through the
ambiguous lane-only request surface.
