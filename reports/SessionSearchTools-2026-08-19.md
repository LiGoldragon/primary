# Session Search Tools — Research

2026-08-19. Research subflow.

**Context:** workspace keeps one markdown file per session under
`sessions/<aspect>/` and psyche rulings under `psyche/Vision/<topic>.md` and
`psyche/Intent/`. A subflow role needs to find, quickly and reliably, the
recent session content and psyche rulings that bear on a parent flow's work.
The psyche has also ruled (session `7c3f0c1d`, 2026-08-19) that sessions
should be indexed in a separate file so the right session is easier to find.

**Material shape (observed, not reported):** Session files are 50–320 lines,
YAML frontmatter with short-id and description, heading-structured body
(Objective, State recovered, Rulings logged, Open forks). Psyche Vision files
use dated heading entries (e.g. `## 2026-08-11 — topic`) followed by verbatim
quoted psyche words and agent-authored provenance paragraphs. Both shapes are
well-suited to heading-scoped grep. The session-log skill requires a terse
summary section at the top of each session file.

---

## 1. Local Full-Text Search (CLI)

### ripgrep

- **What it indexes:** no index; searches files directly on each call
- **How an agent calls it:** `rg --type md -C 3 "pattern" sessions/ psyche/`; JSON output via `--json`
- **Build/update cost:** none
- **Heading-scoped hits:** no native support; headings reachable via multiline patterns or `-B`/`-A` flags; structured heading context requires post-processing
- **Note:** Claude Code switched its own search layer from ripgrep to ugrep in April 2026 (v2.1.117). ugrep is a drop-in replacement with compressed-file support and broader regex compatibility.

