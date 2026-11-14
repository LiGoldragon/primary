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

## Second commit: a bare emission carries a unit; an enum of none is refused

Branch `one-variant-be2651`, head
`f23eacf338a90ce4a6dea011554724fa6488fcc9`, one commit on b2f3898, still
29.0.0. Pushed and not merged. Same worktree.

### A bare emission (Fable's ruling y0ou)

How it stood: a bare emission was accepted, but a bare emission whose name
the file neither declared nor imported generated the unit variant
`Emission::Go`. A variant has no type, so nothing could carry `Emitted` or
implement `Emittable` for it. This is why Energy declares
`CodexRateLimits.{}` and `ClaudeUsage.{}` in its types.

Now such an emission carries a unit of its own: `pub struct Go {}`,
`Emission::Go(Go)`, `impl Emitted for Go { type Outcome = <n-th outcome> }`.
Outcome pairing by position is unchanged. A bare emission naming a declared
or imported type still carries that type and gets no unit. An outcome with
the same name as a unit carries nothing.

- `src/checking.rs`:
  - A trait `Uniting` on File lists the units, each at its emission's path
    `[1 at]`. Only an Emission root has any.
  - `Implying` counts the units as implied names, so they resolve as types
    the way `Input` does, and no other bare variant carries them.
  - `Declared for File` adds the units, so the existing duplicate pass
    refuses a unit named `Emission`, `Outcome`, `Emitted`, `Emittable` or a
    derived name as `Duplicate.<name>`.
  - `Checkable for Emission` runs each unit name through `declare`, so an
    intrinsic name is refused as `Intrinsic.<name>`.
- `src/generation.rs`:
  - The units are emitted after the types section, as a struct of no
    fields, the same item `Go.{}` gives.
  - A trait `United` maps a unit's bare emission to the variant carrying it,
    both in the `Emission` enum and in the `Emitted` bindings.
- Energy's `ethos-565bc8` emission.ethos (aafd0eb), with the two `.{}`
  declarations removed, generates the same items under the new head; only
  the order of the two unit structs differs.

### An enum of no variants

`SingleVariant` is renamed `TooFewVariants`, since 29.0.0 is unreleased. The
one refusal reads true for one variant or none. `Plural` refuses
`len() < 2`. `Never.[]` is now
`Rejected.{ F { 1 20 } Conceptual.{ [ 1 1 0 1 ] TooFewVariants.Never } }`.
The finiteness walk's special case for an empty enum ("declared empty on
purpose") could no longer be reached, so it is removed.

A root's sections still count as the root's and may hold one variant or
none. A Signal with no inputs generates no `Input` enum at all, so it never
relied on an empty enum: `Signal [] [] [] []` and `Emission [] [] [] []`
still check.

`error.ethos` and `src/error.rs` were renamed together, and the hand edit
matches a fresh generation. README and UPGRADES (29.0.0, now in three
parts) and the `Emission` doc in `src/lib.rs` are updated.

### Tests

- `tests/ethos.rs`:
  - `an_enum_of_no_variants_is_refused_naming_the_enum`: a declared enum;
    `Never.[] Holder.{ Never }`; an inline enum; a struct position
    `State.[]` in a Memory; an Emission's types. Empty Signal and Emission
    roots are still accepted.
  - `an_enum_of_two_variants_is_accepted_declared_and_inline` no longer
    carries `Never.[]`, and the finite-type test drops its `Never` line.
  - `a_bare_emission_carries_a_unit_of_its_own_and_binds_its_outcome`:
    `Go(Go)`, `Emitted for Go = Gone_Data`, a declared `Ask` carried with no
    unit, an outcome named as a unit carrying nothing, an imported `Pane`
    carried.
  - `a_bare_emission_whose_unit_a_type_may_not_take_is_refused`: the four
    implied names as `Duplicate` at `[ 1 1 0 ]`, `String` as `Intrinsic`, and
    `Go_Data` beside `Go.{ String }` as `Duplicate.Go_Data`.
  - The past-the-last test now counts three bindings: `Stop` binds `i64`.
- `fixtures/bare-emission.ethos` and `tests/generated/bare-emission.rs` are
  new. Freshness counts 24 fixtures and print counts 26 sources.
- `tests/generated.rs`:
  `a_bare_emission_carries_its_unit_and_yields_the_outcome_its_position_binds`
  implements `Emittable<Prober>` for `Probe` (yielding `Probed_Data`) and
  for `Ping` (yielding `()`), and builds `Emission::Probe(Probe {})`. It
  compiles with datom enabled.
- `tests/cli.rs`: the located refusal now reads `TooFewVariants.Refused`.
- I checked all 213 source literals in tests/ and src/ with the b2f3898
  binary and the new one. Only the intended literals differ: the rename,
  the new zero-variant refusals, and the two new emission refusals. Every
  fixture and `error.ethos` and `ethos-zero.ethos` regenerate byte-equal,
  except the new fixture.

### Gate

`nix-fast-build --remote li@prometheus.goldragon.criome --no-nom
--no-download --eval-workers 1` on `checks.x86_64-linux` at f23eacf exited
0, with all 13 checks passing. The crate's test binaries ran 66, 26, 22,
20, 9, 4 and 0 tests, with 0 failures.

- Log:
  /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-f23eacf.log
- The first push, 27c67e3, failed one test: print's fixture count, still
  25. Log:
  /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-27c67e3.log
- I amended the commit with the count and force-pushed it with a lease.

New binary:
/nix/store/d9nv1n77gypi90h9jy9vqdb450xd6cgx-all-workspace-members/bin/ethos-zero

### Radius additions

- **Zero-variant enums: none in any active repository.** I swept every
  `.ethos` file at origin/main in every LiGoldragon clone, the radius's 23
  repositories freshly fetched, for an empty bracket after a head. Every hit
  was one of these:
  - a trait with no capabilities in a Library's traits section (protos
    `Canonicalizable.[]`; datom-codec `Branchable.[] Budgeted.[]
    Positional.[]`; primary-next's vendored copies of both);
  - a comment (signal-flow, signal-orchestrate).

  The protos and datom-codec files check under the new head, and
  dependency-ethos passes.
- **No file relies on an empty Signal.** An empty Signal section never
  generated an enum.
- **No file changes from b2f3898 to f23eacf.** Check over 303 `.ethos` files
  (119 repositories at origin/main, plus the ethos-565bc8 branches of
  energy-nexus at aafd0eb, signal-energy-nexus and
  meta-signal-energy-nexus) gives the same result under both binaries, with
  `SingleVariant` read as `TooFewVariants`.
- **No active Emission root holds a bare emission without a type of its
  name.** The active Emission roots are:
  - Curriculum emission.ethos;
  - energy-nexus ethos-565bc8 emission.ethos;
  - flow-nexus emission.ethos, which I probed past its five one-variant
    enums;
  - the fixture.

  The three repository files generate byte-equal under both binaries.
- Data:
  - /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/radius2.tsv
    (columns: repo@rev, file, new result, b2f3898 result)
  - /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/zero-text.txt
  - Script:
    /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/tools/radius2.py

To deploy: Energy may drop `CodexRateLimits.{}` and `ClaudeUsage.{}` once
it pins this head. That step is Energy's, and I left it untouched. The
build-base `crate-versions.json` and `crate-features.json` entry for 29.0.0
is still owed at merge.
