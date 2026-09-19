# Operational: Nix-built tests and separate Rust from data

## make sure all the testing uses nix built binaries and scripts that way its all built on the remote builders and offloads my laptop from building anything. create rust-only repos for rust to avoid rebuilds; separate data.

## im going to watch mmovies now so dont overload the laptop cpu or ram

Context: spoken by the living in the current primary conversation on
2026-09-18. The first statement directs the operating shape for testing and
repository boundaries: Nix-built test binaries and scripts, remote-builder
compilation, and Rust source separated from data so data changes do not force
Rust rebuilds. The second statement is a temporary resource constraint while
the living watches movies. It requires lightweight local work now and defers
memory-heavy Nix evaluation, generation, and test builds; it does not create a
permanent ban on local test execution.

> make sure all the testing uses nix built binaries and scripts that way its all built on the remote builders and offloads my laptop from building anything. create rust-only repos for rust to avoid rebuilds; separate data.
>
> im going to watch mmovies now so dont overload the laptop cpu or ram

-- living, current primary conversation, 2026-09-18.

Agent interpretation: Nix invocation alone is not proof that compilation was
offloaded; retain remote-builder evidence. Do not silently fall back to raw
local compilation or rebuilds. The immediate implementation is limited to the
authored rule and raw record; consumer generation and validation are deferred
until the temporary resource constraint is lifted.
