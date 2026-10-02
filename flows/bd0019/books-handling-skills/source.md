
## Handling skills

1. **What exists.** Fifty-two authored skill files and one roles file live in Curriculum. A person runs curriculum-deploy by hand; it copies the skills into the generated trees for Claude and Codex, writes twenty-four role files, and marks user-only skills withheld in each harness's own way. The trees match the authored head right now. Then a person commits. Nothing triggers any of this: no hook, no service, no activation. The checker does not notice extra files in the generated trees, Pi gets roles but no skills, and the flake's test input pins a Curriculum head from weeks ago.

2. **What a running seat sees.** A Claude seat re-reads a skill's body when it is invoked, but its list of skills is fixed when it starts; Codex builds its catalog at start. So an edited body probably reaches a running Claude seat, a new skill or a changed description needs a restart, and Codex probably needs one always. This is read from the harnesses' behaviour and vendor documentation, not yet tested here.

3. **Your words.** Settled: "now vision is skill"; "We need to make a nexus to deploy skills ... changes the ones that have the same name. That sounds simple to me." Open, in your own words: "we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know." Also standing: "the skills will be typed", a nexus "that has a fully typed specification for the different types of inputs that it can take"; and "eventually the skills will live in a daemon not in a Git repo anymore."

4. **The design view.** Deployment is one mechanical act that should happen on one event, a push to Curriculum, with no person in the loop: the Curriculum Nexus subscribes to its repository, generates, commits the trees, and tells Flow which seats now run stale skills; Flow restarts the ones whose skill list changed when they next go idle, and leaves the others, whose bodies refresh on invocation. Your "simple" nexus is exactly this, with the typed input you asked for being the Generate datom that already exists. What it needs decided is only whether a running seat is ever restarted for a skill change without a person's word.

## Ruling

- Stale seats restarted on idle by Flow automatically, or only on your word.