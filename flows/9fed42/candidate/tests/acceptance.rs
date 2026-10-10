//! Acceptance tests of the Flow Nexus contract.
//!
//! Wire: a value of every generated root archives
//! with rkyv and restores equal, with and without the
//! `datom` feature (the Nexus builds without it).
//!
//! Datom (feature `datom`): each datom the design
//! writes in section 1 reads against the type the
//! design gives it, and the value it reads prints and
//! reads back equal.

use flow_ethos_candidate::{
    forms, memory, meta_signal, signal, Address, Aspect, Event, Layer, Lock, Metaflow, Process,
    Request, Said, Source, State, Subaspect,
};

fn crosses<T>(value: T)
where
    T: rkyv::Archive
        + for<'a> rkyv::Serialize<
            rkyv::api::high::HighSerializer<
                rkyv::util::AlignedVec,
                rkyv::ser::allocator::ArenaHandle<'a>,
                rkyv::rancor::Error,
            >,
        > + PartialEq
        + std::fmt::Debug,
    T::Archived: for<'a> rkyv::bytecheck::CheckBytes<rkyv::api::high::HighValidator<'a, rkyv::rancor::Error>>
        + rkyv::Deserialize<T, rkyv::api::high::HighDeserializer<rkyv::rancor::Error>>,
{
    let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&value).expect("archives");
    let restored = rkyv::from_bytes::<T, rkyv::rancor::Error>(&bytes).expect("restores");
    assert_eq!(restored, value);
}

fn address(aspect: Aspect, topic: &str, layer: Layer) -> Address {
    Address { aspect, topic: topic.to_owned(), layer }
}

/// The design's first written metaflow.
fn psyche_core() -> Metaflow {
    Metaflow {
        address: address(Aspect::Psyche, "core", Layer::Primary),
        state: State::Awake("startInputVital".to_owned()),
        past: vec!["zooWrongYouth".to_owned()],
        queue: vec![],
    }
}

/// The design's second written metaflow.
fn mind_flow_refresh() -> Metaflow {
    Metaflow {
        address: address(Aspect::Mind, "flowRefresh", Layer::Secondary),
        state: State::Asleep,
        past: vec![],
        queue: vec![Request::Notice("branch merged".to_owned())],
    }
}

fn flow_record() -> memory::Flow {
    memory::Flow {
        flow_id: "9fed42".to_owned(),
        session: "9fed4256-1f3d-4e5a-b675-7e75fecf623c".to_owned(),
        process: Process { pid: 4242, started: 987_654 },
        events: vec![
            Event::Started,
            Event::ToolUsed("Bash".to_owned()),
            Event::ContextMeasured(flow_ethos_candidate::signal_flow_fixture::ContextMeasured_Data {
                tokens: 120_000,
                window: 1_000_000,
            }),
            Event::Stopped,
        ],
    }
}

fn module_record() -> memory::Module {
    memory::Module {
        subaspect: Subaspect::Vision,
        topic: "flow".to_owned(),
        source: Source {
            repository: "psyche-skills".to_owned(),
            hash: "a3f1".to_owned(),
            path: "vision/flow.md".to_owned(),
        },
    }
}

fn model_record() -> memory::Model {
    memory::Model { layer: Layer::Secondary, native: "claude-opus-4-6".to_owned() }
}

fn threshold_record() -> memory::Threshold {
    memory::Threshold { layer: Layer::Primary, handover: 20, refresh: 40 }
}

/// The design's written request vector, oldest first,
/// the waking request last.
fn drained_queue() -> Vec<Request> {
    vec![
        Request::Notice("branch flowRefresh merged".to_owned()),
        Request::Result("tests pass on the pushed revision".to_owned()),
        Request::Order("bring the refresh to production".to_owned()),
    ]
}

