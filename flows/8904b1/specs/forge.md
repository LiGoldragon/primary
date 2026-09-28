# Forge — specification, first form

Written by Psyche Fable 8904b1 on 2026-09-28 for Mind Astra to build, from the living's words in `flows/8904b1/vision/anatomy.md` (records 8904b1-28 and 8904b1-29). A proposal where the living has not spoken; the living's words govern where they have.

## What it is

Forge builds. It turns a source at an exact revision into a plan, and a plan into a closure. It describes no host, carries nothing between hosts, activates nothing, and holds no authority over any host.

## Why it exists

Lojix holds describing, building, carrying and activating in one request, and is installed by the system it deploys, so mending it needs a deployment. On 2026-09-28 it built on the wrong host although a builder was named. Forge is the building part, alone, usable by hand the day it exists. Lojix is later composed over it.

## Properties that must hold

1. It runs from its own repository. No system or home activation is needed to use a changed Forge.
2. It builds on the host it runs on and nowhere else. It never sends a build to another host and never accepts one silently moved. A build request names the host expected to build; Forge refuses when that is not the host it runs on.
3. Every answer names the host that did the work.
4. Evaluating and building are separate requests. A plan made once can be built later, elsewhere, by the Forge of that host.
5. A source is an exact, immutable revision. A movable reference is refused.
6. One datom in, one datom out. No flags.
7. A refusal or failure says which step failed and why, in its own words, not a shared generic reason.

## Interface

    Type
    Forge.[ Evaluate.{ Source Target }  Build.{ Plan Host }  Inspect.Closure ]
    [ Source.{ Flake Revision }  Target.[ System.Host  Home.{ Host User }  Package.Attribute ]
      Flake.String  Revision.String  Host.String  User.String  Attribute.String  Plan.StorePath  Closure.StorePath  StorePath.String ]

    Type
    Forged.[ Planned.{ Plan Host }  Built.{ Closure Host Seconds }  Inspected.{ Closure Bytes Vector<StorePath> }
             Refused.Reason  Failed.{ Step Reason } ]
    [ Step.[ Evaluation Build ]  Reason.String  Seconds.Integer  Bytes.Integer ]

Examples:

    forge 'Evaluate.{ { github:LiGoldragon/CriomOS 40eeb7d603b1… } System.zeus }'
    Planned.{ /nix/store/…-nixos-system-zeus.drv ouranos }

    forge 'Build.{ /nix/store/…-nixos-system-zeus.drv prometheus }'
    Built.{ /nix/store/…-nixos-system-zeus prometheus 412 }

## Our kind of builds

A host's system is evaluated from generated inputs (horizon, system, deployment, secrets) that Lojix materializes today from the cluster data. Forge does not generate them. In this first form the flake given to Evaluate is the materialized one, and Evaluate runs where those inputs are. The plan is then carried to the building host by other means (today by hand; later by Reach), and that host's Forge builds it.

## Stages

1. The command alone, doing the work directly, with exactly these types. Used by hand and over SSH.
2. The nexus: a daemon on the nexus core, ordinary socket for Inspect and for watching a build, owner socket for Evaluate and Build. The types do not change.

## The existing forge repository

It holds an older, unrelated design with no working code. Start the new Forge in it, replacing what is there, and say in its README what was replaced.

## Acceptance

The Zeus system closure, or the next host's, is built on Prometheus by `forge` run there, and the answer names Prometheus. A build request naming another host is refused. A movable revision is refused. Tests are Nix checks, each seen failing once.

## Not in this form

Carrying, activating, authentication, distribution of build jobs across hosts, sandboxed builds, and the living's earlier Forge ideas of 2026-09-14 (`flows/6cc91b/vision/forge.md`), which are not contradicted here and are left for later forms.
