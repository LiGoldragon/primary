use datom_codec::{Actualizing, Budget, Potential};
use protos::ReaderBudget;
use serde_json::Value;
use std::{env, fs, path::Path};

#[derive(Debug, datom_codec::Composing, datom_codec::Datomizable)]
struct Request { host: String, user: String }

#[derive(Debug, datom_codec::Composing, datom_codec::Datomizable)]
enum Input { Request(Request) }

fn budget() -> Budget { Budget { remaining: 4096, reader: ReaderBudget { remaining: 4096 }, depth: 0, maximum_depth: 256 } }
fn main() {
    let mut args = env::args(); args.next();
    let text = args.next().unwrap_or_else(|| { eprintln!("usage: disk-situation-report 'Request.{{ host user }}'"); std::process::exit(2) });
    if args.next().is_some() { eprintln!("error: exactly one inline Datom argument is required"); std::process::exit(2); }
    let request = match Potential::<Input>::from(text.as_str()).actualize(&mut budget()).unwrap_or_else(|e| { eprintln!("error: Datom request refused: {e:?}"); std::process::exit(2) }) { Input::Request(request) => request };
    let fixture = Path::new(env!("CARGO_MANIFEST_DIR")).join("../../reports/disk-situation/fixtures/fixture.json");
    let data: Value = serde_json::from_str(&fs::read_to_string(fixture).expect("fixture readable")).expect("fixture JSON");
    let host = data.get("host").and_then(Value::as_str).unwrap_or("");
    let user = data.get("user").and_then(Value::as_str).unwrap_or("");
    if request.host != host || request.user != user { eprintln!("error: no fixture dataset for host {} user {}", request.host, request.user); std::process::exit(3); }
    println!("Disk report for {} user {}", request.host, request.user);
    for category in ["store", "build", "cache", "repositories", "dirty", "oversized"] {
        let rows = data.get(category).and_then(Value::as_array).expect("fixture category");
        let bytes: u64 = rows.iter().filter_map(|r| r.get("bytes").and_then(Value::as_u64)).sum();
        println!("{}: {} bytes", category, bytes);
        for row in rows { println!("  {} {} bytes", row.get("path").and_then(Value::as_str).unwrap_or("<unknown>"), row.get("bytes").and_then(Value::as_u64).unwrap_or(0)); }
    }
    let shared_refs: u64 = data["store"].as_array().unwrap().iter().filter(|r| r.get("retention").is_some()).filter_map(|r| r.get("bytes").and_then(Value::as_u64)).sum();
    println!("shared physical store bytes counted once; user retention reference bytes: {}", shared_refs);
    println!("Suggestions: review authorized retention, preserve boot/rollback/unknown data, and measure before/after; no deletion performed.");
}

#[cfg(test)]
mod tests { use super::*; #[test] fn fixture_has_categories() { let p=Path::new(env!("CARGO_MANIFEST_DIR")).join("../../reports/disk-situation/fixtures/fixture.json"); let v:Value=serde_json::from_str(&fs::read_to_string(p).unwrap()).unwrap(); for k in ["store","build","cache","repositories","dirty","oversized"] { assert!(v.get(k).unwrap().is_array()); } } }
