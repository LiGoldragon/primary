# Specialized subflow roles

Status: proposed `curriculum-deploy` role-prompt compiler. It does not authorize implementation or a production launch.

## The compilation boundary

`curriculum-deploy` compiles the role's selected skill text, standing repository paths, allowed commands, lock procedure, capability boundary, and required result shape into one role system prompt. It also binds inherited accounting identity and the trusted caller/process linkage known at launch. The native invocation loads no skill and carries no procedure, repository path, lock name, hash, cursor, capability, or caller bookkeeping. It carries only the role's small task data.

The compiler refuses a missing, duplicate, unreadable, or source-hash-mismatched standing skill before launch. Model choice intersects the role's eligible configured models with caller-authorized model, effort, and execution constraints; it must not silently replace or relax those constraints to choose a cheaper model. A future trusted launcher enforces its compiled grants and authenticates hook/CLI callers from recorded process instance, PID/start time, Capsule association where present, and native thread/session. `FLOW_ID` is accounting only. It never authorizes a caller, recipient, role, command, or result.

This is future enforcement. Existing role instructions remain usable now and do not wait for the Capsule or compiler: current Flow composition already accepts a chosen skill vector and native worker launch explicitly resolves named skills ([composition.rs](/home/li/primary/flow/crates/flow-nexus/src/composition.rs:360), [native-worker-launch.mjs](/home/li/primary/tools/native-worker-launch.mjs:40)).

## Compiled roles and caller briefs

### Messenger

The compiled prompt contains `subflow`, `knowledge-flow`, and `compensation-messenger-clj`; the exact messenger command; recipient voice resolution; the bound-destination receipt requirement; and the returned receipt shape. General routing is guidance, with a rare reasoned exception, not a transport prohibition. Operational messages remain available to ordinary recipients.

The caller sends only:

```text
Messenger.{ <target> <body> }
```

The dispatcher resolves `<target>` to one exact bound destination and records that binding. The native command sends exactly `<body>`. Result contains bound destination, body digest, outcome, and original command receipt.

Fable `9fb0ad` alone has an additional recipient-relevance rule in its compiled prompt: a living question, a recipient-requested result, or `#psyche` material is admitted; operational noise is not. A body cannot self-authorize as requested. The compiled dispatcher checks the living-input record, request provenance, or configured `#psyche` route.

### Publisher

The compiled prompt contains `subflow`, `compensation-primary-commit`, the caller's owned Primary-lane rule, the `PrimaryPublish` procedure, exact hash/baseline computation, conflict stop, result receipt, and release procedure. Publisher is not a generic page publisher.

The caller sends only an optional description:

```text
Publisher.{ «Clarify specialized roles» }
```

The compiler derives the caller's lane and computes path/content hashes and remote baseline. It acquires `PrimaryPublish`, publishes only those paths through the existing compensation, and stops on a content or baseline conflict. It returns original, copy, remote, and release receipts. None of these paths, hashes, lock facts, or command arguments are caller task fields.

### Book

The compiled prompt includes `subflow`, `psyche`, `psyche-distillation`, `vocabulary`, transcript retrieval, artifact creation, presentation rules, and a returned artifact receipt. Book creates one fresh presentation/new artifact from the caller's transcript for the supplied title. It does not reuse or update page rows. It has no messenger, Primary publication, lock, launch, or general filesystem-write grant.

The caller sends only:

```text
Book.{ «Flow roles» }
```

The title identifies the requested subject. The compiler derives caller transcript session and source cursor, then creates the new artifact. Result returns title, source-through cursor, artifact identity/receipt, and outcome. The presently deployed page-updating Book remains an interim instruction path; this is the corrected target role contract.

### Read-only Witness

The compiled prompt contains `subflow`, `behavior`, its trusted authorized-context resolver, the declared evidence result form, and a read-only boundary. It cannot launch, send, publish, lock, mutate, read sibling paths, or use a reported Flow ID as authority.

The caller sends only:

```text
Witness.{ «Does the role compiler inject the required skill text?» }
```

The compiler derives authorized sources from the authenticated caller/context rather than accepting a caller path list. Result returns the question, sources read, findings, evidence locations, and whether each finding is observation or inference.

### LockWatch

The compiled prompt would contain `subflow`, the subscribed lock condition, and the rule to hold one event connection and return ordered observations or closure. The caller sends only:

```text
LockWatch.{ «PrimaryPublish released» }
```

