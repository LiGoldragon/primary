use datom_codec::{Actualizing, Budget, Potential};
use protos::ReaderBudget;
use serde::Deserialize;
use std::{
    collections::{btree_map::Entry as MapEntry, BTreeMap, BTreeSet},
    env, fs,
    path::Path,
};

#[derive(Debug, datom_codec::Composing, datom_codec::Datomizable)]
struct Request {
    host: String,
    user: String,
}

#[derive(Debug, datom_codec::Composing, datom_codec::Datomizable)]
enum Input {
    Request(Request),
}

#[derive(Debug, Deserialize)]
struct Fixture {
    host: String,
    user: String,
    store: Vec<StoreEntry>,
    build: Vec<Entry>,
    cache: Vec<Entry>,
    repositories: Vec<Entry>,
    oversized: Vec<Entry>,
}

#[derive(Debug, Deserialize)]
struct StoreEntry {
    path: String,
    bytes: u64,
    retention_users: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct Entry {
    path: String,
    bytes: u64,
    state: Option<String>,
}

#[derive(Debug)]
struct StorePath {
    bytes: u64,
    retention_users: BTreeSet<String>,
}

fn budget() -> Budget {
    Budget {
        remaining: 4096,
        reader: ReaderBudget { remaining: 4096 },
        depth: 0,
        maximum_depth: 256,
    }
}

fn main() {
    if let Err((status, message)) = run() {
        eprintln!("error: {message}");
        std::process::exit(status);
    }
}

fn run() -> Result<(), (i32, String)> {
    let mut args = env::args();
    args.next();
    let text = args.next().ok_or((
        2,
        "usage: disk-situation-report 'Request.{ host user }'".into(),
    ))?;
    if args.next().is_some() {
        return Err((2, "exactly one inline Datom argument is required".into()));
    }
    let request = match Potential::<Input>::from(text.as_str())
        .actualize(&mut budget())
        .map_err(|error| (2, format!("Datom request refused: {error:?}")))?
    {
        Input::Request(request) => request,
    };
    let fixture = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../reports/disk-situation/fixtures/fixture.json");
    let data: Fixture = serde_json::from_str(
        &fs::read_to_string(fixture)
            .map_err(|error| (1, format!("fixture unreadable: {error}")))?,
    )
    .map_err(|error| (1, format!("fixture JSON refused: {error}")))?;
    if request.host != data.host || request.user != data.user {
        return Err((
            3,
            format!(
                "no fixture dataset for host {} user {}",
                request.host, request.user
            ),
        ));
    }

    let store = deduplicated_store(&data.store).map_err(|message| (1, message))?;
    println!("Disk report for {} user {}", request.host, request.user);
    println!(
        "store: {} bytes",
        total(store.values().map(|entry| entry.bytes))?
    );
    for (path, entry) in &store {
        println!(
            "  {path} {} bytes retained_by={}",
            entry.bytes,
            entry
                .retention_users
                .iter()
                .map(String::as_str)
                .collect::<Vec<_>>()
                .join(",")
        );
    }
    print_entries("build", &data.build)?;
    print_entries("cache", &data.cache)?;
    print_entries("repositories", &data.repositories)?;
    print_entries("oversized", &data.oversized)?;
    let overlapping = data
        .oversized
        .iter()
        .filter(|entry| store.contains_key(&entry.path))
        .map(|entry| entry.path.as_str())
        .collect::<BTreeSet<_>>();
    println!(
        "oversized paths overlap store paths: {}",
        if overlapping.is_empty() {
            "none".into()
        } else {
            overlapping.into_iter().collect::<Vec<_>>().join(", ")
        }
    );
    println!(
        "requested user retention bytes: {}",
        total(
            store
                .values()
                .filter(|entry| entry.retention_users.contains(&request.user))
                .map(|entry| entry.bytes),
        )?
    );
    println!("Suggestions for {}'s agent: review authorized retention, preserve boot/rollback/unknown data, and measure before/after; no deletion performed.", request.user);
    Ok(())
}

fn deduplicated_store(rows: &[StoreEntry]) -> Result<BTreeMap<String, StorePath>, String> {
    let mut paths = BTreeMap::new();
    for row in rows {
        match paths.entry(row.path.clone()) {
            MapEntry::Vacant(slot) => {
                slot.insert(StorePath {
                    bytes: row.bytes,
                    retention_users: row.retention_users.iter().cloned().collect(),
                });
            }
            MapEntry::Occupied(mut slot) => {
                let entry = slot.get_mut();
                if entry.bytes != row.bytes {
                    return Err(format!(
                        "conflicting sizes for {}: {} and {} bytes",
                        row.path, entry.bytes, row.bytes
                    ));
                }
                entry
                    .retention_users
                    .extend(row.retention_users.iter().cloned());
            }
        }
    }
    Ok(paths)
}

fn total(mut bytes: impl Iterator<Item = u64>) -> Result<u64, (i32, String)> {
    bytes.try_fold(0u64, |sum, value| {
        sum.checked_add(value)
            .ok_or((1, "byte total overflow".into()))
    })
}

fn print_entries(category: &str, entries: &[Entry]) -> Result<(), (i32, String)> {
    println!(
        "{category}: {} bytes",
        total(entries.iter().map(|entry| entry.bytes))?
    );
    let mut ordered = entries.iter().collect::<Vec<_>>();
    ordered.sort_by(|left, right| left.path.cmp(&right.path));
    for entry in ordered {
        println!(
            "  {} {} bytes{}",
            entry.path,
            entry.bytes,
            entry
                .state
                .as_deref()
                .map(|state| format!(" state={state}"))
                .unwrap_or_default()
        );
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fixture_uses_typed_retention_users() {
        let path = Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../../reports/disk-situation/fixtures/fixture.json");
        let fixture: Fixture = serde_json::from_str(&fs::read_to_string(path).unwrap()).unwrap();
        assert!(fixture
            .store
            .iter()
            .all(|entry| !entry.retention_users.is_empty()));
    }

    #[test]
    fn requested_retention_deduplicates_paths_and_excludes_other_users() {
        let store = deduplicated_store(&[
            StoreEntry {
                path: "/a".into(),
                bytes: 10,
                retention_users: vec!["alice".into()],
            },
            StoreEntry {
                path: "/a".into(),
                bytes: 10,
                retention_users: vec!["alice".into(), "bob".into()],
            },
            StoreEntry {
                path: "/b".into(),
                bytes: 20,
                retention_users: vec!["bob".into()],
            },
        ])
        .unwrap();
        assert_eq!(
            total(
                store
                    .values()
                    .filter(|entry| entry.retention_users.contains("alice"))
                    .map(|entry| entry.bytes),
            )
            .unwrap(),
            10
        );
    }

    #[test]
    fn conflicting_store_sizes_are_rejected() {
        let error = deduplicated_store(&[
            StoreEntry {
                path: "/a".into(),
                bytes: 10,
                retention_users: vec!["alice".into()],
            },
            StoreEntry {
                path: "/a".into(),
                bytes: 20,
                retention_users: vec!["alice".into()],
            },
        ])
        .unwrap_err();
        assert_eq!(error, "conflicting sizes for /a: 10 and 20 bytes");
    }
}
