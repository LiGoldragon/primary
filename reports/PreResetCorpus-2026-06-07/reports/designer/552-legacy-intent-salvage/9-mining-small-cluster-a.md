# 552 — Legacy intent salvage — mining: small-cluster-A (arca, signal, spirit)

Scope: scanned 19 legacy records across `/tmp/intent-text/arca.txt` (6),
`/tmp/intent-text/signal.txt` (6), `/tmp/intent-text/spirit.txt` (7). Three
genuine salvage candidates survive dedup; the remaining 16 are already
preserved (Spirit, arca `ARCHITECTURE.md`, report 139, or guidance layer) or
are too-specific transient task orders. Propose-only.

## Salvage candidates

### Candidate 1 — Daemon privilege envelope: privileged but not absolute; no ambient access to system private keys

- **Kind:** Principle
- **Proposed topics:** `[daemon privilege access security private-key boundary component-shape]`
- **Proposed description:** A content/data daemon (the arca archive daemon is
  the motivating case) should be fairly privileged — there is nothing
  especially dangerous about ingesting and serving content — but NOT absolutely
  privileged. Its privilege boundary is *"can ingest and serve content"*, not
  *"can read anything on the system"*. It must NOT have ambient access to system
  private-key material (e.g. the system SSH key); if handed a path to a private
  key it should be unable to actually read it. The store directory itself must
  remain unwritable by anything except the daemon (and root, whose writing would
  itself be system misbehavior).
- **Proposed certainty:** High (legacy Maximum, but the psyche audibly worked it
  out mid-statement — "actually that's not true… it shouldn't be able to read
  private keys" — so the *boundary* is firm while the exact carve-out list is
  illustrative; High is the honest read).
- **Supporting verbatim:** "Arca should basically be a pretty privileged daemon
  because there's nothing really dangerous about it. And, well, actually that's
  not true. It shouldn't be able to read private keys… not like system private
  keys, like the system SSH key… So it should not be an absolute privileged
  daemon, but it should absolutely not be writable by pretty much anything
  except root, which actually would be misbehavior by the system."
- **Preservation evidence:** `spirit (Observe …[arca])` → empty; `…[access
  privilege secrets]` returns only Spirit-privacy-tier records, cluster-secret
  records (gopass/sops), and router-access records — nothing about a content
  daemon's privilege boundary or private-key carve-out. `rg -i 'privileg|private
  key|ambient'` across `arca/ARCHITECTURE.md` finds the store-write-authority
  and capability-token model but NOT the privilege-envelope / no-ambient-keys
  principle. Not in `ESSENCE.md` / `AGENTS.md` / `skills/`.
- **At-risk rationale:** The write-authority half (only the daemon writes the
  store) is preserved in `arca/ARCHITECTURE.md` §Invariants. The *read*-side
  privilege boundary — privileged but not absolute, no ambient access to system
  private keys — lives ONLY in this legacy record. On deletion the general
  daemon-privilege principle (reusable for every privileged component) is lost.

### Candidate 2 — Content-addressed / hash identifiers are LLM-token-expensive; the shortest reliable identifier is the design target

- **Kind:** Principle
- **Proposed topics:** `[identifier hash token-cost llm readability content-address naming]`
- **Proposed description:** Opaque content-addressed identifiers (blake3/sha
  hashes and similar) tokenize at roughly one token per character in LLM
  context because they are not natural-language words. When such identifiers land
  in agent context, logs, references, and reports they become a significant and
  recurring cost. Identifier design must therefore treat *the shortest reliable
  identifier* as a first-class target — short readable locators over full long
  hashes — balanced against collision risk (full digest stays the canonical
  identity; the exposed path is a stable shortened locator that is never
  renamed once exposed).
- **Proposed certainty:** Medium (legacy was Medium; the general principle is
  durable but the exact prefix-length policy is correctly excluded as
  too-specific and already lives in report 139).
- **Supporting verbatim:** "these file paths, when they end up in… LLM context,
  they become extremely costly because hashes are not recognizable tokens.
  They're not words or anything in natural language, so they end up costing,
  like, a full byte per character, which is very inefficient."
- **Preservation evidence:** `spirit (Observe …[content-address])` → empty;
  `…[arca])` → empty. `rg` across `ESSENCE.md`/`AGENTS.md`/`skills/`: the only
  hits are `skills/reporting.md` and `skills/spirit-cli.md` on *human-facing*
  self-contained references / long→short sidecar mapping — the human-readability
  angle, NOT the LLM-token-cost-as-design-driver angle. `AGENTS.md` §"Opaque
  identifiers in chat carry an inline description" covers human decodability,
  not token cost. The token-cost reasoning is captured in
  `reports/system-operator/139` only, which is GC-able.
- **At-risk rationale:** The token-cost driver is the *general* rationale behind
  every short-identifier choice in the stack (arca prefixes, bead UIDs, jj
  change-ids, Spirit base36 ids). It currently survives only in a deletable
  report and this legacy file; the durable guidance layer states the human
  angle but not the LLM-cost angle. On deletion the general principle is lost.

### Candidate 3 — Anything that can be done mechanically is not done by agents

- **Kind:** Principle
- **Proposed topics:** `[agent-discipline mechanical automation layering separation routing]`
- **Proposed description:** Any decision or step that can be made mechanically
  must NOT be pushed onto the agent layer — the agent layer is the wrong layer
  for any mechanical decision. The motivating case rejected two CLI
  socket-dispatch designs (a NOTA wrapper that makes the agent name which socket;
  a try-working-then-fall-back-to-policy probe) precisely because both push
  mechanical routing into the agent; the surviving direction was a static,
  contract-derived dispatch macro. Generalized: mechanical routing,
  classification, and projection belong in code / schema-derived machinery, not
  in agent judgment.
