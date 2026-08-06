# Governance

Who decides what a claim label asserts, and how that can change. Complements
[VERSIONING.md](VERSIONING.md); the org-level maintainer model, succession
terms, and IPR match the
[dPLaaX spec's GOVERNANCE](https://github.com/dplaax/spec/blob/main/GOVERNANCE.md).

## Maintainer

[1o1 Co. Ltd.](https://1o1.co.jp/) — a single maintainer today; decisions are
made in public Issues. The dPLaaX spec's six-month succession and
fork-friendliness terms apply here unchanged.

## Changing the claim registry

The registry (`rules/` + `vectors/` + `contexts/`) is the profile's whole
product; its governance is stricter than any prose:

- **Adding a label** — a public proposal issue that states the label's closure
  semantics (closed / closed fold / conformant-closed / open / identity) and
  the issuer warranty it encodes. It lands only together with its rule YAML
  and conformance vectors in the same change.
- **Changing what an existing label asserts** — a semantic change to a label
  already on the wire retroactively changes what issued credentials mean. It
  is treated as breaking per [VERSIONING.md](VERSIONING.md) and requires a
  public proposal issue with explicit maintainer approval recorded on it.
  Where the old meaning must survive, minting a NEW label is preferred over
  mutating an existing one.
- **Retiring a label** — labels are never deleted from the registry; they are
  marked deprecated, so historical credentials remain interpretable.
- **Context document** — `contexts/` is canonical at the byte level and
  sha256-pinned by consumers; any change ships as a new version, never as an
  in-place edit.

## draft → stable

Same criterion as the dPLaaX spec: a rule is promoted when its conformance
vectors are passed by two independent implementations.
