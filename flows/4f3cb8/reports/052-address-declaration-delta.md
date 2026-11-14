# 052 declaration changes by Address — bounded proposal

Scope: new living ruling, not yet body-authorized. The unchanged accepted052 implementation continues. Source ledger: `/home/li/primary/flows/2aed8d/reports/declaration-delta-existing-source-ledger.md`, SHA bcb33580eacbd68a287cef5d0229fe75e14d8cdc3cbe23e2de9abfbf6200b300.

## Exact operation vocabulary proposed

In existing meta `ConfigurationChange`, remove `Metaflows.Vector<ConfigureMetaflow>` and add:

```ethos
Metaflow.ConfigureMetaflow
RemoveMetaflow.Address
```

Keep the accepted052 `ConfigureMetaflow` payload including optional existing Continuity, root second, and every existing field. Keep `ConfigurationSnapshot.Metaflows.Vector<ConfigureMetaflow>`: it describes committed state, not a replacement operation. Keep existing `ConfigureOutcome.[ Replaced Unchanged ]` and reply wrappers `Configured`/`ConfigureRejected`. No second declaration API or aggregate setter survives.

`Configure.Metaflow` defines an absent Address or replaces the entire declaration at that Address. Equal value returns Unchanged; creation/replacement returns Replaced. `Configure.RemoveMetaflow` removes the one Address; present returns Replaced, absent returns Unchanged. This is idempotent set/remove semantics, not create-only/replace-only commands with invented existence errors. Core must judge these exact existence semantics before bodies.

Topic/payload validation remains typed and uses the accepted full resolved configuration rules. In particular both member continuity and default continuity unset is legal at Define; Launch refuses NotConfigured. No replacement operation resets fields of OTHER addresses.

## Startup and transaction

Startup's existing vector of per-value ConfigurationChange may contain multiple Metaflow/RemoveMetaflow operations. The generated conflict identity for both variants is the SAME typed declaration key containing Address. Two operations for one Address refuse, including equal repeats and set/remove conflict; vector order never selects a winner. Omitted Addresses preserve Memory. Other vector-family replacement semantics stay unchanged.

One store-owned mutation guard spans consistent snapshot, resolve, full validation, prepare and the existing single atomic commit. Set compiles to assert/mutate/no change at the one Address key; remove compiles to retract/no change. It must never call the current generic whole-family replacement helper that retracts omitted rows. Startup combines these with other settings/upgrades through the approved opening transaction. Failure before commit changes no logical rows; committed maintenance reporting remains as approved.

## Running flows and removal — proposed boundary

These operations change declaration configuration only. They neither retire, close, relabel nor displace a running flow, and do not release its address admission or alter a composed in-flight launch snapshot. Future operations resolve the now-current configuration through existing presence/absence rules; removal is not proof a seat ended. In particular removal does not implicitly force an active Maintained seat to OnDemand. Existing lifecycle operations remain the explicit way to stop/retire a flow.

The bounded source read found future declaration consumers at launching.rs229; waking.rs626,1471,1664; successor.rs174; metaflow.rs23; sending.rs544,1270,1406; lib.rs330. Independent delta review must check those concrete call sites against this boundary, including later wake/refresh after removal. If any current consumer would silently alter an existing seat's resolved continuity, surface that conflict before wiring; do not add a second stored declaration or a fallback to hide it.

## Persisted and generated reachability

The operation enum changes wire/generated meta Query/Response consumers, startup changes, dispatch, constructors and test producers. It does NOT change the ConfigureMetaflow payload beyond the already allocated member-Option delta. The exact frozen V5→V6 declaration family plan therefore remains; no additional version is proposed. Nexus-v4 and lifecycle/address-hold families remain unchanged unless actual transitive embedding evidence proves otherwise.

Direct persisted wrapper is StoredMetaMetaflowConfiguration in store/metaflow_declaration.rs21–45; historic V1–V4 and frozen V5 remain byte-exact. ConfiguredFamilies snapshot assembly is not archived. The direct-type query is NOT exhaustive transitive proof: independent review must trace ConfigurationChange/Query/Response archived consumers before declaring no further persisted family affected. No shared ordinary Refusal migration follows merely from this meta operation change.

Required coherent consumer edits: meta ethos/generated enum; normal lib.rs352–375 and configuration-only main.rs265ff dispatch; store configuration entry points and configure_meta_change8677ff; declaration validation and single-key planner; generated startup conflict-key mapping; snapshot remains collection; Nix startup declaration producers; capsule/configure.datom and Clojure configure-lines/configure!/on-demand-secondary/workspace-configuration/seat-declaration/takeover-configuration; configuring/rehearsing/secondary/store tests. Old-package takeover fixtures emit that OLD package's whole-family syntax explicitly; current052 producers emit only per-address operations. Never rewrite predecessor-produced compatibility bytes to new syntax.

## Independent delta tests/gate