#[test]
fn every_root_crosses_the_wire() {
    let lock = Lock { address: address(Aspect::Psyche, "core", Layer::Primary), until: 1_791_590_400 };
    let process = Process { pid: 4242, started: 987_654 };
    crosses(psyche_core());
    crosses(mind_flow_refresh());
    crosses(drained_queue());
    crosses(Request::Psyches(vec![Said {
        context: "relayed by a Secondary".to_owned(),
        verbatim: "the words whole".to_owned(),
    }]));
    crosses(signal::Query::Launch(signal::Launch_Data {
        address: address(Aspect::Psyche, "flow", Layer::Primary),
        modules: vec!["vision-flow".to_owned()],
        brief: "Design Flow's module registry.".to_owned(),
    }));
    crosses(signal::Query::Deliver(signal::Deliver_Data {
        lock: lock.clone(),
        sender: address(Aspect::Mind, "flowRefresh", Layer::Secondary),
        request: Request::Question("which branch?".to_owned()),
    }));
    crosses(signal::Query::Identify(process.clone()));
    crosses(signal::Response::Refreshed(signal::Refreshed_Data {
        first_flow_id: "a1b2c3".to_owned(),
        second_flow_id: "d4e5f6".to_owned(),
    }));
    crosses(signal::Response::Refused(signal::Refused_Data::Unidentified(process.clone())));
    crosses(signal::Response::Refused(signal::Refused_Data::NoneAbove));
    crosses(forms::Send {
        recipient: forms::Recipient::Up,
        request: Request::Question("which branch?".to_owned()),
    });
    crosses(meta_signal::Query::Bind(meta_signal::Bind_Data {
        address: address(Aspect::Field, "flow", Layer::Tertiary),
        process,
    }));
    crosses(meta_signal::Response::Refused(meta_signal::Refused_Data::NoSource(
        "vision/flow.md".to_owned(),
    )));
    crosses(forms::Send {
        recipient: forms::Recipient::Address(address(Aspect::Psyche, "flow", Layer::Primary)),
        request: drained_queue().remove(2),
    });
    crosses(forms::Deliver {
        lock: lock.clone(),
        sender: address(Aspect::Mind, "flowRefresh", Layer::Secondary),
        request: Request::Notice("wakes nothing".to_owned()),
    });
    let stored_metaflow: memory::Metaflow = psyche_core();
    let stored_lock: memory::Lock = lock;
    crosses(stored_metaflow);
    crosses(stored_lock);
    crosses(flow_record());
    crosses(module_record());
    crosses(model_record());
    crosses(threshold_record());
}

#[cfg(feature = "datom")]
mod datom {
    use super::*;
    use datom_codec::{Actualizing, Budget, Composing, Datomizable, Potential};
    use protos::{Protosizable, ReaderBudget, Textualizable};

    fn budget() -> Budget {
        Budget {
            remaining: 4096,
            reader: ReaderBudget { remaining: 4096 },
            depth: 0,
            maximum_depth: 1024,
        }
    }

    /// Reads `text` as T, prints what it read, and
    /// reads the print back equal.
    fn reads<T: Composing + Datomizable + PartialEq + std::fmt::Debug>(text: &str) -> T {
        let value = match Potential::<T>::from(text.to_owned()).actualize(&mut budget()) {
            Ok(value) => value,
            Err(error) => panic!("{text} does not read: {error:?}"),
        };
        let printed = value.datomize(vec![]).protosize().textualize();
        println!("read {text}\nprinted {printed}");
        let again = Potential::<T>::from(printed.clone())
            .actualize(&mut budget())
            .expect("the print reads back");
        assert_eq!(again, value, "{printed} reads back equal");
        value
    }

