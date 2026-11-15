# Producer60609 wire fixtures

Owner: Mind curriculum Sol, flow e2487d. Answers FlowNexus question6oa9. No live service, configuration, generated skills, main ref or running-system state was changed. All service/source state was isolated in `/tmp/producer60609-e2487d.a0vRMA` and the service exited after capture.

## Immutable producer

Producer: `60609c55f90432782625275294636a4e396d9497`, ordinary contract `8e63176cb1c0f1429a9797412391b4035a25cc68` (0.2.0). Remote evaluation of that exact published producer's `checks.x86_64-linux.curriculum.outPath` gave `/nix/store/pnwp8n25jv263kxxjvi3mi2lg648fgd5-check-curriculum`; its derivation records test build `/nix/store/v4kg8pnh5q2cx44fdfj68kbx2162iik4-rust_curriculum-0.2.0-test`, whose bin symlinks target `/nix/store/scr8as10g333ym5jvbf8lr8fbj06l9zd-rust_curriculum-0.2.0-bin/bin/{curriculum,curriculum-nexus}`. Derivation and remote flake metadata are retained as `check.drv.json` and `producer-flake-metadata.json` in the capture directory. This records output selection and capture, not a new full gate execution. Core later confirmed the retained accepted full gate receipt at `flows/aa68be/producer-review.md`, log `/tmp/curriculum-aa68be-gate.5Emuey/gate.log`, exit file `exit` equal0. This is the resident datom-enabled CHECK dependency, not the exported plain-feature runtime package. The plain package `/nix/store/v2cajsasnzvyhc6saawj25fwj81hyrn6-rust_curriculum-0.2.0-bin` was reported unrealized. These fixture captures prove the exact compiled check CLI/service wire and behavior; they do not establish exported runtime-package readiness or live deployment acceptance.

Both executables were copied byte-for-byte from that builder output to scratch `bin/`, then used unchanged. Remote and local SHA-256 agree: CLI `ae79297fa8aaedd9d854dd7c512991562ca1ad2fe41c0bfcaad121901afa11a3`; Nexus `32bdd3a0e73403a4549d7f32a091d136f3867cfc11581b1ab6d8fa874d6b0472`. An ordinary Nix copy was refused for an unsigned path; a root SSH copy lacked a builder key. Neither installed anything. SCP copies of the exact executables executed against already-present runtime libraries.

## Captured protocol

`capture.py` starts only that Nexus with isolated runtime, records and three source repositories. A no-effect refresh executable is explicitly configured. No roles file is configured. Inotify socket creation announces readiness. A Unix socket relay receives each own-CLI request, saves its unmodified raw archive, forwards its original big-endian u32 length plus bytes, saves the unmodified service answer archive, and returns the original answer frame to the same CLI. Thus both directions are producer-generated, not newly serialized by consumer code. Matching `.frame` files include the four-byte wire length; `.rkyv` files exclude it.

The four requested local raw archive paths are:

```
/tmp/producer60609-e2487d.a0vRMA/missing-module.query.rkyv
/tmp/producer60609-e2487d.a0vRMA/missing-module.answer.rkyv
/tmp/producer60609-e2487d.a0vRMA/startup-composed.query.rkyv
/tmp/producer60609-e2487d.a0vRMA/startup-composed.answer.rkyv
```

All exact sizes and SHA-256 digests are in `archives.json`. The main query/answer sizes are 102/108 and 102/1221 bytes. Full query text, CLI stdout/stderr and exit statuses are the matching `.query.datom`, `.stdout`, `.stderr`, `.exit`. `verification.txt` records the independent frame-size/payload and clean-source checks. Initial startup failed only because a deliberately absent roles path was configured; removing that optional setting produced the captures. No failed-run archive is presented.

## Exact selections and bodies

The Ethos is `signal-curriculum-nexus` at the immutable contract above, `ethos/signal.ethos`: `ComposeStartup.StartupSelection`; `StartupSelection.{ CallerMetaflow Target SystemModules UserModules Vector<FlowId> }`; each module identity is `{ ModuleKind ModuleSubject Versions }`, where `Versions.[ Single.Version Span.{ First.Version Last.Version } ]`.

Negative datom:

```datom
ComposeStartup.{ { Mind core Sol } Codex [ { Spirit core Single.0 } { Intent absent Single.0 } ] [] [] }
```

The answer is Rejected with reason exactly `missing module intent:absent:0`; the own CLI exits1 and writes this reason plus LF to stderr.

Positive datom:

