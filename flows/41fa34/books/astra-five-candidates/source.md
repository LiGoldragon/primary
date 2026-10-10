# Five candidate systems

## Codex generations

The generation design keeps each installed Codex package,
home, socket, and service recipe behind one immutable identity.
Old sessions stay pinned while later launches reserve the
selected generation through a proposed controller transaction.

```text
Stage → Check → Select current → Reserve launch
                                  ↓
                          bind or cancel
```

Retirement remains unfinished: attached-client evidence is
missing, and shared credential lineage prevents safe overlap.
The controller, slot names, and Flow reservation fields are
proposed contracts, not an adopted deployment or migration.

## Clojure Flow and topics

The offline Babashka Flow prototype has its own EDN file.  It
uses exact Metaflow names and records aspect, topic, layer, and
an ordered Flow-ID chain; an omitted topic becomes `Core`.
Eleven tests with 21 assertions cover its small candidate API.

The separate topic registry has 9 tests with 39 assertions,
plus 2 focused tests with 8 assertions.  Both candidates now
preserve exactly one EDN form and use competing-process locks.
Its PascalCase check is provisional: it is not an English-rule
contract.  Neither candidate connects to Flow, a harness, or
production state.

## Clojure build and format bridge

Five-run medians were 5.400 s for equal timestamps, 0.560 s
for class-later entries, and 2.023 s with matching sources
stripped.  The fixture distinguishes observed runtime
compilation from jar class loading.  A staging-permission fix
and Clojure jar normalizer are proposals; cache reuse is not an
independent reproducibility result.

The bridge is a five-test Ethos-generated Rust fixture.  It
maps proposed exact JSON variant tags through checked generated
types and pinned Datom text.  It adds no generic adapter,
Clojure adapter, wire contract, or production dependency.

## Audit appendix

The audit proposes an offline path:

```text
export → validate → explicit map → import → read back
```

Adapters, validators, and importers are absent.  No live store
was opened or changed.  Metaflow names and ancestry must come
from reviewed mappings; they cannot be inferred from existing
Flow or Messenger records.
