# Perspective 1 — Telos and Layers

*Grounding subagent perspective for session 675-system-with-perspective.
Wide-angle, source-read. Sources cited inline by absolute path + line.*

## The telos in one paragraph

The psyche is building **Persona** — a meta-AI system that organizes
language models into a structure emulating human intelligence, where the
components are *dumb mechanism* and all thinking happens in agent LLMs
that drive those components through CLIs and through Spirit; no component
works without an LLM on the other end of the wire
(`/home/li/primary/INTENT.md:132-139`). The far horizon for the substrate
under Persona is the **eventual Criome / eventual Sema**: a *universal
computing paradigm expressed in Sema that replaces Git, the editor, SSH,
and the web* — encompassing programming, version control, network
identity, validation, and auth/security across the whole stack
(`/git/github.com/LiGoldragon/criome/INTENT.md:20-23`), with Sema as *the
universal medium for meaning — a self-hosting computational substrate, a
fully-typed human-language representation, a universal interlingua*
(`/home/li/primary/protocols/active-repositories.md`, `sema` row). The
governing aesthetic is **software eventually impossible to improve**: in a
bounded domain, the right shape chosen carefully and observed cleanly,
ranked Clarity > Correctness > Introspection > Beauty
(`/home/li/primary/ESSENCE.md:53-65`). Beauty is the *criterion*, not a
finish: "If it isn't beautiful, it isn't done… ugliness is evidence the
problem is unsolved" (`ESSENCE.md:76-81`). Explicitly *not* optimized for:
speed, feature volume, "minimum viable," estimates, or backward
compatibility for systems being born (`ESSENCE.md:67-73`).

## Primacy of psyche intent (the cornerstone)

Intent is **primordial** — the universal fallback when an agent is unsure
what to do; the agent's *core work* is to clarify and capture intent, and
whatever intent is clear enough to warrant action becomes action
(`ESSENCE.md:8-12`, `/home/li/primary/INTENT.md:8-13`). Load-bearing
sub-principles, all source-grounded:

- **Psyche is the human.** Only natural-language psyche prompts are a
  source of *new* intent; agent messages and agent-written files are not
  psyche (`ESSENCE.md:14-16`).
- **Inferring intent is forbidden** — "bearing false witness, the most
  forbidden act." False intent corrupts the layer because downstream
  agents treat it as load-bearing truth. Capture is conservative;
  understate when ambiguous; missing intent is recoverable, over-extending
  is not (`ESSENCE.md:33-45`, `INTENT.md:40-45`).
- **Work instructions are not intent.** "Implement X / fix the macro /
  write the report" is task state; the log captures only what persists
  past the task (`ESSENCE.md:47-50`). The Spirit gate runs on *every*
  psyche prompt, choosing exactly one outcome: no-capture / observe-refresh
  / ask / edit-existing / Record (`INTENT.md:32-45`,
  `/home/li/primary/AGENTS.md` §"Run the Spirit gate").
- **The intent layer outranks every other surface**, and supersession is
  always explicit — *only the psyche can supersede*; an agent meeting
  documented intent that seems wrong **asks, it does not override**
  (`ESSENCE.md:22-27`, `INTENT.md:26-30`).

## The intent layer — three surfaces, increasing distillation

From raw to gold (`/home/li/primary/INTENT.md:16-25`):

1. **Spirit store** — the raw log of psyche statements as typed intent
   records (agent-clarified description, kind, magnitude, daemon-stamped
   time). The sole intent substrate.
2. **Per-repo `INTENT.md`** — each project's psyche intent synthesised
   into prose; an agent entering a repo reads it *first, before code*
   (`ESSENCE.md:29-31`; AGENTS.md required-reading item 7). Every repo
   needs one; its absence is the first gap to fill.
3. **`ESSENCE.md`** — the universal core, "the gold of the gold"; when a
   downstream rule conflicts, essence wins.

