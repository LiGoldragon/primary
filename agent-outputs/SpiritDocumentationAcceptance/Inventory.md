# Spirit v0.26+ Documentation and CLI Acceptance Inventory

Date: 2026-08-04

## Decision and scope

The psyche's approved CLI rule is cross-component architecture: first-party CLI
arguments are NOTA/DOTOS objects, not Unix flags, file-path indirection, or
positional shorthand. A bare typed atom such as `Version`, `Marker`,
`ObserveHead`, or `ObserveHeadObject` is a DOTOS object. `--help` is not a
supported command language and its rejection is not missing help functionality.

The same exchange approved the Luna XHigh train and updating all documentation.
Those are implementation, deployment, and documentation tasks: matter, not core
Spirit intent. The later proposed skill sentence remains unapproved:

```text
Accept CLI arguments only as NOTA/DOTOS objects; never add flags or positional shorthand.
```

No skill file may change without explicit approval of that owning-skill text.

## Acceptance baseline

The accepted live baseline remains Spirit 0.26.0 at
`44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8`. Its active-record contract is:

```text
Entry { Domains Kind Description Importance }
```

The ordinary contract has 21 input roots:

```text
State Record Propose Clarify Supersede Retire ResolveClarification
Observe TextSearch Lookup Count BumpImportance ChangeRecord LookupStash
Tap Untap ApplyAuthorizedRecord SubscribeIntent Version Marker Intent
```

The owner contract has four:

```text
Configure Import ObserveHead ObserveHeadObject
```

The query contract is exactly:

```text
Query { DomainMatch KeywordMatch TextMatch SelectedKind ImportanceSelection }
```

`RecordRequest` contains `Entry` plus `Justification`; justification is not a
fifth entry field. Domain-scoped queries still use typed `DomainScope`; this is
not the removed record-level scope/privacy model.

## Exhaustive documentation acceptance

### Spirit README

- Identifies the exact package, storage schema, and wire-contract version.
- States the four-field `Entry` and five-predicate `Query` exactly.
- Gives one-object invocations for both `spirit` and `meta-spirit`.
- Explains that bare selectors are DOTOS objects, file paths are not accepted by
  user/maintenance CLIs, and Unix flags including `--help` and `--pretty` are
  invalid by design.
- Documents `SPIRIT_SOCKET` and `SPIRIT_META_SOCKET` without implying extra CLI
  operands.
- Points to the exact pinned ordinary and meta schemas as command/type truth.
- Does not call a stale manual complete, and does not claim that help/manpages or
  generated skill usage exist unless they actually ship.

### Spirit manual

- Contains a complete index of all 21 ordinary and four meta roots with at least
  one canonical object example per public/owner operation family.
- Documents current request payloads, replies, error shapes, environment
  variables, and the one-object boundary.
- Removes `Certainty`, core `Privacy`, referent metadata/registration,
  public/private record classes, zero-certainty cleanup, relations fields,
  eight-field `Observe`, `PublicTextSearch`, `PublicRecords`, `RecordDefault`,
  `RecordPrivate`, `ChangePrivacy`, `ChangeCertainty`, and
  `CollectRemovalCandidates` as active-contract concepts.
- Uses `TextSearch`, the five-field `Query`, and explicit lifecycle operations.
- Does not teach temporary `.nota` files as CLI operands.
- Does not claim the manual is generated into skills unless a checked generation
  edge actually exists.

### Spirit architecture

- Describes the four-field shape consistently across wire, live store, archive,
  guardian, import, and mirror boundaries.
- Separates user/maintenance CLI DOTOS text from binary Signal frames and binary
  configuration artifacts.
- States which executable entrypoints are public CLIs and which are daemon-only
  service interfaces. A daemon archive path must not be casually documented as
  an exception to the CLI contract.
- Describes Luna XHigh as the declared production judge profile only after the
  Spirit flake pins and service wrapper prove it.
- Keeps provider redaction, secret/session references, and owner-only sockets as
  operational security boundaries rather than reintroducing core privacy.

### Ordinary and meta contract repositories

- `signal-spirit/schema/signal.schema` remains the sole ordinary command/type
  authority: 21 roots, four-field `Entry`, five-predicate `Query`, no legacy
  metadata or command aliases.
- `meta-signal-spirit/schema/meta-signal.schema` remains the sole owner command
  authority: four roots and four-field imports.
- Generated Rust and authored schemas converge at the exact pinned revisions.
- `examples/canonical.nota` is explicitly labeled as object examples, not a
  shell option grammar or an undifferentiated type fixture.
- Ordinary examples cover every operation family; meta examples cover all four
  meta roots. The current meta file's ordinary `(Intent [All])` dependency
  witness is labeled or moved out of the apparent meta-CLI transcript.
