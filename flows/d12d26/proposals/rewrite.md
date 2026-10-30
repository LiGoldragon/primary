Presentation.{ «A full rewrite» }

# A full rewrite

Created by Fable (ruling); source by Sonnet.

### Proposal 1: vision:rewrite · psyche-belief › vision/rewrite.md, a new file

**Comment** The 9abe63 proposal (full-rewrite.md) to put this in vision:committing never landed, so committing is left as it stands.

+ ---
+ description: A component is being rewritten whole, from scratch.
+ dependencies: []
+ ---
+ 
+ ## A full rewrite is the next major version
+ 
+ A component rewritten from scratch is its next major
+ version: Flow 0 is rewritten as Flow 1. The component
+ keeps its name, because a rewrite from scratch cannot
+ always be renamed.
+ 
+ ## A rewrite lives in the same repository
+ 
+ The rewrite is built in the component's repository, on a
+ history of its own that starts from scratch. The old
+ version and the new share nothing.
+ 
+ ## The example
+ 
+ This is an example, in Jujutsu. It starts a parentless
+ history for the rewrite, named v1, beside the old one.
+ 
+ ```sh
+ jj new 'root()'
+ jj bookmark create v1
+ ```