LockWatch remains unavailable. The installed `orchestrate` CLI reads one observation and exits; repeating it is polling. A real subscription-capable client is required before this role can run.

## Static prompt-token estimates

These are static estimates for a proposed Codex-facing compiled system prompt, not trial usage, billing, or an actual-cost claim. A disposable `/tmp` virtual environment installed `tiktoken`; it used `o200k_base` to encode the complete fixture text and was removed after the measurement. `o200k_base` is the available tokenizer choice, not proof that every eventual selected role model uses that encoding.

Each fixture contains the inherited base separately from the complete standing skill files and a short role frame. The inherited base is the four current `roles.datom` module bodies: general instructions, spirit, intent, and Codex skill-loading. Standing skill text is read in full, including frontmatter, from Curriculum revision `ee00dc8d6a393dcaa26eb48cdcbabff1bf718e66`; the selected file hashes are retained in the measurement record below. The caller brief is deliberately excluded from the standing total because it is a small per-invocation value.

| Role | Complete standing skills | Base tokens | Standing tokens | Role-frame tokens | Combined static tokens |
| --- | --- | ---: | ---: | ---: | ---: |
| Messenger | `subflow`, `knowledge-flow`, `compensation-messenger-clj` | 92 | 1,149 | 22 | 1,263 |
| Publisher | `subflow`, `compensation-primary-commit` | 92 | 469 | 39 | 600 |
| Book | `subflow`, `psyche`, `psyche-distillation`, `vocabulary` | 92 | 2,082 | 30 | 2,204 |
| Witness | `subflow`, `behavior` | 92 | 388 | 24 | 504 |
| LockWatch | `subflow`, `orchestrate` | 92 | 565 | 32 | 689 |

The role frames used only the role's standing instruction summarized above: Messenger resolves/sends and returns bound receipt; Publisher commits the caller lane and stops on conflict; Book derives transcript/page cursor; Witness derives authorized context; LockWatch would subscribe without polling. They are part of the proposed compiler output, not currently generated artifacts.

Measurement method: `tiktoken 0.12.0`, `get_encoding("o200k_base")`, exact UTF-8 source text, no provider call and no harness launch. The compiler, selected runtime model, provider prompt serialization, tool schema, harness base, and caller brief were not available as a compiled artifact. These figures therefore do not establish billable input cost, cached-input cost, cache-write cost, output cost, or context occupancy.

Actual Codex rollout records can separately report `input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, and `reasoning_output_tokens`. Static tokenization cannot predict those fields: cache reads/writes depend on the provider and prefix reuse, output depends on the response, and a selected model may have another tokenizer. No historic usage number is reused as a role-prompt measurement.

The supported cheap isolated trial located is `tools/third-seat/refusal-dry-run.mjs`: it runs OpenCode against a temporary loopback server that always returns 503. It proves isolation/refusal plumbing only; it cannot run `curriculum-deploy` or emit role-prompt usage. `native-worker-launch.mjs` starts a real Codex worker through its supplied app-server socket and is not an isolated no-provider token trial. The remaining blocker to an actual cheap-role trial is the unimplemented compiler/system-prompt injection path. An authorized later trial needs that compiled artifact, a selected model, and a harness/provider that records input, cached/cache-write, output, and reasoning-output usage separately.

Measurement source hashes: `subflow` `9cbc5ca0ba1600c47f8c8258d8b9befa2cb41d883b6e66dd8eaa4369a34db977`; `knowledge-flow` `cf2f7991263bc899131f09e895ed62f9a7f324d21e309e1b91cb90f2f3c22e21`; `compensation-messenger-clj` `5326640892c347ccc2f52b45de3a213d57b1e628daab860d611330e812d79112`; `compensation-primary-commit` `3941641f6f297ff8b90e00251fef91dca60ff0c23fd3721f0db26212e85fce88`; `psyche` `dd28a3c2cfa34eadecbb2f85ba7cb0decc26bb0ab8bce3602e0784c7d538befb`; `psyche-distillation` `10ad8942a957f87385ced9e1d7e1344099abb1187ffb29f2e04c74d2f32e6fdd`; `vocabulary` `60a796008525e56e188037f0f7ee1cae200b90d16b12d6bfc893252421a8a821`; `behavior` `08fed16c6cc10610c3cbf9e31d2069ef5dd9725a7a4aab7902ccbe9e751424b5`; `orchestrate` `ee05c9a4f9f4b6be018dd7098dccac91875f8d4bdbf819efcc5b7289c1379252`.
