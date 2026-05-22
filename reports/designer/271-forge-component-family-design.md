# 271 - Forge component family design (exploratory)

*Designer sketch of the forge component family — the workspace's
emerging build system, intended as the eventual Nix replacement.
Most of this report is direction-not-yet-implementation. Settled
material from psyche intent is marked `(settled)`; speculative
sketches and open questions are marked `(speculative)`.*

> **Intent record locations.** Works from psyche intent carried in
> the parent dispatch — the forge record and content-addressed-store
> record described as `recent` in `intent/workspace.nota`, the
> per-agent Criome identity record (record 38) in
> `intent/persona.nota`, and `intent/component-shape.nota` record 41
> (Nix-flake-versioned upgrade protocol). Future agents should
> resolve those record additions on disk and cite verbatim. Nothing
> here is inferred beyond the prompt's wording.

## 1. What forge is

(Settled — psyche intent.)

Forge is **the workspace's build-system component family** —
the persona-system layer that turns source into runnable
artifacts. Eventual role: **replace Nix** as the workspace's
build substrate. Today Nix carries the whole job; the trajectory
is forge taking it over piece by piece, with Nix phased out as
forge's coverage extends.

Three load-bearing framings:

- **Forge is a component family**, not a single component, with
  several legs that converge over time.
- **Forge is the persona-system layer above the build mechanism.**
  Initially it sits on top of Nix; eventually it owns the layer.
- **The first concrete forge wraps Nix straight up** — no
  reinvention before the wrap.

Forge addresses the immediate upstream concern of the
Nix-flake-versioned upgrade protocol (intent/component-shape.nota
record 41 — components versioned by their flake's content
address). Forge is the build-system shape that protocol needs to
talk to. If components ship as versioned flakes today, forge
owns what those flakes mean tomorrow.

## 2. The forge family map

(Mixed — top-level structure from psyche intent settled; the
internal members of each leg are designer speculation marked
inline.)

Current shape:

```
forge-core/               contract standardisation point
forge-nix-builder/        first concrete forge — wraps Nix
forge-<component>/        per-component forges (many initially, converge later)
workspace-content-store/  eventual; replaces Nix's store + substitution
```

(Settled.) `forge-core` is the standardisation point — where
sub-component forges agree on a single vocabulary.
`forge-nix-builder` is the first concrete forge, wrapping Nix
straight up. Per-component forges exist initially because each
sema-upgrade-shaped component may have its own forge;
convergence on forge-core happens later. The workspace-owned
content-addressed store is the family's eventual reach — the
workspace owns the whole vertical; the store replaces Nix's
store signing and substitution. Forge-core may be a pure-library
leg (contract crates only) rather than a daemon-bearing triad;
open in §9.

## 3. What is eternal in Nix's logic

(Direction settled — psyche flagged content-addressing, derivation
graphs, hermetic builds as eternal. The list below tracks that.)

Forge carries forward what Nix got right. Four abstractions are
eternal — they describe what a build *is*, not what one
implementation chose:

- **Content-addressing of build inputs and outputs.** A build
  artifact is identified by the hash of its bytes. Identity
  flows from content, not from a mutable name. Makes
  substitution sound, makes caches correct, and lets two
  machines confirm they computed the same thing without
  trusting each other.
- **Derivation graphs as build plans.** A build is a typed
  acyclic graph; nodes are derivations (inputs + builder +
  environment + output names), edges are dependencies. The
  graph is the plan; building means walking the graph. Every
  build system that scales has this shape.
- **Hermetic builds — no ambient state.** A derivation's inputs
  are exactly its declared inputs. No `$HOME`, no `/etc`, no
  host compiler that wasn't named, no network unless declared.
  Hermeticism is what makes content-addressing meaningful: if
  the build saw extra state, the output hash wouldn't capture
  the full input.
- **Binary substitution from a store.** A content-addressed
  output computed once can be transported to a recipient who
  confirms the bytes match without re-running the build —
  store-to-store byte transfer keyed by content address.

Forge keeps these four. Forge-core's contract names them
first-class (§6).

## 4. What does NOT belong in the build layer

