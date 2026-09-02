# Credential store

- Entry: `wispr-flow/credentials`
- Safe boundary and method: the identified local Wispr configuration credential document was connected directly as the standard-input file descriptor of GoPass `cat`, whose supported import contract encodes standard input into the named entry. The bytes crossed only the kernel file-descriptor boundary into GoPass and its configured cryptographic/store backend; they were not read by this flow, placed in argv or environment, copied to a clipboard or temporary file, or sent through a filter or printing command.
- Metadata witness: immediately after the import, the non-decrypting `gopass ls wispr-flow` listing showed `wispr-flow/credentials`.

## Sources

- Listener source inspection: `src/transcription.rs` declares and resolves the existing `openai/api-key` GoPass convention.
- GoPass 1.16.1 local CLI help: `gopass cat --help` states that the command encodes and inserts from standard input.
- Direct local witness: the completed import command returned success, followed by the non-decrypting entry listing above.
