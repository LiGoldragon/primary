# Knowledge sweep: candidates for destruction

## beads


> `-t/--type` — bug, feature, task, epic, chore, decision, spike, story, milestone.

`procedure` — bd flag value list; `bd create --help` carries it. Harm 1.


> `-p/--priority` — 0 highest, 2 default.

`procedure` — bd flag defaults; belongs in bd help. Harm 1.


> `--parent`, `--labels`, `--due`, `--estimate`, `--external-ref`.

`procedure` — bd flag list; belongs in bd help. Harm 1.


> Types: blocks, tracks, related, parent-child, discovered-from, until, caused-by, validates, supersedes.

`procedure` — dependency type list; belongs in bd help. Harm 1.


> `bd reopen`, `bd defer --until`, `bd blocked`, `bd query`.

`procedure` — bd subcommand list; belongs in bd help. Harm 1.


> Use `compensation-secrets` to connect `gopass show -o dolthub.com/api-token` directly to curl’s supported secret-input interface; keep the token out of agent output, arguments, and environment.

`too specific` — names a secret-store path and a curl mechanic; compensation-secrets owns delivery. Harm 2.


> Authenticate `GET https://www.dolthub.com/api/v1alpha1/user` and `POST https://www.dolthub.com/api/v1alpha1/database` with `Authorization: token ...`; send `ownerName`, `repoName`, and `visibility` to create the matching database.

`too specific` — HTTP endpoints and header form of a third-party API; can go stale unnoticed. Harm 2.


> Treat a missing-database read returning `400 no such repository` as absent and a creation response returning `409 already exists` as success.

`too specific` — exact HTTP status strings of a third-party API; unverified, can go stale. Harm 2.


> Configure the canonical Beads remote with `bd dolt remote add`.

`procedure` — a bd subcommand how-to; belongs in bd help. Harm 1.


> Use `compensation-secrets` for PAT and JWK delivery.

`duplicate` — said in compensation-secrets, and in the gopass line above. Harm 1.


> When Dolt needs a missing JWK credential, import it through Dolt’s supported stdin contract.

`procedure` — a Dolt credential how-to; belongs in Dolt help. Harm 1.

Statements: 24 kept vs 11 candidates.

Worth keeping after the candidates go: yes — the lifecycle and store rules (claim, close with proof, never run bd in parallel) are not guessable.

## claude-harness


> Claude Code's top stratum is the system prompt. The
> --system-prompt and --system-prompt-file flags replace the whole
> of it; --append-system-prompt and --append-system-prompt-file add
> to the end of the stock one; an output style rewrites it, layering
> over the coding instructions when it says so; the SDK's system
> prompt setting chooses between the minimal default, the Claude
> Code preset with an optional append, and a custom text.
> --exclude-dynamic-system-prompt-sections moves the per-machine
> sections (working directory, environment, git status) out of the
> system prompt into the first user message. --bare skips CLAUDE.md
> discovery; --safe-mode disables every customization.

`too specific` — per-tool flag and SDK-setting mechanics of one vendor release; unverified, ages with the CLI. Harm 2.


> A skill's frontmatter says who may invoke it.
> `disable-model-invocation: true` withholds it from the model: the name is
> absent from the available-skills listing, and the skill interface refuses
> it. `user-invocable: false` withholds it from the typed command list.

`too specific` — per-tool frontmatter keys and their effects; unverified, ages with the CLI. Harm 2.


> A withheld skill enters through the user prompt. The harness reads a
> leading `/name` from that prompt, expands the skill body itself, and
> delivers it as a middle-stratum message; two records mark the turn, one
> naming the command and one carrying the rest of the prompt as its
> argument. The command is read only at the head of the prompt, and the
> first text that is not a command ends the parse, so a command written
> further down a block stays literal. One block of
> startup text carries a skill only when the command is its first token.

`too specific` — per-tool parse mechanics of leading slash commands; no way given to check. Harm 2.


> A launcher has two other routes into the first turn: a SessionStart hook
> returns `initialUserMessage` or `additionalContext`, or the launcher reads
> the skill file and writes its body into the first prompt.

`too specific` — per-tool hook field names; unverified. Harm 1.


> On 2026-10-09, `claude --version` returned `2.1.294 (Claude Code)`.
> This is an observation of the installed command, not a metaflow binding.

`stale` — a dated version observation; the installed command has moved on or will. Harm 3.


> The native Claude launcher reads generated
> `.claude/skills/<name>/SKILL.md` files, sends bounded leading slash
> requests, and verifies the returned skill bodies against those files.
> Configuration is Flow's datom, read with `flow-meta 'Configuration'`.

`too specific` — launcher internals, generated paths, a flow-meta invocation; unverified. Harm 2.


> Claude Code stops its background tasks when the host's free memory
> looks low, judging by free rather than available memory, so another
> process's build can end a long task that is nowhere near its own
> limit. A long-running process launched from the harness runs
> detached, as a transient systemd user service or scope with its own
> memory cap, and the harness watches for its end.

`unverified` — a claim about harness memory heuristics with no way to check; treated as current fact. Harm 2.

Statements: 4 kept vs 7 candidates.

Worth keeping after the candidates go: yes — what the system-prompt replacement keeps and removes, and that a subflow cannot see withheld skills, are acting facts.

## codex-harness


> Codex's top stratum is the base instructions, sent as the
> instructions field of the Responses API request, above the whole
> input array. The stock text is a per-model template served from
> the backend model catalog and cached locally, with a compiled-in
> default as fallback. The model_instructions_file config key
> replaces the base instructions with a file's text and outranks the
> instructions config key, which replaces them with a string; the
> source discourages both, and we use the file.

