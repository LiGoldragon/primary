//! Way (c): what ethos-zero would emit beside its enums. The emitted
//! modules are `signal` and `operation`; memory lives inside operation,
//! and only operation's emitted `Entry` may open it.
//!
//! A signal part that tries to open memory does not compile:
//!
//! ```compile_fail,E0624
//! use chronos_generated::operation::Memory;
//! let memory = Memory::open(); // private to the operation module
//! ```

pub mod library {
    #[derive(Clone, Debug, PartialEq)]
    pub struct Placement { pub latitude: f64, pub longitude: f64 }
}

pub mod signal {
    use crate::{library::Placement, operation::{Operation, Outcome}};
    pub enum Query { Place(Placement), Locate }
    #[derive(Debug, PartialEq)]
    pub enum Response { Placed, Located(Placement), Refused(Refused_Data) }
    #[derive(Debug, PartialEq)]
    #[allow(non_camel_case_types)]
    pub enum Refused_Data { Unplaced, StoreRefused }
    /// Emitted: Signal's kind. No method sees memory.
    pub trait Signaling {
        fn intend(&self, query: Query) -> Operation;
        fn answer(&self, outcome: Outcome) -> Response;
    }
}

pub mod operation {
    use crate::{library::Placement, signal::{Query, Response, Signaling}};
    pub enum Operation { Keep(Placement), Recall }
    #[allow(non_camel_case_types)]
    pub enum Outcome { Kept, Recalled(Placement), Failed(Failed_Data) }
    #[allow(non_camel_case_types)]
    pub enum Failed_Data { NothingKept, StoreRefused }
    #[derive(Debug, PartialEq)]
    pub enum Changed { Succeeded, Failed }

    /// Emitted from the Memory root; opened only below this module.
    pub struct Memory { placing: Option<Placement> }
    impl Memory {
        pub(in crate::operation) fn open() -> Self { Self { placing: None } }
        pub fn change(&mut self, placing: Placement) -> Changed { self.placing = Some(placing); Changed::Succeeded }
        pub fn placing(&self) -> Option<&Placement> { self.placing.as_ref() }
    }

    /// Emitted: one method for every operation; each is handed memory.
    pub trait Operating {
        fn keep(&mut self, placement: Placement, memory: &mut Memory) -> Outcome;
        fn recall(&mut self, memory: &Memory) -> Outcome;
    }
    impl Operation {
        /// Emitted dispatch: a new operation in the ethos is a missing method here.
        pub fn perform<O: Operating>(self, operating: &mut O, memory: &mut Memory) -> Outcome {
            match self {
                Operation::Keep(placement) => operating.keep(placement, memory),
                Operation::Recall => operating.recall(memory),
            }
        }
    }

    /// Emitted entry: the path signal, operation, memory, operation, signal.
    pub struct Entry<S: Signaling, O: Operating> { signal: S, operating: O, memory: Memory }
    impl<S: Signaling, O: Operating> Entry<S, O> {
        pub fn new(signal: S, operating: O) -> Self { Self { signal, operating, memory: Memory::open() } }
        pub fn receive(&mut self, query: Query) -> Response {
            let operation = self.signal.intend(query);
            let outcome = operation.perform(&mut self.operating, &mut self.memory);
            self.signal.answer(outcome)
        }
    }
}

/// Hand-written: the bodies only.
pub mod chronos {
    use crate::{library::Placement, operation::*, signal::*};
    pub struct ChronosSignal;
    pub struct ChronosOperation;
    impl Signaling for ChronosSignal {
        fn intend(&self, query: Query) -> Operation {
            match query { Query::Place(placement) => Operation::Keep(placement), Query::Locate => Operation::Recall }
        }
        fn answer(&self, outcome: Outcome) -> Response {
            match outcome {
                Outcome::Kept => Response::Placed,
                Outcome::Recalled(placement) => Response::Located(placement),
                Outcome::Failed(Failed_Data::NothingKept) => Response::Refused(Refused_Data::Unplaced),
                Outcome::Failed(Failed_Data::StoreRefused) => Response::Refused(Refused_Data::StoreRefused),
            }
        }
    }
    impl Operating for ChronosOperation {
        fn keep(&mut self, placement: Placement, memory: &mut Memory) -> Outcome {
            match memory.change(placement) { Changed::Succeeded => Outcome::Kept, Changed::Failed => Outcome::Failed(Failed_Data::StoreRefused) }
        }
        fn recall(&mut self, memory: &Memory) -> Outcome {
            memory.placing().cloned().map_or(Outcome::Failed(Failed_Data::NothingKept), Outcome::Recalled)
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        #[test]
        fn a_placement_goes_in_and_comes_back() {
            let mut entry = Entry::new(ChronosSignal, ChronosOperation);
            assert_eq!(entry.receive(Query::Locate), Response::Refused(Refused_Data::Unplaced));
            let here = Placement { latitude: 47.6, longitude: -122.3 };
            assert_eq!(entry.receive(Query::Place(here.clone())), Response::Placed);
            assert_eq!(entry.receive(Query::Locate), Response::Located(here));
        }
    }
}
