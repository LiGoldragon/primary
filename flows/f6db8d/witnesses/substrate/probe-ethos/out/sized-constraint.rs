#![allow(dead_code, non_camel_case_types, non_snake_case)]
#[rustfmt::skip]
pub trait Boxy<A: Sized> {
    fn get(&self) -> String;
}