`too specific` — per-tool config keys and the API field; unverified, ages with the CLI. Harm 2.


> A Codex session's model and reasoning effort come from
> `~/.codex/config.toml` at launch and change without notice. A
> launcher that must pin a model passes `-m <model> -c
> model_reasoning_effort=<effort>` rather than inheriting them.

`too specific` — config path and CLI flags; belongs in codex help. Harm 2.


> A launcher passes the role's model by family name, never a version number, and `model_reasoning_effort=medium` unless the role declares otherwise.

`not common sense` — a launcher rule stated as a fact about Codex; the launcher already decides it. Harm 1.


> Codex has three strata with a ranking inside the middle: the
> developer role outranks the user role within the input array.
> developer_instructions is a developer-role message sent beside the
> base instructions and never part of them. AGENTS.md files, from
> the Codex home and from the repository root down to the working
> directory, enter as user-role messages under an AGENTS.md
> instructions marker and cannot override base instructions.

`too specific` — per-tool message-role ranking; unverified, ages with the CLI. Harm 1.


> Codex renders a skills catalog into the session instructions: a name, a
> description and a location for each skill it discovers. The catalog is the
> whole of what the machine knows about them. A skill is withheld by an
> `agents/openai.yaml` beside its `SKILL.md` declaring
> `policy: allow_implicit_invocation: false`; the entry then does not appear,
> and unrecognised frontmatter keys change nothing.

`too specific` — per-tool catalog and yaml-key mechanics; unverified. Harm 2.


> A withheld skill still reaches the machine when the client places it there.
> The turn request's input array takes a skill item carrying a name and a
> path, and that item expands into the turn as the file's text ahead of the
> prompt's own words. This is how a launcher supplies a skill the catalog does
> not offer.

`too specific` — per-tool input-item mechanics; unverified. Harm 1.


> On 2026-10-09, `codex --version` returned
> `0.158.0-alpha.9`, and `codex-next --version` returned
> `0.161.0-alpha.2`. They identify installed commands. Herdr exposes a
> metaflow identity rather than an executable binding, so neither result
> establishes a per-flow active version.

`stale` — dated installed versions; moved on by now. Harm 3.


> The native Codex launcher reads generated
> `.agents/skills/<name>/SKILL.md` files into the first prompt and verifies
> that every selected body is present in the accepted first prompt. Configuration is Flow's datom, read with `flow-meta 'Configuration'`.

`too specific` — launcher internals and generated paths; unverified. Harm 2.


> A subflow renders its own catalog and so cannot see a withheld skill. The
> base instructions also require the main session to read skill instructions
> itself rather than delegate that reading.

`duplicate` — same point as claude-harness (a subflow cannot see a withheld skill), plus per-tool catalog detail. Harm 1.


> The living and the machine both read Codex's base instructions:
> the model catalog cache and the open source carry the stock text,
> and a replacement file is the living's own.

`unverified` — a claim about what the vendor cache and source carry; no way given to check. Harm 1.


> Replacing the base instructions changes only what the main session
> is told. The guardian safety layer is a separate model session
> with its own prompt, untouched by any base-instruction override.

`unverified` — a claim about the vendor guardian layer; no way given to check. Harm 2.

Statements: 0 kept vs 11 candidates.

Worth keeping after the candidates go: no — what survives the candidates is a handful of sentences already said in claude-harness and context-strata.

## datom


> ```rust
> pub struct Datom { pub path: Path, pub form: Form }
> pub enum Form { Struct(Vec<Datom>), Vector(Vec<Datom>), Variant(Symbol, Box<Datom>), Bare(String), String(String), Meaning(Opaque) }
> ```

`too specific` — Rust type definitions in belief; code, and the crate is the source of truth. Harm 2.


> ```
> ; datom, in a position expecting Person: a struct of name String, born Integer, address Address, roles Vector<Role>.
> { Ada 1990 { «12 Rue de la Paix» Paris 75002 } [ Author Reviewer.{ 2024 17 } ] }
>
> ; Reply: an enum of Accepted.{ id Integer  at String }, Refused.{ reason String  code Integer }, Pending
> Accepted.{ 42 2026-09-03T17:46:20 }          ; the timestamp has no space and no delimiter, so it is bare
> Refused.{ «no such file: { } is content» 2 } ; delimited: the string has spaces and braces; inside the guillemets they are content
> Pending                                      ; a variant carrying nothing
>
> [ 0 42 -42 ]                                 ; a vector of Integer
> Observed.Locks.[]                            ; the Observed variant, its Locks variant, the empty vector
> [ Some.42 None ]   Ok.{ Ada 1990 }   Err.«no such lock»   ; Vector, Option and Result read as ordinary variants
> ```

`too specific` — syntax examples as code, including a dated timestamp; the datom syntax belongs to vision-datom and the codec. Harm 1.


> ```rust
> pub trait Composable {
>     fn compose<T: Composing>(&self, budget: &mut Budget) -> Result<T, Error>;
>     fn compose_positions<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>;
> }
> pub trait Composing: Sized { fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error>; }
> pub trait Compositional: Composing { const ARITY: Integer; fn from_positions(positions: Positions<'_>) -> Result<Self, Error>; }
> pub trait Datomizable { fn datomize(&self, at: Path) -> Datom; }
> ```

`too specific` — trait signatures as code; the crate is the source of truth. Harm 2.


