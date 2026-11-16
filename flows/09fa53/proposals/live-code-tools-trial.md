# Live code tools: bounded trial proposal

Status: l0mm remains open. **Superseded by Opus 4hk2:** drop the filesystem A/B, choose the least-setup working method, run tool-versus-text-search pairs with cheap Codex sessions. The original matrix below is retained as proposal history, not current execution authority. Field ll20/bkvb holds runtime and provisioning pending transition/idle-lock priorities; no runtime reservation or process exists.

## Current reduced execution shape

- Source identities: Flow `a044e39ac2bc19cdcd3d435c75448d8697c6a17d` (Flow owner n8yv), Lojix `5d75a4032079cd942a3d4f5ba676da9ade5e8249` (Curriculum dya8 publication evidence; Core tpjf grants read-only independent git archive). No canonical source edits or linked worktrees.
- Filesystem: existing Ouranos sshfs is the least-setup candidate. No synchronizer provisioning and no filesystem-arm comparison. All normal source reads/searches stay native against the local mount path; LSP/builds alone are remote commands.
- Comparison: two corpora × three tools (live LSP tracing, ast-grep overview, ranked-map overview) × one cheap Codex model class = six pairs/twelve fresh sessions. Core has been asked for native model and effort. Each pair has identical model/effort/question/revision/budget; frozen keys stay separate. The old Haiku/capable split is treated as superseded, with that reading sent to Opus.
- Retain shared-server verification, source freshness, fallback text-search behavior and bounded failure observations as operational checks, without recreating the dropped filesystem experiment. Actual power loss remains untested.
- Field alone assigns runtime actor and exact mktemp roots after its hold clears. Next runtime packet must name remote executable provisioning, compiler/build guard, commands and cleanup before execution. Discovery/implementation/provisioning/launch are not authorized by the source-read grants.

The rest of this file records the original broader proposal for traceability.

### Version-specific preflight finding

