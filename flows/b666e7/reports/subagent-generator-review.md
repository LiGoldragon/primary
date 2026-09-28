# Subagent generator review

Prepared 2026-09-28 for Mind Astra 6f51ad. This is a bounded review artifact, not an implementation authorization. Generator work, projection regeneration, readiness work, and host work remain queued behind Zeus.

## Evidence boundary

Psyche Fable's Book specification, dated 2026-09-28, defines the desired record:

    Subagent.{ Name Aspect Purpose Power Vector<Skill> Vector<Tool> Instructions }

Its Power variants are exactly `High`, `Medium`, and `Low`. `Xhigh` belongs to effort vocabulary only and does not fill a missing Power value. The Book is Claude-only for now and calls for effort `medium`; it says the generator must emit instructions, skills, and tools in addition to the fields it emits today.

The current canonical Curriculum source is clean at `4ef05170742faf22f7218279374f5cab79934b66` (`Remove V2 from main-flow titles`). Its role data has six description records and five alias records, which expand to 24 current surface packets. Current data has no Aspect selector, no aspect-isolated output, and no startup skill or tool metadata. Aspect, Power, tools, and skills therefore cannot be recovered safely from the existing data.

The current `curriculum-deploy` source is clean at `dc7f70edce087ac4157d7b48af954177ce454491`. Its generated types still carry `RoleDepth`, `RoleDescription`, and `RoleAlias`; its renderer loops descriptions and aliases, resolves model choices by depth and surface, and writes only the present harness fields. This is the smallest implementation boundary once decisions exist: schema/ethos and generated Rust, role data, packet renderer, and focused tests. It excludes hosts, hooks, readiness, UI, and broader architecture.

## Current definitions and packets

The purposes below copy the current role data. The Low/Medium/High column is a proposed bridge only: Low maps current `trivial`, Medium maps `ordinary`, and High maps `demanding`. It is not approved.

| Definition | Current purpose | Proposed Power | Surfaces | Permission |
|---|---|---|---|---|
| read-trivial | The answer is in one known place. You are fetching it, not finding it. | Low | Claude, Codex, Pi | Restricted |
| read-ordinary | You know what you are looking for but not where it is. | Medium | Claude, Codex, Pi | Restricted |
| read-demanding | The answer is written nowhere. Assemble it from how the parts behave. | High | Claude, Codex, Pi | Restricted |
| write-trivial | The change is fully specified. No decisions remain. | Low | Claude, Codex, Pi | Unrestricted |
| write-ordinary | The approach is known. Applying it is the work. | Medium | Claude, Codex, Pi | Unrestricted |
| write-demanding | The approach has to be chosen. | High | Claude, Codex, Pi | Unrestricted |
| default | General-purpose sub-agent for the Codex orchestrator | Medium | Codex | Unrestricted |
| explorer | Read-only exploration sub-agent for the Codex orchestrator | Medium | Codex | Restricted |
| worker | Implementation sub-agent for the Codex orchestrator | High | Codex | Unrestricted |
| tester | Independent testing worker. Given only a bounded target, immutable revision, authority limits, and acceptance contract, choose the procedure, fixtures, negative cases, and independent oracle; return evidence grades and gaps. | Low | Claude, Codex | Unrestricted |
| book | Keeps the living's page current from your own transcript. Call it with the one line: Update the page. | Low | Claude | Unrestricted |

The first six definitions each produce three packets (18); `default`, `explorer`, and `worker` produce one each (3); `tester` produces two; and `book` produces one: 24 packets total.

## Proposed migration shape

Adopt the Book's `Subagent` record exactly, with a separate proposed policy record:

    SubagentPolicy.{ Name Vector<Surface> Permission }

The external policy retains current surface selection and permission restrictions without reintroducing parallel role definitions. One pipeline must compose common modules, permission, target insertion, and the record's own instructions. It should preserve the current Codex-only skill-loading insertion.

The existing provider model-choice table may be rekeyed by approved Power while retaining the model catalog and validating `medium` effort against each chosen model:

| Proposed Power | Claude | Codex and Pi |
|---|---|---|
| Low | claude-haiku-4-5 | gpt-5.6-luna |
| Medium | claude-sonnet-5 | gpt-5.6-terra |
| High | claude-opus-5 | gpt-5.6-sol |

This does not relax the existing non-Sol helper restriction. The current mapping's Sol entry is a model choice, while the temporary exception applies only to the explicitly requested native Sol seat.

For a behavior-neutral migration, copy each current Name and Purpose exactly, preserve current policy, leave `Instructions` empty for the ten unchanged roles, and use empty `Vector<Skill>` only until Book curates its startup list. Book needs an authored procedure. Do not invent Aspect, Power, tool, or skill values during record migration.

`Vector<Tool>` needs an explicit portability and per-surface decision. Existing roles inherit harness authority today; encoding an empty tool vector for them could remove it. Do not treat `[]` as inheritance.

## Claude tool probe

The local Claude executable was `/home/li/.nix-profile/bin/claude`, version `2.1.280`. The two captured invocations used `--bare --no-session-persistence --permission-mode bypassPermissions --tools default --agents JSON --agent probe --print --output-format stream-json --verbose`.

The explicit-empty configuration was accepted and its initialization record reported:

    "tools":[]

The omitted-tools configuration was accepted and its initialization record reported:

    "tools":["Bash","Edit","Read"]

Both sessions then ended with `authentication_failed` before model execution. The logs are preserved by SHA-256: `empty.log` `6da135ae290e188f853c6f6a129a4add2514fc3f64ffc2b61bc9dbecf8a8de75`; `omitted.log` `6a33f4a56403ee0b26932041304914564fdcf290ec89a88b4036d65b04b25df2`.

This establishes acceptance and observed initialization for that exact CLI invocation. It does not establish YAML agent-file parsing, spawned-agent behavior, or tool enforcement. Official Claude guidance says omitted tools inherit; explicit empty-array semantics require version-pinned parser and spawned-agent tests before landing.

## Decisions required before implementation

1. Approve or replace the Low/Medium/High bridge and every migrated Power value.
2. Supply each Aspect; none is derivable from current data.
3. Specify portable tools, each surface binding, and explicit inventories that preserve intended authority.
4. Author Book instructions and its curated startup skills.
5. Decide the policy record and validate Claude empty-tool behavior with pinned parser and spawned-agent tests.

## Title projection context

The directly typed title instruction is recorded in `flows/b666e7/vision/namesOfFlows.md` (SHA-256 `f72a9e558dd656959efa9a06131a9d6f727184c49295a0597175e4e7ed032004`): “Let's get rid of the V2 in the names of the flows and in the tool that we're using.” The launcher change was pushed as primary `9ed50bda`; its Curriculum source change as `4ef05170`; and primary now pins that Curriculum revision in `38875776`. The generator executable is unavailable without a Nix build, so the two owned main-flow projections and freshness check remain open.

## Sources

- `flows/8904b1/specs/book.md`, Psyche Fable Book specification, 2026-09-28.
- `/git/github.com/LiGoldragon/Curriculum/roles.datom`, current clean revision `4ef05170742faf22f7218279374f5cab79934b66`, read 2026-09-28.
- `repos/curriculum-deploy/src/generated.rs` and `repos/curriculum-deploy/src/roles.rs`, current clean revision `dc7f70edce087ac4157d7b48af954177ce454491`, read 2026-09-28.
- `/tmp/claude-tools-probe.3ynfP9/empty.log` and `omitted.log`, local Claude 2.1.280 probe, read 2026-09-28.
- `flows/b666e7/vision/namesOfFlows.md`, typed psyche record, 2026-09-28.