> ```rust
> #[derive(datom_codec::Datomizable, datom_codec::Composing)]
> pub struct Locus { pub path: Path, pub extent: Extent }
>
> impl Compositional for Locus {                              // generated: the positions, in order
>     const ARITY: Integer = 2;
>     fn from_positions(mut positions: Positions<'_>) -> Result<Self, Error> {
>         Ok(Self { path: positions.position()?, extent: positions.position()? })
>     }
> }
> impl Composing for Locus {                                  // generated: the datom reads, spending the budget
>     fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error> {
>         datom.compose_positions(budget)
>     }
> }
> impl Datomizable for Locus {                                // generated: each child placed as the tree is built
>     fn datomize(&self, at: Path) -> Datom {
>         Datom { path: at.clone(), form: Form::Struct(vec![self.path.datomize(at.child(0)), self.extent.datomize(at.child(1))]) }
>     }
> }
> ```

`too specific` — derive example with generated impls; code in belief, ages with the crate. Harm 2.


> ```rust
> let query: Query = Potential::<Query>::from(text).actualize(&mut budget)?;
> let out = response.datomize(Path::new()).protosize().textualize();
> ```

`too specific` — API call snippet; code in belief. Harm 1.


> ```
> [ 1 x ]                                  ; read as Vector<Integer>
> Error.{ Composition [ 1 ] Value.{ Integer x } }   ; at path 1, the bare string x is not an integer
> ```

`too specific` — error-form example; code in belief. Harm 1.


> ```sh
> orchestrate 'Lock.{ MyLock 6329f1 [ /abs/path ] «why I hold it» }'
> # -> Locked.{ 442 MyLock 6329f1 [ /abs/path ] «why I hold it» }
> ```

`duplicate` — orchestrate request example carrying a flow-id-like token and lock id; orchestrate.md owns it. Harm 2.

Statements: 2 kept vs 7 candidates.

Worth keeping after the candidates go: no — two sentences remain; the syntax lives in vision-datom and the crate.

## ethos


> The sweet form, root head then sections as siblings, is converted to the canonical braced form before reading. Section order: Library imports, types, kinds, associations; Signal imports, queries, responses, types; Operation imports, operations, outcomes, types, proposed and pending the living's word; Memory imports, record types. A Signal generates `pub enum Query` and `pub enum Response`, an Operation `pub enum Operation` and `pub enum Outcome`, from the two sections after imports. A file headed `Sema`, Memory's head before 15.0.0, is refused as `Conceptual.{ [ 0 ] Renamed.Memory }`.

`stale` — section order and a version cutoff ("before 15.0.0") of a generator that moves; unverified. Harm 3.


> The canonical print is vertical: a structure with more than one element, one of which has a next layer, opens on its line and its elements hang aligned beneath the first; the closer ends the last line; a space inside every non-empty bracket and brace, `[]` and `{}` empty, angles tight (`Vector<Event>`). protos owns it as `Textualizable::textualize`; the one-line form is `Compactable::compact`, which the command-line replies use.

`too specific` — printing rules of one generator; protos owns them. Harm 1.


> `Name.Type` is an alias, `Name.{ }` a struct, `Name.[ ]` an enum. An inline struct or enum payload generates a Rust type named `<Variant>_Data`; a vector payload is carried as the vector, with no `_Data`. A struct position may declare its type in place, `Brief.String`, `State.[ Running Ended ]`, `Capsule.{ Home.String Login.Vector<String> }`: the type takes that name in the file's namespace and the position holds it by name (`brief: Brief`). Imports are `protos:String` or `protos:[ String Integer ]`; intrinsics need none: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

`too specific` — generator syntax mechanics; ethos-zero --help and vision-ethos cover them. Harm 2.


> A simple kind is `Name.[ capabilities ]`; receivers `.` self, `!` mutable self, `:` none; a capability with inputs is `push!{ [ inputs ] [ yield ] }`; a complex kind is `Name.{ [ superkinds ] [ associated types ] [ CONSTANTS ] [ capabilities ] }`. A kind in an input or yield becomes a method parameter bounded by it, lettered from `N` (`fn resolve<N: Textualizable>(&self, input: N)`), or `Self::Item` where an associated type is already bounded by that kind (`Item<Textualizable>`). Self, the kind's head parameters and a named associated type stay as written. A concrete type in an input (`String`, `Vector<Self>`, a declared type) is refused with `KindWanted`; a yield may name one. An imported name is taken as a kind in an input and as a type in a yield.

`too specific` — kind-generation mechanics and error names; unverified. Harm 2.


> protos and datom-codec generate their kinds files from their own ethos, with the kinds Spendable (protos), Branchable, Budgeted, Positional and Composable (datom-codec).

`too specific` — which crates generate which kinds files; one-off detail. Harm 1.


> In every root each generated struct and enum derives rkyv's Archive, Serialize and Deserialize, Clone, Debug, PartialEq, Eq and Hash, and its Datomizable and Composing sit behind a `datom` feature that the CLI enables and the Nexus does not. A crate holding generated Rust depends on rkyv 0.8 always and on datom-codec only under `datom`; where a position holds a `Decimal`, a `Meaning` or a datom-codec `Error`, it enables datom-codec 0.32.2's `rkyv` feature, which enables protos's, unconditionally. An alias carries no derive. A generated file opens with `#![allow(dead_code, non_camel_case_types, non_snake_case)]`, every item carries `#[rustfmt::skip]`, names are fully qualified with no `use`. Generated Rust is committed and held fresh by a test.

`stale` — a version pin (datom-codec 0.32.2) and generated-file boilerplate; stale the next release. Harm 3.


> ```
> ethos-zero 'Generate.{ /abs/flow.ethos /abs/out }'
> Generated.[ /abs/out/flow.rs ]
>
> ethos-zero 'Check./abs/flow.ethos'
> Checked./abs/flow.ethos
> ```

`procedure` — command invocations; belongs in ethos-zero help. Harm 1.


> A refused file answers `Rejected.{ file { line column } reason }`, the reason naming the path within the file (`Conceptual.{ [ path ] KindWanted.Path }`), and a rejected Generate writes nothing. With no argument ethos-zero prints its own ethos in the canonical print.

