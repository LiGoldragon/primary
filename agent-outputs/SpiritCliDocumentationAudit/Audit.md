# Spirit 0.26 CLI Documentation Audit

Date: 2026-08-04

Audited release: `spirit` 0.26.0, Spirit commit
`44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8`, ordinary contract commit
`b37fc963292c157452d06e150296c19005dae3f2`, and meta contract commit
`009cb6c8ddf985244189a79d554aa5d5c24605c8`.

## Answer

There is no complete, current, user-facing Spirit CLI guide.

The maintained Spirit `README.md` is the best current quick-start: it gives
working `Record`, `Observe`, `TextSearch`, and `Version` examples at
[README.md](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/README.md:45),
and its four-field and five-predicate descriptions are current at lines 6-10
and 60-63. The complete command and type truth lives one layer lower, in the
pinned authored schemas:

- `signal-spirit@b37fc963: schema/signal.schema:44-45, 55-95, 98-220` is the
  full ordinary command, reply, and type contract.
- `meta-signal-spirit@009cb6c8: schema/meta-signal.schema:7-53` is the full
  owner/meta contract.
- Their `examples/canonical.nota` files provide compact syntax samples, but do
  not cover every command and are not operator manuals.

The file named as the full manual, [manual.md](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/manual.md:1),
was not updated for v14 and is unsafe as a command/type reference. The deployed
binaries have no reachable help command, no `--help`, and no manpages. The
installed Spirit-facing skills govern capture and editing but do not document
CLI usage.

## Deployed behavior

The following checks were read-only. Only `Version` reached the daemon; invalid
help inputs were rejected during local NOTA decoding before socket connection.

| Invocation | Exit | Result |
| --- | ---: | --- |
| `spirit Version` | 0 | `(VersionReported 0.26.0)` |
| `spirit --help` | 1 | `invalid NOTA input: unknown Input variant --help` |
| `meta-spirit --help` | 1 | `invalid NOTA input: unknown Input variant --help` |
| `spirit '(Help)'` | 1 | `invalid NOTA input: unknown Input variant Help` |
| `meta-spirit '(Help)'` | 1 | `invalid NOTA input: unknown Input variant Help` |
| `man -w spirit` | n/a | `No manual entry for spirit` |
| `man -w meta-spirit` | n/a | `No manual entry for meta-spirit` |

Both installed closures contain only their respective executable under `bin/`;
neither carries a manpage or packaged documentation.

This behavior follows the released parsers. `spirit` takes one component
argument, decodes it directly as generated `Input`, then connects
([src/bin/spirit.rs](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/src/bin/spirit.rs:34)).
`meta-spirit` does the same for `MetaInput`
([src/bin/meta-spirit.rs](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/src/bin/meta-spirit.rs:29)).
The pinned `triad-runtime@895d2e6b:src/argument.rs:57-108` accepts exactly one
inline value or existing file and has no option parser.

## Current contract

The ordinary input roots at the deployed pin are:

```text
State Record Propose Clarify Supersede Retire ResolveClarification
Observe TextSearch Lookup Count BumpImportance ChangeRecord LookupStash
Tap Untap ApplyAuthorizedRecord SubscribeIntent Version Marker Intent
```

The owner/meta roots are:

```text
Configure Import ObserveHead ObserveHeadObject
```

The central shapes are:

```text
Entry         { Domains Kind Description Importance }
RecordRequest { Entry Justification }
Query         { DomainMatch KeywordMatch TextMatch SelectedKind ImportanceSelection }
```

Thus a record entry has exactly four fields. The justification is a separate
part of write requests, not a fifth entry field. Queries have five predicates:
domain, description-derived keywords, description text, kind, and importance.
They have no certainty, privacy, or referent predicate. Typed `DomainScope`
values still exist inside domain matching; that is not a resurrected record
metadata field.

The exact producer lines are
`signal-spirit@b37fc963:schema/signal.schema:44-45` for roots,
`:98-143` for request nouns, `:171-216` for query and entry shapes, and
`:219-220` for the closed kind and magnitude enums. The meta roots and shapes
are `meta-signal-spirit@009cb6c8:schema/meta-signal.schema:7-53`.

## Documentation surface map

| Surface | What it actually provides | Status |
| --- | --- | --- |
| Spirit `README.md` | Current four-field overview and four ordinary CLI examples | Correct but partial |
| Spirit `ARCHITECTURE.md` | Current ownership, data boundary, read semantics, admission and lifecycle architecture | Correct architecture; not a usage guide |
| Spirit `manual.md` | Intended conceptual and CLI manual | Materially stale and contradictory |
| Spirit `skills.md` | Repository editing prerequisites | Not CLI usage documentation |
| `signal-spirit` schema | Complete ordinary roots and types | Authoritative contract |
| `signal-spirit` `examples/canonical.nota` | Examples for 13 ordinary forms | Current but incomplete |
| `signal-spirit` `src/help.rs` | A library `HelpRequest` and schema renderer | Compiled library API, not reachable from the CLI |
| `meta-signal-spirit` schema | Complete meta roots and types | Authoritative contract |
| `meta-signal-spirit` `examples/canonical.nota` | Meta examples plus contract dependency witnesses | Current but not a pure CLI transcript |
| Installed `intent-log` / `psyche-interraction` skills | Capture authority and conduct | No command syntax or type guide |
| Binary `--help` / NOTA `Help` | Nothing | Missing |
| Manpages / packaged docs | Nothing | Missing |

