<!-- to-the-living:start -->
Presentation.{ «A context module is named kind:name» }

# A context module is named kind:name

## psyche-context › vision/context-modules.md

````markdown
## Context modules and their review

```
+--------------------------------------------+
| the living                                 |
+--------------------------------------------+
  |                                   |
  | reviews psyche                    | skims
  | proposals,                        | knowledge
  | line by line                      | proposals
  v                                   |
+------------------------------+      |
| Psyche                       |      |
| spirit, intent, vision       |      |
+------------------------------+      |
  |                                   |
  | rules over Mind: a Mind           |
  | line it contradicts is            |
  | removed                           |
  v                                   v
+--------------------------------------------+
| Mind                                       |
|  +--------------------------------------+  |
|  | knowledge: facts verified in code    |  |
|  +--------------------------------------+  |
|    | an audit for truth and currency       |
|    | finds a variation; it goes to         |
|    v                                       |
|  +--------------------------------------+  |
|  | the type that holds what is unclear  |  |
|  +--------------------------------------+  |
+--------------------------------------------+
  |
  | rules over Field: a Field line
  | it contradicts is removed
  v
+--------------------------------------------+
| Field                                      |
| compensation                               |
+--------------------------------------------+
  ^
  | reads it as a whole and checks it
  | against Mind and Psyche
  |
+--------------------------------------------+
| a periodic book or audit                   |
+--------------------------------------------+
```

Mind's second type is inquiry: it holds what is unclear, and what an audit finds varying from stated knowledge.

Knowledge modules are audited from time to time for truth and currency against practice; a variation found goes to the type that holds what is unclear.

A subject the living reviews or asks about has a module, on its topic or a broader one, with room to hold it.

A module declares its placement: the system prompt, or loaded on demand. A skill is the harness's interface for an on-demand module.

The vocabulary is context, context modules and context building.
A skill is the legacy name, one harness name for things that differ, becoming obsolete as harness infrastructure improves.

A context repository holds one folder per module type; no folder is called skills. A file is named by its subject alone, and its folder gives its type.

A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.
````

### Proposal 1: a module's name shows its kind before a colon · psyche-context › vision/context-modules.md

  A context repository holds one folder per module type; no folder is called skills. A file is named by its subject alone, and its folder gives its type.
+
+ A module's name is its kind and its name joined by a colon, as vision:book, so the eye sees where the kind ends and the name begins.
+ On disk the kind stays the folder: vision:book is the file vision/book.md.
+ Every flow learns in its basic training to read a name as kind:name.

Ruling: land, amend, or reject.

## Curriculum › src/registry.rs

