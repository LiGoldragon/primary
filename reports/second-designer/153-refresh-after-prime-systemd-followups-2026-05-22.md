*Kind: Refresh · Topic: prime designer + operator follow-ups since /152 meta-report · Date: 2026-05-22*

# 153 — Refresh after prime + operator systemd follow-ups

## Frame

Refresh per psyche prompt 2026-05-22 — captured intent 241
("Refresh reports and intent before selecting next work") and pulled
the deltas since my meta-report at
`reports/second-designer/152-persona-engine-architecture-overview/`
landed. The shape of this report is a small carry-forward update,
not a new meta-report — substance still lives in /152 and the
references below.

## §1 New intent records absorbed

Records captured by other agents between /152 closing and now:

- **220** workspace Principle — Chat normal-response policy (3-7
  big items per response, balanced between new-design explanations
  and questions; visuals stay in reports). *Predates my record 232;
  my record 232 supersedes by adding the "every response paraphrases
  a report" framing + the three-category breakdown.*
- **221** architecture Decision — `/287` substance distributes to
  per-repo `ARCHITECTURE.md` files; contradictory parts get
  rewritten. *Carried by designer/289.*
- **222** workspace Decision — Encode the 3-7 chat-items policy as
  the default for ALL agents in `AGENTS.md`. *Implemented in the
  `AGENTS.md` edit I committed under record 232; the two records
  are aligned.*
- **223-227** persona-pi (multiple) — Persona-Pi becomes the working
  Pi harness + Codex replacement; GPT-5.5 default + GPT-5.4-mini
  available; packaged Pi extensions via Nix; live terminal usability
  + readable themes acceptance.
- **228** persona Constraint — Operator should continue persona
  engine handover work until no clear work remains, ideally reaching
  readiness to deploy persona-daemon for full component no-downtime
  upgrades. *Aligns with operator's continued claim on
  `primary-a5hu`.*
- **236** persona-pi Clarification — `reports/third-designer/20` is
  relevant Pi harness input.
- **238** persona Clarification — Persona is a permissioned system
  daemon.
- **239** persona Constraint — Persona runs as a permissioned system
  daemon (privileged, supervising component daemons).
- **241** workspace Decision — Refresh reports and intent before
  selecting next work. *This refresh is the instance.*

## §2 New reports absorbed

- `reports/designer/288-actionable-beads-2026-05-22.md` — actionable
  bead inventory (not yet absorbed in depth here)
- `reports/designer/289-arch-distribution-from-287-2026-05-22.md` —
  distributes `/287` substance into five per-repo `ARCHITECTURE.md`
  files (`version-projection`, `signal-version-handover`,
  `sema-engine`, `sema-upgrade`, `persona-spirit`). Persona meta repo
  deferred because operator had in-flight changes — that gap was
  later picked up by my sub-agent 1 at commit `248f339f`.
- `reports/designer/290-persona-arch-diff-suggestions-2026-05-22.md`
  — designer's diff suggestions for the persona ARCH.
- `reports/designer/291-persona-systemd-units-for-daemon-management.md`
  — systemd analysis matching intents 238/239. Recommends hybrid:
  `persona.service` NixOS unit + `SystemdTransientUnitLauncher`
  backend for production component daemons + `DirectProcessLauncher`
  for development.
- `reports/operator/162-persona-owner-version-handover-authority.md`
  — operator's report on the owner-signal-version-handover crate
  + Persona consumption (`d89c3ac5`). Closes bead `primary-7kge`.
- `reports/operator/163-persona-systemd-component-management-position.md`
  — operator's position: yes to systemd for production component
  daemons; Persona keeps authority brain, systemd owns lifecycle.
  Names `persona-component@<component>:<version>.service` template
  shape.
- `reports/third-designer/20-pi-as-codex-replacement-design-2026-05-22.md`
  — Pi harness as Codex replacement design (not load-bearing for
  Persona engine architecture; tracked separately).
