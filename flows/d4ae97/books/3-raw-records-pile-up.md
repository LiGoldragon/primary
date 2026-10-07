<!-- to-the-living:start -->
Presentation.{ «Raw records pile up» }

Archived records sit beside live ones, where every flow searches, and distillation has nearly stopped: 1,519 live raw files today, 254 on 27 August.

## Proposal 1: `psyche-distillation`, where the archive goes
Removed:
```
The raw records a distillation replaces move
into an `archive-` prefixed file beside their
source file.
```
Added:
```
The raw records a distillation replaces move,
in the landing's own commit, to
`psyche-archive/<short-id>/<topic>.md`; an
archived record is no longer raw psyche and
is read only through a sources line.
```

## Proposal 2: `psyche-distillation`, archiving is part of landing
Added:
```
A landing whose sources lines still resolve
to a live raw record is not landed.
```

## Proposal 3: `psyche`, where raw psyche is searched
Removed:
```
Finding raw psyche means searching
`flows/*/vision/`.
```
Added:
```
Finding raw psyche means searching
`flows/*/vision/`; distilled records have
left it for `psyche-archive/`.
```

## Proposal 4: `psyche-distillation`, a pace
Added:
```
A topic holding more than 20 live raw records
is distilled before new work on it.
```

## Proposal 5: `psyche-distillation`, skills owe sources
Added:
```
A distillation into a vision skill keeps a
sources file and archives its records, as one
into `Vision/` does.
```

## Rulings
1. Proposal 1: (a) land (b) amend.
2. Proposal 2: (a) land (b) amend.
3. Proposal 3: (a) land (b) amend.
4. Proposal 4: (a) land (b) amend, naming the number.
5. Proposal 5: (a) land (b) amend.
6. On landing 1 to 3, the 151 existing archive files move and the 29 live sources are archived: (a) yes (b) not now.
<!-- to-the-living:end -->
