# Structural parsing

## Arity discriminates; more head delimiters; the Capability enum of structural forms

2026-08-27, the psyche, dictated, with a handwritten page
(ethosAdvancedStructuralParsing.jpg, transcribed below):

> I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types. And I don't know why I didn't actually seriously contemplate this before. It seems pretty obvious now. Also, I think we should introduce more of the concept of using different delimiters between the head and the delimiter to add even more type differentiation using very minimal character slash token cost. So I handwrote some of these concepts, and this is really just early brainstorming on what For example, how we can differentiate between different capability types. So this would be... I essentially use the ethos -- Syntax for defining an enum to show the different types of capabilities that could exist. And then in the comments, I would I was showing how the the syntax would expose their types by writing them with a different structure, which could include the... and I didn't really elaborate much on this because I was running out of page, but which could also include the number of components in a brace, which symbolically stands for a struck [struct]. But in this case, we wouldn't be limited to a single type of struck [struct].

> <> is a real Protos delimiter of course. I'm surprised you have to ask

### The handwritten page (transcription; the image is authoritative)

    Ethos advanced Structural Parsing

    Capability.[                    ;; A Vector-represented Enum
      SingleYield.{Name Concept}
      ;; ↑ Represented as 'Head.Concept'
      ;; A Concept being a type or a Kind

      ;; Thought experiment: Different head delimiter
      ;; to differentiate mutable self 'Head!Concept'
      MutableSingleYield.{Name Concept}

      MultipleYields.{Name Vector<Concept>}
                      ;; Name.[ConceptOne ConceptTwo ...]

      MutableMultipleYields...

      Multiple-
      Standard.{Name Vector<Concept> Vector<Concept>}
      ;; Head.{[InputOne InputTwo] [OutputOne OutputTwo]}

      ...
    ]
