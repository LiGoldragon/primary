<!-- to-the-living:start -->
Presentation.{ «A Nexus reads a value from a datom file» }

## His words
> "let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this … a variant `me` [sic] that would tell it what type of CLI you would have to use … There's a string involved no matter what unless all of that is, again, put into an external tool."

His book comment on «The Nexus».

## Today
A datom value reaches a Nexus only as an argument string.
```
orchestrate "<one inline datom>"                        # env::args(), no flags
  → Potential::<Query>::from(source).actualize(&mut budget)   # datom-codec 0.31.0
  → Dispatch::Open(Query) → one frame of signal → orchestrate-nexus
```
Orchestrate 0.36.1 refuses anything else: "accepts exactly one inline Datom query and no flags".
`orchestrate-nexus/Cargo.toml`: "No `datom-codec` and no `protos`".

<figure><svg viewBox="0 0 700 270" width="700" role="img" aria-label="Today: three present paths for a datom value" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="270" rx="8" fill="#fbfaf6"/>
<g font-weight="600" font-size="14"><text x="20" y="24">Orchestrate 0.36.1: inline only</text><text x="20" y="109">aggregator 0.7.0: the daemon reads the file</text><text x="20" y="194">Lojix 6.0.0: a written archive</text></g>
<g stroke-width="1.5"><rect x="20" y="34" width="160" height="48" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="270" y="34" width="160" height="48" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="520" y="34" width="160" height="48" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="20" y="119" width="160" height="48" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="520" y="119" width="160" height="48" rx="6" fill="#ffe3df" stroke="#b3261e"/><rect x="20" y="204" width="160" height="48" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="270" y="204" width="160" height="48" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="520" y="204" width="160" height="48" rx="6" fill="#dcebff" stroke="#2a5db0"/></g>
<g text-anchor="middle"><text x="100" y="55">shell</text><text x="100" y="72" font-size="11">one inline datom</text><text x="350" y="55">orchestrate CLI</text><text x="350" y="72" font-size="11">actualize → Query</text><text x="600" y="55">orchestrate-nexus</text><text x="600" y="72" font-size="11">no datom-codec</text><text x="100" y="148">configuration.datom</text><text x="600" y="140">aggregator daemon</text><text x="600" y="157" font-size="11">parses datom text itself</text><text x="100" y="225">shell</text><text x="100" y="242" font-size="11">one inline datom</text><text x="350" y="225" font-size="12">lojix-write-configuration</text><text x="350" y="242" font-size="11">datom → rkyv</text><text x="600" y="225">Lojix Nexus</text><text x="600" y="242" font-size="11">loads the archive</text></g>
<g stroke="#3a4152" stroke-width="1.6" marker-end="url(#m1)"><line x1="180" y1="58" x2="268" y2="58"/><line x1="430" y1="58" x2="518" y2="58"/><line x1="180" y1="143" x2="518" y2="143"/><line x1="180" y1="228" x2="268" y2="228"/><line x1="430" y1="228" x2="518" y2="228"/></g>
<g font-size="11" text-anchor="middle" fill="#4a5263"><text x="225" y="50">argument</text><text x="475" y="50">signal frame</text><text x="350" y="135">--configuration: read_to_string, DatomText::read</text><text x="225" y="220">argument</text><text x="475" y="220">archive file</text><text x="475" y="244">path in env</text></g>
</svg><figcaption>Today a datom reaches a Nexus as one argument; only the aggregator daemon parses a file itself.</figcaption></figure>

### The two settings files outside that path
```rust
// aggregator 0.7.0, src/daemon.rs lines 35 to 38 (datom-codec 0.27.0)
std::fs::read_to_string(configuration_path)  →  DatomText::read
// its CLI reads the same file for the socket paths (src/client.rs line 37)
```
Lojix 6.0.0: `lojix-write-configuration` turns one inline datom into an rkyv archive.
The Nexus loads it from the path in `LOJIX_CONFIGURATION`.

### What the rule says now
```text
skills/datom.md line 95: "datom passes inline at a CLI boundary, never as a datom file"
```
The corpus names this the tension "Settings file" (`ethos-nexus-corpus.md` line 9150).
The ethos below is checked and generated with ethos-zero 16.0.0; nothing ran against a live socket.

