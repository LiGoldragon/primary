# Meta-local Configure projection generator — bounded proposal

Controls: Core NO EthosZero extension. Existing Meta scope only; original worker, existing dependency pins. Supersedes the assertion that EthosZero itself must derive these projections. Existing fields/validation remain authoritative; this packet adds no default, resource value, new library or Memory coordinate.

## Selected available tool and exact local API

Meta already has Rust Cargo/build.rs, committed generated Rust, authored Ethos and Nix cargoTest --all-features. Held successful Ethos invocation is `/nix/store/xw4fj6aza48g00s6fxy0z6rj0d6wchnp-ethos-zero-17.0.0/bin/ethos-zero 'Generate.{ «source.ethos» «outdir» }'`; generated signal.rs compared byte-for-byte. Exact existing build.rs internals are not held: implementation must integrate rather than replace its existing duties.

Use a std-only package-local Rust module `tools/configure_projection.rs`, shared by the existing build.rs and a standalone authoring driver `tools/generate_configure.rs`. The driver can be compiled with the selected Rust toolchain, no new Cargo dependency or published crate. API:

```rust
fn generate(spec: &[Declaration], template: &str) -> Result<Artifacts, GenerationError>;
struct Artifacts { signal_ethos: String, projections_rs: String }
```

The authoring driver writes these two candidate files explicitly; ordinary build only generates into OUT_DIR and compares with committed files, failing on differences. It never rewrites source. The existing Ethos generator then generates signal.rs from the resulting committed signal.ethos as before. Equality checks cover BOTH projection generation and Ethos-to-Rust generation. Nix source filtering must include tools/ and the sole spec/template inputs. No dependency on an external newly published generator.

## ONE input and typed identity metadata

`tools/configure_spec.rs` is the ONE authored ordered declaration inventory. `ethos/signal.template.ethos` holds the rest of the existing contract with one unique generated-declarations insertion marker; it contains none of the three generated enum inventories. Generated signal.ethos remains the actual published/self-description contract.

Each spec entry has exactly:

```rust
struct Declaration {
    variant: &'static str,       // one Configure set variant
    payload: Payload,          // ONE type fact/shape; both languages derived
    identity: Identity,
    domain: Domain,
    removal: Removal,
}
enum Identity {
    Singleton,
    Field { position: usize }, // type resolved from the SAME Record field
}
enum Payload {
    Existing(TypeReference),   // singleton identity only; no introspection
    Record { name: &'static str, fields: &'static [Field] },
}
struct Field { name: &'static str, ty: TypeReference }
enum TypeReference {
    Integer, String,
    Named { namespace: &'static [&'static str], name: &'static str },
    Vector(&'static TypeReference), Option(&'static TypeReference),
}
enum Domain { RuntimePolicy, MetaflowDeclaration, Retained(RetainedDomain) }
enum Removal { None, Named(&'static str) }
```

`RetainedDomain` is a finite public semantic enum for the retained operations listed below, NOT private storage constants or family names. Names are authored generation configuration validated as identifiers, never runtime dispatch or caller-supplied text. One selected correspondence renders TypeReference into Ethos and Rust: Integer→Integer/i64, String→String/String; Named renders the same namespace/name with each language's separator (empty namespace means the generated local signal module); Vector and Option recursively render their single element reference. Existing aliases are Named, not independently restated representations. No paired Ethos/Rust type strings or override escape exists. Keyed Payload::Record owns the complete ordered fields and emits that payload declaration too; remove its former template declaration. Identity::Field selects a zero-based position in that same record, deriving its TypeReference directly. Out-of-range positions or keyed Existing payloads refuse generation. No Ethos parser/import resolver is required or introduced; type namespaces are explicit in the ONE shape. The key type is never authored a second time. Generated compilation and all-entry fixtures check the selected correspondence. No arbitrary string-key encoding.

For each entry generate simultaneously:
- ConfigurationChange set variant and, if named, its removal variant carrying the key type;
- ConfiguredValue set variant with identical name/payload, no removal variants;
- Setting identity variant, nullary for singleton or typed key payload for keyed values;
- exhaustive ConfiguredValue::setting and ConfigurationChange removal-to-Setting projection;
- public semantic setting/domain tags only; NO concrete storage routing or private Flow imports;
- RuntimePolicyValue from ONLY Domain::RuntimePolicy entries, preserving their relative spec order, plus exhaustive fallible conversion from broad ConfiguredValue.

Generated projections are ordinary Rust impls over Ethos-generated types. If no removal applies, the removal projection returns None; a set variant is not mistaken for a removal. Set-value extraction has an exhaustive generated match. Reject duplicate names/removal names, unmatched key metadata, duplicate identities and conflicting domain metadata during generation. There is no handwritten runtime enum/projection fallback. Tests exercise every generated entry and every available removal, not just Model.

## Existing declarations: exact identity and family mapping

