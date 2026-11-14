Presentation.{ «Configuration follows the ontology» Proposal }

# Configuration follows the ontology

Created by Fable 5.2; a worker assembled the page.

### Proposal 1: A value is configured on the thing it is true of · psyche-belief › vision/nexus.md

::: comment
His words, 13 November: «I really want to emphasize everything configurable because, like Stevie Viegie said, we don't know what the thing is going to look like.» «It's really important that we make everything configurable and that the configuration is ontologically sensible, so that we don't jam everything in one configuration. If something is per provider, then it should be a per-provider configuration, right? This per-provider configuration can contain: which models each provider provides; how long their cache is; anything that pertains to that provider in terms of that nexus.»
:::

::: shown
psyche-belief › vision/nexus.md
## Configuration

For now, a Nexus starts with no arguments and there is no bootstrap
binary. Its executable holds a default configuration as a constant. On
start it looks for its memory at the default location: a memory that
exists holds the configuration; a memory created new is seeded with the
defaults. The meta socket carries a Configure interface, and changed
values are accepted through it.
:::

+ A Nexus's configuration follows its ontology: a value is configured on the thing it is true of, and each such thing is a type of its own, set whole. What is true of a provider is that provider's configuration; what is true of a model, a harness or a permaflow is that one's. A Nexus configures of a thing only what pertains to that Nexus.

### Proposal 2: The provider, and the cache of a harness · psyche-belief › vision/flow-nexus.md

::: comment
His words: «we would have a way to configure so that the Nexus knows how long each model stays warm, or maybe each provider. Maybe it's by provider or by model. I don't know. You can research into that.» «it would need to know which provider is with which model so that it could make the association.» The research (reported, /home/li/primary/flows/1e8210/provider-research.md): the lifetime is neither the provider's nor the model's. It is chosen with each request by the harness: Claude Code takes 1 hour for a subscription's main conversation and 5 minutes for a subagent or an API key, renewed on each hit, and reports the expiry to its status line; OpenAI offers 30 minutes or 12 hours, and what Codex chooses is unverified. So the lifetime is the harness's configuration, and where the harness reports the expiry, the report is used.
:::

::: shown
psyche-belief › vision/flow-nexus.md
A harness is described in configuration: every feature it has, and what leaving that feature out does to the launch, a flag or a variable. The Nexus holds no feature and no effect of its own; it reads the effect from the declaration and composes the launch from the names a permaflow lists. A new harness, or a new version of one, is a new declaration. Where two features share one flag, the composition emits that flag once, with the names merged.

```ethos
Library
[ flow:[ Address ] ]                  ; imports: the permaflow's address
[ HarnessName.[ Claude Codex ]        ; types: a harness, by name
  FeatureName.String                  ;   a feature, by name
  Effect.[ Flag.String                ;   what leaving the feature out does to the launch
           Environment.{ Name.String  ;     a variable, set for the harness alone
                         Value.String } ]
  Feature.{ FeatureName Effect }
  Harness.{ HarnessName               ; the declaration: every feature the harness has
            Features.Vector<Feature> }
  Root.String                         ; the flow's working directory
  Permaflow.{ Address
              Option<Root>
              HarnessName
              LeaveOuts.Vector<FeatureName> } ]
[]                                    ; traits
[]                                    ; associations
```
:::

+ A provider is described in configuration as a harness is: the models it provides. A harness's declaration carries how long its cache keeps an idle session. A flow is hot until the expiry its harness last reported, and where the harness reports none, until that lifetime after its last turn.

+ ```ethos
+ Library
+ [ flow:[ Model Minutes HarnessName ] ]     ; imports
+ [ ProviderName.[ Anthropic OpenAI          ; types: a provider, by name
+                  OpenRouter ]
+   Provider.{ ProviderName                  ;   the declaration: what the Flow Nexus needs of a provider
+              Vector<Model> }               ;     the models it provides
+   CacheLifetime.Minutes                    ;   how long a harness's cache keeps an idle session
+   HarnessCache.{ HarnessName               ;   set on the harness, since the harness chooses it
+                  CacheLifetime } ]
+ []                                         ; traits
+ []                                         ; associations
+ ```

+ ```datom
+ Configure.Provider.{ Anthropic [ Fable Opus Sonnet Haiku ] }
+ Configure.Provider.{ OpenAI [ Astra Sol Luna Terra ] }
+ Configure.HarnessCache.{ Claude 60 }
+ Configure.HarnessCache.{ Codex 30 }        ; unverified: what Codex chooses is not yet known
+ ```

### Proposal 3: What is being built · psyche-belief › vision/high-level-view.md

::: comment
His words: «I'm basically more building a framework so that people can create their own meta harness, but we're creating this domain-specific language piece by piece, right? Flow Nexus, Living Nexus, Persona Nexus, Belief Nexus. They're essentially going to build their own personalized machine assistant out of this.»
:::

::: shown
psyche-belief › vision/high-level-view.md
## The very high-level view is looked at routinely

The very high-level view of what is being built is looked at
routinely.

## A view takes room

A high-level view takes room and breaks everything down in-line. It gives someone joining the project, in half an hour, a clear view of the whole engine: each repository, what it is and how much it does.

## The great advancements

In the long term, the great advancements are the improvements that most increase the definition of the psyche.

Each one unlocked raises the system's efficiency, output quality and ease of use.
:::

+ What is built is a framework: a domain-specific language, made piece by piece, the Flow Nexus, the Living Nexus, the Persona Nexus and the Belief Nexus among its pieces, out of which a person builds a machine assistant of his own. So everything in it is configurable.

## Questions

1. The Claude lifetime differs between a main conversation and a subagent, 60 and 5 minutes. Flows are main conversations, so one value per harness is proposed; enough?