The published [lspmux 0.3.0 package README](https://docs.rs/crate/lspmux/0.3.0) is reachable even though Codeberg is not. It documents workspace/environment-based instance sharing, a Unix socket option and explicit `--server-path`, but its command list includes `reload` and omits the survey's `sync`. Therefore `sync` is not yet a verified available operation for the selected artifact. Check actual version/help/source during authorized provisioning; freshness must be demonstrated with that artifact rather than assumed from the survey. The README also says server-originated requests are dropped. Supply initialization settings explicitly and test readiness, request handling and shared-process identity before any model trial. Its internal timed garbage collection is an existing-tool behavior, not a proposed new polling mechanism.

## Corpus decision

Read the remote-server survey in `flows/72fb9a/research/semantic-code-survey.md` before this design. Read the raw instruction in `vision-raw/why-is-rust-analyzer-running.md`: rust-analyzer must not start automatically. Only manually started Prometheus processes are proposed.

Local HEAD survey on 2026-11-15, tracked Rust files including tests and generated/history code:

| Repository | Immutable local revision, publication not yet verified | Rust files | Rust lines |
| --- | --- | ---: | ---: |
| Flow | 53782fba5e1f5b761b87f09809c0b319bcc27ad0 | 128 | 84,185 |
| Lojix | 5d75a4032079cd942a3d4f5ba676da9ade5e8249 | 44 | 28,805 |
| memory-engine | cd57ed6c51f9de4fe37c903c29a8ed70265f7f75 | 51 | 21,208 |
| Curriculum | 4695835442f9369612569b73b0bbeeec67676e79 | 17 | 3,549 |

Counts use `git ls-tree` and newline counts of `git show REV:FILE`, not a working-tree scan. A line-oriented function-declaration regex finds Lojix names `from` 43, `new` 31 and `run` 25 times; this is a noise indicator, not a symbol census. Flow has 113 `record_key` declarations; historical/generated code contributes to its size. The same source filters must apply to both arms.

Candidate second corpus: Lojix, substantially larger than the previous Curriculum corpus, but smaller than current Flow. Opus has been asked whether this interpretation satisfies the task. Its manifest declares Kameo 0.20; no actor-hop claim is made yet. Source owner and publication must be confirmed before fixtures or keys are written against it.

## Filesystem and shared-server matrix

Two independent filesystem arms, on each authorized corpus:

- A: one disposable Prometheus tree, mounted manually on Ouranos with existing sshfs. Native harness reads, edits and text searches use that local mount path.
- B: one disposable local tree and one Prometheus tree, synchronized in both directions by an existing open-source synchronizer. Evaluate Mutagen first, as the survey requests; use only a verified non-SSPL build. Configure `no-watch` and invoke `sync flush` on the edit/query event, rather than introducing a polling design. Confirm two-way mode and conflict behavior. If that artifact is unavailable, bring the concrete limitation and Unison option back to the owner before choosing.

Reuse lspmux first. Its client and server run beside rust-analyzer on Prometheus, reached for each LSP question by one command. One rust-analyzer per repository, shared by every concurrent client. First test path identity, `sync`, client disconnect and simultaneous requests. Map returned remote URIs to the local tree in a thin client only if the harness cannot do so. That client owns framing, request IDs, URI mapping, deadlines and visible failures; it does not own indexing or multiplexing.

For each filesystem arm, hold the corpus and analyzer settings fixed; measure with 1 and 3 concurrent clients. Runtime clients are not model answerers. Record rust-analyzer/lspmux RSS and aggregate process-tree memory, query success and latency. Reuse the single server sequentially between A and B so the trial itself does not create multiple analyzers for one corpus.

## Freshness and failure measurements

- Native local-tool reads, one bounded source edit, and text searches: retain output equality, cold/warm timing, file counts and source hashes. Run five repetitions, record every observation and the median; do not infer statistical generality.
- Before an edit, capture hover/definition and file hashes. Edit an owned fixture, signal synchronization where applicable, invoke lspmux disk synchronization, then make one LSP request. Measure edit acknowledgement to matching fresh result. Verify result content, not just command exit. Separately test add/delete/rename and concurrent conflicting edits.
- Scoped failure: Field authorizes ending only trial-owned transports/processes. Leave a request in flight, sever its transport, check deadline/error, then run native text search and edit on each arm. In A, cached reads may differ from uncached reads; measure both. In B, demonstrate local search and edits during isolation, then explicit conflict handling/reconciliation after return.
- Record acknowledged and unacknowledged edit hashes at both endpoints, interruption during transfer, and restart outcomes. Process termination and a scoped transport break are bounded simulations. Actual power-cut durability, storage flush semantics and loss of host RAM remain untested.
- All artifacts go in temporary directories; one cleanup manifest names every process, session, mount and tree, with the Field owner for its removal. No shared network or host interruption.

## Semantic tasks and frozen oracle

At owner-approved published revisions, hand-audit a tracing packet and an overview packet for each repository. Freeze numbered answer facts and source ranges before any answerer starts; retain a SHA-256 digest and keep the key outside answerer trees.

The tracing packet must exercise definition, implementations, type at position, workspace symbols and outgoing call hierarchy, including one repeated name. A compact recursive outgoing tree is one command with explicit depth/node budgets and cycle markers. Verify edges against source; report trait dispatch and macro breaks. An actor send is a separate message-hop observation, never an invented call edge. Use a labelled fixture only if the selected corpus has no suitable example.

The overview packet asks how the Flow message path works, with the second repository's analogous request lifecycle. Reuse existing Ouranos ast-grep outline. Build the ranked Aider-style map with Nix on Prometheus, no Node; previous Python-environment installation is not the requested Nix packaging proof.

Minimum paired matrix: two corpora × two model classes × three separate tool comparisons = twelve pairs, twenty-four isolated answerer sessions. Comparisons are plain native source tools versus +live LSP on tracing, versus +ast-grep outline on overview, and versus +ranked map on overview. Each pair gets the same question, revision, model, effort, budget and source filter; each session is fresh and sees one arm only. This estimates each tool separately, not a combined stack or an A-versus-B model outcome. Choose one validated filesystem arm for these model trials; report that choice.

Arrange Haiku-class seats through Flow owner; capable seats through owners after idleness confirmation. No Astra and no occupied-lane repurposing. Score fact precision and recall against the frozen key, with unsupported claims counted explicitly. Report all tool-result text tokens under one named tokenizer and elapsed wall time; report model usage separately when available. Tool-build/startup costs and warm/cold readiness are separate from answering time. One pair per cell establishes a worked example, not a general performance claim.

## Owners, sequence and completion

1. ResearchTools surveys and proposes; Opus resolves corpus scope; source owners provide revision/boundaries; Field clears exact runtime and cleanup.
2. ResearchTools freezes keys and packets, prepares only the necessary reusable-tool packaging/client; Mind nixCriomos reviews packaging; Field starts approved manual runtime.
3. ResearchTools measures filesystem/freshness/failure/concurrency; owners supply isolated answerers only after packets and tools are ready. Each phase's command exit or owner reply is the next event; no status polling.
4. ResearchTools audits scores, records cleanup receipts, commits its own report files and replies `Done` to l0mm only after completion.

Final report belongs beside `flows/72fb9a/research/semantic-code-map.md`; it ends with a draft knowledge module of the questions/commands that actually saved work. Nothing is installed as a skill or service.

## Verified reuse qualifications

Mutagen's [watch documentation](https://mutagen.io/documentation/synchronization/watching/) supports `no-watch` with explicit flush cycles. Its [license](https://github.com/mutagen-io/mutagen/blob/master/LICENSE) says official builds from 0.17 include SSPL enhancements and describes building without them. This is an artifact-selection requirement, not a legal conclusion. [Unison's own README](https://github.com/bcpierce00/unison) documents two-way conflict detection and offline local access. The survey's lspmux source could not be fetched through today's web tool; version-specific behavior must be read from the actual selected artifact/source before testing.
