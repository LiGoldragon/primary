use std::marker::PhantomData;

use rkyv::{Archive, Deserialize, Serialize, rancor::Error};

trait Phase {
    type At<Position, Literal, Output>;
}

#[derive(Archive, Serialize, Deserialize)]
struct Logos;

#[derive(Archive, Serialize, Deserialize)]
struct Nomos;

impl Phase for Logos {
    type At<Position, Literal, Output> = Output;
}

impl Phase for Nomos {
    type At<Position, Literal, Output> = Slot<Position, Literal, Output>;
}

#[derive(Archive, Serialize, Deserialize)]
struct VisibilityPosition;

#[derive(Archive, Serialize, Deserialize)]
struct Slot<Position, Literal, Output> {
    literal: Literal,
    position: PhantomData<fn() -> Position>,
    output: PhantomData<fn() -> Output>,
}

#[derive(Archive, Serialize, Deserialize)]
struct Declaration<P: Phase> {
    visibility: P::At<VisibilityPosition, bool, bool>,
}

fn main() {
    let value = Declaration::<Nomos> {
        visibility: Slot {
            literal: true,
            position: PhantomData,
            output: PhantomData,
        },
    };
    let bytes = rkyv::to_bytes::<Error>(&value).unwrap();
    let archived = rkyv::access::<rkyv::Archived<Declaration<Nomos>>, Error>(&bytes).unwrap();
    assert!(archived.visibility.literal);
    println!("rkyv-phase: archived and bytechecked a phase-family projection");
}
