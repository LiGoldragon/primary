# Why signal declares `links = "signal"`

## Method

`git log -S links` and `-G links` on signal's `Cargo.toml` from main
f35460de; `git show` of the two commits found; `git grep` over
schema-rust history for the `links` convention the bootstrap build used;
`grep -rn -i links` over `/home/li/primary/flows/*/reports`, reading only
the matching lines; signal's `src/accord.rs` and `src/exchange.rs` read
by grep for the greeting and exchange.

## The commits

- 3f9d75ee (2026-06-18), "signal-standard: bootstrap shared
  cross-component standards library": introduced `links =
  "signal-standard"` with a schema-rust-next `build.rs`. The message gives
  no reason for `links`. schema-rust's convention (ARCHITECTURE.md and
  skills.md, e.g. 5c743ee) gives the mechanical one: "Contract crates that
  declare a Cargo `links` name should publish their `schema/` directory
  with `CargoSchemaMetadata::emit_schema_directory`", read downstream as
  `DEP_<LINKS>_SCHEMA_DIR`. The bootstrap build.rs calls
  `CargoSchemaMetadata::new(..).emit_schema_directory(..)`. So `links`
  began as a build-metadata channel, not as a one-signal rule.
- 626e407b (2026-09-11), "Become the shared signal repository": renamed
  the key to `signal`; the message says only "The crate, library, and
  Cargo links key are now signal". No reason given.
- Today's `build.rs` (ethos-zero check) emits no Cargo metadata, so the
  original purpose no longer applies; the key's only remaining effect is
  Cargo's one-package-per-`links`-key rule.

Intent of the single-signal rule as such: never written at introduction;
first stated after the fact in flows/f6db8d/reports/landings-consumers.md
("the `links` key is what *enforces* one shared frame per graph, which is
the property a wire wants") and final-sweep.md §4. The guarantee relied
on, witnessed in source: `Signal<T>` (portable.rs), the framing
(frame.rs), and the greeting and exchange (`Contracted::greeting`,
`ExchangeLedger` in accord.rs; `Dispatch::Greet`, `Delivery::Greeted` in
exchange.rs) are one set of types per process; f6db8d also saw E0308
between two `Signal` structs and reproduced the `links` collision in a
scratch crate.

## Landed

signal main 0cad1d1a (from f35460de), README.md, new section "One signal
per build graph"; version unchanged (docs only, not runtime-visible):

> `Cargo.toml` declares `links = "signal"`, so Cargo admits one release of
> this crate per dependency graph: every contract in a process shares one
> `Signal<T>`, one framing, and one exchange and greeting layer, and two
> contracts' frames pass through the same transport (two copies of the
> crate would make two incompatible `Signal` types for one wire). The cost
> is that a crate cannot build two releases of a signal consumer in one
> graph, so a cross-release test lives in a `<repo>-test` repository.
