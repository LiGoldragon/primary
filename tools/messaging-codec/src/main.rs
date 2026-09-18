use datom_codec::{Actualizing, Budget, Composing, Datomizable, Potential};
use protos::{Protosizable, ReaderBudget, Textualizable};

// This is deliberately the one producer grammar. Shell callers do not get a
// second, permissive parser at the trust boundary.
#[derive(Debug, Datomizable, Composing)]
struct Envelope {
    from: String,
    seat: String,
    heard: String,
    mode: String,
    recipients: Vec<String>,
    quote: String,
    context: String,
}
#[derive(Debug, Datomizable, Composing)]
enum Relay { Relay(Envelope) }
#[derive(Debug, Datomizable, Composing)]
enum Ingress { MACHINE(Relay) }

fn budget() -> Budget { Budget { remaining: 4096, reader: ReaderBudget { remaining: 4096 }, depth: 0, maximum_depth: 128 } }
fn valid(e: &Envelope) -> bool {
    e.mode == "unknown" && !e.from.is_empty() && !e.seat.is_empty()
        && !e.recipients.is_empty() && !e.recipients.iter().any(|x| x == &e.from)
        && e.heard.ends_with('Z') && e.heard.contains('T')
}
fn main() {
    if std::env::args().nth(1).as_deref() == Some("example") {
        let value = Ingress::MACHINE(Relay::Relay(Envelope { from: "a".into(), seat: "b".into(), heard: "2026-01-01T00:00:00Z".into(), mode: "unknown".into(), recipients: vec!["c".into()], quote: "x".into(), context: "".into() }));
        println!("{}", value.datomize(vec![]).protosize().textualize());
        return;
    }
    let text = std::io::read_to_string(std::io::stdin()).unwrap();
    let mut potential = Potential::<Ingress>::from(text);
    match potential.actualize(&mut budget()) {
        Ok(Ingress::MACHINE(Relay::Relay(envelope))) if valid(&envelope) => println!("ok"),
        _ => std::process::exit(2),
    }
}
