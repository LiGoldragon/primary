# 681 — signal-standard: the second shared signal- library

Per Spirit `eeeo` (the new-shared-schema decision). `signal-standard` is
the second non-component shared `signal-` library, alongside `signal-frame`.
Where `signal-frame` owns domain-free **wire mechanics** (short headers,
exchange/stream identifiers, request/reply/stream envelopes, rkyv archive
helpers — per its `INTENT.md`), `signal-standard` owns domain-free
**cross-component standards**: the vocabulary every component conforms to.
Its first and central content is the cross-component classification —
the `ComponentKind` roster and the differentiator — plus the
authorized-object interest lattice lifted out of `signal-criome` and a
small embeddable classifier.

Scope is the whole point (`eeeo`): only **genuine cross-component
standards** live here, not a grab-bag of conveniences. It is not
`signal-system` (the System component's own contract, which would be
overloaded) and not `signal-frame` (charter is domain-free frame
mechanics, not domain vocabulary).

## Sources read

- `/git/github.com/LiGoldragon/signal-persona/schema/lib.schema` line 32:
  `ComponentKind [Mind Router Message System Harness Terminal Introspect Orchestrate Spirit]`
  (line 33 `ComponentPrincipal` is the same set reordered).
- `/git/github.com/LiGoldragon/signal-criome/schema/lib.schema` line 86:
  `ComponentKind [Spirit Criome Router Mirror Lojix Persona Agent]`;
  lines 214–232 carry `AuthorizedObjectKind`, `ComponentObjectInterest`,
  `AuthorizedObjectInterest`, `AuthorizedObjectReference`.
- `/home/li/primary/protocols/active-repositories.md` — the full component roster.
- `/git/github.com/LiGoldragon/signal-frame/INTENT.md` — shared-lib precedent.
- Spirit `t312` — the signal-namespace partition (system-types zone +
  component-specific zone, pre-allocated sizes, repartition = major version).
- Spirit `eeeo` — the signal-standard decision itself.
- `/git/github.com/LiGoldragon/schema-next` `main` (`abae95f`) — the engine
  used to validate; `tests/resolution.rs` + `tests/fixtures/import-consumer`
  for the import-brace syntax.

## (a) The reconciled ComponentKind census

The two rosters overlap on `Spirit` and `Router` only. Reconciling them
against `active-repositories.md` gives one authoritative roster of 14
variants. Each old variant maps cleanly; the criome roster contributed
the trust/principal names, the persona roster the supervised-lifecycle
component names.

| Variant | signal-persona | signal-criome | active-repositories evidence | Zone |
|---|---|---|---|---|
| `Spirit` | yes | yes | `spirit` — intent capture daemon | Core |
| `Mind` | yes | — | `mind` — central state component | Core |
| `Criome` | — | yes | `criome` — trust + attestation daemon | Core |
| `Message` | yes | — | `message` — engine ingress daemon | Messaging |
| `Router` | yes | yes | `router` — routing + delivery | Messaging |
| `Mirror` | — | yes | replication / observation mirror | Messaging |
| `Terminal` | yes | — | `terminal` — persona-facing terminal owner | Interaction |
| `Harness` | yes | — | `harness` — process/session boundary | Interaction |
| `Agent` | — | yes | `agent` (`signal-agent`) — API front door | Interaction |
| `System` | yes | — | `system` — OS/window observation | Platform |
| `Introspect` | yes | — | `introspect` — inspection plane | Platform |
| `Orchestrate` | yes | — | `orchestrate` — orchestration runtime | Platform |
| `Lojix` | — | yes | `lojix` — deploy/horizon component | Platform |
| `Persona` | — | yes | the engine as a whole — a principal | Aggregate |

Resolution decisions:

- **`Persona` is not a single daemon.** In the criome roster it names the
  engine-as-principal (a trust subject), not a supervised component. It is
  reconciled into its own AGGREGATE zone and documented as such, so a
  reader does not look for a `persona` daemon. (The persona roster never
  had it — there it was `ComponentName`/`ComponentPrincipal` per-component.)
- **No variant was dropped.** All 9 persona + all 7 criome variants
  survive; the 2 shared (`Spirit`, `Router`) collapse, giving 14.
- **`Mind` vs `Criome` vs `Spirit` are the Core spine** — present-in-every-
  deployment engine center, intent, and trust.

## The partition zones (modeled on Spirit `t312`)

`t312` partitions the 64-bit signal namespace into a system-types zone
and a component-specific zone with **pre-allocated zone sizes**;
repartitioning is a major-version event. `ComponentKind` follows the same
shape — but as **one closed enum** whose zones are documented allocations
(comments inside the enum), exactly as `t312`'s namespace zones are
documented allocations inside one 64-bit space. The closed enum still
type-checks every consumer; "closed-but-partitioned" means closed-enum
plus per-zone reserved room:

| Zone | Members | Reserved room | Rationale |
|---|---|---|---|
| Core | Spirit, Mind, Criome | 3 slots | engine spine in every deployment |
| Messaging | Message, Router, Mirror | 2 slots | ingress / routing / delivery |
| Interaction | Terminal, Harness, Agent | 2 slots | human/agent-facing surfaces |
| Platform | System, Introspect, Orchestrate, Lojix | 3 slots | OS / deploy / introspection |
| Aggregate | Persona | 1 slot | whole-engine principals, not daemons |

**Adding a component is a local edit** inside its area's reserved room —
insert the variant in the right zone, recompile. Not a workspace-wide
rebuild of the classification's structure; the zones and their meanings
stay fixed, the same way `t312` repartitioning (not appending within a
zone) is the major-version event.

## (b) The differentiator + (c) the interest lattice + (d) the classifier

Lifted from `signal-criome` lines 214–232, made standard:

