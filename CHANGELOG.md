# Changelog

All notable changes to this repository are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
