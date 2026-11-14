# Adapter envelope consumer ledger

Source proposal: `052-adapter-envelopes.md`. Query receipt: `adapter-envelope-query-results.txt`, command `rg -n "Invocation\\s*\\{|HookConfiguration\\s*\\{|compose_invocation|flow-compose-invocation|flow-meta-compose-invocation|flow-hook" crates nix --glob '*.rs' --glob '*.nix' --glob '*.ethos'`.

## Exact existing constructors and consumers

| Existing location | Actual symbol/call | Intended projection | Specific test |
|---|---|---|---|
| `crates/flow/src/generated/invocation.rs:5-14` | generated `Invocation`, `HookConfiguration` | regenerate with shared `BootstrapTextBudget`; Invocation adds FrameBytes/socket/query; Hook wraps target `OrdinaryClientConfiguration` | generated roundtrip and prefix rejection |
| `crates/flow-meta/src/generated/invocation.rs:5` | generated Meta `Invocation` | add shared budget/frame/socket/query fields | Meta roundtrip |
| `crates/flow/src/main.rs:30-58` | Flow invocation decode | outer BootstrapTextBudget decodes entire Invocation; use FrameBytes | missing/zero/overflow prefix refuses before connect |
| `crates/flow/src/main.rs:160` | `Invocation { query, .. }` projection | preserve Query-only Nexus wire payload | query projection |
| `crates/flow-meta/src/main.rs:39-66,123` | Meta decode and `Invocation { query, .. }` projection | same with MetaSocketPath | Meta frame/readback |
| `crates/flow/src/compose_invocation.rs:8-31` | `main`, currently two raw argv Datoms; `Invocation {` at `:28` | one ComposerInput argument; outer budget parses, target Invocation is textualized output | one-argument shell quoting, distinct outer/target budgets |
| `crates/flow-meta/src/compose_invocation.rs:8-31` | same Meta composer and `Invocation {` `:28` | one ComposerInput | Meta composer tests |
| `crates/flow/tests/compose_invocation.rs:5,22` | raw composer subprocess callers | pass one rendered ComposerInput | exact rendered argument |
| `crates/flow-meta/tests/compose_invocation.rs:5,22` | raw Meta composer subprocess callers | pass one rendered ComposerInput | exact rendered argument |
| `crates/flow/src/hook.rs:47-98` | HookConfiguration Datom decode and native JSON stdin | outer Hook budget; JSON remains existing native parser; build target Invocation from target client config | malformed/empty hook contract and target budget distinction |
| `crates/flow/src/hook.rs:182` | `let invocation = Invocation {` | construct target Invocation with target budget/frame/socket + Query | projection fields |
| `crates/flow/src/hook.rs:243` | test `HookConfiguration` literal | update fixture to nested OrdinaryClientConfiguration | hook fixture |
| `crates/flow/tests/hook_socket.rs:41-56` | actual `flow-hook` subprocess | configured wrapper/argv; native JSON unchanged | rendered hook command, socket, exit/diagnostics |
| `crates/flow-nexus/src/herdr/launch.rs:484-496` | current `HookConfiguration {` constructor | remove Nexus construction; command uses configured Nix wrapper path | actual wrapper process, no Nexus policy duplicate |
| `crates/flow-nexus/src/herdr.rs:193-194` | fallback hook path construction | supported path becomes configured wrapper; no sibling/PATH fallback | configured executable/refusal |
| `crates/flow-nexus/src/herdr.rs:394` | fixture `PathBuf::from("/fixture/bin/flow-hook")` | fixture-only configured wrapper | Herdr fixture |
| `nix/mk-flow-package.nix:89-117,149-200` | Nix package/config emission | emit separate Flow/Meta composer/client/hook budgets; one rendered composer argument; configured hook wrapper with packaged Flow executable | rendered Nix command/socket and package association |
| `crates/flow-nexus/src/herdr.rs:130` | hook command documentation/consumer context | update to configured wrapper semantics | launch integration |

`crates/flow-nexus/src/generated/send_tool.rs:104` and `src/send_tool.rs:150-156` are unrelated `SendInvocation`, not adapter Invocation and remain out of scope.

## Shared ownership and missing authored detail

`BootstrapTextBudget` has one shared `flow-ethos` owner. Composer outer decode and nested target Invocation budget are distinct typed values. Hook native JSON remains JSON and is not a Datom budget consumer. Exact new Ethos layouts are now supplied by `052-adapter-envelopes.md`; generated Rust output and constructor lines do not yet exist in Flow916 and therefore cannot be cited as current source.

## Query coverage and exact remaining symbols

The query covered all workspace `Invocation {`, `HookConfiguration {`, composer binary names, hook names, Nix files, Ethos files, and Rust tests. Remaining future symbols are generated Invocation/HookConfiguration fields and Nix wrapper outputs after implementation; no current source location exists by design. No source edits/fetches performed.
