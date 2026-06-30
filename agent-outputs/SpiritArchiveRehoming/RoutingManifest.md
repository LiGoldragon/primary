# Spirit Archive Rehoming — Phase 2 Routing Manifest

Record-to-home assignment for all 505 archived Spirit records, for the downstream append fan-out.

## Task and scope

Each archived record routed to exactly one append target by category and topic. Spirit-manual to a single surface; vocabulary-doc to the workspace glossary; code/config to its owning component config surface; architecture-doc to the owning repo's ARCHITECTURE.md by description topic. Records whose best home is a currently-owned/straggler repo (signal-criome, CriomOS, spirit-guardian-config, schema-cc, persona, lojix-cli) are parked in DEFERRED-TO-STRAGGLER. No content surface was edited; this manifest is the only write.

## Inputs consulted

- `/tmp/spirit-archive-extract/archived-spirit-records.dump.md` (505 records; local, non-committed).
- `/home/li/primary/reports/legacy-disposition/decision-surface-2026-06-26.md` (theme/component context for code/config and cloud/lojix routing).
- Repo ARCHITECTURE.md scopes for ownership boundaries (notably `repos/horizon-rs/ARCHITECTURE.md` §VM-hosting/cluster-data, `repos/CriomOS-home/ARCHITECTURE.md` §Spirit-archive/Rust-toolchain, `repos/nexus/ARCHITECTURE.md`, `repos/CriomOS/ARCHITECTURE.md` §metal/hostapd/node).

## Secret handling

Three ids are SECRET-FLAGGED and redacted in the dump: `go41`, `wn7q`, `2qhw`. They are referenced by id only; each carries a `[SECRET]` marker so append workers apply redaction. No secret values appear here.

## Volume table (target surface -> record count)

| target surface | count |
| --- | --- |
| `/home/li/primary/repos/schema-next/ARCHITECTURE.md` | 110 |
| `/home/li/primary/repos/spirit/manual.md` | 76 |
| `/home/li/primary/repos/nota-next/ARCHITECTURE.md` | 47 |
| `/home/li/primary/ARCHITECTURE.md` | 38 |
| `/home/li/primary/repos/spirit/ARCHITECTURE.md` | 29 |
| `/home/li/primary/repos/signal/ARCHITECTURE.md` | 22 |
| `/home/li/primary/repos/CriomOS-home/ARCHITECTURE.md` | 20 |
| `/home/li/primary/repos/criome/ARCHITECTURE.md` | 18 |
| `/home/li/primary/repos/schema-rust-next/ARCHITECTURE.md` | 16 |
| `/home/li/primary/repos/sema/ARCHITECTURE.md` | 13 |
| `/home/li/primary/repos/introspect/ARCHITECTURE.md` | 11 |
| `/home/li/primary/repos/upgrade/ARCHITECTURE.md` | 11 |
| `/home/li/primary/repos/horizon-rs/ARCHITECTURE.md` | 9 |
| `/home/li/primary/repos/sema-engine/ARCHITECTURE.md` | 6 |
| `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md` | 5 |
| `/home/li/primary/repos/mentci-egui/ARCHITECTURE.md` | 4 |
| `/home/li/primary/repos/nexus/ARCHITECTURE.md` | 4 |
| `/home/li/primary/repos/orchestrate/ARCHITECTURE.md` | 4 |
| `/home/li/primary/repos/signal-agent/ARCHITECTURE.md` | 4 |
| `/home/li/primary/repos/harness/ARCHITECTURE.md` | 3 |
| `/home/li/primary/repos/mind/ARCHITECTURE.md` | 3 |
| `/home/li/primary/repos/message/ARCHITECTURE.md` | 2 |
| `/home/li/primary/repos/terminal-cell/ARCHITECTURE.md` | 2 |
| `/home/li/primary/repos/arca/ARCHITECTURE.md` | 1 |
| `/home/li/primary/repos/forge/ARCHITECTURE.md` | 1 |
| `/home/li/primary/repos/router/ARCHITECTURE.md` | 1 |
| `/home/li/primary/repos/skills/ARCHITECTURE.md` | 1 |
| `/home/li/primary/repos/terminal/ARCHITECTURE.md` | 1 |
| **DEFERRED-TO-STRAGGLER** (parked) | 43 |
| **UNROUTABLE** | 0 |
| **TOTAL** | **505** |

## Glossary-surface choice

vocabulary-doc (12) -> `/home/li/primary/ARCHITECTURE.md` (workspace ARCHITECTURE.md). No dedicated glossary file exists (checked nexus, spirit, nota-next, schema-next); ESSENCE.md/INTENT.md are deprecated per decision 8rpu. The 12 records are workspace-wide canon: term/spelling canon (signal noun, sema, criome vs criomos, persona naming, three-part SCHEMA/SIGNAL/SEMA, Help-as-noun, schema-as-idea-language, STT sema normalization) and version/lane vocabulary (next/main/previous, version-pair, concept-designer lane, system-operator lane). nexus owns the Nexus request-record vocabulary, not English term canon, so nexus is the wrong home. The workspace ARCHITECTURE.md already hosts the naming-canon pointer and the workspace vision/intent surface, so it is the correct single glossary home.

## Assignments by target surface

### `/home/li/primary/repos/schema-next/ARCHITECTURE.md`  (110 records)

