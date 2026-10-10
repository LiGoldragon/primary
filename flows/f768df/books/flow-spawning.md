<!-- to-the-living:start -->
Presentation.{ «Flow spawning» }

## 1. Start: Field routes; Flow launches

<svg xmlns="http://www.w3.org/2000/svg" width="360" viewBox="0 0 360 220" role="img" aria-label="Field routes, then Flow composes, opens, spawns, binds and registers"><defs><linearGradient id="a" x2="1" y2="1"><stop stop-color="#e6edff"/><stop offset="1" stop-color="#c5d6ff"/></linearGradient></defs><rect width="360" height="220" rx="18" fill="#f7f8fb"/><path d="M86 110C130 35 220 35 274 110" fill="none" stroke="#b36b16" stroke-width="4"/><path d="M274 110C260 177 174 190 126 153" fill="none" stroke="#317a50" stroke-width="4"/><g stroke-width="2"><rect x="16" y="84" width="96" height="54" rx="12" fill="url(#a)" stroke="#425aaf"/><rect x="132" y="30" width="96" height="54" rx="12" fill="#fff0d7" stroke="#b36b16"/><rect x="248" y="84" width="96" height="54" rx="12" fill="#f2e6ff" stroke="#7543a7"/><rect x="132" y="150" width="96" height="54" rx="12" fill="#e2f3e7" stroke="#317a50"/></g><g text-anchor="middle" font-family="system-ui,sans-serif" font-size="14" fill="#17212b"><text x="64" y="106" font-weight="700">Field routes</text><text x="64" y="126">request</text><text x="180" y="52" font-weight="700">Flow composes</text><text x="180" y="72">then opens</text><text x="296" y="106" font-weight="700">spawn + bind</text><text x="296" y="126">or refuse</text><text x="180" y="172" font-weight="700">register</text><text x="180" y="192">then deliver</text></g></svg>

Field routes a request; Flow performs the deterministic launch.

**Current code — crates/flow-nexus/src/launching.rs, audited 4403a7.** Start consumes this binding result.

~~~rust
let binding = match self.perform(Operation::Bind(pane_launch)) {
    Outcome::Bound(binding) => binding,
    _ => return Response::StartRejected(StartRejection::BindingRefused),
};
if self.perform(Operation::Record(Record_Data::Binding(binding.clone())))
    != Outcome::Recorded { return persistence(); }
~~~

**Activation proof:** a real Flow Start through binding and first turn for both harnesses. Code is not that proof.

## 2. Proposed role and originator

<svg xmlns="http://www.w3.org/2000/svg" width="360" viewBox="0 0 360 210" role="img" aria-label="A Flow has either a voice or a job role"><rect width="360" height="210" rx="18" fill="#f7f8fb"/><rect x="105" y="18" width="150" height="50" rx="14" fill="#fff0d7" stroke="#b36b16" stroke-width="2"/><path d="M180 68v33M180 101l-84 32M180 101l84 32" fill="none" stroke="#4d5968" stroke-width="3"/><rect x="20" y="136" width="148" height="55" rx="14" fill="#f2e6ff" stroke="#7543a7" stroke-width="2"/><rect x="192" y="136" width="148" height="55" rx="14" fill="#e2f3e7" stroke="#317a50" stroke-width="2"/><g text-anchor="middle" font-family="system-ui,sans-serif" font-size="14" fill="#17212b"><text x="180" y="49" font-weight="700">Flow.{ FlowId Role }</text><text x="94" y="159" font-weight="700">Voice</text><text x="94" y="180">Aspect + Layer</text><text x="266" y="159" font-weight="700">Job</text><text x="266" y="180">own FlowId</text></g></svg>

**Proposed Flow Library root:**

~~~text
Library                                   ; Flow's Library root: what Signal, Operation and Memory share
[]                                        ; imports
[ FlowId.Integer                          ; types (Integer pending «Datom» ruling 2; String today)
  Voice.{ Aspect Layer }                  ;   an aspect at a layer
  Role.[ Voice Job ]                      ;   what a flow runs as; a job carries nothing, its identity is the flow id
  Flow.{ FlowId Role }
  Originator.[ Voice.{ Aspect Layer }     ;   how the messenger names a sender
               Job.FlowId ] ]
[]                                        ; kinds
[]                                        ; associations
~~~

This is not compiled wire.

A job is explicit. An unknown or unconfigured flow is neither silently a job nor displayed as a voice.

## 3. Replace: one receiving authority

