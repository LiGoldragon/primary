//! The random-text fixpoint probe cited in the report at section 2.1:
//! 48 557 accepted texts, zero print/reparse instabilities, and
//! Canonicalizable::canonicalize agreeing exactly with a fresh parse
//! of the canonical text in every case. Run with --release.
use protos::{Protosizable, Textualizable, Canonicalizable};

fn rng(state: &mut u64) -> u64 { *state ^= *state << 13; *state ^= *state >> 7; *state ^= *state << 17; *state }

const ALPHABET: &[char] = &['a','B','0','9','-','.','!',':','{','}','[',']','<','>','«','»','(',')',';',' ','\\','\n','_','\u{e9}'];

fn main() {
    let mut state = 0x2545F4914F6CDD1Du64;
    let mut parsed = 0; let mut unstable = 0; let mut extent_bad = 0;
    let mut examples: Vec<(String,String,String)> = Vec::new();
    for _ in 0..400_000 {
        let len = (rng(&mut state) % 12 + 1) as usize;
        let text: String = (0..len).map(|_| ALPHABET[(rng(&mut state) as usize) % ALPHABET.len()]).collect();
        let Ok(first) = text.protosize() else { continue };
        parsed += 1;
        let printed = first.textualize();
        match printed.protosize() {
            Ok(second) => {
                if printed != second.textualize() {
                    unstable += 1;
                    if examples.len() < 8 { examples.push((text.clone(), printed.clone(), second.textualize())); }
                } else {
                    let mut c = first.clone(); c.canonicalize();
                    if c != second { extent_bad += 1; }
                }
            }
            Err(e) => {
                unstable += 1;
                if examples.len() < 8 { examples.push((text.clone(), printed.clone(), format!("PARSE ERR {:?}", e.problem))); }
            }
        }
    }
    println!("parsed {parsed}, print/reparse unstable {unstable}, canonicalize != reparse {extent_bad}");
    for (t,p,q) in &examples { println!("  src {t:?}\n    printed {p:?}\n    reprinted {q}"); }
}
