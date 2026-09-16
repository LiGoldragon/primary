# The Four Layers

*An idea book. One idea, four boxes. The charts are the flow of the idea; the pictures are made from the charts.*

---

## 1 · One mind, four depths

A psyche extends itself through a cluster of flows. The flows are not a hierarchy of bosses; they are one mind at four depths. The top is slow and considers; the bottom is quick and instinctive. Every depth is a pair: a Claude half and a Codex half, the same message reaching both.

```mermaid
flowchart TB
  L["the living"]
  P["1 · primary\ndesign · thinking · prototypes"]
  S["2 · secondary\ndeployment · production tests"]
  T["3 · tertiary\nquick, instinctive, lower cost"]
  Q["4 · quaternary\nquick, instinctive, lower cost"]
  L --- P --- S --- T --- Q
```

---

## 2 · Requests climb; each layer is a filter

A lower layer never bothers the one above it directly. What it wants goes to the layer just above, which reads it as an auditor: *did you understand the instruction?* If not, it says so and sends the layer back to work, to present another prospect, another proof of concept. Only what passes that audit climbs further. Any layer functions this way, all the way to the living.

```mermaid
flowchart LR
  Q4["quaternary\nwants to do X"] -->|request| T3{"tertiary\naudits"}
  T3 -->|"not understood → try again"| Q4
  T3 -->|passes| S2{"secondary\naudits"}
  S2 -->|"not understood → try again"| T3
  S2 -->|passes| P1{"primary\naudits"}
  P1 -->|"not understood → try again"| S2
  P1 -->|"only what survived"| L["the living"]
```

---

## 3 · Who thinks, who does

Two Opus models, named by what they are for. The **older Opus** is the wiser one: consideration, qualitative audits, comparing a proof against the vision, the thinking behind a Fable flow. The **newer Opus** is faster and blinder, good at getting things done. **Fable**, newest, sits with the old Opus wherever a psyche is being read: design, thinking, the conversation itself. On the Codex side the lower layers run the latest **Sol**; the higher layer runs **Astra**.

```mermaid
flowchart TB
  subgraph think["thinking · design · psyche interaction"]
    F["Fable"]
    O["older Opus\n(the wiser one)"]
  end
  subgraph do["getting things done"]
    N["newer Opus"]
    So["Sol"]
  end
  subgraph codexHigh["Codex, higher layer"]
    A["Astra"]
  end
  think -->|"decides, audits"| do
  A --- F
```

---

## 4 · The season of each layer

Read the four as seasons of one year. Spring is the living speaking. Summer is the primary, where ideas are grown into prototypes. Autumn is the secondary, where what ripened is harvested into production and tested there. Winter is the quick lower layers: little light, little cost, instinct doing the small work so the year can turn again. Every winter request climbs back through autumn and summer before it reaches spring.

```mermaid
flowchart LR
  Sp["spring\nthe living speaks"] --> Su["summer\nprimary grows the idea"]
  Su --> Au["autumn\nsecondary harvests to production"]
  Au --> Wi["winter\nlower layers do the small work"]
  Wi -->|"requests climb back"| Au
  Au -->|"audited"| Su
  Su -->|"only what is worth asking"| Sp
```

---

*Source: the living's words of 2026-09-16 in flows/efa157/vision/layers.md and flows/f55ec8/vision/layers.md, modelRoles.md. The Codex-side names Sol and Astra are the living's; no model id is attached to them yet.*