```rust
//! The sole authored module registry: three server-configured repository roots.
use crate::startup_metadata::{declared_placement, instructions, sha256};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    path::{Path, PathBuf},
};
use thiserror::Error;

pub const MODULE_TYPES: &[&str] = &[
    "vision",
    "intent",
    "spirit",
    "knowledge",
    "inquiry",
    "compensation",
    "role",
    "raw",
];
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SkillEntry {
    pub path: PathBuf,
    pub name: String,
    pub body: String,
    pub dependencies: Vec<String>,
}
pub type ResolvedSkill = SkillEntry;
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SkillRegistry {
    entries: BTreeMap<String, SkillEntry>,
    roots: [PathBuf; 3],
    revisions: [String; 3],
}
#[derive(Debug, Error)]
pub enum RegistryError {
    #[error("invalid context source {path}: {message}")]
    InvalidSource { path: PathBuf, message: String },
    #[error("missing module {0}")]
    Missing(String),
    #[error("duplicate module {0}")]
    Duplicate(String),
    #[error("dependency cycle at {0}")]
    Cycle(String),
}
fn invalid(path: &Path, message: impl ToString) -> RegistryError {
    RegistryError::InvalidSource {
        path: path.into(),
        message: message.to_string(),
    }
}
fn canonical(path: &Path) -> Result<PathBuf, RegistryError> {
    fs::canonicalize(path).map_err(|e| invalid(path, e))
}
pub fn valid_id(value: &str) -> bool {
    !value.is_empty()
        && value
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SourceConfiguration {
    pub roots: [PathBuf; 3],
    pub revisions: [String; 3],
}
impl SourceConfiguration {
    pub fn from_environment() -> Result<Self, String> {
        if std::env::var("CURRICULUM_CONTEXT_LAYOUT").as_deref() != Ok("2") {
            return Err("only authored context layout 2 is supported".into());
        }
        let mut roots: [PathBuf; 3] = Default::default();
        let mut revisions: [String; 3] = Default::default();
        for (i, (root, revision)) in [
            (
                "CURRICULUM_PSYCHES_REPOSITORY_DIR",
                "CURRICULUM_PSYCHES_REVISION",
            ),
            ("CURRICULUM_MIND_CONTEXT_DIR", "CURRICULUM_MIND_REVISION"),
            ("CURRICULUM_FIELD_CONTEXT_DIR", "CURRICULUM_FIELD_REVISION"),
        ]
        .iter()
        .enumerate()
        {
            roots[i] = std::env::var_os(root)
                .map(PathBuf::from)
                .ok_or_else(|| format!("missing {root}"))?;
            revisions[i] = std::env::var(revision).map_err(|_| format!("missing {revision}"))?;
        }
        Ok(Self { roots, revisions })
    }
    pub fn read(&self) -> Result<SkillRegistry, RegistryError> {
        SkillRegistry::from_context_repositories(&self.roots, &self.revisions)
    }
}
impl SkillRegistry {
    pub fn from_context_repositories(
        input: &[PathBuf; 3],
        revisions: &[String; 3],
    ) -> Result<Self, RegistryError> {
        let roots = [
            canonical(&input[0])?,
            canonical(&input[1])?,
            canonical(&input[2])?,
        ];
        let mut entries = BTreeMap::new();
        for (i, root) in roots.iter().enumerate() {
            if revisions[i].len() != 40
                || !revisions[i]
                    .bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
            {
                return Err(invalid(
                    root,
                    "immutable source revision must be 40 lowercase hex",
                ));
            }
            if roots
                .iter()
                .enumerate()
                .any(|(j, r)| i != j && (root.starts_with(r) || r.starts_with(root)))
            {
                return Err(invalid(root, "repository roots overlap"));
            }
            if fs::symlink_metadata(root.join("skills")).is_ok() {
                return Err(invalid(root, "legacy skills directory forbidden"));
            }
            for kind in MODULE_TYPES {
                let directory = root.join(kind);
                match fs::symlink_metadata(&directory) {
                    Err(e) if e.kind() == std::io::ErrorKind::NotFound => continue,
                    Err(e) => return Err(invalid(&directory, e)),
                    Ok(m) if !m.is_dir() || m.file_type().is_symlink() => {
                        return Err(invalid(
                            &directory,
                            "type folder must be an actual directory",
                        ));
                    }
                    _ => (),
                }
                for entry in fs::read_dir(&directory).map_err(|e| invalid(&directory, e))? {
                    let path = entry.map_err(|e| invalid(&directory, e))?.path();
                    let metadata = fs::symlink_metadata(&path).map_err(|e| invalid(&path, e))?;
                    if !metadata.is_file() || metadata.file_type().is_symlink() {
                        return Err(invalid(
                            &path,
                            "nested directories and symlinks are forbidden",
                        ));
                    }
                    if path.extension().is_none_or(|e| e != "md") {
                        return Err(invalid(
                            &path,
                            "module type folder contains non-Markdown source",
                        ));
                    }
                    let subject = path
                        .file_stem()
                        .and_then(|s| s.to_str())
                        .unwrap_or_default();
                    if !valid_id(subject) {
                        return Err(invalid(&path, "invalid subject"));
                    }
                    let name = format!("{kind}-{subject}");
                    let body = fs::read_to_string(&path).map_err(|e| invalid(&path, e))?;
                    let text = instructions(&body).map_err(|e| invalid(&path, e))?;
                    if text.trim().is_empty() {
                        return Err(invalid(&path, "empty body"));
                    }
                    let dependencies = dependencies(&path, &body)?;
                    if entries
                        .insert(
                            name.clone(),
                            SkillEntry {
                                path,
                                name: name.clone(),
                                body,
                                dependencies,
                            },
                        )
                        .is_some()
                    {
                        return Err(RegistryError::Duplicate(name));
                    }
                }
            }
        }
        let registry = Self {
            entries,
            roots,
            revisions: revisions.clone(),
        };
        registry.expand_skills(&registry.skill_names()?)?;
        Ok(registry)
    }
    pub fn resolve_exact(&self, ids: &[String]) -> Result<Vec<ResolvedSkill>, RegistryError> {
        let mut seen = BTreeSet::new();
        ids.iter()
            .map(|id| {
                if !valid_id(id) {
                    return Err(RegistryError::Missing(id.clone()));
                }
                if !seen.insert(id) {
                    return Err(RegistryError::Duplicate(id.clone()));
                }
                self.entries
                    .get(id)
                    .cloned()
                    .ok_or_else(|| RegistryError::Missing(id.clone()))
            })
            .collect()
    }
    pub fn resolved_exact_sources(
        &self,
        ids: &[String],
    ) -> Result<Vec<crate::generated::ResolvedModule>, RegistryError> {
        self.resolve_exact(ids)?
            .into_iter()
            .map(|s| self.describe(s))
            .collect()
    }
    pub fn resolved_sources(
        &self,
        ids: &[String],
    ) -> Result<Vec<crate::generated::ResolvedModule>, RegistryError> {
        self.expand_skills(ids)?
            .into_iter()
            .map(|s| self.describe(s))
            .collect()
    }
    fn describe(
        &self,
        skill: ResolvedSkill,
    ) -> Result<crate::generated::ResolvedModule, RegistryError> {
        if canonical(&skill.path)? != skill.path
            || fs::read(&skill.path).map_err(|e| invalid(&skill.path, e))? != skill.body.as_bytes()
        {
            return Err(invalid(
                &skill.path,
                "source changed since registry admission",
            ));
        }
        let i = self
            .roots
            .iter()
            .position(|r| skill.path.starts_with(r))
            .ok_or_else(|| invalid(&skill.path, "outside configured roots"))?;
        let (kind, subject) = skill
            .name
            .split_once('-')
            .ok_or_else(|| invalid(&skill.path, "invalid identity"))?;
        let text = instructions(&skill.body).map_err(|e| invalid(&skill.path, e))?;
        Ok(crate::generated::ResolvedModule {
            module_identity: skill.name.clone(),
            repository_name: ["psyche-context", "mind-context", "field-context"][i].into(),
            source_revision: self.revisions[i].clone(),
            source_root: self.roots[i].to_string_lossy().into_owned(),
            source_relative_path: skill
                .path
                .strip_prefix(&self.roots[i])
                .unwrap()
                .to_string_lossy()
                .into_owned(),
            module_type: kind.into(),
            module_subject: subject.into(),
            declared_placement: declared_placement(&skill.body).into(),
            source_sha256: sha256(skill.body.as_bytes()),
            body_sha256: sha256(text.as_bytes()),
            string: text.to_owned(),
            string_vector: skill.dependencies,
        })
    }
    fn visit(
        &self,
        id: &str,
        visiting: &mut BTreeSet<String>,
        seen: &mut BTreeSet<String>,
        output: &mut Vec<ResolvedSkill>,
    ) -> Result<(), RegistryError> {
        if seen.contains(id) {
            return Ok(());
        }
        if !visiting.insert(id.into()) {
            return Err(RegistryError::Cycle(id.into()));
        }
        let source = self
            .entries
            .get(id)
            .ok_or_else(|| RegistryError::Missing(id.into()))?;
        for dependency in &source.dependencies {
            self.visit(dependency, visiting, seen, output)?;
        }
        visiting.remove(id);
        seen.insert(id.into());
        output.push(source.clone());
        Ok(())
    }
}
pub trait ExpandsSkills {
    fn expand_skills(&self, roots: &[String]) -> Result<Vec<ResolvedSkill>, RegistryError>;
    fn skill_names(&self) -> Result<Vec<String>, RegistryError>;
}
impl ExpandsSkills for SkillRegistry {
    fn expand_skills(&self, roots: &[String]) -> Result<Vec<ResolvedSkill>, RegistryError> {
        let mut visiting = BTreeSet::new();
        let mut seen = BTreeSet::new();
        let mut output = Vec::new();
        for root in roots {
            self.visit(root, &mut visiting, &mut seen, &mut output)?;
        }
        Ok(output)
    }
    fn skill_names(&self) -> Result<Vec<String>, RegistryError> {
        Ok(self.entries.keys().cloned().collect())
    }
}
fn dependencies(path: &Path, body: &str) -> Result<Vec<String>, RegistryError> {
    let Some((header, _)) = body
        .strip_prefix("---\n")
        .and_then(|b| b.split_once("\n---\n"))
    else {
        return Ok(vec![]);
    };
    let Some(value) = header.lines().find_map(|l| l.strip_prefix("dependencies:")) else {
        return Ok(vec![]);
    };
    let value = value.trim();
    let Some(inner) = value.strip_prefix('[').and_then(|v| v.strip_suffix(']')) else {
        return Err(invalid(path, "dependencies must be an inline ID list"));
    };
    let ids: Vec<String> = inner
        .split(|c: char| c == ',' || c.is_whitespace())
        .filter(|s| !s.is_empty())
        .map(str::to_owned)
        .collect();
    let mut seen = BTreeSet::new();
    if ids.iter().any(|id| !valid_id(id) || !seen.insert(id)) {
        return Err(invalid(path, "invalid or duplicate dependency ID"));
    }
    Ok(ids)
}
```