## Three ways from the file to the Nexus

<figure><svg viewBox="0 0 700 330" width="700" role="img" aria-label="Three ways the value travels from the file to the Nexus" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="330" rx="8" fill="#fbfaf6"/>
<g font-weight="600" font-size="14"><text x="20" y="24">a) the Nexus runs a reader</text><text x="20" y="134">b) the Nexus asks, the CLI answers</text><text x="20" y="244">c) the caller reads, the Nexus unchanged</text></g>
<g stroke-width="1.5"><rect x="20" y="38" width="110" height="50" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="20" y="148" width="110" height="50" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="20" y="258" width="110" height="50" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="180" y="38" width="160" height="50" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="180" y="148" width="160" height="50" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="180" y="258" width="160" height="50" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="480" y="38" width="120" height="50" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="480" y="148" width="120" height="50" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="480" y="258" width="120" height="50" rx="6" fill="#dcebff" stroke="#2a5db0"/></g>
<g text-anchor="middle"><text x="75" y="68">file.datom</text><text x="75" y="178">file.datom</text><text x="75" y="288">file.datom</text><text x="260" y="60">reader subprocess</text><text x="260" y="77" font-size="11">spawned by the Nexus</text><text x="260" y="170">CLI, connected</text><text x="260" y="187" font-size="11">reads when asked</text><text x="260" y="280">shell and CLI</text><text x="260" y="297" font-size="11">$(cat file.datom)</text><text x="540" y="68">Nexus</text><text x="540" y="178">Nexus</text><text x="540" y="288">Nexus</text></g>
<g stroke="#3a4152" stroke-width="1.6" marker-end="url(#m2)"><line x1="130" y1="63" x2="178" y2="63"/><line x1="478" y1="50" x2="342" y2="50"/><line x1="340" y1="76" x2="478" y2="76"/><line x1="130" y1="173" x2="178" y2="173"/><line x1="478" y1="160" x2="342" y2="160"/><line x1="340" y1="186" x2="478" y2="186"/><line x1="130" y1="283" x2="178" y2="283"/><line x1="340" y1="283" x2="478" y2="283"/></g>
<g font-size="11" text-anchor="middle" fill="#4a5263"><text x="410" y="45">spawn lojix-read + path</text><text x="410" y="90">rkyv on stdout</text><text x="410" y="155">ReadFile.Roster.path</text><text x="410" y="200">Supply.{ path Roster }</text><text x="410" y="278">Configure.{ … }</text></g>
<g font-size="11" font-weight="600" fill="#b3261e"><text x="608" y="60">program name</text><text x="608" y="76">and path</text><text x="608" y="178">path only</text><text x="608" y="288">no string</text></g>
</svg><figcaption>Right column: the string each way leaves inside the Nexus.</figcaption></figure>

## a) The Nexus runs a reader as a subprocess
No ethos added to the Signal. The reader is a Memory value; his variant names the CLI.
```
Reader.[ Orchestrate Lojix ]               ; which reader program the Nexus spawns
```
Rust, Nexus side, compiled in the scratch crate without the `datom` feature:
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

