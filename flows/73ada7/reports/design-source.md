# Design Source Report

**Blob id at 9541cd08:** 1ce61fb172391437fd910c874e89e4551dc475d2

**Later commits on origin/main (e992c34f3) that change this path:** None. Commit 9541cd08a is the most recent on main touching this file.

**Configuration examination:** Yes, the blob carries Configuration with three paths and both ordinary and meta Configure contracts.

Lines 163-166 show the three paths:
```
[ Configuration.{
     Ordinary.String            ; socket paths: records on the way
     Meta.String                ; to a typed path
     Flow.String } ]            ; the Flow edge
```

Lines 101-104 establish both contract types:
```
- First configuration [R] (vision-nexus): Memory's `Standard` record
  has `MetaConfigured`. While it is false, `Configure` is answered on
  the ordinary socket too. A meta `Configure` sets it true, after
  which an ordinary `Configure` is refused `AlreadyConfigured`.
```