- If schema-backed `Help` remains a library facility rather than an input root,
  docs say so; they do not advertise `--help` or `(Help)` as deployed commands.

### Judge contract and adapter documentation

- `signal-spirit-judge` remains admission-only with one `JudgeAdmission` root,
  a four-field record dependency, and typed redacted diagnostics.
- `judge` documents public `ReasoningEffort::XHigh` and its exact provider
  serialization where the public adapter API enumerates supported efforts.
- `spirit-judge` documents one-object `Serve` configuration, exact Luna/XHigh
  support, fail-closed behavior, and the external-session reference without
  exposing credentials.
- `spirit-judge-config` documents exact production
  `(Production gpt-5.6-luna XHigh)`. Terra/Medium appears only as a labeled
  compatibility test, never as production.
- Prompt record shape, justification shape, and verdict output remain positional
  NOTA and match the four-field admission contract.
- Cross-repository links point to a guide that is current at the linked revision;
  they do not call the stale v0.26 manual complete.

### Canonical CLI objects across shipped binaries

The new ruling is broader than the current blocked plan's two user binaries.
Acceptance inventories every first-party executable that presents itself as a
CLI:

| Executable | Required argument grammar |
| --- | --- |
| `spirit` | exactly one ordinary Input object |
| `meta-spirit` | exactly one meta Input object |
| `spirit-write-configuration` | exactly one configuration-write object |
| `spirit-migrate-store` | exactly one migration object |
| `spirit-judge` | exactly one `Serve` object |
| `spirit-judge-witness` | exactly one typed witness object, if it remains a shipped CLI |

No entry above may read an existing argument as a `.nota` or Signal file, parse
`--pretty`, or publish flag-based usage. Tests must prove rejection of zero and
multiple operands, `--help`, `--pretty`, and existing file paths without reading
the file or reaching mutable state.

`spirit-daemon` currently consumes an immutable binary configuration artifact
path. The owning architecture must either classify this strictly as a private
service entrypoint or wrap the artifact reference in one typed DOTOS startup
object. External tools such as Nix, Jujutsu, systemd, `setsid`, and Codex are not
first-party Spirit CLI grammars; their own flags are outside this ruling.

### Home deployment checks

- Pin the exact new Spirit release revision rather than separately selecting
  judge/config packages.
- Prove the generated judge wrapper contains `OpenAiCodex`,
  `gpt-5.6-luna`, and `(Some XHigh)`, and lacks Terra/Medium as production
  selections.
- Preserve `codex-login` as an opaque external-session reference, the Nix-owned
  Codex executable, process-group teardown, and absence of embedded secrets.
- Invoke wrapper fixtures with canonical objects, for example `spirit Version`
  and `meta-spirit ObserveHead`; do not call fake user CLIs with zero arguments.
- Assert wrapper forwarding preserves exactly one object and does not add
  options.
- Keep configuration writer, migration, and judge service fixtures object-shaped.
- Prove package/service ownership, socket wiring, immutable artifact paths,
  rollback inputs, and absence of obsolete wrappers as the existing check does.

### Release and deployment evidence

- Spirit release checks prove immutable producer pins, package/version policy,
  generated wrapper contents, contract/schema convergence, and all CLI-negative
  grammar cases.
- Home and CriomOS checks run from their repository origins after pinning the
  exact Spirit revision.
- Before activation, bounded Count/Marker and service/socket health are observed
  without exposing record bodies.
- After authorized declarative activation, evidence proves Luna true, XHigh
  true, Terra false, Medium false, the expected immutable executables, one
  bounded provider judgment, unchanged Count/Marker, and healthy sockets.
- Failure invokes the already accepted rollback revision and repeats bounded
  health checks. This audit lane does not activate or roll back anything.

## Core privacy versus operational confidentiality

The word `privacy` must not be removed mechanically from every document.

Core Spirit has no privacy field, privacy magnitude, public/private record
class, privacy query predicate, or privacy-aware guardian policy. Confidential
intent belongs in a separate higher-layer Spirit component in its own
environment.

Operational confidentiality remains mandatory outside that core data model:
credential values, external-session material, raw provider request/output,
live corpus material, record bodies, private store/backup locations, and
diagnostics remain closed or redacted. Owner-only sockets, filesystem modes,
secret references, hashes, and redaction are operational security controls, not
core `Entry` metadata. Documentation passes only when it preserves this
distinction explicitly.

## Independent origin audit

### Clean landed surfaces

- `spirit-judge@b590c2bdd6499cc391ac01dddf2ab67b0d53bd6a`
  README lines 3-18 and architecture lines 34-48 correctly state
  admission-only judgment, the four fields, absence of core certainty/privacy/
  referents, and provider-boundary redaction.
