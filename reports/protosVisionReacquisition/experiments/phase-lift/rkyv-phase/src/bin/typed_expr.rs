use rkyv::{Archive, Deserialize, Serialize, rancor::Error};

#[derive(Archive, Serialize, Deserialize)]
#[rkyv(serialize_bounds(
    __S: rkyv::ser::Writer + rkyv::ser::Allocator,
    __S::Error: rkyv::rancor::Source,
))]
#[rkyv(deserialize_bounds(__D::Error: rkyv::rancor::Source))]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
enum Expr<T> {
    Constant {
        value: T,
    },
    If {
        #[rkyv(omit_bounds)]
        condition: Box<Expr<bool>>,
        #[rkyv(omit_bounds)]
        when_true: Box<Expr<T>>,
        #[rkyv(omit_bounds)]
        when_false: Box<Expr<T>>,
    },
}

fn main() {
    let expression = Expr::<u64>::If {
        condition: Box::new(Expr::Constant { value: true }),
        when_true: Box::new(Expr::Constant { value: 11 }),
        when_false: Box::new(Expr::Constant { value: 22 }),
    };
    let bytes = rkyv::to_bytes::<Error>(&expression).unwrap();
    let _archived = rkyv::access::<rkyv::Archived<Expr<u64>>, Error>(&bytes).unwrap();
    println!("typed-expr: recursive heterogeneous children archived after explicit bounds");
}
