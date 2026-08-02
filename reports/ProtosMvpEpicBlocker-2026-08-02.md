# Protos MVP Slices 1–3 Delivery Report — 2026-08-02

This is the morning-style report required by
[`handoffs/codex-mvp-slices-1-3-2026-08-02.md`](/home/li/primary/handoffs/codex-mvp-slices-1-3-2026-08-02.md)
for the Protos MVP train. It retains the original hard-stop evidence and its
explicit supersession, then records the completed Slice 1–3 landing.

## 1. Landed Slice 1 and original green gates

Slice 1 landed in `core-ethos` as version `0.24.0` at
`70e3b7fdc536543e64f5fe2b232eab3c0d988910`. Local `main` and
`main@origin` matched that revision after push. The landing added the composite
header-imports-body codec, kind-selected Interface/Nexus/Sema roots, the fixture
vocabulary needed by the three reviewed Spirit documents, exact fixture copies
in the crate, and Nix exposure of those `.ethos` files.

The original landing gates were green:

- `cargo check --jobs 2` passed.
- The focused `spirit_fixtures` suite passed all four tests.
- The full bounded Cargo test run passed 18 tests.
- warning-denied Clippy and rustdoc passed.
- formatting verification passed.
- `nix flake check --no-build --no-write-lock-file --max-jobs 1 --cores 2`
  passed.
- The final full `nix flake check --no-write-lock-file
  --print-build-logs --max-jobs 1 --cores 2` passed, including the four Spirit
  fixture tests. An earlier Nix attempt exposed that the source filter omitted
  `.ethos`; the filter was corrected before the landed green run.

Those gates establish the state of the landed change. They do not override the
independent audit below. In particular, the original golden test passed because
the encode path returned retained input text after separately invoking the
structural writer; it did not prove encoded-to-text re-emission.

## 2. Independent audit failure

The acceptance audit failed Slice 1 after it landed. The following public
invariant defects remain unfixed:

- `WholeEthosHeader::new` accepts any version even though the codec documents
  and decodes only compatibility generation `1`.
- `WholeEthos::new` accepts a header whose kind disagrees with its body variant.
- `WholeEthos::to_archive_bytes` serializes without first enforcing the
  supported-version and header/body-kind invariants. Archive restoration does
  validate them, so the two public archive directions do not uphold the same
  boundary.
- Public constructors admit grammar-impossible empty structs, enumerations,
  operator payloads, and traits.
- Archive validation checks encoded identities and references but does not
  reject those empty cardinalities. An impossible value can therefore enter
  through public construction or archive data and survive as an encoded
  carrier even though the grammar cannot emit it.
- `EthosCodec::encode` computes the shared writer's output, discards it, and
  returns retained source text. The golden test consequently witnesses source
  retention rather than re-emission from typed/encoded `WholeEthos`.
- The public module description in `src/lib.rs` still calls the `whole` surface
  “types-only,” despite the landed composite document model.

No remediation for these defects was retained. The mandated re-emission
feasibility gate below failed first, so work stopped without weakening the
acceptance criterion.

## 3. Exact structural-writer blocker evidence

A bounded diagnostic temporarily returned the actual result of
`StructuralEvaluator::encode_text` from `EthosCodec::encode`. It ran only:

```text
cargo test --test spirit_fixtures \
  all_three_spirit_goldens_decode_typed_and_reemit_byte_identically \
  --jobs 2 -- --exact --nocapture
```

The test failed before moving beyond the Interface fixture. The distinguishing
prefixes were:

```text
shared writer: Interface.1 [] {[Record.Entry ...
golden:        Interface.1\n[]\n{\n  [Record.Entry ...
```

The corresponding exact prefix bytes were:

```text
shared writer: [73, 110, 116, 101, 114, 102, 97, 99, 101, 46, 49,
                32, 91, 93, 32, 123, 91]
golden:        [73, 110, 116, 101, 114, 102, 97, 99, 101, 46, 49,
                10, 91, 93, 10, 123, 10, 32, 32, 91]
```