### Proposal 2: the module ID becomes kind:name · Curriculum › src/registry.rs

```
        +-------------------------+
        | a module: vision:book   |
        +------------+------------+
                     |
     +---------------+---------------+
     |               |               |
     | kept on       | shown by      | written,
     | disk as       | Claude and    | where a
     |               | Codex as      | colon is
     |               |               | refused, as
     v               v               v
+----------+  +--------------+  +-------------+
| folder   |  | /vision:book |  | vision-book |
| vision/, |  | $vision:book |  | in a Nix    |
| file     |  |              |  | store name  |
| book.md  |  |              |  | and OpenCode|
+----------+  +--------------+  +-------------+
```

```rust
  pub fn valid_id(value: &str) -> bool {
  ...
  }
+ /// A module ID is its kind and its subject
+ /// joined by a colon: vision:book.
+ pub fn valid_module_id(value: &str) -> bool {
+     value.split_once(':').is_some_and(|(k, s)| {
+         MODULE_TYPES.contains(&k) && valid_id(s)
+     })
+ }
+ impl SkillEntry {
+     /// The ID where a colon is refused, as in a
+     /// Nix store name: vision-book.
+     pub fn kebab_name(&self) -> String {
+         self.name.replacen(':', "-", 1)
+     }
+ }
```

