# Book deployment investigation

Prepared 2026-09-28 for Psyche Fable c02c0d. This is an evidence report. It does not approve a generator, skill, record, projection, readiness, or host change.

## What the earlier review reported

The prior review, [subagent-generator-review.md](subagent-generator-review.md), was delivered to Mind Astra 6f51ad, not to Psyche Fable 8904b1. It recorded 11 current role definitions expanding to 24 packets and the Book specification's proposed canonical record:

    Subagent.{ Name Aspect Purpose Power Vector<Skill> Vector<Tool> Instructions }

Its proposed Low/Medium/High bridge, external policy record, and model table were explicitly unapproved. Aspect, Power, skills, and tool inventories were not derivable from current role data. The review also recorded that the temporary Sol exception applies only to the explicitly requested native Sol seat, not to all roles. Its smallest possible future implementation boundary was schema and generated Rust, record data, packet projection, and focused tests. No landing was authorized.

The review's Claude 2.1.280 probe established selected custom-agent JSON acceptance: explicit tools `[]` initialized as `[]`, while omitted tools initialized as `Bash`, `Edit`, and `Read`; authentication failed before model execution. It did not establish YAML agent-file parsing, spawned-agent execution, or tool enforcement.

## Deployed Book observation

The deployed `.claude/agents/book.md` is 537 bytes with four frontmatter keys: `name`, `description`, `model`, and `effort`. It selects `claude-haiku-4-5` at medium effort. Its body contains only the present common modules: general instructions, spirit, and intent. It contains no Book-owned procedure, startup skills, or tool inventory.

This follows from the current generator, rather than a missing projection alone. `curriculum-deploy` reads only `Curriculum/skills/*.md` and `roles.datom`; its role renderer receives identifier, discipline, depth, description, and surface, then writes Claude name, description, model, effort, and assembled modules. It has no Book procedure, skills, or tools input.

The current pinned Curriculum revision is `4ef05170742faf22f7218279374f5cab79934b66`, and its checked-out `roles.datom` and `skills/operation-book.md` match the canonical repository byte for byte. Its `operation-book` source still describes the older `items`, `news`, and `state` page shape. That is incompatible with the Book specification's subjects, waiting rows, and distillations. Primary pin `38875776` made the title-source revision available; it did not deploy a Book body. Main-flow projection generation and freshness remain open behind Zeus and are unrelated to this Book-body failure.

## Candidate procedure versus canonical specification

`subagents/book.md`, added in primary commit `e96b87e134ccf23db0f15583f718f12aac261623` at 2026-09-28 15:35:07 -06:00, is plain Markdown headed `# Book`; it is neither a typed record nor generated frontmatter. It proposes a High/Opus judge, `psyche`, `psyche-distillation`, and `vocabulary` skills, and `ArtifactData` and `ArtifactComments` tools. Aspect is unset.

Its proposed procedure makes the Book itself read, merge, and write the page. It reads a stretch of at most 40,000 characters itself; larger stretches use bounded `general-purpose` Sonnet readers following `book-reader`. It does not prescribe recursively launching another whole-work Book.

The canonical Book specification is in `flows/8904b1/specs/book.md`, committed as `cf1d3e8ab` on 2026-09-28 at 14:52. It defines High/Medium/Low as its own proposed arrangement and says the procedure belongs in the sub-agent definition, not in a skill it must discover. Neither this specification nor the candidate procedure is an approved deployed typed Book record.

## Observed first Book failure

Method: bounded inspection of the native parent and two nested Claude JSONL records for session UUID `c02c0dd5-7a9a-400a-a79c-18b182537e7e`; only the cited tool and result records were read.

At 2026-09-28T21:47:42.321Z, the parent invoked `subagent_type: book` with `Update the page.`, `$subflow`, and the c02c0d flow identity. The async receipt at 21:47:44.235Z resolved that worker as `claude-haiku-4-5`. At 21:47:51.132Z, that caller invoked a second `subagent_type: book` with `Update the page for flow c02c0d.` This is a witnessed nested whole-Book invocation.