- `reports/third-designer/21-audit-cluster-operator-6-pi-harness-2026-05-22.md`
  — audit (Pi-track).
- `reports/cluster-operator/6-pi-harness-defaults-and-extension-packaging-2026-05-22.md`
  — Pi defaults + Nix extension packaging.

## §3 What this changes in the /152 picture

### Bead changes

- **`primary-7kge` already closed by operator** (per operator/162
  §"Beads"). My /152 sub-report 7 + sub-report 9 §6 recommended
  closure with a refinement queue — operator beat me to it. The
  refinement queue (Q1-Q6 in sub-report 7) remains valid as
  follow-ups under `primary-wvdl` or `primary-a5hu`.

### Operator commits beyond what /152 §3 status table listed

Two new persona commits referenced in designer/291 §8:

- `persona@f82d180e` — Persona calls `RecoverFromFailure` if
  completion fails after readiness
- `persona@d93c6d54` — `DriveVersionHandover` records
  `UpgradePrepared` before socket I/O
- `persona-spirit@e5dadc24` — `RecoverFromFailure` returns failed
  readiness window to `Active`

The /152 §3 status table mentioned `d89c3ac5` + `22089f47` +
`04ec9302`; these three are additional iterations on the same path.
The status table's "Persona owner-socket binding + HandoverDriver"
rows are still LANDED — just deeper than the snapshot represented.

### Selector-flip physical mechanism — DIRECTION SETTLING

My /152 sub-report 9 §4 carried this as a "no designer lean —
competing" question. Designer/291 + operator/163 now both recommend
the same answer:

- **Persona's active-version snapshot table (manager schema v4)** is
  the authority for which version is active.
- **systemd transient units** (`persona-component@<component>:<version>.service`)
  carry process identity in production; Persona issues
  `start-transient-unit` / `stop-unit` via D-Bus.
- **Public-traffic routing** to the active version is operator's
  pending decision (proxy/router maps public socket → active version,
  OR systemd exposes stable socket and Persona switches which unit
  owns it).

The competing-design pressure narrows to the routing piece. Worth
formal Spirit Decision capture once psyche ratifies.

### `/289` distribution + my sub-agents are complementary, not duplicative

`/289` distributed `/287` substance into five repo ARCH files
2026-05-22 19:32; my sub-agents ran ~20:15 and respected the new
state ("ARCH already current" in sub-agents 3, 4, 5 reports for
sema-engine / version-projection / signal-version-handover /
persona-spirit). Sub-agent 1 + 2 + 5 added what /289 didn't cover
(persona meta repo §1.6.7; signal-persona engine-management rename
notes; sema-upgrade two-submodule pattern naming). No conflicts;
neither report duplicates the other.

## §4 New questions worth surfacing

Beyond the still-open questions catalogued in /152 sub-report 9 §4,
these emerged from the new reports:

**Q-new-1 — Public-traffic routing during version cutover.** With
systemd transient units owning process identity and Persona owning
active-version selection, the missing piece is how PUBLIC clients
reach the right version. Three candidates from operator/163 + /291:

