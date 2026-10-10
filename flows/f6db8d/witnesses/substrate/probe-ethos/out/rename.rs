#![allow(dead_code, non_camel_case_types, non_snake_case)]
#[rustfmt::skip]
#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
pub struct A {
    pub string: String,
}
#[rustfmt::skip]
const _: () = {
    fn assert_a_clonable<T: std::clone::Clone>() {}
    let _ = assert_a_clonable::<A>;
};
