<!-- to-the-living:start -->
Presentation.{ «A Nexus reads a value from a datom file» }

How it is now. A datom value reaches a Nexus only as an argument string. The Orchestrate CLI (`/git/github.com/LiGoldragon/orchestrate/crates/orchestrate/src/main.rs`, workspace 0.36.1, HEAD `bc5cd36`, 2026-10-02) takes `env::args()`, refuses anything but one inline datom ("accepts exactly one inline Datom query and no flags"), actualizes it with `Potential::<Query>::from(source).actualize(&mut budget)` from datom-codec 0.31.0 (rev `09e2a9d`), signalizes the typed `Query` into a `Dispatch::Open` and writes it as one frame of `signal`; `orchestrate-nexus/Cargo.toml` carries "No `datom-codec` and no `protos`". Two components keep a settings file outside that path: the aggregator daemon (aggregator 0.7.0, `01fba5e`) reads `configuration.datom` itself through `--configuration` (`src/daemon.rs` lines 35 to 38, `std::fs::read_to_string` then `DatomText::read`, datom-codec 0.27.0), and its CLI reads the same file for the socket paths (`src/client.rs` line 37); Lojix 6.0.0 (`c4bba4f`) has `lojix-write-configuration` turn one inline datom into an rkyv archive, which the Nexus loads from the path in `LOJIX_CONFIGURATION`. The skill `datom` (Curriculum `c7d35e2`, `skills/datom.md` line 95) says "datom passes inline at a CLI boundary, never as a datom file"; the corpus lists this as the tension "Settings file" (`flows/bad807/reports/ethos-nexus-corpus.md` line 9150). The ethos below is checked and generated with ethos-zero 16.0.0 (`c2653dd`), and nothing here was run against a live socket.

His words (typed, book comment, 2026-10-04, on «The Nexus»): "let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this … a variant `me` [sic] that would tell it what type of CLI you would have to use … There's a string involved no matter what unless all of that is, again, put into an external tool."

Three ways the value can travel from the file to the Nexus:

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="330" viewBox="0 0 700 330" font-family="sans-serif" font-size="13">
  <rect x="0" y="0" width="700" height="330" fill="#ffffff"/>
  <defs><marker id="f8" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
  <g font-weight="bold" font-size="14"><text x="12" y="24">a) the Nexus runs a reader</text><text x="12" y="134">b) the Nexus asks, the CLI answers</text><text x="12" y="244">c) the caller reads, the Nexus unchanged</text></g>
  <g fill="#fff4d6" stroke="#a07800"><rect x="20" y="40" width="90" height="50" rx="6"/><rect x="20" y="150" width="90" height="50" rx="6"/><rect x="20" y="260" width="90" height="50" rx="6"/></g>
  <g text-anchor="middle"><text x="65" y="70">file.datom</text><text x="65" y="180">file.datom</text><text x="65" y="290">file.datom</text></g>
  <g fill="#eeeeee" stroke="#555"><rect x="170" y="40" width="150" height="50" rx="6"/><rect x="170" y="150" width="150" height="50" rx="6"/><rect x="170" y="260" width="150" height="50" rx="6"/></g>
  <g text-anchor="middle"><text x="245" y="62">reader subprocess</text><text x="245" y="80" font-size="11">spawned by the Nexus</text>
    <text x="245" y="172">CLI, connected</text><text x="245" y="190" font-size="11">reads when asked</text>
    <text x="245" y="282">shell and CLI</text><text x="245" y="300" font-size="11">$(cat file.datom)</text></g>
  <g fill="#dcebff" stroke="#2a5db0"><rect x="430" y="40" width="150" height="50" rx="6"/><rect x="430" y="150" width="150" height="50" rx="6"/><rect x="430" y="260" width="150" height="50" rx="6"/></g>
  <g text-anchor="middle"><text x="505" y="70">Nexus</text><text x="505" y="180">Nexus</text><text x="505" y="290">Nexus</text></g>
  <g stroke="#333" stroke-width="1.6" marker-end="url(#f8)">
    <line x1="110" y1="65" x2="168" y2="65"/><line x1="320" y1="72" x2="428" y2="72"/><line x1="428" y1="52" x2="322" y2="52"/>
    <line x1="110" y1="175" x2="168" y2="175"/><line x1="428" y1="160" x2="322" y2="160"/><line x1="320" y1="188" x2="428" y2="188"/>
    <line x1="110" y1="285" x2="168" y2="285"/><line x1="320" y1="285" x2="428" y2="285"/></g>
  <g font-size="11" text-anchor="middle"><text x="375" y="47">spawn "lojix-read" path</text><text x="375" y="86">rkyv on stdout</text>
    <text x="375" y="155">ReadFile.Roster.path</text><text x="375" y="202">Supply.{ path Roster.[…] }</text>
    <text x="375" y="280">Configure.{ … }</text></g>
  <g font-size="12" fill="#b00"><text x="595" y="60">program name</text><text x="595" y="76">and path</text><text x="595" y="170">path only</text><text x="595" y="280">no string</text></g>