```rust
  // from_context_repositories, per module file
- let name = format!("{kind}-{subject}");
+ let name = format!("{kind}:{subject}");
```

```rust
  // resolve_exact
- if !valid_id(id) {
+ if !valid_module_id(id) {
```

```rust
  // describe
  let (kind, subject) = skill
      .name
-     .split_once('-')
+     .split_once(':')
```

```rust
  // dependencies
  let mut seen = BTreeSet::new();
- if ids.iter().any(|id| !valid_id(id) || !seen.insert(id)) {
+ if ids.iter().any(|id| {
+     !valid_module_id(id) || !seen.insert(id)
+ }) {
```

Ruling: land, amend, or reject.

## curriculum-deploy › src/runtime.rs

```rust
use std::{
    fs, io,
    path::{Component, Path, PathBuf},
};

use datom_codec::{Actualizing, Budget, Composing, Datomizable, Potential};
use protos::{Protosizable, ReaderBudget, Textualizable};
use thiserror::Error as ThisError;

use crate::catalog::{Skill, SkillCatalog};
use crate::generated::{
    Checked_Data, Generated_Data, GeneratedRoleOutputDocument, GeneratedRoleOutputs, Output,
    Request, RolesDocument, Visualized_Data,
};
use crate::roles::RolePacket;

#[derive(Debug, ThisError)]
pub enum Error {
    #[error("curriculum-deploy accepts exactly one inline Datom request")]
    Argument,
    #[error("{0}")]
    Datom(String),
    #[error("read {0}: {1}")]
    Read(PathBuf, io::Error),
    #[error("write {0}: {1}")]
    Write(PathBuf, io::Error),
    #[error("generated output differs: {0}")]
    Different(PathBuf),
    #[error("roles: {0}")]
    Roles(String),
    #[error("skill {name} is defined by two sources: {first} and {second}")]
    DuplicateSkill {
        name: String,
        first: String,
        second: String,
    },
    #[error("skill template {source_path}: {message}")]
    Template {
        source_path: PathBuf,
        message: String,
    },
}

trait DatomFaulting {
    fn datom_fault(self) -> Error;
}

impl DatomFaulting for datom_codec::Error {
    fn datom_fault(self) -> Error {
        Error::Datom(self.datomize(vec![]).protosize().textualize())
    }
}

trait BudgetedActualizing<T> {
    fn actualize_with_limit(&mut self, limit: i64) -> Result<T, datom_codec::Error>;
}

impl<T: Composing> BudgetedActualizing<T> for Potential<T> {
    fn actualize_with_limit(&mut self, limit: i64) -> Result<T, datom_codec::Error> {
        self.actualize(&mut Budget {
            remaining: limit,
            reader: ReaderBudget {
                remaining: usize::try_from(limit).expect("positive fixed budget"),
            },
            depth: 0,
            maximum_depth: limit,
        })
    }
}

trait DatomTextualizing {
    fn datom_text(&self) -> String;
}

impl<T: Datomizable> DatomTextualizing for T {
    fn datom_text(&self) -> String {
        self.datomize(vec![]).protosize().textualize()
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CommandLine {
    arguments: Vec<String>,
}

impl CommandLine {
    pub fn from_arguments(arguments: impl IntoIterator<Item = String>) -> Self {
        Self {
            arguments: arguments.into_iter().collect(),
        }
    }

    pub fn run(&self) -> Result<String, Error> {
        let [argument] = self.arguments.as_slice() else {
            return Err(Error::Argument);
        };
        if argument.starts_with('-') {
            return Err(Error::Argument);
        }
        let request = actualize_request(argument)?;
        request.execute()
    }
}

fn actualize_request(text: &str) -> Result<Request, Error> {
    Potential::<Request>::from(text)
        .actualize_with_limit(1_024)
        .map_err(DatomFaulting::datom_fault)
}

impl Request {
    fn execute(self) -> Result<String, Error> {
        let (mode, configuration) = match self {
            Self::Generate(configuration) => (Mode::Generate, configuration),
            Self::Check(configuration) => (Mode::Check, configuration),
            Self::Visualize(configuration) => (Mode::Visualize, configuration),
        };
        let deployment = Deployment::read(
            PathBuf::from(configuration.first_string),
            SkillCatalog::read(&configuration.skill_source_vector)?,
            PathBuf::from(configuration.second_string),
        )?;
        let output = match mode {
            Mode::Generate => {
                deployment.write()?;
                Output::Generated(Generated_Data {
                    first_integer: deployment.skills.count() as i64,
                    second_integer: deployment.roles.len() as i64,
                })
            }
            Mode::Check => {
                deployment.check()?;
                Output::Checked(Checked_Data {
                    first_integer: deployment.skills.count() as i64,
                    second_integer: deployment.roles.len() as i64,
                })
            }
            Mode::Visualize => Output::Visualized(Visualized_Data {
                first_integer: deployment.skills.count() as i64,
                second_integer: deployment.roles.len() as i64,
            }),
        };
        Ok(output.datom_text())
    }
}

enum Mode {
    Generate,
    Check,
    Visualize,
}

struct Deployment {
    workspace: PathBuf,
    skills: SkillCatalog,
    roles: Vec<RolePacket>,
    standing_skills: Vec<String>,
}

/// A harness a skill body is rendered for. Pi bodies are parsed but have no
/// projected surface.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum SkillTarget {
    Claude,
    Codex,
    OpenCode,
    Pi,
}

impl SkillTarget {
    /// Every target with a projected surface, in output order.
    const PROJECTED: [Self; 3] = [Self::Codex, Self::Claude, Self::OpenCode];

    /// The workspace directory the harness reads its skills from.
    fn surface(self) -> Option<&'static str> {
        match self {
            Self::Codex => Some(".agents/skills"),
            Self::Claude => Some(".claude/skills"),
            Self::OpenCode => Some(".opencode/skills"),
            Self::Pi => None,
        }
    }
}

struct ConditionalBlock {
    selected: bool,
    otherwise_seen: bool,
}

trait SkillBodyRendering {
    fn rendered_skill(self, skill: &Skill) -> Result<String, Error>;
    fn rendered(self, body: &str, source: &Path) -> Result<String, Error>;
}

impl SkillBodyRendering for SkillTarget {
    /// OpenCode loads a skill only when its frontmatter names it; the other
    /// harnesses name a skill by its directory.
    fn rendered_skill(self, skill: &Skill) -> Result<String, Error> {
        let rendered = self.rendered(&skill.body, &skill.source)?;
        if self != Self::OpenCode {
            return Ok(rendered);
        }
        let name = format!("name: {}\n", skill.name);
        Ok(match rendered.strip_prefix("---\n") {
            Some(rest) => format!("---\n{name}{rest}"),
            None => format!("---\n{name}---\n{rendered}"),
        })
    }

    fn rendered(self, body: &str, source: &Path) -> Result<String, Error> {
        let mut rendered = String::new();
        let mut blocks = Vec::<ConditionalBlock>::new();
        let mut raw = false;

        for (index, line) in body.split_inclusive('\n').enumerate() {
            let line_number = index + 1;
            let directive = line.trim();
            if raw {
                if directive == "{% endraw %}" {
                    raw = false;
                } else if blocks.iter().all(|block| block.selected) {
                    rendered.push_str(line);
                }
                continue;
            }
            let selected = match directive {
                "{% if claude %}" => Some(self == Self::Claude),
                "{% if codex %}" => Some(self == Self::Codex),
                "{% if opencode %}" => Some(self == Self::OpenCode),
                "{% if pi %}" => Some(self == Self::Pi),
                "{% raw %}" => {
                    raw = true;
                    continue;
                }
                "{% endraw %}" => {
                    return Err(Error::Template {
                        source_path: source.to_path_buf(),
                        message: format!("line {line_number}: endraw without raw"),
                    });
                }
                "{% else %}" => {
                    let block = blocks.last_mut().ok_or_else(|| Error::Template {
                        source_path: source.to_path_buf(),
                        message: format!("line {line_number}: else without if"),
                    })?;
                    if block.otherwise_seen {
                        return Err(Error::Template {
                            source_path: source.to_path_buf(),
                            message: format!("line {line_number}: repeated else"),
                        });
                    }
                    block.selected = !block.selected;
                    block.otherwise_seen = true;
                    continue;
                }
                "{% endif %}" => {
                    if blocks.pop().is_none() {
                        return Err(Error::Template {
                            source_path: source.to_path_buf(),
                            message: format!("line {line_number}: endif without if"),
                        });
                    }
                    continue;
                }
                _ => None,
            };
            if let Some(selected) = selected {
                blocks.push(ConditionalBlock {
                    selected,
                    otherwise_seen: false,
                });
                continue;
            }
            if blocks.iter().all(|block| block.selected) {
                if self == Self::Claude && directive == "user-only: true" {
                    rendered.push_str("disable-model-invocation: true\n");
                } else {
                    rendered.push_str(line);
                }
            }
        }

        if !blocks.is_empty() {
            return Err(Error::Template {
                source_path: source.to_path_buf(),
                message: "unclosed if".into(),
            });
        }
        if raw {
            return Err(Error::Template {
                source_path: source.to_path_buf(),
                message: "unclosed raw".into(),
            });
        }
        Ok(rendered)
    }
}

impl Deployment {
    fn read(
        curriculum_root: PathBuf,
        skills: SkillCatalog,
        workspace_root: PathBuf,
    ) -> Result<Self, Error> {
        let role_path = curriculum_root.join("roles.datom");
        let source =
            fs::read_to_string(&role_path).map_err(|error| Error::Read(role_path, error))?;
        let RolesDocument::Roles(roles) = Potential::<RolesDocument>::from(source)
            .actualize_with_limit(16_384)
            .map_err(DatomFaulting::datom_fault)?;
        let standing = roles.standing_skills().map_err(Error::Roles)?.to_vec();
        let mut packets = roles.packets().map_err(Error::Roles)?;
        for packet in &mut packets {
            packet.append_standing_skills(&skills, &standing)?;
            packet.append_authored_procedure(&workspace_root)?;
        }
        Ok(Self {
            workspace: workspace_root,
            skills,
            roles: packets,
            standing_skills: standing,
        })
    }

    fn outputs(&self) -> Result<Vec<(PathBuf, String)>, Error> {
        let mut outputs = Vec::new();
        for skill in self.skills.skills() {
            for target in SkillTarget::PROJECTED {
                let surface = target.surface().expect("projected target has a surface");
                outputs.push((
                    PathBuf::from(surface).join(&skill.name).join("SKILL.md"),
                    target.rendered_skill(skill)?,
                ));
            }
            if user_only(&skill.body) {
                outputs.push((
                    PathBuf::from(".agents/skills")
                        .join(&skill.name)
                        .join("agents/openai.yaml"),
                    "policy:\n  allow_implicit_invocation: false\n".into(),
                ));
            }
        }
        let inventory_paths = self.roles.iter().map(|role| role.path.clone()).collect();
        let inventory = GeneratedRoleOutputDocument::GeneratedRoleOutputs(GeneratedRoleOutputs {
            string_vector: inventory_paths,
        });
        let inventory_text = inventory.datom_text();
        for role in &self.roles {
            outputs.push((PathBuf::from(&role.path), role.text.clone()));
        }
        outputs.push((
            PathBuf::from("skills/generated-role-outputs.datom"),
            inventory_text,
        ));
        outputs.push((
            PathBuf::from("tools/standing-skill-selection.mjs"),
            standing_skill_selection_module(&self.standing_skills),
        ));
        Ok(outputs)
    }

    fn write(&self) -> Result<(), Error> {
        self.clean_previous_skills()?;
        self.clean_previous_roles()?;
        for (relative, body) in self.outputs()? {
            let path = self.safe(&relative)?;
            let parent = path.parent().expect("output parent");
            fs::create_dir_all(parent)
                .map_err(|error| Error::Write(parent.to_path_buf(), error))?;
            fs::write(&path, body).map_err(|error| Error::Write(path, error))?;
        }
        Ok(())
    }

    fn check(&self) -> Result<(), Error> {
        for (relative, expected) in self.outputs()? {
            let path = self.safe(&relative)?;
            let actual =
                fs::read_to_string(&path).map_err(|error| Error::Read(path.clone(), error))?;
            if actual != expected {
                return Err(Error::Different(path));
            }
        }
        Ok(())
    }

    fn clean_previous_skills(&self) -> Result<(), Error> {
        for target in SkillTarget::PROJECTED {
            let relative = Path::new(target.surface().expect("projected target has a surface"));
            let path = self.safe(relative)?;
            if !path.exists() {
                continue;
            }
            for entry in fs::read_dir(&path).map_err(|error| Error::Read(path.clone(), error))? {
                let entry = entry.map_err(|error| Error::Read(path.clone(), error))?;
                let skill_path = entry.path().join("SKILL.md");
                let name = entry.file_name().to_string_lossy().into_owned();
                if skill_path.is_file() && !self.skills.defines(&name) {
                    let retired = entry.path();
                    fs::remove_dir_all(&retired).map_err(|error| Error::Write(retired, error))?;
                }
            }
        }
        Ok(())
    }

    fn clean_previous_roles(&self) -> Result<(), Error> {
        let inventory = self.workspace.join("skills/generated-role-outputs.datom");
        if !inventory.exists() {
            return Ok(());
        }
        let source = fs::read_to_string(&inventory)
            .map_err(|error| Error::Read(inventory.clone(), error))?;
        let Ok(GeneratedRoleOutputDocument::GeneratedRoleOutputs(old)) =
            Potential::<GeneratedRoleOutputDocument>::from(source).actualize_with_limit(1_024)
        else {
            return Ok(());
        };
        for relative in &old.string_vector {
            let path = self.safe(&PathBuf::from(relative))?;
            if path.exists() {
                fs::remove_file(&path).map_err(|error| Error::Write(path, error))?;
            }
        }
        Ok(())
    }

    fn safe(&self, relative: &Path) -> Result<PathBuf, Error> {
        if relative.is_absolute()
            || relative
                .components()
                .any(|component| matches!(component, Component::ParentDir))
        {
            return Err(Error::Argument);
        }
        Ok(self.workspace.join(relative))
    }
}

fn standing_skill_selection_module(names: &[String]) -> String {
    let names = names
        .iter()
        .map(|name| format!("  {name:?},"))
        .collect::<Vec<_>>()
        .join("\n");
    format!(
        "// Generated by curriculum-deploy from Curriculum roles.datom. Do not edit.\nexport const STANDING_SKILLS = Object.freeze([\n{names}\n]);\n"
    )
}

fn user_only(body: &str) -> bool {
    body.strip_prefix("---\n")
        .and_then(|body| body.split_once("\n---\n"))
        .is_some_and(|(frontmatter, _)| frontmatter.lines().any(|line| line == "user-only: true"))
}
```

