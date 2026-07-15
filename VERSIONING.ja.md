# Versioning

- 現状: **0.1 (draft)**。タグはまだ切っていない（条件は下記）。
- **0.1 タグの条件**: `rules/` の全 entry が `draft` 以上 / 各 `draft` rule が
  conformance vector を 1 本以上持つ / lint green / provin.oss が profile context を
  本 repo から vendoring している（実装が canonical の代役を降りている）こと。
- **1.0 の条件**: 土台のプロトコルが 1.0 に達し、実運用での検証期間を経て、
  0.x 内で breaking を出し尽くしたあと。
- 互換性の単位は **rule の `id` と `statement` の意味**。ファイル配置は規範の
  範囲外（→ README.ja.md）。
- 0.x では rule の削除と意味変更を minor 内で許す。1.0 以降はそれらが major を
  上げる唯一の正当理由になる。
- vector の追加は常に minor 以下。既存 vector の期待値変更は、その rule の意味変更として扱う。

## 「claim の意味が凍る」の実際のコスト

ここには既に不変なものが 2 つあり、本 repo が緩められるものではない。

- **context URI `https://provin.dev/vc/v1`**。署名スコープに bytes として乗るため、
  差し替えは実装間の hash 分断になる。v0 wire と共に凍結。
- **登録済み label の主張**。`provin:filter` で既に署名された credential を別の意味へ
  再発行することはできず、2 年前の chain を読む verifier は**今日の registry を
  昨日の bytes に適用する**。したがって label が保証する内容の拡大・縮小は、
  wire のバイトが 1 つも動かなくても MAJOR である — 変わったのは bytes ではなく
  真理条件だからだ。

label の**追加**は minor: 旧 verifier はそれに出会っても open-world のまま
（dplaax `credential.claim.open-world-accept`）であり、アップグレードではなく
default で安全である。**撤回**はそうではない — credential は決定より長く生きる。
