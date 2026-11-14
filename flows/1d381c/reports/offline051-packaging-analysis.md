# Bounded packaging analysis — no helper edits/build
UTC interval 2026-11-06T00:19:43Z–00:20:52Z.
Actual failed source: /nix/store/a13fmxxycg9d64zgf788vq0mw7mfhxkg-offline-051-adapter-source; drv r40g53ajckbdhcs9asn7q0x9jiq9qbys; complete failed log remote-build.REVIEW3.log SHAa4748382b3aafce45d174d470b7aa90a0660cd40eae8a059fffc3247c637e707.

Observed root Cargo.toml:6 explicitly members=["."], line7 nine excludes. Cargo's WorkspaceRootConfig::is_excluded computes `!explicit_member && excluded`, and both predicates use path-prefix tests. Dot explicitly matches every descendant, overriding all nine exclusions. find_path_deps recursively includes the path dependencies; same-name17/16 ethos packages reach name uniqueness validation.
Primary source: https://rust.googlesource.com/cargo/+/f8984e1169dc670fd1c002d68c8c5efee63ff514/src/cargo/core/workspace.rs , is_excluded1817–1830, find_path_deps821–871. This is a pinned upstream source reference, not an attestation of the installed Cargo source revision. Official root-package rule: https://doc.rust-lang.org/cargo/reference/workspaces.html .

Actual path graph: root9–12→meta54,flowethos0.51,datom0.32.2,protos0.32.2. meta17–21→codec/protos/signal8/signalflow42/flowethos; signalflow17–20→codec/protos/signal/flowethos; signal24–25→codec/protos; datom24–25→protos/derive0.32.0; both ethos27–28→codec/protos. Build consumers meta25/signalflow24/flowethos21→ethos17@07714b; signal34→ethos16@c2653d. No ethos [workspace], package.workspace or metadata inheritance. Datom's own workspace11–12 owns derive; no changes proposed there. Installed flow-ethos metadata explicit1.89/0.51.0, unchanged.

Single proposed correction: delete ONLY root members=["."] line6, retain [workspace], exact nine excludes and all other bytes. Root [package] remains implicit member. Source bodies/identities/pins/layout unchanged. Static tomllib inspection plus independent reproduction of the published prefix predicate yielded all nine current_excluded=false and proposed_excluded=true, including nested derive. This is a falsifiable static check, not Cargo execution or a build guarantee. Independent reviewer must challenge it before any grant.

No helper edits, Cargo/Nix build, retry, runtime query, payload generation or production effects performed in this analysis.