- `spirit-judge-config@fc648d2796513b83cee27ffeb319ceb01134a60e`
  README lines 3-14, architecture lines 16-32, the prompt record shape, and
  `config/provider-policy.nota:5` correctly distinguish the four-field core from
  confidential provider material and select Luna XHigh for production.
- `signal-spirit-judge@4fc339fee6adf3aeed82125aa0de8940bdd1f589`
  is admission-only and treats redaction as operational security, not record
  privacy.

### Current failures and gaps

- `spirit-judge/README.md:20-22` and
  `spirit-judge-config/README.md:16-18` call Spirit `manual.md` the complete
  ordinary/meta CLI guide. At origin Spirit 0.26.0, that manual is still stale;
  these claims are false until the blocked manual repair lands.
- `spirit-judge/src/main.rs:3-9,64-75` explicitly accepts inline NOTA or a
  `.nota`/Signal file operand. Strict cross-CLI object acceptance requires
  removing file indirection, despite the adapter being an internal component.
- `spirit-judge/src/bin/spirit-judge-witness.rs:64-65` publishes a flag-based
  usage grammar. It must become one typed object or be explicitly removed from
  the shipped CLI surface.
- `spirit-judge/skills.md:7-10` names the Luna/Terra Medium compatibility matrix
  but omits the new Luna XHigh case. This is a flagged skill gap only; no skill
  edit is authorized.
- Spirit origin `44ab8e97` still reads `.nota` files in `spirit`, `meta-spirit`,
  `spirit-write-configuration`, and `spirit-migrate-store`. The apply plan only
  changes the first two.
- Spirit `manual.md` still contains the removed v13 vocabulary and commands
  enumerated above. README/architecture remain current but partial.
- Home origin `47f5494a4168a93ecfc5208032c778e909ca1313`
  still asserts Terra/Medium at `checks/spirit-deployment/default.nix:151` and
  lines 370-380, calls the fake `spirit` wrapper with no object at line 329, and
  does not exercise the meta wrapper with a canonical object.

## Audit of the blocked apply plan

[SpiritJudgeLunaXHighTrain.md](/home/li/primary/reports/runtimeTrainWorker/SpiritJudgeLunaXHighTrain.md:1)
correctly records the three portable producer revisions, Luna/XHigh release
pins, exact service-wrapper assertions, Home/CriomOS validation order,
declarative activation boundary, bounded evidence, and rollback.

Its CLI step at lines 32-35 is not apply-ready under the later cross-CLI ruling:

1. It changes only `spirit` and `meta-spirit`, leaving file operands in the
   configuration writer, migration CLI, and judge adapter and leaving flags in
   the judge witness.
2. It says to recognize and reject `--pretty` before object decoding. The CLI
   should have no special flag grammar; rejection should arise from the
   one-object/typed-input boundary.
3. It exempts configuration and internal judge transports categorically. Each
   executable must instead be classified and tested: object CLI, daemon-only
   artifact interface, or external provider tool.
4. Rejecting an existing file is necessary, but the stronger witness is that no
   argument-driven filesystem probe or file read occurs before rejection.

The model pin, service wrapper, Home/CriomOS, activation, and rollback portions
remain usable after these CLI corrections are integrated.

## Concise ownership inventory

Live `orchestrate (Observe Lanes)` shows:

- `dotos_components` has 26 active repository claims for component-root DOTOS
  migration. The relevant collision is `/git/github.com/LiGoldragon/spirit`,
  which blocks the Spirit 0.27 release, CLI/parser/tests, service bundle, and
  README/manual/architecture work. The durable train report records the shared
  checkout as dirty and `RequestWorktree` as rejected with
  `RepositoryNotFound`; this is a proven blocker.
- `dotos_foundations` has 79 active claims for signal-family migration. The
  relevant collisions are `/git/github.com/LiGoldragon/signal-spirit`,
  `/git/github.com/LiGoldragon/meta-signal-spirit`, and
  `/git/github.com/LiGoldragon/signal-spirit-judge`; `signal-domain` may also be
  implicated if canonical domain examples change. These are live ownership
  conflicts awaiting owner coordination. The inspected durable train report
  contains no independent `RequestWorktree` failure witness for them, so they
  should not be described as proven tool blockers without that evidence.

CriomOS Home and CriomOS are downstream only after the immutable Spirit release
exists. Their relevant Spirit pin/check paths are not owned by either DOTOS lane
in the observed snapshot; normal exact-path claims are still required before
editing.

## Current state

No Spirit, contract, judge, configuration, Home, CriomOS, skill, or deployment
file was changed by this audit. No activation or provider call was made. No
skill wording was approved. Bead `primary-7z3.4` now tracks ownership handoff,
object-only CLI integration, Luna XHigh deployment, documentation convergence,
rollback readiness, and bounded post-activation evidence.
