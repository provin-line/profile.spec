# provin wire profile (draft)

The normative spec for the **`provin` wire profile** of the
[dPLaaX protocol](https://github.com/dplaax/spec).

dPLaaX records, at every boundary data crosses, who received what, did what, and
passed on what — so the chain can be verified by a third party. It pins the
credential wire, the canonicalization, the signature suites, the chain rules,
and the identity model. It deliberately stops short of one thing: dplaax
`credential.claim.grammar` fixes the claim's grammar — one `<namespace>:<label>`
token — and then says in as many words that dplaax does not define claim
semantics, and that pinning meaning (closed/open world, content relationship) is
the profile's job.

This repository is that job. It says what `provin:filter` and its six siblings
**assert**, which is the one thing a verifier cannot work out from the wire: the
shape of a credential is visible in its parameters, but what the issuer warrants
about where the output's information came from is not.

Why it has to be written down somewhere other than code: the implementation
knows the labels and, by design, not their meaning — its claim check is
"structural, requiring no profile knowledge". A constant named `ClaimFilter` tells
a reader the string, not what asserting it commits the issuer to. The v0 wire is
frozen and crosses organizational boundaries; an auditor holding
`"transformationClaim":"provin:filter"` needs a document, and this is it.

> **Status: v0.1 (draft).** All rules are `draft` and will evolve on
> implementation feedback (→ [VERSIONING.md](VERSIONING.md)).

## Normative scope

**The source of truth is exactly these three artifacts**; prose is
non-normative.

| artifact | normative scope | format |
| --- | --- | --- |
| `rules/` | the claim registry: what each label asserts | YAML |
| `vectors/` | materialization of those norms (conformance vectors) | JSON |
| `contexts/` | the profile context document, canonical at the byte level | JSON-LD |

There is no `schemas/` here, and its absence is the point: this profile defines
no wire shape. The shape of a credential is dPLaaX's, and every rule below sits
inside it. What a profile owns is meaning.

All markdown (this document included) is non-normative and references rule ids
rather than restating them — mechanically enforced by `tools/lint.py`.

## What the registry says

Each label pins whether the claim is **closed** — the declared conformant inputs
are the output's complete information source, so absence from the declared set
licenses an exclusion inference — or acknowledges information beyond them. That
distinction is the whole product: "this lot cannot be in that output" is only
answerable because someone warranted the set was complete.

| label | closure | rule |
| --- | --- | --- |
| `provin:filter` | closed | `claim.filter` |
| `provin:convert` | closed | `claim.convert` |
| `provin:filter-convert` | closed | `claim.filter-convert` |
| `provin:aggregate` | closed fold | `claim.aggregate` |
| `provin:enrich` | conformant-closed | `claim.enrich` |
| `provin:generate` | open | `claim.generate` |
| `provin:sink-receipt` | identity (not a transformation) | `claim.sink-receipt` |

Two of those rows carry most of the weight. `provin:enrich` and
`provin:aggregate` have the **same N:1 shape** and different warranties: an
enrich joins side-fetched data no chain covers, so exclusion inferences hold for
conformant flows only. `provin:generate` looks like an aggregate too, and is
open: the dominant source is the model's weights, hence its training corpus, and
declaring a synthesis as `provin:aggregate` would falsely license a closed-world
reading of an output nothing closed over. The shape cannot tell these apart. The
claim is what does.

## Reading order

1. [rules/claim.yaml](rules/claim.yaml) — the normative body
2. [vectors/](vectors/) — the conformance vectors
3. [contexts/README.md](contexts/README.md) — the grounding document and its ownership
4. [STATUS.md](STATUS.md) — current drafting state (temporary; removed when stable)

## rule catalog format

Mirrors dPLaaX's, so a reader moves between the two without relearning:

| field | convention |
| --- | --- |
| `id` | `<domain>.<topic>[.<name>]`, frozen on promotion to `draft` |
| `status` | `todo` / `draft` / `stable` |
| `class` | `core` / `audit-reachable` |
| `statement` | the normative statement; ≤256 chars; ≥1 RFC 2119 keyword. One rule, one expression |
| `uses` | rule ids this depends on — cross-reference instead of repeating |
| `vectors` | the vectors that materialize it (bidirectional; lint enforces) |
| `notes` | non-normative. RFC 2119 keywords here fail the lint |

Rule ids in `uses` may name dPLaaX rules (`credential.claim.grammar`); the lint
resolves only this repository's, so cross-protocol references live in `notes`.

## Relationship to the implementation

[provin.oss](https://github.com/provin-line/oss) is the reference
implementation. It vendors `contexts/v1.jsonld` byte-exact and pins its sha256:
the `@context` array rides the signing scope, so a divergence would partition
hashes across implementations rather than fail loudly.

The dependency points one way. This profile does not describe provin.oss's
behavior, and provin.oss is not where the profile's meaning is decided — that
arrangement is what this repository exists to end.
