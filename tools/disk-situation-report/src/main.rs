use datom_codec::{Actualizing, Budget, Potential};
use protos::ReaderBudget;
use serde_json::Value;
use std::{env, fs, path::Path};

#[derive(Debug, datom_codec::Composing, datom_codec::Datomizable)]
struct Request { host: String, user: String }

fn budget() -> Budget { Budget { remaining: 4096, reader: ReaderBudget { remaining: 4096 }, depth: 0, maximum_depth: 256 } }
fn main() {
    let mut args = env::args(); args.next();
    let text = args.next().unwrap_or_else(|| { eprintln!("usage: disk-situation-report '{{ host user }}'"); std::process::exit(2) });
    if args.next().is_some() { eprintln!("error: exactly one inline Datom argument is required"); std::process::exit(2); }
    let request: Request = Potential::from(text.as_str()).actualize(&mut budget()).unwrap_or_else(|e| { eprintln!("error: Datom request refused: {e:?}"); std::process::exit(2) });
    let fixture = Path::new(env!("CARGO_MANIFEST_DIR")).join("../../reports/disk-situation/fixtures/fixture.json");
    let data: Value = serde_json::from_str(&fs::read_to_string(fixture).expect("fixture readable")).expect("fixture JSON");
    println!("Disk report for {} user {}", request.host, request.user);
    for category in ["store", "build", "cache", "repositories", "dirty", "oversized"] {
        let rows = data.get(category).and_then(Value::as_array).map_or(0, Vec::len);
        println!("{}: {} fixture entries", category, rows);
    }
    println!("Shared paths: attribute once to physical owner; mark retention references separately.");
    println!("Suggestions: review authorized retention and measure before/after; no deletion performed.");
}
#[cfg(test)]
mod tests { use super::*; #[test] fn fixture_has_categories() { let p=Path::new(env!("CARGO_MANIFEST_DIR")).join("../../reports/disk-situation/fixtures/fixture.json"); let v:Value=serde_json::from_str(&fs::read_to_string(p).unwrap()).unwrap(); for k in ["store","build","cache","repositories","dirty","oversized"] { assert!(v.get(k).unwrap().is_array()); } } }
