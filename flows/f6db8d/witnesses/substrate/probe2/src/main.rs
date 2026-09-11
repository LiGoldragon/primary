use datom_codec::*;
use protos::Textualizable;

fn b(remaining: Integer) -> Budget {
    Budget { remaining, reader: protos::ReaderBudget { remaining: 10_000_000 }, depth: 0, maximum_depth: 256 }
}

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub enum Flag { On, Off }

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub enum Odd { Unit, Empty(), Named {}, One(i64), Two(i64, String) }

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub struct Pair<T>(pub T, pub Vec<T>);

#[derive(Debug, PartialEq, Datomizable, Compositional)]
pub struct Nest { pub inner: Pair<i64>, pub flag: Flag, pub opt: Option<Box<Nest>> }

fn round<T: Datomizable<Output=Datom> + Compositional + std::fmt::Debug + PartialEq>(label: &str, v: T) {
    let text = protos::Protosizable::protosize(&v.datomize(Path::new())).textualize();
    let mut p = Potential::<T>::from(text.clone());
    let mut bud = b(1_000_000);
    match p.actualize(&mut bud) {
        Ok(back) => println!("  {label}: {text:?} -> {}", if back == v {"SAME".to_string()} else {format!("*** DIFFERENT {back:?}")}),
        Err(e) => println!("  {label}: {text:?} -> *** ERR {e:?}"),
    }
}

fn main() {
    println!("=== Q1: derive round-trips");
    round("Flag::On", Flag::On);
    round("Odd::Unit", Odd::Unit);
    round("Odd::Empty()", Odd::Empty());
    round("Odd::Named{}", Odd::Named{});
    round("Odd::One", Odd::One(7));
    round("Odd::Two", Odd::Two(7, "x".into()));
    round("Pair<i64>", Pair(1i64, vec![2i64,3]));
    round("Nest", Nest{ inner: Pair(1, vec![2]), flag: Flag::Off, opt: Some(Box::new(Nest{ inner: Pair(3, vec![]), flag: Flag::On, opt: None })) });

    println!("=== Q2: composition budget bypass on derived bare variants");
    let many: Vec<Flag> = (0..10_000).map(|_| Flag::On).collect();
    let text = protos::Protosizable::protosize(&many.datomize(Path::new())).textualize();
    let mut bud = b(5);
    let mut p = Potential::<Vec<Flag>>::from(text.clone());
    println!("  10000 bare variants, budget.remaining = 5 -> {:?}", p.actualize(&mut bud).map(|v| v.len()));
    println!("  budget left after: {}", bud.remaining);
    let many2: Vec<i64> = (0..10_000).collect();
    let text2 = protos::Protosizable::protosize(&many2.datomize(Path::new())).textualize();
    let mut bud2 = b(5);
    let mut p2 = Potential::<Vec<i64>>::from(text2);
    println!("  10000 integers,      budget.remaining = 5 -> {:?}", p2.actualize(&mut bud2).map(|v| v.len()).map_err(|e| e.kind));

    println!("=== Q3: protos reader depth / budget");
    let deep = format!("{}{}", "{ ".repeat(300), "}".repeat(300));
    println!("  300 nested braces -> {:?}", protos::Protosizable::protosize(deep.as_str()).map(|_|"OK").map_err(|e| e.problem));
    let deep2 = format!("{}{}", "{ ".repeat(255), "}".repeat(255));
    println!("  255 nested braces -> {:?}", protos::Protosizable::protosize(deep2.as_str()).map(|_|"OK").map_err(|e| e.problem));
    let wide = format!("[ {}]", "0 ".repeat(5000));
    println!("  5000 wide (default 4096 budget) -> {:?}", protos::Protosizable::protosize(wide.as_str()).map(|_|"OK").map_err(|e| e.problem));

    println!("=== Q4: composition depth stack safety");
    let n = 5000;
    let deep = format!("{}{}", "Some.".repeat(n), "None");
    let mut bud = Budget { remaining: 10_000_000, reader: protos::ReaderBudget{remaining:10_000_000}, depth: 0, maximum_depth: 1_000_000 };
    let mut p = Potential::<i64>::from(deep.clone());
    println!("  {n} Some. heads, maximum_depth 1e6 -> {:?}", std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| p.actualize(&mut bud).map(|_|"OK").map_err(|e| format!("{:?}", e.kind)))));

    println!("=== Q5: non-canonical but accepted texts");
    for t in ["{a b}", "{  a   b  }", "[]", "{ }", "«»", "()"] {
        match protos::Protosizable::protosize(t) {
            Ok(p) => println!("  {t:?} -> canonical {:?}", p.textualize()),
            Err(e) => println!("  {t:?} -> ERR {:?}", e.problem),
        }
    }

    println!("=== Q6: Option None spelling");
    for t in ["None", "Some.42"] {
        let mut bud = b(1000);
        let mut p = Potential::<Option<i64>>::from(t.to_string());
        println!("  {t:?} -> {:?}", p.actualize(&mut bud).map_err(|e| e.kind));
    }
    println!("=== Q7: integer canonicality");
    for t in ["0", "-0", "007", "+4", "9223372036854775808"] {
        let mut bud = b(1000);
        let mut p = Potential::<i64>::from(t.to_string());
        println!("  {t:?} -> {:?}", p.actualize(&mut bud).map_err(|e| e.kind));
    }
}
