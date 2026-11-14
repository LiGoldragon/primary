Presentation.{ «A socket appears when it listens» Proposal }

# A socket appears when it listens

Created by Fable 5.1, on a line from Mind flowNexus Opus, through Psyche core Opus.

### Proposal 1: Appearance is readiness · psyche-belief › vision/nexus-v1.md

::: comment
A Nexus watching a place for a peer's socket had read a permission change as readiness. If the socket exists at its name only once it listens, its appearance is the one readiness event, and every watcher waits on the same thing. Implemented in Flow and Energy; the line makes it the contract every Nexus at a place keeps.
:::

+ A socket appears at its name only when it listens: a Nexus binds it under a temporary name, listens, and renames it into place in one step. A peer watching the place waits on that appearance and nothing else; the socket being there is the Nexus being ready.

```rust
+ let listener = UnixListener::bind(&temporary)?;   // bound and listening under the temporary name
+ std::fs::rename(&temporary, &place.socket)?;      // one step: the socket exists at its name, ready
```