<figure><svg viewBox="0 0 700 180" width="700" role="img" aria-label="Way a: the Nexus spawns a reader and decodes its stdout" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="180" rx="8" fill="#fbfaf6"/>
<g stroke-width="1.5"><rect x="10" y="20" width="150" height="52" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="185" y="20" width="150" height="52" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="360" y="20" width="150" height="52" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="535" y="20" width="150" height="52" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="185" y="115" width="150" height="40" rx="6" fill="#ffe3df" stroke="#b3261e"/><rect x="360" y="115" width="150" height="40" rx="6" fill="#ffe3df" stroke="#b3261e"/><rect x="535" y="115" width="150" height="40" rx="6" fill="#ffe3df" stroke="#b3261e"/></g>
<g text-anchor="middle"><text x="85" y="42">Reader.Lojix</text><text x="85" y="60" font-size="11">program() → "lojix-read"</text><text x="260" y="42">Command::new</text><text x="260" y="60" font-size="11">.arg(path).output()</text><text x="435" y="42">lojix-read</text><text x="435" y="60" font-size="11">found on PATH</text><text x="610" y="42">rkyv::from_bytes</text><text x="610" y="60" font-size="11">→ Roster</text><text x="260" y="140">ReadFailure::Spawn</text><text x="435" y="140">ReadFailure::Exit</text><text x="610" y="140">ReadFailure::Archive</text></g>
<g stroke="#3a4152" stroke-width="1.6" marker-end="url(#m3)"><line x1="160" y1="46" x2="183" y2="46"/><line x1="335" y1="46" x2="358" y2="46"/><line x1="510" y1="46" x2="533" y2="46"/><line x1="260" y1="72" x2="260" y2="113"/><line x1="435" y1="72" x2="435" y2="113"/><line x1="610" y1="72" x2="610" y2="113"/></g>
<g font-size="11" fill="#4a5263"><text x="266" y="98">cannot start</text><text x="441" y="98">non-zero exit</text><text x="616" y="98">bad archive</text></g>
</svg><figcaption>Way a: the Nexus starts a program by name and trusts its stdout.</figcaption></figure>

The names `Orchestrate`, `Lojix`, `orchestrate-read` and `lojix-read` are the flow's illustration.
No such reader binary exists; no CLI of ours prints rkyv today.

The no-text rule keeps its letter: the Nexus parses no datom.
It loses its spirit: the Nexus starts processes by name and trusts their stdout.

- For: the Nexus pulls on its own, at any time, with no caller connected.
- Against: a command string and a process boundary inside the Nexus; a reader binary per contract.
- Against: `PATH` on the host decides what runs, not the contracts the Nexus is compiled with.

## b) The Nexus asks; the CLI reads, decodes and sends the typed value
Ethos added to the Signal. `Check` with ethos-zero 16.0.0 answers `Checked`.
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
`Roll`, `roll-meta`, `Roster` and `Member` are the flow's invented example names.

### Two exchanges on one connection

<figure><svg viewBox="0 0 700 355" width="700" role="img" aria-label="ReadFile and Supply over two exchanges" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="355" rx="8" fill="#fbfaf6"/>
<rect x="275" y="72" width="400" height="86" fill="#eaf1ff"/><rect x="275" y="248" width="400" height="92" fill="#eaf1ff"/>
<g font-size="11" font-weight="600" fill="#2a5db0"><text x="282" y="87">exchange 1, opened by the CLI</text><text x="282" y="263">exchange 2, opened by the CLI</text></g>
<g stroke-width="1.5"><rect x="35" y="18" width="130" height="40" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="285" y="18" width="130" height="40" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="535" y="18" width="130" height="40" rx="6" fill="#dcebff" stroke="#2a5db0"/></g>
<g text-anchor="middle"><text x="100" y="43">roster.datom</text><text x="350" y="43">roll-meta (CLI)</text><text x="600" y="43">Roll (Nexus)</text></g>
<g stroke="#8a91a0" stroke-dasharray="4 4"><line x1="100" y1="58" x2="100" y2="345"/><line x1="350" y1="58" x2="350" y2="345"/><line x1="600" y1="58" x2="600" y2="345"/></g>
<g stroke="#3a4152" stroke-width="1.6" marker-end="url(#m4)"><line x1="350" y1="108" x2="598" y2="108"/><line x1="600" y1="145" x2="352" y2="145"/><line x1="350" y1="180" x2="102" y2="180"/><line x1="100" y1="205" x2="348" y2="205"/><line x1="350" y1="290" x2="598" y2="290"/><line x1="600" y1="328" x2="352" y2="328"/></g>
<rect x="300" y="215" width="100" height="26" rx="4" fill="#eef1ea" stroke="#5f7a52"/><text x="350" y="232" text-anchor="middle" font-size="11">actualize Roster</text>
<g font-size="11" text-anchor="middle" fill="#1d2330"><text x="475" y="102">Configure.{ /run/roll/roll.sock [] }</text><text x="475" y="139">ReadFile.Roster.path</text><text x="225" y="174">read_to_string(path)</text><text x="225" y="199">datom text</text><text x="475" y="284">Supply.{ path Roster.[ Ada Grace … ] }</text><text x="475" y="322">Configured</text></g>
</svg><figcaption>The CLI answers ReadFile by opening exchange 2 with Supply; the Nexus never touches the file.</figcaption></figure>

