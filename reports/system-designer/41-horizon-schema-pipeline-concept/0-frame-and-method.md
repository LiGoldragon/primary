# Frame — Horizon schema pipeline concept (show it actually working)

*Meta-report orchestrator's frame. Psyche directive 2026-05-28 (Spirit 1048 Decision + 1049 Correction + 1050 Clarification): build a working concept prototype that generates all needed Horizon datatypes from a PURE schema, demonstrated step-by-step end to end — schema source → imports → assembled schema (Asschema) → emitted Rust — actually running in a worktree, with the REAL artifacts shown at each step. The psyche is explicit: prior schema-stack work has read as marketing; they want to SEE a fully-working pipeline, not be told it works. Horizon's runtime shape (signal-only / triad / library) is open — the concept illuminates it, doesn't force it.*

## The ask, precisely

Three things, in priority order:

1. **A pure schema that generates Horizon's datatypes** — and the concept must show the GENERATION, step by step, with real artifacts: the `.schema` the author writes, the imports it pulls, the assembled schema (Asschema) it lowers to, the Rust it emits.
2. **It must actually run** — a worktree, a real Nix build witness. Per Spirit 1049 (Correction) + record 1006 (prove-not-pretend): SHOW it working, don't claim it. No marketing. If something doesn't work, show that honestly too.
3. **Illuminate Horizon's runtime shape** — the psyche is unsure (signal-only? triad? library?). The concept shows the datatypes generate regardless; the runtime-shape decision is surfaced, not forced.

## The enabling step — collections (record 1034)

`/40` established that Horizon's cluster proposal is collection-bearing (112 container-field-lines: 21 BTreeMap, 39 Vec) and CANNOT emit from schema today because `schema-next`'s `TypeReference` is a bare name with no type arguments (`/40/4` explains this in full). So a working Horizon datatype demonstration REQUIRES implementing collections first. The psyche proposed the syntax in record 1034: **positional macro forms, collection name first** — `Vec <element-type>`, `KeyValueMap <key-type> <value-type>`, fitting the head-symbol-dispatch macro model (record 880). `Option`'s exact form is still open (the subagent proposes one, aligned with the same model).

So this concept does double duty: it IMPLEMENTS the decisive gate from `/40` (collections) AND demonstrates it on the real Horizon domain. This is the prototype-driven-component-development cycle (records 971-974): the prototype needs collections → develop collections → demonstrate. Building it also gives the psyche the evidence to confirm record 1034 (currently "proposed, pending confirmation").

## The concept — Horizon as a schema-driven component

The schema (`schema/horizon.schema`) is designed to exercise the FULL feature set the psyche wants to see — imports, collections, the four-position document, the pipeline — on a representative slice of the real Horizon cluster proposal:

```text
{ Magnitude schema-core:magnitude:Magnitude }        ; position 0: IMPORTS (cross-crate, per /39)
(Input ((Project ClusterProposal)))                  ; position 1: the projection request
(Output ((Projected NodeConfigSet) (Rejected ProjectionError)))  ; position 2: the result
{                                                    ; position 3: NAMESPACE
  ClusterProposal [Nodes Users]
  Nodes (KeyValueMap NodeName NodeProposal)          ; COLLECTION — the map of nodes
  Users (Vec UserProposal)                           ; COLLECTION — the list of users
  NodeProposal [NodeRole Trust Placement OptionalCache]
  OptionalCache (Option BinaryCache)                 ; OPTION — an optional field
  NodeRole (Center Edge Builder)
  Trust Magnitude                                    ; IMPORTED leaf type
  NodeConfigSet (KeyValueMap NodeName NodeConfig)    ; the projection output (collection)
  ...
}
```

(Illustrative — the subagent refines the exact slice. The point is it MUST contain at least one `KeyValueMap`, one `Vec`, one `Option`, and one cross-crate import, so the demonstration shows all four.)

This framing answers the psyche's runtime-shape musing: declaring `Input`/`Output` makes Horizon a SIGNAL-leaning component (the projection is `Project → Projected`), which (a) satisfies the four-position document naturally (no types-only-module gap), (b) matches "maybe Horizon is a triad component," and (c) leaves room for a future Sema plane holding cluster state. The concept demonstrates this shape works; the report surfaces the alternatives (pure library needing types-only-module per `/39`; full triad with sema) without forcing the choice.

## The step-by-step demonstration (the deliverable's center)

The whole point is the psyche SEES each transformation. The subagent's report must show the REAL artifact at each step:

