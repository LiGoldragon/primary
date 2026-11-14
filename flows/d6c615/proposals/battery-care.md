Presentation.{ «Battery care, a capability of a laptop node» Review }

# Battery care, a capability of a laptop node

Created by Fable 5.2; Field core Sol found what the hardware offers, and a Sonnet reader gathered it.

### Proposal 1: Battery care · psyche-belief › vision/criomos.md

::: comment
His words, 13 November: «lithium batteries last longer if they're not always fully charged. Because my laptop is usually plugged in, it's not very good to keep it charged all the time. I would like this mechanism, if it's possible, to not be something that the flow just does manually, but something that is done automatically on the nodes in my cluster that have that feature enabled.» «it charges to 80%, and then, once in a while, it charges up all the way and then lets it discharge.» «it could stay plugged in, and then we don't want it to just stay at 100% for weeks because it did the full charge, which is really just to reset the gauge.» «I would like this to be like a service, if possible, so I don't have to tell you to do this again manually.» The module already says CriomOS has no timer and no periodic job, so «once in a while» is answered by an event: a charge that begins when the last full charge is older than the configured days. The event that announces a full battery has not been observed on his laptop yet, so that one arrow is tentative.

His comment on the page refused the sentence «Whatever ends the service, it leaves the battery charging as the firmware does by itself» as magic, and it landed rewritten as «When the service stops, and again when it starts, it returns the battery to charging as the firmware does by itself, so a discharge left unfinished ends at the next start.» He answered the questions by approving the name and the values as written. Landed as psyche-belief d80bc4e.
:::

+ ### Battery care

+ Battery care is a capability of a laptop node, declared in the cluster data with its values. The battery is held between two levels while the charger is connected. When a charge begins and the last full charge is older than the configured days, that charge goes to full, which resets the gauge; when the battery reports full, the node discharges it back to the limit with the charger still connected, and holds it there again. Where the hardware cannot discharge while connected, the node returns to holding and the level falls when the charger is next away.

+ The firmware may forget the levels; they are written again, and read back, at every boot, every resume from any sleep and every connection of the charger. When the service stops, and again when it starts, it returns the battery to charging as the firmware does by itself, so a discharge left unfinished ends at the next start.

```ethos
+ Library
+ []                                   ; imports
+ [ Percent.Integer                    ; types
+   Days.Integer
+   BatteryCare.{ Resume.Percent       ; the capability: charging resumes below this level
+                 Limit.Percent        ;   and stops at this one
+                 FullEvery.Days }     ;   a charge goes to full when the last full charge is older
+   Phase.[ Holding                    ; held between Resume and Limit
+           Calibrating                ; this charge goes to full
+           Returning ] ]              ; full reached: discharging to Limit, charger connected
+ []                                   ; traits
+ []                                   ; associations
```

```datom
+ ; a laptop node in the cluster data; the names are an example
+ { laptop Laptop [ BatteryCare.{ 75 80 30 } ] }
```

```mermaid
+ flowchart TB
+     h["Holding: between Resume and Limit"] -- "a charge begins, the last full charge older than FullEvery" --> c["Calibrating: this charge goes to full"]
+     c -- "the battery reports full" --> r["Returning: discharging, charger connected"]
+     r -- "the level reaches Limit" --> h
+     e["boot, resume, charger connected"] -- "writes the levels again, and reads them back" --> h
```
