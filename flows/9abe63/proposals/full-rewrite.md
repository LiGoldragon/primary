# Full rewrites

Created by Fable.

Source for the book metaflow. Markers: [+added+] green. The section is new; the module is shown whole as it would stand.

## psyche-belief › vision/committing.md — one section added

Why: his words this morning: a component rewritten from scratch keeps its name, so the rewrite is told apart by its major version and its branch.

[+## A full rewrite is the next major version+]

[+A component rewritten from scratch keeps its name and takes the next major version: Flow 1 is a full rewrite of Flow 0, and the two share nothing. The rewrite lives in the same repository, on a branch forked from the root commit, whose first commit removes everything the root held; the new code grows on that empty base, and the old version's branch goes on serving until the new one replaces it.+]

```
git branch flow-1 <root-commit>
git switch flow-1
git rm -r .
git commit -m "Flow 1: empty base"
```