| Step | Artifact shown | Proves |
|---|---|---|
| 0 | The `schema/horizon.schema` source (what the author writes) | the pure schema input |
| 1 | nota-next parse output — the structural blocks / StructureHeader | the raw structural read |
| 2 | schema-next lower output — the **Asschema** (its Debug form): resolved imports + namespace with collection-bearing `TypeReference`s | imports resolved + macros applied + assembled |
| 3 | schema-rust-next emit — the generated `src/schema/horizon.rs` (the REAL Rust: `pub struct ClusterProposal { pub nodes: BTreeMap<NodeName, NodeProposal>, pub users: Vec<UserProposal> }`, etc.) | the datatypes generated |
| 4 | A test constructing a real `ClusterProposal` value + running a projection method on it | the emitted types are usable + projection works on schema-emitted nouns |
| 5 | `nix flake check` output | the whole pipeline builds + runs in Nix |

Each row is a real artifact pasted into the report, not a description. That is the anti-marketing demonstration the psyche asked for.

## Method

One focused build subagent (background, inherits this system-designer lane per record 920), then orchestrator verification + synthesis:

- Subagent: implements collections in schema-next + schema-rust-next, authors `schema/horizon.schema`, runs the pipeline capturing artifacts at each step, lands a Nix witness, writes the artifact-rich step-by-step walkthrough at `1-build-and-step-by-step-walkthrough.md`.
- Orchestrator (me): VERIFY by reading the actual emitted Rust + confirming the Nix check output (anti-marketing means I check it's real, not just relayed), then write `2-overview.md` with the verification + the runtime-shape synthesis + the answer to "is it really working."

## Subagent dispatch brief

*Verbatim. The subagent reads this as its complete instruction set.*

### You are a designer subagent

You are a designer-class subagent dispatched by the system-designer lane (inherit this lane + lock per record 920; no `-assistant` lane; reports under `reports/system-designer/`). Your task: build a WORKING concept prototype that generates Horizon's datatypes from a pure schema, and demonstrate it step-by-step with real artifacts. The psyche is tired of marketing — they want to SEE the pipeline working. Honesty is paramount: show what works AND what doesn't; never fake a passing step.

### Required reading, in order

1. `/home/li/primary/reports/system-designer/41-horizon-schema-pipeline-concept/0-frame-and-method.md` — THIS frame (the concept, the schema sketch, the step-by-step table).
2. `/home/li/primary/AGENTS.md` — rust-skill hard override (read skills/rust-discipline.md before Rust); per-repo INTENT/ARCH manifestation (record 944).
3. `/home/li/primary/skills/rust-discipline.md` + sub-skills + `skills/abstractions.md` + `skills/feature-development.md` + `skills/jj.md` (headless, `-m` inline) + `skills/testing.md` (all tests in Nix).
4. `/home/li/primary/reports/system-designer/40-horizon-lojix-schema-next-port-feasibility/4-collections-and-option-gate-explained.md` — WHY collections is the gate + the exact `TypeReference` shape to grow (`{ name: Name }` → enum with Plain/Vector/Map/Optional).
5. `/git/github.com/LiGoldragon/schema-next/src/asschema.rs` (the `TypeReference`/`TypeDeclaration` you extend) + `src/engine.rs` + `src/declarative.rs` (the macro lowering you add the collection forms to).
6. `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs` (the emitter you teach to write `Vec<T>`/`BTreeMap<K,V>`/`Option<T>`).
7. `/git/github.com/LiGoldragon/schema-core/` — the `/39` cross-crate import proof (your imports demonstration builds on this; import a shared type like `Magnitude` from it).
8. `/git/github.com/LiGoldragon/spirit-next/build.rs` + `flake.nix` — the crane pipeline pattern to model your concept's flake on.
9. `/git/github.com/LiGoldragon/horizon-rs/` (the `horizon-leaner-shape` branch / worktree) — the REAL Horizon datatypes + projection methods to draw your representative slice from (don't reinvent; mirror the actual `ClusterProposal`/`NodeProposal`/projection shape, scaled to a demonstrable slice).

### Worktree

Per `skills/feature-development.md` + `skills/major-break-via-new-repo.md`: create a concept repo `horizon-next` (modeled on spirit-next/schema-core — Cargo + flake + schema/ + build.rs + src/schema/) OR a `schema-driven-horizon` branch worktree — your call, document it. If you extend schema-next/schema-rust-next for collections, do that on `schema-driven-horizon`/`collections` branch worktrees of those repos. Claim each: `tools/orchestrate claim system-designer '[draft:horizon-schema-pipeline-2026-05-28]' <path> -- '<reason>'`.

### Deliverable

1. **Collections in schema-next + schema-rust-next** (record 1034): grow `TypeReference` to carry type arguments (Plain/Vector/Map/Optional); lower the macro forms `Vec <T>`, `KeyValueMap <K> <V>`, and an `Option <T>` form (propose Option's exact shape, aligned with head-symbol dispatch); schema-rust-next emits `Vec<T>`/`BTreeMap<K,V>`/`Option<T>`. Methods on data-bearing types per the no-free-functions rule. Preserve all existing schema-next/schema-rust-next tests (the legacy path stays byte-identical for non-collection schemas).
2. **`schema/horizon.schema`** in the concept repo: imports a shared type from schema-core (cross-crate, per /39), declares `Input`/`Output` (Horizon-as-component: Project/Projected), and a representative cluster-proposal namespace that USES at least one `KeyValueMap`, one `Vec`, one `Option`, and the imported type. Mirror the real horizon-rs shapes.
3. **The pipeline run, artifacts captured at each step** (Step 0-5 in the frame's table) — paste the REAL output of each step into your report.
4. **A projection method** on the emitted `ClusterProposal` (mirror horizon-rs's `ClusterProposal::project` shape, scaled) — proving projection works as methods-on-schema-emitted-nouns (the `/40` Wave A finding that projection is already schema-at-heart).
5. **A Nix witness**: `nix flake check` (modeled on spirit-next's crane flake) builds the whole pipeline, compiles the emitted Rust, and runs a test that constructs a real `ClusterProposal` + runs the projection. Dispatch to the remote builder if heavy.
6. **Per-repo INTENT.md + ARCHITECTURE.md** (record 944) in every repo touched.

### The report — the step-by-step walkthrough (the centerpiece)

Write `reports/system-designer/41-horizon-schema-pipeline-concept/1-build-and-step-by-step-walkthrough.md`. Structure it as the SIX STEPS, each showing the REAL artifact:
- Step 0: the `schema/horizon.schema` source (full, pasted).
- Step 1: the nota-next structural parse (the blocks / StructureHeader — actual output).
- Step 2: the Asschema (the assembled schema, its Debug form — actual output, showing resolved imports + collection-bearing TypeReferences).
- Step 3: the emitted `src/schema/horizon.rs` (the real generated Rust — pasted, showing the BTreeMap/Vec/Option fields).
- Step 4: the projection test (the code + what it asserts).
- Step 5: the `nix flake check` output (the actual pass lines).

Then: the runtime-shape observation (Horizon-as-component worked; surface the library / signal-only / full-triad alternatives), what's still rough (honestly), and what landing this confirms (record 1034 collections + the `/40` Gate-1 unlock).

### Hard rules + honesty

- No free functions outside main/cfg-test; schema-emitted types are the nouns; methods on them.
- NOTA strings from brackets only; never emit `"`.
- Headless jj, `-m` inline; designer lanes don't push to main (per-repo feature branches; `jj git push --bookmark <branch> --allow-new`).
- Sub-sub-agent dispatches MUST be `run_in_background: true`.
- **HONESTY (record 1049)**: the psyche is tired of marketing. If collections turn out harder than expected, or a step doesn't work, SHOW IT — a half-working pipeline honestly reported is worth more than a fake green. Capture any new Spirit Clarifications you hit; do NOT re-capture 1048/1049/1050.

### Don't

- Don't push to main of any repo. Don't modify workspace guidance files (per-repo INTENT/ARCH is fine).
- Don't search /nix/store. Don't cat/head/tail/sed/awk when Read/Edit fit.
- Don't over-build a runtime — the CENTER is the datatype-generation pipeline. A minimal Input/Output + the projection method is enough; surface the runtime-shape question, don't resolve it with a big engine.

Begin by reading the frame's §"The concept" + §"The step-by-step demonstration".

## Risks + open questions

- **Collections implementation depth** — growing `TypeReference` into an enum touches the lowering + emitter + likely the macro registry. If the subagent can't fully land Map (the harder one) but lands Vec + Option, that's still a strong demonstration — show the partial honestly.
- **Option's exact syntax** — record 1034 left it open. The subagent proposes; the psyche confirms later.
- **Horizon-as-component vs library vs triad** — the concept demonstrates the component shape (Input/Output); the runtime-shape decision stays the psyche's. If the psyche later wants Horizon as a pure library, the types-only-module gap (`/39`) becomes the path instead.
- **Scope** — this is collections (the /40 gate) + a Horizon schema + a pipeline demo + a Nix witness. Substantial but bounded. If it's too much for one pass, the subagent prioritizes: collections working + ONE collection-bearing type emitting + the Nix witness is the minimum viable demonstration; the full cluster slice is the stretch.
