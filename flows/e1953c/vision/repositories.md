# Repositories

## The federation identity is a repo for now; everything is a repo; a root repo holds the data about all repositories; garbage collection by snapshot stages

Context: answer to the federation-identity question.

> Well, the federation identity is just going to be a repo for now. Everything is a repo, so our databases are amalgamation repos. We should have a root repo that holds essentially all the data about all the repositories:
> - what they're called
> - if they're active or if they are archived
> - if they should be potentially garbage collected because they've been archived a long time
>
> Garbage collecting could mean creating a snapshot, maybe a different one-stage or maybe more than one stage, depending on whether we want to keep some of the history, some of the important versions.

-- psyche, typed.