- Define absent, replace unequal, equal no-op, remove present, remove absent; exact existing outcomes.
- Updating/removing A preserves B byte-for-byte and preserves B's active seat/transcript/continuity. Removing A does not itself end or reclassify A's active seat.
- Startup multiple distinct addresses atomically commit; omitted preserve; same-address duplicates/set-remove conflicts refuse with typed key and no mutation.
- Concurrent distinct-address meta changes serialize safely and both survive, without a shared operator declaration window. Same-address changes follow the actual serial commit order.
- Invalid one-address payload or invalid combined startup state refuses before logical changes; optional continuity domain absence still allows Define and refuses Launch.
- Snapshot/readback lists actual resulting declarations; whole-family setter no longer parses/dispatches in052.
- Rendered Nix/capsule producers use new syntax, exact old-version fixtures retain old syntax; all archived reachability and existing V5→V6 bytes/reopen oracles remain covered.

Request Core judgment on idempotent set/remove outcomes and lifecycle boundary, then a fresh independent DELTA review against this artifact and exact source ledger. No additional writer, broad inventory,051 API change or source body is authorized by this proposal.

## Core judgment and precise lifecycle qualification

Core approves idempotent Metaflow set/upsert and RemoveMetaflow with existing Replaced/Unchanged, snapshot vector retained, aggregate setter removed; duplicate/conflicting same-address startup operations refuse, distinct addresses share one transaction, omission preserves. Removing a declaration does not terminate its seat or rewrite already composed work.

The earlier lifecycle boundary is limited to the change operation's immediate effects. It does NOT promise a seat's continuity is forever frozen: later operations may resolve declaration/default under their existing explicit rules. Before this delta's bodies, the independent consumer review must specify the actual missing-declaration refusal for each future launch/refresh/wake path. No invented fallback, retained shadow declaration or duplicated policy is allowed. If an existing consumer silently defaults on missing declaration, identify its exact location and propose the minimal typed refusal using witnessed operation outcomes for Core judgment. The review must distinguish absence of a declaration from an existing declaration whose member and configured default continuity are both unset.

Fresh independent delta review of exact consumers, transitive archived reachability and all producers/tests remains mandatory before CoreSecondary body clearance. Unchanged accepted work proceeds.

## Independent gap closure proposed: declaration absence is not inheritance

Fresh independent review of09015ce4 found real production fallbacks. Proposed exact corrections, awaiting Core judgment:

| Consumer | Missing declaration | Present declaration |
|---|---|---|
| Launch composition, launching.rs227–238 / sending.rs542–550 | Existing `StartRejected(Undeclared)`; do not use SourceRoot as evidence that a declaration exists | `root_option=None` still uses configured SourceRoot; this is explicit root policy, not missing-declaration fallback |
| Refresh, waking.rs1471–1492 /1764–65 | Existing `RefreshRejected(Undeclared)`; remove reconstruction from predecessor LaunchProfile | Use current declaration and the already approved one-time continuity resolution; no change to previously composed work |
| Wake, waking.rs1471–1492 and496–524 | Existing `WakeRefusal::StartRejected(StartRejection::Undeclared)` propagated through existing typed retry/outcome machinery; never mislabel as Herdr refusal | Use declared settings; member/default continuity both absent remains a configuration failure, not Undeclared |
| successor continuity, store/successor.rs170–177 consumed waking.rs1713–1728 | Remove absent→OnDemand. Return typed absence to the operation so it selects its existing Undeclared outcome above | Resolve explicit member then configured default once; unresolved is the separately ruled configuration absence |

For present-but-unresolved continuity, Launch retains the explicitly ruled `Response::Refused(NotConfigured)`. Propose Refresh uses that same existing ordinary refusal where its response boundary already permits it; Wake retains its actual internal `CompositionRefused(Unconfigured)` and truthful retry projection unless Core requires a distinct mapping. Do not add a public refusal variant merely to equate internal and public names. Independent follow-up must verify each selected existing response constructor is actually reachable at that boundary before bodies.

Deleting a declaration therefore leaves the current native seat intact but denies future declaration-dependent launch/refresh/wake with truthful missing-declaration outcomes. There is no shadow declaration in a previous profile, no silent OnDemand substitution, and no automatic revival of removed settings. A configured default Continuity does not create a missing declaration.

### Additional exact consumers/test producers from independent review

- `flow-meta/src/main.rs311–319`: snapshot-to-Configure restoration must emit one Metaflow setter per observed declaration, not the removed whole-family setter. Restoration cannot infer deletions of unrelated existing addresses from omission; exact rollback that needs removal must carry explicit known per-address removals.
- `capsule/flow-capsule.clj1130–1148`: configure-line/broken-metaflows/restore-configuration must model per-address operations and deliberate invalid fixtures. Avoid a single family-line search/replacement that resets unrelated addresses.
- Rust constructor fixtures `tests/ending.rs110`, `refresh_and_compaction.rs113`, `refreshing.rs60`, `send_admission.rs368`, `waking.rs120/4033/5456`, and `lib.rs4365/4394/5649` require per-address semantic expectations, not just enum compilation fixes.
- Preserve earlier capsule/configure.datom and takeover producer obligations, with old package syntax retained only in explicitly historical branches/fixtures.

### Transitive archive result and remaining verification

