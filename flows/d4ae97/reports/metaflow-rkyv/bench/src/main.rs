// Metaflow record: fixed-width vs vectored, under the rkyv and redb
// versions and features Flow uses today. Prints one JSON object.
include!("../../types.rs");

use redb::{Database, Durability, ReadableDatabase, ReadableTable, ReadableTableMetadata, TableDefinition};
use rkyv::munge::munge;
use rkyv::option::ArchivedOption;
use rkyv::rancor::Error;
use std::collections::BTreeSet;
use std::hint::black_box;
use std::mem::{align_of, size_of};
use std::time::Instant;

const TABLE: TableDefinition<i64, &[u8]> = TableDefinition::new("metaflows");

struct Random(u64);
impl Random {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

fn kind(r: &mut Random) -> Kind {
    let layer = match r.below(4) {
        0 => Layer::Primary,
        1 => Layer::Secondary,
        2 => Layer::Tertiary,
        _ => Layer::Quaternary,
    };
    match r.below(4) {
        0 => Kind::Implementation { layer },
        1 => Kind::Voice { aspect: Aspect::Psyche, layer },
        2 => Kind::Voice { aspect: Aspect::Mind, layer },
        _ => Kind::Voice { aspect: Aspect::Field, layer },
    }
}

fn fixed(r: &mut Random, id: i64) -> Metaflow {
    let current = (r.next() & 0xFF_FFFF) as i64;
    Metaflow {
        metaflow: id,
        kind: kind(r),
        state: match r.below(3) {
            0 => State::Awake(current),
            1 => State::Asleep,
            _ => State::Ended,
        },
        current,
        predecessor: if r.below(5) == 0 { None } else { Some((r.next() & 0xFF_FFFF) as i64) },
        flows: r.below(1000) as i64,
        changed: 1_791_000_000 + r.below(10_000_000) as i64,
    }
}

fn vectored(r: &mut Random, id: i64, past_max: u64) -> MetaflowVectored {
    let len = r.below(past_max + 1) as usize;
    MetaflowVectored {
        metaflow: id,
        kind: kind(r),
        name: ["flowRefresh", "ethosDesign", "metaflowRecordBench"][r.below(3) as usize].to_string(),
        state: State::Awake((r.next() & 0xFF_FFFF) as i64),
        past: (0..len).map(|_| (r.next() & 0xFF_FFFF) as i64).collect(),
    }
}

fn hex6(r: &mut Random) -> String {
    format!("{:06x}", r.next() & 0xFF_FFFF)
}

fn words(r: &mut Random) -> String {
    let w = ["start", "Input", "Vital", "zoo", "Wrong", "Youth", "about", "Blanket", "Boat"];
    format!("{}{}{}", w[r.below(3) as usize], w[3 + r.below(3) as usize], w[6 + r.below(3) as usize])
}

fn ns(start: Instant, count: usize) -> f64 {
    start.elapsed().as_nanos() as f64 / count as f64
}

fn lengths<T, F: FnMut(&mut Random, i64) -> T>(n: usize, mut make: F) -> (BTreeSet<usize>, f64)
where
    T: for<'a> rkyv::Serialize<
        rkyv::api::high::HighSerializer<rkyv::util::AlignedVec, rkyv::ser::allocator::ArenaHandle<'a>, Error>,
    >,
{
    let mut r = Random(0x9E37_79B9_7F4A_7C15);
    let mut set = BTreeSet::new();
    let mut total = 0usize;
    for i in 0..n {
        let len = rkyv::to_bytes::<Error>(&make(&mut r, i as i64)).unwrap().len();
        total += len;
        set.insert(len);
    }
    (set, total as f64 / n as f64)
}

fn set_json(set: &BTreeSet<usize>) -> String {
    let v: Vec<String> = set.iter().take(6).map(|x| x.to_string()).collect();
    format!("{{\"distinct\":{},\"min\":{},\"max\":{},\"first\":[{}]}}",
        set.len(), set.iter().next().unwrap(), set.iter().last().unwrap(), v.join(","))
}

fn field_offset(record: &ArchivedMetaflow) -> (usize, usize) {
    let base = record as *const _ as usize;
    (
        &record.current as *const _ as usize - base,
        &record.flows as *const _ as usize - base,
    )
}

fn scale(n: usize, out: &mut Vec<String>, db_dir: &std::path::Path) {
    let mut r = Random(0xD1B5_4A32_D192_ED03 ^ n as u64);
    // Sparse ids, shuffled, so no id equals its position.
    let mut ids: Vec<i64> = (0..n as i64).map(|i| i * 7 + 3).collect();
    for i in (1..n).rev() {
        ids.swap(i, r.below(i as u64 + 1) as usize);
    }
    let records: Vec<Metaflow> = ids.iter().map(|&id| fixed(&mut r, id)).collect();
    let size = size_of::<ArchivedMetaflow>();

    // 1. Concatenate independently archived records.
    let t = Instant::now();
    let mut series: Vec<u8> = Vec::with_capacity(n * size);
    for rec in &records {
        series.extend_from_slice(&rkyv::to_bytes::<Error>(rec).unwrap());
    }
    let build_ns = ns(t, n);
    assert_eq!(series.len(), n * size);

    // 2. Every slot [i*size, (i+1)*size) validates and round-trips.
    let t = Instant::now();
    for (i, rec) in records.iter().enumerate() {
        let a = rkyv::access::<ArchivedMetaflow, Error>(&series[i * size..(i + 1) * size]).unwrap();
        let back: Metaflow = rkyv::deserialize::<Metaflow, Error>(a).unwrap();
        assert_eq!(&back, rec);
    }
    let validate_ns = ns(t, n);

    // 3. The series equals the element block of one archived Vec<Metaflow>.
    let whole = rkyv::to_bytes::<Error>(&records).unwrap();
    let identical = whole[..n * size] == series[..];
    let vec_overhead = whole.len() - n * size;

    // The whole series as a slice, checked once.
    let t = Instant::now();
    let slice = rkyv::access::<rkyv::Archived<Vec<Metaflow>>, Error>(&whole).unwrap().as_slice();
    let check_all_ms = t.elapsed().as_secs_f64() * 1e3;

    let queries: Vec<i64> = (0..100_000).map(|_| ids[r.below(n as u64) as usize]).collect();

    // 4a. Linear scan.
    let linear_q = if n >= 1_000_000 { 200 } else { 10_000 };
    let t = Instant::now();
    let mut hit = 0i64;
    for q in &queries[..linear_q] {
        let found = slice.iter().find(|m| m.metaflow.to_native() == *q).unwrap();
        hit += found.current.to_native();
    }
    let linear_ns = ns(t, linear_q);
    black_box(hit);

    // 4b. Sorted, binary search on the archived slice.
    let mut sorted_records = records.clone();
    sorted_records.sort_by_key(|m| m.metaflow);
    let sorted_bytes = rkyv::to_bytes::<Error>(&sorted_records).unwrap();
    let sorted = rkyv::access::<rkyv::Archived<Vec<Metaflow>>, Error>(&sorted_bytes).unwrap().as_slice();
    let t = Instant::now();
    let mut hit = 0i64;
    for q in &queries {
        let i = sorted.binary_search_by_key(q, |m| m.metaflow.to_native()).unwrap();
        hit += sorted[i].current.to_native();
    }
    let binary_ns = ns(t, queries.len());
    black_box(hit);

    // 4c. Dense ordinal ids: offset = i * size, no search at all.
    let t = Instant::now();
    let mut hit = 0i64;
    for q in &queries {
        let i = ((q - 3) / 7) as usize; // position when ids are ordinals
        let a = unsafe { rkyv::access_unchecked::<ArchivedMetaflow>(&series[i * size..(i + 1) * size]) };
        hit += a.current.to_native();
    }
    let direct_ns = ns(t, queries.len());
    black_box(hit);

    // 4d. redb, as Sema stores it: key -> archived bytes.
    let path = db_dir.join(format!("fixed-{n}.redb"));
    let _ = std::fs::remove_file(&path);
    let db = Database::create(&path).unwrap();
    let t = Instant::now();
    {
        let mut w = db.begin_write().unwrap();
        w.set_durability(Durability::Immediate).unwrap();
        {
            let mut table = w.open_table(TABLE).unwrap();
            for (i, rec) in records.iter().enumerate() {
                table.insert(rec.metaflow, &series[i * size..(i + 1) * size]).unwrap();
            }
        }
        w.commit().unwrap();
    }
    let redb_load_ns = ns(t, n);
    let read = db.begin_read().unwrap();
    let table = read.open_table(TABLE).unwrap();
    let t = Instant::now();
    let mut hit = 0i64;
    for q in &queries {
        let g = table.get(*q).unwrap().unwrap();
        let a = rkyv::access::<ArchivedMetaflow, Error>(g.value()).unwrap();
        hit += a.current.to_native();
    }
    let redb_access_ns = ns(t, queries.len());
    let t = Instant::now();
    for q in &queries {
        let g = table.get(*q).unwrap().unwrap();
        let m: Metaflow = rkyv::from_bytes::<Metaflow, Error>(g.value()).unwrap();
        hit += m.current;
    }
    let redb_decode_ns = ns(t, queries.len());
    // A query over the series: count Awake metaflows.
    let t = Instant::now();
    let mut awake_redb = 0usize;
    for entry in table.iter().unwrap() {
        let (_, v) = entry.unwrap();
        let m: Metaflow = rkyv::from_bytes::<Metaflow, Error>(v.value()).unwrap();
        if matches!(m.state, State::Awake(_)) {
            awake_redb += 1;
        }
    }
    let redb_scan_ms = t.elapsed().as_secs_f64() * 1e3;
    let t = Instant::now();
    let awake_slice = slice.iter().filter(|m| matches!(m.state, ArchivedState::Awake(_))).count();
    let slice_scan_ms = t.elapsed().as_secs_f64() * 1e3;
    assert_eq!(awake_redb, awake_slice);
    black_box(hit);
    drop(table);
    drop(read);

    // 5. Update in place.
    let (off_current, off_flows) = field_offset(slice.first().unwrap());
    let updates: Vec<(usize, i64)> = (0..100_000).map(|_| (r.below(n as u64) as usize, (r.next() & 0xFF_FFFF) as i64)).collect();
    let t = Instant::now();
    for &(i, flow) in &updates {
        let seal = rkyv::access_mut::<ArchivedMetaflow, Error>(&mut series[i * size..(i + 1) * size]).unwrap();
        munge!(let ArchivedMetaflow { mut current, mut flows, .. } = seal);
        *current = <rkyv::Archived<i64>>::from_native(flow);
        let f = flows.to_native();
        *flows = <rkyv::Archived<i64>>::from_native(f + 1);
    }
    let seal_ns = ns(t, updates.len());
    let t = Instant::now();
    for &(i, flow) in &updates {
        let at = i * size + off_current;
        series[at..at + 8].copy_from_slice(&flow.to_le_bytes());
    }
    let raw_ns = ns(t, updates.len());
    let (i, flow) = *updates.last().unwrap();
    let a = rkyv::access::<ArchivedMetaflow, Error>(&series[i * size..(i + 1) * size]).unwrap();
    assert_eq!(a.current.to_native(), flow);

    // redb update, patch bytes vs Sema's decode/encode, one transaction.
    let redb_update = |patch: bool| -> f64 {
        let t = Instant::now();
        let mut w = db.begin_write().unwrap();
        w.set_durability(Durability::Immediate).unwrap();
        {
            let mut table = w.open_table(TABLE).unwrap();
            for &(i, flow) in &updates[..20_000] {
                let id = ids[i];
                let mut bytes = table.get(id).unwrap().unwrap().value().to_vec();
                if patch {
                    bytes[off_current..off_current + 8].copy_from_slice(&flow.to_le_bytes());
                    table.insert(id, bytes.as_slice()).unwrap();
                } else {
                    let mut m: Metaflow = rkyv::from_bytes::<Metaflow, Error>(&bytes).unwrap();
                    m.current = flow;
                    m.flows += 1;
                    let out = rkyv::to_bytes::<Error>(&m).unwrap();
                    table.insert(id, out.as_slice()).unwrap();
                }
            }
        }
        w.commit().unwrap();
        ns(t, 20_000)
    };
    redb_update(true);
    redb_update(false);
    let redb_patch_ns = redb_update(true);
    let redb_reencode_ns = redb_update(false);
    let redb_bytes = {
        let rt = db.begin_read().unwrap();
        let t = rt.open_table(TABLE).unwrap();
        t.stats().unwrap().stored_bytes()
    };
    drop(db);
    let _ = std::fs::remove_file(&path);

    // 6. The vectored record, same scale, past 0..=16 flows.
    let vrecords: Vec<MetaflowVectored> = ids.iter().map(|&id| vectored(&mut r, id, 16)).collect();
    let vbytes: Vec<rkyv::util::AlignedVec> = vrecords.iter().map(|m| rkyv::to_bytes::<Error>(m).unwrap()).collect();
    let vtotal: usize = vbytes.iter().map(|b| b.len()).sum();
    let vlens: BTreeSet<usize> = vbytes.iter().map(|b| b.len()).collect();
    // A concatenation needs an offsets vector; without it slot i is unknown.
    let mut offsets: Vec<u32> = Vec::with_capacity(n + 1);
    let mut vseries: Vec<u8> = Vec::with_capacity(vtotal);
    for b in &vbytes {
        offsets.push(vseries.len() as u32);
        vseries.extend_from_slice(b);
    }
    offsets.push(vseries.len() as u32);
    let stride_guess_fails = (1..n.min(1000))
        .filter(|&i| rkyv::access::<ArchivedMetaflowVectored, Error>(&vseries[i * (vtotal / n)..(i + 1) * (vtotal / n)]).is_err())
        .count();
    let vpath = db_dir.join(format!("vectored-{n}.redb"));
    let _ = std::fs::remove_file(&vpath);
    let vdb = Database::create(&vpath).unwrap();
    {
        let w = vdb.begin_write().unwrap();
        {
            let mut table = w.open_table(TABLE).unwrap();
            for (m, b) in vrecords.iter().zip(&vbytes) {
                table.insert(m.metaflow, b.as_slice()).unwrap();
            }
        }
        w.commit().unwrap();
    }
    let read = vdb.begin_read().unwrap();
    let table = read.open_table(TABLE).unwrap();
    let t = Instant::now();
    let mut hit = 0i64;
    for q in &queries {
        let g = table.get(*q).unwrap().unwrap();
        let a = rkyv::access::<ArchivedMetaflowVectored, Error>(g.value()).unwrap();
        if let ArchivedState::Awake(f) = &a.state {
            hit += f.to_native();
        }
    }
    let vredb_access_ns = ns(t, queries.len());
    let t = Instant::now();
    for q in &queries {
        let g = table.get(*q).unwrap().unwrap();
        let m: MetaflowVectored = rkyv::from_bytes::<MetaflowVectored, Error>(g.value()).unwrap();
        hit += m.past.len() as i64;
    }
    let vredb_decode_ns = ns(t, queries.len());
    black_box(hit);
    drop(table);
    drop(read);
    let t = Instant::now();
    {
        let w = vdb.begin_write().unwrap();
        {
            let mut table = w.open_table(TABLE).unwrap();
            for &(i, flow) in &updates[..20_000] {
                let id = ids[i];
                let bytes = table.get(id).unwrap().unwrap().value().to_vec();
                let mut m: MetaflowVectored = rkyv::from_bytes::<MetaflowVectored, Error>(&bytes).unwrap();
                m.past.push(match m.state { State::Awake(f) => f, _ => 0 });
                m.state = State::Awake(flow);
                let out = rkyv::to_bytes::<Error>(&m).unwrap();
                table.insert(id, out.as_slice()).unwrap();
            }
        }
        w.commit().unwrap();
    }
    let vredb_update_ns = ns(t, 20_000);
    let vredb_bytes = {
        let rt = vdb.begin_read().unwrap();
        let t = rt.open_table(TABLE).unwrap();
        t.stats().unwrap().stored_bytes()
    };
    drop(vdb);
    let _ = std::fs::remove_file(&vpath);

    out.push(format!(
        "{{\"n\":{n},\"fixed\":{{\"size\":{size},\"series_bytes\":{},\"archive_ns\":{build_ns:.1},\"validate_roundtrip_ns\":{validate_ns:.1},\"series_equals_vec_elements\":{identical},\"vec_overhead_bytes\":{vec_overhead},\"check_whole_ms\":{check_all_ms:.2},\"linear_ns\":{linear_ns:.0},\"linear_queries\":{linear_q},\"binary_ns\":{binary_ns:.1},\"direct_ns\":{direct_ns:.1},\"redb_load_ns\":{redb_load_ns:.0},\"redb_access_ns\":{redb_access_ns:.0},\"redb_decode_ns\":{redb_decode_ns:.0},\"redb_scan_awake_ms\":{redb_scan_ms:.1},\"slice_scan_awake_ms\":{slice_scan_ms:.2},\"awake\":{awake_slice},\"offset_current\":{off_current},\"offset_flows\":{off_flows},\"update_seal_ns\":{seal_ns:.1},\"update_raw_ns\":{raw_ns:.1},\"redb_update_patch_ns\":{redb_patch_ns:.0},\"redb_update_reencode_ns\":{redb_reencode_ns:.0},\"redb_stored_bytes\":{redb_bytes}}},\"vectored\":{{\"past_max\":16,\"mean_bytes\":{:.1},\"lengths\":{},\"offsets_bytes\":{},\"stride_guess_failures_of_999\":{stride_guess_fails},\"redb_access_ns\":{vredb_access_ns:.0},\"redb_decode_ns\":{vredb_decode_ns:.0},\"redb_append_update_ns\":{vredb_update_ns:.0},\"redb_stored_bytes\":{vredb_bytes}}}}}",
        series.len(),
        vtotal as f64 / n as f64,
        set_json(&vlens),
        offsets.len() * 4,
    ));
}

fn main() {
    let db_dir = std::path::PathBuf::from(std::env::args().nth(1).expect("db dir"));
    std::fs::create_dir_all(&db_dir).unwrap();

    let sample = Metaflow {
        metaflow: 1,
        kind: Kind::Voice { aspect: Aspect::Psyche, layer: Layer::Primary },
        state: State::Awake(2),
        current: 2,
        predecessor: Some(3),
        flows: 4,
        changed: 5,
    };
    let sample_bytes = rkyv::to_bytes::<Error>(&sample).unwrap();
    let opt = size_of::<ArchivedOption<rkyv::Archived<i64>>>();
    let layout = format!(
        "{{\"features\":\"unaligned\",\"ArchivedMetaflow\":{{\"size\":{},\"align\":{},\"to_bytes\":{}}},\"ArchivedKind\":{{\"size\":{},\"align\":{}}},\"ArchivedState\":{{\"size\":{},\"align\":{}}},\"ArchivedOptionI64\":{{\"size\":{opt},\"align\":{}}},\"ArchivedSuccession\":{{\"size\":{},\"align\":{}}},\"ArchivedString\":{{\"size\":{}}},\"ArchivedVecI64\":{{\"size\":{}}},\"fields_sum\":{}}}",
        size_of::<ArchivedMetaflow>(),
        align_of::<ArchivedMetaflow>(),
        sample_bytes.len(),
        size_of::<ArchivedKind>(),
        align_of::<ArchivedKind>(),
        size_of::<ArchivedState>(),
        align_of::<ArchivedState>(),
        align_of::<ArchivedOption<rkyv::Archived<i64>>>(),
        size_of::<ArchivedSuccession>(),
        align_of::<ArchivedSuccession>(),
        size_of::<rkyv::string::ArchivedString>(),
        size_of::<rkyv::vec::ArchivedVec<rkyv::Archived<i64>>>(),
        8 + size_of::<ArchivedKind>() + size_of::<ArchivedState>() + 8 + opt + 8 + 8,
    );

    // Archive length across a million random records of each shape.
    let (fixed_lens, _) = lengths(1_000_000, |r, i| fixed(r, i));
    let (hex_lens, hex_mean) = lengths(1_000_000, |r, i| MetaflowStringIds {
        metaflow: i,
        kind: kind(r),
        awake: r.below(2) == 0,
        current: hex6(r),
        predecessor: Some(hex6(r)),
        flows: 1,
        changed: 2,
    });
    let (word_lens, word_mean) = lengths(1_000_000, |r, i| MetaflowStringIds {
        metaflow: i,
        kind: kind(r),
        awake: r.below(2) == 0,
        current: words(r),
        predecessor: if r.below(2) == 0 { None } else { Some(words(r)) },
        flows: 1,
        changed: 2,
    });
    let (vec_lens, vec_mean) = lengths(1_000_000, |r, i| vectored(r, i, 16));
    let (proposed_lens, _) = lengths(1_000_000, |r, i| {
        let m = fixed(r, i);
        MetaflowProposed {
            metaflow: m.metaflow,
            kind: m.kind,
            state: match m.state { State::Awake(_) => Wakefulness::Awake, State::Asleep => Wakefulness::Asleep, State::Ended => Wakefulness::Ended },
            current: m.current,
            predecessor: m.predecessor,
            flows: m.flows,
            changed: m.changed,
        }
    });
    let (succession_lens, _) = lengths(1_000_000, |r, i| Succession { metaflow: i, ordinal: r.below(100) as i64, flow: (r.next() & 0xFF_FFFF) as i64, started: r.next() as i64 >> 4 });
    let mut vec_growth = Vec::new();
    for past in [0usize, 1, 2, 4, 8, 16, 64, 256, 1024] {
        let m = MetaflowVectored {
            metaflow: 1,
            kind: Kind::Voice { aspect: Aspect::Psyche, layer: Layer::Primary },
            name: "ethosDesign".into(),
            state: State::Asleep,
            past: vec![7; past],
        };
        vec_growth.push(format!("[{past},{}]", rkyv::to_bytes::<Error>(&m).unwrap().len()));
    }

    let mut scales = Vec::new();
    for n in [10_000usize, 1_000_000] {
        scale(n, &mut scales, &db_dir);
    }

    println!(
        "{{\"rkyv\":\"0.8.18\",\"redb\":\"4.3.0\",\"layout\":{layout},\"constancy\":{{\"proposed\":{},\"proposed_size_of\":{},\"succession\":{},\"fixed\":{},\"string_ids_hex6\":{},\"string_ids_hex6_mean\":{hex_mean:.1},\"string_ids_words\":{},\"string_ids_words_mean\":{word_mean:.1},\"vectored_past_0_16\":{},\"vectored_mean\":{vec_mean:.1},\"vectored_growth\":[{}]}},\"scales\":[{}]}}",
        set_json(&proposed_lens),
        size_of::<ArchivedMetaflowProposed>(),
        set_json(&succession_lens),
        set_json(&fixed_lens),
        set_json(&hex_lens),
        set_json(&word_lens),
        set_json(&vec_lens),
        vec_growth.join(","),
        scales.join(","),
    );
}
