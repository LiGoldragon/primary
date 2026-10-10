# Spirit deployment fixture fix — witness

## Method

Independent re-derivation from the immutable pinned agent contract and the
untouched Home consumer source, then a targeted two-line edit to
`checks/spirit-deployment/default.nix` (the only file in scope), verified by
manual trace of all three exercised code paths (real positive case via the
product's own `agentDaemonConfiguration` derivation, and the two hardcoded
negative fixtures already in the file). No Nix eval, build, check, or
activation was run; no secret value was read or written; the Orchestrate lock
was only observed, never seized.

## Preconditions checked before editing

1. Skills loaded (receipts): `subflow`, `nix-workflow`, `testing`, `orchestrate`,
   `flow-evidence`.
2. Base revision: workspace at
   `/home/li/wt/github.com/LiGoldragon/CriomOS-home/spirit-deployment-fixture-6fe957`
   was at Home commit `2fdfdf29f69419f7f3bf23b3e2dbc643f28e3d84`
   ("Home: match current ProviderSeed fixture contract") on bookmark
   `spirit-deployment-provider-seed-fixture-6fe957`, parent `f368ed706e47b61495324142e60219a518b5b8a2`
   ("Home: register solar and active network Noctalia plugins") — matches the
   brief's stated base exactly. The bookmark and `@origin` coincide with this
   commit; no later successor was found, so this base was used as-is.
3. Orchestrate lock 8189 read-only check via `orchestrate 'Observe.Locks'`:
   confirmed `{ 8189 SpiritDeploymentFixtureProposal 6fe957 [ /git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix /git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix ] «Reserve exact Home fixture and consumer paths for minimal ProviderSeed matcher correction» }`
   — holder and both paths match the brief exactly. Not seized, released, or
   reacquired.
4. Independent re-verification of the three evidence items (own inspection,
   not taken on faith):
   - (a) Agent repo at `/git/github.com/LiGoldragon/agent` (a git checkout),
     commit `3a3534931be790e63d3db01bbd238ad044b2d35f` confirmed to exist
     (`git cat-file -e`). `tests/configuration_writer.rs` at that revision
     builds its request via
     `format!("AgentConfigurationWriteRequest.{{{} {} 384 {} [ProviderSeed.{{... Gopass.platform.deepseek.com/api-key}}] {}}}", ...)`
     — the bare, unbraced `Gopass.platform.deepseek.com/api-key` form, ending
     the whole request in a single `}` right after the output path with no
     intervening space. This is source construction of the agent's own test
     contract, not proof of an executed passing test (no Nix build/test was
     run to confirm it currently passes).
   - (b) `flake.lock` at the base commit: `nodes.agent.locked.rev` =
     `3a3534931be790e63d3db01bbd238ad044b2d35f`, `type: github`,
     `owner: LiGoldragon`, `repo: agent` — matches the pinned agent revision
     from (a) exactly.
   - (c) `modules/home/profiles/min/spirit.nix` at the base commit, line 75:
     `"AgentConfigurationWriteRequest.{${agentSocketPath} ${agentMetaSocketPath} 384 ${agentDatabasePath} [ProviderSeed.{${providerName} ${providerEndpoint} ${defaultModel} Gopass.${providerGopassPath}}] $out/${agentConfigurationPath}}"`
     with `providerGopassPath = "platform.deepseek.com/api-key"` (line 40) —
     confirms the unbraced `Gopass.${providerGopassPath}` interpolation
     producing the bare canonical form, and confirms the whole request ends
     in exactly one `}` immediately after the output path (no trailing
     space).

All three checks passed; no discrepancy found, so no stop was warranted.

## Coordinator refinement (Mind Astra 6fe957) addressed

Mid-task, a refinement arrived tightening item (B): `output_path` (from
`${request##* }`) already contains a trailing `}`; the fix is to strip
exactly one trailing `}` from that suffix, then reconstruct `expected` from
the stripped value plus the canonical bare Gopass form. My own independent
trace of the immutable fake-agent script (below) converged on exactly this
mechanism before I read the refinement — no discrepancy to report.

## Mechanism traced (why the fix is exactly this)

The mock `agent-write-configuration` script (defined entirely inside the
in-scope file, standing in for the real pinned agent binary) computes:

    output_path=${request##* }

`${request##* }` strips everything up to and including the last space,
i.e. it takes the request's last whitespace-delimited token. Because the
real request (built by the untouched `spirit.nix`) ends in
`... $out/agent.config.rkyv}` — the output path immediately followed by the
single closing `}` of the outer `AgentConfigurationWriteRequest.{...}`, with
no space before that `}` — the extracted `output_path` is actually
`<real-path>}`, i.e. it already carries the outer closing delimiter fused
onto the end of the path.

The old `expected=` line then appended *another* literal `}` right after
`$output_path`, so `expected` ended in `...}}"` (two braces) while any real
request from the untouched product code ends in only one. That mismatch is
exactly why the check's positive case (exercised implicitly at build time
through `agentDaemonConfiguration` in `spirit.nix`, which invokes the real
writer with the real request and requires `test -s "$out/agent.config.rkyv"`
to succeed) could never pass: the file would have been written to
`<real-path>}` — a path with a stray `}` in its name — not to the real
`$out/agent.config.rkyv`, and even ignoring the write target, the `test
"$request" = "$expected"` equality itself required the impossible extra
brace.

## Fix applied (diff)

Only `checks/spirit-deployment/default.nix` was touched, two lines changed:

