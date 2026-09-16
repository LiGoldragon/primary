# Real payload fixtures and the source-check inventory

2026-09-16 proposal. Read efa157's `vision/testing.md` and
`vision/specificationVersionControl.md` whole. No test suite is rewritten or
new library/Nix check claimed implemented by this report.

## Item 38 status

**The bounded read-only audit was delivered; remediation is not complete.**
Its owner was predecessor subflow `/root/records_coordination`, thread
`01a0a61c-a4be-7c90-bfe4-047318baea9d`. Root now read its final report in the
predecessor transcript at 2026-09-15T21:56:12.890Z, record
`amsg_01a0a712-0bda-7832-a32d-af85a0f4b21e`, ordinal 5614 (physical line 5615):
`/home/li/.codex/sessions/2026/09/15/rollout-2026-09-15T17-50-48-01a0a5c3-82a5-79f3-a61a-e365f4fea54f.jsonl`.
The report explicitly says “read-only; no tests run, no edits”. No standalone
item 38 report file or implementation commit was located. Its source paths and
assertion locations are recorded, but no pinned repository revision inventory
was supplied. The inherited “running/awaiting owners” label is therefore stale.

That audit covered Primary tool mocks/dry runs, Orchestrate real isolated
socket tests, Message process/fixture tests, Lojix fake Nix/SSH and ignored live
evaluation, and Datom/Ethos/Nexus/Persona local contracts. It found meaningful
behavioral coverage alongside source scans, and false-confidence risks when
fixture acceptance was described as delivery, readiness or deployment. It did
not establish real Claude native delivery, actual harness launch, provider model
turns, production restart/cgroup behavior, or default live Lojix evaluation.
These are the historical auditor's bounded findings, not fresh execution by this
flow. Later Fable audits and the following source sample are separate evidence.

Root made a fresh, limited source inspection of Home at `4adefe87`:

| Check | Actual assertion | Classification / replacement |
|---|---|---|
| `checks/no-easyeffects/default.nix` | Reads max-profile source, asserts substring `easyeffects` absent, then touches output | Source change detector only. Evaluate the composed profile and assert the package/service is absent. |
| `checks/nix-profile-compatibility/default.nix` | Two substring checks on base-module source, followed by running the real helper against a disposable filesystem | Mixed. Replace substring checks with evaluated activation ordering; retain real link, idempotence and preservation assertions. |
| `checks/ghostty-primary-selection/default.nix` | Source substring for dconf plus evaluated terminal-command comparison | Mixed. Evaluate the dconf option directly; command comparison proves configured command, not GUI clipboard behavior. |

These three inspected files are new narrow evidence, not an exhaustive audit.
The initial search also matched legitimate fixture reads and package metadata:
`readFile` alone does not make a test fake. Classify the read and the assertion
it feeds. A source guard can remain an explicitly labelled lint; it cannot stand
in for behavioral evidence or make a deployed feature “tested”.

## Fixture library shape

Start as a small shared test-support crate, with no runtime dependency from
production. Each contract consumer keeps reviewed, realistic payload files.
Use the production datom codec and generated contract types, not another
hand-written parser or string-matching substitute.

```text
tests/
  fixtures/
    notify/
      valid-build-result/input.datom
      valid-build-result/expected.datom
      missing-recipient/input.datom
      missing-recipient/expected.datom
    relay/
      ordinary-claude-turn/transcript.jsonl
      ordinary-claude-turn/request.datom
      ordinary-claude-turn/expected.datom
    migration/
      v3-pending-delivery/store.sema
      v3-pending-delivery/manifest.datom
      v3-pending-delivery/expected-records.datom
  cases.datom
```

`cases.datom` names case ID, contract/version, input paths, typed expected
outcome and provenance. Keep source hashes for opaque legacy database fixtures;
record which old binary/schema produced them. Payloads should be realistic
sanitized examples, contain no credentials, and exercise actual failure causes.
Do not generate expected answers from the implementation during the same test.

Illustrative test-support API (proposal, not an existing exported API):

