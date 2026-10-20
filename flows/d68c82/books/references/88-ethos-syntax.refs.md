# References: Ethos: imports and definition brackets

## The living's words

- flows/d68c82/vision/ethos.md, "Imports start with a colon and can be inline" (2026-10-19 17:33 book comment): leading colon, uncapitalized namespace addressing the registry, further colons down to the type, same syntax in the import section
- flows/d68c82/vision/ethos.md, "White braces define a struct; white square brackets define a vector" (same comment): white braces for struct definition versus struct declaration; white square brackets instead of the word vector
- flows/d68c82/vision/ethos.md, "White square brackets as sugar; layers; traits as capabilities" (2026-10-16) and the comment ordering an Ethos book (the new vector and struct syntax, "run by the ethos topic stack")
- Author's brief: white braces are U+2983 U+2984; white square brackets U+27E6 U+27E7; "struct declaration" read as the struct value

## Current modules, origin main 4de1d9a

- psyche-context vision/ethos.md: "Imports" (181-200: `protos:String`, `protos:[ String Integer ]`, intrinsic names including Vector, `Topic.custom:Name`); "Shapes and placement" (342-349: "a bracket is an enum, never a vector"); "The type ethos" (174-179); "Spacing" (481-489)
- mind-context skills/knowledge-ethos.md: imports are `protos:String` or `protos:[ String Integer ]`; labelled "As of 16.0.0" and still says kinds (main of ethos-zero says traits)

## Witnessed in code (read subflows)

- ethos-zero main 07714b0 (17.0.0): `Check` of a scratch file with an import, two structs, a vector field and a vector alias returned Checked, exit 0; `Map<String Integer>` refused as Undeclared.Map
- ethos-zero: imports `source:Name` / `source:[ Name ... ]`, a renamed import `Ethos.Emitted`, a source is one Rust path name (no leading `::`, no `Self`, no generics); a sourced reference `source:Name` anywhere a type goes, no import needed; a second source level is refused (Expected.Reference); `Custom:Name` is accepted (the vision text says a lowercase first letter); `std:clone:Clonable.Clone` refused (README says it works)
- ethos-zero probes: `:custom:Name` read as `Name.«:custom:Name»`; `ethos-zero:Name` read as `Name.ethos-zero`; the file with all three proposed forms refused as Expected.Import
- protos 0.32.2: colon is one of three separators; a leading colon makes the whole run one bare node; `Head.:x:Y` and `:x:[ ... ]` are not read as headed; Enclosure has three pairs (the vision text says five)
- datom-codec: no colon separator; a headed node with a colon is turned back into a bare string; a string with a leading or trailing colon is quoted; no map and no set (Form: Struct, Vector, Variant, Bare, String, Meaning)
- Unmerged branches `ethos-proposals` in protos (7832e59 white brackets, 7e4d540 white braces), datom-codec (6909d5c), ethos-zero (3fc2f3d sugaring, 423103d colon chain for std): the white pairs as exact sugar for plain braces and Vector; the colon chain resolves through Rust paths, with no leading colon
- Colon uses: capability receiver `name:[ ... ]`; flow vision `core:Name` topic; context module names `kind:name` (words only, no parser found)
- Not witnessed: the glyphs on a phone; any implementation of the registry; counts of live files using Vector, structs or imports (not stated in the book)

## Glyph measurement (author)

- Chrome headless, canvas measureText at 20px, stacks "Roboto Mono, Droid Sans Mono, Noto Sans Mono, Menlo, monospace", DejaVu Sans Mono and FreeMono: M, colon, braces, brackets and ⟦ ⟧ measure 12 (cell); ⦃ ⦄ measure 14.68 (fallback to DejaVu Sans, proportional). fc-list: U+2983 is in no monospace face except Iosevka Nerd Font Mono and Unifont; U+27E6 is in DejaVu Sans Mono and FreeMono. Phone not observed; hence Proposal 4.

## Checks

- Examples marked "today (checked)" in Proposal 5 passed ethos-zero main `Check`; the proposed forms are not parseable and are labelled
- tools/book-check.mjs passed
- Proposals 1 to 3 show an import, a struct and a vector; every proposal anchors on text of vision/ethos.md as origin main has it

## Proposals

1. vision/ethos.md "Imports": leading-colon import, inline and in the import section
2. vision/ethos.md new section "White braces define a struct"
3. vision/ethos.md new section "White square brackets define a vector"; "Shapes and placement" line; intrinsic names without Vector
4. vision/ethos.md new section "ASCII spellings of the white delimiters" (question; shown because the white braces fall outside the monospace cell)
5. mind-context inquiry/ethos-syntax-imports-and-brackets.md (new): colon conflicts, map and set, registry grammar, reader and generator changes