```diff
diff --git a/checks/spirit-deployment/default.nix b/checks/spirit-deployment/default.nix
index 22b369d4e5..b705da6dfb 100644
--- a/checks/spirit-deployment/default.nix
+++ b/checks/spirit-deployment/default.nix
@@ -41,7 +41,8 @@
         *'LOCAL_LLM_API_KEY'* | *'goldragon.criome/local-llm-api-token'*) exit 64 ;;
       esac
       output_path=''${request##* }
-      expected="AgentConfigurationWriteRequest.{/home/li/.local/state/agent/agent.sock /home/li/.local/state/agent/agent-meta.sock 384 /home/li/.local/state/agent/agent.sema [ProviderSeed.{deepseek https://api.deepseek.com/v1 deepseek-v4-flash Gopass.{platform.deepseek.com/api-key}}] $output_path}"
+      output_path=''${output_path%\}}
+      expected="AgentConfigurationWriteRequest.{/home/li/.local/state/agent/agent.sock /home/li/.local/state/agent/agent-meta.sock 384 /home/li/.local/state/agent/agent.sema [ProviderSeed.{deepseek https://api.deepseek.com/v1 deepseek-v4-flash Gopass.platform.deepseek.com/api-key}] $output_path}"
       test "$request" = "$expected" || exit 65
       printf 'fake agent configuration archive\n' > "$output_path"
       printf '(AgentConfigurationWritten %s)\n' "$output_path"
```

(A) The braced `Gopass.{platform.deepseek.com/api-key}` form is replaced with
the canonical bare `Gopass.platform.deepseek.com/api-key`, matching the
pinned agent's own test contract (evidence (a)) and the untouched consumer's
unbraced interpolation (evidence (c)).

(B) `output_path` is now re-bound to itself with exactly one trailing `}`
stripped (`${output_path%\}}`, the bash shortest-suffix-match idiom already
used identically elsewhere in this same file at the spirit fixture,
`output_path=${output_path%))}`), before being used both to write the output
file and to reconstruct `expected`. `expected` still appends one literal `}`
after `$output_path`, which now reconstructs the single real trailing brace
instead of doubling it.

## Trace of all three exercised paths after the fix

1. **Real positive case** (implicit, via the untouched `spirit.nix`'s
   `agentDaemonConfiguration` derivation, which calls the real writer with
   the real product-constructed request): request ends in
   `.../agent.config.rkyv}` (single trailing brace, no preceding space).
   `output_path` (raw) = `.../agent.config.rkyv}`; after stripping one
   trailing `}`, `output_path` = `.../agent.config.rkyv` (the correct real
   path, matching `spirit.nix`'s own `test -s "$out/${agentConfigurationPath}"`
   assertion). `expected` reconstructs to
   `...Gopass.platform.deepseek.com/api-key}] .../agent.config.rkyv}` — byte
   identical to the real request. Match succeeds; file is written to the
   correct path. This case was preserved and, by this fix, made able to
   actually succeed for the first time under the bare-form contract.

2. **Old parenthesized-syntax negative** (`old_provider_seed`, hardcoded in
   the file, unedited): still contains the obsolete
   `ProviderSeed (deepseek ... (Gopass platform.deepseek.com/api-key))` shape,
   which cannot equal the dotted/braced `expected` regardless of the brace
   change — `test "$request" = "$expected"` still fails, `exit 65`, no file
   written (`test ! -e "$rejected_archive"` still holds).

3. **Malformed/missing-outer-brace negative** (`malformed_provider_seed`,
   hardcoded, unedited): this request has no trailing `}` at all (it ends
   right after `$rejected_archive`). `output_path%\}` finds no trailing `}`
   to strip, so `output_path` is unchanged (no-op on no match, standard bash
   behavior). `expected` then appends its one literal `}` after
   `$output_path`, producing a string with a trailing `}` that the malformed
   request itself lacks — the two strings still differ, so `test` still
   fails, `exit 65`, no file written. Preserved.

## Explicit confirmations

- No Nix eval, build, check, runtime, service, activation, or Home main move
  was performed at any point.
- No secret value was exposed; only reference/path names were read
  (`platform.deepseek.com/api-key` is a Gopass reference name, never a
  secret value).
- Orchestrate lock 8189 was only observed (`Observe.Locks`), never
  seized/released/reacquired.
- `modules/home/profiles/min/spirit.nix` and no other file was touched;
  only `checks/spirit-deployment/default.nix` was edited.
- No claim is made that the braced parser is invalid beyond this one
  fixture; the fixture's own hardcoded braced-form malformed negative case
  was left as-is and still behaves as a negative.
- No claim of test-green or Field execution is made; this is a source edit
  only, pending the Field's own execution and Home main's own review/merge.

## Sources

- `/home/li/wt/github.com/LiGoldragon/CriomOS-home/spirit-deployment-fixture-6fe957/checks/spirit-deployment/default.nix`
- `/home/li/wt/github.com/LiGoldragon/CriomOS-home/spirit-deployment-fixture-6fe957/modules/home/profiles/min/spirit.nix`
- `/home/li/wt/github.com/LiGoldragon/CriomOS-home/spirit-deployment-fixture-6fe957/flake.lock`
- `/git/github.com/LiGoldragon/agent` commit `3a3534931be790e63d3db01bbd238ad044b2d35f`,
  `tests/configuration_writer.rs`
- `orchestrate 'Observe.Locks'` output, read at task time
