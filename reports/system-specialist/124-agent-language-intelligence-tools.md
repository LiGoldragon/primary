# Agent Language Intelligence Tools

*Research on LSP, syntax-tree, and code-graph tooling for agents.*

---

## Summary

Agents can benefit materially from language-server and syntax-tree tools,
but the winning shape is not "give the model raw LSP." LSP was designed for
human IDE clients: many operations are position-based, results may be large,
capabilities vary per server, and the server lifecycle assumes an editor
session. The useful agent systems add a second layer: warm indexing, symbol
queries that do not require the model to know the exact cursor position,
result shaping and pagination, safe edit previews, diagnostics after edits,
and workflow constraints that force the agent through the right sequence.

For this workspace, the high-signal direction is an agent-facing language
intelligence component that uses existing language servers and syntax-tree
tools underneath. The component should expose typed agent verbs such as
`SymbolExploration`, `ReferenceImpact`, `RenamePreview`, `SafeSymbolEdit`,
and `DiagnosticVerification`, not raw `textDocument/*` calls. It should be
Nix-packaged, local-first, and testable through architecture witnesses:
LSP was actually used, large result sets were bounded, edits were previewed
before writing, and diagnostics were captured after mutation.

## What LSP Actually Gives

The Language Server Protocol is JSON-RPC between an editor-like client and a
language server. The specification includes the core facts agents usually try
to reconstruct badly with text search: go-to-definition, find references,
document and workspace symbols, diagnostics, code actions, formatting, and
workspace-wide rename.

The useful LSP verbs for agents are:

- symbol discovery: document symbols, workspace symbols;
- semantic navigation: definition, declaration, type definition,
  implementation, references, call hierarchy, type hierarchy;
- validation: diagnostics pushed by the server;
- mutation assistance: rename, code actions, formatting;
- local explanation: hover and signature help.

The limitation is equally important: the protocol is editor-shaped. Many
requests start from a document position. An agent often has a symbol name,
a vague responsibility, or a file-level concern, not a cursor position. The
adapter layer has to translate agent intent into LSP-compatible selectors
and then translate the response back into bounded, agent-useful facts.

Sources:

- Microsoft LSP 3.17 specification: go-to-definition resolves symbol
  definition locations; references resolves project-wide references;
  diagnostics are server-owned validation results; code actions compute
  fixes/refactors; rename computes a workspace edit.
- Tree-sitter documentation: Tree-sitter builds concrete syntax trees and
  updates them incrementally as files change.
- ast-grep documentation: ast-grep is a fast polyglot structural search,
  lint, and rewrite tool built on syntax trees.

## Tool Survey

### Serena

Serena is the most mature-looking general-purpose agent-facing option in this
survey. It is an MCP coding toolkit that exposes semantic retrieval and
editing capabilities. It uses LSP by default and optionally a JetBrains plugin
backend. Its advertised shape matches the right abstraction layer better than
raw LSP: symbol lookup, file outline, references, declaration, diagnostics,
rename, replacing symbol bodies, inserting before/after symbols, and safe
delete. Serena explicitly says the LLM still orchestrates the work; Serena
provides tools.

What looks good:

- LSP-backed symbolic operations rather than raw file search.
- Large language coverage, including Rust and Nix.
- Editing verbs are already symbol-shaped instead of only position-shaped.
- It can be attached to Codex/Claude-style clients via MCP.

Concerns:

- It includes a memory system; this workspace must not use harness-private or
  tool-private memory as durable truth. That part would need to be disabled or
  constrained to disposable tool cache.
- Its own capability table shows LSP backend limits: external dependency
  declaration lookup and implementations vary by language server; move,
  inline, and richer refactors are JetBrains-only.
- Community reports include cases where symbol-finding tools returned no
  results in Claude Code, so server setup and project initialization need
  explicit doctor checks.

### agent-lsp

agent-lsp is a newer MCP server that wraps real language servers, keeps
sessions warm, and adds a skills/workflow layer. Its core argument is highly
aligned with what agents need: raw tools get ignored or misordered, so the
system supplies workflows like impact analysis, safe edit, rename, verify,
and refactor. It also claims CI coverage for many real language servers.

What looks good:

- Warm daemon mode addresses the cold-start/indexing problem.
- It names the exact agent failure: tools alone are not the product; skills
  and phase enforcement are.
- It has speculative edit and diagnostic-delta concepts, which match this
  workspace's architecture-truth-test instinct.
