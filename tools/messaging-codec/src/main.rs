use datom_codec::{Actualizing,Budget,Composing,Datomizable,Potential};
use protos::ReaderBudget;
#[derive(Datomizable,Composing)] struct Relay { from:String, seat:String, heard:String, mode:String, recipients:Vec<String>, quote:String, context:String }
#[derive(Datomizable,Composing)] enum Ingress { MACHINE(Relay) }
fn main(){ let text=std::io::read_to_string(std::io::stdin()).unwrap(); let mut p=Potential::<Ingress>::from(text); let r=p.actualize(&mut Budget{remaining:4096,reader:ReaderBudget{remaining:4096},depth:0,maximum_depth:128}); match r { Ok(Ingress::MACHINE(x)) if x.mode=="unknown" => println!("ok"), _=>std::process::exit(2) } }