The structural output ended at the final closing delimiter; the reviewed
golden also carries a final newline. Nested golden sections require differing
newline and indentation spellings as depth changes.

This difference follows the current shared contract rather than a random
renderer choice. `structural-codec` rendering policy names one canonical
whitespace trigger per discovery context, and the Standard whitespace
trigger's canonical spelling is the single byte `0x20` (`" "`). Product and
repetition rendering join their members with that canonical spelling. The
current contract has no encoded choice for the fixture's newlines, indentation,
or final newline.

The diagnostic patch was reverted immediately. The reviewed fixtures were not
edited, retained source was not presented as structural emission, and no
canonical one-line output was silently accepted in their place.

## 4. Current state and downstream epic map

`core-ethos` is clean at the landed head
`70e3b7fdc536543e64f5fe2b232eab3c0d988910`. Bead `primary-vq6.1` was
reopened and is blocked with the audit and writer evidence. No later Protos MVP
epic bead began: in particular, neither `primary-vq6.2` nor
`primary-vq6.3` was claimed or modified.

The epic map currently covers 12 child beads, with the universal-trait-home and
rename-scope decisions already closed. Its remaining implementation surfaces
are known downstream gates, not causes of the present stop:

- `primary-vq6.2` carries trait and struct vocabulary through Logos to compiling
  Rust and is directly blocked by Slice 1.
- `primary-vq6.3` formalizes the offline `.ethos`-to-`.rs` generator after that
  vocabulary path exists.
- Interface emission, Stream semantics, Sema storage, Spirit production
  integration, Mind generation, orchestrator/messenger contract conversion,
  and the remaining daemon/service renames are mapped in later epic children.

Those downstream witnesses and their dependency ordering remain necessary for
the MVP. None resolves the current disagreement between the byte-identical
fixture authority and the shared writer's canonical-text authority.

## 5. Ranked question for the psyche

1. **Which authority must change—the byte-identical fixture re-emission
   acceptance and golden formatting, or the shared writer's
   canonical-whitespace contract—so encoded `WholeEthos` can truthfully
   re-emit?** The first authority surface is the reviewed fixture text together
   with Slice 1's byte-identical acceptance criterion. The second is
   `structural-codec`'s table-owned canonical rendering contract, under which a
   context selects one canonical whitespace spelling and currently cannot
   encode depth-sensitive indentation or a final newline. A ruling must identify
   which surface governs the required textual identity before Slice 1 can be
   remediated and independently accepted.

## 6. Superseding ruling and resumed remediation

The authority conflict and ranked question in sections 4–5 are superseded by
the direct psyche ruling seated in
[`design/ProtosEngine/encodedMeaningRoundTrip-2026-08-02.md`](/home/li/primary/design/ProtosEngine/encodedMeaningRoundTrip-2026-08-02.md).
Encoded meaning is authoritative: textual emission is correct when reparsing it
produces the same encoded value. Presentation whitespace is not identity; text
that is actual encoded content remains meaningful.

The byte evidence in section 3 remains as historical evidence that the shared
writer canonicalizes layout and that the original test witnessed source
retention. It is no longer blocker evidence. The agent-authored byte-identical
handoff wording was not psyche authority and has been replaced with the semantic
decode → canonical shared-writer emission → decode criterion. Remediation of the
independent public-invariant defects resumed under that criterion; later epic
work remained unstarted while Slice 1 was corrected.

Remediation then completed in `core-ethos` version `0.25.0` at pushed `main`
head `83feebbd34b66d493a0a3c7ffea68dab1dd7873c`. The codec now reflects
typed `WholeEthos` and typed source-only imports into a fresh checked structural
value, emits only the shared writer's canonical text, and proves canonical
reparse equality for all three untouched goldens, including identical
`WholeEthos` archive bytes. Public construction, serialization, and archive
restoration enforce the audited version, kind, identity, visibility, and grammar
cardinality invariants. The final Cargo suite passed 23 tests; the focused
Spirit suite passed 7/7; the focused invariant suite passed 2/2; check,
formatting, warning-denied Clippy and rustdoc, Nix evaluation, and all eight full
flake checks passed. `primary-vq6.1` is closed with that proof. No later epic
bead began during the remediation.

