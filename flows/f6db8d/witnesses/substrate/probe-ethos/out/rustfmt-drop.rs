#![allow(dead_code, non_camel_case_types, non_snake_case)]
#[rustfmt::skip]
#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
pub struct B_Data {
    pub string: String,
}
#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
pub struct C_Data {
    pub integer: i64,
}
#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
pub enum A {
    B(B_Data),
    C(C_Data),
}
