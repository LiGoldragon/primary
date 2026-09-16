# proposal · transcript-nexus

*Flow 48cff7 · 2026-09-16 · pending living review*
*Kind: new skill*
*Source records: flows/48cff7/vision/transcriptNexus.md*

---

## description

Extracting a block from a session transcript — the block bounded by two anchor phrases, or a live-typed message with context, or a raw record at a line.

## body

The transcript nexus is a Nexus: `transcript-nexus` binary, ordinary and meta sockets, sema store, Signal wire, `transcript` and `transcript-meta` CLIs each taking one inline datom.

Signal operations paired with their typed replies:

- `Show.{ session_ref  context  cap }` → `Shown` — every typed message with preceding assistant context.
- `Search.{ pattern  recent  over }` → `Searched` — regex over typed messages; `over` widens to assistant text.
- `Raw.{ session_ref  lines }` → `RawLines` — raw records at line numbers.
- `Block.{ session_ref  from  to  scope  which }` → `Blocked | NoMatch | Ambiguous` — the block between two anchor phrases.

Anchors are literal substrings; `scope` and `which` disambiguate.

The pre-nexus argparse shim at `/git/github.com/LiGoldragon/transcript` is misimplemented; it stands only until the nexus runs.
