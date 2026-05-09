# Operator Work And Sema Impact Review

## Scope

Reviewed the latest operator-shaped work around the Persona stack and checked
whether Sema commit `b30d0250` (`Table::ensure`, typed table `iter`/`range`,
owned table keys, contextual rkyv errors, Nix test scripts) requires downstream
updates.

Latest operator cluster reviewed:

- `signal-persona` `f2916a824112` - drop Persona type prefixes.
- `persona-system` `eafb99601b2b` - drop Persona type prefixes.
- `persona-message` `2427924e9379` - typed endpoint transport kind.
- `persona-message` `0fb51a952011` - consume `persona-system::Error`.
- `persona-router` `0f37fb9f74fc` - drop Persona type prefixes and consume
  typed endpoint kinds.

## Findings

### No blocking issue found in the latest operator code

The prefix-removal commits are mechanically consistent across the reviewed
surface:

- `signal-persona` now exposes `RequestPayload`, `ReplyPayload`, and `Error`;
  no residual `Persona*` type names were found in `src/`, `tests/`, README, or
  architecture docs.
- `persona-system` now exposes `Error` and `SystemEvent`; no residual
  `PersonaSystem*` type names were found in its active code/docs.
- `persona-router` now consumes `persona_message::schema::EndpointKind` as a
  closed enum instead of comparing endpoint kind strings.
- `persona-message` setup/test scripts now emit `Human`, `PtySocket`, and
  `WezTermPane`, matching the new `NotaEnum` endpoint kind shape.

Verification:

- `nix flake check` evaluated cleanly for `signal-persona`, `persona-system`,
  `persona-message`, and `persona-router`.
- Explicit check builds passed with:
  - `nix build .#checks.x86_64-linux.default --no-link` in `signal-persona`
  - `nix build .#checks.x86_64-linux.default --no-link` in `persona-system`
  - `nix build .#checks.x86_64-linux.default --no-link` in `persona-router`
  - `nix build .#checks.x86_64-linux.default --no-link` in `persona-message`

Notes:

- Several flakes still emit app `meta` warnings or report `running 0 flake
  checks` from `nix flake check`. That is test-surface hygiene, not a regression
  in the operator commits reviewed here.

### Sema impact: persona-sema should adopt `Table::ensure`

`persona-sema` is the downstream component that should change because of the
new Sema surface.

Current state:

- `persona-sema/Cargo.lock` pins Sema at `01a21939`, before `Table::ensure`,
  `Table::iter`, and `Table::range`.
- `persona-sema/src/store.rs` says `PersonaSema::open` creates declared tables
  on first open, but the implementation only calls `Sema::open_with_schema`.
- `persona-sema/src/tables.rs` already centralizes every typed table constant,
  which is exactly the shape `Table::ensure` was added to support.

Recommended update after the active designer claim clears:

1. Bump `persona-sema`'s Sema dependency to `b30d0250` or later.
2. Add one local method that ensures every table constant from `src/tables.rs`.
3. Call that method inside `PersonaSema::open` after `Sema::open_with_schema`.
4. Add a test that opening a fresh database materializes empty tables without
   inserting rows.

This is not a breaking change: existing `persona-sema` code still builds with
its pinned old Sema. The update is warranted because it makes the current docs
true and moves table materialization into the consumer typed layer where it
belongs.

Tracked follow-up:

- `primary-0q2` - `persona-sema materializes typed tables with sema Table::ensure`

### Sema impact: criome does not need an immediate update

`criome` still uses Sema's legacy slot-store surface:

- writes through `Sema::store`
- reads through legacy `Sema::iter`
- uses `reader_count`

Sema commit `b30d0250` did not change those APIs. `criome`'s current check build
passed against its existing pinned Sema. The later per-kind table migration can
use `Table::iter` / `range`, but that belongs to the existing Sema-kernel
migration work rather than an urgent compatibility update.

## Lock Context

`persona-sema` and `criome` are currently under the designer role's architecture
revamp claim. I did not edit them. The concrete `persona-sema` adoption work is
recorded as `primary-0q2` for the next available implementation pass.
