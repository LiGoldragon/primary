*Kind: Frame · Topic: design cascade + context sweep · Date: 2026-05-23*

# 0 — Frame and method

## What this directory is

Meta-report per intent record 231 — sub-agents run in parallel
along six lanes; this directory is the session unit. Final
synthesis in `7-overview.md`.

Per psyche 2026-05-23: get the design ready for everything stated
this session, refresh from intent and manifest what marries with
the current context, create smaller distributable beads, do
context maintenance, and audit operator work in relation to what
designer is designing. Use sub-agents with meta-report approach.

## Intent records driving this session

Recent + just-captured:

- **270** component binary naming convention (CLI=`<comp>`, daemon=`<comp>-daemon`)
- **280** drop `persona-` prefix from supervised components (Reading B extended)
- **309** delete `persona-sema` repo (legacy design-phase residue; audit + absorb + delete)
- **310** rename `persona-llm-client` to `agent` (new triad component; supervised; hooks to mind)
- plus older context: 244/251 (three-tier signal sizing), 252 (Design D Persona FD-handoff), 271-273 (verb-namespace + universal data variants + extended tier), 274 (Mirror raw container), 275 (persona-mind agent-error events), 276 (NOTA-as-comments)
- 255 (designer delegation pattern), 256 (audits feed beads)

## Sub-reports + sub-agent assignments

| # | Title | Author |
|---|---|---|
| 0 | Frame + method (this file) | second-designer (orchestrator) |
| 1 | Agent triad design (new component per intent 310) | sub-agent A |
| 2 | persona-sema audit + absorb + delete plan (intent 309) | sub-agent B |
| 3 | Context maintenance sweep across recent reports | sub-agent C |
| 4 | Operator audit — alignment with current design | sub-agent D |
| 5 | Intent refresh + manifestation gap audit | sub-agent E |
| 6 | Bead-splitting sweep (smaller distributable beads) | sub-agent F |
| 7 | Overview synthesis with visuals | second-designer (orchestrator) |

## Sub-agent contract

1. You are a second-designer-window sub-agent (designer discipline:
   architecture as craft).
2. Stick to your slice. Don't expand scope.
3. **Do NOT dispatch sub-sub-agents** (intent record 5).
4. Observe Spirit with `spirit '(Observe (Records (None None WithProvenance)))'`.
   Do NOT capture new intent records (orchestrator handles intent capture).
5. Use `jj` for version control with HEADLESS `-m '<msg>'` flag
   (intent 237). NEVER let jj open an editor.
6. All `nix` invocations use `--max-jobs 0`.
7. Use full English names per `skills/naming.md`.
8. NOTA records are positional per `skills/nota-design.md`.
9. No `---` horizontal-rule lines in markdown.
10. Opaque identifiers (commit hashes, bead UIDs) carry inline
    descriptions on first mention in chat-facing text.
11. Per `skills/mermaid.md`: NO `;` in sequenceDiagram Notes or
    messages; NO Unicode arrows in sequenceDiagram body; NO
    pipe-delimited labels in sequenceDiagram (that is flowchart
    syntax — use separate sequence-diagram messages OR a flowchart).
    Quoted flowchart node labels accept HTML `<br/>` and Unicode
    arrows safely.
12. Sub-report path: `/home/li/primary/reports/second-designer/161-design-cascade-and-context-sweep/<N>-<slug>.md`.
13. Chat response shape per intent 232: 3-7 items balanced across
    (a) intent questions/clarifications, (b) observations/explanations,
    (c) examples/evolving picture.

## Working context (pre-session state)

Operator window holds `primary-a5hu` claim (Persona engine systemd
unit management slice). Several routing beads landed in /155 +
/157 + earlier sessions: `primary-l02o`, `primary-bg9l`,
`primary-b86d`, `primary-2py5`, `primary-ezzp`, `primary-x5ba`,
`primary-ak4g`, `primary-wehu` (CLOSED), `primary-yvno`,
`primary-7kpe`, `primary-pjyk`, `primary-tfdj`, `primary-k8cn`,
plus constraint tests `primary-2o7p`, `primary-2ach`,
`primary-l9iz`, `primary-fv2l`, `primary-vjg3`, `primary-n9st`,
`primary-lfb0`, `primary-e2bc`. Bead `primary-0m1u` covers the
coordinated persona-prefix rename (24 repos).

Recent reports:
- second-designer: /152 meta-dir, /153-/158, /159 meta-dir, /160
- designer: /285, /286, /287, /288, /289, /290, /291, /299, /300, /301, /302
- operator: /157-/163 plus three 2026-05-23 unreported structural commits
- second-operator: /165-/170
- third-designer: /17-/21
- cluster-operator: /2-/6

This is the surface the sub-agents operate against. Each sub-agent
absorbs only what they need for their slice.

## Garbage collection

Per intent 231 this directory is one session unit. When substance
migrates to permanent homes (ARCH, skills, INTENT, beads), the
directory retires together.
