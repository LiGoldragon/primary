# Actual listener span proof: blocked before launch

Field34g0/Psycheu7pq required production `vision/listener/0-1.md`, a relevant Single1 fetch resolving to Span0-1, then one fresh cheap flow receiving that version and stopped. Priorwuov singleton proof was explicitly insufficient.

Actual production Ouranos queries through the deployed typed Curriculum client:
- `ResolveSources.[ { Vision listener Single.1 } ]`: exit1, `missing module vision:listener:1`.
- `ResolveSources.[ { Vision listener Single.0 } ]`: exit1, `missing module vision:listener:0`.
- Known `ResolveSources.[ { Spirit core Single.0 } ]`: exit0, `SourcesResolved`, actual serving Psyche revision `508e6ca924e06837ba9e52488c5f14c965d0f92c`.

Fresh origin main read returned the same508e6ca revision. Exact immutable Git tree inspection at that head found no `vision/listener` file and no listener registration in `modules.datom`. This is an absent actual source/registration boundary, not a decoder failure or a fixture result.

No throwaway was launched, so no lifecycle STOP was needed. No authored source, fixture, configuration, continuity or sleep setting was changed. No new switch or replay occurred. Field received Result34g0; Core received the explicit source blocker and serving-read completion/builder-clear notice.

Evidence: `/tmp/flow-5441e0-listener-span/` contains requests, stdout/stderr, exits and successful source-head response. The current live/source observations are limited to the queries above and the checked immutable source head. gxph remains open pending actual span source landing and the subsequently authorized one-flow context/stop proof.