`too specific` — error shape of one tool; unverified. Harm 1.

Statements: 0 kept vs 8 candidates.

Worth keeping after the candidates go: no — nothing remains; every paragraph is generator mechanics owned by ethos-zero and vision-ethos.

## flow


> These are the authorized contracts; this section does not establish deployed runtime behavior while the configuration rewrite is pending.

`stale` — says it establishes nothing while a rewrite is pending; names a state that has moved or will. Harm 2.


> The tool that starts flows merges its configuration files in order, shared, aspect, metaflow, map into map, so a later file's value wins at each key.

`unverified` — a claim about config merge order of a tool, no way given to check. Harm 2.


> A context is young while it stays under half the layer's refresh threshold.

`too specific` — a threshold rule of one layer; one-off detail. Harm 1.


> A launch that needs a Primary starts its Secondary first.

`unverified` — a launch-order claim with no way given to check. Harm 1.

Statements: 0 kept vs 4 candidates.

Worth keeping after the candidates go: no — nothing remains of four statements, all unverified.

## flow-seats


> Source: Flow `d87b15a`, `crates/flow/src/main.rs`, `crates/flow-nexus/src/sending.rs` and `waking.rs`; signal-flow `994ce15`, `src/generated/signal.rs`. These are source contracts, not evidence of an installed revision.

`stale` — commit hashes of two repos, stated as not evidence of an installed revision. Harm 3.


> ```sh
> flow 'Current.{ Mind tools Secondary }'
> flow 'Metaflows'
> flow 'Send.{ Address.{ Mind tools Secondary } Wake Soft.Order.«Review the source packet.» }'
> flow 'Send.{ Address.{ Mind tools Secondary } Queue Soft.Notice.«The source packet is available.» }'
> flow 'Send.{ Up Wake Soft.Result.«The bounded package is ready.» }'
> flow 'BindSeat.{ Mind tools Secondary }'
> flow 'Launch.{ { Mind tools Secondary } «Review the declared task.» }'
> ```

`procedure` — CLI command list; belongs in flow help. Harm 1.


> `Send` has three positions: recipient, delivery, message. The recipient is `Address.{ Aspect topic Layer }` or `Up`, the layer above in the sender's aspect and topic. Delivery is `Wake` or `Queue`. `Wake` requests wake and queue draining; `Queue` retains work without independently requesting a wake. Delivery is explicit and independent of the message kind. `DeliverAll.{ Mind tools Secondary }` requests delivery of all work already queued for that address.

`procedure` — CLI positions and delivery modes; belongs in flow help. Harm 1.


> The CLI also accepts a two-position `Send`, recipient followed by message, and supplies `Wake`. It sends the same typed three-position request to Nexus:
>
> ```sh
> flow 'Send.{ Address.{ Mind tools Secondary } Soft.Order.«Review the source packet.» }'
> ```

`procedure` — CLI shorthand form with a second example; belongs in flow help. Harm 1.


> A message is a priority carrying a request. Priorities are `Soft`, `MiddleAbrupt` and `HardAbrupt`. Request kinds are `Order`, `Question`, `Result`, `Notice`, `Psyche` and `Psyches`. `Psyche` carries context and verbatim strings; `Psyches` carries their vector. The sender is resolved from the calling process; no command supplies a sender Flow ID.

`too specific` — priority and request-kind names; vision-messaging and flow help cover them. Harm 1.


> ```sh
> flow 'Send.{ Address.{ Psyche core Secondary } Wake Soft.Psyche.{ «The context.» «The exact words.» } }'
> flow 'Send.{ Up Queue Soft.Psyches.[ { «First context.» «First words.» } { «Second context.» «Second words.» } ] }'
> ```

`procedure` — more CLI examples; belongs in flow help. Harm 1.


> Successful admission returns `SendAccepted.{ logical-delivery-id cursor Queued }`. This witnesses durable acceptance, not native arrival, reading or completion. `ObserveSends.None` opens the sender's outcome stream; a returned cursor can resume it. An unknown recipient returns `Refused.Unknown.Address`; sending does not declare or launch an unknown metaflow. `Up` from a Primary returns `Refused.NoneAbove`.

`too specific` — reply shapes and error names of the CLI; the sentence "This witnesses durable acceptance, not native arrival, reading or completion" is the only part worth saving elsewhere. Harm 1.


> `Current` reports `Current.Awake.<id>`, `Current.Asleep` or `Current.Unknown`. `Metaflows` lists addresses, current state, prior flows and queued requests. A closed pane alone does not establish that a metaflow is absent.

`too specific` — reply shapes of the CLI; the closed-pane sentence is the only part worth saving elsewhere. Harm 1.


> `BindSeat` identifies the calling native seat and binds it to the supplied address. Its only position is the address; it takes no supplied native session, process or Flow ID. An occupied address can refuse as `Taken`; an unlocated caller refuses as `Unidentified`.

`too specific` — per-command refusal names; belongs in flow help. Harm 1.


> `Launch` has two positions: address and instruction string. It composes the address's declared system and user modules with the configured model and layer effort. Missing declarations return `StartRejected.Undeclared`; a missing configured model refuses as `NotConfigured`. Launching the caller's own live address replaces that flow. Launch success, send acceptance and native receipt are separate observations.

`too specific` — per-command refusal names; belongs in flow help. Harm 1.

Statements: 0 kept vs 10 candidates.

Worth keeping after the candidates go: no — the CLI is its own help; nothing durable remains.

## lojix


> Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.

`procedure` — which client talks to which socket; lojix --help carries it. Harm 1.


> Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.

