# dc7b: current proposal Ethos check

Checked all 12 Ethos fences in the three current d9cedc proposals on Prometheus with ethos-zero 29, published revision f23eacf338a90ce4a6dea011554724fa6488fcc9. Addition prefixes were removed mechanically; the whole fence was passed directly to Check, without implied-Library wrapping. Ten original fences pass. Two refuse. All twelve pass with the candidate corrections below. Sources have not been changed.

## Chronos Memory, source line 109

Complete refusal:

```datom
Rejected.{ { 3 3 } Conceptual.{ [ 1 1 0 ] Expected.Declaration } }
```

The bare imported Configuration is not a record declaration in Memory. Candidate replacement fence (same fields as the Library configuration):

```ethos
Memory
[ chronos:[ Location Display ] ]         ; imports
[ Configuration.{ Location Vector<Display> } ; records: the configuration last read
  Answer.[ Succeeded Failed ] ]
```

This repeats the Library configuration shape; whether Memory should instead support referring to an imported record is a design question. This candidate is a grammar-valid expression of the existing record, not a proposed change to the configuration data.

## Listener Emission, source line 228

Complete refusal:

```datom
Rejected.{ { 8 3 } Conceptual.{ [ 1 1 4 ] Duplicate.Text } }
```

Paste, Copy and Notify carry Text, but an emission payload type binds to one outcome. Give the emissions distinct inline payload types, retaining one Text field each:

```ethos
  Paste.{ Text }
  Copy.{ Text }
  Notify.{ Text }
```

All seven emission/outcome pairings and the text carried are preserved. The candidate passes Check.

## Evidence

Original extracted fences and complete results: /tmp/book-b1218b/{fences,results}.json. Candidate fences and complete results: /tmp/book-b1218b/{corrected,corrected-results}.json. Checker script: /tmp/book-b1218b/check.clj. The same checker and files are on Prometheus; original fences.json there was replaced with the candidate file for the second check.

Code anatomy has one fence and passes unchanged. Its v3 publication receipt was carried by ab4e4b; Chronos and Listener republication follow corrected-source approval.
