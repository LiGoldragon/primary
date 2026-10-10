Presentation.{ «The deployment, in four parts» }

Respond by comment. Nothing here has buttons.

## 1. Why it stalled

The deployment is done: the new Flow, Message and Orchestrate run as the regular versions, with generation 1039 kept as the rollback.

```mermaid
flowchart TD
  A[Mind source review and acceptance] --> B[Field Sol publishes Home source]
  B --> C[Consumer and build definition]
  C --> D[Lojix deployment]
  D --> E[Home profile advances]
  E --> F{Activate: does the old file match the guard?}
  F -->|No: diagnostic kept| G[ActivationFailed: partial profile]
  F -->|Yes| H[Switch services]
  G --> I[Mind accepts narrow predecessor correction]
```

Home deployment puts the new Flow software on the living's machine. The final switch was refused twice. Home Manager puts the messenger commands into your home as links into the Nix store. A module in CriomOS-home added its own check on those links, accepting them only if they pointed into one particular older set of files; since September 30 they pointed into a newer set, so the check failed at activation and refused every new generation and every rollback. The fix removed that check and let Home Manager's own link check, which compares against the previous generation, guard the links.

## 2. How the ordered fix works

```mermaid
flowchart TD
  A[Verify remote consumer state] --> B{Is the corrected consumer published?}
  B -->|No| C[Publish corrected consumer]
  B -->|Yes| D[One ordered retry]
  C --> D
  R[Previous version kept for rollback] --- D
  D --> E{Does activation succeed?}
  E -->|No| F[Record failure; rollback path stays]
  E -->|Yes| G[Record switched profile]
  G --> H[Fresh launch and first-turn witness]
```

The fix is one ordered retry by Field Sol. It publishes the corrected piece only if it is missing, then retries once with the old version kept for going back. A fresh flow then proves it.

## 3. Where Home now stands

```mermaid
flowchart TD
  H[Home deployment: current outcome] --> F[Stable Flow 0.23.0]
  H --> N[Next Flow 0.23.0]
  H --> M[Stable and Next Message 0.19]
  H --> R[Rollback executable]
  O[Orchestrate process 0.37; sockets and lock pass] --> C[Current process witness]
  F --> B[Fresh Start remains separate]
  N --> B
  M --> B
  B --> U[No new Start or first-turn witness claimed]
```

The retry worked. Flow 0.23.0 and Message 0.19 now run in both stable and Next, and the old override is gone. No fresh flow has yet answered a first turn.

## 4. What a working flow needs

```mermaid
flowchart TD
  A[Flow Start: Voice and requested work] --> B[Deterministic allocator and registry]
  B --> C[Native harness session]
  C --> D[Bind native ID, FlowId, Voice, Capsule]
  D --> E[Compose main prompt modules]
  E --> F[One actual first turn]
  F --> G[Hooks and lifecycle evidence]
  G --> H[Current Voice route and recovery]
  H --> I[Fresh-launch receipt]
```

```mermaid
flowchart TD
  A[Hearing flow classifies entry] --> B[Managed recorder: quote and provenance]
  B --> C[Durable event: record, typed topic, source]
  C --> D{Topic-owner flow bound?}
  D -->|No| E[Pending for replay]
  D -->|Yes| F[At-least-once delivery]
  F --> G[Dedupe receipt]
  E --> H[Restart replays durable pending event]
```

A working flow needs a readable three-word address, a real session, a prompt and a true first turn. Plain code does the allocating and the lookup. The draft word kind is below.

```ethos
Library
[]
[ DictionaryVersion.{
    DictionaryName.String
    Revision.Integer }
  WordParseError.[
    Empty
    NonCanonicalText
    UnknownWord.String
    WrongWordCount.{
      Integer
      Integer }
    InvalidIndex.Integer
    DictionaryMismatch.{
      DictionaryVersion
      DictionaryVersion }
    NonCanonicalPadding ] ]
[ Wordable.{
    []
    [ Dictionary
      Words ]
    [ WIDTH_BITS.Integer ]
    [ as_words.[ Words ]
      parse_words:{
        [ Words ]
        [ Result<Self
                 WordParseError> ] } ] } ]
[]
```

What is left: a flow launched by Flow that answers its first turn; it is in progress.

1. Noted. 2. Comment.
