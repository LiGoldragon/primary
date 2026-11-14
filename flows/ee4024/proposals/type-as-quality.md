Presentation.{ «A type in an input position» Account }

# A type in an input position

Created by Fable 5.1, for a conversation with the living.

One capability of Sema's Structural trait is enough to see the whole question: outline, which takes a depth and yields the headings down to it.

```ethos
Depth.Integer
Outline.{ Title.String Vector<Outline> }
Structural.[ outline.{ [ Depth ] [ Vector<Outline> ] } ]
```

As Ethos lowers it today, the input is the type itself. Rust is content with this.

```rust
pub type Integer = i64;
pub struct Depth(pub Integer);
pub struct Outline { pub title: String, pub children: Vec<Outline> }

pub trait Structural {
    fn outline(&self, depth: Depth) -> Vec<Outline>;
}
```

The vision says otherwise: a capability speaks in traits, and a concrete type in an input is a trait not yet named. The generator obeys the vision and refuses Depth in that position. The idea behind the line is that a capability's contract is about qualities: what a thing must be able to do to stand in that position, never which thing it is.

Written out literally, the quality is a trait, Deep, anything that has a depth, and the capability takes any bearer of it.

```ethos
Deep.[ depth.[ Integer ] ]                        ; the quality: anything that has a depth
StructuralByQuality.[ outline.{ [ Deep ] [ Vector<Outline> ] } ]
```

```rust
pub trait Deep { fn depth(&self) -> Integer; }

impl Deep for Depth { fn depth(&self) -> Integer { self.0 } }

pub trait StructuralByQuality {
    fn outline<D: Deep>(&self, depth: D) -> Vec<Outline>;
}
```

What I see in it: the concrete type has not left, it has moved one layer down, into `depth.[ Integer ]`. Deep is a wrapper that names nothing Depth did not, and Sema would need one such wrapper for every piece of data an operation takes, Placed, Searching, Editing. Followed to the bottom, Integer becomes a quality too, and at that point the words type and trait name one thing.

That last step is, I think, the real idea, and it can be taken now without a wrapper. A declared type is already the quality of being itself: Depth is the quality of being a depth, the newtype Depth is its canonical bearer, and any other type may bear it by saying how it becomes a Depth. Rust has exactly this quality, and spells it Into.

```ethos
; the same signature as today: Depth in an input position is read as the quality of being a Depth
StructuralByType.[ outline.{ [ Depth ] [ Vector<Outline> ] } ]
```

```rust
// what Ethos would generate: the input is anything that becomes a Depth
pub trait StructuralByType {
    fn outline(&self, depth: impl Into<Depth>) -> Vec<Outline>;
}

// another type bears the quality by saying how it becomes a Depth
impl From<Integer> for Depth {
    fn from(integer: Integer) -> Depth { Depth(integer) }
}

// a caller passes the canonical bearer or any other
fn callers<S: StructuralByType>(sema: &S) -> (Vec<Outline>, Vec<Outline>) {
    (sema.outline(Depth(2)), sema.outline(2))
}
```

So the rule keeps its sense, a position is a quality, and the Ethos stays as written: a type in an input position means anything that is that type, lowered to Into. A trait is written where the quality is wider than one type, Serializable for push. The output is left as a type for now, because the caller wants to hold what comes back; the far version may make it a quality too, and nothing written today would change.