### Proposal 3: Claude and Codex folders are kind:name, OpenCode stays kebab · curriculum-deploy › src/runtime.rs

```rust
  // impl SkillTarget
+ /// The folder a harness finds a skill in:
+ /// kind:name for Claude and Codex; OpenCode
+ /// refuses a colon and keeps kind-name.
+ fn folder(self, name: &str) -> String {
+     match (self, name.split_once('-')) {
+         (Self::OpenCode, _) | (_, None) => {
+             name.into()
+         }
+         (_, Some((kind, subject))) => {
+             format!("{kind}:{subject}")
+         }
+     }
+ }
```

```rust
  // outputs
- PathBuf::from(surface).join(&skill.name).join("SKILL.md"),
+ PathBuf::from(surface)
+     .join(target.folder(&skill.name))
+     .join("SKILL.md"),
```

```rust
  // outputs, the Codex policy file
  PathBuf::from(".agents/skills")
-     .join(&skill.name)
+     .join(SkillTarget::Codex.folder(&skill.name))
      .join("agents/openai.yaml"),
```

```rust
  // clean_previous_skills: a kind:name folder
  // is the skill kind-name, not a retired one
- if skill_path.is_file() && !self.skills.defines(&name) {
+ let stem = name.replacen(':', "-", 1);
+ let defined = self.skills.defines(&stem);
+ if skill_path.is_file() && !defined {
```

