# 20 — Arca content-addressed substrate: design exploration

Date: 2026-05-17
Role: system-assistant
Scope: Standalone exploration of Arca as the user described it,
weighed against the existing `arca` repo at
`/git/github.com/LiGoldragon/arca`. Engages with the user's specific
debates (short hashes, path topology, file-vs-directory naming,
length-scaling). Identifies what's already designed, what the user's
revamp adds, what should be kept, what should be revised. Names the
**lojix-mesh-integration** use case as the first consumer.

Pairs with SYS/19 (deploy mesh + Arca substrate together). This
report is Arca-only.

---

## 0. Critical context: there is already a substantial arca repo

The user said "*it's already a repository that I've created before*"
and proposed a revamp. The existing repo already has:

- A mature `ARCHITECTURE.md` (~8 KB).
- Library + daemon split (`arca` library is reader; `arca-daemon` is
  the only writer).
- Multi-store layout (`~/.arca/<store-name>/<hash>/`).
- Per-store redb index DB.
- Write-only staging (`~/.arca/_staging/`) with TOCTOU-protected
  atomic move into canonical location.
- Capability tokens signed by criome gating writes.
- "Day-one canonical alongside forge" intent.
- Blake3 as the canonical hash.
- Skeleton-as-design with `todo!()` bodies (per skill).

**The user's proposal is a revamp, but several existing properties
are good and should likely survive.** SYS/20 lays out the axes of
disagreement explicitly so the user can decide which existing
properties to keep.

---

## 1. The five axes of the revamp

The user's verbal proposal touches five distinct design choices, each
independently revisable:

| Axis | Existing | User's revamp | Recommendation (see below) |
|---|---|---|---|
| A. Component shape | library + daemon | triad: CLI + daemon + signal-arca | **Keep both — add CLI/signal as a *layer* over existing reader-library** |
| B. Hash length in path | full blake3 (~64 hex chars) | short (3 chars → grows on collision, scales by file size) | **Reject dynamic-grow; recommend fixed 16-hex (64-bit) prefix** |
| C. Path topology | `~/.arca/<store>/<hash>/` (always directory) | `/Arca/<hash>` (dir) **or** `/Arca/<hash>-<filename>` (file) | **Keep always-directory for canonical store; add named-symlink view via daemon API** |
| D. Multi-store with capability tokens | yes | (not mentioned — implicit single-store) | **Keep multi-store; lojix integration uses one named store** |
| E. Cross-node propagation | (not in existing) | "parallel call between Arca daemons" peer mesh | **Add — this is the genuinely new piece** |

The big architectural addition (axis E) is what makes Arca useful for
the lojix mesh. The other axes are smaller adjustments to existing
shape.

---

## 2. Axis A — component shape: library + daemon + CLI + signal-arca?

The user's stated rule: "*All of my components are going to be triad
components. They're going to have the CLI, daemon, and the signal
contract to talk to it.*" Per `skills/component-triad.md`, this is
the workspace-wide invariant.

Existing arca's library-as-reader pattern is a useful asymmetry:
- **Reads are direct filesystem access** (no daemon round-trip). Any
  process links `arca` and reads.
- **Writes go through `arca-daemon`** (only privileged writer; gated
  by capability tokens).

The triad shape is about the *write* path: how does an external
caller (operator, lojix-daemon, anything-else) ask Arca to ingest
content? Today this is undefined in the existing repo (the daemon is
skeleton). The triad shape would add:

- `signal-arca` contract (request/reply for writes + non-direct
  reads + metadata queries).
- `arca` CLI as the thin text adapter.

**Reads should stay direct.** Routing every read through a daemon
adds latency to a high-frequency operation (every `exec` of a binary
under `/arca/<hash>/bin/foo`). Direct filesystem access via the
`arca` library is good design and matches what nix-store does.

**Triad applies to the write/admin path.** signal-arca verbs for:
- `IngestContent` (with capability token)
- `QueryMetadata { hash }` (returns sema record)
- `CreateNamedView { hash, target_path, filename }` (creates a
  symlink at request)
- `ListContents` (for admin/audit)
- `PinHash { hash, reason }` / `UnpinHash`
- `EnumerateStores` (admin)

The CLI maps to these verbs. signal-arca is the wire.

**Direct-FS reads remain library-only.** No CLI verb needed for "open
this hash and read its bytes" — that's `cat /arca/<hash>` or an
`open()` call. The library exposes typed helpers but no daemon round
trip.

