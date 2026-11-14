Read-only design analysis (56ed874)

Current runtime ownership:
- src/registry.rs::SourceConfiguration::read -> read_declarations(root), with modules.datom at DECLARATIONS_FILE. The datom path decodes generated::ModuleDeclarations; non-datom path rejects.
- src/roles.rs::read_declared reads CURRICULUM_ROLES_FILE and decodes generated::RolesDocument::Roles; non-datom path rejects.
- src/service.rs::SkillMemory::open loads registry and roles once; CurriculumOperation reloads SourceConfiguration per request. compose_role consumes typed generated::Roles and registry resolution.
- src/generated.rs defines ModuleDeclaration/ModuleDeclarations and Roles/RoleDefinition, all rkyv archiveable; Datomizable/Composing derives are cfg(feature="datom").
- src/main.rs is the CLI entrypoint; src/client.rs parses one inline Datom Input and sends existing rkyv signal_curriculum_nexus::Input/Output over the Unix socket. Server path is XDG_RUNTIME_DIR/curriculum/curriculum.sock. Server config is CURRICULUM_RECORDS_DIR, CURRICULUM_ROLES_FILE, and the three source roots read by SourceConfiguration.

Smallest coherent path: a deployment/preparation process (the existing curriculum-deploy boundary) reads each modules.datom and the optional roles file with datom-codec/protos, validates them, and writes a typed rkyv archive containing ModuleDeclarations and Roles plus source-root/revision metadata. Nexus receives only archive paths/configuration and reads the typed archive; it continues reading module bodies by the declared relative paths. Move read_declarations/read_declared decoding out of the plain Nexus; retain admit/validate/registry resolution in Nexus over typed values.

No new signal schema is needed if the archive is a local deployment artifact named by configuration: existing Input/Output and CurriculumSignal remain unchanged, and declarations are preparation state rather than an operation. A signal schema operation would be required only if declarations were to be sent through the Unix Nexus protocol at runtime, which is a larger design and is not the smallest path.