A subtlety: every statement in an essence/intent surface must be anchored
in an actual Spirit record — "a claim with no record behind it does not
belong, or the intent is recorded first" (`INTENT.md:62-64`). The intent
layer is thus *not* free-form documentation; it is a distillation with a
provenance obligation back to Spirit.

## Today-vs-eventually scope discipline

The sharpest discipline cutting across the whole system: **today's
component is one realization step, not the eventual vision; do not let
eventual scope leak into today's shape.** Worked example —
`/git/github.com/LiGoldragon/criome/INTENT.md:12-33`: today's `criome` is
a *minimal Spartan BLS-signature authentication and attestation daemon*
(identity registry, sign/verify, delegation grants, replay guard, typed
audit log); the *eventual* `Criome` is the universal computing paradigm
above. "Today's Spartan daemon… brings forward the auth/identity slice; it
does not carry the eventual scope." The same today/eventual split is
called out for `sema` (today: typed storage kernel of redb + rkyv + schema
guard; eventual: the universal medium for meaning) in
`active-repositories.md` (`sema` row) and the adjacent `criome` row.

This pairs with the **no-backward-compatibility-pre-production** override
(`AGENTS.md` §"Hard overrides"; `ESSENCE.md:96-104`): the restructuring
stack has no production to protect, so design bottom-up for the single
best shape and expect every component to change. Two deploy stacks
coexist: production runs the old monolith on `main` in canonical
checkouts; the lean rewrite lives on rewrite branches in worktrees and has
*not* been cut over — cutover is a coordinated multi-repo merge after
parity, never piecemeal folding (`INTENT.md:91-98`).

**Grounding finding (dangling reference):** `criome/INTENT.md:84-85`
points to `primary/ESSENCE.md §"Today and eventually"` for the scope
discipline, but `ESSENCE.md` has no such section — its headings are
Intent-is-the-cornerstone / Inferring-is-forbidden / What-I-am-building /
What-I'm-not-optimising-for / Beauty / Naming / Backward-compatibility
(`ESSENCE.md`, grep of `^##`). The scope discipline now lives in per-repo
`INTENT.md` files and `active-repositories.md`, not ESSENCE. The
cross-reference is stale and worth flagging to the orchestrator.

## The vertical layer stack

The system is built as a top-down stack, intent at the apex flowing down
to running metal. Each layer is grounded:

```
┌─ INTENT (Spirit) ───────────────────────────────────────────────┐
│  Primordial. Psyche NL prompts → typed Spirit records →          │
│  per-repo INTENT.md → ESSENCE.md. Outranks all agent surfaces.   │
│  Repos: spirit / signal-spirit / meta-signal-spirit.             │
│  (ESSENCE.md:8-31; INTENT.md:8-30)                                │
├─ SCHEMA (typed source of truth) ────────────────────────────────┤
│  "A language is data — structural macros all the way down."      │
│  Schema is a specialized NOTA dialect (a .schema file IS NOTA).  │
│  nota-next (parser + StructuralMacroNode codec, frozen seed)     │
│   → schema-next (schema-in-Rust, no separate Asschema step)      │
│   → schema-rust-next (LOWERS to Rust via quote!/proc-macro2).    │
│  BUILD-TIME ONLY: the compiler emits each component's typed Rust │
│  and never links into the runtime binary.                        │
│  (INTENT.md:142-162; active-repositories.md schema-* / nota-next) │
├─ COMPONENTS (triads) ───────────────────────────────────────────┤
│  Every stateful capability = a triad of THREE repos:             │
│   <component> (daemon + bundled thin CLI),                       │
│   signal-<component> (working wire contract),                    │
│   meta-signal-<component> (meta policy contract).                │
│  Inside the daemon: a runtime triad of three schema-driven       │
│  planes — Signal + Nexus + SEMA. Binaries carry only strict      │
│  rkyv wire + storage contracts; daemons take one binary startup. │
│  (skills/component-triad.md; AGENTS.md §"Component triad")        │
├─ STORAGE / ENGINE (within & under components) ──────────────────┤
│  sema (typed kernel: redb + rkyv + schema guard) +              │
│  signal-sema (Assert/Mutate/Retract/Match/Subscribe/Validate) + │
│  sema-engine (full DB engine library). Each component owns its   │
│  own <component>.sema store.                                     │
│  (active-repositories.md sema / signal-sema / sema-engine)       │
├─ DEPLOY (CriomOS / cluster) ────────────────────────────────────┤
│  CriomOS = NixOS host platform for the sema ecosystem; consumes  │
│  projected Horizon data, exposes one network-neutral             │
│  nixosConfigurations.target. Cluster/node/user identity enters   │
│  via lojix-projected inputs; modules render projected facts,     │
│  never branch on concrete names. CriomOS-home = home-manager     │
│  surface; CriomOS-test-cluster = cluster fixtures.               │
│  (CriomOS/INTENT.md; active-repositories.md CriomOS rows)         │
└──────────────────────────────────────────────────────────────────┘
```

