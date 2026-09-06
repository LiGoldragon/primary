# Review-only authored-skill patch

## Scope

This is a review artifact, not an authored-skill change. It proposes scoped updates to the Curriculum sources below and does not edit them, regenerate instruction trees, mutate a Primary checkout, or advance a bookmark. The concrete unified diff is [authored-skill-review.patch](authored-skill-review.patch).

The correction replaces the earlier incorrect generalization that every payload variant has a braced body. Current Datom delegates a variant-to-variant payload with a unary dotted path: `Query.ByNode.{ ... }` and `Deploy.Host.{ ... }`. Braces represent the delegated product body. A scalar unary payload uses its own dotted form, such as `SecretsDirectory./absolute/path`.

## Authored sources frozen for this review

| Source | SHA-256 |
| --- | --- |
| `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md` | `2f32f2db5e7cc53375170354458ca840a5415f560b77f4b1939d71d2f1bf518d` |
| `/git/github.com/LiGoldragon/Curriculum/skills/file-editing.md` | `e105f5320aa5853a26cec1d15141413bde5f9c55912017a8197eb41f0b5fe838` |
| `flows/542442/reports/authored-skill-review.patch` | `72a8a49cc4af74a0b8c5ea8aaa5e211ead17ca88bc6aafbf92f0c693ea5cb604` |

The patch applies cleanly in a disposable copy of those two sources with `patch --dry-run -p1`. It changes only `skills/lojix.md` and `skills/file-editing.md` in its labels. It is not applied anywhere.

## Implementation sources used to validate the proposal

| Component | Immutable revision | Source evidence |
| --- | --- | --- |
| Lojix | `7e29c37f51092e5a20abf88c670aabd2acee6e52` | `/home/li/wt/github.com/LiGoldragon/lojix/lojix-datom-horizon-542442` |
| ordinary Signal | `5ce3f11feac22a0ddbed028dec2a60385f77fa55` | `/home/li/wt/github.com/LiGoldragon/signal-lojix/signal-lojix-datom-542442` |
| owner Signal | `55c1df20ddfa6ae99e0f4bca57b803bf366b781f` | `/home/li/wt/github.com/LiGoldragon/meta-signal-lojix/meta-signal-lojix-datom-542442` |

The Lojix ingress source is `ethos/ingress.ethos` (`0d57d8b5c5750263df6b9d7a9bd2a063ee2de1fb42992d34894efc9e998b0878`). The syntax witnesses are `tests/bootstrap.rs` (`6d356dcb9efad299cbb9e3640d776953e9512989f17e346bcac721aa1678a2b2`), `tests/store_inspection.rs` (`4b6c646ef1842d0e29e3bd1217ccd469d1cff546e53a745e3c61a17335c86433`), and `tests/write_configuration.rs` (`a20a6fb529930300f73693e96c811794c83298c5fc1bc25c054387b29f3f1484`).

The ordinary Signal schema is `ethos/lib.ethos` (`c0c4f74622ad7fae2027527da6a687032d56c17a0bd8ed856c7026c1b18b7572`) and its binding is in `src/lib.rs` (`55fa4841d78fecd6a32127afa02a5ef91937d00db8312d75a1e8ed85d779bc66`): contract 5, revision 4. The owner schema is `ethos/lib.ethos` (`eabd3d142cc5477c013fc4603ace205c83b68d86c7839905d99245e437da9c08`) and its binding is in `src/lib.rs` (`0f7242a065fc3cefb4710e7a82a87242814296f40c4b42b88500e119dc80b6b2`): contract 6, revision 3.

## Exact decoder validation

Focused contract suites passed without changing source:

```text
signal-lojix: cargo test --test contract                 3 passed
meta-signal-lojix: cargo test --test contract            2 passed
lojix: cargo test --test bootstrap --test store_inspection --test write_configuration
                                                        21 passed
```

An isolated temporary Rust harness invoked the exact public decoders, without calling `run` or opening a socket. It accepted all of the following current forms:

