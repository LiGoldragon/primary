# Datom forming capability — bounded held evidence

Reported by existing controller9da2ba from held immutable2f5 source/e1 callsite verification, not a fresh76e read. Integer is maximum allowed DATOM-FORMING DEPTH for this conversion, supplied by Budget.forming_maximum_depth; not mutable remaining tokens, reader depth or composition depth. Rootdepth0; depth>=limit refuses. No downstream-wide completeness claim.

```rust
// Authored Ethos currently rejected by selected generator:
// DatomForming.[ datom_form.{ [ Branchable Integer ] [ Result<Datom Error> ] } ]
// Generated declared surface (separate from handwritten trait below):
fn datom_form<N: Branchable>(&self,input_0:N,input_1:i64)->Result<crate::Datom,crate::Error>;
enum Forming<'a> {
    Visit(&'a protos::Protos, Path, Integer),
    Enclosed(Path, bool, usize),
    Headed(Path, protos::Symbol),
}
struct Former<'a> { work: Vec<Forming<'a>>, values: Vec<Datom> }
trait FormingDatoms<'a> {
    fn form(root:&'a protos::Protos,path:Path,maximum_depth:Integer)->Result<Datom,Error>;
}
// Implementation body excerpt:
let mut former=Self{work:vec![Forming::Visit(root,path,0)],values:Vec::new()};
while let Some(work)=former.work.pop() {
    match work {
        Forming::Visit(protos,path,depth)=>{
            if depth>=maximum_depth {
                return Err(Error{layer:ErrorLayer::Datom,path,kind:ErrorKind::Budget});
            }
            // Children: path.child(index), depth+1 (source100–105).
            // Headed body: path.child(1), depth+1 (source146).
        }
        // Other assembly variants omitted from this bounded excerpt.
    }
}
impl DatomForming for protos::Protos {
    fn datom_form(&self,path:Path,maximum_depth:Integer)->Result<Datom,Error>{
        Former::form(self,path,maximum_depth)
    }
}
// Potential::actualize production consumer:
let datom=crate::DatomForming::datom_form(&protos,Path::new(),budget.forming_maximum_depth)?;
datom.compose(budget)
```

Held repo consumer kinds: handwritten declaration/implementation composition.rs6/178; production core.rs473 Potential; direct fixtures tests/core.rs333,1168 (4096 explicit test data); generated/datom-codec-kinds.rs9–15 declaration; Potential boundary fixtures core679–714(cap1refusal/cap2success). Full downstream generated consumers unproved. Source pointers composition.rs29–55,100–105,142–179; core.rs25–31,469–475. Generated and handwritten traits are distinct surfaces until proved otherwise; do not assert a single nominal identity.

Selected build failure is actual KindWanted.Integer at authored12:44; worker reports pinned Ethos06d73 deliberately rejects concrete capability inputs. No bypass/backrepin/general generator rewrite proposed. Need smallest typed forming-depth capability that preserves actual limit/path/error semantics and updates both surfaces and consumers coherently, following Core judgment.
