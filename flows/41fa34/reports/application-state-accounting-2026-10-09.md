# Application-state accounting — 2026-10-09

This is a source/configuration accounting note.  It does not read application
state, transcripts, ledgers, credentials, tokens, or live process metadata.

## Qualified paths and owners

| Application | Qualified retained state path | Lifecycle/source owner | Accounting status |
| --- | --- | --- | --- |
| messenger-clj | `~/.local/state/messenger-clj` | messenger-clj typed store and its supported CLI | Source-qualified path; backup/export and migration procedure need the messenger owner. |
| Codex | `~/.codex` and a generation-selected Codex Next home | installed wrapper plus Codex/harness deployment work | Path family is source-qualified; exact backup/export contract and generation migration owner remain unqualified. |
| Herdr | state path not qualified in production configuration | Herdr package/server and supported Herdr lifecycle | Do not infer a production path from fixtures; Field must supply a declaration or owner-backed migration contract. |

`messenger-clj/src/messenger_clj/core.clj` constructs its typed-store default
under the user's `.local/state/messenger-clj`.  Codex launch source selects a
home-owned app-server-control endpoint; installed wrapper evidence records a
generation-specific Codex Next home.  These observations identify state
families, not their contents.

## Declarative context and gap

CriomOS-home declares immutable package inputs for messenger-clj and Herdr in
`flake.nix`.  The reviewed declaration material does not yet account for the
mutable messenger, Codex, and Herdr lifecycle data above.  That is a source
accounting fact; it is not evidence that the data is disposable or that a
service should be added.

## Required migration discipline

Any host or generation change must use an application-supported backup or
export format, match the application version expected by the target, and
transfer through a coordinated owner handoff.  It must preserve active
authentication sessions where the application supports doing so, and must
never initialize empty user state in place of existing state.  No token or
credential snapshot belongs in this report.

## Handoff

A registered knowledge-source owner should decide where this operational
contract is authored after Astra and Field confirm path ownership.  Field's
pending runtime packet is required to qualify Herdr's production location and
any deployment migration procedure.  Zeus remains separate and owner-unknown;
this note neither adopts its service nor reads its data.