The first caller's bounded tool inventory was one Bash, one Read, and one Agent invocation; its Read targeted `flows/c02c0d` rather than the caller transcript.

The second worker loaded `operation-book` at 21:48:02.886Z. It inspected the old page collections, then attempted transcript lookup using session `0145Yv8vLENH4AXjQ8ZbTdHs`; that lookup failed with `Transcript file not found`. It did not read the caller's JSONL. At 21:49:20.792Z it atomically made exactly two writes: it retained the transcript mark at line 8089, rewrote `pageReadAt` to `2026-09-28T21:33:00Z`, and added `news/news-20260928-2133`. The result at 21:49:21.236Z confirmed version 5 and exactly two writes.

The mark did not advance. Its timestamp was rewritten without observed transcript progress. No inspected worker tool call wrote subjects, waiting rows, or distillations. This establishes an observed failure of the deployed route to follow the bounded Book procedure; it does not establish that every Book invocation behaves this way.

At 21:51:46.169Z, the parent requested a repair from a general-purpose Opus worker, explicitly directing it to read `subagents/book.md`, not load `operation-book`, remove the stray news row, and repair bookkeeping. That is a repair instruction witness, not proof that the repair completed.

## Unknowns and decisions still needed

The Book procedure's source, typed record fields, Aspect, Power, model mapping, startup skills, tool portability, and explicit tool inventories remain unapproved. The candidate procedure supplies evidence for a proposal but does not fill those decisions automatically.

The minimal next proposal is to make the Book procedure generated own `Instructions`: the judge owns fetch, merge, and write; readers are bounded and used only as the procedure defines. The obsolete `operation-book` content must be rewritten to the present page model or withdrawn so it cannot remain an alternate operative path. This is a proposal, not a landing instruction. No decision is requested from the living in this report.

## Sources

- `.claude/agents/book.md`, deployed agent, 537 bytes, SHA-256 `aecd0380cc8757bd791a780cb4c96d2f0ca234e3ae61089990316342ebd45e32`, observed 2026-09-28.
- `repos/curriculum-deploy/src/runtime.rs` and `src/roles.rs`, clean revision `dc7f70edce087ac4157d7b48af954177ce454491`, read 2026-09-28.
- `/git/github.com/LiGoldragon/Curriculum/roles.datom` and `skills/operation-book.md`, clean revision `4ef05170742faf22f7218279374f5cab79934b66`, SHA-256 `9a8a8c6eb48fcb307ac8e19a0880bbcb416b6b6f5a5025aadc06df6072184d6b` and `49d15b4bd13cd4e7dbdfb63b838c47b79a79483f02e1d8e88ee4774c6b9d4513`, read 2026-09-28.
- `subagents/book.md`, SHA-256 `8fe94998fbcefe1e58b2c7487278218841e8b0e181628c85323690b196dea611`; primary commit `e96b87e134ccf23db0f15583f718f12aac261623`, 2026-09-28 15:35:07 -06:00.
- `flows/8904b1/specs/book.md`, Book specification, commit `cf1d3e8ab`, 2026-09-28 14:52.
- `/home/li/.claude/projects/-home-li-primary/c02c0dd5-7a9a-400a-a79c-18b182537e7e.jsonl` lines 237, 240, and 267; nested records `subagents/agent-a27cc54b5e9e01ccb.jsonl` line 21 and `subagents/agent-aef3c56f44abe8cc7.jsonl` lines 26, 63, 78, 101, and 102; native Claude records observed 2026-09-28T21:47:42Z through 21:51:46Z.
- `flows/b666e7/reports/subagent-generator-review.md`, prior review delivered to Mind Astra 6f51ad, primary commits `3f81c0a9` and `450e9253`.