```text
Query.ByNode.{ fieldlab mercury None }
WatchDeployments.{ None None None }
WatchCacheRetention.{ None None }
Pin.{ fieldlab mercury 42 keep }
Deploy.Host.{ fieldlab mercury CompleteHost /tmp/horizon-definition.datom NoSecrets github:owner/repository?rev=0123456789abcdef0123456789abcdef01234567 { ssh-ng://root@mercury root@mercury } Horizon { nixosConfigurations.mercury.config.system.build.toplevel } NixosSystemdBootV1 Evaluate RequireImmutable None [] }
BootstrapRun.{ request BuildOnly.{ Direct.{ github:owner/repository/0123456789abcdef0123456789abcdef01234567 x86_64-linux nixosConfigurations.mercury.config.system.build.toplevel } NoBuilder /tmp/journal /tmp/root /tmp/evidence } }
BootstrapRun.{ request BuildOnly.{ Horizon.{ /tmp/horizon-definition.datom fieldlab mercury CompleteHost SecretsDirectory./tmp/secrets github:owner/repository/0123456789abcdef0123456789abcdef01234567 x86_64-linux nixosConfigurations.mercury.config.system.build.toplevel } NixBuilder.builder /tmp/journal /tmp/root /tmp/evidence } }
InspectStore.{ /tmp/lojix-v5.sema }
ResetStore
```

The full `Deploy.Host` line above is explicitly a **decoder-only** witness: `MetaClient::from_arguments` establishes current typed Datom structure and does not open a socket or prove daemon admission. The `RequireImmutable` admission test separately passed for the displayed query-revision source `github:owner/repository?rev=<40-lowercase-hex>`. Bootstrap deliberately retains its distinct slash-revision form.

The Horizon bootstrap request in that harness used unary `NixBuilder.builder`; it decoded successfully; the same decoder rejected `NixBuilder.{ builder }`. The patch therefore names `NixBuilder.<builder-spec>`.

Separate isolated generated-response decoders accepted `Watching.{ 9 12 }`, `WatchRejected.{ MalformedWatch }`, and `DeployAccepted.{ 13 { 263 263 } }`. The current writer binary accepted the proposed braced `ConfigurationWriteRequest.{ ... }` form and wrote a nonempty archive to a temporary path. No daemon, deploy socket, or live configuration was used.

## Proposed Lojix wording

The diff is deliberately scoped. It retains existing ordinary/owner request lists, watch success and rejection guidance, routing, action, reply, deployment, placement, and direct/remote/bootstrap guidance unless the current contract changed that statement. It replaces only stale Dotos grammar and old parenthesized examples; updates the deployment field order with explicit `SecretsInput`; changes the public source to `horizon-definition.datom`; replaces the v4-current-store block; and adds the current Horizon bootstrap shape without dropping the direct shape.

Examples with angle-bracket values are explicitly labelled schematic field-order forms. They establish generated field order only and are not pasteable deployment requests. Decoder-witnessed examples contain concrete non-live fixture values.

`SecretsInput` is separate caller-owned authority after `ProposalSource`: bare `NoSecrets` or unary `SecretsDirectory./absolute/path`. It is never part of the public Horizon artifact. The artifact is one absolute regular non-symlink `horizon-definition.datom`; Lojix resolves its selected `(cluster, node)` and performs no catalog, sibling, or secret discovery.

The durable-store wording describes a non-destructive v5 cutover: retain the v4 store at its old path and use a distinct new v5 `store_path`. It does not invent a `NoSecrets` mapping. The only retained-v4 full-history reader is Lojix `0.20.3` at `46585a2c8303bffe885b1722bfebd97d5353ca17`, invoked exactly as:

```sh
lojix-inspect-store '(InspectStore <absolute-v4-store-path>)'
```

The v5 `InspectStore.{ <absolute-v5-store-path> }` interface is incompatible with v4 jobs and history. The v5 reset command is bare `ResetStore`.

The bootstrap replacement retains the direct form and makes the exact immutable bootstrap reference explicit: `github:<owner>/<repo>/<40-lowercase-hex-revision>`. Query, branch, tag, and other mutable forms are rejected. The Horizon `BuildOnly` form materializes explicit `system`, `horizon`, `deployment`, and `secrets` inputs and has no transport or activation field. Direct `BuildOnly` remains supported and does not imply that Horizon composition path.

## File-editing guard

The patch follows the authored `main-feature-integration` source: “Integrate from current main on the assigned integration branch. Test affected branches together. Land portable producers before consumers.” It adds a guard only for consumer integration: a consumer may not advance `main` until its assigned integration branch contains affected producer and consumer revisions and their combined required checks pass. Independently tested portable producers may land after their own required contract and package checks before consumer integration.

## Rationale

The prior skill directed operators to removed Dotos ingress, parenthesized payload forms, `proposal.datom`, and a v4-current-store model. Those instructions would now produce rejected input or risk an unsafe durable-store interpretation. The revised patch corrects the actual generated grammar while preserving guidance that the source has not changed.