Independent source review found ConfigurationChange/Query/Response rkyv wire archives but no Flow EngineRecord embedding. ConfigureMetaflow remains the sole directly persisted changed shared payload in StoredMetaMetaflowConfiguration; existing frozen V5→V6 plan applies. ConfigurationSnapshot is wire-archived; ConfiguredFamilies is not stored. No additional Memory version is evidenced. Add meta Datom+rkyv roundtrips for both new variants and unchanged snapshot, plus the already required predecessor-produced row/reopen fixtures. This is a bounded reviewed reachability finding, not a claim that nominal wire changes preserve old wire decoders.

Core must judge the above missing-declaration and unresolved-continuity projections, then the same independent reviewer re-pins this delta and closes its exact gaps before body clearance. No new architecture or wider inventory is requested.

## Controlling Core semantics for corrected independent re-pin

Core approves absence→Undeclared for Launch/Refresh/Wake, with predecessor-profile and absent→OnDemand fallbacks removed. Present root None uses configured SourceRoot. A present declaration with member/default Continuity both unset remains storable, but every launch-producing Refresh/Wake must refuse NotConfigured BEFORE successor creation or close effects. This supersedes any suggestion that an internal Unconfigured label alone establishes the required outward semantics.

Reuse existing typed wrappers only where exact generated contracts support those meanings. Do not extend shared Refusal for naming symmetry. If no supported wrapper can carry the required NotConfigured outcome at a particular wake boundary, report the exact missing variant/projection for judgment before any allocation/edit.

On either refusal preserve the held native seat and queued requests. Do not retire/reclassify the seat or drain requests toward a guessed successor. The independent corrected re-pin must verify actual generated projections and archived reachability plus ALL listed CLI/capsule producer tests before CoreSecondary clears these bodies.

## Minimal local Wake outcome extension proposed

The corrected independent packet proves the required Wake semantics are not representable today. `flow-nexus/ethos/operation` owns `Operation.Wake(Address)` and `Outcome.Woken(FlowId)|Failed(Failed_Data)`. Its generated Failed_Data has no Undeclared/NotConfigured carrier. Internal WakeRefusal only carries StoreUnreadable, NotAsleep, NothingQueued, SessionLive, HerdrUnreadable, Unplaceable, FreshNotStarted(Failed_Data), StartRejected(StartRejection), AwakeNotRecorded. Its current answer degrades Undeclared to Unstarted.

Propose ONE local reason type and one local outcome variant, authored in that existing operation namespace:

```ethos
DeclarationRefusal.[ Undeclared NotConfigured ]
; add to existing Failed_Data, preserving all other variants:
DeclarationRefused.DeclarationRefusal
```

The internal WakeRefusal gains a matching `DeclarationRefused(DeclarationRefusal)` carrier; AnswersWakeRefusal projects it exactly to `Outcome::Failed(Failed_Data::DeclarationRefused(reason))`. Missing declaration is Undeclared; an existing declaration with unresolved member/default continuity is NotConfigured. No shared signal Refusal or StartRejection variant changes. This local generated operation API changes coherently with its actual consumers under the allocated Flow0.52 package; no new Memory coordinate is proposed.

Perform declaration/configuration eligibility before successor/close or queue-drain effects. The local failure must be returned to the direct caller, not discarded as currently in sending.rs1323–28. For a queue-driving send, keep its already accepted durable delivery/queue state unchanged; expose/record the local wake refusal through the operation's truthful observation/diagnostic path without converting an accepted queued send into a false clean send failure. A later explicit wake/new normal trigger may retry after configuration changes; this delta adds no timer/retry loop.

Do NOT encode NotConfigured as shared `RetryCause::WakeRefused(StartRejection::Undeclared)` or `CompositionRefused(Unconfigured)`. Do NOT use terminal `DeliveryState::Failed(Refusal::NotConfigured)` merely because that existing variant can carry the word: it would change queued-request semantics. Retain pending requests on both declaration failures, without inventing a persisted retry marker. Existing non-declaration wake failures retain their existing retry machinery.

For a direct public operation whose response boundary supports the current ordinary Response, project Undeclared to its already existing appropriate StartRejected/RefreshRejected(Undeclared), and NotConfigured to existing Refused(NotConfigured). No blanket generic mapping is authorized: the independent check must enumerate actual direct Wake consumers and confirm which expose an ordinary Response versus internal Outcome versus already accepted queue result. The sending accepted-queue diagnostic path must be named concretely before bodies; this proposal does not authorize a fictitious public Wake response or a new journal schema.

### Archive evidence and tests

The bounded structural trace found no EngineRecord embedding of local Outcome/Failed_Data despite its rkyv derive. Shared DeliverySnapshot→DeliveryState→RetryCause DOES reach current/eventV5; shared Refusal also reaches send-outcomeV6. Leaving those shared types unchanged avoids those additional migrations. Verify local generated Datom/rkyv roundtrips and all exhaustive consumers; preserve existing frozen families and predecessor bytes.

Tests must demonstrate exact local reason, public projection where it exists, preserved seat/queue/accepted send, no successor/close/drain, and a successful later normal wake after configuration repair. No body grant follows from this proposal; request Core judgment on the local carrier and the unchanged pending-queue semantics, followed by exact consumer/projection re-review.
