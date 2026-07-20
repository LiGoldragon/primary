---
name: nota-schema-design
description: 'Nota schema design rules.'
---

# NOTA shape checklist

- Start from the expected type.
- Emit every positional value in order.
- Use vectors only for repeatable values and maps only for keyed values.

## NOTA schema design

- Make each value shape explicit in schema.
- Keep fields, arguments, and variant payloads positional.
- Model optionality and alternatives as typed data.
- Keep schema, codec, help, and round trips aligned.
