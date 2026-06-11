# 91 — Versioning component Sema databases (beads/Dolt, ID forms, server-backed atomic VC)

Frame and method for this dispatched-subagent session. The psyche asked, in one sitting, three linked questions:

1. **Beads** — do we still use it? Are beads and Spirit using "the same short hashes"?
2. **Version-controlling component databases** — they must be backed up on a **server**, **atomically**; beads uses Dolt (a version-controlled DB) and that is the thread worth pulling. How do we do this *properly* given our strictly-typed, hard-migration-on-every-schema-change architecture?
3. **Analyze our Sema system** and infer how to do the version-controlling-with-a-server part properly.

## Spirit gate

Outcome: **Record.** The durable constraint — *component Sema databases must have atomic, server-backed, version-controlled durability; state loss is unacceptable; pursue native version control rather than treating the store as an opaque blob* — was captured as Spirit **`29pb`** (the atomic-server-backup + native-VC constraint). The mechanism itself is design, not yet psyche intent; the synthesis lists candidate captures pending the psyche's affirmation (it does not record them — only the psyche is the source of new intent).

## Method

A background Workflow of **7 agents** — five parallel investigators, a synthesis, and an adversarial accuracy critic:

| # | File | What it established |
|---|---|---|
| 1 | `1-beads-and-dolt.md` | Beads reality: a real `steveyegge/beads` + embedded Dolt install, quiet since Jun 9; and exactly how Dolt version-controls on disk (the reference design). |
| 2 | `2-id-forms.md` | Bead `primary-<code>` vs Spirit bare `<code>` — identical base36 alphabet, overlapping length; the disambiguation convention. |
| 3 | `3-sema-architecture.md` | The core deep-read: on-disk redb+rkyv, destructive operation model, metadata-only log, counter (not hash) snapshot id, single-writer ACID with no online-snapshot path, full-rewrite migration. |
| 4 | `4-content-addressing-and-server.md` | Content-addressing inventory (Sema is sequence-addressed; criome's blake3 is the lone hash) + server infra + repository-ledger as the ingest precedent. *(Carried the host error — corrected; see banner in-file.)* |
| 5 | `5-dolt-and-prior-art.md` | Dolt/noms/prolly-tree internals, why git's blob problem disappears, and Datomic/irmin/TerminusDB lessons for a typed store. |
| 6 | `6-synthesis.md` | **The deliverable** — verdicts, the core tension, the four options, the recommended native design, the migration-as-discontinuity model, the staged path, and the corrections ledger. |

## The adversarial critic earned its keep

The seventh agent re-checked the synthesis against source and caught a **high-severity, load-bearing factual error**: the design pointed the backup server at **prometheus**, but `goldragon/datom.nota` assigns `GitoliteServer` + `TailnetController` to **ouranos** (verified directly against `datom.nota:28-97` before correcting). Prometheus is the NixBuilder/NixCache + `criome-backup`-SSID Btrfs node — a backup *target*, not the Gitolite/control host. That error threaded through the mermaid diagram, all three stages, and three recommendations; all are corrected in `6-synthesis.md`, with the full corrections ledger (one high, two medium, four low) at the end of that file. The critic also confirmed the central design argument — typed-transform migration discontinuity + content-addressed intra-version sharing — holds against source.

## One-paragraph conclusion

Beads is **retired in practice** (harvest the Dolt lesson, let it go per `INTENT.md`). The two ID spaces are **distinct but bare-ambiguous** — fixed by a writing convention, no code change. The Sema stack today is a current-state redb+rkyv store with a metadata-only log and **no backup path at all**; version control is **not half-built**. The recommended direction is a **native content-addressed Sema remote** — a payload-bearing Datomic-style operation log under a blake3-chunk snapshot layer, shipped to the Gitolite host (**ouranos**) via the repository-ledger triad pattern — with an **atomic file-snapshot floor shippable now** (Btrfs reflink on the backup target + git-push off-host). A schema migration is represented as a **typed-transform discontinuity commit**, not a cell diff, because each schema version is a genuinely different rkyv type set.
