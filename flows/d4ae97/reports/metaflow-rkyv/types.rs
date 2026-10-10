// Shared record shapes, included by both crates.
// Ids are Integer (i64), the only fixed-width scalar ethos-zero generates.

use rkyv::{Archive, Deserialize, Serialize};

#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum Aspect {
    Psyche,
    Mind,
    Field,
}

#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum Layer {
    Primary,
    Secondary,
    Tertiary,
    Quaternary,
}

#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum Kind {
    Voice { aspect: Aspect, layer: Layer },
    Implementation { layer: Layer },
}

/// State with the flow id carried by the variant (ethos `Awake.FlowId`).
#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum State {
    Awake(i64),
    Asleep,
    Ended,
}

/// The fixed record: no vector, no string.
#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub struct Metaflow {
    pub metaflow: i64,
    pub kind: Kind,
    pub state: State,
    pub current: i64,
    pub predecessor: Option<i64>,
    pub flows: i64,
    pub changed: i64,
}

/// The same record, flow ids as String (signal-flow's FlowId.String today).
#[derive(Archive, Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct MetaflowStringIds {
    pub metaflow: i64,
    pub kind: Kind,
    pub awake: bool,
    pub current: String,
    pub predecessor: Option<String>,
    pub flows: i64,
    pub changed: i64,
}

/// The vectored record: the second-edition shape (name and past inline).
#[derive(Archive, Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct MetaflowVectored {
    pub metaflow: i64,
    pub kind: Kind,
    pub name: String,
    pub state: State,
    pub past: Vec<i64>,
}

/// One succession row per flow run: fixed, keyed (metaflow, ordinal).
#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub struct Succession {
    pub metaflow: i64,
    pub ordinal: i64,
    pub flow: i64,
    pub started: i64,
}

/// The shape the book proposes: State without payload, Current the one pointer.
#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum Wakefulness {
    Awake,
    Asleep,
    Ended,
}

#[derive(Archive, Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub struct MetaflowProposed {
    pub metaflow: i64,
    pub kind: Kind,
    pub state: Wakefulness,
    pub current: i64,
    pub predecessor: Option<i64>,
    pub flows: i64,
    pub changed: i64,
}