- `1aam` — schema as macro-language source of truth
- `1sa2` — schema/module-system namespace shape
- `20id` — single-type field syntax enum-variant
- `26e7` — contract-is-channel, per-channel schema files
- `2cuo` — type system struct/unit-variant reduction
- `2f04` — interface is root enum, Input/Output roots
- `2i75` — schema imports selective by name
- `2v9u` — three schema languages share 4-position shape
- `31nz` — schema lowering executor walks NOTA tree
- `3742` — type kind by delimiter, generics
- `3don` — schema lowering rejects duplicate declarations
- `3itj` — deep schema type trees, type index recursion
- `506w` — macros sugar in schema layer, enum homogeneity
- `58bv` — schema-next keeps one lowering engine
- `5jac` — camelCase fields vs PascalCase types
- `5mxn` — schema stack does not reference Nexus, MacroRegistry
- `6cfr` — Asschema IR removed, methods on schema-in-rust
- `6grf` — SpecifiedSchema IR canonical value
- `6jdv` — schema namespaces, module decomposition
- `6wwf` — schema purely positional, dot differentiator
- `7118` — plane payloads shed prefix, Input/Output naming
- `7c71` — structural-macro set as data, self-hosting
- `8u1o` — enum-encoded composite identifiers, multilingual
- `94sj` — DomainScope schema-emitted recursive enum, typed all-through
- `9uje` — schema headers are ordered enum-root declarations
- `9yxh` — append-only namespace, enum-slot upgrade compatibility
- `a5tg` — schema-types-centric design, no two fields share a type
- `b05y` — schema handles workspace Rust subset, no tuples
- `b0s4` — resolve enum-vs-macro paren ambiguity with discriminator
- `b0v3` — schema files use dot-schema extension
- `ba6d` — pipe-brace traits/impls as data catalog, method calls
- `bkzd` — define AssembledSchema first, TypeReference/TypeDeclaration sums
- `brgo` — streaming full schema-derived push, event/stream root
- `bw9v` — schema files carry structure not explanatory comments
- `c8b3` — component derives internal effect + external wire vocab
- `c8lc` — schema namespaces use maps, nested type namespaces import
- `cbtg` — schema daemon resolves/caches namespaces, precompiled-schemas runtime arm
- `d3r2` — component code-generation, opt-in Deref/VariantMatch, pipe-brace
- `d6if` — micro-macros small composable named macro units
- `ddlv` — every component repo gets concept schema file v0.1
- `dqmc` — schema-next bare @-sigil type derives binding name
- `e8iu` — macro-node binding-and-reference sigil, single-object sugar
- `er9w` — schema is programmable composability layer over NOTA
- `esn1` — schema header variant references resolve namespace/inline
- `f8ds` — component triad split, Signal in contract repo
- `fhe8` — schema root type is message surface, colon-path imports
- `fry8` — schema variant namespaces reserve numeric ranges, input/output tag-space
- `g2xr` — schema self-hosting all-the-way-down, schema-of-schemas
- `gjr1` — separate categorical KIND from additive CAPABILITY vector
- `h053` — one typed noun per semantic object, SpecifiedSchema projections
- `h9xd` — schema examples include multi-variant headers
- `hckx` — schema-stack presentations show schema-to-interface path
- `hl1z` — schema declares data types only, no effects
- `hrte` — schema root header bare PascalCase Input/Output names
- `i8wt` — schema declares roots at one point, free-datatype namespace
- `i9xk` — runner concurrency is runtime config, contract no parallelism
- `iypq` — built-in type-name vocabulary in Schema not NOTA
- `izib` — Domain subdomains mandatory to leaf, DomainScope prefix language
- `kfqa` — schema reader multi-pass NOTA-first, NotaValue tree, codec
- `khbv` — schema language self-describing, schema-library bootstrap namespace
- `l1ip` — schema root struct shape known from root KIND, positional values
- `l6zw` — component contract carries only wire vocabulary, Nexus/SEMA internal
- `lf7y` — assembled schema reserves scalar pass-through type references
- `m76h` — schema header declarations first drive dispatch triage
- `mcuk` — .schema header-first sections, positional input/output bodies
- `mimk` — reactive schema extends base schema, plane reaction surface
- `mn3k` — domain relations first-class taxonomy schema surface
- `mqlb` — move schema declaration into NOTA-format language, codegen slots
- `neib` — new schema stack clean repository names acceptable option
- `nm97` — external vs internal schema categories, one channel each
- `o8x5` — daemon three execution centers Signal/Nexus/SEMA trait order
- `oe6s` — double-wrapped Input/Output form denied under macro grammar
- `ooxy` — full request pipeline Signal-Nexus-SEMA, rolling origin identifiers
- `ospz` — schema patterns emerged in Aski language, aski-core triad
- `oxgh` — schema IR struct key-value brace, visibility-tagged declarations
- `p8sq` — .schema file reads in known Schema context, positional fields
- `ppuk` — schema macro expansion ends AssembledSchema, pure NOTA-representable
- `pul9` — macro dispatch two-phase structure-match then per-shape
- `qe84` — schema macros compose from reusable micro-macros
- `qv4q` — schema file root identity from filename, spirit.schema
- `rfg9` — schema macro resolution closed macro space, dual dispatch
- `rmqo` — sectioned three-part schema structure and headers
- `rmv8` — three plane schema types Signal/Nexus/SEMA
- `sanf` — bootstrap schema-schema macro interface
- `sd7x` — AssembledSchema macro-variant lowering engine
- `str0` — engine method-count-matches-wire-events spec
- `t5wx` — schema-codegen closed, integration/migration phase
- `tace` — schema as Cap'n-Proto superset spec language
- `tbff` — shallow inline declarations promoted to namespace
- `tw15` — Technology hardware/software domain-vocabulary split
- `udjq` — schema effect-table closed message-to-effect mapping
- `ugig` — schema root Plane data-carrying enum
- `ujb2` — seven-root-variant component surface ceiling
- `umsv` — everything-is-a-struct foundational schema model
- `uuh7` — enum recompile trivial, zero-downtime upgrade goal
- `uujd` — schema names refer to typed declarations, dependency-ordered
- `uzxp` — precompiled schema library, implicit core namespace
- `w6y1` — schema header is public type-level interface
- `wvpg` — enum-of-enums two-layer variant structure
- `wx5c` — core macros always imported, user macros lazy
- `xbc2` — schema files as strict typed interface contracts
- `xbu8` — schema component full triad daemon
- `xiqa` — typed error/help in domain enum for empty cells
- `xprx` — push repetition into schema macro
- `xqkv` — optional trace-instrumentation build surface
- `ycmd` — hand-Rust only engine logic, structural emits from schema
- `ymq8` — authored-schema declaration forms
- `yngr` — single-owner consensus before storage mutation
- `yp29` — Bytes primitive and hash-identifier type
- `z9kv` — schema Kind enum over three planes

