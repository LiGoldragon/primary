# Lojix ownership

## 2026-08-13T15:40:20+02:00 — System ownership

Agent-authored context: after hearing that Lojix was present in both the
operating-system and home-environment configurations, the psyche ruled its
ownership boundary. Verbatim:

> it should only be in OS

## 2026-08-13T23:32:19+02:00 — Past database is disposable

Agent-authored context: while asking for a clean working Lojix service, the
psyche removed preservation of the existing Lojix database as a recovery
requirement. Verbatim:

> I dont care about any past lojix database.

## 2026-08-14T09:06+02:00 — Deploy lojix first, then upgrade

Agent-authored context: after discovering the installed daemon (0.11.0, schema v2)
cannot read the store (schema v4, written by 0.17.x), blocking lojix-bootstrap
from generating fresh materialized inputs for the dependency upgrade. The psyche
ruled the deployment order. Verbatim:

> the system has to be redeployed with only the newer Lojix daemon, nothing else. And then we can use Lojix to deploy the upgrade. That should have been done already.
