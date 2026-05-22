# Spirit master-upgrade smoke test against deployed redb (2026-05-21)

## What was tested

The hypothesis: a purely-additive but variant-position-inserting schema
change to persona-spirit is wire-compatible for unaffected variants and
storage-compatible end-to-end. The master HEAD differs from the deployed
build by exactly one commit (`spirit: add topic catalog observation`, change
`kklxtowxkmks`) which inserts:

- `Topics` into the `Observation` enum mid-position (between `Records` and
  `State`), shifting rkyv discriminants for variants past position 1
- `TopicsObserved` into the `Reply` enum (between `RecordProvenancesObserved`
  and `QuestionsObserved`), shifting reply variants past position 4
- a `ReadTopics` `Command` and a `RecordStore::observe_topics()` actor path

The test exercises master daemon + master CLI against an existing redb file
written by the deployed daemon. It does not test cross-version wire
compatibility (master daemon vs deployed CLI, or vice versa) — that is a
separate axis.

## Setup

Deployed daemon: `/nix/store/w4bc190shb229kw1k8aash8dyzvb40x3-persona-spirit-daemon`
running at PID 4065334 on sockets under
`/home/li/.local/state/persona-spirit/`. Storage:
`persona-spirit.redb` (192512 bytes, 42 existing records). Left running
untouched throughout.

Master binaries (already built, supplied by psyche):

- daemon `/nix/store/mygavgnxadbm2nif8rkmkgc4721p0bsy-persona-spirit-daemon`
- CLI `/nix/store/0n95fwqchm8dqzxhnhzpjl6g9776rm7c-spirit`

Test scratch: `/tmp/spirit-test/`. The deployed redb was copied with `cp`
while the deployed daemon held it read-write; the copy succeeded with
`exit=0` and matched the source byte count (192512). This is consistent with
redb's MVCC-shaped on-disk layout: a hot-copy from a quiescent moment lands
a consistent snapshot view.

The master daemon was launched on test sockets `ord.sock` / `own.sock` with
the single positional NOTA argument
`("/tmp/spirit-test/ord.sock" "/tmp/spirit-test/own.sock" "/tmp/spirit-test/persona-spirit.redb" 384 None)`
(socket permissions 0o600, no bootstrap policy file). Daemon bound cleanly
within 3 seconds; `daemon.log` stayed empty.

## Results

### Test 1 — `(Observe (Records (None None SummaryOnly)))`

Exit 0. Master daemon decoded every one of the 42 existing records written
by the deployed daemon and replied with a well-formed `RecordsObserved`
list. Sample first entries:

```
(RecordsObserved ([(1 component-shape Principle "CLIs are thin Signal clients" Maximum)
                   (2 persona Correction "Spirit clients do not provide capture time" Maximum)
                   ...
                   (42 signal Principle "The workspace's Rust subset has no tuples..." Maximum)]))
```

No truncation, no decode error, no panic. Storage compatibility holds.

### Test 2 — `(Record (test Decision "master upgrade smoke test" "from designer/265" Maximum "test verbatim"))`

Exit 0. Reply:

```
(RecordAccepted ((43 test Decision "master upgrade smoke test" Maximum)))
```

Master daemon allocated id 43 and accepted the write into the
deployed-written redb without complaint. The token-cheap accept-reply shape
from intent records 14/17/18 is honoured.

### Test 3 — `(Observe Topics)`

Exit 0. Reply:

```
(TopicsObserved ([(component-shape 4) (nota 7) (persona 4) (signal 8) (spirit 15) (test 1) (workspace 4)]))
```

Topic counts sum to 43, matching the post-write record count. The new
`test` topic from Test 2 shows count 1; existing topics (`component-shape`,
`nota`, `persona`, `signal`, `spirit`, `workspace`) carry their
deployed-daemon-written counts. The new operation runs cleanly against the
mixed corpus of deployed-written and master-written rows.

### Teardown verification

`kill -TERM 4121907` ended the test daemon on the first signal; deployed
daemon at PID 4065334 still running. A query against the deployed socket
via the master CLI returned the same 42-record corpus (the deployed daemon
has not seen the +1 from the test copy, as expected). Scratch directory
`/tmp/spirit-test/` removed; `ls` confirms gone. Only PID 4065334 remains
in `pgrep -af persona-spirit-daemon`.

## Interpretation

The result validates the rkyv-headroom Principle recorded as intent record
30 in the deployed Spirit DB (paraphrased: small-variant enum discriminants
fit in a byte with headroom; variant additions are zero-cost wire-compatible
provided variant order is preserved). The master `Observation` enum gains
a new variant; existing variant positions before the insertion (only
`Records` at position 0) are unaffected, and the rkyv-encoded payloads on
disk decode cleanly under the new schema.