Two cross-cutting principles thread the whole stack downward:

- **Role is type — the dimensional principle.** A struct field's role is
  its type; no struct has two fields of the same type; field-name equals
  type-name by default; an explicit field name signals a missing newtype
  or a collection (`INTENT.md:165-172`, Spirit `ov30`). This is the
  newtype-per-domain-value rule pushed to a newtype-per-role endpoint.
- **Push, not poll.** Polling design is forbidden across every layer;
  producers push events, consumers subscribe; when a mechanism appears
  poll-only, escalate deeper into the stack and build a real event surface
  (`INTENT.md:67-72`, Spirit `c5nq`).

## Governing principles (the apex set)

1. **Intent is primordial; ask when unclear; never infer.**
   (`ESSENCE.md:8-20`)
2. **Inferring/recording un-stated intent is forbidden — bearing false
   witness.** (`ESSENCE.md:33-39`)
3. **Clarity > Correctness > Introspection > Beauty**; beauty is the
   done-criterion. (`ESSENCE.md:53-81`)
4. **Today is not eventually** — realize one slice; don't carry eventual
   scope into today's shape. (`criome/INTENT.md:20-23`,
   `active-repositories.md`)
5. **No backward compatibility pre-production**; compatibility binds only
   at explicitly-declared boundaries. (`ESSENCE.md:96-104`, AGENTS.md
   overrides)
6. **The language is data; the compiler is build-time only; binaries
   carry only rkyv contracts.** (`INTENT.md:142-162`)
7. **Component triad = daemon + working signal + meta policy signal;
   single-source the wire types from the contract repo.** (AGENTS.md;
   `skills/component-triad.md`)
8. **Components are dumb mechanism; the LLM is the thinking on the other
   end of every wire.** (`INTENT.md:132-139`)
9. **Role is type; push not poll; spell full English words; names drop
   ancestry.** (`INTENT.md:67-72,165-172`; `ESSENCE.md:83-94`)
10. **Workspace truth lives in files every agent can open; the intent
    layer outranks every agent-written surface.** (`INTENT.md:117-122`,
    `ESSENCE.md:22-27`)

## Sources read (absolute paths)

- `/home/li/primary/ESSENCE.md` (full)
- `/home/li/primary/INTENT.md` (full)
- `/home/li/primary/AGENTS.md` (overrides + role model; via session
  context + cross-checks)
- `/git/github.com/LiGoldragon/criome/INTENT.md` (full)
- `/home/li/primary/skills/component-triad.md` (triad shape, two-triad
  distinction)
- `/home/li/primary/protocols/active-repositories.md` (live repo map:
  schema stack, sema stack, deploy stack, today/eventual rows)
- `/git/github.com/LiGoldragon/CriomOS/INTENT.md` (deploy layer)
