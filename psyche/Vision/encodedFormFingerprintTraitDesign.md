# "encodedform trait must implement the fingerprint trait"

> so encodedform trait must implement the fingerprint trait. the
> fingerprint trait by default uses the rkyv of that object and gets
> the hash of it. all references use the encodedid of the thing it
> refers to. does that make sense? or is it encodable and
> fingerprintable? are we using nouns or qualifiers for traits? Id
> really like to talk about traits more, how we design them and name
> them, and use them

— psyche, 2026-08-06T21:58:07Z (Designer session 5abf3be8; entry
captured 2026-08-08 from the session transcript during the
rulings-audit backfill)

Context, kept apart from the quote: the identity trait design —
fingerprinting defaults to hashing the RKYV serialization; references
use the encoded identity. The nouns-vs-qualifiers trait-naming thread
opened here; the vocabulary was settled later the same evening (see
letsUseTheSameVocabulary.md: TrueName is the trait, EncodedName
preferred).

*(2026-08-14 annotation, consistency audit: this entire 2026-08-06 entry is in dead vocabulary — encodedform, encodable, and EncodedName all carry code/encoded, which was dropped 2026-08-13 per encodedFormIsTheCode.md 2026-08-13 and traitsAsCapabilities.md 2026-08-13. The nouns-vs-qualifiers question opened here was resolved to qualifiers (traitsAsCapabilities.md 2026-08-13T17:17 "all traits will be qualifiers"), later qualified by verb acceptance (traitsAsCapabilities.md 2026-08-14). EncodedName's successor lineage remains open per traitsAsCapabilities.md 2026-08-13 and encodedFormIsTheCode.md 2026-08-13.)*
