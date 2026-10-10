# Clojure Database: Datalevin

## Database Information

**Name:** Datalevin

**What it is:** A Clojure and Java Datalog database built on LMDB (Lightning Memory-Mapped Database). It provides an immutable, queryable in-process database compatible with Datomic's Datalog syntax but optimized for simplicity and performance.

## Projects Using Datalevin

1. **clojure-experiments** (`/git/github.com/jumarko/clojure-experiments`)
   - Uses Datalevin v0.6.29 (in deps.edn)
   - Includes direct usage in `src/clojure_experiments/datomic/datalevin.clj`
   - Status: Active use

2. **clojure-lsp** (`/git/github.com/clojure-lsp/clojure-lsp`)
   - Previously used Datalevin for cache database (v0.5.26-0.5.27)
   - Later replaced with transit format for faster startup and better GraalVM compatibility
   - Status: Deprecated in favor of transit caching

## Correction

**Datalevin is written in Clojure and Java, not Rust.** It runs on top of LMDB, a C library for memory-mapped I/O. Earlier reports suggesting Datalevin was Rust-backed were inaccurate.

## Sources

- `/git/github.com/jumarko/clojure-experiments/deps.edn` - Datalevin dependency declaration
- `/git/github.com/jumarko/clojure-experiments/src/clojure_experiments/datomic/datalevin.clj` - Direct usage example
- `/git/github.com/clojure-lsp/clojure-lsp/CHANGELOG.md` - Historical usage and migration notes
- Datalevin repository: https://github.com/juji-io/datalevin