This preserves the existing library's value while satisfying the
triad rule.

---

## 3. Axis B — hash length in the path: a real debate

The user explicitly invited debate:

> "*I really want to, like, debate that hard because these file paths,
> when they end up in things like, well, anywhere really, but
> especially LLM context, they become extremely costly because hashes
> are not recognizable tokens.*"

That cost concern is real. A full blake3 hash is 32 bytes = 64 hex
chars; at LLM tokenization rates of ~1 token per character for
random hashes, every reference burns 64 tokens. In a chat with 100
hash references, that's 6,400 tokens. Real money.

### The user's specific proposal

Start at 3 hex chars (12 bits). On collision, **rename both files** to
a longer prefix until disambiguated. Scale baseline by file size:

> "*files up to 10 megabytes or 3 characters, up to 105 [100?], and up
> to a gigabyte, say, there's 7*"

### Why I'm pushing back on the dynamic-rename approach

The headline concern: **cross-node consistency**.

If Tiger's local Arca has file X at `/arca/abc` and Balboa receives
the same content but already had `/arca/abc` taken by something else,
Balboa extends to `/arca/abcd`. Tiger says "give me file abc" → on
Balboa that's `abcd`. Every reference becomes per-node-translated.

The only fix is to either:
- Carry the full-hash on the wire (so peers can canonicalize). Then
  the short hash is **only** a local-disk-and-CLI convenience; LLM
  context still sees the full hash. **Defeats the original cost
  argument.**
- Coordinate hash assignment across nodes (every node uses the same
  prefix length for the same content). That's a distributed
  consensus problem.

Neither is acceptable.

