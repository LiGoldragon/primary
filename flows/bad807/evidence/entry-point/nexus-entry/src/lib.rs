//! The standard entry point, as kameo actors. Four actors: main, signal,
//! operation, memory. The edges are the handles each one is given:
//! main and signal hold an `OperationHandle`; operation holds a
//! `MemoryHandle`; memory holds nothing. Both handles are built only here.

use kameo::actor::{Actor, ActorRef, Spawn};
use kameo::message::{Context, Message};
use std::convert::Infallible;
use std::path::{Path, PathBuf};

/// What memory answers every change.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Changed { Succeeded, Failed }

/// The right to open memory. Its field is private and it has no public
/// constructor, so only this crate's main actor can hand one out.
pub struct Admission { directory: PathBuf }
impl Admission {
    pub fn directory(&self) -> &Path { &self.directory }
}

/// Signal: what the Nexus says. Its methods see no memory.
pub trait Signaling: Send + Sync + 'static {
    type Query: Send + 'static;
    type Response: Send + 'static;
    type Operation: Send + 'static;
    type Outcome: Send + 'static;
    fn decode(&self, frame: &[u8]) -> Option<Self::Query>;
    fn encode(&self, response: Self::Response) -> Vec<u8>;
    fn intend(&self, query: Self::Query) -> Self::Operation;
    fn answer(&self, outcome: Self::Outcome) -> Self::Response;
    fn undecodable(&self) -> Self::Response;
}

/// Memory: what the Nexus remembers. Opening it takes an Admission.
pub trait Remembering: Sized + Send + 'static {
    type Change: Send + 'static;
    type Reading: Send + 'static;
    type Remembered: Send + 'static;
    fn open(admission: Admission) -> Option<Self>;
    fn change(&mut self, change: Self::Change) -> Changed;
    fn read(&self, reading: Self::Reading) -> Self::Remembered;
}

/// Operation: what the Nexus does; the one part handed memory.
pub trait Operating<M: Remembering>: Send + 'static {
    type Operation: Send + 'static;
    type Outcome: Send + 'static;
    fn perform(&mut self, operation: Self::Operation, memory: &MemoryHandle<M>)
        -> impl Future<Output = Self::Outcome> + Send;
}

/// A whole Nexus names its three parts.
pub trait Nexus: Send + 'static {
    type Memory: Remembering;
    type Operation: Operating<Self::Memory>;
    type Signal: Signaling<
        Operation = <Self::Operation as Operating<Self::Memory>>::Operation,
        Outcome = <Self::Operation as Operating<Self::Memory>>::Outcome>;
    fn signal() -> Self::Signal;
    fn operation() -> Self::Operation;
    /// Where its memory lives; the executable owns this default.
    fn directory() -> PathBuf;
}

// Memory actor: talks to no one; answers whoever holds its handle.
pub struct MemoryActor<M: Remembering> { memory: M }
impl<M: Remembering> Actor for MemoryActor<M> {
    type Args = M;
    type Error = Infallible;
    async fn on_start(memory: M, _: ActorRef<Self>) -> Result<Self, Infallible> { Ok(Self { memory }) }
}
struct Change<C>(C);
struct Reading<R>(R);
impl<M: Remembering> Message<Change<M::Change>> for MemoryActor<M> {
    type Reply = Result<Changed, Infallible>;
    async fn handle(&mut self, change: Change<M::Change>, _: &mut Context<Self, Self::Reply>) -> Self::Reply {
        Ok(self.memory.change(change.0))
    }
}
impl<M: Remembering> Message<Reading<M::Reading>> for MemoryActor<M> {
    type Reply = Result<M::Remembered, Infallible>;
    async fn handle(&mut self, reading: Reading<M::Reading>, _: &mut Context<Self, Self::Reply>) -> Self::Reply {
        Ok(self.memory.read(reading.0))
    }
}

/// The only way to memory. No public constructor: given to operation alone.
pub struct MemoryHandle<M: Remembering> { actor: ActorRef<MemoryActor<M>> }
impl<M: Remembering> MemoryHandle<M> {
    pub async fn change(&self, change: M::Change) -> Changed {
        self.actor.ask(Change(change)).await.unwrap_or(Changed::Failed)
    }
    pub async fn read(&self, reading: M::Reading) -> Option<M::Remembered> {
        self.actor.ask(Reading(reading)).await.ok()
    }
}

