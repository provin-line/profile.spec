# STATUS — 起草の現状（一時文書）

> 本ファイルは作業台帳であり spec の一部ではない。spec 安定後に削除する。
> tools/lint.py の走査対象外（規範語の引用が許される唯一の markdown）。
> (English) This file is the drafting ledger, kept in Japanese only. It is
> temporary — not part of the spec — and will be deleted once the spec
> stabilizes. The spec itself is English-primary.

## 現状宣言（2026-07-16）

- repo 新設。claim registry（7 label + grounding + registry 閉性 + topology
  非依存 = 10 rule / 13 vector）を provin.oss `vc/credential.go` の doc comment
  から転記して規範化した。転記元に無かった内容は追加していない。
- profile context（`contexts/v1.jsonld`）の正規を本 repo へ移管済み
  （Model A。dplaax `contexts/README` と provin.oss `vc/context.go` の双方が
  本 repo を指し、sha256 pin で相互検証する）。
- 実装側 harness は provin.oss `conformance/provinprofile_test.go`。
  vector 13 本の内訳: **駆動 3**（grammar/grounding/topology）、
  **ledgered skip 9**（closure 系 7 = issuer/consumer を縛る規範で library の
  計算対象外、sink-receipt 2 = cmd/standalone の発行者義務）、
  **claim-003 は駆動済み**（registry 閉性の発行時強制、2026-07-16 裁定 →
  同日 provin.oss `vc.New` に実装。同一 fixture で「発行は拒否 / 受信は
  open-world で受理」の両方向を pin）。

## 0.1 タグ条件の充足状況

- [x] 全 rule が `draft` 以上（10/10）
- [x] 各 draft rule に vector ≥ 1（lint の双方向参照で機械検証）
- [x] lint green
- [x] provin.oss が context を本 repo から vendoring（2026-07-16）
- [x] 各 vector が「駆動」または「駆動できない理由の ledger」を持つ
      （claim-003 駆動化で充足、2026-07-16）

**→ 0.1 タグ条件はすべて充足。** タグを切るかは public 化の判断と併せて
maintainer が決める（repo は現状 private）。

## 未着手（dplaax 同等構成との差分）

- `concept.md` / `GLOSSARY.md` / `CONTRIBUTING.md`（+ ja）— profile 単独の
  concept が要るか（README §What the registry says で足りている可能性）は
  public 化の判断と併せて決める。repo は現状 private。
