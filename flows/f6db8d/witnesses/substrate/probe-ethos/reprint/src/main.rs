use ethos_zero::{Actualizing, File, Potential};
use protos::{Protosizable, Textualizable};
fn main() {
    for path in std::env::args().skip(1) {
        let text = std::fs::read_to_string(&path).unwrap();
        match Potential::<File>::from(text).actualize() {
            Ok(file) => println!("=== {path}\n{}", file.protosize().textualize()),
            Err(e) => println!("=== {path}\nERR {e:?}"),
        }
    }
}
