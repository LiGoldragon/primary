# Vision migration

Method: probe python3 /tmp/w5-vision-migration.py --verify

Approved manifest SHA-256: `7fdfae454f458506b3fdc8b984ae16d8fc284cca5a03bd53b212ae9abaf73718`. The replay verified 308 raw quoted-record hashes and their actual transcript record identities, then migrated 308 units into 135 camelCase destinations across 28 origin flows. It reconstructed 19 newly absent flow logs and index records, preserved each raw source remainder exactly, and retained all raw-Vision files not named by the manifest. The 308 actual transcript-record SHA-256 values combine to `51683bf649384291c4eef3ec1d77f8356a218d1fdf997433dca6a5fe3e21f8c5`.