</svg>

*Where the string lives, right: in a, the Nexus holds a program name and a path; in b only a path, as a typed position; in c nothing, since the shell composes the inline datom.*

### a) The Nexus runs a reader as a subprocess

Ethos added: none to the Signal; the reader is a Memory value, his variant naming the CLI. The names `Orchestrate`, `Lojix`, `orchestrate-read` and `lojix-read` are the flow's illustration; no such reader binary exists.
```
Reader.[ Orchestrate Lojix ]               ; which reader program the Nexus spawns
```
Rust, Nexus side, compiled without `datom`:
```rust
impl Invoking for Reader {
    fn program(&self) -> &'static str {
        match self { Self::Orchestrate => "orchestrate-read", Self::Lojix => "lojix-read" }
    }
    fn read_roster(&self, path: &FilePath) -> Result<Roster, ReadFailure> {
        let output = std::process::Command::new(self.program()).arg(path).output().map_err(|_| ReadFailure::Spawn)?;
        if !output.status.success() { return Err(ReadFailure::Exit) }
        rkyv::from_bytes::<Roster, rkyv::rancor::Error>(&output.stdout).map_err(|_| ReadFailure::Archive)
    }
}
```
Compiled in the scratch crate, Nexus side without the `datom` feature (2026-10-04).

The string lives in the Nexus: one program name per variant, and the path as an argument. The no-text rule keeps its letter (the Nexus parses no datom) and loses its spirit: the Nexus starts processes by name and trusts their stdout, and every contract needs a reader binary that prints rkyv, which no CLI of ours does today.
- For: the Nexus pulls on its own, at any time, with no caller connected.
- Against: a command string and a process boundary inside the Nexus; a reader binary per contract.
- Against: what runs is decided by `PATH` on the host, not by the contracts the Nexus is compiled with.

### b) The Nexus asks; the CLI reads, decodes and sends the typed value

Ethos added to the Signal. `Roll`, `roll-meta`, `Roster` and `Member` are the flow's invented example names. Checked with ethos-zero 16.0.0: `Check` answers `Checked` (2026-10-04).
```
Signal
[]                                                ; imports
[ Configure.Configuration                         ; queries
  Supply.Supplied ]                               ;   the CLI hands in what was asked for
[ Configured                                      ; responses
  ReadFile.Wanted                                 ;   the Nexus asks the caller for a file
  Refused.[ NotWanted.FilePath ] ]                ;   a supply nobody asked for
[ FilePath.String                                 ; types
  Wanted.[ Configuration.FilePath                 ;   the variant names the type, and so the CLI
           Roster.FilePath ]
  Supplied.{ FilePath Reading.[ Configuration.Configuration
                                Roster.Roster
                                Missing
                                Unreadable ] }
  Configuration.{ SocketPath.FilePath Roster }
  Roster.Vector<Member>
  Member.String ]
```
Rust, the Nexus's answer (compiled in the scratch crate without the `datom` feature, 2026-10-04):
```rust
impl Answering for Roll {
    fn answer(&mut self, query: Query) -> Response {
        match query {
            Query::Configure(Configuration { roster, .. }) if roster.is_empty() =>
                Response::ReadFile(Wanted::Roster(self.roster_path.clone())),
            Query::Configure(Configuration { roster, .. }) => { self.roster = Some(roster); Response::Configured }
            Query::Supply(Supplied { file_path, reading: Reading::Roster(roster) }) if file_path == self.roster_path =>
                { self.roster = Some(roster); Response::Configured }
            Query::Supply(Supplied { file_path, .. }) => Response::Refused(Refused_Data::NotWanted(file_path)),
        }
    }
}
```
Rust, the CLI's supply (compiled in the scratch crate with datom-codec 0.32.2, 2026-10-04):
```rust
impl RosterFile<'_> {
    fn read(&self) -> Reading {
        let Ok(text) = std::fs::read_to_string(self.0) else { return Reading::Missing };
        let mut budget = Budget { remaining: 10_000, reader: ReaderBudget { remaining: 10_000 }, depth: 0, maximum_depth: 256 };
        Potential::<Roster>::from(text).actualize(&mut budget).map(Reading::Roster).unwrap_or(Reading::Unreadable)
    }
}
```
Run in the scratch crate on a good, a malformed and a missing file (2026-10-04), on `[ Ada Grace «Barbara Liskov» ]`, it answers `Supply(Supplied { file_path: "…/roster.datom", reading: Roster(["Ada", "Grace", "Barbara Liskov"]) })`; on `[ Ada { }` it answers `Unreadable`; on a missing file `Missing`.