    #[test]
    fn the_written_request_vector_reads_oldest_first_waking_last() {
        let text = "[  Notice.«branch flowRefresh merged»
   Result.«tests pass on the pushed revision»
   Order.«bring the refresh to production» ]";
        assert_eq!(reads::<Vec<Request>>(text), drained_queue());
    }

    #[test]
    fn the_written_psyche_metaflow_reads() {
        let text = "{  { Psyche core Primary }
   Awake.startInputVital
   [ zooWrongYouth ]
   [] }";
        assert_eq!(reads::<Metaflow>(text), psyche_core());
    }

    #[test]
    fn the_written_mind_metaflow_reads() {
        let text = "{  { Mind flowRefresh Secondary }
   Asleep
   []
   [ Notice.«branch merged» ] }";
        assert_eq!(reads::<Metaflow>(text), mind_flow_refresh());
    }

    #[test]
    fn a_psyche_request_carries_context_and_verbatim() {
        let text = "Psyche.{ «said in the Flow books thread» «his words, whole» }";
        assert_eq!(
            reads::<Request>(text),
            Request::Psyche(Said {
                context: "said in the Flow books thread".to_owned(),
                verbatim: "his words, whole".to_owned(),
            })
        );
    }

    #[test]
    fn the_written_configure_module_payload_reads() {
        let text = "Configure.Module.{
   Vision
   flow
   { psyche-skills
     a3f1…9c2e
     vision/flow.md } }";
        assert_eq!(
            reads::<meta_signal::Query>(text),
            meta_signal::Query::Configure(meta_signal::Configure_Data::Module(
                meta_signal::Configure_Data_Module_Data {
                    subaspect: Subaspect::Vision,
                    topic: "flow".to_owned(),
                    source: Source {
                        repository: "psyche-skills".to_owned(),
                        hash: "a3f1…9c2e".to_owned(),
                        path: "vision/flow.md".to_owned(),
                    },
                }
            ))
        );
    }

    #[test]
    fn the_written_launch_reads() {
        let text = "Launch.{
   { Psyche flow Primary }
   [ vision-flow
     knowledge-ethos ]
   «Design Flow's module registry.» }";
        assert_eq!(
            reads::<signal::Query>(text),
            signal::Query::Launch(signal::Launch_Data {
                address: address(Aspect::Psyche, "flow", Layer::Primary),
                modules: vec!["vision-flow".to_owned(), "knowledge-ethos".to_owned()],
                brief: "Design Flow's module registry.".to_owned(),
            })
        );
    }

    #[test]
    fn a_written_send_reads_with_up_and_with_an_address() {
        assert_eq!(
            reads::<forms::Send>("{ Up Order.«bring the refresh to production» }"),
            forms::Send {
                recipient: forms::Recipient::Up,
                request: Request::Order("bring the refresh to production".to_owned()),
            }
        );
        assert_eq!(
            reads::<forms::Send>("{ Address.{ Psyche flow Primary } Question.«which branch?» }"),
            forms::Send {
                recipient: forms::Recipient::Address(address(
                    Aspect::Psyche,
                    "flow",
                    Layer::Primary
                )),
                request: Request::Question("which branch?".to_owned()),
            }
        );
    }

    #[test]
    fn every_memory_record_reads_and_prints() {
        assert_eq!(
            reads::<memory::Flow>(
                "{  9fed42
   9fed4256-1f3d-4e5a-b675-7e75fecf623c
   { 4242 987654 }
   [ Started ToolUsed.Bash ContextMeasured.{ 120000 1000000 } Stopped ] }"
            ),
            flow_record()
        );
        assert_eq!(
            reads::<memory::Module>("{ Vision flow { psyche-skills a3f1 vision/flow.md } }"),
            module_record()
        );
        assert_eq!(reads::<memory::Model>("{ Secondary claude-opus-4-6 }"), model_record());
        assert_eq!(reads::<memory::Threshold>("{ Primary 20 40 }"), threshold_record());
        assert_eq!(
            reads::<memory::Lock>("{ { Psyche core Primary } 1791590400 }"),
            Lock { address: address(Aspect::Psyche, "core", Layer::Primary), until: 1_791_590_400 }
        );
        assert_eq!(
            reads::<memory::Metaflow>(
                "{ { Mind flowRefresh Secondary } Asleep [] [ Notice.«branch merged» ] }"
            ),
            mind_flow_refresh()
        );
    }
}