| Set variant / payload | Setting identity | Sole storage authority | Removal |
|---|---|---|---|
| Model / ConfigureModel{Address, Native.String} | Model(Address) | RuntimePolicy V1 | RemoveModel(Address) |
| Continuity / ConfigureContinuity{Address, Continuity} | Continuity(Address) | RuntimePolicy V1 | RemoveContinuity(Address) |
| Metaflow / ConfigureMetaflow current fresh payload excluding Continuity | Metaflow(Address) | existing allocated metaflow-configuration V6 ONLY | RemoveMetaflow(Address) |
| Thresholds / Vector<ConfigureThreshold> | Thresholds | retained threshold family | none added |
| LeaveOuts / Vector<ConfigureLeaveOut> | LeaveOuts | retained default-leave-out family | none added |
| Nexus / ConfigureNexus | Nexus | retained Nexus configuration family | none added |
| SendServers / Vector<ConfigureSendServer> | SendServers | retained send-server family | none added |
| HarnessFlags / Vector<ConfigureHarnessFlags> | HarnessFlags | retained harness-flags family | none added |
| Investigation / Address | Investigation | retained investigation family | none added |
| DefaultMinutes / Minutes | DefaultMinutes | retained default-minutes family | none added |
| Heartbeat / Option<HeartbeatConfig> | Heartbeat | retained heartbeat family | none added |
| Counters / ConfigureCounters | Counters | existing atomic Counters operation across THREE retained families | none added |

Retained vector setters other than Models/Metaflows were explicitly unchanged by the per-Address ruling; do not silently split their storage or invent removal operations. Setting identifies the declared whole vector for those existing setters. Each actual stored row retains its existing key and schema. ConfigureNexus retains its already-configured source root/endpoints/profiles/meta-aspects/message/curriculum/lease/presentation fields; no copies in RuntimePolicy. Model old Layer/Aspect family is not active authority in the fresh052 place. No051 import.

Meta emits semantic Domain tags, never imports Flow storage constants. At Flow's owning configuration operation, ONE exhaustive adapter matches those tags to the existing storage capabilities/constants; compiler exhaustiveness catches new domains. Counters invokes its existing atomic multi-family operation, not a fictitious single-family store. No reverse dependency.

Broad ConfiguredValue is transient/wire vocabulary ONLY at this boundary. `StoredRuntimePolicy` embeds the separately GENERATED `RuntimePolicyValue`, never broad ConfiguredValue. The restricted enum contains only Domain::RuntimePolicy entries; Metaflow and retained-family payloads are excluded at the type level. `TryFrom<ConfiguredValue> for RuntimePolicyValue` exhaustively returns the original non-runtime value as its error, not a cast or silent drop. Its key projection is generated from the same entries. Prior broad StoredRuntimePolicy WIP must be replaced before writes; source dispatch alone is not archive isolation.

### Actual complete keyed payload shapes (one source)

These are the existing approved fields, in exact order. TypeReference namespaces encode the displayed paths once; existing local aliases retain their definitions outside this spec. The spec emits these payload declarations and the template removes the old copies. All three key positions are ZERO (Address).

```ethos
ConfigureModel.{ Address Native.String }
ConfigureContinuity.{ Address Continuity }
ConfigureMetaflow.{ Address Option<Root> SystemModules UserModules
                    FlowKind ToolSet Purpose Records }
```

Qualified shapes for the record metadata: Address=`flow_ethos::Address`; ConfigureModel Native uses existing local alias Native=String; Continuity uses the current local Continues/Ends declaration. ConfigureMetaflow Root is local String alias; SystemModules/UserModules/FlowKind/ToolSet are `signal_flow` types; Purpose=local String alias; Records=local Vec<RecordPath>, RecordPath=String. This preserves the witnessed original declaration order Address/root_option/system_modules/user_modules/flow_kind/tool_set/purpose/records and removes ONLY obsolete Continuity. No guessed tail or added field. Emitted Rust field names follow the existing generator convention; compile/equality checks confirm exact names.

### Restricted archive order and unreleased coordinate

RuntimePolicyValue order is EXACTLY: Model, Continuity, then every new runtime leaf in the table below, group order top-to-bottom and fields left-to-right. Metaflow and retained-family entries contribute ZERO variants. This is the authored variant ordering, not a promise of stable old bytes. The generator emits an ordered variant manifest beside the code; independent review compares it with this order and actual archive derives.

Retain allocated RuntimePolicy V1 only after actual evidence shows NO earlier candidate Memory bytes were written for this unreleased family. A worker statement/no known runtime effects is evidence to record, not universal proof. If earlier candidate bytes exist, stop writes and return the exact archive shape/data identity for a compatibility decision; no silent reuse, erase, or import. No051 import.

## COMPLETE approved new runtime-leaf inventory

Each comma-separated leaf below is a SEPARATE nullary Setting and one set variant, named by concatenating group and field (for example ReminderFirings). Its payload is the indicated approved semantic type. Every entry has Domain::RuntimePolicy and belongs to the restricted RuntimePolicyValue V1. Group products are not persisted or configured as a second authority.

