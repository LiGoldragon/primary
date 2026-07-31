use std::marker::PhantomData;

trait Phase {
    type At<Position, Literal, Output>;
}

enum Logos {}
enum Nomos {}
enum VisibilityPosition {}

impl Phase for Logos {
    type At<Position, Literal, Output> = Output;
}

impl Phase for Nomos {
    type At<Position, Literal, Output> = Slot<Position, Literal, Output>;
}

struct Slot<Position, Literal, Output> {
    literal: Literal,
    position: PhantomData<fn() -> Position>,
    output: PhantomData<fn() -> Output>,
}

struct Declaration<P: Phase> {
    visibility: P::At<VisibilityPosition, bool, bool>,
}

fn accepts_only_logos(_value: Declaration<Logos>) {}

fn main() {
    let nomos = Declaration::<Nomos> {
        visibility: Slot {
            literal: true,
            position: PhantomData,
            output: PhantomData,
        },
    };
    accepts_only_logos(nomos);
}
