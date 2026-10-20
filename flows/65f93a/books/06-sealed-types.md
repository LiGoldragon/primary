<!-- to-the-living:start -->
Presentation.{ «A sealed type in Ethos» }

# A sealed type in Ethos

### Proposal 1: A sealed type, a new section after Traits are explicit; bodies are hand-written · psyche-context › vision/ethos.md

+ A sealed type keeps its positions private: no code outside its own file can read or build them.
+ It is built only by its constructor, a capability with no self that yields the type or a refusal, borne by a trait the type is associated with in the same file.
+ A sealed type cannot be forged, so holding one is proof that its constructor ran.
+ A sealed type is declared with `Sealed` between its name and its shape.

```ethos
+ Library.
+ { [ curriculum:Composed     ; imports: what
+     flow:Requested ]        ;   it is checked by
+   [ VerifiedContext.Sealed. ; types: private
+        { Address            ;   positions
+          String
+          Vector<String> }
+     Refusal.[ Mismatch      ; why it is refused
+               Unknown ] ]
+   [ VerifiesContext.        ; traits: the one
+        [ verified:          ;   constructor, no
+           { [ Requested      ;   self, from a
+               Composed ]     ;   request and a
+             [ Result<Self    ;   composition
+                      Refusal> ] } ] ]
+   [ VerifiedContext.        ; associations
+        [ VerifiesContext ] ] }
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