On `signal` 8.0.0 the querying side only opens exchanges (`Dispatch::{ Greet Open Abandon }`), so the CLI answers `ReadFile` on exchange 1 by opening exchange 2 with `Supply`, on the same connection; the frame and the greeting stay as they are. The string lives in the Nexus as one `FilePath` position, held in Memory and never opened or parsed by the Nexus. His variant naming the CLI becomes the `Wanted` variant naming the type: the CLI built with that contract is the one already connected, so no program name is stored.
- For: no datom, no file access and no command string in the Nexus; the Nexus still decides which file and which type.
- For: works on `signal` 8.0.0 unchanged; the CLI side is about 20 lines per contract, generated from the `Wanted` variants.
- Against: the Nexus can ask only while a CLI is connected; a pull with no caller present needs a.

### c) The caller reads the file; the Nexus is unchanged

Ethos added: none. The shell composes the one inline datom, so the CLI also stays unchanged:
```sh
roll-meta "Configure.{ /run/roll/roll.sock $(cat roster.datom) }"
# actualized in the scratch crate (2026-10-04) as Configure(Configuration { socket_path: "/run/roll/roll.sock", roster: ["Ada", "Grace", "Barbara Liskov"] })
```
No string anywhere in the Nexus. The cost to the no-text rule is nil. The second way of his 2026-09-29 words (183ae0, a notion), "next to it would be the compiled signal file so that then the Nexus could load it because it's already signal", is this way with the reader writing an archive, which is what `lojix-write-configuration` does today; the Nexus then holds the archive's path.
- For: free today, for every Nexus; nothing to design or build.
- Against: the Nexus cannot pull; the caller must know which file holds which position.
- Against: the file must hold exactly one position's value; it cannot be spliced in deeper than the shell can quote.

### What the flow proposes

Way b, for the Nexuses that declare it, with c left as what every Nexus has already. It is the one way in which the Nexus pulls, as he asks, and still sees only signal: the variant he wanted names a type, never a program; the one string is a path, held and passed, never read. Way a puts a command string and a process boundary into the Nexus, which is the string he wanted out "unless … put into an external tool". This recommendation is the flow's proposal, not his.

### The datom file form

One real settings file, `/git/github.com/LiGoldragon/aggregator/examples/configuration.datom`, one line, verbatim:
```
{ /run/aggregator/aggregator.sock 432 /run/aggregator/aggregator-meta.sock 384 /var/lib/aggregator/aggregator.sema [ { example-repository /srv/aggregator/repositories/example } ] [ Claude.{ /srv/aggregator/transcripts/claude } Codex.{ /srv/aggregator/transcripts/codex } ] MetadataOnly { 32 4096 } { { DaemonLocalStorePath OpaqueStaleCapable FragileReferenceAscending } { 64 4096 65536 1024 131072 32768 8388608 262144 1024 } [] } }
```
It is read against `AggregatorConfiguration` in `meta-signal-aggregator` 0.7.0 (`ethos/signal.ethos` lines 66 to 68, `5baab64`); the test `example_configuration_carries_the_written_sockets_and_sources` actualizes it and passes (2026-10-04):
```
AggregatorConfiguration.{ OrdinarySocketPath OrdinarySocketMode MetaSocketPath MetaSocketMode
                          StorePath ActiveRepositories TranscriptSources DefaultProjection
                          DefaultLimitPolicy OutputInterfaceConfiguration }
```
A datom file is one datom, no root, written against one type; its positions follow the type's fields in order (`432` is the ordinary socket's mode, 0o660). Under way b the file holds the value of one `Wanted` variant; under c, the value of one position in the inline datom.

