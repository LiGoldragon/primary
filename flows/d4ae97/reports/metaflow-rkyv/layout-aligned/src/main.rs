// Layout under rkyv's default (aligned) features, for comparison with
// the unaligned features Flow uses.
include!("../../types.rs");

use rkyv::rancor::Error;
use std::mem::{align_of, size_of};

fn main() {
    let record = Metaflow {
        metaflow: 1,
        kind: Kind::Voice { aspect: Aspect::Psyche, layer: Layer::Primary },
        state: State::Awake(2),
        current: 2,
        predecessor: Some(3),
        flows: 4,
        changed: 5,
    };
    let bytes = rkyv::to_bytes::<Error>(&record).unwrap();
    println!(
        "{{\"features\":\"aligned\",\"ArchivedMetaflow\":{{\"size\":{},\"align\":{},\"to_bytes\":{}}},\"ArchivedKind\":{{\"size\":{},\"align\":{}}},\"ArchivedState\":{{\"size\":{},\"align\":{}}},\"ArchivedOptionI64\":{{\"size\":{},\"align\":{}}},\"ArchivedSuccession\":{{\"size\":{},\"align\":{}}},\"fields_sum\":{}}}",
        size_of::<ArchivedMetaflow>(),
        align_of::<ArchivedMetaflow>(),
        bytes.len(),
        size_of::<ArchivedKind>(),
        align_of::<ArchivedKind>(),
        size_of::<ArchivedState>(),
        align_of::<ArchivedState>(),
        size_of::<rkyv::option::ArchivedOption<rkyv::Archived<i64>>>(),
        align_of::<rkyv::option::ArchivedOption<rkyv::Archived<i64>>>(),
        size_of::<ArchivedSuccession>(),
        align_of::<ArchivedSuccession>(),
        8 + size_of::<ArchivedKind>() + size_of::<ArchivedState>() + 8 + size_of::<rkyv::option::ArchivedOption<rkyv::Archived<i64>>>() + 8 + 8,
    );
}
