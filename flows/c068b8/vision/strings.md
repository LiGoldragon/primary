## Strings are only manipulated by the encoding library
Context: confirming Psyche core Secondary's reading that the Nexus may carry string fields inside types but never handle text.
"Yeah that's right. You understood. Any kind of string manipulation is forbidden because we don't manipulate strings. We manipulate data and 100% of everything that has to do with string manipulation happens in the encoding and decoding layer, which is never handwritten. All of the logic comes from the encoding and decoding library so that anything that touches this only uses the library. Anything that we want to change in terms of how strings are manipulated has to be done in the library and not in some kind of ad hoc handwritten bullshit."
-- psyche, STT.

