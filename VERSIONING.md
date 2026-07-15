# Versioning

- Current state: **0.1 (draft)**. No tag is cut yet — see the conditions below.
- **Conditions for the 0.1 tag**: every entry in `rules/` at `draft` or above /
  each `draft` rule carries at least one conformance vector / lint green /
  provin.oss vendoring the profile context from this repository rather than
  standing in as its canonical (met 2026-07-16) / every vector either driven by
  an implementation or carrying a ledgered reason it cannot be.
- **Conditions for 1.0**: the protocol this profile sits on reaches its own 1.0,
  plus a period of real-world validation and the exhaustion of breaking changes
  within 0.x.
- The unit of compatibility is the **`id` of a rule and the meaning of its
  `statement`**. File layout is outside the normative scope (→ README.md).
- Rule deletion and semantic changes are permitted within a minor release in
  0.x. From 1.0 onward they are the sole justification for a major increment.
- Adding vectors is always a minor change or smaller. Changing an existing
  vector's expected value is a semantic change to its rule.

## What a claim's meaning being frozen actually costs

Two things here are already immutable and are not this repository's to relax:

- **The context URI `https://provin.dev/vc/v1`.** It rides the signing scope as
  bytes, so repointing it partitions hashes across implementations. Frozen with
  the v0 wire.
- **A registered label's assertion.** Credentials already signed under
  `provin:filter` cannot be re-issued to mean something else, and a verifier
  reading a two-year-old chain applies today's registry to yesterday's bytes.
  Narrowing or widening what a label warrants is therefore a MAJOR change even
  though no byte of the wire moves — the bytes did not change, the truth
  conditions did.

Adding a label is a minor change: an older verifier meets it and stays
open-world (dplaax `credential.claim.open-world-accept`), which is safe by
default rather than by upgrade. Retiring one is not — the credentials outlive
the decision.