On `signal` 8.0.0 the querying side only opens exchanges:
```
Dispatch::{ Greet Open Abandon }
```
So `Supply` rides a second exchange on the same connection; the frame and the greeting stay as they are.

### The Nexus's answer
Compiled in the scratch crate without the `datom` feature:
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

<figure><svg viewBox="0 0 700 300" width="700" role="img" aria-label="The Nexus's answer: four outcomes" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="300" rx="8" fill="#fbfaf6"/>
<g stroke-width="1.5"><rect x="20" y="125" width="110" height="50" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="190" y="40" width="150" height="50" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="190" y="210" width="150" height="50" rx="6" fill="#dcebff" stroke="#2a5db0"/><rect x="470" y="10" width="210" height="44" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="470" y="70" width="210" height="44" rx="6" fill="#e3f3e0" stroke="#3f7a35"/><rect x="470" y="180" width="210" height="44" rx="6" fill="#e3f3e0" stroke="#3f7a35"/><rect x="470" y="240" width="210" height="44" rx="6" fill="#ffe3df" stroke="#b3261e"/></g>
<g text-anchor="middle"><text x="75" y="155">Query</text><text x="265" y="70">Configure</text><text x="265" y="240">Supply</text><text x="575" y="29">ReadFile.Roster.path</text><text x="575" y="46" font-size="11">ask the caller</text><text x="575" y="89">Configured</text><text x="575" y="106" font-size="11">keep the roster</text><text x="575" y="199">Configured</text><text x="575" y="216" font-size="11">keep the roster</text><text x="575" y="259">Refused.NotWanted.path</text><text x="575" y="276" font-size="11">a supply nobody asked for</text></g>
<g stroke="#3a4152" stroke-width="1.6" marker-end="url(#m5)"><line x1="130" y1="140" x2="188" y2="70"/><line x1="130" y1="160" x2="188" y2="230"/><line x1="340" y1="58" x2="468" y2="34"/><line x1="340" y1="74" x2="468" y2="92"/><line x1="340" y1="228" x2="468" y2="204"/><line x1="340" y1="244" x2="468" y2="262"/></g>
<g font-size="11" text-anchor="middle" fill="#4a5263"><text x="404" y="38">roster empty</text><text x="404" y="98">roster given</text><text x="400" y="208">asked path, Roster</text><text x="404" y="268">anything else</text></g>
</svg><figcaption>The Nexus decides which file and which type; it only holds the path.</figcaption></figure>

### The CLI's supply
Compiled in the scratch crate with datom-codec 0.32.2:
```rust
impl RosterFile<'_> {
    fn read(&self) -> Reading {
        let Ok(text) = std::fs::read_to_string(self.0) else { return Reading::Missing };
        let mut budget = Budget { remaining: 10_000, reader: ReaderBudget { remaining: 10_000 }, depth: 0, maximum_depth: 256 };
        Potential::<Roster>::from(text).actualize(&mut budget).map(Reading::Roster).unwrap_or(Reading::Unreadable)
    }
}
```

