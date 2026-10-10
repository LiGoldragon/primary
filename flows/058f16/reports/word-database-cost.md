# Cost of a word database for checking camelCase identifiers (measured 2026-10-10)

## Which list prior records used
BIP-39 English (2048 words). Source: flows/5578cc/vision/identifiers.md, 2026-10-03: `abandonAbilityAble`
is "a 33-bit id written as three BIP-39 words" (3 x 11 bits). The 2026-10-10 naming record (flows/d68c82/vision/naming.md)
names no list; it asks for "a database of words" and for this size-cost measurement. The larger list is my choice (a claim of mine, not a record).

## Lists
- bip: bitcoin/bips bip-0039/english.txt, 2048 words, 13,116 bytes.
- large: dwyl/english-words words_alpha.txt, lowercased, a-z only, deduped, 370,105 words, 3,864,805 bytes.
  (Contains many obscure/archaic words; it is a size stand-in for "a full English list", not a vetted vocabulary.)

## Method
Crate: scratchpad/wordcost (Rust 1.97.1, built locally, 14 cores; Prometheus not needed). Release, opt-level 3, lto, codegen-units 1, panic abort, strip.
build.rs embeds the list in one of four forms: array = `static [&str]` sorted, binary search; packed = one byte blob + u32 offset table, binary search;
phf = phf_codegen Set (phf 0.11); fst = fst 0.4 Set bytes via include_bytes, `Set::new(&'static [u8])`.
Baseline binary = same program, bip build with no database (checker returns true), 364,440 bytes. Size added = binary size minus baseline (fst code itself ~ few KB included).
Check = split camelCase at uppercase, lowercase each segment, look up each; no allocation.
Workload: 100,000 ids per list (bip: 3 words; large: 2-4 words), 10% with one corrupted segment (90,000 accepted in every variant: correct).
Time = best of 7 passes over the 100k ids, ns per identifier, in process. RSS = VmRSS from /proc/self/status at process start (before any code of ours),
after 100k checks, and after touching every page of the data. The check process also holds the 100k ids (~5.5 MB), so RSS is read from the
server process (no ids loaded) where possible.
Socket: separate process `serve`, Unix stream socket, newline protocol, one request one reply. persistent = one connection, 200,000 calls;
perconn = connect+send+reply+close, 50,000 calls. Client in another process, wall time per call. Single machine, not pinned, other load present (load avg unknown): treat as +-20%.

## Results
| list | form | binary added | RSS at start (kB) | RSS after checks, ids excluded (kB) | ns / id |
|---|---|---|---|---|---|
| none | baseline | 0 (364,440 total) | 2,180 | - | 50 (loop only) |
| bip | array | +92,408 | 2,196 | ~2,270 (server) | 342 |
| bip | packed | +18,200 | 2,120 | ~2,200 | 325 |
| bip | phf | +95,536 | 2,196 | ~2,300 | 87 |
| bip | fst | +12,632 | 2,144 | 2,356 (server) | 300 |
| large | array | +18,298,280 | 16,760 | 20,048 (server) | 1,240 |
| large | packed | +4,974,056 | 2,196 | ~7,200 (touched-all 13.7 MB minus 5.5 ids) | 851 |
| large | phf | +18,890,320 | 16,776 | ~21,800 | 479 |
| large | fst | +1,652,456 | 2,196 | 3,788 (server) | 676 |

RSS rows marked ~ are derived: (afterchecks - idsloaded + start); those marked server are measured in the serving process.
Array and phf hold pointer tables: the dynamic linker applies relocations at start, so the whole table is resident immediately (large: 16.8 MB at start, before any lookup).
packed and fst are position-independent and page in lazily from the binary file (page cache, shared).

Socket round trip (separate process, includes the lookup):
| list (server form) | persistent connection | connect per request | server RSS kB |
|---|---|---|---|
| bip (array) | 7.4 us | 13.0 us | 2,268 |
| bip (fst) | 6.9 us | 12.0 us | 2,356 |
| large (array) | 10.4 us | 17.1 us | 20,048 |
| large (fst) | 8.0 us | 14.7 us | 3,788 |
Round trip minus in-process check: about 6.5 us persistent, 12 us per-connection; the socket costs ~20x the lookup of the smallest list.

## Not measured
Build/compile time per form (all nine builds finished within one command; not timed). Cold-start page-fault latency. Non-x86/other kernels. Any word-list quality/coverage question (e.g. whether `abandonAbilityAble` words suffice for names).
