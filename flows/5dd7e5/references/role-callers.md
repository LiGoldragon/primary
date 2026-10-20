# References: Roles that call roles

## Sources read (witnessed by this subflow, 2026-10-19)

- `curriculum.ethos`, whole file (Proposal 6 shows it whole, because the builder checks each ethos block as a complete document; lines over 52 columns reflowed): `RoleCallers`, `RoleDefinition`, `Roles`, `RoleComposition`, `CliRequest`, the header comment.
- `curriculum.ethos`, lines 40-45: `RoleCallers.[ Any Only.Vector<CallerMetaflow> ]`, `RoleDefinition`, `Roles`, `RoleComposition`.
- `roles.datom`, line 26 (book: `Explicit.[ Read Bash Agent Artifact ] Any`), line 28 (illustrator: `Explicit.[] Any`), line 32 (`] }`).
- `src/roles.rs`, line 59 onwards: an `Only` caller list is validated as `{ word word Primary|Secondary|Tertiary|Quaternary }` tuples.
- `src/claude_agent.rs`, line 13: native rendering refuses any role whose callers are not `Any`; it supports only book and illustrator.
- `README.md`, lines 8-21: the producer writes no files. The deployment owner installs the rendered output as `.claude/agents/book.md`.
- `tests/explicit_role_policy.rs`, line 40: an `Only` fixture names a `Publisher` metaflow caller.
- The local checkout is detached from b56284c and has uncommitted changes to `roles.datom` and `src/`, which belong to another flow. Nothing here reads them.

primary `.claude/agents`: `/home/li/primary/.claude/agents`, tracked in git.
- Files: book.md, book-page.md, illustrator.md, read-demanding.md, read-ordinary.md, read-trivial.md, tester.md, write-demanding.md, write-ordinary.md, write-trivial.md.
- book.md and illustrator.md were last written by primary commit 4d8171d "Install Curriculum generated book and illustrator agents" on 2026-10-19. Their frontmatter matches the output of `claude_agent.rs`.
- The other eight were last written by 5e34953 on 2026-10-16. They come from the retired Curriculum file projection: `src/projection.rs` exists only on `origin/backup/pre-sources-rewrite-20261012`, and 925a55c retired the projection.
- No flow log or tool found under primary names the flow that made 4d8171d.

Flow: `/git/github.com/LiGoldragon/flow`, commit f1dee77 on `aa034f-compose-role`.
- `crates/flow-defaults/src/lib.rs`, line 110: `SUBAGENT_ROLES = ["comment-relay", "book", "illustrator"]`.
- `crates/flow-nexus/src/role.rs`, line 373: `if call.nested { return AgentDecision::Denied(AgentDenial::NestedCaller) }`. This is the role-to-role deny. Lines 257-265: `permits` matches only `Any` or the flow's Address.
- `crates/flow/src/hook.rs`, lines 155-164: an Agent call is `nested` when the event carries `agent_id`. Line 192 holds the denial text.
- `crates/flow-nexus/ethos/role.ethos`: `AgentFile`, `AgentCall`, `AgentDenial`, `RoleRefusal`.
- `crates/flow-nexus/src/herdr/launch.rs`:
  - line 1505: the pane `--cwd` is `configured_workspace_root()`.
  - lines 624-640: the workspace root is the parent of the configured `flows` root, which is /home/li/primary.
  - lines 1676-1697: roles are composed into `role_files` and passed with `--add-dir`.
  - line 1933 onwards: `hold_roles` creates the role root.
- `DESIGN.md`, lines 33-60: the roles section.

## Claims relayed, not witnessed

- Claude ranks a same-named project agent in the working directory's `.claude/agents` above the `--add-dir` one. This is Psyche flow Secondary aa034f's claim, relayed by 5dd7e5. No probe ran here.
- Whether Claude searches parents of the working directory for `.claude/agents` is unknown. Proposal 4 checks every ancestor because the brief speaks of the working-directory chain.

## Records drawn from

- d68c82 flow: "2026-10-16 11:29 A role may call a subagent model one rung up" and "2026-10-16 11:25 Roles defined as datom data in their own repository".
- da2038 flow: the entry on the Publisher calling a Sonnet Illustrator subagent, and the entry on a role overriding its allowed subagent models.
- d68c82 messenger: "2026-10-16 11:29 The illustrator and the publisher".
- 48cff7 curriculumSubagentGap: Curriculum has no authored surface for specialty subagents.
- 28d847 curriculum: "Edits in the workspace regenerate per harness".
- psyche-context vision/flow.md (origin/main 6c8e266): "Starting flows", which covers the Nexus replacing harness subagents.
- psyche-context vision/subflows.md: long term, actual flows replace the harness subagent tool.
