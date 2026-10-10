use datom_codec::*;
use protos::Textualizable;

fn bud() -> Budget { Budget { remaining: 1_000_000, reader: protos::ReaderBudget{remaining:1_000_000}, depth:0, maximum_depth: 4096 } }

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub enum Either<A, B> { Left(A), Right(B), Neither }

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub enum Tree { Leaf(i64), Node(Box<Tree>, Box<Tree>) }

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub struct Named { pub a: Option<Vec<Either<i64, String>>>, pub b: Result<Tree, String> }

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub enum Shadow { Some(i64), None, Ok(i64), Err(i64) }

fn round<T: Datomizable<Output=Datom> + Compositional + std::fmt::Debug + PartialEq>(l: &str, v: T) {
    let text = protos::Protosizable::protosize(&v.datomize(Path::new())).textualize();
    let mut p = Potential::<T>::from(text.clone());
    let mut b = bud();
    match p.actualize(&mut b) {
        Ok(back) => println!("  {l}: {text}  -> {}", if back==v {"SAME"} else {"*** DIFFERENT"}),
        Err(e) => println!("  {l}: {text}  -> *** ERR {:?}", e.kind),
    }
}
fn main() {
    println!("=== R1 generic / recursive / shadowing derives");
    round("Either::Left", Either::<i64,String>::Left(1));
    round("Either::Right", Either::<i64,String>::Right("x".into()));
    round("Either::Neither", Either::<i64,String>::Neither);
    round("Tree", Tree::Node(Box::new(Tree::Leaf(1)), Box::new(Tree::Node(Box::new(Tree::Leaf(2)), Box::new(Tree::Leaf(3))))));
    round("Named", Named { a: Some(vec![Either::Left(1), Either::Right("y".into()), Either::Neither]), b: Ok(Tree::Leaf(9)) });
    round("Shadow::Some", Shadow::Some(1));
    round("Shadow::None", Shadow::None);
    round("Shadow::Ok", Shadow::Ok(2));

    println!("=== R2 nested variant payload path labels vs tree position");
    let d = Tree::Node(Box::new(Tree::Leaf(1)), Box::new(Tree::Leaf(2))).datomize(Path::new());
    fn walk(d: &Datom, real: Vec<Integer>, out: &mut Vec<String>) {
        if d.path != real { out.push(format!("MISMATCH labelled {:?} actual {:?} form {:?}", d.path, real, d.form)); }
        match &d.form {
            Form::Struct(c) | Form::Vector(c) => for (i, ch) in c.iter().enumerate() { let mut r = real.clone(); r.push(i as Integer); walk(ch, r, out); },
            Form::Variant(_, b) => { let mut r = real.clone(); r.push(1); walk(b, r, out); },
            _ => {}
        }
    }
    let mut out = Vec::new(); walk(&d, vec![], &mut out);
    println!("  Tree::Node derived: {} mismatches", out.len()); for m in &out { println!("    {m}"); }
    let e = protos::Extent{start:3,end:7}.datomize(Path::new());
    let mut out = Vec::new(); walk(&e, vec![], &mut out);
    println!("  protos::Extent hand-written: {} mismatches", out.len()); for m in &out { println!("    {m}"); }
    let er = datom_codec::Error{ layer: ErrorLayer::Datom, path: vec![1], kind: ErrorKind::Budget }.datomize(Path::new());
    let mut out = Vec::new(); walk(&er, vec![], &mut out);
    println!("  datom_codec::Error hand-written: {} mismatches", out.len()); for m in &out { println!("    {m}"); }
    println!("  Error text: {}", protos::Protosizable::protosize(&er).textualize());
}
