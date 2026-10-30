# The golden rule of design

Created by Fable; sources gathered by Sonnet (flows/9abe63/research-simplicity.md).

Source for the book metaflow. The module is rewritten whole: show it as a new module shows, the whole text green, and beside it the present module whole in red, under the same path. One why.

## psyche-belief › intent/design.md — rewritten whole

Why: his review of the first version: weigh every line for its ghost, move out what belongs elsewhere, make the symptoms clear about what they are and what only sounds like them, and make the module read as one. What left: the horizon line (vision:psyche has horizons), the free-function line (intent:mandatory-traits has it), the where-it-runs line (spirit:core has configuration over hardwiring). What stays is design alone.

A system is simple when each thing in it does one thing and the things are not braided together, so that any part is understood on its own and changed without touching the rest. Complexity is whatever makes a system hard to understand or to change. Simple is not easy: easy is near at hand, simple is unentangled, and the patch is always the easy move.

A design is one set of ideas held whole by one mind, drawn from the complete concept it belongs to; a good idea holds together like a person. It is made so simple that there are obviously no deficiencies, rather than so complicated that there are no obvious ones.

A design is begun by listing its unknowns and judging them against the complete concept. Research feeds it options to choose from. It advances one step at a time, each step one thing judged on its own: the design, or an abstraction the design needs, or the behavior on that abstraction; a line that needs an abstraction the system lacks is two steps, the abstraction first. A short-term proposal names what it builds on and proposes only what can be built next.

A rewrite is designed first and small: a complex system that works grew from a simple system that worked, so the new system is the smallest one that works, and grows from there.

## The symptoms

A symptom is a place where two concerns were tied into one knot; each knot is where the next change trips. Where one is met, the abstraction under it is redone, rather than the knot added to. Each symptom below is told from the sound thing it resembles.

A special case: a branch that exists for one caller, one host, one file or one moment. A match over the variants of a type is one design deciding by its data, and is sound; the special case is a branch the type does not know.

A fallback chain: the same effect sought by a second design when the first fails, then a third. A match that handles each variant, a failure among them, is one design; a chain of attempts is several designs for one effect, and the effect was owed one.

A flag: a boolean parameter that makes one function behave as two. An option in the data is sound; the two behaviors are two capabilities or two types.

A bare scalar: an integer or a string whose meaning is only in its name. The meaning is a type.

A string in code: a name, a path, a command, a format or a message written as a literal is data the code has swallowed. A string lives in a datom field made to hold one, and the codec is the one place that handles it; a Nexus holds none.

A fact held twice: two places that must agree are one place that was split.

A comment that explains an exception: the knot, confessing.
