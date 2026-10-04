//! Chronos on the standard entry point: three hand-written parts.
//! Each block below is a signal part reaching for memory; none compiles.
//!
//! It cannot open memory, an Admission not being its to make:
//!
//! ```compile_fail,E0451
//! use nexus_entry::{Admission, Remembering};
//! let memory = chronos_toy::ChronosMemory::open(Admission { directory: "/tmp".into() });
//! ```
//!
//! It cannot build a memory handle:
//!
//! ```compile_fail,E0451
//! fn reach() -> nexus_entry::MemoryHandle<chronos_toy::ChronosMemory> {
//!     nexus_entry::MemoryHandle { actor: todo!() }
//! }
//! ```
//!
//! It cannot reach through the operation handle it holds:
//!
//! ```compile_fail,E0616
//! fn reach(operation: &nexus_entry::OperationHandle<chronos_toy::Chronos>) {
//!     let _ = &operation.actor;
//! }
//! ```

extern crate self as chronos;

#[allow(unexpected_cfgs)]
pub mod generated { pub mod library; pub mod signal; pub mod operation; pub mod memory; }
pub use generated::library::*;

use generated::{memory::Placing, operation::{Failed_Data, Operation, Outcome}, signal::{Query, Refused_Data, Response}};
use nexus_entry::{Admission, Changed, MemoryHandle, Nexus, Operating, Remembering, Signaling};
use redb::{Database, ReadableDatabase, TableDefinition};
use std::path::PathBuf;

const PLACINGS: TableDefinition<&str, &[u8]> = TableDefinition::new("placing");

/// Signal: rkyv frames to and from the Chronos vocabulary.
pub struct ChronosSignal;
impl Signaling for ChronosSignal {
    type Query = Query;
    type Response = Response;
    type Operation = Operation;
    type Outcome = Outcome;
    fn decode(&self, frame: &[u8]) -> Option<Query> { rkyv::from_bytes::<Query, rkyv::rancor::Error>(frame).ok() }
    fn encode(&self, response: Response) -> Vec<u8> {
        rkyv::to_bytes::<rkyv::rancor::Error>(&response).map(|bytes| bytes.to_vec()).unwrap_or_default()
    }
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
    fn undecodable(&self) -> Response { Response::Refused(Refused_Data::StoreRefused) }
}

/// Memory: one redb table holding the last placing.
pub struct ChronosMemory { database: Database }
pub struct Latest;
impl Remembering for ChronosMemory {
    type Change = Placing;
    type Reading = Latest;
    type Remembered = Option<Placing>;
    fn open(admission: Admission) -> Option<Self> {
        Database::create(admission.directory().join("chronos.redb")).ok().map(|database| Self { database })
    }
    fn change(&mut self, placing: Placing) -> Changed {
        let Ok(bytes) = rkyv::to_bytes::<rkyv::rancor::Error>(&placing) else { return Changed::Failed };
        let written = self.database.begin_write().ok().and_then(|transaction| {
            transaction.open_table(PLACINGS).ok()?.insert("latest", bytes.as_slice()).ok()?;
            transaction.commit().ok()
        });
        if written.is_some() { Changed::Succeeded } else { Changed::Failed }
    }
    fn read(&self, _: Latest) -> Option<Placing> {
        let transaction = self.database.begin_read().ok()?;
        let table = transaction.open_table(PLACINGS).ok()?;
        let bytes = table.get("latest").ok()??;
        rkyv::from_bytes::<Placing, rkyv::rancor::Error>(bytes.value()).ok()
    }
}

/// Operation: the one part handed memory.
pub struct ChronosOperation;
impl Operating<ChronosMemory> for ChronosOperation {
    type Operation = Operation;
    type Outcome = Outcome;
    async fn perform(&mut self, operation: Operation, memory: &MemoryHandle<ChronosMemory>) -> Outcome {
        match operation {
            Operation::Keep(placement) => match memory.change(placement).await {
                Changed::Succeeded => Outcome::Kept,
                Changed::Failed => Outcome::Failed(Failed_Data::StoreRefused),
            },
            Operation::Recall => match memory.read(Latest).await {
                Some(Some(placement)) => Outcome::Recalled(placement),
                Some(None) => Outcome::Failed(Failed_Data::NothingKept),
                None => Outcome::Failed(Failed_Data::StoreRefused),
            },
        }
    }
}

/// The whole Nexus names its parts.
pub struct Chronos;
impl Nexus for Chronos {
    type Memory = ChronosMemory;
    type Operation = ChronosOperation;
    type Signal = ChronosSignal;
    fn signal() -> ChronosSignal { ChronosSignal }
    fn operation() -> ChronosOperation { ChronosOperation }
    fn directory() -> PathBuf { PathBuf::from("/run/user/1001/chronos") }
}