- Persona-owned routing socket (Persona proxies public traffic to
  the active unit's socket)
- Stable systemd socket activation (one socket file, Persona swaps
  which unit it activates)
- Component-CLI version negotiation (each call asks Persona which
  version, then connects directly)

Designer lean: socket activation if it composes with the upgrade
protocol's freeze window; otherwise routing socket.

**Q-new-2 — Quarantine policy gate.** Operator/162 §"Remaining Work"
item 4 flags that `Quarantine` records an event but doesn't gate
future upgrade attempts. Should land before the owner socket exposes
to a real operator-facing client. Designer lean: yes, gate at
`HandleOwnerVersionHandover` before issuing any state-change
operations against a quarantined version.

**Q-new-3 — Spirit v0.1.0 protocol-aware maintenance build OR
intentionally-staged path.** Operator/162 §"Remaining Work" item 3
names this fork: either rebuild + redeploy v0.1.0 with the new
handover protocol code (clean smart cutover path) OR accept a
different first-cutover path (e.g. start v0.1.1 cold + import legacy
file substrate). Designer lean: maintenance build is the clean path;
the staged alternative compromises the no-downtime story.

**Q-new-4 — Operator pivot order: systemd-Slice-A first, OR
Mirror-payload-application first?** Both are pre-cutover work.
Slice A (`persona.service` NixOS module) is a system-specialist
slice; Mirror payload application is operator-on-persona-spirit.
Can run in parallel if second-operator takes one (per intent 230 +
second-operator's pivot to Persona review). Designer lean:
parallelize — Slice A by system-specialist, Mirror by operator,
second-operator audits both.

## §5 Carry-forward questions from /152 §4 — status check

The seven open questions from /152 sub-report 9 §4 are mostly
unchanged. Status delta:

| /152 §4 ID | Question | Status |
|---|---|---|
| A — `AttemptHandover` socket-paths-in-body | Shrink once Persona has catalog | Still open; designer lean: shrink later |
| A — Mirror payload raw bytes vs typed enum | Still open | Still open; designer lean: bytes |
| A — Read semantics during handover | Still open | Still open; designer lean: keep off this contract |
| A — Mirror payload application on persona-spirit-daemon | Still PENDING (sandbox-only) | Now also covered in Q-new-4 |
| B — signal-persona crate-split | Competing, no lean | Still competing |
| B — Selector flip physical mechanism | Competing, no lean | **Now SETTLING (per §3 above) — systemd + Persona-snapshot; public routing is the residual** |
| B — Persona ARCH headline reframing | Pending psyche | Still pending |
| C — Asymmetric Spirit release | Sub-report 6 confirmed deliberate | Designer recommends Spirit Decision capture |
| C — sema-upgrade self-upgrade bootstrap | Designer lean: hand-written | Still pending |
| C — Divergence sink location | Designer lean: in-memory for prototype | Still pending |
| D — `ComponentName` overlap | Designer lean: execute the split | Still pending; not yet on any bead |
| E — `EffectEmitted` generalisation | Designer recommendation (sub-report 7) | **STILL UNANSWERED by psyche; recommendation is to capture as Spirit Decision (Medium)** |
| E — `HandoverSucceeded.commit_sequence` newtype | Cosmetic | Still open |
| E — `UnimplementedReason::IntegrationNotLanded` | Remove after Spirit cutover | Still open |
| F — Auditor authority class | Proposed-not-decided | Still proposed-not-decided |
| F — Auditor lane mechanism | Proposed-not-decided | Still proposed-not-decided |
| F — Audit-output substrate | Proposed-not-decided | Still proposed-not-decided |

## §6 What's actionable next (designer side)

- **Capture Spirit Decisions for the two settled questions** (per
  psyche ratification): asymmetric Spirit release principle (triad-leg
  versions advance independently per leg's schema delta); selector-flip
  physical mechanism (Persona snapshot + systemd unit + routing TBD).
- **Capture EffectEmitted = SemaObservation default** as a Spirit
  Decision (Medium) once psyche ratifies the framing (still waiting
  on that since /152).
- **Absorb `reports/designer/288-actionable-beads-2026-05-22.md`**
  in depth — not done in this refresh.
- **Re-audit persona ARCH coherence** after `/290` + `/291` + my
  sub-agent 1's `248f339f` all touched the same file. Probably
  clean since all three respect the architecture-editor template,
  but worth verifying before the next ARCH edit pass.

## §7 See also

- `reports/second-designer/152-persona-engine-architecture-overview/`
  — the meta-report this refreshes against
- `reports/designer/288` through `/291`
- `reports/operator/162` + `/163`
- `reports/third-designer/20` + `/21`
- `reports/cluster-operator/6`
- Spirit records 220-227, 228, 236, 238, 239, 241 (this refresh's input)
