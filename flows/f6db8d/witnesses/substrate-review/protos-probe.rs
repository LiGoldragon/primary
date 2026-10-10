//! Adversarial probes for protos 0.30.0, written by the substrate-review subflow.
//! The shipped suite fuzzes opaque content; these probe the bare/headed run,
//! which it does not, and the new iterative Clone/PartialEq/Debug.
use protos::{Canonicalizable, Enclosure, Extent, Protos, Protosizable, Textualizable};

const NOWHERE: Extent = Extent { start: 0, end: 0 };

/// Every text the reader accepts must print back to exactly that text.
/// Enumerated over the glyphs that decide the bare/headed split.
#[test]
fn accepted_text_reprints_itself() {
    let alphabet = ['a', '.', ':', '\\', '<', '>', '{', '}', '(', ')', '«', '»', ';', ' ', '1'];
    let mut failures = Vec::new();
    let mut checked = 0usize;
    for length in 1..=3usize {
        let total = alphabet.len().pow(length as u32);
        for mut code in 0..total {
            let mut text = String::new();
            for _ in 0..length {
                text.push(alphabet[code % alphabet.len()]);
                code /= alphabet.len();
            }
            let Ok(tree) = text.protosize() else { continue };
            checked += 1;
            let printed = tree.textualize();
            if printed != text {
                failures.push(format!("{text:?} -> {printed:?}"));
            }
        }
    }
    assert!(checked > 0);
    assert!(failures.is_empty(), "{checked} accepted; {} disagree: {failures:#?}", failures.len());
}

/// A built bare run must survive canonical print and re-read.
#[test]
fn built_bare_runs_round_trip() {
    let mut failures = Vec::new();
    for text in ["a\\b", "a\\", "\\a", "a<b", "a>b", "a;b", "a b", "", "a..b", ".a", "a."] {
        let mut form = Protos::Bare { extent: NOWHERE, text: text.to_owned() };
        form.canonicalize();
        let printed = form.textualize();
        match printed.protosize() {
            Ok(read) if read == form => {}
            Ok(read) => failures.push(format!("Bare({text:?}) wrote {printed:?} read back {read:?}")),
            Err(error) => failures.push(format!("Bare({text:?}) wrote {printed:?} refused {error:?}")),
        }
    }
    assert!(failures.is_empty(), "{failures:#?}");
}

/// A 200k-deep built tree must clone, compare and show from an explicit stack.
#[test]
fn deep_built_trees_clone_compare_and_show_without_recursion() {
    let mut tree = Protos::Bare { extent: NOWHERE, text: "leaf".into() };
    for _ in 0..200_000 {
        tree = Protos::Enclosed { extent: NOWHERE, enclosure: Enclosure::Braced, children: vec![tree] };
    }
    let copy = tree.clone();
    assert!(copy == tree, "a clone must equal its original");
    assert!(format!("{tree:?}").len() > 200_000);
    assert!(format!("{tree:#?}").len() > 200_000, "the alternate flag must not recurse");
}

/// Clone must place a head's constraints and body on the right sides.
#[test]
fn clone_preserves_constrained_heads() {
    let text = "Vector<Integer>.{ a b }";
    let tree = text.to_owned().protosize().expect("reads");
    assert_eq!(tree.clone(), tree);
    assert_eq!(tree.clone().textualize(), tree.textualize());
    assert!(matches!(&tree, Protos::Headed { constraints: Some(_), .. }));
}
