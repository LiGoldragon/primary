# Report 28 - Operator consequences of designer/138

Date: 2026-05-12
Role: designer-assistant

## Scope

This scans the operator work that followed
`reports/designer/138-contract-types-own-wire-and-text-derives.md`.
Designer report 139 is about Wi-Fi PKI and does not materially change
this contract-migration review.

The review uses current working-tree state. Several contract crates are
dirty, so this is a scan of in-flight operator work, not only pushed
history.

## Current reading

Designer/138 made this rule canonical:

- contract crates own the typed records;
- the same contract types own rkyv wire derives and NOTA text derives;
- consumers must stop carrying schema-side mirror types and
  `from_contract` enum projections;
- tests should prove both binary frame round trips and NOTA text round
  trips through the production types.

This now agrees with `skills/contract-repo.md`: the contract value is
the wire value and the text-encodable value. Surface owners decide where
NOTA is rendered, but they do not invent duplicate text-side types.

## What is good

The main direction is right. `signal-persona` and
`signal-persona-auth` have already moved into the new shape: explicit
`nota-codec` dependencies, the canonical rkyv feature set, direct NOTA
derives or closed manual codecs on contract types, and round-trip tests.

The in-flight work in `signal-persona-message`,
`signal-persona-system`, `signal-persona-harness`, and
`signal-persona-terminal` follows the same broad pattern. Each crate now
has an explicit `nota-codec` dependency, and `cargo test --quiet` passed
locally in each of those dirty repos.

The persona meta crate has also absorbed part of the cleanup:
status-shaped Pattern A mirrors are mostly gone, and the strum
discriminant move from the related designer reports has landed for
engine events. This is a real reduction in duplicate vocabulary.

The rkyv feature mismatch previously seen in `signal-persona-auth` also
appears fixed. All checked contract manifests use the canonical feature
set: `std`, `bytecheck`, `little_endian`, `pointer_width_32`,
`unaligned`.

## Gaps

The immediate operational blocker is that the relation-contract changes
are not landed yet. `signal-persona-message`, `signal-persona-mind`,
`signal-persona-system`, `signal-persona-harness`, and
`signal-persona-terminal` are dirty. Until those repos are committed and
pushed, the open bead `primary-8c1` remains blocked: `persona` cannot
refresh its lock files to stable remote commits and prove the whole
stack with `nix flake check`.

`signal-persona-mind` is the largest risk. It has many manual NOTA impls
and several contract structs near the current channel choreography that
still appear to lack NOTA derives. Its own `ARCHITECTURE.md` still says
NOTA projection is missing and lists missing witnesses. `cargo test`
passed, but it emitted an unused `NotaSum` import warning, and I did not
find NOTA round-trip tests comparable to the other relation crates.

The other dirty relation crates have representative NOTA tests, not
obviously exhaustive contract-surface coverage. That may be acceptable
for a first pass, but it does not yet meet the stronger wording in
`skills/contract-repo.md`: every record kind should have both rkyv and
NOTA round-trip witnesses. This matters most where the codec is manual.

`signal-persona-terminal` is structurally correct but worth watching.
It has several hand-written `NotaEncode` / `NotaDecode` impls for
payload-bearing enums such as prompt patterns, prompt state, worker
lifecycle, and exit status. Manual closed codecs are not wrong, but they
must be variant-exhaustively tested or they become the new mirror debt.

The persona meta crate still has remaining projection debt. Pattern B
operation-kind report enums remain in `persona/src/schema.rs`, with
`from_kind` / `from_operation` conversions. `TextEngineId` also remains
even though `signal-persona-auth::EngineId` is now NOTA-capable. This is
not the old Pattern A status mirror problem, but it is the same family
of duplicated typed vocabulary.

Some repo architecture files are now stale. Several still describe
wire-only contract tests or say text projection lives elsewhere. Those
statements conflict with the new contract rule and should be updated
after the code lands.

## Pattern to watch

The worrying pattern is not the migration direction. It is manual codec
creep.

When a derive macro does not fit an enum shape, the operators are
hand-writing NOTA codecs in the contract crate. That keeps ownership in
the right crate, but it can quietly recreate the same maintenance
problem under a different name: a new enum variant gets added, the
manual codec is not updated, and the tests only cover the happy variant.

The rule I would apply is:

- derive first;
- use manual NOTA impls only when the closed sum shape requires it;
- document why the manual impl exists;
- test every variant of that manual impl through decode and encode;
- keep `cargo test` warning-free before landing.

This preserves the designer/138 decision without turning contract crates
into fragile parser islands.

## Best path forward

1. Finish the dirty relation-contract repos before touching more persona
   consumers. `signal-persona-mind` should be the stop sign: remove the
   unused import, add real NOTA round-trip tests for the missing contract
   surfaces, and reconcile its architecture file.

2. For every relation crate with manual NOTA codecs, add
   variant-exhaustive tests or a clear witness table in the architecture.
   Representative tests are fine for derived records; manual codecs need
   stronger proof.

3. Commit and push the five dirty contract repos, then close the pin
   refresh bead by updating `persona` to those remote commits. The
   acceptance should be a clean `nix flake check` in `persona` with no
   local git/file overrides.

4. After the remote contract pins are stable, finish the persona-side
   cleanup: delete or justify `TextEngineId`, remove Pattern B
   operation-kind report mirrors, and make tests round-trip the contract
   values directly wherever a presentation wrapper is not semantically
   adding anything.

5. Update the stale architecture files after code lands. The docs should
   say the contract crate owns both rkyv wire and NOTA text derives, and
   consumers own only surfaces and projection policy.

6. Add a small repo-wide guard later: every `signal-*` contract crate
   with rkyv should have explicit `nota-codec`; contract test suites
   should contain named NOTA witnesses; and CI should reject warnings for
   these crates.

## Verification performed

I read designer/138, designer/139, `skills/contract-repo.md`,
`skills/rust-discipline.md`, and `skills/testing.md`.

I inspected current repo status and recent diffs for:

- `signal-persona`
- `signal-persona-auth`
- `signal-persona-message`
- `signal-persona-mind`
- `signal-persona-system`
- `signal-persona-harness`
- `signal-persona-terminal`
- `signal-core`
- `persona`

I ran `cargo test --quiet` in the dirty relation-contract crates:

- `signal-persona-message` - passed
- `signal-persona-mind` - passed, with an unused `NotaSum` warning
- `signal-persona-system` - passed
- `signal-persona-harness` - passed
- `signal-persona-terminal` - passed

I did not run the full cross-repo Nix proof because the relevant
contract repos are still dirty and the `persona` pin-refresh bead is
explicitly waiting for landed remote commits.