<svg xmlns="http://www.w3.org/2000/svg" width="360" viewBox="0 0 360 220" role="img" aria-label="Replacement stops predecessor then releases successor"><rect width="360" height="220" rx="18" fill="#f7f8fb"/><path d="M75 106C122 35 235 35 285 106" fill="none" stroke="#b0453a" stroke-width="4"/><path d="M285 120C244 186 155 188 92 151" fill="none" stroke="#317a50" stroke-width="4"/><rect x="16" y="86" width="110" height="58" rx="14" fill="#fde7e5" stroke="#b0453a" stroke-width="2"/><rect x="234" y="86" width="110" height="58" rx="14" fill="#e6edff" stroke="#425aaf" stroke-width="2"/><rect x="107" y="158" width="146" height="47" rx="14" fill="#e2f3e7" stroke="#317a50" stroke-width="2"/><g text-anchor="middle" font-family="system-ui,sans-serif" font-size="14" fill="#17212b"><text x="71" y="109" font-weight="700">predecessor</text><text x="71" y="130">Stopped first</text><text x="289" y="109" font-weight="700">successor</text><text x="289" y="130">unroutable</text><text x="180" y="180" font-weight="700">reap succeeds</text><text x="180" y="199">successor routes</text></g></svg>

**Current code — crates/flow-nexus/src/launching.rs, audited 4403a7.** Replace consumes reap; delivery refuses the predecessor before pane closure.

~~~rust
if node.flow_lifecycle != FlowLifecycle::Stopped
    && self.perform(Operation::Record(Record_Data::Stopped(
        replacement.predecessor.clone(),
    ))) != Outcome::Recorded
{
    return refuse(ReplaceRejection::ReapRefused(
        StopRejection::PersistenceRefused,
    ));
}
~~~

**Proposed boundary:** a Voice association moves to the successor only in this successful replacement. A Job has no voice association to move.

**Acceptance:** a failed or ambiguous replacement leaves the prior Voice claim in place; there is never a dual receiver.

## 4. Composition exists; queued delivery is proposed

<svg xmlns="http://www.w3.org/2000/svg" width="360" viewBox="0 0 360 205" role="img" aria-label="Role and brief make a first prompt; later queued delivery is proposed"><rect width="360" height="205" rx="18" fill="#f7f8fb"/><rect x="20" y="22" width="130" height="55" rx="14" fill="#f2e6ff" stroke="#7543a7" stroke-width="2"/><rect x="210" y="22" width="130" height="55" rx="14" fill="#fff0d7" stroke="#b36b16" stroke-width="2"/><path d="M150 50h55" stroke="#4d5968" stroke-width="3"/><rect x="83" y="111" width="194" height="54" rx="14" fill="#e2f3e7" stroke="#317a50" stroke-width="2"/><rect x="105" y="177" width="150" height="20" rx="10" fill="#eceff2" stroke="#79818d" stroke-width="2" stroke-dasharray="6 4"/><g text-anchor="middle" font-family="system-ui,sans-serif" font-size="14" fill="#17212b"><text x="85" y="45" font-weight="700">role</text><text x="85" y="65">standing</text><text x="275" y="45" font-weight="700">brief</text><text x="275" y="65">this work</text><text x="180" y="135" font-weight="700">one first prompt</text><text x="180" y="155">current code</text><text x="180" y="193">proposed delivery</text></g></svg>

**Current code — crates/flow-nexus/src/composition.rs, audited 4403a7.** After the current aspect/power header, the composer appends the task brief.

~~~rust
body.push('\n');
body.push_str(&profile.instruction_prompt);
~~~

Queued context at the next useful wake is proposed; this book does not claim it is implemented. SystemPrompt, FirstPrompt, and Loadable composition remain an existing Context modules ruling, not a decision made here.

## 5. The title has a written example

<svg xmlns="http://www.w3.org/2000/svg" width="360" viewBox="0 0 360 190" role="img" aria-label="Legacy model title and the living's written example"><rect width="360" height="190" rx="18" fill="#f7f8fb"/><rect x="24" y="20" width="312" height="54" rx="14" fill="#fde7e5" stroke="#b0453a" stroke-width="2"/><rect x="24" y="116" width="312" height="54" rx="14" fill="#e2f3e7" stroke="#317a50" stroke-width="2"/><path d="M180 77v32" stroke="#4d5968" stroke-width="3"/><g text-anchor="middle" font-family="system-ui,sans-serif" font-size="14" fill="#17212b"><text x="180" y="44" font-weight="700">current: Aspect.{ Model FlowId }</text><text x="180" y="64">model-derived</text><text x="180" y="140" font-weight="700">his example: { Mind Tertiary 918df4 }</text><text x="180" y="160">ruling still open</text></g></svg>

**Current code — crates/flow-nexus/src/title.rs, audited 4403a7.** native_title supplies the Herdr-facing title.

~~~rust
let model = self.model_name.model_display_name()
    .ok_or_else(|| TitleRefused::UnmappedModel(self.model_name.clone()))?;
Ok(NativeTitle(format!("{aspect}.{{ {model} {flow_id} }}")))
~~~

His written example is { Mind Tertiary 918df4 }; whether the title is that struct or the Flow as written, { 918df4 Voice.{ Mind Tertiary } }, is ruling 1 of «A voice’s name». A job’s title carries its flow id and Job, { 7f3a21 Job }, under either.

<!-- to-the-living:end -->
