# Conditional datom-codec-derive impact

Query: `rg -n 'Budget|DatomForming|datom_form|Composing|Datomizable' /home/li/.cargo/git/checkouts/datom-codec-9f95a6bbf327d45b/4dff16b/`.

Observed derive generator `crates/datom-codec-derive/src/lib.rs:16,62,116,123` emits `Composing` methods with `fn compose(..., budget: &mut ::datom_codec::Budget)` but does not construct `Budget` and does not call `datom_form`. Adding fields to `Budget` therefore leaves generated `&mut Budget` type signatures unchanged. Approved `DatomForming::datom_form` signature and `datom-codec-kinds.ethos` generated declaration are the targeted codec changes; derive output itself requires no source change, only normal client regeneration where generated kinds are regenerated. Package manifests: datom-codec 0.32.2; datom-codec-derive 0.32.0.
