# Changelog

All notable changes to this repository are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-07-27

The draft line, tagged. `VERSIONING.md` lists five conditions for this tag and
`STATUS.md` recorded the last of them met on 2026-07-16, leaving one thing
open: *"タグを切るかは public 化の判断と併せて maintainer が決める"* — whether to
cut it was tied to the decision to publish. The repository went public on
2026-07-27, so this is that decision arriving, not a new one.

Re-verified at the cut rather than trusted from the ledger: 10 rules all at
`draft`, every rule carrying at least one of the 13 vectors, and `tools/lint.py`
green (`OK — 10 rules (0 todo)`).

`draft` is the status of every rule here and the tag does not change that. What
the tag fixes is the pair `VERSIONING.md` names as the unit of compatibility —
**a rule's `id` and the meaning of its `statement`** — at a citable point, so a
credential issued today can be read against the registry it was issued under.
Within `0.x`, rule deletion and semantic change remain permitted in a minor
release.

### Added — the profile's first normative body

The `provin` wire profile had no spec. dPLaaX delegates claim semantics to the
profile in a normative statement (`credential.claim.grammar`: "dplaax does not
define claim semantics — pinning meaning is the profile's job"), and the
delegation landed nowhere: the seven labels were defined by Go constants in
provin.oss, whose own claim check is documented as "structural, requiring no
profile knowledge". Meaning had no home, in a frozen wire that crosses
organizational boundaries.

- `rules/claim.yaml` — the claim registry, transcribed from the definitions that
  had accumulated as doc comments on `vc.TransformationClaim`: the closed labels
  (`filter`, `convert`, `filter-convert`, `aggregate`), the conformant-closed
  `enrich`, the open `generate`, and the `sink-receipt` identity. Plus the
  grounding requirement, the issuance-closed registry, and the independence of
  claims from chain topology.
- `vectors/claim-001..013` — the norms materialized, including the pair that
  motivates the registry existing at all: `aggregate` and `generate` have the
  same N:1 shape and opposite closure.
- `contexts/v1.jsonld` — the profile context, now canonical here. Model A always
  said the profile context's source of truth "lives with the profile"; with no
  profile repository, provin.oss's copy stood in, and dplaax's README named it as
  such. This repository takes that ownership back.
- `tools/lint.py` — dPLaaX's, unchanged: RFC 2119 keywords stay out of `notes`,
  ids stay unique, rule↔vector references stay bidirectional.

### Not here, deliberately

No `schemas/`. This profile defines no wire shape — the shape is dPLaaX's, and a
profile owns meaning. The one shape-adjacent rule (`claim.sink-receipt`'s
identity: `previousCredential` = the consumed credential, `inputHash` ==
`outputHash`) is a cross-field equality no JSON Schema expresses, and it is an
issuer obligation rather than a wire-form check.

[Unreleased]: https://github.com/provin-line/profile.spec/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/provin-line/profile.spec/releases/tag/v0.1.0
