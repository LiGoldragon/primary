# 217 — Component triad + Mutate authority state (2026-05-18)

*Topic compendium for the universal component triad pattern and Mutate
authority direction. Part of the 2026-05-18 workspace state-of-art
series. Master index lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

The component triad pattern and Mutate-as-authority direction are now
permanent workspace doctrine. Canonical home:
`/home/li/primary/skills/component-triad.md` (tier-1 in
`AGENTS.md`'s skill-importance table). Five load-bearing invariants:

1. **CLI has one Signal peer** — its own daemon, no shortcuts.
2. **Daemon speaks `signal-core` only** at the external boundary.
3. **Verb declared per variant** in `signal_channel!`.
4. **Daemon state through `sema-engine`** — durable state lives in a
   typed record store, not bespoke files.
5. **Privileged authority uses a separate `owner-signal-<component>`
   surface** when present.

Mutate is the **authority verb**: top-down order ("change this, I do
not care what you think"); issuer holds *possibly-mutated* state until
subordinate confirms; on confirmation, *now-mutated*. Authority chain:
`mind → orchestrate → router/harness`. The Mutate semantics also live
in:

- `signal-core/ARCHITECTURE.md` §1 (paragraph about authority direction)
- `persona-mind/ARCHITECTURE.md` §6.6
- `persona-router/ARCHITECTURE.md` §2.5
- `skills/contract-repo.md` (verb table extended with authority-direction column)
- `skills/micro-components.md` (cross-ref in triad-shape sequence step 4)

Remaining design substance in reports is mostly the *audit that
motivated the skill* (designer/209) and *applications to specific
components* (terminal /211; orchestrate DA/115; permission DA/116;
executor DA/119). The triad itself is no longer the open question — its
application to each component is.

---

## 2 · Load-bearing reports

| Path | Carries |
|---|---|
| `reports/designer/210-component-triad-decisions-and-mutate-authority-2026-05-17.md` | User-decision record (Q1 skill location → workspace skill; Q3 Mutate → authority verb). §4 persona-terminal 10-binary correction. §6 follow-up table. Decision-record substance is unique here. |
| `reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md` | Applies the triad to persona-terminal. Actor topology, sema-engine registry, contract changes, migration sequence. Not yet in `persona-terminal/ARCHITECTURE.md`. |
| `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md` | OwnerSignal discipline rationale + per-component Unix-user/group decision. Triad skill names `owner-signal-<component>` as the pattern but doesn't carry the OS-security-boundary argument or candidate owner-graph. |
| `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md` | Records-vs-machinery split; full-triad decision for `persona-orchestrate`; user-approved authority-chain diagram. Bead `primary-699g` consumes this. |
| `reports/designer-assistant/118-signal-core-sema-engine-fit-investigation-brief-2026-05-17.md` | The brief that asked whether signal-core + sema-engine compose at the seam. |
| `reports/designer-assistant/119-full-signal-executor-architecture-concept-2026-05-18.md` | Names the component-local execution plane that every triad daemon takes. |
| `reports/second-operator-assistant/2-signal-core-sema-engine-fit-audit-2026-05-17.md` | Code-grounded answer to /118; twelve in-code witnesses. |
| `reports/second-operator-assistant/3-full-signal-executor-architecture-consideration-2026-05-18.md` | Operator endorsement of DA/119 with implementation-order specifics. |
| `reports/second-designer-assistant/6-roles-as-config-owner-socket-mutable-2026-05-17.md` | User direction: lane/role registry as config loaded at startup, mutable via OwnerSignal. Adds `LaneRegistry*` family to orchestrate owner contract. |
| `reports/operator/134-terminal-orchestrate-porting-decisions-2026-05-17.md` | User-approved decisions: communication/supervision socket naming; CreateSession = Mutate; terminal session authority. The "communication vs supervision socket" naming decision is not yet in the triad skill. |
| `reports/designer/214-criome-architecture-record-2026-05-17.md` | Carries the criome triad's authority-direction specifics (single-owner-as-Unix-user; owner-socket discipline; master-keypair-as-identity). Cross-topic; covered in detail in /216. |

---

## 3 · Migration-complete reports (retire candidates)

Per `skills/reporting.md` §"What gets absorbed, not kept", these
report's substance has fully migrated to skills/ARCH and they should
retire.

| Path | Substance migrated to |
|---|---|
| `reports/designer/209-component-triad-daemon-cli-contract-2026-05-17.md` | Three-invariant framing (now five) → `skills/component-triad.md`; verb-question answer → triad skill + `signal-core/ARCHITECTURE.md` + `skills/contract-repo.md`; per-component fit table → each component's ARCH. |
| `reports/designer-assistant/50-signal-core-base-verb-shape.md` | Six-root closure with structural atomicity is permanent in `signal-core/ARCHITECTURE.md` + `skills/contract-repo.md`. |
| `reports/designer-assistant/53-signal-core-cli-verb-implementation-audit.md` | CLI-as-thin-Signal-client + per-variant verb mapping in `skills/component-triad.md` + `skills/contract-repo.md`. |
| `reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md` | Substance in `signal-core/ARCHITECTURE.md` (six verbs + read-plan operators) + sema-engine ARCH. |
| `reports/designer-assistant/94-lojix-daemon-design-on-persona-engine-pattern.md` | Substance landed in `lojix/ARCHITECTURE.md` (the cleanest triad exemplar today). Skill names the pattern universally. |
| `reports/designer-assistant/117-review-operator-134-terminal-orchestrate-porting-decisions-2026-05-17.md` | Self-marks "Superseded in part by operator/135". Residual correction (ordinary surfaces may carry ordinary Mutate variants) now in triad skill invariant 5. |

---

## 4 · Contradictions resolved

| Topic | Loser → Winner |
|---|---|
| Invariant count | /209 said "three invariants" → **skill now states five** (added: sema-engine state; OwnerSignal as separate surface) |
| persona-terminal CLI count | /209 said "five CLIs" → **/210 §4** corrected to 10 binaries (two daemons + six control-plane CLIs + two data-plane attachers) |
| op/134 row "non-owner socket does not know Mutate" | Wrong as written → **triad skill invariant 5**: boundary is request vocabulary + socket, not the verb. Ordinary surfaces may carry ordinary Mutate variants. |
| orchestrate placement | DA/115 first-draft "co-resident actor inside mind" → **DA/115 final**: full triad daemon |

---

## 5 · Open questions

- **/210 §6 follow-ups** — none individually decided:
  - (a) update `signal-core/src/verb.rs` doc comments to reflect authority direction
  - (b) `signal-criome` per-variant verb-mapping audit (gap from /209 §6)
  - (c) `persona-terminal` CLI consolidation (per /211; in flight per operator/135)
  - (d) re-audit each existing contract crate's `signal_channel!` for verb correctness under Mutate-as-authority — anything currently `Assert` whose semantics are "order the receiver to change something" should be `Mutate`
  - (e) `persona-orchestrate` contract design (bead `primary-699g`)
- **/209 Q4** — does `persona-harness` get a debugging CLI? Designer-side read was "yes, useful, not urgent"; no user decision.
- **op/134 — "communication" / "supervision" socket naming** not yet in the triad skill or in `skills/component-triad.md` §"Witness tests".
- **signal-core ↔ sema-engine fit (DA/118 → s-OA/2 → DA/119 → s-OA/3)** — recommendation set ready; skill/ARCH unchanged. See `reports/designer/220-full-signal-executor-state-2026-05-18.md`.
- **sec-DA/6 — `LaneRegistry*` family** on orchestrate owner contract; supersedes sec-OA/1's RoleName-gap paths. No designer-side acknowledgement landed yet.

---

## 6 · Implementation state across components

| Component | Daemon | CLI | Contract | Notes |
|---|---|---|---|---|
| `persona-mind` | live (`mind --daemon`) | live (`mind`) | `signal-persona-mind` | ARCH §6.6 carries authority direction |
| `persona-router` | live | live | `signal-persona-router` | ARCH §2.5 carries authority direction |
| `persona-message` | live | live | `signal-persona-message` | Triad-clean |
| `persona-introspect` | live | live | `signal-persona-introspect` | Daemon is multi-peer Signal client (legitimate carve-out 3) |
| `persona-harness` | live | **absent** (intentional; AI harness is input surface) | `signal-persona-harness` | Possible debug-CLI = /209 Q4 open |
| `persona-terminal` | **10 binaries** (consolidation pending per /211) | violates one-CLI-per-daemon rule | `signal-persona-terminal` + `owner-signal-persona-terminal` | Both contracts shipping; runtime consolidation in flight |
| `persona-orchestrate` | **does not exist yet** | not yet | design pending (bead `primary-699g`) | Authority-chain target per DA/115 + /210 |
| `lojix` | live on horizon-leaner-shape worktree | live | `signal-lojix` (impl on horizon-leaner-shape) | Cleanest triad exemplar |
| `criome` | live | live | `signal-criome` shipping; `owner-signal-criome` future | Per-variant verb-mapping audit pending |
| `arca` | skeleton | skeleton | `signal-arca` does not exist yet | Triad in progress |

---

## 7 · Recommendations for context maintenance

### Retire now

Six reports per §3 — substance fully migrated.

### Keep until the next sweep

- `/210` until terminal consolidation lands and follow-ups close
- `/211` until consolidation lands in `persona-terminal/ARCHITECTURE.md`
- `/214` while owner-signal-criome design is open
- DA/115, DA/116, DA/118, DA/119, s-OA/2, s-OA/3, sec-DA/6 — inform `persona-orchestrate` and signal-core/sema-engine fit; both open
- op/134 until "communication" / "supervision" socket naming reaches the triad skill
- SYS/22, SYS/141 stay while the criome-routed-authorization arc is implementing

### Promote to skill (consider)

The OwnerSignal discipline (DA/116 §1-§9 + the five A1-A5 settlements at §13) recurs across orchestrate, terminal, criome. Candidate: extend `skills/contract-repo.md` with an OwnerSignal section, or create `skills/owner-signal.md`. Either retires DA/116 cleanly.

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master.
- `skills/component-triad.md` — canonical.
- `reports/designer/218-persona-terminal-consolidation-state-2026-05-18.md`, `/219`, `/220` — adjacent topics applying the triad.