(Direction settled — psyche identified authentication, binary
signing, per-build secrets, cross-host coordination as not
belonging. Specific destinations marked speculative where
psyche named them softly.)

Carve-outs — concerns Nix bundles into the build layer that
forge separates out:

- **Authentication.** (Settled — moves to Criome, per
  intent/persona.nota record 38, per-agent Criome identity.)
  Who is allowed to do what is not a build-system question.
  Nix's `trusted-users`, signed-binary caches, and substituter
  authentication all conflate identity with build mechanism. In
  the workspace, identity is Criome's concern; forge calls
  Criome when it needs to know who is asking. Matters most at
  the substitution boundary — "can this peer download this
  binary?" is a Criome question.
- **Binary signing.** (Settled — moves to the workspace-owned
  content-addressed store.) Nix bundles binary signing into its
  cache substitution protocol — substituters present
  ed25519-signed narinfos, the receiving daemon verifies against
  trusted public keys. Forge separates this: signing belongs to
  the workspace-owned content-addressed store (§8). The build
  system asks the store for a content address; the store decides
  if it can serve, signs if it does. Forge never holds signing
  keys.
- **Per-build secrets.** (Speculative destination — psyche said
  "probably persona-mind or a dedicated secrets component".)
  Per-build secrets (API token a build needs, private key for an
  outbound fetch) are cross-cutting; their natural home is
  either persona-mind or a dedicated secrets component that
  forge calls into. Forge does not own secret storage.
- **Cross-host coordination.** (Speculative destination —
  psyche said "probably persona-orchestrate".) Nix's remote
  builder mechanism (`/etc/nix/machines`, ssh-ng builders,
  schedule-this-here) is cross-host orchestration embedded in
  the build daemon. Forge separates this: orchestrating where a
  build runs is persona-orchestrate's domain. Forge declares the
  build plan; orchestrate decides which host runs it; forge on
  that host executes. Consistent with orchestrate owning
  mechanical allocation generally.

Pattern: forge keeps the **build math** — content addressing,
graph walking, hermeticism. Forge sheds the **cross-cutting
concerns** — identity, signing, secrets, orchestration — to
components that own them end-to-end.

## 5. Forge-nix-builder — the first concrete forge

(Direction settled — wraps Nix straight up. Operation sketch
below is speculative; the contract is not yet drafted.)

Forge-nix-builder is the first concrete forge — the
persona-system layer above Nix. Under the hood it speaks `nix
build` / `nix path-info` / `nix flake check` / `nix copy`; above
the hood it speaks forge-core's contract.

The wrap is intentionally thin at v1: Nix already implements the
four eternal abstractions correctly; the wrap exposes them
through a typed signal contract.

(Speculative operation sketch.) The daemon offers roughly:

| Operation | Sema class | What it does |
|---|---|---|
| `Build(BuildPlan)` | Mutate | Realise the plan; return a BuildResult with content addresses. Translates to `nix build`. |
| `Query(ContentAddress)` | Match | Is this address already realised? Translates to `nix path-info`. |
| `Substitute(ContentAddress, BuildHost)` | Mutate | Copy bytes for an address between hosts. Translates to `nix copy`. |
| `Validate(BuildPlan)` | Validate | Dry-run a plan without realising. Translates to `nix flake check` / `nix build --dry-run`. |

Wire payloads name forge-core types (§6), not Nix-specific
shapes. That is what makes the wrap a forge: the operations are
forge operations; the implementation underneath happens to be
Nix today.

(Speculative.) The owner contract carries configuration: which
substituters to use, which builders the daemon delegates to,
policy on local vs remote build slots. As forge matures, these
settings stop being Nix-specific and become forge-core
vocabulary. Forge-nix-builder is the only forge that has to know
Nix exists.

## 6. Forge-core — the standardisation point

(Direction settled — forge-core is where sub-component forges
standardise. The contract vocabulary below is speculative.)

Forge-core is the standardisation point for the family. As
per-component forges emerge and accumulate operations, the ones
that prove universal converge into forge-core. The contract is
where the family agrees on what a build *is*.

