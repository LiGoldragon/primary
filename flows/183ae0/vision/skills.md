# Skills

## Distilled vision is automatically a skill

> I mean, to edit the skill or create one, the models don't seem to understand that distilled vision is automatically a skill. There's no more separation. We have to make that clear: that vision is automatically a skill, because otherwise it's not very useful. It's just a file. My vision is what should imbue some of the most important context of the model.

Context: said after reading Psyche Fable's page on the Criome–Mentci bridge, which the living found "a bunch of gap-filling with a poor understanding of my approach", going against much the living has said before.

-- psyche, typed.

## Skills leave the Curriculum; three skill repos

> The skills are not supposed to be in the curriculum anymore. The curriculum is just the executable source code. Now we need three skill repos so we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know.

Context: answered this flow's proposal to keep vision skills in the Curriculum skills source.

-- psyche, typed.

## Why skills leave the Rust code

> You see the skills can't be with the Rust code because then we rebuild the whole executable every time we change a skill.

Context: the reason for the entry above.

-- psyche, typed.

## Typed skills, a skill nexus

> No the skills will be typed. Just copying the directory name is dirty. We make a nexus that has a fully typed specification for the different types of inputs that it can take. Let's do the anatomy of that.

Context: answered this flow's reading that the generator writes a skill's prefix from the directory it sits in.

-- psyche, typed.

## Vision moves into skills

> I do want to move the vision into skills. It is too bad that changing any skill requires recompiling the entire Rust binary that we use to deploy it, which is ridiculous. It would be nice to fix that but maybe we just take a fresh look at the whole problem of skill deployment or maybe it's not. There's a lot to think about.

-- psyche, typed.

## Three skill repos, and log repos beside them

> I would like [agents] to be able to edit skills that pertain to them easily. That's why the three repos. Each of these repos is actually where I think we should keep the distilled part separate. We could have another repo for psyche logs, mind logs, and field logs for the actual logs. We could just write a simple Clojure script to query all of the logs because we would symlink these repos into the workspace. To search all the vision from the three different repos, the raw vision, we could have a Clojure executable that does that.

-- psyche, typed. Transcription corrected: "Asian" → "agents".