- **Proposed certainty:** High (legacy Maximum on the specific dispatch
  rejection; the general principle is stated categorically — "Anything that can
  be done mechanically will not be done by agents" — High is the honest read for
  the generalized form).
- **Supporting verbatim:** "There's no way we're going to make the agents
  responsible for figuring out which socket goes where. That's a mechanical
  thing. Anything that can be done mechanically will not be done by agents… And
  option C, try parse as working and policy. No, that's bad."
- **Preservation evidence:** `spirit (Observe …)` across `[automation]`,
  `[agent-discipline]`, `[routing]`, and the saved `[signal sema executor]` deep
  dump — none contain the mechanical-not-by-agents principle (routing records
  found are about e2e harness witnesses and origin-route metadata, not the
  agent-layer boundary). `rg -i 'mechanical'` across `ESSENCE.md`/`AGENTS.md`/
  `skills/` finds only descriptive uses (auditor work "is mostly mechanical",
  "mechanical translation", "mechanical renames") — never the categorical
  principle that mechanical work is kept off the agent layer by design.
- **At-risk rationale:** This is one of the load-bearing rationales for the
  entire schema-derivation / macro-emission thrust (let the machine derive what
  is derivable; reserve agents for judgment) and for the small-model auditor.
  It is stated nowhere durably as a principle. On deletion it is lost.

## Already preserved / dropped — safe to delete

### arca.txt (6 records)

- **Rec 1 (content-addressed-vs-nix-store distinction; triad-shaped):**
  preserved — `arca/ARCHITECTURE.md` opens with exactly this (content-addressed,
  nix-store analogue addressed by content not derivation recipe, holds
  blob-shaped data). Triad-shape is in `AGENTS.md` §Component triad + `skills/`.
- **Rec 2 (only the daemon writes the store; TOCTOU invariant):** preserved —
  `arca/ARCHITECTURE.md` §"Write-only staging" + §Invariants ("the hash arca
  computes is the hash of exactly what arca moved into the store. No TOCTOU
  race"). The general privilege *read*-boundary half was split out as Candidate 1.
- **Rec 3 (`/arca` root, flat layout):** too-specific (exact on-disk path); the
  canonical decision lives in `reports/system-operator/139` (short-prefix policy,
  base32 floor). Note: `arca/ARCHITECTURE.md` still shows the *older*
  `~/.arca/<store>/<hash>` framing that this record corrects — a repo-INTENT
  drift, but a path-specific one, not durable design intent to salvage.
- **Rec 4 (sema is source of truth for file meaning; bytes in arca):**
  preserved — `arca/ARCHITECTURE.md` §"Role in the sema-ecosystem" + §Invariants
  ("No typing. arca does not know what a hash points at; sema records own that").
- **Rec 5 (privilege envelope):** SALVAGED as Candidate 1.
- **Rec 6 (hashes are LLM-token-expensive):** general principle SALVAGED as
  Candidate 2; the specific prefix-length policy is dropped (in report 139).

### signal.txt (6 records)

- **Rec 1 (ToSemaOperation/ToSemaOutcome two-trait projection shape):**
  too-specific to a since-superseded trait layout; the live signal/sema/Nexus
  design is deep in Spirit `[signal sema executor]` (40KB of records). Drop.
- **Rec 2 (move all signal-executor code to three-layer design; update arch):**
  transient task order ("all the code must move"), not durable intent. Drop.
- **Rec 3 (rename SemaEffectEmitted away after SemaEffect removed):** one-off
  rename order ("obviously"); the general naming discipline is in `skills/naming.md`.
  Drop.
- **Rec 4 (consider report 144 in convergence work):** transient pointer to a
  report; not intent. Drop.
- **Rec 5 (persona-spirit pilot done; pilot-first gate lifted):** transient state
  reaction (a gate that has since fully resolved). Drop.
- **Rec 6 (reject NOTA-socket-wrapper / try-parse dispatch options):** the
  *specific* option rejection is transient; the GENERAL principle behind it
  (mechanical → not agents) is SALVAGED as Candidate 3.

### spirit.txt (7 records)

All 7 are about the Spirit query/proving/deployment design and are deeply
preserved in the live Spirit store and the deployed daemon itself:

- **Rec 1 (prove readiness via live daemon + thin CLI, not only unit tests):**
  preserved in spirit `[spirit]` records on live-use / proving-not-pretending,
  and realized — Spirit is deployed and this audit is querying it live.
- **Rec 2 (query surface: summaries-only / with verbatim+context / topic+kind
  filters)** and **Rec 7 (topic catalog with per-topic counts):** preserved —
  Spirit record `0huc` ("full Observe/Topics vocabulary with certainty and
  recency selection") and `xbb5` (search-style summary shorthand); both are
  shipped (`SummaryOnly`, `Partial`, and `TopicsObserved` are exactly what this
  audit used).
- **Recs 3, 4, 5, 6 (package persona-spirit on CriomOS as user/system service;
  socket discovery; follow component design; write a report on design flaw):**
  deployment task orders for a since-completed packaging task; the general
  daemon-deploy discipline is in `skills/` and Spirit `[deployment]`. Drop.
