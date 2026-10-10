# Flow Nexus contract, candidate

The Flow Nexus's Ethos files and acceptance tests, from
`flows/f5a6e9/reports/flow-buildable-design.md` at
revision e17a62ca. Read with ethos-zero 16.0.0 at
b2fa8b0e.

## Files

| file | what it is |
|---|---|
| `ethos/flow.library.ethos` | Library: the types both Signals and Memory share (FlowId, Topic, Blake3, Layer, Subaspect, Source, Said, Request, Address, Metaflow, Lock, Process, Sender) |
| `ethos/flow.memory.ethos` | Memory: the Metaflow, Lock, Flow, Module, Model and Threshold records |
| `ethos/flow.signal.ethos` | Signal, the flow socket: Launch, Wake, Refresh, End, Current, Lock, Identify, Deliver, Release and their responses |
| `ethos/flow.meta.signal.ethos` | Signal, the meta socket: Configure, Forget, Bind |
| `ethos/forms.signal.ethos` | Signal holding Message's simple form Send (to an Address or Up) and extended form Deliver as types of their own |
| `tests/fixtures/signal-flow.library.ethos` | test stand-in for signal-flow's Event as the design states it |
| `tests/fixtures/curriculum.library.ethos` | test stand-in for curriculum's Name |
| `tests/acceptance.rs` | the acceptance tests |
| `src/lib.rs` | the test crate: mounts the generated Rust and is `flow_ethos`, `curriculum` and `signal_flow` to it |
| `Cargo.toml`, `Cargo.lock` | the test crate's manifest and lock |
| `flake.nix`, `flake.lock` | Check and the tests as Nix derivations |

The files are the design's ethos text, with these
differences. Two designed types are carried as String,
each with a comment naming the designed type: `Topic.String` for
`Topic:Name`, `Blake3.String` for `Blake3.Bytes<32>`. The meta socket imports `Path`,
which its `NoSource.Path` refusal names; without it
Check answers `Undeclared.Path`.

## Tests

`every_root_crosses_the_wire` (with and without the
`datom` feature): a value of the Library, both Signals'
queries and responses, both forms and every Memory
record archives with rkyv and restores equal.

With `datom`, each datom section 1 of the design writes
reads against its type, prints, and reads back equal:

- `the_written_request_vector_reads_oldest_first_waking_last`
- `the_written_psyche_metaflow_reads`
- `the_written_mind_metaflow_reads`
- `a_psyche_request_carries_context_and_verbatim`
- `the_written_configure_module_payload_reads`
- `the_written_launch_reads`
- `every_memory_record_reads_and_prints`
- `a_written_send_reads_with_up_and_with_an_address`

Memory lists the Library's Metaflow and Lock as records
in the form `Metaflow.flow_ethos:Metaflow`: an alias
whose target is imported inline. ethos-zero refuses a
bare imported name in a record section
(`Expected.Declaration`).

## Running

Everything runs through Nix on the remote builder; the
generated Rust is written to `src/generated` inside the
build, never into this tree. From a copy of this
directory on the builder:

```sh
nix build path:$PWD#check-report -L
nix build path:$PWD#checks.x86_64-linux.test -L
nix build path:$PWD#checks.x86_64-linux.test-datom -L
nix flake check path:$PWD -L
```

`check-report` runs `ethos-zero 'Check.<file>'` on
every file under `ethos/` and prints each reply as
ethos-zero prints it; it always builds. `ethos-check`
fails when any reply is `Rejected`. `test` and
`test-datom` generate the Rust and run `cargo test
--no-fail-fast`, the second with `--features datom`;
the test output is in `nix log` of the derivation.