<figure><svg viewBox="0 0 700 190" width="700" role="img" aria-label="The CLI's read: three outcomes" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="190" rx="8" fill="#fbfaf6"/>
<g stroke-width="1.5"><rect x="20" y="30" width="110" height="50" rx="6" fill="#fff4d6" stroke="#a07800"/><rect x="180" y="30" width="150" height="50" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="380" y="30" width="150" height="50" rx="6" fill="#eef1ea" stroke="#5f7a52"/><rect x="570" y="30" width="120" height="50" rx="6" fill="#e3f3e0" stroke="#3f7a35"/><rect x="195" y="130" width="120" height="40" rx="6" fill="#ffe3df" stroke="#b3261e"/><rect x="395" y="130" width="120" height="40" rx="6" fill="#ffe3df" stroke="#b3261e"/></g>
<g text-anchor="middle"><text x="75" y="60">path</text><text x="255" y="60">read_to_string</text><text x="455" y="60">actualize Roster</text><text x="630" y="60">Reading::Roster</text><text x="255" y="155">Missing</text><text x="455" y="155">Unreadable</text></g>
<g stroke="#3a4152" stroke-width="1.6" marker-end="url(#m6)"><line x1="130" y1="55" x2="178" y2="55"/><line x1="330" y1="55" x2="378" y2="55"/><line x1="530" y1="55" x2="568" y2="55"/><line x1="255" y1="80" x2="255" y2="128"/><line x1="455" y1="80" x2="455" y2="128"/></g>
<g font-size="11" fill="#4a5263"><text x="261" y="108">no file</text><text x="461" y="108">[ Ada { }</text><text x="690" y="100" text-anchor="end">[ Ada Grace «Barbara Liskov» ]</text></g>
</svg><figcaption>Run in the scratch crate on a good, a malformed and a missing file.</figcaption></figure>

The good file answers:
```text
Supply(Supplied { file_path: "…/roster.datom", reading: Roster(["Ada", "Grace", "Barbara Liskov"]) })
```
### What b costs and gives
His variant naming the CLI becomes the `Wanted` variant naming the type.
The CLI built with that contract is the one already connected, so no program name is stored.

- For: no datom, no file access and no command string in the Nexus; the Nexus still decides which file and which type.
- For: works on `signal` 8.0.0 unchanged; the CLI side is about 20 lines per contract, generated from the `Wanted` variants.
- Against: the Nexus can ask only while a CLI is connected; a pull with no caller present needs a.

## c) The caller reads the file; the Nexus is unchanged
No ethos added. The shell composes the one inline datom; the CLI stays unchanged too.
```sh
roll-meta "Configure.{ /run/roll/roll.sock $(cat roster.datom) }"
# actualized in the scratch crate as
# Configure(Configuration { socket_path: "/run/roll/roll.sock", roster: ["Ada", "Grace", "Barbara Liskov"] })
```
No string in the Nexus; the cost to the no-text rule is nil.

His earlier words (a notion) are this way with the reader writing an archive:

> "next to it would be the compiled signal file so that then the Nexus could load it because it's already signal"

That is what `lojix-write-configuration` does today; the Nexus then holds the archive's path.

- For: free today, for every Nexus; nothing to design or build.
- Against: the Nexus cannot pull; the caller must know which file holds which position.
- Against: the file must hold exactly one position's value; it cannot be spliced in deeper than the shell can quote.

## Where the string lives

<figure><svg viewBox="0 0 700 215" width="700" role="img" aria-label="Where the string lives in each way" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<rect width="700" height="215" rx="8" fill="#fbfaf6"/>
<g font-weight="600" font-size="14" text-anchor="middle"><text x="120" y="26">a) reader</text><text x="350" y="26">b) ReadFile / Supply</text><text x="580" y="26">c) caller reads</text></g>
<g stroke-width="1.5" fill="#dcebff" stroke="#2a5db0"><rect x="20" y="38" width="200" height="110" rx="8"/><rect x="250" y="38" width="200" height="110" rx="8"/><rect x="480" y="38" width="200" height="110" rx="8"/></g>
<g font-size="11" fill="#2a5db0"><text x="30" y="54">inside the Nexus</text><text x="260" y="54">inside the Nexus</text><text x="490" y="54">inside the Nexus</text></g>
<g fill="#ffe3df" stroke="#b3261e"><rect x="50" y="66" width="140" height="28" rx="14"/><rect x="50" y="104" width="140" height="28" rx="14"/><rect x="280" y="66" width="140" height="28" rx="14"/></g>
<g text-anchor="middle"><text x="120" y="85" fill="#b3261e">"lojix-read"</text><text x="120" y="123" fill="#b3261e">path</text><text x="350" y="85" fill="#b3261e">FilePath</text><text x="350" y="123" font-size="11">held, never opened</text><text x="580" y="98" fill="#4a5263">no string</text></g>
<g font-size="11" text-anchor="middle" fill="#4a5263"><text x="120" y="175">datom parsed by:</text><text x="350" y="175">datom parsed by:</text><text x="580" y="175">datom parsed by:</text></g>
<g text-anchor="middle"><text x="120" y="195">a reader binary per contract</text><text x="350" y="195">the connected CLI</text><text x="580" y="195">the CLI, from the shell</text></g>
</svg><figcaption>Only a holds a program name; b holds one typed path; c holds nothing.</figcaption></figure>