## 7. Slice 2 landing

Slice 2 landed producer-first across the current structural train:

- `core-logos` `0.22.0` at `bd5155f51ee5301b78cd8b3c070a98e2267e7477`;
- `rust-logos` `0.22.0` at `14491e0cc2e34799b771573f1eeeaaf44a616405`;
- `core-nomos` `0.33.0` at `e5dfc0577f7b5f69b9b1b55ecca410f5f771b8fd`;
- `language-engine-witness` `0.17.0` at
  `7cd47d4d65bb1db1ee6b90accc713aeeb43acd26`.

The train carries typed structs, trait definitions, trait implementations, and
associated-type bindings through WholeLogos and Rust emission. Nexus projects
traits before types and emits plain Rust. Interface shared types project with
the ruled rkyv wire attributes. The untouched Nexus golden emits its two traits
and two decision enums and compiles in the witness scratch crate.

The producer and witness Cargo suites, warning-denied Clippy, rustdoc, and
formatting gates passed. Each of `core-logos`, `rust-logos`, and `core-nomos`
exposes five x86_64-linux flake checks and completed its full bounded Nix gate;
the Slice 2 witness was likewise green. `primary-vq6.2` is closed with that
proof.

## 8. Slice 3 landing

Slice 3 added the file-kind-neutral type-declaration projection in `core-nomos`
`0.34.0` at `f1f6ca55fbc69afec135b385ed758725f4c2696a`, then landed
`nomos-engine` `0.7.0` at
`f95b38c6805a031fbf7adad78234349d784d9845`. The engine now exposes a
socket-free library API and `nomos-generate` binary. The caller supplies all
translator-issued names and structural identities; the generator performs no
identity allocation. Its daemon continues on its existing coherent dependency
train and behavior, isolated from the current batch dependencies by explicit
crate aliases.

Nexus projection is complete for the Slice 2 vocabulary. Interface emits wire
declarations while returning typed deferred values for its three input
memberships, three output memberships, two refusal semantics, and two Stream
applications. Sema emits six plain record declarations while returning its
three typed tables as deferred. Stable outcome receipts therefore report
deferred counts `10`, `0`, and `3` for Interface, Nexus, and Sema respectively.

`language-engine-witness` `0.18.0` landed at
`88df6a67d917d0619689b78c25247a791ddd693b`. Its build script calls the library
directly; its process witness calls the installed CLI for all three byte-exact
copies of the reviewed fixtures; and only the Nexus `.rs` artifact is compiled.
Its dedicated Nix derivation independently calls the installed generator on all
three fixtures.

Final bounded evidence:

- `core-nomos` enumerates 112 Cargo tests and its five flake checks pass.
- `nomos-engine` enumerates 20 Cargo tests; 19 pass and the one-shot freeze
  generator remains deliberately ignored. Its five flake checks pass.
- `language-engine-witness` enumerates 15 Cargo tests and all pass inside its
  full process environment. Its seven flake checks pass, including
  `offline-generator` and the process test.
- All three witness fixture files compare byte-for-byte with
  `reports/spiritEthosFixtures/`.
- Typed `UnknownFileKind` and `UnsupportedVersion` refusals are matched through
  the library; the CLI exits unsuccessfully and writes no artifacts for the
  unknown-kind case.

The failures encountered during implementation were integration gates and were
fixed before landing: a direct current-core upgrade initially split the daemon
across incompatible dependency versions, so the batch train was isolated by
aliases; warning-denied Clippy rejected an explicit test counter; and Nix could
not evaluate new fixture paths until they existed in a local commit. No fixture
text or acceptance boundary was weakened.

`[assumption] None`: no provisional semantic choice remains in Slices 1–3.
Interface membership/refusal behavior, Stream semantics, and Sema tables/storage
are explicitly deferred to Slices 5, 6, and 7 rather than assumed. No ranked
psyche question remains because no unresolved gate was hit. Beads
`primary-vq6.1`, `primary-vq6.2`, and `primary-vq6.3` are closed with the proof
above.
