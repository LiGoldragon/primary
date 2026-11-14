# Design: Configuration follows the ontology

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file. Title: «Configuration follows the ontology». Kind: Proposal. Signature line: Created by Fable 5.2; a worker assembled the page. Wording marked ADD or COMMENT is final. Modules: /git/github.com/LiGoldragon/psyche-belief. The page ends with the section «Questions».

---

## Proposal 1: A value is configured on the thing it is true of · psyche-belief › vision/nexus.md

COMMENT
His words, 13 November: «I really want to emphasize everything configurable because, like Stevie Viegie said, we don't know what the thing is going to look like.» «It's really important that we make everything configurable and that the configuration is ontologically sensible, so that we don't jam everything in one configuration. If something is per provider, then it should be a per-provider configuration, right? This per-provider configuration can contain: which models each provider provides; how long their cache is; anything that pertains to that provider in terms of that nexus.»

Show the section «## Configuration» as it stands.

ADD, to the section «## Configuration», at its end:
A Nexus's configuration follows its ontology: a value is configured on the thing it is true of, and each such thing is a type of its own, set whole. What is true of a provider is that provider's configuration; what is true of a model, a harness or a permaflow is that one's. A Nexus configures of a thing only what pertains to that Nexus.

---

## Proposal 2: The provider, and the cache of a harness · psyche-belief › vision/flow-nexus.md

COMMENT
His words: «we would have a way to configure so that the Nexus knows how long each model stays warm, or maybe each provider. Maybe it's by provider or by model. I don't know. You can research into that.» «it would need to know which provider is with which model so that it could make the association.» The research (reported, /home/li/primary/flows/1e8210/provider-research.md): the lifetime is neither the provider's nor the model's. It is chosen with each request by the harness: Claude Code takes 1 hour for a subscription's main conversation and 5 minutes for a subagent or an API key, renewed on each hit, and reports the expiry to its status line; OpenAI offers 30 minutes or 12 hours, and what Codex chooses is unverified. So the lifetime is the harness's configuration, and where the harness reports the expiry, the report is used.

Show the paragraph beginning «A harness is described in configuration» and the Ethos block under it, as they stand.

ADD, after the datom block that follows them:
A provider is described in configuration as a harness is: the models it provides. A harness's declaration carries how long its cache keeps an idle session. A flow is hot until the expiry its harness last reported, and where the harness reports none, until that lifetime after its last turn.

```ethos
Library
[ flow:[ Model Minutes HarnessName ] ]     ; imports
[ ProviderName.[ Anthropic OpenAI          ; types: a provider, by name
                 OpenRouter ]
  Provider.{ ProviderName                  ;   the declaration: what the Flow Nexus needs of a provider
             Vector<Model> }               ;     the models it provides
  CacheLifetime.Minutes                    ;   how long a harness's cache keeps an idle session
  HarnessCache.{ HarnessName               ;   set on the harness, since the harness chooses it
                 CacheLifetime } ]
[]                                         ; traits
[]                                         ; associations
```

```datom
Configure.Provider.{ Anthropic [ Fable Opus Sonnet Haiku ] }
Configure.Provider.{ OpenAI [ Astra Sol Luna Terra ] }
Configure.HarnessCache.{ Claude 60 }
Configure.HarnessCache.{ Codex 30 }        ; unverified: what Codex chooses is not yet known
```

---

## Proposal 3: What is being built · psyche-belief › vision/high-level-view.md

COMMENT
His words: «I'm basically more building a framework so that people can create their own meta harness, but we're creating this domain-specific language piece by piece, right? Flow Nexus, Living Nexus, Persona Nexus, Belief Nexus. They're essentially going to build their own personalized machine assistant out of this.»

Show the module whole, as it stands.

ADD, at the end of the module:
What is built is a framework: a domain-specific language, made piece by piece, the Flow Nexus, the Living Nexus, the Persona Nexus and the Belief Nexus among its pieces, out of which a person builds a machine assistant of his own. So everything in it is configurable.

---

## Questions

1. The Claude lifetime differs between a main conversation and a subagent, 60 and 5 minutes. Flows are main conversations, so one value per harness is proposed; enough?
