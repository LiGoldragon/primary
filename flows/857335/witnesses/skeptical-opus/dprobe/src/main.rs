use datom_codec::*;
use protos::{Protosizable, Textualizable};

#[derive(Datomizable, Compositional, Debug, PartialEq)]
pub struct Remark { pub author: String, pub body: String }

#[derive(Datomizable, Compositional, Debug, PartialEq)]
pub struct Pair { pub a: i64, pub b: i64 }

fn budget() -> Budget { Budget { remaining: 4096, reader: protos::ReaderBudget{remaining:4096}, depth:0, maximum_depth: 4096 } }

fn read<T: Compositional>(text: &str) -> Result<T, Error> {
    let mut p = Potential::<T>::from(text);
    let mut b = budget();
    p.actualize(&mut b)
}

fn main() {
    // 1. guillemet ascent: a String with a space and a trailing backslash
    let value = Remark { author: "Ada".into(), body: "a \\".into() };
    let text = value.datomize(Path::new()).protosize().textualize();
    println!("1 ascent text = {text:?}");
    println!("1 descent = {:?}", read::<Remark>(&text).map(|v| v.body));

    // 1b. protos level: content ending in a backslash
    let t2 = "«a \\»";
    println!("1b protosize({t2:?}) = {:?}", t2.protosize().map(|f| f.textualize()));

    // 1c. content with backslash before a guillemet
    let form = protos::Protos::Opaque { extent: protos::Extent{start:0,end:0}, boundary: protos::Boundary::Guillemets, content: "x\\\u{bb}y".into() };
    let printed = form.textualize();
    println!("1c print of content {:?} -> {:?}", "x\\\u{bb}y", printed);
    println!("1c reread = {:?}", printed.protosize().map(|f| f.textualize()));

    // 2. leading plus integer
    println!("2 {{ +42 -0 }} as Pair = {:?}", read::<Pair>("{ +42 7 }"));
    println!("2 {{ +042 7 }} as Pair = {:?}", read::<Pair>("{ +042 7 }"));

    // 3. Meaning in a String position
    println!("3 Meaning in String position = {:?}", read::<Remark>("{ Ada (the build passed (twice)) }"));

    // 4. Extent: derive vs hand impl
    let e = protos::Extent { start: 1, end: 2 };
    println!("4 protos::Extent datom text = {:?}", e.datomize(Path::new()).protosize().textualize());

    // 5. bare run with a colon in a String position (Vision example)
    println!("5 timestamp = {:?}", read::<Remark>("{ Ada 2026-09-03T17:46:20 }"));

    // 6. arity: extra position
    println!("6 extra position = {:?}", read::<Pair>("{ 1 2 3 }").is_err());
    println!("6 missing position = {:?}", read::<Pair>("{ 1 }").is_err());

    // 7. datom-level reverse projection symmetry for a dotted bare string
    let v = Remark { author: "a.b".into(), body: "Ada".into() };
    let up = v.datomize(Path::new());
    let txt = up.clone().protosize().textualize();
    let mut b = budget();
    let mut pot = Potential::<Remark>::from(txt.as_str());
    let _ : Remark = pot.actualize(&mut b).unwrap();
    let down = txt.as_str().protosize().unwrap().datomize(Path::new()).unwrap();
    println!("7 text = {txt:?}");
    println!("7 up   = {:?}", up.form);
    println!("7 down = {:?}", down.form);
    println!("7 equal = {}", up.form == down.form);
}
