# repoChecklist

## 2026-09-16 — every repository has a checklist for conformance; touch it and either it passes or someone modernizes it

Context: while dispatching the concept subagent test, the living named the checklist rule for repository work.

> Let's make a checklist of all the things. When you encounter a new repository that hasn't been touched in a while, or any repository, you have a checklist to see if it still conforms with our checklist. Either ask questions of the designer or from the psyche, and make the changes to modernize or adapt it to the new checklist.

-- psyche, typed.

Flow reading, not the living's words: every touch on a repository is an opportunity to bring it into conformance. When a flow enters a repository (any repository — new, old, freshly discovered, or one being modified for other reasons), it runs the checklist. Non-conformance is not left in place: the flow either asks the designer / the psyche for what should happen, or performs the modernization itself when the answer is clear.

## Draft checklist (proposal for the living to correct)

For any repository this flow enters:

1. **Nexus shape (if applicable).** Does the repo hold a durable component (a tool, a service, a long-running behavior) that should be a Nexus? If yes and it is not one, name it as misimplemented per the porting rule in `flows/48cff7/proposals/nexus-porting-addition.md`.
2. **Wire types in Ethos.** If the repo carries a wire (JSON headers, ad hoc positional CLIs, ad hoc serialisation), migrate to `signal-<name>` and `meta-signal-<name>` per the `nexus` skill.
3. **Datom at boundaries.** CLIs take one inline datom argument, no flags. Rejects for legacy shape.
4. **README currency.** The README names what the component is today, not what it was. "Temporary, pending X" flags are opened as issues or promoted to vision entries.
5. **Skill coverage.** The repo's domain is covered by a skill (body + rationale if psyche-facing). Missing coverage becomes a proposal.
6. **Curriculum reference.** Repos generated from Curriculum reference their source; hand-authored repos declare their design docs.
7. **Attribution & psyche citation.** Recent commits carry the current attribution footer. Vision entries this repo depends on are cited in the README or the design docs.
8. **`.claude/` and `.codex/` generation.** If the repo is a workspace with `.claude/` or `.codex/` trees, they are generated evidence — never hand-edited — and regenerable from Curriculum.
9. **Long-running artefacts.** Nexus binaries and sema stores live at documented locations; the socket names and sema paths are recorded.
10. **Tests round-trip.** Every wire type has a concrete text example with a round-trip test per the `nexus` skill.

When a check fails: raise a psyche citation (a vision entry or an existing skill line) and either ask the designer or the psyche for direction, or modernize on the flow's own authority if the answer is clear from the citation.

## Non-conformance protocol

The order of moves when a check fails:

1. **Cite** — the vision/intent/spirit that makes this a non-conformance.
2. **Ask** — the designer named in the repo, or the psyche via the escalation citation rule (per `flows/48cff7/vision/escalationHierarchy.md`).
3. **Modernize** — perform the change when either the citation is unambiguous or the answer to the ask arrives.
4. **Record** — every modernization change carries the citation in its commit message.

Do not skip step 1. A silent fix without a citation is not conformance work; it is drift.

## Open questions worth the living's word

1. Confirm the ten checklist items above, or edit / cut / add.
2. Which repos this checklist applies to today — every repo under `Repository root`, or a named subset.
3. Where the checklist lives once settled — a `repo-conformance` skill, a `curriculum` entry, or a top-level `Checklist/` folder.
4. Whether the checklist is human-run (a flow reads it and applies it) or Nexus-enforced (a `curriculum-nexus` operation that scans and reports).
5. Whether this flow authors the initial checklist skill, or a dedicated design flow does.
