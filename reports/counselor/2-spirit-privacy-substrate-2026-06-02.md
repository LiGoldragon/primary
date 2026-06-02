# Spirit privacy substrate — options brainstorm — 2026-06-02

## Frame

Per psyche 2026-06-02 (Spirit records 1431-1434, High certainty), assistant
and counselor work moves to private role repositories; intent capture needs a
privacy-aware path. The interim rule (`skills/privacy.md`) keeps private
substance in private reports with `Private intent` notes; ordinary Spirit
gets privacy-safe meta-intent only.

The forward-looking question — what is the durable Spirit-side substrate
for private intent — is the psyche's brainstorm prompt. This report lays
out candidate shapes and recommends a path.

## Workspace state right now

- `private-repos/` exists at the workspace top with `assistant-reports/`
  and `counselor-reports/` subdirectories (operator-created).
- `skills/privacy.md`, `skills/assistant.md`, `skills/counselor.md`, and
  `AGENTS.md` route private substance to private repos.
- Four pre-rule Spirit captures from this counselor session contain
  personal substance and predate the privacy decision being absorbed by
  this lane: records 1429, 1430, 1435, 1436. Per
  `skills/intent-maintenance.md`, over-removal is worse than
  under-removal; they're held pending psyche authorisation rather than
  acted on unilaterally. The substance is local-only (Spirit DB isn't
  git-checked).

## Candidate shapes for the durable substrate

### A. Separate private-Spirit daemon

A second daemon + thin CLI, same `signal-persona-spirit` wire contract as
public Spirit, own socket pair, own redb file, own deployment slot.
Routing is by binary: `spirit "(...)"` for public,
`private-spirit "(...)"` for private. The two daemons never share state.

- Schema change: none (contract reused).
- Pros: clean separation; wire contract unchanged; encryption at rest
  comes naturally (separate DB file on encrypted volume); future
  cross-machine portability matches the workspace's main/next/previous
  deployment-slot pattern; if/when public Spirit becomes git-checked,
  private stays out.
- Cons: cross-query is impossible (a "show all counselor-scope intent"
  query hits both DBs and the agent merges); deployment surface doubles;
  routing discipline is the substrate's correctness guarantee, not a
  type-level wall.

### B. Private-prefixed Kinds in the current daemon

Extend the `Kind` enum: `Decision | Principle | Correction | Clarification
| Constraint` becomes 10 variants with `Private`-prefixed twins. Same DB,
same daemon, wire-shape adds 5 enum variants. Queries filter by Kind.

- Schema change: `Kind` enum doubles.
- Pros: single DB; type-level discrimination at the Kind axis.
- Cons: the privacy axis is **orthogonal to Kind** — a private Decision
  is distinct from a public Decision in privacy, not in decision-ness;
  doubling the enum conflates two axes that should be separate; private
  substance still in the same DB file as public, so a DB-leak vector
  leaks everything; this is a convention, not a security boundary.

### C. Privacy axis on Entry (orthogonal field)

Add a `Privacy` field to Entry: `Public | Private` (or finer:
`Public | RoleOnly | OwnerOnly`). Same DB, same daemon, wire-shape adds
one field. Queries filter on the new axis.

- Schema change: +1 field on `Entry`.
- Pros: keeps Kind enum at 5; explicitly orthogonal axis; cleaner than B
  on the type system.
- Cons: same DB-leak issue as B; wire-shape change touches the contract
  crate and migrations; still not a security boundary, just a typed
  convention.

### D. Topic-vocabulary-only convention

Reserve a topic (e.g., `private`) and treat any record tagged with it as
private. Filter from default queries. No schema change.

- Schema change: none.
- Pros: zero infrastructure cost; maximum flexibility.
- Cons: easy to forget the tag; not enforceable; public DB still
  contains private substance.

### E. Encryption at rest (orthogonal to A-D)

Encrypt the `Description` field of private records with the psyche's key
(age, gpg, hardware-key). Stored encrypted; decrypted on read with key
access. Combinable with any of A-D.

- Schema change: `Description` becomes ciphertext for private records.
- Pros: strongest privacy guarantee — DB leak yields ciphertext only;
  maps cleanly onto the workspace's `secrets.md` discipline (encryption
  as the substrate for "agent never sees the value"); future-extensible
  to hardware-key signing.
- Cons: key management is operational overhead; encrypted strings cannot
  be queried by content; agents that need to reason about content need
  the decryption key in scope.

### F. Combo — A (separate daemon) + E (encryption at rest)

Separate `private-spirit` daemon whose redb file lives on encrypted
storage (LUKS volume, ZFS native encryption, age-wrapped backups). Wire
contract unchanged. Encryption is at the storage layer, transparent to
the daemon.

- Schema change: none (encryption is below the daemon).
- Pros: defense in depth — daemon separation **and** ciphertext-at-rest;
  daemon code identical to public Spirit; encryption substrate handled
  at the OS layer where this kind of work belongs.
- Cons: highest setup complexity; ops surface compounds (daemon + key
  custody + encrypted storage).

### G. No Spirit-side substrate — use private-report `Private intent` notes (current interim)

Private intent lives as a `## Private intent` section inside the
relevant private report under `private-repos/<role>-reports/`. Queries
are repo-grep across those reports.

- Schema change: none.
- Pros: zero infrastructure cost; works today; aligns with
  `skills/privacy.md`'s current text.
