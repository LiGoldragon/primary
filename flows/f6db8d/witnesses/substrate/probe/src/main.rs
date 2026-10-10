use datom_codec::*;
use protos::{Boundary, Protos, Protosizable, Textualizable};

fn budget() -> Budget {
    Budget { remaining: 1_000_000, reader: protos::ReaderBudget { remaining: 1_000_000 }, depth: 0, maximum_depth: 256 }
}

fn show(label: &str, s: &str) {
    match s.protosize() {
        Ok(p) => println!("{label}: parse OK -> {:?}\n      reprint {:?}", p, p.textualize()),
        Err(e) => println!("{label}: parse ERR {:?}", e),
    }
}

fn main() {
    println!("=== P1: guillemet writer does not escape backslash");
    for content in ["a b\\", "a\\\u{BB}b", "x\\"] {
        let node = Protos::Opaque { extent: protos::Extent{start:0,end:0}, boundary: Boundary::Guillemets, content: content.to_string() };
        let text = node.textualize();
        print!("  content {:?} -> text {:?} -> ", content, text);
        match text.protosize() {
            Ok(p) => println!("reparse {:?}", p),
            Err(e) => println!("reparse ERR {:?}", e),
        }
    }
    println!("  (parentheses, for contrast)");
    for content in ["a b\\", "a\\)b", "x\\"] {
        let node = Protos::Opaque { extent: protos::Extent{start:0,end:0}, boundary: Boundary::Parentheses, content: content.to_string() };
        let text = node.textualize();
        print!("  content {:?} -> text {:?} -> ", content, text);
        match text.protosize() {
            Ok(p) => println!("reparse {:?}", p),
            Err(e) => println!("reparse ERR {:?}", e),
        }
    }

    println!("=== P2: String round-trip through the full ascent/descent");
    for s in ["a b\\", "a\\\u{BB}b", "plain", "a.b", "a:b", "no such file: { } is content"] {
        let d = s.to_string().datomize(Path::new());
        let text = protos::Protosizable::protosize(&d).textualize();
        let mut potential = Potential::<String>::from(text.clone());
        let mut b = budget();
        match potential.actualize(&mut b) {
            Ok(back) => println!("  {:?} -> {:?} -> {:?} {}", s, text, back, if back==s {"SAME"} else {"*** DIFFERENT ***"}),
            Err(e) => println!("  {:?} -> {:?} -> ERR {:?}  *** FAILED ***", s, text, e),
        }
    }

    println!("=== P3: MissingHead reachability");
    for t in [".foo", "..", "a..b", ".{ }", ".", "a.", "a. b"] { show(&format!("  {t:?}"), t); }

    println!("=== P4: angle constraints without a following separator");
    for t in ["Vector<Integer>", "[ Scores.Vector<Integer> ]", "Foo<Bar>.{ x }"] { show(&format!("  {t:?}"), t); }

    println!("=== P5: decimal recognised by structure, not position");
    for t in ["3.14", "-0.5", "3.14.15", "1.x"] {
        let p = t.protosize().unwrap();
        println!("  {t:?} protos {:?}", p);
        println!("        datom  {:?}", Datomizable::datomize(&p, Path::new()));
    }

    println!("=== P6: f64 ascent panics on non-finite (catch_unwind)");
    let r = std::panic::catch_unwind(|| f64::NAN.datomize(Path::new()));
    println!("  NAN.datomize -> {}", if r.is_err() {"PANIC"} else {"ok"});
    let r = std::panic::catch_unwind(|| <String as Compositional>::from_positions(
        Datom{path:Path::new(), form:Form::Struct(vec![])}.positions("Struct").unwrap(), &mut budget()));
    println!("  String::from_positions -> {}", if r.is_err() {"PANIC"} else {"ok"});

    println!("=== P7: Meaning accepted in a String position (lossy)");
    let mut b = budget();
    let mut potential = Potential::<String>::from("(a (b) c)".to_string());
    match potential.actualize(&mut b) {
        Ok(s) => {
            let back = protos::Protosizable::protosize(&s.datomize(Path::new())).textualize();
            println!("  \"(a (b) c)\" as String -> {:?} -> retextualized {:?}", s, back);
        }
        Err(e) => println!("  ERR {:?}", e),
    }

    println!("=== P8: datomize path labels vs tree position");
    let e = protos::Extent { start: 3, end: 7 };
    let d = e.datomize(vec![]);
    println!("  Extent datom: {:#?}", d);
    println!("  text: {}", protos::Protosizable::protosize(&d).textualize());
}
