# A vector carries a name

*Created by Opus.*

## Added, to vision:ethos, under "What a declaration turns into"

A position holding a constructed type, a Vector or an Option, carries a name, since the name is its documentation; a position holding a declared type is bare.

Pre-approved, his words: "you can give type names to your vector types so that we actually know what you are showing us; the name of a type is a form of documentation"

The Ethos:

```ethos
Metaflow.{ MetaflowName                    ; a declared type: bare
           Complexes.Vector<ComplexName>   ; a constructed type: named
           Routes.Vector<Route>
           Speaker.ComplexName }
```

The Rust generated from it:

```rust
#[derive(Datomizable, Compositional)]
pub struct Metaflow { pub metaflow_name: MetaflowName, pub complexes: Complexes, pub routes: Routes, pub speaker: Speaker }
```
