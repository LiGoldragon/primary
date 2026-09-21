# Speech-to-text interpretation and Wispr Flow

## Proposed instruction edit for review

The direct correction was that “contacts” in a context-and-usage request meant “context”; the main flow already understood this and should not have interrupted. The living says speech-to-text is the primary input and they cannot proofread every message. Existing `psyche-interraction.md` already says to correct known transcription errors **inside** psyche quotes and note the correction beside them. Its last line already requires a behavioral correction to reach the owning skill in the same reply. `correction.md`, loaded through `spirit`, nevertheless says to fix the instruction file before fixing output, while `psyche-interraction.md` requires approval before every skill edit. The proposal below resolves that sequencing conflict and makes contextual STT reading available to ordinary flows through `behavior`, which `spirit` loads. No authored skill or generated projection was changed.

Exact proposed edits in authored Curriculum sources:

```diff
diff --git a/skills/behavior.md b/skills/behavior.md
@@
 description: A claim is relayed, a thing is called verified, an act is explained, or a value that differs between setups is written.
 dependencies: []
 ---

+Expect speech-to-text errors in the living's messages; the living does not have time to proofread every message. Resolve a clear error from the immediate context and confirmed vocabulary without interrupting the work. Ask only when competing readings materially change the action. When recording a correction, retain the received wording, intended reading, provenance, and context; a context-specific reading is not a global text replacement.

diff --git a/skills/correction.md b/skills/correction.md
@@
-Fix the file that sentence came from, or should have come from, before fixing the output.
+Bring every behavioral correction from the living forward in the same reply as an exact proposed edit to its owning skill or prompt. When the edit requires approval, present it before changing the file; once approved, fix the source before revising the output. A corrected answer or vision record alone does not carry the instruction to later flows.
```

No role manifest change appears necessary for these two edits: `spirit` depends on both `behavior` and `correction`; the deployed `spirit` is in the available skill catalog for every task. `psyche-interraction` continues to own quote repair and direct conversation. After approval, the authored files must be changed, generated projections regenerated, and a fresh-flow test should replay the “contacts” context without asking a redundant question. If the prompt, rather than a skill, caused an individual mistake, the correction procedure still identifies that prompt owner. This proposal is deliberately not a new general-purpose substitution table.

## Correction ledger seed

| Received | Intended | Scope | Evidence | Wispr action |
| --- | --- | --- | --- | --- |
| `contacts` | `context` | Flow context/usage reporting in the 2026-09-21 exchange | Explicitly confirmed by the living in `flows/6db4fe/vision/speechToText.md` | **Do not import as a global Wispr replacement.** “Contacts” is a valid word; Wispr corrections are literal and context-insensitive. Track this as a contextual interpretation unless the living confirms a narrower spoken phrase and repeat pattern. |

Other archived vision records contain individually corrected names and terms, but this review did not certify them as recurrent errors or as dictionary import candidates. A future per-user ledger can hold observed output, intended wording, source quote, confirmation grade, domain, frequency, and destination (context-only, dictionary word, literal replacement, or snippet). The living's wish to customize speech recognition to each person's voice is a project direction; it is not evidence that a trained model or deployment has been authorized.

## Wispr Flow facilities and limits

Wispr's current dictionary supports words and phrases to improve recognition. On Mac/Windows and iOS, “Correct a misspelling” maps a persistent wrong phrase to a desired one. Desktop replacements match whole words case-insensitively, prefer longer phrases, and are literal across contexts. Android can use synced corrections but the current dictionary guide says it cannot create them there. Only the 200 most recently modified personal/shared dictionary entries are used in dictation. Dictionary and snippets sync across signed-in devices when eligible and online. [Dictionary guide](https://docs.wisprflow.ai/articles/4052411709-Teach-Flow-your-words-with-the-dictionary).

An eligible paid/trial account can enable **Settings → Experimental → Bulk import** on Mac/Windows. Dictionary accepts a one- or two-column CSV (word alone or wrong phrase → correct phrase), up to 1,000 entries and 3 MB, with 60-character fields. Imports can target personal or team scope and show a preview before submission. Mobile bulk import is unavailable. The September 1 bulk-import article still says Android has no Dictionary, while the newer September 20 dictionary guide documents Android support; treat the latter as current for individual Android editing, and verify the installed app before a mobile workflow. [Bulk-import guide](https://docs.wisprflow.ai/articles/8955301725-How-Do-I-Bulk-Import-Dictionary-Items-and-Snippets), [dictionary guide](https://docs.wisprflow.ai/articles/4052411709-Teach-Flow-your-words-with-the-dictionary).

Snippets expand a spoken trigger into saved text and are suited to deliberate commands, not an ambiguous `contacts` → `context` correction. [Snippet guide](https://docs.wisprflow.ai/articles/5784437944-create-and-use-snippets). Wispr's published MCP connector is a read-only Notetaker meeting-content route; it excludes dictation history and cannot edit dictionary entries. [MCP guide](https://docs.wisprflow.ai/articles/4759919286). The reviewed official guides document no public dictionary API, bulk export, or user-specific voice-model training interface. This is an absence in the reviewed documentation, not proof that none exists privately. The “Improve the model for everyone” privacy control allows Wispr to use audio, transcripts, and edits to improve its models; it does **not** promise a model personalized to one user. Dictation is cloud processed, while consent, cloud storage, and local history are separate controls. [Data controls](https://docs.wisprflow.ai/articles/9609615338-Private-Cloud-Sync-and-Data-Sharing-preferences-in-Wispr-Flow).

Wispr lists Mac, Windows, iOS, and Android; its Linux/WSL guide says there is no native Linux app. This matters for the current Linux desktop: any Wispr integration there needs its own supported route or later custom Listener work, rather than assuming desktop bulk import is locally available. [Supported devices](https://docs.wisprflow.ai/articles/1036674442-Supported-devices-and-system-requirements), [Linux/terminal guide](https://docs.wisprflow.ai/articles/6478598909-using-flow-with-linux-wsl-and-terminal-applications). The older psyche records propose a personalized, possibly self-hosted STT model and a Listener integration; those remain future design directions, distinct from Wispr's documented dictionary and model-improvement setting.

## Sources

- Direct living correction: `flows/6db4fe/vision/speechToText.md`, read 2026-09-21. Earlier psyche direction: `flows/024bc7/vision/speechToText.md`, `flows/6cc91b/vision/transcriptExtraction.md`, `flows/2ef42163/vision/psycheLogging.md`, `flows/019fe121/vision/dictationVocabulary.md`.
- Authored Curriculum skills read-only: `skills/psyche-interraction.md`, `skills/correction.md`, `skills/behavior.md`, `skills/spirit.md`; deployed generated copies and `roles.datom` consulted only to locate current load paths.
- Wispr primary docs: [dictionary](https://docs.wisprflow.ai/articles/4052411709-Teach-Flow-your-words-with-the-dictionary), [bulk import](https://docs.wisprflow.ai/articles/8955301725-How-Do-I-Bulk-Import-Dictionary-Items-and-Snippets), [snippets](https://docs.wisprflow.ai/articles/5784437944-create-and-use-snippets), [MCP](https://docs.wisprflow.ai/articles/4759919286), [data controls](https://docs.wisprflow.ai/articles/9609615338-Private-Cloud-Sync-and-Data-Sharing-preferences-in-Wispr-Flow), [platform support](https://docs.wisprflow.ai/articles/1036674442-Supported-devices-and-system-requirements), [Linux/terminal behavior](https://docs.wisprflow.ai/articles/6478598909-using-flow-with-linux-wsl-and-terminal-applications).
