Presentation.{ «Ethos is never gone around» Proposal }

# Ethos is never gone around

Created by Fable 5.1, on the living's words.

### Proposal 1: Every type is generated at every build, and nothing runs beside it · psyche-belief › vision/ethos.md

::: comment
The Sema flow typed its structs by hand when the generator refused its schema, and the audit found the same in most active repositories. The vision said types are generated; nothing made certain of it. A type compiled in proves nothing about the path data takes at runtime, so the check goes further: with every function a generated trait capability, the hand-written code has nothing else to call. It is deterministic and runs in the build of each component that matters.
:::

+ ## The build makes certain of it

+ Generated Rust is never kept: the repository holds the ethos and the hand-written bodies alone. Ethos Zero is a flake input of the component, pinned as every dependency is, and the generation is a derivation of the ethos and that pinned generator; so the build is deterministic, nothing rebuilds unless the ethos or the pin changes, and a generator bump is a pin change that rebuilds what it should. Cargo reads the generated module from the build's output directory, never from the repository.

+ A component's build makes certain, every time, that its runtime has no path but the ontology. It checks three things: that no struct, enum or trait is declared outside the generated code; that no function stands outside a trait body but `fn main`, and no inherent impl exists; and that every trait's capability signatures are the generated ones, so the hand-written Rust is trait bodies and nothing else. A body can then call only generated capabilities on generated types, because the component holds no other function; the data cannot run beside the types. Any check failing fails the build. Tests aside.

+ The check is one Nix check that every component shares, and the components it binds are the running Nexuses and the stack under them: Protos, Datom, Signal, Ethos Zero, Nexus, Flow, Belief, herdr, Orchestrate, Lojix, Sema.

```nix
+ # the component's flake: the generator pinned as an input, the generated Rust a derivation
+ inputs.ethos-zero.url = "github:LiGoldragon/ethos-zero/v22.0.0";
+ generated = pkgs.runCommand "generated" { nativeBuildInputs = [ ethos-zero ]; } ''
+   ethos-zero generate ${./ethos} --out $out                # the types, made at build, never kept
+ '';
+ # the crate's build places $generated as its generated module through OUT_DIR
+
+ # the shared check, as each component's flake includes it; command names tentative
+ checks.ethos = pkgs.runCommand "ethos-holds" { nativeBuildInputs = [ ethos-zero ]; } ''
+   ethos-zero declared ${./src} --outside ${generated}     # every struct, enum or trait declared outside
+                                                            #   the generated code; any line fails
+   ethos-zero free ${./src}                                 # every free function but main, every inherent impl,
+                                                            #   every signature not generated; any line fails
+   touch $out
+ '';
```

### Proposal 2: A refusal from the generator is the work · psyche-belief › intent/anatomy.md

::: comment
Loaded by Mind flows. The thinking machine keeps acting, in Ethos.
:::

+ When Ethos Zero refuses a schema, the work goes on in Ethos: the schema or the generator is fixed, or the refusal is brought up as a question. The types are never written by hand around it.

### Proposal 3: The variant rule holds in every section · psyche-belief › vision/ethos.md

::: comment
A variant named as a defined type carries that type; the rule was being read as a types-section rule because the Signal example itself broke it, an input Lock beside a type Lock. The example is the fault: the input is the verb.
:::

+ A variant named as a defined type carries that type in every section, a Signal's inputs and outputs and an Operation's attempts among them; a variant so named that declares any payload of its own is refused at its line.

```ethos
- [ Lock.LockRequest                 ; inputs
+ [ Acquire.LockRequest              ; inputs: the verb, since Lock names the type
    Release.LockId ]
```

```rust
- pub enum Input  { Lock(LockRequest), Release(LockId) }
+ pub enum Input  { Acquire(LockRequest), Release(LockId) }
```
