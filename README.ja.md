# provin wire profile (draft)

**`provin` wire profile** の normative spec。
[dPLaaX プロトコル](https://github.com/dplaax/spec_draft) の profile である。

dPLaaX は、データが境界を越えるたびに「誰が何を受け取り、何を行い、何を渡したか」を
記録し、その連なりを第三者が確かめられるようにする。credential の wire、
canonicalization、署名 suite、chain 規則、identity model — そのすべてを pin する。
そして 1 点だけ、意図的に手前で止まる: dplaax `credential.claim.grammar` は claim の
文法（`<namespace>:<label>` 1 token）を固定したうえで、**dplaax は claim の意味論を
定義せず、意味（closed/open world、内容関係）の pin は profile の仕事である**と明言している。

本 repo がその仕事である。`provin:filter` とその 6 つの兄弟が**何を主張するのか**を書く。
それは verifier が wire から導けない唯一のものだ — credential の**形**は wire
parameter に見えているが、出力の情報がどこから来たのかについて発行者が**何を保証したか**は
見えていない。

なぜコード以外の場所に書く必要があるのか: 実装は label を知っているが、**設計として
意味を知らない**（claim 検査は「構造的で、profile 知識を要さない」と実装自身が書いている）。
`ClaimFilter` という定数名は読み手に文字列を教えるだけで、それを主張することが発行者に
何を約束させるのかを語らない。v0 wire は凍結済みで組織境界を越える。
`"transformationClaim":"provin:filter"` を受け取った監査人には文書が要る。これがそれだ。

> **Status: v0.1 (draft)。** すべての rule は `draft` であり、実装からの
> フィードバックで変わり続ける（→ [VERSIONING.ja.md](VERSIONING.ja.md)）。

## 規範の範囲

**規範の SoT は次の 3 artifact のみ**であり、散文は規範を持たない。

| artifact | 規範の範囲 | 形式 |
| --- | --- | --- |
| `rules/` | claim registry: 各 label が何を主張するか | YAML |
| `vectors/` | その規範の materialization（conformance vector） | JSON |
| `contexts/` | profile context 文書、byte level で canonical | JSON-LD |

`schemas/` は**無い。それが要点である**: この profile は wire shape を定義しない。
credential の形は dPLaaX のものであり、下記のすべての rule はその形の**中**に座る。
profile が所有するのは意味である。

markdown（本文書を含む）はすべて non-normative で、規範を再表現せず rule id を参照する
（`tools/lint.py` が機械的に強制する）。

## registry が言っていること

各 label は **closed** — 宣言された conformant 入力が出力の情報源の全部であり、宣言集合に
無いことが除外推論を許す — か、それを超える情報の存在を認めるか、を pin する。
この区別が製品そのものだ:「このロットはその出力に入り得ない」が答えられるのは、
誰かが「集合は完全だ」と保証したからに他ならない。

| label | closure | rule |
| --- | --- | --- |
| `provin:filter` | closed | `claim.filter` |
| `provin:convert` | closed | `claim.convert` |
| `provin:filter-convert` | closed | `claim.filter-convert` |
| `provin:aggregate` | closed fold | `claim.aggregate` |
| `provin:enrich` | conformant-closed | `claim.enrich` |
| `provin:generate` | open | `claim.generate` |
| `provin:sink-receipt` | identity（変換ではない） | `claim.sink-receipt` |

重みの大半はこの表の 2 行が担っている。`provin:enrich` と `provin:aggregate` は
**N:1 の形が同一で、保証が違う**: enrich はどの chain も覆わない side-fetch データを
join するので、除外推論は conformant flow に限って成立する。`provin:generate` も
aggregate に見えるが open だ — 支配的情報源はモデルの重み、すなわちその学習コーパスであり、
synthesis を `provin:aggregate` と名乗ることは、何も閉じていない出力に closed-world の
読みを許すことになる。**形はこれらを区別できない。claim が区別する。**

## 読む順番

1. [rules/claim.yaml](rules/claim.yaml) — 規範本体
2. [vectors/](vectors/) — conformance vector
3. [contexts/README.ja.md](contexts/README.ja.md) — grounding 文書とその所有
4. [STATUS.md](STATUS.md) — 起草の現状（一時文書、安定後に削除）

## rule catalog 形式

dPLaaX に合わせてある。両者を行き来する読み手が学び直さずに済むように:

| field | 規約 |
| --- | --- |
| `id` | `<domain>.<topic>[.<name>]`。`draft` 昇格で凍結 |
| `status` | `todo` / `draft` / `stable` |
| `class` | `core` / `audit-reachable` |
| `statement` | 規範文。256 文字以内。RFC 2119 規範語を 1 つ以上含む。1 rule 1 表現 |
| `uses` | 依存する rule id。繰り返さず相互参照する |
| `vectors` | それを materialize する vector（双方向。lint が強制） |
| `notes` | non-normative。ここに規範語があると lint が落ちる |

`uses` の rule id は dPLaaX の rule（`credential.claim.grammar` 等）を指し得るが、
lint が解決するのは本 repo のもののみ。プロトコル横断の参照は `notes` に置く。

## 実装との関係

[provin.oss](https://github.com/provin-line/oss) が reference implementation。
`contexts/v1.jsonld` を byte-exact に vendoring し sha256 を pin する:
`@context` 配列は署名スコープに乗るため、drift は「失敗」ではなく
**実装間の hash 分断**になるからだ。

依存は一方向である。本 profile は provin.oss の挙動を記述しないし、provin.oss は
profile の意味が決まる場所ではない — **その状態を終わらせるために本 repo は存在する**。
