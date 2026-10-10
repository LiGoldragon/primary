# Codex web-reporting procedure recovery

The report hub exists at [Codex Reports](https://codex-reports-hub.ligoldragon.chatgpt.site). Current read-only Sites evidence says it is version 1, deployed successfully with owner-only access, no external visitors, and no failure state.

The procedure was not stated in one message. It is reconstructed from explicit living instructions plus witnessed agent and hosting actions. The reconstruction is preparation for a Codex-only skill, not yet an approved skill contract.

## What the living explicitly asked for

> Use ratios rather than absolute values and give me some visuals.

Codex `01a04236-2355-7d20-94aa-e3b814a52b32`, 2026-08-27T08:42:08.620Z, transcript line 368.

> Problem: I can't see this remotely. Is there a plugin or something to allow you to publish those on a server the way Claude puts reports on claude.ai?

Codex `01a04236-2355-7d20-94aa-e3b814a52b32`, 2026-08-27T09:00:41.430Z, transcript line 462.

> Yes use the hub

Codex `01a04236-2355-7d20-94aa-e3b814a52b32`, 2026-08-27T09:05:53.795Z, transcript line 495. Private access was agent-proposed immediately before this acceptance, not independently ruled as a universal default.

> Check a recent codex session for the web reporting procedure which we'll put in a codex only skill

Codex `01a0428b-fc0e-7200-904e-2e2991e5425f`, 2026-08-27T10:16:44.427Z, transcript line 334.

> I didn't mean use terra for everything, I meant for the report writing

Codex `01a0428b-fc0e-7200-904e-2e2991e5425f`, 2026-08-27T10:18:14.709Z, transcript line 389.

The settled boundary is: when a report needs remote viewing, produce a web report through the hub with ratio-based visuals and an accessible URL. Terra is for report writing, not general investigation or implementation.

## Reconstructed witnessed procedure

1. Establish whether the request is for an inline visual or a remotely hosted web report. Resolve speech-to-text ambiguity before building.
2. Have an investigation subflow recover exact typed-message provenance and separate the living's instruction, written psyche, direct witnesses, agent reconstruction, and unknowns.
3. Write an editorial report rather than an invented dashboard: include durable Flow identity, sources, ratio-based visuals, findings, evidence, and open questions, with a place for later reports in the same hub.
4. Keep media distinct: ASCII in a response, Mermaid in a stored artifact, and a web report page for remote presentation. The HTML implementation is not itself a psyche ruling.
5. Keep site ownership with the Codex flow that owns the checkout and Sites operations. Research and image subflows return evidence or assets; they do not own deployment.
6. Build and validate locally: scaffold the Sites project, inspect configuration, build report/navigation, add metadata and any optional social image, run local development, repair runtime failures, verify HTTP 200, and verify the production build.
7. Publish deliberately: create the site once and retain its project identity, commit the exact validated source, package and save a version tied to the pushed revision, select access mode, deploy, and observe terminal success.
8. Hand off the verified URL. Keep credentials, signed URLs, private archives, and sensitive deployment material out of reports and conversation.

## What was proved

- Local report serving eventually returned HTTP 200.
- The production build succeeded.
- A Sites project and version 1 were created and a private deployment initiated.
- The report URL was returned in the original parent session.
- Current Sites evidence reports deployment status `succeeded`, version 1, and custom owner-only access.

The original run encountered and repaired a development-server `EPIPE`, Nix/workerd loader problems, an initial HTTP 500, and a hung first push. Historical transcript polling reached only pending/publishing; current Sites state supplies the later terminal-success witness.

## What was not proved

- Browser screenshot or DOM-level verification after deployment.
- Multi-report navigation and routing.
- A subsequent report update and version cycle.
- Future URL/slug collision behavior.
- Rollback behavior.
- Whether owner-only access should always be the default.

Child session `01a04285-f8f1-7202-8bbd-9131fba65747` generated and inspected a social-preview image. That was an implementation contribution, not a living requirement. Its encrypted task brief cannot establish another living instruction.

## Excluded from canon

These were agent choices and should not become Codex-skill law:

- D3, HTML, viewport, editorial styling, and individual chart choices.
- ImageGen use, social-card copy, and the generated image.
- A particular dependency upgrade.
- Alternate credential handling used after the first push hung.
- Private access as a permanent default merely because it was proposed and accepted in this one exchange.

Privacy protection is required. The exact access policy remains open.

## Proposed Codex-only skill anatomy

Trigger: a Codex report or visual needs remote viewing through the established hub.

Inputs to establish first:

- hosted versus inline output;
- source Flow and session identity;
- audience and access requirement;
- whether the report contains private material;
- whether this is a new report or a hub update.

Required phases:

1. Recover typed-message provenance.
2. Separate living instruction, witness, inference, and unknown.
3. Use Terra for report writing when the living requests that model boundary.
4. Write the report with Flow identity, sources, findings, ratios/visuals, and open questions.
5. Use a site-owning Codex flow for modification and deployment.
6. Validate local HTTP and production build.
7. Version against the exact source revision.
8. Deploy with an explicitly selected access mode.
9. Observe terminal deployment success and return the verified URL.
10. Record unresolved claims and keep sensitive material private.

Proof gates:

- Exact request and transcript provenance.
- No conflation of reconstruction with instruction.
- Terra confined to report writing.
- Local HTTP success and production build success.
- Deployment version tied to source revision.
- Terminal deployment success.
- Verified URL and access mode.
- No credentials or private deployment material in the report.
- Explicit open-question section.

## Procedure checklist

```text
[ ] Hosted viewing explicitly wanted?
[ ] Typed living request recovered with line provenance?
[ ] Instruction / witness / inference / unknown separated?
[ ] Flow identity and source trail included?
[ ] Ratio visual and readable report prepared?
[ ] Site-owning Codex flow owns build/deploy?
[ ] Local HTTP 200 and production build pass?
[ ] Version bound to validated pushed source?
[ ] Access mode explicitly chosen?
[ ] Deployment terminal-success verified?
[ ] URL returned and private data withheld?
[ ] Later-update, routing, rollback, and ACL unknowns recorded?
```

## Sources

- Codex transcript `01a04236-2355-7d20-94aa-e3b814a52b32`, exact lines cited above and build/deploy lines recorded in the witness.
- Codex transcript `01a0428b-fc0e-7200-904e-2e2991e5425f`, exact lines cited above.
- Codex child transcript `01a04285-f8f1-7202-8bbd-9131fba65747`.
- `flows/01a0428b/witnesses/codexWebReportingProcedureRecovery.md`.
- Current Sites project and deployment state for `https://codex-reports-hub.ligoldragon.chatgpt.site`.