## What the flow proposes
Way b, for the Nexuses that declare it; c stays as what every Nexus already has.
It is the one way the Nexus pulls, as he asks, and still sees only signal.

The variant he wanted names a type, never a program; the one string is a path, held and passed, never read.
Way a puts a command string and a process boundary into the Nexus: the string he wanted out "unless … put into an external tool".

This recommendation is the flow's proposal, not his.

## The datom file form
One real settings file, `/git/github.com/LiGoldragon/aggregator/examples/configuration.datom`, one line, verbatim:
```text
{ /run/aggregator/aggregator.sock 432 /run/aggregator/aggregator-meta.sock 384 /var/lib/aggregator/aggregator.sema [ { example-repository /srv/aggregator/repositories/example } ] [ Claude.{ /srv/aggregator/transcripts/claude } Codex.{ /srv/aggregator/transcripts/codex } ] MetadataOnly { 32 4096 } { { DaemonLocalStorePath OpaqueStaleCapable FragileReferenceAscending } { 64 4096 65536 1024 131072 32768 8388608 262144 1024 } [] } }
```
It is read against this type, `meta-signal-aggregator` 0.7.0, `ethos/signal.ethos` lines 66 to 68:
```
AggregatorConfiguration.{ OrdinarySocketPath OrdinarySocketMode MetaSocketPath MetaSocketMode
                          StorePath ActiveRepositories TranscriptSources DefaultProjection
                          DefaultLimitPolicy OutputInterfaceConfiguration }
```

<figure><svg viewBox="0 0 700 290" width="700" role="img" aria-label="Each position of the file fills one field, in order" font-family="system-ui,sans-serif" font-size="13" fill="#1d2330">
<defs><marker id="m7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3a4152"/></marker></defs><rect width="700" height="290" rx="8" fill="#fbfaf6"/>
<g font-size="11" font-weight="600" fill="#4a5263"><text x="20" y="24">FILE POSITION</text><text x="465" y="24">FIELD</text></g>
<g font-family="ui-monospace,Menlo,monospace" font-size="12" fill="#7a5a00"><text x="20" y="50">/run/aggregator/aggregator.sock</text><text x="20" y="74">432</text><text x="20" y="98">/run/aggregator/aggregator-meta.sock</text><text x="20" y="122">384</text><text x="20" y="146">/var/lib/aggregator/aggregator.sema</text><text x="20" y="170">[ { example-repository … } ]</text><text x="20" y="194">[ Claude.{ … } Codex.{ … } ]</text><text x="20" y="218">MetadataOnly</text><text x="20" y="242">{ 32 4096 }</text><text x="20" y="266">{ { DaemonLocalStorePath … } … [] }</text></g>
<g stroke="#8a91a0" stroke-width="1.2" marker-end="url(#m7)"><line x1="400" y1="46" x2="458" y2="46"/><line x1="400" y1="70" x2="458" y2="70"/><line x1="400" y1="94" x2="458" y2="94"/><line x1="400" y1="118" x2="458" y2="118"/><line x1="400" y1="142" x2="458" y2="142"/><line x1="400" y1="166" x2="458" y2="166"/><line x1="400" y1="190" x2="458" y2="190"/><line x1="400" y1="214" x2="458" y2="214"/><line x1="400" y1="238" x2="458" y2="238"/><line x1="400" y1="262" x2="458" y2="262"/></g>
<g fill="#2a5db0"><text x="465" y="50">OrdinarySocketPath</text><text x="465" y="74">OrdinarySocketMode (0o660)</text><text x="465" y="98">MetaSocketPath</text><text x="465" y="122">MetaSocketMode</text><text x="465" y="146">StorePath</text><text x="465" y="170">ActiveRepositories</text><text x="465" y="194">TranscriptSources</text><text x="465" y="218">DefaultProjection</text><text x="465" y="242">DefaultLimitPolicy</text><text x="465" y="266">OutputInterfaceConfiguration</text></g>
</svg><figcaption>A datom file is one datom, no root, against one type: positions follow its fields in order.</figcaption></figure>