- Its own benchmark writeup claims large token reductions for reference and
  rename tasks compared with grep/read loops.

Concerns:

- It is young. At the time of reading, the GitHub repository is small compared
  with Serena.
- Its published numbers are self-reported by the project. They are useful as
  a direction signal, not as proof for our architecture.
- The public page includes agent testimonials, which are not evidence by
  themselves. The CI-verified-language-server claim is more relevant.

### mcpls

mcpls is a universal MCP-to-LSP bridge. It is Rust-based and aims to expose
type inference, cross-reference analysis, semantic navigation, diagnostics,
code actions, rename, and hover via MCP.

What looks good:

- Rust implementation is culturally closer to this workspace than Python or
  a container-only service.
- It aims at a generic LSP bridge and has explicit per-language configuration.

Concerns:

- It appears closer to a raw bridge than an opinionated agent workflow.
  That means it may reproduce the central failure: the agent gets many tools
  but no enforced sequence.
- It has a smaller visible user surface than Serena.

### lsproxy

lsproxy exposes IDE-like code navigation through a REST API. It runs language
servers and ast-grep underneath, with a unified API and auto-configuration.

What looks good:

- REST API can be easy for non-editor agents to call.
- Combining LSP and ast-grep is the right hybrid pattern: LSP for semantic
  facts, syntax trees for fast structural search and rewrites.

Concerns:

- Its easiest path is Docker. CriomOS discipline says services are NixOS
  modules, not OCI workloads. This can only be a reference or would need
  native Nix packaging.
- Several important features in the docs are marked "Coming Soon":
  diagnostics, call/type hierarchies, procedural refactoring.

### Aider Repo Map

Aider is not primarily an LSP tool. It uses Tree-sitter grammars to build a
repository map that helps the model navigate larger codebases. This is a
proven adjacent pattern: use syntax trees to create compact structural
context, then use normal read/edit tools for the concrete change.

What looks good:

- Mature, widely used terminal coding assistant.
- Tree-sitter repository maps are a robust broad-context primitive.
- It works even where no reliable language server exists.

Concerns:

- Tree-sitter does not know types, macro expansion, trait resolution, import
  resolution, or compiler diagnostics. It is structural, not semantic.
- It is a context-selection technique, not a safe-edit or refactor substrate.

### Tree-sitter and ast-grep Directly

Tree-sitter and ast-grep are the right primitives for fast, deterministic
source-structure work. Tree-sitter supplies incremental concrete syntax
trees. ast-grep supplies structural search, lint, and rewrite across many
languages.

What looks good:

- Fast and local.
- Works without the sometimes-fragile LSP project setup.
- Good for source scans, codemods, architectural checks, and "find all
  functions matching this shape" tasks.

Concerns:

- Syntax trees are not enough for semantic refactors. A syntax match cannot
  prove a reference resolves to the symbol you intend.
- Agents still need a result-shaping layer; raw tree output can be as noisy
  as grep if dumped into context.

## What People Report Is Working

The consistent positive signal is token-efficient, precise navigation:
definition lookup, reference lookup, finding implementations, symbol outlines,
and impact analysis. Serena users report reduced token use and better quality
when the agent can explore symbolically rather than reading whole files. The
agent-lsp author reports large token savings and false-positive reductions on
reference and rename tasks across medium and large repositories. Community
comments around Claude Code LSP support repeatedly name the same desire:
direct access to go-to-definition, references, hover/type info, and diagnostics
outside the IDE UI.

The strongest pattern is hybrid:

- Tree-sitter or ast-grep for broad structural discovery and cheap code maps.
- LSP for type-aware, symbol-specific questions.
- Compiler/build/test commands for final truth.
- Agent skills or phase gates to force the sequence.

That hybrid avoids two bad extremes: grep-only wandering, and raw-LSP floods.

## What Is Not Working

Raw LSP exposed directly to agents is unreliable in practice.

Observed failure modes:

- Agents do not reliably choose the LSP tool unless the workflow forces it.
  Community reports around agent-lsp and Claude Code say instructions alone
  are not enough; agents often fall back to grep/read.
- Large reference results can overflow context. One Claude Code report says a
  `findReferences` call on a TypeScript interface in a roughly 50k-line
  project produced a 250k-token response and made the session unusable.
- LSP position-orientation does not match agent intent. Agents often need
  "the type named X" or "the implementation of this trait method" before they
  know a file/line/column.
- Project setup is fragile. Language servers need the right root, build
  files, toolchain, dependency cache, and sometimes minutes of indexing.
