# 052 explicit adapter envelopes and producers

Core approved these adapter envelopes and configured-hook producer; implementation remains gated. Exact916 composers take TWO raw CLI arguments (socket Datom, Query Datom), then decode each with Rust budgets. Ordinary/meta Invocation is currently {socket Query}. Hook argv configuration is Datom; native stdin is separately Claude JSON. This replaces those constructors/consumers together; no native JSON parser is mislabeled a Datom consumer.

## Shared edge vocabulary

The ONE five-limit record already approved as BootstrapTextBudget is owned in the shared flow-ethos Library with its five existing typed leaves. Its name means the adapter's initial decode budget, not exclusively Nexus startup. Reuse this exact record in Startup and each adapter; no second copy of the five declarations. FrameBytes is one positive checked usize/u32 quantity for actual length-prefixed client transport, inbound and outbound. Socket path types remain existing shared types. CliExecutablePath is an explicit absolute executable path, lexical validation only, not PATH search or sibling discovery.

The Ethos shared addition (the five scalar declarations are the existing approved declarations, listed here by reference, not redeclared in each client):

```ethos
Library
[]                                        ; intrinsic scalar types
[ BootstrapTextBudget.{                   ; existing five fields, one shared owner
     StructuralNodeLimit
     StructuralDepthLimit
     DatomFormDepthLimit
     CompositionStepLimit
     CompositionDepthLimit }
  FrameBytes.Integer                      ; positive, checked usize and u32
  CliExecutablePath.String ]              ; explicit executable used by hook
[]                                        ; traits: use approved decoder/transport capabilities
[]                                        ; associations
```

## Ordinary adapter — exact field order

```ethos
Library
[ :flow_ethos:[ BootstrapTextBudget FrameBytes OrdinarySocketPath CliExecutablePath ]
  :signal_flow:Query ]                     ; only Query crosses the Nexus wire
[ Invocation.{                            ; ONE Datom argument to flow binary
     BootstrapTextBudget
     FrameBytes
     OrdinarySocketPath
     Query }
  ComposerInput.{                         ; ONE Datom argument to flow-compose-invocation
     BootstrapTextBudget
     Invocation }
  OrdinaryClientConfiguration.{          ; target invocation settings, no Query yet
     BootstrapTextBudget
     FrameBytes
     OrdinarySocketPath
     CliExecutablePath }
  HookConfiguration.{                    ; ONE Datom argv argument to flow-hook
     BootstrapTextBudget
     OrdinaryClientConfiguration } ]
[]                                        ; traits
[]                                        ; associations
```

## Meta adapter — exact field order

```ethos
Library
[ :flow_ethos:[ BootstrapTextBudget FrameBytes MetaSocketPath ]
  :meta_signal_flow:Query ]                ; only Query crosses the meta wire
[ Invocation.{                            ; ONE Datom argument to flow-meta binary
     BootstrapTextBudget
     FrameBytes
     MetaSocketPath
     Query }
  ComposerInput.{                         ; ONE Datom argument to flow-meta-compose-invocation
     BootstrapTextBudget
     Invocation } ]
[]                                        ; traits
[]                                        ; associations
```

The first field of every text entry is the same fixed five-scalar budget. The approved borrowed nonrecursive lexical scanner reads that prefix, then budget-decodes the ENTIRE corresponding envelope using that prefix. Outer envelopes still have their actual enclosing braces, whitespace/comments and exact arity; no special grammar. Nested target budgets are decoded as typed data, validated for representability, and passed unchanged to their own future boundary. A producer never silently substitutes its parsing budget for the target's.

Example ordinary composer Datom, illustrative values only:

```datom
{ { 65536 256 4096 65536 1024 }
  { { 32768 128 2048 32768 512 }
    1048576
    /run/user/1001/flow/flow.sock
    Report.{ abc Started.None } } }
```

The Query example uses the existing witnessed Report/Started shape; abc is illustrative FlowId data, not a claim of a registered flow.

## Exact constructor projections

