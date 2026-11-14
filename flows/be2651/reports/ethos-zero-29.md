# ethos-zero 29.0.0: an enum of one variant is refused

Branch `one-variant-be2651` on LiGoldragon/ethos-zero, head
`b2f389837071bcb4f08e97dda0f08eb979d83f08`, one commit on origin/main
970459d (28.0.0). Pushed and not merged. Worktree:
/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/ethos-zero

## The change

- `src/checking.rs`: a trait `Plural` on `[Variant]` refuses a list of exactly
  one variant as `Problem::SingleVariant(<enum>)` at the enum's variants
  (path `… 1`, the bracket). It is called in the enum arm of
  `Checkable for TypeDeclaration`, naming the declaration, and in the
  `Variant::Enum` arm of `Checkable for Variant`, naming the variant. That
  covers declared enums in every root's types and every enum a variant
  declares in place, including one inside a Signal input's struct payload.
  A root's own sections (a Signal's inputs and outputs, an Operation's
  operations and outcomes, an Emission's emissions and outcomes) are not
  counted, so a Signal with one input still checks.
- `error.ethos` and `src/error.rs`: `Problem` gains `SingleVariant.String`
  after `Unpaired`. The hand edit matches a fresh generation.
- Located: `Reply.[ Accepted ]` →
  `Rejected.{ <file> { 1 20 } Conceptual.{ [ 1 1 0 1 ] SingleVariant.Reply } }`.
- `Never.[]`, an enum with no variants, is still accepted, because a test
  requires it to be. The vision says "two variants or more", which would
  also rule out zero. That is left for Psyche to decide.
- Fixtures and test sources that held a one-variant enum each got a second
  variant, and their generated files were regenerated:
  - `orchestrate.ethos`: `ReleaseRejection.[ UnknownLockId AlreadyReleased ]`,
    `ObserveSelection.[ Locks Lock.LockId ]`, `Observation.[ Locks Lock ]`.
  - `composition-types.ethos`: `Nested`/`Choice`.
  - `inline-collision.ethos` and `nested-collision.ethos`: the inline probes.
  - `SinkError.[ Closed Full ]` in the round-trip library (tests/ethos.rs and
    src/lib.rs).
  - `E.[ Only.E Also.E ]` in the cycle test, which is still refused as
    `Cycle.E` at the same path.

  I found every affected test literal by checking all 191 source literals in
  tests/ and src/ with both the 28 and the 29 binary. After the fixes, none
  of them differs.
- The README has a new paragraph on the rule, and its `Part.[ Block ]`
  example now has a second variant. UPGRADES.md has a 29.0.0 entry.
  Cargo.toml, Cargo.lock and Cargo.nix are at 29.0.0.

## Tests

- `tests/ethos.rs`:
  - `an_enum_of_one_variant_is_refused_naming_the_enum`: declared enums in
    Library, Memory and Signal types.
  - `an_inline_enum_of_one_variant_is_refused_naming_its_variant`: an inline
    enum, a nested inline enum, and an inline enum in a Signal input.
  - `an_enum_of_two_variants_is_accepted_declared_and_inline`: generates
    `Reply{Accepted,Refused(Refused_Data)}` and `Refused_Data{Busy,Down}`,
    with `Never.[]` beside them. A one-input Signal is accepted.
- `tests/cli.rs`:
  - `check_locates_an_inline_enum_of_one_variant_naming_the_file_and_the_enum`:
    `{ 4 19 } … [ 1 1 0 1 1 1 ] SingleVariant.Refused`.

## Gate

`nix-fast-build --remote li@prometheus.goldragon.criome --no-nom --no-download
--eval-workers 1` on `checks.x86_64-linux` at b2f3898 exited 0. All 13
checks passed: cargo-nix, crate-features, crate-versions, default,
dependency-ethos, ethos-zero, flow-contract, flow-contract-datom, fmt,
no-free-functions, no-inherent-methods,
operation-free-signal-without-datom, signal-without-datom. The crate's test
binaries ran 63, 25, 22, 20, 9, 4 and 0 tests, with 0 failures.

Log:
/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-b2f3898.log

The remote has to be `li@`. With `nix-ssh@` from /etc/nix/machines,
nix-fast-build fails at `nix config show` (exit 255).

The protos and datom-codec ethos files that dependency-ethos reads all
check.

