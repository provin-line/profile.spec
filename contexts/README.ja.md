# contexts/ — provin profile context の SoT

provin profile の JSON-LD context 文書の正規。**byte level で canonical** —
実装は compile 時に byte-exact なコピーを埋め込む（runtime fetch は禁止）。
`@context` 配列は署名スコープ内で byte 列として働くため、実装間の byte 差は
hash を分断する。vendoring 先は sha256 pin テストで drift を止める。

## この文書の位置（Model A）

dPLaaX は 2026-06-11 に所有の二層モデルを確定した（→ dplaax `contexts/README.ja.md`）:

1. **protocol context** — dplaax wire key → IRI の写像。protocol 所有で、profile を
   またいで同一。正規は dplaax `contexts/v1.jsonld`。
2. **profile 拡張 context（本ディレクトリ）** — claim の接地と、profile 所有の
   custom subject field の term。正規は **profile 側**、すなわちここ。protocol term の
   再定義は不可（`@protected` が機械的に阻止する）。

本 repo が存在するまで profile 側に置き場が無かったため、provin.oss
`vc/contexts/provin-v1.jsonld` が既定の canonical を務め、dplaax の README も
そう名指ししていた。**書かれていない spec の代わりに実装が立っていた**状態である。
本ディレクトリは profile が自分の artifact の所有を引き取ったものであり、
provin.oss は今後ここから vendoring する。

## この文書がやること

接地、それだけ: `provin` claim namespace prefix をその vocabulary URL へ写像し、
claim の identity を裸の prefix 文字列ではなく **(接地 URL, label) の対**にする
（→ dplaax `credential.claim.grounding`、本 profile の `claim.namespace`）。
裸の prefix には所有者がいない。接地は署名スコープに乗るので、別の場所に接地した
偽の `provin:` は byte で区別できる。

claim の**値**（`provin:filter` 等）は wire 上の文字列値であり context の対象外 —
protocol context が `transformationClaim` を `@type: "@vocab"` と宣言しているため、
値は JSON-LD 展開時に接地 URL 配下の IRI へ解決される。各 label が**何を主張するか**は
claim registry（`rules/claim.yaml`）の仕事であって、context の仕事ではない。

## Files

| file | URI | sha256 |
|---|---|---|
| `v1.jsonld` | `https://provin.dev/vc/v1` | `35c8066d47eba1c0c284632f3b390fdb525162b45f5629b31457b030e41a9b86` |

- URI `https://provin.dev/vc/v1` は v0 wire の一部として凍結され不変:
  `@context` 配列は署名スコープに bytes として乗るため、差し替えは実装間の
  hash 分断 — 互換変更ではなく next-MAJOR の破壊である。
- 本文書を変更したら上表の sha256 を更新し、vendoring 先（provin.oss
  `vc/contexts/`）へ byte-exact に同期する。両者が一致するまで pin テストが落ちる。