The test `example_configuration_carries_the_written_sockets_and_sources` actualizes it and passes.
Under b the file holds the value of one `Wanted` variant; under c, the value of one position in the inline datom.

## Proposals
### 1. [vision] `/home/li/primary/Vision/nexus.md`
New section "A value from a file", after "Signal only". Assumes Ruling 1 (b).
Grounded: his book comment, "ostensibly the CLI that it's meant to work with".
The `ReadFile` and `Supply` names are the flow's proposal, not his.

Now: no such section. Proposed:
```text
## A value from a file

A Nexus that needs a value kept in a datom file asks its caller for it. It answers with `ReadFile`, whose variant names the type it wants and carries the file's path; the CLI, built with the same contract, reads the file, actualizes the value and sends it back as `Supply`. The Nexus holds the path and never opens the file. A Nexus declares this only when it needs it. A caller may always read a file itself and send its value inline.
```
### 2. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/datom.md`
Line 95, its last clause. Built on a yes to proposal 1.
Grounded: his book comment, "pull in a value from a file".

Now:
```text
A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, never as a datom file.
```
Proposed:
```text
A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, and a CLI reads a datom file only when its Nexus answers with `ReadFile`, sending the value back as signal.
```
### 3. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`
Line 14, a sentence after "never by a claim." Built on a yes to proposal 1.
Grounded: his book comment, "pull in a value from a file".

Now: no such sentence. Proposed:
```text
A Nexus that wants a value from a datom file answers `ReadFile` with the wanted type's variant and the path; the CLI reads and actualizes the file and opens a second exchange with `Supply`; the Nexus holds the path and never the text.
```
### 4. [implementation] `/git/github.com/LiGoldragon/aggregator/src/daemon.rs`
Lines 35 to 38. Independent of proposals 1 to 3.
Follows "A Nexus starts with no arguments" (`Vision/nexus.md`, "Configuration").
Grounded: "the Nexus only gets signal".

Now:
```rust
    pub fn run(&self) -> Result<()> {
        let configuration_path = self.arguments.configuration_path()?;
        let configuration_store = ConfigurationStore::at_path(configuration_path);
        let configuration = configuration_store.read_configuration()?;
```
Proposed: the daemon starts from its built-in defaults with no `--configuration`.
`meta-aggregator` sends the file's value as `Configure.{ … }` (way c), so the daemon is built without datom-codec.

## Rulings
### 1. Which way a Nexus gets a value from a datom file
- (a) It runs a reader subprocess named by a variant. His book comment: "a variant … that would tell it what type of CLI you would have to use".
- (b) It asks with `ReadFile`, the connected CLI supplies. His book comment: "ostensibly the CLI that it's meant to work with"; the flow's proposal.
- (c) The caller reads and sends it, the Nexus unchanged. His book comment: "unless all of that is, again, put into an external tool"; a notion: "next to it would be the compiled signal file".

### 2. Whether the no-text rule admits a path string in a Nexus
- (a) Yes, a path held and passed but never parsed. `Vision/nexus.md` "Signal only": "the string fields it still carries are records on the way to a fully typed form".
- (b) No, a path is first given a type of its own. A record: "in a way, it's a string when you print it, but it's not a string per se".

### 3. Whether every Nexus can ask for a file
- (a) Only those that declare it in their Signal. His book comment: "Maybe not all the Nexuses need this".
- (b) Every Nexus, through the shared nexus library. `Vision/nexus.md` "First configuration": "whatever else comes up as standard nexus configuration data".
<!-- to-the-living:end -->