- Cons: no NOTA-typed structure; no Kind/Magnitude discrimination; no
  daemon-stamped provenance; querying is text-search, not typed-query;
  encryption comes from the filesystem only.

## Comparison

| Option | Schema change | Deploy delta | Cross-query | DB-leak resilient | Setup cost | When |
|---|---|---|---|---|---|---|
| A. Private daemon | none | +1 daemon | merge-at-client | filesystem-layer | medium | next milestone |
| B. Private Kinds | Kind doubles | none | yes | no | low | discouraged |
| C. Privacy axis | +1 field | none | yes | no | low | discouraged |
| D. Topic convention | none | none | yes | no | very low | bridge only |
| E. Encryption | Description ciphertext | +key mgmt | content-queries blocked | yes | medium | wave 2 |
| F. A + E combo | none | +1 daemon + keys | merge-at-client | yes | high | end-state |
| G. Private reports | none | none | grep-only | filesystem-layer | zero | today |

## Convergence with assistant's parallel analysis

`reports/assistant/2-private-repositories-and-intent-privacy-2026-06-02.md`
covers the same brainstorm in close alignment. Direct correspondences:

| Assistant report | This report |
|---|---|
| A. Separate private Spirit database | A. Separate private-Spirit daemon |
| B. Privacy-marked variants of every Kind | B. Private-prefixed Kinds |
| C. Privacy field on intent entries | C. Privacy axis on Entry |
| D. Private intent as private reports (interim) | G. Private reports (interim) |

This report adds three branches the assistant report doesn't address:
**D. Topic-vocabulary convention** (least-effort baseline; named for
completeness), **E. Encryption at rest** (orthogonal storage-layer
mechanism), and **F. Combo A+E** (end-state pairing). Of those, only F
changes the joint endgame in a load-bearing way — D and E are minor
branches to be aware of, not chosen.

The assistant report makes one nuance worth absorbing: **B-style typed
Kinds or C-style typed fields can be used *inside* a separate private DB
(A or F) as type-level privacy markers**, even when they're insufficient
as the substrate themselves. In that read, the privacy boundary is the
daemon/storage layer (A or F); B/C are local discrimination conveniences
within it. This report's "avoid B/C/D as endgame" judgment stands only
when they are the **only** mechanism.

Joint direction: private reports today → separate daemon next →
encryption-at-rest after that. The two reports agree on the spine; this
one extends by one step (encryption end-state) and names two minor
branches.

## Recommendation

**Run G today, plan toward F as end-state, take A as the mid-step.**

- **G today.** `skills/privacy.md`'s current text already mandates this.
  Private substance lives in private reports; ordinary Spirit gets only
  privacy-safe meta-intent. Everything works without new infrastructure;
  the discipline is the substrate.
- **A next.** When private-intent volume grows enough that text-grep
  becomes the bottleneck, stand up a `private-spirit` daemon. Same wire
  contract, separate DB, separate socket — extends the workspace's
  spirit-next/main/previous slot pattern naturally. The cutover is a
  thin-client routing change; the typed surface is unchanged.
- **F end-state.** When private substance warrants ciphertext-at-rest
  (e.g., the substrate gets backed up to cloud storage or replicated
  across machines), layer storage-layer encryption under the private
  daemon. Daemon code untouched; encryption is OS-layer.

Avoid B, C, D as **end-state** choices: each leaves private substance in
the same DB file as public, which is exactly the leak vector the privacy
discipline is trying to prevent. They are conventions, not boundaries.
**However** — B-style typed Kinds or C-style typed fields can be used
*inside* a separate private DB (A or F) as local type-level
discrimination conveniences (per assistant's report nuance); they're
useful within a boundary, just not sufficient as the boundary. Likewise
topic-vocabulary discipline (D-style tagging) inside the private
substrate is fine; D as the **only** mechanism is not.

The progression G → A → F has a property worth naming: at each step,
no prior work has to migrate destructively. Private reports stay in
their repo when A lands (A complements them; doesn't replace). When F
lands, A's storage layer is replaced by encrypted storage, with the
daemon untouched.

## Open questions for the psyche

1. **Direction**: does the G → A → F path match your read, or reroute?
2. **Pre-rule captures**: records 1429, 1430, 1435, 1436 contain
   personal substance from this session that predates the rule landing
   in this lane. Authorise removal via `spirit "(Remove N)"`? Hold
   pending the substrate so they can migrate later? Leave indefinitely?
3. **Naming**: when A lands, binary name? `private-spirit`,
   `personal-spirit`, `pspirit`, something else?
4. **Encryption layer**: when F lands, filesystem-layer (encrypted
   home / LUKS / ZFS native) or application-layer (age envelope per
   `Description`)? Filesystem-layer is simpler and reuses existing
   discipline (gopass / sops-nix); application-layer gives finer
   record-level control.
5. **Deploy slot**: parallel to current Spirit slots
   (`private-spirit-next`, `private-spirit-vX.Y.Z`) or a single slot
   that the private substrate lives in for now? Side-by-side slots are
   the workspace pattern but add ceremony if the private substrate
   evolves slowly.

## Adjacent — pending counselor work

The deep-research dispatch on EU financial presence (Canadian citizen +
sub-€30k consulting + Spain bias) was prepped one turn ago but not
fired. Holding until you direct: the report's destination is
`private-repos/counselor-reports/` (per the new discipline), but I'd
rather take your read on the substrate brainstorm before launching
research that will accrete more personal-affairs Spirit traffic. Say the
word and it goes.
