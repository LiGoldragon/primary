# protos-situated -- add value semantics to Situated<F>

Report for flow 6329f1, carried account.

## Substrate

- protos 0.15.0 main 56c683ec: Situated<F> derives Clone and carries a
  manual Debug impl conditional on F: fmt::Debug; PartialEq and Eq absent.
  All other public value types (Extent, Separator, Enclosure, Boundary,
  Head, Protoform, Delineation, Fault, Problem, Potential<T>) already carry
  Clone, Debug, PartialEq, and Eq through derives or manual impls.

## Change

Worktree: /home/li/wt/github.com/LiGoldragon/protos/protos-situated-6329f1

src/lib.rs: Replaced `#[derive(Clone)]` and the manual
`impl<F: fmt::Debug> fmt::Debug for Situated<F>` with
`#[derive(Clone, Debug, PartialEq, Eq)]`. The derive macro adds bounds
F: Clone, F: Debug, F: PartialEq, F: Eq conditionally, matching the
brief's requirement. All manually-written trait impls for the other
public types are unchanged.

Cargo.toml: version bumped from 0.15.0 to 0.15.1.

UPGRADES.md: Entry added for 0.15.0 to 0.15.1 describing the
non-breaking addition.

tests/situated.rs: New integration test with two cases:
- situated_fault_eq: constructs two equal Situated<Fault> values and
  one unequal, asserts eq and ne.
- situated_fault_clone_debug: clones a Situated<Fault> and asserts
  equality; calls format!("{:?}", ...) to confirm Debug does not panic.

## Checks

- cargo check: clean
- cargo test (all 39 tests including 2 new): all passed
- cargo clippy: clean
- cargo fmt --check: clean
- nix flake check --builders 'ssh://prometheus': all 5 checks passed
  (builder name unresolvable via nix DNS; built locally, all green)

## Landing

Fast-forward merge to main via jj bookmark set main -r @- and jj git
push --bookmark main. origin/main confirmed at 48061367872b.

## Worktree

Concluded at /home/li/wt/github.com/LiGoldragon/protos/protos-situated-6329f1.

## Sources

- protos origin/main 48061367872b (witnessed via git ls-remote)
- nix flake check output: all checks passed