Ruling: land, amend, or reject.

## mind-context › knowledge/vocabulary.md

````markdown
Flow: one run of a voice, from launch to end: its main thread and every subflow it starts; also the Nexus that manages flows.

Flow identity: the canonical short `FLOW_ID` shared by that whole flow.

Flow directory: the main-flow-owned `FLOW_DIRECTORY` shared by that whole flow.

Thread: one running model session and its context. A `THREAD_ID` identifies one thread in a harness.

Transcript: the file the harness writes holding one thread from beginning to end.

Living messenger: the user interface through which a flow reaches the living, asynchronous to the chat; a presentation is one message in it.

Illustrated book: a book to which a model has added illustrations, deciding where each goes. Flashbook, picture book and photo book name the same thing.

Witness: an observation of the thing itself — a test run, a probe,
the code read. What someone says about the thing is a claim.

Quackery: output that stands in for understanding the flow does not
have — a claim it cannot ground, prose that sounds deep over a gap, a
test that only confirms itself.

The living: the living psyche.

Past: the flows a flow has remembered, and theirs in turn.

Base context: the harness-built portion of the top stratum — the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt.

Vision impurity: a working instruction (what to do now, in what order,
at what scope, on which project, through which dispatch) logged as a
vision record.

A defined term overrides competing terminology in the flow's own words.

