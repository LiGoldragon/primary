# Spirit v14 live-cutover independent verification

Date: 2026-08-03, Europe/Madrid

Outcome: **accepted**. No rollback condition was observed.

This verification was read-only with respect to live Spirit state and service
control. The cutover executor's Lojix `Current` result was used only as the
start signal. Provenance, runtime health, migrated structure, retained data,
and cleanup were then observed independently. No record, archive, journal,
secret, or recovery-material body was printed.

## Bounded pre-state

Before cutover, direct runtime witnesses showed:

| Surface | Observation |
|:--|:--|
| Lojix | deployment/generation `1/1`, `Current`, query marker `19/19` |
| CriomOS | `e658bf55bb0f06af012c8edf429d519c3b238c93` |
| CriomOS-home | `d2d02bb61eb3557594b2c302e2862e5e0f58fb86` |
| Spirit | `eabe6c6d96112b46d15443e1c1a29d940605785f`, version `0.25.1` |
| Runtime | judge and daemon active/running/success; required ordering intact; three listeners |
| Store | count `24`; marker `(974, 7784350440604474991)` |

These observations are now historical rather than current, but form the
bounded comparison baseline.

## Exact post-cutover provenance

Independent reads after Lojix reported the target current showed:

| Surface | Accepted observation |
|:--|:--|
| Lojix | deployment/generation `2/2`, `UserEnvironment`, `LiveActivation`, `Current` |
| CriomOS | `b46390940cf641e19bc9bbd243726308286a8bd2` |
| CriomOS-home | `47f5494a4168a93ecfc5208032c778e909ca1313` |
| Spirit | `44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8` |
| Spirit CLI | version `0.26.0` |

The exact CriomOS lock selects the exact Home revision, and Home follows the
root Spirit input at the revision above.

Non-blocking observation: the Lojix node query labels both generations 1 and 2
`Current`. The active user profile and both running Spirit executables
independently resolve to generation 2's exact closure, so this did not weaken
cutover acceptance. The ambiguous historical label remains an open Lojix
reporting issue; this verifier did not mutate Lojix state.

## Independent migration witness

During an executor-controlled quiescent window, the verifier copied the v14
live/archive state and retained v13 live/archive sources byte-identically into
a private mode-`0700` root with mode-`0600` files. A separately compiled,
code-only validator opened only that copy and emitted bounded structural facts,
counts, markers, and equality results.

| Invariant | Result |
|:--|:--|
| Frozen v13 source | 24 records, 941 referents, one prior migration row |
| Current v14 store | 24 records |
| Identity | all 24 source identifiers retained exactly |
| Retained substance | domains, kind, description, and importance equal for every record |
| Entry shape | exhaustive compiled destructuring contains exactly those four fields |
| Live families | exactly `MigrationsFamily` and `RecordsFamily` |
| Removed structure | certainty, privacy, referents, scope, and `ReferentsFamily` absent |
| Migration receipt | exactly one v13-to-v14 receipt with count 24 |
| Fresh history | 25 entries: 24 records and the receipt |
| v14 marker | `(25, 5374348791551424496)` |
| Lifecycle archive | 1,498 rows before and after; every identifier and retained field equal |
| Archive families | exactly `RecordsFamily` |
| Guardian journal | isolated first open created v7 with zero decisions |

No count, identity, retained-substance, migration, archive, or journal
invariant failed; therefore no rollback signal was issued.

The validator is not a release interface. Its disposable source compiled
against exact Spirit `44ab8e97` through the release's Nix-vendored graph and
was deleted with the private source tree. It was never run against live state
because engine opens can update storage bookkeeping.

## Restored runtime and active-state cleanup

After service restoration, independent direct observations found:

- judge and daemon `active/running`, result `success`, main status `0`;
- no unit drop-ins;
- daemon dependency and ordering on the judge intact;
- exactly three Spirit Unix listeners;
- version `0.26.0`;
- count `24` through the v14 query surface;
- marker `(25, 5374348791551424496)`;
- live and lifecycle archive present;
- zero migration temporaries, legacy journals, legacy backups, rollback
  directories, or candidate directories;
- live v7 journal absent, consistent with lazy first use and zero decisions.

The verifier deleted its 4,788,224-byte private candidate and confirmed that
no matching candidate directory remained. Intentionally retained recovery
material is not identified in this report.

## Witness classification and remaining gaps

| Classification | Claims |
|:--|:--|
| Wired/direct | Lojix current generation, immutable lock provenance, systemd unit/dependency state, listener count, CLI version/count/marker, active-state cleanup |
| Wired/isolated | identity and four-field equality, exact family inventories, receipt/history, archive projection, fresh v7 journal |
| Release-internal | migrator snapshot staging, frozen catalog validation, projection/reopen comparisons, atomic exposure, temporary sweep, `Current` detection |
| Contract-only | none used as acceptance evidence |
| Conceptual | none used as acceptance evidence |
| Stale | the bounded pre-cutover provenance and v13 marker, retained only as comparison evidence |

The dual-`Current` Lojix label is a wired observation but not an accepted
statement that both generations are active. Active-profile and executable
closure resolution were the runtime authority for generation selection.

This cutover does not prove the broader open behaviors: accepted
write-through-guardian and observer-stream end-to-end operation, queued private
capture replay, vocabulary completion, psyche consultation, judge-independent
reads, durable configuration persistence, or restart/dependent recovery under
malformed, unavailable, and timeout failures.

## Bookkeeping

The implementation bead `primary-vq6.8.1` and manifest-transfer bead
`primary-whb` were closed after acceptance. Broader goals remain open.

The Orchestrate record for repository `spirit`, branch/lane
`SpiritV14Implementation`, remains `Active` / `AncestorOfMain`. This is a
bookkeeping orphan rather than a runtime blocker: the deployed conclusion
request identifies only a lane and cannot safely disambiguate the three
worktree records that share it.
