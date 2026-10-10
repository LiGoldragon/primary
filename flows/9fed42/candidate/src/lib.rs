//! The Flow Nexus's contract, generated at build time
//! from ../ethos by ethos-zero into src/generated.
//! The generated files name `flow_ethos::`,
//! `curriculum::` and `signal_flow::`; this crate is
//! all three, re-exporting the Library and the two
//! test stand-ins at its root.

extern crate self as flow_ethos;
extern crate self as curriculum;
extern crate self as signal_flow;

pub use library::*;
pub use curriculum_fixture::Name;
pub use signal_flow_fixture::Event;

#[path = "generated/flow.library.rs"]
pub mod library;
#[path = "generated/flow.signal.rs"]
pub mod signal;
#[path = "generated/flow.meta.signal.rs"]
pub mod meta_signal;
#[path = "generated/forms.signal.rs"]
pub mod forms;
#[path = "generated/flow.memory.rs"]
pub mod memory;

#[path = "generated/curriculum.library.rs"]
pub mod curriculum_fixture;
#[path = "generated/signal-flow.library.rs"]
pub mod signal_flow_fixture;
