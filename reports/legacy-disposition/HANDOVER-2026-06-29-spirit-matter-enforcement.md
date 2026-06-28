# Handover — Spirit/Matter Boundary and Enforcement (2026-06-29)

Supersedes `reports/legacy-disposition/HANDOVER-2026-06-28-spirit-matter-boundary.md`.

Fresh-context pickup for the spirit/matter effort. Section 1 is the psyche's durable intent (the load-bearing part). Section 2 is current state. Section 3 is open items. Section 4 is matter-context locators. No transcript or correction history is included by design.

## 1. Psyche intent (durable)

### The boundary
Spirit holds only the psyche's durable intent and stays slim — intent is rare and highly valuable. Concrete *matter* (code, specs, architecture, mechanism descriptions, tracked work/beads, and descriptions of how Spirit itself works) does not belong in Spirit; it lives in code, ARCHITECTURE docs, skills, or beads.

### The keep/remove test
A record stays (is intent) only if it states a **universal rule** — applicable across almost any scenario, optionally carrying color about how it applies in specific areas — expressing the psyche's own direction about the work or the world. It is **matter** if (a) scoped to a single mechanism, component, or one-off architectural decision, or (b) Spirit-usage / agent-training material (any rule about how to use or operate Spirit itself). **Strip test:** judge by the load-bearing directive stripped of framing — an action performed on or with Spirit is matter; a general work-or-world behavior that Spirit merely records is intent, even when a narrower version also appears in a doc.

### Intent is rare
The default response to any psyche utterance is *not* to capture; capture is the exception. Over-capture — logging nearly everything the psyche says, including non-directive remarks and private content — is the failure being corrected. A statement is intent only if directive AND durable AND universal. Not intent: no-directive (information), private/personal, matter, ephemeral. When unsure, do not capture.

### Bundled records to split
When a record welds a thin directive to matter, remove it and reintroduce a clean record holding only the directive. At the guardian gate, reject the whole mixed submission and re-capture the clean directive later.

### Removal model
Hard removal with archive-first. Remove-then-rehome (the archive bridges; rehoming is a follow-on pass). A conflict at a matter's natural home signals *stale matter* — the home wins. Soft removal = Zero-certainty (reversible, excluded from default Observe). Physical archive-and-delete via the guardian-free meta-socket CollectRemovalCandidates (available in 0.18.1).

### Calibration loop (how the removal wording is tuned)
A fresh agent each round works only from the current wording (not accumulated dialogue), surfaces the single hardest edge record; the psyche rules; on disagreement the wording is refined and a new edge brought; convergence = the psyche agrees on the hardest edge (adversarial agreement). Rulings so far: `0xqp` ("always Observe"), `5tar` ("educate before submitting"), `otel` ("capture densely"), `g78b` ("refresh intent before work") = matter/remove (Spirit-usage training). `qjrf` = split: shed the Spirit-mechanics clause, keep a clean "ask the psyche when a design surface is incomplete; don't fabricate" maxim.

### The guardian
Must disallow matter at admission. Its criteria are compiled-in code (prompt markdown + the `GuardianRejectionReason` enum in signal-spirit) — not retrainable on a live daemon; changing it is a code change plus redeploy. The guardian is day-to-day defense to keep matter out. Deliberate curation by the psyche plus agents who have done the thinking bypasses the guardian (owner-only meta socket).

### Privacy is nominal
Privacy is a level (Zero = public, any nonzero = private), all in one database, with no real security fail-safe — name-only. Treat all Spirit data as potentially exposed. Genuinely sensitive content goes to actually-private storage (private repos), not Spirit. Privacy is orthogonal to the Matter test; a genuine private-affairs *want* is admissible intent carrying a privacy level, a private non-directive *remark* is not (no directive). May become secure-private later. Documented in spirit ARCHITECTURE.md and INTENT.md.

### Version-control discipline
All work is based off main; no divergent branches; consolidate. Reconcile against the existing main-next skill (which legitimizes a long-lived `next`) — a possible tension to settle.

### Misc
- Spirit does not depend on mentci (dev-dep plus its e2e test removed).
- Communication: no emotional framing; state things plainly; do not project states onto the psyche or the agent.

## 2. Current state (done this session)