// Operation actor: the one actor that holds memory.
pub struct OperationActor<N: Nexus> { operation: N::Operation, memory: MemoryHandle<N::Memory> }
impl<N: Nexus> Actor for OperationActor<N> {
    type Args = (N::Operation, MemoryHandle<N::Memory>);
    type Error = Infallible;
    async fn on_start((operation, memory): Self::Args, _: ActorRef<Self>) -> Result<Self, Infallible> {
        Ok(Self { operation, memory })
    }
}
type OperationOf<N> = <<N as Nexus>::Operation as Operating<<N as Nexus>::Memory>>::Operation;
type OutcomeOf<N> = <<N as Nexus>::Operation as Operating<<N as Nexus>::Memory>>::Outcome;
struct Perform<O>(O);
impl<N: Nexus> Message<Perform<OperationOf<N>>> for OperationActor<N> {
    type Reply = Result<OutcomeOf<N>, Infallible>;
    async fn handle(&mut self, perform: Perform<OperationOf<N>>, _: &mut Context<Self, Self::Reply>) -> Self::Reply {
        Ok(self.operation.perform(perform.0, &self.memory).await)
    }
}

/// The only way to operation; held by main and signal.
pub struct OperationHandle<N: Nexus> { actor: ActorRef<OperationActor<N>> }
impl<N: Nexus> Clone for OperationHandle<N> { fn clone(&self) -> Self { Self { actor: self.actor.clone() } } }
impl<N: Nexus> OperationHandle<N> {
    pub async fn perform(&self, operation: OperationOf<N>) -> Option<OutcomeOf<N>> {
        self.actor.ask(Perform(operation)).await.ok()
    }
}

// Signal actor: holds operation, never memory. Its sub-actors (one per
// socket connection) hold only the signal actor.
pub struct SignalActor<N: Nexus> { signal: N::Signal, operation: OperationHandle<N> }
impl<N: Nexus> Actor for SignalActor<N> {
    type Args = (N::Signal, OperationHandle<N>);
    type Error = Infallible;
    async fn on_start((signal, operation): Self::Args, _: ActorRef<Self>) -> Result<Self, Infallible> {
        Ok(Self { signal, operation })
    }
}
pub struct Frame(pub Vec<u8>);
impl<N: Nexus> Message<Frame> for SignalActor<N> {
    type Reply = Result<Vec<u8>, Infallible>;
    async fn handle(&mut self, frame: Frame, _: &mut Context<Self, Self::Reply>) -> Self::Reply {
        let response = match self.signal.decode(&frame.0) {
            None => self.signal.undecodable(),
            Some(query) => {
                let operation = self.signal.intend(query);
                match self.operation.perform(operation).await {
                    Some(outcome) => self.signal.answer(outcome),
                    None => self.signal.undecodable(),
                }
            }
        };
        Ok(self.signal.encode(response))
    }
}

/// Where frames enter: the signal actor's address, as a socket listener holds it.
pub struct Door<N: Nexus> { signal: ActorRef<SignalActor<N>> }
impl<N: Nexus> Door<N> {
    pub async fn knock(&self, frame: Vec<u8>) -> Vec<u8> {
        self.signal.ask(Frame(frame)).await.unwrap_or_default()
    }
}

/// Main actor: builds the three, then keeps only the operation handle.
pub struct MainActor<N: Nexus> { operation: OperationHandle<N> }
impl<N: Nexus> MainActor<N> {
    pub fn operation(&self) -> &OperationHandle<N> { &self.operation }
}
/// The one path, provided once for every Nexus.
pub trait Entering: Nexus + Sized {
    fn open(directory: PathBuf) -> Option<(MainActor<Self>, Door<Self>)> {
        let memory = Self::Memory::open(Admission { directory })?;
        let memory = MemoryHandle { actor: MemoryActor::spawn(memory) };
        let operation = OperationHandle { actor: OperationActor::<Self>::spawn((Self::operation(), memory)) };
        let signal = SignalActor::<Self>::spawn((Self::signal(), operation.clone()));
        Some((MainActor { operation }, Door { signal }))
    }
    /// Run until terminated: the body of every Nexus's `main`.
    fn enter() -> std::process::ExitCode {
        let Ok(runtime) = tokio::runtime::Runtime::new() else { return std::process::ExitCode::FAILURE };
        runtime.block_on(async {
            match Self::open(Self::directory()) {
                Some((_main, _door)) => { let _ = tokio::signal::ctrl_c().await; std::process::ExitCode::SUCCESS }
                None => std::process::ExitCode::FAILURE,
            }
        })
    }
}
impl<N: Nexus> Entering for N {}

/// `nexus_entry::main!(Chronos);` is the whole of a Nexus's main.rs.
#[macro_export]
macro_rules! main {
    ($nexus:ty) => {
        fn main() -> std::process::ExitCode { <$nexus as $crate::Entering>::enter() }
    };
}
