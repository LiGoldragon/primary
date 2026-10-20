<!-- to-the-living:start -->
Presentation.{ «Flow, the decisions, second edition» }

# Flow, the decisions, second edition

### Proposal 24: A second Secondary without a pane is started again, and the cause of its loss is sought · primary › docs/flow-up.md

**Comment** Same record as Proposals 1 to 23 of the first edition (7pUh2hzCFMDiKaAfrETuuH), which stand as they were sent; the three entries here follow rulings 11 to 13.

+ Second restart. Psyche core Secondary ca28a4, with its pane gone and no continuation left, is started again through Flow, `flow-start Psyche core Secondary -p ca28a4`, by 4201a3. Result: Flow Awake.379e7a, pane w3E:p1. The route of ca28a4 is retired first, and flow-start registers the route of 379e7a itself and writes its continuation. Mind core Secondary finds the cause of pane loss from the Herdr and Flow records before a third Secondary is lost, as work ahead of gap 8.
+ - Why: the hub of the topic must answer, and a Secondary whose pane is gone is asleep (Proposal 17), to be started again through Flow (Proposal 18).
+ - Corner: the retire bypassed the live-pane check for a pane proven gone (Proposal 9). Landing owed: the cause, from Herdr and Flow records.

Ruling: land, amend, or reject.

### Proposal 25: A flow asleep after its turn is not lost · primary › docs/flow-up.md

+ Designed close. A flow Asleep after its turn is not lost. 4201a3 reports (a claim, with the designed sleep of Flow 0.34.4 behind it) that the Asleep state of ca28a4 was the designed close and only its continuation was missing, because a hand registration (hm-register) writes none. The pane-loss cause of Proposal 24 is withdrawn for ca28a4; for 9864c0 it remains unknown.
+ - Why: Our reading: the first start of ca28a4 launched its pane and failed at registration, so the hand registration that followed left no continuation; Flow slept it as designed.
+ - Corner: the claim is not witnessed by this seat. Landing owed: the witness, with the cause for 9864c0.

Ruling: land, amend, or reject.

### Proposal 26: A send to an Asleep flow is queued and wakes it · primary › docs/flow-up.md

+ Sleeping address. A send to an Asleep flow is queued through Flow and wakes it, exactly as the queue delivered 4201a3's orders to this flow. The messenger never refuses a send because the target's pane is closed, and a closed pane is never shown STALE for an Asleep address. No Secondary is restarted for being asleep again. Mind lands this with ruling 10 (Proposals 3 and 19).
+ - Why: Our reading: a closed pane is the designed close of an Asleep flow, so reaching it is a queue and a wake, not a restart.
+ - Corner: not landed; until it is, the sender relay of Proposal 11 and the hand retire of Proposal 9 stand. Landing owed: the messenger and relay change.

```text
+----------------------------------+
| sender                           |
+----------------------------------+
        |
        | sends through
        v
+----------------------------------+
| Flow queue                       |
+----------------------------------+
        |
        | wakes
        v
+----------------------------------+
| Asleep flow, pane closed         |
+----------------------------------+
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
