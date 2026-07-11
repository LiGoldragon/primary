# Research: Off-laptop Rust build and test workloads with fast agent feedback

## Summary

The most practical near-term architecture is a pool of native Nix remote builders plus a shared binary cache, with Rust checks split into separate derivations at the crate/check-suite level. This actually executes compilation and tests remotely, preserves the developer's normal `nix build` interface, and isolates concurrent agents; however, Nix only schedules derivations, so a monolithic `cargo test` derivation remains one coarse remote job and small source edits generally invalidate the whole source-dependent derivation.

For faster edit/compile loops, add compiler-object caching (`sccache`) or adopt a true remote-execution graph such as Bazel `rules_rust`; neither choice should be confused with remote test execution. Hosted CI/background-agent products are operationally easier but normally have push/queue latency and weaker local-loop ergonomics.

## Findings

1. **Nix remote builders execute whole derivations, not individual Rust test cases.** Nix can dispatch eligible derivations over SSH according to system, supported/mandatory features, speed factor, and job limits. Inputs are copied to the builder and results copied back. Granularity is the derivation graph: separate `checks.<system>.<name>` or package/check derivations can run independently, whereas one derivation running `cargo test --workspace` cannot be subdivided by Nix. This makes crate-level or suite-level checks the useful practical boundary; overly fine derivations increase evaluation, transfer, and scheduling overhead. [Nix distributed builds](https://nix.dev/manual/nix/latest/advanced-topics/distributed-builds) [Flake checks schema](https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-flake-check)

2. **Remote execution and binary substitution are complementary, not interchangeable.** A remote builder executes a cache miss; a binary cache serves a previously built store path without executing it. `builders-use-substitutes` allows remote builders to fetch dependencies from substituters rather than receiving everything from the client. A trusted signed shared cache improves reuse across laptops and agents, while the trust/signing model must be configured deliberately. [Nix configuration reference](https://nix.dev/manual/nix/latest/command-ref/conf-file) [Binary cache guide](https://nix.dev/manual/nix/latest/package-management/binary-cache)

3. **A normal remote `nix build` still materializes the requested result locally.** Remote build outputs are copied into the local Nix store. The default `result` symlink is a local GC root; `--no-link` avoids creating that root but does not turn the operation into “leave all outputs remote.” `--out-link` changes the symlink name/location. Thus large outputs can still impose return-transfer and laptop-storage costs. For “status only” test workloads, make the successful check output tiny; publish reusable build artifacts to the cache separately. [nix build options](https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-build) [Garbage-collector roots](https://nix.dev/manual/nix/latest/package-management/garbage-collector-roots)

4. **Nix cache reuse across small source edits depends on derivation structure.** Store identities are input-addressed. If a derivation consumes a repository-wide source snapshot, any included-file edit changes that input and usually invalidates its output, even when Cargo would have rebuilt only one crate. Split sources/derivations by stable boundaries, use dependency artifacts from fixed lock/vendor inputs where feasible, and avoid including irrelevant files. Nix then gives strong reproducibility and cross-agent reuse, but it is not inherently an incremental Rust compiler cache. [Nix store model](https://nix.dev/manual/nix/latest/store/store-object/content-address)

5. **Clean source transport has two robust modes, with different feedback latency.**
   - For interactive local commands, let Nix copy the evaluated source/store inputs directly to remote builders. No branch push is needed, and work-in-progress can be tested, but Git-backed flakes only include files visible to Git; untracked files are a common surprise. A path input has different cleanliness/reproducibility characteristics.
   - For durable asynchronous jobs, create a Jujutsu change/commit, move a per-agent bookmark, and `jj git push --bookmark …`; trigger CI against the immutable commit ID. Jujutsu changes can be rewritten, so remote systems should report both Git commit and change/bookmark identity, and agents should use distinct bookmarks to avoid races. `jj git fetch`/`push` provide the Git bridge; colocated repositories keep Git tooling available. [Jujutsu Git compatibility](https://jj-vcs.github.io/jj/latest/git-compatibility/) [Jujutsu bookmarks](https://jj-vcs.github.io/jj/latest/bookmarks/) [Nix flake Git inputs](https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-flake)

6. **`sccache` is primarily compilation caching; its distributed mode does not remotely execute tests.** As a `RUSTC_WRAPPER`, sccache stores compiler outputs in local or cloud storage. This can significantly reuse unchanged crate compilations among clean workspaces, subject to matching compiler flags/toolchain and cacheability. Its distributed mode sends compilation jobs to scheduler-managed build servers, but subsequent linking, build scripts that are not cacheable, and `cargo test` process execution remain with the client unless separately offloaded. Shared-cache credentials, eviction, scheduler availability, and cache poisoning/trust are operational concerns. [sccache README](https://github.com/mozilla/sccache) [Distributed sccache](https://github.com/mozilla/sccache/blob/main/docs/DistributedQuickstart.md)

7. **Bazel remote execution is the strongest fine-grained option, but a migration rather than a toggle.** Bazel's Remote Execution API can execute declared actions remotely and its remote cache reuses action results; `rules_rust` models Rust compilation and tests in Bazel's graph. This offers better action-level reuse, remote test execution, platform isolation, and concurrency than a repository-wide Nix derivation. Costs include BUILD metadata, Cargo/build-script/proc-macro integration work, hermetic toolchains, an execution backend, and debugging two build models if Cargo remains canonical. It fits large, long-lived, many-agent repositories when build latency pays back the migration, not a small team seeking a quick offload. [Bazel remote execution overview](https://bazel.build/remote/rbe) [Remote Execution API](https://github.com/bazelbuild/remote-apis) [rules_rust](https://bazelbuild.github.io/rules_rust/)

8. **Hosted CI and self-hosted runners truly execute tests remotely, but feedback is normally branch/queue oriented.** GitHub Actions supports hosted and self-hosted runners, matrices, concurrency controls, caches, and artifacts. Self-hosted runners provide hardware locality and toolchain control, but GitHub warns that they are not clean ephemeral VMs by default; autoscaled ephemeral runners reduce cross-job contamination. Buildkite similarly supplies orchestration while agents run on customer infrastructure. These systems give excellent audit trails (commit, job, logs, artifacts) and scale-out, but push/webhook/checkout/queue startup is usually slower than a persistent remote builder for sub-minute iterations. [GitHub self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) [GitHub cache dependency docs](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows) [Buildkite agents](https://buildkite.com/docs/agent/v3)

9. **Hosted Nix builders can reduce operations but should be evaluated as vendors, not as a new execution primitive.** Services such as Depot expose remote Nix builds and cache infrastructure, potentially eliminating builder-pool management and improving warm-cache performance. The semantic limits remain: derivation granularity, source-sensitive hashes, and result transfer. Measure cold and warm latency with the actual repository, region, concurrency, and trust requirements; vendor benchmarks are not independent evidence. [Depot Nix builds documentation](https://depot.dev/docs/nix/overview)

10. **Public evidence about coding-agent teams supports isolated remote environments more strongly than any single Rust build stack.** Cursor documents Background Agents running in isolated remote Ubuntu machines, GitHub Codespaces provides per-repository cloud development environments, and OpenAI Codex cloud tasks run in isolated environments against repositories. These are direct evidence that agent products use remote isolated workspaces, but public documentation does not establish that their Rust workloads use Nix remote builders, sccache distributed, or Bazel. Claims about “what coding-agent teams actually use” beyond the documented environment architecture should therefore be treated as unattributed anecdotes. [Cursor Background Agents](https://docs.cursor.com/background-agent) [GitHub Codespaces overview](https://docs.github.com/en/codespaces/overview) [OpenAI Codex cloud](https://developers.openai.com/codex/cloud)

## Comparative evaluation

| Option | Compilation off laptop | Tests off laptop | Warm small-edit latency | Cross-agent reuse | Setup/operations | Isolation and attribution | Many-agent fit |
|---|---:|---:|---|---|---|---|---|
| Nix remote builders + cache | Yes | Yes, per derivation | Good when derivations/caches hit; source-wide misses can hurt | Strong for identical store paths | Medium | Strong derivation isolation; logs need agent/change metadata | Strong with pool limits and per-agent jobs |
| Shared `sccache` only | Cache hit avoids compile; distributed mode executes compile remotely | No | Often excellent for unchanged crates | Strong if toolchains/flags match | Low–medium; distributed mode medium–high | Weaker action provenance unless logs added | Strong cache, scheduler capacity required |
| Bazel + `rules_rust` + RBE | Yes | Yes | Potentially best action-level reuse | Strong | Very high migration and backend cost | Strong declared-action provenance | Excellent at scale |
| Hosted CI | Yes | Yes | Fair–poor for tight loops due to queue/startup | Good with explicit caches | Low | Excellent commit/job audit trail | Good, bounded by quotas/cost |
| Ephemeral self-hosted runners | Yes | Yes | Fair–good if prewarmed/autoscaled | Good with shared cache | High | Strong if one job/VM; maintain metadata | Excellent if operated well |
| Remote dev VM/background agent | Yes, because workspace itself is remote | Yes | Excellent after warm-up, network/editor dependent | Per-VM unless shared cache | Low as SaaS, medium self-hosted | Strong VM boundary; product-dependent audit | Good, with cost/idle lifecycle controls |

## Concrete recommendations

1. **Default architecture:** run a persistent, autoscaled Linux Nix builder pool near a signed shared cache. Configure builders to use substituters. Keep laptop concurrency low so work is scheduled remotely; retain a local fallback only deliberately.
2. **Design test boundaries explicitly:** expose formatting/lints, unit tests by crate or coherent group, integration suites, and expensive end-to-end tests as separate flake checks/derivations. Avoid one workspace-wide check, but do not create thousands of tiny derivations. A useful target is independently cacheable jobs lasting roughly tens of seconds to several minutes.
3. **Use two source workflows:** direct Nix input transfer for immediate WIP feedback; immutable pushed Git commits on per-agent Jujutsu bookmarks for CI, review, retry, and attribution. Record agent/run ID, `jj` change ID, Git commit, derivation path, builder, and cache hit/miss in results.
4. **Add ordinary shared sccache before distributed sccache** when developers or remote runners repeatedly compile similar Cargo graphs outside Nix. Benchmark hit rate first. Adopt distributed compilation only if compilation, rather than linking/tests/queueing, dominates.
5. **Keep acceptance tests remote and authoritative.** Compiler caching alone must never be reported as remote testing. Use Nix check derivations or CI/RBE jobs for the actual test processes and return compact logs/status.
6. **Consider Bazel/RBE only after measurement:** choose it when many concurrent agents, a large monorepo, and poor Nix/source-level incremental reuse justify owning a second build graph. Run a representative crate/test pilot and compare p50/p95 edit-to-result, cache hit rate, and engineer maintenance time.
7. **Operational controls:** use ephemeral credentials, signed caches, untrusted-PR isolation, per-agent quotas, cancellation of superseded commits, timeouts, and separate trusted release builders. Prewarm toolchains/dependencies and locate builders/cache together.

## Measurement plan

Evaluate candidates on the same change corpus: no-op rebuild, one Rust function edit, public API edit, `Cargo.lock` change, build-script change, and integration-test-only edit. Capture p50/p95 queue time, input upload, compile, link, test, result download, cache hit rate/bytes, CPU-minutes, and cost. Run at 1, 10, and expected peak concurrent agents; distinguish compile-cache hits, Nix substitutions, and tests actually executed.

## Sources

- Kept: [Nix distributed builds](https://nix.dev/manual/nix/latest/advanced-topics/distributed-builds) — primary execution and scheduling semantics.
- Kept: [Nix binary caches](https://nix.dev/manual/nix/latest/package-management/binary-cache) and [nix build](https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-build) — substitution, result, and out-link behavior.
- Kept: [Jujutsu documentation](https://jj-vcs.github.io/jj/latest/) — authoritative Git/bookmark workflow.
- Kept: [sccache](https://github.com/mozilla/sccache) — upstream distinction between caching and distributed compilation.
- Kept: [Bazel RBE](https://bazel.build/remote/rbe), [Remote APIs](https://github.com/bazelbuild/remote-apis), and [rules_rust](https://bazelbuild.github.io/rules_rust/) — primary remote action/test mechanism.
- Kept: GitHub, Buildkite, Cursor, Codespaces, OpenAI Codex, and Depot documentation linked above — direct product capability evidence.
- Dropped: vendor benchmark/blog claims — workloads and attribution are insufficiently comparable.
- Dropped: forum anecdotes about coding-agent infrastructure — not authoritative enough to answer actual adoption.

## Gaps and residual risks

- **Evidence limitation:** this worker runtime provided no web-search or HTTP-fetch capability. Primary URLs are known documentation targets but were not live-verified on 2026-07-11; product details and URL paths should be checked before a procurement decision.
- There is little public, independently verifiable evidence naming the build/test substrate used by Rust-specific coding-agent teams. Remote isolated workspaces are documented; the underlying compiler/test architecture generally is not.
- Actual performance is topology- and repository-dependent. In particular, Nix source filtering/derivation design, Rust build scripts, proc macros, link time, cache locality, and output size can reverse generic rankings.
- Shared caches and remote execution enlarge the trust boundary. Untrusted contributions must not write artifacts consumed by trusted release jobs without policy separation.
- Nix check splitting can duplicate compilation unless derivations share explicit build outputs or a cache; benchmark the graph rather than assuming finer granularity is free.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Research findings, recommendations, source links, and severity-tagged residual risks are recorded in /home/li/primary/.pi-subagents/artifacts/outputs/ff37554a-5d4f-41e7-90a7-b76884511749/research.md."
    }
  ],
  "changedFiles": [
    "/home/li/primary/.pi-subagents/artifacts/progress/ff37554a-5d4f-41e7-90a7-b76884511749/progress.md",
    "/home/li/primary/.pi-subagents/artifacts/outputs/ff37554a-5d4f-41e7-90a7-b76884511749/research.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Report distinguishes compiler caching, distributed compilation, binary substitution, and remote test execution.",
    "Report includes concrete recommendations, comparative criteria, primary-source links, adoption-evidence limits, and residual risks."
  ],
  "residualRisks": [
    "medium: source URLs and current product behavior could not be live-verified because this worker had no web/HTTP tool",
    "medium: real latency and cache reuse require repository-specific concurrent benchmarks",
    "high: cache trust and untrusted-code isolation require explicit security design",
    "low: public evidence for Rust-specific coding-agent team adoption remains sparse"
  ],
  "noStagedFiles": true,
  "diffSummary": "Added the requested research artifact and progress record; no implementation or repository source changes.",
  "reviewFindings": [
    "no blockers",
    "medium: /home/li/primary/.pi-subagents/artifacts/outputs/ff37554a-5d4f-41e7-90a7-b76884511749/research.md - primary links were not live-verified in this runtime",
    "high: operational design - do not allow untrusted jobs to populate a cache used by trusted release builds without separation and signing policy"
  ],
  "manualNotes": "No implementation was performed. Validate current documentation links and run the proposed workload benchmark before selecting infrastructure."
}
```
