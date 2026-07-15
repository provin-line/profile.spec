# contexts/ — source of truth for the provin profile context

The canonical document for the provin profile's JSON-LD context. **Canonical at
the byte level** — implementations embed a byte-exact copy at compile time
(runtime fetching is prohibited). The `@context` array operates as a byte
sequence within the signature scope, so byte differences between implementations
partition hashes. Vendoring targets prevent drift with sha256 pinning tests.

## Where this sits (Model A)

dPLaaX finalized a two-layer ownership model on 2026-06-11 (→ dplaax
`contexts/README.md`):

1. **Protocol context** — the dplaax wire keys → IRIs. Owned by the protocol,
   identical across profiles, canonical in dplaax `contexts/v1.jsonld`.
2. **Profile extension context (this directory)** — claim grounding, and terms
   for any profile-owned custom subject fields. Canonical **on the profile's
   side**, which is here. Redefining protocol terms is not permitted
   (`@protected` enforces it mechanically).

Until this repository existed the profile context had no home on the profile
side, so provin.oss `vc/contexts/provin-v1.jsonld` served as the canonical by
default and dplaax's README named it as such. That was the implementation
standing in for a missing spec; this directory is the profile taking ownership
of its own artifact, and provin.oss now vendors from here.

## What this document does

Grounding, and only grounding: it maps the `provin` claim namespace prefix to
its vocabulary URL, which makes claim identity the **(grounding URL, label)**
pair rather than the bare prefix string (→ dplaax `credential.claim.grounding`,
this profile's `claim.namespace`). A bare prefix has no owner; the grounding
rides the signing scope, so an impostor `provin:` grounded elsewhere is
byte-distinguishable.

Claim VALUES (`provin:filter` and the rest) are string values on the wire and
are outside the context's scope — `transformationClaim` is declared
`@type: "@vocab"` by the protocol context, so a value resolves to an IRI under
the grounding URL on JSON-LD expansion. What each label ASSERTS is the claim
registry's job (`rules/claim.yaml`), not the context's.

## Files

| file | URI | sha256 |
|---|---|---|
| `v1.jsonld` | `https://provin.dev/vc/v1` | `35c8066d47eba1c0c284632f3b390fdb525162b45f5629b31457b030e41a9b86` |

- The URI `https://provin.dev/vc/v1` is frozen as part of the v0 wire and is
  immutable: the `@context` array rides the signing scope as bytes, so
  repointing it would partition hashes across implementations — a next-MAJOR
  break, not a compatible change.
- After modifying this document, update the sha256 above and synchronize the
  change byte-exact to the vendoring target (provin.oss `vc/contexts/`), whose
  pinning test fails until both agree.
