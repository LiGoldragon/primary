use protos::{Protosizable, Textualizable, Protos, Boundary, Extent};

fn rng(state: &mut u64) -> u64 { *state ^= *state << 13; *state ^= *state >> 7; *state ^= *state << 17; *state }
const A: &[char] = &['a','\\','«','»','(',')',' ','{','}','x'];

fn main() {
    // Structurally built opaque leaves: does write-then-read return the same content?
    let mut state = 12345u64;
    let mut gbad = 0; let mut pbad = 0; let mut total = 0;
    let mut gex: Vec<String> = Vec::new(); let mut pex: Vec<String> = Vec::new();
    for _ in 0..300_000 {
        let len = (rng(&mut state) % 6) as usize;
        let content: String = (0..len).map(|_| A[(rng(&mut state) as usize) % A.len()]).collect();
        for boundary in [Boundary::Guillemets, Boundary::Parentheses] {
            total += 1;
            let node = Protos::Opaque { extent: Extent{start:0,end:0}, boundary, content: content.clone() };
            let text = node.textualize();
            let ok = match text.protosize() {
                Ok(Protos::Opaque { content: ref back, boundary: b, .. }) => b == boundary && *back == content,
                _ => false,
            };
            if !ok {
                match boundary {
                    Boundary::Guillemets => { gbad += 1; if gex.len() < 10 { gex.push(format!("{content:?} -> {text:?}")); } }
                    Boundary::Parentheses => { pbad += 1; if pex.len() < 10 { pex.push(format!("{content:?} -> {text:?}")); } }
                }
            }
        }
    }
    println!("built opaque leaves: {total} trials");
    println!("  guillemets   round-trip failures: {gbad}");
    for e in &gex { println!("    {e}"); }
    println!("  parentheses  round-trip failures: {pbad}");
    for e in &pex { println!("    {e}"); }
}
