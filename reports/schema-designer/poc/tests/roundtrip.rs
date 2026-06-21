//! rkyv round-trip under DEFAULT (daemon) features — no nota-text. Proves both
//! the help model AND the actualized typed help-tree are embeddable /
//! transmittable as binary even on a build that carries no NOTA rendering at all.

use schema_help_poc::generated::Input;
use schema_help_poc::{HelpEntry, HelpModel, HelpQuery, HelpShape, HelpTree, Name};

#[test]
fn help_model_round_trips_through_rkyv() {
    let model = Input::help_model();
    let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&model).expect("serialize help model");
    let restored: HelpModel =
        rkyv::from_bytes::<HelpModel, rkyv::rancor::Error>(&bytes).expect("deserialize help model");
    assert_eq!(model, restored);
}

#[test]
fn resolve_yields_a_typed_tree_not_a_string() {
    // The settled framing: (Help X) resolves to an actualized typed data-tree.
    let tree = Input::help_model()
        .resolve(&HelpQuery::topic(Name::from("Record")))
        .expect("known topic resolves");
    match tree {
        HelpTree::Topic(entry) => {
            assert_eq!(entry.name().as_str(), "Record");
            match entry.shape() {
                HelpShape::Structure(fields) => assert_eq!(fields.len(), 2),
                other => panic!("Record payload is a struct, got {other:?}"),
            }
        }
        HelpTree::Index(_) => panic!("a topic query yields a Topic node"),
    }
}

#[test]
fn actualized_help_tree_round_trips_through_rkyv() {
    // The typed tree itself serializes — available on the daemon build, though
    // only the client ever renders or asks for it.
    let tree: HelpTree = Input::help_model()
        .resolve(&HelpQuery::all())
        .expect("bare help resolves");
    let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&tree).expect("serialize help tree");
    let restored: HelpTree =
        rkyv::from_bytes::<HelpTree, rkyv::rancor::Error>(&bytes).expect("deserialize help tree");
    assert_eq!(tree, restored);
}

#[test]
fn bare_index_is_one_entry_per_root() {
    let tree = Input::help_model().resolve(&HelpQuery::all()).expect("resolves");
    let HelpTree::Index(entries) = tree else { panic!("bare help is an Index") };
    let names: Vec<&str> = entries.iter().map(|entry: &HelpEntry| entry.name().as_str()).collect();
    assert_eq!(
        names,
        ["State", "Record", "Observe", "Version", "Marker", "RecordAccepted", "Proposed"]
    );
}
