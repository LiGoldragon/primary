## 2026-08-22 — considering: psyche logging into the flow protocol; more frequent distillation; a distilled file in the flow's directory

Design session `15b67974`, typed (captured 2026-08-22T13:39+02:00),
stated as a consideration, after the flows/ protocol landed:

> now im considering moving psyche logging into the flow protocol as
> well, and emphasizing more frequent psyche distillation, with
> distilled entries kept in their flow's directory but moved into a
> "distilled" file or something similar.

## 2026-08-22 — psyche/Vision becomes the home of distilled psyche; raw psyche lives in flows/*/psyche/; archives are archive- prefixed files in the same directory

Design session `15b67974`, typed (captured 2026-08-22T15:19+02:00),
answering the anatomy questions on the flow-protocol move.

On whether psyche/Vision/<topic>.md remains the live merged view
while flow directories hold the raw records:

> yes and that would now become the home of distilled psyche going
> forward. so finding raw psyche would search flows/*/psyche/

On whether psyche-archive/ stands unchanged as the destination for
distilled-away raw records:

> no, distilled logs are moved into an archive- prefixed file in the
> same directory

## 2026-08-22 — distillation defined: self-standing records, clarified and purified by the model, always explicitly reviewed by the living psyche; agglomerate across flows, favor recency and certainty

Design session `15b67974`, typed (captured 2026-08-22T16:28+02:00),
answering the unratified "agent annotations are not records" flag
(06196cc7 L716, reconstructed above):

> context is crucial to understand any statement. a distilled record
> is self-standing; clarified and purified by the model, which do
> this very well, but *always reviewed explicitely by the living
> psyche*

> so essentially, psyche distillation is the model attempting to
> articulate the psyche in a more coherent form, agglomerating
> records made across several flows that touch the same topic,
> favoring more recent statements, and favouring statements made
> with more certainty, when overlapping or contradictory readings
> surface.

## 2026-08-22 — a skill is still a file; rename the undistilled corpus; log vision: flows/<id>/vision/; top-level psyche/ maybe unnecessary — Vision/ and Intent/ as typed directories

Design session `15b67974`, typed (captured 2026-08-22T16:47+02:00),
on the proposed psyche-skill wording ("psyche/Vision/<topic>.md —
distilled psyche"; the existing line "The spirit skill — Spirit
lives there, not in a file"):

> 1. a skill is still a file. and untill the entire psyche/ corpus is
> distilled, that proposal isnt true. we could rename the current
> corpus's main directory to make this clear, and encourage
> distillation into the new location
>
> and I just noticed something; we are loggin psyche, yes, but more
> specifically we are logging psyche *vision*. so we should make it
> flows/<id>/vision/...
>
> this could even make the top level psyche/ unecessary. distillation
> could happen in vision/ and intent/ (maybe Vision/ and Intent/
> carry more cognitive weight, and the caps imply a typed directory),
> with spirit being treated in a special way for technical reasons.

The same message continues on spirit and entry files; that part is
logged in spirit.md (2026-08-22).

## 2026-08-22 — forks ruled: psyche-raw good; the case split liked; raw intent and spirit only from the living

Design session `15b67974`, typed (captured 2026-08-22T16:55+02:00),
ruling the four forks of the reshaped proposal:

> 1. good
> 2. clever. I like it
> 3. raw intent, as well as spirit, will always be explicitely brought
> up by the living <- wow! the living is a perfect shorthand for
> living psyche.

Context (agent-authored): 1 approves the psyche-raw/ rename for the
undistilled corpus; 2 approves the case split — caps for the
top-level typed Vision/ and Intent/, lowercase for the flow's raw
vision/; 3 rules that Intent/ and spirit enter only on the living's
explicit word — no flow writes raw intent on its own. The vocabulary
coinage is logged in letsUseTheSameVocabulary; fork 4 (spirit skill,
entry files) in spirit.md and entryFiles.md, same date.
