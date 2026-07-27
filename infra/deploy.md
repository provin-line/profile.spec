# Deployment — provin.dev wire surface (S3 + CloudFront)

`provin.dev` serves one **machine-readable wire identifier**: the JSON-LD
context at `/vc/v1`. (provin's JSON Schemas are served from `dplaax.dev`, not
here.) This is a different surface from the landing page at `www.provin.dev`
(that lives in `provin-line/site`). **Nothing here runs automatically** —
`.github/workflows/deploy.yml` ships disabled; this documents the target.

## Why S3 + CloudFront (not Pages)

`/vc/v1` is extensionless and frozen. GitHub Pages would serve it as
`application/octet-stream` with no way to override the header. S3 object
metadata serves it as `application/ld+json`.

## Prior state this replaced (migrated 2026-07-24)

Before the migration, `provin.dev` (apex) was aliased to the **same**
CloudFront distribution and S3 bucket (`www.provin.dev`) as the landing page —
and that bucket is deployed with `aws s3 sync ./dist --delete`, so placing
`/vc/v1` in the shared bucket would have let the next LP deploy delete it.
This surface fixed that by giving the wire its **own** bucket + distribution,
physically separated from the LP (the topology below is the live state).

## Topology

```text
Route 53                 CloudFront                     S3
─────────                ──────────                     ──
provin.dev  ──ALIAS──▶ Distribution  ──OAC──▶  s3://wire.provin.dev
                          (private bucket, versioning on)

www.provin.dev  ──ALIAS──▶ (separate LP distribution)  ──▶  s3://www.provin.dev
```

## S3 bucket

- Name: `wire.provin.dev`
- Public access: **blocked** (CloudFront via OAC)
- Static website hosting: **off**
- Versioning: **on**
- Holds only the assembled wire tree.

## Served object layout

| path (URI) | S3 key       | Content-Type          |
| ---------- | ------------ | --------------------- |
| `/vc/v1`   | `vc/v1`      | `application/ld+json` |
| `/` (root) | `index.html` | `text/html`           |
| 404        | `404.html`   | `text/html`           |

`/vc/v1` is stored as an extensionless object; the deploy sets its
`Content-Type` explicitly (S3 would otherwise guess `application/octet-stream`).

## CloudFront distribution

- Origin: `wire.provin.dev` via Origin Access Control (OAC)
- Default root object: `index.html`
- Custom error responses: `403`/`404` → `/404.html` (return HTTP 404)
- Compress objects: on; HTTP/2 + HTTP/3
- TLS: ACM certificate in `us-east-1` for `provin.dev`
- Alternate domain name (CNAME): `provin.dev`

## Bring-up

1. Provision the bucket and distribution above — but **without** the
   `provin.dev` alternate domain name at first. The alias is currently attached
   to the LP distribution, and CloudFront enforces global uniqueness of
   alternate domain names, so creating the new distribution with it fails with
   `CNAMEAlreadyExists`. Attach the ACM cert from the start — it is what makes
   the later alias association valid.
2. Run the deploy and verify on the distribution domain (`d….cloudfront.net`)
   **before** touching the alias or DNS: byte-exact `/vc/v1` (sha256
   `35c8066…`) **and** `Content-Type: application/ld+json`.
3. Move the apex alias from the LP distribution to this one:
   `aws cloudfront associate-alias --target-distribution-id <WIRE_DIST_ID>
   --alias provin.dev` (same-account move). If that path is unavailable, remove
   `provin.dev` from the LP distribution's aliases, wait for it to deploy, then
   add it here — accepting a brief window where the apex answers with the
   CloudFront no-such-alias 403.
4. Repoint the `provin.dev` Route 53 alias record at this distribution.
5. Re-verify against `https://provin.dev/vc/v1`.

## Manual deploy fallback

```bash
# from the repo root, with AWS creds for the wire account.
# fail fast: a partial assembly must never reach a --delete sync of the live
# bucket, and drift must never pass under the frozen URI.
set -euo pipefail

rm -rf _site && mkdir -p _site/vc
cp site/index.html _site/index.html
cp site/404.html   _site/404.html
cp contexts/v1.jsonld _site/vc/v1

# the same recorded-sha256 guard the workflow enforces
expected=$(grep -oE '[0-9a-f]{64}' contexts/README.md | head -1)
[ "$(shasum -a 256 _site/vc/v1 | cut -d' ' -f1)" = "$expected" ] \
  || { echo "vc/v1 drifted from the recorded sha256"; exit 1; }

# the extensionless context key is excluded from the sync and uploaded once
# with the right type (same rationale as the workflow: no octet-stream window)
aws s3 sync _site/ s3://wire.provin.dev/ --delete --exclude "vc/v1"
aws s3 cp _site/vc/v1 s3://wire.provin.dev/vc/v1 --content-type application/ld+json
aws cloudfront create-invalidation --distribution-id <DIST_ID> --paths "/*"
```

## CI deployment

`.github/workflows/deploy.yml` ships disabled (`if: false`). The bucket and the
distribution already exist and serve — publishing happens through the manual
fallback above. What is missing is only the trust path from the workflow to
them. To enable:

1. Create an AWS IAM role trusted by GitHub OIDC
   (`token.actions.githubusercontent.com`) with S3 sync + CloudFront
   `create-invalidation` permissions on **this** bucket / distribution only.

   Scope the **trust policy** as tightly as the permissions, on `sub`:

   ```json
   "StringEquals": {
     "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
     "token.actions.githubusercontent.com:sub":
       "repo:provin-line/profile.spec:ref:refs/heads/main"
   }
   ```

   Two things this pins that a looser policy does not. `repo:provin-line/*`
   would let **any** repository in the organisation assume the role and rewrite
   a frozen wire URI. And without the `ref:` component, a pull request from a
   fork — or any branch — could assume it; the workflow's own `branches: [main]`
   trigger is not an authorization boundary, it is a scheduling one.

2. Add repo secrets: `AWS_ROLE_TO_ASSUME`, `AWS_REGION`, `S3_BUCKET`
   (`wire.provin.dev`), `CLOUDFRONT_DISTRIBUTION_ID`. None are set today.
3. Change `if: false` to `if: github.ref == 'refs/heads/main'`.

> **Historical note.** Until 2026-07-27 this repository's default branch was
> `develop` and no `main` existed, while `deploy.yml` triggered on
> `branches: [main]` and the steps above named `main` throughout. Enabling it
> then would have produced a workflow that never fired — worse than a disabled
> one, because it looks enabled. The rename to `main` (all four public
> repositories now share the trunk name) removed that trap.