| Group | Exact individual leaves and payload types |
|---|---|
| Reminder | Firings:ItemCount; Scan:DurationMilliseconds; StopPoll:DurationMilliseconds |
| Delivery | Payload:ByteCount; Deadline:DurationMilliseconds; ServingSlice:DurationMilliseconds; InterruptedReplay:DurationMilliseconds |
| Retry | FirstWait:DurationMilliseconds; LongestWait:DurationMilliseconds; Multiplier:RetryMultiplier |
| History | PageSize:ItemCount; Pages:ItemCount; RememberedTurns:ItemCount; ClaudeTail:ByteCount |
| Ancestry | Processes:DepthCount; Threads:DepthCount |
| Polling | HeartbeatConfiguration:DurationMilliseconds; AgentStop:DurationMilliseconds; CompactionWindow:DurationMilliseconds |
| Transport | CodexExchange:DurationMilliseconds; CurriculumExchange:DurationMilliseconds; HerdrPrompt:DurationMilliseconds; HerdrCall:DurationMilliseconds |
| Title | Attempts:ItemCount; Interval:DurationMilliseconds; PaneRest:DurationMilliseconds |
| Pane | SubmissionReads:ItemCount; SubmissionInterval:DurationMilliseconds; InterruptPresses:ItemCount; InterruptWait:DurationMilliseconds; ComposerLines:LineCount; StoppedRest:DurationMilliseconds; RetractionLines:LineCount |
| Frame | WebSocketHeader:ByteCount; WebSocketMessage:ByteCount; CurriculumReply:ByteCount; HerdrEnvelopeAllowance:ByteCount |
| Parser | StructuralNodes:ItemCount; StructuralDepth:DepthCount; DatomFormDepth:DepthCount; CompositionSteps:ItemCount; CompositionDepth:DepthCount |
| Launch | Herdr:ExecutablePath; FlowIdentity:ExecutablePath; Hook:ExecutablePath; ClaudeHome:DirectoryPath; FlowDirectory:DirectoryName; DefaultSession:SessionName |
| Effort | EffortPolicy:Vector<EffortSelection{Aspect,Layer,Effort}> (one validated complete twelve-pair declaration, approved existing table semantics) |
| ContextWarning | Share:ContextWarningShare{Numerator.Integer,Denominator.Integer}; Message:ContextWarningMessage.String |

Naming exception: EffortPolicy is the complete approved set variant, not EffortEffortPolicy. RetryMultiplier remains its payload type; its variant is RetryMultiplier. All numeric domains/actual widths, lexical paths, cross-field RetryFirstWait<=RetryLongestWait and exact native constraints remain those of accepted052-policy-validation. Duration fields are milliseconds, lines/bytes remain distinct; no guessed defaults. Warning share is exact rational0<N<=D, message literal/nonempty. No warning-only timeout is introduced. Core explicitly approves TransportHerdrCall for the actual same-Herdr call capability, resolved at the operation boundary; warning uses that capability's configured value.

### Removed or moved leaves — explicit accounting

- DefaultContinuity is REMOVED, not a row. Per-Address Continuity is separate; absent authorizes no idle close and does not block launch.
- Old RuntimePolicy product/singleton `policy` is REMOVED.
- FramePolicy.Nexus is external TranslatorConfiguration.FrameBytes, not a duplicate runtime row.
- TransportPolicy.SocketRead/SocketWrite are external translator ReadTimeoutMilliseconds/WriteTimeoutMilliseconds, not runtime rows. ConnectTimeoutMilliseconds is translator-only.
- Bootstrap five limits, client/composer/hook budgets and frame configuration are explicit translator/adapter-owned values, not Memory runtime values. Parser leaves above cover ONLY actual domain text work. Any former wire-only parser consumer moves outside core rather than causing a hidden Memory bootstrap dependency.
- Existing thresholds, model bindings, heartbeat recipients/period, lease, source root, profiles, endpoint/model sets, flags, leave-outs, investigation and minutes remain the existing authorities above, not duplicated leaves.
- Native fixed protocol widths, checked arithmetic and witnessed terminal/Herdr/textual-Codex constraints are not configurable leaves.

This inventory is complete against the accepted runtime-policy-shape plus later warning/ownership/Continuity rulings, not a claim all consumers are implemented. Actual newly discovered chosen policy must be named rather than defaulted or silently excluded.

## Bounded acceptance before affected bodies

Review input-to-enum/typed-identity/storage semantics and compare inventory against the listed accepted source documents. Then same writer implements local tooling+tests/package wiring only. Verify each entry's generated equality, all typed keys/removals, no duplicate active storage, restricted RuntimePolicyValue archive reachability, deterministic readiness deduplication and absence semantics. Compilation must use actual pinned Ethos/Rust; fixture/static assurances are not executed generation proof. No Meta publication until new immutable review passes. No new root/library/EthosZero release is needed.