Sources: [Code Search for AI Agents](https://ceaksan.com/en/code-search-for-ai-agents-which-tool-when), [Ripgrep at 10 Years](https://www.buildmvpfast.com/blog/ripgrep-10-years-fast-cli-tools-ai-agents-2026)

### SQLite FTS5 (with markdown import script)

- **What it indexes:** markdown body parsed into documents + sections tables; YAML frontmatter fields as columns (short-id, description, date, aspect); section text under its heading
- **How an agent calls it:** `sqlite3 sessions.db "SELECT snippet(notes_fts, ...) FROM notes_fts WHERE notes_fts MATCH 'skill session-log'"`; or a thin wrapper script
- **Build/update cost:** one-time import script; incremental via a file-watcher script or pre-agent hook; index can drift if not triggered
- **Heading-scoped hits:** yes, if sections table stores (document, heading, body); BM25 ranking via `rank` column; `snippet()` function returns context around hits
- **Prior art:** markdown-vault-mcp implements a SQLite FTS5 schema with documents, sections, document_tags, and notes_fts tables for markdown indexing. hugo-search-indexer parses YAML frontmatter and markdown body into FTS5 tables.

Sources: [markdown-vault-mcp FTS5 issue](https://github.com/pvliesdonk/markdown-vault-mcp/issues/3), [sqlite-memory](https://github.com/sqliteai/sqlite-memory), [SQLite FTS5 projects](https://lausanne.aitinkerers.org/technologies/sqlite-fts5)

### sqlite-memory (sqliteai)

- **What it indexes:** markdown content chunked into persistent agent memory; hybrid FTS5 + vector (local llama.cpp embeddings)
- **How an agent calls it:** SQLite extension; SQL queries or bundled API
- **Build/update cost:** extension install; chunking on ingest
- **Heading-scoped hits:** yes (markdown-aware chunking); returns both keyword and semantic context
- **Network-free:** yes; local llama.cpp for embeddings

Source: [sqlite-memory](https://www.sqlite.ai/sqlite-memory)

### Tantivy / tantivy-cli

- **What it indexes:** full document text; schema-defined fields
- **How an agent calls it:** `tantivy search -i <index> -q "pattern"` or REST
- **Build/update cost:** index build step required; not auto-incremental
- **Heading-scoped hits:** no; returns documents, not sections
- **Note:** BM25 ranking; Rust; a local code+markdown search tool built on Tantivy exists but is not a maintained CLI product

Source: [tantivy](https://github.com/quickwit-oss/tantivy)

### Meilisearch / Typesense

- **What it indexes:** JSON documents ingested via API
- **How an agent calls it:** REST API; requires a running daemon
- **Build/update cost:** server process overhead; daemon must be running
- **Heading-scoped hits:** yes, if sections are ingested as separate records
- **Note:** overkill for a local personal-workspace use case; both are designed for web-app search

Source: [Meilisearch vs Typesense 2026](https://www.pkgpulse.com/guides/meilisearch-vs-typesense-vs-algolia-search-engine-apis-2026)

### QMD (Query Markdown)

- **What it indexes:** markdown files; BM25 for keyword, vector embeddings for semantic, local LLM for reranking
- **How an agent calls it:** `qmd search "query"` CLI; also an MCP server variant
- **Build/update cost:** index build step; local GGUF model required for reranking (Llama 3, Mistral, Phi-3)
- **Heading-scoped hits:** yes (semantic chunking); returns heading context
- **Network-free:** yes; node-llama-cpp runs GGUF locally without GPU or API keys
- **Note:** purpose-built for markdown knowledge bases; Node.js / Bun runtime

Sources: [qmd (tobi)](https://github.com/tobi/qmd), [qmd blog](https://www.blog.brightcoding.dev/2026/04/28/qmd-the-revolutionary-local-search-engine-for-developers), [qmd MCP variant](https://github.com/ehc-io/qmd)

---

## 2. Semantic / Embedding Local Search

### llm CLI (Simon Willison)

- **What it indexes:** arbitrary text; embeddings stored in SQLite via `llm embed`; similarity search via `llm similar`
- **How an agent calls it:** `llm embed-multi sessions -d sessions.db --files sessions/ '**/*.md'` then `llm similar -d sessions.db -c "skill ruling"`
- **Build/update cost:** embed step per file; incremental by re-running on changed files; SQLite stores the index
- **Network-free:** yes, with local embedding plugins (llm-sentence-transformers); otherwise requires API
- **Heading-scoped hits:** no; returns whole-document similarity scores; chunking must be done manually before embedding

Sources: [llm CLI](https://llm.datasette.io/), [PyPI](https://pypi.org/project/llm/), [TILs on embeddings](https://til.simonwillison.net/llms)

### sqlite-vec + manual embedding pipeline

- **What it indexes:** embedding vectors stored in SQLite; combined with FTS5 for hybrid BM25 + vector retrieval
- **How an agent calls it:** SQL: `SELECT ... FROM vec_index WHERE ... ORDER BY distance`; can run from sqlite3 CLI
- **Build/update cost:** embedding generation step (local model via Ollama or llama.cpp); index stored in .sqlite file
- **Network-free:** yes with local model
- **Heading-scoped hits:** yes if sections are embedded separately

Sources: [sqlite-vec article](https://ai.plainenglish.io/embedded-intelligence-how-sqlite-vec-delivers-fast-local-vector-search-for-ai-de6d62936055), [local-first RAG](https://www.pingcap.com/blog/local-first-rag-using-sqlite-ai-agent-memory-openclaw/)

### memweave

- **What it indexes:** markdown files as primary storage; local SQLite indexes for BM25 + vector hybrid
- **How an agent calls it:** Python library / CLI
- **Build/update cost:** indexing on ingest; SQLite-backed
- **Network-free:** yes
- **Heading-scoped hits:** depends on chunking strategy

Source: [memweave](https://towardsdatascience.com/memweave-zero-infra-ai-agent-memory-with-markdown-and-sqlite-no-vector-database-required/)

### Khoj

- **What it indexes:** markdown files, PDFs, notes; self-hostable
- **How an agent calls it:** REST API or chat interface; not a headless CLI in the traditional sense
- **Build/update cost:** server deployment; local LLM support (llama, mistral, etc.)
- **Network-free:** yes (fully self-hosted)
- **Heading-scoped hits:** yes (document chunking)
- **Note:** designed as a personal AI second brain, not a targeted subagent search tool

Source: [khoj](https://github.com/khoj-ai/khoj)

---

## 3. Agent Products and Session-History Memory

### Claude Code (CLAUDE.md + Auto Memory / MEMORY.md)

- CLAUDE.md: explicit, human-authored, loaded at session start as ground truth. Not searchable — flat injection. (Claim from blog.memoryplugin.com)
- Auto Memory (MEMORY.md): Claude Code discovers project patterns and writes them back autonomously; first 200 lines or 25KB loaded at session start. Also flat injection, not queryable. (Claim from developersdigest.tech)
- Neither system provides a search API an agent can call to retrieve specific past session content.

Sources: [Claude Code Memory](https://blog.memoryplugin.com/claude-code-memory/), [Auto Memory guide](https://www.developersdigest.tech/guides/auto-memory)

### Codex (AGENTS.md)

- Flat-file instructions, similar architecture to CLAUDE.md. Not searchable. (Claim from hackernoon.com)

Source: [Agent memory files guide](https://hackernoon.com/the-complete-guide-to-ai-agent-memory-files-claudemd-agentsmd-and-beyond)

### agentmemory (rohitg00)

- **What it indexes:** every tool call, decision, file interaction; BM25 + ONNX embeddings (zero-LLM mode)
- **How an agent calls it:** 54 MCP tools or 130 REST endpoints; integrates with Claude Code, Codex CLI, Cursor, Gemini CLI
- **Build/update cost:** single Node.js process; auto-capture hooks; zero external databases
- **Network-free:** yes (ONNX embeddings on-device)
- **Session-history search:** yes — retrieval at R@5 claimed at 95.2% accuracy; 92% fewer tokens for re-contextualization (claims from repo README)
- **Note:** the only product in this survey that explicitly solves "subagent retrieves relevant past session content before starting work" as its primary use case

Sources: [agentmemory](https://github.com/rohitg00/agentmemory), [agent-memory.dev](https://www.agent-memory.dev/)

### Mem0

- Cloud-hosted vector DB extraction; memory searchable via API. Priced $0–$249/month. Network-dependent. (Claims from edenai.co)

Source: [Mem0 vs Letta](https://vectorize.io/articles/mem0-vs-letta)

### Zep

- Temporal knowledge graph + vector search. Credit-based pricing from $25/month. Network-dependent. (Claims from agentmarketcap.ai)

Source: [Agent Memory in Production 2026](https://agentmarketcap.ai/blog/2026/04/11/agent-memory-architecture-production-2026)

### Letta (formerly MemGPT)

- Full agent runtime with OS-inspired three-tier memory: core / recall / archival. Designed for long-running agents (weeks, not sessions). (Claims from vectorize.io)

Source: [Mem0 vs Letta](https://vectorize.io/articles/mem0-vs-letta)

---

## 4. Prior Art for Index / Summary Files as Primary Discovery Surface

### Zettelkasten index notes

- Index entries are title-only, marked with IDs (e.g. 0000.0000.0), tagged `type::"#moc"`. Used as navigation entry points, not search replacements.
- Stays usable because entries are atomic (one idea) and the index is small relative to the corpus.

Source: [Zettelkasten Forum](https://forum.zettelkasten.de/discussion/2755/how-do-you-find-the-proper-index-note)

### Obsidian MOCs (Maps of Content)

- Notes that list links to clusters of related notes. Not exclusive like folders; a note can appear in multiple MOCs. Over 1.5M monthly active Obsidian users as of 2025. (Claim from obsibrain.com)
- Stays usable because each MOC is a curated list, not auto-generated; curators update it intentionally.

Source: [MOC in Zettelkasten](https://publish.obsidian.md/johndray/020+Zettelkasten/Understanding+Map+of+Content+(MOC)+in+Zettelkasten)

### ADR (Architecture Decision Records) logs

- Numbered monotonically (0042-use-sqlite.md). Each ADR has a status field: proposed / accepted / superseded. An index file lists all records with status.
- Stays usable because: monotonic numbering gives stable references; status field allows filtering without reading full records; each ADR is self-contained; the directory listing alone reads as a summary.
- Tools: Log4brains generates interactive sites from ADR directories.

Sources: [adr.github.io](https://adr.github.io/), [Martin Fowler on ADRs](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html)

### git log as index

- `git log --oneline` is an instant session index if commit messages are written well. Churn from file renaming defeats it (commit messages reference old names). Stable filenames are prerequisite.

### Changelogs

- CHANGELOG.md by version: entry per version with one-line summary of changes. Stays usable with disciplined short entries; degrades when entries become verbose.

**Common pattern across all that stay usable:** short, curated entries (title + status/date + one line); stable references (no renaming); machine-writable format; updated intentionally at defined moments, not continuously.

**Psyche ruling on the index file** (session `7c3f0c1d`, 2026-08-19, typed):

> "we should index them in a separate file, so the right session is easier to find"

The same ruling established that session files drop frontmatter, adopt a terse summary section at the top (re-editable as the session goes), and are named by short-id. The index file is ruled; its format is not yet specified.

---

## 5. Structured-Data Route

### Psyche on Datom

datomSyntax.md, 2026-08-11 (typed, correcting Designer's syntax sheet):

> "datom doesnt do generics, it only carries data, like json (but strictly typed of course)"

Datom is the data carrier for this workspace's language stack — strictly typed, JSON-like. It is the data layer; Ethos is the computation layer. No ruling was found in datomSyntax.md or surveyingAllFlows.md on using Datom records specifically as a session/ruling index.

surveyingAllFlows.md contains only a single ruling: the psyche's desire for a surveying aspect ("Overseer maybe"), with no technical specification of how it would access session or psyche data.

### What the structured-data route buys over grep

Keeping sessions and rulings as typed records in SQLite (or eventually Datom, if the workspace's own stack matures to support queries) enables queries that grep structurally cannot answer:

- "All open forks mentioning topic X from the last 14 days" (join sessions × forks × date)
- "All psyche rulings on topic Y, ordered by date, latest first" (ruling text is a column, date is filterable)
- "Which sessions touched aspect 'design' and contain the term 'session-log'" (aspect is a column, FTS for the term)
- Deduplication and supersession tracking: a `superseded_by` column lets agents skip stale rulings

**Schema sketch** (agent-callable via `sqlite3`):

```sql
CREATE TABLE sessions(
  short_id TEXT PRIMARY KEY,
  aspect TEXT,
  started_at TEXT,
  description TEXT,
  summary TEXT           -- terse summary section, re-editable
);
CREATE VIRTUAL TABLE sessions_fts USING fts5(
  short_id UNINDEXED, summary, content='sessions', content_rowid='rowid'
);

CREATE TABLE rulings(
  topic TEXT,
  heading TEXT,
  date TEXT,
  body TEXT,             -- verbatim psyche quote + provenance
  superseded_by TEXT     -- heading of later ruling on same subject, or NULL
);
CREATE VIRTUAL TABLE rulings_fts USING fts5(
  topic UNINDEXED, heading UNINDEXED, body, content='rulings', content_rowid='rowid'
);
```

**Build/update cost:** a script that parses session frontmatter + summary section and psyche Vision heading entries into these tables. Must run before an agent's search subflow starts. Incremental via file modification timestamps.

**What it does not buy:** semantic matching; requires disciplined schema evolution as the session format changes.

---

## Comparison Table

| Tool | Build step | Incremental | Heading-scoped | Network-free | Agent call form | Returns context |
|------|-----------|-------------|----------------|--------------|-----------------|-----------------|
| ripgrep / ugrep | None | N/A (no index) | No (regex only) | Yes | CLI one-liner | Yes (-C flag) |
| SQLite FTS5 (import script) | Yes | Manual / watcher | Yes (sections table) | Yes | sqlite3 SQL | Yes (snippet()) |
| sqlite-memory | Yes (extension) | Yes | Yes (chunked) | Yes | sqlite3 / API | Yes |
| QMD | Yes (index build) | Partial | Semantic | Yes (local GGUF) | CLI | Yes |
| llm CLI + sqlite-vec | Yes (embed step) | Yes | Semantic | Yes (local plugin) | CLI | Yes |
| agentmemory | Yes (server) | Yes (auto-capture) | Semantic + BM25 | Yes | MCP / REST | Yes |
| Tantivy-cli | Yes (index build) | Manual | No | Yes | CLI | Yes |
| Meilisearch / Typesense | Yes (server daemon) | Yes | Yes (per-section ingest) | Yes | REST | Yes |
| Index file + ripgrep | Index: manual; rg: none | Index: per-session | Index: yes; rg: regex | Yes | Read file + CLI | Yes |

---

## Top Three Options (trade-offs stated, not a decision)

### Option A — ripgrep / ugrep (zero build step)

No setup; works on the markdown files as canonical source; an agent can call it as a one-liner from any context. Retrieves context lines around hits. Usable today, no infrastructure change.

Trade-off: structurally blind to headings as semantic units; cannot answer "all rulings under heading X" without post-processing; no ranking; false positives in verbose prose files. Effective only when the agent knows a distinctive keyword. Degrades as the corpus grows.

### Option B — SQLite FTS5 with a per-section import script

An import script (runnable as a pre-search hook) parses session summary sections and psyche Vision heading entries into a sections table. The agent calls `sqlite3` with FTS5 MATCH queries, gets BM25-ranked results with `snippet()` context and structured column filters (aspect, date, topic). Combines naturally with the per-session index file: the index file is fast-path navigation; FTS5 is deep search.

Trade-off: the import script must be written and maintained; schema evolves with the session-log format; index drifts if not triggered before each search subflow run. No semantic matching — misses synonymous terms.

### Option C — Per-session index file as primary surface + ripgrep as fallback

The psyche has ruled the index file (2026-08-19). The index lists sessions with their short-id and terse summary; a subflow agent reads the index first, identifies candidate sessions by summary text, then targets those files with ripgrep for the specific content. Similarly, psyche Vision files have dated headings that are already a human-readable index within each topic file.

Trade-off: quality depends entirely on how well session summaries are written by prior agents — a weak summary makes a session invisible to the index-scan step; no ranking; the index file itself must be kept current. Lowest infrastructure cost; highest reliance on human/agent discipline at write time.

**Relationship between options:** these are not mutually exclusive. The index file (Option C) is ruled and low-cost to start. Option B adds structured querying on top without displacing the index. Option A fills in when neither the index nor the database is available.