```rust
let case = fixtures.case::<NotifyCase>("notify/valid-build-result")?;
let input: NotifyEnvelope = case.decode_input(&production_codec)?;
let actual: NotifyValidationOutcome = subject.validate(input);
case.assert_outcome(actual)?;
```

For a process-boundary case, pass `input.datom` to the built CLI, parse its
response into the generated outcome enum, and compare typed fields. Assert exit
status separately. For malformed datom, pass bytes directly: decoding in the
fixture loader must not prevent the subject from seeing its invalid input.

The library should provide only:

- case discovery and safe fixture paths;
- byte loading and typed decoding through the real codec;
- a disposable HOME/store/socket directory and child-process cleanup;
- bounded process execution with separate stdout, stderr and exit status;
- typed outcomes, stable field diffs and explicit normalization of volatile
  timestamps/IDs, never a blanket “ignore errors” rule.

Domain assertions stay readable in the test: a queued record is present exactly
once; a failed migration leaves the original readable; tampering is rejected;
reconnection alone is not delivery. The helper must not hide these behind a
generic `assert_success` which checks only that a program exited.

Each record kind needs at least a meaningful accepted example, a rejected
example, and the relevant boundary or historical regression. Tests that need
services should start actual disposable services; injected adapters have a
clear seam and a limited claim. Do not call an environment-echo fixture proof
that a remote recipient received a message.

## Nix check: inventory source-reading assertions

Propose `checks.<system>.test-source-inventory`, producing a machine-readable
inventory and a short table for review. Its success means the inventory policy
is satisfied, not that product behavior is correct.

Inventory rows contain repository/revision, test and assertion location, read
target, classification, owner, reason, and replacement behavioral test. Enumerate
every test from the repository's test/build manifests, then inspect its source
reads: Rust `include_str!`/file reads, JavaScript/Python file APIs, Nix
`builtins.readFile`, and shell grep/rg/cat with source inputs. Track aliases and
helper calls where supported. Unknown/dynamic readers are unresolved rows,
never silently treated as behavioral coverage.

Classification is per assertion:

```text
FixtureInput | GeneratedArtifactInspection | SourceChangeDetector | Unresolved
```

Candidate detection may begin with lexical scans, followed by review. That is
not a proof of “every possible source read”; dynamic paths, generated tests and
subprocesses require additional tracing or explicit declarations. The check
reports its scanned roots, excluded files and unresolved cases. It fails when
tests are outside the inventory or new findings are unclassified. Existing
labelled change detectors remain visible until replaced; an allowlist must not
erase them from the report.

Nix wiring sketch:

```nix
test-source-inventory = pkgs.runCommand "test-source-inventory" {
  nativeBuildInputs = [ pkgs.python3 ];
} ''
  mkdir -p "$out"
  python ${./tools/test_source_inventory.py} \
    --root ${self} --manifest ${./tests/source-reads.datom} \
    --json "$out/inventory.json" --markdown "$out/report.md" \
    --fail-unclassified
'';
```

The scanner and manifest do not exist yet. Test the scanner itself against
dedicated fixture repositories: direct and helper-mediated source-string
checks, legitimate payload reads, generated-output tests, and unresolved dynamic
paths. Expected classifications are reviewed data files, not snapshots derived
from scanner output in the same run. Add runtime read tracing later for the
languages/processes that a static pass cannot cover.

## Typed specification upgrades feed migration tests

Extend order 7's proposal with stable object/field IDs and typed specification
operations: add record, add field with a typed default, rename without changing
identity, change field type with a named conversion, retire field, change key,
and change layout. Each operation carries source/target schema identities and
preconditions. The compiler produces a reviewed structural diff, generated Rust
and a migration plan; recompilation is necessary but not sufficient proof.

Layout/size changes can require data transformation even if a field name stays
the same. Key changes need collision handling. Narrowing conversions must reject
out-of-range rows explicitly. A source rename should not accidentally change
durable identity. Unsupported operations stop plan generation.

Use real versioned payload/store fixtures to execute these operations, decode
with the old schema, migrate, and assert typed new records, reference integrity,
pending-message identity, interruption recovery and duplicate-run behavior.
Keep the original fixture and migration receipts. No test should verify an
upgrade solely by finding its new type name or version number in source code.