- Ordinary/meta composers replace the two-argument interface with one ComposerInput. They decode with the OUTER BootstrapTextBudget, validate target limits/socket/frame values, then textualize exactly `input.invocation` using retained output Datomizable/Protosizable/Compactable. No parsing budget is introduced on the output path. No client call or socket effect occurs in a composer.
- Ordinary/meta clients decode their Invocation using its first budget, then perform request/reply framing using its FrameBytes and connect to its explicit socket. Only Query is serialized onto the Signal wire, not the adapter configuration. Typed frame checks cover outbound length before any write and inbound announced length before allocation.
- Hook decodes HookConfiguration with its OUTER budget. It translates native stdin JSON into the existing typed Query using existing behavior. It constructs Invocation from the target OrdinaryClientConfiguration budget/frame/socket plus that Query, and executes exactly its CliExecutablePath with the textualized one Invocation argument. No PATH/sibling fallback. Target CLI parses with TARGET budget; hook budget never governs that parser by implication.
- Native JSON stdin parsing and existing malformed-input/event handling are unchanged by this Datom change. No claim that the five Datom limits bound JSON bytes/depth or raw argv acquisition. A wider hook error audit remains separate scope.

## Nix producer and launched hook — one authority per fact

Nix supplies separate declared values for ordinary composer initial decode, ordinary client initial decode/frame, meta composer initial decode, meta client initial decode/frame, hook initial decode and its target ordinary client settings. Share a configured value only when explicitly chosen in Nix; no Rust fallback or hidden coupling. Repeated use of a path/value is generated from its one Nix declaration, not independent authored authorities.

Nix ordinary/meta wrappers now pass ONE rendered ComposerInput to their corresponding composer, embedding the user Query as data in the target Invocation; the composer validates the full typed envelope before emitting client input. Shell quoting passes one argument, never evaluates Query as shell code. All wrapper callers change in the same composition.

For launched hooks, Nix emits a configured executable wrapper that invokes the actual flow-hook binary with ONE rendered HookConfiguration. Its ordinary socket is drawn from the SAME declared startup place used by this Nexus; this pass already makes socket placement startup-only. Its target CliExecutablePath is the exact packaged flow binary, and its budgets/frame are explicit adapter configuration. `LaunchPolicy.Hook` names this configured wrapper. The Nexus Herdr launch constructor no longer manufactures a HookConfiguration from a socket plus missing policy: it emits the configured wrapper path as the hook command. This removes hook budget ownership from the Nexus and avoids a second adapter policy store. A different explicit Nexus place needs the matching generated hook wrapper in its startup data; Nix fixtures test this association.

Core approved this wrapper producer change; final consumer/schema/custody review and sole-writer body clearance remain required. It preserves one Start envelope and existing ConfigurationChange vocabulary; it does not add adapter settings to RuntimePolicy or silently add fields to Start. A manually supplied hook wrapper is explicit executable configuration whose behavior is outside the Nexus's typed promise, like any external executable; the packaged Nix composition is the supported coherent producer.

## Exact consumer/test ledger requirements

Replace crates/flow/ethos/invocation.ethos6–9, crates/flow-meta/ethos/invocation.ethos5–7 and regenerate each invocation module. Update both compose_invocation.rs8–31 argument/decode/output paths, both clients' main decode/framing, flow hook.rs47–98 and ReportsThroughCli constructor/executable selection, Herdr launch.rs484–496 hook command composition, and nix/mk-flow-package.nix89–117 plus149–200 wrapper/default replacement. Source ledger must enumerate every other Invocation/HookConfiguration literal and raw composer caller, including tests.

Tests: ordinary/meta/compose/hook missing/zero/overflow five-prefix values fail before effects; producer and target deliberately different budgets remain distinct; exact constructor projections and one-argument shell quoting; user Query cannot execute shell; client bidirectional frame checks; output textualization gains no parsing cap; hook native JSON still follows its existing contract; Nix actual rendered hook command/socket/CLI matches startup place and package; no Rust literals supply any missing policy. Native hook argv/stdin, nonblocking exit and diagnostic behavior are preserved; tests execute the ACTUAL rendered configured wrapper and CLI invocation, not merely compare snippets. Empty/invalid hook config follows the existing nonblocking hook exit contract while recording existing diagnostics, not a fake successful Nexus report. Actual compile/process/capsule execution follows body clearance; the complete typed plan is reviewed now.