`procedure` — which client talks to which socket; lojix --help carries it. Harm 1.


> Use `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET`; neither socket has a default path.

`too specific` — environment variable names. Harm 1.


> Each public client rejects files, zero arguments, and extra arguments. A request root is one value.

`procedure` — client argument rules; belongs in the CLI help. Harm 1.


> A struct is brace-enclosed and positional, a vector is bracket-enclosed, a variant is a head with the period glued to both sides, and a variant carrying nothing is bare. `None` is bare and `Some` carries one glued payload. A string with a space or a delimiter is written in guillemets.
>
> ```text
> Variant.{ field0 field1 field2 }
> [ field0 field1 ]
> Some.Value
> «alpha beta»
> ```

`duplicate` — datom syntax; said in datom and vision-datom. Harm 1.


> Never name a field in a request; the position carries the data.

`duplicate` — datom positional rule; said in datom. Harm 1.


> `Query` carries `ByNode`, `ByGeneration`, `ByDeployment`, `ByEventLog`, or `ByTestRun`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `ByNode` has, in order:
>
> 1. cluster name
> 2. node name
> 3. optional requested generation artifact

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Exact witnessed form:
>
> ```sh
> lojix 'Query.ByNode.{ alpha node-1 None }'
> ```

`too specific` — a one-off example request (alpha node-1). Harm 1.


> `ByGeneration` carries one generation identifier.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `ByDeployment` carries one deployment identifier.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `ByEventLog` has, in order:
>
> 1. first event-log position
> 2. last event-log position

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `ByTestRun` has, in order:
>
> 1. cluster name
> 2. node name
> 3. optional test-run identifier

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `WatchDeployments` has, in order:
>
> 1. optional deployment identifier
> 2. optional cluster name
> 3. optional node name

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> The all-target schema-derived form is:
>
> ```sh
> lojix 'WatchDeployments.{ None None None }'
> ```

`too specific` — a derived example request. Harm 1.


> `WatchCacheRetention` has, in order:
>
> 1. optional cluster name
> 2. optional node name

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> The all-target schema-derived form is:
>
> ```sh
> lojix 'WatchCacheRetention.{ None None }'
> ```

`too specific` — a derived example request. Harm 1.


> A successful watch request returns:
>
> ```text
> Watching.{ subscription-token commit-sequence }
> ```

`too specific` — reply shape with unexplained token fields. Harm 1.


> A rejection is `WatchRejected.MalformedWatch`, `WatchRejected.SubscriptionLimitReached`, or `WatchRejected.StreamUnavailable`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Unwatch` carries one subscription token.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Deploy.Host` has, in order:
>
> 1. cluster name
> 2. node name
> 3. host composition
> 4. proposal source
> 5. secrets input
> 6. flake reference
> 7. deployment transport
> 8. deployment input mode
> 9. deployment output selector
> 10. activation backend
> 11. host deploy action
> 12. source revision policy
> 13. optional Nix builder
> 14. extra substituters

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Deploy.UserEnvironment` has, in order:
>
> 1. cluster name
> 2. node name
> 3. user name
> 4. proposal source
> 5. secrets input
> 6. flake reference
> 7. deployment transport
> 8. deployment input mode
> 9. deployment output selector
> 10. activation backend
> 11. user-environment action
> 12. source revision policy
> 13. optional Nix builder
> 14. extra substituters

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> A deployment transport is the positional product of:
>
> 1. Nix store URI
> 2. SSH destination

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> A deployment output selector is a one-field positional product.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> An optional builder is `None` or `Some` carrying its string.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Extra substituters are a vector of two-string positional products.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Host compositions are `CompleteHost` and `BaseHost`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Host deploy actions are `Evaluate`, `Realize`, `SetBootProfile`, `ActivateNow`, `TestActivation`, and `ScheduleBootOnce`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> User-environment actions are `Realize`, `SetProfile`, and `ActivateNow`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Deployment input modes are `Horizon` and `Direct`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Activation backends are `NixosSystemdBootV1` and `HomeManagerNixProfileV1`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Source revision policies are `RequireImmutable` and `ResolveAndRecord`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Pin` has, in order:
>
> 1. cluster name
> 2. node name
> 3. generation identifier
> 4. pin label

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Exact witnessed form:
>
> ```sh
> lojix-meta 'Pin.{ alpha node-1 42 keep }'
> ```

`too specific` — a one-off example request (alpha node-1, 42, keep). Harm 1.


