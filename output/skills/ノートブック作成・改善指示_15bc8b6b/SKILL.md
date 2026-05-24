---
name: ノートブック作成・改善指示
skill_id: 15bc8b6b-e2ef-4a2d-b66a-e7d76925bc1c
version: 1.0.0
category: ノートブック作成指示
status: public
source_count: 11
unique_user_count: 5
variables:
- notebook_ids
- action
- additional_guidelines
triggers:
- notebook作って
- ノートブック修正して
- notebookのエラー直して
- notebookに解説追加して
- notebook比較して
---

# ノートブック作成・改善指示

**説明**: ノートブックの作成、修正、比較、解説追加を指示するスキル
**ステータス**: ✅ 公開中 | **ソース数**: 11 件 | **ユニークユーザー**: 5 人 | **カテゴリ**: ノートブック作成指示

---

## テンプレートプロンプト

```
{notebook_ids}について、{action}して下さい。{additional_guidelines}
```

## 変数一覧

- `{{notebook_ids}}`: 対象のノートブック番号または範囲（例: notebook30-32, notebook16と17）
- `{{action}}`: 実行してほしい作業内容（例: 実装、修正、比較して論じるセクション追加、説明を詳しくする）
- `{{additional_guidelines}}`: 追加の条件や注意点（例: notebook guidelinesに沿う、浮動小数点の丸め誤差について詳しく説明）

## 活用シーン

- 新しいノートブックを連番で作成してほしいとき
- 既存のノートブックのエラー修正を依頼するとき
- ノートブック間の比較や解説の追加を依頼するとき

## トリガーフレーズ

- `notebook作って`
- `ノートブック修正して`
- `notebookのエラー直して`
- `notebookに解説追加して`
- `notebook比較して`

---

## 具体インスタンス

### インスタンス 1: ノートブック実装指示

> 元プロンプト: *指定されたカリキュラムに沿って、notebook30-32を実装して下さい　notebookのガイドラインに沿うように作成して下さい*

**変数の値**
  - `notebook_ids`: notebook30-32
  - `action`: 指定されたカリキュラムに沿って実装
  - `additional_guidelines`: notebookのガイドラインに沿うように作成して下さい

**実際のプロンプト**
```
{notebook_ids}について、{action}して下さい。{additional_guidelines}
```

---

### インスタンス 2: ノートブックエラー修正

> 元プロンプト: *notebook39が実行途中でエラーになっているので修正して*

**変数の値**
  - `notebook_ids`: notebook39
  - `action`: 実行途中でエラーになっているので修正
  - `additional_guidelines`: 

**実際のプロンプト**
```
{notebook_ids}について、{action}して下さい。
```

---

### インスタンス 3: ノートブック比較・解説追加

> 元プロンプト: *notebook16と17の結果を比べて、17の方でどういう操作が違ったのか、どこでどういう改善があったかなど比較して論じるセクションを１７の末尾に加えてくれますか*

**変数の値**
  - `notebook_ids`: notebook16と17
  - `action`: 結果を比べて、後者の方でどういう操作が違ったのか、どこでどういう改善があったかなど比較して論じるセクションを後者の末尾に追加
  - `additional_guidelines`: 

**実際のプロンプト**
```
{notebook_ids}の結果を比べて、{action}して下さい。
```