(Speculative vocabulary — the bones the contract probably
carries:)

- **`BuildPlan`** — a derivation graph: nodes are derivations
  (typed inputs + builder + environment + named outputs), edges
  are dependencies. What the caller submits.
- **`BuildResult`** — the realisation of a plan: for each
  declared output, a `ContentAddress` plus requested metadata
  (logs, duration, hermeticity assertion).
- **`ContentAddress`** — workspace-canonical name for a hash of
  bytes. Carries hash algorithm explicitly; carries the thing
  addressed (file, directory tree, structured output). The type
  that flows everywhere — the identity of every artifact.
- **`BuildHost`** — typed name of a machine that can execute a
  derivation. Carries reachability, declared capabilities
  (architecture, toolchains), and the Criome identity for
  authenticated delegation. Compatible with persona-orchestrate's
  cross-host coordination.
- **`Substitution`** — the act of moving bytes for a content
  address between stores. Forge-core names the act; the
  workspace-owned store (§8) eventually implements it without
  Nix in the middle.

(Speculative.) Forge-core probably owns no daemon — it is the
contract leg of the family, like signal-frame is the contract
leg of the actor system. The "standardisation" framing pushes
that direction. Forge-core also probably owns the **plan format**:
if `BuildPlan` is content-addressable too (it ought to be, given
§3), the plan's content address is itself a forge identity, and
the upgrade protocol (intent/component-shape.nota record 41) can
key on it directly. One place where the design's cohesion shows.

## 7. Convergence path — per-component forges to forge-core

(Direction settled — each sema-upgrade-shaped component may
have its own forge initially; convergence happens later. The
mechanism of convergence is speculative.)

Today, sema-upgrade-shaped components live with the
flake-per-component model — each has its own `flake.nix`, its
own derivations, its own `nix flake check`. As the workspace
migrates to forge, each such component naturally gets its own
forge.

(Speculative convergence mechanism.)

1. **Each per-component forge starts as a wrapper around
   forge-nix-builder.** It speaks forge-nix-builder's contract,
   adds component-specific policy (which flakes the inputs come
   from, which builder is preferred), exposes the result through
   its own working signal.
2. **Operations that prove universal migrate to forge-core.**
   As "build this", "substitute this address", "validate this
   plan" appear in every per-component forge, those operations
   move *up*. Per-component forges shed bespoke versions and
   call forge-core instead.
3. **Eventually, per-component forges are just policy.** The
   mechanism lives in forge-core; the per-component forge
   becomes a thin policy layer — "this component's substituters
   are X, its build hosts are Y" — on top of the universal
   vocabulary.

(Speculative.) At end-state, "a per-component forge" may not
be a separate daemon at all — it may collapse into a policy
record inside forge-core's database, with one forge-core daemon
serving all components. Whether per-component forges remain
distinct (fault isolation, per-component owners) or collapse is
open — see §9.

## 8. The eventual workspace-owned content-addressed store

(Direction settled — workspace owns the whole vertical
eventually; the store is what replaces Nix's store signing and
substitution. Components below are speculative.)

The forge family's end-state includes a **workspace-owned
content-addressed store** — what replaces Nix's `/nix/store`
plus its signed-substitution protocol.

(Speculative components — three pieces:)

- **A content-addressed blob store.** Bytes keyed by content
  address (§6). Read by address; write produces an address. The
  workspace's analogue of `/nix/store` — substrate that holds
  realised outputs and source trees.
- **A derivation graph store.** Where `BuildPlan`s themselves
  live, content-addressed. Makes reproducibility legible: given
  an output's address, ask "what plan produced this?" and walk
  back to source.
- **The substitution protocol.** How peers transfer bytes
  between stores. Owns signing (carve-out from §4): a peer
  authenticates through Criome; the store decides whether to
  vend; if it does, it signs the bytes with the workspace's key;
  the receiver verifies against the workspace's trust root.

(Speculative.) The substitution protocol replaces Nix's "binary
cache" — but without the conflation of signing and
authentication. Criome answers who-you-are; signing is just
integrity attestation (these bytes match the address).

