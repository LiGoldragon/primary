# Spirit split and residual dependency inventory

## Workspace packages
spirit-nexus: /tmp/flow857335-spirit-1050/crates/spirit-nexus/Cargo.toml
spirit: /tmp/flow857335-spirit-1050/Cargo.toml
spirit-client: /tmp/flow857335-spirit-1050/crates/spirit-client/Cargo.toml
spirit-meta-client: /tmp/flow857335-spirit-1050/crates/spirit-meta-client/Cargo.toml
spirit-offline-tools: /tmp/flow857335-spirit-1050/crates/spirit-offline-tools/Cargo.toml

## Active legacy references outside frozen fixtures
Cargo.toml:8:description  = "Runnable schema-derived Spirit pilot: NOTA CLI, rkyv socket, generated schema types."
Cargo.toml:32:nota-text = ["dep:nota", "nota-text-query/nota-text"]
Cargo.toml:52:# deploy-gated. Pulls the `mirror` crate (and its signal-mirror/nota
Cargo.toml:124:nota = { package = "nota", git = "https://github.com/LiGoldragon/nota.git", branch = "main", optional = true }
Cargo.toml:133:# signal-mirror/meta-signal-mirror/nota unconditionally, so leaving it out
Cargo.toml:134:# of the default build keeps nota out of the binary-only daemon dependency
Cargo.toml:135:# tree — the daemon's no-NOTA invariant (INTENT). default-features = false drops
Cargo.toml:136:# mirror's own nota-text codec, which the shipper does not use.
Cargo.toml:147:# (triad-runtime, sema-engine, nota) with the mirror leg in one
Cargo.toml:148:# binary. default-features = false on signal-criome drops its nota-text codec,
Cargo.toml:170:# = false drops its nota-text codec from non-text builds; spirit's own nota-text
Cargo.toml:177:# nota dependency, so leaving it out of the default daemon build keeps
Cargo.toml:178:# nota out of the binary-only runtime tree (the daemon's no-NOTA invariant).
Cargo.toml:184:# Optional and pulled in only by `testing-trace`, for the same no-NOTA reason.
Cargo.toml:189:nota-text-query = { git = "https://github.com/LiGoldragon/nota-text-query.git", rev = "6140a3e9afe3f81c18a39cb0a11dec4eab68b561", default-features = false }
Cargo.toml:208:required-features = ["agent-guardian", "signal-agent", "nota-text"]
Cargo.toml:220:[patch."https://github.com/LiGoldragon/nota-next.git"]
Cargo.toml:221:nota = { package = "nota", git = "https://github.com/LiGoldragon/nota.git", branch = "main" }
Cargo.toml:222:nota-derive = { package = "nota-derive", git = "https://github.com/LiGoldragon/nota.git", branch = "main" }
tests/operator_271_closed_claims.rs:5://! left by the schema-rust removal.
tests/operator_271_closed_claims.rs:35:            "schema-rust",
tests/operator_271_closed_claims.rs:37:            "signal-frame",
tests/operator_271_closed_claims.rs:38:            "NotaDecode",
tests/operator_271_closed_claims.rs:39:            "NotaEncode",
src/config.rs:6://! reads to bind listeners and open the store. No NOTA is linked here.
tests/nix_integration.rs:22://!      NOTA arguments — the SAME single-NOTA-argument contract
tests/nix_integration.rs:25://!      `Response::to_string()` NOTA round-trip) by parsing it back into
tests/nix_integration.rs:87://!   schema-emitted `Response::FromStr`, proving the NOTA form and the
tests/nix_integration.rs:288:        ("nota-source", github_source("nota", "NOTA_REF")),
tests/nix_integration.rs:291:            "schema-rust-source",
tests/nix_integration.rs:292:            github_source("schema-rust", "SCHEMA_RUST_REF"),
tests/nix_integration.rs:300:            "signal-frame-source",
tests/nix_integration.rs:301:            github_source("signal-frame", "SIGNAL_FRAME_REF"),
tests/nix_integration.rs:412:/// Run the CLI binary against the daemon's socket with one NOTA
tests/nix_integration.rs:549:    // back through the reverse plane chain, the CLI writes the NOTA
tests/nix_integration.rs:585:    // schema-emitted NOTA round-trip; we parse it back through
tests/nix_integration.rs:703:    // prints the NOTA, we parse it back through the schema-emitted
tests/nix_integration.rs:760:    // schema-emitted Response::FromStr. The test proves the NOTA wire
src/production_migration/v13.rs:195:    Notation,
tests/instrumentation_logging.rs:139:    #[cfg(feature = "nota-text")]
tests/instrumentation_logging.rs:145:            .expect("trace event parses from generated NOTA");
src/production_migration/v14.rs:28:/// every Entry field. This offline-only copy excludes its Nota derives and
src/production_migration/v14.rs:183:    Notation,
src/production_migration.rs:184:            v13::Language::Notation => signal_domain::LanguageDomain::Notation,
src/production_migration.rs:819:            v14::Language::Notation => signal_domain::LanguageDomain::Notation,
tests/observe_head_object.rs:26:#![cfg(feature = "nota-text")]
tests/observe_head_object.rs:34:/// node-a's spirit daemon (mkCriomeAuthWitnessTest `importNota`).
tests/observe_head_object.rs:35:const WITNESS_IMPORT_NOTA: &str = "(Import [(witness-record-1 ([(Technology (Software (Programming CodeGeneration)))] Decision [criome auth witness record] Low))])";
tests/observe_head_object.rs:45:    let MetaInput::Import(import) = WITNESS_IMPORT_NOTA
tests/observe_head_object.rs:47:        .expect("parse witness import NOTA")
tests/observe_head_object.rs:49:        panic!("witness NOTA must be an Import");
tests/guardian_live_scenarios.rs:40:const JUDGE_LIVE_EVAL_FIXTURE: &str = include_str!("fixtures/spirit_judge_live_eval.nota");
tests/guardian_live_scenarios.rs:782:                &["software", "nota"],
tests/guardian_live_scenarios.rs:785:                "NOTA strings should use quotation marks as the canonical representation.",
tests/guardian_live_scenarios.rs:788:                "let us make quotation marks the canonical NOTA string form",
tests/guardian_live_scenarios.rs:800:                "The daemon rejects inline NOTA configuration.",
tests/guardian_live_scenarios.rs:804:                Some("shall we make the daemon reject inline NOTA configuration"),
tests/guardian_live_scenarios.rs:815:                "The daemon rejects inline NOTA configuration.",
tests/dependency_surface.rs:73:fn binary_only_surface_has_no_nota_runtime_dependency() {
tests/dependency_surface.rs:78:        !CargoTree::new(&tree).contains_package("nota"),
tests/dependency_surface.rs:79:        "binary-only runtime dependency tree must not contain nota:\n{tree}"
tests/dependency_surface.rs:100:fn text_client_surface_has_nota_runtime_dependency() {
tests/dependency_surface.rs:102:    let tree = manifest.cargo_tree(&["--edges", "normal", "--features", "nota-text"]);
tests/dependency_surface.rs:105:        CargoTree::new(&tree).contains_package("nota"),
tests/dependency_surface.rs:106:        "nota-text runtime dependency tree must contain nota:\n{tree}"
tests/dependency_surface.rs:126:        !tree.contains_package("schema-rust"),
src/engine.rs:104:#[cfg_attr(feature = "nota-text", derive(nota::NotaDecode, nota::NotaEncode))]
src/engine.rs:315:    // feature (which the binary-only daemon build excludes to keep nota
src/engine.rs:1182:    /// default meta-signal tree stays free of `nota` — the same constraint the
tests/observe_head.rs:14://!     NOTA the witness sends over the meta socket), `ObserveHead` reports a
tests/observe_head.rs:24:#![cfg(feature = "nota-text")]
tests/observe_head.rs:31:/// node-a's spirit daemon (mkCriomeAuthWitnessTest `importNota`).
tests/observe_head.rs:32:const WITNESS_IMPORT_NOTA: &str = "(Import [(witness-record-1 ([(Technology (Software (Programming CodeGeneration)))] Decision [criome auth witness record] Low))])";
tests/observe_head.rs:48:    let MetaInput::Import(import) = WITNESS_IMPORT_NOTA
tests/observe_head.rs:50:        .expect("parse witness import NOTA")
tests/observe_head.rs:52:        panic!("witness NOTA must be an Import");
tests/socket_negative.rs:8:fn transport_rejects_length_prefixed_raw_nota_text() {
tests/socket_negative.rs:9:    let nota =
tests/socket_negative.rs:12:        .encode_body(&FrameBody::new(nota.to_vec()))
tests/socket_negative.rs:18:        "daemon wire transport must reject length-prefixed raw NOTA bytes"
tests/socket_negative.rs:36:fn generated_input_decoder_rejects_raw_nota_text_directly() {
tests/socket_negative.rs:37:    let nota =
tests/socket_negative.rs:41:        Signal::<Query>::from(nota.to_vec()).restore().is_err(),
tests/socket_negative.rs:42:        "schema-emitted binary decoder must reject raw NOTA text"
tests/fixtures/spirit_judge_live_eval.nota:2:# description, and importance; each payload crosses the generated NOTA boundary.
tests/fixtures/spirit_judge_live_eval.nota:4:seed notation-brackets (Record (([(Technology (Software (Programming DomainSpecificLanguages)))] Decision [NOTA strings are represented with bracket forms; quotation marks are not valid NOTA string syntax.] Minimum) ([([NOTA strings are represented with bracket forms; quotation marks are not valid NOTA string syntax.] None)] [NOTA strings are represented with bracket forms; quotation marks are not valid NOTA string syntax.])))
tests/fixtures/spirit_judge_live_eval.nota:23:case contradiction-quotation-form Reject:Contradiction,InsufficientWarrant (Propose (([(Technology (Software (Programming DomainSpecificLanguages)))] Decision [NOTA strings should use quotation marks as the canonical representation.] Minimum) ([([let us make quotation marks the canonical NOTA string form] None)] [The quote conflicts with the live bracket-form rule and needs an explicit lifecycle operation.])))
tests/fixtures/spirit_judge_live_eval.nota:34:case bare-yes-with-antecedent Accept (Propose (([(Technology (Software (Operations ConfigurationManagement)))] Decision [The daemon rejects inline NOTA configuration.] Minimum) ([([yes do that] (Some [shall we make the daemon reject inline NOTA configuration]))] [The psyche affirmed the antecedent question, which carries the arrow.])))
tests/fixtures/spirit_judge_live_eval.nota:35:case bare-yes-no-antecedent Reject:MissingTestimony (Propose (([(Technology (Software (Operations ConfigurationManagement)))] Decision [The daemon rejects inline NOTA configuration.] Minimum) ([([yes do that] None)] [An affirmation with no antecedent.])))
flake.nix:31:    nota-source = {
flake.nix:32:      url = "github:LiGoldragon/nota";
flake.nix:39:    schema-language-source = {
flake.nix:40:      url = "github:LiGoldragon/schema-language/6aae825d668e3f607a2754afa6b7d94e9f246c41";
flake.nix:43:    schema-rust-source = {
flake.nix:44:      url = "github:LiGoldragon/schema-rust";
flake.nix:55:    signal-frame-source = {
flake.nix:56:      url = "git+https://github.com/LiGoldragon/signal-frame.git?ref=main";
flake.nix:87:    nota-text-query-source = {
flake.nix:88:      url = "github:LiGoldragon/nota-text-query";
flake.nix:175:      nota-source,
flake.nix:177:      schema-language-source,
flake.nix:178:      schema-rust-source,
flake.nix:181:      signal-frame-source,
flake.nix:189:      nota-text-query-source,
flake.nix:234:              notaNextSource = nota-source;
flake.nix:236:              schemaLanguageSource = schema-language-source;
flake.nix:237:              schemaRustNextSource = schema-rust-source;
flake.nix:240:              signalFrameSource = signal-frame-source;
flake.nix:248:              notaTextQuerySource = nota-text-query-source;
flake.nix:273:              cp -R "$notaNextSource" $out/vendor-sources/nota
flake.nix:275:              cp -R "$schemaLanguageSource" $out/vendor-sources/schema-language
flake.nix:276:              cp -R "$schemaRustNextSource" $out/vendor-sources/schema-rust
flake.nix:279:              cp -R "$signalFrameSource" $out/vendor-sources/signal-frame
flake.nix:287:              cp -R "$notaTextQuerySource" $out/vendor-sources/nota-text-query
flake.nix:325:                --replace-fail 'nota = { package = "nota", git = "https://github.com/LiGoldragon/nota.git", branch = "main", optional = true }' 'nota = { path = "vendor-sources/nota", optional = true }' \
flake.nix:326:                --replace-fail 'nota = { package = "nota", git = "https://github.com/LiGoldragon/nota.git", branch = "main" }' 'nota = { path = "vendor-sources/nota" }' \
flake.nix:327:                --replace-fail 'nota-derive = { package = "nota-derive", git = "https://github.com/LiGoldragon/nota.git", branch = "main" }' 'nota-derive = { path = "vendor-sources/nota/derive" }' \
flake.nix:329:                --replace-fail 'signal-frame = { git = "https://github.com/LiGoldragon/signal-frame.git", branch = "main" }' 'signal-frame = { path = "vendor-sources/signal-frame" }' \
flake.nix:341:                --replace-fail 'nota-text-query = { git = "https://github.com/LiGoldragon/nota-text-query.git", rev = "6140a3e9afe3f81c18a39cb0a11dec4eab68b561", default-features = false }' 'nota-text-query = { path = "vendor-sources/nota-text-query", default-features = false }' \
flake.nix:343:                --replace-fail 'schema-rust = { package = "schema-rust", git = "https://github.com/LiGoldragon/schema-rust.git", rev = "f3b4563163dd11ba1cbbcca8081701ab7830b8f5" }' 'schema-rust = { path = "vendor-sources/schema-rust", package = "schema-rust" }' \
flake.nix:347:                --replace-fail 'schema-language = { git = "https://github.com/LiGoldragon/schema-language.git", rev = "6aae825d668e3f607a2754afa6b7d94e9f246c41" }' 'schema-language = { path = "vendor-sources/schema-language" }' \
flake.nix:367:              ${pkgs.python3}/bin/python3 - "$out/vendor-sources/schema-rust/Cargo.toml" <<'PYEOF'
flake.nix:377:                  'nota = { git = "https://github.com/LiGoldragon/nota.git", branch = "main" }': 'nota = { path = "../nota" }',
flake.nix:378:                  'nota = { git = "https://github.com/LiGoldragon/nota.git", branch = "structural-forms-integration" }': 'nota = { path = "../nota" }',
flake.nix:379:                  'nota = { package = "nota", git = "https://github.com/LiGoldragon/nota.git", branch = "main" }': 'nota = { path = "../nota" }',
flake.nix:381:                  'signal-frame = { git = "https://github.com/LiGoldragon/signal-frame.git", branch = "main" }': 'signal-frame = { path = "../signal-frame" }',
flake.nix:404:                  "nota": "nota",
flake.nix:406:                  "schema-rust": "schema-rust",
flake.nix:439:              [patch."https://github.com/LiGoldragon/nota.git"]
flake.nix:440:              nota = { path = "vendor-sources/nota" }
flake.nix:441:              nota-derive = { path = "vendor-sources/nota/derive" }
flake.nix:447:              [patch."https://github.com/LiGoldragon/schema-rust.git"]
flake.nix:448:              schema-rust = { path = "vendor-sources/schema-rust" }
flake.nix:450:              [patch."https://github.com/LiGoldragon/schema-language.git"]
flake.nix:451:              schema-language = { path = "vendor-sources/schema-language" }
flake.nix:452:              schema-language-cc = { path = "vendor-sources/schema-language/schema-language-cc" }
flake.nix:460:              [patch."https://github.com/LiGoldragon/signal-frame.git"]
flake.nix:461:              signal-frame = { path = "vendor-sources/signal-frame" }
flake.nix:462:              signal-frame-macros = { path = "vendor-sources/signal-frame/macros" }
flake.nix:470:              [patch."https://github.com/LiGoldragon/nota-text-query.git"]
flake.nix:471:              nota-text-query = { path = "vendor-sources/nota-text-query" }
flake.nix:556:              "schema-rust": "main",
flake.nix:560:              "nota": "0.5.1",
flake.nix:561:              "nota-derive": "0.3.0",
flake.nix:562:              "schema-rust": "0.7.0",
flake.nix:569:              "nota",
flake.nix:570:              "nota-derive",
flake.nix:572:              "schema-rust",
flake.nix:573:              "schema-language",
flake.nix:574:              "schema-language-cc",
flake.nix:578:              "signal-frame",
flake.nix:579:              "signal-frame-macros",
flake.nix:583:              "nota-text-query",
flake.nix:705:        notaTextCargoArtifacts = craneLib.buildDepsOnly (
flake.nix:708:            cargoExtraArgs = "--features nota-text";
flake.nix:729:        notaTextTestingTraceCargoArtifacts = craneLib.buildDepsOnly (
flake.nix:732:            cargoExtraArgs = "--features nota-text,testing-trace";
flake.nix:928:            ${judgeConfigPackage}/config/provider-policy.nota
flake.nix:930:            ${judgeConfigPackage}/config/provider-policy.nota
flake.nix:982:          build-nota-text = craneLib.cargoBuild (
flake.nix:985:              cargoArtifacts = notaTextCargoArtifacts;
flake.nix:986:              cargoExtraArgs = "--features nota-text";
flake.nix:996:          test-nota-text = craneLib.cargoTest (
flake.nix:999:              cargoArtifacts = notaTextCargoArtifacts;
flake.nix:1000:              cargoExtraArgs = "--features nota-text";
flake.nix:1025:              cargoArtifacts = notaTextCargoArtifacts;
flake.nix:1026:              cargoExtraArgs = "--features nota-text --test observe_head_object";
flake.nix:1032:              cargoArtifacts = notaTextCargoArtifacts;
flake.nix:1033:              cargoExtraArgs = "--features nota-text --test process_boundary configuration_writer_prebuilds_binary_archive_for_daemon_startup -- --exact";
flake.nix:1046:              cargoArtifacts = notaTextTestingTraceCargoArtifacts;
flake.nix:1047:              cargoExtraArgs = "--features nota-text,testing-trace --test process_boundary cli_receives_testing_trace_events_from_daemon_trace_socket -- --exact";
flake.nix:1082:          nota-surface-is-opt-in = pkgs.runCommand "spirit-nota-surface-is-opt-in" { } ''
flake.nix:1084:            # runs cargo tree for the binary-only and nota-text surfaces.
flake.nix:1087:            ! grep -R "nota" ${src}/src/config.rs ${src}/src/daemon.rs ${src}/crates/spirit-nexus/src/main.rs
flake.nix:1088:            ! grep -R "NotaSource" ${src}/src/config.rs ${src}/src/daemon.rs ${src}/crates/spirit-nexus/src/main.rs
flake.nix:1146:          clippy-nota-text = craneLib.cargoClippy (
flake.nix:1150:              cargoClippyExtraArgs = "--features nota-text --all-targets -- -D warnings";
flake.nix:1156:              cargoArtifacts = notaTextTestingTraceCargoArtifacts;
flake.nix:1157:              cargoClippyExtraArgs = "--features nota-text,testing-trace --all-targets -- -D warnings";
tests/end_to_end_offline_full_chain.rs:31://! (triad-runtime, sema-engine, nota, signal-frame) also pin `branch=main`,
tests/process_boundary.rs:650:    let nota_file = temp.path().join("must-not-read.nota");
tests/process_boundary.rs:651:    fs::write(&nota_file, "Version").expect("write sentinel file");
tests/process_boundary.rs:659:            vec![nota_file.display().to_string()],
tests/process_boundary.rs:674:            if arguments == [nota_file.display().to_string()] {
tests/process_boundary.rs:898:fn cli_and_daemon_exchange_nota_over_rkyv_socket() {
tests/process_boundary.rs:1092:fn cli_and_daemon_report_version_from_bare_nota_atom() {

## Nexus normal dependency graph
spirit-nexus v0.27.0 (/tmp/flow857335-spirit-1050/crates/spirit-nexus)
└── spirit v0.27.0 (/tmp/flow857335-spirit-1050)
    ├── blake3 v1.8.5
    │   ├── arrayref v0.3.9
    │   ├── arrayvec v0.7.8
    │   ├── cfg-if v1.0.4
    │   ├── constant_time_eq v0.4.2
    │   └── cpufeatures v0.3.0
    ├── getrandom v0.3.4
    │   ├── cfg-if v1.0.4
    │   └── libc v0.2.186
    ├── meta-signal-spirit v1.0.1 (/git/github.com/LiGoldragon/meta-signal-spirit)
    │   ├── rkyv v0.8.18
    │   │   ├── bytecheck v0.8.2
    │   │   │   ├── bytecheck_derive v0.8.2 (proc-macro)
    │   │   │   │   ├── proc-macro2 v1.0.106
    │   │   │   │   │   └── unicode-ident v1.0.24
    │   │   │   │   ├── quote v1.0.46
    │   │   │   │   │   └── proc-macro2 v1.0.106 (*)
    │   │   │   │   └── syn v2.0.118
    │   │   │   │       ├── proc-macro2 v1.0.106 (*)
    │   │   │   │       ├── quote v1.0.46 (*)
    │   │   │   │       └── unicode-ident v1.0.24
    │   │   │   ├── ptr_meta v0.3.1
    │   │   │   │   └── ptr_meta_derive v0.3.1 (proc-macro)
    │   │   │   │       ├── proc-macro2 v1.0.106 (*)
    │   │   │   │       ├── quote v1.0.46 (*)
    │   │   │   │       └── syn v2.0.118 (*)
    │   │   │   ├── rancor v0.1.2
    │   │   │   │   └── ptr_meta v0.3.1 (*)
    │   │   │   └── simdutf8 v0.1.5
    │   │   ├── hashbrown v0.17.1
    │   │   ├── munge v0.4.7
    │   │   │   └── munge_macro v0.4.7 (proc-macro)
    │   │   │       ├── proc-macro2 v1.0.106 (*)
    │   │   │       ├── quote v1.0.46 (*)
    │   │   │       └── syn v2.0.118 (*)
    │   │   ├── ptr_meta v0.3.1 (*)
    │   │   ├── rancor v0.1.2 (*)
    │   │   ├── rend v0.5.4
    │   │   │   └── bytecheck v0.8.2 (*)
    │   │   └── rkyv_derive v0.8.18 (proc-macro)
    │   │       ├── proc-macro2 v1.0.106 (*)
    │   │       ├── quote v1.0.46 (*)
    │   │       └── syn v3.0.5
    │   │           ├── proc-macro2 v1.0.106 (*)
    │   │           ├── quote v1.0.46 (*)
    │   │           └── unicode-ident v1.0.24
    │   └── signal-spirit v1.2.0 (/git/github.com/LiGoldragon/signal-spirit)
    │       ├── rkyv v0.8.18 (*)
    │       └── signal-domain v1.0.1 (https://github.com/LiGoldragon/signal-domain.git?rev=da553c9557bd650e71c8c897947b35bf8abf22b8#da553c95)
    │           └── rkyv v0.8.18 (*)
    ├── nexus v0.1.1 (https://github.com/LiGoldragon/nexus.git?rev=a84bfa960c0d5c02d30048c4bbbc67dfef79a67c#a84bfa96)
    │   ├── rkyv v0.8.18 (*)
    │   └── thiserror v2.0.18
    │       └── thiserror-impl v2.0.18 (proc-macro)
    │           ├── proc-macro2 v1.0.106 (*)
    │           ├── quote v1.0.46 (*)
    │           └── syn v2.0.118 (*)
    ├── nota-text-query v0.1.0 (https://github.com/LiGoldragon/nota-text-query.git?rev=6140a3e9afe3f81c18a39cb0a11dec4eab68b561#6140a3e9)
    │   ├── rkyv v0.8.18 (*)
    │   └── thiserror v2.0.18 (*)
    ├── rkyv v0.8.18 (*)
    ├── sema-engine v0.7.0 (https://github.com/LiGoldragon/sema-engine.git?branch=main#b3b5fb71)
    │   ├── blake3 v1.8.5 (*)
    │   ├── rkyv v0.8.18 (*)
    │   ├── sema v0.1.1 (https://github.com/LiGoldragon/sema.git?branch=main#51d7927c)
    │   │   ├── redb v4.1.0
    │   │   ├── rkyv v0.8.18 (*)
    │   │   └── thiserror v2.0.18 (*)
    │   ├── signal-frame v0.3.0 (https://github.com/LiGoldragon/signal-frame.git?branch=main#fd7909d1)
    │   │   ├── paste v1.0.15 (proc-macro)
    │   │   ├── rkyv v0.8.18 (*)
    │   │   ├── signal-frame-macros v0.1.1 (proc-macro) (https://github.com/LiGoldragon/signal-frame.git?branch=main#fd7909d1)
    │   │   │   ├── proc-macro2 v1.0.106 (*)
    │   │   │   ├── quote v1.0.46 (*)
    │   │   │   └── syn v2.0.118 (*)
    │   │   └── thiserror v2.0.18 (*)
    │   ├── signal-sema v0.2.0 (https://github.com/LiGoldragon/signal-sema.git?branch=main#8d4a0223)
    │   │   ├── rkyv v0.8.18 (*)
    │   │   └── thiserror v2.0.18 (*)
    │   └── thiserror v2.0.18 (*)
    ├── signal-domain v1.0.1 (https://github.com/LiGoldragon/signal-domain.git?rev=da553c9557bd650e71c8c897947b35bf8abf22b8#da553c95) (*)
    ├── signal-spirit v1.2.0 (/git/github.com/LiGoldragon/signal-spirit) (*)
    ├── thiserror v2.0.18 (*)
    ├── tokio v1.52.3
    │   ├── bytes v1.12.0
    │   ├── libc v0.2.186
    │   ├── mio v1.2.1
    │   │   └── libc v0.2.186
    │   ├── pin-project-lite v0.2.17
    │   ├── socket2 v0.6.4
    │   │   └── libc v0.2.186
    │   └── tokio-macros v2.7.0 (proc-macro)
    │       ├── proc-macro2 v1.0.106 (*)
    │       ├── quote v1.0.46 (*)
    │       └── syn v2.0.118 (*)
    └── triad-runtime v0.6.1 (https://github.com/LiGoldragon/triad-runtime.git?branch=main#895d2e6b)
        ├── kameo v0.20.0 (https://github.com/LiGoldragon/kameo.git?branch=main#f491b45d)
        │   ├── downcast-rs v2.0.2
        │   ├── dyn-clone v1.0.20
        │   ├── futures v0.3.32
        │   │   ├── futures-channel v0.3.32
        │   │   │   ├── futures-core v0.3.32
        │   │   │   └── futures-sink v0.3.32
        │   │   ├── futures-core v0.3.32
        │   │   ├── futures-executor v0.3.32
        │   │   │   ├── futures-core v0.3.32
        │   │   │   ├── futures-task v0.3.32
        │   │   │   └── futures-util v0.3.32
        │   │   │       ├── futures-channel v0.3.32 (*)
        │   │   │       ├── futures-core v0.3.32
        │   │   │       ├── futures-io v0.3.32
        │   │   │       ├── futures-macro v0.3.32 (proc-macro)
        │   │   │       │   ├── proc-macro2 v1.0.106 (*)
        │   │   │       │   ├── quote v1.0.46 (*)
        │   │   │       │   └── syn v2.0.118 (*)
        │   │   │       ├── futures-sink v0.3.32
        │   │   │       ├── futures-task v0.3.32
        │   │   │       ├── memchr v2.8.2
        │   │   │       ├── pin-project-lite v0.2.17
        │   │   │       └── slab v0.4.12
        │   │   ├── futures-io v0.3.32
        │   │   ├── futures-sink v0.3.32
        │   │   ├── futures-task v0.3.32
        │   │   └── futures-util v0.3.32 (*)
        │   ├── kameo_macros v0.20.0 (proc-macro) (https://github.com/LiGoldragon/kameo.git?branch=main#f491b45d)
        │   │   ├── heck v0.5.0
        │   │   ├── proc-macro2 v1.0.106 (*)
        │   │   ├── quote v1.0.46 (*)
        │   │   └── syn v2.0.118 (*)
        │   ├── serde v1.0.228
        │   │   ├── serde_core v1.0.228
        │   │   └── serde_derive v1.0.228 (proc-macro)
        │   │       ├── proc-macro2 v1.0.106 (*)
        │   │       ├── quote v1.0.46 (*)
        │   │       └── syn v2.0.118 (*)
        │   ├── tokio v1.52.3 (*)
        │   └── tracing v0.1.44
        │       ├── pin-project-lite v0.2.17
        │       ├── tracing-attributes v0.1.31 (proc-macro)
        │       │   ├── proc-macro2 v1.0.106 (*)
        │       │   ├── quote v1.0.46 (*)
        │       │   └── syn v2.0.118 (*)
        │       └── tracing-core v0.1.36
        │           └── once_cell v1.21.4
        ├── rkyv v0.8.18 (*)
        ├── rustix v1.1.4
        │   ├── bitflags v2.13.0
        │   └── linux-raw-sys v0.12.1
        ├── signal-frame v0.3.0 (https://github.com/LiGoldragon/signal-frame.git?branch=main#fd7909d1) (*)
        ├── thiserror v2.0.18 (*)
        └── tokio v1.52.3 (*)

## 2026-09-10 root text-path closure

Removed root `nota-text`, direct `nota`, `nota-text-query`, and the root Nota patch. The text-only `SignalObjectName` representation uses its existing `datom-cli` derives. `ObserveHead` and `ObserveHeadObject` now construct the current typed `meta_signal_spirit::ImportRequest`; their former NOTA source was not retained as a compatibility parser. The trace render/restore witness now uses the Datom chain.

Focused evidence is `spirit-datom-text-removal.log` (exit in the adjacent `.exit`): dependency boundary 5/5, current typed head witnesses 3/3 and 2/2, trace Datom witness 5/5, and the combined `datom-cli agent-guardian production-migration testing-trace criome-gate` all-target check.

The declared `mirror-shipper` path remains active and is not disabled. Its current failure is upstream `mirror@b1da05c3` build generation: `Schema(ExplicitFieldOnUniqueProductComponent { field: "store", type_name: "StoreName" })`. It needs coordinated mirror/signal-mirror/meta-signal-mirror migration before the full matrix can close. The Nix source no longer vendors or patches `nota-text-query`; other old-source vendor entries are transitive to still-active mirror/router paths and remain explicitly pending migration.