### `/home/li/primary/repos/spirit/manual.md`  (76 records)

- `0fmg` — Spirit-facing skills (skills/spirit-cli.md canonical, intent-log.md points there
- `0s5u` — Guardian training starts as a decision-log flywheel: every gated decision record
- `0xqp` — Running a Spirit Observe is standard routine practice, not optional: agents obse
- `1rcj` — Subagents that need to understand a domain, referent, or unknown named thing beg
- `29ed` — A registered but undelegated domain name returns a typed no-records result.
- `2gj4` — Add an auditor role that closes the loop back to designer — mostly mechanical (d
- `2o5j` — The active agent role is the topic of the psyche window
- `2st7` — Spirit pilots Criome-backed operation authorization as observability/tracing sca
- `2vp2` — Distinguish a lean-pending-information from a ratified Decision: a psyche statem
- `3jkx` — Spirit record identity uses a random/opaque hash, not a content-address fingerpr
- `3pfh` — Spirit archive semantics (meta-signal Configure ArchiveTarget) are redirect-forw
- `3v3r` — Spirit exposes a single guarded CollectRemovalCandidates Signal-root operation t
- `3w61` — Spirit random identifier codes should use four characters as the minimum display
- `5g5h` — Spirit needs a real in-place record mutation path so an existing intent record's
- `5tar` — An agent educates itself in a domain before submitting intent into it: query and
- `5trg` — Spirit record identifiers must not be reused after removal; reuse makes referenc
- `69fa` — The main thread is the most precious context: the early high-fidelity window (th
- `6kfz` — A Spirit short identifier is the shortest-unique base36-lowercase prefix of the
- `7mvx` — Spirit's intent gate / guardian runs a strong (open-weight if self-hosted, provi
- `80zj` — Agent workflow should favor fresh sessions over context compacting: the psyche c
- `853n` — Spirit record identity is a stable, non-reusable, opaque random handle assigned
- `8jtz` — Spirit ordinary agent-facing replies should not include database markers; databa
- `8l2a` — Spirit must handle concurrent capture of the same psyche prompt across multiple
- `8rpu` — All intent is driven from Spirit: the static intent files — ESSENCE.md, the work
- `9c6f` — Spirit provides RecordDefault, a short-form recording op taking only commonly-cu
- `9huv` — Agents using Spirit must track the DEPLOYED version's wire interface, not curren
- `a3l4` — Provenance and agglomeration are expressed through a relations field on records
- `arb2` — Long-term intent-recording direction: spirit-CLI-driven intent-recording-of-role
- `bwxn` — Spirit should not call the referent guardian when a referent registration reques
- `ca65` — Skills should instruct agents to use the unsuffixed spirit CLI for normal intent
- `cws0` — Deployed Spirit can REMOVE intent records, superseding the append-only/flag-only
- `dfii` — Spirit guardian rejection replies are remands that name the coherent repair shap
- `ek8w` — Intent agglomeration and refresh is triggered by an automated auditor that auto-
- `f5jr` — Each V2 generated worker role packet carries enough bundled, curated critical do
- `fiw4` — Versioned CLIs need an active-version selector. Spirit exposes version lookup as
- `g78b` — Refresh intent before maintenance or implementation. Refresh intent means the ag
- `g8ln` — If a separate weight axis is added, it uses the same qualitative Magnitude ladde
- `h7sz` — Spirit should gain a ChangePrivacy operation mirroring ChangeCertainty — change
- `hgvg` — Cite a Spirit intent record in prose by quoting its description summary literall
- `hvfe` — Manifest the recurring architecture patterns across active worktrees, primary sk
- `icpa` — Spirit's overriding design goal is to be maximally clutter-free, a curated prist
- `j6r4` — Spirit certainty follows an honest 8-level magnitude rubric. Maximum only for fo
- `jn3m` — Spirit profile defaults must not cut over to a new versioned database until exis
- `k12x` — Spirit gets an explicit capability to remove intent entries beyond supersession/
- `kasm` — Spirit capture is a blocking guardian gate, not an advisory check: the guardian
- `kfon` — Content-extracting/emitting Spirit operations accept a customizable output-targe
- `kg2z` — Spirit CLI invocations default to inline NOTA wrapped in shell double quotes; th
- `mlq0` — Spirit operations should report outcomes with self-describing NOTA enums and str
- `nob8` — All is a complete leaf domain value available at every level of the domain tree
- `nr7h` — Spirit guardian admits intent captures whose operative guidance states the affir
- `oj3i` — Zero certainty is the removal-candidate state: a Zero record has no value and mu
- `opbj` — Re-importing vetted records into a fresh Spirit database needs a privileged meta
- `otel` — Intent capture should be denser and less verbose: durable records preserve the c
- `qr5o` — The closed Domain taxonomy is the broad-routing layer only; fine-grained specifi
- `qy15` — Private intent capture gains an explicit named short-form (e.g. RecordPrivate/Re
- `rh29` — Spirit record acceptance replies should display the shortest collision-free lowe
- `rvnf` — Agents must not respond to Spirit overcapture by avoiding Spirit entirely; the c
- `s0wd` — Preferred topology: one designer + one operator double-lane per workspace, commu
- `sn1g` — Spirit may expose common search paths as explicit low-level shorthand Signal ver
- `t4uq` — Spirit entries carry exactly two orthogonal axes: Certainty (confidence the stat
- `tf2o` — Intent refresh and agglomeration is primarily agent behavior trained through a s
- `tfpd` — The guardian judges a proposed intent change against the actual verbatim words o
- `tw81` — The Spirit short identifier (returned by the tool and cited in chat) is the shor
- `uara` — Spirit topics are user-creatable single strings — broad atomic single-word conce
- `urnt` — Psyche-facing agents must keep intent-logging guidance fresh in context, and usi
- `vjye` — Spirit metadata rungs use both direct psyche declaration and argued evidence. Wh
- `x1rz` — Spirit write acknowledgements are token-cheap: creation returns only the created
- `xblw` — The Spirit skill manual half — what Spirit and intent are, the CLI and wire shap
- `xf25` — Spirit without a configured guardian fails closed rather than accepting ungated
- `xpen` — Spirit should support agent catch-up queries from a recorded time so agents can
- `y212` — Current reporting protocols stay in force where required, while intent-led orche
- `ywua` — Spirit categories are an open curated vocabulary that may grow to hundreds of sp
- `z3ka` — Intent capture is modeled as a court of law: the submitting agent advocates, psy
- `zjho` — Spirit is a universal intent tool for every human, not bespoke to one psyche or
- `zjop` — Per-role model selection — agent roles map to the best-fit LLM models. Claude is
- `ztX` — Agents must not respond to Spirit overcapture by avoiding Spirit entirely; the c

### `/home/li/primary/repos/nota-next/ARCHITECTURE.md`  (47 records)

- `0dsr` — NOTA bare-atom delimiter rules
- `2dzp` — NOTA composite type constructors Vec/Option/KeyValue
- `3naf` — NOTA encoders avoid over-bracketing
- `3qjw` — NOTA four-char bracket-pipe multiline string
- `3sq4` — known-enum slot omits enum type name
- `4itr` — everything serializable data, macro-as-data
- `5myr` — NOTA namespace section key-value map
- `5p9s` — NOTA formatter derived from macros
- `61lk` — NOTA+schema pure data spec, half-step to Sema
- `6oun` — three NOTA delimiters map to schema sections
- `7rrs` — NOTA inline-string square-bracket block-string
- `7y8w` — NOTA bracket-only string embedding-safe
- `8p0r` — trace events render as NOTA at client edge
- `a9sq` — rkyv single encoded form, NOTA text projection at CLI edge
- `b1vi` — text/binary boundary in client, daemons NOTA-free
- `bexd` — component feedback as typed self-descriptive NOTA enums
- `bhs5` — NOTA block-string bracket-pipe form
- `cyik` — NOTA encode/decode derives optional, daemon-only binary-only
- `f8m3` — NOTA two bracket-string forms, inline and block
- `fo38` — macro application and enum declaration grouped form
- `fvtf` — NOTA classification qualifies-as not is, promote-at-parse
- `ghw7` — NOTA brace strict key-value map, typed enum keys
- `h6fh` — Macro declaration NOTA syntax, positional record form
- `hc0t` — assembled schema canonical NOTA-and-rkyv typed codec
- `hetk` — Help retrieval always one NOTA argument, signal-channel auto-wire
- `laim` — NOTA bare-atom punctuation set, double-semicolon comments
- `n5ch` — NOTA mirrors rkyv root + relative-pointer box layout
- `o2xk` — CLI-with-NOTA forces binary daemon protocol
- `oqwb` — NOTA enum variant optional empty payload renders data-carrying
- `own9` — @-binder surface abandoned, positional bracket/brace form
- `pmg5` — TraceEvent transparent newtype, single object shape
- `qw1j` — brackets are vector delimiter, never redefined as struct
- `r0le` — each symbol fully-qualified SymbolPath, NOTA renders at edges
- `rnrg` — NOTA typed-text reliability rationale
- `sqx6` — NOTA owns structure, schema owns type-name vocabulary
- `t4gd` — daemon binary NOTA-free, text-edge codec only
- `ur16` — daemon startup one rkyv Configure message
- `v0n6` — typed structural macro nodes over raw parser
- `vfjw` — NOTA strings come from bracket forms
- `voa8` — square brackets raw vector vs Vec declaration
- `vqbt` — plural record replies expose vector directly
- `vr32` — NOTA positional structs, no field tags
- `wqdi` — flat positional multi-argument type references
- `xai7` — type-directed structural macro node matching
- `ychx` — bracket semantics parens-enum brackets-struct
- `ydpa` — macro loading index-then-lazy-resolve passes
- `zg84` — assembled-schema Public/Private visibility variant

### `/home/li/primary/ARCHITECTURE.md`  (38 records)

- `06l6` — match-matrix engine design, cross-component principle
- `1i1b` — 'signal' noun ambiguous: rkyv binary vs NOTA text, disambiguate
- `2foy` — content-daemon privilege boundary principle
- `3chp` — meta-socket naming for triad components
- `3d5z` — runtime logic triad Signal/Nexus/SEMA roles
- `4oev` — no NOTA between components, CLI text edge
- `4vde` — SEMA is the compact data format defined by schema
- `54g9` — async actor interaction with Criome authorization
- `62r4` — separate repos for nota/schema/schema-rust-next
- `7d4x` — components must drive live system end-to-end
- `7sx6` — component-triad two-contract pattern, meta-signal canonical
- `8koe` — Help is a noun (documentation entity), not a verb
- `8y24` — every actor has channel-contract schema, ACTION/RESPONSE
- `96mi` — triad-runtime actor-vs-Tokio-task wording discipline
- `9v7h` — SO_PEERCRED owner-socket auth via triad-runtime ConnectionContext
- `ahop` — counselor/assistant pair like designer/operator, private affairs
- `beue` — concept-designer is ephemeral occasional invocation, not persistent lane
- `bnxx` — engine-manager canonical short name is Persona; repo/binary naming
- `cgd8` — daemon configuration via meta-signal socket, verbs in meta-signal
- `cx2m` — criome (auth) vs criomos (OS) spelling; mentci canonical
- `d2ql` — system-operator is operator lane for psyche-directed production code
- `fwme` — schema is textual representation of psyche idea language
- `g31j` — component binary naming <component>/<component>-daemon convention
- `go9u` — LLM prompt prose in plain-text files, include_str at build
- `hp9n` — repos directory stays untracked local symlink index
- `k6w1` — daemon concurrency primitive in shared triad-runtime
- `kmhb` — version-pair vocabulary: current/main vs proposal/dev/next
- `l3ca` — per-role role-space sub-workspace Git repo, push-gated by SSH key
- `ng1x` — roll workspace forward, migration removes superseded path
- `ngk0` — workspace version vocabulary NEXT/MAIN/PREVIOUS, from-chain
- `pb1g` — every component meta slot, signal/meta-signal repo split
- `plum` — fully-qualified-symbol-path universal machine-readable identity, ESSENCE/ARCHITECTURE
- `ppp4` — shortest reliable identifier first-class, blake3 locator shortened
- `qerc` — three-part vocabulary SCHEMA/SIGNAL/SEMA spec/transport/state
- `qxye` — Bird/Aether has forked workspace and soul repositories
- `ssk2` — two-contract triad two-authority-surface pattern
- `tnam` — STT may hear sema as sim, normalize to sema before storing
- `zgwf` — primary gitignored top-level private-repos directory

### `/home/li/primary/repos/spirit/ARCHITECTURE.md`  (29 records)

- `081i` — domain-vocabulary hierarchy structural nesting
- `0dys` — Spirit operation variant ladder short/complex roots
- `2rb7` — domain names self-explanatory, no gloss layer
- `34hu` — DomainScope typed nested prefix of Domain enum
- `42rh` — intent unit is domain, closed enum
- `4wt3` — domain vocabulary variable-depth tree
- `5fck` — trace optional compile-time, NOTA build-config
- `70gd` — production orchestration relies on Spirit not Mind
- `8rew` — Spirit small-record type, CollectRemovalCandidates
- `9npk` — rename persona ancestry away from Spirit, core terminology
- `beaj` — no daemon-side printline, typed trace interface only
- `cx7y` — Spirit archive storage daemon-derived default path, configurable
- `dun9` — Spirit as federation of key-gated GoPass stores, crypto-shred
- `ef6i` — near-term mentci/spirit/criome milestone, trace before blocking
- `ezcy` — canonical Spirit record one uniform shape, no per-kind variants
- `k5y3` — Spirit privacy is Magnitude on privacy axis, Zero=public
- `lw73` — Spirit ordinary/owner sockets, versioned sockets, signal-version-handover
- `lxo3` — Spirit RecordQuery composes filter dimensions, RecencySelection
- `ozbz` — Spirit identifier migration data stored as NOTA not SEMA
- `p6k5` — persona-spirit deployed production, spirit-next schema-derived pilot
- `q4l0` — data-lifecycle ladder closed set on schema-derived spirit
- `qbx7` — Spirit timestamp daemon-stamped
- `sqrk` — Spirit observation intelligent topic retrieval
- `t0tu` — migration as logged fold over version chain
- `w1ss` — in-process versioned reads daemon migration
- `w54p` — Spirit verbal depth scope vocabulary
- `xhwa` — spirit 1-of-1 local criome-gating production target
- `xnnb` — intent recorder voice-recognition psyche cutoff
- `ypb5` — Spirit record privacy Optional field

### `/home/li/primary/repos/signal/ARCHITECTURE.md`  (22 records)

- `07pn` — origin-route return-address metadata across planes
- `2qia` — root signal enum input/output 8-bit header
- `3got` — Communicate wire trait rkyv signal-frame mail-queue
- `44dp` — short-header 64-bit micro-message structure
- `5fdr` — Signal is NOTA-free, binary/rkyv only
- `cqxg` — 64-bit signal root-verb namespace per-component, SignalCore zone
- `d5v6` — universal Magnitude type in signal-core/signal-sema, eight variants
- `dcqz` — wire-header pattern extension, Tier1 micro-header prefix, tap-anywhere
- `isia` — component CLIs complete typed text edge, signal-backed
- `jl3k` — wire protocol is Signal Protocol, universal mail mechanism, correlation-ids
- `lvy9` — real-time streaming new Signal capability signal-real-time
- `pdbn` — root signal object carries signal-frame protocol, rkyv dispatch
- `q33b` — owner/permission distinction as Permission variant, two-socket current
- `r2jx` — signal-frame protocol declarative root-level schema, imported
- `sjcy` — CLIs are thin Signal clients
- `sqnx` — Signal Core namespace concept retained
- `u7fj` — signal engine is message triage only
- `u7tj` — .schema files live with contract source-of-truth
- `wv2a` — 64-bit short header per-message prefix
- `x2yz` — per-repo signal-X versioned schema libraries enable recovery
- `yzwg` — universal primitive variants pre-allocated across namespaces
- `zrrv` — daemon multiple signal surfaces via root enumerator

### `/home/li/primary/repos/CriomOS-home/ARCHITECTURE.md`  (20 records)

- `11m7` — Claude Code/Codex/Pi updated together via CriomOS-home lock
- `1vj5` — DJI mic/PipeWire desktop-audio path
- `4fao` — DJI microphone keepalive for STT
- `51u8` — Pi extensions packaged declaratively via Nix flake inputs
- `87ts` — Android Criome WiFi name resolution
- `9xwr` — nix-managed Emacs .eln native-compile at build
- `bc6f` — Bird Zeus crayon-os home-profile redeploy, root SSH
- `bdse` — Playwright Chrome extension token in gopass, browser wrappers
- `bev5` — Home-profile activation persists across reboot, keeps session
- `go41` [SECRET] — SECRET; secret paths scoped to served resource zone
- `jtos` — cluster Rust toolchain newest nightly pinned via fenix lock
- `mz16` — desktop/resource-safety research first, smallest safe session-preserving
- `ok16` — core interactive programs higher CPU/IO priority, rescue terminal
- `p675` — recording-system laptop-mic to large-ai-node hop explicit
- `qmsh` — firmware gating reuses existing policy, no broad Horizon schema
- `ud6l` — Bird/Zeus update authority uses LiGoldragon main default
- `vgon` — Syncthing excluded from phone media mirror, Immich uploader
- `wp91` — pi-subagents extra subagents mined selectively, case-by-case
- `wvgh` — three-tier browser control on CriomOS AI node
- `zdie` — CriomOS builds Spirit startup archive at Nix build

### `/home/li/primary/repos/criome/ARCHITECTURE.md`  (18 records)

- `32wj` — Criome error-kind subtype development
- `3fm6` — agent cryptographic identity via Criome master key
- `7let` — criome/lojix cluster VM test substrate, spirit gate
- `a4i6` — per-agent Criome identity, per-Unix-user daemon trust boundary
- `ay3y` — criome decentralized quorum-attested crystallized-time AttestedMoment
- `burk` — criome daemon peer discovery and node indexing
- `crlc` — domain-criome content-addressed DNS authority for .criome domains
- `dx10` — agent short identifier from Criome master-key prefix bytes
- `ermr` — criome cluster-root identity signs member keys, RegisterIdentity
- `i6ih` — Criome stack last-known-acknowledgment quorum-of-agreement state
- `ic4o` — criome guard workflow trust two planes, quorum co-signatures
- `lt44` — CriomOS two transport lanes, Router general, criome auth-only peer
- `m3ms` — criome universal guard substrate, typed policy language, orchestrate executes
- `mzfj` — first criome quorum contract mirrors SSH authorized-keys, one-of-any
- `p43g` — criome owns key custody, authorization decider, SO_PEERCRED submitter
- `psc6` — criome daemon encrypted multi-key store, master BLS, self-start key
- `pviw` — Telos umbrella, criome agreement organ, quorum primitive, BLS verdicts
- `z9d6` — content-addressed composable Criome authorization contracts

### `/home/li/primary/repos/schema-rust-next/ARCHITECTURE.md`  (16 records)

- `3nla` — InteractTrait retracted, no emitted Interact traits
- `4d8f` — regenerate emitted Rust on schema change
- `4np2` — schema-to-Rust lowering token-based quote
- `5zgi` — emitter consolidates same-shape sibling variants
- `6th4` — schema help hybrid catalog, emitted accessors
- `77i8` — single macro emits all Rust+NOTA+rkyv
- `bkcd` — rkyv universal wire base, NOTA codec opt-in per consumer
- `bybe` — newtype assembled-schema single-element brace, NotaTransparent emit
- `czw0` — schema source carries triad engine mechanism, generated glue
- `gb3d` — AssembledSchema public-vs-local visibility preserved in Rust
- `l8ox` — lowered output fully-qualified identifiers, import clashes error
- `lk22` — generated Rust one module per schema file, colon separator
- `m91k` — signal/sema macro derives wire layer, Tier1 header, VersionProjection
- `ntsg` — each Rust crate schema folder lib.schema entry, crate-name imports
- `sarw` — Rust alias-vs-newtype emission rules
- `zjmc` — schema-derived triad engine canonical mechanism

### `/home/li/primary/repos/sema/ARCHITECTURE.md`  (13 records)

- `0yx5` — version-control mirror component triad
- `29pb` — component Sema databases versioned atomic durability
- `edqu` — contract schemas content-addressable layout for rkyv migration
- `gvgu` — rkyv storage headroom enables zero-cost migration-free changes
- `i4ak` — reusable component version-control, branch/fork/rebase/merge policy
- `iir4` — versioned operation log authoritative, redb materialized view
- `py4h` — upgrade mechanisms live typed SEMA operations on schema, diff families
- `qkrg` — archive system specialized sema-database, CollectRemovalCandidates
- `rj9y` — tailnet version-control mirror transport in triad-runtime
- `twlp` — archival lowering before deletion, privacy preserved
- `wrjl` — content-addressable schema-layout migration index
- `x0ja` — blake3 + Criome BLS cryptographic basis for version-control
- `ycwf` — name persistent store the SEMA database

### `/home/li/primary/repos/introspect/ARCHITECTURE.md`  (11 records)

- `4frx` — trace-client library, generic CLI trace-siting
- `bwid` — trace COMPACT vs EXTENDED variant-chain forms
- `cd76` — persona-introspect home for cross-version error logs, Pi capture
- `jaz4` — trace events persisted to purpose-built SEMA trace store
- `js6b` — trace client behavior in reusable library, thin CLI wrapper
- `m5jl` — tracing schema-defined closed enum vocab, macro-emitted names
- `q13r` — tracing in schema-generated engine traits default no-op
- `rpog` — queryable tool-call trace as agent persistent memory
- `so0p` — introspect as configurable trace destination
- `tdfp` — per-crate trace enablement, tracing untraced
- `tpvu` — CLI as log surface in testing mode

### `/home/li/primary/repos/upgrade/ARCHITECTURE.md`  (11 records)

- `5cyn` — schema-diff drives upgrade trait, VersionProjection
- `7tqc` — daemon boilerplate to libs, version-projection crate
- `88eq` — upgrade substrate Nix-flake versions, content-addressed
- `9pil` — schema changes via upgrade-testing pipeline, disposable db copy
- `c6j4` — schema diffs infer standard migrations, ambiguous need annotations
- `c9fv` — schema migration prerequisite for every persona triad redb
- `i1jw` — next-version failure, main recovers caller intent via partial-application
- `lilh` — dual-version upgrade replies distinguish old/new db write failures
- `rq3p` — emit observable event on accepted version upgrade
- `thi1` — schema and upgrade carry explicit provenance
- `tmji` — sema-upgrade universal stateful schema-upgrade component

### `/home/li/primary/repos/horizon-rs/ARCHITECTURE.md`  (9 records)

- `1924` — editor selection is horizon user-preference data
- `242o` — ouranos swap/zram via cluster-data + Horizon projection
- `a2t4` — Horizon expresses WHAT not HOW, input=output type reuse
- `iwbt` — cluster config carries public-domain mapping, criome.net
- `q4gd` — horizon node model derives facets from typed source enums
- `qkvx` — type end-to-end never string-keyed, NodeService enum, SymbolPath
- `rxcp` — raw/pretty horizon split for lojix-next stack
- `tdvr` — VmHost typed resource limits, lojix runtime ledger
- `y1v5` — VM-testing node feature is cluster-data-generated

### `/home/li/primary/repos/sema-engine/ARCHITECTURE.md`  (6 records)

- `2uhh` — IntakePolicy universal admission interface
- `7l7l` — Sema classification vocabulary internal, off wire
- `duis` — sema short header symmetric with signal, tap-anywhere
- `en7k` — splitting SEMA out of daemon is distant-future only
- `fosp` — sema-engine exclusive DB boundary, single-writer, redb
- `y3ag` — durable write reply reports persistence outcome

### `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md`  (5 records)

- `7x5z` — mentci universal component-general UI surface
- `80bl` — Mentci observation surface querying introspect
- `jwm9` — Mentci-lib async engine layer, actor system, Nexus/SEMA, Android-portable
- `mu0o` — mentci stack toward deployed observation/debugging/approval console
- `xk7f` — Mentci prompt-to-bead-weave harness routing

### `/home/li/primary/repos/mentci-egui/ARCHITECTURE.md`  (4 records)

- `cok7` — Mentci GUI theming follows system light/dark theme
- `nc9k` — mentci-egui controlled through shared signal-mentci-client contract
- `xen8` — mentci-egui socket displays component/authority identity
- `xlrk` — mentci-egui interactive GUI client for daemon

### `/home/li/primary/repos/nexus/ARCHITECTURE.md`  (4 records)

- `fcsg` — Nexus schema-defined decision/effect language, NexusEffect variants
- `fuls` — Nexus inner recursive runtime engine, backpressure scheduling
- `vdiu` — Nexus slim acknowledgement output
- `z6qu` — Nexus interface as engine internal feature catalog

### `/home/li/primary/repos/orchestrate/ARCHITECTURE.md`  (4 records)

- `5d5o` — orchestrate kept on current triad/signal/sema
- `irmw` — persona-orchestrate lane registry NOTA vectors, base discipline last
- `potn` — dynamic topic-named lanes orchestrate model, discipline metadata
- `udgu` — lane/claim management via orchestrate daemon CLIs

### `/home/li/primary/repos/signal-agent/ARCHITECTURE.md`  (4 records)

- `7yth` — persona-llm-client becomes agent component triad
- `f8k7` — agent models LLM providers as generic OpenAI-compatible API
- `gdbf` — agent component over harness backends, LLM-API-call component
- `l0w8` — LLM calls computation units, provider fallback chain, criome escalate

### `/home/li/primary/repos/harness/ARCHITECTURE.md`  (3 records)

- `eo25` — Pi harness compaction-abort recurring reliability problem
- `hqg7` — harness production one daemon owning multiple instances
- `s8lq` — browser automation attach-to-visible-tab for secrets

### `/home/li/primary/repos/mind/ARCHITECTURE.md`  (3 records)

- `wgii` — persona-mind typed agent-error event logging
- `wl2a` — agent memory defaults to shared system
- `x92t` — role-vector-driven skill loading via persona-mind

### `/home/li/primary/repos/message/ARCHITECTURE.md`  (2 records)

- `alom` — message owns EXISTENCE fact, router owns delivery
- `q73w` — message lifecycle hookable MessageSent action at sent boundary

### `/home/li/primary/repos/terminal-cell/ARCHITECTURE.md`  (2 records)

- `of73` — terminal-cell abduco per-application wrapper, process-per-app
- `ux9i` — terminal-cell lifecycle ownership three-way split

### `/home/li/primary/repos/arca/ARCHITECTURE.md`  (1 records)

- `i1b5` — ARCA performs database migration on format change, mandatory cascade

### `/home/li/primary/repos/forge/ARCHITECTURE.md`  (1 records)

- `gopu` — Forge build-system family, forge-nix-builder wraps Nix

### `/home/li/primary/repos/router/ARCHITECTURE.md`  (1 records)

- `57f9` — Router routing protocol, criome/mirror fan-out

### `/home/li/primary/repos/skills/ARCHITECTURE.md`  (1 records)

- `dfl5` — skills generator V1 active NOTA manifest, module dependency index

### `/home/li/primary/repos/terminal/ARCHITECTURE.md`  (1 records)

- `f8tb` — terminal-control program-agnostic session-control component

## DEFERRED-TO-STRAGGLER (parked until owner/straggler clears)

These records' best home is a currently-skipped repo. They wait; the intended target is named per record.

### intended: `repos/lojix-cli`  (18 records)

- `150a` — cloud provisioning DO/Hetzner (intended: lojix-cli)
- `16l0` — cloud flarectl runtime-dep makeWrapper (intended: lojix-cli/cloud)
- `2alg` — lojix deploy daemon concurrency (intended: lojix-cli)
- `2qhw` [SECRET] — SECRET; lojix-daemon GitHub auth (intended: lojix-cli)
- `5pf6` — cloud node low trust, doris (intended: lojix-cli)
- `75pw` — Lojix safe typed Nix interface (intended: lojix-cli)
- `7kyx` — cloud API triad Cloudflare DNS (intended: lojix-cli)
- `8fe9` — cloud Plan->Mutate rename, Mutated reply state (intended: lojix-cli/cloud)
- `h03z` — lojix criome machine-identity production cutover (intended: lojix-cli)
- `iprx` — cloud credential custody toward criome machine-identity (intended: lojix-cli/cloud)
- `lc28` — lojix substituter resolution into daemon, Yggdrasil (intended: lojix-cli)
- `m3eg` — cloud daemon almost-stateless caches Cloudflare state (intended: lojix-cli/cloud)
- `mbmy` — cloud home for provider API machinery Cloudflare/Hetzner (intended: lojix-cli/cloud)
- `mq5s` — lojix deploy testing/deployment one function, contained-vs-production (intended: lojix-cli)
- `nsi2` — cloud flarectl gopass shim CF_API_TOKEN (intended: lojix-cli/cloud)
- `vfgk` — ergonomic contained-test authoring interface (intended: lojix-cli)
- `vudl` — lojix two-contract authority split (intended: lojix-cli)
- `zeqq` — provision cloud nodes on-role only, doris low-trust placeholder (intended: lojix-cli/cloud)

### intended: `repos/CriomOS`  (13 records)

- `0a9p` — Prometheus-local AI model prefetch/build node policy (intended: CriomOS)
- `1hyg` — LojixOS/CriomOS split, OS image (intended: CriomOS)
- `6wz8` — synthetic bare-metal firmware-gating generic Nix checks (intended: CriomOS)
- `878r` — CriomOS website-hosting node, doris (intended: CriomOS)
- `cncj` — CriomOS VM-testing per-node gpu-passthrough VFIO, disabled on Prometheus (intended: CriomOS)
- `kx32` — large-AI-node deploy preserves hostapd/dnsmasq network (intended: CriomOS)
- `nz0t` — prometheus gopass-fed API auth token, mint tool (intended: CriomOS)
- `osoo` — backup WiFi password via sops-nix not plaintext (intended: CriomOS)
- `p7kn` — Prometheus install big Gemma multimodal models bf16 (intended: CriomOS)
- `ufjd` — node NixOS configs build/realize on target node (intended: CriomOS)
- `upza` — privileged cluster ops via SSH root account, operator key (intended: CriomOS)
- `wn7q` [SECRET] — SECRET; Prometheus USB backup admin network, sops-nix (intended: CriomOS)
- `wprd` — ouranos ThinkPad battery-care 75-80% thresholds (intended: CriomOS)

### intended: `repos/persona`  (11 records)

- `8pux` — agents vs runtime functions, persona-engine (intended: persona)
- `b9ao` — persona system federated triads (intended: persona)
- `flqt` — Persona Pi Codex-advisor harness, GPT model (intended: persona)
- `kzk5` — Persona permissioned system daemon (intended: persona)
- `ns7t` — Persona FD handoff SCM_RIGHTS atomic cutover (intended: persona)
- `p6fx` — Persona live runtime manager, systemd drain-with-mirror (intended: persona)
- `pbgy` — Persona-Pi terminal usability, terminal-cell/harness surfaces (intended: persona)
- `rc8v` — drop persona- prefix from component crate names (intended: persona)
- `s5dz` — version-suffixed daemon coexistence (intended: persona)
- `xe6q` — Persona Pi agent-chain self-authorization (intended: persona)
- `yr2w` — persona-pi adapts Pi into signal-data-tree (intended: persona)

### intended: `repos/schema-cc`  (1 records)

- `vpbx` — schema compiler-compiler typed data (intended: schema-cc)

## UNROUTABLE  (0 records)

Every record routed with a confident single home; none required the unroutable bucket.

