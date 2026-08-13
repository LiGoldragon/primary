# Protos-family stack segregation tracker

This is the single maintained tracker for the temporary quick-new MVP
segregation boundary.  It records observed checkout state, not authority to
redesign a stack.  Update it in the same change as any Protos-family or
quick-new dependency, generator, or artifact-boundary change.

## Governing ruling

> I need to see a visual of the repo dep graphs, and that there is no
> crossover. spirit is the only component were considering for the mvp, and
> since its being reworked and renamed to psyche, then there is no problem. the
> new correct stack is out of scope for now, but it should be clearly marked
> and not abandnned or otherwise modified with the wrong design while we do
> the quick-new stack

Psyche, 2026-08-13T23:11:37+02:00; recorded verbatim in
[the three-stacks Vision log](../psyche/Vision/threeStacks.md#2026-08-13t2311370200--i-need-to-see-a-visual-of-the-repo-dep-graphs).

The temporary boundary ends only when the psyche separately rules resumption
of the terminal correct-new design.  It is not an abandonment, retirement, or
permission to shape that stack with the MVP's shortcut design.

## Legend

```text
-->  observed Cargo or Nix product/build dependency
..>  permitted human re-authoring, explicit generation, or committed artifact flow
-X-> forbidden Cargo/Nix dependency or architectural modification
```

## Four distinct estates

```text
+-----------------------+   +-------------------------------+
| LEGACY / DONOR        |   | FROZEN INCORRECT-NEW          |
| Spirit and old        |   | core-*, *-engine, rust-logos, |
| Schema/NOTA evidence  |   | sema-translator, spirit-ethos |
+-----------------------+   +-------------------------------+

+---------------------------------------------------------------+
| QUICK-NEW MVP (active)                                        |
| datom, ethos-rust, psyche, signal-psyche, meta-signal-psyche |
| and the universal `protos` structural substrate               |
+---------------------------------------------------------------+

+---------------------------------------------------------------+
| TERMINAL CORRECT-NEW (protected, out of scope)                |
| future Ethos/Nomos/Logos daemon-era architecture              |
+---------------------------------------------------------------+
```

`protos` is quick-new occupancy by the explicit 2026-08-14 ruling: universal
shape/walk/string substrate lives there, with a prominent occupancy notice.
The terminal daemon-era architecture remains protected and out of scope. The
legacy checkout and its contract heads are not part of the quick-new closure.
Their existing mixed edges are described below solely so an agent does not
mistake them for permitted precedent.

## Observed product graph: manifests, 2026-08-14

This graph is observed directly from the current Cargo manifests and flakes.
It is intentionally distinct from the intended human/artifact flow below.

```text
+---------+   +----------------+   +--------+   +---------------+   +--------------------+
|  datom  |   |   ethos-rust   |   | psyche |   | signal-psyche |   | meta-signal-psyche |
| first 0 |   | first 0        |   | first 0|   | first 0       |   | first 0            |
|         |   | external:      |   |        |   |                |   |                    |
|         |   | thiserror = 2  |   |        |   |                |   |                    |
+---------+   +----------------+   +--------+   +---------------+   +--------------------+

No lines join these repositories: no first-party Cargo product dependency,
no first-party Nix product/build input, and no inter-repository edge is
observed among the five quick-new repositories.

Every quick-new repository except Datom -X-> legacy/donor, frozen
incorrect-new, and terminal correct-new product dependencies. Datom's one
observed quick-new Cargo edge is shown below.
```

```text
+----------+
|  protos  |  direct Cargo product dependencies: none
| quick-new|  Nix inputs: nixpkgs, flake-utils, rust-build
+----------+

protos -X-> legacy/donor, frozen incorrect-new, Datom, Signal, and terminal
correct-new product dependencies.
```

`thiserror = "2"` is an external crate, not a first-party repository edge.
The common flake inputs (`nixpkgs`, `flake-utils`, and `rust-build`) are
generic bootstrap/build tooling, not component-stack dependencies.

`datom` has one observed quick-new product edge at published revision
`a0e0dbc4bd9b033f583e105977a11f9b27af4c5c`: Cargo pins `protos` at
`d0f98aca41104b970862679c622d828222a83cfa`. This actual manifest fact is
separate from the intended human/artifact flow below; it creates no edge to a
legacy, frozen, Signal, or terminal checkout.

## Intended artifact flow: not wired

This is a future source/artifact relationship, not the observed graph above
and not permission to add a Cargo or Nix dependency.

```text
legacy Spirit semantics
        |
        | ..> read and re-author only
        v
Psyche Ethos sources
        |
        | ..> explicit ethos-rust invocation
        v
+----------------+       ..> committed generated Rust       +----------------+
|   ethos-rust   |------------------------------------------>|     psyche     |
| generator tool |                                           | Nexus / Sema   |
+----------------+                                           +----------------+

psyche component anatomy ..> signal-psyche
psyche component anatomy ..> meta-signal-psyche
```

No intended arrow is presently a Cargo/Nix edge.  `ethos-rust` remains an
explicit generator tool, never a Psyche or contract-repository dependency.

### Snapshot nodes and revisions

The revision is the visible main parent unless noted.  A dirty working copy is
not silently treated as a committed revision.

| Estate | Checkout | Observed revision/state | Direct Cargo product dependencies | Nix flake inputs |
| --- | --- | --- | --- | --- |
| quick-new | `datom` | `a0e0dbc4bd9b033f583e105977a11f9b27af4c5c`; clean and published | git `protos` @ `d0f98aca41104b970862679c622d828222a83cfa` | `nixpkgs`, `flake-utils`, `rust-build` |
| quick-new | `ethos-rust` | `c0f4e112fe38d2eb7ba95ceb0687a4b3487e9b09` | `thiserror = "2"` only | `nixpkgs`, `flake-utils`, `rust-build` |
| quick-new | `psyche` | `14b9c3e79e03d9db12e57ca52274fd7999510b9e`; clean and published | none | `nixpkgs`, `flake-utils`, `rust-build` |
| quick-new | `signal-psyche` | `09ecca6968f0995749a13da851fb9a85444abd61` | none | `nixpkgs`, `flake-utils`, `rust-build` |
| quick-new | `meta-signal-psyche` | `5b03ff6577db84825bc229a145eeacc5ac3f2268`; clean and published | none | `nixpkgs`, `flake-utils`, `rust-build` |
| legacy/donor | `spirit` | current working-copy snapshot `45f7a9af5aa68c71311941b9925bceaffd21a7a7`; unrelated working changes present | mixed legacy closure; see next section | legacy closure; quarantined and not fully inventoried here |
| quick-new | `protos` | `d0f98aca41104b970862679c622d828222a83cfa`; clean and published | none | `nixpkgs`, `flake-utils`, `rust-build` |

`nixpkgs`, `flake-utils`, and `rust-build` are generic bootstrap/build-tool
inputs in these five quick-new flakes.  They are not product dependencies on
another component stack.

## Quarantined legacy and frozen graph

```text
spirit
  --> nota (optional), sema-engine, signal-frame, signal-domain
  --> signal-spirit, meta-signal-spirit, triad-runtime
  --> schema-rust (build), schema-language (dev)

signal-spirit      --> protos, rust-logos, sema-translator, core-nomos
meta-signal-spirit --> protos, signal-spirit, rust-logos, sema-translator, core-nomos

quick-new -X-> spirit, signal-spirit, meta-signal-spirit
quick-new -X-> core-nomos, rust-logos, sema-translator, and every frozen donor
```

Those `signal-spirit` and `meta-signal-spirit` entries are direct Cargo
declarations in their current checkout heads.  They pin an older `protos`
revision (`d06c4a9`) and frozen references; they do not establish an allowed
edge from quick-new to Protos or from Psyche to Spirit.

The frozen reference nodes inspected at this snapshot are: `core-ethos`
`818620982ff9ec7f0be46c24e83c9c87b9424439`, `core-logos`
`98873669c0a024c815a55f2d89ef99ffab1e4c0c`, `core-nomos`
`63c9226b20b5bac4c8d903410f64e0b67f8794ee`, `ethos-engine`
`3a80a3ec6a1603db50a149a75d1feee59f6e8383`, `logos-engine`
`7c8dcb0ca4840b2d67178a9e7293ba97e10b7df2`, `nomos-engine`
`b7b3ec2fc2e629257c9635ecae07bd0efddc2982`, `rust-logos`
`52adea6179525c509dee0688b07af431a9e21756`, `sema-translator`
`40cc5e607a066a7c6a338f1f9498a02eacde9205`, `spirit-ethos`
`b92b3bfd54912e14b6b35594bf7076254c983eac`, `protos-engine`
`7a1bfd191dce44d6d665a166ecd9c5e59d76aebb`, and `dotos`
`d97dd5c17688a49ed41b12d3c20ef51fe3c692ae`.  They are reference-only here;
this list is not a work queue.

## Boundary rules

Allowed:

- Read legacy Spirit semantics as donor evidence and re-author them in Psyche.
- Invoke `ethos-rust` explicitly, then commit its generated Rust artifacts in
  their owning quick-new repository.
- Add a quick-new product edge only after a Psyche ruling names the edge and
  its purpose; update this tracker and durable checks in that same change.

Forbidden without a separate Psyche ruling:

- Any Cargo, Nix, runtime, or build dependency from quick-new to legacy,
  frozen incorrect-new, or terminal correct-new repositories.
- Copying legacy or frozen architecture/code into Psyche under the label of
  re-authoring.
- A Cargo or Nix dependency on `ethos-rust` from Psyche or either contract
  repository.  The generator is a tool, not a product dependency.
- Modifying future terminal daemons to accommodate the MVP, or treating the
  old contract-head crossovers as a design template.

## Verification procedure

Run these from `/home/li/primary`; none invokes `bd`.

```text
for repo in datom ethos-rust psyche signal-psyche meta-signal-psyche; do
  (cd "repos/$repo" && jj log -r '@-|@' --no-graph -T 'commit_id ++ "\n"')
  (cd "repos/$repo" && cargo metadata --locked --offline --no-deps --format-version 1)
  (cd "repos/$repo" && nix flake metadata --offline --json)
done

rg -n 'spirit|schema|nota|dotos|core-|ethos-engine|nomos-engine|logos-engine|rust-logos|sema-translator|spirit-ethos|protos' \
  repos/{datom,ethos-rust,psyche,signal-psyche,meta-signal-psyche}/{Cargo.toml,flake.nix}
```

The `rg` command is expected to return no product-dependency matches.  If it
finds a deliberate documented guard/test string, inspect the surrounding line;
it must not be a Cargo or flake input declaration.  `cargo tree --locked
--offline --edges normal,build,dev` may supplement the direct-metadata check
when all locked crates are locally available.

## Open and unresolved edges

- The exact Ethos-to-Datom implementation edge is ruled conceptually but not
  wired in Cargo/Nix; its package shape and direction need an implementation
  ruling before change.
- Psyche's Ethos sources, generated Nexus/Sema artifacts, and both signal
  vocabularies are deliberately unruled/unimplemented.  Their eventual
  package dependencies must be reviewed before landing.
- The current Protos substrate manifest has no product dependencies. Legacy
  contract heads may still pin an older Protos plus frozen nodes; those old
  heads do not create an edge into the active substrate. Whether and how the
  terminal correct-new architecture eventually resumes is out of scope.
- The frozen-reference roster is preserved, but it is not a complete
  dependency-closure proof for every historical checkout.  This tracker
  records the direct, relevant edges observed above and must be refreshed at
  each boundary change.