build-base pins ethos-zero by git revision in `crate-versions.json`
(22.0.0, 27.0.0, 28.0.0) and `crate-features.json`. 29.0.0 would need an
entry once the branch is merged. build-base is unchanged.

## Radius

I ran the 29 binary's Check over every `.ethos` file at each repository's
origin/main, plus the ethos-565bc8 branch of energy-nexus,
signal-energy-nexus and meta-signal-energy-nexus. That is 66 files.

For each refused enum, the scan inserted a probe second variant at the
reported bracket and checked again, until no SingleVariant remained, so
every one-variant enum in a file is listed. Some files 28 already refused
for another reason. I patched that earlier refusal in a scratch copy and
scanned them the same way: signal-energy-nexus (Duplicate.Input), herdr-nexus
meta-call and public-call (Duplicate.Input), belief-nexus emission,
signal-belief-nexus and meta-signal-belief-nexus (Undeclared.Query). Only
meta-signal-energy-nexus holds one. signal-herdr-nexus and signal-lojix
(Wrapping, under 28 too) hold none: the types are checked before the
Wrapping pass, so a one-variant enum would have been reported first.

Files the new rule refuses (enum @ line):

| Repository @ rev | File | One-variant enums |
|---|---|---|
| flow @ eabddc8d | crates/flow-ethos/ethos/library.ethos | StartRefusal@84 |
| flow @ eabddc8d | crates/flow-nexus/ethos/emission.ethos | ScreenFormat@53, ShellLine@56, MetadataSource@67, CodexTitle@86, HerdrSocketRequest@117 |
| flow @ eabddc8d | crates/flow-nexus/ethos/landing.ethos | RefreshCause@48 |
| flow @ eabddc8d | crates/flow-nexus/ethos/startup.ethos | StartRefusal@9 |
| meta-signal-flow @ cdb4e7d | ethos/signal.ethos | ReadSendOutcomesRejected@380, InspectRejected@383, StoreRefusal@597 |
| meta-signal-flow @ cdb4e7d | tests/fixtures/meta-signal-flow-78.ethos | ReadSendOutcomesRejected@366, InspectRejected@372, StoreRefusal@591 |
| Curriculum @ 47d110e | curriculum.ethos | RolesDocument@29 |
| signal-orchestrate @ e4fda9b | ethos/signal.ethos | ReleaseRejection@75, ObserveSelection@76, Observation@77, Refusal@78 |
| meta-signal-orchestrate @ 27ac19c | ethos/signal.ethos | ConfigurationRejectionReason@17 |
| meta-signal-energy-nexus @ 3264d6f (main) | signal.ethos | Input@3 (inline `Input.[ Configure.Set ]` in `Call.{ … }`; 28 refused the file as Duplicate.Input) |
| meta-signal-energy-nexus @ 24958c7 (ethos-565bc8) | tests/fixtures/signal-0.5.0.ethos | Input@3 (the same; 28 refused it as Duplicate.Input) |
| lojix @ da0ad8a | ethos/ingress.ethos | InspectionRequest@3, ResetStoreRequest@5, BootstrapRequest@6, BootstrapStrictHostKeyMode@23, ConfigurationWriterInput@42 |
| horizon-rs @ e723ce1 | lib/ethos/horizon.ethos | MotherBoard@67, DomainProvider@69, SiteRenderer@77, PersonaCapability@123, CompositionCommand@173 |

That is 13 files and 32 enums. Every other file checks under 29 exactly as
it did under 28. The meta-signal-energy-nexus ethos-565bc8 `ethos/signal.ethos`
and all energy-nexus ethos-565bc8 files check.

Repositories in the brief I could not match exactly:

- No `horizon-lib` repository exists. Its ethos is horizon-rs's
  `lib/ethos/horizon.ethos`, which is the file scanned above.
- No `book-nexus` repository exists locally or under the LiGoldragon
  account. books and BookMaker have no `.ethos` files, so book-nexus and
  its contracts are not covered.
- `nexus` has no `.ethos` file at origin/main.

Data:

- Table:
  /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/radius.tsv
  (columns: repo@rev, file, 28 result, 29 result, enums, result after probing)
- Scripts:
  - /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/tools/radius.py
  - /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/tools/scan.py
- Binaries:
  - 29: /nix/store/cfagcjijhn62x5f4xw26jhzwgpvx8vmb-all-workspace-members/bin/ethos-zero
  - 28: /nix/store/383qv46b46g3p6ccn2zn3r1c0qxvcxhz-all-workspace-members/bin/ethos-zero