Machine: short for thinking machine.

Use machine, not AI; use flow, not agent, except when reproducing an external name or quotation.
````

### Proposal 4: basic training reads kind:name · mind-context › knowledge/vocabulary.md

  Machine: short for thinking machine.
+
+ Module name: kind:name, the module's kind (vision, intent, spirit, knowledge, inquiry, compensation, role) before the colon and its hyphenated name after it; vision:book is the vision module book, the file vision/book.md, written vision-book only where a colon is refused.

Ruling: land, amend, or reject.

## mind-context › inquiry/context-source-contracts.md

````markdown
- What authoritative rule maps a module kind and hyphenated filename to a registry Subaspect/Topic key with Topic:Name camelCase validation? Curriculum currently preserves the stem and Flow's shared Topic declaration is String. No such converter was verified; inventing a casing example would not settle its namespace or collision rules.
- Which held queue is intended for prompt-hook consumption: messenger pending delivery, a Flow metaflow queue, or another store? What supported operation selects the current recipient, leases/removes entries, preserves psyche payloads and acknowledges delivery only after native context inclusion? A hook's additionalContext output alone provides none of these queue semantics.
- Which current main source declares and implements that held-queue bridge for each harness, and which native witness proves delivery and duplicate/refusal behavior? Existing pending records and hook support are separate facts; no automatic queue-drain proof was found in the inspected paths.
- What current source should replace or restore the absent vision-flow-ethos module referenced by Psyche's ethos vision? There is no verified hand-maintained or generated current module to choose between. The `.ethos` sources govern their generated Rust types, but that does not decide the intended reviewed vision representation.
- Does Claude's latest distributed implementation exactly match the older version-qualified hook conversion already inspected? Its public GitHub main does not expose that implementation. Current Codex main was checked directly; a claim of identical latest Claude implementation remains unverified.
- Which actual launch path/configuration is in use for each seat, and does it select intent-main-flow despite a metaflow override? Current main declarations establish selection paths, not universal loading by every live layer.
````

### Proposal 5: kind:name beside Ethos's name: import · mind-context › inquiry/context-source-contracts.md

  - What authoritative rule maps a module kind and hyphenated filename to a registry Subaspect/Topic key with Topic:Name camelCase validation? Curriculum currently preserves the stem and Flow's shared Topic declaration is String. No such converter was verified; inventing a casing example would not settle its namespace or collision rules.
+ - In Ethos a name before a colon already means an import from that source (Topic.custom:Name, std:time:[ Instant ]); when a module name such as vision:book is written in Ethos or Datom, is its kind read as a source, is the name quoted, or does one side take another separator?

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
