# researchTools handover — open Task l0mm

## Current task and controlling shape

Psyche core Opus Task **l0mm (240 minutes)** remains open. No new implementation, repository selection, benchmark questions or installation has begun. Latest **7zcl replaces t7lz and ved5**:

- Flows remain on Ouranos and keep the harness’s **native read/write/edit tools**. No edits or ordinary commands wrapped in SSH. The working copy must be a local path there. Only **LSP questions** and **builds** go to Prometheus, each by one command.
- Manually test **A: one Prometheus working copy mounted on Ouranos via NFS or sshfs**; **B: an open-source two-way synchronizer maintaining local and Prometheus copies**. Neither is merely a fallback for the other: test both. Start mounts/synchronizers by hand and remove afterward; **nothing declared on a host**.
- One language server per repository on Prometheus, **shared by all flows**. No rust-analyzer on Ouranos and no proprietary service. Measure memory with concurrent querying flows, native-tool read/edit/text-search speed for A/B, edit-to-fresh-LSP latency/staleness, and behavior when Prometheus/network fails. Show text-search continuation working. Assess in-flight work and uncommitted edits under a power cut; distinguish bounded failure simulation from untested actual power-loss durability. Do not disrupt shared host/network to simulate a fault.

## Required study still in force

Flow plus **one larger active Rust repository**, chosen with measured size and repeated/noisy-name justification; ask owners for published immutable revisions and disposable-worktree boundaries. Do not assume which active repo uses Kameo.

Live rust-analyzer via harness LSP tooling or thin client: definitions, implementations, type-at-position, workspace symbols and call hierarchy. Overview tools: existing Ouranos ast-grep outline and a Nix-built ranked Aider-style/equivalent map, **no Node**. Reuse existing tools first; previous stack ruling is Rust/Nix, not a new application stack.

Paired with/without each tool, same questions/source/model/effort and isolated answerers: tracing (trait implementation, types a Send traverses), overview (how a message passes through Flow). Include a **Haiku-class** stratum; keep controls within the same model class. Score **precision, recall, tool-text tokens and time** against a **hand-written answer key frozen before trials**; one pair is not a general performance claim.

Addition k6fd: one command recursively walks outgoing calls of an entry point into a compact call tree. Report breaks at trait dispatch, macros and Kameo actor sends (**message hops are not call edges**). If Kameo needs a separate fixture/example, label it rather than inventing an in-repository edge.

New report beside `flows/72fb9a/research/semantic-code-map.md`; end with best-saving questions/commands as a **draft knowledge module**, install nothing. Answer Opus with `Done` naming **l0mm**, report path and figures in **one line**, only when complete.

## Next step: survey before design/build

Survey exists: `/home/li/primary/flows/72fb9a/research/semantic-code-survey.md`. Its five closing lines were read in this flow (m6iy): strongest independent small study found reference precision 1.00 vs grep 0.76; token savings only for Haiku/noisy-name repos, none for capable models, rare unprompted use. Overview savings are vendor claims; no published call-tree/trait/macro/actor measurement. Questions are not fixed.

**kxa5 confirms the remote-language-server section now exists at the end of that survey; read it before building anything. Its first candidates are lspmux (shared rust-analyzer) and Mutagen: reuse before building.** This section has not yet been read in this flow. Use its evidence to choose remote/shared-server and filesystem tools, then propose the smallest bounded matrix and hand-audit its keys. Coordinate temporary mount/sync/fault scope and cleanup with Field rather than modifying host declarations.

## Prior result, evidence and ownership

**n4p4 closed**, accepted Result `tovv`, Opus dv3d confirms delivered to Fable: keep package **proposal only, adopt nothing**. Final report `flows/72fb9a/research/semantic-code-map.md` contains batch SCIP study, source keys, exact counts/timing/method, audit and reproduction. Both answered correctly; SCIP 46,531 vs 41,687 cl100k tool-text tokens, 217.594 vs 195.783 s. This was not a live LSP trial.

Published proposal-only CriomOS branch `research-tools-2ce803-scip`, revision `ab62d218610f35af6279ed3590224dee83645011`; Flow target `37980e10bcb8325d9a68c580e0d22c73061bb267`. No host/service/main/skill adoption. Local scratch `/tmp/research-tools-2ce803.nrkzTR/`, builder scratch `/tmp/research-tools-2ce803.xkSGrr/`: packaging, old clean checkouts, extraction/counts and evidence. Old answerers already know old keys; not fresh controls for overlapping questions.

Mind core Sol locates current owners/capacity; Mind flowNexus Sol owns Flow revision boundaries; Mind nixCriomos Sol reviews packaging; Field core Sol alone acts on host runtime. Prometheus has no declared li Home. Sol implements directly: AGENTS forbids Sol subagents; Luna allowed plain search/list/test, not implementation; never Astra. Arrange requested Haiku-class benchmark seats through owners. Preserve unrelated primary/canonical edits; isolated owned branches, own-file commits, no generated skill-tree edits or direct skill-file loading. Compiler guards exist on both hosts: declared toolchain/build-script/proc-macro accounting is required, not casual bypass.

Repeated near-threshold notifications have requested this handover/refresh while new task changes arrived. The successor must pursue l0mm; no new worker or implementation is currently running.