The test however does not refute the schema-migration concern raised in
intent record 10. It demonstrates the easy case — additive change with
position preservation for the *stored* payload type (`Entry` struct,
unchanged across the two commits). The hard case is when a payload
struct gains a field or an enum variant order is reordered: those changes
require either rkyv-layer headroom (struct trailing-padding, declared
discriminator width) or an explicit migration path. The schema-migration
discipline in `reports/designer/260` and the schema specification
language design in `reports/designer/263` remain the right place to
encode that broader case.

What this test *does* establish:

- The deployed redb file format and the master daemon's storage code agree
  on the `Entry` shape.
- An additive `Observation` variant insertion that keeps position 0
  (`Records`) stable is safe for clients that only use positions before the
  insertion.
- The `ReadTopics` command is wired through dispatch → store → reply
  correctly, and its read path uses `SemaReader` without touching the write
  plane (matches the architecture table addition in the commit).

## Observations on variant insertion specifically

The commit inserts `Topics` at position 1 of `Observation` and
`TopicsObserved` at position 4 of `Reply`. For the deployed CLI talking to
the master daemon, this matters: any deployed CLI sending the rkyv
discriminant for `Observation::State` (now at position 2 in master) would
have its byte interpreted by the master daemon as `Topics`, causing either
a wrong-operation execution or a decode failure depending on payload shape.
For variants past position 4 in the `Reply` enum (e.g.,
`QuestionsObserved`, subscription replies, `RequestUnimplemented`), the
discriminant byte produced by a master daemon would be misread by a
deployed CLI as the variant one slot earlier. This is the wire-break case
the test deliberately does not exercise (master daemon + master CLI sees
matched discriminants on both ends).

Practically: deployed CLIs in flight will break against an upgraded daemon
on any operation past variant position 0 of `Observation`, until they are
also upgraded. This is the kind of break that the rkyv-headroom Principle
does *not* protect against — the headroom argument requires that variants
be *appended* at the end, never inserted mid-position. The commit chose
mid-insertion (presumably for readability of the source ordering) and
accepted the wire-break for affected variants; the test confirms only that
master-vs-master is healthy.

A follow-up discipline question for intent capture: should the
schema-layout schema (intent record 29) explicitly forbid mid-variant
insertion, or should the content-addressable diff step recognise it as a
breaking change and require an explicit acknowledgement?

## Recommended next step — Nix flake pipeline sketch

The psyche described automating this test as a Nix derivation. The shape
would be a flake check (`checks.<system>.spirit-upgrade-compat`) producing
a derivation whose `buildPhase` does, roughly:

1. Take three flake inputs: `persona-spirit-deployed` (pinned to the
   running-production commit, sourced from the CriomOS Home flake), and
   `persona-spirit-master` (defaulting to `self`, the local working
   commit). Optionally a third `persona-spirit-testing` for staged
   pre-deploy verification (matches intent record 41's "named variants
   like unstable and testing").
2. In a sandboxed `runCommand`: launch the deployed daemon on
   ephemeral Unix sockets under `$TMPDIR/deployed/`, run the deployed CLI
   to seed a known fixture set of records (small, deterministic — e.g.,
   one of each topic/kind/certainty combination), then `SIGTERM` the
   deployed daemon.
3. Copy the resulting `.redb` to `$TMPDIR/master/`. Launch the master
   daemon on a second pair of ephemeral sockets pointed at the copied
   storage.
4. Run a fixed query battery through the master CLI: read-all-records,
   per-topic filters, the new `Observe Topics`, a `Record` write, and a
   re-read after write. Compare the read output to expected golden NOTA
   strings stored under `tests/upgrade-compat/golden/`.
5. SIGTERM the master daemon and assert the storage file is still
   readable by a second master-daemon restart (catches half-written or
   corrupt-on-shutdown states).

The derivation is commit-first by construction (per intent record 41 —
Nix sees only committed state). The flake check runs the whole pipeline
in `nix flake check`; CI gates merge to main on its success.

Optional extension: parametrise over the cartesian product of
`{deployed, master}` daemon × `{deployed, master}` CLI to exercise the
wire-compatibility axis explicitly, with assertions about which
combinations are expected to break on which variants. That gives the
schema-layout-diff machinery (intent record 29) something concrete to
test against once it lands.

The fixture-seeding step is the substantive design work — the seed must
exercise every variant position the wire contract distinguishes, so that
a future variant insertion or reorder triggers a golden-file diff rather
than silently passing.