A second concern: **rename cascade**. The user proposed that Arca
"keep track of all the linked files so that it could change the link
dynamically." This means every consumer that ever resolved a hash to
a path has a back-reference Arca tracks, and renames trigger
notifications. That works in principle, but:
- Adds a stateful back-link relation between Arca and every consumer
  (currently a one-way relation: consumers read, Arca doesn't know).
- Cross-node cascades are even harder (does Balboa renaming a local
  hash trigger a notification to Tiger's lojix-daemon?).
- Notifications can race with reads (consumer caches the path, Arca
  renames, consumer's cached path is now stale).

### My counter-proposal: fixed reasonable prefix

Use a **fixed prefix length** that:
1. Is short enough to be much cheaper than full blake3.
2. Is long enough that birthday collision is negligible for any
   realistic single-user corpus.

Birthday collision math:

| Prefix bits (hex chars) | 1M items | 10M items | 100M items |
|---|---|---|---|
| 32 bits (8 hex) | ~12% | ~99% | ~100% |
| 48 bits (12 hex) | ~0.18% | ~18% | ~100% |
| 64 bits (16 hex) | ~3 × 10⁻⁸ | ~3 × 10⁻⁶ | ~0.03% |
| 80 bits (20 hex) | ~5 × 10⁻¹³ | ~5 × 10⁻¹¹ | ~5 × 10⁻⁹ |

**Recommendation: 16 hex chars (64 bits).** Birthday collision is
essentially zero for any single-user-lifetime corpus. LLM cost is
~25% of full blake3 (16 chars vs 64). Path becomes
`/arca/3f8e2a1b9c4d5e6f` — readable, copyable, distinct.

If the user wants to go further: 12 hex (48 bits) is fine for
≤1M items per store. Below 12 is risky.

**Same fixed prefix everywhere on every node, no dynamic rename.** If
two pieces of content ever collide at 16 hex (essentially
impossible), one of them rejects ingest with `HashPrefixCollision`
and we deal with it as the operational incident it would be. We do
**not** try to make this graceful in the path layout.

If even further LLM-cost optimization matters later, the daemon API
could expose a short alias scheme that doesn't touch the canonical
path: `arca alias create my-deployment-plan-2026-05-17 <hash>` → the
alias is stable, human-readable, and never collides because it's
operator-named. That's a better answer to the LLM-cost problem than
shortening the canonical hash.

### Length-scaling by file size

The user proposed: small files → short prefix, large files → long
prefix. I think this is over-engineering:
- File size has no relation to hash collision probability (the hash
  domain is the same).
- Length-scaling makes every path's length depend on something the
  reader has to compute (file size) — unpredictable from the hash
  alone.
- Operationally weird: a file growing across a threshold means
  renaming.

A fixed prefix avoids all this.

---

## 4. Axis C — path topology: file vs directory naming

The user proposed: directories at `/Arca/<hash>/`, regular files at
`/Arca/<hash>-<filename>`, with the rule that two files only clash
if hash + filename match.

The existing arca takes a different approach: **everything is a
directory**, and the canonical encoding of a single-file entry
includes the filename inside the encoded tree (so two files with same
bytes but different names hash differently, and naturally don't
collide).

### My read

The user's `<hash>-<filename>` approach has a hidden cost:
**deduplication is lost for regular files.** If `config.toml` and
`data.bin` happen to have identical content (unlikely but possible —
e.g. both contain `{}\n`), they end up as two separate copies under
two paths. Pure content-addressing would store one.

The user might want this — preserving filename in the path is more
human-readable when listing `/arca/`. But it's not really content-
addressed anymore; it's "content-hash-prefixed and filename-tagged".

### Three coherent options

**Option C1 — Always-directory (existing arca).**
- Canonical: `/arca/<hash>/` always points at a directory; single
  files are encoded as a one-entry directory `<hash>/<filename>`.
- Hash captures filename → dedup naturally distinguishes "same bytes,
  different name" without conflating.
- Listing `/arca/` shows only hash directories — clean but opaque.
- For "I need this file with its filename": consumer asks daemon for
  a named symlink at a request path.

**Option C2 — User's proposal (hybrid).**
- Dirs: `/arca/<hash>/`
- Files: `/arca/<hash>-<filename>`
- Filename is identity for regular files; consequence: same bytes
  with different names = two store entries.
- Listing `/arca/` is more legible (`abc123-config.toml` is
  recognizable).
- Trade: usability gain, dedup loss.

**Option C3 — Pure content addressing (always-file-form).**
- Canonical: `/arca/<hash>` is just bytes; no filename anywhere.
- Filename lives only in the sema-db as metadata.
- For "I need this file with its filename": same daemon-symlink
  pattern as C1.
- Cleanest theoretically; least usable for direct browsing.

### Recommendation

**Option C1 (keep existing arca's always-directory approach), with
an explicit named-symlink API.**

Reasoning:
- Preserves dedup (the architectural promise of content-addressing).
- Matches existing arca, so we don't throw away work.
- The "I want to see meaningful names" use case is solved by an
  on-demand symlink view, not by the canonical store layout.
- The existing arca's canonical encoding already handles single-file
  vs directory uniformly.

The user's usability concern is real but better addressed in the
daemon API ("`arca view <hash> --at /tmp/view/config.toml`") than in
the canonical path layout.

---

## 5. Axis D — multi-store with capability tokens

The user did not mention multi-store. The existing arca has it
explicitly: `~/.arca/system/`, `~/.arca/user-foo/`, `~/.arca/project-
bar/`, with per-store redb indexes and capability tokens scoped to a
target store.

This is a real feature worth keeping:
- System artifacts (Nix outputs, Horizon plans) should not share a
  trust boundary with user files (documents, attachments).
- Capability tokens scoped to a store give clavifaber a natural
  authorization unit ("this writer may write to store X but not to
  store Y").
- For lojix integration: lojix-daemon writes plans to a dedicated
  store (e.g. `~/.arca/lojix-runtime/` or `/arca/system/` on
  privileged daemons).

**Recommendation: keep multi-store.** Lojix integration uses one
named store, scoped to a lojix-issued capability token.

---

## 6. Axis E — cross-node propagation: the genuinely new addition

The existing arca is single-host. The user's framing — "*creating a
parallel call between the Arca daemons on all these machines to
propagate all of the inputs as content addressed Arca files*" — adds
a peer-mesh layer that doesn't exist today.

This is the addition that makes Arca useful as the lojix substrate
(per SYS/19). It's also the biggest implementation surface.

### What it needs

**E.1 — Peer discovery.** Each arca-daemon needs to know which other
arca-daemons it can ask for content. Initial form: static config
listing peer addresses. Later: dynamic, possibly via clavifaber's
node registry.

**E.2 — Fetch-by-hash protocol.** `signal-arca` verb: `FetchHash
{ hash, requested_by }`. Returns either content (atomic move into
local store after verification) or `HashNotPresent`. Streaming for
large trees.

**E.3 — Discover-where-hash-lives.** When a daemon doesn't have a
hash locally, it needs to find which peer does. Options:
  - **Pull-broadcast:** ask all peers in parallel; first one with the
    hash wins. Simple, bandwidth-cheap for small queries, wasteful
    for hot content.
  - **Directory layer:** a content-location index, possibly held in
    sema-db across the cluster. More complex; better at scale.
  - **Caller hint:** the request that triggered the fetch (e.g. the
    `BuildForJob` from lojix) says "this hash came from Uranus." The
    local Arca tries Uranus first. Falls back to broadcast.
  - **Recommended for v1:** caller-hint + broadcast fallback. No
    directory layer.

**E.4 — Authorization.** Who can fetch what from whom? Trust is
*not* intrinsic — the content's hash proves integrity but not "this
peer is allowed to read this." For lojix's use case, every node in a
cluster trusts every other node, so this is permissive
within-cluster. Cross-cluster is more interesting; defer to v2 like
the lojix mesh.

**E.5 — GC interaction.** If Uranus writes content, sends a hash to
Tiger, then GCs the content locally, Tiger's fetch fails. The
"plan-artifact-pinned-until-DeploymentReleased" mechanism that
SYS/19 §5 mentioned for lojix needs an Arca-side equivalent: a hash
is pinned (held against GC) as long as some peer is known to be
fetching it, plus a grace window.

**E.6 — Bandwidth + cost awareness.** Same considerations as the
lojix mesh (metered networks, slow links). Probably v2. v1: best-
effort fetch over Tailnet.

### Recommended v1 minimum

- Static peer config (no discovery).
- `FetchHash` verb with caller-hint routing + broadcast fallback.
- Within-cluster permissive authorization (any cluster member can
  fetch any hash from any other).
- "Pin until peers ack" semantics for content pushed in service of a
  request.

That's a real chunk of work but bounded.

---

## 7. Integration with lojix (the first consumer)

For SYS/19's mesh-deploy flow, the lojix↔Arca integration looks
like:

```
Uranus lojix-daemon                Uranus arca-daemon
  │                                  │
  ├─ projects plan ─────────────────▶│ IngestContent(plan)
  │                                  │ ──▶ ArcaHash(planA)
  │
  ├─ BuildForJob{plan: ArcaHash(planA)} ──▶ Tiger lojix-daemon
  │                                            │
  │                                            ├─ asks local arca-daemon
  │                                            │   for ArcaHash(planA)
  │                                            │
  │                              Tiger arca-daemon
  │                                ├─ not local
  │                                ├─ caller-hint says Uranus
  │                                ├─ FetchHash from Uranus arca-daemon
  │                                ├─ verifies blake3 matches
  │                                └─ atomically into local store
  │                                            │
  │                                            ▼
  │                                  Tiger lojix-daemon reads plan
  │                                  begins build...
```

Three properties this gives lojix:

1. **Determinism.** Every peer reads identical bytes (verified by
   hash). No "Uranus and Tiger projected slightly different
   horizons."
2. **Cheap wire.** signal-lojix messages stay small (a hash + role
   + endpoint, not the full plan).
3. **Decoupled propagation.** signal-lojix doesn't carry bulk data;
   signal-arca handles that on its own schedule with its own
   backpressure.

The same pattern applies to other artifacts lojix might want to
share: target system flake outputs (if not via /nix/store), shared
secrets (if encrypted), large config blobs.

**Not for v1: shipping nix-store NAR closures via Arca.** Nix has
its own efficient closure-copy mechanism (`nix copy --to ssh://...`)
that handles incremental dedup against the target's existing store.
Re-inventing that in Arca is a v3+ research project. The lojix mesh
should use `nix copy` (or the SshStore source) for closures, and
Arca for the smaller artifacts.

---

## 8. Gaps in the user's described Arca intent

These are decisions the user didn't make explicit; each needs an
answer before implementation.

### G_arca_1 — Where on disk does the canonical store live?

User said `/Arca/<hash>`. Existing arca says `~/.arca/<store>/<hash>/`.
- `/Arca` (root-level) is system-wide, requires root to create, more
  visible.
- `~/.arca` (user-home) is per-user, less privileged, lojix-daemon
  runs as some uid that has access.
- The existing arca's path is already in use (presumably tested).

**Recommend keeping `~/.arca/<store-name>/<hash>/` (or, if a
system-wide store is wanted for system artifacts, a parallel
`/arca/<store-name>/<hash>/`).** Multi-store from §5 makes this a
clean fit.

### G_arca_2 — Library + daemon + CLI: read still goes through library?

Yes — see §2. Reads bypass the daemon for performance; writes always
go through daemon for TOCTOU protection + capability check. The CLI
is a new front-end for writes/admin only.

### G_arca_3 — Relationship to criome's capability tokens

Existing arca expects criome-signed capability tokens for writes.
The user's revamp narrative doesn't mention criome. Is that part
preserved?

**Recommend: yes, preserve.** Capability tokens are the existing
authorization mechanism; lojix-daemon's writes happen under a
capability token issued by criome (or clavifaber as criome's
delegate).

### G_arca_4 — Index DB scope

Existing arca uses per-store redb. The user mentioned sema as
source of truth ("*the real source of truth or important reference
for all of the files in the ARCA store, which is managed by the ARCA
daemon, is going to be held in the ARCA SEMA database engine*").

These can coexist: sema is the authoritative metadata store (what
the hash *means*, who created it, when, why); redb is the per-store
fast lookup (hash → on-disk path + size + presence flag). The
user's framing implies sema is the long-term answer; whether redb
stays as an intermediate index or gets folded into sema is a v2
question.

**Recommend v1: keep redb per existing arca; sema records hold the
semantic metadata.**

### G_arca_5 — Cross-cluster Arca

Like cross-cluster lojix mesh, defer to v2.

### G_arca_6 — What happens to existing skeleton-as-design bodies?

Existing arca has `todo!()` bodies in `writer.rs`, `bundle.rs`,
`deposit.rs`, `token.rs`, `main.rs`. The user's revamp implies these
get implemented. The skeleton is consistent with what's been
discussed — the bodies are still TBD.

### G_arca_7 — Nix CA derivations relevance

User mentioned: "*the next store has been trying to move to an
intentional store [content-addressed derivations] for years now, and
there's maybe some code in there for that. And we should actually
research that in parallel because it's probably going to be
relevant in case we want to move some next derivations into Arca.*"

Brief context: Nix CA derivations (`experimental-features =
ca-derivations`) are content-addressed at the output level — the
hash of the output, not the hash of the derivation recipe. This
makes Nix store paths content-addressed.

Implications:
- If/when CA derivations stabilize, Arca and Nix CA store could
  share content (a Nix output at blake3 hash X could live in /arca/X
  as well).
- Today: Nix outputs are recipe-hashed; Arca artifacts are content-
  hashed. They live in separate stores with separate hash domains.
  No conflict, no sharing.
- v1 recommendation: ignore CA derivations; Nix store and Arca are
  separate. Revisit when CA derivations are stable (not yet).

---

## 9. What to land first (tactical proposal)

If the user adopts these recommendations, the order I'd build in:

1. **Existing arca: implement the skeleton bodies.** Per existing
   skeleton-as-design discipline; the writer/deposit/token/daemon
   bodies. This is already-designed work; finish it.
2. **Add signal-arca contract repo + thin `arca` CLI.** Triad
   completion. CLI exposes the write/admin verbs; signal-arca is the
   wire.
3. **Add cross-node `FetchHash` to signal-arca + arca-daemon.**
   Caller-hint routing + broadcast fallback. Static peer config.
   This is the genuinely-new addition.
4. **Integrate as the lojix plan-artifact substrate.** lojix-daemon
   writes plan artifacts to local Arca; signal-lojix carries Arca
   hashes; peer lojix-daemons fetch via local Arca.
5. **(Later)** sema-as-Arca-metadata-source-of-truth migration.
6. **(Later)** GC pinning via lojix's `DeploymentReleased`.

Step 1 is independent of everything else. Step 2 is the triad
completion. Steps 3 + 4 are the new substrate work; they can land
together as the "arca mesh" milestone.

---

## 10. Open question for the user

The single biggest decision: **does the user want to keep the
existing arca's multi-store + capability-token + always-directory
shape (with the user's revamp limited to triad completion + cross-
node mesh)?** Or is the proposal a more aggressive rewrite that
discards those properties?

My read of the verbal proposal: the user was sketching from first
principles without recalling every existing arca property. I think
the recommendation in §1's table (keep multi-store, keep capability
tokens, keep always-directory, fix hash length at 16 hex, add cross-
node mesh, add triad shape) is the cleanest synthesis — most of the
revamp is **additive**, not substitutive.

If that read is wrong (the user genuinely wants single-store,
no-capability-tokens, hybrid file-vs-directory paths), say so and
SYS/20 should be revised.

The second-biggest decision: **hash length in path** (axis B). The
user proposed dynamic short hashes; I'm proposing fixed 16 hex
(64-bit) prefix. The cross-node consistency problem with dynamic
rename is the load-bearing argument. If the user has a counter to
that, I want to hear it before going further.