- **Lever 1 — agent-training docs: landed.** The doctrine is threaded into the capture skills (intent-log, spirit-cli, human-interaction, intent-manifestation, intent-maintenance) and AGENTS.md plus ESSENCE.md; matter-as-intent examples replaced; regenerated and pushed (skills repo `009164c`, primary `55ef70f`). Source of truth = skills repo `/git/github.com/LiGoldragon/skills/modules/<name>/full.md`; the in-tree `.claude/skills/.../SKILL.md` are generated via `nix run .#generate-skills` — never hand-edit them.
- **Lever 2 — guardian enforcement: deployed.** spirit `main` = 0.18.1 (`f64bc8ad`): Matter boundary reconciled to the doctrine, mentci removed, plus a store-migration step for the live 0.16.0 records family (`dbe53794`) proven against a backup copy. Deployed to production via lojix; **0.18.1 live, 1389 records (650 non-Zero) intact, zero data loss, guardian enforcing.** CriomOS-home main = `059afda` (spirit re-pin plus the 7-field config with AuthorizationMode=Gating).
- **Branch cleanup:** 7 stray spirit branches deleted (4 merged plus 3 confirmed-redundant; all SHAs recoverable). Production pin (`operator/guardian-alignment-production`) and `spirit-removal-rework` preserved (the latter's content is now on main).

## 3. Open items

1. **Confirm the `Matter` gate fires.** The two deploy-time matter probes were rejected but tripped *earlier* gates (Duplicate-referent collision; referent-gate NonReferent) — enforcement is proven, but the `Matter` reason itself is not yet witnessed. Run one clean probe (valid-referent, non-duplicate, genuine matter) that only the Matter gate catches.
2. **Held branches — land/abandon call:** `mirror-shipper` (stale experimental engine-pin; recommend abandon), `schema-help` (genuine unlanded local `(Help)` reflection feature — needs rebase if wanted), `structural-forms-integration` (positional-grammar migration; behind main, so landing = re-migrate). SHAs recorded; recoverable.
3. **Resume the legacy cull.** The original work — curating the *existing* ~650 non-Zero corpus down to real intent — paused for the emergency. With the bleed stopped, resume. `qjrf` disposition is decided and pending execution: Zero-mark the bundled record plus meta-`Import` a clean "ask-don't-fabricate" maxim (guardian-free remove-and-reintroduce now works on 0.18.1).
4. **Capture this session's durable intent to Spirit** (the genuine universal-rule items in section 1) via an intent-maintainer; the matter/Spirit-usage doctrine is already in docs. By the doctrine, the mechanical criterion is itself matter and belongs in docs, not Spirit — capture only genuine universal direction.
5. **Minor:** CriomOS system-repo `criomos-home` input re-pin for lock consistency; delete the stale systemd drop-in `~/.config/systemd/user/spirit-daemon.service.d/guardian-alignment.conf.disabled-20260628T221924`; fix `AGENTS.md` boot pointer (still names retired `skills/skills.nota`; discovery moved to generated role packets — `skills/generated-role-outputs.nota`).

## 4. Matter-context (locators)

- spirit `/git/github.com/LiGoldragon/spirit`, main 0.18.1 `f64bc8ad`. Guardian prompts `src/guardian-prompts/{checklist,few-shot,record-shape}.md`; `GuardianRejectionReason` (incl. `Matter`) in signal-spirit `src/schema/signal.rs`; migration `src/production_migration.rs` (the `dbe53794` to `eb29cb6c` relabel step plus its test).
- Deploy: lojix, direct `meta-lojix '(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=<REV> Activate None [])))'`. Push-first (daemon fetches the github rev). `Build` HomeMode validates non-activating; `Activate` switches. Authoritative outcome in `journalctl -u lojix-daemon.service`. NOT the `n` wrapper.
- Store: `~/.local/state/spirit/spirit.sema` plus `spirit.archive.sema`; predeploy backups `.predeploy-20260628T183555` and `.predeploy-20260628T221924`. Guardian-free ops: meta socket `meta-spirit.sock` — `Import` (reintroduce/upsert, bypasses guardian) and `CollectRemovalCandidates` (archive-first delete); soft-remove = `ChangeCertainty <id> Zero`.
- Deploy/safety pattern that worked: Build-validate (non-activating) then fresh store backup then Activate then verify (version, counts, guardian probe); rollback = restore store plus revert-pin.