(Speculative.) The workspace-owned store is plausibly the **last
piece of forge to land**. As long as Nix's store underneath
forge-nix-builder works, the workspace rides on it. The store
gets owned when the workspace needs something Nix doesn't give —
typed entry from non-Nix forges, or signing policy Nix's narinfo
signing doesn't express.

## 9. Open design questions

(All speculative — this report is exploratory; the questions
below are what future designer work has to settle.)

Many. In no particular order:

- **Is forge-core a triad or a pure-library leg?** If
  pure-library (contract crates only), it follows the
  signal-frame / signal-sema carve-out. If a triad with its
  own daemon, it implements operations centrally. Open.

- **Does forge-nix-builder ever shed Nix entirely?** First
  version wraps Nix; end-state replaces Nix. Whether
  forge-nix-builder gradually does more work directly (until
  no Nix call is left), or retires in favour of a new
  forge-native, is open.

- **How do per-component forges register with forge-core?**
  Especially before forge-core has a daemon. Registration
  policy state in forge-nix-builder? A forge-registry
  component? Persona-mind? Open.

- **How does the upgrade protocol talk to forge?** Record 41
  keys on flake content addresses; forge takes responsibility
  for that layer. Upgrade protocol migrates to keying on
  forge's `BuildPlan` addresses. Whether the protocol gets
  rewritten in forge terms or forge exposes a flake-content
  compatibility surface is open.

- **Where does the secrets carve-out land?** Psyche named
  persona-mind or "a dedicated secrets component" as probable.
  Choosing between (or building) is open.

- **How are hermeticity assertions surfaced?** Nix asserts
  hermeticity implicitly through the sandbox; forge-core
  surfaces it as a typed assertion in `BuildResult`. Shape and
  how forge-nix-builder populates it from Nix's sandbox is open.

- **Cross-architecture builds and platform vocabulary.** Nix
  carries platform strings (`x86_64-linux`) through
  derivations; forge-core needs a typed equivalent on
  `BuildHost` and derivation declarations. Taxonomy open.

- **Forge-core's audit/observation surface?** Per the universal
  Tap/Untap mandate, forge daemons must be observable. What
  events does a build emit — `BuildStarted`,
  `BuildOutputRealised`, `BuildFailed`, `SubstitutionPerformed`?
  Open.

- **How does forge interact with persona-orchestrate for
  cross-host builds?** Does forge ask orchestrate "where should
  I run this?" before each build, or does forge carry a host
  pool that orchestrate populates? Open.

## 10. What this report is not

This report sketches the family at the level of names, roles,
and direction. It does not:

- Sketch implementation (code shape, contract literals, daemon
  internals).
- Reproduce Nix internals. §3 names the abstractions forge
  inherits; Nix's implementation details are out of scope.
- Touch the sema-upgrade component design (separate, /270).
- Touch the Magnitude type design (separate, /269).

Next designer-lane work, presumably:

1. Resolve the open record-locations in `intent/workspace.nota`
   so this report's footing is fully on disk, not just in the
   parent dispatch.
2. Choose between §9 questions one at a time, with psyche
   escalation where needed.
3. Draft forge-core's contract — `BuildPlan`, `BuildResult`,
   `ContentAddress`, `BuildHost`, `Substitution` — as a
   contract-crate proposal once the family's shape settles
   enough to commit to a signal tree.

## See also

- `skills/component-triad.md` — universal shape forge follows.
- `skills/nix-discipline.md` — what forge wraps today; hygiene
  forge inherits.
- `skills/nix-usage.md` — Nix CLI surface forge-nix-builder
  translates against.
- `intent/component-shape.nota` record 41 — Nix-flake-versioned
  upgrade protocol; the immediate upstream concern.
- `intent/persona.nota` record 38 — per-agent Criome identity;
  where the authentication carve-out lands.
- `reports/designer/263-schema-specification-language-design.md`
  — adjacent content-addressable direction; the schema-layout
  and build-plan address machineries probably share vocabulary.
- `reports/designer/270-*` (sema-upgrade) and `269-*` (Magnitude) — sibling exploratory reports.
