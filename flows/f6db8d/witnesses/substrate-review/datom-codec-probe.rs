//! Adversarial probes for datom-codec 0.26.1, written by the substrate-review subflow.
use datom_codec::{
    Actualizing, Budget, Compositional, Datomizable, Form, Path, Potential,
};
use protos::ReaderBudget;
use proptest::prelude::*;

fn budget() -> Budget {
    Budget { remaining: 1_000_000, reader: ReaderBudget { remaining: 1_000_000 }, depth: 0, maximum_depth: 4_096 }
}

/// The whole open chain, out and back: datomize, protosize, textualize, then
/// actualize the text into the same value.
fn survives<T>(value: &T) -> Result<T, String>
where T: Datomizable<Output = Datom> + Compositional {
    use protos::Textualizable;
    let text = value.datomize(Path::root()).protosize().textualize();
    Potential::<T>::from(text.clone()).actualize(&mut budget())
        .map_err(|error| format!("{text:?} refused {error:?}"))
}
use datom_codec::Datom;

#[derive(Debug, PartialEq, Compositional, Datomizable)]
struct Held { text: String }
#[derive(Debug, PartialEq, Compositional, Datomizable)]
struct Decimal { value: f64 }
#[derive(Debug, PartialEq, Compositional, Datomizable)]
enum Shapes { Empty, Braced {}, Parens(), One(i64), Two(i64, String) }
#[derive(Debug, PartialEq, Compositional, Datomizable)]
struct Generic<T> { held: T, also: Vec<T> }
#[derive(Debug, PartialEq, Compositional, Datomizable)]
struct SemaRecord { name: String, entries: Vec<Entry> }
#[derive(Debug, PartialEq, Compositional, Datomizable)]
struct Entry { key: String, count: i64 }

proptest! {
    #![proptest_config(ProptestConfig::with_cases(4096))]
    /// Any string at all must come back through text, backslashes included.
    #[test]
    fn any_string_position_round_trips(text in ".*") {
        let value = Held { text };
        prop_assert_eq!(survives(&value).map_err(|e| e), Ok(value));
    }
    /// Any finite decimal must come back through text.
    #[test]
    fn any_finite_decimal_round_trips(value in proptest::num::f64::NORMAL | proptest::num::f64::SUBNORMAL | proptest::num::f64::ZERO) {
        let value = Decimal { value };
        prop_assert_eq!(survives(&value).map_err(|e| e), Ok(value));
    }
}

/// Strings built only from the glyphs that decide the bare/quoted split.
#[test]
fn punctuated_strings_round_trip() {
    let alphabet = ['a', '.', ':', '!', '\\', '<', '>', '«', '»', '(', ')', ';', ' ', '{', '}'];
    let mut failures = Vec::new();
    for length in 0..=3usize {
        for mut code in 0..alphabet.len().pow(length as u32) {
            let mut text = String::new();
            for _ in 0..length { text.push(alphabet[code % alphabet.len()]); code /= alphabet.len(); }
            let value = Held { text: text.clone() };
            match survives(&value) {
                Ok(back) if back == value => {}
                other => failures.push(format!("{text:?} => {other:?}")),
            }
        }
    }
    assert!(failures.is_empty(), "{} failures: {failures:#?}", failures.len());
}

/// Every variant shape, including the two empty-field spellings.
#[test]
fn every_variant_shape_round_trips() {
    for value in [Shapes::Empty, Shapes::Braced {}, Shapes::Parens(), Shapes::One(-7), Shapes::Two(3, "a b".into())] {
        let back = survives(&value);
        assert_eq!(back.as_ref(), Ok(&value), "{value:?}");
    }
}

#[test]
fn generic_and_sema_shapes_round_trip() {
    let value = Generic { held: "a.b".to_owned(), also: vec!["x".into(), "".into()] };
    assert_eq!(survives(&value).as_ref(), Ok(&value));
    let record = SemaRecord { name: "Lock".into(), entries: vec![Entry { key: "k.v".into(), count: 0 }] };
    assert_eq!(survives(&record).as_ref(), Ok(&record));
}

/// A non-finite decimal: what does the chain do with it now that the assert is gone?
#[test]
fn non_finite_decimals_are_reported_not_silently_lost() {
    use protos::Textualizable;
    for value in [f64::NAN, f64::INFINITY, f64::NEG_INFINITY] {
        let held = Decimal { value };
        let text = held.datomize(Path::root()).protosize().textualize();
        let back = Potential::<Decimal>::from(text.clone()).actualize(&mut budget());
        println!("{value} => text {text:?} => {back:?}");
    }
}

/// A meaning form at a string position must refuse, not silently read as text.
#[test]
fn meaning_does_not_pass_as_a_string() {
    let datom = Datom { path: Path::root(), form: Form::Struct(vec![
        Datom { path: Path::root().child(0), form: Form::Meaning("x".into()) }]) };
    use datom_codec::Composable;
    let back: Result<Held, _> = datom.compose(&mut budget());
    println!("meaning at a string position => {back:?}");
    assert!(back.is_err(), "a meaning must not compose as a String");
}

/// Deeply nested composition must refuse or succeed, never blow the stack.
#[test]
fn deep_nesting_is_bounded() {
    let depth = 100_000usize;
    let text = format!("{}{}{}", "Some.".repeat(depth), "0", "");
    let mut b = budget();
    b.maximum_depth = 512;
    let result = Potential::<i64>::from(text).actualize(&mut b);
    println!("deep Some chain => {:?}", result.is_err());
}
