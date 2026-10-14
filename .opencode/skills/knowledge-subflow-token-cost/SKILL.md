---
name: knowledge-subflow-token-cost
description: Verified main-context text comparisons and observed provider token usage for direct reads and predefined subflows, with their measurement limits.
---

A smaller return to the main flow and fewer tokens consumed across all flows are different quantities. A child can keep a large tool result out of the main context while consuming its own instructions, tool schemas, repeated input and output tokens. Text length, provider token usage, cached tokens and monetary cost are also different quantities.

The measurements below were rechecked on 2026-10-13 against the source-addressed Claude and Codex transcripts in the Mind Tools study. They describe selected historical cases, not a population-wide saving rate.

## Five large reads: verified text arithmetic

The study selected five completed main-flow episodes containing a Claude `Read`, its returned text and a final answer. The alternative briefs and concise returns were reconstructed later; they are not observed delegated executions. Their ability to replace the original reads without further questions was not tested.

All counts here are Unicode characters, not model tokens. Direct text is the compact JSON call arguments plus the actual tool result. Candidate text is the reconstructed brief plus return, before additional transport overhead.

| Case | Direct arguments + result | Candidate brief + return | Difference |
|---|---:|---:|---:|
| quota report | 4,027 | 395 | 3,632 |
| census report | 8,939 | 356 | 8,583 |
| model comparison | 3,994 | 453 | 3,541 |
| task summary | 6,826 | 355 | 6,471 |
| topology brief | 9,801 | 413 | 9,388 |
| total | 33,587 | 1,972 | 31,615 |

That construction reduces the selected call/result package by **94.1%**. It does not measure a 94.1% reduction in tokens, the entire main context, total consumption or price. Original arguments totaled 403 characters; proposed briefs totaled 613, an increase of 210 emitted characters. Received results fell from 33,184 characters to 1,359 candidate-return characters. The actual final answers totaled 4,945 characters and were held common to both alternatives. Including that common final text changes the comparison to 38,532 versus 6,917 characters, a reduction of **82.0%**, still before other overhead.

The ten distinct actual provider requests for those direct episodes reported, in total, 20 ordinary input tokens, 2,154,402 cache-read input tokens, 14,570 cache-creation input tokens and 1,728 output tokens. Presented input was 2,168,992 tokens. Most of that was reused prefix context, rather than newly read material. No matched delegated-parent usage was recorded for these five alternatives, so these provider totals do not establish delegation savings.

## Five small reads: overhead changes the comparison

Five further call/result examples had direct packages of 408, 263, 698, 458 and 535 characters. Their reconstructed brief/return packages were 270, 337, 194, 179 and 218. At zero added overhead, four candidate packages were smaller and one larger. Adding 300 parent-side envelope characters made two smaller and three larger; adding 1,000 made all five larger. These are arithmetic sensitivity calculations, not observed transport costs or completed alternative runs. The examples' full user objectives and terminal answers were not established as matched episodes. “Small reads favour direct calls” is therefore not a verified universal finding.

## A real predefined reader's token usage

A fresh-history Codex `read-trivial` child, recorded as `gpt-5.6-luna` at low effort, completed a known-answer file-read task. It read the mandatory worker instructions and setup variables, made one additional environment-inspection command, and returned the two requested transcript-root values in 109 characters. Both commands completed successfully.

| Request | Input tokens | Cached-input subset | Output tokens | Reasoning-output subset |
|---|---:|---:|---:|---:|
| first | 33,374 | 5,888 | 123 | 44 |
| second | 34,334 | 32,512 | 75 | 13 |
| third | 34,432 | 33,536 | 71 | 35 |
| total | 102,140 | 71,936 | 269 | 92 |

The first-request figure is **33.4k input tokens**, not the whole child cost. Its completed turn consumed **102,409 input-plus-output tokens**, with 30,204 input tokens outside the cached-input subset and zero cache-write tokens. Cached input is already included in input; reasoning output is already included in output. Adding those subsets again would double-count them.

The child's recorded injected instruction/environment user text totaled 4,380 characters. That is not the caller's brief. The study separately reconstructed a 126-character task sentence, but the archived spawn-message field is encrypted, so its exact original serialized brief was not independently recoverable. The child's 109-character final result reached the parent in a 194-character completion message: 85 characters of framing, excluding any other transport/notification overhead.

Two parent requests around spawning and handling this probe reported 234,926 input-plus-output tokens. Adding the child's complete usage gives 337,335 for that observed parent/child interval. The parent was also conducting the research study; this is an interval total, not an isolated marginal task cost, a matched direct comparison or proof of savings. Other historical completed-child artifacts recorded 17,304 to 744,296 input-plus-output tokens, for different tasks and configurations; they do not establish a fixed child overhead.

## What the break-even expression measures

With the final answer held common, the study's visible-text comparison defines:

- `C`: direct main call text; `O`: its results; `A`: other avoidable main text.
- `B`: child brief; `R`: returned text; `H`: additional parent-side envelopes, notifications, followups and polling.

Under those definitions, the delegated parent package is smaller exactly when `C + O + A > B + R + H`. This is an accounting identity in the chosen units, not a rule about when to delegate. The verified case tables use characters; applying it to tokens requires token measurements for those same terms and a return that answers the task adequately.

Total reported-token comparison instead includes every parent and child request. If `D` is direct-parent usage, `P` delegated-parent usage and `S` all child usage for equivalent completed tasks, total delegation uses fewer reported tokens exactly when `P + S < D`. The study does not supply matched values of all three for the same task. A universal call-count cutoff, whole-system saving percentage and monetary break-even are not established.

## Evidence and counting

The five large-read windows and the five small-read call/results were independently recounted from their native transcripts and the study's literal candidate strings. The reader probe was checked against three unique Codex response IDs, their per-request usage records, cumulative totals, two completed commands and its terminal result. Claude usage was deduplicated by provider request ID because one request can appear in multiple streamed content records. Codex cumulative snapshots were not summed as independent requests. Exact transcript locations, arithmetic and scoped verification are retained with this module's publication evidence.