- **`AuthorizedObjectKind [Operation Contract Agreement Time]`** — verbatim.
- **`Differentiator { component ComponentKind, kind AuthorizedObjectKind }`**
  — a component is distinguished cross-system by which kind it is and which
  object kind it acts over. (criome had this implicitly as the fields of
  `ComponentObjectInterest` / `AuthorizedObjectReference`; named here.)
- **`AuthorizedObjectInterest`** — the four-rung lattice:
  `AnyAuthorizedObject` / `(Component ComponentKind)` /
  `(ObjectKind AuthorizedObjectKind)` / `(ComponentObject ComponentObjectInterest)`.
- **`ComponentObjectInterest`** and **`AuthorizedObjectReference`** —
  carried over so the lattice and its references are complete.
- **`ComponentClassification { differentiator, advertises }`** — the new
  small embeddable classifier: the minimal standard nameplate a daemon
  stamps onto its frames so peers classify it without a lookup. Genuinely
  cross-component, nothing more.

The crate is a **pure vocabulary library**: Input `[]` and Output `[]`
root sections are empty; component contracts import these types and
reference them inside their own roots.

## Validation result — passes (with one honest caveat)

The canonical prototype at `/tmp/signal-standard/schema/lib.schema` uses
the **positional dot-differentiator** struct-field form from
`skills/structural-forms.md` / `nota-design.md` (`kind.AuthorizedObjectKind`).
The schema-next checkout I could locate and build is `main` at `abae95f`,
which **predates that form** — it still uses the name-value pair form
(`fieldName Type`, e.g. `commitSequence CommitSequence` in its own
fixtures) and the `*` shorthand. The dot/positional form lives on the
`next/structural-forms` epic branch, not on this `main`.

So I validated **honestly two ways**:

1. Authored the canonical prototype in the positional form (the form the
   migration target will actually use, per the active skills).
2. Wrote a name-value variant `/tmp/signal-standard/schema/lib.namevalue.schema`
   — identical types/zones/census, only struct-field spelling differs —
   and lowered it through `schema_next::SchemaEngine::lower_source` with a
   throwaway integration test. **Result: lowers cleanly**, all seven types
   (`ComponentKind`, `AuthorizedObjectKind`, `Differentiator`,
   `ComponentObjectInterest`, `AuthorizedObjectInterest`,
   `AuthorizedObjectReference`, `ComponentClassification`) resolve. The
   temp test was removed afterward (schema-next is operator-owned).

Caveat stated plainly: the positional-form file is **not** machine-validated
here because no checkout of the epic-branch engine was available to build;
its correctness rests on the structural-forms skill + the equivalence to
the validated name-value variant. When the operator lands this, build
against whichever schema-next form is current on `main` at that time.

## (e) Migration plan (operator-lane — designer prototypes only)

`signal-standard` touches code-repo `main`, so the actual edits are
operator work. The plan:

1. **Create `signal-standard`** as a new `signal-` library crate (the
   second alongside `signal-frame`): `Cargo.toml` mirroring
   `signal-criome`'s shape (`signal-frame` dep, `nota-text` feature),
   `schema/lib.schema` = the prototype here, generated `src/schema/`.
2. **signal-criome** — delete local `ComponentKind` (line 86),
   `AuthorizedObjectKind` (214), `ComponentObjectInterest` (216–219),
   `AuthorizedObjectInterest` (221–226), `AuthorizedObjectReference`
   (228–232). Add the import brace:
   `{ ComponentKind signal-standard:lib:ComponentKind`
   ` AuthorizedObjectKind signal-standard:lib:AuthorizedObjectKind`
   ` ComponentObjectInterest signal-standard:lib:ComponentObjectInterest`
   ` AuthorizedObjectInterest signal-standard:lib:AuthorizedObjectInterest`
   ` AuthorizedObjectReference signal-standard:lib:AuthorizedObjectReference }`.
   `ObjectDigest` stays criome-local (criome already declares its own).
   Regenerate; criome's `Evidence`, `AuthorizedObjectObservation`,
   `ContractTimeCheck`, etc. now reference the imported types unchanged.
3. **signal-persona** — delete local `ComponentKind` (line 32). `ComponentPrincipal`
   (line 33) is the same set and **collapses into the imported `ComponentKind`**
   (psyche-decided — no persona-local alias); both fields reference the imported
   type and the `ComponentPrincipal` name is retired. Add
   `{ ComponentKind signal-standard:lib:ComponentKind }`.
   Regenerate; `ComponentStatus`, `Presence`, `SpawnEnvelope` reference it.
4. **Any other ComponentKind users** — grep the `signal-*` repos; current
   evidence shows only these two declare a local `ComponentKind`.
5. **Roster reconciliation is the breaking change.** Both consumers move
   from a 7/9-variant local enum to the shared 14-variant one. Per the
   no-backward-compat override this is normal — all consumers rebuild at
   once against the reconciled roster. Old variant ordinals do not carry
   over; this is a coordinated rebuild, not a wire-compatible bump.

### Old→new variant mapping (both rosters)

Every old variant maps to exactly one reconciled variant (see census
table). signal-persona: `Mind Router Message System Harness Terminal
Introspect Orchestrate Spirit` → identical-named reconciled variants.
signal-criome: `Spirit Criome Router Mirror Lojix Persona Agent` →
identical-named reconciled variants. No renames, no merges beyond the two
shared names collapsing — only the **enum grows** to the union, so every
existing match arm stays valid and new arms are required only where code
exhaustively matches `ComponentKind` (the rebuild surfaces those).

## Prototype files

- `/tmp/signal-standard/schema/lib.schema` — canonical (positional/dot form).
- `/tmp/signal-standard/schema/lib.namevalue.schema` — validated variant
  (name-value form; lowered cleanly through schema-next `main`).
