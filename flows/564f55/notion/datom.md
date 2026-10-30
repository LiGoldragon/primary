# datom

## 2026-09-09 — the value layer: a brainstorm, ruling nothing

The psyche's words on a value layer between datom and the native Rust value were logged in vision/datom.md under the headings "another layer: the abstraction for the value itself, as JSON has Value" and the surrounding exchange; the psyche then said they were a notion. They are held here as notion, the bottom layer:

> I was introducing the concept of another layer. Of course I know that the value is a concrete instance. ... That's why I'm saying: what is that instance? What are we going to make the abstraction for that value so that JSON [STT: Jason] has Value, right? What is the value? Well, we don't know. It's going to find out when it tries to serialize it, so we don't have that layer.

> The reason I brought up the value layer was: imagine you're writing the code, the general code that's going to Datomize something. Maybe you want an actual type somewhere, which is generic enough to not really know what it is at that moment in the code, to just call Datomize on it. Since you're going to derive Datomize, then I guess my fears were unfounded. It's just going to be derived from the derived macro, and that's where the Datomize code will go in.

-- psyche, STT.