```datom
ComposeStartup.{ { Mind core Sol } Codex [ { Spirit core Single.0 } { Intent energy Single.0 } ] [] [] }
```

Source files have no frontmatter and no trailing LF. `spirit/core/0.md` contains exactly `SPIRIT_BODY`; `intent/energy/0.md` contains exactly `INTENT_BODY`. User and records text are empty. The system payload SHA-256 is `26b1811fa4fab2aa64c2c9b7309cdb0a9351897f9cf5c88994068c980cbe1a6f`; empty user/records hash is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Actual provenance

The sources are real clean Git repositories, not invented HEAD files. Psyche fixture HEAD is `74279bd7868e77ca2ba0f1cf886ffeef31d62ea5`; mind and field fixture HEADs are `0412944e349e07c78e58926b8f198679020106cf`. Their exact source trees and histories are preserved in `psyche-belief.bundle`, `mind-belief.bundle`, `field-belief.bundle`; `revisions.json` records the heads. These are isolated synthetic fixtures, not production authored-module snapshots. Reproduction with identical provenance must retain these fixture heads, not create fresh commits.

The positive answer has two provenance entries, repository `psyche-belief` and the Psyche head above, placements System0 and System1 respectively. Paths are `spirit/core/0.md` and `intent/energy/0.md`. Source/body/rendered hashes each coincide for these untemplated, unframed bodies: core `c2bd27aa351090bbd9c1ca61b20764545c0cc12fa1a9cb5ee05c1d48bcf98ead`; energy `1d62ee8fdb041ae6d82fcb652edb2e7e980137fda0bc5d2c9265fd3afbb0d070`. `startup-composed.stdout` is the complete own-CLI decoded oracle, including every rendered byte and provenance position.

## Binding1 and inclusive span

Optional additional raw query/answer pairs are `binding1-singleton.{query,answer}.rkyv` and `binding0-1-span.{query,answer}.rkyv` in the same directory. Their exact datoms and decoded observations accompany them.

Selecting `{ Spirit binding Single.1 }` plus Intent energy0 returns actual provenance in order: binding Single1 at System0, binding Span0-1 at System1, energy Single0 at System2. The producer's binding expansion includes the spanning module; it must not be reduced to the selection's singleton identity. Selecting binding Span0-1 directly plus energy0 returns span at System0 and energy at System1. Both are successful own-CLI compositions.

Binding sources are `spirit/binding/1.md` with exact no-LF body `BINDING_SINGLE_BODY`, hash `46a2491605ccdef28dc36c1a78aca1c78f22e2ec3fc6f46dcb8de17454f8fb32`, and `spirit/binding/0-1.md` with exact no-LF body `BINDING_SPAN_BODY`, hash `0720d47407f8841444b7e50885e431c9c19b47a09dd4abf7a74ec608afb44a60`. Both carry the same actual Psyche fixture revision. Complete returned bodies/hashes/provenance are frozen in the matching stdout files.

## Consumer receipt

FlowNexus Sol explicitly accepted these selections/bodies in result hqyp and reported copying all four main archives plus binding1 and exact-span captures, decoded oracle outputs, hashes and source revisions into Flow unit fixtures. Its owner retains full immutable Flow gate responsibility; this capture report does not claim that gate.

## Plain-runtime review, pc2p

Source at exact60609 disproves readiness of its exported plain-feature runtime: `Cargo.toml` defaults to no features; `flake.nix` enables datom only in memberChecks. `src/registry.rs`'s non-datom `read_declarations` always returns `source declarations require the datom package feature`. `src/service.rs` requires a successful source read both at Memory open and on each operation. Thus plain Nexus cannot admit these manifests or successfully serve Modules/ModulesVerbose. Datom-enabled check captures do not discharge that boundary.

Retained authority is `flows/299aa3/reports/nyq8-custody.md`: Psyche inea/d67y holds shared-configurator separation under primary-q8li, preserves the deployed datom-enabled package, and requires a new order for separation. `flows/4c69d7/continuation-detail.md:27` corroborates the hold. No embedded producer is evidenced: read-only Flow candidate inspection at d091b11ee7f045aecd6854cc859d5fb003deaaa3 finds `context.rs` using the external Curriculum Unix socket and a contract-only dependency, not an embedded Curriculum library. An explicitly packaged datom-enabled interim producer or an authorized configurator solution remains a deployment dependency; producer60609's current exports alone supply neither. These conclusions were returned to Core in Result pc2p; no source change was requested or made.