> `Unpin` has, in order:
>
> 1. cluster name
> 2. node name
> 3. pin label

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Retire` has, in order:
>
> 1. cluster name
> 2. node name
> 3. generation identifier

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Test` carries `Run` or `Check`.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Test.Run` has, in order:
>
> 1. cluster name
> 2. node selection
> 3. host selection
> 4. test execution profile

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> A node selection is bare `All` or `Nodes` carrying a node-name vector.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> A host selection is bare `DefaultHost` or `OnHost` carrying a node name.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> A test execution profile has, in order:
>
> 1. test mode
> 2. Nix system
> 3. deployment output selector
> 4. optional deployment transport

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> `Test.Check` carries a node-name vector.

`too specific` — field list or variant names of the contract; signal-lojix is the source of truth. Harm 1.


> Ordinary reply families are `Queried`, `DeploymentEventsQueried`, `TestRunsQueried`, `Watching`, `Unwatched`, `QueryRejected`, `WatchRejected`, and `UnwatchRejected`.

`too specific` — reply names; signal-lojix is the source of truth. Harm 1.


> Owner reply families are `DeployAccepted`, `DeployRejected`, `DeployTerminal`, `Pinned`, `PinRejected`, `Unpinned`, `UnpinRejected`, `Retired`, `RetireRejected`, `Tested`, and `TestRejected`.

`too specific` — reply names; signal-lojix is the source of truth. Harm 1.


> `DeployAccepted` has, in order:
>
> 1. deployment identifier
> 2. state marker

`too specific` — reply field list; signal-lojix is the source of truth. Harm 1.


> Exact witnessed reply:
>
> ```text
> DeployAccepted.{ 13 { 263 263 } }
> ```

`too specific` — a transcript of one reply with literal ids (13, 263). Harm 2.


> `DeployTerminal` carries the terminal deployment record.

`too specific` — reply shape. Harm 1.


> A deployment terminal is bare `Succeeded`, `Rejected` carrying a terminal reason, or `Failed` carrying failure stage and terminal reason.

`too specific` — reply shape. Harm 1.


> Exact witnessed failed-activation form:
>
> ```text
> Some.Failed.{ Activate ActivationFailed }
> ```

`too specific` — a transcript of one failed activation. Harm 1.


> `Pinned` and `Unpinned` carry generation identifier, pin label, source slot, destination slot, and state marker.

`too specific` — reply field list. Harm 1.


> `Retired` carries generation identifier, generation slot, and state marker.

`too specific` — reply field list. Harm 1.


> `Tested` carries test-run identifier and state marker.

`too specific` — reply field list. Harm 1.


> A deployment proposal must be an existing absolute regular non-symlink `horizon-definition.datom` file.

`too specific` — a literal file name. Harm 1.


> The Nexus does not accept operator requests. `lojix-write-configuration` is the datom-to-startup boundary and writes the archive consumed by `lojix-nexus`.

`too specific` — binary name of a startup helper; per-tool mechanics. Harm 1.


> Its single request is the `ConfigurationWriteRequest` struct with:
>
> 1. ordinary socket path
> 2. ordinary socket mode
> 3. owner socket path
> 4. owner socket mode
> 5. state directory
> 6. store path
> 7. Nexus host
> 8. test-default choice
> 9. output path

`too specific` — field list of a startup request. Harm 1.


> Exact tested form:
>
> ```text
> ConfigurationWriteRequest.{ /run/fixture-lojix/ordinary.sock 432 /run/fixture-lojix/owner.sock 384 /var/lib/fixture-lojix /var/lib/fixture-lojix/configured-lojix-store.db fixture-nexus NoTestDefaults /tmp/startup.rkyv }
> ```

`too specific` — a fixture request with literal paths and numeric modes (432, 384). Harm 2.


> Production uses bare `NoTestDefaults`.

`too specific` — variant name. Harm 1.


> The nested development form is `TestDefaults` with, in order:
>
> 1. cluster name
> 2. VM host
> 3. mode
> 4. flake
> 5. Nix system
> 6. output selector
> 7. proposal source

`too specific` — field list of a development form. Harm 1.


> Success prints:
>
> ```text
> ConfigurationWritten.[ path ]
> ```

`too specific` — reply shape. Harm 1.


> Inspect a store read-only with exactly:
>
> ```sh
> lojix-inspect-store 'InspectStore.{ /tmp/lojix.sema }'
> ```

`procedure` — store-inspect command; belongs in the tool help. Harm 1.


> Inspection does not create or register missing tables.

`too specific` — tool mechanic. Harm 1.


> Reset accepts only:
>
> ```sh
> lojix-reset-store 'ResetStore'
> ```

`procedure` — store-reset command; belongs in the tool help. Harm 1.


> It takes no path. Store selection comes from the service-owned `LOJIX_CONFIGURATION` archive.

`too specific` — tool mechanic with an environment variable name. Harm 1.


> The Nexus accepts schema v5 and refuses earlier schemas. Reset removes and recreates recognized v2/v3/v4 stores as v5. An existing v5 store is left intact.

`stale` — a schema version number (v5) and the v2/v3/v4 history; stale when the schema moves. Harm 3.


> Successful reset replies are:
>
> ```text
> LojixStoreReset.{ path 5 count }
> LojixStoreAlreadyCurrent.{ path 5 }
> ```

`stale` — reply shapes carrying the schema number 5. Harm 2.


> Reset is destructive for a recognized v2/v3/v4 store.

`stale` — depends on the recognized schema list above. Harm 2.


> `lojix-bootstrap` is a separate Nexus-free ingress. It accepts exactly one inline `BootstrapRun` value and does not read Nexus sockets, configuration, or store state.

`too specific` — tool mechanics of a separate binary. Harm 1.


> `BootstrapRun` is a struct with:
>
> 1. request identifier
> 2. bootstrap mode

`too specific` — field list. Harm 1.


> `BuildOnly` carries:
>
> 1. direct immutable build request
> 2. optional builder
> 3. journal parent
> 4. GC root
> 5. terminal-evidence path

`too specific` — field list. Harm 1.


> The direct immutable build request carries:
>
> 1. immutable flake
> 2. Nix system
> 3. output selector

`too specific` — field list. Harm 1.


> `BootOnce` additionally carries a test plan and either `RemoteNixosSystemdBootV1` or `LocalBootstrapV1`.

`too specific` — variant names. Harm 1.


> `RemoteNixosSystemdBootV1` carries:
>
> 1. Nix store URI
> 2. SSH destination
> 3. SSH policy
> 4. system profile
> 5. boot entries

`too specific` — field list. Harm 1.


> Its SSH policy carries caller-owned identity, caller-owned known-hosts, and bare `RequireKnownHost`. Ambient SSH configuration is not accepted.

`too specific` — field list. Harm 1.


> `LocalBootstrapV1` carries:
>
> 1. system profile
> 2. boot entries

`too specific` — field list. Harm 1.


> Bootstrap immutable flakes use:
>
> ```text
> github:owner/repository/40-lowercase-hex-revision
> ```

`too specific` — flake-reference syntax with a hash-length detail. Harm 1.


> This differs from Nexus deployment flake syntax.

`duplicate` — compares with the syntax above; only meaningful with it. Harm 1.


> Terminal output is bare `BootstrapTerminal.Succeeded` or `BootstrapTerminal.Failed`. Parse or validation failure prints a redacted `BootstrapRejected.[ … ]`.

`too specific` — reply names. Harm 1.

Statements: 15 kept vs 77 candidates.

Worth keeping after the candidates go: yes — the deployment contract (explicit transport, node match, admission is not completion, Current is not live state) is not discoverable from the CLI.

## nexus


> Orchestrate: read the current source version in the declared Orchestrate repository’s `Cargo.toml`.
> Flow: read the current source version in the declared Flow repository’s `Cargo.toml`.
> Message: read the current source version in the declared Message repository’s `Cargo.toml`.
> Lojix: read the current source version in the declared Lojix repository’s `Cargo.toml`.

`procedure` — a how-to to read Cargo.toml; four near-identical lines that state no fact about any nexus, despite the module title. Harm 2.


> Curriculum receives one typed request through the socket at
> `$XDG_RUNTIME_DIR/curriculum/curriculum.sock`. Its three authored-context
> checkouts come from `CURRICULUM_PSYCHES_REPOSITORY_DIR`,
> `CURRICULUM_MIND_CONTEXT_DIR` and `CURRICULUM_FIELD_CONTEXT_DIR`; its refresh
> executable comes from `CURRICULUM_CONTEXT_REFRESH_PROGRAM`. These configured
> values, including the service account and checkout locations, belong to the
> installation and are read there rather than assumed from another setup.

`too specific` — socket path and environment variable names of one installation. Harm 2.


> At Curriculum `2d74e7725bfff88ee3aec1ebe9ce31d52873ebbc`, every query follows
> `CurriculumOperation::perform` → `SourceConfiguration::from_environment` →
> `SourceConfiguration::read`. `read` runs the configured refresh executable
> synchronously and requires its success before reading the three checkout
> revisions and their module sources; only then does `perform` dispatch
> `ResolveSkills`, `ResolveSources`, `ComposeStartup` or `ComposeRole`. Nexus
> startup also calls `read` while opening its memory. Thus `ExecStartPre` is not
> the request-time refresh: it is an additional startup action.

`stale` — pinned to one Curriculum commit hash and internal function names; stale on the next commit. Harm 3.


> The 2026-10-29 operational witness from Psyche Primary
> `psyche228c47e` (with Mind `2eff0f9` and Field `77feb34`) observed the user
> `curriculum-nexus.service`, with no root process, configured to run
> `curriculum-refresh-contexts`. That program fetches each context repository's
> `origin/main` and detaches its configured checkout there. The same witnessed
> checkout update was performed manually with `git fetch origin` followed by
> `git checkout --detach origin/main`. A
> `ResolveSources.[ ModuleIdentity ]` request through the configured socket then
> reported the revision from which Curriculum served that module. The returned
> revision witnesses the request's source checkout; it does not identify the
> Curriculum executable revision by itself.

`stale` — a dated witness naming flow ids and commit hashes, and a manual git procedure; the transcript of one run. Harm 3.

Statements: 0 kept vs 4 candidates.

Worth keeping after the candidates go: no — nothing remains; the title promises what the nexuses are today and the text is a dated transcript.

## orchestrate


> Datom strings are in guillemets, «like this»; curly quotes and ASCII double quotes are not delimiters. A copyable multi-word reason example is:

`duplicate` — datom guillemet rule; said in datom and lojix modules. Harm 1.


>     orchestrate 'Lock.{ OrchestrateDocs 444e5e [ /absolute/path/to/file ] «Clarify Lock fields» }'

`too specific` — example carrying a flow-id-like token. Harm 1.


> Release by the returned integer ID using the Orchestrate release request skill variable, substituting the integer for <lock-id>. Read the typed reply.

`unverified` — points at an Orchestrate release request skill variable not shown here. Harm 1.


> A lock whose holder has no live flow is stale: check the holder's six-character id against `herdr pane list` labels and `flow 'Metaflows'`; `orchestrate 'Release.<id>'` releases any lock by its number, whoever holds it, and a stale lock is released by whoever meets it.

`too specific` — names herdr and flow commands for a stale-lock check; per-tool mechanics. Harm 2.

Statements: 11 kept vs 4 candidates.

Worth keeping after the candidates go: yes — the Lock field rules (own FLOW_ID only in FlowId, snapshot not subscription, client failure is failure) are acting facts.

## protos


> ```
> ; textual: these characters, uninterpreted
> { Ada 1990 }
> ```

`too specific` — illustrative code snippet in belief. Harm 1.


> ```rust
> // protosic: an enclosure of two bare runs, each structure at its extent in the text
> Protos::Enclosed { extent: Extent { start: 0, end: 12 }, enclosure: Braced, children: vec![
>     Protos::Bare { extent: Extent { start: 2, end: 5 }, text: "Ada".to_owned() },
>     Protos::Bare { extent: Extent { start: 6, end: 10 }, text: "1990".to_owned() } ] }
> // conceptual, here datomic: a struct of two positions, each datom at its path
> Datom { path: vec![], form: Form::Struct(vec![
>     Datom { path: vec![0], form: Form::Bare("Ada".to_owned()) },
>     Datom { path: vec![1], form: Form::Bare("1990".to_owned()) } ]) }
> // compositional: the meaning fully absorbed; no position, because the tree is consumed
> Person { name: String::from("Ada"), born: 1990 }
> ```

`too specific` — Rust constructors as illustration; code in belief. Harm 2.


> | type | kind | becomes |
> |---|---|---|
> | composition | `Composing` | read from a datom; a struct form states its positions through `Compositional` |

`too specific` — a table with one row; dead weight. Harm 1.


> ```rust
> pub enum Protos {
>     Headed { extent: Extent, head: Symbol, constraints: Option<Box<Protos>>, separator: Separator, body: Box<Protos> },
>     Enclosed { extent: Extent, enclosure: Enclosure, children: Vec<Protos> },
>     Opaque { extent: Extent, boundary: Boundary, content: String },
>     Bare { extent: Extent, text: String },
> }
> pub enum Enclosure { Braced, Bracketed, Angled }
> pub enum Boundary  { Guillemets, Parentheses }
> pub enum Separator { Period, Exclamation, Colon }
> pub struct Extent { pub start: usize, pub end: usize }
> pub struct Error  { pub extent: Extent, pub problem: Problem }
> pub struct ReaderBudget { pub remaining: usize }
>
> pub trait Protosizable    { type Output; fn protosize(&self) -> Self::Output; }  // String -> Result<Protos, Error>; Datom -> Protos
> pub trait Textualizable   { fn textualize(&self) -> String; }
> pub trait Canonicalizable { fn canonicalize(&mut self); }
>
> let text = person.datomize(Path::new()).protosize().textualize();
> ```

`too specific` — type definitions copied from the crate; code in belief, ages with the crate. Harm 2.

Statements: 2 kept vs 4 candidates.

Worth keeping after the candidates go: no — two sentences remain beside empty headings.

## psyche


> - **Spirit** — philosophy. Almost never changes. Load the `spirit:core` belief module.
> - **Intent** — declared goals and guiding rules. Broader and fewer than Vision.
> - **Vision** — concrete, topic-scoped, abundant, moves constantly.
>   The default level. Everything starts here unless obviously broader.
>
> - **Notion** — a brainstorm: an idea the living is turning over, binding nothing. The bottom level. Logged verbatim; never built on as if ruled.

`duplicate` — four levels are said in vision-psyche. Harm 1.


> Inversion signals unenunciated Vision or contaminated levels.

`not common sense` — unexplained inference rule. Harm 1.


> A notion may be drawn upon for suggestions. A flow told explicitly to implement without asking for clarifications may rely on a notion only when its need matches the notion exactly.

`duplicate` — notion use is said in intent-psyche. Harm 1.


> - The `spirit:core` belief module — spirit's current home; entry files will
>   carry it.

`stale` — "entry files will carry it" is a future tense about a state that has moved or will. Harm 2.


> - `flows/<short-id>/vision/<topic>.md` — raw records, in the flow
>   that heard them. Finding raw psyche means searching
>   `flows/*/vision/`.

`too specific` — a path layout and a search glob. Harm 2.


> - `flows/<short-id>/notion/<topic>.md` — raw notions, in the flow that heard them.

`too specific` — a path layout. Harm 1.


> - `vision-raw/<topic>.md` — legacy: the vision corpus not yet crystallized
>   heard before flows, draining into vision belief modules as crystallization
>   touches it; phased out, gone when empty. Nothing new lands
>   there — a raw record lives in the flow that heard it.

`stale` — a legacy corpus described as draining and phased out; names a state that moves. Harm 2.


> A topic is a noun subject an agent would guess before knowing any ruling; a statement is an entry heading inside it.

`not common sense` — a topic-naming rule; not common sense, belongs where topics are made. Harm 1.


> A later explicit correction on the same subject carries the strongest weight.
> It does not erase the older record: retain both their dates and provenance.
> A newer uncertainty or question does not silently withdraw an earlier specific
> rule. When records point to incompatible actions, the flow takes his latest word, acts on it, and says in its report which reading it took and why. He is asked only when the two readings would cost him differently.

`duplicate` — weighing the later word against the earlier is intent-psyche. Harm 1.

Statements: 8 kept vs 9 candidates.

Worth keeping after the candidates go: yes — the core stance (written psyche is lossy, never ground truth, preserve raw words) is common sense a flow needs.

## vocabulary


> Illustrated book: a book to which a model has added illustrations, deciding where each goes. Flashbook, picture book and photo book name the same thing.

`not common sense` — coins a term with aliases (flashbook, picture book, photo book). Harm 1.


> Drifting context: context that passes from flow to flow by handover and message and is landed in no module, so a new flow starts without it. Good drifting context is lost for want of landing; bad drifting context is meant to be lost.

`not common sense` — a coined term with a judgement attached. Harm 1.


> Quackery: output that stands in for understanding the flow does not
> have — a claim it cannot ground, prose that sounds deep over a gap, a
> test that only confirms itself.

`not common sense` — a coined term. Harm 1.


> Past: the flows a flow has remembered, and theirs in turn.

`not common sense` — a term whose meaning is not clear from its line. Harm 1.


> Vision impurity: a working instruction (what to do now, in what order,
> at what scope, on which project, through which dispatch) logged as a
> vision record.

`duplicate` — vision impurity is said in vision-crystallization. Harm 1.


> Memory: The database of a Nexus is Memory, in every flow's words; a file or crate still named sema is a legacy name, said as Memory and renamed when met. Sema names only the meaning dialect.

`duplicate` — Memory and the Sema naming is said in vision-memory and vision-sema; a rename instruction. Harm 1.


> Evolution is the dynamic procedure of improvement and redeployment: the system improving itself and deploying the improvement.

`not common sense` — a coined term. Harm 1.

Statements: 12 kept vs 7 candidates.

Worth keeping after the candidates go: yes — it defines the owner's own terms, which are what vocabulary is for.