The ordinary help library is real but unwired. It recognizes `(Help)` and
`(Help Entry)` in `signal-spirit@b37fc963:src/help.rs:58-87`, and is exported
behind `nota-text` in `src/lib.rs:12-19`. However, `Help` is absent from the
generated `Input` roots (`schema/signal.schema:44`), and the released Spirit
binary has no pre-`Input` interception at
[src/bin/spirit.rs](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/src/bin/spirit.rs:34).
The Spirit repository contains no use of `HelpRequest` or `HelpModel` at this
release. The meta contract has no parallel help module.

## Stale and missing material

### Spirit manual

The largest documentation fault is not merely omission: `manual.md` positively
teaches the removed v13 model.

- Lines 9-10 promise certainty guidance even though certainty is absent.
- Lines 184-199 direct agents through referents and privacy.
- Lines 227-273 make certainty and referent judgment part of admission.
- Lines 305-355 define a two-axis certainty/importance entry and a certainty
  rubric. Current entries have importance only.
- Lines 362-375 teach zero-certainty removal and a meta
  `CollectRemovalCandidates` command. Neither exists.
- Lines 380-399 teach a relations field, provenance machinery, and
  low-confidence maintenance that are absent from the current entry.
- Lines 422-454 describe certainty floors, privacy/referent selection, an
  eight-field `Observe`, `PublicTextSearch`, and catch-up queries. Current
  `Query` has five predicates and the command is `TextSearch`.
- Lines 490-503 name nonexistent `RecordDefault`, `RecordPrivate`,
  `ChangePrivacy`, `ChangeCertainty`, and `CollectRemovalCandidates` commands.
- Lines 518-524 place specificity in an open referent layer that v14 removed.
- Lines 551-563 claim the production manual is generated into a Spirit-facing
  skill that thoroughly documents every operation, wire shape, errors, and
  environment variables. The release packaging and installed skills do not do
  that.

Some material remains correct: the one-argument inline/file convention and bare
`Version` selector at lines 456-489, and much of the intent/capture doctrine.
That valid content does not make the manual safe as a current CLI reference.

### README and architecture

[README.md](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/README.md:45)
documents only four of the 21 ordinary roots and none of the four meta roots.
It names the owner-only meta socket at lines 34-35 but gives no `meta-spirit`
invocation or `SPIRIT_META_SOCKET` guidance. `ARCHITECTURE.md:63-71` correctly
summarizes the five principal reads and `BumpImportance`, but intentionally
does not specify complete invocation syntax.

### Producer examples and help

`signal-spirit@b37fc963:examples/canonical.nota:1-13` gives current examples for
only a subset of ordinary forms; it omits the lifecycle, stash, subscription,
and authorization forms. `meta-signal-spirit@009cb6c8:examples/canonical.nota:1-5`
provides all four meta inputs, but line 6 is an ordinary `Intent` dependency
witness rather than a meta input, which is easy to misread without the test
context (`tests/round_trip.rs:123-151`).

The schema-backed help model is missing its executable integration. There is
also no conventional usage synopsis, explanation that `--help` is not an
option, or error message pointing the user to README/schema documentation.

### Skills and installed surface

[intent-log/SKILL.md](/home/li/primary/.agents/skills/intent-log/SKILL.md:6)
contains capture classification and authority rules only. The installed
`psyche-interraction` skill adds approval rules but no syntax. The Spirit
repository's [skills.md](/home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation/skills.md:1)
and the pinned producer `skills.md` files are editing contracts, not operational
guides. Therefore the manual's claim that agents receive a thorough generated
CLI skill is currently false.

## Repair boundary

No documentation, schema, CLI, packaging, or skill file was changed during this
audit. A repair needs an explicit choice of canonical user surface:

1. update or replace `manual.md` from the pinned schemas and current doctrine;
2. publish a complete ordinary/meta command index with canonical examples;
3. either wire the existing schema-backed help model into `spirit` and add a
   meta equivalent, or deliberately implement conventional `--help`;
4. document `SPIRIT_SOCKET`, `SPIRIT_META_SOCKET`, inline/file argument rules,
   and the absence or presence of manpages;
5. make the manual-to-skill generation claim true, or remove it and name the
   actual authority chain.

Until that work lands, the safe lookup order is: deployed `Version`, pinned
Spirit README for basic examples, then the exact pinned ordinary/meta schemas
for commands and types. Do not use `manual.md` for current wire shapes.