- Language-server capabilities vary. "LSP support" does not imply every
  language supports rename, implementations, call hierarchy, external
  dependencies, or accurate diagnostics equally.
- Diagnostics can be stale or resource-heavy. Community reports name RAM
  usage and stale diagnostics as reasons native LSP support can stay off or
  manual.
- Some bridges stop at "tool exposure" and lack workflow, preview,
  transactional apply, and result limits.

The lesson: LSP is a source of compiler-grade facts, not an agent product.

## Criteria For A CriomOS/Persona-Compatible Shape

If we adopt or build this, the shape should satisfy these constraints:

- Nix-owned installation and tests. No `cargo install`, no Docker service as
  the production path, no mutable application install outside Nix.
- Local-first. The server reads local checkouts and local language servers.
  No paid cloud inference or remote code upload is part of the language
  intelligence plane.
- Warm runtime. Language servers are long-lived per workspace/repo, with
  explicit start, status, and shutdown. Cold-start indexing is surfaced.
- Typed agent verbs. The agent-facing API should not expose raw
  `textDocument/*` as the primary surface. It should expose domain verbs like
  `ExploreSymbol`, `PreviewRename`, `ReferenceImpact`, `ApplyVerifiedEdit`,
  and `CollectDiagnostics`.
- Bounded responses. Every broad query has limits, filters, grouping, and
  continuation tokens or artifact outputs.
- Preview before mutation. Any rename, code action, or symbol edit returns a
  planned workspace edit and diagnostic delta before writing.
- Transactional apply. Mutations are applied atomically or through a clear
  patch artifact that can be reviewed before application.
- Diagnostics as witness. After mutation, diagnostics are captured and
  summarized; full details go to an artifact, not the chat context.
- Syntax-tree fallback. Tree-sitter/ast-grep supplies broad structural
  search when LSP cannot answer or is too expensive.
- No private memory truth. Any "memory" feature in a third-party tool is
  disposable cache only. Durable agent state stays in workspace files or the
  future Persona mind graph.

## Suggested Next Experiment

Do not build from scratch first. Run a Nix-contained comparison on one Rust
repo and one Nix-heavy repo:

1. Package or run, through Nix, one LSP/MCP candidate and one syntax-tree
   candidate:
   - Serena or agent-lsp for LSP workflows;
   - ast-grep and Tree-sitter for structure.
2. Define three benchmark tasks:
   - find every caller of a Rust method and classify test vs production;
   - preview a safe rename and show the exact file edits;
   - inspect a Nix module symbol or option path and find callers/usages.
3. Capture artifacts:
   - tool-call transcript;
   - token-sized response summaries;
   - full result artifact files;
   - before/after diagnostics;
   - final `nix flake check` or component-specific Nix check.
4. Make architectural-truth checks:
   - `reference_impact_cannot_use_text_grep_only`;
   - `rename_cannot_apply_without_preview`;
   - `large_reference_result_cannot_enter_chat_unbounded`;
   - `diagnostic_verification_cannot_skip_language_server`.

The first thing to prove is not that the agent "likes" the tool. It is that
the tool can produce bounded, accurate, inspectable facts that an agent can
use without flooding context or improvising an unsafe edit sequence.

## Source Notes

- Microsoft LSP 3.17 specification:
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/
- Serena repository:
  https://github.com/oraios/serena
- agent-lsp repository:
  https://github.com/blackwell-systems/agent-lsp
- mcpls repository:
  https://github.com/bug-ops/mcpls
- lsproxy documentation:
  https://docs.lsproxy.dev/get-started/introduction
- Aider language and repo-map documentation:
  https://aider.chat/docs/languages.html
- Tree-sitter documentation:
  https://tree-sitter.github.io/tree-sitter/
- ast-grep documentation:
  https://ast-grep.github.io/
- Reinforcement Learning from Compiler and Language Server Feedback:
  https://arxiv.org/abs/2510.22907
- Claude Code / Serena community discussion:
  https://www.reddit.com/r/ClaudeAI/comments/1l42cn6/claude_and_serena_mcp_a_dream_team_for_coding/
- Claude Code LSP result-size complaint:
  https://www.reddit.com/r/ClaudeCode/comments/1q83m0x/is_lsp_support_in_claude_code_dead_on_arrival/
- agent-lsp workflow discussion:
  https://www.reddit.com/r/mcp/comments/1t7li5c/ai_coding_agents_cant_use_lsp_tools_correctly_so/
