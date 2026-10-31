
## The Nexus cannot turn a message into text

Context: relayed by Psyche core Secondary; said to it after being shown that flow-nexus renders each message to text in delivery/body.rs (datomize, protosize, compact) and runs herdr agent prompt with it from herdr/pane.rs.

"Well that's what I'm saying. The Nexus cannot itself turn a message into text. It has to use another tool because it cannot have text in its code."

-- psyche, STT.

## String manipulation lives only in the encoding and decoding library

Context: relayed by Psyche core Secondary; the living confirming that the Nexus may carry string fields inside types but never handle text; for the text-tool book.

"Yeah that's right. You understood. Any kind of string manipulation is forbidden because we don't manipulate strings. We manipulate data and 100% of everything that has to do with string manipulation happens in the encoding and decoding layer, which is never handwritten. All of the logic comes from the encoding and decoding library so that anything that touches this only uses the library. Anything that we want to change in terms of how strings are manipulated has to be done in the library and not in some kind of ad hoc handwritten bullshit."

-- psyche, STT.