### Proposals

1. **[vision] `/home/li/primary/Vision/nexus.md`, new section "A value from a file", after "Signal only".** Assumes Ruling 1 (b).
   Grounded: 2026-10-04, bad807 (typed, book comment), "ostensibly the CLI that it's meant to work with".
   The `ReadFile` and `Supply` names are the flow's proposal, not his.
   Now: no such section.
   Proposed:
   > ## A value from a file
   >
   > A Nexus that needs a value kept in a datom file asks its caller for it. It answers with `ReadFile`, whose variant names the type it wants and carries the file's path; the CLI, built with the same contract, reads the file, actualizes the value and sends it back as `Supply`. The Nexus holds the path and never opens the file. A Nexus declares this only when it needs it. A caller may always read a file itself and send its value inline.

2. **[implementation] `/git/github.com/LiGoldragon/Curriculum/skills/datom.md`, line 95, its last clause.** Built on a yes to proposal 1.
   Grounded: 2026-10-04, bad807 (typed, book comment), "pull in a value from a file".
   Now:
   ```
   A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, never as a datom file.
   ```
   Proposed:
   ```
   A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, and a CLI reads a datom file only when its Nexus answers with `ReadFile`, sending the value back as signal.
   ```

3. **[implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`, line 14, a sentence after "never by a claim."** Built on a yes to proposal 1.
   Grounded: 2026-10-04, bad807 (typed, book comment), "pull in a value from a file".
   Now: no such sentence.
   Proposed:
   ```
   A Nexus that wants a value from a datom file answers `ReadFile` with the wanted type's variant and the path; the CLI reads and actualizes the file and opens a second exchange with `Supply`; the Nexus holds the path and never the text.
   ```

4. **[implementation] `/git/github.com/LiGoldragon/aggregator/src/daemon.rs`, lines 35 to 38.** Independent of proposals 1 to 3; follows "A Nexus starts with no arguments" (`Vision/nexus.md`, "Configuration").
   Grounded: 2026-09-15, 05c604, "the Nexus only gets signal".
   Now:
   ```rust
       pub fn run(&self) -> Result<()> {
           let configuration_path = self.arguments.configuration_path()?;
           let configuration_store = ConfigurationStore::at_path(configuration_path);
           let configuration = configuration_store.read_configuration()?;
   ```
   Proposed: the daemon starts from its built-in defaults with no `--configuration`, and `meta-aggregator` sends the file's value as `Configure.{ … }` (way c), so the daemon is built without datom-codec.

## Rulings

1. Which way a Nexus gets a value from a datom file.
   (a) It runs a reader subprocess named by a variant: typed, book comment, 2026-10-04: "a variant … that would tell it what type of CLI you would have to use".
   (b) It asks with `ReadFile`, the connected CLI supplies: typed, book comment, 2026-10-04: "ostensibly the CLI that it's meant to work with"; the flow's proposal.
   (c) The caller reads and sends it, the Nexus unchanged: typed, book comment, 2026-10-04: "unless all of that is, again, put into an external tool"; 2026-09-29, 183ae0 (a notion), "next to it would be the compiled signal file".
2. Whether the no-text rule admits a path string in a Nexus.
   (a) Yes, a path held and passed but never parsed: `Vision/nexus.md` "Signal only", "the string fields it still carries are records on the way to a fully typed form".
   (b) No, a path is first given a type of its own: 2026-09-15, 692df8, "in a way, it's a string when you print it, but it's not a string per se".
3. Whether every Nexus can ask for a file.
   (a) Only those that declare it in their Signal: typed, book comment, 2026-10-04: "Maybe not all the Nexuses need this".
   (b) Every Nexus, through the shared nexus library: `Vision/nexus.md` "First configuration", "whatever else comes up as standard nexus configuration data".
<!-- to-the-living:end -->
