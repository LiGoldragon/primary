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
        && rfc3339_seconds(&e.heard)
}
fn rfc3339_seconds(value: &str) -> bool {
    let bytes = value.as_bytes();
    if bytes.len() != 20 || bytes[4] != b'-' || bytes[7] != b'-' || bytes[10] != b'T' || bytes[13] != b':' || bytes[16] != b':' || bytes[19] != b'Z' { return false; }
    [0..4, 5..7, 8..10, 11..13, 14..16, 17..19].iter().all(|r| bytes[r.clone()].iter().all(u8::is_ascii_digit))
}
fn quoted(value: &str) -> String {
    let mut out = String::from("\"");
    for c in value.chars() { match c { '\\' => out.push_str("\\\\"), '"' => out.push_str("\\\""), '\n' => out.push_str("\\n"), '\r' => out.push_str("\\r"), '\t' => out.push_str("\\t"), c if c.is_control() => out.push_str(&format!("\\u{:04x}", c as u32)), c => out.push(c) } }
    out.push('"'); out
}
fn emit(e: Envelope) {
    let recipients = e.recipients.iter().map(|x| quoted(x)).collect::<Vec<_>>().join(",");
    println!("{{\"producer\":\"MACHINE\",\"claimed_from\":{},\"claimed_seat\":{},\"heard\":{},\"mode\":{},\"recipients\":[{}],\"quote\":{},\"context\":{}}}", quoted(&e.from), quoted(&e.seat), quoted(&e.heard), quoted(&e.mode), recipients, quoted(&e.quote), quoted(&e.context));
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
        Ok(Ingress::MACHINE(Relay::Relay(envelope))) if valid(&envelope) => emit(envelope),
        _ => std::process::exit(2),
    }
}
