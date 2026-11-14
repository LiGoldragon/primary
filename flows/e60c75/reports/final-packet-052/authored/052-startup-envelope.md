# 052 one startup surface

Proposed exact envelope for final approval. This is version-zero Start plus its approved configuration changes, not version-one Place/Set.

The Ethos:

```ethos
Library
[ :meta_signal_flow:ConfigurationChange ] ; same per-value vocabulary used by meta Configure
[ StructuralNodeLimit.Integer             ; checked conversion to the actual reader counter
  StructuralDepthLimit.Integer
  DatomFormDepthLimit.Integer
  CompositionStepLimit.Integer
  CompositionDepthLimit.Integer
  BootstrapTextBudget.{                  ; five distinct stage budgets, no hidden caps
     StructuralNodeLimit
     StructuralDepthLimit
     DatomFormDepthLimit
     CompositionStepLimit
     CompositionDepthLimit } ; translator-owned first-decode budget
  OrdinarySocketPath.String
  MetaSocketPath.String
  StorePath.String
  Start.{                                 ; existing three placement fields plus startup changes
     OrdinarySocketPath
     MetaSocketPath
     StorePath
     Vector<ConfigurationChange> }
  Startup.{ BootstrapTextBudget Start } ]  ; the ONE input emitted by Nix
[]                                        ; traits
[]                                        ; associations
```

The datom (illustrative values only; not baked defaults; empty changes preserve stored configuration and succeed only when the resolved required values exist):

```datom
{ { 65536 256 4096 65536 1024 }
  { /run/user/1001/flow-next/flow.sock
    /run/user/1001/flow-next/flow-meta.sock
    /home/li/.local/state/flow-next/flow.sema
    [] } }
```

## Fixed intrinsic prefix, then budgeted parsing

The translator borrows/scans only the fixed typed prefix before calling the general datom parser. It uses the SAME pinned Datom lexical whitespace/comment rules and canonical Integer spelling, reading enclosing delimiters and exactly five scalar positions. Equivalent whitespace/comments are accepted; there is no startup-only spacing dialect. Reuse the codec's exact lexical helpers or expose them without changing their semantics; do not run a recursive parser before the budget is known.

The five integers use the existing Integer representation (signed64-bit). Checked conversion and canonical spelling reject leading zero, plus sign, zero/negative, overflow, wrong arity and missing values before general parsing. Lexical scanning borrows the existing input without recursive allocation. Representability is intrinsic, not a default policy budget.

After successful prefix decoding, the translator calls the existing budgeted datom decoder on the ENTIRE SAME Startup datom with exactly that supplied budget. Typed decoding confirms full shape, identical prefix values and no trailing values. It interprets no Start paths/settings during the intrinsic phase. Excess structural nodes/depth, Datom-form depth, composition steps/depth refuses before Memory open, directory/socket effects or launch. Node/depth budgets do NOT bound string bytes or raw input size. This proposal makes no streaming/raw-byte guarantee; argv acquisition has its external process-interface bound. If a raw transport byte cap is required, it must be a separately typed bootstrap field checked before allocation/parsing, not an invented constant or an assumed consequence of these five limits.

BootstrapTextBudget is owned and consumed by this first-decode translator boundary only. The Nexus sees decoded Start; it does not store or apply BootstrapTextBudget as runtime request policy. Runtime ParserPolicy comes from the committed configuration and can change independently through meta. No environment/PATH/default chain supplies either budget.

## Startup and meta activation

Decoded Start holds the actual store/socket placement, startup-only this pass. A meta attempt to alter those settings refuses with the named setting. SourceRoot is existing live future-launch policy, distinct from placement.

Startup changes share the same ConfigurationChange vocabulary and generated field mapping as meta. Present overrides, absent preserves, absent from both refuses where required after full resolution. Explicit domain absence, including DefaultContinuity unset, remains valid; Launch refuses if member and default are both unset. Duplicate setting/key and aggregate/individual overlap refuse. One owned opening prepares required upgrades and resolved configuration, validates, then commits once before runtime activation.

## Tests and consumers

Replace nix/mk-flow-package.nix149–174 ConfigureNexus Rust generation and189–200 feature/environment injection with this Nix-emitted datom source. The executable startup decode consumes the fixed prefix and budgeted Startup, then routes decoded Start into the approved owned-opening path. No parallel executable-default source remains.

Tests: missing/wrong-shape/zero/negative/overflow integer prefix refuses before parser; wrong extra prefix field refuses; excess-node or excess-depth Start refuses before effects, each of the five stages isolated so another cap does not mask it; minimum valid budget that cannot decode the envelope refuses normally; full arity/trailing-input validation; changing runtime parser policy leaves bootstrap budget unchanged and vice versa; paths/config absent/invalid semantics; startup-only placement refusal. Equivalent whitespace/comment placements and canonical/noncanonical integer fixtures must match the pinned Datom codec. The exact reused helper names and any required visibility change are pre-body consumer evidence.

## Adapter-owned settings

Ordinary/meta client Invocation and hook configuration each carry explicit codec limits and response-frame bytes where consumed. Nix supplies these to actual invocation composition; they are not Nexus RuntimePolicy values and do not claim live meta propagation. Types may be shared, values belong to each adapter. The hook constructor passes its explicit configuration rather than relying on environment/default codec settings. The exact shared five-limit codec type is reused across bootstrap and adapter configuration; BootstrapTextBudget names ownership/use, not a second set of defaults. Existing public reader/forming/composition consumers all pass these limits; fixed256/4096 disappear from chosen-policy paths.
